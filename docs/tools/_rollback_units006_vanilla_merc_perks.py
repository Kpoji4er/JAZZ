# -*- coding: utf-8 -*-
"""Rollback UNITS-006 overrides for listed vanilla merc personal perks.

Removes ModItemCharacterEffectCompositeDef + companion + metadata.code entries
so stock JA3 CE loads again. Also clears jazz-units TheGrim fearAoE override.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
UNITS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")

# Perk Ids with jazz CE overrides to delete
PERKS = [
    "YouSeeIgor",
    "WeGotThis",
    "NailsPerk",
    "SecondStoryMan",
    "ShoulderToShoulder",
    "IcePerk",
    "DedicatedCamper",
    "TagTeam",
    "BunsPerk",
    "Spotter",
    "SidneyPerk",
    "OnMyTarget",
]

# Loc IDs only used by these CE DisplayName/Description (optional purge)
LOC_IDS = [
    890000000006500,
    890000000006501,
    890000000006502,
    890000000006503,
    890000000006504,
    890000000006505,
    890000000006508,
    890000000006509,
    890000000006510,
    890000000006511,
    890000000006514,
    890000000006515,
    890000000009863,
    890000000009864,
    890000000009865,
    890000000009866,
    890000000009867,
    890000000009868,
    890000000009871,
    890000000009872,
    890000000009879,
    890000000009880,
    890000000009883,
    890000000009884,
]


def remove_moditem_ce(text: str, perk_id: str) -> tuple[str, int]:
    """Remove PlaceObj('ModItemCharacterEffectCompositeDef' … Id=perk_id … }),"""
    # Match from PlaceObj to the closing }), that ends this ModItem (depth of braces
    # after PlaceObj call). Use Id anchor then scan braces.
    pat = re.compile(
        rf"PlaceObj\('ModItemCharacterEffectCompositeDef',\s*\{{",
        re.M,
    )
    removed = 0
    out = []
    pos = 0
    for m in pat.finditer(text):
        start = m.start()
        # Find matching close for the PlaceObj( ... )
        i = m.end() - 1  # at '{'
        depth = 0
        j = i
        while j < len(text):
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    # expect }), or }),\n
                    end = j + 1
                    if end < len(text) and text[end] == ")":
                        end += 1
                    if end < len(text) and text[end] == ",":
                        end += 1
                    # swallow following newline/tabs only if whole line was the PlaceObj
                    while end < len(text) and text[end] in "\r\n":
                        end += 1
                    block = text[start:end]
                    if re.search(rf"'Id',\s*\"{re.escape(perk_id)}\"", block):
                        out.append(text[pos:start])
                        pos = end
                        removed += 1
                        print(f"  removed ModItem {perk_id} @ {start}")
                    break
            j += 1
    out.append(text[pos:])
    return "".join(out), removed


def remove_metadata_code(text: str, rel: str) -> tuple[str, int]:
    # "CharacterEffect/Foo.lua",
    pat = re.compile(rf'\t\t"{re.escape(rel)}",\r?\n')
    text2, n = pat.subn("", text)
    return text2, n


def purge_csv_ids(path: Path, ids: set[int]) -> int:
    raw = path.read_bytes()
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    lines = raw.decode("utf-8").splitlines(keepends=True)
    out = []
    n = 0
    for ln in lines:
        m = re.match(r'^"?(\d+)"?,', ln)
        if m and int(m.group(1)) in ids:
            n += 1
            continue
        out.append(ln)
    path.write_bytes("".join(out).encode("utf-8"))
    # normalize newlines if needed — keep as decoded join without forcing
    return n


def main() -> int:
    items = JAZZ / "items.lua"
    meta = JAZZ / "metadata.lua"
    raw = items.read_bytes()
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    text = raw.decode("utf-8")

    total = 0
    for pid in PERKS:
        text, n = remove_moditem_ce(text, pid)
        total += n
        if n == 0:
            print(f"WARN: no ModItem for {pid}")

    if "},," in text:
        print("ERROR stacked commas")
        return 2

    items.write_bytes(text.replace("\r\n", "\n").replace("\n", nl.decode("ascii")).encode("utf-8"))
    print(f"items.lua removed {total} ModItems")

    mraw = meta.read_bytes()
    mnl = b"\r\n" if b"\r\n" in mraw else b"\n"
    mtext = mraw.decode("utf-8")
    mn = 0
    for pid in PERKS:
        rel = f"CharacterEffect/{pid}.lua"
        mtext, n = remove_metadata_code(mtext, rel)
        mn += n
        if n == 0:
            print(f"WARN: metadata missing {rel}")
        ce = JAZZ / "CharacterEffect" / f"{pid}.lua"
        if ce.exists():
            ce.unlink()
            print(f"  deleted {ce.name}")
        else:
            print(f"WARN: no companion {ce.name}")
    meta.write_bytes(mtext.replace("\r\n", "\n").replace("\n", mnl.decode("ascii")).encode("utf-8"))
    print(f"metadata code entries removed: {mn}")

    # jazz-units TheGrim
    u_items = UNITS / "items.lua"
    u_meta = UNITS / "metadata.lua"
    if u_items.exists():
        uraw = u_items.read_bytes()
        unl = b"\r\n" if b"\r\n" in uraw else b"\n"
        utext = uraw.decode("utf-8")
        utext, n = remove_moditem_ce(utext, "TheGrim")
        if n:
            u_items.write_bytes(
                utext.replace("\r\n", "\n").replace("\n", unl.decode("ascii")).encode("utf-8")
            )
            print(f"jazz-units items TheGrim removed: {n}")
        um = u_meta.read_text(encoding="utf-8") if u_meta.exists() else ""
        if um:
            um2, n2 = remove_metadata_code(um, "CharacterEffect/TheGrim.lua")
            if n2:
                u_meta.write_text(um2, encoding="utf-8", newline="\n" if "\r\n" not in um else None)
                # keep original newlines simply:
                u_meta.write_bytes(
                    um2.replace("\r\n", "\n")
                    .replace("\n", ("\r\n" if "\r\n" in um else "\n"))
                    .encode("utf-8")
                )
                print(f"jazz-units metadata TheGrim: {n2}")
        tg = UNITS / "CharacterEffect" / "TheGrim.lua"
        if tg.exists():
            tg.unlink()
            print("deleted jazz-units TheGrim.lua")

    # loc purge
    ids = set(LOC_IDS)
    for name in ("Russian.csv", "English.csv"):
        p = JAZZ / name
        if p.exists():
            n = purge_csv_ids(p, ids)
            print(f"{name}: purged {n} rows")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
