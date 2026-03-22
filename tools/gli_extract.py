#!/usr/bin/env python3
"""Extract sprites from Airline Tycoon GLIB2 .gli files as PNG images.

Requires: pip install Pillow

Usage:
  python gli_extract.py <file.gli>                           # list sprites
  python gli_extract.py <file.gli> --extract                 # extract to ./<basename>/ folder
  python gli_extract.py <file.gli> --extract --out-dir DIR   # extract to DIR
  python gli_extract.py --all DIR [--extract] [--out-dir DIR]
"""

import argparse
import os
import struct
import sys
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
except ImportError:
    print("Pillow is required: pip install Pillow", file=sys.stderr)
    sys.exit(1)

CHUNK_GFX = 1
CHUNK_NAME = 2
CHUNK_PALETTE = 3

# GfxLibHeader layout (read after 4-byte "GLIB" magic):
#   Length(I) Unknown0(I) Unknown1(H) Unknown2-5(4×I) BitDepth(I) Files(I) Pos(I) Unknown6-8(3×I)
#   Total: 50 bytes
_HDR_FMT = "<IHIIIIIIIIII"  # 12 values, 46 bytes (after Length dword)

# GfxChunkImage layout (76 bytes):
#   Length Size Width Height Unknown0 Flags BitDepth PlaneSize
#   Rmask Gmask Bmask OffsetColor OffsetAlpha OffsetZ Unknown1-5
_IMG_FMT = "<IIIIIIIIIIIIIIIIIII"  # 19 × dword = 76 bytes


def _mask_shift_max(mask: int):
    """Return (right_shift, max_value) for a bitmask channel."""
    if not mask:
        return 0, 0
    shift = (mask & -mask).bit_length() - 1
    bits = mask.bit_length() - shift
    return shift, (1 << bits) - 1


def _decode_pixels(pixel_data: bytes, width: int, height: int,
                   bit_depth: int, rmask: int, gmask: int, bmask: int,
                   img_size: int) -> Optional[Image.Image]:
    """Convert raw pixel bytes to a PIL Image using the channel masks."""
    if not (width and height and img_size):
        return None

    pitch = img_size // height  # bytes per row (may include row padding)
    bpp = bit_depth // 8

    if bit_depth == 8:
        # No palette support (game's SDL port doesn't support it either).
        # Output as grayscale so something visible is produced.
        rows = [pixel_data[y * pitch: y * pitch + width] for y in range(height)]
        return Image.frombytes("L", (width, height), b"".join(rows))

    if bit_depth in (15, 16):
        r_shift, r_max = _mask_shift_max(rmask)
        g_shift, g_max = _mask_shift_max(gmask)
        b_shift, b_max = _mask_shift_max(bmask)
        out = bytearray(width * height * 3)
        idx = 0
        for y in range(height):
            row = y * pitch
            for x in range(width):
                px = struct.unpack_from("<H", pixel_data, row + x * 2)[0]
                out[idx]     = ((px & rmask) >> r_shift) * 255 // r_max if r_max else 0
                out[idx + 1] = ((px & gmask) >> g_shift) * 255 // g_max if g_max else 0
                out[idx + 2] = ((px & bmask) >> b_shift) * 255 // b_max if b_max else 0
                idx += 3
        return Image.frombytes("RGB", (width, height), bytes(out))

    if bit_depth == 24:
        rows = [pixel_data[y * pitch: y * pitch + width * 3] for y in range(height)]
        return Image.frombytes("RGB", (width, height), b"".join(rows))

    if bit_depth == 32:
        rows = [pixel_data[y * pitch: y * pitch + width * 4] for y in range(height)]
        raw = b"".join(rows)
        mode = "BGRA" if bmask == 0xFF else "RGBA"
        return Image.frombytes("RGBA", (width, height), raw, "raw", mode).convert("RGB")

    print(f"    Warning: unsupported bit depth {bit_depth}, skipping", file=sys.stderr)
    return None


