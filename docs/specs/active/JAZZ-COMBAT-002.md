---
id: JAZZ-COMBAT-002
status: implemented
owner: project-owner
systems:
  - combat-cth-actions
  - armor-damage-wounds-will
  - weapons-ammo-components
  - visibility-weather-appearance
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/ExecFirearmAttacks.lua
  - jazz/Code/MeleeWeapon.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/Strings.csv
  - jazz/Localization/EnglishManual.csv
  - jazz/InventoryItem/SmokeGrenade.lua
  - jazz/InventoryItem/TearGasGrenade.lua
  - jazz/InventoryItem/ToxicGasGrenade.lua
  - jazz/InventoryItem/MortarShell_Smoke.lua
  - jazz/InventoryItem/MortarShell_Gas.lua
  - jazz/InventoryItem/_MortarShell_Smoke.lua
  - jazz/InventoryItem/_MortarShell_Gas.lua
  - jazz/InventoryItem/JAZZ_AMMO_MortarShell_Smoke.lua
  - jazz/InventoryItem/JAZZ_AMMO_MortarShell_Gas.lua
  - jazz/docs/specs/active/JAZZ-COMBAT-002.md
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/technical/systems/visibility-weather-appearance.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMBAT-002: grazing только от CTH-кривой и укрытия

## Проблема

См. draft history: magic graze от near-miss band, fog/dust, C++ smoke LoF.

## Цели

- Miss→graze: `min(50, floor(50×((100−cth)/100)²))`.
- Cover→graze ∝ cover CTH bonus, cap 100%.
- Smoke/fog/dust env/LoF graze removed; knives included.
- Docs/loc sync.

## Non-goals

- CTH formula, GrazingHitDamage value, AI BunkerDown flow, C++ LoF rewrite.

## Решения владельца

| Решение | Итог |
| --- | --- |
| Кривая | `^2` |
| Cover | ∝ cover CTH bonus |
| Дым | всегда `ignore_smoke` |
| Ножи | да |
| Thermal | только cover-graze |

## Требования

- `JAZZ-COMBAT-002-REQ-001` — только miss→graze (^2, cap 50) и cover-graze (∝ bonus, cap 100).
- `JAZZ-COMBAT-002-REQ-002` — нет fog/dust env graze; нет smoke LoF graze; knives `ignore_smoke`.
- `JAZZ-COMBAT-002-REQ-003` — плоский +3/+6 удалён; CTH 20 → 32% miss-graze.
- `JAZZ-COMBAT-002-REQ-004` — cover-graze = `|cover_cth|/|cover_full|×100`.
- `JAZZ-COMBAT-002-REQ-005` — `GrazingHitDamage` без изменения семантики.
- `JAZZ-COMBAT-002-REQ-006` — smoke/gas hints и combat docs без magic graze.
- `JAZZ-COMBAT-002-REQ-007` — miss-graze band из того же attack roll (sync-safe).

## Acceptance criteria / Evidence

- `JAZZ-COMBAT-002-AC-001`: `PASS (static)` — Fog/Dust ветки удалены; `ignore_smoke=true`; нет threshold 3/6.
- `JAZZ-COMBAT-002-AC-002`: `PASS (static)` — `JAZZ_CalcMissGrazeChance`: 100→0, 80→2, 50→12, 20→32, 10→40.
- `JAZZ-COMBAT-002-AC-003`: `BLOCKED (runtime)` — smoke/knife playtest.
- `JAZZ-COMBAT-002-AC-004`: `BLOCKED (runtime)` — full/half cover graze rates.
- `JAZZ-COMBAT-002-AC-005`: `PASS (static)` / `BLOCKED (runtime)` — формула; бой.
- `JAZZ-COMBAT-002-AC-006`: `PASS (static)` — wiki/showcase/hints scrubbed; editor loc round-trip pending.
- `JAZZ-COMBAT-002-AC-007`: `BLOCKED (human)`.

## Impact

- Vanilla LoF smoke-graze нейтрализован Lua-границей.
- `version_minor` 35; `MeleeWeapon.lua` в `metadata.code`.
- Generated: ConstDef Fog/DustGrazeChance=0; Inventory AdditionalHint; editor round-trip recommended.

## Documentation delta

Обновлены `combat-cth-actions.md` (секция Grazing), `visibility-weather-appearance.md`, `file-coverage.md`, `testing.md`, `accuracy-model.md`, wiki + showcase RU/EN. Правило синхронизации: `.cursor/rules/jazz-docs-wiki-sync.mdc`.
