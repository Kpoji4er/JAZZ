# R.I.S. battle-report paragraph templates

Runtime: `Code/System_RIS_Content.lua` + `System_RIS_Combat.lua` (JAZZ-UI-RIS-001 Phase B).

## Slots

| Slot | Bands | Pick |
| --- | --- | --- |
| Headline | win/loss/retreat × low/mid/high × ≥3 variants | deterministic hash |
| **Sector** | display name via `GetSectorName` (+ optional POI/label) | always |
| **Quest** | `GetQuestsAssociatedWithSector` badges; else `GetActiveQuest` | one/many/active/none |
| Weather | clear / rain / night / fog / heat / dust / default | map GameState / weather |
| Intensity | low / mid / high | Heat delta + casualty rate |
| Forces | counts | `<player>` / `<enemy>` |
| Character | win / loss / retreat / ambush (+ quest_* variants) | ConflictEnd + quest link |
| Losses | KIA/WIA both sides | combat snap |
| Elite+named | killed / wounded / escaped / threat | `T{…, name=…}` per elite |
| Closing | quiet / noise / disaster | intensity × outcome |

Loc IDs allocated from `890000000011000` by `_apply_ris_phase_b.py`.
