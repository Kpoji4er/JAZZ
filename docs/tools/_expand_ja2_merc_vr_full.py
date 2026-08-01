# -*- coding: utf-8 -*-
"""Expand stub Jazz_* VoiceResponse blocks to Colby-like full slot coverage.

Copies slot *structure* from Jazz_Colby (line counts per slot). For each missing
slot line, allocates a new T-id, inserts RU/EN loc rows, and leaves text as a
short placeholder (ship script fills audio from JA2 archive by slot).

Does NOT touch: Jazz_Colby, JAZZ_Merc_Spouke / done_manual, Merc_* workshop,
or mercs marked need_pack without profile_id.

Usage (jazz/):
  python docs/tools/_expand_ja2_merc_vr_full.py --dry-run
  python docs/tools/_expand_ja2_merc_vr_full.py --only ira,hobbit,blade
  python docs/tools/_expand_ja2_merc_vr_full.py
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz")
JU = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units")
MAP = JAZZ / "docs/design/mercs-ja12/_voice-source/jazz_to_ja2_profile.csv"
ITEMS = JU / "items.lua"
RU = JAZZ / "Russian.csv"
EN = JAZZ / "English.csv"
TID_START = 890000000007000

# Critical gameplay slots that stubs omit (must exist for audible combat).
# Counts match Jazz_Colby where possible; otherwise 1–3 lines.
EXPAND_SLOTS: OrderedDict[str, int] = OrderedDict(
    [
        ("Selection", 3),
        ("SelectionStealth", 3),
        ("Order", 3),
        ("CombatMovement", 3),
        ("CombatMovementStealth", 3),
        ("GroupOrder", 3),
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
        ("DeathGeneral", 1),
        ("Idle", 3),
        ("BecomeHidden", 2),
        ("LevelUp", 1),
        ("LootFound", 2),
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
        ("OverwatchSelection", 1),
        ("GasAreaSelection", 1),
        ("MissedByKillShot", 1),
        ("AnimalFound", 1),
        ("CombatTaskGiven", 1),
        ("CombatTaskCompleted", 1),
        ("CombatTaskFailed", 1),
        ("MockDislike1", 1),
        ("PraisesBuddy1", 1),
    ]
)

PLACEHOLDER_RU = {
    "Selection": "На связи.",
    "SelectionStealth": "Тихо.",
    "Order": "Есть.",
    "CombatMovement": "Двигаюсь.",
    "CombatMovementStealth": "Крадусь.",
    "GroupOrder": "С вами.",
    "AimAttack": "Есть цель!",
    "AimAttackStealth": "Тихо сниму.",
    "AimAttack_Low": "Сложный выстрел.",
    "AimAttack_LowStealth": "Плохой угол.",
    "OpponentFound": "Вижу их!",
    "ManyEnemiesSelection": "Их много!",
    "OpponentKilled": "Готов.",
    "NoAmmo": "Патроны кончились.",
    "AmmoLow": "Патроны на исходе!",
    "WeaponJammed": "Клин!",
    "Pain": "Аргх!",
    "Wounded": "Ранен!",
    "Downed": "Меня подбили…",
    "HeavilyWoundedSelection": "Плохо…",
    "CombatStartPlayer": "К бою!",
    "CombatStartDetected": "Контакт!",
    "CombatEndNoEnemies": "Чисто.",
    "CombatEndEnemiesRemain": "Ещё остались.",
    "DeathGeneral": "Конец…",
    "Idle": "Жду.",
    "BecomeHidden": "Прячусь.",
    "LevelUp": "Учусь.",
    "LootFound": "Интересно…",
    "DoorLocked": "Закрыто.",
    "Exhausted": "Устал…",
    "HeavyBreathing": "(пыхтит)",
    "HealReceived": "Спасибо.",
    "NotNow": "Не сейчас.",
    "ActivityFinished": "Готово.",
    "TakeCover": "В укрытие!",
    "ThrowGrenade": "Граната!",
    "Autofire": "Очередь!",
    "Climbing": "(лезет)",
    "Jumping": "(прыжок)",
    "Startled": "Что?!",
    "ThreatSelection": "Опасно!",
    "Overwatch": "Держу сектор.",
    "OverwatchSelection": "Наготове.",
    "GasAreaSelection": "(кашляет)",
    "MissedByKillShot": "Почти…",
    "AnimalFound": "Зверь!",
    "CombatTaskGiven": "Есть идея.",
    "CombatTaskCompleted": "Сделано.",
    "CombatTaskFailed": "Не вышло.",
    "MockDislike1": "Только не это.",
    "PraisesBuddy1": "Отличная работа.",
}

PLACEHOLDER_EN = {
    k: {
        "Selection": "Online.",
        "SelectionStealth": "Quiet.",
        "Order": "Roger.",
        "CombatMovement": "Moving.",
        "CombatMovementStealth": "Sneaking.",
        "GroupOrder": "With you.",
        "AimAttack": "Target!",
        "AimAttackStealth": "Quiet take-down.",
        "AimAttack_Low": "Tough shot.",
        "AimAttack_LowStealth": "Bad angle.",
        "OpponentFound": "I see them!",
        "ManyEnemiesSelection": "Too many!",
        "OpponentKilled": "Down.",
        "NoAmmo": "I'm out!",
        "AmmoLow": "Low ammo!",
        "WeaponJammed": "Jam!",
        "Pain": "Argh!",
        "Wounded": "I'm hit!",
        "Downed": "I'm down…",
        "HeavilyWoundedSelection": "Hurting…",
        "CombatStartPlayer": "Engage!",
        "CombatStartDetected": "Contact!",
        "CombatEndNoEnemies": "Clear.",
        "CombatEndEnemiesRemain": "Still hostiles.",
        "DeathGeneral": "That's it…",
        "Idle": "Waiting.",
        "BecomeHidden": "Hiding.",
        "LevelUp": "Learning.",
        "LootFound": "Hmm…",
        "DoorLocked": "Locked.",
        "Exhausted": "Tired…",
        "HeavyBreathing": "(panting)",
        "HealReceived": "Thanks.",
        "NotNow": "Not now.",
        "ActivityFinished": "Done.",
        "TakeCover": "Cover!",
        "ThrowGrenade": "Grenade!",
        "Autofire": "Full auto!",
        "Climbing": "(climbing)",
        "Jumping": "(jump)",
        "Startled": "What?!",
        "ThreatSelection": "Threat!",
        "Overwatch": "Watching.",
        "OverwatchSelection": "Ready.",
        "GasAreaSelection": "(coughs)",
        "MissedByKillShot": "Close…",
        "AnimalFound": "Animal!",
        "CombatTaskGiven": "Got an idea.",
        "CombatTaskCompleted": "Done.",
        "CombatTaskFailed": "Failed.",
        "MockDislike1": "Not this.",
        "PraisesBuddy1": "Nice work.",
    }[k]
    for k in PLACEHOLDER_RU
}

SKIP_UNITS = {
    "Jazz_Colby",  # gold — already full
    "JAZZ_Merc_Spouke",
    "Jazz_Spouke",
}


def esc_lua(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def esc_csv(s: str) -> str:
    if any(c in s for c in ',|"\n'):
        return '"' + s.replace('"', '""') + '"'
    return s


def load_ship_units() -> dict[str, dict]:
    out = {}
    if MAP.exists():
        with MAP.open(encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                uid = (row.get("unit_id") or "").strip()
                if uid:
                    out[uid] = row
    return out


def parse_vr_raw(items: str) -> dict[str, tuple[int, int, str, dict[str, list[tuple[int, str]]]]]:
    """uid -> (start, end, group, slots->[(tid,text)]) covering full PlaceObj."""
    out = {}
    for m in re.finditer(r"PlaceObj\('ModItemVoiceResponse',\s*\{", items):
        start = m.start()
        # find id =
        head = items[start : start + 80000]
        idm = re.search(r'\bid\s*=\s*"(Jazz_[A-Za-z0-9_]+|JAZZ_[A-Za-z0-9_]+)"', head)
        if not idm:
            continue
        uid = idm.group(1)
        # end at closing of this PlaceObj after id line
        after_id = start + idm.end()
        end_m = re.search(r"\}\),?", items[after_id : after_id + 200])
        if not end_m:
            continue
        end = after_id + end_m.end()
        body = items[start:end]
        gm = re.search(r'group\s*=\s*"([^"]+)"', body)
        group = gm.group(1) if gm else "MercenariesOld"
        slots: dict[str, list[tuple[int, str]]] = OrderedDict()
        for km in re.finditer(r"^\s*([A-Za-z0-9_]+)\s*=\s*TConcat\(\{", body, re.M):
            slot = km.group(1)
            if slot in ("group", "id"):
                continue
            s0 = km.end()
            nxt = re.search(r"^\s*[A-Za-z0-9_]+\s*=\s*", body[s0:], re.M)
            chunk = body[s0 : s0 + nxt.start()] if nxt else body[s0:]
            lines = []
            for tm in re.finditer(
                r'T\((\d+),\s*--\[\[[^\]]*\]\]\s*"((?:\\.|[^"\\])*)"', chunk
            ):
                lines.append((int(tm.group(1)), tm.group(2).encode().decode("unicode_escape") if "\\" in tm.group(2) else tm.group(2)))
            # simpler text extract
            lines = []
            for tm in re.finditer(r"T\((\d+),", chunk):
                tid = int(tm.group(1))
                # take comment+string roughly
                rest = chunk[tm.end() : tm.end() + 400]
                sm = re.search(r'\]\]\s*"((?:\\.|[^"\\])*)"', rest)
                text = sm.group(1) if sm else PLACEHOLDER_RU.get(slot, "…")
                text = text.replace('\\"', '"').replace("\\\\", "\\")
                lines.append((tid, text))
            if lines:
                slots[slot] = lines
        out[uid] = (start, end, group, slots)
    return out


def build_vr_block(
    uid: str,
    group: str,
    slots: OrderedDict[str, list[tuple[int, str]]],
    indent: str = "\t\t\t\t",
) -> str:
    i1 = indent
    i2 = indent + "\t"
    i3 = indent + "\t\t"
    parts = [f"{i1}PlaceObj('ModItemVoiceResponse', {{"]
    for slot, lines in slots.items():
        parts.append(f"{i2}{slot} = TConcat({{")
        for j, (tid, text) in enumerate(lines):
            comma = "," if j < len(lines) - 1 else ""
            parts.append(
                f"{i3}T({tid}, --[[ModItemVoiceResponse {uid} {slot} "
                f"VoiceResponse {slot} voice:{uid}]] \"{esc_lua(text)}\"){comma}"
            )
        parts.append(f"{i2}}}),")
    parts.append(f'{i2}group = "{group}",')
    parts.append(f'{i2}id = "{uid}",')
    parts.append(f"{i1}}}),")
    return "\n".join(parts)


def append_loc(path: Path, rows: list[tuple[int, str]], dry: bool) -> None:
    if dry or not rows:
        return
    raw = path.read_text(encoding="utf-8-sig")
    if not raw.endswith("\n"):
        raw += "\n"
    additions = [
        f"{tid},{esc_csv(text)},{esc_csv(text)},,jazz-units:items.lua:VoiceResponse"
        for tid, text in rows
    ]
    path.write_text(raw + "\n".join(additions) + "\n", encoding="utf-8")


def next_tid(items: str, ru: str, en: str, start: int) -> int:
    # JAZids are 8900… with variable width (15+ digits) — do not require fixed \d{12}.
    ids = [int(x) for x in re.findall(r"\b(8900\d+)\b", items + "\n" + ru + "\n" + en)]
    return max([start] + ([max(ids) + 1] if ids else []))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", type=str, default="")
    ap.add_argument(
        "--min-slots",
        type=int,
        default=40,
        help="Skip units that already have at least this many VR slots",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Expand even if slot count >= min-slots (still fills missing slots)",
    )
    args = ap.parse_args()

    only = {s.strip() for s in args.only.split(",") if s.strip()}
    ship = load_ship_units()
    items = ITEMS.read_text(encoding="utf-8")
    ru_text = RU.read_text(encoding="utf-8-sig") if RU.exists() else ""
    en_text = EN.read_text(encoding="utf-8-sig") if EN.exists() else ""
    tid = next_tid(items, ru_text, en_text, TID_START)
    vr = parse_vr_raw(items)

    # Expand Jazz_* stub VR. Prefer CSV shippable rows; also stub-only mercs
    # that already have some lines (hobbit/hitman etc. may lag CSV).
    targets = []
    for uid, (_a, _b, _g, slots) in sorted(vr.items()):
        if uid in SKIP_UNITS:
            continue
        if not uid.startswith("Jazz_"):
            continue
        if uid.startswith("Jazz_Recruter"):
            continue
        n_slots = len(slots)
        n_lines = sum(len(v) for v in slots.values())
        row = ship.get(uid)
        slug = (row.get("slug") if row else None) or uid.replace("Jazz_", "").lower()
        status = (row.get("status") if row else "") or ""
        pid = ((row.get("profile_id") if row else "") or "").strip()
        if only:
            key = slug
            if key not in only and uid not in only and uid.replace("Jazz_", "").lower() not in only:
                continue
        if status == "done_manual":
            print(f"SKIP {uid}: done_manual")
            continue
        if status in ("need_pack", "missing") and not pid:
            print(f"SKIP {uid}: need_pack / no profile")
            continue
        # Empty VR with no CSV profile — do not invent (Allik/Monk/… until mapped)
        if n_lines == 0 and not pid:
            print(f"SKIP {uid}: empty VR and no profile_id")
            continue
        if n_slots >= args.min_slots and not args.force:
            print(f"SKIP {uid}: already {n_slots} slots / {n_lines} lines")
            continue
        targets.append(uid)

    print(f"Expand targets: {len(targets)} next_tid={tid}")
    ru_rows: list[tuple[int, str]] = []
    en_rows: list[tuple[int, str]] = []
    # Apply from end so offsets stay valid
    replacements: list[tuple[int, int, str]] = []

    for uid in targets:
        start, end, group, slots = vr[uid]
        new_slots: OrderedDict[str, list[tuple[int, str]]] = OrderedDict()
        # Keep existing slots first (preserve texts/tids), then add missing
        for slot, need in EXPAND_SLOTS.items():
            existing = list(slots.get(slot, []))
            while len(existing) < need:
                text_ru = PLACEHOLDER_RU.get(slot, "…")
                text_en = PLACEHOLDER_EN.get(slot, "…")
                existing.append((tid, text_ru))
                ru_rows.append((tid, text_ru))
                en_rows.append((tid, text_en))
                tid += 1
            new_slots[slot] = existing[: max(need, len(existing))]
            # if existing had MORE than need, keep all
            if len(slots.get(slot, [])) > need:
                new_slots[slot] = list(slots[slot])
        # Preserve any extra slots not in EXPAND_SLOTS (buddy deaths, etc.)
        for slot, lines in slots.items():
            if slot not in new_slots:
                new_slots[slot] = lines

        block = build_vr_block(uid, group, new_slots)
        old_n = sum(len(v) for v in slots.values())
        new_n = sum(len(v) for v in new_slots.values())
        print(f"  {uid}: {old_n} -> {new_n} lines, {len(slots)} -> {len(new_slots)} slots")
        replacements.append((start, end, block))

    if args.dry_run:
        print(f"DRY: would patch {len(replacements)} VR blocks, add {len(ru_rows)} loc rows")
        return 0

    for start, end, block in sorted(replacements, key=lambda x: -x[0]):
        items = items[:start] + block + items[end:]

    ITEMS.write_text(items, encoding="utf-8")
    append_loc(RU, ru_rows, dry=False)
    append_loc(EN, en_rows, dry=False)
    print(f"Patched {len(replacements)} units; loc +{len(ru_rows)}; next_tid={tid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
