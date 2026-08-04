# -*- coding: utf-8 -*-
"""Align remaining mag/parts loc Text collisions after AME/perk remap."""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

HINT_SHORT_RU = (
    "Съёмный модуль. Перетащите на совместимое оружие или установите в кабинете модификации."
)
HINT_SHORT_EN = (
    "Removable module. Drag onto a compatible firearm or install in the weapon modification screen."
)


def load_csv(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def save_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)


def unquote(s: str) -> str:
    body = s[1:-1]
    return body.replace("\\\\", "\\").replace('\\"', '"').replace("\\n", "\n")


def escape(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def collect_lua_hints() -> dict[int, set[tuple[str, str]]]:
    """id -> set of (source_text, relpath) from AdditionalHint T()."""
    out: dict[int, set[tuple[str, str]]] = defaultdict(set)
    pat = re.compile(
        r"AdditionalHint\s*=\s*T\(\s*(\d+)\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?(\"(\"\"|[^\"])*\")",
        re.DOTALL,
    )
    # also items.lua 'AdditionalHint'
    pat2 = re.compile(
        r"'AdditionalHint',\s*T\(\s*(\d+)\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?(\"(\"\"|[^\"])*\")",
        re.DOTALL,
    )
    for p in list((ROOT / "InventoryItem").glob("*.lua")) + [ROOT / "items.lua"]:
        t = p.read_text(encoding="utf-8")
        rel = str(p.relative_to(ROOT))
        for patx in (pat, pat2):
            for m in patx.finditer(t):
                out[int(m.group(1))].add((unquote(m.group(2)), rel))
    return out


def family_en(ru: str) -> str:
    m = re.match(r"Семья магазинов:\s*([^.]+)\.\s*(.*)", ru, re.DOTALL)
    if m:
        return (
            f"Magazine family: {m.group(1).strip()}. "
            + HINT_SHORT_EN
        )
    if ru == HINT_SHORT_RU or ru.startswith("Съёмный модуль"):
        return HINT_SHORT_EN
    return ru


def upsert_all(rows: list[list[str]], lid: int, text: str, translation: str, ctx: str) -> int:
    """Update ALL rows with this ID (dedupe collisions from duplicate CSV lines)."""
    sid = str(lid)
    n = 0
    for i, row in enumerate(rows):
        if row and row[0] == sid:
            while len(row) < 5:
                row.append("")
            row[1] = text
            row[2] = translation
            if ctx:
                row[4] = ctx
            rows[i] = row
            n += 1
    if n == 0:
        rows.append([sid, text, translation, "", ctx])
        return 1
    return n


def align_lua_to_canonical(canonical: dict[int, str]) -> list[str]:
    """Force all AdditionalHint T(id) texts to canonical[id]."""
    changed = []
    files = list((ROOT / "InventoryItem").glob("JAZZ_Mag*.lua")) + [ROOT / "items.lua"]
    for p in files:
        t = p.read_text(encoding="utf-8")
        orig = t
        for lid, src in canonical.items():

            def repl(m: re.Match, lid=lid, src=src) -> str:
                cmt = re.search(r"--\[\[[^\]]*\]\]", m.group(0))
                cmt_s = f" {cmt.group(0)} " if cmt else " "
                # keep prefix through T(id,
                head = m.group(0).split("T(", 1)[0] + f"T({lid},"
                return f"{head}{cmt_s}{escape(src)})"

            # AdditionalHint = T(id, ...)
            t = re.sub(
                rf"AdditionalHint\s*=\s*T\(\s*{lid}\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?\"(?:\"\"|[^\"])*\"\s*\)",
                repl,
                t,
            )
            t = re.sub(
                rf"'AdditionalHint',\s*T\(\s*{lid}\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?\"(?:\"\"|[^\"])*\"\s*\)",
                repl,
                t,
            )
        if t != orig:
            p.write_text(t, encoding="utf-8", newline="\n")
            changed.append(str(p.relative_to(ROOT)))
    return changed


def main() -> None:
    hints = collect_lua_hints()
    # Prefer family-prefixed RU text when any lua source has it; else short RU.
    canonical: dict[int, str] = {}
    multi = 0
    for lid, pairs in sorted(hints.items()):
        texts = {t for t, _ in pairs}
        if len(texts) > 1:
            multi += 1
            fam = [t for t in texts if t.startswith("Семья магазинов")]
            if fam:
                canonical[lid] = sorted(fam, key=len, reverse=True)[0]
            elif HINT_SHORT_RU in texts:
                canonical[lid] = HINT_SHORT_RU
            else:
                # pick non-English if possible
                ru = [t for t in texts if not t.startswith("Removable") and not t.startswith("Magazine")]
                canonical[lid] = ru[0] if ru else next(iter(texts))
            print(f"multi {lid}: -> {canonical[lid][:60]!r} from {sorted(texts, key=len)}")
        else:
            t = next(iter(texts))
            # normalize EN-only sources to RU short if it's the generic hint
            if t == HINT_SHORT_EN:
                canonical[lid] = HINT_SHORT_RU
            elif t.startswith("Magazine family:"):
                # convert EN family to RU family for T() source consistency
                m = re.match(r"Magazine family:\s*([^.]+)\.\s*", t)
                if m:
                    canonical[lid] = (
                        f"Семья магазинов: {m.group(1).strip()}. {HINT_SHORT_RU}"
                    )
                else:
                    canonical[lid] = t
            else:
                canonical[lid] = t

    print(f"hint ids={len(hints)} multi={multi} canonical={len(canonical)}")
    changed = align_lua_to_canonical(canonical)
    print("lua aligned:", len(changed))

    ru_rows = load_csv(ROOT / "Russian.csv")
    en_rows = load_csv(ROOT / "English.csv")
    for lid, src in canonical.items():
        upsert_all(ru_rows, lid, src, src, "mag-hint-aligned")
        upsert_all(en_rows, lid, src, family_en(src), "mag-hint-aligned")

    # ScopeParts plural/hint if EN/RU mismatch in lua+csv
    # 990002501 DisplayNamePlural, 990002502 AdditionalHint — align Text to RU lua
    scope = ROOT / "InventoryItem" / "JAZZ_ScopeParts.lua"
    st = scope.read_text(encoding="utf-8")
    for m in re.finditer(
        r"(DisplayNamePlural|AdditionalHint|DisplayName)\s*=\s*T\(\s*(\d+)\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?(\"(\"\"|[^\"])*\")",
        st,
    ):
        lid = int(m.group(2))
        src = unquote(m.group(3))
        if m.group(1) == "DisplayNamePlural":
            upsert_all(ru_rows, lid, src, src, "scope-parts")
            upsert_all(en_rows, lid, src, "Scope Parts", "scope-parts")
        elif m.group(1) == "AdditionalHint":
            upsert_all(ru_rows, lid, src, src, "scope-parts")
            upsert_all(
                en_rows,
                lid,
                src,
                "Used when repairing a firearm that has a scope installed. Also salvaged when a scope breaks on a failed removal.",
                "scope-parts",
            )
        elif m.group(1) == "DisplayName":
            upsert_all(ru_rows, lid, src, src, "scope-parts")
            upsert_all(en_rows, lid, src, "Scope Parts", "scope-parts")

    # Align Barrel/Scope Parts T() sources in items.lua to RU companion text.
    items = (ROOT / "items.lua").read_text(encoding="utf-8")
    parts_map = {
        990002500: "Детали прицелов",
        990002501: "Детали прицелов",
        990002502: (
            "Нужны при ремонте оружия с установленным прицелом. "
            "Также получаются при поломке прицела при неудачном снятии."
        ),
        990002002: "Ствольные запчасти",
    }
    for lid, src in parts_map.items():

        def repl_t(m, lid=lid, src=src):
            cmt = re.search(r"--\[\[[^\]]*\]\]", m.group(0))
            cmt_s = f" {cmt.group(0)} " if cmt else " "
            return f"T({lid},{cmt_s}{escape(src)}"

        items = re.sub(
            rf"T\(\s*{lid}\s*,\s*(?:--\[\[[^\]]*\]\]\s*)?\"(?:\"\"|[^\"])*\"",
            repl_t,
            items,
        )

    (ROOT / "items.lua").write_text(items, encoding="utf-8", newline="\n")

    save_csv(ROOT / "Russian.csv", ru_rows)
    save_csv(ROOT / "English.csv", en_rows)
    print("CSV updated")


if __name__ == "__main__":
    main()
