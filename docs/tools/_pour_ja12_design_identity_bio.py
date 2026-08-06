# -*- coding: utf-8 -*-
"""Synchronize JA12 merc Name/Bio source strings from executable design articles.

The tool deliberately owns only the 42 mercs whose generated UnitData still used
WIP Name/Bio source strings when JAZZ-LOC-002 was approved. It updates the
generated companion and the matching ModItem in jazz-units/items.lua while
preserving localization IDs and every unrelated byte. Runtime localization CSVs
are intentionally out of scope; the bilingual review artifact is written to
docs/tools/localization-copy-edits/ja12_identity_bio.csv.

Usage (from the jazz repository):

    python docs/tools/_pour_ja12_design_identity_bio.py --dry-run
    python docs/tools/_pour_ja12_design_identity_bio.py --apply
    python docs/tools/_pour_ja12_design_identity_bio.py --check
"""
from __future__ import annotations

import argparse
import csv
import io
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


JAZZ = Path(__file__).resolve().parents[2]
JAZZ_UNITS = JAZZ.parent / "jazz-units"
DESIGN = JAZZ / "docs" / "design" / "mercs-ja12"
UNITDATA = JAZZ_UNITS / "UnitData"
ITEMS = JAZZ_UNITS / "items.lua"
CATALOG = (
    JAZZ
    / "docs"
    / "tools"
    / "localization-copy-edits"
    / "ja12_identity_bio.csv"
)

# This is intentionally an allowlist: ready/executable mercs that had WIP
# identity/bio source strings at JAZZ-LOC-002 preflight. Existing finished
# mercs and planned Benny/Simon must never be swept into this repair.
TARGET_SLUGS = (
    "allik",
    "biff",
    "biggens",
    "blade",
    "bull",
    "carlos",
    "conrad",
    "cord",
    "cougar",
    "devin",
    "dimitri",
    "dynamo",
    "eskimo",
    "flo",
    "gamos",
    "gaston",
    "grace",
    "grom",
    "henning",
    "highball",
    "hitman",
    "hobbit",
    "horg",
    "ira",
    "kulba",
    "laura",
    "lucky",
    "madman",
    "manuel",
    "meat",
    "miguel",
    "mike",
    "monk",
    "nervous",
    "quinten",
    "ricochet",
    "shank",
    "static",
    "steiger",
    "vicious",
    "vilde",
    "vince",
)

LUA_STRING_PATTERN = r'''"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*' '''
LUA_STRING_PATTERN = LUA_STRING_PATTERN.strip()
PLACEHOLDER_RE = re.compile(r"(?i)(?:\[?WIP\]?|work in progress|placeholder)")


class PourError(RuntimeError):
    pass


@dataclass(frozen=True)
class DesignMerc:
    slug: str
    unit_id: str
    name_ru: str
    name_en: str
    bio_ru: str
    bio_en: str
    article: Path


@dataclass(frozen=True)
class CatalogRow:
    tid: str
    source: str
    russian: str
    english: str
    notes: str


@dataclass
class Plan:
    desired: dict[Path, bytes]
    catalog_rows: list[CatalogRow]
    changed_companion_fields: int
    changed_items_fields: int
    placeholder_fields: int

    @property
    def changed_paths(self) -> list[Path]:
        out: list[Path] = []
        for path, wanted in self.desired.items():
            current = path.read_bytes() if path.exists() else None
            if path == CATALOG and current is not None:
                current = current.replace(b"\r\n", b"\n")
                wanted = wanted.replace(b"\r\n", b"\n")
            if current != wanted:
                out.append(path)
        return out


