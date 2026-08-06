# R.I.S. (Recon Intelligence Services)

Current-state for JAZZ-UI-RIS-001.

## Load

| File | Role |
| --- | --- |
| `Code/System_RIS_Mail.lua` | Desk queue (welcome + Legion briefs), `ris` tab lock |
| `Code/System_RIS_Content.lua` | Loc banks: dossiers, AAR templates (generated) |
| `Code/System_RIS_Combat.lua` | Kill counters, CombatEnd/ConflictEnd AAR snapshots |
| `Code/System_RIS_Browser.lua` | PDA mode `ris`: Bulletin / Dossiers / Battle reports |

Tabs call `JAZZ_RIS_RefreshPage` (find `idRISPage` under `idBrowserContent` / scroll; `IdNode` on content+scroll). Inject always replaces the `ris` mode on `DataLoaded` / `ModsReloaded`. Mode hosts `PDAGenericCloseAction` (bottom-right ActionBar Close, same as AIM/AME).

GameVar: `gv_JAZZ_RIS` — `welcome_*`, `last_mailed_tier`, `mail_queue`, `next_dispatch_at`, `kills`, `dossiers`, `quest_met`, `battles` (FIFO 20).

## Mail desk queue

- At most **one** R.I.S. Email every **5** campaign hours (`next_dispatch_at`).
- **Welcome:** enqueue at awake, `ready_at = awake + 2h` (arrives before the baseline brief).
- **Baseline brief** (current tier, usually 11 / T1-1): enqueue at awake, `ready_at = awake + 7h`.
- **Tier raise:** enqueue with `ready_at = now + 5h` (not instant).
- Drain on `SatelliteTick` / `OpenSatelliteView` / Load: first queue item with `ready_at ≤ now`, then slot +5h.
- Catch-up on Load: one queued brief for current tier if never mailed — not an immediate dump.
- **Unit sighting:** first combat contact with a `JAZZ_Legion_*` type → queue `RIS_UnitSighting`; on deliver unlock `dossiers[type]` (site catalog).
- **Obituaries:** named `elite` death → `RIS_EliteObit`; key NPC (`JAZZ_RIS_KEY_NPCS` / quest cards) → `RIS_NpcObit`; same desk spacing.

## AAR context

- **Sector:** `GetSectorName` (+ optional POI/label) in every report; title suffix `— <sector>`.
- **Quest:** `GetQuestsAssociatedWithSector` (badge notes) preferred; else `GetActiveQuest` as soft link; `quest_linked` only when sector-badged.
- Character templates switch to `quest_win` / `quest_loss` / `quest_retreat` when badge-linked.
- Elite+named paragraphs via `T{…, name=…}`; no mail per battle.

## Dossiers

Unlock after **3** player-side kills of a `JAZZ_Legion_*` type. Quest cards: Pierre / Bastien / TheMajor / Legion (IsMet / first Legion kill).

## Design canon

- [`docs/design/ris-legion-tier-briefs.md`](../../design/ris-legion-tier-briefs.md)
- [`docs/design/ris-legion-dossiers.md`](../../design/ris-legion-dossiers.md)
- [`docs/design/ris-battle-report-templates.md`](../../design/ris-battle-report-templates.md)
