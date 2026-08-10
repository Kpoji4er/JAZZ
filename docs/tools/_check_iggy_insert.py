from pathlib import Path

u = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua").read_text(encoding="utf-8")
for n in ["Jazz_Iggy", "Loot_JAZZ_Iggy", "JAZZ_Iggy50", 'id = "Iggy"']:
    print(n, u.count(n))
i = u.find('id = "Iggy"')
print("appearance ctx:", repr(u[i - 100 : i + 60]))
i = u.find("'Id', \"Jazz_Iggy\"")
print("unit Id at", i)
# delimiter balance
for a, b in [("(", ")"), ("{", "}"), ("[", "]")]:
    print(a, u.count(a), b, u.count(b), "diff", u.count(a) - u.count(b))
