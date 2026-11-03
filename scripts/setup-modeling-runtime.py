"""Prepare isolated Python 3.11 + bpy 4.2 wheels under ignored tmp/; no global installs."""
from pathlib import Path
import hashlib
import subprocess
import sys
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "tmp" / "modeling-runtime"
BASE.mkdir(parents=True, exist_ok=True)
PYDIR = BASE / "python311"
WHEELS = BASE / "wheels"
WHEELS.mkdir(exist_ok=True)
archive = BASE / "python311.zip"
if not archive.exists():
    print("Downloading official Python embedded runtime", flush=True)
    urllib.request.urlretrieve("https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip", archive)
if not (PYDIR / "python.exe").exists():
    with zipfile.ZipFile(archive) as z:
        z.extractall(PYDIR)
import json
for package, version in [('bpy','4.2.0'),('numpy','1.26.4'),('zstandard','0.23.0'),
        ('requests','2.32.3'),('charset-normalizer','3.4.0'),('idna','3.10'),
        ('urllib3','2.2.3'),('certifi','2024.8.30'),('cython','3.0.12')]:
    with urllib.request.urlopen(f'https://pypi.org/pypi/{package}/{version}/json', timeout=30) as response:
        info=json.load(response)
    candidates=[f for f in info['urls'] if f['filename'].endswith('.whl') and
        (('cp311' in f['filename'] and 'win_amd64' in f['filename']) or
         'py3-none-any' in f['filename'] or 'py2.py3-none-any' in f['filename'])]
    if not candidates: raise RuntimeError('No compatible wheel: '+package)
    entry=candidates[0];destination=WHEELS/entry['filename']
    if destination.exists() and hashlib.sha256(destination.read_bytes()).hexdigest()==entry['digests']['sha256']:
        continue
    print('Downloading',entry['filename'],round(entry['size']/1e6,1),'MB',flush=True)
    with urllib.request.urlopen(entry['url'],timeout=60) as source, destination.open('wb') as target:
        total=0;checkpoint=0
        while True:
            chunk=source.read(1024*1024)
            if not chunk:break
            target.write(chunk);total+=len(chunk)
            if total-checkpoint>=50*1024*1024:
                print(round(total/1e6,1),'MB',flush=True);checkpoint=total
    if hashlib.sha256(destination.read_bytes()).hexdigest()!=entry['digests']['sha256']:
        raise RuntimeError('Wheel checksum mismatch: '+entry['filename'])
packages = PYDIR / "site-packages"
packages.mkdir(exist_ok=True)
for wheel in WHEELS.glob("*.whl"):
    marker = BASE / (wheel.name + ".extracted")
    if marker.exists():
        continue
    print("Extracting", wheel.name, flush=True)
    with zipfile.ZipFile(wheel) as z:
        z.extractall(packages)
    marker.write_text(hashlib.sha256(wheel.read_bytes()).hexdigest())
(PYDIR / "python311._pth").write_text("python311.zip\n.\nsite-packages\nsite-packages/bpy-4.2.0.data/purelib\nimport site\n")
subprocess.run([str(PYDIR / "python.exe"), "-c", "import bpy; print('Blender runtime', bpy.app.version_string)"], check=True)
