from pathlib import Path

p = Path(__file__).resolve().parents[2] / "items.lua"
t = p.read_text(encoding="utf-8")
marker = "'Id', \"Concussion\""
start = t.find(marker)
if start < 0:
    raise SystemExit("Concussion missing")
end = start + 3000
chunk = t[start:end]
repl = {
    "890000000010220": "890000000010277",
    "890000000010221": "890000000010278",
    "890000000010222": "890000000010279",
    "890000000010223": "890000000010280",
}
orig = chunk
for a, b in repl.items():
    chunk = chunk.replace(a, b)
if chunk == orig:
    print("no change (already fixed or old ids absent)")
else:
    p.write_text(t[:start] + chunk + t[end:], encoding="utf-8")
    print("fixed Concussion loc IDs in items.lua")
