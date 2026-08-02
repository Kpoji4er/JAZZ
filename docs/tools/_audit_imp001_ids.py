"""Static audit: IMP-001 gear/perk class IDs resolve in jazz (+ optional jazz-units)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT.parent / "jazz-units"

NEED = [
    "TT33",
    "R870",
    "SKS",
    "MPL",
    "TMP",
    "CAR15",
    "MP5SD",
    "BAR",
    "RPD",
    "M79",
    "APS",
    "MicroUZI",
    "Glock17",
    "CamoArmor_Light",
    "KevlarVest",
    "JazzArmor_ZylonLight",
    "LightHelmet",
    "FlakLeggings",
    "FlareStick",
    "Knife",
    "Knife_Balanced",
    "FragGrenade",
    "Crowbar",
    "SkillMag_Leadership",
    "SkillMag_Wisdom",
    "SkillMag_Mechanical",
    "SkillMag_Medical",
    "Wirecutter",
    "Lockpick",
    "Parts",
    "TNT",
    "PipeBomb",
    "Medkit",
    "FirstAidKit",
    "Meds",
    "Molotov",
    "SmokeGrenade",
    "ConcussiveGrenade",
    "Machete",
    "_40mmFlashbangGrenade",
    "_40mmFragGrenade",
    "AutoWeapons",
    "HeavyWeaponsTraining",
    "Stealthy",
    "MeleeTraining",
    "CQCTraining",
    "Scoundrel",
    "Teacher",
    "MartialArts",
    "MrFixit",
    "NightOps",
    "Throwing",
    "Psycho",
    "Negotiator",
]


def gather_blob(roots):
    parts = []
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*.lua"):
            if any(x in path.parts for x in (".git", "docs", "node_modules")):
                continue
            try:
                parts.append(path.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                pass
    return "\n".join(parts)


def main():
    blob = gather_blob([ROOT, UNITS])
    fails = []
    for item_id in NEED:
        patterns = (
            f"UndefineClass('{item_id}')",
            f"'Id', \"{item_id}\"",
            f'Id = "{item_id}"',
            f'id = "{item_id}"',
        )
        ok = any(p in blob for p in patterns)
        print(("OK" if ok else "MISS"), item_id)
        if not ok:
            fails.append(item_id)
    print("FAILS", fails or "none")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
