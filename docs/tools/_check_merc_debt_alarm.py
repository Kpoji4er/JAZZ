# -*- coding: utf-8 -*-
"""Static: JAZZ-UI-MERC-002 MERC debt chip + 7/9/10 popups."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACCOUNT = ROOT / "Code" / "System_MERC_Account.lua"
BROWSER = ROOT / "Code" / "System_MERC_Browser.lua"
LOC_IDS = [f"8900000000099{n}" for n in range(44, 58)]


def main() -> int:
    account = ACCOUNT.read_text(encoding="utf-8")
    browser = BROWSER.read_text(encoding="utf-8")
    failed: list[str] = []

    checks = [
        (ACCOUNT, account, 'MERC_REMINDER_DAYS = 7', "reminder 7d"),
        (ACCOUNT, account, "MERC_GRACE_DAYS = 3", "grace 3d"),
        (ACCOUNT, account, "MERC_EVE_DAYS = 2", "eve +2d"),
        (ACCOUNT, account, "eve_popup_sent", "eve flag"),
        (ACCOUNT, account, "reminder_popup_sent", "reminder popup flag"),
        (ACCOUNT, account, "lClearDebtAlarm", "clear alarm on pay"),
        (ACCOUNT, account, 'Id = "idJazzMERCDebt"', "chip id"),
        (ACCOUNT, account, "WaitPopupChoice", "ZuluChoice popup"),
        (ACCOUNT, account, 'JAZZ_MERC_ShowDebtPopup("reminder")', "day-7 popup"),
        (ACCOUNT, account, 'JAZZ_MERC_ShowDebtPopup("eve")', "day-9 popup"),
        (ACCOUNT, account, "lLogQuitCombatLog", "quit CombatLog"),
        (ACCOUNT, account, "890000000009952", "quit CombatLog loc"),
        (ACCOUNT, account, "lInstallMoneyOpenWrap", "PDAMoneyText wrap"),
        (ACCOUNT, account, "g_JAZZ_MERC_MoneyOpenFn", "money wrap flag"),
        (ACCOUNT, account, "g_Combat", "skip popup in combat"),
        (BROWSER, browser, "function JAZZ_MERC_OpenSite", "open site"),
        (BROWSER, browser, 'browser_page = "merc"', "merc browser page"),
        (BROWSER, browser, 'SetMode("merc")', "force merc submode"),
        (ACCOUNT, account, 'AddTimelineEvent', "timeline add"),
        (ACCOUNT, account, 'RemoveTimelineEvent', "timeline remove"),
        (ACCOUNT, account, '"jazz-merc-reminder"', "reminder event id"),
        (ACCOUNT, account, '"jazz-merc-quit"', "quit event id"),
        (ACCOUNT, account, '"jazz_merc_debt"', "timeline typ"),
        (ACCOUNT, account, "JAZZ_MERC_EnsureTimelineEventDef", "timeline def"),
        (ACCOUNT, account, "SatelliteTimelineEvents", "timeline map"),
    ]
    for _path, text, needle, label in checks:
        if needle not in text:
            failed.append(label)

    if not re.search(r"day - clock >= MERC_EVE_DAYS", account):
        failed.append("eve clock vs MERC_EVE_DAYS")
    if not re.search(r"lClearDebtAlarm\(account\)", account):
        failed.append("clear alarm calls")

    ru = (ROOT / "Russian.csv").read_text(encoding="utf-8")
    en = (ROOT / "English.csv").read_text(encoding="utf-8")
    for eid in LOC_IDS:
        if eid not in ru:
            failed.append(f"Russian.csv {eid}")
        if eid not in en:
            failed.append(f"English.csv {eid}")

    if failed:
        print("FAIL")
        for item in failed:
            print(" -", item)
        return 1
    print("OK", ACCOUNT.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
