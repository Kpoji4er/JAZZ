#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Jazz_AME_* VoiceResponse banks from enemy-donor remesh (JAZZ-UNITS-005).

Problem: AME slots pointed at LegionRaider / ArmySoldier / AnneLeMitrailleur —
those are enemy banks (mostly AI* slots) and lack hireable-merc phrases
(Selection, AimAttack, Order, …).

Solution: three shared Jazz-owned presets:
  Jazz_AME_Male_Low   ← LegionRaider phrases + alt voice takes (*-1.opus)
  Jazz_AME_Male_Hard  ← remesh ArmySoldier (vanilla English.hpk)
  Jazz_AME_Female     ← remesh AnneLeMitrailleur

Only remesh a player slot when donor has **suitable** takes (same-tone source
slots). Calm UI slots (Selection / Order / CombatMovement / Idle / …) are **not**
filled from BecomeAware («Enemies!») — if the enemy bank has no native line,
omit the slot (silence; UnitData FallbackMissingVR is Pain/AiDeath only and
points at LegionRaider/ArmySoldier/Anne — never Ice/Fox).

Combat remesh still OK where tone matches (AIAttack→AimAttack, Pain, etc.).
EN subtitles = donor line text; lines mentioning Legion/Major are skipped.
RU subtitles translate the audible donor phrase via `_ame_voice_subtitles_ru.py`.

Usage (jazz/):
  python docs/tools/_import_legion_raider_alt_voices.py   # once, if *-1.opus missing
  python docs/tools/_gen_ame_voice_responses.py --extract-voices
  python docs/tools/_gen_ame_voice_responses.py
  python docs/tools/_gen_ame_voice_responses.py --dry-run
