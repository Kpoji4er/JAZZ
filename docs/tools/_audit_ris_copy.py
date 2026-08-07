#!/usr/bin/env python3
"""Read-only structural and editorial audit of the canonical R.I.S. copy bank.

The script imports ``_ris_copy_bank.py``, reads the approved Major Strategy
design for exact-text comparison, prints actionable failures, and never writes
files.
"""

from __future__ import annotations

from collections import Counter
import re
from pathlib import Path

import _ris_copy_bank as bank
import _rewrite_ris_legion_briefs as brief_bank


ROOT = Path(__file__).resolve().parents[2]
MAJOR_STRATEGY_DESIGN = ROOT / "docs/design/ris-major-strategy.md"
DOSSIER_REVIEW_DESIGN = ROOT / "docs/design/ris-legion-dossiers.md"
BRIEF_REVIEW_DESIGN = ROOT / "docs/design/ris-legion-tier-briefs.md"
COMPAT_APPLY_WRAPPERS = (
    "_apply_ris_mail_emails.py",
    "_apply_ris_phase_b.py",
    "_fix_ris_brief11_ru_calque.py",
    "_apply_ris_dossier_copy.py",
    "_apply_ris_queue_field_mails.py",
    "_fix_ris_sighting_loc.py",
    "_fix_ris_english_csv_text_keys.py",
)

EXPECTED_COUNTS = {
    "DOSSIERS": 38,
    "DOSSIER_LOC_IDS": 38,
    "QUEST_DOSSIERS": 4,
    "QUEST_DOSSIER_LOC_IDS": 4,
    "WELCOME_FIXES": 3,
    "UI_FIXES": 13,
    "AAR_FIXES": 60,
    "FIELD_MAIL_FIXES": 7,
    "RIS_FIXED_STRINGS": 3,
    "RIS_EXTRA_STRINGS": 8,
    "STRING_FIXES": 76,
    "ALL_SIMPLE_STRINGS": 94,
    "MAJOR_STRATEGY": 9,
}

EXPECTED_BRIEF_KEYS = ("11", "12", "13", "21", "22", "23", "24", "25", "31", "32", "33")

EXPECTED_STRATEGY = {
    "RIS_MajorStrategy_Network": "strategy_network",
    "RIS_MajorStrategy_Roads": "strategy_roads",
    "RIS_MajorStrategy_Villages": "strategy_villages",
    "RIS_MajorStrategy_Recon": "strategy_eyes",
    "RIS_MajorStrategy_Response": "strategy_answer",
    "RIS_MajorStrategy_Cargo": "strategy_cargo",
    "RIS_MajorStrategy_Recovery": "strategy_wounded",
    "RIS_MajorStrategy_Retribution": "strategy_red",
    "RIS_MajorStrategy_Awakening": "strategy_sleep",
}

REQUIRED_PUBLIC_EXPORTS = {
    "DOSSIERS",
    "DOSSIER_LOC_IDS",
    "QUEST_DOSSIERS",
    "QUEST_DOSSIER_LOC_IDS",
    "WELCOME_FIXES",
    "UI_FIXES",
    "AAR_FIXES",
    "FIELD_MAIL_FIXES",
    "RIS_FIXED_STRINGS",
    "RIS_EXTRA_STRINGS",
    "STRING_FIXES",
    "ALL_SIMPLE_STRINGS",
    "MAJOR_STRATEGY",
}

EXPECTED_LIST_IDS = {
    "WELCOME_FIXES": tuple(str(value) for value in range(890000000006922, 890000000006925)),
    "UI_FIXES": tuple(str(value) for value in range(890000000011000, 890000000011013)),
    "AAR_FIXES": tuple(str(value) for value in range(890000000011097, 890000000011157)),
    "FIELD_MAIL_FIXES": tuple(str(value) for value in range(890000000011200, 890000000011207)),
    "RIS_FIXED_STRINGS": (
        "890000000006920",
        "890000000006921",
        "890000000006939",
    ),
    "RIS_EXTRA_STRINGS": tuple(str(value) for value in range(890000000011340, 890000000011348)),
}

EXPECTED_ALL_IDS = (
    set(EXPECTED_LIST_IDS["RIS_FIXED_STRINGS"])
    | set(EXPECTED_LIST_IDS["WELCOME_FIXES"])
    | {str(value) for value in range(890000000011000, 890000000011157)}
    | set(EXPECTED_LIST_IDS["FIELD_MAIL_FIXES"])
    | {str(value) for value in range(890000000011300, 890000000011348)}
)

