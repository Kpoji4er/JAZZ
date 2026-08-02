"""Fix bare newline after IMP-001 last_changes bullet (invalid Lua string)."""
from pathlib import Path

MARKER = "[new game recommended]\n- "
REPL = "[new game recommended]\\n- "

roots = [
    Path(__file__).resolve().parents[2],
    Path(__file__).resolve().parents[2].parent / "jazz-units",
]

for root in roots:
    path = root / "metadata.lua"
    text = path.read_text(encoding="utf-8")
    if MARKER not in text:
        print(f"{path}: no bare-newline pattern")
        continue
    path.write_text(text.replace(MARKER, REPL, 1), encoding="utf-8", newline="\n")
    print(f"{path}: fixed")
