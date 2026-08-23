# Static smoke for JAZZ-STRATEGY-026 tier money / T2 money+people pulses.
# Run from jazz/: python docs/tools/_check_strategy026_tier_convoys.py

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def must(cond: bool, msg: str, fails: list[str]) -> None:
    if not cond:
        fails.append(msg)


def extract_fn(src: str, name: str) -> str:
    start = -1
    for prefix in (f"local function {name}(", f"function {name}("):
        start = src.find(prefix)
        if start >= 0:
            break
    if start < 0:
        return ""
    nxt = re.search(r"\n(?:local )?function ", src[start + 1 :])
    if not nxt:
        return src[start:]
    return src[start : start + 1 + nxt.start()]


def main() -> int:
    fails: list[str] = []
    tier = read(ROOT / "Code" / "LegionTierProgression.lua")
    ai = read(ROOT / "Code" / "Guardpost_Patrols.lua")

    must(
        'Msg("JAZZ_LegionTierRaised", current, computed)' in tier,
        "lApplyTierRaise missing Msg(JAZZ_LegionTierRaised, old, new)",
        fails,
    )
    apply = extract_fn(tier, "lApplyTierRaise")
    must("JAZZ_RIS_OnTierRaised" in apply, "Msg should stay after RIS hook", fails)
    ris_at = apply.find("JAZZ_RIS_OnTierRaised")
    msg_at = apply.find("JAZZ_LegionTierRaised")
    must(ris_at >= 0 and msg_at > ris_at, "Msg must follow JAZZ_RIS_OnTierRaised", fails)
    must("computed <= current" in apply, "raise still gated on computed > current", fails)

    spawn = extract_fn(ai, "lSpawnManaged")
    must("skip_global_spawn" in spawn, "lSpawnManaged missing skip_global_spawn", fails)
    must("lConsumeGlobalSpawn(root)" in spawn, "regular spawn still consumes pool", fails)
    must(
        "if not opts.skip_global_spawn then" in spawn
        and "lConsumeGlobalSpawn(root)" in spawn,
        "consume must be gated by skip_global_spawn",
        fails,
    )

    must("function JAZZ_LegionAIOnTierRaised" in ai, "public OnTierRaised missing", fails)
    must("function OnMsg.JAZZ_LegionTierRaised" in ai, "OnMsg listener missing", fails)
    must("old_tier < 21 and new_tier >= 21" in ai, "T2 crossing gate missing", fails)
    must("lPulseSpawnSupply" in ai and "lPulseSpawnManpower" in ai, "pulse helpers missing", fails)
    must("lCollectLivingOutposts" in ai, "living outpost collector missing", fails)
    must("lPickPulseSupplyTarget" in ai, "priority target pick missing", fails)
    must("{ skip_global_spawn = true }" in ai, "pulse spawn must skip daily pool", fails)

    handler = extract_fn(ai, "JAZZ_LegionAIOnTierRaised")
    must("lPulseSpawnSupply" in handler and "lPulseSpawnManpower" in handler, "handler missing both pulses", fails)
    must("lPickPulseSupplyTarget" in handler, "non-T2 path missing priority pick", fails)
    # T2 path must call both per outpost; non-T2 only supply.
    t2_block = handler[handler.find("crossed_t2") :] if "crossed_t2" in handler else ""
    must("lPulseSpawnManpower" in t2_block, "T2 block must send manpower", fails)

    for name in ("lPulseSpawnSupply", "lPulseSpawnManpower"):
        body = extract_fn(ai, name)
        must(body, f"{name} not found", fails)
        must("skip_global_spawn" in body, f"{name} must skip daily pool", fails)
        must("root.major.money =" not in body, f"{name} must not deduct major.money", fails)
        must("root.major.manpower =" not in body, f"{name} must not deduct major.manpower", fails)

    travel = extract_fn(ai, "lPulseDispatchTravel")
    must("lSetRoute" in travel, "pulse travel must try lSetRoute", fails)
    must('phase = "loading"' in travel, "no-path hold must reuse loading tick", fails)
    must("hold_until = lNow()" in travel, "no-path hold_until must be now (skip 12h)", fails)

    living = extract_fn(ai, "lOutpostIsLivingUncaptured")
    must("JAZZ_IsLegionSide" in living, "living gate missing Legion Side", fails)
    must('owner_faction ~= "legion"' in living, "living gate missing owner_faction", fails)
    must("hq_sector" in living, "living gate must skip Major HQ", fails)

    tech = read(ROOT / "docs" / "technical" / "systems" / "strategy-squads-sectors.md")
    must("STRATEGY-026" in tech or "JAZZ-STRATEGY-026" in tech, "technical missing 026", fails)
    must("skip_global_spawn" in tech, "technical missing skip_global_spawn", fails)

    wiki = read(ROOT / "docs" / "wiki" / "legion-global-ai.md")
    must("подтира" in wiki and "денежный конвой" in wiki, "wiki missing sub-tier money pulse", fails)
    must("каждый живой незахваченный" in wiki, "wiki missing T2 all-outpost pulse", fails)
    must("вне" in wiki and "суточн" in wiki, "wiki missing daily-cap exception", fails)

    ru = read(ROOT / "docs" / "showcase" / "ru" / "legion-strategy.md")
    en = read(ROOT / "docs" / "showcase" / "en" / "legion-strategy.md")
    must("подтира" in ru and "тир **II**" in ru, "showcase RU missing pulse wording", fails)
    must("sub-tier" in en and "tier **II**" in en, "showcase EN missing pulse wording", fails)

    if fails:
        print("FAIL STRATEGY-026 static:")
        for item in fails:
            print(" -", item)
        return 1
    print("OK STRATEGY-026 static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
