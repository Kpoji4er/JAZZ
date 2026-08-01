# -*- coding: utf-8 -*-
"""Integrate Shady Job Khalif trio voices (+ Benny/Simon UnitData stubs).

Source: C:\\Users\\SsAnd\\Downloads\\SJ\\data (speech/battlesnds/mercedt)
  066 = Simon Garandier
  067 = Alexandra «Benny» Benedict
  076 = Sergey «Grom» Gromov

Also notes: SJ 058 = Gaston (already shipped from UB); no WF AIM SPEECH banks.

Usage (jazz/):
  python docs/tools/_integrate_sj_khalif_mercs.py
  python docs/tools/_integrate_sj_khalif_mercs.py --skip-create  # only ship grom
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
SJ = Path(r"C:\Users\SsAnd\Downloads\SJ\data")
CACHE = JAZZ / "docs/design/mercs-ja12/_voice-source/_sj_cache"
MAP = JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv"
SJ_MERCEDT = JAZZ / "docs/design/mercs-ja12/_voice-source/sj-mercedt"
ITEMS = JU / "items.lua"
RU = JAZZ / "Russian.csv"
EN = JAZZ / "English.csv"

sys.path.insert(0, str(JAZZ / "docs/tools"))
from _extract_ja2_mercedt import decode_edt  # noqa: E402
from _ship_ja2_merc_voices import (  # noqa: E402
    find_ffmpeg,
    parse_vr_blocks,
    pick_stems,
    wav_to_opus,
)

SLOT_LINES = [
    ("Selection", ["041", "044", "078"], "На связи.", "Online."),
    ("AimAttack", ["000", "001", "002"], "Есть цель!", "Target!"),
    ("AimAttack", ["001", "002", "027"], "В бой!", "Engage!"),
    ("OpponentKilled", ["027", "015", "062"], "Готов.", "Down."),
    ("DeathGeneral", ["014", "016", "077"], "Конец...", "That's it..."),
    ("Downed", ["014", "020", "024"], "Ранен!", "I'm hit!"),
    ("AmmoLow", ["013", "012"], "Патроны!", "Low ammo!"),
    ("CombatStartDetected", ["001", "002", "000"], "Контакт!", "Contact!"),
    ("Idle", ["035", "044", "045"], "Жду.", "Waiting."),
    ("LevelUp", ["046", "053", "035"], "Учусь.", "Learning."),
    ("MockDislike1", ["039", "040", "064"], "Только не это.", "Not this."),
    ("PraisesBuddy1", ["051", "053", "052"], "Отличная работа.", "Nice work."),
]


def ensure_cache() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    for sub in ("speech", "battlesnds", "mercedt"):
        (CACHE / sub).mkdir(exist_ok=True)
    for pid in ("058", "066", "067", "076"):
        for folder, exts in (
            ("speech", (".wav", ".WAV", ".gap")),
            ("battlesnds", (".wav", ".WAV")),
        ):
            src = SJ / folder
            for p in src.glob(f"{pid}_*"):
                if p.suffix in exts or p.suffix.lower() == ".wav":
                    dest = CACHE / folder / p.name
                    if not dest.exists():
                        shutil.copy2(p, dest)
        edt = SJ / "mercedt" / f"{pid}.edt"
        if edt.exists():
            shutil.copy2(edt, CACHE / "mercedt" / edt.name)
    g = SJ / "speech" / "Gromov_with.WAV"
    if g.exists():
        shutil.copy2(g, CACHE / "speech" / g.name)


def export_mercedt_csv() -> None:
    SJ_MERCEDT.mkdir(parents=True, exist_ok=True)
    nicks = {"058": "Gaston", "066": "Simon", "067": "Benny", "076": "Gromov"}
    for pid, nick in nicks.items():
        edt = CACHE / "mercedt" / f"{pid}.edt"
        if not edt.exists():
            edt = SJ / "mercedt" / f"{pid}.edt"
        lines = decode_edt(edt.read_bytes())
        per = SJ_MERCEDT / f"{pid}_{nick}.csv"
        with per.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["line", "text"])
            for i, t in enumerate(lines):
                w.writerow([f"{i:03d}", t])


def update_map_csv() -> None:
    with MAP.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    fields = ["slug", "unit_id", "profile_id", "speech_source", "status", "notes"]
    clean: list[dict[str, str]] = []
    for r in rows:
        clean.append({k: (r.get(k) or "") for k in fields})
    by = {r["slug"]: r for r in clean}

    def upsert(slug: str, **kw):
        if slug in by:
            by[slug].update(kw)
        else:
            row = {k: "" for k in fields}
            row["slug"] = slug
            row.update(kw)
            clean.append(row)
            by[slug] = row

    upsert(
        "grom",
        unit_id="Jazz_Grom",
        profile_id="076",
        speech_source="sj_folder",
        status="shipped",
        notes="SJ Sergey Gromov; speech+battle 076_*; Gromov_with.WAV extra",
    )
    upsert(
        "benny",
        unit_id="Jazz_Benny",
        profile_id="067",
        speech_source="sj_folder",
        status="ready",
        notes="SJ Alexandra Benedict / Benny; female lockpick+explosives; buddy Simon",
    )
    upsert(
        "simon",
        unit_id="Jazz_Simon",
        profile_id="066",
        speech_source="sj_folder",
        status="ready",
        notes="SJ Simon Garandier / Грандье; sniper loner; buddy Benny",
    )
    if "gaston" in by:
        note = by["gaston"].get("notes") or ""
        if "SJ 058" not in note:
            by["gaston"]["notes"] = note + "; also present as SJ speech 058"

    with MAP.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(clean)
    print("Updated jazz_to_ja2_profile.csv")


def patch_ship_script() -> None:
    path = JAZZ / "docs/tools/_ship_ja2_merc_voices.py"
    text = path.read_text(encoding="utf-8")
    if "sj_folder" in text and "SJ_FOLDER" in text:
        print("ship script already has sj_folder")
        return
    if "SJ_FOLDER" not in text:
        text = text.replace(
            "UB_WF_FOLDER = (",
            "SJ_FOLDER = JAZZ / \"docs/design/mercs-ja12/_voice-source/_sj_cache\"\n"
            "UB_WF_FOLDER = (",
        )
    if 'if source == "ub_wildfire_folder":' in text and "sj_folder" not in text:
        text = text.replace(
            'if source == "ub_wildfire_folder":',
            'if source == "sj_folder":\n'
            "        return [SJ_FOLDER] if SJ_FOLDER.exists() else []\n"
            '    if source == "ub_wildfire_folder":',
        )
    # allow status ready after create
    if '"benny"' not in text:
        text = text.replace(
            '    "grom",\n',
            '    "grom",\n    "benny",\n    "simon",\n',
        )
    path.write_text(text, encoding="utf-8")
    print("Patched _ship_ja2_merc_voices.py for sj_folder")


def load_sj_lines(pid: str) -> dict[str, str]:
    files = list(SJ_MERCEDT.glob(f"{pid}_*.csv"))
    out: dict[str, str] = {}
    if not files:
        return out
    with files[0].open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            t = (row.get("text") or "").strip()
            if t:
                out[row["line"].zfill(3)] = t
    return out


def pick_text(lines: dict[str, str], prefs: list[str], fb: str) -> str:
    for p in prefs:
        t = lines.get(p.zfill(3))
        if t and len(t) < 160:
            return t
    for p in prefs:
        t = lines.get(p.zfill(3))
        if t:
            return t[:120]
    return fb


def next_tid(items: str) -> int:
    existing = [int(x) for x in re.findall(r"T\((8900\d+),", items)]
    return max(existing) + 1 if existing else 890000000007000


def esc_lua(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def build_vr(unit: str, entries: list[tuple[str, int, str]]) -> str:
    by: dict[str, list[tuple[int, str]]] = {}
    order: list[str] = []
    for slot, tid, text in entries:
        if slot not in by:
            order.append(slot)
            by[slot] = []
        by[slot].append((tid, text))
    parts = ["\t\t\t\tPlaceObj('ModItemVoiceResponse', {"]
    for slot in order:
        parts.append(f"\t\t\t\t\t{slot} = TConcat({{")
        lines = by[slot]
        for i, (tid, text) in enumerate(lines):
            comma = "," if i < len(lines) - 1 else ""
            parts.append(
                f"\t\t\t\t\t\tT({tid}, --[[ModItemVoiceResponse {unit} {slot} "
                f"VoiceResponse {slot} voice:{unit}]] \"{esc_lua(text)}\"){comma}"
            )
        parts.append("\t\t\t\t\t}),")
    parts.append('\t\t\t\t\tgroup = "MercenariesOld",')
    parts.append(f'\t\t\t\t\tid = "{unit}",')
    parts.append("\t\t\t\t}),")
    return "\n".join(parts)


def append_loc(rows: list[tuple[int, str, str]]) -> None:
    """rows: tid, ru, en"""

    def esc(s: str) -> str:
        if any(c in s for c in ',|"\n'):
            return '"' + s.replace('"', '""') + '"'
        return s

    for path, idx in ((RU, 1), (EN, 2)):
        raw = path.read_text(encoding="utf-8-sig")
        if not raw.endswith("\n"):
            raw += "\n"
        adds = []
        for tid, ru, en in rows:
            text = ru if idx == 1 else en
            adds.append(
                f"{tid},{esc(text)},{esc(text)},,jazz-units:items.lua:VoiceResponse"
            )
        path.write_text(raw + "\n".join(adds) + "\n", encoding="utf-8")


def create_merc_folder(
    items: str,
    *,
    unit: str,
    tid_start: int,
    stats: dict,
    lines: dict[str, str],
) -> tuple[str, int, list[tuple[int, str, str]]]:
    """Insert ModItemFolder after Jazz_Eskimo block. Returns new items, next tid, loc rows."""
    if f'id = "{unit}"' in items or f"'Id', \"{unit}\"" in items:
        print(f"{unit} already in items.lua")
        return items, tid_start, []

    tid = tid_start
    loc: list[tuple[int, str, str]] = []

    def take(ru: str, en: str) -> int:
        nonlocal tid
        cur = tid
        loc.append((cur, ru, en))
        tid += 1
        return cur

    name_t = take(stats["name_ru"], stats["name_en"])
    nick_t = take(stats["nick_ru"], stats["nick_en"])
    caps_t = take(stats["caps_ru"], stats["caps_en"])
    bio_t = take("work in progress", "work in progress")
    title_t = take(stats["title_ru"], stats["title_en"])
    email_t = take(stats["email"], stats["email"])
    snype_t = take(stats["snype"], stats["snype"])
    off_t = take(stats["offline_ru"], stats["offline_en"])
    greet_t = take(stats["greet_ru"], stats["greet_en"])
    restart_t = take("Связь прервалась.", "Connection lost.")
    idle_t = take("Жду.", "Waiting.")
    part_t = take("Идём.", "Let's go.")
    rehire_i = take("Контракт заканчивается?", "Contract ending?")
    rehire_o = take("Остаюсь.", "Staying.")

    vr_entries: list[tuple[str, int, str]] = []
    for slot, prefs, ru_fb, en_fb in SLOT_LINES:
        ru = pick_text(lines, prefs, ru_fb)
        en = en_fb
        vr_entries.append((slot, tid, ru))
        loc.append((tid, ru, en))
        tid += 1
    vr_block = build_vr(unit, vr_entries)

    likes = ",\n\t\t\t\t".join(f'"{x}"' for x in stats["likes"])
    dislikes = (
        ",\n\t\t\t\t".join(f'"{x}"' for x in stats["dislikes"])
        if stats["dislikes"]
        else ""
    )
    dislikes_block = (
        f"\t\t\t\t'Dislikes', {{\n\t\t\t\t{dislikes},\n\t\t\t\t}},\n"
        if stats["dislikes"]
        else "\t\t\t\t'Dislikes', {},\n"
    )
    perks = ",\n\t\t\t\t".join(f'"{x}"' for x in stats["perks"])

    # Placeholder portraits — Lynx/Shadow until SJ face convert
    portrait = stats["portrait"]
    big = stats["big_portrait"]

    folder = f"""\t\t\tPlaceObj('ModItemFolder', {{
\t\t\t\t'name', "{unit}",
\t\t\t}}, {{
\t\t\t\tPlaceObj('ModItemUnitDataCompositeDef', {{
\t\t\t\t\t'Group', "MercenariesOld",
\t\t\t\t\t'Id', "{unit}",
\t\t\t\t\t'object_class', "UnitData",
\t\t\t\t'Affiliation', "Locals",
\t\t\t\t'Health', {stats['Health']},
\t\t\t\t'Agility', {stats['Agility']},
\t\t\t\t'Dexterity', {stats['Dexterity']},
\t\t\t\t'Strength', {stats['Strength']},
\t\t\t\t'Wisdom', {stats['Wisdom']},
\t\t\t\t'Will', {stats['Will']},
\t\t\t\t'Leadership', {stats['Leadership']},
\t\t\t\t'Marksmanship', {stats['Marksmanship']},
\t\t\t\t'Mechanical', {stats['Mechanical']},
\t\t\t\t'Explosives', {stats['Explosives']},
\t\t\t\t'Medical', {stats['Medical']},
\t\t\t\t'Portrait', "{portrait}",
\t\t\t\t'BigPortrait', "{big}",
\t\t\t\t'IsMercenary', true,
\t\t\t\t'Name', T({name_t}, --[[ModItemUnitDataCompositeDef {unit} Name]] "{esc_lua(stats['name_ru'])}"),
\t\t\t\t'Nick', T({nick_t}, --[[ModItemUnitDataCompositeDef {unit} Nick]] "{esc_lua(stats['nick_ru'])}"),
\t\t\t\t'AllCapsNick', T({caps_t}, --[[ModItemUnitDataCompositeDef {unit} AllCapsNick]] "{esc_lua(stats['caps_ru'])}"),
\t\t\t\t'Bio', T({bio_t}, --[[ModItemUnitDataCompositeDef {unit} Bio]] "work in progress"),
\t\t\t\t'Nationality', "{stats['nationality']}",
\t\t\t\t'Title', T({title_t}, --[[ModItemUnitDataCompositeDef {unit} Title]] "{esc_lua(stats['title_ru'])}"),
\t\t\t\t'Email', T({email_t}, --[[ModItemUnitDataCompositeDef {unit} Email]] "{stats['email']}"),
\t\t\t\t'snype_nick', T({snype_t}, --[[ModItemUnitDataCompositeDef {unit} snype_nick]] "{stats['snype']}"),
\t\t\t\t'Offline', {{ PlaceObj('ChatMessage', {{ 'Text', T({off_t}, --[[ModItemUnitDataCompositeDef {unit} Text Offline ChatMessage voice:{unit}]] "{esc_lua(stats['offline_ru'])}") }}) }},
\t\t\t\t'GreetingAndOffer', {{ PlaceObj('ChatMessage', {{ 'Text', T({greet_t}, --[[ModItemUnitDataCompositeDef {unit} Text GreetingAndOffer ChatMessage voice:{unit}]] "{esc_lua(stats['greet_ru'])}") }}) }},
\t\t\t\t'ConversationRestart', {{ PlaceObj('ChatMessage', {{ 'Text', T({restart_t}, --[[ModItemUnitDataCompositeDef {unit} Text ConversationRestart ChatMessage voice:{unit}]] "Связь прервалась.") }}) }},
\t\t\t\t'IdleLine', {{ PlaceObj('ChatMessage', {{ 'Text', T({idle_t}, --[[ModItemUnitDataCompositeDef {unit} Text IdleLine ChatMessage voice:{unit}]] "Жду.") }}) }},
\t\t\t\t'PartingWords', {{ PlaceObj('ChatMessage', {{ 'Text', T({part_t}, --[[ModItemUnitDataCompositeDef {unit} Text PartingWords ChatMessage voice:{unit}]] "Идём.") }}) }},
\t\t\t\t'RehireIntro', {{ PlaceObj('ChatMessage', {{ 'Text', T({rehire_i}, --[[ModItemUnitDataCompositeDef {unit} Text RehireIntro ChatMessage voice:{unit}]] "Контракт заканчивается?") }}) }},
\t\t\t\t'RehireOutro', {{ PlaceObj('ChatMessage', {{ 'Text', T({rehire_o}, --[[ModItemUnitDataCompositeDef {unit} Text RehireOutro ChatMessage voice:{unit}]] "Остаюсь.") }}) }},
\t\t\t\t'MedicalDeposit', "none",
\t\t\t\t'StartingSalary', 0,
\t\t\t\t'SalaryIncrease', 0,
\t\t\t\t'SalaryLv1', 0,
\t\t\t\t'SalaryMaxLv', 0,
\t\t\t\t'StartingLevel', {stats['StartingLevel']},
\t\t\t\t'CustomEquipGear', function (self, items)
\t\t\t\tself:TryEquip(items, "Handheld A", "Firearm")
\t\t\t\tself:TryEquip(items, "Handheld B", "Firearm")
\t\t\t\tend,
\t\t\t\t'MaxHitPoints', {stats['Health']},
\t\t\t\t'Likes', {{
\t\t\t\t{likes},
\t\t\t\t}},
{dislikes_block}\t\t\t\t'StartingPerks', {{
\t\t\t\t{perks},
\t\t\t\t}},
\t\t\t\t'AppearancesList', {{ PlaceObj('AppearanceWeight', {{ 'Preset', "{stats['appearance']}" }}) }},
\t\t\t\t'Equipment', {{ "Loot_JAZZ_{stats['loot_suffix']}" }},
\t\t\t\t'Tier', "{stats['Tier']}",
\t\t\t\t'Specialization', "{stats['Specialization']}",
\t\t\t\t'pollyvoice', "{stats['polly']}",
\t\t\t\t'gender', "{stats['gender']}",
\t\t\t\t'VoiceResponseId', "{unit}",
\t\t\t\t'FallbackMissingVR', "Ice",
\t\t\t\t'DaysUntilOnline', 0,
\t\t\t\t}}),
{vr_block}
\t\t\t\t}}),
"""

    # Insert before NewMercs folder
    marker = "\t\tPlaceObj('ModItemFolder', {\n\t\t\t'name', \"NewMercs\","
    if marker not in items:
        raise SystemExit("NewMercs marker not found")
    items = items.replace(marker, folder + marker, 1)
    return items, tid, loc


def write_unitdata_companion(unit: str, stats: dict, tid_map: dict[str, int]) -> None:
    path = JU / "UnitData" / f"{unit}.lua"
    likes = ", ".join(f'"{x}"' for x in stats["likes"])
    dislikes = ", ".join(f'"{x}"' for x in stats["dislikes"])
    perks = ",\n\t".join(f'"{x}"' for x in stats["perks"])
    content = f"""UndefineClass('{unit}')
