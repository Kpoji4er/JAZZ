# -*- coding: utf-8 -*-
"""Redistribute AIM/Merc/AME hire medicine loot by Medical / Doctor / Tier.

Rules (owner 2026-08-10 + Med<20 clarification):
- Medical < 20: bandages only (no kits, no morphine).
- AIM/Merc kits by usable Medical (>=30/50/80); cascade down leaf tiers;
  Doctor always >= Small on every leaf.
- Non-Doctor AIM/Merc: kits only if Medical > 30; not every preset.
- AME: Small kits only (Doctor or Medical >= 30).
- Bandages: everyone 1–2 floor; scale with Medical up to 10; Doctors up to 30
  spread across leaves (± full / half stacks).
- Morphine: Tier=Veteran get 1 (if Medical >= 20); Doctors up to 10 spread.
- Preserves Meds / JAZZ_SurgicalKit; only rewrites Bandage/Morphine/kits.

Idempotent. Scope: hireable IsMercenary Equipment leaves in jazz-units/items.lua.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

UNITS_ITEMS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
UNITDATA = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\UnitData")

MED_ITEMS = ("JAZZ_Bandage", "JAZZ_Morphine", "FirstAidKit", "Medkit", "Reanimationsset")
KIT_FULL = {"FirstAidKit": 5, "Medkit": 10, "Reanimationsset": 15}
KIT_RANK = {"FirstAidKit": 1, "Medkit": 2, "Reanimationsset": 3}
RANK_KIT = {1: "FirstAidKit", 2: "Medkit", 3: "Reanimationsset"}
TIER_ORDER = (50, 35, 25, 20, 10)


@dataclass
class Merc:
    unit_id: str
    medical: int
    specialization: str
    tier: str
    ame_role: str
    equipment: str

    @property
    def is_medic(self) -> bool:
        return self.specialization == "Doctor" or self.ame_role == "Medic"

    @property
    def is_ame(self) -> bool:
        return self.unit_id.startswith("JAZZ_AME_")

    @property
    def is_veteran(self) -> bool:
        return self.tier == "Veteran"


@dataclass
class LeafPlan:
    loot_id: str
    bandage: int = 0
    morphine: int = 0
    kit: str | None = None
    notes: list[str] = field(default_factory=list)


def load_mercs() -> list[Merc]:
    out: list[Merc] = []
    for p in sorted(UNITDATA.glob("*.lua")):
        t = p.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"IsMercenary\s*=\s*true", t):
            continue
        mid = re.search(r"DefineClass\.([\w]+)\s*=", t)
        uid = mid.group(1) if mid else p.stem
        med_m = re.search(r"Medical\s*=\s*(\d+)", t)
        if not med_m:
            continue
        spec_m = re.search(r'Specialization\s*=\s*"([^"]+)"', t)
        tier_m = re.search(r'Tier\s*=\s*"([^"]+)"', t)
        ame_m = re.search(r'AMERole\s*=\s*"([^"]+)"', t)
        eq_m = re.search(r'Equipment\s*=\s*\{\s*"([^"]+)"', t)
        out.append(
            Merc(
                unit_id=uid,
                medical=int(med_m.group(1)),
                specialization=spec_m.group(1) if spec_m else "",
                tier=tier_m.group(1) if tier_m else "",
                ame_role=ame_m.group(1) if ame_m else "",
                equipment=eq_m.group(1) if eq_m else "",
            )
        )
    return out


def extract_loot_blocks(text: str) -> dict[str, tuple[int, int, str]]:
    """loot_id -> (start, end, block) for ModItemLootDef."""
    results: dict[str, tuple[int, int, str]] = {}
    for m in re.finditer(r"PlaceObj\('ModItemLootDef',\s*\{", text):
        start = m.start()
        i = text.find("{", start)
        depth = 0
        end = None
        for j in range(i, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    if end < len(text) and text[end] == ")":
                        end += 1
                    if end < len(text) and text[end] == ",":
                        end += 1
                    break
        if end is None:
            continue
        block = text[start:end]
        idm = re.search(r"\bid\s*=\s*\"([^\"]+)\"", block)
        if not idm:
            continue
        results[idm.group(1)] = (start, end, block)
    return results


def parent_children(block: str) -> list[str]:
    return re.findall(r'loot_def\s*=\s*"([^"]+)"', block)


def leaf_tier(loot_id: str) -> int | None:
    m2 = re.search(r"(10|20|25|35|50)$", loot_id)
    if m2:
        return int(m2.group(1))
    return None


def is_hire_gear_leaf(loot_id: str, block: str) -> bool:
    """Hire kit leaves under a merc Equipment tree (Mercs/Ernie/…); skip weapon packs."""
    if re.search(r"AssaultRifles_|_Mag_|AmmoPack|WeaponParts", loot_id):
        return False
    if loot_id.startswith("Loot_JAZZ_AME_"):
        return True
    if leaf_tier(loot_id) is not None:
        return True
    # Single-leaf / hybrid oddballs (Flay, Smiley, Larry, Spike, Pierre…)
    if "LootEntryInventoryItem" in block:
        return True
    return False


def resolve_leaves(eq: str, loots: dict[str, tuple[int, int, str]]) -> list[str]:
    if not eq or eq not in loots:
        return []
    _, _, block = loots[eq]
    results: list[str] = []
    # Hybrid parents (Spike/Pierre) may carry medicine on the parent itself
    if "LootEntryInventoryItem" in block and is_hire_gear_leaf(eq, block):
        results.append(eq)
    for k in parent_children(block):
        if k not in loots or k == eq:
            continue
        _, _, kb = loots[k]
        if is_hire_gear_leaf(k, kb):
            results.append(k)

    def key(lid: str):
        t = leaf_tier(lid)
        # parents without tier sort after numbered leaves? Prefer numbered first (desc), then bare
        return (0 if t is not None else 1, -(t or 0), lid)

    # unique preserve sort
    return sorted(set(results), key=key)


def is_canonical_equipment_owner(unit_id: str, equipment: str) -> bool:
    """True when Equipment id matches this unit's own loot tree name."""
    if not equipment:
        return False
    if equipment == unit_id:
        return True
    if equipment == f"Loot_{unit_id}":
        return True
    # Jazz_Laura → Loot_JAZZ_Laura
    if unit_id.startswith("Jazz_"):
        nick = unit_id[len("Jazz_") :]
        if equipment == f"Loot_JAZZ_{nick}":
            return True
    if unit_id.startswith("JAZZ_AME_") and equipment == f"Loot_{unit_id}":
        return True
    return False


