#!/usr/bin/env python3
"""Build the JAZZ localization copy-review register.

The audit is read-only unless ``--write`` is supplied.  It consumes the
current catalog plus the two source-keyed manual memories and emits one review
record per active catalog row using this schema::

    ID,SourceText,Russian,English,Flags,Decision,Notes

CSV is parsed as records, not physical lines, so quoted multiline text is
preserved throughout.
"""

from __future__ import annotations

import argparse
import csv
import io
import os
import re
import sys
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
CATALOG_REQUIRED = ("ID", "SourceText", "Russian", "English", "Packages", "Locations")
ENGLISH_FIELDS = ("N", "AnchorID", "SourceText", "English", "Notes")
RUSSIAN_FIELDS = ("N", "AnchorID", "SourceText", "Russian", "Notes")
REVIEW_FIELDS = ("ID", "SourceText", "Russian", "English", "Flags", "Decision", "Notes")
CONTEXT_MARKER = "\n[catalog-context]\n"


class AuditError(Exception):
    """A malformed input or unsafe audit state."""


@dataclass
class ManualMemory:
    exact: dict[tuple[str, str], dict[str, str]]
    duplicate_anchors: set[str]
    conflicting_anchors: set[str]
    malformed_rows: int


@dataclass
class PriorReview:
    exact: dict[tuple[str, str], dict[str, str]]
    conflicting_keys: set[tuple[str, str]]


def normalize_header(value: str | None) -> str:
    text = (value or "").strip().lstrip("\ufeff")
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
    missing_ok: bool = False,
) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists() and missing_ok:
        return list(known_fields or required), []
    if not path.is_file():
        raise AuditError(f"CSV file does not exist: {path}")
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            raw_header = next(reader, None)
            if raw_header is None:
                raise AuditError(f"CSV file is empty: {path}")
            header = [normalize_header(value) for value in raw_header]
            aliases = {field.casefold(): field for field in (known_fields or header)}
            header = [aliases.get(value.casefold(), value) for value in header]
            if len(set(header)) != len(header):
                raise AuditError(f"duplicate CSV columns in {path}: {header!r}")
            missing = [field for field in required if field not in header]
            if missing:
                raise AuditError(
                    f"missing columns in {path}: {', '.join(missing)}; got {header!r}"
                )
            rows: list[dict[str, str]] = []
            for record_number, raw in enumerate(reader, start=2):
                if not raw or not any(value != "" for value in raw):
                    continue
                if len(raw) > len(header):
                    raise AuditError(
                        f"{path}: CSV record {record_number} has {len(raw)} fields; "
                        f"header has {len(header)}"
                    )
                raw += [""] * (len(header) - len(raw))
                rows.append(dict(zip(header, raw)))
    except (OSError, UnicodeError, csv.Error) as exc:
        raise AuditError(f"cannot read {path}: {exc}") from exc
    return header, rows


def markup_tokens(text: str) -> Counter[str]:
    token_re = re.compile(
        r"<[^<>\r\n]+>"
        r"|\\[nrt]"
        r"|%(?:\d+\$)?[-+#0 ]*\d*(?:\.\d+)?[A-Za-z]"
        r"|%[A-Za-z_][A-Za-z0-9_]*%?"
        r"|\{[^{}\r\n]+\}"
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


def has_cyrillic(text: str) -> bool:
    return bool(re.search(r"[\u0400-\u052f]", text or ""))


def has_latin(text: str) -> bool:
    return bool(re.search(r"[A-Za-z]", text or ""))


def looks_mojibake(text: str) -> bool:
    # UTF-8 decoded as a single-byte encoding commonly produces alternating
    # Cyrillic Р/С leaders.  Three pairs is conservative for natural Russian.
    return bool(re.search(r"(?:(?:Р|С).){3,}", text or "")) or "ï»¿" in (text or "")


def technical_text(text: str) -> bool:
    value = (text or "").strip()
    if not value:
        return False
    without_markup = re.sub(r"<[^<>]+>|\{[^{}]+\}|%[A-Za-z0-9_$+.# -]+", "", value)
    if not re.search(r"[A-Za-z\u0400-\u052f]", without_markup):
        return True
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.:/+\-]*", value):
        return True
    if re.fullmatch(r"[A-Z0-9_.:/+\- ]+", value) and not re.search(r"[a-z]", value):
        return True
    return False


def natural_latin_text(text: str) -> bool:
    words = re.findall(r"[A-Za-z]{2,}", text or "")
    return len(words) >= 2 or (len(words) == 1 and len(words[0]) >= 5)


def split_notes(*values: str) -> str:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        for part in re.split(r"\s*;\s*", value or ""):
            part = part.strip()
            if part and part not in seen:
                seen.add(part)
                result.append(part)
    return "; ".join(result)


