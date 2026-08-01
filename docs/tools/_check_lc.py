from pathlib import Path

for p in [
    Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\metadata.lua"),
    Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\metadata.lua"),
]:
    t = p.read_text(encoding="utf-8")
    i = t.find("'last_changes'")
    print(p.parent.name, "idx", i)
    print(repr(t[i : i + 140]))
    print("---")