EXPECTED_RESERVED_ALLOCATED = {
    str(value) for value in range(890000000011322, 890000000011348)
}
EXPECTED_RESERVED_UNALLOCATED = {
    str(value) for value in range(890000000011348, 890000000011350)
}

ALLOWED_PLACEHOLDERS = {
    "count",
    "unit_title",
    "player",
    "enemy",
    "sector",
    "poi",
    "quest",
    "quests",
    "note",
    "pkia",
    "pwia",
    "ekia",
    "ewia",
    "name",
    "time",
}

EXPECTED_PLACEHOLDERS = {
    "890000000011007": ("count",),
    "890000000011134": ("player", "enemy"),
    "890000000011135": ("sector",),
    "890000000011136": ("sector", "poi"),
    "890000000011137": ("quest", "note"),
    "890000000011138": ("quest",),
    "890000000011139": ("quests",),
    "890000000011140": ("quest",),
    "890000000011149": ("pkia", "pwia", "ekia", "ewia"),
    "890000000011150": ("name",),
    "890000000011151": ("name",),
    "890000000011152": ("name",),
    "890000000011153": ("name",),
    "890000000011201": ("unit_title",),
    "890000000011202": ("unit_title",),
    "890000000011203": ("name",),
    "890000000011204": ("name",),
    "890000000011205": ("name",),
    "890000000011206": ("name",),
    "890000000011343": ("sector",),
    "890000000011347": ("sector", "time"),
}

PLACEHOLDER_RE = re.compile(r"<([a-z][a-z0-9_]*)>")
ANGLE_TOKEN_RE = re.compile(r"<([^<>]+)>")

# Match only prose tokens, not substrings such as "opposite".  ``Heat`` is
# case-sensitive so the ordinary weather phrase "in the heat" remains valid.
FORBIDDEN_TOKENS = {
    "archetype": re.compile(r"\barchetypes?\b", re.IGNORECASE),
    "catalog": re.compile(r"\bcatalog(?:s|ue|ues)?\b", re.IGNORECASE),
    "site": re.compile(r"\bsites?\b", re.IGNORECASE),
    "tab": re.compile(r"\btabs?\b", re.IGNORECASE),
    "subscription": re.compile(r"\bsubscriptions?\b", re.IGNORECASE),
    "tier": re.compile(r"\btiers?\b", re.IGNORECASE),
    "role": re.compile(r"\broles?\b", re.IGNORECASE),
    "spawn": re.compile(r"\bspawn(?:s|ed|ing)?\b", re.IGNORECASE),
    "tick": re.compile(r"\bticks?\b", re.IGNORECASE),
    "Heat": re.compile(r"\bHeat\b"),
    "QRF": re.compile(r"\bQRF\b"),
    "REINFORCE": re.compile(r"\bREINFORCE\b"),
    "Global AI": re.compile(r"\bGlobal AI\b", re.IGNORECASE),
    "MapVar": re.compile(r"\bMapVar\b"),
    "UI": re.compile(r"\bUI\b"),
    "runtime": re.compile(r"\bruntime\b", re.IGNORECASE),
    "debug": re.compile(r"\bdebug\b", re.IGNORECASE),
    "tooltip": re.compile(r"\btooltips?\b", re.IGNORECASE),
    "unlock": re.compile(r"\bunlock(?:s|ed|ing)?\b", re.IGNORECASE),
    "interface": re.compile(r"\binterfaces?\b", re.IGNORECASE),
    "button": re.compile(r"\bbuttons?\b", re.IGNORECASE),
    "архетип": re.compile(r"\bархетип\w*\b", re.IGNORECASE),
    "каталог": re.compile(r"\bкаталог\w*\b", re.IGNORECASE),
    "сайт": re.compile(r"\bсайт\w*\b", re.IGNORECASE),
    "вкладка": re.compile(r"\bвкладк\w*\b", re.IGNORECASE),
    "подписка": re.compile(r"\bподписк\w*\b", re.IGNORECASE),
    "тир": re.compile(r"\bтир(?:ы|а|ов|е|у|ом)?\b", re.IGNORECASE),
    "роль": re.compile(r"\b(?:роль|роли|ролей|ролью)\b", re.IGNORECASE),
    "спавн": re.compile(r"\bспавн\w*\b", re.IGNORECASE),
    "интерфейс": re.compile(r"\bинтерфейс\w*\b", re.IGNORECASE),
    "отладка": re.compile(r"\bотлад\w*\b", re.IGNORECASE),
    "тултип": re.compile(r"\bтултип\w*\b", re.IGNORECASE),
    "разблокировка": re.compile(r"\bразблок\w*\b", re.IGNORECASE),
    "кнопка": re.compile(r"\bкноп\w*\b", re.IGNORECASE),
}

