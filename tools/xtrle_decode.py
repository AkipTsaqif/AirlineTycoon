#!/usr/bin/env python3
"""Decode xtRLE-encoded Airline Tycoon data files to plain text.

The game's CRLEReader falls back to plain text if no xtRLE header is found,
so decoded files can be dropped directly into the data folder and used as-is.

Usage:
  python xtrle_decode.py <file> [file2 ...]           # decode to stdout
  python xtrle_decode.py <file> --out-dir DIR          # decode to directory
  python xtrle_decode.py --all DIR --out-dir DIR       # batch decode all .csv in DIR
"""

import argparse
import os
import struct
import sys
from typing import Optional

MAGIC = b"xtRLE\x00"
XOR_KEY = 0xA5


def decode_xtrle(data: bytes) -> bytes:
    """Decode xtRLE-encoded bytes. Returns plain text bytes unchanged if not encoded."""
    if data[:6] != MAGIC:
        return data  # already plain text, pass through

    pos = 6
    version = struct.unpack_from("<I", data, pos)[0]
    pos += 4

    xor_key = XOR_KEY if version >= 0x102 else 0

    expected_size: Optional[int] = None
    if version >= 0x101:
        expected_size = struct.unpack_from("<I", data, pos)[0]
        pos += 4

    out = bytearray()

    while pos < len(data):
        length_byte = data[pos]
        pos += 1

        if length_byte & 0x80:
            # Literal sequence: read (length & 0x7F) raw bytes
            count = length_byte & 0x7F
            if count == 0:
                continue
            chunk = bytearray(data[pos : pos + count])
            pos += count
            if xor_key:
                for i in range(len(chunk)):
                    chunk[i] ^= xor_key
            out.extend(chunk)
        else:
            # RLE run: repeat one byte `length_byte` times
            count = length_byte
            if count == 0:
                continue
            if pos >= len(data):
                break
            run_byte = data[pos]  # XOR is NOT applied to run bytes (only to literal sequences)
            pos += 1
            out.extend(bytes([run_byte]) * count)

    if expected_size is not None and len(out) != expected_size:
        print(
            f"Warning: decoded {len(out)} bytes, expected {expected_size}",
            file=sys.stderr,
        )

    return bytes(out)


def process_file(path: str, out_dir: Optional[str]) -> None:
    with open(path, "rb") as f:
        data = f.read()

    decoded = decode_xtrle(data)

    if out_dir:
        out_path = os.path.join(out_dir, os.path.basename(path))
        with open(out_path, "wb") as f:
            f.write(decoded)
        print(f"  {os.path.basename(path)} -> {out_path} ({len(decoded)} bytes)")
    else:
        sys.stdout.buffer.write(decoded)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Decode xtRLE-encoded Airline Tycoon data files to plain text."
    )
    parser.add_argument("files", nargs="*", help="File(s) to decode")
    parser.add_argument(
        "--out-dir", metavar="DIR", help="Write decoded files here instead of stdout"
    )
    parser.add_argument(
        "--all",
        metavar="DIR",
        dest="all_dir",
        help="Decode all .csv files in DIR",
    )
    args = parser.parse_args()

    if args.out_dir:
        os.makedirs(args.out_dir, exist_ok=True)

    if args.all_dir:
        csv_files = sorted(
            os.path.join(args.all_dir, f)
            for f in os.listdir(args.all_dir)
            if f.lower().endswith(".csv")
        )
        if not csv_files:
            print(f"No .csv files found in {args.all_dir}", file=sys.stderr)
            sys.exit(1)
        print(f"Decoding {len(csv_files)} files...")
        for path in csv_files:
            process_file(path, args.out_dir)
    elif args.files:
        for path in args.files:
            process_file(path, args.out_dir)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
