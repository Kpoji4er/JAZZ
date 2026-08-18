"""Index all JAZZ change specs: status, evidence, TBD, related IDs."""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPECS = ROOT / "docs" / "specs"

FRONT = re.compile(r"^---\n(.*?)\n---", re.S)
AC_ID = re.compile(r"`(JAZZ-[A-Z0-9-]+-AC-\d+)`")
REQ_ID = re.compile(r"`(JAZZ-[A-Z0-9-]+-REQ-\d+)`")
SPEC_REF = re.compile(r"JAZZ-[A-Z][A-Z0-9-]*")
EV_LOOSE = re.compile(
    r"`(JAZZ-[A-Z0-9-]+-AC-\d+)`[:\s].{0,80}?\b(PASS|FAIL|BLOCKED|PARTIAL)\b",
    re.I,
)


def parse_front(text: str) -> dict:
    m = FRONT.match(text)
    if not m:
        return {}
    data = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data


def evidence_counts(text: str) -> Counter:
    c = Counter()
    ev = text
    if "## Evidence" in text:
        ev = text.split("## Evidence", 1)[1]
        if "\n## " in ev:
            ev = ev.split("\n## ", 1)[0]
    for m in EV_LOOSE.finditer(ev):
        c[m.group(2).upper()] += 1
    return c


def main() -> None:
    rows = []
    for path in sorted(SPECS.rglob("*.md")):
        if path.name in {"README.md", "change.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        fm = parse_front(text)
        rel = path.relative_to(ROOT).as_posix()
        folder = path.parent.name
        sid = fm.get("id", path.stem)
        status = fm.get("status", "?")
        acs = sorted(set(AC_ID.findall(text)))
        reqs = sorted(set(REQ_ID.findall(text)))
        ev = evidence_counts(text)
        tbd = len(re.findall(r"\bTBD\b", text, re.I))
        todo = len(re.findall(r"\bTODO\b", text, re.I))
        refs = sorted({r for r in SPEC_REF.findall(text) if r != sid})
        refs = [
            r
            for r in refs
            if re.match(r"^JAZZ-[A-Z]+(?:-[A-Z]+)?-\d+$", r)
            or r.endswith("ROADMAP")
        ]
        rows.append(
            {
                "file": rel,
                "folder": folder,
                "id": sid,
                "status": status,
                "acs": len(acs),
                "reqs": len(reqs),
                "pass": ev.get("PASS", 0),
                "fail": ev.get("FAIL", 0),
                "blocked": ev.get("BLOCKED", 0),
                "partial": ev.get("PARTIAL", 0),
                "tbd": tbd,
                "todo": todo,
                "refs": refs,
            }
        )

    by_status = Counter(r["status"] for r in rows)
    print("=== COUNT BY STATUS ===")
    for k, v in sorted(by_status.items()):
        print(f"{k}: {v}")
    print(f"total: {len(rows)}")
    print()

    print("=== FOLDER vs STATUS MISMATCH ===")
    for r in rows:
        st, fol = r["status"], r["folder"]
        ok = (
            (st == "superseded" and fol == "superseded")
            or (st == "accepted" and fol == "accepted")
            or (st in {"draft", "approved", "implemented"} and fol == "active")
        )
        if not ok:
            print(f"{r['id']} status={st} folder={fol}")
    print()

    print("=== IMPLEMENTED WITH FAIL ===")
    for r in rows:
        if r["status"] == "implemented" and r["fail"]:
            print(f"{r['id']} FAIL={r['fail']} BLOCKED={r['blocked']}")
    print()

    print("=== IMPLEMENTED WITH BLOCKED ===")
    n = 0
    for r in rows:
        if r["status"] == "implemented" and r["blocked"]:
            n += 1
            print(f"{r['id']}\tBLOCKED={r['blocked']}\tPASS={r['pass']}\tAC={r['acs']}")
    print(f"implemented+blocked: {n}")
    print()

    print("=== APPROVED WITH FAIL ===")
    for r in rows:
        if r["status"] == "approved" and r["fail"]:
            print(f"{r['id']} FAIL={r['fail']}")
    print()

    print("=== DRAFT LIST ===")
    for r in rows:
        if r["status"] == "draft":
            print(f"{r['id']}\tTBD={r['tbd']} TODO={r['todo']}")
    print()

    print("=== APPROVED WITH TBD/TODO ===")
    for r in rows:
        if r["status"] == "approved" and (r["tbd"] or r["todo"]):
            print(f"{r['id']}\tTBD={r['tbd']} TODO={r['todo']}")
    print()

    print("=== IMPLEMENTED WITH TBD/TODO ===")
    for r in rows:
        if r["status"] == "implemented" and (r["tbd"] or r["todo"]):
            print(f"{r['id']}\tTBD={r['tbd']} TODO={r['todo']}")
    print()

    print("=== NO AC / NO REQ ===")
    for r in rows:
        if r["folder"] == "_template":
            continue
        if r["acs"] == 0 or r["reqs"] == 0:
            print(f"{r['id']} reqs={r['reqs']} acs={r['acs']} status={r['status']}")
    print()

    print("=== CROSS-REFS ===")
    ids = {r["id"] for r in rows}
    graph = defaultdict(set)
    for r in rows:
        for ref in r["refs"]:
            if ref in ids:
                graph[r["id"]].add(ref)
    for src in sorted(graph):
        print(f"{src} -> {', '.join(sorted(graph[src]))}")


if __name__ == "__main__":
    main()
