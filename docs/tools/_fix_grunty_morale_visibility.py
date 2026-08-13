# -*- coding: utf-8 -*-
"""One-shot: sync items.lua GruntyPerk_JAZZ OnBeginTurn + desc to companion."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
RU = ROOT / "Russian.csv"
EN = ROOT / "English.csv"

ID_OK = 890000000009960
ID_FAIL = 890000000009961
ID_DESC = 845332100943

DESC_RU = (
    "В начале боя получает +50% ОД на первый ход. На каждом следующем ходу "
    "с шансом <em>10% × личный боевой дух</em> снова получает тот же бонус (+50% ОД). "
    "Личный БД = командный уровень ± симпатии/раны (как в бою), для шанса 0…5; "
    "при 0 эффект не срабатывает."
)
DESC_EN = (
    "At combat start gains +50% AP for the first turn. On each later turn, "
    "with chance <em>10% × personal morale</em>, gains the same +50% AP buff again. "
    "Personal morale = team morale ± likes/wounds (combat value), chance uses 0…5; "
    "at 0 it does not proc."
)
LOG_OK_EN = (
    "<em><LogName></em>: Überraschung! (+50% AP; morale <morale>, chance <chance>%, roll <roll>)"
)
LOG_OK_RU = (
    "<em><LogName></em>: Юберрашунг! (+50% ОД; БД <morale>, шанс <chance>%, бросок <roll>)"
)
LOG_FAIL_EN = (
    "<em><LogName></em>: Überraschung did not proc (morale <morale>, chance <chance>%, roll <roll>)"
)
LOG_FAIL_RU = (
    "<em><LogName></em>: Юберрашунг не сработал (БД <morale>, шанс <chance>%, бросок <roll>)"
)

NEW = f"""PlaceObj('UnitReaction', {{
\t\t\t\t\t\t\tEvent = "OnBeginTurn",
\t\t\t\t\t\t\tHandler = function (self, target)
\t\t\t\t\t\t\t\tif not g_Combat then
\t\t\t\t\t\t\t\t\treturn
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\t-- First turn already covered by OnCombatStarted buff.
\t\t\t\t\t\t\t\tif target:HasStatusEffect("Grunty_AdditionalAP") then
\t\t\t\t\t\t\t\t\treturn
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\t-- Personal morale = team BD + likes/wounds/etc; chance uses max(0,morale).
\t\t\t\t\t\t\t\tlocal morale = 0
\t\t\t\t\t\t\t\tif target.GetPersonalMorale then
\t\t\t\t\t\t\t\t\tmorale = target:GetPersonalMorale() or 0
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\tlocal chance = 10 * Max(0, morale)
\t\t\t\t\t\t\t\tif chance <= 0 then
\t\t\t\t\t\t\t\t\treturn
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\t\tlocal roll = InteractionRand(100, "GruntyPerk_JAZZ")
\t\t\t\t\t\t\t\tif roll < chance then
\t\t\t\t\t\t\t\t\ttarget:AddStatusEffect("Grunty_AdditionalAP")
\t\t\t\t\t\t\t\t\tCombatLog("short", T{{{ID_OK}, "{LOG_OK_EN}",
\t\t\t\t\t\t\t\t\t\tLogName = target:GetLogName(),
\t\t\t\t\t\t\t\t\t\tmorale = morale,
\t\t\t\t\t\t\t\t\t\tchance = chance,
\t\t\t\t\t\t\t\t\t\troll = roll,
\t\t\t\t\t\t\t\t\t}})
\t\t\t\t\t\t\t\telse
\t\t\t\t\t\t\t\t\tCombatLog("short", T{{{ID_FAIL}, "{LOG_FAIL_EN}",
\t\t\t\t\t\t\t\t\t\tLogName = target:GetLogName(),
\t\t\t\t\t\t\t\t\t\tmorale = morale,
\t\t\t\t\t\t\t\t\t\tchance = chance,
\t\t\t\t\t\t\t\t\t\troll = roll,
\t\t\t\t\t\t\t\t\t}})
\t\t\t\t\t\t\t\tend
\t\t\t\t\t\t\tend,
\t\t\t\t\t\t}}),"""


def _csv(s: str) -> str:
    if any(c in s for c in ',"\n'):
        return '"' + s.replace('"', '""') + '"'
    return s


def upsert_csv(path: Path, row_id: int, en: str, ru: str, source: str) -> None:
    line = f"{row_id},{_csv(en)},{_csv(ru)},,{source}"
    text = path.read_text(encoding="utf-8")
    pat = re.compile(rf"^{row_id},[^\n]*\n?", re.M)
    if pat.search(text):
        text = pat.sub(line + "\n", text, count=1)
    else:
        if not text.endswith("\n"):
            text += "\n"
        text += line + "\n"
    path.write_text(text, encoding="utf-8")


def brace_end(s: str, start: int) -> int:
    depth = 0
    j = start
    while j < len(s):
        c = s[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                endj = j + 1
                if endj < len(s) and s[endj] == ")":
                    endj += 1
                if endj < len(s) and s[endj] == ",":
                    endj += 1
                return endj
        j += 1
    raise SystemExit("brace end not found")


def bump_meta() -> None:
    text = META.read_text(encoding="utf-8")
    m = re.search(r"'version',\s*(\d+)", text)
    if not m:
        raise SystemExit("version not found")
    ver = int(m.group(1)) + 1
    text = re.sub(r"'version',\s*\d+", f"'version', {ver}", text, count=1)
    bullet = (
        "- UNITS-006: GruntyPerk_JAZZ — CombatLog morale roll (10%×personal BD); "
        "clarify desc [no new game]\\n"
    )
    m2 = re.search(r"'last_changes',\s*\"", text)
    if not m2:
        raise SystemExit("last_changes missing")
    text = text[: m2.end()] + bullet + text[m2.end() :]
    META.write_text(text, encoding="utf-8")
    print(f"metadata version -> {ver}")


def main() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    marker = "'Id', \"GruntyPerk_JAZZ\","
    second = text.find(marker)
    if second < 0:
        raise SystemExit("CE ModItem GruntyPerk_JAZZ not found")
    end = text.find("PlaceObj('ModItemCharacterEffectCompositeDef'", second + 1)
    if end < 0:
        raise SystemExit("next CE after Grunty not found")
    chunk = text[second:end]
    start = chunk.find('Event = "OnBeginTurn"')
    start = chunk.rfind("PlaceObj('UnitReaction'", 0, start)
    if start < 0:
        raise SystemExit("OnBeginTurn PlaceObj not found in CE chunk")
    brace_at = chunk.find("{", start)
    endj = brace_end(chunk, brace_at)

    chunk2 = chunk[:start] + NEW + chunk[endj:]
    pat = re.compile(
        rf"('Description',\s*T\({ID_DESC},\s*--\[\[[^\]]*\]\]\s*\")([\s\S]*?)(\"\))",
        re.M,
    )
    m = pat.search(chunk2)
    if not m:
        raise SystemExit("Description not found in CE chunk")
    chunk2 = chunk2[: m.start(2)] + DESC_RU + chunk2[m.end(2) :]
    ITEMS.write_text(text[:second] + chunk2 + text[end:], encoding="utf-8")
    print("items.lua patched")

    src = "jazz:CharacterEffect/GruntyPerk_JAZZ.lua"
    for path in (RU, EN):
        upsert_csv(path, ID_DESC, DESC_EN, DESC_RU, src)
        upsert_csv(path, ID_OK, LOG_OK_EN, LOG_OK_RU, src)
        upsert_csv(path, ID_FAIL, LOG_FAIL_EN, LOG_FAIL_RU, src)
    print("CSV updated")

    bump_meta()

    for rel, line in (
        (
            "docs/showcase/ru/perks.md",
            "| `GruntyPerk_JAZZ` | Grunty | Старт боя → +50% AP; далее шанс `10%×личный БД` (0…5; лог броска) |",
        ),
        (
            "docs/showcase/en/perks.md",
            "| `GruntyPerk_JAZZ` | Grunty | Combat start → +50% AP; later turns `10%×personal morale` (0…5; CombatLog roll) |",
        ),
    ):
        p = ROOT / rel
        t = p.read_text(encoding="utf-8")
        t2, n = re.subn(r"\| `GruntyPerk_JAZZ` \|[^\n]+\n", line + "\n", t, count=1)
        if n:
            p.write_text(t2, encoding="utf-8")
            print("updated", rel)

    tech = ROOT / "docs/technical/systems/units-progression-specializations.md"
    t = tech.read_text(encoding="utf-8")
    t2, n = re.subn(
        r"- \*\*Grunty `GruntyPerk_JAZZ`:\*\*[^\n]+",
        "- **Grunty `GruntyPerk_JAZZ`:** Passive CA + HUD `perk_grunty_perk`; combat start → `Grunty_AdditionalAP` (+50% max AP, one turn); later turns proc at `10% × max(0, GetPersonalMorale())` with CombatLog of morale/chance/roll.",
        t,
        count=1,
    )
    if n:
        tech.write_text(t2, encoding="utf-8")
        print("updated technical")

    notes = ROOT / "docs/tools/_units006_namedperks_notes.md"
    if notes.exists():
        t = notes.read_text(encoding="utf-8")
        t2, n = re.subn(
            r"\| `GruntyPerk_JAZZ` \|[^|]+\|[^|]+\|",
            "| `GruntyPerk_JAZZ` | Passive CA + morale CombatLog | start +50% AP; later `10%×max(0,GetPersonalMorale())` + short log |",
            t,
            count=1,
        )
        if n:
            notes.write_text(t2, encoding="utf-8")

    readme = ROOT / "docs/tools/README.md"
    entry = (
        "| `_fix_grunty_morale_visibility.py` | Grunty: CombatLog on morale AP proc "
        "(chance/roll); clarify personal-BD desc; sync CE/items/CSV/meta. |\n"
    )
    rt = readme.read_text(encoding="utf-8")
    if "_fix_grunty_morale_visibility.py" not in rt:
        if "| `_fix_grunty_passive_ca.py`" in rt:
            rt = rt.replace(
                "| `_fix_grunty_passive_ca.py`",
                entry + "| `_fix_grunty_passive_ca.py`",
            )
        else:
            rt += "\n" + entry
        readme.write_text(rt, encoding="utf-8")

    import subprocess

    r = subprocess.run(
        ["python", str(ROOT / "docs/tools/_validate_items_quick.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    if r.returncode:
        print(r.stderr)
        raise SystemExit(r.returncode)


if __name__ == "__main__":
    main()
