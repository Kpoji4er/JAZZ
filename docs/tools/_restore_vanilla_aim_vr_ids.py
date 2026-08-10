# -*- coding: utf-8 -*-
"""Restore vanilla T-IDs for Raven/Thor/Vicki/Wolf ModItemVoiceResponse.

Regression: jazz-units bb6d97a remapped voiced VR lines to mod-only 8900* IDs
without shipping opus banks → silent vanilla AIM mercs.

Restores T-ids from bb6d97a^ (aligned by slot order). Then run
`_purge_restored_aim_vr_loc.py` to drop orphaned 8900* CSV rows safely.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
MERCS = ("Raven", "Thor", "Vicki", "Wolf")
OLD_REV = "bb6d97a^"


def git_show(rev: str, rel: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{rev}:{rel}"],
        cwd=UNITS,
        encoding="utf-8",
        errors="replace",
    )


def extract_vr_block(text: str, merc: str) -> tuple[int, int, str]:
    for m in re.finditer(r"PlaceObj\('ModItemVoiceResponse',\s*\{", text):
        start = m.start()
        window = text[start : start + 300000]
        gm = re.search(r'group = "MercenariesOld",\s*id = "([^"]+)"', window)
        if not gm or gm.group(1) != merc:
            continue
        end = start + gm.end()
        # include trailing }),
        close = text.find("}),", end)
        if close < 0:
            raise RuntimeError(f"no close for {merc}")
        end = close + 3
        return start, end, text[start:end]
    raise RuntimeError(f"VR block not found: {merc}")


def tids(block: str) -> list[str]:
    return re.findall(r"T\((\d+),", block)


def main() -> None:
    old_text = git_show(OLD_REV, "items.lua")
    cur_path = UNITS / "items.lua"
    cur_text = cur_path.read_text(encoding="utf-8")

    mapping: dict[str, str] = {}  # new -> old

    for merc in MERCS:
        _, _, old_block = extract_vr_block(old_text, merc)
        _, _, new_block = extract_vr_block(cur_text, merc)
        old_ids = tids(old_block)
        new_ids = tids(new_block)
        if len(old_ids) != len(new_ids):
            raise RuntimeError(
                f"{merc}: T-id count mismatch old={len(old_ids)} new={len(new_ids)}"
            )
        changed = 0
        for o, n in zip(old_ids, new_ids):
            if o == n:
                continue
            if n in mapping and mapping[n] != o:
                raise RuntimeError(f"conflicting map {n}: {mapping[n]} vs {o}")
            mapping[n] = o
            changed += 1
        print(f"{merc}: slots={len(new_ids)} restore={changed} unchanged={len(new_ids)-changed}")

    # Apply only inside the four VR blocks (avoid touching unrelated 8900 ids)
    out = cur_text
    for merc in MERCS:
        start, end, block = extract_vr_block(out, merc)

        def repl(m: re.Match[str]) -> str:
            tid = m.group(1)
            return f"T({mapping.get(tid, tid)},"

        new_block = re.sub(r"T\((\d+),", repl, block)
        out = out[:start] + new_block + out[end:]

    if out == cur_text:
        raise RuntimeError("no changes applied")
    # Match git object: LF-only (avoid \r\r\n from naive CRLF rewrite)
    cur_path.write_bytes(out.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))
    print(f"wrote {cur_path} ({len(mapping)} id remaps)")

    verify = cur_path.read_text(encoding="utf-8")
    for merc in MERCS:
        _, _, block = extract_vr_block(verify, merc)
        ids = tids(block)
        n8900 = sum(1 for t in ids if t.startswith("8900"))
        print(f"verify {merc}: n={len(ids)} remaining_8900={n8900}")

    print("Next: python docs/tools/_purge_restored_aim_vr_loc.py")


if __name__ == "__main__":
    main()
