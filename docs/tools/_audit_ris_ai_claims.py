#!/usr/bin/env python3
"""Audit Legion AI settings vs ROLE/CMD/SNIPER specs and R.I.S. dossier claims.

Mirrors JazzAI_InferRoleFamily order (Assault before Gunner) so AssaultGunner
collisions are visible. Read-only. Exit 1 on FAIL.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units"
UD = UNITS / "UnitData"
RECIPES = JAZZ / "scripts" / "legion-loadouts" / "data" / "recipes.json"
TIERS = JAZZ / "docs" / "technical" / "systems" / "legion-units-equipment-tiers.md"
STANCE = UNITS / "Code" / "AICombatStance.lua"
AURA = JAZZ / "Code" / "AIContextProfiles.lua"

sys.path.insert(0, str(JAZZ / "docs" / "tools"))
import _ris_copy_bank as bank  # noqa: E402

TECH_ARCH_RE = re.compile(
    r"\|\s*T\d\s*\|\s*`(?P<id>JAZZ_Legion_[^`]+)`\s*\|[^|]+\|[^|]+\|\s*`(?P<role>[^`]+)`\s*\|\s*`(?P<arch>[^`]+)`"
)
KW_RE = re.compile(r"AIKeywords\s*=\s*\{(?P<body>.*?)\},", re.S)
ARCH_RE = re.compile(r'^\tarchetype = "([^"]+)"', re.M)
REPOS_RE = re.compile(r'^\tRepositionArchetype = "([^"]+)"', re.M)
ROLE_RE = re.compile(r'^\trole = "([^"]+)"', re.M)
PERK_RE = re.compile(r"StartingPerks\s*=\s*\{(?P<body>.*?)\},", re.S)
PICK_RE = re.compile(r"PickCustomArchetype\s*=\s*function")
MEDIC_RE = re.compile(r"allow_medic\s*=\s*true")
STR_RE = re.compile(r'"([^"]+)"')

CARRIES_SMOKE = re.compile(
    r"\b(?:carry|carries|also (?:carry|bring)|covering the move with|some also carry)\b.*\bsmoke\b|"
    r"\bsmoke (?:grenades?|or a knife|or firebombs)\b",
    re.I,
)
PLAYER_SMOKE = re.compile(r"\b(?:use|with|under) smoke\b|\bblock.{0,20}smoke\b|\bscreen.{0,20}smoke\b", re.I)
KNIFE = re.compile(r"\bknife\b|\bmachete\b", re.I)
ORDERS = re.compile(r"\borders\b|focus(?:ing)? their fire|push nearby|hold them in place", re.I)
SNIPER_COPY = re.compile(r"scoped rifles?|pinning an exposed|long-range fire", re.I)
SLIP_AWAY = re.compile(r"slipping away|shift(?:ing)? between flanking", re.I)
HOLD_LANE = re.compile(r"hold (?:cover|useful ground|it)|wait for (?:a clean|an exposed)|firing lane and hold", re.I)


def parse_ud(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    kws = STR_RE.findall(KW_RE.search(text).group("body")) if KW_RE.search(text) else []
    perks = STR_RE.findall(PERK_RE.search(text).group("body")) if PERK_RE.search(text) else []
    return {
        "id": path.stem,
        "keywords": kws,
        "archetype": (ARCH_RE.search(text) or [None, None])[1],
        "reposition": (REPOS_RE.search(text) or [None, None])[1],
        "role": (ROLE_RE.search(text) or [None, None])[1],
        "perks": perks,
        "pick": bool(PICK_RE.search(text)),
        "allow_medic": bool(MEDIC_RE.search(text)),
    }


def infer_family(uid: str) -> str:
    """Same substring order as JazzAI_InferRoleFamily."""
    if "Flanker" in uid or uid == "RebelFlanker":
        return "Scout"
    if "Assault" in uid:
        return "Pusher"
    if "Gunner" in uid or "Machinegun" in uid:
        return "MG"
    if "Heavy" in uid or "Mortar" in uid or "Rocketeer" in uid:
        return "Heavy"
    if "Leader" in uid or "Sergeant" in uid or "Lieutenant" in uid or "Captain" in uid:
        return "Leader"
    if "Bonemaker" in uid or "Medic" in uid:
        return "Medic"
    if "Recruit" in uid:
        return "Recruit"
    return "Line"


def intended_family(uid: str) -> str:
    if "Gunner" in uid:
        return "MG"
    return infer_family(uid)


def expected_archetype(uid: str) -> str:
    if "Recruit" in uid:
        return "Legion_Assaulter"
    if "Flanker" in uid:
        return "Legion_Flanker"
    if "Gunner" in uid:
        return "Legion_Machinegunner"
    if "Assault" in uid:
        return "Legion_Assaulter"
    if "LeaderT1" in uid:
        return "Legion_Assaulter"
    if "Leader" in uid:
        return "Legion_Frontliner"
    if "HeavyT1" in uid or "Rocketeer" in uid:
        return "Legion_Frontliner"
    if "Heavy" in uid:
        return "Artillery"
    return "Legion_Frontliner"


def never_melee(uid: str, kws: list[str]) -> bool:
    fam = infer_family(uid)
    if fam in ("MG", "Heavy", "Leader"):
        return True
    if "Sniper" in kws or "Ordnance" in kws:
        return "Melee" not in kws
    return False


def recipe_flags(rec: dict | None) -> dict:
    if not rec:
        return {"melee": False, "smoke": False, "molotov": False}
    melee = rec.get("melee")
    util = rec.get("utility") or {}
    smoke = any("smoke" in str(k).lower() for k in util)
    molotov = any("molotov" in str(k).lower() for k in util)
    return {"melee": bool(melee), "smoke": smoke, "molotov": molotov}


def main() -> int:
    fails: list[str] = []
    warns: list[str] = []

    units = [parse_ud(p) for p in sorted(UD.glob("JAZZ_Legion_*.lua"))]
    by_id = {u["id"]: u for u in units}
    recipes = json.loads(RECIPES.read_text(encoding="utf-8"))
    tech = {
        m.group("id"): (m.group("role"), m.group("arch"))
        for m in TECH_ARCH_RE.finditer(TIERS.read_text(encoding="utf-8"))
    }
    stance = STANCE.read_text(encoding="utf-8")
    aura = AURA.read_text(encoding="utf-8")

    print(f"unitdata={len(units)} dossiers={len(bank.DOSSIERS)} recipes={len(recipes)}")

    if set(bank.DOSSIERS) != set(by_id):
        fails.append(
            f"dossier/UnitData set mismatch missing={sorted(set(bank.DOSSIERS) - set(by_id))} "
            f"extra={sorted(set(by_id) - set(bank.DOSSIERS))}"
        )

    for u in units:
        uid = u["id"]
        inferred = infer_family(uid)
        intended = intended_family(uid)
        if inferred != intended:
            fails.append(
                f"{uid}: JazzAI_InferRoleFamily sees {inferred} (substring Assault before Gunner), "
                f"intended {intended}. PickCombatStance will not keep Machinegunner."
            )
        exp = expected_archetype(uid)
        if u["archetype"] != exp:
            if not u["archetype"] and uid.endswith("Rocketeer"):
                warns.append(
                    f"{uid}: companion/items omit archetype; ResolveKnownArchetype(nil) "
                    f"falls through to {exp}"
                )
            else:
                fails.append(f"{uid}: archetype={u['archetype']!r} expected {exp!r}")
        if uid in tech:
            role, arch = tech[uid]
            if u["role"] != role:
                warns.append(f"{uid}: role={u['role']!r} technical={role!r}")
            if u["archetype"] and u["archetype"] != arch:
                fails.append(f"{uid}: archetype={u['archetype']!r} technical={arch!r}")
        if not u["pick"]:
            fails.append(f"{uid}: PickCustom does not call JazzAI_PickCombatStance")
        if uid.endswith("Bonemaker") and not u["allow_medic"]:
            fails.append(f"{uid}: missing allow_medic=true")
        if "Flanker" in uid and u["reposition"] not in (None, "Legion_Flanker"):
            fails.append(f"{uid}: RepositionArchetype={u['reposition']!r}")

    if "function JazzAI_PickCombatStance" not in stance:
        fails.append("JazzAI_PickCombatStance missing")
    if "want_push and is_pusher" in stance:
        warns.append(
            "ROLE-002-REQ-002: Scout NeedPush->Assaulter is gated by aura is_pusher, "
            "not every Flanker on NeedPush"
        )
    if "return 15" not in aura or "return 25" not in aura or "return 1000" not in aura:
        fails.append("CMD-001 aura radii 15/25/1000 not found")

    print("\n== RIS combat claims vs UnitData / recipe / loaded AI ==")
    for uid, copy in bank.DOSSIERS.items():
        u = by_id.get(uid)
        if not u:
            continue
        rec = recipe_flags(recipes.get(uid))
        body = copy["body_en"]
        kws = u["keywords"]
        notes = []

        if KNIFE.search(body):
            if never_melee(uid, kws) and rec["melee"]:
                fails.append(
                    f"RIS {uid}: knife/machete in copy and recipe, but InferRoleFamily/"
                    f"keywords make NeverMelee (AI will not switch)"
                )
                notes.append("KNIFE-NEVER")
            elif inferred := infer_family(uid):
                if inferred == "Pusher" and intended_family(uid) == "MG" and rec["melee"]:
                    warns.append(
                        f"RIS {uid}: machete copy matches accidental Pusher melee, not MG NeverMelee"
                    )
                    notes.append("KNIFE-VIA-BUG")
                elif not rec["melee"] and "Melee" not in kws:
                    warns.append(f"RIS {uid}: knife/machete copy, no recipe melee / Melee kw")
                    notes.append("KNIFE-GEAR")

        if CARRIES_SMOKE.search(body) and not rec["smoke"] and "Smoke" not in kws:
            warns.append(f"RIS {uid}: unit-carries-smoke copy, no smoke utility / Smoke kw")
            notes.append("SMOKE-GEAR")

        if "Heal" in body or "bleeding" in body.lower() or "medic" in body.lower():
            if uid.endswith("Bonemaker"):
                if "Heal" not in kws or not u["allow_medic"]:
                    fails.append(f"RIS {uid}: medic copy but Heal/allow_medic missing")

        if ORDERS.search(body) and "Leader" not in kws:
            fails.append(f"RIS {uid}: officer-orders copy but no Leader keyword")

        if SNIPER_COPY.search(body) and uid.endswith("Sniper") and "Sniper" not in kws:
            fails.append(f"RIS {uid}: sniper copy but no Sniper keyword")

        hold_kw = "Sniper" in kws or "Marksman" in kws
        if SLIP_AWAY.search(body) and hold_kw:
            warns.append(
                f"RIS {uid}: mobile/slip-away copy, but Sniper/Marksman keyword triggers "
                "SNIPER-001 stay-hold when a shot exists"
            )
            notes.append("HOLD-VS-SLIP")
        if HOLD_LANE.search(body) and hold_kw:
            notes.append("hold-ok")

        print(
            f"{uid:<42} fam={infer_family(uid):<8}->{intended_family(uid):<8} "
            f"{u['archetype'] or '-':<22} kws={','.join(kws):<40} "
            f"{','.join(notes) or '-'}"
        )

    print("\n== FAIL ==")
    for line in fails:
        print("FAIL", line)
    print("\n== WARN ==")
    for line in warns:
        print("WARN", line)
    print(f"\nsummary fails={len(fails)} warns={len(warns)}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
