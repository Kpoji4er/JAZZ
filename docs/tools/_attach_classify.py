# -*- coding: utf-8 -*-
"""Classify weapon components: leftover optics vs entity/visual vs shared/JAZZ."""
from __future__ import annotations

# Vanilla optic packages JAZZ replaced with JAZZ_*/Jazz_* lines.
# These are gameplay Scope options — not iron/entity wrappers.
VANILLA_OPTIC_LEFTOVERS = frozenset(
    {
        "ReflexSight",
        "ReflexSightAdvanced",
        "ReflexSightAdvanced_Glock",
        "LROptics",
        "LROpticsAdvanced",
        "LROptics_DragunovDefault",
        "ScopeCOG",
        "ScopeCOGQuick",
        "ThermalScope",
        "AdvancedHOLO",
        "AnotherOptic",
        "CollimatorMP7",
        "PSG_DefaultScope",
        "GewehrDefaultSight",
    }
)

IRON_ID_HINTS = ("Ironsight", "IronSight", "Irons")


def is_jazz_id(cid: str) -> bool:
    return cid.startswith("JAZZ_") or cid.startswith("Jazz_")


def is_iron_or_default_sight(cid: str) -> bool:
    if any(h in cid for h in IRON_ID_HINTS):
        return True
    # Integrated default optic mesh (AUG etc.) — Visuals/Entity, not leftover package
    if cid.endswith("Scope_Default") or cid.endswith("ScopeDefault"):
        return True
    # Anaconda-specific Scope-slot dots / flash — ApplyTo visuals, not generic optic ladder
    if cid.endswith("_Anaconda"):
        return True
    return False


def classify_component(cid: str, slot: str, effects: list[str] | None = None) -> list[str]:
    """Return zero or more catalog flags for a component id."""
    flags: list[str] = []
    slot_l = (slot or "").strip().lower()
    fx = [e for e in (effects or []) if e]
    jazz = is_jazz_id(cid)

    if cid in VANILLA_OPTIC_LEFTOVERS:
        flags.append("leftover_optic")
        return flags

    if is_iron_or_default_sight(cid):
        flags.append("entity_visual")
        return flags

    # Jazz iron lines are entity defaults with optional minor effects
    if jazz and ("IronSight" in cid or "G36Sight" in cid):
        flags.append("entity_visual")
        return flags

    # Empty Scope without jazz prefix and not already classified — treat as entity if named like sight
    if slot_l == "scope" and not jazz and not fx:
        if any(x in cid.lower() for x in ("sight", "scope", "optic", "holo", "collim")):
            # Unknown empty scope-ish id: entity-ish, not leftover ladder
            flags.append("entity_visual")
            return flags

    if slot_l == "scope" and not jazz and fx:
        # Gameplay scope that isn't in the known leftover set and isn't JAZZ_
        # (e.g. weapon-specific) — mark for review but not as leftover_optic
        flags.append("nonjazz_scope")

    return flags
