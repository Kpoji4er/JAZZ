from pathlib import Path
import re

units_items = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
t = units_items.read_text(encoding="utf-8")
i = t.find("'Id', \"Jazz_Carlos\"")
print("carlos Id", i)
# find end of this ModItemUnitData — next ModItemVoiceResponse or folder close
chunk = t[i : i + 8000]
j = chunk.find("'StartingPerks'")
print("StartingPerks relative", j)
print(chunk[max(0, j - 250) : j + 300])
print("--- Dislikes in chunk?", "Jazz_Iggy" in chunk[:j] if j > 0 else None)

# last_changes
for p in [
    Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\metadata.lua"),
    Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\metadata.lua"),
]:
    text = p.read_text(encoding="utf-8")
    m = re.search(r"'last_changes',\s*\"((?:\\.|[^\"\\])*)\"", text)
    s = m.group(1) if m else ""
    # raw newline would break the regex or appear as actual \n char
    has_raw = "\n" in s or "\r" in s
    print(p.parent.name, "has_raw_nl", has_raw, "prefix", s[:100].replace("\\n", " | "))