"""
from __future__ import annotations

import argparse
import codecs
import csv
import re
import shutil
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path

from _ame_voice_subtitles_ru import russian_subtitle

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
JU = JAZZ.parent / "jazz-units"
JA3 = Path(r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3")
VR_SRC = JA3 / "ModTools" / "Src" / "Data" / "VoiceResponse"
VOICES_HPK = JA3 / "Local" / "Voices" / "English.hpk"
HPK = JA3 / "ModTools" / "hpk-v0.3.12-x86_64-pc-windows-msvc" / "hpk.exe"
EXTRACT = JAZZ / ".tmp" / "voices-en-extract"
ITEMS = JU / "items.lua"
VOICES_OUT = JU / "voices"
RU = JAZZ / "Russian.csv"
EN = JAZZ / "English.csv"
# Legion Raider alternate takes (same T-ids as vanilla, other voice).
ALT_LEGION_DIRS = [
    VOICES_OUT,  # already imported *-1.opus
    Path.home() / "Downloads" / "1" / "1",
    Path.home() / "Downloads" / "1",
]

SECTION = "JAZZ-UNITS-005-AME-VR"
ITEMS_BEGIN = f"-- {SECTION}-BEGIN"
ITEMS_END = f"-- {SECTION}-END"
LOC_BEGIN = f"# {SECTION}-LOC-BEGIN"
LOC_END = f"# {SECTION}-LOC-END"
AME_END_MARKER = "-- JAZZ-UNITS-005-AME-END"

# 5800–5913 were the unmarked legacy projection.  Keep the canonical,
# regeneration-safe bank in its own marked range.
TID_START = 890000000005914
VOICE_LOC_CONTEXT = "jazz-units:items.lua:VoiceResponse AME"

# preset_id, donor VoiceResponse id, unused_legacy, prefer_alt_opus (-1 takes)
BANKS: list[tuple[str, str, str, bool]] = [
    ("Jazz_AME_Male_Low", "LegionRaider", "LegionRaider", True),
    ("Jazz_AME_Male_Hard", "ArmySoldier", "ArmySoldier", False),
    ("Jazz_AME_Female", "AnneLeMitrailleur", "AnneLeMitrailleur", False),
]

# Player-merc slot coverage (same critical set as JA12 expand).
TARGET_SLOTS: OrderedDict[str, int] = OrderedDict(
    [
        ("Selection", 3),
        ("SelectionStealth", 2),
        ("Order", 3),
        ("CombatMovement", 3),
        ("CombatMovementStealth", 2),
        ("GroupOrder", 2),
        ("AimAttack", 3),
        ("AimAttackStealth", 2),
        ("AimAttack_Low", 1),
        ("AimAttack_LowStealth", 1),
        ("OpponentFound", 2),
        ("ManyEnemiesSelection", 1),
        ("OpponentKilled", 2),
        ("NoAmmo", 1),
        ("AmmoLow", 1),
        ("WeaponJammed", 1),
        ("Pain", 2),
        ("Wounded", 1),
        ("Downed", 1),
        ("HeavilyWoundedSelection", 1),
        ("CombatStartPlayer", 1),
        ("CombatStartDetected", 1),
        ("CombatEndNoEnemies", 1),
        ("CombatEndEnemiesRemain", 1),
        ("DeathGeneral", 2),
        ("Idle", 3),
        ("BecomeHidden", 2),
        ("LevelUp", 1),
        ("LootFound", 1),
        ("DoorLocked", 1),
        ("Exhausted", 1),
        ("HeavyBreathing", 1),
        ("HealReceived", 1),
        ("NotNow", 1),
        ("ActivityFinished", 1),
        ("TakeCover", 1),
        ("ThrowGrenade", 1),
        ("Autofire", 1),
        ("Climbing", 1),
        ("Jumping", 1),
        ("Startled", 1),
        ("ThreatSelection", 1),
        ("Overwatch", 1),
        ("GasAreaSelection", 1),
        ("AnimalFound", 1),
        ("MockDislike1", 1),
        ("PraisesBuddy1", 1),
    ]
)

# Calm hireable UI / satellite slots: enemy banks have no native takes.
# Do NOT remesh BecomeAware («Enemies!») / TacticalPressing into these —
# omit → silence (FallbackMissingVR is Pain/AiDeath only, not Select/Move).
_CALM_NATIVE_ONLY = (
    "Selection",
    "SelectionStealth",
    "Order",
    "CombatMovement",
    "CombatMovementStealth",
    "GroupOrder",
    "Idle",
    "BecomeHidden",
    "LevelUp",
    "LootFound",
    "DoorLocked",
    "HealReceived",
    "NotNow",
    "ActivityFinished",
    "MockDislike1",
    "PraisesBuddy1",
)

# Prefer these donor slots when filling a player slot (first hit wins pool).
# Calm slots: native name only (empty on Legion/Army/Anne → skip).
SLOT_SOURCES: dict[str, list[str]] = {
    **{s: [s] for s in _CALM_NATIVE_ONLY},
    "AimAttack": ["AIAttack", "TacticalKilling", "TacticalTaunt"],
    "AimAttackStealth": ["AIAttack", "TacticalKilling"],
    "AimAttack_Low": ["AILoseCover", "TacticalLoss", "AIAttack"],
    "AimAttack_LowStealth": ["TacticalCareful", "AILoseCover"],
    "OpponentFound": ["BecomeAware", "TacticalTaunt", "AIFlanked"],
    "ManyEnemiesSelection": ["AIFlanked", "TacticalPressing", "BecomeAware"],
    "OpponentKilled": ["TacticalKilling", "TacticalRevenge", "AIAttack"],
    "NoAmmo": ["AILoseCover", "TacticalLoss", "Wounded"],
    "AmmoLow": ["AILoseCover", "TacticalLoss", "Wounded"],
    "WeaponJammed": ["AILoseCover", "Startled", "Pain"],
    "Pain": ["Pain", "Wounded", "AIDeath"],
    "Wounded": ["Wounded", "Pain"],
    "Downed": ["Wounded", "Pain", "AIDeath"],
    "HeavilyWoundedSelection": ["Wounded", "Pain", "TacticalLoss"],
    "CombatStartPlayer": ["AIAttack", "TacticalPressing", "TacticalTaunt"],
    "CombatStartDetected": ["BecomeAware", "AIFlanked", "Startled"],
    "CombatEndNoEnemies": ["TacticalKilling", "TacticalTaunt", "AIAttack"],
    "CombatEndEnemiesRemain": ["TacticalPressing", "TacticalFocus", "TacticalTaunt"],
    "DeathGeneral": ["AIDeath", "Pain", "Wounded"],
    "Exhausted": ["HeavyBreathing", "Wounded", "Pain"],
    "HeavyBreathing": ["HeavyBreathing", "Pain"],
    "TakeCover": ["TakeCover", "AILoseCover", "TacticalCareful"],
    "ThrowGrenade": ["AIDoubleBarrel", "AIAttack", "TacticalTaunt"],
    "Autofire": ["AIAutofire", "AIAttack"],
    "Climbing": ["Climbing", "Jumping", "HeavyBreathing"],
    "Jumping": ["Jumping", "Climbing"],
    "Startled": ["Startled", "AIFlanked"],
    "ThreatSelection": ["AIFlanked", "TacticalPressing", "BecomeAware"],
    "Overwatch": ["TakeCover", "TacticalFocus"],
    "GasAreaSelection": ["AIGasAreaSelection", "HeavyBreathing", "Pain"],
    "AnimalFound": ["AIDeadAnimal", "Startled"],
}

PLACEHOLDER_RU = {
    "Selection": ["На связи.", "Слушаю.", "Готов."],
    "SelectionStealth": ["Тихо.", "Без шума."],
    "Order": ["Есть.", "Понял.", "Сделаю."],
    "CombatMovement": ["Двигаюсь.", "Иду.", "Перемещаюсь."],
    "CombatMovementStealth": ["Крадусь.", "Тихо иду."],
    "GroupOrder": ["С вами.", "Держимся вместе."],
    "AimAttack": ["Есть цель!", "Бью.", "Держу на мушке."],
    "AimAttackStealth": ["Тихо сниму.", "Без шума."],
    "AimAttack_Low": ["Сложный выстрел."],
    "AimAttack_LowStealth": ["Плохой угол."],
    "OpponentFound": ["Вижу их!", "Контакт справа!"],
    "ManyEnemiesSelection": ["Их много!"],
    "OpponentKilled": ["Готов.", "Лежит."],
    "NoAmmo": ["Патроны кончились!"],
    "AmmoLow": ["Патроны на исходе!"],
    "WeaponJammed": ["Клин!"],
    "Pain": ["Аргх!", "Ух!"],
    "Wounded": ["Ранен!"],
    "Downed": ["Меня подбили…"],
    "HeavilyWoundedSelection": ["Плохо…"],
    "CombatStartPlayer": ["К бою!"],
    "CombatStartDetected": ["Контакт!"],
    "CombatEndNoEnemies": ["Чисто."],
    "CombatEndEnemiesRemain": ["Ещё остались."],
    "DeathGeneral": ["Конец…", "Агх…"],
    "Idle": ["Жду.", "На месте.", "Спокоен."],
    "BecomeHidden": ["Прячусь.", "Низкий профиль."],
    "LevelUp": ["Учусь."],
    "LootFound": ["Интересно…"],
    "DoorLocked": ["Закрыто."],
    "Exhausted": ["Устал…"],
    "HeavyBreathing": ["(пыхтит)"],
    "HealReceived": ["Спасибо."],
    "NotNow": ["Не сейчас."],
    "ActivityFinished": ["Готово."],
    "TakeCover": ["В укрытие!"],
    "ThrowGrenade": ["Граната!"],
    "Autofire": ["Очередь!"],
    "Climbing": ["(лезет)"],
    "Jumping": ["(прыжок)"],
    "Startled": ["Что?!"],
    "ThreatSelection": ["Опасно!"],
    "Overwatch": ["Держу сектор."],
    "GasAreaSelection": ["(кашляет)"],
    "AnimalFound": ["Зверь!"],
    "MockDislike1": ["Только не это."],
    "PraisesBuddy1": ["Отличная работа."],
}

PLACEHOLDER_EN = {
    "Selection": ["Online.", "Listening.", "Ready."],
    "SelectionStealth": ["Quiet.", "Keep it down."],
    "Order": ["Roger.", "Understood.", "On it."],
    "CombatMovement": ["Moving.", "Going.", "Repositioning."],
    "CombatMovementStealth": ["Sneaking.", "Soft steps."],
    "GroupOrder": ["With you.", "Staying close."],
    "AimAttack": ["Target!", "Firing.", "Got the shot."],
    "AimAttackStealth": ["Quiet take-down.", "Silent."],
    "AimAttack_Low": ["Tough shot."],
    "AimAttack_LowStealth": ["Bad angle."],
    "OpponentFound": ["I see them!", "Contact right!"],
    "ManyEnemiesSelection": ["Too many!"],
    "OpponentKilled": ["Down.", "He's done."],
    "NoAmmo": ["I'm out!"],
    "AmmoLow": ["Low ammo!"],
    "WeaponJammed": ["Jam!"],
    "Pain": ["Argh!", "Ugh!"],
    "Wounded": ["I'm hit!"],
    "Downed": ["I'm down…"],
    "HeavilyWoundedSelection": ["Bad…"],
    "CombatStartPlayer": ["Engaging!"],
    "CombatStartDetected": ["Contact!"],
    "CombatEndNoEnemies": ["Clear."],
    "CombatEndEnemiesRemain": ["Still some left."],
    "DeathGeneral": ["That's it…", "Agh…"],
    "Idle": ["Waiting.", "Holding.", "Steady."],
    "BecomeHidden": ["Going quiet.", "Low profile."],
    "LevelUp": ["Learning."],
    "LootFound": ["Interesting…"],
    "DoorLocked": ["Locked."],
    "Exhausted": ["Tired…"],
    "HeavyBreathing": ["(panting)"],
    "HealReceived": ["Thanks."],
    "NotNow": ["Not now."],
    "ActivityFinished": ["Done."],
    "TakeCover": ["Cover!"],
    "ThrowGrenade": ["Grenade!"],
    "Autofire": ["Suppressing!"],
    "Climbing": ["(climbing)"],
    "Jumping": ["(jump)"],
    "Startled": ["What?!"],
    "ThreatSelection": ["Danger!"],
    "Overwatch": ["Watching the sector."],
    "GasAreaSelection": ["(coughing)"],
    "AnimalFound": ["Beast!"],
    "MockDislike1": ["Not this."],
    "PraisesBuddy1": ["Nice work."],
}


def sanitize_ame_line(text: str) -> str:
    """Strip Legion / Major propaganda from donor subtitles (AME hireables)."""
    if not text:
        return text
    s = text
    # Phrase-level first (order matters).
    replacements = [
        (r"Alerter! Alerter!", "Alerte! Alerte!"),
        (
            r"Remember the Major's teaching\.",
            "Remember the training.",
        ),
        (
            r"Fuck\. The Major will have our hides if we keep missing\.",
            "Fuck. We'll catch hell if we keep missing.",
        ),
        (
            r"The Major will be pleased\.",
            "The boss will be pleased.",
        ),
        (
            r"You regret facing the Legion now, yes\?",
            "You regret facing us now, yes?",
        ),
        (
            r"Get them! Make them pay! For the Legion!",
            "Get them! Make them pay!",
        ),
        (
            r"The Legion will be victorious this day!",
            "We'll be victorious this day!",
        ),
        (
            r"Now you know to fear the Legion!",
            "Now you know to fear us!",
        ),
        (r"For the Legion!", "Push forward!"),
        (r"For the Major!", "On me!"),
        (
            r"They will wipe us out\. Remember - if we die, the Major will come to hell and give our souls a beating\.",
            "They will wipe us out. Remember — if we die, nobody's coming to save us.",
        ),
        (
            r"if we die, the Major will come to hell and give our souls a beating",
            "if we die, nobody's coming to save us",
        ),
    ]
    for pat, rep in replacements:
        s = re.sub(pat, rep, s, flags=re.I)
    # Residual word scrub.
    s = re.sub(r"\bthe Major's\b", "the boss's", s, flags=re.I)
    s = re.sub(r"\bMajor's\b", "boss's", s, flags=re.I)
    s = re.sub(r"\bthe Major\b", "the boss", s, flags=re.I)
    s = re.sub(r"\bMajor\b", "boss", s, flags=re.I)
    s = re.sub(r"\bthe Legion\b", "us", s, flags=re.I)
    s = re.sub(r"\bLegion\b", "crew", s, flags=re.I)
    return s


def parse_donor(path: Path) -> dict[str, list[tuple[int, str]]]:
    text = path.read_text(encoding="utf-8")
    slots: dict[str, list[tuple[int, str]]] = {}
    for m in re.finditer(
        r"^\t([A-Za-z0-9_]+) = TConcat\(\{([\s\S]*?)^\t\}\),",
        text,
        re.M,
    ):
        slot, body = m.group(1), m.group(2)
        if slot in ("group", "id"):
            continue
        lines: list[tuple[int, str]] = []
        for tm in re.finditer(r'T\((\d+),[\s\S]*?"([^"]*)"', body):
            tid = int(tm.group(1))
            raw = tm.group(2).replace('\\"', '"').replace("\\\\", "\\")
            lines.append((tid, raw))
        if lines:
            slots[slot] = lines
    return slots


def line_banned(text: str) -> bool:
    """True for faction-specific donor audio unsuitable for shared AME hires."""
    return bool(
        re.search(
            r"\b(Legion|Major|Grand Chien|national symbols?)\b",
            text or "",
            re.I,
        )
    )


def has_alt_opus(donor_tid: int) -> bool:
    for d in ALT_LEGION_DIRS:
        if (d / f"{donor_tid}-1.opus").is_file():
            return True
    return False


def build_pool(
    donor: dict[str, list[tuple[int, str]]],
    slot: str,
) -> list[tuple[int, str]]:
    """Only SLOT_SOURCES — no BecomeAware dump into calm slots, no whole-bank fallback."""
    pool: list[tuple[int, str]] = []
    for src in SLOT_SOURCES.get(slot, [slot]):
        pool.extend(donor.get(src, []))
    return pool


def pick_donor_lines(
    donor: dict[str, list[tuple[int, str]]],
    slot: str,
    need: int,
    prefer_alt: bool = False,
) -> list[tuple[int, str]]:
    """Return up to `need` suitable unique takes. Empty = omit player slot."""
    pool = build_pool(donor, slot)
    if not pool:
        return []

    # Skip Legion/Major takes entirely (no banned-audio last resort).
    pool = [p for p in pool if not line_banned(p[1])]
    if not pool:
        return []

    if prefer_alt:
        with_alt = [p for p in pool if has_alt_opus(p[0])]
        if with_alt:
            seen = set(id(x) for x in with_alt)
            rest = [p for p in pool if id(p) not in seen]
            pool = with_alt + rest

    # Deduplicate by tid while preserving order.
    seen_tid: set[int] = set()
    unique: list[tuple[int, str]] = []
    for tid, text in pool:
        if tid in seen_tid:
            continue
        seen_tid.add(tid)
        unique.append((tid, text))

    # Do not pad/repeat to force `need` — fewer suitable takes → fewer lines.
    return unique[:need]


def lua_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def resolve_opus(donor_tid: int, prefer_alt: bool) -> Path | None:
    """Prefer *-1.opus alt takes when requested; else vanilla extract base."""
    if prefer_alt:
        for d in ALT_LEGION_DIRS:
            p = d / f"{donor_tid}-1.opus"
            if p.is_file():
                return p
    base = EXTRACT / f"{donor_tid}.opus"
    if base.is_file():
        return base
    # last chance: alt even when not preferred
    for d in ALT_LEGION_DIRS:
        p = d / f"{donor_tid}-1.opus"
        if p.is_file():
            return p
    return None


def build_vr_lua(
    preset_id: str,
    fallback: str,
    lines_by_slot: OrderedDict[str, list[tuple[int, str, str]]],
) -> str:
    """lines_by_slot[slot] = [(tid, ru, en), ...] — we embed EN as PlaceObj default text."""
    parts = [
        "\t\tPlaceObj('ModItemVoiceResponse', {",
        f'\t\t\tgroup = "Default",',
        f'\t\t\tid = "{preset_id}",',
    ]
    for slot, rows in lines_by_slot.items():
        if not rows:
            continue
        parts.append(f"\t\t\t{slot} = TConcat({{")
        for tid, _ru, en in rows:
            comment = (
                f"ModItemVoiceResponse {preset_id} {slot} "
                f"VoiceResponse {slot} voice:{preset_id}"
            )
            parts.append(
                f'\t\t\t\tT({tid}, --[[{comment}]] "{lua_escape(en)}"),'
            )
        parts.append("\t\t\t}),")
    parts.append("\t\t}),")
    return "\n".join(parts)


def wrap_vr_folder(vr_blocks: list[str]) -> str:
    inner = "\n".join(vr_blocks)
    return (
        "\tPlaceObj('ModItemFolder', {\n"
        '\t\t\'name\', "AME_VoiceResponses",\n'
        "\t}, {\n"
        f"{inner}\n"
        "\t}),"
    )


def replace_marked(text: str, begin: str, end: str, body: str) -> str:
    block = f"{begin}\n{body}\n{end}"
    if begin in text and end in text:
        return re.sub(
            re.escape(begin) + r".*?" + re.escape(end),
            block,
            text,
            count=1,
            flags=re.S,
        )
    # Prefer after AME unitdata end marker.
    if AME_END_MARKER in text:
        idx = text.find(AME_END_MARKER) + len(AME_END_MARKER)
        if text[idx : idx + 1] != "\n":
            return text[:idx] + "\n" + block + "\n" + text[idx:]
        return text[: idx + 1] + block + "\n" + text[idx + 1 :]
    anchor = "PlaceObj('ModItemTranslatedVoices'"
    idx = text.rfind(anchor)
    if idx >= 0:
        return text[:idx] + block + "\n\t" + text[idx:]
    return text.rstrip() + "\n" + block + "\n"


def free_managed_loc_ids(text: str, used: set[int]) -> None:
    """Allow stable ID reuse even after another CSV round-trip strips comments."""
    for line in text.splitlines():
        if not line.endswith("," + VOICE_LOC_CONTEXT):
            continue
        match = re.match(r"^(\d{12,}),", line)
        if match:
            used.discard(int(match.group(1)))


def upsert_loc(
    path: Path,
    rows_en: list[tuple[int, str]],
    rows_ru: list[tuple[int, str]] | None,
    dry: bool,
) -> None:
    """CSV: ID,Text,Translation,VoiceActor,Context (same as _inject_vr_stubs)."""
    if not path.exists():
        raise SystemExit(f"missing loc: {path}")
    raw = path.read_bytes()
    bom = raw.startswith(codecs.BOM_UTF8)
    text = raw[len(codecs.BOM_UTF8) if bom else 0 :].decode("utf-8")
    newline = "\r\n" if text.count("\r\n") > text.count("\n") - text.count("\r\n") else "\n"
    by_en = dict(rows_en)
    by_ru = dict(rows_ru) if rows_ru is not None else by_en
    body_lines = []
    for tid, en in rows_en:
        ru = by_ru.get(tid, en)

        def esc(s: str) -> str:
            if any(c in s for c in ",\"\n"):
                return '"' + s.replace('"', '""') + '"'
            return s

        body_lines.append(
            f"{tid},{esc(en)},{esc(ru)},,{VOICE_LOC_CONTEXT}"
        )
    body = newline.join(body_lines)
    block = f"{LOC_BEGIN}{newline}{body}{newline}{LOC_END}"
    if LOC_BEGIN in text and LOC_END in text:
        text = re.sub(
            re.escape(LOC_BEGIN)
            + r".*?"
            + re.escape(LOC_END)
            + r"(?:\r?\n)?",
            "",
            text,
            count=1,
            flags=re.S,
        )
    # Remove the pre-marker projection and any interrupted generated pass.
    text = "".join(
        line
        for line in text.splitlines(keepends=True)
        if not line.rstrip("\r\n").endswith("," + VOICE_LOC_CONTEXT)
    )
    if text and not text.endswith(("\r", "\n")):
        text += newline
    text = text + block + newline
    if not dry:
        payload = text.encode("utf-8")
        path.write_bytes((codecs.BOM_UTF8 + payload) if bom else payload)


def extract_voices() -> None:
    if not HPK.exists():
        raise SystemExit(f"hpk not found: {HPK}")
    if not VOICES_HPK.exists():
        raise SystemExit(f"Voices hpk not found: {VOICES_HPK}")
    if EXTRACT.exists() and any(EXTRACT.glob("*.opus")):
        print(f"extract cache exists: {EXTRACT} ({len(list(EXTRACT.glob('*.opus')))} opus)")
        return
    EXTRACT.mkdir(parents=True, exist_ok=True)
    print(f"extracting {VOICES_HPK} → {EXTRACT}")
    subprocess.run([str(HPK), "extract", str(VOICES_HPK), str(EXTRACT)], check=True)
    print(f"done: {len(list(EXTRACT.glob('*.opus')))} opus")


def next_tid(used: set[int]) -> int:
    tid = TID_START
    while tid in used:
        tid += 1
    used.add(tid)
    return tid


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--extract-voices", action="store_true")
    args = ap.parse_args()

    if args.extract_voices:
        extract_voices()
        return 0

    if not EXTRACT.exists() or not any(EXTRACT.glob("*.opus")):
        if args.dry_run:
            print("WARN: no extract cache — dry-run will report missing base opus")
        else:
            print("WARN: no extract cache — running extract first")
            extract_voices()

    used_tids: set[int] = set()
    # Reserve against existing loc IDs in RU if present.
    if RU.exists():
        ru_text = RU.read_text(encoding="utf-8-sig")
        for m in re.finditer(r"^(?:# )?(\d{12,})", ru_text, re.M):
            used_tids.add(int(m.group(1)))
        free_managed_loc_ids(ru_text, used_tids)

    all_loc_ru: list[tuple[int, str]] = []
    all_loc_en: list[tuple[int, str]] = []
    vr_blocks: list[str] = []
    opus_copied = 0
    opus_missing = 0
    opus_alt = 0
    opus_base = 0

    VOICES_OUT.mkdir(parents=True, exist_ok=True)

    for preset_id, donor_id, fallback, prefer_alt in BANKS:
        donor_path = VR_SRC / f"{donor_id}.lua"
        if not donor_path.exists():
            raise SystemExit(f"donor VR missing: {donor_path}")
        donor = parse_donor(donor_path)
        print(
            f"{preset_id}: donor={donor_id} slots={len(donor)} prefer_alt={prefer_alt}"
        )

        lines_by_slot: OrderedDict[str, list[tuple[int, str, str]]] = OrderedDict()
        skipped: list[str] = []
        for slot, need in TARGET_SLOTS.items():
            donor_lines = pick_donor_lines(donor, slot, need, prefer_alt=prefer_alt)
            if not donor_lines:
                skipped.append(slot)
                continue
            en_pool = PLACEHOLDER_EN.get(slot, ["…"])
            rows: list[tuple[int, str, str]] = []
            for i, (src_tid, src_text) in enumerate(donor_lines):
                if line_banned(src_text or ""):
                    raise SystemExit(
                        f"banned donor audio slipped through: {preset_id}.{slot} "
                        f"tid={src_tid} {src_text!r}"
                    )
                tid = next_tid(used_tids)
                # EN = clean donor phrase (Legion/Major takes filtered out of pool).
                en = sanitize_ame_line((src_text or "").strip()) or en_pool[i % len(en_pool)]
                try:
                    ru = russian_subtitle(en, preset_id)
                except KeyError as error:
                    raise SystemExit(str(error)) from error
                rows.append((tid, ru, en))
                all_loc_ru.append((tid, ru))
                all_loc_en.append((tid, en))
                src = resolve_opus(src_tid, prefer_alt)
                dst = VOICES_OUT / f"{tid}.opus"
                if src is not None:
                    if not args.dry_run:
                        shutil.copy2(src, dst)
                    opus_copied += 1
                    if src.name.endswith("-1.opus"):
                        opus_alt += 1
                    else:
                        opus_base += 1
                else:
                    opus_missing += 1
                    print(f"  MISSING opus donor {src_tid} for {preset_id}.{slot}")
            lines_by_slot[slot] = rows
        if skipped:
            print(f"  omit (no suitable): {', '.join(skipped)}")

        vr_blocks.append(build_vr_lua(preset_id, fallback, lines_by_slot))

    body = wrap_vr_folder(vr_blocks)
    items_text = ITEMS.read_text(encoding="utf-8")
    new_items = replace_marked(items_text, ITEMS_BEGIN, ITEMS_END, body)

    print(f"opus copied={opus_copied} missing={opus_missing} alt={opus_alt} base={opus_base}")
    print(f"loc lines={len(all_loc_ru)}")
    print(f"items bytes {len(items_text)} -> {len(new_items)}")

    if args.dry_run:
        print("dry-run: no writes")
        return 0

    ITEMS.write_text(new_items, encoding="utf-8")
    upsert_loc(RU, all_loc_en, all_loc_ru, dry=False)
    upsert_loc(EN, all_loc_en, all_loc_en, dry=False)
    print(f"wrote {ITEMS}")
    print(f"wrote loc markers in {RU.name} / {EN.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