FORBIDDEN_UI_INSTRUCTIONS = {
    "read-message instruction": re.compile(
        r"\bread (?:this|the) (?:message|mail)\b", re.IGNORECASE
    ),
    "open-tab instruction": re.compile(
        r"\bopen (?:the )?(?:R\.I\.S\. )?tab\b", re.IGNORECASE
    ),
    "click/hover instruction": re.compile(r"\b(?:click|hover)\b", re.IGNORECASE),
    "прочитайте письмо": re.compile(
        r"\b(?:прочитайте|прочти)\b.{0,40}\bписьм\w*\b", re.IGNORECASE
    ),
    "откройте вкладку": re.compile(
        r"\bоткро\w*\b.{0,40}\bвкладк\w*\b", re.IGNORECASE
    ),
    "наведите курсор": re.compile(
        r"\bнавед\w*\b.{0,40}\bкурсор\w*\b", re.IGNORECASE
    ),
}

# Phrases retired after checking the copy against actual runtime evidence.  They
# either expose nonexistent UI behavior, overstate a single final-state sample,
# assume who attacked, or promise equipment not guaranteed by the loadout bank.
RETIRED_FACTUAL_PHRASES = {
    "fictional red route": re.compile(r"\bmarks? a route in red\b", re.IGNORECASE),
    "fictional red route ru": re.compile(r"\bпомет\w+ маршрут красным\b", re.IGNORECASE),
    "first-contact force count": re.compile(r"\bat first contact\b", re.IGNORECASE),
    "first-contact force count ru": re.compile(
        r"\bна момент первого контакта\b", re.IGNORECASE
    ),
    "unsupported concussion charge": re.compile(
        r"\bconcussion charges?\b", re.IGNORECASE
    ),
    "unsupported concussion charge ru": re.compile(
        r"\bоглушающ\w+ заряд\w*\b", re.IGNORECASE
    ),
    "game-action rocket wording": re.compile(r"\bonly one attack\b", re.IGNORECASE),
    "game-action rocket wording ru": re.compile(r"\bатаковать снова\b", re.IGNORECASE),
    "legion-only generic report": re.compile(
        r"\b(?:local|higher) Legion command\b", re.IGNORECASE
    ),
    "unsupported escaped-area claim": re.compile(
        r"\bescaped the area\b", re.IGNORECASE
    ),
}

# These patterns deliberately target id shapes rather than all capitals.  This
# keeps valid prose such as "R.I.S." and display titles such as "GPMG".
RAW_ID_PATTERNS = {
    "JAZZ/RIS id": re.compile(r"(?<![A-Za-z0-9.])(?:JAZZ|RIS)_[A-Za-z0-9_]+"),
    "strategy id": re.compile(r"(?<![A-Za-z0-9])strategy_[a-z0-9_]+"),
    "save id": re.compile(r"(?<![A-Za-z0-9])gv_JAZZ_RIS(?![A-Za-z0-9])"),
    "raw quest/session/unit/sector id": re.compile(
        r"(?<![A-Za-z0-9])(?:quest|session|unit|sector)_[A-Za-z0-9_]+",
        re.IGNORECASE,
    ),
}

STRATEGY_BLOCK_RE = re.compile(
    r"^### \d+ — .+?\n\n"
    r"\*\*RU — (?P<title_ru>.+?)\*\*\n\n"
    r"(?P<body_ru>.+?\n\n— Полевой отдел R\.I\.S\.)\n\n"
    r"\*\*EN — (?P<title_en>.+?)\*\*\n\n"
    r"(?P<body_en>.+?\n\n— R\.I\.S\. Field Desk)"
    r"(?=\n\n(?:### \d+ —|## Проверка текста))",
    re.MULTILINE | re.DOTALL,
)

CANONICAL_SIGNATURE_EN = "— R.I.S. Field Desk"
CANONICAL_SIGNATURE_RU = "— Полевой отдел R.I.S."
CANONICAL_FULL_NAME_EN = "Recon Intelligence Services"
CANONICAL_FULL_NAME_RU = "Разведывательно-информационная служба R.I.S."

ALTERNATE_SIGNATURES = (
    "— Recon Intelligence Services",
    "— RIS Field Desk",
    "— Полевой стол R.I.S.",
    "— Разведывательно-информационная служба R.I.S.",
)


