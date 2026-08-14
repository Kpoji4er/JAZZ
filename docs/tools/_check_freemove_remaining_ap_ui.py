# Static: remaining Free Move AP is shown in tooltip / icon / merc AP line.
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

NEEDLES = {
    ROOT / "Code" / "System_EnergyLadder.lua": (
        "JazzFormatFreeMoveDescription",
        "JazzFreeMoveOwner",
        "890000000013122",
        "890000000013123",
        "lHookFreeMoveIconText",
        "lPatchPDAMercRolloverAP",
        "UnitAPChanged",
    ),
    ROOT / "CharacterEffect" / "FreeMove.lua": (
        'key == "Description"',
        "function FreeMove:GetDescription()",
        "JazzFormatFreeMoveDescription",
    ),
}


def main() -> int:
    failed = 0
    for path, needles in NEEDLES.items():
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                print(f"FAIL {path.name}: missing {needle!r}")
                failed += 1
            else:
                print(f"OK {path.name}: {needle}")
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
