# -*- coding: utf-8 -*-
"""Diff Лист2 perk cols: fresh TSV vs earlier WebFetch snapshot."""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
FRESH = ROOT / "docs/tools/_tmp_list2_perks_fresh.tsv"
OLD_MD = pathlib.Path(
    r"C:\Users\SsAnd\.cursor\projects\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz"
    r"\agent-tools\252f8fcd-6b9f-42ac-835a-a1392125ef78.txt"
)
NEW_MD = pathlib.Path(
    r"C:\Users\SsAnd\.cursor\projects\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz"
    r"\agent-tools\00ffcc29-ff02-4ae9-8713-1767cbe445fd.txt"
)
OUT = ROOT / "docs/tools/_tmp_list2_sheet_diff.md"


def decode_bytes(data: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8", "utf-16", "cp1251"):
        try:
            text = data.decode(enc)
        except UnicodeDecodeError:
            continue
        if "Ice" in text:
            return text
    return data.decode("utf-8", errors="replace")


def parse_tsv(text: str) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    for i, line in enumerate(text.splitlines()):
        parts = line.split("\t")
        if i == 0 or len(parts) < 12:
            continue
        mid = parts[0].strip().strip('"')
        if not mid:
            continue
        rows[mid] = (parts[10].strip().strip('"'), parts[11].strip().strip('"'))
    return rows


def parse_md(text: str) -> dict[str, tuple[str, str]]:
    rows: dict[str, tuple[str, str]] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 12:
            continue
        if parts[0].isdigit():
            mid, perk, desc = parts[1], parts[10], parts[11]
        else:
            mid, perk, desc = parts[0], parts[10], parts[11]
        if not re.match(r"^[A-Za-z]", mid):
            continue
        rows[mid] = (perk, desc)
    return rows


def main() -> int:
    if not FRESH.exists():
        print("missing fresh tsv", FRESH, file=sys.stderr)
        return 1
    fresh = parse_tsv(decode_bytes(FRESH.read_bytes()))
    old = parse_md(OLD_MD.read_text(encoding="utf-8")) if OLD_MD.exists() else {}
    new_md = parse_md(NEW_MD.read_text(encoding="utf-8")) if NEW_MD.exists() else {}

    print(f"fresh={len(fresh)} old_md={len(old)} new_md={len(new_md)}")
    # sample encoding check
    g = fresh.get("Grunty")
    print("Grunty fresh:", g)

    lines = ["# Лист2 perk diff (fresh TSV vs first WebFetch)", ""]
    diffs = 0
    for mid in sorted(set(old) | set(fresh), key=str.lower):
        a = old.get(mid)
        b = fresh.get(mid)
        if a == b:
            continue
        diffs += 1
        lines.append(f"## {mid}")
        if a is None:
            lines.append(f"- **ADDED:** `{b[0]}` — {b[1]}")
        elif b is None:
            lines.append(f"- **REMOVED:** `{a[0]}` — {a[1]}")
        else:
            if a[0] != b[0]:
                lines.append(f"- name: `{a[0]}` → `{b[0]}`")
            if a[1] != b[1]:
                lines.append(f"- OLD desc: {a[1]}")
                lines.append(f"- NEW desc: {b[1]}")
        lines.append("")
    lines.insert(2, f"Total changed rows: **{diffs}**\n")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} diffs={diffs}")

    # also vs latest webfetch
    md_diffs = sum(1 for m in set(new_md) | set(fresh) if new_md.get(m) != fresh.get(m))
    print(f"fresh vs latest webfetch diffs={md_diffs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