def audit() -> tuple[list[str], int, int]:
    errors: list[str] = []
    pair_count = 0
    localization_ids: dict[str, str] = {}

    def error(message: str) -> None:
        errors.append(message)

    def register_localization_id(value: object, location: str) -> None:
        if not isinstance(value, str) or not value.isdigit():
            error(f"{location}: localization id must be a decimal string, got {value!r}")
            return
        previous = localization_ids.get(value)
        if previous is not None:
            error(f"{location}: duplicate localization id {value}; first used by {previous}")
            return
        localization_ids[value] = location

    def audit_text(location: str, value: object) -> str | None:
        if not isinstance(value, str):
            error(f"{location}: expected str, got {type(value).__name__}")
            return None
        if not value.strip():
            error(f"{location}: player-facing text is empty")
            return None

        for label, pattern in FORBIDDEN_TOKENS.items():
            match = pattern.search(value)
            if match:
                error(f"{location}: forbidden token {label!r}: {match.group(0)!r}")
        for label, pattern in FORBIDDEN_UI_INSTRUCTIONS.items():
            match = pattern.search(value)
            if match:
                error(f"{location}: forbidden UI instruction {label!r}: {match.group(0)!r}")
        for label, pattern in RETIRED_FACTUAL_PHRASES.items():
            match = pattern.search(value)
            if match:
                error(f"{location}: retired factual phrase {label!r}: {match.group(0)!r}")
        prose_without_placeholders = PLACEHOLDER_RE.sub("", value)
        for label, pattern in RAW_ID_PATTERNS.items():
            match = pattern.search(prose_without_placeholders)
            if match:
                error(f"{location}: raw {label}: {match.group(0)!r}")
        for signature in ALTERNATE_SIGNATURES:
            if signature in value:
                error(f"{location}: non-canonical signature {signature!r}")

        for angle_token in ANGLE_TOKEN_RE.findall(value):
            is_placeholder = re.fullmatch(r"[a-z][a-z0-9_]*", angle_token)
            is_email = re.fullmatch(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                angle_token,
            )
            if not is_placeholder and not is_email:
                error(f"{location}: malformed placeholder <{angle_token}>")
        return value

    def audit_pair(
        location: str,
        en: object,
        ru: object,
        expected_placeholders: tuple[str, ...] = (),
    ) -> None:
        nonlocal pair_count
        pair_count += 1
        en_text = audit_text(f"{location}.en", en)
        ru_text = audit_text(f"{location}.ru", ru)
        if en_text is None or ru_text is None:
            return

        en_placeholders = Counter(PLACEHOLDER_RE.findall(en_text))
        ru_placeholders = Counter(PLACEHOLDER_RE.findall(ru_text))
        if en_placeholders != ru_placeholders:
            error(
                f"{location}: placeholder parity mismatch: "
                f"EN={dict(en_placeholders)}, RU={dict(ru_placeholders)}"
            )
        unknown = (set(en_placeholders) | set(ru_placeholders)) - ALLOWED_PLACEHOLDERS
        if unknown:
            error(f"{location}: unknown placeholder(s): {', '.join(sorted(unknown))}")
        expected_counter = Counter(expected_placeholders)
        if en_placeholders != expected_counter:
            error(
                f"{location}: placeholder contract mismatch: "
                f"expected={dict(expected_counter)}, found={dict(en_placeholders)}"
            )

    def audit_signature(location: str, en: object, ru: object) -> None:
        if isinstance(en, str) and not en.endswith(CANONICAL_SIGNATURE_EN):
            error(f"{location}.en: missing canonical signature")
        if isinstance(ru, str) and not ru.endswith(CANONICAL_SIGNATURE_RU):
            error(f"{location}.ru: missing canonical signature")

    categories = {name: getattr(bank, name, None) for name in EXPECTED_COUNTS}
    for category, expected in EXPECTED_COUNTS.items():
        value = categories[category]
        if value is None:
            error(f"{category}: required category is missing")
            continue
        try:
            actual = len(value)
        except TypeError:
            error(f"{category}: category has no length")
            continue
        if actual != expected:
            error(f"{category}: expected {expected} entries, found {actual}")

    exports = set(getattr(bank, "__all__", ()))
    missing_exports = REQUIRED_PUBLIC_EXPORTS - exports
    if missing_exports:
        error(f"__all__: missing public exports: {', '.join(sorted(missing_exports))}")

    russian_probe: list[list[str]] = []
    english_probe: list[list[str]] = []
    brief_bank.upsert_rows(russian_probe, "1", "English source", "Русский перевод")
    brief_bank.upsert_rows_en_file(english_probe, "1", "English source")
    if russian_probe != [["1", "English source", "Русский перевод", "", brief_bank.TAG]]:
        error("_rewrite_ris_legion_briefs.py: Russian.csv writer orientation is invalid")
    if english_probe != [["1", "English source", "English source", "", brief_bank.TAG]]:
        error("_rewrite_ris_legion_briefs.py: English.csv writer orientation is invalid")

    fix_parts = tuple(
        categories[name] for name in ("WELCOME_FIXES", "UI_FIXES", "AAR_FIXES")
    )
    if all(isinstance(part, list) for part in fix_parts):
        expected_string_fixes = fix_parts[0] + fix_parts[1] + fix_parts[2]
        if categories["STRING_FIXES"] != expected_string_fixes:
            error("STRING_FIXES: must equal WELCOME_FIXES + UI_FIXES + AAR_FIXES")

    all_simple_parts = (
        categories["RIS_FIXED_STRINGS"],
        categories["STRING_FIXES"],
        categories["FIELD_MAIL_FIXES"],
        categories["RIS_EXTRA_STRINGS"],
    )
    if all(isinstance(part, list) for part in all_simple_parts):
        expected_all_simple = (
            all_simple_parts[0]
            + all_simple_parts[1]
            + all_simple_parts[2]
            + all_simple_parts[3]
        )
        if categories["ALL_SIMPLE_STRINGS"] != expected_all_simple:
            error(
                "ALL_SIMPLE_STRINGS: must equal RIS_FIXED_STRINGS + STRING_FIXES + "
                "FIELD_MAIL_FIXES + RIS_EXTRA_STRINGS"
            )

    dossier_specs = (
        ("DOSSIERS", "DOSSIER_LOC_IDS", 890000000011013),
        ("QUEST_DOSSIERS", "QUEST_DOSSIER_LOC_IDS", 890000000011089),
    )
    for category_name, id_category_name, first_id in dossier_specs:
        category = categories[category_name]
        id_category = categories[id_category_name]
        if not isinstance(category, dict):
            error(f"{category_name}: expected dict, got {type(category).__name__}")
            continue
        if not isinstance(id_category, dict):
            error(
                f"{id_category_name}: expected dict, got "
                f"{type(id_category).__name__}"
            )
            continue
        if tuple(id_category) != tuple(category):
            error(f"{id_category_name}: keys/order must match {category_name}")

        for index, (key, entry) in enumerate(category.items()):
            location = f"{category_name}[{key!r}]"
            if not isinstance(entry, dict):
                error(f"{location}: expected dict, got {type(entry).__name__}")
                continue
            required_fields = {"title_en", "title_ru", "body_en", "body_ru"}
            missing = required_fields - set(entry)
            if missing:
                error(f"{location}: missing fields: {', '.join(sorted(missing))}")
                continue
            audit_pair(f"{location}.title", entry["title_en"], entry["title_ru"])
            audit_pair(f"{location}.body", entry["body_en"], entry["body_ru"])

            loc_entry = id_category.get(key)
            if not isinstance(loc_entry, dict):
                error(f"{id_category_name}[{key!r}]: missing or not a dict")
                continue
            expected_title_id = str(first_id + index * 2)
            expected_body_id = str(first_id + index * 2 + 1)
            if loc_entry.get("title_id") != expected_title_id:
                error(
                    f"{id_category_name}[{key!r}].title_id: expected "
                    f"{expected_title_id}, found {loc_entry.get('title_id')!r}"
                )
            if loc_entry.get("body_id") != expected_body_id:
                error(
                    f"{id_category_name}[{key!r}].body_id: expected "
                    f"{expected_body_id}, found {loc_entry.get('body_id')!r}"
                )
            register_localization_id(
                loc_entry.get("title_id"), f"{id_category_name}[{key!r}].title_id"
            )
            register_localization_id(
                loc_entry.get("body_id"), f"{id_category_name}[{key!r}].body_id"
            )

    simple_by_id: dict[str, tuple[str, str, str]] = {}
    simple_category_names = (
        "WELCOME_FIXES",
        "UI_FIXES",
        "AAR_FIXES",
        "FIELD_MAIL_FIXES",
        "RIS_FIXED_STRINGS",
        "RIS_EXTRA_STRINGS",
    )
    for category_name in simple_category_names:
        category = categories[category_name]
        if not isinstance(category, list):
            error(f"{category_name}: expected list, got {type(category).__name__}")
            continue
        actual_ids = tuple(
            entry[0]
            for entry in category
            if isinstance(entry, tuple) and len(entry) == 3
        )
        if actual_ids != EXPECTED_LIST_IDS[category_name]:
            error(
                f"{category_name}: localization id coverage/order mismatch: "
                f"expected {EXPECTED_LIST_IDS[category_name]!r}, found {actual_ids!r}"
            )
        for index, entry in enumerate(category):
            location = f"{category_name}[{index}]"
            if not isinstance(entry, tuple) or len(entry) != 3:
                error(f"{location}: expected (localization_id, en, ru) tuple")
                continue
            localization_id, en, ru = entry
            register_localization_id(localization_id, location)
            if isinstance(localization_id, str):
                simple_by_id[localization_id] = (category_name, en, ru)
            audit_pair(
                f"{category_name}[{localization_id}]",
                en,
                ru,
                EXPECTED_PLACEHOLDERS.get(localization_id, ()),
            )

    signed_simple_ids = {
        "890000000006923",
        "890000000011202",
        "890000000011204",
        "890000000011206",
    }
    for localization_id in signed_simple_ids:
        category_name, en, ru = simple_by_id.get(
            localization_id, ("missing", None, None)
        )
        audit_signature(f"{category_name}[{localization_id}]", en, ru)

    canonical_exact = {
        "890000000011000": (CANONICAL_FULL_NAME_EN, CANONICAL_FULL_NAME_RU),
        "890000000011200": (
            "R.I.S. <desk@ris-intel.net>",
            "R.I.S. <desk@ris-intel.net>",
        ),
        "890000000011340": ("The Major's Strategy", "Стратегия Майора"),
    }
    for localization_id, expected_pair in canonical_exact.items():
        _category, en, ru = simple_by_id.get(
            localization_id, ("missing", None, None)
        )
        if (en, ru) != expected_pair:
            error(
                f"{localization_id}: canonical text mismatch: "
                f"expected={expected_pair!r}, found={(en, ru)!r}"
            )

    briefs = getattr(brief_bank, "BRIEFS", None)
    if not isinstance(briefs, dict):
        error(f"SUPPLY_BRIEFS: expected dict, got {type(briefs).__name__}")
    else:
        actual_brief_keys = tuple(briefs)
        if actual_brief_keys != EXPECTED_BRIEF_KEYS:
            error(
                "SUPPLY_BRIEFS: keys/order mismatch: "
                f"expected {EXPECTED_BRIEF_KEYS!r}, found {actual_brief_keys!r}"
            )
        if len(briefs) != len(EXPECTED_BRIEF_KEYS):
            error(
                f"SUPPLY_BRIEFS: expected {len(EXPECTED_BRIEF_KEYS)} entries, "
                f"found {len(briefs)}"
            )
        for index, brief_key in enumerate(EXPECTED_BRIEF_KEYS):
            location = f"SUPPLY_BRIEFS[{brief_key!r}]"
            entry = briefs.get(brief_key)
            if not isinstance(entry, dict):
                error(f"{location}: missing or not a dict")
                continue
            required_fields = {
                "title_id",
                "body_id",
                "title_en",
                "title_ru",
                "body_en",
                "body_ru",
            }
            missing = required_fields - set(entry)
            if missing:
                error(f"{location}: missing fields: {', '.join(sorted(missing))}")
                continue
            expected_title_id = str(890000000011300 + index * 2)
            expected_body_id = str(890000000011301 + index * 2)
            if entry["title_id"] != expected_title_id:
                error(
                    f"{location}.title_id: expected {expected_title_id}, "
                    f"found {entry['title_id']!r}"
                )
            if entry["body_id"] != expected_body_id:
                error(
                    f"{location}.body_id: expected {expected_body_id}, "
                    f"found {entry['body_id']!r}"
                )
            register_localization_id(entry["title_id"], f"{location}.title_id")
            register_localization_id(entry["body_id"], f"{location}.body_id")
            audit_pair(f"{location}.title", entry["title_en"], entry["title_ru"])
            audit_pair(f"{location}.body", entry["body_en"], entry["body_ru"])
            audit_signature(f"{location}.body", entry["body_en"], entry["body_ru"])

    strategy = categories["MAJOR_STRATEGY"]
    if not isinstance(strategy, dict):
        error(f"MAJOR_STRATEGY: expected dict, got {type(strategy).__name__}")
    else:
        actual_keys = tuple(strategy)
        expected_keys = tuple(EXPECTED_STRATEGY)
        if actual_keys != expected_keys:
            error(
                "MAJOR_STRATEGY: keys/order mismatch: "
                f"expected {expected_keys!r}, found {actual_keys!r}"
            )

        for index, (email_id, design_id) in enumerate(EXPECTED_STRATEGY.items()):
            location = f"MAJOR_STRATEGY[{email_id!r}]"
            entry = strategy.get(email_id)
            if not isinstance(entry, dict):
                error(f"{location}: missing or not a dict")
                continue
            required_fields = {
                "design_id",
                "title_id",
                "body_id",
                "title_en",
                "title_ru",
                "body_en",
                "body_ru",
            }
            missing = required_fields - set(entry)
            if missing:
                error(f"{location}: missing fields: {', '.join(sorted(missing))}")
                continue
            if entry["design_id"] != design_id:
                error(
                    f"{location}.design_id: expected {design_id!r}, "
                    f"found {entry['design_id']!r}"
                )
            expected_title_id = str(890000000011322 + index * 2)
            expected_body_id = str(890000000011323 + index * 2)
            if entry["title_id"] != expected_title_id:
                error(
                    f"{location}.title_id: expected {expected_title_id}, "
                    f"found {entry['title_id']!r}"
                )
            if entry["body_id"] != expected_body_id:
                error(
                    f"{location}.body_id: expected {expected_body_id}, "
                    f"found {entry['body_id']!r}"
                )
            audit_pair(f"{location}.title", entry["title_en"], entry["title_ru"])
            audit_pair(f"{location}.body", entry["body_en"], entry["body_ru"])
            audit_signature(f"{location}.body", entry["body_en"], entry["body_ru"])
            register_localization_id(entry["title_id"], f"{location}.title_id")
            register_localization_id(entry["body_id"], f"{location}.body_id")

    if not MAJOR_STRATEGY_DESIGN.is_file():
        error(f"Major Strategy design is missing: {MAJOR_STRATEGY_DESIGN}")
    else:
        design_text = MAJOR_STRATEGY_DESIGN.read_text(encoding="utf-8")
        approved_blocks = list(STRATEGY_BLOCK_RE.finditer(design_text))
        if len(approved_blocks) != len(EXPECTED_STRATEGY):
            error(
                "ris-major-strategy.md: expected 9 canonical text blocks, "
                f"found {len(approved_blocks)}"
            )
        elif isinstance(strategy, dict):
            for email_id, match in zip(EXPECTED_STRATEGY, approved_blocks, strict=True):
                entry = strategy.get(email_id, {})
                for field_name in ("title_en", "title_ru", "body_en", "body_ru"):
                    expected_text = match.group(field_name)
                    if entry.get(field_name) != expected_text:
                        error(
                            f"MAJOR_STRATEGY[{email_id!r}].{field_name}: "
                            "does not exactly match ris-major-strategy.md"
                        )

    actual_ids = set(localization_ids)
    missing_ids = EXPECTED_ALL_IDS - actual_ids
    unexpected_ids = actual_ids - EXPECTED_ALL_IDS
    if missing_ids:
        error(
            "localization ids: missing expected ids: "
            + ", ".join(sorted(missing_ids, key=int))
        )
    if unexpected_ids:
        error(
            "localization ids: unexpected ids: "
            + ", ".join(sorted(unexpected_ids, key=int))
        )

    allocated_reserved = {
        localization_id
        for localization_id in actual_ids
        if 890000000011322 <= int(localization_id) <= 890000000011349
    }
    if allocated_reserved != EXPECTED_RESERVED_ALLOCATED:
        error(
            "reserved strategy range: allocated ids mismatch: "
            f"expected={sorted(EXPECTED_RESERVED_ALLOCATED, key=int)!r}, "
            f"found={sorted(allocated_reserved, key=int)!r}"
        )
    accidentally_allocated = actual_ids & EXPECTED_RESERVED_UNALLOCATED
    if accidentally_allocated:
        error(
            "reserved strategy range: ids 11348…11349 must remain unallocated: "
            + ", ".join(sorted(accidentally_allocated, key=int))
        )

    if pair_count != len(EXPECTED_ALL_IDS):
        error(
            f"bilingual pair coverage: expected {len(EXPECTED_ALL_IDS)}, "
            f"validated {pair_count}"
        )

    if not DOSSIER_REVIEW_DESIGN.is_file():
        error(f"Dossier review design is missing: {DOSSIER_REVIEW_DESIGN}")
    else:
        dossier_review_text = DOSSIER_REVIEW_DESIGN.read_text(encoding="utf-8")
        reviewed_dossiers = set(
            re.findall(
                r"^\| `(JAZZ_Legion_[^`]+)` \|.*\| PASS \| PASS \|$",
                dossier_review_text,
                re.MULTILINE,
            )
        )
        expected_dossiers = set(bank.DOSSIERS)
        if reviewed_dossiers != expected_dossiers:
            error(
                "ris-legion-dossiers.md: reviewed unit set mismatch: "
                f"missing={sorted(expected_dossiers - reviewed_dossiers)!r}, "
                f"unexpected={sorted(reviewed_dossiers - expected_dossiers)!r}"
            )
        reviewed_quests = set(
            re.findall(
                r"^\| `(Pierre|Bastien|TheMajor|Legion)` \|.*\| PASS \| PASS \|$",
                dossier_review_text,
                re.MULTILINE,
            )
        )
        expected_quests = set(bank.QUEST_DOSSIERS)
        if reviewed_quests != expected_quests:
            error(
                "ris-legion-dossiers.md: reviewed quest set mismatch: "
                f"missing={sorted(expected_quests - reviewed_quests)!r}, "
                f"unexpected={sorted(reviewed_quests - expected_quests)!r}"
            )

    if not BRIEF_REVIEW_DESIGN.is_file():
        error(f"Supply brief review design is missing: {BRIEF_REVIEW_DESIGN}")
    else:
        brief_review_text = BRIEF_REVIEW_DESIGN.read_text(encoding="utf-8")
        reviewed_briefs = tuple(
            re.findall(
                r"^\| (11|12|13|21|22|23|24|25|31|32|33) \|.*"
                r"\| PASS \| PASS \|$",
                brief_review_text,
                re.MULTILINE,
            )
        )
        if reviewed_briefs != EXPECTED_BRIEF_KEYS:
            error(
                "ris-legion-tier-briefs.md: reviewed brief order mismatch: "
                f"expected={EXPECTED_BRIEF_KEYS!r}, found={reviewed_briefs!r}"
            )

    tools_dir = ROOT / "docs/tools"
    for filename in COMPAT_APPLY_WRAPPERS:
        wrapper = tools_dir / filename
        if not wrapper.is_file():
            error(f"{filename}: compatibility wrapper is missing")
            continue
        source = wrapper.read_text(encoding="utf-8-sig")
        if "from _apply_ris_editorial import main" not in source:
            error(f"{filename}: does not delegate to _apply_ris_editorial.py")
        if "write_text(" in source or "write_bytes(" in source or "os.replace(" in source:
            error(f"{filename}: compatibility wrapper still contains a write path")

    brief_source = (tools_dir / "_rewrite_ris_legion_briefs.py").read_text(
        encoding="utf-8-sig"
    )
    if "from _apply_ris_editorial import main as editorial_main" not in brief_source:
        error("_rewrite_ris_legion_briefs.py: CLI does not delegate to the unified apply")

    return errors, pair_count, len(localization_ids)


