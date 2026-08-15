# -*- coding: utf-8 -*-
"""Sync jazz-units mod-only T() IDs into runtime loctables.

Vanilla AIM VoiceResponse IDs stay in Game.csv (never copied into JAZZ CSV).
Raven/Thor/Vicki/Wolf must keep vanilla T-ids — restore via
`_restore_vanilla_aim_vr_ids.py` before this sync.

1. Append missing *mod-only* IDs (8900* JA12 VR, Cougar/Gamos holes) to jazz
   Russian.csv / English.csv.
2. Write jazz-units/Russian.csv and fill jazz-units/English.csv so the Units
   editor loctable resolves (was English-only → Missing text).

Usage (from jazz/):
  python docs/tools/_restore_vanilla_aim_vr_ids.py
  python docs/tools/_purge_restored_aim_vr_loc.py
  python docs/tools/_sync_units_vr_loctables.py
"""
from __future__ import annotations

import csv
import io
import os
import re
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"

FIELDS = ["ID", "Text", "Translation", "VoiceActor", "Context"]
T_RE = re.compile(
    r'T\((\d{6,})\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?"((?:\\.|[^"\\])*)"',
    re.S,
)
CYR_RE = re.compile(r"[А-Яа-яЁё]")


def find_game_csv() -> Path | None:
    roots: list[Path] = []
    env = os.environ.get("JA3_ROOT")
    if env:
        roots.append(Path(env))
    for drive in "CDEF":
        roots.append(Path(rf"{drive}:\SteamLibrary\steamapps\common\Jagged Alliance 3"))
        roots.append(Path(rf"{drive}:\Program Files (x86)\Steam\steamapps\common\Jagged Alliance 3"))
    for root in roots:
        p = root / "ModTools" / "Game.csv"
        if p.is_file():
            return p
    return None


def load_game_ids(path: Path | None) -> set[str]:
    if not path:
        return set()
    ids: set[str] = set()
    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.reader(f):
            if row and row[0].isdigit():
                ids.add(row[0])
    return ids


def is_mod_only(tid: str, game_ids: set[str]) -> bool:
    """Vanilla Game.csv IDs stay vanilla — never copy them into JAZZ CSV."""
    if tid.startswith("8900"):
        return True
    if not game_ids:
        return False
    return tid not in game_ids