def pick_equipment_owner(owners: list[Merc]) -> Merc | None:
    """Prefer name-matched owner; else sole consumer; else best Medical/medic."""
    if not owners:
        return None
    for m in owners:
        if is_canonical_equipment_owner(m.unit_id, m.equipment):
            return m
    if len(owners) == 1:
        return owners[0]
    return max(owners, key=lambda m: (m.is_medic, m.medical, m.is_veteran, m.unit_id))


def bandage_total(med: int, is_medic: bool) -> int:
    if is_medic:
        return 30  # MaxStacks, spread across leaves
    if med < 10:
        return 1
    if med < 20:
        return 2
    # 20 → 2, 50 → 10
    return min(10, 2 + round((med - 20) * 8 / 30))


def morphine_total(merc: Merc) -> int:
    if merc.medical < 20:
        return 0
    if merc.is_medic:
        return 10
    if merc.is_veteran:
        return 1
    return 0


def best_kit_rank(merc: Merc) -> int:
    """0 = none. Non-medic needs Medical > 30. Medic always >=1 if med>=20 else 0."""
    med = merc.medical
    if med < 20:
        return 0
    if merc.is_ame:
        if merc.is_medic or med >= 30:
            return 1  # Small only
        return 0
    if med >= 80:
        return 3
    if med >= 50:
        return 2
    if merc.is_medic:
        return 1  # always Small
    if med > 30:
        return 1
    return 0