def load_manual(path: Path, fields: Sequence[str], value_field: str) -> ManualMemory:
    _, rows = read_csv_rows(path, required=fields, known_fields=fields)
    by_anchor: dict[str, list[dict[str, str]]] = defaultdict(list)
    malformed = 0
    for row in rows:
        anchor_id = row.get("AnchorID", "").strip()
        source = row.get("SourceText", "")
        if not re.fullmatch(r"\d+", anchor_id) or source == "":
            malformed += 1
            continue
        clean = {field: row.get(field, "") for field in fields}
        clean["AnchorID"] = anchor_id
        by_anchor[anchor_id].append(clean)

    exact: dict[tuple[str, str], dict[str, str]] = {}
    duplicate_anchors: set[str] = set()
    conflicting_anchors: set[str] = set()
    for anchor_id, anchor_rows in by_anchor.items():
        if len(anchor_rows) > 1:
            duplicate_anchors.add(anchor_id)
        variants = {
            (row.get("SourceText", ""), row.get(value_field, "")) for row in anchor_rows
        }
        if len(variants) > 1:
            conflicting_anchors.add(anchor_id)
        for row in anchor_rows:
            key = (anchor_id, row.get("SourceText", ""))
            previous = exact.get(key)
            if previous is None:
                exact[key] = row
            elif not previous.get(value_field, "") and row.get(value_field, ""):
                exact[key] = row
    return ManualMemory(exact, duplicate_anchors, conflicting_anchors, malformed)


def load_prior_review(path: Path) -> PriorReview:
    _, rows = read_csv_rows(
        path, required=REVIEW_FIELDS, known_fields=REVIEW_FIELDS, missing_ok=True
    )
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row.get("ID", "").strip(), row.get("SourceText", ""))].append(row)
    exact: dict[tuple[str, str], dict[str, str]] = {}
    conflicts: set[tuple[str, str]] = set()
    for key, variants in grouped.items():
        decisions = {(row.get("Decision", ""), row.get("Notes", "")) for row in variants}
        if len(decisions) > 1:
            conflicts.add(key)
        exact[key] = variants[-1]
    return PriorReview(exact, conflicts)


RU_CALQUE_PATTERNS = (
    re.compile(r"\bна данный момент времени\b", re.IGNORECASE),
    re.compile(r"\bсогласно данных\b", re.IGNORECASE),
    re.compile(r"\bвыполнить решение\b", re.IGNORECASE),
    re.compile(r"\bбрать за\b", re.IGNORECASE),
    re.compile(r"\bимеет место быть\b", re.IGNORECASE),
)
EN_CALQUE_PATTERNS = (
    re.compile(r"\bon the current moment\b", re.IGNORECASE),
    re.compile(r"\bin the nearest time\b", re.IGNORECASE),
    re.compile(r"\bmake a photo\b", re.IGNORECASE),
    re.compile(r"\btake a decision\b", re.IGNORECASE),
    re.compile(r"\baccording to the data of\b", re.IGNORECASE),
    re.compile(r"\bmore better\b", re.IGNORECASE),
)
WIP_RE = re.compile(
    r"(?:\bWIP\b|\bTODO\b|\bTBD\b|\bPLACEHOLDER\b|\bSTUB\b|заглушк)",
    re.IGNORECASE,
)


def copy_flags(
    *,
    anchor_id: str,
    source: str,
    russian: str,
    english: str,
    notes: str,
    packages: str,
    locations: str,
    duplicate_ids: set[str],
    conflicting_ids: set[str],
    english_memory: ManualMemory,
    russian_memory: ManualMemory,
    prior_conflict: bool,
) -> list[str]:
    flags: set[str] = set()
    technical = "technical-copy" in notes.casefold() or technical_text(source)
    if not anchor_id:
        flags.add("missing-id")
    if source == "":
        flags.add("missing-source")
    if not russian.strip():
        flags.add("missing-ru")
    if not english.strip():
        flags.add("missing-en")
    if not packages or not locations:
        flags.add("catalog-location-incomplete")
    if anchor_id in duplicate_ids:
        flags.add("duplicate-id")
    if anchor_id in conflicting_ids:
        flags.add("duplicate-id-conflict")
    if anchor_id in english_memory.duplicate_anchors:
        flags.add("manual-duplicate-en")
    if anchor_id in english_memory.conflicting_anchors:
        flags.add("manual-conflict-en")
    if anchor_id in russian_memory.duplicate_anchors:
        flags.add("manual-duplicate-ru")
    if anchor_id in russian_memory.conflicting_anchors:
        flags.add("manual-conflict-ru")
    if prior_conflict:
        flags.add("prior-review-conflict")

    note_fold = notes.casefold()
    if "google-draft" in note_fold or "google draft" in note_fold:
        flags.add("google-draft")
    if re.search(r"\b(machine|deepl|google[- ]translate)\b", note_fold):
        flags.add("machine-draft")
    if WIP_RE.search("\n".join((source, russian, english, notes))):
        flags.add("wip-placeholder")
    if looks_mojibake(russian):
        flags.add("mojibake-ru")
    if looks_mojibake(english):
        flags.add("mojibake-en")

    if russian and has_latin(russian) and not has_cyrillic(russian):
        if natural_latin_text(russian) and not technical:
            flags.add("wrong-script-ru")
    if english and has_cyrillic(english) and not technical:
        flags.add("wrong-script-en")

    if any(pattern.search(russian) for pattern in RU_CALQUE_PATTERNS):
        flags.add("machine-calque-ru")
    if any(pattern.search(english) for pattern in EN_CALQUE_PATTERNS):
        flags.add("machine-calque-en")

    expected = markup_tokens(source)
    if russian and markup_tokens(russian) != expected:
        flags.add("markup-mismatch-ru")
    if english and markup_tokens(english) != expected:
        flags.add("markup-mismatch-en")
    return sorted(flags)


