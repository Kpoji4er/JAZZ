"""Bump jazz metadata after IMP-001 Sniper/LMG fix commit."""
from pathlib import Path

path = Path(__file__).resolve().parents[2] / "metadata.lua"
text = path.read_text(encoding="utf-8")
if "'version', 5976," not in text:
    raise SystemExit(f"expected version 5976, got other: {path}")
text = text.replace("'version', 5976,", "'version', 5977,", 1)
# Literal backslash-n for valid Lua string content (not a Python newline).
fix = (
    "- IMP-001 fix: Sniper OnCalcMaxAimActions signature; "
    "LMG Mark>=60; safe inventory clear\\n"
)
needle = "'last_changes', \"- IMP-001: JA2-style"
if "- IMP-001 fix: Sniper" not in text:
    if needle not in text:
        raise SystemExit("last_changes IMP-001 bullet not found")
    text = text.replace(needle, "'last_changes', \"" + fix + "- IMP-001: JA2-style", 1)
path.write_text(text, encoding="utf-8", newline="\n")
print("metadata -> version 5977 + fix bullet")
