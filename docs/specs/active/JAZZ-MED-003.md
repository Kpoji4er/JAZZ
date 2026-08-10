---
id: JAZZ-MED-003
status: approved
owner: project-owner
systems:
  - armor-damage-wounds-will
  - bobby-ray-shop
repositories:
  - jazz
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - Code/System_JazzStackableMedicine.lua
  - Code/Systems_Medicine.lua
  - Code/System_UnitInventory.lua
  - Code/System_BobbyRay_ECON004.lua
  - InventoryItem/FirstAidKit.lua
  - InventoryItem/Medkit.lua
  - InventoryItem/Reanimationsset.lua
  - items.lua
  - metadata.lua
  - Russian.csv
  - English.csv
  - Localization/Strings.csv
  - Localization/RussianManual.csv
  - Localization/EnglishManual.csv
  - docs/specs/active/JAZZ-MED-003.md
  - docs/specs/active/JAZZ-MED-001.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/technical/systems/bobby-ray-shop.md
  - docs/wiki/combat-and-accuracy.md
  - docs/wiki/bobby-ray.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
  - docs/showcase/ru/bobby-ray.md
  - docs/showcase/en/bobby-ray.md
  - docs/tools/_audit_med003_kits.py
  - docs/tools/README.md
  - jazz-units/items.lua (Bonemaker_Inventory + Mercs hire medicine + Legion class medicine)
  - docs/tools/_apply_legion_med_loot_redistribute.py
  - docs/tools/_audit_legion_med_loot_redistribute.py
  - scripts/legion-loadouts/generate.py
  - scripts/legion-loadouts/run_static_tests.py
exclusive_resources:
  - items.lua
  - metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-MED-003: medkit tier package (S/M/L)

Extends [JAZZ-MED-001](JAZZ-MED-001.md) kit surface. Display names already Small/Medium/Large; this spec locks combat/shop/loot differentiation.

## Проблема

Три кита для `Bandage` слабо дифференцированы: большая не требовала Medical, частично чистила кровь, не имела чёткой роли в заживлении травм / инфекции / боли; Bobby Ray и лут Legion-медика не отражали «маленькая обычная / средняя редкая / большая дорогая».

## Цели

- Три аптечки с читаемой лестницей: порог Medical, стек, хилл, кровь, **заживление** (`jazz_healing`) по тиру травмы, боль/downed, снятие `WoundInfected`.
- Все три в Bobby Ray; большая — дорогая и редкая (soft-tail, не staple).
- Legion Bonemaker: в основном маленькая; средняя с **5%**.

## Non-goals

- Мгновенный clear Trauma* (только `jazz_healing`).
- Хирургический набор / госпиталь clear (MED-002).
- Переименование class ID (`FirstAidKit` / `Medkit` / `Reanimationsset` сохраняются).
- Soft-sanitar (Fox уже Doctor; Mouse/Scully без Spec=Doctor не форсятся в «медик»).

## Требования

### Display / stacks

- `JAZZ-MED-003-REQ-001` — DisplayName: Small / Medium / Large Medkit (RU: Маленькая / Средняя / Большая аптечка). Public IDs unchanged.
- `JAZZ-MED-003-REQ-002` — `MaxStacks`: Small **5**, Medium **10**, Large **15**. One use = −1 Amount.

### Medical / heal / bleed

- `JAZZ-MED-003-REQ-003` — Medical gates (`JazzMedicineRequiredMedical`, `>=`): Small **30**, Medium **50**, Large **80** (owner «>80» → порог **80**).
- `JAZZ-MED-003-REQ-004` — Heal modifiers on kit Bandage: Small **+0%**, Medium **+50%**, Large **+100%**.
- `JAZZ-MED-003-REQ-005` — All three kits call `JazzClearAllBleeding` (full stack clear). Large no longer uses partial `JazzClearBleedStrong`.

### Trauma healing (`jazz_healing` only)

- `JAZZ-MED-003-REQ-006` — On successful kit Bandage, mark **one** unhealed Trauma* with `jazz_healing` (same progress rules as MED-001 TreatWounds flag: half interval, improve 100%, worsen 0). Prefer heaviest eligible unhealed trauma (zone order on ties).
  - Small: only **Light**
  - Medium: **Medium** or **Light** (prefer Medium if both)
  - Large: **any** tier (Light/Medium/Heavy)