def read_utf8_exact(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8")
    except FileNotFoundError as exc:
        raise PourError(f"missing required file: {path}") from exc
    except UnicodeDecodeError as exc:
        raise PourError(f"not valid UTF-8: {path}: {exc}") from exc


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        raise PourError(f"missing YAML frontmatter: {path}")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$", line)
        if item:
            values[item.group(1)] = item.group(2).strip().strip("\"'")
    return values


def markdown_scalar(raw: str) -> str:
    """Collapse Markdown soft wraps while preserving paragraph breaks."""
    paragraphs = re.split(r"\r?\n\s*\r?\n", raw.strip())
    return "\n\n".join(
        " ".join(line.strip() for line in paragraph.splitlines() if line.strip())
        for paragraph in paragraphs
        if paragraph.strip()
    )


def section(text: str, heading: str, path: Path) -> str:
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\s*\r?\n(.*?)(?=^## |\Z)", text
    )
    if not match:
        raise PourError(f"missing '## {heading}' section: {path}")
    return match.group(1)


def parse_design(slug: str) -> DesignMerc:
    path = DESIGN / f"{slug}.md"
    text = read_utf8_exact(path)
    # Some older design articles carry a UTF-8 BOM; it is not Markdown content.
    text = text.removeprefix("\ufeff")
    meta = parse_frontmatter(text, path)
    if meta.get("status") != "ready" or meta.get("executable", "").lower() != "true":
        raise PourError(
            f"target article is not status=ready + executable=true: {path} "
            f"(status={meta.get('status')!r}, executable={meta.get('executable')!r})"
        )
    unit_id = meta.get("unit_id", "")
    if not re.fullmatch(r"Jazz_[A-Za-z0-9_]+", unit_id):
        raise PourError(f"invalid or missing unit_id in {path}: {unit_id!r}")

    identity = section(text, "Identity", path)
    name_ru = name_en = ""
    for line in identity.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[0] == "Name":
            name_ru, name_en = cells[1], cells[2]
            break
    if not name_ru or not name_en:
        raise PourError(f"Identity Name must contain non-empty RU and EN: {path}")

    bio = section(text, "Bio", path)
    ru_match = re.search(r"(?ms)^\*\*RU:\*\*\s*(.*?)(?=^\*\*EN:\*\*)", bio)
    en_match = re.search(r"(?ms)^\*\*EN:\*\*\s*(.*?)\s*\Z", bio)
    if not ru_match or not en_match:
        raise PourError(f"Bio must contain **RU:** and **EN:** paragraphs: {path}")
    bio_ru = markdown_scalar(ru_match.group(1))
    bio_en = markdown_scalar(en_match.group(1))
    if not bio_ru or not bio_en:
        raise PourError(f"Bio RU/EN must be non-empty: {path}")

    return DesignMerc(
        slug=slug,
        unit_id=unit_id,
        name_ru=name_ru,
        name_en=name_en,
        bio_ru=bio_ru,
        bio_en=bio_en,
        article=path,
    )


def lua_unescape(body: str) -> str:
    out: list[str] = []
    i = 0
    escapes = {
        "n": "\n",
        "r": "\r",
        "t": "\t",
        "\\": "\\",
        '"': '"',
        "'": "'",
    }
    while i < len(body):
        if body[i] != "\\":
            out.append(body[i])
            i += 1
            continue
        if i + 1 >= len(body):
            raise PourError("unterminated Lua escape in source string")
        nxt = body[i + 1]
        if nxt not in escapes:
            raise PourError(f"unsupported Lua escape \\{nxt} in source string")
        out.append(escapes[nxt])
        i += 2
    return "".join(out)


def lua_literal(value: str, quote: str) -> str:
    body = (
        value.replace("\\", "\\\\")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        .replace(quote, "\\" + quote)
    )
    return quote + body + quote


def companion_field_pattern(field: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?m)^[ \t]*{re.escape(field)}[ \t]*=[ \t]*T\([ \t]*"
        rf"(?P<id>\d+)[ \t]*,[ \t]*(?:--\[\[[^\r\n]*\]\][ \t]*)?"
        rf"(?P<literal>{LUA_STRING_PATTERN})"
    )


def items_field_pattern(field: str, tid: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?m)^[ \t]*['\"]{re.escape(field)}['\"][ \t]*,[ \t]*T\([ \t]*"
        rf"{re.escape(tid)}[ \t]*,[ \t]*(?:--\[\[[^\r\n]*\]\][ \t]*)?"
        rf"(?P<literal>{LUA_STRING_PATTERN})"
    )


def one_match(pattern: re.Pattern[str], text: str, label: str) -> re.Match[str]:
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise PourError(f"expected exactly one {label}, found {len(matches)}")
    return matches[0]


def literal_value(match: re.Match[str]) -> str:
    literal = match.group("literal")
    return lua_unescape(literal[1:-1])


def replace_literal(text: str, match: re.Match[str], value: str) -> str:
    start, end = match.span("literal")
    quote = match.group("literal")[0]
    return text[:start] + lua_literal(value, quote) + text[end:]


def assert_safe_old_value(old: str, wanted: str, label: str) -> None:
    if old == wanted or PLACEHOLDER_RE.search(old):
        return
    raise PourError(
        f"refusing to overwrite non-placeholder source at {label}: "
        f"current={old!r}, design={wanted!r}"
    )


def assert_items_owner(text: str, match: re.Match[str], unit_id: str, label: str) -> None:
    block_start = text.rfind("PlaceObj('ModItemUnitDataCompositeDef', {", 0, match.start())
    if block_start < 0:
        raise PourError(f"cannot locate enclosing UnitData ModItem for {label}")
    prefix = text[block_start : match.start()]
    owner = re.search(r"['\"]Id['\"][ \t]*,[ \t]*['\"]([^'\"]+)['\"]", prefix)
    if not owner or owner.group(1) != unit_id:
        raise PourError(
            f"wrong enclosing items.lua owner for {label}: "
            f"expected {unit_id}, found {owner.group(1) if owner else '<none>'}"
        )


def catalog_bytes(rows: list[CatalogRow]) -> bytes:
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["ID", "SourceText", "Russian", "English", "Notes"])
    for row in rows:
        writer.writerow([row.tid, row.source, row.russian, row.english, row.notes])
    return buf.getvalue().encode("utf-8")


