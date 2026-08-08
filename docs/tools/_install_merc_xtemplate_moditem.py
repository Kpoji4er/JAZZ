#!/usr/bin/env python3
"""Install PDAMERCBrowser XTemplate + register MERC Code/Emails (JAZZ-UI-MERC-001)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Code" / "System_MERC_Browser_Template.lua"
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
BEGIN = "-- JAZZ-UI-MERC-001-XTEMPLATE-BEGIN"
END = "-- JAZZ-UI-MERC-001-XTEMPLATE-END"

CODE_FILES = [
    "Code/System_MERC_Filters.lua",
    "Code/System_MERC_Account.lua",
    "Code/System_MERC_Browser.lua",
    "Code/System_MERC_Mail.lua",
    "Code/System_MERC_World.lua",
]

EMAIL_BLOCK = r'''
		-- JAZZ-UI-MERC-001-EMAIL-BEGIN
		PlaceObj('ModItemEmail', {
			body = T(890000000007201, --[[ModItemEmail MERC_Welcome body]] "Commander!\n\nGreat news — M.E.R.C. is OPEN FOR BUSINESS again. Fresh site, same low daily rates, and you don't pay up front. Hire now, settle the account when you can. (I'll nudge you. Friendly-like.)\n\nOne snag. My partner Biff was supposed to keep the books. He hasn't checked in. If you bump into him out there, tell him Speck needs him back at the desk. Preferably still breathing.\n\nOpen M.E.R.C. in your PDA browser and pick a contractor. We're not A.I.M. — we're cheaper.\n\nYour friend in the hiring business,\nSpeck T. Kline\nM.E.R.C. — More Economic Recruiting Center"),
			delayAfterCombat = false,
			group = "Default",
			id = "MERC_Welcome",
			label = "Important",
			sender = T(890000000007200, --[[ModItemEmail MERC_Welcome sender]] "Speck <speck@merc.com>"),
			title = T(890000000007202, --[[ModItemEmail MERC_Welcome title]] "M.E.R.C. is OPEN — and where's Biff?"),
		}),
		PlaceObj('ModItemEmail', {
			body = T(890000000007204, --[[ModItemEmail MERC_AccountReminder body]] "Commander!\n\nHate to bother a valued customer, but your M.E.R.C. account still shows $<balance> outstanding.\n\nDaily rates, remember? Pay Account on the site before my people start writing resignation notes in muddy boots.\n\nSpeck"),
			delayAfterCombat = false,
			group = "Default",
			id = "MERC_AccountReminder",
			label = "Important",
			repeatable = true,
			sender = T(890000000007203, --[[ModItemEmail MERC_AccountReminder sender]] "Speck <accounts@merc.com>"),
			title = T(890000000007205, --[[ModItemEmail MERC_AccountReminder title]] "M.E.R.C. — please settle up"),
		}),
		PlaceObj('ModItemEmail', {
			body = T(890000000007207, --[[ModItemEmail MERC_QuitWarning body]] "Commander!\n\nI warned you. $<balance> still unpaid. My contractors walked.\n\nWant them back? Clear the ledger first — if any of them still answer the phone.\n\nSpeck"),
			delayAfterCombat = false,
			group = "Default",
			id = "MERC_QuitWarning",
			label = "Important",
			repeatable = true,
			sender = T(890000000007206, --[[ModItemEmail MERC_QuitWarning sender]] "Speck <accounts@merc.com>"),
			title = T(890000000007208, --[[ModItemEmail MERC_QuitWarning title]] "M.E.R.C. — they're walking"),
		}),
		-- JAZZ-UI-MERC-001-EMAIL-END
'''


def build_moditem_block() -> str:
    text = SRC.read_text(encoding="utf-8")
    lines = text.splitlines()
    while lines and (lines[0].startswith("--") or not lines[0].strip()):
        lines.pop(0)
    body = "\n".join(lines)
    if not body.startswith("PlaceObj('XTemplate'"):
        raise RuntimeError(f"unexpected template start: {body[:80]!r}")
    body = body.replace("PlaceObj('XTemplate'", "PlaceObj('ModItemXTemplate'", 1)
    body = body.replace("XTemplate PDAMERCBrowser", "ModItemXTemplate PDAMERCBrowser")
    indented = "\n".join(("\t\t" + ln if ln.strip() else ln) for ln in body.splitlines())
    return f"\t\t{BEGIN}\n{indented.rstrip()},\n\t\t{END}\n"


def _find_moditem_xtemplate_span(text: str, template_id: str) -> tuple[int, int] | None:
    needle = f'id = "{template_id}"'
    id_idx = text.find(needle)
    if id_idx < 0:
        return None
    start = text.rfind("PlaceObj('ModItemXTemplate'", 0, id_idx)
    if start < 0:
        return None
    open_paren = text.find("(", start)
    depth = 0
    i = open_paren
    in_str = False
    str_ch = ""
    escape = False
    while i < len(text):
        ch = text[i]
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == str_ch:
                in_str = False
        else:
            if ch in ("'", '"'):
                in_str = True
                str_ch = ch
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    if end < len(text) and text[end] == ",":
                        end += 1
                    while end < len(text) and text[end] in " \t\r":
                        end += 1
                    if end < len(text) and text[end] == "\n":
                        end += 1
                    return start, end
        i += 1
    return None


def patch_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    block = build_moditem_block()
    if BEGIN in text:
        pattern = re.compile(
            r"[ \t]*" + re.escape(BEGIN) + r".*?" + r"[ \t]*" + re.escape(END) + r"[ \t]*\n?",
            re.S,
        )
        text, n = pattern.subn(lambda _m: block, text, count=1)
        if n != 1:
            raise RuntimeError(f"MERC XTemplate replace count={n}")
        print("replaced MERC XTemplate block")
    else:
        span = _find_moditem_xtemplate_span(text, "PDAMERCBrowser")
        if span is not None:
            start, end = span
            text = text[:start] + block + text[end:]
            print("replaced markerless PDAMERCBrowser")
        else:
            # After AME block or before Constants
            ame_end = text.find("-- JAZZ-UNITS-005-AME-XTEMPLATE-END")
            if ame_end >= 0:
                insert_at = text.find("\n", ame_end) + 1
                text = text[:insert_at] + block + text[insert_at:]
                print("inserted MERC XTemplate after AME")
            else:
                needle = "\tPlaceObj('ModItemFolder', {\n\t\t'name', \"Constants\","
                idx = text.find(needle)
                if idx < 0:
                    raise SystemExit("Constants folder anchor not found")
                text = text[:idx] + block + text[idx:]
                print("inserted MERC XTemplate before Constants")

    if "id = \"MERC_Welcome\"" not in text:
        # insert after AME_ListingUpdate block (before RIS_Welcome)
        ris = text.find("id = \"RIS_Welcome\"")
        if ris < 0:
            raise SystemExit("RIS_Welcome anchor missing")
        start = text.rfind("PlaceObj('ModItemEmail'", 0, ris)
        text = text[:start] + EMAIL_BLOCK + text[start:]
        print("inserted MERC emails")
    else:
        # refresh email bodies if markers present
        if "JAZZ-UI-MERC-001-EMAIL-BEGIN" in text:
            pattern = re.compile(
                r"[ \t]*-- JAZZ-UI-MERC-001-EMAIL-BEGIN.*?-- JAZZ-UI-MERC-001-EMAIL-END\n?",
                re.S,
            )
            text, n = pattern.subn(lambda _m: EMAIL_BLOCK.lstrip("\n"), text, count=1)
            print(f"replaced MERC email block n={n}")
        else:
            print("MERC emails already present (no markers)")

    ITEMS.write_text(text, encoding="utf-8")


def patch_metadata() -> None:
    text = META.read_text(encoding="utf-8")
    # Ensure code entries after AME_Mail
    for code in CODE_FILES:
        entry = f'\t\t"{code}",\n'
        if f'"{code}"' not in text:
            anchor = '\t\t"Code/System_AME_Mail.lua",\n'
            if anchor not in text:
                raise RuntimeError("AME_Mail code anchor missing")
            text = text.replace(anchor, anchor + entry, 1)
            print("added code", code)
        else:
            print("code present", code)
    # Never load template as Code
    text = text.replace('\n\t\t"Code/System_MERC_Browser_Template.lua",', "")
    text = text.replace('\t\t"Code/System_MERC_Browser_Template.lua",\n', "")
    res = (
        "\t\tPlaceObj('ModResourcePreset', {\n"
        '\t\t\t\'Class\', "XTemplate",\n'
        '\t\t\t\'Id\', "PDAMERCBrowser",\n'
        '\t\t\t\'ClassDisplayName\', "UI Template (XTemplate)",\n'
        "\t\t}),\n"
    )
    if "'Id', \"PDAMERCBrowser\"" not in text:
        anchor = "'Id', \"PDAAIMEBrowser\","
        aidx = text.find(anchor)
        if aidx < 0:
            anchor = "'Id', \"PDAAIMBrowser\","
            aidx = text.find(anchor)
        if aidx < 0:
            raise RuntimeError("XTemplate resource anchor missing")
        end = text.find("}),", aidx) + 3
        text = text[:end] + "\n" + res + text[end:]
        print("added ModResourcePreset PDAMERCBrowser")
    else:
        print("ModResourcePreset PDAMERCBrowser present")
    META.write_text(text, encoding="utf-8")


def main() -> int:
    patch_items()
    patch_metadata()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
