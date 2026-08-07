#!/usr/bin/env python3
"""Validate and atomically install paired JA3 localization exports."""

from __future__ import annotations

import argparse
import csv
import io
import os
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIELDS = ("ID", "Text", "Translation", "VoiceActor", "Context")


def read_export(path: Path) -> tuple[bytes, set[str]]:
    payload = path.read_bytes()
    text = payload.decode("utf-8-sig")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "sep=,":
        raise ValueError(f"{path}: first line must be 'sep=,'")
    reader = csv.DictReader(io.StringIO("".join(lines[1:])))
    if tuple(reader.fieldnames or ()) != FIELDS:
        raise ValueError(f"{path}: expected header {FIELDS}, got {reader.fieldnames}")

    ids: set[str] = set()
    for number, row in enumerate(reader, start=3):
        loc_id = (row.get("ID") or "").strip()
        if not loc_id.isdigit():
            raise ValueError(f"{path}:{number}: non-numeric localization ID {loc_id!r}")
        if loc_id in ids:
            raise ValueError(f"{path}:{number}: duplicate localization ID {loc_id}")
        ids.add(loc_id)
    return payload, ids


def replace_atomically(path: Path, payload: bytes) -> None:
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("russian_export", type=Path)
    parser.add_argument("english_export", type=Path)
    parser.add_argument("--russian-target", type=Path, default=ROOT / "Russian.csv")
    parser.add_argument("--english-target", type=Path, default=ROOT / "English.csv")
    parser.add_argument("--require-id", action="append", default=[])
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    russian_payload, russian_ids = read_export(args.russian_export.resolve())
    english_payload, english_ids = read_export(args.english_export.resolve())
    if russian_ids != english_ids:
        missing_ru = sorted(english_ids - russian_ids)
        missing_en = sorted(russian_ids - english_ids)
        raise ValueError(
            f"language ID sets differ: missing Russian={missing_ru[:10]}, "
            f"missing English={missing_en[:10]}"
        )
    missing = sorted(set(args.require_id) - russian_ids)
    if missing:
        raise ValueError(f"required localization IDs are absent: {missing}")

    mode = "apply" if args.apply else "check"
    print(f"mode={mode} rows={len(russian_ids)} id_sets=equal")
    if args.apply:
        replace_atomically(args.russian_target.resolve(), russian_payload)
        replace_atomically(args.english_target.resolve(), english_payload)
        print(f"updated: {args.russian_target.resolve()}")
        print(f"updated: {args.english_target.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