def without_catalog_context(notes: str) -> str:
    return (notes or "").split(CONTEXT_MARKER, 1)[0].rstrip()


def review_notes(
    prior_notes: str,
    catalog_notes: str,
    memory_notes: str,
    packages: str,
    locations: str,
) -> str:
    human = without_catalog_context(prior_notes) if prior_notes else split_notes(
        catalog_notes, memory_notes
    )
    context = f"Packages={packages}\nLocations={locations}"
    return (human + CONTEXT_MARKER + context) if human else (CONTEXT_MARKER.lstrip("\n") + context)


def resolved_auto_decision(
    source: str, russian: str, english: str, notes: str, flags: Sequence[str]
) -> str | None:
    if flags:
        return None
    source_equal = russian == source and english == source
    technical = "technical-copy" in notes.casefold() or technical_text(source)
    if technical and source_equal:
        return "approved-technical"
    if source_equal:
        return "approved-source-equal"
    return None


def render_csv(rows: Sequence[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=list(REVIEW_FIELDS),
        extrasaction="ignore",
        lineterminator="\n",
        quoting=csv.QUOTE_MINIMAL,
    )
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in REVIEW_FIELDS})
    return stream.getvalue().encode("utf-8")


def atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", prefix=f".{path.name}.", suffix=".tmp", dir=path.parent, delete=False
        ) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
            temp_path = Path(handle.name)
        os.replace(temp_path, path)
        temp_path = None
    except OSError as exc:
        raise AuditError(f"cannot write {path}: {exc}") from exc
    finally:
        if temp_path is not None:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass


def is_blocking(flag: str, decision: str) -> bool:
    if flag == "google-draft":
        return decision.casefold() != "manual-reviewed-google"
    return flag.startswith(
        (
            "missing-",
            "markup-mismatch-",
            "duplicate-id",
            "manual-conflict-",
            "prior-review-conflict",
            "catalog-location-incomplete",
            "wip-placeholder",
            "mojibake-",
        )
    )


