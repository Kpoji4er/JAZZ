#!/usr/bin/env python3
"""Plan, check, or apply the approved JAZZ-UI-RIS-002 editorial data.

Canonical prose comes from ``_ris_copy_bank.py`` and the ``BRIEFS`` mapping in
``_rewrite_ris_legion_briefs.py``.  The default mode is a read-only dry-run.
Use ``--check`` for a drift-sensitive exit code or ``--apply`` to write all
changed targets as one best-effort atomic transaction.

The tool owns these generated projections:

* ``Code/System_RIS_Content.lua``;
* the Major Strategy ``ModItemCode``, existing R.I.S. Email text fields, and
  the nine Major Strategy Email blocks in ``items.lua``;
* the nine Major Strategy Email resources in ``metadata.lua``;
* R.I.S. rows in both runtime localization tables, the working catalog, and
  the two exact-source manual translation memories.
"""

from __future__ import annotations

import argparse
import codecs
import csv
import io
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import _ris_copy_bank as bank
from _rewrite_ris_legion_briefs import BRIEFS


ROOT = Path(__file__).resolve().parents[2]
SPEC_TAG = "JAZZ-UI-RIS-002"
MANUAL_NOTE = "manual-translation"

TARGET_RELATIVE_PATHS = (
    Path("Code/System_RIS_Content.lua"),
    Path("items.lua"),
    Path("metadata.lua"),
    Path("English.csv"),
    Path("Russian.csv"),
    Path("Localization/Strings.csv"),
    Path("Localization/EnglishManual.csv"),
    Path("Localization/RussianManual.csv"),
)

UI_FIELDS = (
    "site_title",
    "tab_bulletin",
    "tab_dossiers",
    "tab_reports",
    "empty_bulletin",
    "empty_dossiers",
    "empty_reports",
    "kills_progress",
    "dossier_locked",
    "section_quest",
    "section_legion",
    "supply_header",
    "mail_archive",
)

AAR_HEADLINES = (
    ("win|low", ("890000000011097", "890000000011098", "890000000011099")),
    ("win|mid", ("890000000011100", "890000000011101", "890000000011102")),
    ("win|high", ("890000000011103", "890000000011104", "890000000011105")),
    ("loss|low", ("890000000011106", "890000000011107", "890000000011108")),
    ("loss|mid", ("890000000011109", "890000000011110", "890000000011111")),
    ("loss|high", ("890000000011112", "890000000011113", "890000000011114")),
    ("retreat|low", ("890000000011115", "890000000011116", "890000000011117")),
    ("retreat|mid", ("890000000011118", "890000000011119", "890000000011120")),
    ("retreat|high", ("890000000011121", "890000000011122", "890000000011123")),
)

AAR_WEATHER = (
    ("clear", "890000000011124"),
    ("rain", "890000000011125"),
    ("night", "890000000011126"),
    ("fog", "890000000011127"),
    ("heat", "890000000011128"),
    ("dust", "890000000011129"),
    ("default", "890000000011130"),
)

AAR_INTENSITY = (
    ("low", "890000000011131"),
    ("mid", "890000000011132"),
    ("high", "890000000011133"),
)

AAR_SECTOR = (
    ("line", "890000000011135"),
    ("poi", "890000000011136"),
)

AAR_QUEST = (
    ("one", "890000000011137"),
    ("one_nonote", "890000000011138"),
    ("many", "890000000011139"),
    ("active", "890000000011140"),
    ("none", "890000000011141"),
)

AAR_CHARACTER = (
    ("win", "890000000011142"),
    ("loss", "890000000011143"),
    ("retreat", "890000000011144"),
    ("ambush", "890000000011145"),
    ("quest_win", "890000000011146"),
    ("quest_loss", "890000000011147"),
    ("quest_retreat", "890000000011148"),
)

AAR_ELITE = (
    ("killed", "890000000011150"),
    ("wounded", "890000000011151"),
    ("escaped", "890000000011152"),
    ("threat", "890000000011153"),
)

AAR_CLOSING = (
    ("quiet", "890000000011154"),
    ("noise", "890000000011155"),
    ("disaster", "890000000011156"),
)

EXTRA_FIELDS = (
    ("strategy_heading", "890000000011340"),
    ("auto_resolve", "890000000011341"),
    ("legacy_title", "890000000011342"),
    ("legacy_body", "890000000011343"),
    ("hostiles_remain", "890000000011344"),
    ("legacy_contact", "890000000011345"),
    ("legacy_opponent", "890000000011346"),
)

KEY_NPCS = (
    "Pierre",
    "Bastien",
    "TheMajor",
    "Spike",
    "Faucheux",
    "CorazonSantiago",
    "Boss",
    "Emma",
    "Biff",
    "FleatownBoss",
    "Luigi",
    "Baron",
    "DiamondRedBoss",
)

BASE_EMAIL_IDS = (
    "RIS_Welcome",
    "RIS_UnitSighting",
    "RIS_EliteObit",
    "RIS_NpcObit",
    *(f"RIS_LegionBrief_{tier}" for tier in BRIEFS),
)

STRATEGY_EMAIL_IDS = tuple(bank.MAJOR_STRATEGY)
EXPECTED_RIS_EMAIL_IDS = frozenset((*BASE_EMAIL_IDS, *STRATEGY_EMAIL_IDS))
STRATEGY_DESIGN_ORDER = tuple(
    copy["design_id"] for copy in bank.MAJOR_STRATEGY.values()
)
STRATEGY_EMAIL_BY_DESIGN = {
    copy["design_id"]: email_id for email_id, copy in bank.MAJOR_STRATEGY.items()
}
STRATEGY_CODE_PATH = "Code/System_RIS_Strategy.lua"
STRATEGY_CODE_ANCHOR = "Code/Guardpost_Patrols.lua"

EXPECTED_ACTIVE_LOC_IDS = frozenset(
    {
        "890000000006920",
        "890000000006921",
        "890000000006939",
        *(str(value) for value in range(890000000006922, 890000000006925)),
        *(str(value) for value in range(890000000011000, 890000000011157)),
        *(str(value) for value in range(890000000011200, 890000000011207)),
        *(str(value) for value in range(890000000011300, 890000000011347)),
    }
)

RUNTIME_FIELDS = ("ID", "Text", "Translation", "VoiceActor", "Context")
CATALOG_FIELDS = (
    "ID",
    "SourceText",
    "VanillaText",
    "Russian",
    "English",
    "Status",
    "Context",
    "Packages",
    "Locations",
    "Notes",
)
ENGLISH_MANUAL_FIELDS = ("N", "AnchorID", "SourceText", "English", "Notes")
RUSSIAN_MANUAL_FIELDS = ("N", "AnchorID", "SourceText", "Russian", "Notes")


class ValidationError(Exception):
    """A refusal caused by ambiguous input or a broken canonical contract."""


@dataclass(frozen=True)
class LocEntry:
    source_en: str
    russian: str
    english: str
    context: str
    category: str
    locations: str


@dataclass(frozen=True)
class EmailSpec:
    email_id: str
    title_id: str
    body_id: str
    sender_id: str
    repeatable: bool | None = None


@dataclass(frozen=True)
class LuaBlock:
    start: int
    end: int
    text: str


@dataclass
class CsvDocument:
    header: list[str]
    rows: list[list[str]]
    sep_prefix: str | None
    delimiter: str
    bom: bool
    newline: str
    original_header: list[str]
    original_rows: list[list[str]]
    raw_header: str
    raw_rows: list[str]

    def clone(self) -> "CsvDocument":
        return CsvDocument(
            list(self.header),
            [list(row) for row in self.rows],
            self.sep_prefix,
            self.delimiter,
            self.bom,
            self.newline,
            list(self.original_header),
            [list(row) for row in self.original_rows],
            self.raw_header,
            list(self.raw_rows),
        )

    def render(self) -> bytes:
        def render_record(record: Sequence[str]) -> str:
            stream = io.StringIO(newline="")
            writer = csv.writer(
                stream,
                delimiter=self.delimiter,
                lineterminator=self.newline,
                quoting=csv.QUOTE_MINIMAL,
            )
            writer.writerow(record)
            return stream.getvalue()

        records: list[str] = []
        if self.sep_prefix is not None:
            records.append(self.sep_prefix + self.newline)
        records.append(
            self.raw_header
            if self.header == self.original_header
            else render_record(self.header)
        )
        for index, row in enumerate(self.rows):
            if index < len(self.original_rows) and row == self.original_rows[index]:
                rendered = self.raw_rows[index]
            else:
                rendered = render_record(row)
            if records and rendered and not records[-1].endswith(("\r", "\n")):
                records.append(self.newline)
            records.append(rendered)
        text = "".join(records)
        payload = text.encode("utf-8")
        return (codecs.BOM_UTF8 + payload) if self.bom else payload


@dataclass(frozen=True)
class FilePlan:
    relative_path: Path
    path: Path
    original: bytes
    desired: bytes

    @property
    def changed(self) -> bool:
        return self.original != self.desired


def _raise_csv_field_limit() -> None:
    limit = sys.maxsize
    while True:
        try:
            csv.field_size_limit(limit)
            return
        except OverflowError:
            limit //= 10


_raise_csv_field_limit()


def _find_simple_string(localization_id: str) -> tuple[str, str]:
    matches = [
        (source_en, russian)
        for candidate, source_en, russian in bank.ALL_SIMPLE_STRINGS
        if candidate == localization_id
    ]
    if len(matches) != 1:
        raise ValidationError(
            f"canonical simple string {localization_id}: expected one row, found {len(matches)}"
        )
    return matches[0]


