"""Read-only extraction of Zstandard frames from JA3 saves for bug triage.

Usage: python docs/tools/_extract_save_lua_frames.py SAVE --out DIRECTORY
Writes decompressed frames, never executes save Lua or changes the save.
"""
import argparse
from pathlib import Path
import zstandard


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("save", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    data = args.save.read_bytes()
    args.out.mkdir(parents=True, exist_ok=True)
    pos, count = 0, 0
    while True:
        start = data.find(b"\x28\xb5\x2f\xfd", pos)
        if start < 0:
            break
        dec = zstandard.ZstdDecompressor().decompressobj()
        try:
            raw = dec.decompress(data[start:])
            if not dec.eof:
                raise ValueError("incomplete frame")
        except (zstandard.ZstdError, ValueError):
            pos = start + 4
            continue
        pos = len(data) - len(dec.unused_data)
        count += 1
        output = args.out / f"frame-{count:04d}.bin"
        output.write_bytes(raw)
        print(f"{output.name}: offset={start} bytes={len(raw)}")
    print(f"Extracted {count} frames from {args.save.name}")


if __name__ == "__main__":
    main()
