# Remaining Free Move AP UI: tooltip + merc-card suffix (IDs 890000000013122–13123).
# Russian.csv: Text = English T() source, Translation = Russian (JA3 displays Translation).
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = "jazz:COMBAT-007-freemove-ui"

ROWS = [
    (
        "890000000013122",
        "Перемещение без траты ОД. Осталось: <em><apn(remain)> ОД</em>. Снимается после атаки или когда запас исчерпан (зависит от Ловкости).",
        "Move without spending AP. Remaining: <em><apn(remain)> AP</em>. Removed after attacking or after using up the allowance (based on Agility).",
    ),
    (
        "890000000013123",
        " <em>(<apn(fm)> FM)</em>",
        " <em>(<apn(fm)> FM)</em>",
    ),
]


def csv_field(s: str) -> str:
    if any(c in s for c in ',"\n'):
        return '"' + s.replace('"', '""') + '"'
    return s


def upsert(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines(True)
    by_id = {}
    english = path.name.startswith("English")
    for id_, ru, en in ROWS:
        # Text = T() source (English); Translation = language column.
        if english:
            by_id[id_] = f"{id_},{csv_field(en)},{csv_field(en)},,{SRC}\n"
        else:
            by_id[id_] = f"{id_},{csv_field(en)},{csv_field(ru)},,{SRC}\n"
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