def build_localization_map() -> dict[str, LocEntry]:
    """Build the complete active R.I.S. ID map and reject conflicting IDs."""

    entries: dict[str, LocEntry] = {}
    origins: dict[str, str] = {}

    def register(
        localization_id: str,
        source_en: str,
        russian: str,
        category: str,
        locations: str,
        *,
        english: str | None = None,
        origin: str,
    ) -> None:
        if not re.fullmatch(r"\d+", localization_id):
            raise ValidationError(f"{origin}: non-numeric localization id {localization_id!r}")
        if not source_en or not russian or not (english if english is not None else source_en):
            raise ValidationError(f"{origin}: empty source or translation")
        if any(
            "<field_note>" in value
            for value in (source_en, russian, english if english is not None else source_en)
        ):
            raise ValidationError(f"{origin}: forbidden <field_note> placeholder")
        entry = LocEntry(
            source_en=source_en,
            russian=russian,
            english=english if english is not None else source_en,
            context=f"{SPEC_TAG}:{category}",
            category=category,
            locations=locations,
        )
        previous = entries.get(localization_id)
        if previous is not None:
            previous_copy = (previous.source_en, previous.russian, previous.english)
            next_copy = (entry.source_en, entry.russian, entry.english)
            if previous_copy != next_copy:
                raise ValidationError(
                    f"localization id {localization_id} has conflicting copy: "
                    f"{origins[localization_id]}={previous_copy!r}, {origin}={next_copy!r}"
                )
            return
        entries[localization_id] = entry
        origins[localization_id] = origin

    desk_sender_en, desk_sender_ru = _find_simple_string("890000000011200")
    fixed_strings = (
        (
            "890000000006920",
            "R.I.S.",
            "R.I.S.",
            "brand",
            "jazz:Code/System_RIS_Mail.lua",
        ),
        (
            "890000000006921",
            desk_sender_en,
            desk_sender_ru,
            "welcome.sender",
            "jazz:items.lua",
        ),
        (
            "890000000006939",
            "R.I.S. <legion-desk@ris-intel.net>",
            "R.I.S. <legion-desk@ris-intel.net>",
            "supply_brief.sender",
            "jazz:items.lua",
        ),
    )
    for localization_id, source_en, russian, category, locations in fixed_strings:
        register(
            localization_id,
            source_en,
            russian,
            category,
            locations,
            origin=f"fixed[{localization_id}]",
        )

    welcome_categories = ("welcome.title", "welcome.body", "welcome.description")
    for index, (localization_id, source_en, russian) in enumerate(bank.WELCOME_FIXES):
        register(
            localization_id,
            source_en,
            russian,
            welcome_categories[index],
            "jazz:items.lua" if index < 2 else "jazz:Code/System_RIS_Mail.lua",
            origin=f"WELCOME_FIXES[{index}]",
        )

    if len(bank.UI_FIXES) != len(UI_FIELDS):
        raise ValidationError(
            f"UI field count mismatch: fields={len(UI_FIELDS)} bank={len(bank.UI_FIXES)}"
        )
    for field, (localization_id, source_en, russian) in zip(
        UI_FIELDS, bank.UI_FIXES, strict=True
    ):
        register(
            localization_id,
            source_en,
            russian,
            f"ui.{field}",
            "jazz:Code/System_RIS_Content.lua",
            origin=f"UI_FIXES[{field}]",
        )

    for dossier_id, copy in bank.DOSSIERS.items():
        ids = bank.DOSSIER_LOC_IDS.get(dossier_id)
        if ids is None:
            raise ValidationError(f"missing DOSSIER_LOC_IDS entry for {dossier_id}")
        for field in ("title", "body"):
            register(
                ids[f"{field}_id"],
                copy[f"{field}_en"],
                copy[f"{field}_ru"],
                f"dossier.{dossier_id}.{field}",
                "jazz:Code/System_RIS_Content.lua",
                origin=f"DOSSIERS[{dossier_id!r}].{field}",
            )

    for dossier_id, copy in bank.QUEST_DOSSIERS.items():
        ids = bank.QUEST_DOSSIER_LOC_IDS.get(dossier_id)
        if ids is None:
            raise ValidationError(f"missing QUEST_DOSSIER_LOC_IDS entry for {dossier_id}")
        for field in ("title", "body"):
            register(
                ids[f"{field}_id"],
                copy[f"{field}_en"],
                copy[f"{field}_ru"],
                f"quest_dossier.{dossier_id}.{field}",
                "jazz:Code/System_RIS_Content.lua",
                origin=f"QUEST_DOSSIERS[{dossier_id!r}].{field}",
            )

    aar_context: dict[str, str] = {}
    for key, localization_ids in AAR_HEADLINES:
        for variant, localization_id in enumerate(localization_ids, start=1):
            aar_context[localization_id] = f"aar.headline.{key}.variant{variant}"
    for key, localization_id in AAR_WEATHER:
        aar_context[localization_id] = f"aar.weather.{key}"
    for key, localization_id in AAR_INTENSITY:
        aar_context[localization_id] = f"aar.intensity.{key}"
    aar_context["890000000011134"] = "aar.forces"
    for key, localization_id in AAR_SECTOR:
        aar_context[localization_id] = f"aar.sector.{key}"
    for key, localization_id in AAR_QUEST:
        aar_context[localization_id] = f"aar.quest.{key}"
    for key, localization_id in AAR_CHARACTER:
        aar_context[localization_id] = f"aar.character.{key}"
    aar_context["890000000011149"] = "aar.losses"
    for key, localization_id in AAR_ELITE:
        aar_context[localization_id] = f"aar.elite.{key}"
    for key, localization_id in AAR_CLOSING:
        aar_context[localization_id] = f"aar.closing.{key}"

    for index, (localization_id, source_en, russian) in enumerate(bank.AAR_FIXES):
        category = aar_context.get(localization_id)
        if category is None:
            raise ValidationError(f"AAR_FIXES[{index}]: unstructured id {localization_id}")
        register(
            localization_id,
            source_en,
            russian,
            category,
            "jazz:Code/System_RIS_Content.lua",
            origin=f"AAR_FIXES[{index}]",
        )
    if set(aar_context) != {row[0] for row in bank.AAR_FIXES}:
        raise ValidationError("AAR structure and canonical ID set differ")

    field_categories = (
        "field_mail.sender",
        "field_mail.sighting.title",
        "field_mail.sighting.body",
        "field_mail.elite_obit.title",
        "field_mail.elite_obit.body",
        "field_mail.npc_obit.title",
        "field_mail.npc_obit.body",
    )
    for index, (localization_id, source_en, russian) in enumerate(bank.FIELD_MAIL_FIXES):
        register(
            localization_id,
            source_en,
            russian,
            field_categories[index],
            "jazz:items.lua",
            origin=f"FIELD_MAIL_FIXES[{index}]",
        )

    for tier, copy in BRIEFS.items():
        for field in ("title", "body"):
            register(
                copy[f"{field}_id"],
                copy[f"{field}_en"],
                copy[f"{field}_ru"],
                f"supply_brief.{tier}.{field}",
                "jazz:items.lua",
                origin=f"BRIEFS[{tier!r}].{field}",
            )

    for email_id, copy in bank.MAJOR_STRATEGY.items():
        for field in ("title", "body"):
            register(
                copy[f"{field}_id"],
                copy[f"{field}_en"],
                copy[f"{field}_ru"],
                f"strategy.{copy['design_id']}.{field}",
                "jazz:Code/System_RIS_Content.lua | jazz:items.lua",
                origin=f"MAJOR_STRATEGY[{email_id!r}].{field}",
            )

    extra_by_id = {localization_id: key for key, localization_id in EXTRA_FIELDS}
    for index, (localization_id, source_en, russian) in enumerate(
        bank.RIS_EXTRA_STRINGS
    ):
        key = extra_by_id.get(localization_id)
        if key is None:
            raise ValidationError(f"RIS_EXTRA_STRINGS[{index}]: unexpected id {localization_id}")
        register(
            localization_id,
            source_en,
            russian,
            f"extra.{key}",
            "jazz:Code/System_RIS_Content.lua",
            origin=f"RIS_EXTRA_STRINGS[{index}]",
        )

    actual_ids = frozenset(entries)
    if actual_ids != EXPECTED_ACTIVE_LOC_IDS:
        missing = sorted(EXPECTED_ACTIVE_LOC_IDS - actual_ids, key=int)
        unexpected = sorted(actual_ids - EXPECTED_ACTIVE_LOC_IDS, key=int)
        raise ValidationError(
            f"active localization ID coverage mismatch: missing={missing!r}, "
            f"unexpected={unexpected!r}"
        )
    return entries


def run_canonical_audit() -> None:
    """Reuse the approved copy audit, including placeholder parity."""

    try:
        import _audit_ris_copy
    except ImportError as exc:
        raise ValidationError(f"cannot import _audit_ris_copy.py: {exc}") from exc
    errors, _pair_count, _localization_id_count = _audit_ris_copy.audit()
    if errors:
        preview = "\n".join(f"  - {message}" for message in errors[:20])
        suffix = "\n  - ..." if len(errors) > 20 else ""
        raise ValidationError(
            f"canonical R.I.S. copy audit failed ({len(errors)} errors):\n"
            f"{preview}{suffix}"
        )


def lua_escape(value: str) -> str:
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    escaped = (
        normalized.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\t", "\\t")
        .replace("\n", "\\n")
    )
    if "\n" in escaped or "\r" in escaped:
        raise ValidationError("lua_escape left a raw newline in a quoted payload")
    return escaped


def lua_unescape(value: str) -> str:
    result: list[str] = []
    index = 0
    mapping = {"n": "\n", "r": "\r", "t": "\t", '"': '"', "'": "'", "\\": "\\"}
    while index < len(value):
        char = value[index]
        if char != "\\":
            result.append(char)
            index += 1
            continue
        if index + 1 >= len(value):
            raise ValidationError("trailing backslash in Lua string")
        escaped = value[index + 1]
        if escaped not in mapping:
            raise ValidationError(f"unsupported Lua escape \\{escaped}")
        result.append(mapping[escaped])
        index += 2
    return "".join(result)