DefineClass.{unit} = {{
\t__parents = {{ "UnitData" }},
\t__generated_by_class = "ModItemUnitDataCompositeDef",

\tobject_class = "UnitData",
\tAffiliation = "Locals",
\tHealth = {stats['Health']},
\tAgility = {stats['Agility']},
\tDexterity = {stats['Dexterity']},
\tStrength = {stats['Strength']},
\tWisdom = {stats['Wisdom']},
\tWill = {stats['Will']},
\tLeadership = {stats['Leadership']},
\tMarksmanship = {stats['Marksmanship']},
\tMechanical = {stats['Mechanical']},
\tExplosives = {stats['Explosives']},
\tMedical = {stats['Medical']},
\tPortrait = "{stats['portrait']}",
\tBigPortrait = "{stats['big_portrait']}",
\tIsMercenary = true,
\tName = T({tid_map['name']}, "[WIP] {stats['name_ru']}"),
\tNick = T({tid_map['nick']}, "{stats['nick_ru']}"),
\tAllCapsNick = T({tid_map['caps']}, "{stats['caps_ru']}"),
\tBio = T({tid_map['bio']}, "work in progress"),
\tNationality = "{stats['nationality']}",
\tTitle = T({tid_map['title']}, "{stats['title_ru']}"),
\tEmail = T({tid_map['email']}, "{stats['email']}"),
\tsnype_nick = T({tid_map['snype']}, "{stats['snype']}"),
\tMedicalDeposit = "none",
\tStartingSalary = 0,
\tSalaryIncrease = 0,
\tSalaryLv1 = 0,
\tSalaryMaxLv = 0,
\tStartingLevel = {stats['StartingLevel']},
\tMaxHitPoints = {stats['Health']},
\tLikes = {{ {likes} }},
\tDislikes = {{ {dislikes} }},
\tStartingPerks = {{
\t{perks},
\t}},
\tAppearancesList = {{ PlaceObj('AppearanceWeight', {{ 'Preset', "{stats['appearance']}" }}) }},
\tEquipment = {{ "Loot_JAZZ_{stats['loot_suffix']}" }},
\tTier = "{stats['Tier']}",
\tSpecialization = "{stats['Specialization']}",
\tpollyvoice = "{stats['polly']}",
\tgender = "{stats['gender']}",
\tVoiceResponseId = "{unit}",
\tFallbackMissingVR = "Ice",
\tDaysUntilOnline = 0,
}}
"""
    path.write_text(content, encoding="utf-8")
    print("Wrote", path)


def ship_merc(slug: str, unit: str, pid: str) -> tuple[int, int]:
    """Ship from SJ_FOLDER cache using same slot map as ship script."""
    # Import after patch
    import importlib

    ship = importlib.import_module("_ship_ja2_merc_voices")
    importlib.reload(ship)

    items = ITEMS.read_text(encoding="utf-8")
    vr = parse_vr_blocks(items)
    if unit not in vr:
        print(f"ship FAIL: no VR for {unit}")
        return 0, 1
    ffmpeg = find_ffmpeg()
    ok = fail = 0
    from collections import defaultdict

    slot_i: dict[str, int] = defaultdict(int)
    opus_cache: dict[str, Path] = {}
    for slot, tid in vr[unit]:
        stems = pick_stems(slot, slot_i[slot])
        slot_i[slot] += 1
        wav = None
        used = None
        for stem in stems:
            wav = ship.resolve_wav(pid, stem, {}, {}, "sj_folder")
            if wav:
                used = stem
                break
        if not wav:
            print(f"  FAIL {tid} {slot}")
            fail += 1
            continue
        dest = JU / "voices" / f"{tid}.opus"
        print(f"  {tid} {slot} <- {pid}_{used}")
        key = str(wav.resolve())
        if key not in opus_cache:
            tmp = CACHE / f"_opus_{wav.stem}.opus"
            if not wav_to_opus(ffmpeg, wav, tmp):
                fail += 1
                continue
            opus_cache[key] = tmp
        shutil.copy2(opus_cache[key], dest)
        ok += 1
    print(f"{slug}: ok={ok} fail={fail}")
    return ok, fail


def write_design_articles() -> None:
    design = JAZZ / "docs/design/mercs-ja12"
    benny = design / "benny.md"
    simon = design / "simon.md"
    if not benny.exists():
        benny.write_text(
            """---
