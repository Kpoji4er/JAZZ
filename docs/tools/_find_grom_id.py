from pathlib import Path

t = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua").read_text(encoding="utf-8")
idx = t.find('\tid = "Grom",\n\t\t}),')
if idx < 0:
    # try alternate
    idx = t.find('id = "Grom",\n\t\t}),')
    print("alt", idx)
else:
    print("exact close near id", idx)

# find the id line that is followed soon by }),
needle = 'id = "Grom",'
pos = 0
while True:
    i = t.find(needle, pos)
    if i < 0:
        break
    snippet = t[i : i + 40]
    print("at", i, repr(snippet))
    pos = i + 1