def assert_no_raw_newlines_in_lua_strings(text: str, label: str) -> None:
    index = 0
    while index < len(text):
        if text.startswith("--[[", index):
            end = text.find("]]", index + 4)
            if end < 0:
                raise ValidationError(f"{label}: unterminated Lua block comment")
            index = end + 2
            continue
        if text.startswith("--", index):
            end = text.find("\n", index + 2)
            index = len(text) if end < 0 else end + 1
            continue
        if text.startswith("[[", index):
            end = text.find("]]", index + 2)
            if end < 0:
                raise ValidationError(f"{label}: unterminated Lua long string")
            index = end + 2
            continue
        quote = text[index]
        if quote not in {'"', "'"}:
            index += 1
            continue
        index += 1
        while index < len(text):
            char = text[index]
            if char in "\r\n":
                raise ValidationError(f"{label}: raw newline inside a Lua string")
            if char == "\\":
                index += 2
                continue
            index += 1
            if char == quote:
                break
        else:
            raise ValidationError(f"{label}: unterminated Lua string")


def _tref(entries: dict[str, LocEntry], localization_id: str) -> str:
    try:
        source = entries[localization_id].source_en
    except KeyError as exc:
        raise ValidationError(f"content generator references unknown id {localization_id}") from exc
    return f'T({localization_id}, "{lua_escape(source)}")'


def generate_content_lua(entries: dict[str, LocEntry]) -> str:
    lines = [
        "-- R.I.S. editorial content banks (generated by docs/tools/_apply_ris_editorial.py).",
        "-- GENERATED_FILE / ownership boundary (JAZZ-UI-RIS-002):",
        "--   Do not hand-edit numeric T(...) IDs or dossier/AAR/strategy payload tables.",
        "--   Re-run docs/tools/_apply_ris_editorial.py --apply to refresh.",
        "--   Runtime code may read these globals; treat this file as data-only.",
        "",
        "JAZZ_RIS_KILL_THRESHOLD = 3",
        "JAZZ_RIS_BATTLE_CAP = 20",
        "",
        "JAZZ_RIS_UI = {",
    ]
    for field, (localization_id, _source_en, _russian) in zip(
        UI_FIELDS, bank.UI_FIXES, strict=True
    ):
        lines.append(f"\t{field} = {_tref(entries, localization_id)},")
    lines.extend(("}", "", "JAZZ_RIS_DOSSIERS = {"))

    for dossier_id, copy in bank.DOSSIERS.items():
        del copy
        ids = bank.DOSSIER_LOC_IDS[dossier_id]
        lines.append(
            f'\t["{dossier_id}"] = {{ '
            f"title = {_tref(entries, ids['title_id'])}, "
            f"body = {_tref(entries, ids['body_id'])} "
            "},"
        )
    lines.extend(("}", "", "JAZZ_RIS_QUEST_DOSSIERS = {"))

    for dossier_id, copy in bank.QUEST_DOSSIERS.items():
        del copy
        ids = bank.QUEST_DOSSIER_LOC_IDS[dossier_id]
        lines.append(
            f'\t["{dossier_id}"] = {{ '
            f"title = {_tref(entries, ids['title_id'])}, "
            f"body = {_tref(entries, ids['body_id'])} "
            "},"
        )
    lines.extend(("}", "", "JAZZ_RIS_AAR = {", "\theadlines = {"))

    for key, localization_ids in AAR_HEADLINES:
        variants = ", ".join(_tref(entries, value) for value in localization_ids)
        lines.append(f'\t\t["{key}"] = {{ {variants} }},')
    lines.extend(("\t},", "\tweather = {"))
    for key, localization_id in AAR_WEATHER:
        lines.append(f"\t\t{key} = {_tref(entries, localization_id)},")
    lines.extend(("\t},", "\tintensity = {"))
    for key, localization_id in AAR_INTENSITY:
        lines.append(f"\t\t{key} = {_tref(entries, localization_id)},")
    lines.extend(
        (
            "\t},",
            f"\tforces = {_tref(entries, '890000000011134')},",
            "\tsector = {",
        )
    )
    for key, localization_id in AAR_SECTOR:
        lines.append(f"\t\t{key} = {_tref(entries, localization_id)},")
    lines.extend(("\t},", "\tquest = {"))
    for key, localization_id in AAR_QUEST:
        lines.append(f"\t\t{key} = {_tref(entries, localization_id)},")
    lines.extend(("\t},", "\tcharacter = {"))
    for key, localization_id in AAR_CHARACTER:
        lines.append(f"\t\t{key} = {_tref(entries, localization_id)},")
    lines.extend(
        (
            "\t},",
            f"\tlosses = {_tref(entries, '890000000011149')},",
            "\telite = {",
        )
    )
    for key, localization_id in AAR_ELITE:
        lines.append(f"\t\t{key} = {_tref(entries, localization_id)},")
    lines.extend(("\t},", "\tclosing = {"))
    for key, localization_id in AAR_CLOSING:
        lines.append(f"\t\t{key} = {_tref(entries, localization_id)},")
    lines.extend(("\t},", "}", "", "JAZZ_RIS_STRATEGY = {"))

    for email_id, copy in bank.MAJOR_STRATEGY.items():
        lines.extend(
            (
                f'\t["{email_id}"] = {{',
                f'\t\temail_id = "{email_id}",',
                f'\t\tdesign_id = "{copy["design_id"]}",',
                f"\t\ttitle = {_tref(entries, copy['title_id'])},",
                f"\t\tbody = {_tref(entries, copy['body_id'])},",
                "\t},",
            )
        )
    lines.extend(("}", "", "JAZZ_RIS_EXTRA = {"))
    for key, localization_id in EXTRA_FIELDS:
        lines.append(f"\t{key} = {_tref(entries, localization_id)},")
    lines.extend(
        (
            "}",
            "",
            "-- Key NPC session_ids for R.I.S. obituaries (same desk queue).",
            "JAZZ_RIS_KEY_NPCS = {",
        )
    )
    for npc_id in KEY_NPCS:
        lines.append(f"\t{npc_id} = true,")
    lines.extend(("}", ""))

    content = "\n".join(lines)
    assert_no_raw_newlines_in_lua_strings(content, "System_RIS_Content.lua")
    if "<field_note>" in content:
        raise ValidationError("System_RIS_Content.lua: forbidden <field_note>")
    if content.count("JAZZ_RIS_KILL_THRESHOLD = 3") != 1:
        raise ValidationError("System_RIS_Content.lua: kill threshold constant drift")
    if content.count("JAZZ_RIS_BATTLE_CAP = 20") != 1:
        raise ValidationError("System_RIS_Content.lua: battle cap constant drift")
    if content.count("JAZZ_RIS_KEY_NPCS = {") != 1:
        raise ValidationError("System_RIS_Content.lua: KEY_NPCS block count drift")
    if content.count("JAZZ_RIS_STRATEGY = {") != 1:
        raise ValidationError("System_RIS_Content.lua: strategy block count drift")

    expected_t_ids = {row[0] for row in bank.UI_FIXES}
    for ids in (*bank.DOSSIER_LOC_IDS.values(), *bank.QUEST_DOSSIER_LOC_IDS.values()):
        expected_t_ids.update((ids["title_id"], ids["body_id"]))
    expected_t_ids.update(row[0] for row in bank.AAR_FIXES)
    for strategy in bank.MAJOR_STRATEGY.values():
        expected_t_ids.update((strategy["title_id"], strategy["body_id"]))
    expected_t_ids.update(row[0] for row in bank.RIS_EXTRA_STRINGS)
    actual_t_ids = re.findall(r"\bT\(\s*(\d+)\s*,", content)
    if len(actual_t_ids) != len(set(actual_t_ids)):
        raise ValidationError("System_RIS_Content.lua: duplicate localization T id")
    if set(actual_t_ids) != expected_t_ids:
        missing = sorted(expected_t_ids - set(actual_t_ids), key=int)
        unexpected = sorted(set(actual_t_ids) - expected_t_ids, key=int)
        raise ValidationError(
            "System_RIS_Content.lua: localization T ids differ from canon: "
            f"missing={missing!r}, unexpected={unexpected!r}"
        )
    return content


def _matching_brace(text: str, opening: int, label: str) -> int:
    depth = 0
    index = opening
    while index < len(text):
        if text.startswith("--[[", index):
            end = text.find("]]", index + 4)
            if end < 0:
                raise ValidationError(f"{label}: unterminated block comment")
            index = end + 2
            continue
        if text.startswith("--", index):
            end = text.find("\n", index + 2)
            index = len(text) if end < 0 else end + 1
            continue
        if text.startswith("[[", index):
            end = text.find("]]", index + 2)
            if end < 0:
                raise ValidationError(f"{label}: unterminated long string")
            index = end + 2
            continue
        char = text[index]
        if char in {'"', "'"}:
            quote = char
            index += 1
            while index < len(text):
                char = text[index]
                if char in "\r\n":
                    raise ValidationError(f"{label}: raw newline inside quoted string")
                if char == "\\":
                    index += 2
                    continue
                index += 1
                if char == quote:
                    break
            else:
                raise ValidationError(f"{label}: unterminated quoted string")
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
            if depth < 0:
                raise ValidationError(f"{label}: unexpected closing brace")
        index += 1
    raise ValidationError(f"{label}: unterminated PlaceObj table")


def find_placeobj_blocks(text: str, class_name: str) -> list[LuaBlock]:
    pattern = re.compile(
        rf"^[ \t]*(?P<call>PlaceObj\(\s*(['\"]){re.escape(class_name)}\2\s*,\s*\{{)",
        re.MULTILINE,
    )
    blocks: list[LuaBlock] = []
    for match in pattern.finditer(text):
        opening = match.end() - 1
        closing = _matching_brace(text, opening, class_name)
        end = closing + 1
        while end < len(text) and text[end] in " \t":
            end += 1
        if end >= len(text) or text[end] != ")":
            raise ValidationError(
                f"{class_name} block at offset {match.start()}: missing closing parenthesis"
            )
        end += 1
        while end < len(text) and text[end] in " \t":
            end += 1
        if end < len(text) and text[end] == ",":
            end += 1
        start = match.start("call")
        blocks.append(LuaBlock(start, end, text[start:end]))
    return blocks


