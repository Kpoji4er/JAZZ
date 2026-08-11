# UNITS-006 audit follow-up (2026-08-09)

Static audit vs Mechanics / §A / §C CHANGE after batches 1–4.

## Fixed in this push

| Gap | Fix |
| --- | --- |
| Mike PinDown +2 | `BeginTurn` PinDown loop fires +2 extra `ProvokeOpportunityAttack_Pindown` |
| Vince −25% | Keep EV 25% skip for amount=1; scale amount>1 ×75% |
| BuildingConfidence heal | `OnCalcHealAmount` + `Unit:CalcHealAmount` wrap: ±10% × (MD level − patient level), cap ±50% |

## Fixed later (same day)

| Gap | Fix |
| --- | --- |
| Nervous stack | CE: `Jazz_NervousConsumeBonus` then `Jazz_NervousAddHitStack(hits)`; Apply peek-only + idempotent cache (Execute→GetActionResults); cap via `stack_cap` |

## Still PARTIAL / deferred

| Id | Note |
| --- | --- |
| Mike reactions always | Soft — no clear interrupt fail-roll hook; text kept |
| Blade Brutalize | Damage replay, not full chain fidelity |
| Ice shot-list | Text only |
| MakeThemBleed apply | Aura only; groin/animal apply soft |
| GloryHog / RecklessAssault | GloryHog recruit + RecklessAssault List2 wired |
| Nazdarovya / ExplodingPalm / DangerClose stim | ExplodingPalm wired; DangerClose List2 + stim immune + ExplosionPrecalc wrap |
| §B HARD leftovers | Biff economy, Livewire money op, … |
| §D Benny/Simon | CE + StartingPerks shipped; CombatAction soft-cut |

## Spec Evidence

Updated in `JAZZ-UNITS-006.md` Evidence (Nervous AC-002; AC-008 partial).
