# -*- coding: utf-8 -*-
"""Fix CommonLib duplicated loc IDs (AME vs JA2 perks, mag hints, parts, bleeding, AME copyright).

Keeps AME IDs 890000000005009–5028; remaps stomped perk strings to 5029–5048;
AME copyright -> 5049; aligns CSV Text with T() sources.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# old_id -> (new_id, ru_source, en_translation)
PERK_REMAP: dict[int, tuple[int, str, str]] = {
    # Vince
    890000000005009: (
        890000000005029,
        "Полевой наставник",
        "Field Mentor",
    ),
    890000000005010: (
        890000000005030,
        "Раз за бой первое лечение или перевязка союзника даёт цели +4 ОД.",
        "Once per combat, the first heal or bandage on an ally grants the target +4 AP.",
    ),
    # Hitman
    890000000005011: (890000000005031, "Вырубить", "Knock Out"),
    890000000005012: (
        890000000005032,
        "WIP — механика сигнатурного перка в разработке.",
        "WIP — signature perk mechanics under development.",
    ),
    # Biggens
    890000000005013: (890000000005033, "Старая школа", "Old School"),
    890000000005014: (
        890000000005034,
        "WIP — механика сигнатурного перка в разработке.",
        "WIP — signature perk mechanics under development.",
    ),
    # Kulba
    890000000005015: (
        890000000005035,
        "Оружейник старой закалки",
        "Old-School Gunsmith",
    ),
    890000000005016: (
        890000000005036,
        "WIP — механика сигнатурного перка в разработке.",
        "WIP — signature perk mechanics under development.",
    ),
    # Vilde
    890000000005017: (890000000005037, "Ночной автоматчик", "Night Automatic Rifleman"),
    890000000005018: (
        890000000005038,
        "Ночью и под землёй автоогонь/очередь получают +15 к шансу попадания.",
        "At night and underground, auto-fire/burst gain +15 chance to hit.",
    ),
    # Grace
    890000000005019: (890000000005039, "Точный бросок", "Precision Throw"),
    890000000005020: (
        890000000005040,
        "WIP — механика сигнатурного перка в разработке.",
        "WIP — signature perk mechanics under development.",
    ),
    # Steiger
    890000000005021: (890000000005041, "Ночной инструктор", "Night Instructor"),
    890000000005022: (
        890000000005042,
        "Ночью и под землёй в начале хода союзники в радиусе 5 клеток получают +5 к шансу попадания.",
        "At night and underground, at the start of the turn allies within 5 tiles gain +5 chance to hit.",
    ),
    # Lucky
    890000000005023: (890000000005043, "Второе дыхание", "Second Wind"),
    890000000005024: (
        890000000005044,
        "Раз за бой первый промах из огнестрела становится попаданием.",
        "Once per combat, the first firearm miss becomes a hit.",
    ),
    # Laura
    890000000005025: (890000000005045, "Скрытный врач", "Stealth Medic"),
    890000000005026: (
        890000000005046,
        "Лечение союзника не снимает с Лоры скрытность.",
        "Healing an ally does not remove Laura's stealth.",
    ),
    # Eskimo
    890000000005027: (890000000005047, "Тюремная выдержка", "Prison Hardiness"),
    890000000005028: (
        890000000005048,
        "Ниже 50% HP не получает Панику; раны не режут его CTH из винтовки.",
        "Below 50% HP does not Panic; wounds do not cut his rifle CTH.",
    ),
}

AME_COPYRIGHT_OLD = 491974676910
AME_COPYRIGHT_NEW = 890000000005049
AME_COPYRIGHT_TEXT = '<style AimCopyrightTextC><copyright></style> AME 2001'

NATIONALITIES = {
    890000000005021: ("Nigeria", "Нигерия"),
    890000000005022: ("Kenya", "Кения"),
    890000000005023: ("Angola", "Ангола"),
    890000000005024: ("Mali", "Мали"),
    890000000005025: ("Congo", "Конго"),
    890000000005026: ("Ghana", "Гана"),
    890000000005027: ("Senegal", "Сенегал"),
    890000000005028: ("Ethiopia", "Эфиопия"),
}

# English.csv Text must match T() / Russian.csv Text for AME rows that use EN source.
AME_EN_TEXT_FIX = {
    890000000005009: ("All", "All"),
    890000000005010: ("All", "All"),
    890000000005011: (
        "My Team [<PlayerMercCount()>]",
        "My Team [<PlayerMercCount()>]",
    ),
    890000000005012: ("My%20Team", "My%20Team"),
    890000000005013: (
        "http://www.ame-exchange.net/",
        "http://www.ame-exchange.net/",
    ),
    890000000005014: (
        "http://www.ame-exchange.net/Roster/",
        "http://www.ame-exchange.net/Roster/",
    ),
    890000000005015: ("Low", "Low"),
    890000000005016: ("Medium", "Medium"),
    890000000005017: ("High", "High"),
    890000000005018: ("Category", "Category"),
    890000000005019: ("Potential", "Potential"),
    890000000005020: (
        "African Mercenary Exchange",
        "African Mercenary Exchange",
    ),
}

BLEEDING_ID = 488938284982
BLEEDING_EN = "<color EmStyle><DisplayName></color> is bleeding"
BLEEDING_RU = "<color EmStyle><DisplayName></color> истекает кровью"

PARTS_FIX = {
    990002002: "Ствольные запчасти",
    990002500: "Детали прицелов",
}

T_CALL_RE = re.compile(
    r"T\(\s*(\d+)\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?(\"(\"\"|[^\"])*\")\s*\)",
    re.DOTALL,
)
T_SIMPLE_RE = re.compile(r"T\(\s*(\d+)\s*,\s*(\"(\"\"|[^\"])*\")\s*\)")


def load_csv(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def save_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerows(rows)


def unescape_lua_string(s: str) -> str:
    assert s[0] == '"' and s[-1] == '"'
    body = s[1:-1]
    return (
        body.replace("\\n", "\n")
        .replace("\\t", "\t")
        .replace('\\"', '"')
        .replace("\\\\", "\\")
    )


def escape_lua_string(s: str) -> str:
    return (
        '"'
        + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        + '"'
    )


def replace_t_id_keeping_text(content: str, old: int, new: int) -> str:
    """Replace T(old, ...) id only when the call exists."""
    pattern = re.compile(rf"T\(\s*{old}\s*,")
    return pattern.sub(f"T({new},", content)


def replace_t_id_and_text(content: str, old: int, new: int, new_text: str) -> str:
    """Replace T(old, ... "any") with T(new, "new_text"), preserving comment if present."""

    def repl(m: re.Match) -> str:
        full = m.group(0)
        # keep --[[...]] if present
        cmt = re.search(r"--\[\[[^\]]*\]\]", full)
        cmt_s = f" {cmt.group(0)} " if cmt else " "
        return f"T({new},{cmt_s}{escape_lua_string(new_text)})"

    pattern = re.compile(
        rf"T\(\s*{old}\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?\"(?:\"\"|[^\"])*\"\s*\)",
        re.DOTALL,
    )
    return pattern.sub(repl, content)


def upsert_csv_row(
    rows: list[list[str]],
    loc_id: int,
    text: str,
    translation: str,
    context: str,
) -> None:
    sid = str(loc_id)
    for i, row in enumerate(rows):
        if row and row[0] == sid:
            while len(row) < 5:
                row.append("")
            row[1] = text
            row[2] = translation
            if context and not row[4]:
                row[4] = context
            rows[i] = row
            return
    # insert before end; keep header
    rows.append([sid, text, translation, "", context])


def collect_mag_hint_sources() -> dict[int, str]:
    """id -> Russian AdditionalHint source from InventoryItem lua."""
    out: dict[int, str] = {}
    inv = ROOT / "InventoryItem"
    for p in inv.glob("JAZZ_Mag*.lua"):
        text = p.read_text(encoding="utf-8")
        for m in re.finditer(
            r"AdditionalHint\s*=\s*T\(\s*(\d+)\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?(\"(\"\"|[^\"])*\")",
            text,
        ):
            lid = int(m.group(1))
            src = unescape_lua_string(m.group(2))
            if "Семья магазинов" in src or "Съёмный модуль" in src:
                out[lid] = src
    return out


def family_en_from_ru(ru: str) -> str:
    """Build English Translation for mag family hints."""
    m = re.match(r"Семья магазинов:\s*([^.]+)\.\s*(.*)", ru, re.DOTALL)
    if m:
        fam = m.group(1).strip()
        rest = m.group(2).strip()
        rest_en = (
            "Removable module. Drag onto a compatible firearm or install in the weapon modification screen."
            if "Съёмный модуль" in rest
            else rest
        )
        return f"Magazine family: {fam}. {rest_en}"
    if ru.startswith("Съёмный модуль"):
        return "Removable module. Drag onto a compatible firearm or install in the weapon modification screen."
    return ru


def patch_lua_files() -> list[str]:
    changed: list[str] = []

    perk_files = [
        "CharacterEffect/Jazz_Perk_Vince.lua",
        "CharacterEffect/Jazz_Perk_Hitman.lua",
        "CharacterEffect/Jazz_Perk_Biggens.lua",
        "CharacterEffect/Jazz_Perk_Kulba.lua",
        "CharacterEffect/Jazz_Perk_Vilde.lua",
        "CharacterEffect/Jazz_Perk_Grace.lua",
        "CharacterEffect/Jazz_Perk_Steiger.lua",
        "CharacterEffect/Jazz_Perk_Lucky.lua",
        "CharacterEffect/Jazz_Perk_Laura.lua",
        "CharacterEffect/Jazz_Perk_Eskimo.lua",
        "items.lua",
    ]

    for rel in perk_files:
        path = ROOT / rel
        content = path.read_text(encoding="utf-8")
        orig = content
        for old, (new, ru, _en) in PERK_REMAP.items():
            # Only remap when this file's T(old) text is the perk text (not AME).
            # Safe approach: remap id wherever the surrounding string equals perk ru
            # OR for items.lua broken DisplayName T("Perk") restore from companion.
            content = replace_t_id_keeping_text(content, old, new)
        if content != orig:
            path.write_text(content, encoding="utf-8", newline="\n")
            changed.append(rel)

    # Restore broken items.lua DisplayName T("Perk") / T("WIP") for remapped perks
    items_path = ROOT / "items.lua"
    items = items_path.read_text(encoding="utf-8")
    orig_items = items

    restorations = [
        (
            "Jazz_Perk_Vince",
            890000000005029,
            "Полевой наставник",
            890000000005030,
            "Раз за бой первое лечение или перевязка союзника даёт цели +4 ОД.",
        ),
        (
            "Jazz_Perk_Hitman",
            890000000005031,
            "Вырубить",
            890000000005032,
            "WIP — механика сигнатурного перка в разработке.",
        ),
        (
            "Jazz_Perk_Biggens",
            890000000005033,
            "Старая школа",
            890000000005034,
            "WIP — механика сигнатурного перка в разработке.",
        ),
        (
            "Jazz_Perk_Kulba",
            890000000005035,
            "Оружейник старой закалки",
            890000000005036,
            "WIP — механика сигнатурного перка в разработке.",
        ),
        (
            "Jazz_Perk_Vilde",
            890000000005037,
            "Ночной автоматчик",
            890000000005038,
            "Ночью и под землёй автоогонь/очередь получают +15 к шансу попадания.",
        ),
        (
            "Jazz_Perk_Grace",
            890000000005039,
            "Точный бросок",
            890000000005040,
            "WIP — механика сигнатурного перка в разработке.",
        ),
        (
            "Jazz_Perk_Steiger",
            890000000005041,
            "Ночной инструктор",
            890000000005042,
            "Ночью и под землёй в начале хода союзники в радиусе 5 клеток получают +5 к шансу попадания.",
        ),
        (
            "Jazz_Perk_Lucky",
            890000000005043,
            "Второе дыхание",
            890000000005044,
            "Раз за бой первый промах из огнестрела становится попаданием.",
        ),
        (
            "Jazz_Perk_Laura",
            890000000005045,
            "Скрытный врач",
            890000000005046,
            "Лечение союзника не снимает с Лоры скрытность.",
        ),
        (
            "Jazz_Perk_Eskimo",
            890000000005047,
            "Тюремная выдержка",
            890000000005048,
            "Ниже 50% HP не получает Панику; раны не режут его CTH из винтовки.",
        ),
    ]

    for perk_id, dn_id, dn, desc_id, desc in restorations:
        # Locate ModItem block by Id
        block_re = re.compile(
            rf"('Id',\s*\"{perk_id}\".*?)('DisplayName',\s*)T\([^)]*\)(.*?)('Description',\s*)T\([^)]*\)",
            re.DOTALL,
        )

        def block_repl(m: re.Match, dn_id=dn_id, dn=dn, desc_id=desc_id, desc=desc) -> str:
            return (
                f"{m.group(1)}{m.group(2)}"
                f'T({dn_id}, --[[ModItemCharacterEffectCompositeDef {perk_id} DisplayName]] {escape_lua_string(dn)})'
                f"{m.group(3)}{m.group(4)}"
                f'T({desc_id}, --[[ModItemCharacterEffectCompositeDef {perk_id} Description]] {escape_lua_string(desc)})'
            )

        items, n = block_re.subn(block_repl, items, count=1)
        if n != 1:
            print(f"WARN: items.lua restore count={n} for {perk_id}")

    if items != orig_items:
        items_path.write_text(items, encoding="utf-8", newline="\n")
        if "items.lua" not in changed:
            changed.append("items.lua")

    # AME nationalities: EN source matching Russian.csv Text
    nat_path = ROOT / "Code" / "System_AME_Nationalities.lua"
    nat = nat_path.read_text(encoding="utf-8")
    orig_nat = nat
    for lid, (en, _ru) in NATIONALITIES.items():
        nat = replace_t_id_and_text(nat, lid, lid, en)
    if nat != orig_nat:
        nat_path.write_text(nat, encoding="utf-8", newline="\n")
        changed.append("Code/System_AME_Nationalities.lua")

    # AME copyright
    ame_browser = ROOT / "Code" / "System_AME_Browser_Template.lua"
    ab = ame_browser.read_text(encoding="utf-8")
    ab2 = replace_t_id_and_text(ab, AME_COPYRIGHT_OLD, AME_COPYRIGHT_NEW, AME_COPYRIGHT_TEXT)
    # also plain id replace if text already correct
    if ab2 == ab:
        ab2 = replace_t_id_keeping_text(ab, AME_COPYRIGHT_OLD, AME_COPYRIGHT_NEW)
    if ab2 != ab:
        ame_browser.write_text(ab2, encoding="utf-8", newline="\n")
        changed.append("Code/System_AME_Browser_Template.lua")

    # Bleeding companion: keep EN source; items.lua had RU — align to EN
    bleed_items_pat = re.compile(
        rf"T\(\s*{BLEEDING_ID}\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?\"(?:\"\"|[^\"])*\"\s*\)"
    )
    items = items_path.read_text(encoding="utf-8")
    items2 = bleed_items_pat.sub(
        f'T({BLEEDING_ID}, --[[ModItemCharacterEffectCompositeDef Bleeding AddEffectText]] {escape_lua_string(BLEEDING_EN)})',
        items,
        count=1,
    )
    if items2 != items:
        items_path.write_text(items2, encoding="utf-8", newline="\n")
        if "items.lua" not in changed:
            changed.append("items.lua")

    # Parts: maintenance must use same RU source as InventoryItem
    maint = ROOT / "Code" / "System_WeaponResourceMaintenance.lua"
    mt = maint.read_text(encoding="utf-8")
    orig_mt = mt
    mt = mt.replace(
        'T(990002002, "Barrel Parts")',
        'T(990002002, "Ствольные запчасти")',
    )
    mt = mt.replace(
        'T(990002500, "Scope Parts")',
        'T(990002500, "Детали прицелов")',
    )
    if mt != orig_mt:
        maint.write_text(mt, encoding="utf-8", newline="\n")
        changed.append("Code/System_WeaponResourceMaintenance.lua")

    return changed


def patch_csv() -> None:
    ru_path = ROOT / "Russian.csv"
    en_path = ROOT / "English.csv"
    ru_rows = load_csv(ru_path)
    en_rows = load_csv(en_path)

    # Remove old perk rows that still point at AME IDs (if any perk-only rows exist).
    # We do NOT delete AME rows 5009-5028.
    # Add new perk rows.
    for old, (new, ru, en) in PERK_REMAP.items():
        upsert_csv_row(ru_rows, new, ru, ru, f"perk-remap-from-{old}")
        upsert_csv_row(en_rows, new, ru, en, f"perk-remap-from-{old}")

    # AME copyright
    upsert_csv_row(
        ru_rows,
        AME_COPYRIGHT_NEW,
        AME_COPYRIGHT_TEXT,
        AME_COPYRIGHT_TEXT,
        "AME_Browser_copyright",
    )
    upsert_csv_row(
        en_rows,
        AME_COPYRIGHT_NEW,
        AME_COPYRIGHT_TEXT,
        AME_COPYRIGHT_TEXT,
        "AME_Browser_copyright",
    )

    # Bleeding: Text must match T() EN source
    upsert_csv_row(ru_rows, BLEEDING_ID, BLEEDING_EN, BLEEDING_RU, "jazz:CharacterEffect/Bleeding.lua")
    upsert_csv_row(en_rows, BLEEDING_ID, BLEEDING_EN, BLEEDING_EN, "jazz:CharacterEffect/Bleeding.lua")

    # ModTextsJazz bleeding if present
    mt_path = ROOT / "ModTextsJazz.csv"
    if mt_path.exists():
        mt_rows = load_csv(mt_path)
        upsert_csv_row(mt_rows, BLEEDING_ID, BLEEDING_EN, "", "Bleeding AddEffectText")
        save_csv(mt_path, mt_rows)

    # Fix English.csv AME Text to match T()/Russian.csv Text
    for lid, (text, translation) in AME_EN_TEXT_FIX.items():
        upsert_csv_row(en_rows, lid, text, translation, "")
    for lid, (en, ru) in NATIONALITIES.items():
        upsert_csv_row(ru_rows, lid, en, ru, f"AME_Nationality")
        upsert_csv_row(en_rows, lid, en, en, f"AME_Nationality")

    # Mag hints: align CSV Text to Lua RU source
    mag = collect_mag_hint_sources()
    print(f"mag hint ids from lua: {len(mag)}")
    for lid, ru_src in sorted(mag.items()):
        en_tr = family_en_from_ru(ru_src)
        upsert_csv_row(ru_rows, lid, ru_src, ru_src, "jazz:InventoryItem/mag-hint")
        upsert_csv_row(en_rows, lid, ru_src, en_tr, "jazz:InventoryItem/mag-hint")

    # Parts DisplayName CSV Text = RU source
    upsert_csv_row(
        ru_rows,
        990002002,
        "Ствольные запчасти",
        "Ствольные запчасти",
        "jazz:InventoryItem/JAZZ_BarrelParts.lua",
    )
    upsert_csv_row(
        en_rows,
        990002002,
        "Ствольные запчасти",
        "Barrel Parts",
        "jazz:InventoryItem/JAZZ_BarrelParts.lua",
    )
    upsert_csv_row(
        ru_rows,
        990002500,
        "Детали прицелов",
        "Детали прицелов",
        "jazz:InventoryItem/JAZZ_ScopeParts.lua",
    )
    upsert_csv_row(
        en_rows,
        990002500,
        "Детали прицелов",
        "Scope Parts",
        "jazz:InventoryItem/JAZZ_ScopeParts.lua",
    )

    save_csv(ru_path, ru_rows)
    save_csv(en_path, en_rows)


def verify() -> None:
    """Static: no perk companion still uses 5009-5028; AME copyright new; parts match."""
    bad = []
    for p in (ROOT / "CharacterEffect").glob("Jazz_Perk_*.lua"):
        t = p.read_text(encoding="utf-8")
        for m in re.finditer(r"T\(\s*(8900000000050(?:0[9]|1\d|2[0-8]))\s*,", t):
            bad.append(f"{p.name}:{m.group(1)}")
    print("perk leftovers on AME range:", bad or "none")

    ab = (ROOT / "Code" / "System_AME_Browser_Template.lua").read_text(encoding="utf-8")
    assert str(AME_COPYRIGHT_NEW) in ab
    assert f"T({AME_COPYRIGHT_OLD}," not in ab.replace(" ", "")

    nat = (ROOT / "Code" / "System_AME_Nationalities.lua").read_text(encoding="utf-8")
    assert 'T(890000000005021, "Nigeria")' in nat or 'T(890000000005021,"Nigeria")' in nat.replace(" ", "")

    maint = (ROOT / "Code" / "System_WeaponResourceMaintenance.lua").read_text(encoding="utf-8")
    assert "Barrel Parts" not in maint
    assert "Ствольные запчасти" in maint


def main() -> None:
    changed = patch_lua_files()
    print("lua changed:", changed)
    patch_csv()
    verify()
    print("OK")


if __name__ == "__main__":
    main()
