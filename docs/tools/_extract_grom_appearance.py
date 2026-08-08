from pathlib import Path

t = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua").read_text(encoding="utf-8")
close = t.find('id = "Grom",\n\t\t}),')
start = t.rfind("PlaceObj('ModItemAppearancePreset'", 0, close)
end = close + len('id = "Grom",\n\t\t}),')
block = t[start:end]
out = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\docs\tools\_grom_snippets\Appearance_Grom.lua.txt")
out.write_text(block + "\n", encoding="utf-8")
print("len", len(block), "lines", block.count("\n") + 1)
print(block[-80:])
