#!/usr/bin/env python3
"""Validate and apply reviewed bilingual localization copy edits.

The input is one or more RFC-4180 CSV files with this schema::

    ID,SourceText,Russian,English,Notes

By default the command is a read-only check.  ``--apply`` rewrites only the
two manual translation memories.  It never edits ``Strings.csv`` or either
runtime localization CSV.
"""

from __future__ import annotations

import argparse
import csv
import io
import os
import re
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
EDIT_FIELDS = ("ID", "SourceText", "Russian", "English", "Notes")
CATALOG_REQUIRED = ("ID", "SourceText")
ENGLISH_FIELDS = ("N", "AnchorID", "SourceText", "English", "Notes")
RUSSIAN_FIELDS = ("N", "AnchorID", "SourceText", "Russian", "Notes")


class ValidationError(Exception):
    """A safe, user-correctable validation failure."""


@dataclass(frozen=True)
class Edit:
    anchor_id: str
    source: str
    russian: str
    english: str
    notes: str
    origin: str


@dataclass
class CleanupStats:
    input_rows: int = 0
    exact_duplicates_removed: int = 0
    stale_anchor_rows_removed: int = 0
    edited_anchor_rows_removed: int = 0


def normalize_header(value: str | None) -> str:
    """Normalize BOM-damaged/over-quoted headers without touching row data."""

    text = (value or "").strip().lstrip("\ufeff")
    # Both common UTF-8-BOM-as-text spellings have existed in this repository.
    for prefix in ("ï»¿", "п»ї"):
        if text.startswith(prefix):
            text = text[len(prefix) :]
    text = text.strip()
    while len(text) >= 2 and text[0] == text[-1] == '"':
        text = text[1:-1].strip()
    return text


def read_csv_rows(
    path: Path,
    *,
    required: Sequence[str],
    known_fields: Sequence[str] | None = None,
) -> tuple[list[str], list[dict[str, str]]]:
    """Read UTF-8 CSV without splitting multiline quoted records."""

    if not path.is_file():
        raise ValidationError(f"CSV file does not exist: {path}")
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            raw_header = next(reader, None)
            if raw_header is None:
                raise ValidationError(f"CSV file is empty: {path}")
            header = [normalize_header(value) for value in raw_header]
            aliases = {field.casefold(): field for field in (known_fields or header)}
            header = [aliases.get(value.casefold(), value) for value in header]
            if len(set(header)) != len(header):
                raise ValidationError(f"duplicate CSV columns in {path}: {header!r}")
            missing = [field for field in required if field not in header]
            if missing:
                raise ValidationError(
                    f"missing columns in {path}: {', '.join(missing)}; got {header!r}"
                )

            rows: list[dict[str, str]] = []
            for record_number, raw in enumerate(reader, start=2):
                if not raw or not any(value != "" for value in raw):
                    continue
                if len(raw) > len(header):
                    raise ValidationError(
                        f"{path}: CSV record {record_number} has {len(raw)} fields; "
                        f"header has {len(header)}"
                    )
                raw += [""] * (len(header) - len(raw))
                rows.append(dict(zip(header, raw)))
    except (OSError, UnicodeError, csv.Error) as exc:
        raise ValidationError(f"cannot read {path}: {exc}") from exc
    return header, rows


def markup_tokens(text: str) -> Counter[str]:
    """Return a multiset of engine-significant markup/placeholders."""

    token_re = re.compile(
        r"<[^<>\r\n]+>"  # JA3/UI tags and named placeholders
        r"|\\[nrt]"  # explicit Lua/control escapes
        r"|%(?:\d+\$)?[-+#0 ]*\d*(?:\.\d+)?[A-Za-z]"  # printf token
        r"|%[A-Za-z_][A-Za-z0-9_]*%?"  # named percent placeholder
        r"|\{[^{}\r\n]+\}"  # brace placeholder
        r"|\r\n|\r|\n"
    )
    tokens: Counter[str] = Counter()
    for match in token_re.finditer(text or ""):
        token = match.group(0)
        if token in {"\r\n", "\r", "\n", "\\n"}:
            token = "<NEWLINE>"
        elif token == "\\t":
            token = "<TAB>"
        elif token == "\\r":
            token = "<RETURN>"
        tokens[token] += 1
    return tokens