- `JAZZ-MED-003-REQ-007` — Kits never instant-clear Trauma*. No mark if no eligible unhealed trauma.

### Pain / downed / infection

- `JAZZ-MED-003-REQ-008` — Any kit Bandage applies `Analgesia` (clears/blocks Pain like morphine) and refunds current-turn Pain AP via existing helper when applicable.
- `JAZZ-MED-003-REQ-009` — Any kit can rally downed (existing DownedRally / Bandage path; targeting treats downed as eligible). Morphine remains separate action.
- `JAZZ-MED-003-REQ-010` — Any kit Bandage clears `WoundInfected` via `JazzClearWoundInfected`.

### Targeting / consume

- `JAZZ-MED-003-REQ-011` — Kit Bandage eligible when: bleed, HP debt, downed/unconscious, Pain, WoundInfected, or kit-eligible unhealed trauma for the equipped kit. Consume one stack if any successful effect (heal, bleed clear, trauma mark, pain/analgesia, infection clear, or rally treat).

### Bobby Ray

- `JAZZ-MED-003-REQ-012` — Small + Medium remain staples (flat restock, Tier 1).
- `JAZZ-MED-003-REQ-013` — Large (`Reanimationsset`): `CanAppearInShop=true`, Tier **3**, high `Cost` (≥1500), low `RestockWeight` (≤20), `MaxStock` ≤2; **not** in Bobby flat-staple table (soft-tail like specialty med).

### Legion loot

- `JAZZ-MED-003-REQ-014` — `Bonemaker_Inventory`: guaranteed Small Medkit (`FirstAidKit`, stack to MaxStacks); Medium (`Medkit`) with `generate_chance = 5`; no guaranteed Medium/Large.
- `JAZZ-MED-003-REQ-021` — Legion **class_tier 2** inventories: `JAZZ_Bandage` stack **1–2** (guaranteed entry).
- `JAZZ-MED-003-REQ-022` — Legion **class_tier 3** inventories: `JAZZ_Morphine` ×1 with `generate_chance = 30` (not guaranteed).
- `JAZZ-MED-003-REQ-023` — Legion medic (`utility.medkit` / `Bonemaker_Inventory`): Bandage **1–10**, Morphine **0–3** (guaranteed ranges) beside kits from REQ-014. T1/T4 non-medic: no field bandage/morphine.
- Apply/audit: `docs/tools/_apply_legion_med_loot_redistribute.py`, `_audit_legion_med_loot_redistribute.py`; generator `scripts/legion-loadouts/generate.py` emits the same so regen does not clobber.

### Hire medicine loot (AIM / JAZZ Merc / AME)

Owner lock 2026-08-10. Apply: `docs/tools/_apply_merc_med_loot_redistribute.py`; audit: `_audit_merc_med_loot_redistribute.py`. Canonical Equipment owners only (skip borrowed stubs: BarrySeal→Ice, Simon→Ira, …).

