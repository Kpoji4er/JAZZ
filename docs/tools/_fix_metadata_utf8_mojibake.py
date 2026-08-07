#!/usr/bin/env python3
"""Repair one accidental UTF-8 -> Windows-1251 metadata transcoding pass."""

from __future__ import annotations

import argparse
import codecs
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_METADATA = ROOT / "metadata.lua"
FIELDS = ("title", "description", "last_changes")
MOJIBAKE_MARKERS = (
    "Р”",
    "Рµ",
    "Рѕ",
    "Р°",
    "С‚",
    "СЂ",
    "вЂ",
    "в†",
    "в‰",
    "Г—",
)


def field_pattern(field: str) -> re.Pattern[str]:
    return re.compile(
        rf'^(?P<prefix>[ \t]*\'{re.escape(field)}\', ")'
        rf'(?P<value>(?:\\.|[^"\\])*)'
        rf'(?P<suffix>",\s*)$',
        re.MULTILINE,
    )


def mojibake_score(value: str) -> int:
    marker_score = sum(value.count(marker) for marker in MOJIBAKE_MARKERS)
    control_score = sum(1 for char in value if 0x80 <= ord(char) <= 0x9F)
    return marker_score + control_score


def windows_1251_bytes(value: str) -> bytes:
    payload = bytearray()
    for char in value:
        try:
            payload.extend(char.encode("cp1251"))
        except UnicodeEncodeError:
            codepoint = ord(char)
            if 0x80 <= codepoint <= 0x9F:
                payload.append(codepoint)
            else:
                raise
    return bytes(payload)


def repair_value(value: str, field: str) -> str:
    before = mojibake_score(value)
    if before == 0:
        return value
    try:
        repaired = windows_1251_bytes(value).decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"{field}: mojibake is not reversibly Windows-1251 encoded") from exc
    after = mojibake_score(repaired)
    if after >= before:
        raise ValueError(
            f"{field}: repair did not reduce mojibake score ({before} -> {after})"
        )
    return repaired


def repair_metadata(text: str) -> tuple[str, list[str]]:
    result = text
    repaired_fields: list[str] = []
    for field in FIELDS:
        pattern = field_pattern(field)
        match = pattern.search(result)
        if not match:
            raise ValueError(f"{field}: metadata field not found")
        value = match.group("value")
        repaired = repair_value(value, field)
        if repaired != value:
            result = (
                result[: match.start()]
                + match.group("prefix")
                + repaired
                + match.group("suffix")
                + result[match.end() :]
            )
            repaired_fields.append(field)
    return result, repaired_fields


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("metadata", nargs="?", type=Path, default=DEFAULT_METADATA)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    path = args.metadata.resolve()
    original = path.read_bytes()
    bom = original.startswith(codecs.BOM_UTF8)
    text = original.decode("utf-8-sig")
    repaired, fields = repair_metadata(text)

    if fields and not args.apply:
        print(f"metadata mojibake: {', '.join(fields)}")
        return 1
    if not fields:
        print("OK metadata UTF-8 text")
        return 0

    payload = repaired.encode("utf-8")
    if bom:
        payload = codecs.BOM_UTF8 + payload
    path.write_bytes(payload)
    print(f"repaired metadata UTF-8 fields: {', '.join(fields)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
