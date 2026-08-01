# -*- coding: utf-8 -*-
"""Audit WorkshopMerc SNYPE/hire lines with EN left in Russian.csv Translation."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RU = ROOT / "Russian.csv"
UNITS = ROOT.parent / "jazz-units" / "items.lua"

MERC_IDS = [
    "Merc_AnnieDubois",
    "Merc_CarolThompson",
    "Merc_HectorSanchez",
    "Merc_JerrySinclair",
    "Merc_MildredPatterson",
    "Merc_SamuelNkosi",
]

CHAT_FIELDS = (
    "Offline",
    "GreetingAndOffer",
    "ConversationRestart",
    "IdleLine",
    "PartingWords",
    "RehireIntro",
    "RehireOutro",
    "MercChatHaggle",
    "Refusal",
    "Failure",
)


def has_cyrillic(s: str) -> bool:
    return bool(re.search(r"[\u0400-\u04FF]", s or ""))


def has_latin(s: str) -> bool:
    return bool(re.search(r"[A-Za-z]", s or ""))


def load_ru():
    with RU.open("r", encoding="utf-8-sig", newline="") as f:
        first = f.readline()
        reader = csv.DictReader(f)
        return {r["ID"]: r for r in reader}


def extract_chat_tids(text: str):
    """Return {merc_id: {field: [(tid, source_text), ...]}} from jazz-units items.lua."""
    out = {m: {} for m in MERC_IDS}
    # Split by UnitData ModItem blocks roughly
    for merc in MERC_IDS:
        # Find UnitData block starting at 'Id', "Merc_..."
        pat = re.compile(
            rf"'Id',\s*\"{merc}\".*?'object_class',\s*\"UnitData\".*?(?=PlaceObj\('ModItemUnitDataCompositeDef'|PlaceObj\('ModItemVoiceResponse'|PlaceObj\('ModItemLootDef'|PlaceObj\('ModItemAppearancePreset'|PlaceObj\('ModItemCharacterEffectCompositeDef'|PlaceObj\('ModItemCode'|PlaceObj\('ModItemInventoryItemCompositeDef'|PlaceObj\('ModItemFolder'|PlaceObj\('ModItemOption|$\Z)",
            re.S,
        )
        m = pat.search(text)
        if not m:
            # fallback: from Name line area
            idx = text.find(f"'Id', \"{merc}\"")
            if idx < 0:
                print(f"MISSING block {merc}")
                continue
            chunk = text[idx : idx + 25000]
        else:
            chunk = m.group(0)

        level_m = re.search(r"'StartingLevel',\s*(\d+)", chunk)
        level = level_m.group(1) if level_m else "(omitted=1)"
        print(f"LEVEL {merc}: {level}")

        for field in CHAT_FIELDS:
            for tm in re.finditer(
                rf"--\[\[ModItemUnitDataCompositeDef {merc} Text[^\]]*?\b{field}\b[^\]]*\]\]\s*\"((?:\\.|[^\"\\])*)\"",
                chunk,
            ):
                # Better: match T(id, ... "text")
                pass

        # Match all T(id, --[[... Text FIELD ...]] "text")
        for tm in re.finditer(
            rf"T\((\d+),\s*--\[\[ModItemUnitDataCompositeDef {merc} Text ([^\]]+)\]\]\s*\"((?:\\.|[^\"\\])*)\"\)",
            chunk,
        ):
            tid, ctx, src = tm.group(1), tm.group(2), tm.group(3)
            field = None
            for f in CHAT_FIELDS:
                if f in ctx:
                    field = f
                    break
            if not field:
                continue
            out[merc].setdefault(field, []).append((tid, src.encode("utf-8").decode("unicode_escape") if "\\" in src else src))

    return out


def main():
    ru = load_ru()
    units_text = UNITS.read_text(encoding="utf-8")
    chats = extract_chat_tids(units_text)

    print("\n=== HIRE/SNYPE chat lines EN-in-RU ===")
    fixed_candidates = []
    for merc in MERC_IDS:
        print(f"\n## {merc}")
        for field, entries in chats.get(merc, {}).items():
            for tid, src in entries:
                row = ru.get(tid)
                if not row:
                    print(f"  MISSING CSV {field} {tid}: {src[:80]}")
                    continue
                tr = row.get("Translation") or ""
                en_in_ru = has_latin(tr) and not has_cyrillic(tr) and len(tr.strip()) > 2
                mark = "EN-IN-RU" if en_in_ru else ("OK-RU" if has_cyrillic(tr) else "??")
                print(f"  [{mark}] {field} {tid}")
                print(f"    EN: {src[:100]}")
                print(f"    RU: {tr[:100]}")
                if en_in_ru:
                    fixed_candidates.append((merc, field, tid, src, tr))

    print(f"\nTOTAL EN-IN-RU hire/SNYPE: {len(fixed_candidates)}")
    for c in fixed_candidates:
        print(f"{c[0]}|{c[1]}|{c[2]}|{c[3][:90]}")


if __name__ == "__main__":
    main()
