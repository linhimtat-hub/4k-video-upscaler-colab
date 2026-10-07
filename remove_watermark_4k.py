#!/usr/bin/env python3
"""Clean a user-owned watermark/logo region, then upscale to UHD 4K."""
import argparse, subprocess, shutil, tempfile
from pathlib import Path

def run(c): subprocess.run(c, check=True)

p=argparse.ArgumentParser()
p.add_argument("input"); p.add_argument("output")
p.add_argument("--watermark", required=True, help="x:y:w:h in source pixels")
a=p.parse_args()
if not shutil.which("ffmpeg"): raise SystemExit("ffmpeg required")
x,y,w,h=map(int,a.watermark.split(":"))
src=Path(a.input); out=Path(a.output)
tmp=Path(tempfile.mkdtemp()); clean=tmp/"clean.mp4"
# Spatial reconstruction for the selected user-owned watermark area.
run(["ffmpeg","-y","-i",str(src),"-vf",f"delogo=x={x}:y={y}:w={w}:h={h}:show=0",
     "-c:v","libx264","-crf","14","-preset","slow","-c:a","copy",str(clean)])
# UHD export. Use the repo's Real-ESRGAN notebook first when AI detail recovery is desired.
run(["ffmpeg","-y","-i",str(clean),"-vf",
     "scale=3840:2160:force_original_aspect_ratio=decrease:flags=lanczos,pad=3840:2160:(ow-iw)/2:(oh-ih)/2",
     "-c:v","libx265","-crf","16","-preset","slow","-pix_fmt","yuv420p10le",
     "-c:a","aac","-b:a","192k",str(out)])
print(out)
