# Bump jazz core ModDef display to 0.18 (version_minor 18, rev +1).
from pathlib import Path
import re

p = Path(__file__).resolve().parents[2] / "metadata.lua"
text = p.read_text(encoding="utf-8-sig")

old_title = '[EN/RU] JAZZ - Tactical Overhaul - v0.17 Демо Острова Эрни'
new_title = '[EN/RU] JAZZ - Tactical Overhaul - v0.18 Демо Острова Эрни'
if old_title not in text:
	raise SystemExit("title v0.17 not found")
text = text.replace(old_title, new_title, 1)

needle = "'last_changes', \""
i = text.find(needle)
if i < 0:
	raise SystemExit("last_changes not found")
j = i + len(needle)
bullet = "- Suite display version set to 0.18 (version_minor 18)\\n"
if not text.startswith(bullet, j):
	text = text[:j] + bullet + text[j:]

m = re.search(
	r"('author', \"Kpoji4er\",\n\t'version_major', 0,\n\t'version_minor', )17(,\n\t'version', )6014,",
	text,
)
if not m:
	raise SystemExit("core version block 0/17/6014 not found")
text = text[: m.start(1)] + m.group(1) + "18" + m.group(2) + "6015," + text[m.end() :]

# last_changes: no raw LF between quotes
lc = re.search(r"'last_changes', \"(.*?)\"", text, re.DOTALL)
if not lc:
	raise SystemExit("last_changes parse fail")
val = lc.group(1)
k = 0
while k < len(val):
	if val[k] == "\\" and k + 1 < len(val) and val[k + 1] == "n":
		k += 2
		continue
	if val[k] in "\n\r":
		raise SystemExit("RAW newline in last_changes")
	k += 1

p.write_text(text, encoding="utf-8")
print("OK -> display 0.18-6015")
print("title:", new_title)
print("last_changes head:", val[:80])
