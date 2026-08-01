# -*- coding: utf-8 -*-
"""Extract + decrypt JA2 / NightOps MERCEDT.SLF speech subtitles to UTF-8 CSV.

NightOps Russian EDT layout (observed):
  - UTF-16LE slots with CP1251 in the low byte (high byte 0)
  - text rows every 3rd 160-byte record (lines 000..116)
  - encryption: each byte > 0x20 stored as (c+1); 0x00/0x20 unchanged
  - letter Я (CP1251 0xFF) encrypts to 0x00 — restored when a lone 0 is
    followed by more payload

Usage (from jazz/):
  python docs/tools/_extract_ja2_mercedt.py
  python docs/tools/_extract_ja2_mercedt.py --slf PATH --out DIR
"""
from __future__ import annotations

import argparse
import csv
import struct
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_SLF = Path(
    r"C:\Users\SsAnd\Downloads\NightOps_v1.50.14\ja2no150\Data\MERCEDT.SLF"
)
DEFAULT_OUT = Path(
    r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz"
    r"\docs\design\mercs-ja12\_voice-source\ja2no-mercedt"
)

# Vanilla JA2 AIM/MERC/RPC nicknames (profile id → nick). NightOps may override.
JA2_NICKS: dict[int, str] = {
    0: "Barry",
    1: "Blood",
    2: "Lynx",
    3: "Grizzly",
    4: "Ivan",
    5: "Trevor",
    6: "Fox",
    7: "Skyrider",  # often transport; keep id
    8: "Kit",
    9: "Ice",
    10: "Spider",
    11: "Shadow",
    12: "Red",
    13: "Raider",
    14: "Scully",
    15: "Gumpy",
    16: "Current",  # placeholder — verify in build
    17: "Magic",
    18: "Stephen",
    19: "Scully",
    20: "Malice",
    21: "Dr Q",
    22: "Nails",
    23: "Thor",
    24: "Scope",
    25: "Wolf",
    26: "MD",
    27: "Meltdown",
    28: "Buns",
    29: "Gasket",
    30: "Hitman",
    31: "Buzz",
    32: "Claymore",
    33: "Spider",
    34: "Spike",
    35: "Vince",
    36: "Conrad",
    37: "Larry",
    38: "Flo",
    39: "Gaston",
    40: "Stogie",
    41: "Iggy",
    42: "Trevor",  # often unused slot variants — overwritten below from EDT peek
}


def list_slf(path: Path) -> list[tuple[str, bytes]]:
    data = path.read_bytes()
    i_used = struct.unpack_from("<i", data, 516)[0]
    entry = 280
    start = len(data) - i_used * entry
    out: list[tuple[str, bytes]] = []
    for i in range(i_used):
        off = start + i * entry
        fname = data[off : off + 256].split(b"\0", 1)[0].decode("latin1", "replace")
        ui_off, ui_len = struct.unpack_from("<II", data, off + 256)
        out.append((fname.replace("\\", "/"), data[ui_off : ui_off + ui_len]))
    return out


def decode_edt_line(chunk: bytes) -> str:
    lows = bytes(chunk[i] for i in range(0, len(chunk), 2))
    out = bytearray()
    i = 0
    while i < len(lows):
        c = lows[i]
        if c == 0:
            if i + 1 < len(lows) and lows[i + 1] != 0:
                out.append(0xFF)  # encrypted Я
                i += 1
                continue
            break
        out.append((c - 1) & 0xFF if c > 0x20 else c)
        i += 1
    return out.decode("cp1251", "replace").strip()


def decode_edt(blob: bytes, width: int = 160) -> list[str]:
    rows = len(blob) // width
    lines: list[str] = []
    for row in range(0, rows, 3):
        lines.append(decode_edt_line(blob[row * width : (row + 1) * width]))
    return lines


def guess_nick_from_lines(lines: list[str], profile_id: int) -> str:
    # Prefer AIM greeting ~108: "Говорит X" / "X speaking"
    if len(lines) > 108 and lines[108]:
        t = lines[108]
        for pref in ("Говорит ", "Speaking, ", "This is "):
            if t.startswith(pref):
                rest = t[len(pref) :].split(".")[0].split(",")[0].strip()
                if rest:
                    return rest
    return JA2_NICKS.get(profile_id, f"id{profile_id:03d}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slf", type=Path, default=DEFAULT_SLF)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    if not args.slf.is_file():
        raise SystemExit(f"SLF missing: {args.slf}")

    args.out.mkdir(parents=True, exist_ok=True)
    index_rows: list[dict[str, str]] = []
    all_path = args.out / "all_lines.csv"
    with all_path.open("w", encoding="utf-8-sig", newline="") as fall:
        wall = csv.writer(fall, lineterminator="\n")
        wall.writerow(["profile_id", "nick", "line", "text"])

        for fname, blob in sorted(list_slf(args.slf), key=lambda x: x[0]):
            stem = Path(fname).stem
            if not stem.isdigit():
                continue
            pid = int(stem)
            lines = decode_edt(blob)
            nick = guess_nick_from_lines(lines, pid)
            per = args.out / f"{pid:03d}_{_safe(nick)}.csv"
            with per.open("w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(["line", "text"])
                for i, text in enumerate(lines):
                    w.writerow([f"{i:03d}", text])
                    wall.writerow([f"{pid:03d}", nick, f"{i:03d}", text])
            nonempty = sum(1 for t in lines if t)
            index_rows.append(
                {
                    "profile_id": f"{pid:03d}",
                    "nick": nick,
                    "lines": str(len(lines)),
                    "nonempty": str(nonempty),
                    "file": per.name,
                    "sample_000": lines[0] if lines else "",
                    "sample_108": lines[108] if len(lines) > 108 else "",
                }
            )
            print(f"{pid:03d} {nick:20s} nonempty={nonempty}/{len(lines)} -> {per.name}")

    idx = args.out / "index.csv"
    with idx.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "profile_id",
                "nick",
                "lines",
                "nonempty",
                "file",
                "sample_000",
                "sample_108",
            ],
            lineterminator="\n",
        )
        w.writeheader()
        w.writerows(index_rows)

    readme = args.out / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# JA2 / NightOps MERCEDT subtitles (decoded)",
                "",
                f"Source: `{args.slf}`",
                "",
                "Decrypt: CP1251 in UTF-16LE low bytes; bytes `>0x20` stored as `c+1`;",
                "encrypted `Я` (`0xFF→0x00`) restored when a lone `0` is followed by more data.",
                "",
                "Files:",
                "- `index.csv` — profile id → nick guess + samples",
                "- `NNN_<nick>.csv` — lines `000`..`116`",
                "- `all_lines.csv` — flat table",
                "",
                "Tool: `docs/tools/_extract_ja2_mercedt.py`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"DONE profiles={len(index_rows)} out={args.out}")
    return 0


def _safe(s: str) -> str:
    keep = []
    for ch in s:
        if ch.isalnum() or ch in ("-", "_"):
            keep.append(ch)
        elif ch in (" ", "."):
            keep.append("_")
    return "".join(keep)[:40] or "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