status: planned
priority: medium
origin: shadyjob
unit_id: Jazz_Benny
portrait_id: Benny
affiliation: Locals
role: Explosives
tier: Veteran
specialization: ExplosiveExpert
gender: Female
nationality: USA
voice_source: shadyjob
starting_level: 5
will: 70
salary:
  starting: 0
  increase: 0
  lv1: 0
  max: 0
medical_deposit: none
haggling: none
executable: false
---

# Бенни — Александра «Бенни» Бенедикт

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Александра «Бенни» Бенедикт | Alexandra "Benny" Benedict |
| Nick | Бенни | Benny |
| AllCapsNick | БЕННИ | BENNY |
| Title | Взломщица с Халифа | Khalif Locksmith |
| Email | Benny@khalif.sj | Benny@khalif.sj |
| snype_nick | benny | benny |

## Bio

**RU:** Наёмница острова Халиф (Shady Job). Электроника и отмычки экспертного уровня, взрывчатка почти на потолке; меткость средняя — сама напоминает, что она взломщик, не снайпер. Работает в паре с Саймоном Гарандье; симпатизирует Рыси, может сблизиться с Тревором. Бесплатный найм на Халифе.

**EN:** Khalif-island hire from Shady Job. Elite electronics/lockpicking and near-max explosives; middling marksmanship — she reminds you she's a burglar, not a sniper. Partners with Simon Garandier; likes Lynx, can warm to Trevor. Free hire on Khalif.

