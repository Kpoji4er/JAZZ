# -*- coding: utf-8 -*-
"""UNITS-006 Smiley RecklessAssault: add recharge_on_kill=1 like JAZZ RunAndGun."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
CE = ROOT / "CharacterEffect" / "RecklessAssault.lua"

DN = "890000000009935"
DESC = "890000000009936"

DESC_RU = (
    "Улучшенный <em>Run and Gun</em>: до <em>4</em> атак с пистолет-пулемётом, карабином или автоматом. "
    "<em>+<cth_bonus></em> к точности. Без потери <GameTerm('Energy')>. "
    "<color EmStyle>Заряжается после убийства другим способом.</color>"
)
DESC_EN = (
    "Improved <em>Run and Gun</em>: up to <em>4</em> attacks with an SMG, carbine, or assault rifle. "
    "<em>+<cth_bonus></em> Accuracy. No <GameTerm('Energy')> loss. "
    "<color EmStyle>Recharges after a kill with another attack.</color>"
)

ROWS = {
    DN: ("Безрассудный натиск", "Reckless Rush", "jazz:CharacterEffect/RecklessAssault.lua"),
    DESC: (DESC_RU, DESC_EN, "jazz:CharacterEffect/RecklessAssault.lua"),
}

RECHARGE_PARAM = """\t\t\t\t\t\tPlaceObj('PresetParamNumber', {
\t\t\t\t\t\t\t'Name', "recharge_on_kill",
\t\t\t\t\t\t\t'Value', 1,
\t\t\t\t\t\t\t'Tag', "<recharge_on_kill>",
\t\t\t\t\t\t}),
"""


def csv_escape(s: str) -> str:
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def patch_csv(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    found: set[str] = set()
    out: list[str] = []
    for line in lines:
        rid = line.split(",", 1)[0] if line else ""
        if rid in ROWS:
            ru, en, src = ROWS[rid]
            nl = "\r\n" if line.endswith("\r\n") else "\n"
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}{nl}")
            found.add(rid)
        else:
            out.append(line)
    missing = [rid for rid in ROWS if rid not in found]
    if missing:
        if out and not out[-1].endswith("\n"):
            out[-1] += "\n"
        for rid in missing:
            ru, en, src = ROWS[rid]
            out.append(f"{rid},{csv_escape(ru)},{csv_escape(en)},,{src}\n")
    path.write_text("".join(out), encoding="utf-8-sig")
    print(f"{path.name}: upsert {sorted(found)}; appended={missing}")


def patch_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    m = re.search(
        r"id = \"RecklessAssault\",\s*\}\),",
        text,
    )
    if not m:
        raise SystemExit("RecklessAssault CA end marker missing")
    start = text.rfind("PlaceObj('ModItemCombatAction'", 0, m.start())
    if start < 0:
        raise SystemExit("RecklessAssault CA start missing")
    block = text[start : m.end()]
    if "'Name', \"recharge_on_kill\"" in block:
        print("items.lua: recharge_on_kill already present")
    else:
        needle = """\t\t\t\t\tParameters = {
\t\t\t\t\t\tPlaceObj('PresetParamNumber', {
\t\t\t\t\t\t\t'Name', "mobile_move_ap",
\t\t\t\t\t\t\t'Value', 12,
\t\t\t\t\t\t\t'Tag', "<mobile_move_ap>",
\t\t\t\t\t\t}),
"""
        if needle not in block:
            raise SystemExit("RecklessAssault Parameters mobile_move_ap anchor missing")
        new_block = block.replace(needle, needle + RECHARGE_PARAM, 1)
        text = text[:start] + new_block + text[m.end() :]
        print("items.lua: inserted recharge_on_kill")

    old = (
        "Улучшенный <em>Run and Gun</em>: до <em>4</em> атак с пистолет-пулемётом, карабином или автоматом. "
        "<em>+<cth_bonus></em> к точности. Без потери <GameTerm('Energy')>."
    )
    if DESC_RU in text:
        print("items.lua: CE Description already new")
    elif old in text:
        text = text.replace(old, DESC_RU, 1)
        print("items.lua: CE Description string replaced")
    else:
        print("WARN: CE Description not updated in items")

    ITEMS.write_text(text, encoding="utf-8")


def patch_ce() -> None:
    text = CE.read_text(encoding="utf-8")
    old = (
        "Улучшенный <em>Run and Gun</em>: до <em>4</em> атак с пистолет-пулемётом, карабином или автоматом. "
        "<em>+<cth_bonus></em> к точности. Без потери <GameTerm('Energy')>."
    )
    if DESC_RU in text:
        print("CE companion: already new")
        return
    if old not in text:
        raise SystemExit("CE companion description anchor missing")
    CE.write_text(text.replace(old, DESC_RU, 1), encoding="utf-8")
    print("CE companion: Description updated")


def bump_meta() -> None:
    meta = META.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", meta)
    if not m:
        raise SystemExit("version missing")
    ver = int(m.group(1)) + 1
    meta = meta[: m.start(1)] + str(ver) + meta[m.end(1) :]
    bullet = (
        "- UNITS-006: Smiley RecklessAssault — recharge_on_kill like RunAndGun [no new game]\\n"
    )
    marker = "'last_changes', \""
    i = meta.find(marker) + len(marker)
    if "RecklessAssault — recharge_on_kill" not in meta[i : i + 200]:
        meta = meta[:i] + bullet + meta[i:]
    chunk = meta[i : meta.find('",', i)]
    if "\n" in chunk or "\r" in chunk:
        raise SystemExit("raw newline in last_changes")
    META.write_text(meta, encoding="utf-8", newline="\n")
    print(f"metadata version={ver}")


def main() -> None:
    patch_items()
    patch_ce()
    bump_meta()
    patch_csv(ROOT / "English.csv")
    patch_csv(ROOT / "Russian.csv")
    print("OK RecklessAssault recharge_on_kill")


if __name__ == "__main__":
    main()
