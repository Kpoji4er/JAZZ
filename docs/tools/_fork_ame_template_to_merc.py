#!/usr/bin/env python3
"""Fork System_AME_Browser_Template.lua → System_MERC_Browser_Template.lua (JAZZ-UI-MERC-001)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Code" / "System_AME_Browser_Template.lua"
DST = ROOT / "Code" / "System_MERC_Browser_Template.lua"


def main() -> None:
    t = SRC.read_text(encoding="utf-8")
    t = t.replace(
        "Canonical shipped template is ModItemXTemplate in items.lua (id=PDAAIMEBrowser).",
        "Canonical shipped template is ModItemXTemplate in items.lua (id=PDAMERCBrowser).",
    )
    t = t.replace(
        "re-run docs/tools/_install_ame_xtemplate_moditem.py",
        "re-run docs/tools/_install_merc_xtemplate_moditem.py",
    )
    reps = [
        ("PDAAIMEBrowser", "PDAMERCBrowser"),
        ("GetAMEScreenFilters", "GetMERCScreenFilters"),
        ("CurrentAMEFilter", "CurrentMERCFilter"),
        ("GetFilteredAMEMercs", "GetFilteredMERCMercs"),
        ("AMEPlayerMercCount", "MERCPlayerMercCount"),
        ("JAZZ_AME_GetCategoryLabel", "JAZZ_MERC_GetOrgLabel"),
        ("JAZZ_AME_GetPotentialLabel", "JAZZ_MERC_GetStatusLabel"),
        ("ame-exchange.net", "merc.com"),
        ("AME_PdaBackdrop", "MERC_PdaBackdrop"),
        ("AME_Mark", "MERC_Mark"),
        ("AME_BannerPad", "MERC_BannerPad"),
        ('AddPageToBrowserHistory("ame")', 'AddPageToBrowserHistory("merc")'),
        ("'ame'", "'merc'"),
        ('"mode", "ame"', '"mode", "merc"'),
    ]
    for a, b in reps:
        t = t.replace(a, b)
    # Undo over-replace of Affiliation / comments if any — restore intentional merc strings only.
    # AME hide-perks comment → show perks for MERC
    t = t.replace(
        "-- AME: hide Traits/Perks strip (keep Equipment). AIM browser unchanged.",
        "-- MERC: keep Traits/Perks strip (named mercs). AME still hides them.",
    )
    # Color shift ochre → bargain green-grey (common AME tint prefixes)
    for old, new in (
        ("RGBA(180, 140, 70", "RGBA(90, 120, 95"),
        ("RGBA(160, 120, 50", "RGBA(70, 100, 80"),
        ("RGBA(200, 160, 90", "RGBA(110, 140, 115"),
        ("RGBA(140, 110, 55", "RGBA(60, 90, 70"),
    ):
        t = t.replace(old, new)
    DST.write_text(t, encoding="utf-8")
    print(f"wrote {DST.relative_to(ROOT)} lines={len(t.splitlines())}")
    print(
        "remaining AME=",
        t.count("AME"),
        "PDAAIME=",
        t.count("PDAAIME"),
        "ame-exchange=",
        t.count("ame-exchange"),
    )


if __name__ == "__main__":
    main()