def build_plan() -> Plan:
    if len(TARGET_SLUGS) != 42 or len(set(TARGET_SLUGS)) != 42:
        raise PourError("TARGET_SLUGS must contain exactly 42 unique merc slugs")
    mercs = [parse_design(slug) for slug in TARGET_SLUGS]
    if len({merc.unit_id for merc in mercs}) != 42:
        raise PourError("target design articles do not have 42 unique unit_id values")

    items_current = read_utf8_exact(ITEMS)
    items_wanted = items_current
    desired: dict[Path, bytes] = {}
    rows: list[CatalogRow] = []
    seen_ids: set[str] = set()
    changed_companion_fields = 0
    changed_items_fields = 0
    placeholder_fields = 0

    for merc in mercs:
        companion = UNITDATA / f"{merc.unit_id}.lua"
        companion_current = read_utf8_exact(companion)
        if not re.search(
            rf"(?m)^DefineClass\.{re.escape(merc.unit_id)}\s*=", companion_current
        ):
            raise PourError(f"companion does not define {merc.unit_id}: {companion}")
        companion_wanted = companion_current

        fields = (
            ("Name", merc.name_ru, merc.name_en),
            ("Bio", merc.bio_ru, merc.bio_en),
        )
        for field, russian, english in fields:
            companion_match = one_match(
                companion_field_pattern(field),
                companion_wanted,
                f"{merc.unit_id}.{field} in {companion}",
            )
            tid = companion_match.group("id")
            if tid in seen_ids:
                raise PourError(f"duplicate Name/Bio localization ID among targets: {tid}")
            seen_ids.add(tid)

            companion_old = literal_value(companion_match)
            assert_safe_old_value(
                companion_old,
                russian,
                f"{companion}:{merc.unit_id}.{field} T({tid})",
            )
            if PLACEHOLDER_RE.search(companion_old):
                placeholder_fields += 1
            if companion_old != russian:
                changed_companion_fields += 1
                companion_wanted = replace_literal(
                    companion_wanted, companion_match, russian
                )

            item_match = one_match(
                items_field_pattern(field, tid),
                items_wanted,
                f"{merc.unit_id}.{field} T({tid}) in {ITEMS}",
            )
            assert_items_owner(items_wanted, item_match, merc.unit_id, f"T({tid})")
            item_old = literal_value(item_match)
            assert_safe_old_value(
                item_old,
                russian,
                f"{ITEMS}:{merc.unit_id}.{field} T({tid})",
            )
            if item_old != russian:
                changed_items_fields += 1
                items_wanted = replace_literal(items_wanted, item_match, russian)

            article_rel = merc.article.relative_to(JAZZ).as_posix()
            rows.append(
                CatalogRow(
                    tid=tid,
                    source=russian,
                    russian=russian,
                    english=english,
                    notes=(
                        f"design={article_rel}; unit={merc.unit_id}; field={field}; "
                        "status=ready; executable=true"
                    ),
                )
            )

        desired[companion] = companion_wanted.encode("utf-8")

    if len(rows) != 84 or len(seen_ids) != 84:
        raise PourError(
            f"expected 84 unique logical fields, found rows={len(rows)} ids={len(seen_ids)}"
        )
    desired[ITEMS] = items_wanted.encode("utf-8")
    desired[CATALOG] = catalog_bytes(rows)
    return Plan(
        desired=desired,
        catalog_rows=rows,
        changed_companion_fields=changed_companion_fields,
        changed_items_fields=changed_items_fields,
        placeholder_fields=placeholder_fields,
    )


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, raw_tmp = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    tmp = Path(raw_tmp)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except Exception:
        try:
            tmp.unlink(missing_ok=True)
        finally:
            raise