def counter_delta(expected: Counter[str], actual: Counter[str]) -> str:
    missing = expected - actual
    extra = actual - expected
    chunks = []
    if missing:
        chunks.append(f"missing={dict(sorted(missing.items()))}")
    if extra:
        chunks.append(f"extra={dict(sorted(extra.items()))}")
    return ", ".join(chunks) or "no difference"


def validate_markup(edit: Edit) -> None:
    expected = markup_tokens(edit.source)
    for language, translation in (("Russian", edit.russian), ("English", edit.english)):
        actual = markup_tokens(translation)
        if actual != expected:
            raise ValidationError(
                f"{edit.origin}: ID {edit.anchor_id} {language} markup mismatch: "
                f"{counter_delta(expected, actual)}"
            )


def load_edits(paths: Iterable[Path]) -> list[Edit]:
    edits: list[Edit] = []
    seen: dict[str, str] = {}
    for path in paths:
        _, rows = read_csv_rows(path, required=EDIT_FIELDS, known_fields=EDIT_FIELDS)
        for record_number, row in enumerate(rows, start=2):
            anchor_id = row["ID"].strip()
            origin = f"{path}:{record_number}"
            if not re.fullmatch(r"\d+", anchor_id):
                raise ValidationError(f"{origin}: ID must contain digits only: {anchor_id!r}")
            if anchor_id in seen:
                raise ValidationError(
                    f"duplicate edit ID {anchor_id}: {seen[anchor_id]} and {origin}"
                )
            source = row["SourceText"]
            russian = row["Russian"]
            english = row["English"]
            if source == "":
                raise ValidationError(f"{origin}: SourceText is empty")
            if not russian.strip():
                raise ValidationError(f"{origin}: Russian translation is empty")
            if not english.strip():
                raise ValidationError(f"{origin}: English translation is empty")
            edit = Edit(anchor_id, source, russian, english, row["Notes"], origin)
            validate_markup(edit)
            seen[anchor_id] = origin
            edits.append(edit)
    if not edits:
        raise ValidationError("no edit records were supplied")
    return edits


def catalog_sources(path: Path) -> tuple[dict[str, set[str]], list[dict[str, str]]]:
    header, rows = read_csv_rows(path, required=CATALOG_REQUIRED)
    del header
    result: dict[str, set[str]] = {}
    for row in rows:
        anchor_id = row.get("ID", "").strip()
        if anchor_id:
            result.setdefault(anchor_id, set()).add(row.get("SourceText", ""))
    return result, rows


def validate_sources(
    edits: Sequence[Edit], sources: dict[str, set[str]], *, allow_source_update: bool
) -> None:
    for edit in edits:
        current = sources.get(edit.anchor_id)
        if not current:
            raise ValidationError(
                f"{edit.origin}: ID {edit.anchor_id} is absent from the current catalog"
            )
        if edit.source not in current and not allow_source_update:
            rendered = ", ".join(repr(value) for value in sorted(current))
            raise ValidationError(
                f"{edit.origin}: SourceText does not exactly match catalog ID "
                f"{edit.anchor_id}; catalog source(s): {rendered}. "
                "Use --allow-source-update only for a coordinated source change."
            )


def load_manual(path: Path, fields: Sequence[str]) -> list[dict[str, str]]:
    _, rows = read_csv_rows(path, required=fields, known_fields=fields)
    normalized: list[dict[str, str]] = []
    for record_number, row in enumerate(rows, start=2):
        anchor_id = row.get("AnchorID", "").strip()
        if not anchor_id and not any(row.get(field, "") for field in fields if field != "N"):
            continue
        if not re.fullmatch(r"\d+", anchor_id):
            raise ValidationError(
                f"{path}:{record_number}: AnchorID must contain digits only: {anchor_id!r}"
            )
        normalized.append({field: row.get(field, "") for field in fields})
    return normalized


