# Global AI — playtest notes (28 июля 2026)

Locked defaults after playtest (militia training out of scope).

## Economy / POI

1. **POI pulse** every **3 days** (`POIGenerationInterval=72h`): city/farm `$` + recruits on **economic POI only** (Farm/Mine/Guardpost/Port, or City+Militia/Hospital) — not every City-tagged wilderness tile.
2. Per pulse defaults: city **$2500**, farm **$800**; city recruits **3**, farm **2**; caps 16/8.
3. Tax cargo max **$12000**, Recruiter cargo max **16**; TaxCap/RecruiterCap **1**.
4. Mine diamond stock remains hourly → shipment (not tax).

## Caps / spawn

5. Max **1 squad spawn / day / outpost** (regular + logistics share the gate).
6. Garrison cap = **important Legion sectors + 1**; garrison with **≤10 living** returns to base for refit.
7. Soft caps: MG / sniper / **heavy** (separate) / specialist.

## Hospital

8. Unlocked Hospital **buffs** managed Legion squads (`Inspired`, 24h) — no HP heal (satellite enemies have no usable HP). Re-applied on CombatStart.

## Recruiter

8b. Recruits: strip into `outpost.manpower` (cap 32); overflow → `outbound_manpower` → manpower caravan **to Major**. Major→outpost caravan only when outpost manpower is **0**.

## Out of scope

9. Militia training Operation — not in this task.