def display_path(path: Path) -> str:
    try:
        return path.relative_to(JAZZ).as_posix()
    except ValueError:
        return "../jazz-units/" + path.relative_to(JAZZ_UNITS).as_posix()


def print_summary(mode: str, plan: Plan, changed: list[Path]) -> None:
    print(
        f"mode={mode} targets=42 fields=84 catalog_rows={len(plan.catalog_rows)} "
        f"companion_field_changes={plan.changed_companion_fields} "
        f"items_field_changes={plan.changed_items_fields} "
        f"target_placeholders={plan.placeholder_fields} changed_files={len(changed)}"
    )
    marker = "would update" if mode == "dry-run" else "drift"
    for path in changed:
        print(f"  {marker}: {display_path(path)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--apply", action="store_true", help="write the validated transaction")
    modes.add_argument("--check", action="store_true", help="fail if any target differs")
    modes.add_argument("--dry-run", action="store_true", help="show the pending transaction")
    args = parser.parse_args()
    mode = "apply" if args.apply else "check" if args.check else "dry-run"

    try:
        plan = build_plan()
        changed = plan.changed_paths
        if mode == "dry-run":
            print_summary(mode, plan, changed)
            return 0
        if mode == "check":
            print_summary(mode, plan, changed)
            if changed:
                print("CHECK FAILED: run with --apply to synchronize the approved targets")
                return 1
            if plan.placeholder_fields:
                print("CHECK FAILED: target Name/Bio placeholders remain")
                return 1
            print("CHECK PASSED: 42 mercs / 84 Name+Bio fields match design and catalog")
            return 0

        for path in changed:
            atomic_write(path, plan.desired[path])
        after = build_plan()
        after_changed = after.changed_paths
        if after_changed or after.placeholder_fields:
            raise PourError(
                "post-apply verification failed: "
                f"changed={len(after_changed)} placeholders={after.placeholder_fields}"
            )
        print_summary(mode, plan, changed)
        print("APPLY PASSED: 42 mercs / 84 Name+Bio fields synchronized")
        return 0
    except PourError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