def _one_property_match(block: str, pattern: re.Pattern[str], label: str) -> re.Match[str]:
    matches = list(pattern.finditer(block))
    if len(matches) != 1:
        raise ValidationError(f"{label}: expected one property, found {len(matches)}")
    return matches[0]


EMAIL_ID_RE = re.compile(
    r'^[ \t]*id[ \t]*=[ \t]*"(?P<value>(?:\\.|[^"\\\r\n])*)"[ \t]*,[ \t]*\r?$',
    re.MULTILINE,
)


def index_email_blocks(text: str) -> dict[str, LuaBlock]:
    indexed: dict[str, LuaBlock] = {}
    first_offsets: dict[str, int] = {}
    for block in find_placeobj_blocks(text, "ModItemEmail"):
        match = _one_property_match(block.text, EMAIL_ID_RE, "ModItemEmail.id")
        email_id = lua_unescape(match.group("value"))
        if email_id in indexed:
            raise ValidationError(
                f"duplicate active ModItemEmail id {email_id!r} at offsets "
                f"{first_offsets[email_id]} and {block.start}"
            )
        indexed[email_id] = block
        first_offsets[email_id] = block.start
    return indexed


CODE_FILE_NAME_RE = re.compile(
    r'^[ \t]*[\'"]CodeFileName[\'"][ \t]*,[ \t]*'
    r'"(?P<value>[^"\r\n]+)"[ \t]*,[ \t]*\r?$',
    re.MULTILINE,
)


def _code_item_blocks(text: str, code_path: str) -> list[LuaBlock]:
    matches: list[LuaBlock] = []
    for block in find_placeobj_blocks(text, "ModItemCode"):
        fields = list(CODE_FILE_NAME_RE.finditer(block.text))
        if len(fields) != 1:
            raise ValidationError(
                f"ModItemCode at offset {block.start}: expected one CodeFileName, "
                f"found {len(fields)}"
            )
        if fields[0].group("value") == code_path:
            matches.append(block)
    return matches


def _new_strategy_code_item(indent: str, newline: str) -> str:
    property_indent = indent + "\t"
    return newline.join(
        (
            f"{indent}PlaceObj('ModItemCode', {{",
            f'{property_indent}\'name\', "System_RIS_Strategy",',
            f'{property_indent}\'CodeFileName\', "{STRATEGY_CODE_PATH}",',
            f"{indent}}}),",
        )
    )


def patch_strategy_code_item(text: str) -> str:
    """Keep one editor-owned code item after Guardpost_Patrols."""

    newline = _detect_newline(text)
    anchors = _code_item_blocks(text, STRATEGY_CODE_ANCHOR)
    targets = _code_item_blocks(text, STRATEGY_CODE_PATH)
    if len(anchors) != 1:
        raise ValidationError(
            "items.lua: expected one Guardpost_Patrols ModItemCode anchor, "
            f"found {len(anchors)}"
        )
    if len(targets) > 1:
        raise ValidationError("items.lua: duplicate System_RIS_Strategy ModItemCode")

    if targets and targets[0].start < anchors[0].start:
        target = targets[0]
        text = text[: target.start] + text[target.end :]
        anchors = _code_item_blocks(text, STRATEGY_CODE_ANCHOR)
        targets = []

    if not targets:
        anchor = anchors[0]
        indent = _block_indent(text, anchor.start)
        block = _new_strategy_code_item(indent, newline)
        text = text[: anchor.end] + newline + block + text[anchor.end :]

    anchors = _code_item_blocks(text, STRATEGY_CODE_ANCHOR)
    targets = _code_item_blocks(text, STRATEGY_CODE_PATH)
    if len(anchors) != 1 or len(targets) != 1 or targets[0].start <= anchors[0].start:
        raise ValidationError(
            "items.lua: Strategy observer must have one ModItemCode after Guardpost_Patrols"
        )
    return text


