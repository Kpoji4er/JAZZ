# UNITS-006 batch 6 notes (§D Benny / Simon)

## Shipped

| Id | Deliverable |
| --- | --- |
| `Jazz_Perk_Benny` | CE «Вам посылка» + loc RU/EN (`9920/9921`) + helpers `Jazz_BennyDecoyReady` / `Jazz_BennyPickLureTarget` |
| `Jazz_Perk_Simon` | CE «Абсолютный снайпер» + loc (`9922/9923`) + optic≥4× helpers + CD clear on kill |
| UnitData | `Jazz_Benny` / `Jazz_Simon` StartingPerks prepend named perk (jazz-units companion + items) |

## Soft cuts

- Full CombatAction decoy lure (explosion on arrival AI path)
- Full CombatAction perfect shot (forced hit / no scatter) — helpers only
- Personal perk PNG icons (temporary `DesignerExplosives` / `HawksEye` UI icons)

## Tools

- `docs/tools/_gen_units006_batch5.py` (also emits §D CEs)
- `docs/tools/_units006_batch6_startingperks.py`
- Runtime: `Code/System_NamedPerks_006_Batch6.lua`
