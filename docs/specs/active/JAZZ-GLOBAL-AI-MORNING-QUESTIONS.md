# Global AI — playtest notes (28 июля 2026)

Locked defaults after playtest (militia training out of scope).

**Cadence supersede (STRATEGY-016, 2026-08-02 / docs lock 2026-08-18):** `POIGenerationInterval` **96h** (не 72h), `TaxCooldown` / `RecruiterCooldown` **48h**, `CommandInterval` **12h**, combat spawn **1 / 48h**. Ниже — исторические числа 28 июля; 72h у STRATEGY-019 `logistics_open_at` (новые аванпосты) **не** этот пульс.

## Economy / POI

1. **POI pulse** every **4 days** (`POIGenerationInterval=96h`, 016; playtest 28 июля was 72h / 3 days): city/farm `$` + recruits on **economic POI only** (Farm/Mine/Guardpost/Port, or City+Militia/Hospital) — not every City-tagged wilderness tile.
2. Per pulse defaults: city **$2500**, farm **$800**; city recruits **3**, farm **2**, guardpost **2**, port **1**; caps city/farm/guardpost/port **16/8/12/8**.
3. Tax cargo max **$12000**, Recruiter cargo max **16**; TaxCap/RecruiterCap **1**.
4. Mine diamond stock remains hourly → shipment (not tax).

## Caps / spawn

5. Max **1 squad spawn / 48h / outpost** (016; playtest 28 июля was 1/day). Regular + logistics share the gate.
6. Garrison cap = **important Legion sectors + 1**; garrison with **≤10 living** returns to base for refit.
7. Soft caps: MG / sniper / **heavy** (separate) / specialist.

## Hospital

8. Unlocked Hospital **buffs** managed Legion squads (`Inspired`, 24h) — no HP heal (satellite enemies have no usable HP). Re-applied on CombatStart.

## Recruiter

8b. Recruits: strip into `outpost.manpower` (cap 32); overflow → `outbound_manpower` → manpower caravan **to Major**. Major→outpost caravan only when outpost manpower is **0**.

## Out of scope

9. Militia training Operation — not in this task.
