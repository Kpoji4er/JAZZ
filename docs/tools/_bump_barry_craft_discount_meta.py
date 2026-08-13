# Bump jazz Revision for Barry DesignerExplosives craft discount fix.
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
meta = ROOT / "metadata.lua"
text = meta.read_text(encoding="utf-8")
m = re.search(r"'version',\s*(\d+)", text)
ver = int(m.group(1)) + 1
text = re.sub(r"'version',\s*\d+", f"'version', {ver}", text, count=1)
bullet = (
    "- UNITS-006: Barry DesignerExplosives — CraftAmmo/Explosives −30% Parts "
    "(sector Barry, not only op assignee); craft_discount cache [no new game]\\n"
)
marker = "'last_changes', \""
i = text.find(marker) + len(marker)
if "Barry DesignerExplosives — CraftAmmo" not in text[i : i + 200]:
    text = text[:i] + bullet + text[i:]
meta.write_text(text, encoding="utf-8", newline="\n")
chunk = text[i : text.find('",', i)]
if "\n" in chunk or "\r" in chunk:
    raise SystemExit("raw newline in last_changes")
print(f"OK version={ver}")
