#!/usr/bin/env python3
"""Read-only artwork sampling and pixel-scope checks. Requires Pillow and NumPy."""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image


def load_image(path):
    with Image.open(path) as image:
        if image.mode not in {"RGB", "RGBA", "L", "LA", "P"}:
            raise ValueError("Convert a copy to 8-bit RGB/RGBA before comparing.")
        return np.array(image.convert("RGBA"))


def identity(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def roi_value(text):
    try:
        values = tuple(int(value) for value in text.split(","))
        if len(values) != 4:
            raise ValueError()
        x, y, width, height = values
        if x < 0 or y < 0 or width <= 0 or height <= 0:
            raise ValueError()
        return values
    except ValueError as error:
        raise argparse.ArgumentTypeError("ROI must be x,y,width,height with positive size") from error


def sample(args):
    pixels = load_image(args.image)
    height, width = pixels.shape[:2]
    samples = []
    for x, y, w, h in args.roi:
        if x + w > width or y + h > height:
            raise ValueError("ROI lies outside the image; coordinates are not silently clipped.")
        region = pixels[y:y+h, x:x+w]
        opaque = region[:, :, 3] == 255
        rgb = region[:, :, :3].astype(np.float64)
        selected = rgb[opaque]
        if not selected.size:
            raise ValueError("ROI contains no fully opaque pixels for reliable RGB sampling.")
        mean, median = selected.mean(axis=0), np.median(selected, axis=0)
        median_hex = "#" + "".join(f"{int(round(channel)):02X}" for channel in median)
        # Local five-point residual is a texture/noise proxy, not a perceptual score.
        residual_std = None
        if w >= 3 and h >= 3 and opaque.all():
            local_mean = (rgb[1:-1, 1:-1] + rgb[:-2, 1:-1] + rgb[2:, 1:-1]
                          + rgb[1:-1, :-2] + rgb[1:-1, 2:]) / 5
            residual_std = float((rgb[1:-1, 1:-1] - local_mean).std())
        samples.append({"roi_xywh": [x, y, w, h], "opaque_pixels": int(opaque.sum()),
                        "rgb_mean": mean.tolist(), "rgb_median": median.tolist(),
                        "hex_from_median": median_hex, "rgb_std": selected.std(axis=0).tolist(),
                        "local_residual_std": residual_std})
    return {"operation": "sample", "image": identity(args.image),
            "size": [width, height], "samples": samples,
            "limitations": "Encoded RGB, no ICC transform. ROI statistics do not establish full-image noise or material identity."}


def compare(args):
    before, after = load_image(args.before), load_image(args.after)
    report = {"operation": "compare", "before": identity(args.before),
              "after": identity(args.after), "same_dimensions": before.shape == after.shape,
              "before_size": [before.shape[1], before.shape[0]],
              "after_size": [after.shape[1], after.shape[0]]}
    if before.shape != after.shape:
        report["scope_check"] = "failed_dimension_mismatch"
        return report, False
    delta = np.abs(after.astype(np.int16) - before.astype(np.int16))
    changed = np.any(delta != 0, axis=2)
    report.update(changed_pixels=int(changed.sum()),
                  max_rgba_delta=delta.max(axis=(0, 1)).tolist(),
                  alpha_changed_pixels=int((delta[:, :, 3] != 0).sum()))
    success = True
    if args.editable_mask:
        with Image.open(args.editable_mask) as image:
            if image.size != (before.shape[1], before.shape[0]):
                raise ValueError("Mask and artwork dimensions differ; masks are never resized.")
            if image.mode not in {"L", "1"}:
                raise ValueError("Use a grayscale L/1 mask: white editable, black protected.")
            allowed = np.array(image.convert("L")) != 0
        outside = ~allowed
        outside_changes = int((changed & outside).sum())
        success = outside_changes == 0
        report.update(editable_mask=identity(args.editable_mask),
                      editable_pixels=int(allowed.sum()), protected_pixels=int(outside.sum()),
                      changed_outside_mask=outside_changes,
                      max_protected_delta=int(delta[outside].max()) if outside.any() else None,
                      scope_check="passed" if success else "failed_outside_changes")
        if not outside.any():
            report["scope_check"] = "inconclusive_no_protected_pixels"
            success = False
    else:
        report["scope_check"] = "not_checked_no_mask"
    report["limitations"] = "Pixel scope only; equal dimensions and protected pixels do not prove unchanged geometry inside the editable region. Alpha is reported separately."
    return report, success


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    sampling = commands.add_parser("sample")
    sampling.add_argument("image", type=Path)
    sampling.add_argument("--roi", type=roi_value, required=True, action="append")
    comparison = commands.add_parser("compare")
    comparison.add_argument("before", type=Path)
    comparison.add_argument("after", type=Path)
    comparison.add_argument("--editable-mask", type=Path)
    for command in (sampling, comparison):
        command.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Output exists; choose a new report path.")
    try:
        report, success = (sample(args), True) if args.command == "sample" else compare(args)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps({"report": str(args.output.resolve()), "checks_passed": success}, ensure_ascii=False))
    return 0 if success else 2


if __name__ == "__main__":
    raise SystemExit(main())
