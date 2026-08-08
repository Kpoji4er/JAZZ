# Export hireable merc salary fields for docs/tools/merc-salary-calculator.html.
# Sources: jazz-units UnitData + items.lua Affiliation; vanilla AIM IsMercenary presets.
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1].parent  # jazz/
UNITS = ROOT.parent / "jazz-units" / "UnitData"
ITEMS = ROOT.parent / "jazz-units" / "items.lua"
VANILLA = Path(
    r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3\ModTools\Src\Lua\UnitDataCompositeDef"
)
OUT_JSON = Path(__file__).resolve().parent / "merc-salary-data.json"

NICK_RE = re.compile(
    r'Nick\s*=\s*T\(\d+,\s*--\[\[[^\]]*\]\]\s*"([^"]+)"',
    re.S,
)
NAME_RE = re.compile(
    r'Name\s*=\s*T\(\d+,\s*--\[\[[^\]]*\]\]\s*"([^"]+)"',
    re.S,
)


def field_str(text: str, key: str, default: str | None = None) -> str | None:
    m = re.search(rf'{key}\s*=\s*"([^"]+)"', text)
    return m.group(1) if m else default


def field_int(text: str, key: str, default: int | None = None) -> int | None:
    m = re.search(rf"{key}\s*=\s*(-?\d+)", text)
    return int(m.group(1)) if m else default


def load_items_affiliation() -> dict[str, str]:
    if not ITEMS.is_file():
        return {}
    text = ITEMS.read_text(encoding="utf-8", errors="replace")
    out: dict[str, str] = {}
    # ModItem blocks: 'Id', "Jazz_X" ... 'Affiliation', "AIM"
    for m in re.finditer(
        r"'Id',\s*\"([^\"]+)\"([\s\S]{0,8000}?)(?:PlaceObj\(|^\t\t\}\))",
        text,
        re.M,
    ):
        uid, chunk = m.group(1), m.group(2)
        am = re.search(r"'Affiliation',\s*\"([^\"]+)\"", chunk)
        if am:
            out[uid] = am.group(1)
    return out


def parse_unit(path: Path, uid: str, source: str, aff_map: dict[str, str]) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if "IsMercenary = true" not in text and "IsMercenary=true" not in text:
        # AME always hireable even if flag missing
        if not uid.startswith("JAZZ_AME_"):
            return None
    salary = field_int(text, "StartingSalary")
    if salary is None:
        return None

    nick_m = NICK_RE.search(text)
    name_m = NAME_RE.search(text)
    nick = nick_m.group(1) if nick_m else (name_m.group(1) if name_m else uid)

    aff = field_str(text, "Affiliation") or aff_map.get(uid) or ""
    if source == "vanilla" and not aff:
        aff = "AIM"

    # Drop enemy/NPC junk
    if aff in ("Thugs", "Legion", "Army", "Adonis", "Rebel", "Civilian"):
        return None
    if uid.startswith("JAZZ_Legion") or uid.startswith("JAZZ_Army"):
        return None

    return {
        "id": uid,
        "nick": nick,
        "aff": aff or "AIM",
        "role": field_str(text, "Specialization", "") or "",
        "tier": field_str(text, "Tier", "") or "",
        "lvl": field_int(text, "StartingLevel", 1) or 1,
        "salary": salary,
        "inc": field_int(text, "SalaryIncrease", 250) or 250,
        "med": field_str(text, "MedicalDeposit", "small") or "small",
        "disc": field_str(text, "DurationDiscount", "normal") or "normal",
        "hag": field_str(text, "Haggling", "normal") or "normal",
        "src": source,
    }


def main() -> None:
    aff_map = load_items_affiliation()
    rows: dict[str, dict] = {}

    if VANILLA.is_dir():
        for p in sorted(VANILLA.glob("*.generated.lua")):
            uid = p.name.replace(".generated.lua", "")
            r = parse_unit(p, uid, "vanilla", aff_map)
            if r:
                rows[uid] = r

    if UNITS.is_dir():
        for p in sorted(UNITS.glob("*.lua")):
            uid = p.stem
            if not (
                uid.startswith("Jazz_")
                or uid.startswith("JAZZ_AME_")
                or uid.startswith("JAZZ_Merc_")
            ):
                continue
            r = parse_unit(p, uid, "jazz", aff_map)
            if r:
                rows[uid] = r

    data = sorted(rows.values(), key=lambda r: (r["aff"], r["nick"].lower(), r["id"]))
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    by: dict[str, int] = {}
    for r in data:
        by[r["aff"]] = by.get(r["aff"], 0) + 1
    print("wrote", OUT_JSON.name, "count", len(data), "by_aff", by)


if __name__ == "__main__":
    main()
