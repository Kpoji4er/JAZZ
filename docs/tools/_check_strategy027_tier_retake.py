# Static smoke for JAZZ-STRATEGY-027 tier retakes on player-captured outposts.
# Run from jazz/: python docs/tools/_check_strategy027_tier_retake.py

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
    ai = read(ROOT / "Code" / "Guardpost_Patrols.lua")

    must("lPulseShouldRetake" in ai, "retake trigger helper missing", fails)
    must("lCollectPlayerCapturedOutposts" in ai, "captured collector missing", fails)
    must("lPulseSpawnMajorRetake" in ai, "major retake pulse missing", fails)
    must('owner_faction == "player"' in ai, "player owner stamp missing", fails)

    trig = extract_fn(ai, "lPulseShouldRetake")
    must("old_tier < 21 and new_tier >= 21" in trig, "T2 trigger missing", fails)
    must("old_tier < 23 and new_tier >= 23" in trig, "T2-3 trigger missing", fails)
    must("old_tier < 25 and new_tier >= 25" in trig, "T2-5 trigger missing", fails)

    spawn = extract_fn(ai, "lPulseSpawnMajorRetake")
    must("skip_global_spawn" in spawn, "retake must skip daily pool", fails)
    must('"major"' in spawn, "retake must spawn major/retribution", fails)
    must("next_response_time" not in spawn, "pulse must not start 72h cooldown", fails)
    must("root.major.money =" not in spawn, "pulse must not deduct major.money", fails)
    must("root.major.manpower =" not in spawn, "pulse must not deduct major.manpower", fails)

    handler = extract_fn(ai, "JAZZ_LegionAIOnTierRaised")
    must("lPulseShouldRetake" in handler, "handler missing retake gate", fails)
    must("lCollectPlayerCapturedOutposts" in handler, "handler missing captured list", fails)
    must("lPulseSpawnMajorRetake" in handler, "handler missing retake spawn", fails)
    # Logistics may log empty living list but must not return before retake.
    living_log = handler.find("no living outposts")
    retake_call = handler.find("lPulseShouldRetake")
    must(living_log < 0 or retake_call > living_log, "retake must run after empty-living log, not return early", fails)
    must("return false" not in handler[handler.find("living = lCollectLivingOutposts") : retake_call],
         "handler must not return false before retake because living is empty", fails)

    wiki = read(ROOT / "docs" / "wiki" / "legion-global-ai.md")
    must("T2-3" in wiki and "T2-5" in wiki, "wiki missing T2-3/T2-5", fails)
    must("возмезд" in wiki, "wiki missing retribution wording", fails)

    ru = read(ROOT / "docs" / "showcase" / "ru" / "legion-strategy.md")
    en = read(ROOT / "docs" / "showcase" / "en" / "legion-strategy.md")
    must("T2-3" in ru and "T2-5" in ru and "возмезд" in ru, "showcase RU missing retake wording", fails)
    must("T2-3" in en and "T2-5" in en and "retribution" in en, "showcase EN missing retake wording", fails)

    tech = read(ROOT / "docs" / "technical" / "systems" / "strategy-squads-sectors.md")
    must("STRATEGY-027" in tech or "JAZZ-STRATEGY-027" in tech, "technical missing 027", fails)

    if fails:
        print("FAIL STRATEGY-027 static:")
        for item in fails:
            print(" -", item)
        return 1
    print("OK STRATEGY-027 static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
