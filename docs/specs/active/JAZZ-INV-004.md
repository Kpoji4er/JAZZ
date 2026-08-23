---
id: JAZZ-INV-004
status: implemented
owner: project-owner
systems:
  - inventory-items-loot-crafting
  - explosives-traps-heavy-weapons
repositories:
  - jazz
  - jazz-units
risk: low
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-INV-004.md
  - jazz/Code/System_OR_Traps.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/scripts/legion-loadouts/data/recipes.json
  - jazz/scripts/legion-loadouts/generate.py
  - jazz/scripts/legion-loadouts/run_static_tests.py
  - jazz/scripts/legion-loadouts/TESTING.md
  - jazz/docs/tools/_audit_inv004_powder.py
  - jazz/docs/tools/README.md
  - jazz/docs/technical/systems/inventory-items-loot-crafting.md
  - jazz/docs/technical/systems/explosives-traps-heavy-weapons.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz-units/items.lua
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz-units/items.lua
related_decisions:
  - none
related_specs:
  - JAZZ-INV-003
approved_by: project-owner
---

# JAZZ-INV-004: порох с гренадеров, разбор зарядов, salvage мин

## Проблема

Кустарные патроны (INV-003) требуют BlackPowder, а основной источник — Bobby Ray. У ванили гренадеры иногда несут `ExplosiveComponents` (3–5 пороха, вес ~25%). Легионные `Grenadier_Inventory` / `HeavyGrenadier_Inventory` пороха не дают. Разбор fused TNT/C4/PETN в ванили возвращает кирпич + детонатор, не порох. Успешный disarm мины даёт только 1–2 Parts.

## Цели

- Гренадеры и гранатомётчики носят немного пороха в луте.
- Inventory-combine RecipeDef: кирпич TNT/C4/PETN + кусачки → порох (кусачки возвращаются).
- Успешный разбор мины с шансом кладёт в сумку отряда закладываемый заряд (TNT/C4/PETN).

## Non-goals

- Не менять цены CraftAmmo / INV-003.
- Не менять ванильные fused-рецепты (`TNT_Prox_Disassemble` и аналоги: кирпич + детонатор).
- Не разбирать Frag/HE/40mm/PipeBomb в новые рецепты (PipeBomb→порох уже ваниль).
- Не добавлять порох рокетёрам и миномётчикам.
- Не менять триггер proximity C4 (радиус, союзники).

## Требования

- `JAZZ-INV-004-REQ-001` — `Grenadier_Inventory`: гарантированно BlackPowder **1–2**. `HeavyGrenadier_Inventory`: **2–3**. Источник — `utility.powder` в `scripts/legion-loadouts/data/recipes.json` + generator.
- `JAZZ-INV-004-REQ-002` — тот же «чутка пороха» на фракционных гренадерах/ГЛ: `ArmyDemo`, `ArmyDemo_Elite`, `ArmyCommando_Demo` (1–2); `AdonisDemolitions`, `AdonisDemolitions_Elite` (2–3); `RebelGrenadier` (1–2); `RebelRPG` (2–3). Существующий `ExplosiveComponents` не снимать.
- `JAZZ-INV-004-REQ-003` — RecipeDef group `Explosives`, `ExplosivesRoll`: `JAZZ_TNT_Disassemble_Powder` TNT+Wirecutter → BlackPowder×**2**+Wirecutter, Diff 25; `JAZZ_C4_Disassemble_Powder` C4 → ×**3**, Diff 40; `JAZZ_PETN_Disassemble_Powder` PETN → ×**4**, Diff 55. Новых InventoryItem нет (Bobby не требуется).
- `JAZZ-INV-004-REQ-004` — `OnMsg.TrapDisarm` после успеха на `Landmine` (включая `DynamicSpawnLandmine`): **40%** один заряд в squad bag. Если `item_thrown` — Proximity/Timed/Remote C4/TNT/PETN, тип = базовый кирпич; иначе вес TNT 60 / C4 30 / PETN 10. Ванильные Parts сохраняются. Не Landmine (бочка, booby) — без заряда.

## Инварианты и ограничения

- Thug grenadier/GL, которые ссылаются на Legion inventory, получают порох автоматически.
- Fused disassemble не перекрывать новыми ID.
- Salvage использует `unit:Random` (детерминизм сети).
- Новых глобалов из OnMsg не создавать; helper объявлен на top-level файла.
- `items.lua` / `metadata.lua` после правки проходят `_validate_items_quick.py`.

## Acceptance criteria

- `JAZZ-INV-004-AC-001` — static: generator recipes + `Grenadier_Inventory` / `HeavyGrenadier_Inventory` содержат BlackPowder со стеками REQ-001; `run_static_tests.py` PASS.
- `JAZZ-INV-004-AC-002` — static: восемь фракционных LootDef из REQ-002 содержат BlackPowder с указанными стеками.
- `JAZZ-INV-004-AC-003` — static: три RecipeDef в `jazz/items.lua` + `ModResourcePreset` в `metadata.lua`; yields/Diff как REQ-003.
- `JAZZ-INV-004-AC-004` — static: `Jazz_TrySalvageMineCharge` + `OnMsg.TrapDisarm` в `System_OR_Traps.lua` с шансом 40 и mapping thrown→кирпич.
- `JAZZ-INV-004-AC-005` — docs: technical inventory + explosives, wiki и showcase RU/EN описывают порох с гренадеров, разбор кирпичей и salvage мин.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: RecipeDef — новые ID, ваниль не override. TrapDisarm — дополнительный handler. Legion loot — generator transaction.
- Saves: старые сейвы без пороха в уже заспавненном луте; новые спавны и combine/disarm — сразу.
- Network/determinism: `unit:Random` на том же TrapDisarm, что и Parts.
- Generated data: `jazz-units/items.lua` Legion inventories через generator; hand loot Army/Adonis/Rebel; `jazz` RecipeDef + metadata presets.
- Cross-package references: loot item `BlackPowder` / `TNT` / `C4` / `PETN` уже в jazz.
- Rollback/recovery: удалить RecipeDef, powder entries и TrapDisarm handler.

## План и ownership

- Пакет-владелец: `jazz` (рецепты, traps, docs); `jazz-units` (лут).
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: `jazz/items.lua`, `jazz/metadata.lua`, `jazz-units/items.lua`

## Решение владельца

- Статус: implemented
- Кто подтвердил: project-owner (чат «давай добавим…», 2026-08-23)
- Дата: 2026-08-23

## Evidence

- `JAZZ-INV-004-AC-001`: `PASS` — static: `run_static_tests.py` PASSED; `_audit_inv004_powder.py` OK (Grenadier 1–2, HeavyGrenadier 2–3).
- `JAZZ-INV-004-AC-002`: `PASS` — static: audit eight faction LootDef stacks.
- `JAZZ-INV-004-AC-003`: `PASS` — static: three RecipeDef + metadata presets; `_validate_items_quick.py` jazz + jazz-units OK.
- `JAZZ-INV-004-AC-004`: `PASS` — static: `Jazz_TrySalvageMineCharge` + `OnMsg.TrapDisarm`, chance 40, thrown→brick map.
- `JAZZ-INV-004-AC-005`: `PASS` — docs inventory/explosives/weapons-ammo + wiki + showcase RU/EN.

## Documentation delta

- `docs/technical/systems/inventory-items-loot-crafting.md` — RecipeDef пороха, лут.
- `docs/technical/systems/explosives-traps-heavy-weapons.md` — proximity C4 current-state + mine salvage.
- `docs/wiki/weapons-and-ammo.md` и showcase RU/EN — порох, разбор, мины.
