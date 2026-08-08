# Upsert GrizzlyPerk Description localization (JAZZ-WEAPONS-012).
from pathlib import Path

RID = "272740235755"
RU = (
    "Сигнатурная атака из пулемета игнорирует штрафы <em>без опоры</em> к точности "
    "и отдаче, дает более длинную очередь с пониженным уроном и гораздо лучше удерживает отдачу."
)
EN = (
    "<em>Signature machine-gun attack</em> ignores <em>unsupported</em> accuracy and recoil "
    "penalties, fires a longer burst with reduced damage, and keeps much tighter recoil control."
)


def esc(s: str) -> str:
    if any(c in s for c in ',"\n'):
        return '"' + s.replace('"', '""') + '"'
    return s


def upsert(path: Path, text: str, translation: str) -> None:
    raw = path.read_text(encoding="utf-8")
    ends_nl = raw.endswith("\n")
    lines = raw.splitlines()
    row = f"{RID},{esc(text)},{esc(translation)},,jazz:CharacterEffect/GrizzlyPerk.lua"
    out = []
    found = False
    for line in lines:
        if line.startswith(RID + ","):
            out.append(row)
            found = True
        else:
            out.append(line)
    if not found:
        rid_i = int(RID)
        inserted = False
        new = []
        for i, line in enumerate(out):
            new.append(line)
            if inserted:
                continue
            try:
                cur = int(line.split(",", 1)[0])
            except ValueError:
                continue
            nxt = None
            if i + 1 < len(out):
                try:
                    nxt = int(out[i + 1].split(",", 1)[0])
                except ValueError:
                    nxt = None
            if cur < rid_i and (nxt is None or nxt > rid_i):
                new.append(row)
                inserted = True
        if not inserted:
            new.append(row)
        out = new
        print(path.name, "inserted")
    else:
        print(path.name, "replaced")
    path.write_text("\n".join(out) + ("\n" if ends_nl else ""), encoding="utf-8")


upsert(Path("Russian.csv"), RU, RU)
upsert(Path("English.csv"), RU, EN)
