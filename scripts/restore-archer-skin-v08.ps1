[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$InputPath,
    [Parameter(Mandatory = $true)][string]$ReferencePath,
    [Parameter(Mandatory = $true)][string]$OutputPath,
    [Parameter(Mandatory = $true)][string]$MaskPath
)

$ErrorActionPreference = 'Stop'
if ((Test-Path -LiteralPath $OutputPath) -or (Test-Path -LiteralPath $MaskPath)) {
    throw 'Use new paths for the output image and mask.'
}

Add-Type -AssemblyName System.Drawing
Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @'
using System;
using System.Drawing;
using System.Drawing.Imaging;

public static class ArcherSkinV08 {
    static double Smooth(double value) {
        double t = Math.Max(0, Math.Min(1, value));
        return t * t * (3 - 2 * t);
    }

    static int Median(Bitmap source, int[,] rectangles, int channel) {
        int[] histogram = new int[256];
        int count = 0;
        for (int row = 0; row < rectangles.GetLength(0); row++) {
            int x = rectangles[row, 0], y = rectangles[row, 1];
            int width = rectangles[row, 2], height = rectangles[row, 3];
            for (int py = y; py < y + height; py++) {
                for (int px = x; px < x + width; px++) {
                    Color color = source.GetPixel(px, py);
                    histogram[channel == 0 ? color.G : color.B]++;
                    count++;
                }
            }
        }
        int cumulative = 0;
        for (int value = 0; value < histogram.Length; value++) {
            cumulative += histogram[value];
            if (cumulative > count / 2) return value;
        }
        throw new InvalidOperationException("The skin sample is empty.");
    }

    static double NearFeature(int x, int y, double cx, double cy, double rx, double ry) {
        double dx = (x - cx) / rx;
        double dy = (y - cy) / ry;
        double distance = Math.Sqrt(dx * dx + dy * dy);
        return 1 - Smooth((distance - 0.80) / 0.28);
    }

    static double FaceDetailWeight(int x, int y, Color color) {
        if (y >= 358 || color.G >= 224) return 1;
        double eyes = Math.Max(NearFeature(x, y, 477, 304, 24, 18), NearFeature(x, y, 544, 304, 24, 18));
        double brows = Math.Max(NearFeature(x, y, 474, 269, 22, 5), NearFeature(x, y, 547, 269, 22, 5));
        double mouth = NearFeature(x, y, 511, 346, 10, 5);
        double protection = Math.Max(eyes, Math.Max(brows, mouth));
        return 1 - protection * (1 - Smooth((color.G - 190) / 34.0));
    }

    public static int[] Run(string input, string reference, string outputPath, string maskPath) {
        using (var source = new Bitmap(input))
        using (var palette = new Bitmap(reference))
        using (var output = source.Clone(new Rectangle(0, 0, source.Width, source.Height), PixelFormat.Format32bppArgb))
        using (var mask = new Bitmap(source.Width, source.Height, PixelFormat.Format24bppRgb)) {
            if (source.Width != 1024 || source.Height != 1536 || source.Size != palette.Size)
                throw new InvalidOperationException("Requires the 1024x1536 v07 and v06 sheets.");
            using (var graphics = Graphics.FromImage(mask)) graphics.Clear(Color.Black);

            int[,] sourceScalp = {{497, 228, 28, 14}};
            int[,] referenceScalp = {{504, 207, 14, 18}};
            int[,] sourceLimbs = {{410,480,10,16},{371,620,10,16},{456,839,12,16},{450,1176,10,16},{448,1346,10,14}};
            int[,] referenceLimbs = {{415,471,10,16},{358,650,10,16},{455,820,12,16},{448,1190,10,16},{447,1345,10,14}};
            int scalpGreen = Median(palette, referenceScalp, 0) - Median(source, sourceScalp, 0);
            int scalpBlue = Median(palette, referenceScalp, 1) - Median(source, sourceScalp, 1);
            int limbGreen = Median(palette, referenceLimbs, 0) - Median(source, sourceLimbs, 0);
            int limbBlue = Median(palette, referenceLimbs, 1) - Median(source, sourceLimbs, 1);
            int changed = 0;

            // The base uses warm skin fills, a neutral unitard and a nearly neutral background.
            for (int y = 186; y <= 1392; y++) {
                double headWeight = 1 - Smooth((y - 321) / 91.0);
                double greenLift = limbGreen + (scalpGreen - limbGreen) * headWeight;
                double blueLift = limbBlue + (scalpBlue - limbBlue) * headWeight;
                for (int x = 295; x <= 727; x++) {
                    Color color = source.GetPixel(x, y);
                    if (color.R - color.G <= 7 || color.R - color.B <= 7 || color.G <= 42 || color.B <= 34) continue;
                    // Fade off dark linework and low-chroma fabric, then apply a RGB-only correction.
                    double strength = Smooth((color.R - color.G - 7) / 5.0)
                                      * Smooth((color.R - color.B - 7) / 5.0)
                                      * Smooth((color.G - 173) / 46.0)
                                      * Smooth((color.B - 166) / 51.0)
                                      * FaceDetailWeight(x, y, color);
                    // Match the warmer line color while keeping edge positions and facial linework.
                    double lineTone = Smooth((color.R - color.G - 28) / 34.0)
                                    * Smooth((color.R - color.B - 24) / 30.0)
                                    * Smooth((color.R - 128) / 54.0)
                                    * Smooth((color.G - 42) / 42.0)
                                    * (1 - Smooth((color.G - 170) / 50.0))
                                    * FaceDetailWeight(x, y, color);
                    int green = Math.Min(255, color.G + (int)Math.Round(greenLift * strength + 27 * lineTone));
                    int blue = Math.Min(255, color.B + (int)Math.Round(blueLift * strength + 23 * lineTone));
                    if (green == color.G && blue == color.B) continue;
                    output.SetPixel(x, y, Color.FromArgb(color.A, color.R, green, blue));
                    mask.SetPixel(x, y, Color.White);
                    changed++;
                }
            }
            output.Save(outputPath, ImageFormat.Png);
            mask.Save(maskPath, ImageFormat.Png);
            return new int[] {changed, scalpGreen, scalpBlue, limbGreen, limbBlue};
        }
    }
}
'@

$result = [ArcherSkinV08]::Run($InputPath, $ReferencePath, $OutputPath, $MaskPath)
[pscustomobject]@{
    MaskedPixels = $result[0]
    ScalpGreenLift = $result[1]
    ScalpBlueLift = $result[2]
    LimbGreenLift = $result[3]
    LimbBlueLift = $result[4]
} | ConvertTo-Json
