# Static + numeric: throw mishap uses Strength range + Str/Dex/Expl blend,
# smoothstep 0→full, no quarter/half cliff (JAZZ-GRENADES-001 playtest).
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
weapons = (ROOT / "Code" / "System_OR_Weapons.lua").read_text(encoding="utf-8")

fn_start = weapons.find("function MishapProperties:GetMishapChance")
fn_end = weapons.find("function MishapProperties:GetMishapDeviationBounds")
blend_start = weapons.find("function MishapProperties:GetMishapSkillBlend")
full_start = weapons.find("function MishapProperties:GetMishapFullRange")
failed = []
if fn_start < 0 or fn_end <= fn_start or blend_start < 0 or full_start < 0:
    print("FAIL: mishap functions not found")
    sys.exit(1)

chance = weapons[fn_start:fn_end]
blend = weapons[blend_start:full_start]
full = weapons[full_start:weapons.find("function MishapProperties:GetEffectiveMishapDist")]

for name, blob, pat in [
    ("throw blend Str+Dex+Expl", blend, r"str \+ dex \* 2 \+ expl \* 2"),
    ("GetMaxAimRange Strength", full, r"GetMaxAimRange"),
    ("smoothstep helper", weapons, r"function JazzMishapSmoothstepX100"),
    ("chance uses personal ref", chance, r"GetMishapFullRange\(\s*attacker\s*\)"),
    ("smoothstep in chance", chance, r"JazzMishapSmoothstepX100"),
    ("skill far cap 60", chance, r"MulDivRound\(blend, 60, 100\)"),
]:
    if not re.search(pat, blob):
        failed.append(name)

if re.search(r"quarter", chance):
    failed.append("chance still has quarter cliff")
if re.search(r"half - quarter", chance):
    failed.append("chance still ramps quarter→half")
if re.search(r"ConfidenceThreshold|competence", chance):
    failed.append("chance still remaps at threshold 50")


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def far(blend_v):
    return max(25.0, min(100.0, 100.0 - blend_v * 60.0 / 100.0))


def throw_blend(strength, dexterity, explosives):
    return round((strength + dexterity * 2 + explosives * 2) / 5.0)


def chance_at(dist, full_tiles, blend_v):
    t = dist / float(full_tiles)
    return smoothstep(t) * far(blend_v)


elite = throw_blend(100, 100, 100)
mid = throw_blend(50, 50, 50)
strong_clumsy = throw_blend(100, 30, 30)
weak_skilled = throw_blend(30, 100, 100)
if elite != 100:
    failed.append(f"elite blend {elite}")
if mid != 50:
    failed.append(f"mid blend {mid}")
if not (strong_clumsy < mid < weak_skilled):
    failed.append(f"stat order {strong_clumsy}/{mid}/{weak_skilled}")

c_elite_mid = chance_at(12.5, 25, elite)
c_elite_max = chance_at(25, 25, elite)
c_avg_mid = chance_at(12.5, 25, mid)
c20 = chance_at(5, 25, mid)
c26 = chance_at(6.5, 25, mid)

if c_elite_mid >= 30:
    failed.append(f"elite mid too high ({c_elite_mid:.1f})")
if c_elite_max >= 50:
    failed.append(f"elite max too high ({c_elite_max:.1f})")
if c_avg_mid <= c_elite_mid:
    failed.append("Dex/Expl do not change mid chance")
if abs(c26 - c20) >= 12:
    failed.append(f"sharp step near ¼ ({c20:.1f}→{c26:.1f})")

if failed:
    print("FAIL grenade mishap curve:", ", ".join(failed))
    sys.exit(1)
print(
    f"OK grenade mishap curve "
    f"(elite mid={c_elite_mid:.0f}% max={c_elite_max:.0f}%; "
    f"avg mid={c_avg_mid:.0f}%; blend 100/50/clumsy/skilled="
    f"{elite}/{mid}/{strong_clumsy}/{weak_skilled})"
)
sys.exit(0)