- `JAZZ-MED-003-REQ-015` — **Medical < 20:** только `JAZZ_Bandage` (нет аптечек, нет морфия) — даже при `Tier=Veteran`.
- `JAZZ-MED-003-REQ-016` — **Kits by Medical** (usable thresholds ≥30/50/80): AIM/Merc get best usable kit on highest gear leaf; lower leaves cascade down one tier. `Specialization=Doctor` / AME `AMERole=Medic` always ≥ Small on every leaf (if Medical ≥ 20).
- `JAZZ-MED-003-REQ-017` — **Non-Doctor AIM/Merc:** kits only if Medical **> 30**; not every preset (Small → highest leaf only; Medium → *50 + Small on next; Large → *50/*35/*25 cascade).
- `JAZZ-MED-003-REQ-018` — **AME:** Small kits only (`FirstAidKit`) when Doctor/Medic or Medical ≥ 30.
- `JAZZ-MED-003-REQ-019` — **Bandages:** everyone 1–2 floor; scale with Medical up to **10**; Doctors up to MaxStacks **30** spread across leaves.
- `JAZZ-MED-003-REQ-020` — **Morphine:** `Tier=Veteran` → 1 (if Medical ≥ 20); Doctors up to MaxStacks **10** spread. Preserve `Meds` / `JAZZ_SurgicalKit`.

## Инварианты и ограничения

- Public IDs `FirstAidKit` / `Medkit` / `Reanimationsset` preserved.
- Field bandage (`JAZZ_Bandage`) and Morphine unchanged except shared DownedRally stack-safety.
- MED-001 TreatWounds → mark **all** traumas healing remains.
- Deterministic loot RNG contexts unchanged except Bonemaker medicine entries.

## Acceptance criteria

- `JAZZ-MED-003-AC-001` — static: Medical 30/50/80; heal +0/+50/+100; MaxStacks 5/10/15; companion/`items.lua` parity.
- `JAZZ-MED-003-AC-002` — static: all three kits full bleed clear; Large no `JazzClearBleedStrong` path in `GetBandaged`.
- `JAZZ-MED-003-AC-003` — static: trauma mark helpers enforce Light / ≤Medium / any; only `jazz_healing`.
- `JAZZ-MED-003-AC-004` — static: GetBandaged applies Analgesia + `JazzClearWoundInfected` for kit classes.
- `JAZZ-MED-003-AC-005` — static: Large shop fields + not in `JAZZ_BOBBY_FLAT`; Small/Medium still flat.
- `JAZZ-MED-003-AC-006` — static: Bonemaker_Inventory FirstAidKit guaranteed; Medkit generate_chance 5.
- `JAZZ-MED-003-AC-009` — static: hire Mercs/Ernie/AME medicine loot matches REQ-015…020 (`_audit_merc_med_loot_redistribute.py`).
- `JAZZ-MED-003-AC-010` — static: Legion class inventories match REQ-021…023 (`_audit_legion_med_loot_redistribute.py`).
- `JAZZ-MED-003-AC-007` — docs: technical + wiki + showcase RU/EN + bobby-ray notes synced.
- `JAZZ-MED-003-AC-008` — runtime/human: Bandage with each kit matches REQ-006…010 (BLOCKED until playtest).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: kit Bandage / GetBandaged / Bobby restock weights.
- Saves: existing stacks clamp to new MaxStacks on next merge; OK.
- Network/determinism: unit RNG unchanged.
- Generated data: jazz `items.lua` + companions; jazz-units Bonemaker + Mercs/Ernie/AME hire medicine loot.
- Cross-package: jazz-units loot defs.
- Rollback: revert write_set; MED-001 REQ-018 superseded by this package.

## План и ownership

- Пакет-владелец: jazz (+ jazz-units loot)
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive resources: items.lua, metadata.lua

## Решение владельца

- Статус: **approved**
- Кто подтвердил: project-owner (chat 2026-08-10: stacks S/M/L 5/10/15; Large Med≥80 +100% heal; full bleed; BR all three / large rare; Legion 95% small 5% medium; trauma healing by tier; clear infection; all kits pain+downed; hire loot by Medical + Med<20 bandages-only; «и спеку под все это сразу пиши»)
- Дата: 2026-08-10

## Evidence

- `JAZZ-MED-003-AC-001`…`006`: `PASS` — static `python docs/tools/_audit_med003_kits.py`.
- `JAZZ-MED-003-AC-007`: `PASS` — wiki/showcase/technical updated this change set.
- `JAZZ-MED-003-AC-008`: `BLOCKED` — runtime/human playtest.
- `JAZZ-MED-003-AC-009`: `PASS` — `python docs/tools/_audit_merc_med_loot_redistribute.py`.
- `JAZZ-MED-003-AC-010`: `PASS` — `python docs/tools/_audit_legion_med_loot_redistribute.py`.

status note: code + loot + docs wired; mark `implemented` after smoke.

## Documentation delta

- `docs/technical/systems/armor-damage-wounds-will.md` — kit table + hire/Legion loot policy
- `docs/technical/systems/bobby-ray-shop.md` — Large soft-tail
- `docs/wiki/combat-and-accuracy.md` + showcase RU/EN
- `docs/wiki/bobby-ray.md` + showcase RU/EN
- `docs/wiki/african-mercenary-exchange.md` + showcase RU/EN — starting medicine
- `docs/wiki/legion-global-ai.md` + showcase `legion-units` RU/EN — Legion field medicine
- `docs/specs/active/JAZZ-MED-001.md` — note REQ-018 superseded by MED-003
- ECON-004: Large specialty soft-tail noted here; full ECON-004 amend optional follow-up
