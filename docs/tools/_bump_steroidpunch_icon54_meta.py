# Append SteroidPunch Passive 54x54 icon bullet; bump Revision if still 6150.
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
meta = ROOT / "metadata.lua"
text = meta.read_text(encoding="utf-8")
m = re.search(r"'version',\s*(\d+)", text)
if not m:
    raise SystemExit("no version")
ver = int(m.group(1))
new_ver = ver + 1
text = re.sub(r"'version',\s*\d+", f"'version', {new_ver}", text, count=1)
bullet = (
    "- UNITS-006: SteroidPunch Passive hotbar icon 54x54 "
    "(not 108 dual; SetColumns=1) + CA name from perk [no new game]\\n"
)
marker = "'last_changes', \""
i = text.find(marker)
if i < 0:
    raise SystemExit("last_changes missing")
ins = i + len(marker)
if "SteroidPunch Passive hotbar icon 54x54" not in text[ins : ins + 200]:
    text = text[:ins] + bullet + text[ins:]
meta.write_text(text, encoding="utf-8", newline="\n")
start = text.find(marker) + len(marker)
end = text.find('",', start)
if "\n" in text[start:end] or "\r" in text[start:end]:
    raise SystemExit("raw newline in last_changes")
print(f"OK version={new_ver}")
