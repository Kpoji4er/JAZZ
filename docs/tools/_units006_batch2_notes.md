# UNITS-006 batch 2 notes (§C combat CHANGE)

Shipped in working tree / commit after this note.

## Done

| Id | Effect |
| --- | --- |
| `GruntyPerk_JAZZ` | Combat start +50% AP; later turns `10%×max(0,GetPersonalMorale())` → same buff |
| `GrizzlyPerk` | Signature only: WEAPONS-012 ignore (existing) + `GetAutofireShots` ×2 + `suppressionbonus` ×2 |
| `YouSeeIgor` | Kill → +3 AP |
| `WeGotThis` | Kill → +10 Grit squad |
| `NailsPerk` | After first kill → +20% damage until combat end |
| `JackOfAllTrades` | `GetOperationTimeLeft` ×(100−33)/100 |
| `SecondStoryMan` | High ground → +50 crit chance |
| `ShoulderToShoulder` | End turn adjacent ally → +15 Grit self+neighbors |
| `SteroidPunch` | All melee CTH from Strength; melee crit → Prone+Unconscious; Stimmed CTH pen cleared; ~30% fire dmg taken |
| `IcePerk` | DisplayName/Description only |

## Soft cuts / deferred

- **Ice**: five-limb shot list still vanilla CombatAction engine; CE text only (batch 3+ if CA rewrite needed).
- **Steroid fire dmg**: heuristic hit/action/weapon flags; not every Burning surface path guaranteed.
- **Wolf ops**: wraps `GetOperationTimeLeft` only (not every ETA helper).
- Loc IDs `890000000006500–6515` (outside VR-clogged 6300–6499 exclusive band).

## Validate

`python docs/tools/_validate_items_quick.py` → OK after apply.
