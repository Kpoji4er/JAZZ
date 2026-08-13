# -*- coding: utf-8 -*-
"""UNITS-006 Red HaveABlast: use GrenadesInventory pockets (ThrowGrenadeAG–DG).

Runtime: Code/System_HaveABlast.lua (already patched by agent).
This script: metadata bump + showcase/technical/CE desc sync.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "metadata.lua"
CE = ROOT / "CharacterEffect" / "HaveABlast.lua"
ITEMS = ROOT / "items.lua"
RU = ROOT / "Russian.csv"
EN = ROOT / "English.csv"

DESC_ID = "890000000009874"
DESC_RU = (
    "Переключатель. Пока активен: после атаки по себе (попадание или промах) отвечает гранатой "
    "(руки, слоты гранат или из рюкзака); урон от взрывов по себе −50%. Выключен — без эффекта."
)
DESC_EN = (
    "Toggle. While on: after being attacked (hit or miss) retaliates with a grenade "
    "(hands, grenade pockets, or backpack); explosion damage taken −50%. Off — no effect."
)


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def upsert_csv(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    out = []
    found = False
    line_new = f"{DESC_ID},{csv_escape(DESC_RU)},{csv_escape(DESC_EN)},,jazz:CharacterEffect/HaveABlast.lua\n"
    for line in lines:
        rid = line.split(",", 1)[0] if line else ""
        if rid == DESC_ID:
            nl = "\r\n" if line.endswith("\r\n") else "\n"
            out.append(line_new.rstrip("\n") + nl)
            found = True
        else:
            out.append(line)
    if not found:
        if out and not out[-1].endswith("\n"):
            out[-1] += "\n"
        out.append(line_new)
    path.write_text("".join(out), encoding="utf-8-sig")


def patch_desc_file(path: Path, key: str) -> None:
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf"({re.escape(key)}\s*T\({DESC_ID},\s*--\[\[[^\]]*\]\]\s*\")([\s\S]*?)(\"\))",
        re.M,
    )
    m = pat.search(text)
    if not m:
        print(f"WARN: desc not in {path.name}")
        return
    path.write_text(text[: m.start(2)] + DESC_RU + text[m.end(2) :], encoding="utf-8")
    print(f"patched desc {path.name}")


def bump_meta() -> None:
    text = META.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", text)
    ver = int(m.group(1)) + 1
    text = re.sub(r"'version',\s*\d+", f"'version', {ver}", text, count=1)
    bullet = (
        "- UNITS-006: Red HaveABlast — retaliate from GrenadesInventory pockets "
        "(AG–DG), not only hands [no new game]\\n"
    )
    m2 = re.search(r"'last_changes',\s*\"", text)
    i = m2.end()
    if "HaveABlast — retaliate from GrenadesInventory" not in text[i : i + 220]:
        text = text[:i] + bullet + text[i:]
    META.write_text(text, encoding="utf-8")
    print(f"metadata version -> {ver}")


def patch_docs() -> None:
    reps = [
        (
            ROOT / "docs/showcase/ru/perks.md",
            r"\| `HaveABlast` \|[^\n]+\n",
            "| `HaveABlast` | Red | Toggle: ответ гранатой при попадании **или** промахе (руки / **слоты гранат** / рюкзак); **−50%** урона от взрывов по себе пока активен |\n",
        ),
        (
            ROOT / "docs/showcase/en/perks.md",
            r"\| `HaveABlast` \|[^\n]+\n",
            "| `HaveABlast` | Red | Toggle: grenade retaliate on hit **or** miss (hands / **grenade pockets** / backpack); **−50%** explosion damage taken while active |\n",
        ),
    ]
    for path, pat, line in reps:
        t = path.read_text(encoding="utf-8")
        t2, n = re.subn(pat, line, t, count=1)
        if n:
            path.write_text(t2, encoding="utf-8")

    tech = ROOT / "docs/technical/systems/units-progression-specializations.md"
    t = tech.read_text(encoding="utf-8")
    # insert/replace HaveABlast line if present
    if "HaveABlast" in t:
        t2, n = re.subn(
            r"- \*\*(?:Red )?`HaveABlast`:\*\*[^\n]+",
            "- **Red `HaveABlast`:** toggle retaliate on hit/miss with grenade from hands, "
            "`GrenadesInventory` (`ThrowGrenadeAG–DG`), or pull from backpack Inventory; "
            "incoming blast ×50% while on (`System_HaveABlast.lua`).",
            t,
            count=1,
        )
        if n:
            tech.write_text(t2, encoding="utf-8")
        elif "- **Red `HaveABlast`:**" not in t:
            # append near Fidel DoubleToss if possible
            t = t.replace(
                "- **Fidel `DoubleToss`:",
                "- **Red `HaveABlast`:** toggle retaliate on hit/miss with grenade from hands, "
                "`GrenadesInventory` (`ThrowGrenadeAG–DG`), or pull from backpack Inventory; "
                "incoming blast ×50% while on (`System_HaveABlast.lua`).\n"
                "- **Fidel `DoubleToss`:",
            )
            tech.write_text(t, encoding="utf-8")

    notes = ROOT / "docs/tools/_units006_namedperks_notes.md"
    if notes.exists():
        nt = notes.read_text(encoding="utf-8")
        nt2, n = re.subn(
            r"\| `HaveABlast` \|[^|\n]+\|",
            "| `HaveABlast` | Toggle: hit/miss retaliate; hands + **GrenadesInventory** + Inventory pull; blast DR 50% |",
            nt,
            count=1,
        )
        if n:
            notes.write_text(nt2, encoding="utf-8")

    readme = ROOT / "docs/tools/README.md"
    entry = (
        "| `_fix_haveablast_grenade_pockets.py` | Red HaveABlast: docs/meta for "
        "GrenadesInventory AG–DG retaliate (runtime `System_HaveABlast.lua`). |\n"
    )
    rt = readme.read_text(encoding="utf-8")
    if "_fix_haveablast_grenade_pockets.py" not in rt:
        if "| `_apply_haveablast_fix.py`" in rt:
            rt = rt.replace("| `_apply_haveablast_fix.py`", entry + "| `_apply_haveablast_fix.py`")
        else:
            rt += "\n" + entry
        readme.write_text(rt, encoding="utf-8")


def main() -> None:
    patch_desc_file(CE, "Description =")
    # items.lua CE ModItem
    text = ITEMS.read_text(encoding="utf-8")
    pat = re.compile(
        rf"('Description',\s*T\({DESC_ID},\s*--\[\[[^\]]*\]\]\s*\")([\s\S]*?)(\"\))",
        re.M,
    )
    m = pat.search(text)
    if m:
        ITEMS.write_text(text[: m.start(2)] + DESC_RU + text[m.end(2) :], encoding="utf-8")
        print("patched items.lua desc")
    upsert_csv(RU)
    upsert_csv(EN)
    bump_meta()
    patch_docs()
    print("OK HaveABlast grenade pockets docs")


if __name__ == "__main__":
    main()