## Stats (MercsSJ)

Health 91 · Agility 87 · Dexterity 100 · Strength 56 · Leadership 14 · Wisdom 99 · Marksmanship 73 · Mechanical 99 · Explosives 95 · Medical 28 · Level 5

## Voice

JA2 SJ profile **067** (`_sj_cache`, mercedt `067_Benny.csv`).
""",
            encoding="utf-8",
        )
        print("Wrote", benny)
    if not simon.exists():
        simon.write_text(
            """---
status: planned
priority: medium
origin: shadyjob
unit_id: Jazz_Simon
portrait_id: Simon
affiliation: Locals
role: Sniper
tier: Elite
specialization: Marksmen
gender: Male
nationality: France
voice_source: shadyjob
starting_level: 9
will: 75
salary:
  starting: 0
  increase: 0
  lv1: 0
  max: 0
medical_deposit: none
haggling: none
executable: false
---

# Саймон — Саймон Гарандье

## Identity

| Field | RU | EN |
| --- | --- | --- |
| Name | Саймон Гарандье | Simon Garandier |
| Nick | Саймон | Simon |
| AllCapsNick | САЙМОН | SIMON |
| Title | Снайпер с Халифа | Khalif Marksman |
| Email | Simon@khalif.sj | Simon@khalif.sj |
| snype_nick | simon | simon |