def clean_manual(
    rows: Sequence[dict[str, str]],
    *,
    fields: Sequence[str],
    value_field: str,
    edits: Sequence[Edit],
    sources: dict[str, set[str]],
) -> tuple[list[dict[str, str]], CleanupStats]:
    """Deduplicate memory and replace every edited anchor authoritatively."""

    stats = CleanupStats(input_rows=len(rows))
    edited_ids = {edit.anchor_id for edit in edits}
    by_exact: dict[tuple[str, str], dict[str, str]] = {}
    order: list[tuple[str, str]] = []

    for row in rows:
        anchor_id = row["AnchorID"].strip()
        source = row["SourceText"]
        if anchor_id in edited_ids:
            stats.edited_anchor_rows_removed += 1
            continue

        current_sources = sources.get(anchor_id)
        if current_sources and len(current_sources) == 1 and source not in current_sources:
            # A stale source-keyed memory entry is safe to discard: the current
            # catalog gives an unambiguous replacement source for this anchor.
            stats.stale_anchor_rows_removed += 1
            continue

        key = (anchor_id, source)
        previous = by_exact.get(key)
        if previous is None:
            by_exact[key] = dict(row)
            order.append(key)
            continue

        previous_value = previous.get(value_field, "")
        next_value = row.get(value_field, "")
        if previous_value and next_value and previous_value != next_value:
            raise ValidationError(
                f"conflicting {value_field} memory for AnchorID {anchor_id}, "
                f"SourceText={source!r}; supply that ID in the edit CSV to resolve it"
            )
        if not previous_value and next_value:
            previous[value_field] = next_value
        if not previous.get("Notes", "") and row.get("Notes", ""):
            previous["Notes"] = row["Notes"]
        stats.exact_duplicates_removed += 1

    # Different live SourceText values under one non-edited anchor remain unsafe.
    per_anchor: dict[str, set[str]] = {}
    for anchor_id, source in order:
        per_anchor.setdefault(anchor_id, set()).add(source)
    conflicts = {anchor: values for anchor, values in per_anchor.items() if len(values) > 1}
    if conflicts:
        anchor, values = next(iter(sorted(conflicts.items())))
        raise ValidationError(
            f"conflicting source-keyed memory for AnchorID {anchor}: "
            + ", ".join(repr(value) for value in sorted(values))
            + "; supply that ID in the edit CSV to resolve it"
        )

    result = [by_exact[key] for key in order]
    for edit in edits:
        translation = edit.english if value_field == "English" else edit.russian
        prior_notes = ""
        for row in rows:
            if row["AnchorID"].strip() == edit.anchor_id and row["SourceText"] == edit.source:
                prior_notes = row.get("Notes", "")
                if prior_notes:
                    break
        result.append(
            {
                "N": "",
                "AnchorID": edit.anchor_id,
                "SourceText": edit.source,
                value_field: translation,
                "Notes": edit.notes or prior_notes or "manual-translation",
            }
        )

    for index, row in enumerate(result, start=1):
        row["N"] = str(index)
        for field in fields:
            row.setdefault(field, "")
    return result, stats


