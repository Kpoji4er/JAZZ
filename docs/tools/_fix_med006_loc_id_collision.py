# -*- coding: utf-8 -*-
"""Move MED-006 loc off VoiceResponse IDs 010220-222 onto 010290-292."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP = {
    "890000000010220": "890000000010290",
    "890000000010221": "890000000010291",
    "890000000010222": "890000000010292",
}
TEXTS = {
    "890000000010290": {
        "en": "<target> trauma stabilized",
        "ru": "<target>: травма стабилизирована",
    },
    "890000000010291": {
        "en": "Stabilized: combat penalties eased (one tier lighter). Does not heal the trauma — field treatment / hospital required.",
        "ru": "Стабилизирована: боевые штрафы ослаблены (на один тир легче). Не лечит травму — нужна полевая операция / госпиталь.",
    },
    "890000000010292": {
        "en": "Max HP debt from this trauma: <em><pct>%</em>.",
        "ru": "Долг макс. ОЗ от этой травмы: <em><pct>%</em>.",
    },
}
VR = {
    "890000000010220": ("Есть.", "On it.", "Есть."),
    "890000000010221": ("Есть.", "On it.", "Есть."),
    "890000000010222": ("Двигаюсь.", "Moving.", "Двигаюсь."),
}


def patch_code() -> None:
    for rel in ("Code/System_UnitInventory.lua", "Code/Systems_Medicine.lua"):
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        for old, new in MAP.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
        print("patched", rel)


def upsert_csv(path: Path, lang: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    seen = set()
    for line in lines:
        rid = line.split(",", 1)[0].strip().strip('"')
        if rid in MAP:  # old medicine ids that stole VR — restore VR in jazz csv or drop med
            src, en, ru = VR[rid]
            if lang == "en":
                out.append(f"{rid},{src},{en},,jazz-units:VoiceResponse-restore")
            else:
                out.append(f"{rid},{src},{ru},,jazz-units:VoiceResponse-restore")
            seen.add(rid)
            continue
        if rid in TEXTS:
            # replace existing new ids if any
            t = TEXTS[rid]
            if lang == "en":
                out.append(f"{rid},{t['en']},{t['en']},,jazz:MED-006")
            else:
                out.append(f"{rid},{t['en']},{t['ru']},,jazz:MED-006")
            seen.add(rid)
            continue
        out.append(line)
    for rid, t in TEXTS.items():
        if rid not in seen:
            if lang == "en":
                out.append(f"{rid},{t['en']},{t['en']},,jazz:MED-006")
            else:
                out.append(f"{rid},{t['en']},{t['ru']},,jazz:MED-006")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("csv", path.name)


def main() -> None:
    patch_code()
    upsert_csv(ROOT / "English.csv", "en")
    upsert_csv(ROOT / "Russian.csv", "ru")


if __name__ == "__main__":
    main()
