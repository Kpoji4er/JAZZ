# -*- coding: utf-8 -*-
"""Fix EN-in-RU medical / concussion loc after mag-hint-align collateral damage.

Root cause: `_fix_mag_hint_loc_align.py` upserted *all* InventoryItem AdditionalHint
T() IDs into Russian.csv as Text=Translation=EN source (ctx mag-hint-aligned), wiping
MED-001 Russian Translations and stomping vanilla Game.csv overrides.

Also `_append_grenade_concussion_loc.py` wrote id,RU,EN into Russian.csv (IMP Mimicry class).

NOTE: jazz runtime Russian.csv / English.csv use `sep=,` then data rows — NO header row.
Do not use DictReader/`_loc_csv_io.load_rows` on these files (first data row becomes "header").
"""
from __future__ import annotations

import csv
import io
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MED_HINT_IDS = {
    "890000000010013",  # JAZZ_Bandage AdditionalHint
    "890000000010016",  # JAZZ_Morphine AdditionalHint
    "890000000010019",  # JAZZ_SurgicalKit AdditionalHint
    "890000000010024",  # FirstAidKit (IFAK) AdditionalHint
    "890000000010027",  # Medkit AdditionalHint
}

REANIM_ID = "890000000010030"
REANIM_EN = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Restores lost HP and stabilizes dying characters\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Required for Bandage\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Bandage restores 60% more HP\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> One use = one item from the stack\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Used automatically while in inventory"
)
REANIM_RU = (
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Восстанавливает потерянные ОЗ и стабилизирует умирающих\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нужен для перевязки\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Перевязка восстанавливает на 60% больше ОЗ\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Один юз = одна штука из стака\n"
    "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически из инвентаря"
)

CONCUSSION = {
    "890000000010277": (
        "Concussion",
        "Контузия",
        "jazz:CharacterEffect/Concussion.lua",
    ),
    "890000000010278": (
        "Disoriented by blast: <color EmStyle>−<APLoss> AP</color>, <color EmStyle>−<cth_penalty>% chance to hit</color>, move cost <color EmStyle>+<move_ap_modifier>%</color>, no Free Move. Lasts about 1–2 turns.",
        "Дезориентация от взрыва: <color EmStyle>−<APLoss> ОД</color>, <color EmStyle>−<cth_penalty>% к точности</color>, стоимость хода <color EmStyle>+<move_ap_modifier>%</color>, без Free Move. Около 1–2 ходов.",
        "jazz:CharacterEffect/Concussion.lua",
    ),
    "890000000010279": (
        "<color EmStyle><DisplayName></color> is concussed",
        "<color EmStyle><DisplayName></color> контужен",
        "jazz:CharacterEffect/Concussion.lua",
    ),
    "890000000010280": (
        "<color EmStyle><DisplayName></color> clears concussion",
        "<color EmStyle><DisplayName></color> приходит в себя после контузии",
        "jazz:CharacterEffect/Concussion.lua",
    ),
}


def has_cyrillic(s: str) -> bool:
    return any("\u0400" <= c <= "\u04FF" for c in s or "")


def looks_english(s: str) -> bool:
    if not s:
        return False
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return False
    return not has_cyrillic(s) and any("a" <= c.lower() <= "z" for c in letters)


def norm_nl(s: str) -> str:
    return (s or "").replace("\r\n", "\n").replace("\r", "\n")


def read_runtime_csv(path: Path) -> tuple[str | None, list[list[str]]]:
    """Return (sep_line_or_None, data_rows). No header row."""
    raw = path.read_text(encoding="utf-8-sig")
    sep = None
    body = raw
    if raw.startswith("sep="):
        nl = raw.find("\n")
        sep = raw[:nl].rstrip("\r") if nl >= 0 else raw.rstrip("\r")
        body = raw[nl + 1 :] if nl >= 0 else ""
    rows = list(csv.reader(io.StringIO(body)))
    return sep, rows


def write_runtime_csv(path: Path, sep: str | None, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        if sep:
            f.write(sep + "\n")
        csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_MINIMAL).writerows(rows)


