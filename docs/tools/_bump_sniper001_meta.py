# One-shot: bump jazz metadata revision + prepend last_changes bullet.
from pathlib import Path
import re
import sys

p = Path(__file__).resolve().parents[2] / "metadata.lua"
t = p.read_text(encoding="utf-8")
m = re.search(r"'version', (\d+),", t)
if not m:
    sys.exit("version not found")
old, new = int(m.group(1)), int(m.group(1)) + 1
t = t.replace(f"'version', {old},", f"'version', {new},", 1)

bullet = "- AI SNIPER-001: hold if shot; soft HighGround decay after useless turns"
# Insert after opening quote of last_changes value. Value uses double quotes with \n escapes.
needle = "'last_changes', \""
i = t.find(needle)
if i < 0:
    sys.exit("last_changes not found")
insert_at = i + len(needle)
# Ensure we write literal backslash-n between bullets, not raw LF.
ins = bullet + "\\n"
t = t[:insert_at] + ins + t[insert_at:]

# Gate: no raw LF inside last_changes quotes
start = insert_at
# find closing unescaped " — naive: next " that ends the field before next key
# Verify no raw newline between open and the first real content end is hard;
# check the whole last_changes segment for raw LF between quotes.
seg_m = re.search(r"'last_changes', \"((?:\\.|[^\"\\])*)\"", t)
if not seg_m:
    sys.exit("last_changes parse failed after edit")
if "\n" in seg_m.group(1) or "\r" in seg_m.group(1):
    sys.exit("raw newline inside last_changes")

p.write_text(t, encoding="utf-8")
print(f"OK metadata version {old}->{new}; prepended last_changes")
