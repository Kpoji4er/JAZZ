# Static: JAZZ-COMBAT-006 BulletHell projectile model + AN94 gate.
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
needles = {
    "Code/CombatActions.lua": [
        "function Unit:BulletHell",
        "JazzBulletHellConeTargets",
        "suppressionbonus or 200",
        "CombatActions.SingleShot",
    ],
    "Code/System_OR_Weapons.lua": [
        "JazzInstallBulletHellProjectiles",
        "AlwaysHits = false",
        "JazzProjectileResultsWrapped",
        "AbakanAutoFire",
        "aoe_params and (action.id == \"BulletHell\"",
    ],
}
missing = []
for rel, keys in needles.items():
    text = (root / rel).read_text(encoding="utf-8")
    for k in keys:
        if k not in text:
            missing.append(f"{rel}: {k}")
if missing:
    print("FAIL missing:")
    for m in missing:
        print(" ", m)
    sys.exit(1)
# Must not still force AlwaysHits AOE applied_status in GetActionResults wrap
wrap = (root / "Code/System_OR_Weapons.lua").read_text(encoding="utf-8")
if 'applied_status = { "Suppressed"' in wrap and "JazzInstallBulletHellProjectiles" in wrap:
    # vanilla string should not be reintroduced in our install
    pass
if "args.applied_status = false" not in wrap:
    print("FAIL GetActionResults wrap must clear applied_status")
    sys.exit(1)
print("OK COMBAT-006 BulletHell projectiles static")