# Lua-only VR lines (not in jazz CSV / units EN). Keep EN next to RU.
LUA_EN: dict[str, str] = {
    "890000000006500": "Task complete. Awaiting orders.",
    "890000000006501": "There's always something to get better at.",
    "890000000006502": "Anything but that.",
    "890000000006503": "Just another example of how well Wolf works.",
    "890000000006504": "I'm on the job now.",
    "890000000006505": "Pathetic!",
    "890000000006506": "I see them! I see those wretches!",
    "890000000006507": "Farewell, wretch!",
    "890000000006508": "It hurts. It hurts a lot.",
    "890000000006509": "It hurts, Mr. Jack.",
    "890000000006510": "Looking for a bullet. No more bullet.",
    "890000000006514": "Anything but that.",
    "890000000006515": "Excellent work.",


def unescape_lua(s: str) -> str:
    return (
        s.replace("\\n", "\n")
        .replace("\\t", "\t")
        .replace('\\"', '"')
        .replace("\\\\", "\\")
    )


def read_runtime(path: Path) -> tuple[str, list[list[str]]]:
    text = path.read_text(encoding="utf-8-sig")
    prefix = ""
    body = text
    if text.startswith("sep="):
        i = text.find("\n")
        prefix = text[: i + 1]
        body = text[i + 1 :]
    return prefix, list(csv.reader(io.StringIO(body)))


def write_runtime(path: Path, prefix: str, rows: list[list[str]], *, bom: bool) -> None:
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    for row in rows:
        w.writerow(row)
    data = prefix + out.getvalue()
    enc = "utf-8-sig" if bom else "utf-8"
    path.write_text(data, encoding=enc)


def row_id(row: list[str]) -> str:
    return (row[0] if row else "").strip()


def index_rows(rows: list[list[str]]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for row in rows:
        i = row_id(row)
        if i.isdigit():
            out[i] = row
    return out


def pad5(row: list[str]) -> list[str]:
    r = list(row) + [""] * 5
    return r[:5]


def collect_lua_t(root: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    for path in [root / "items.lua", *sorted((root / "UnitData").glob("*.lua") if (root / "UnitData").is_dir() else []), *sorted((root / "Code").glob("*.lua") if (root / "Code").is_dir() else []), *sorted((root / "CharacterEffect").glob("*.lua") if (root / "CharacterEffect").is_dir() else [])]:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in T_RE.finditer(text):
            tid, raw = m.group(1), unescape_lua(m.group(2))
            if tid not in found:
                found[tid] = raw
    return found


def has_header(rows: list[list[str]]) -> bool:
    return bool(rows) and row_id(rows[0]).upper() == "ID"


def main() -> None:
    game_ids = load_game_ids(find_game_csv())
    print(f"vanilla Game.csv ids={len(game_ids)}")

    lua = collect_lua_t(UNITS)
    ru_prefix, ru_rows = read_runtime(JAZZ / "Russian.csv")
    en_prefix, en_rows = read_runtime(JAZZ / "English.csv")
    uen_prefix, uen_rows = read_runtime(UNITS / "English.csv")
    jazz_ru = index_rows(ru_rows)
    jazz_en = index_rows(en_rows)
    units_en = index_rows(uen_rows)

    needed = {
        tid
        for tid in (set(lua) | set(units_en))
        if is_mod_only(tid, game_ids)
    }

    added_ru_rows: list[list[str]] = []
    added_en_rows: list[list[str]] = []
    lua_en_used = 0
    for tid in sorted(needed, key=lambda s: int(s)):
        urow = units_en.get(tid)
        lua_text = lua.get(tid, "")
        ru_text = (urow[1] if urow and len(urow) > 1 and urow[1] else "") or lua_text
        en_text = (urow[2] if urow and len(urow) > 2 and urow[2] else "") or LUA_EN.get(tid, "")
        if not en_text:
            if lua_text and not CYR_RE.search(lua_text):
                en_text = lua_text
            else:
                en_text = lua_text
                if tid in lua and CYR_RE.search(lua_text):
                    lua_en_used += 1
        ctx = ""
        if urow and len(urow) > 4:
            ctx = urow[4]
        elif tid in lua:
            ctx = "jazz-units:items.lua"
        if tid not in jazz_ru and ru_text:
            row = [tid, ru_text, ru_text, "", ctx]
            added_ru_rows.append(row)
            jazz_ru[tid] = row
        if tid not in jazz_en and ru_text:
            row = [tid, ru_text, en_text or ru_text, "", ctx]
            added_en_rows.append(row)
            jazz_en[tid] = row

    def append_only(path: Path, extra: list[list[str]]) -> None:
        if not extra:
            return
        text = path.read_text(encoding="utf-8")
        if text and not text.endswith("\n"):
            text += "\n"
        buf = io.StringIO()
        csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL).writerows(extra)
        path.write_text(text + buf.getvalue(), encoding="utf-8")

    append_only(JAZZ / "Russian.csv", added_ru_rows)
    append_only(JAZZ / "English.csv", added_en_rows)
    print(f"jazz Russian.csv appended {len(added_ru_rows)}; English.csv appended {len(added_en_rows)}")
    if lua_en_used:
        print(f"WARN: {lua_en_used} IDs used RU source as EN (no units EN / LUA_EN)")

    # Units English: add anything jazz EN has for needed IDs.
    uen_extra: list[list[str]] = []
    for tid in sorted(needed, key=lambda s: int(s)):
        if tid in units_en:
            continue
        src = jazz_en.get(tid)
        if not src:
            continue
        row = pad5(src)
        uen_extra.append(row)
        units_en[tid] = row
    append_only(UNITS / "English.csv", uen_extra)
    print(f"jazz-units English.csv appended {len(uen_extra)} (now {len(units_en)} ids)")

    # Units Russian: full loctable for needed IDs (editor Russian language).
    ru_out: list[list[str]] = [FIELDS]
    for tid in sorted(needed, key=lambda s: int(s)):
        src = jazz_ru.get(tid)
        if not src:
            continue
        ru_out.append(pad5(src))
    write_runtime(UNITS / "Russian.csv", "sep=,\n", ru_out, bom=True)
    print(f"wrote jazz-units/Russian.csv rows={len(ru_out)-1}")

    meta = UNITS / "metadata.lua"
    text = meta.read_text(encoding="utf-8")
    old = """\t'loctables', {
		{
			filename = "Mod/Dv3mFVN/English.csv",
			language = "English",
		},
	},"""
    new = """\t'loctables', {
		{
			filename = "Mod/Dv3mFVN/Russian.csv",
			language = "Russian",
		},
		{
			filename = "Mod/Dv3mFVN/English.csv",
			language = "English",
		},
	},"""
    if old not in text:
        if "Mod/Dv3mFVN/Russian.csv" in text:
            print("metadata.lua already has Russian loctable")
        else:
            raise SystemExit("loctables block not found in jazz-units/metadata.lua")
    else:
        meta.write_text(text.replace(old, new, 1), encoding="utf-8")
        print("metadata.lua: added Russian.csv loctable")


if __name__ == "__main__":
    main()
