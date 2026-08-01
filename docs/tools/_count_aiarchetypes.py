from pathlib import Path
import re

text = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua").read_text(
    encoding="utf-8"
)
starts = [m.start() for m in re.finditer(r"PlaceObj\('ModItemAIArchetype'", text)]
ids = []
for s in starts:
    chunk = text[s : s + 100000]
    end_m = re.search(r'\n\t\t\t\tgroup = "[^"]*",\n\t\t\t\tid = "([^"]+)",', chunk)
    if end_m:
        ids.append(end_m.group(1))
    else:
        m = list(re.finditer(r'\tid = "([^"]+)",', chunk))
        ids.append(m[-1].group(1) if m else "?")

print("count", len(ids))
for i in sorted(ids):
    if "Rebel" in i or "Flanker" in i:
        print(i)
print("has Rebels_Flanker", "Rebels_Flanker" in ids)
print("has Legion_Flanker", "Legion_Flanker" in ids)
