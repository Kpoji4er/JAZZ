# UNITS-006 audit follow-up (2026-08-09)

Static audit vs Mechanics / §A / §C CHANGE after batches 1–4.

## Fixed in this push

| Gap | Fix |
| --- | --- |
| Mike PinDown +2 | `BeginTurn` PinDown loop fires +2 extra `ProvokeOpportunityAttack_Pindown` |
| Vince −25% | Keep EV 25% skip for amount=1; scale amount>1 ×75% |
| BuildingConfidence heal | `OnCalcHealAmount` +10%×Level cap +50% |

## Still PARTIAL / deferred

| Id | Note |
| --- | --- |
| Mike reactions always | Soft — no clear interrupt fail-roll hook; text kept |
| Blade Brutalize | Damage replay, not full chain fidelity |
| Ice shot-list | Text only |
| MakeThemBleed apply | Aura only; groin/animal apply soft |
| GloryHog / RecklessAssault / Nazdarovya / DesignerExplosives / DangerClose / ExplodingPalm / NaturalHealing | Batch 5/6 or later |
| §B HARD | Rothman/Biff/Ira/Miguel/Livewire → batch5 |
| §D Benni/Simon | batch6 |

## Spec Evidence

Updated in `JAZZ-UNITS-006.md` Evidence section for batch4 + audit fixes.