def build_review(
    catalog_rows: Sequence[dict[str, str]],
    english_memory: ManualMemory,
    russian_memory: ManualMemory,
    prior: PriorReview,
) -> tuple[list[dict[str, str]], dict[str, int]]:
    # A row is active when the catalog points to at least one package/location.
    # Rows with only one side populated are still included and flagged.
    active = [
        row
        for row in catalog_rows
        if row.get("Packages", "").strip() or row.get("Locations", "").strip()
    ]
    by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in active:
        by_id[row.get("ID", "").strip()].append(row)
    duplicate_ids = {anchor_id for anchor_id, rows in by_id.items() if len(rows) > 1}
    conflicting_ids = {
        anchor_id
        for anchor_id, rows in by_id.items()
        if len({row.get("SourceText", "") for row in rows}) > 1
    }

    output: list[dict[str, str]] = []
    flag_counts: Counter[str] = Counter()
    retained = 0
    auto = 0
    for catalog in active:
        anchor_id = catalog.get("ID", "").strip()
        source = catalog.get("SourceText", "")
        key = (anchor_id, source)
        english_row = english_memory.exact.get(key, {})
        russian_row = russian_memory.exact.get(key, {})
        english = english_row.get("English", "") or catalog.get("English", "")
        russian = russian_row.get("Russian", "") or catalog.get("Russian", "")
        memory_notes = split_notes(
            english_row.get("Notes", ""), russian_row.get("Notes", "")
        )
        all_notes = split_notes(catalog.get("Notes", ""), memory_notes)
        packages = catalog.get("Packages", "").strip()
        locations = catalog.get("Locations", "").strip()
        previous = prior.exact.get(key, {})

        flags = copy_flags(
            anchor_id=anchor_id,
            source=source,
            russian=russian,
            english=english,
            notes=all_notes,
            packages=packages,
            locations=locations,
            duplicate_ids=duplicate_ids,
            conflicting_ids=conflicting_ids,
            english_memory=english_memory,
            russian_memory=russian_memory,
            prior_conflict=key in prior.conflicting_keys,
        )
        flag_counts.update(flags)
        prior_decision = previous.get("Decision", "").strip()
        if prior_decision:
            decision = prior_decision
            retained += 1
        else:
            decision = resolved_auto_decision(source, russian, english, all_notes, flags) or "pending"
            if decision != "pending":
                auto += 1
        output.append(
            {
                "ID": anchor_id,
                "SourceText": source,
                "Russian": russian,
                "English": english,
                "Flags": ";".join(flags),
                "Decision": decision,
                "Notes": review_notes(
                    previous.get("Notes", ""),
                    catalog.get("Notes", ""),
                    memory_notes,
                    packages,
                    locations,
                ),
            }
        )

    pending = sum(row["Decision"].strip().casefold() in {"", "pending"} for row in output)
    owner_blocked = sum(row["Decision"].strip().casefold() == "owner-blocked" for row in output)
    blocking = 0
    for row in output:
        decision = row["Decision"]
        flags = [flag for flag in row["Flags"].split(";") if flag]
        if decision.strip().casefold() == "owner-blocked" or any(
            is_blocking(flag, decision) for flag in flags
        ):
            blocking += 1
    summary = {
        "catalog_rows": len(catalog_rows),
        "active_rows": len(active),
        "unique_ids": len(by_id),
        "duplicate_ids": len(duplicate_ids),
        "pending": pending,
        "blocking_rows": blocking,
        "owner_blocked": owner_blocked,
        "retained_decisions": retained,
        "auto_decisions": auto,
    }
    summary.update({f"flag:{name}": count for name, count in sorted(flag_counts.items())})
    return output, summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Audit every active localization catalog row for missing copy, draft/style "
            "markers, script errors, placeholder damage, and duplicate IDs. Read-only "
            "unless --write is supplied."
        ),
        epilog=(
            "Examples:\n"
            "  python docs/tools/_audit_localization_copy_quality.py\n"
            "  python docs/tools/_audit_localization_copy_quality.py --write\n"
            "  python docs/tools/_audit_localization_copy_quality.py --strict"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
    parser.add_argument(
        "--review", type=Path, default=ROOT / "Localization" / "CopyReview.csv",
        help="review register to read/preserve and optionally write (default: %(default)s)",
    )
    parser.add_argument(
        "--write", action="store_true",
        help="write CopyReview.csv atomically; without this flag no file is written",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="return exit code 2 when any row is pending or structurally blocking",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    _, catalog_rows = read_csv_rows(args.catalog.resolve(), required=CATALOG_REQUIRED)
    english_memory = load_manual(args.english_manual.resolve(), ENGLISH_FIELDS, "English")
    russian_memory = load_manual(args.russian_manual.resolve(), RUSSIAN_FIELDS, "Russian")
    prior = load_prior_review(args.review.resolve())
    review_rows, summary = build_review(
        catalog_rows, english_memory, russian_memory, prior
    )

    print(
        "copy-audit: "
        f"catalog={summary['catalog_rows']} active={summary['active_rows']} "
        f"unique_ids={summary['unique_ids']} duplicate_ids={summary['duplicate_ids']}"
    )
    print(
        "decisions: "
        f"retained={summary['retained_decisions']} auto={summary['auto_decisions']} "
        f"pending={summary['pending']} owner_blocked={summary['owner_blocked']} "
        f"blocking_rows={summary['blocking_rows']}"
    )
    print(
        "manual-memory: "
        f"english_malformed={english_memory.malformed_rows} "
        f"russian_malformed={russian_memory.malformed_rows}"
    )
    flag_items = [(key[5:], value) for key, value in summary.items() if key.startswith("flag:")]
    if flag_items:
        print("flags: " + " ".join(f"{name}={count}" for name, count in flag_items))
    else:
        print("flags: none")

    if args.write:
        path = args.review.resolve()
        atomic_write(path, render_csv(review_rows))
        print(f"updated: {path}")
    else:
        print("read-only: CopyReview.csv not written (use --write to update it)")

    unresolved = summary["pending"] or summary["blocking_rows"]
    if args.strict and unresolved:
        print(
            f"STRICT FAILED: pending={summary['pending']} "
            f"blocking_rows={summary['blocking_rows']}",
            file=sys.stderr,
        )
        return 2
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except AuditError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
