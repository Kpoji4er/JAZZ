# -*- coding: utf-8 -*-
"""Generate Code/System_WeaponComponent_Set.lua from vanilla FirearmBase:SetWeaponComponent."""
from __future__ import annotations

from pathlib import Path

VANILLA = Path(
    r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3"
    r"\ModTools\Src\Lua\Tactical\Weapon.lua"
)
DEST = Path(__file__).resolve().parents[2] / "Code" / "System_WeaponComponent_Set.lua"


def main() -> None:
    lines = VANILLA.read_text(encoding="utf-8", errors="replace").splitlines()
    # 1-based lines 500-646 inclusive
    chunk = lines[499:646]
    out: list[str] = [
        "-- JAZZ-ATTACH-001: MagazineSizeSet via ModificationType = \"Set\"",
        "-- Vanilla FirearmBase:SetWeaponComponent only handles Add/Multiply/Subtract.",
        "-- Engine: MulDivRound(base + mod_add, mod_mul, 1000).",
        "-- Set must use mul=1000, add=N-base (mul=0 always yields 0 → MagSize 1 in UI).",
        "",
    ]
    i = 0
    while i < len(chunk):
        line = chunk[i]
        if 'if mod.ModificationType == "Add" then' in line:
            indent = "\t\t\t\t\t"
            out.extend(
                [
                    indent + "local add = 0",
                    indent + "local mul = 1000",
                    indent + 'if mod.ModificationType == "Add" then',
                    indent + "\tadd = value",
                    indent + 'elseif mod.ModificationType == "Multiply" then',
                    indent + "\tmul = value * 10",
                    indent + 'elseif mod.ModificationType == "Subtract" then',
                    indent + "\tadd = -value",
                    indent + 'elseif mod.ModificationType == "Set" then',
                    indent + "\t-- Absolute overwrite: (base + (N - base)) * 1000/1000 = N.",
                    indent + "\tmul = 1000",
                    indent + '\tlocal base = self["base_" .. mod.StatToModify] or 0',
                    indent + "\tadd = value - base",
                    indent + "end",
                    indent,
                    indent + "self:AddModifier(id, mod.StatToModify, mul, add)",
                ]
            )
            while i < len(chunk) and "self:AddModifier(id, mod.StatToModify" not in chunk[i]:
                i += 1
            i += 1
            continue
        if line.strip() in ("local add = 0", "local mul = 1000"):
            i += 1
            continue
        out.append(line)
        i += 1

    DEST.write_text("\n".join(out) + "\n", encoding="utf-8")
    text = DEST.read_text(encoding="utf-8")
    assert 'ModificationType == "Set"' in text
    assert "add = value - base" in text
    print(f"wrote {DEST} ({len(out)} lines)")


if __name__ == "__main__":
    main()
