#!/usr/bin/env python3
"""Polish System_MERC_Browser_Template.lua labels after fork."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "Code" / "System_MERC_Browser_Template.lua"
t = p.read_text(encoding="utf-8")
reps = [
    (
        "========== AME LUA BROWSER SOURCE (JAZZ-UNITS-005) ==========",
        "========== MERC LUA BROWSER SOURCE (JAZZ-UI-MERC-001) ==========",
    ),
    ("'comment', \"AME mark\"", "'comment', \"MERC mark\""),
    ("'comment', \"AME brand strip\"", "'comment', \"MERC brand strip\""),
    ("A.M.E. 2001", "M.E.R.C."),
    ("JAZZ_AME_GetDepartureReasonText", "JAZZ_MERC_GetDepartureReasonText"),
    ("idAMECategory", "idMERCOrg"),
    ("idAMEPotential", "idMERCStatus"),
    (
        'T(890000000005018, --[[XTemplate PDAMERCBrowser Text]] "Category:")',
        'T(890000000007018, --[[XTemplate PDAMERCBrowser Text]] "Org:")',
    ),
    (
        'T(890000000005019, --[[XTemplate PDAMERCBrowser Text]] "Potential:")',
        'T(890000000007019, --[[XTemplate PDAMERCBrowser Text]] "Status:")',
    ),
    (
        'T(890000000005049, --[[XTemplate PDAMERCBrowser Text]] "<style AimCopyrightTextC><copyright></style> M.E.R.C.")',
        'T(890000000007049, --[[XTemplate PDAMERCBrowser Text]] "<style AimCopyrightTextC><copyright></style> M.E.R.C.")',
    ),
]
for a, b in reps:
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("polished", p.name, "AME left", t.count("AME"))
