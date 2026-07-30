# -*- coding: utf-8 -*-
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NERF = {"MPL": {"AimAccuracy": 11}, "BerettaM12": {"AimAccuracy": 13}}


def set_lua(path: Path, fields: dict) -> None:
    t = path.read_text(encoding="utf-8")
    for k, v in fields.items():
        t2, n = re.subn(rf"^(\t{k} = )-?\d+,", rf"\g<1>{v},", t, count=1, flags=re.M)
        if n != 1:
            raise SystemExit(f"{path} {k}")
        t = t2
    path.write_text(t, encoding="utf-8")


def set_items(wid: str, fields: dict) -> None:
    path = ROOT / "items.lua"
    text = path.read_text(encoding="utf-8")
    i = text.find(f"'Id', \"{wid}\"")
    if i < 0:
        raise SystemExit(wid)
    w = text[i : i + 3500]
    nw = w
    for k, v in fields.items():
        nw, n = re.subn(rf"('{k}', )-?\d+", rf"\g<1>{v}", nw, count=1)
        if n != 1:
            raise SystemExit(f"items {wid} {k}")
    path.write_text(text[:i] + nw + text[i + len(w) :], encoding="utf-8")


def main():
    for wid, f in NERF.items():
        set_lua(ROOT / f"InventoryItem/{wid}.lua", f)
        set_items(wid, f)
        print("nerf", wid, f)
    path = ROOT / "docs/technical/weapons/data/weapons.csv"
    rows = []
    with path.open(encoding="utf-8", newline="") as fh:
        r = csv.DictReader(fh)
        fields = r.fieldnames
        for row in r:
            if row["id"] in NERF:
                row["aim_accuracy"] = str(NERF[row["id"]]["AimAccuracy"])
            rows.append(row)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("csv ok")


if __name__ == "__main__":
    main()