def kit_for_leaf(merc: Merc, leaf_index: int, n_leaves: int, best: int) -> str | None:
    if best <= 0:
        return None
    if merc.is_ame:
        return "FirstAidKit" if best >= 1 else None
    if merc.is_medic:
        # every leaf >= Small; cascade down from best
        rank = max(1, best - leaf_index)
        return RANK_KIT[rank]
    # non-medic: not every preset
    if best == 1:
        return "FirstAidKit" if leaf_index == 0 else None
    if best == 2:
        if leaf_index == 0:
            return "Medkit"
        if leaf_index == 1:
            return "FirstAidKit"
        return None
    # best == 3
    if leaf_index == 0:
        return "Reanimationsset"
    if leaf_index == 1:
        return "Medkit"
    if leaf_index == 2:
        return "FirstAidKit"
    return None


def spread_amounts(total: int, n: int, prefer_high: bool = True) -> list[int]:
    """Spread total across n leaves; prefer higher tiers. Allow 0 on lower leaves."""
    if n <= 0 or total <= 0:
        return [0] * max(n, 0)
    amounts = [0] * n
    # Prefer chunk sizes: half/full-ish of remaining / slots
    remaining = total
    for i in range(n):
        slots_left = n - i
        if remaining <= 0:
            break
        if prefer_high and i == 0 and n > 1:
            # put about half on top leaf, capped reasonably
            chunk = max(1, min(remaining - (slots_left - 1), (remaining + 1) // 2))
        else:
            chunk = max(0, (remaining + slots_left - 1) // slots_left)
            if chunk == 0 and remaining > 0:
                chunk = remaining
        amounts[i] = chunk
        remaining -= chunk
    # dump leftover on first
    if remaining > 0:
        amounts[0] += remaining
    return amounts


def entry_line(indent: str, item: str, stack: int) -> str:
    if stack <= 1 and item == "JAZZ_Morphine":
        return f"{indent}PlaceObj('LootEntryInventoryItem', {{ item = \"{item}\", stack_min = 1, stack_max = 1 }}),"
    return (
        f"{indent}PlaceObj('LootEntryInventoryItem', "
        f'{{ item = "{item}", stack_min = {stack}, stack_max = {stack} }}),'
    )


def kit_entry_line(indent: str, kit: str) -> str:
    stack = KIT_FULL[kit]
    return (
        f"{indent}PlaceObj('LootEntryInventoryItem', "
        f'{{ item = "{kit}", stack_min = {stack}, stack_max = {stack} }}),'
    )


def iter_loot_entry_spans(block: str) -> list[tuple[int, int, str]]:
    """Return (start, end, inner) for each LootEntryInventoryItem in block."""
    spans: list[tuple[int, int, str]] = []
    for m in re.finditer(r"PlaceObj\('LootEntryInventoryItem',\s*\{", block):
        start = m.start()
        i = block.find("{", m.start())
        depth = 0
        for j in range(i, len(block)):
            if block[j] == "{":
                depth += 1
            elif block[j] == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    if end < len(block) and block[end] == ")":
                        end += 1
                    if end < len(block) and block[end] == ",":
                        end += 1
                    # include leading indent/newline for clean removal
                    line_start = start
                    while line_start > 0 and block[line_start - 1] in " \t":
                        line_start -= 1
                    if line_start > 0 and block[line_start - 1] == "\n":
                        line_start -= 1
                    spans.append((line_start, end, block[i + 1 : j]))
                    break
    return spans


def strip_med_entries(block: str) -> tuple[str, str]:
    """Remove Bandage/Morphine/kit entries; return (new_block, indent)."""
    indent = "\t\t\t\t\t"
    for line in block.splitlines():
        m = re.match(r"^(\t+)PlaceObj\('LootEntry", line)
        if m:
            indent = m.group(1)
            break

    remove: list[tuple[int, int]] = []
    for start, end, inner in iter_loot_entry_spans(block):
        im = re.search(r'item\s*=\s*"([^"]+)"', inner)
        if im and im.group(1) in MED_ITEMS:
            remove.append((start, end))
    if not remove:
        return block, indent
    parts: list[str] = []
    last = 0
    for start, end in remove:
        parts.append(block[last:start])
        last = end
    parts.append(block[last:])
    cleaned = "".join(parts)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned, indent


def insert_med_entries(block: str, indent: str, lines: list[str]) -> str:
    if not lines:
        return block
    payload = "\n".join(lines) + "\n"
    # Prefer after Meds / SurgicalKit if present; else before closing of ModItemLootDef
    for key in ("JAZZ_SurgicalKit", "Meds"):
        idx = block.find(f'item = "{key}"')
        if idx < 0:
            continue
        end_entry = block.find("}),", idx)
        if end_entry >= 0:
            pos = end_entry + 3
            return block[:pos] + "\n" + payload + block[pos:]
    # insert before final closing `})` / `}),` of the loot def body
    # find last PlaceObj entry end, or after id line
    m = re.search(r"(\n)([ \t]*\}\)?,?\s*)$", block)
    if m:
        return block[: m.start(1) + 1] + payload + block[m.start(2) :]
    # fallback: before last }
    last = block.rfind("}")
    return block[:last] + payload + block[last:]


def plan_merc(merc: Merc, leaves: list[str]) -> dict[str, LeafPlan]:
    plans: dict[str, LeafPlan] = {lid: LeafPlan(loot_id=lid) for lid in leaves}
    n = len(leaves)
    if n == 0:
        return plans

    band_total = bandage_total(merc.medical, merc.is_medic)
    morph_total = morphine_total(merc)
    best = best_kit_rank(merc)

    band_spread = spread_amounts(band_total, n, prefer_high=True)
    # Morphine: medics spread; veterans put 1 on highest leaf only
    if merc.is_medic and morph_total > 0:
        morph_spread = spread_amounts(morph_total, n, prefer_high=True)
    elif morph_total > 0:
        morph_spread = [0] * n
        morph_spread[0] = morph_total
    else:
        morph_spread = [0] * n

    for i, lid in enumerate(leaves):
        plans[lid].bandage = band_spread[i]
        plans[lid].morphine = morph_spread[i]
        plans[lid].kit = kit_for_leaf(merc, i, n, best)
        if merc.medical < 20:
            plans[lid].notes.append("med<20:bandages-only")
    return plans


def apply_plan_to_block(block: str, plan: LeafPlan) -> str:
    cleaned, indent = strip_med_entries(block)
    lines: list[str] = []
    if plan.bandage > 0:
        lines.append(entry_line(indent, "JAZZ_Bandage", plan.bandage))
    if plan.morphine > 0:
        lines.append(entry_line(indent, "JAZZ_Morphine", plan.morphine))
    if plan.kit:
        lines.append(kit_entry_line(indent, plan.kit))
    return insert_med_entries(cleaned, indent, lines)


def main() -> int:
    dry = "--dry" in sys.argv
    mercs = load_mercs()
    text = UNITS_ITEMS.read_text(encoding="utf-8")
    loots = extract_loot_blocks(text)

    # Only rewrite leaves that belong to hireable merc Equipment trees
    leaf_plans: dict[str, LeafPlan] = {}
    skipped: list[str] = []
    from collections import defaultdict

    by_eq: dict[str, list[Merc]] = defaultdict(list)
    for merc in mercs:
        if not merc.equipment:
            skipped.append(f"{merc.unit_id}: no Equipment")
            continue
        by_eq[merc.equipment].append(merc)

    for eq, owners in sorted(by_eq.items()):
        primary = pick_equipment_owner(owners)
        if primary is None:
            continue
        for m in owners:
            if m.unit_id != primary.unit_id:
                skipped.append(
                    f"{m.unit_id}: shares Equipment {eq} (owner {primary.unit_id})"
                )
        leaves = resolve_leaves(eq, loots)
        if not leaves:
            skipped.append(f"{primary.unit_id}: Equipment {eq} missing")
            continue
        for lid, plan in plan_merc(primary, leaves).items():
            leaf_plans[lid] = plan

    # Apply by replacing blocks from end to start so offsets stay valid
    replacements: list[tuple[int, int, str]] = []
    for lid, plan in leaf_plans.items():
        if lid not in loots:
            continue
        start, end, block = loots[lid]
        # Skip pure parents (only LootEntryLootDef, no inventory) — should not be in leaf_plans
        if "LootEntryLootDef" in block and "LootEntryInventoryItem" not in block and parent_children(block):
            continue
        new_block = apply_plan_to_block(block, plan)
        if new_block != block:
            replacements.append((start, end, new_block))

    replacements.sort(key=lambda x: x[0], reverse=True)
    new_text = text
    for start, end, new_block in replacements:
        new_text = new_text[:start] + new_block + new_text[end:]

    stats = {
        "mercs": len(mercs),
        "leaves": len(leaf_plans),
        "rewritten": len(replacements),
        "med_lt20": sum(1 for m in mercs if m.medical < 20),
        "medics": sum(1 for m in mercs if m.is_medic),
        "with_kit": sum(1 for p in leaf_plans.values() if p.kit),
        "with_morphine": sum(1 for p in leaf_plans.values() if p.morphine > 0),
        "skipped": len(skipped),
    }

    report_lines = [
        f"mercs={stats['mercs']} leaves={stats['leaves']} rewritten={stats['rewritten']} "
        f"med<20={stats['med_lt20']} medics={stats['medics']} "
        f"leaves_with_kit={stats['with_kit']} leaves_with_morphine={stats['with_morphine']} "
        f"skipped={stats['skipped']}"
    ]
    for s in skipped[:30]:
        report_lines.append(f"  skip: {s}")
    # sample plans
    for sample in ("MD50", "MD10", "Fidel50", "Ice50", "JAZZ_Laura50", "JAZZ_Laura20", "Loot_JAZZ_AME_01", "Loot_JAZZ_AME_49"):
        p = leaf_plans.get(sample)
        if p:
            report_lines.append(
                f"  plan {sample}: bandage={p.bandage} morphine={p.morphine} kit={p.kit}"
            )

    print("\n".join(report_lines))

    if dry:
        print("DRY RUN — no write")
        # show a few rewritten blocks from new_text
        for sample in ("MD50", "Fidel50", "Ice50", "Loot_JAZZ_AME_01", "Loot_JAZZ_AME_49"):
            im = re.search(rf'\bid\s*=\s*"{sample}"', new_text)
            if not im:
                continue
            start = new_text.rfind("PlaceObj('ModItemLootDef'", 0, im.start())
            i = new_text.find("{", start)
            depth = 0
            for j in range(i, len(new_text)):
                if new_text[j] == "{":
                    depth += 1
                elif new_text[j] == "}":
                    depth -= 1
                    if depth == 0:
                        end = j + 1
                        if end < len(new_text) and new_text[end] == ")":
                            end += 1
                        print(f"---- rewritten {sample} ----")
                        for line in new_text[start:end].splitlines():
                            if any(
                                k in line
                                for k in (
                                    "Bandage",
                                    "Morphine",
                                    "FirstAid",
                                    "Medkit",
                                    "Reanim",
                                    "Meds",
                                    "Surgical",
                                    "id =",
                                )
                            ):
                                print(line)
                        break
        return 0

    UNITS_ITEMS.write_text(new_text, encoding="utf-8")
    print(f"wrote {UNITS_ITEMS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
