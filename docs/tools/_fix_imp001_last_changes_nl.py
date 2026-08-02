"""Fix bare newline after IMP-001 last_changes bullets (invalid Lua string)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT.parent / "jazz-units"

# Patterns that must be escaped inside the Lua single-quoted last_changes string.
PATTERNS = (
    ("[new game recommended]\n- ", "[new game recommended]\\n- "),
    (
        "safe inventory clear\n- IMP-001:",
        "safe inventory clear\\n- IMP-001:",
    ),
)

for root in (ROOT, UNITS):
    path = root / "metadata.lua"
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    changed = False
    for old, new in PATTERNS:
        if old in text:
            text = text.replace(old, new)
            changed = True
    if changed:
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"{path}: fixed bare newlines")
    else:
        print(f"{path}: ok")
