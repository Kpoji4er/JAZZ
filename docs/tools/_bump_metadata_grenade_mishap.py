# Bump jazz metadata version + append last_changes for grenade mishap retune.
from pathlib import Path
import re

path = Path(__file__).resolve().parents[2] / "metadata.lua"
text = path.read_text(encoding="utf-8")

text2, n = re.subn(r"('version', )6114\b", r"\g<1>6115", text, count=1)
if n != 1:
    raise SystemExit(f"version bump failed n={n}")

bullet = (
    "- GRENADES-001: throw mishap thr 50; chance ramps 1/4→1/2; "
    "half≈old max scatter, max≈+25% (90/90 ~80% prior); hints/docs [no new game]\\n"
)
# Insert after opening quote of last_changes
pat = r"('last_changes', \")"
m = re.search(pat, text2)
if not m:
    raise SystemExit("last_changes open not found")
ins_at = m.end()
text3 = text2[:ins_at] + bullet + text2[ins_at:]

# Verify no raw newline inside last_changes value
# Extract value between quotes after last_changes
m2 = re.search(r"'last_changes', \"((?:\\.|[^\"\\])*)\"", text3)
if not m2:
    raise SystemExit("could not re-parse last_changes")
val = m2.group(1)
if "\n" in val or "\r" in val:
    raise SystemExit("raw newline inside last_changes")

path.write_text(text3, encoding="utf-8")
print("metadata: version 6115, last_changes appended")
