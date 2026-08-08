#!/usr/bin/env python3
"""Retint System_MERC_Browser_Template.lua to JA2 MERC teal theme."""
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "Code" / "System_MERC_Browser_Template.lua"
t = p.read_text(encoding="utf-8")
t = t.replace('AddPageToBrowserHistory("ame", nil)', 'AddPageToBrowserHistory("merc", nil)')
t = t.replace("bkg frame savannah", "bkg frame JA2-MERC teal")
t = t.replace("bg khaki", "bg merc teal")
reps = [
    ("RGBA(255, 230, 190, 255)", "RGBA(150, 235, 225, 255)"),
    ("RGBA(168, 128, 72, 255)", "RGBA(0, 145, 155, 255)"),
    ("RGBA(186, 150, 92, 255)", "RGBA(15, 125, 135, 255)"),
    ("RGBA(172, 132, 74, 255)", "RGBA(10, 115, 125, 255)"),
    ("RGBA(186, 150, 90, 255)", "RGBA(40, 170, 175, 255)"),
    ("RGBA(148, 110, 58, 180)", "RGBA(0, 100, 110, 180)"),
    ("RGBA(90, 60, 28, 255)", "RGBA(20, 70, 80, 255)"),
    ("RGBA(55, 40, 22, 140)", "RGBA(10, 45, 55, 150)"),
]
for a, b in reps:
    print(a, "->", t.count(a))
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("merc history", 'AddPageToBrowserHistory("merc"' in t)