def main() -> int:
    errors, pair_count, localization_id_count = audit()
    if errors:
        print(f"R.I.S. copy audit: FAIL ({len(errors)} error(s))")
        for message in errors:
            print(f"- {message}")
        return 1

    print("R.I.S. copy audit: OK")
    print(
        "editorial categories: "
        f"welcome={len(bank.WELCOME_FIXES)}, "
        f"ui={len(bank.UI_FIXES)}, "
        f"aar={len(bank.AAR_FIXES)}, "
        f"field_mail={len(bank.FIELD_MAIL_FIXES)}, "
        f"fixed_identity={len(bank.RIS_FIXED_STRINGS)}, "
        f"unit_dossiers={len(bank.DOSSIERS)}, "
        f"quest_dossiers={len(bank.QUEST_DOSSIERS)}, "
        f"supply_briefs={len(brief_bank.BRIEFS)}, "
        f"strategy={len(bank.MAJOR_STRATEGY)}, "
        f"reserved_extras={len(bank.RIS_EXTRA_STRINGS)}"
    )
    print(
        f"validated bilingual pairs={pair_count}, "
        f"unique localization ids={localization_id_count}"
    )
    print(
        "reserved ids allocated=890000000011322-890000000011347; "
        "unallocated=890000000011348-890000000011349"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