def load_pre_mag_russian() -> dict[str, list[str]]:
    try:
        blob = subprocess.check_output(
            ["git", "show", "e5ae559^:Russian.csv"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    text = blob.decode("utf-8-sig")
    if text.startswith("sep="):
        nl = text.find("\n")
        text = text[nl + 1 :] if nl >= 0 else ""
    return {r[0]: r for r in csv.reader(io.StringIO(text)) if r}


def upsert_row(
    rows: list[list[str]], iid: str, text: str, trans: str, ctx: str
) -> str:
    text, trans = norm_nl(text), norm_nl(trans)
    n = 0
    for i, row in enumerate(rows):
        if row and row[0] == iid:
            while len(row) < 5:
                row.append("")
            row[1], row[2], row[4] = text, trans, ctx
            rows[i] = row
            n += 1
    if n == 0:
        rows.append([iid, text, trans, "", ctx])
        return "appended"
    return f"updatedx{n}"


def main() -> None:
    pre = load_pre_mag_russian()
    ru_sep, ru_rows = read_runtime_csv(ROOT / "Russian.csv")
    en_sep, en_rows = read_runtime_csv(ROOT / "English.csv")

    fixed: list[str] = []

    for iid in sorted(MED_HINT_IDS):
        old = pre.get(iid)
        if not old or len(old) < 3 or not has_cyrillic(old[2]):
            raise SystemExit(f"no Cyrillic Translation for {iid} in e5ae559^:Russian.csv")
        en_text = norm_nl(old[1])
        ru_trans = norm_nl(old[2])
        ctx = old[4] if len(old) > 4 and old[4] else f"jazz:MED-001-{iid}"
        # Keep current EN Text if mag-hint refreshed it to match Lua
        for row in ru_rows:
            if row and row[0] == iid and len(row) > 1 and looks_english(row[1]):
                en_text = norm_nl(row[1])
                break
        a = upsert_row(ru_rows, iid, en_text, ru_trans, ctx)
        upsert_row(en_rows, iid, en_text, en_text, ctx)
        fixed.append(f"{iid} med-hint ({a})")

    a = upsert_row(ru_rows, REANIM_ID, REANIM_EN, REANIM_RU, "jazz:stack-kits")
    upsert_row(en_rows, REANIM_ID, REANIM_EN, REANIM_EN, "jazz:stack-kits")
    fixed.append(f"{REANIM_ID} reanimationsset ({a})")

    for iid, (en, ru, ctx) in CONCUSSION.items():
        upsert_row(ru_rows, iid, en, ru, ctx)
        upsert_row(en_rows, iid, en, en, ctx)
        fixed.append(f"{iid} concussion")

    # Drop mag-hint-aligned vanilla stomps (EN Translation overriding Game.csv RU).
    game_path = ROOT / "Localization" / "CurrentLanguage" / "Game.csv"
    game_ids: set[str] = set()
    if game_path.exists():
        with game_path.open(encoding="utf-8-sig", newline="") as f:
            game_ids = {r[0] for r in csv.reader(f) if r}

    removed: list[str] = []

    def purge(rows: list[list[str]], lang: str) -> list[list[str]]:
        keep = []
        for row in rows:
            if not row:
                keep.append(row)
                continue
            while len(row) < 5:
                row.append("")
            iid, trans, ctx = row[0], row[2], row[4]
            if (
                ctx == "mag-hint-aligned"
                and iid in game_ids
                and looks_english(trans)
                and not iid.startswith("890000000010")
            ):
                removed.append(f"{lang}:{iid}")
                continue
            keep.append(row)
        return keep

    ru_rows = purge(ru_rows, "RU")
    en_rows = purge(en_rows, "EN")

    write_runtime_csv(ROOT / "Russian.csv", ru_sep, ru_rows)
    write_runtime_csv(ROOT / "English.csv", en_sep, en_rows)

    # Verify
    _, check = read_runtime_csv(ROOT / "Russian.csv")
    by = {r[0]: r for r in check if r}
    bad = []
    for iid in list(MED_HINT_IDS) + [REANIM_ID] + list(CONCUSSION):
        r = by.get(iid)
        if not r or not has_cyrillic(r[2]):
            bad.append(iid)
    if bad:
        raise SystemExit(f"VERIFY FAIL still EN-in-RU: {bad}")

    print(f"fixed={len(fixed)} removed_stomps={len(removed)}")
    for line in fixed:
        print(" ", line.encode("ascii", "backslashreplace").decode("ascii"))
    for line in removed:
        print("  remove", line)
    print("VERIFY OK: medical+concussion Russian.csv Translations are Cyrillic")


if __name__ == "__main__":
    main()