def render_csv(fields: Sequence[str], rows: Sequence[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=list(fields),
        extrasaction="ignore",
        lineterminator="\n",
        quoting=csv.QUOTE_MINIMAL,
    )
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return stream.getvalue().encode("utf-8")


def replace_files_atomically(payloads: Sequence[tuple[Path, bytes]]) -> None:
    """Prepare all files first and make a best-effort rollback on replace failure."""

    originals = {path: path.read_bytes() if path.exists() else None for path, _ in payloads}
    temp_paths: dict[Path, Path] = {}
    replaced: list[Path] = []
    try:
        for path, payload in payloads:
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="wb", prefix=f".{path.name}.", suffix=".tmp", dir=path.parent, delete=False
            ) as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
                temp_paths[path] = Path(handle.name)
        for path, _ in payloads:
            os.replace(temp_paths[path], path)
            replaced.append(path)
    except OSError as exc:
        for path in reversed(replaced):
            original = originals[path]
            if original is None:
                try:
                    path.unlink()
                except OSError:
                    pass
            else:
                try:
                    path.write_bytes(original)
                except OSError:
                    pass
        raise ValidationError(f"cannot update manual CSV files atomically: {exc}") from exc
    finally:
        for temp_path in temp_paths.values():
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate bilingual localization copy edits and source-aware upsert them "
            "into EnglishManual.csv and RussianManual.csv. Default mode is read-only."
        ),
        epilog=(
            "Example: python docs/tools/_apply_localization_copy_edit.py "
            "docs/tools/localization-copy-edits/wave-01.csv --apply"
        ),
    )
    parser.add_argument("edits", nargs="+", type=Path, help="edit CSV file(s), in order")
    parser.add_argument(
        "--catalog", type=Path, default=ROOT / "Localization" / "Strings.csv",
        help="current Strings.csv catalog (default: %(default)s)",
    )
    parser.add_argument(
        "--english-manual", type=Path,
        default=ROOT / "Localization" / "EnglishManual.csv",
        help="English manual memory (default: %(default)s)",
    )
    parser.add_argument(
        "--russian-manual", type=Path,
        default=ROOT / "Localization" / "RussianManual.csv",
        help="Russian manual memory (default: %(default)s)",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check", action="store_true",
        help="validate and print the proposed update without writing (default)",
    )
    mode.add_argument(
        "--apply", action="store_true",
        help="write both manual memory files after all validation succeeds",
    )
    parser.add_argument(
        "--allow-source-update", action="store_true",
        help=(
            "allow an edit SourceText that differs from the current catalog; this does "
            "not modify the catalog and is only for coordinated source changes"
        ),
    )
    return parser


def run(args: argparse.Namespace) -> None:
    edit_paths = [path.resolve() for path in args.edits]
    edits = load_edits(edit_paths)
    sources, _ = catalog_sources(args.catalog.resolve())
    validate_sources(edits, sources, allow_source_update=args.allow_source_update)

    english_path = args.english_manual.resolve()
    russian_path = args.russian_manual.resolve()
    english_input = load_manual(english_path, ENGLISH_FIELDS)
    russian_input = load_manual(russian_path, RUSSIAN_FIELDS)
    english_rows, english_stats = clean_manual(
        english_input,
        fields=ENGLISH_FIELDS,
        value_field="English",
        edits=edits,
        sources=sources,
    )
    russian_rows, russian_stats = clean_manual(
        russian_input,
        fields=RUSSIAN_FIELDS,
        value_field="Russian",
        edits=edits,
        sources=sources,
    )
    english_payload = render_csv(ENGLISH_FIELDS, english_rows)
    russian_payload = render_csv(RUSSIAN_FIELDS, russian_rows)

    mode = "apply" if args.apply else "check"
    print(f"mode={mode} edits={len(edits)} unique_ids={len({e.anchor_id for e in edits})}")
    print(
        "english-memory: "
        f"input={english_stats.input_rows} output={len(english_rows)} "
        f"deduped={english_stats.exact_duplicates_removed} "
        f"stale={english_stats.stale_anchor_rows_removed} "
        f"replaced={english_stats.edited_anchor_rows_removed}"
    )
    print(
        "russian-memory: "
        f"input={russian_stats.input_rows} output={len(russian_rows)} "
        f"deduped={russian_stats.exact_duplicates_removed} "
        f"stale={russian_stats.stale_anchor_rows_removed} "
        f"replaced={russian_stats.edited_anchor_rows_removed}"
    )
    if args.allow_source_update:
        print("warning: catalog SourceText mismatch allowed; catalog was not modified")

    if args.apply:
        replace_files_atomically(
            ((english_path, english_payload), (russian_path, russian_payload))
        )
        print(f"updated: {english_path}")
        print(f"updated: {russian_path}")
    else:
        print("check passed; no files written (use --apply to update manual memories)")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        run(args)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
