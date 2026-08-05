# CloseRange inventory-card rollover loc (RolloverPropTextRight values).
# Label reuses T(982641736210) «Ближняя зона» / «Close range».
# Values: 890000000001937 boost, 890000000001938 penalty (no hint bullets).
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = "jazz:Code/System_Firearm_AddProperties.lua"

ROWS = [
    (
        "890000000001937",
        "+<bonus> (<tiles> кл.)",
        "+<bonus> (<tiles> tiles)",
    ),
    (
        "890000000001938",
        "−<penalty>% (<tiles> кл.)",
        "−<penalty>% (<tiles> tiles)",
    ),
]


def csv_field(s: str) -> str:
    if any(c in s for c in ',"\n'):
        return '"' + s.replace('"', '""') + '"'
    return s


def upsert(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines(True)
    by_id = {}
    for id_, ru, en in ROWS:
        if path.name.startswith("English"):
            by_id[id_] = f"{id_},{csv_field(ru)},{csv_field(en)},,{SRC}\n"
        else:
            by_id[id_] = f"{id_},{csv_field(ru)},{csv_field(ru)},,{SRC}\n"
    out = []
    seen = set()
    for line in lines:
        hit = None
        for id_ in by_id:
            if line.startswith(id_ + ","):
                hit = id_
                break
        if hit:
            out.append(by_id[hit])
            seen.add(hit)
            print(f"{path.name}: updated {hit}")
        else:
            out.append(line)
    for id_, row in by_id.items():
        if id_ not in seen:
            if out and not out[-1].endswith("\n"):
                out[-1] += "\n"
            out.append(row)
            print(f"{path.name}: appended {id_}")
    path.write_text("".join(out), encoding="utf-8")


def main() -> None:
    upsert(ROOT / "Russian.csv")
    upsert(ROOT / "English.csv")


if __name__ == "__main__":
    main()