def _split_line_ending(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n") or line.endswith("\r"):
        return line[:-1], line[-1]
    return line, ""


def _patch_t_property(
    block: str,
    email_id: str,
    field: str,
    localization_id: str,
    source_en: str,
) -> str:
    pattern = re.compile(
        rf"(?P<prefix>[ \t]*{re.escape(field)}[ \t]*=[ \t]*)"
        r"T\([ \t]*(?P<id>\d+)[ \t]*,[ \t]*"
        r"(?:--\[\[[^\r\n]*?\]\][ \t]*)?"
        r'"(?P<source>(?:\\.|[^"\\\r\n])*)"[ \t]*\)'
        r"(?P<suffix>[ \t]*,[ \t]*)"
    )
    lines = block.splitlines(keepends=True)
    matches: list[tuple[int, re.Match[str], str]] = []
    for index, line in enumerate(lines):
        body, ending = _split_line_ending(line)
        match = pattern.fullmatch(body)
        if match:
            matches.append((index, match, ending))
    if len(matches) != 1:
        raise ValidationError(
            f"ModItemEmail {email_id}.{field}: expected one T property, found {len(matches)}"
        )
    index, match, ending = matches[0]
    lines[index] = (
        f"{match.group('prefix')}T({localization_id}, "
        f"--[[ModItemEmail {email_id} {field}]] \"{lua_escape(source_en)}\")"
        f"{match.group('suffix')}{ending}"
    )
    return "".join(lines)


def _extract_t_property(block: str, email_id: str, field: str) -> tuple[str, str]:
    pattern = re.compile(
        rf"^[ \t]*{re.escape(field)}[ \t]*=[ \t]*"
        r"T\([ \t]*(?P<id>\d+)[ \t]*,[ \t]*"
        r"(?:--\[\[[^\r\n]*?\]\][ \t]*)?"
        r'"(?P<source>(?:\\.|[^"\\\r\n])*)"[ \t]*\)'
        r"[ \t]*,[ \t]*\r?$",
        re.MULTILINE,
    )
    match = _one_property_match(block, pattern, f"ModItemEmail {email_id}.{field}")
    return match.group("id"), lua_unescape(match.group("source"))


def _set_repeatable_false(block: str, email_id: str, newline: str) -> str:
    pattern = re.compile(
        r"^(?P<prefix>[ \t]*repeatable[ \t]*=[ \t]*)"
        r"(?P<value>true|false)(?P<suffix>[ \t]*,[ \t]*)\r?$",
        re.MULTILINE,
    )
    matches = list(pattern.finditer(block))
    if len(matches) > 1:
        raise ValidationError(f"ModItemEmail {email_id}: ambiguous repeatable properties")
    if len(matches) == 1:
        match = matches[0]
        return (
            block[: match.start()]
            + match.group("prefix")
            + "false"
            + match.group("suffix")
            + block[match.end() :]
        )

    lines = block.splitlines(keepends=True)
    label_re = re.compile(r'^(?P<indent>[ \t]*)label[ \t]*=[ \t]*".*"[ \t]*,[ \t]*$')
    label_matches: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        body, _ending = _split_line_ending(line)
        match = label_re.fullmatch(body)
        if match:
            label_matches.append((index, match.group("indent")))
    if len(label_matches) != 1:
        raise ValidationError(
            f"ModItemEmail {email_id}: cannot anchor repeatable=false after label"
        )
    index, indent = label_matches[0]
    ending = _split_line_ending(lines[index])[1] or newline
    lines.insert(index + 1, f"{indent}repeatable = false,{ending}")
    return "".join(lines)


def _extract_repeatable(block: str, email_id: str) -> bool | None:
    pattern = re.compile(
        r"^[ \t]*repeatable[ \t]*=[ \t]*(true|false)[ \t]*,[ \t]*\r?$",
        re.MULTILINE,
    )
    matches = list(pattern.finditer(block))
    if len(matches) > 1:
        raise ValidationError(f"ModItemEmail {email_id}: duplicate repeatable properties")
    if not matches:
        return None
    return matches[0].group(1) == "true"


def build_email_specs() -> dict[str, EmailSpec]:
    specs = {
        "RIS_Welcome": EmailSpec(
            "RIS_Welcome",
            "890000000006922",
            "890000000006923",
            "890000000006921",
        ),
        "RIS_UnitSighting": EmailSpec(
            "RIS_UnitSighting",
            "890000000011201",
            "890000000011202",
            "890000000011200",
        ),
        "RIS_EliteObit": EmailSpec(
            "RIS_EliteObit",
            "890000000011203",
            "890000000011204",
            "890000000011200",
        ),
        "RIS_NpcObit": EmailSpec(
            "RIS_NpcObit",
            "890000000011205",
            "890000000011206",
            "890000000011200",
        ),
    }
    for tier, copy in BRIEFS.items():
        email_id = f"RIS_LegionBrief_{tier}"
        specs[email_id] = EmailSpec(
            email_id,
            copy["title_id"],
            copy["body_id"],
            "890000000006939",
        )
    for email_id, copy in bank.MAJOR_STRATEGY.items():
        specs[email_id] = EmailSpec(
            email_id,
            copy["title_id"],
            copy["body_id"],
            "890000000011200",
            repeatable=False,
        )
    if frozenset(specs) != EXPECTED_RIS_EMAIL_IDS:
        raise ValidationError("Email spec IDs do not match the approved R.I.S. set")
    return specs


def _detect_newline(text: str) -> str:
    crlf = text.count("\r\n")
    bare_lf = text.count("\n") - crlf
    return "\r\n" if crlf > bare_lf else "\n"


def _block_indent(text: str, start: int) -> str:
    line_start = text.rfind("\n", 0, start) + 1
    indent = text[line_start:start]
    if indent.strip():
        raise ValidationError(f"PlaceObj at offset {start} is not line-indented normally")
    return indent


def _new_email_block(
    indent: str,
    newline: str,
    spec: EmailSpec,
    entries: dict[str, LocEntry],
) -> str:
    property_indent = indent + "\t"
    body = entries[spec.body_id].source_en
    sender = entries[spec.sender_id].source_en
    title = entries[spec.title_id].source_en
    lines = [
        f"{indent}PlaceObj('ModItemEmail', {{",
        f"{property_indent}body = T({spec.body_id}, "
        f"--[[ModItemEmail {spec.email_id} body]] \"{lua_escape(body)}\"),",
        f"{property_indent}delayAfterCombat = false,",
        f'{property_indent}group = "Default",',
        f'{property_indent}id = "{spec.email_id}",',
        f'{property_indent}label = "Important",',
        f"{property_indent}repeatable = false,",
        f"{property_indent}sender = T({spec.sender_id}, "
        f"--[[ModItemEmail {spec.email_id} sender]] \"{lua_escape(sender)}\"),",
        f"{property_indent}title = T({spec.title_id}, "
        f"--[[ModItemEmail {spec.email_id} title]] \"{lua_escape(title)}\"),",
        f"{indent}}}),",
    ]
    return newline.join(lines)


def _replace_blocks(text: str, replacements: Iterable[tuple[LuaBlock, str]]) -> str:
    ordered = sorted(replacements, key=lambda pair: pair[0].start, reverse=True)
    previous_start = len(text) + 1
    for block, replacement in ordered:
        if block.end > previous_start:
            raise ValidationError("overlapping Lua block replacements")
        text = text[: block.start] + replacement + text[block.end :]
        previous_start = block.start
    return text


def validate_items_projection(
    text: str,
    specs: dict[str, EmailSpec],
    entries: dict[str, LocEntry],
) -> None:
    anchors = _code_item_blocks(text, STRATEGY_CODE_ANCHOR)
    strategy_code_items = _code_item_blocks(text, STRATEGY_CODE_PATH)
    if (
        len(anchors) != 1
        or len(strategy_code_items) != 1
        or strategy_code_items[0].start <= anchors[0].start
    ):
        raise ValidationError(
            "items.lua: expected one System_RIS_Strategy ModItemCode after "
            "Guardpost_Patrols"
        )
    indexed = index_email_blocks(text)
    actual_ris_ids = frozenset(email_id for email_id in indexed if email_id.startswith("RIS_"))
    if actual_ris_ids != EXPECTED_RIS_EMAIL_IDS:
        missing = sorted(EXPECTED_RIS_EMAIL_IDS - actual_ris_ids)
        unexpected = sorted(actual_ris_ids - EXPECTED_RIS_EMAIL_IDS)
        raise ValidationError(
            f"active R.I.S. Email IDs mismatch: missing={missing!r}, unexpected={unexpected!r}"
        )
    actual_strategy = frozenset(
        email_id for email_id in actual_ris_ids if email_id.startswith("RIS_MajorStrategy_")
    )
    if actual_strategy != frozenset(STRATEGY_EMAIL_IDS):
        raise ValidationError("Major Strategy Email IDs differ from the canonical bank")

    for email_id, spec in specs.items():
        block = indexed[email_id].text
        for field, localization_id in (
            ("title", spec.title_id),
            ("body", spec.body_id),
            ("sender", spec.sender_id),
        ):
            actual_id, actual_source = _extract_t_property(block, email_id, field)
            if actual_id != localization_id:
                raise ValidationError(
                    f"ModItemEmail {email_id}.{field}: expected id {localization_id}, "
                    f"found {actual_id}"
                )
            expected_source = entries[localization_id].source_en
            if actual_source != expected_source:
                raise ValidationError(
                    f"ModItemEmail {email_id}.{field}: source text differs from canon"
                )
        if spec.repeatable is False and _extract_repeatable(block, email_id) is not False:
            raise ValidationError(f"ModItemEmail {email_id}: repeatable must be false")
        if "<field_note>" in block:
            raise ValidationError(f"ModItemEmail {email_id}: forbidden <field_note>")
        assert_no_raw_newlines_in_lua_strings(block, f"ModItemEmail {email_id}")


def patch_items(
    text: str,
    specs: dict[str, EmailSpec],
    entries: dict[str, LocEntry],
) -> str:
    newline = _detect_newline(text)
    text = patch_strategy_code_item(text)
    indexed = index_email_blocks(text)
    missing_base = [email_id for email_id in BASE_EMAIL_IDS if email_id not in indexed]
    if missing_base:
        raise ValidationError(
            "items.lua is missing required existing R.I.S. Email block(s): "
            + ", ".join(missing_base)
        )
    unknown_ris = sorted(
        email_id
        for email_id in indexed
        if email_id.startswith("RIS_") and email_id not in specs
    )
    if unknown_ris:
        raise ValidationError(
            "items.lua has R.I.S. Email IDs outside the approved set: "
            + ", ".join(unknown_ris)
        )

    replacements: list[tuple[LuaBlock, str]] = []
    for email_id, spec in specs.items():
        block_info = indexed.get(email_id)
        if block_info is None:
            continue
        block = block_info.text
        block = _patch_t_property(
            block, email_id, "body", spec.body_id, entries[spec.body_id].source_en
        )
        block = _patch_t_property(
            block, email_id, "sender", spec.sender_id, entries[spec.sender_id].source_en
        )
        block = _patch_t_property(
            block, email_id, "title", spec.title_id, entries[spec.title_id].source_en
        )
        if spec.repeatable is False:
            block = _set_repeatable_false(block, email_id, newline)
        replacements.append((block_info, block))
    text = _replace_blocks(text, replacements)

    previous_id = "RIS_LegionBrief_33"
    for email_id in STRATEGY_EMAIL_IDS:
        indexed = index_email_blocks(text)
        if email_id not in indexed:
            anchor = indexed.get(previous_id)
            if anchor is None:
                raise ValidationError(
                    f"items.lua: ambiguous strategy insertion; anchor {previous_id!r} missing"
                )
            indent = _block_indent(text, anchor.start)
            block = _new_email_block(indent, newline, specs[email_id], entries)
            text = text[: anchor.end] + newline + block + text[anchor.end :]
        previous_id = email_id

    validate_items_projection(text, specs, entries)
    return text


RESOURCE_CLASS_RE = re.compile(
    r'^[ \t]*[\'"]Class[\'"][ \t]*,[ \t]*"(?P<value>[^"\r\n]+)"[ \t]*,[ \t]*\r?$',
    re.MULTILINE,
)
RESOURCE_ID_RE = re.compile(
    r'^[ \t]*[\'"]Id[\'"][ \t]*,[ \t]*"(?P<value>[^"\r\n]+)"[ \t]*,[ \t]*\r?$',
    re.MULTILINE,
)


def index_email_resources(text: str) -> dict[str, LuaBlock]:
    indexed: dict[str, LuaBlock] = {}
    offsets: dict[str, int] = {}
    for block in find_placeobj_blocks(text, "ModResourcePreset"):
        class_matches = list(RESOURCE_CLASS_RE.finditer(block.text))
        id_matches = list(RESOURCE_ID_RE.finditer(block.text))
        email_class_matches = [
            match for match in class_matches if match.group("value") == "Email"
        ]
        if not email_class_matches:
            continue
        if len(class_matches) != 1 or len(id_matches) != 1:
            raise ValidationError(
                "ambiguous active Email ModResourcePreset: "
                f"Class fields={len(class_matches)}, Id fields={len(id_matches)}"
            )
        resource_id = id_matches[0].group("value")
        if resource_id in indexed:
            raise ValidationError(
                f"duplicate active Email resource {resource_id!r} at offsets "
                f"{offsets[resource_id]} and {block.start}"
            )
        indexed[resource_id] = block
        offsets[resource_id] = block.start
    return indexed


def _new_email_resource(indent: str, newline: str, resource_id: str) -> str:
    property_indent = indent + "\t"
    return newline.join(
        (
            f"{indent}PlaceObj('ModResourcePreset', {{",
            f'{property_indent}\'Class\', "Email",',
            f'{property_indent}\'Id\', "{resource_id}",',
            f'{property_indent}\'ClassDisplayName\', "Email",',
            f"{indent}}}),",
        )
    )


def _metadata_contract_value(text: str, key: str) -> str:
    if key == "last_changes":
        pattern = re.compile(
            r'^(?P<indent>[ \t]*)[\'"]last_changes[\'"][ \t]*,[ \t]*'
            r'"(?P<value>(?:\\.|[^"\\\r\n])*)"[ \t]*,[ \t]*\r?$',
            re.MULTILINE,
        )
    else:
        pattern = re.compile(
            rf"^(?P<indent>[ \t]*)[\'\"]{re.escape(key)}[\'\"][ \t]*,[ \t]*"
            r"(?P<value>\d+)[ \t]*,[ \t]*\r?$",
            re.MULTILINE,
        )
    matches = list(pattern.finditer(text))
    if not matches:
        raise ValidationError(f"metadata.{key}: property is missing")
    minimum_indent = min(len(match.group("indent").expandtabs(4)) for match in matches)
    top_level = [
        match
        for match in matches
        if len(match.group("indent").expandtabs(4)) == minimum_indent
    ]
    if len(top_level) != 1:
        raise ValidationError(
            f"metadata.{key}: expected one least-indented property, found {len(top_level)}"
        )
    match = top_level[0]
    return match.group("value")


def _patch_strategy_code_registration(text: str) -> str:
    """Keep one Strategy observer entry after the Legion AI message producer."""

    newline = _detect_newline(text)
    lines = text.splitlines(keepends=True)

    def positions(value: str) -> list[tuple[int, str]]:
        pattern = re.compile(
            rf"^(?P<indent>[ \t]*)[\"']{re.escape(value)}[\"'][ \t]*,[ \t]*$"
        )
        found: list[tuple[int, str]] = []
        for index, line in enumerate(lines):
            body, _ending = _split_line_ending(line)
            match = pattern.fullmatch(body)
            if match:
                found.append((index, match.group("indent")))
        return found

    anchors = positions(STRATEGY_CODE_ANCHOR)
    targets = positions(STRATEGY_CODE_PATH)
    if len(anchors) != 1:
        raise ValidationError(
            "metadata.lua: expected one Guardpost_Patrols code anchor, "
            f"found {len(anchors)}"
        )
    if len(targets) > 1:
        raise ValidationError(
            "metadata.lua: duplicate System_RIS_Strategy code registrations"
        )

    if targets:
        target_index, _target_indent = targets[0]
        anchor_index, _anchor_indent = anchors[0]
        if target_index > anchor_index:
            return text
        lines.pop(target_index)

    anchors = positions(STRATEGY_CODE_ANCHOR)
    anchor_index, indent = anchors[0]
    ending = _split_line_ending(lines[anchor_index])[1] or newline
    lines.insert(anchor_index + 1, f'{indent}"{STRATEGY_CODE_PATH}",{ending}')
    result = "".join(lines)

    check_lines = result.splitlines(keepends=True)
    old_lines = lines
    lines = check_lines
    try:
        anchors = positions(STRATEGY_CODE_ANCHOR)
        targets = positions(STRATEGY_CODE_PATH)
    finally:
        lines = old_lines
    if len(anchors) != 1 or len(targets) != 1 or targets[0][0] <= anchors[0][0]:
        raise ValidationError(
            "metadata.lua: Strategy observer must load once after Guardpost_Patrols"
        )
    return result


def patch_metadata(text: str) -> str:
    newline = _detect_newline(text)
    protected = {
        key: _metadata_contract_value(text, key)
        for key in ("version_major", "version_minor", "version", "last_changes")
    }
    text = _patch_strategy_code_registration(text)
    indexed = index_email_resources(text)
    if not indexed:
        raise ValidationError("metadata.lua: no Email resource anchor exists")

    previous_id: str | None = None
    for email_id in STRATEGY_EMAIL_IDS:
        indexed = index_email_resources(text)
        if email_id not in indexed:
            if previous_id is not None and previous_id in indexed:
                anchor = indexed[previous_id]
            else:
                anchor = max(indexed.values(), key=lambda block: block.start)
            indent = _block_indent(text, anchor.start)
            block = _new_email_resource(indent, newline, email_id)
            text = text[: anchor.end] + newline + block + text[anchor.end :]
        previous_id = email_id

    indexed = index_email_resources(text)
    missing = [email_id for email_id in STRATEGY_EMAIL_IDS if email_id not in indexed]
    if missing:
        raise ValidationError(
            "metadata.lua: missing Major Strategy Email resources: " + ", ".join(missing)
        )
    strategy_resources = {
        resource_id
        for resource_id in indexed
        if resource_id.startswith("RIS_MajorStrategy_")
    }
    if strategy_resources != set(STRATEGY_EMAIL_IDS):
        raise ValidationError(
            "metadata.lua: Major Strategy resource IDs differ from the canonical bank"
        )
    strategy_code_count = len(
        re.findall(
            rf"^[ \t]*[\"']{re.escape(STRATEGY_CODE_PATH)}[\"'][ \t]*,[ \t]*\r?$",
            text,
            re.MULTILINE,
        )
    )
    if strategy_code_count != 1:
        raise ValidationError(
            "metadata.lua: expected one System_RIS_Strategy code registration"
        )
    for key, expected in protected.items():
        actual = _metadata_contract_value(text, key)
        if actual != expected:
            raise ValidationError(f"metadata.lua: {key} changed during editorial projection")
    return text


def _run_strategy_contract_model_tests() -> None:
    """Deterministic models for the Stage 4 timing and ordering invariants."""

    expected_order = (
        "strategy_network",
        "strategy_roads",
        "strategy_villages",
        "strategy_eyes",
        "strategy_answer",
        "strategy_cargo",
        "strategy_wounded",
        "strategy_red",
        "strategy_sleep",
    )
    if STRATEGY_DESIGN_ORDER != expected_order:
        raise ValidationError(
            "Major Strategy design order differs from the approved nine-material order"
        )

    def choose_next(
        observed: dict[str, int], delivered: set[str]
    ) -> str | None:
        if "strategy_network" not in delivered:
            return "strategy_network" if "strategy_network" in observed else None
        candidates = [
            (observed[material_id], index, material_id)
            for index, material_id in enumerate(expected_order[1:], start=1)
            if material_id in observed and material_id not in delivered
        ]
        return min(candidates)[2] if candidates else None

    observed = {"strategy_roads": 1, "strategy_network": 50}
    if choose_next(observed, set()) != "strategy_network":
        raise ValidationError("strategy model: Network-first invariant failed")

    observed.update(
        {
            "strategy_villages": 20,
            "strategy_eyes": 10,
            "strategy_answer": 10,
        }
    )
    if choose_next(observed, {"strategy_network"}) != "strategy_roads":
        raise ValidationError("strategy model: first-observation FIFO failed")
    observed["strategy_roads"] = 30
    if choose_next(observed, {"strategy_network"}) != "strategy_eyes":
        raise ValidationError("strategy model: canonical tie order failed")

    queue = (
        {"kind": "strategy", "ready_at": 0},
        {"kind": "brief", "ready_at": 0},
    )
    now, next_strategy_at = 10, 24
    picked = next(
        (
            index
            for index, row in enumerate(queue)
            if row["ready_at"] <= now
            and not (
                row["kind"] == "strategy"
                and now < next_strategy_at
            )
        ),
        None,
    )
    if picked != 1:
        raise ValidationError("strategy model: ordinary-mail bypass failed")

    pending = [
        "strategy_strategy_roads",
        "strategy_strategy_network",
        "strategy_strategy_network",
    ]
    desired_key = "strategy_strategy_network"
    normalized_pending = [desired_key] if desired_key in pending else []
    normalized_again = [desired_key] if desired_key in normalized_pending else []
    if len(normalized_pending) != 1 or normalized_again != normalized_pending:
        raise ValidationError("strategy model: more than one pending row")
    delivery_order = [
        "strategy_network",
        "strategy_roads",
        "strategy_network",
    ]
    normalized_order = list(dict.fromkeys(delivery_order))
    if list(dict.fromkeys(normalized_order)) != normalized_order:
        raise ValidationError("strategy model: reload normalization is not idempotent")


def _strategy_mapping_from_lua(text: str, label: str) -> tuple[tuple[str, str], ...]:
    matches = re.findall(
        r'^[ \t]*(strategy_[a-z]+)[ \t]*=[ \t]*'
        r'"(RIS_MajorStrategy_[A-Za-z]+)"[ \t]*,[ \t]*\r?$',
        text,
        re.MULTILINE,
    )
    if len(matches) != 9 or len(set(matches)) != 9:
        raise ValidationError(f"{label}: expected nine unique strategy mappings")
    return tuple(matches)


def _strip_lua_strings_and_comments(text: str) -> str:
    stripped_lines: list[str] = []
    string_re = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')
    for line in text.splitlines():
        code = line.split("--", 1)[0]
        stripped_lines.append(string_re.sub('""', code))
    return "\n".join(stripped_lines)


def validate_strategy_runtime_sources(root: Path) -> None:
    """Static Stage 4 checks; writes nothing and never evaluates campaign code."""

    sources: dict[str, str] = {}
    for relative in (
        Path("Code/System_RIS_Mail.lua"),
        Path(STRATEGY_CODE_PATH),
        Path("Code/System_RIS_Browser.lua"),
    ):
        path = root / relative
        if not path.is_file():
            raise ValidationError(f"required Strategy runtime source is missing: {path}")
        try:
            sources[relative.as_posix()] = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            raise ValidationError(f"cannot read Strategy runtime source {path}: {exc}") from exc

    mail = sources["Code/System_RIS_Mail.lua"]
    strategy = sources[STRATEGY_CODE_PATH]
    browser = sources["Code/System_RIS_Browser.lua"]
    expected_mapping = tuple(STRATEGY_EMAIL_BY_DESIGN.items())
    if _strategy_mapping_from_lua(strategy, STRATEGY_CODE_PATH) != expected_mapping:
        raise ValidationError("System_RIS_Strategy.lua mapping/order differs from canon")
    if _strategy_mapping_from_lua(mail, "Code/System_RIS_Mail.lua") != expected_mapping:
        raise ValidationError("System_RIS_Mail.lua mapping/order differs from canon")

    for marker in (
        "function JAZZ_RIS_RecordStrategyObservation(",
        "function JAZZ_RIS_UpdateStrategyQueue(",
        "function JAZZ_RIS_PollStrategySignals(",
    ):
        if marker not in strategy:
            raise ValidationError(f"{STRATEGY_CODE_PATH}: missing public API {marker}")
    if "function JAZZ_RIS_EnqueueMail(" not in mail:
        raise ValidationError("System_RIS_Mail.lua: shared public enqueue API is missing")
    if "local RIS_STATE_SCHEMA = 3" not in mail:
        raise ValidationError("System_RIS_Mail.lua: gv_JAZZ_RIS schema is not 3")
    if "local RIS_STRATEGY_SPACING_H = 24" not in mail:
        raise ValidationError("System_RIS_Mail.lua: strategy spacing is not 24h")
    for field in (
        "strategy_observed",
        "strategy_delivered",
        "strategy_delivery_order",
        "next_strategy_at",
        "strategy_catchup_done",
        "strategy_major_delivery_baseline",
    ):
        if field not in mail or field not in strategy:
            raise ValidationError(f"Strategy state field is not wired end-to-end: {field}")

    for message in (
        "JAZZ_LegionAISquadManaged",
        "JAZZ_LegionAITaskAssigned",
        "JAZZ_LegionAIMajorResponse",
        "JAZZ_LegionAISquadRefit",
    ):
        if f"function OnMsg.{message}" not in strategy:
            raise ValidationError(f"{STRATEGY_CODE_PATH}: missing {message} observer")
    for lifecycle in (
        "NewHour",
        "SatelliteTick",
        "OpenSatelliteView",
        "LoadGame",
        "ModsReloaded",
        "NewGame",
    ):
        if f"function OnMsg.{lifecycle}" not in strategy:
            raise ValidationError(f"{STRATEGY_CODE_PATH}: missing {lifecycle} poll")

    if "strategy_blocked" not in mail or "lPickDueIndex" not in mail:
        raise ValidationError("System_RIS_Mail.lua: blocked-strategy bypass is missing")
    if 'local key = material_id and ("strategy_" .. material_id)' not in strategy:
        raise ValidationError(f"{STRATEGY_CODE_PATH}: stable strategy queue key is missing")
    if "lPruneStrategyRows" not in strategy:
        raise ValidationError(f"{STRATEGY_CODE_PATH}: one-pending-row guard is missing")

    for marker in (
        'rawget(_G, "JAZZ_RIS_STRATEGY")',
        "st.strategy_delivery_order",
        "st.strategy_delivered[material_id]",
        "lTranslate(card.title)",
        "lTranslate(card.body)",
        "^RIS_MajorStrategy_",
    ):
        if marker not in browser:
            raise ValidationError(
                "System_RIS_Browser.lua: current-language Strategy archive "
                f"marker missing: {marker}"
            )
    if 'not string.match(email.id, "^RIS_MajorStrategy_")' not in browser:
        raise ValidationError(
            "System_RIS_Browser.lua: strategy mail is not excluded from generic archive"
        )

    executable_strategy = _strip_lua_strings_and_comments(strategy)
    if re.search(r"\bgv_JAZZ_LegionAI\s*(?:=|\[|\.)", executable_strategy):
        raise ValidationError(
            f"{STRATEGY_CODE_PATH}: observer directly writes/uses Legion AI global"
        )
    if re.search(
        r"\b(?:root|row|outpost|report)\.[A-Za-z_][A-Za-z0-9_]*[ \t]*=(?!=)",
        executable_strategy,
    ):
        raise ValidationError(f"{STRATEGY_CODE_PATH}: observer mutates an AI snapshot row")
    _run_strategy_contract_model_tests()


def parse_csv_document(path: Path, payload: bytes) -> CsvDocument:
    bom = payload.startswith(codecs.BOM_UTF8)
    try:
        text = payload.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{path}: not valid UTF-8: {exc}") from exc
    newline = _detect_newline(text)
    sep_prefix: str | None = None
    delimiter = ","
    body = text
    first_newline = text.find("\n")
    first_line = text if first_newline < 0 else text[:first_newline]
    if first_line.rstrip("\r").startswith("sep="):
        sep_prefix = first_line.rstrip("\r")
        delimiter = sep_prefix.removeprefix("sep=")
        if len(delimiter) != 1 or delimiter in {'"', "\r", "\n"}:
            raise ValidationError(f"{path}: unsupported CSV separator {delimiter!r}")
        body = "" if first_newline < 0 else text[first_newline + 1 :]
    physical_lines = body.splitlines(keepends=True)
    try:
        reader = csv.reader(
            io.StringIO(body, newline=""), delimiter=delimiter, strict=True
        )
        records_with_raw: list[tuple[list[str], str]] = []
        line_cursor = 0
        for record in reader:
            line_end = reader.line_num
            raw_record = "".join(physical_lines[line_cursor:line_end])
            records_with_raw.append((record, raw_record))
            line_cursor = line_end
    except csv.Error as exc:
        raise ValidationError(f"{path}: malformed CSV: {exc}") from exc
    if not records_with_raw:
        raise ValidationError(f"{path}: CSV has no header")
    header = [
        value.lstrip("\ufeff") if index == 0 else value
        for index, value in enumerate(records_with_raw[0][0])
    ]
    if not header or any(not field for field in header):
        raise ValidationError(f"{path}: empty CSV header field")
    if len(header) != len(set(header)):
        raise ValidationError(f"{path}: duplicate CSV header fields")
    rows: list[list[str]] = []
    raw_rows: list[str] = []
    for record_number, (row, raw_row) in enumerate(records_with_raw[1:], start=2):
        if len(row) > len(header):
            raise ValidationError(
                f"{path}: record {record_number} has {len(row)} fields; header has {len(header)}"
            )
        rows.append(row + [""] * (len(header) - len(row)))
        raw_rows.append(raw_row)
    if line_cursor != len(physical_lines):
        raise ValidationError(f"{path}: CSV raw record boundary mismatch")
    raw_header = records_with_raw[0][1]
    document = CsvDocument(
        header=list(header),
        rows=[list(row) for row in rows],
        sep_prefix=sep_prefix,
        delimiter=delimiter,
        bom=bom,
        newline=newline,
        original_header=list(header),
        original_rows=[list(row) for row in rows],
        raw_header=raw_header,
        raw_rows=raw_rows,
    )
    if document.render() != payload:
        raise ValidationError(f"{path}: CSV parser cannot preserve a no-op byte-for-byte")
    return document


def _require_fields(document: CsvDocument, fields: Sequence[str], label: str) -> None:
    missing = [field for field in fields if field not in document.header]
    if missing:
        raise ValidationError(f"{label}: missing CSV fields: {', '.join(missing)}")


def _target_row_positions(
    document: CsvDocument,
    key_field: str,
    target_keys: set[str] | frozenset[str],
    label: str,
) -> dict[str, int]:
    key_index = document.header.index(key_field)
    positions: dict[str, int] = {}
    for index, row in enumerate(document.rows):
        key = row[key_index].strip()
        if key not in target_keys:
            continue
        if key in positions:
            raise ValidationError(f"{label}: duplicate target key {key!r}")
        positions[key] = index
    return positions


def upsert_runtime_csv(
    document: CsvDocument,
    entries: dict[str, LocEntry],
    *,
    language: str,
    label: str,
) -> CsvDocument:
    _require_fields(document, RUNTIME_FIELDS, label)
    result = document.clone()
    positions = _target_row_positions(result, "ID", frozenset(entries), label)
    field_index = {field: result.header.index(field) for field in RUNTIME_FIELDS}

    for localization_id, entry in entries.items():
        row_index = positions.get(localization_id)
        if row_index is None:
            row = [""] * len(result.header)
            result.rows.append(row)
            row_index = len(result.rows) - 1
            positions[localization_id] = row_index
        row = result.rows[row_index]
        row[field_index["ID"]] = localization_id
        row[field_index["Text"]] = entry.source_en
        row[field_index["Translation"]] = (
            entry.english if language == "english" else entry.russian
        )
        row[field_index["Context"]] = entry.context

    validate_runtime_csv(result, entries, language=language, label=label)
    return result


def validate_runtime_csv(
    document: CsvDocument,
    entries: dict[str, LocEntry],
    *,
    language: str,
    label: str,
) -> None:
    positions = _target_row_positions(document, "ID", frozenset(entries), label)
    field_index = {field: document.header.index(field) for field in RUNTIME_FIELDS}
    if set(positions) != set(entries):
        raise ValidationError(f"{label}: active R.I.S. ID set is incomplete")
    for localization_id, entry in entries.items():
        row = document.rows[positions[localization_id]]
        expected_translation = entry.english if language == "english" else entry.russian
        if row[field_index["Text"]] != entry.source_en:
            raise ValidationError(f"{label}: {localization_id} Text is not the English source")
        if row[field_index["Translation"]] != expected_translation:
            raise ValidationError(f"{label}: {localization_id} Translation differs from canon")
        if row[field_index["Context"]] != entry.context:
            raise ValidationError(f"{label}: {localization_id} Context differs from canon")


def upsert_catalog(
    document: CsvDocument,
    entries: dict[str, LocEntry],
    *,
    label: str,
) -> CsvDocument:
    _require_fields(document, CATALOG_FIELDS, label)
    result = document.clone()
    positions = _target_row_positions(result, "ID", frozenset(entries), label)
    field_index = {field: result.header.index(field) for field in CATALOG_FIELDS}
    updated_fields = (
        "ID",
        "SourceText",
        "Russian",
        "English",
        "Context",
        "Packages",
        "Notes",
    )

    for localization_id, entry in entries.items():
        row_index = positions.get(localization_id)
        is_new = row_index is None
        if is_new:
            row = [""] * len(result.header)
            result.rows.append(row)
            row_index = len(result.rows) - 1
            positions[localization_id] = row_index
            row[field_index["Status"]] = "new-id"
            row[field_index["Locations"]] = entry.locations
        row = result.rows[row_index]
        values = {
            "ID": localization_id,
            "SourceText": entry.source_en,
            "Russian": entry.russian,
            "English": entry.english,
            "Context": entry.context,
            "Packages": "jazz",
            "Notes": MANUAL_NOTE,
        }
        for field in updated_fields:
            row[field_index[field]] = values[field]

    positions = _target_row_positions(result, "ID", frozenset(entries), label)
    if set(positions) != set(entries):
        raise ValidationError(f"{label}: active R.I.S. ID set is incomplete")
    for localization_id, entry in entries.items():
        row = result.rows[positions[localization_id]]
        if row[field_index["SourceText"]] != entry.source_en:
            raise ValidationError(f"{label}: {localization_id} SourceText differs from canon")
        if row[field_index["Russian"]] != entry.russian:
            raise ValidationError(f"{label}: {localization_id} Russian differs from canon")
        if row[field_index["English"]] != entry.english:
            raise ValidationError(f"{label}: {localization_id} English differs from canon")
        if row[field_index["Context"]] != entry.context:
            raise ValidationError(f"{label}: {localization_id} Context differs from canon")
        if row[field_index["Packages"]] != "jazz":
            raise ValidationError(f"{label}: {localization_id} Packages differs from canon")
        if row[field_index["Notes"]] != MANUAL_NOTE:
            raise ValidationError(
                f"{label}: {localization_id} Notes must mark intentional translation"
            )
    return result


def _manual_desired_by_source(
    entries: dict[str, LocEntry],
    value_field: str,
) -> dict[str, tuple[str, str]]:
    desired: dict[str, tuple[str, str]] = {}
    for localization_id, entry in entries.items():
        value = entry.english if value_field == "English" else entry.russian
        previous = desired.get(entry.source_en)
        if previous is not None and previous[1] != value:
            raise ValidationError(
                f"{value_field} manual memory cannot represent SourceText "
                f"{entry.source_en!r}: {previous[1]!r} vs {value!r}"
            )
        if previous is None:
            desired[entry.source_en] = (localization_id, value)
    return desired


def upsert_manual_memory(
    document: CsvDocument,
    entries: dict[str, LocEntry],
    *,
    value_field: str,
    label: str,
) -> CsvDocument:
    required = (
        ENGLISH_MANUAL_FIELDS if value_field == "English" else RUSSIAN_MANUAL_FIELDS
    )
    _require_fields(document, required, label)
    result = document.clone()
    field_index = {field: result.header.index(field) for field in required}
    desired = _manual_desired_by_source(entries, value_field)
    target_sources = set(desired)

    positions: dict[str, int] = {}
    for index, row in enumerate(result.rows):
        source = row[field_index["SourceText"]]
        if source not in target_sources:
            continue
        if source in positions:
            raise ValidationError(f"{label}: duplicate canonical SourceText {source!r}")
        positions[source] = index

    for source, (anchor_id, value) in desired.items():
        row_index = positions.get(source)
        if row_index is None:
            row = [""] * len(result.header)
            result.rows.append(row)
            positions[source] = len(result.rows) - 1
        else:
            row = result.rows[row_index]
        row[field_index["AnchorID"]] = anchor_id
        row[field_index["SourceText"]] = source
        row[field_index[value_field]] = value
        row[field_index["Notes"]] = MANUAL_NOTE

    sequence = 0
    for row in result.rows:
        if not any(row):
            continue
        sequence += 1
        row[field_index["N"]] = str(sequence)

    seen_target_sources: dict[str, list[str]] = {}
    for row in result.rows:
        source = row[field_index["SourceText"]]
        if source not in target_sources:
            continue
        if source in seen_target_sources:
            raise ValidationError(f"{label}: duplicate canonical SourceText {source!r}")
        seen_target_sources[source] = row
    if set(seen_target_sources) != target_sources:
        raise ValidationError(f"{label}: canonical SourceText set is incomplete")
    for source, (anchor_id, expected) in desired.items():
        row = seen_target_sources[source]
        if row[field_index[value_field]] != expected:
            raise ValidationError(f"{label}: translation conflict for SourceText {source!r}")
        if row[field_index["AnchorID"]] != anchor_id:
            raise ValidationError(f"{label}: AnchorID drift for SourceText {source!r}")
        if row[field_index["Notes"]] != MANUAL_NOTE:
            raise ValidationError(
                f"{label}: Notes must mark intentional translation for {source!r}"
            )
    return result


def _decode_lua(path: Path, payload: bytes) -> tuple[str, bool]:
    bom = payload.startswith(codecs.BOM_UTF8)
    try:
        return payload.decode("utf-8-sig"), bom
    except UnicodeDecodeError as exc:
        raise ValidationError(f"{path}: not valid UTF-8: {exc}") from exc


def _encode_lua(text: str, bom: bool) -> bytes:
    payload = text.encode("utf-8")
    return (codecs.BOM_UTF8 + payload) if bom else payload


def build_plan(root: Path = ROOT) -> tuple[list[FilePlan], dict[str, LocEntry]]:
    root = root.resolve()
    run_canonical_audit()
    validate_strategy_runtime_sources(root)
    entries = build_localization_map()
    specs = build_email_specs()

    originals: dict[Path, bytes] = {}
    for relative in TARGET_RELATIVE_PATHS:
        path = root / relative
        if not path.is_file():
            raise ValidationError(f"required target does not exist: {path}")
        try:
            originals[relative] = path.read_bytes()
        except OSError as exc:
            raise ValidationError(f"cannot read {path}: {exc}") from exc

    desired: dict[Path, bytes] = {}

    content_relative = Path("Code/System_RIS_Content.lua")
    _content_text, content_bom = _decode_lua(
        root / content_relative, originals[content_relative]
    )
    desired[content_relative] = _encode_lua(generate_content_lua(entries), content_bom)

    items_relative = Path("items.lua")
    items_text, items_bom = _decode_lua(root / items_relative, originals[items_relative])
    desired[items_relative] = _encode_lua(
        patch_items(items_text, specs, entries), items_bom
    )

    metadata_relative = Path("metadata.lua")
    metadata_text, metadata_bom = _decode_lua(
        root / metadata_relative, originals[metadata_relative]
    )
    desired[metadata_relative] = _encode_lua(patch_metadata(metadata_text), metadata_bom)

    english_relative = Path("English.csv")
    english_doc = parse_csv_document(
        root / english_relative, originals[english_relative]
    )
    desired[english_relative] = upsert_runtime_csv(
        english_doc, entries, language="english", label="English.csv"
    ).render()

    russian_relative = Path("Russian.csv")
    russian_doc = parse_csv_document(
        root / russian_relative, originals[russian_relative]
    )
    desired[russian_relative] = upsert_runtime_csv(
        russian_doc, entries, language="russian", label="Russian.csv"
    ).render()

    catalog_relative = Path("Localization/Strings.csv")
    catalog_doc = parse_csv_document(
        root / catalog_relative, originals[catalog_relative]
    )
    desired[catalog_relative] = upsert_catalog(
        catalog_doc, entries, label="Localization/Strings.csv"
    ).render()

    english_manual_relative = Path("Localization/EnglishManual.csv")
    english_manual_doc = parse_csv_document(
        root / english_manual_relative, originals[english_manual_relative]
    )
    desired[english_manual_relative] = upsert_manual_memory(
        english_manual_doc,
        entries,
        value_field="English",
        label="Localization/EnglishManual.csv",
    ).render()

    russian_manual_relative = Path("Localization/RussianManual.csv")
    russian_manual_doc = parse_csv_document(
        root / russian_manual_relative, originals[russian_manual_relative]
    )
    desired[russian_manual_relative] = upsert_manual_memory(
        russian_manual_doc,
        entries,
        value_field="Russian",
        label="Localization/RussianManual.csv",
    ).render()

    if set(desired) != set(TARGET_RELATIVE_PATHS):
        raise ValidationError("internal target plan is incomplete")
    plans = [
        FilePlan(relative, root / relative, originals[relative], desired[relative])
        for relative in TARGET_RELATIVE_PATHS
    ]
    return plans, entries


def replace_plans_atomically(plans: Sequence[FilePlan]) -> None:
    changed = [plan for plan in plans if plan.changed]
    if not changed:
        return
    for plan in changed:
        try:
            current = plan.path.read_bytes()
        except OSError as exc:
            raise ValidationError(f"cannot re-read {plan.path}: {exc}") from exc
        if current != plan.original:
            raise ValidationError(
                f"target changed after planning; refusing stale write: {plan.path}"
            )

    originals = {plan.path: plan.original for plan in changed}
    temp_paths: dict[Path, Path] = {}
    replaced: list[Path] = []
    try:
        for plan in changed:
            mode = stat.S_IMODE(plan.path.stat().st_mode)
            with tempfile.NamedTemporaryFile(
                mode="wb",
                prefix=f".{plan.path.name}.",
                suffix=".tmp",
                dir=plan.path.parent,
                delete=False,
            ) as handle:
                handle.write(plan.desired)
                handle.flush()
                os.fsync(handle.fileno())
                temp_path = Path(handle.name)
            os.chmod(temp_path, mode)
            temp_paths[plan.path] = temp_path
        for plan in changed:
            os.replace(temp_paths[plan.path], plan.path)
            replaced.append(plan.path)
    except OSError as exc:
        for path in reversed(replaced):
            try:
                path.write_bytes(originals[path])
            except OSError:
                pass
        raise ValidationError(f"cannot update R.I.S. targets atomically: {exc}") from exc
    finally:
        for temp_path in temp_paths.values():
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Synchronize all approved JAZZ-UI-RIS-002 generated editorial data. "
            "Default: dry-run with no writes."
        )
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="write nothing; exit 1 when any target differs",
    )
    mode.add_argument(
        "--apply",
        action="store_true",
        help="write every changed target after all projections validate",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help=argparse.SUPPRESS,
    )
    return parser


def run(args: argparse.Namespace) -> int:
    plans, entries = build_plan(args.root)
    changed = [plan for plan in plans if plan.changed]
    for plan in plans:
        state = "changed" if plan.changed else "unchanged"
        print(
            f"{state:9} {plan.relative_path.as_posix()} "
            f"(current={len(plan.original)}B desired={len(plan.desired)}B)"
        )

    mode = "apply" if args.apply else ("check" if args.check else "dry-run")
    print(
        f"summary: mode={mode} files={len(plans)} changed={len(changed)} "
        f"unchanged={len(plans) - len(changed)} localization_ids={len(entries)} "
        f"emails={len(EXPECTED_RIS_EMAIL_IDS)} strategy={len(STRATEGY_EMAIL_IDS)}"
    )
    if args.apply:
        replace_plans_atomically(plans)
        print(f"applied: {len(changed)} file(s)")
        return 0
    print("no files written")
    if args.check and changed:
        return 1
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except (ValidationError, OSError, UnicodeError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
