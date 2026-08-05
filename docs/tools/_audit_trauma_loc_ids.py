# Audit Trauma* T() IDs vs Russian.csv / English.csv Text+Translation.
import csv
import re
from pathlib import Path

root = Path(__file__).resolve().parents[2]


def load(path: Path):
    """JA3 runtime CSV: sep=, then rows ID,Text,Translation,VoiceActor,Context (often no header)."""
    rows = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        first = f.readline()
        if not first.startswith("sep="):
            f.seek(0)
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0] == "ID":
                continue
            rows.setdefault(row[0], []).append(row)
    return rows


ru = load(root / "Russian.csv")
en = load(root / "English.csv")

pat = re.compile(r'T\((\d+),\s*"([^"]*)"\)')
from_files = {}
for p in sorted((root / "CharacterEffect").glob("Trauma*.lua")):
    text = p.read_text(encoding="utf-8")
    for m in pat.finditer(text):
        from_files.setdefault(m.group(1), []).append((p.name, m.group(2)))

med = (root / "Code" / "Systems_Medicine.lua").read_text(encoding="utf-8")
for m in re.finditer(r'T\{?(\d+),\s*"([^"]*)"', med):
    tid = m.group(1)
    if tid.startswith("8900000000101") or tid.startswith("8900000000102"):
        from_files.setdefault(tid, []).append(("Systems_Medicine.lua", m.group(2)))

print("=== Companion/Medicine T() vs CSV ===")
broken = []
for tid, locs in sorted(from_files.items()):
    src = locs[0][1]
    ru_rows = ru.get(tid, [])
    en_rows = en.get(tid, [])
    issues = []
    if not ru_rows:
        issues.append("MISSING_RU")
    if not en_rows:
        issues.append("MISSING_EN")
    if len(ru_rows) > 1:
        issues.append(f"DUP_RU={len(ru_rows)}")
    if len(en_rows) > 1:
        issues.append(f"DUP_EN={len(en_rows)}")
    if ru_rows and ru_rows[0][1] != src:
        issues.append("RU_TEXT_MISMATCH")
    if en_rows and en_rows[0][1] != src:
        issues.append("EN_TEXT_MISMATCH")
    if ru_rows and not (ru_rows[0][2] if len(ru_rows[0]) > 2 else "").strip():
        issues.append("EMPTY_RU_TR")
    if en_rows and not (en_rows[0][2] if len(en_rows[0]) > 2 else "").strip():
        issues.append("EMPTY_EN_TR")
    if ru_rows and len(ru_rows[0]) > 2:
        tr = ru_rows[0][2] or ""
        if "Тора" in tr or "Schnell" in tr or "пороховницах" in tr:
            issues.append("GARBAGE_RU_TR")
    status = "OK" if not issues else ";".join(issues)
    loc = ",".join(sorted({x[0] for x in locs}))
    print(f"{tid} [{loc}] {status}")
    if issues:
        broken.append(tid)
        print(f"  src: {src[:100]!r}")
        if ru_rows:
            print(f"  ru Text: {ru_rows[0][1][:100]!r}")
            print(f"  ru Tr:   {(ru_rows[0][2] if len(ru_rows[0])>2 else '')[:100]!r}")

print(f"\nBroken count: {len(broken)}")
if broken:
    raise SystemExit(1)
print("OK")