## Bio

**RU:** Наёмник острова Халиф (Shady Job). Скрытность и снайпер; меткость 100, одиночка по характеру. Самопредставление в боевых репликах: «Это сказал Саймон Грандье». Напарница — Александра Бенедикт; симпатизирует Потрошителю, может сблизиться с Лысым. Бесплатный найм на Халифе.

**EN:** Khalif-island hire from Shady Job. Stealth + sniper; Marksmanship 100, loner. Self-ID line: «That's what Simon Garandier said.» Partners with Alexandra Benedict; likes Reaper, can warm to Scully. Free hire on Khalif.

## Stats (MercsSJ)

Health 85 · Agility 84 · Dexterity 81 · Strength 80 · Leadership 26 · Wisdom 83 · Marksmanship 100 · Mechanical 35 · Explosives 39 · Medical 57 · Level 9

## Voice

JA2 SJ profile **066** (`_sj_cache`, mercedt `066_Simon.csv`).
""",
            encoding="utf-8",
        )
        print("Wrote", simon)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-create", action="store_true")
    args = ap.parse_args()

    ensure_cache()
    export_mercedt_csv()
    patch_ship_script()
    update_map_csv()
    write_design_articles()

    # Always ship Grom (existing UnitData)
    print("=== ship grom ===")
    ship_merc("grom", "Jazz_Grom", "076")

    if args.skip_create:
        return 0

    items = ITEMS.read_text(encoding="utf-8")
    tid = next_tid(items)
    all_loc: list[tuple[int, str, str]] = []

    benny_stats = {
        "name_ru": "[WIP] Александра «Бенни» Бенедикт",
        "name_en": '[WIP] Alexandra "Benny" Benedict',
        "nick_ru": "Бенни",
        "nick_en": "Benny",
        "caps_ru": "БЕННИ",
        "caps_en": "BENNY",
        "title_ru": "Взломщица с Халифа",
        "title_en": "Khalif Locksmith",
        "email": "Benny@khalif.sj",
        "snype": "benny",
        "offline_ru": "Бенни на линии позже.",
        "offline_en": "Benny offline.",
        "greet_ru": "Бенедикт. Говорите.",
        "greet_en": "Benedict. Talk.",
        "nationality": "USA",
        "gender": "Female",
        "polly": "Amy",
        "Health": 91,
        "Agility": 87,
        "Dexterity": 100,
        "Strength": 56,
        "Wisdom": 99,
        "Will": 70,
        "Leadership": 14,
        "Marksmanship": 73,
        "Mechanical": 99,
        "Explosives": 95,
        "Medical": 28,
        "StartingLevel": 5,
        "Tier": "Veteran",
        "Specialization": "ExplosiveExpert",
        "likes": ["Jazz_Simon", "Jazz_Lynx"],
        "dislikes": [],
        "perks": ["Stealthy", "MrFixit", "Throwing", "TrueGrit"],
        "appearance": "Lynx",  # temp female appearance until SJ face
        "loot_suffix": "Benny",
        "portrait": "Mod/Dv3mFVN/MercPortraits/Lynx.png",
        "big_portrait": "Mod/Dv3mFVN/MercPortraits/Lynx_Big.png",
    }
    simon_stats = {
        "name_ru": "[WIP] Саймон Гарандье",
        "name_en": "[WIP] Simon Garandier",
        "nick_ru": "Саймон",
        "nick_en": "Simon",
        "caps_ru": "САЙМОН",
        "caps_en": "SIMON",
        "title_ru": "Снайпер с Халифа",
        "title_en": "Khalif Marksman",
        "email": "Simon@khalif.sj",
        "snype": "simon",
        "offline_ru": "Гарандье недоступен.",
        "offline_en": "Garandier offline.",
        "greet_ru": "Саймон Грандье. Слушаю.",
        "greet_en": "Simon Garandier. Listening.",
        "nationality": "France",
        "gender": "Male",
        "polly": "Matthew",
        "Health": 85,
        "Agility": 84,
        "Dexterity": 81,
        "Strength": 80,
        "Wisdom": 83,
        "Will": 75,
        "Leadership": 26,
        "Marksmanship": 100,
        "Mechanical": 35,
        "Explosives": 39,
        "Medical": 57,
        "StartingLevel": 9,
        "Tier": "Elite",
        "Specialization": "Marksmen",
        "likes": ["Jazz_Benny", "Reaper"],
        "dislikes": [],
        "perks": ["Stealthy", "SteadyBreathing", "Deadeye", "TrueGrit"],
        "appearance": "Shadow",
        "loot_suffix": "Simon",
        "portrait": "Mod/Dv3mFVN/MercPortraits/Hitman.png",
        "big_portrait": "Mod/Dv3mFVN/MercPortraits/Hitman_Big.png",
    }

    # Ensure loot defs exist as aliases to a minimal existing loot if needed — use Knife via empty Equipment skip
    # Point Equipment to Loot_JAZZ_Ira as temporary if Benny loot missing
    for s in (benny_stats, simon_stats):
        loot_id = f"Loot_JAZZ_{s['loot_suffix']}"
        if loot_id not in items and f'Loot_JAZZ_{s["loot_suffix"]}' not in items:
            s["loot_suffix"] = "Ira"  # temporary shared loot until dedicated
            print(f"Using temp loot Loot_JAZZ_Ira for {s['nick_en']}")

    for unit, stats, pid in (
        ("Jazz_Benny", benny_stats, "067"),
        ("Jazz_Simon", simon_stats, "066"),
    ):
        lines = load_sj_lines(pid)
        before = tid
        items, tid, loc = create_merc_folder(
            items, unit=unit, tid_start=tid, stats=stats, lines=lines
        )
        all_loc.extend(loc)
        # tid_map for companion — first 14 identity tids
        id_tids = [t for t, _, _ in loc[:14]]
        keys = [
            "name",
            "nick",
            "caps",
            "bio",
            "title",
            "email",
            "snype",
            "off",
            "greet",
            "restart",
            "idle",
            "part",
            "rehire_i",
            "rehire_o",
        ]
        tid_map = {k: id_tids[i] for i, k in enumerate(keys) if i < len(id_tids)}
        write_unitdata_companion(unit, stats, tid_map)
        print(f"Created {unit} tids {before}..{tid-1}")

    ITEMS.write_text(items, encoding="utf-8")
    append_loc(all_loc)
    print(f"Wrote items + {len(all_loc)} loc rows")

    # mark ready→shipped after voice
    update_map_csv()  # benny/simon still ready
    # reload ship module after items write
    print("=== ship benny ===")
    ship_merc("benny", "Jazz_Benny", "067")
    print("=== ship simon ===")
    ship_merc("simon", "Jazz_Simon", "066")

    # mark shipped
    with MAP.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        if r["slug"] in ("benny", "simon", "grom"):
            r["status"] = "shipped"
            r["speech_source"] = "sj_folder"
    with MAP.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    print(
        "DONE. WF AIM not in SJ SPEECH. Gaston SJ-058 also in cache (already shipped from UB)."
    )
    print("NOTE: Benny/Simon use temp portraits/appearance/loot; metadata sync still needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
