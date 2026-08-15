# -*- coding: utf-8 -*-
"""Static: smoke/tear/toxic/fire must not roll ballistic bleed or DangerClose bleed."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def must(path: Path, needle: str) -> None:
    text = path.read_text(encoding="utf-8")
    if needle not in text:
        raise SystemExit(f"{path.relative_to(ROOT)}: missing {needle!r}")


def main() -> None:
    med = ROOT / "Code" / "Systems_Medicine.lua"
    armor = ROOT / "Code" / "System_ArmorRating.lua"
    perks = ROOT / "Code" / "System_NamedPerks.lua"
    must(med, "function JazzIsEnvironmentalAoeHit")
    must(med, 'aoe == "smoke" or aoe == "teargas" or aoe == "toxicgas" or aoe == "fire"')
    must(med, "if JazzIsEnvironmentalAoeHit(hit) then")
    must(armor, "JazzIsEnvironmentalAoeHit(hit)")
    must(armor, 'effect == "Bleeding"')
    must(perks, "JazzIsEnvironmentalAoeHit")
    must(perks, "bleed_stacks_to_add")
    print("OK smoke/gas/fire skip ballistic bleed")


if __name__ == "__main__":
    raise SystemExit(main())
