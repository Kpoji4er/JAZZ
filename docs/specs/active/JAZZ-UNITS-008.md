---
id: JAZZ-UNITS-008
status: approved
owner: project-owner
systems:
  - legion-units-equipment
  - inventory-items-loot
repositories:
  - jazz
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-UNITS-008.md
  - jazz/scripts/legion-loadouts/data/early_variants.json
  - jazz/scripts/legion-loadouts/generate.py
  - jazz/scripts/legion-loadouts/run_static_tests.py
  - jazz/scripts/legion-loadouts/README.md
  - jazz/scripts/legion-loadouts/TESTING.md
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz/docs/design/legion-loadouts.md
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-units.md
  - jazz/docs/showcase/en/legion-units.md
exclusive_resources:
  - jazz-units/items.lua
  - jazz/scripts/legion-loadouts/data/early_variants.json
related_decisions:
  - none
approved_by: project-owner chat 2026-08-14 — restore M1 no-gate; module niches; folded AR into carbine at low chance
related:
  - JAZZ-UNITS-004
  - JAZZ-COMPAT-008
---

# JAZZ-UNITS-008: Early module variants (M1 carbine + niche borrow)

## Проблема

После UNITS-003 генератора `M2Carbine` открывается только с CSV `1-2` (Amount 12). Maps-тир (COMPAT-008) держит Эрни на `11` семь суток, а T1 assault/SMG классы больше не берут карабин. Игрок не видит «М1» с первого сектора. Задумка ствола: один `M2Carbine` = M1 / M2 / M3 комплектациями; без приклада это ПП; часть штурмовых со складным/лёгким прикладом может редко стоять в нише карабина. Модульный конфиг может падать раньше CSV-тира.

## Цели

- M1-конфиг (`StockNormal`, магазин 15, без автоогня) снова в arch1 **без нижнего порога Amount** (как `LegionT1_Carbine` / `Carbines_M1Carbine`).
- Ниша зависит от набора: приклад = carbine, без приклада = smg, автоогонь = carbine+assault.
- Штурмовые со складным/лёгким прикладом — в carbine-пул на **низком** весе, со своего CSV unlock (не раньше).
- Общий каталог `early_variants.json` + авто-borrow, чтобы другие стволы могли повторить паттерн.

## Non-goals

- Смена формулы `JAZZ_Legion_Tier` / COMPAT-008 таймеров.
- Отдельный InventoryItem `M1Carbine`.
- Ночник M3 / полный rewrite `packages.json` keyword matcher.
- Менять `primary_tags` рецептов (Roughneck без carbine-нормы сохраняется).

## Требования

- `JAZZ-UNITS-008-REQ-001` — `early_variants.json`: M1 (stock) → `carbine`, `no_lower_gate`, arch1 `<=19`; no-stock → `smg`; M2 autofire+30 mag → `carbine`+`assault` с Amount 12.
- `JAZZ-UNITS-008-REQ-002` — генератор матчит variant `tags` с recipe tags нужного arch; не CSV-теги ствола.
- `JAZZ-UNITS-008-REQ-003` — AssaultRifle с `StockLightFolded` / `StockFolded` / `StockLight`, у которых ещё нет тега `carbine`, получают carbine-borrow на весе **6000** с CSV Amount.
- `JAZZ-UNITS-008-REQ-004` — Roughneck не получает stocked M1 (carbine); получает no-stock как SMG.

## Инварианты и ограничения

- CSV `tier_label` 1-2 для «полного» M2 не меняется; исключение только variant-слоем.
- Arch bands `[11,19]` / `[21,29]` / `≥31` и ~1% remnant не ломаются.
- Upgrade ID только из `weapon-component-options.csv`.
- Public LootDef id остаются `JAZZ_GenW_*`.

## Acceptance criteria

- `JAZZ-UNITS-008-AC-001` — static: `generate.py --dry-run` + `run_static_tests.py` PASS; новые combo id в metadata.
- `JAZZ-UNITS-008-AC-002` — static: `Warden_Firearm` содержит `M2Carbine_early_m1` без Amount ≥; combo = `JAZZ_StockNormal`, без `JAZZ_Autofire`.
- `JAZZ-UNITS-008-AC-003` — static: `Roughneck_Firearm` содержит `early_m1_smg` (`JAZZ_StockNo`) и не содержит stocked `early_m1` без `_smg`.
- `JAZZ-UNITS-008-AC-004` — static: carbine-класс (Warden) имеет `carbine_fold` штурмовую (например `Zastava_M70` / `AKM`) с весом 6000 и Amount = CSV тир.
- `JAZZ-UNITS-008-AC-005` — runtime/human: на Эрни при tier 11 M1-карбайн падает с дозорного/костоправа; без приклада — с головореза.

## Impact и совместимость

- Vanilla/CommonLib: нет.
- Saves: существующие отряды обновятся при `RegenerateLegionLoot` / OpenSatellite; новые сектора сразу.
- Network/determinism: тот же loot RNG seed.
- Generated data: `jazz-units/items.lua` generated markers + metadata `JAZZ_Gen*`.
- Cross-package: generator в `jazz`, LootDef в `jazz-units`.
- Rollback: убрать `early_variants.json` inject и перегенерировать.

## План и ownership

- Пакет-владелец: `jazz` (generator) / `jazz-units` (LootDef)
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. front-matter
- Exclusive resources: generated Legion LootDef block; `early_variants.json`

## Решение владельца

- Статус: **approved**
- Кто подтвердил: project-owner (chat 2026-08-14)
- Дата: 2026-08-14
- Решения: M1 без порога как исключение; ниша carbine/SMG/early assault по модулям; складные/лёгкие штурмовые в carbine на низком шансе.

## Evidence

- `JAZZ-UNITS-008-AC-001`: `PASS` (static) — `generate.py` 37/37, 720 combos; `run_static_tests.py` PASSED; `_validate_items_quick.py` OK on jazz-units; +10 `JAZZ_Gen*` in metadata.
- `JAZZ-UNITS-008-AC-002`: `PASS` (static) — `Warden_Firearm` `M2Carbine_early_m1` Amount=19 `<=` only; combo `JAZZ_StockNormal`, no Autofire.
- `JAZZ-UNITS-008-AC-003`: `PASS` (static) — `Roughneck_Firearm` has `early_m1_smg` (`JAZZ_StockNo`), not stocked `early_m1`.
- `JAZZ-UNITS-008-AC-004`: `PASS` (static) — Warden `Zastava_M70_carbine_fold` weight=6000 Amount=[22, 29].
- `JAZZ-UNITS-008-AC-005`: `BLOCKED` (runtime/human) — Ernie day-one M1 drop smoke.

## Documentation delta

- `docs/design/legion-loadouts.md` — L11 / module niches.
- `docs/technical/systems/legion-units-equipment-tiers.md` — early variants current-state.
- `docs/wiki/legion-global-ai.md` + showcase RU/EN `legion-units.md` — игрок: карбайн с первого дня, компактные штурмовые редко у карабин-ролей.