def _read_sprites(path: str) -> list:
    """Parse a GLIB2 file and return a list of sprite metadata dicts."""
    sprites = []
    with open(path, "rb") as f:
        magic = f.read(4)
        if magic != b"GLIB":
            return []

        length = struct.unpack("<I", f.read(4))[0]
        rest = f.read(length - 4)
        if len(rest) < 42:
            return []

        (u0, u1, u2, u3, u4, u5, lib_bd, files, dir_pos,
         u6, u7, u8) = struct.unpack(_HDR_FMT, rest)

        f.seek(dir_pos)
        for _ in range(files):
            entry_start = f.tell()
            raw = f.read(5)
            if len(raw) < 5:
                break
            entry_size, chunk_type = struct.unpack("<IB", raw)

            if chunk_type == CHUNK_GFX:
                name_raw, img_offset = struct.unpack("<8sI", f.read(12))
                name = name_raw.rstrip(b"\x00").decode("ascii", errors="replace")

                saved = f.tell()
                f.seek(img_offset)
                img_hdr = f.read(76)
                if len(img_hdr) == 76:
                    (img_len, img_size, width, height, _u0, flags,
                     bit_depth, plane_size, rmask, gmask, bmask,
                     off_color, off_alpha, off_z,
                     _1, _2, _3, _4, _5) = struct.unpack(_IMG_FMT, img_hdr)
                    sprites.append({
                        "name": name,
                        "width": width,
                        "height": height,
                        "bit_depth": bit_depth,
                        "img_size": img_size,
                        "rmask": rmask,
                        "gmask": gmask,
                        "bmask": bmask,
                        "off_color": off_color,  # absolute file offset to pixels
                    })
                f.seek(saved)

            f.seek(entry_start + entry_size)

    return sprites


def _extract(path: str, sprites: list, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "rb") as f:
        for s in sprites:
            f.seek(s["off_color"])
            pixel_data = f.read(s["img_size"])
            img = _decode_pixels(
                pixel_data, s["width"], s["height"],
                s["bit_depth"], s["rmask"], s["gmask"], s["bmask"],
                s["img_size"],
            )
            if img is None:
                print(f"  {s['name']:8s}  skipped (empty or unsupported)")
                continue
            out_path = os.path.join(out_dir, f"{s['name']}.png")
            img.save(out_path)
            print(f"  {s['name']:8s}  {s['width']}x{s['height']}  {s['bit_depth']}bpp  -> {out_path}")


def process_file(path: str, do_extract: bool, out_dir: Optional[str]) -> None:
    sprites = _read_sprites(path)
    if not sprites and open(path, "rb").read(4) != b"GLIB":
        print(f"{path}: not a GLIB file", file=sys.stderr)
        return

    label = os.path.basename(path)
    if do_extract:
        target = out_dir or os.path.join(".", Path(path).stem)
        print(f"{label}: extracting {len(sprites)} sprite(s) -> {target}")
        _extract(path, sprites, target)
    else:
        print(f"{label}: {len(sprites)} sprite(s)")
        for s in sprites:
            print(f"  {s['name']:8s}  {s['width']}x{s['height']}  {s['bit_depth']}bpp")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract sprites from Airline Tycoon GLIB2 .gli files as PNG."
    )
    parser.add_argument("files", nargs="*", help=".gli file(s) to process")
    parser.add_argument(
        "--extract", action="store_true",
        help="Extract sprites as PNG (default: list only)",
    )
    parser.add_argument(
        "--out-dir", metavar="DIR",
        help="Output directory for extracted PNGs",
    )
    parser.add_argument(
        "--all", metavar="DIR", dest="all_dir",
        help="Process all .gli/.glj files in DIR",
    )
    args = parser.parse_args()

    if args.all_dir:
        gli_files = sorted(
            os.path.join(args.all_dir, f)
            for f in os.listdir(args.all_dir)
            if f.lower().endswith((".gli", ".glj"))
        )
        if not gli_files:
            print(f"No .gli files found in {args.all_dir}", file=sys.stderr)
            sys.exit(1)
        for path in gli_files:
            process_file(path, args.extract, args.out_dir)
    elif args.files:
        for path in args.files:
            process_file(path, args.extract, args.out_dir)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
