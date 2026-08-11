# Static: Spike BulletHell COMBAT-006 v2 — FirearmAttack + projectile arc (no AlwaysHits AOE dump).
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
needles = {
    "Code/CombatActions.lua": [
        "function Unit:BulletHell",
        'SetActionCommand("FirearmAttack"',
    ],
    "Code/System_OR_Weapons.lua": [
        "JazzInstallBulletHellProjectiles",
        "AlwaysHits = false",
        "JazzProjectileResultsWrapped",
        "jazz_bh_arc_sprayed",
        "AbakanAutoFire",
        "JAZZ_LargeAutoFire",
    ],
    "Code/ExecFirearmAttacks.lua": [
        "jazz_bh_arc_sprayed",
    ],
}
forbidden = {
    "Code/CombatActions.lua": [
        "JazzBulletHellConeTargets",
    ],
}
missing = []
for rel, keys in needles.items():
    text = (root / rel).read_text(encoding="utf-8")
    for k in keys:
        if k not in text:
            missing.append(f"{rel}: missing {k}")
extra = []
for rel, keys in forbidden.items():
    text = (root / rel).read_text(encoding="utf-8")
    for k in keys:
        if k in text:
            extra.append(f"{rel}: leftover {k}")
if missing or extra:
    print("FAIL:")
    for m in missing + extra:
        print(" ", m)
    sys.exit(1)
print("OK BulletHell FirearmAttack + cone-arc projectiles (COMBAT-006 v2)")
sys.exit(0)
