#!/usr/bin/env python3
"""Resize an image and compress it as JPEG under a size limit.

Usage:
  fit_image.py <src> <dst> --width 1200 --height 800 --max-kb 200   # featured: exact crop
  fit_image.py <src> <dst> --width 800 --max-kb 100                 # body: width only
Keeps the highest JPEG quality that fits under the limit (1 KB = 1000 bytes).
"""
import argparse
import io
import sys

from PIL import Image, ImageOps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--width", type=int, required=True)
    ap.add_argument("--height", type=int)
    ap.add_argument("--max-kb", type=int, required=True)
    args = ap.parse_args()

    im = Image.open(args.src).convert("RGB")
    if args.height:
        im = ImageOps.fit(im, (args.width, args.height), Image.LANCZOS)
    else:
        im = im.resize((args.width, round(im.height * args.width / im.width)), Image.LANCZOS)

    limit = args.max_kb * 1000
    for q in range(90, 29, -2):
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() <= limit:
            open(args.dst, "wb").write(buf.getvalue())
            print(f"{args.dst}: {im.width}x{im.height}, quality {q}, {buf.tell() / 1000:.0f} KB (max {args.max_kb} KB)")
            return
    sys.exit(f"Could not fit {args.src} under {args.max_kb} KB")


if __name__ == "__main__":
    main()
