---
id: JAZZ-HOTFIX-003
status: approved
owner: project-owner
systems:
  - combat-actions
  - suppression
  - weapon-fx
  - legion-loadouts
repositories:
  - jazz
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/ExecFirearmAttacks.lua
  - CharacterEffect/suppressionPinned.lua
  - items.lua
  - Russian.csv
  - English.csv
  - Localization/Strings.csv
  - scripts/legion-loadouts/data/recipes.json
  - scripts/legion-loadouts/run_static_tests.py
  - scripts/legion-loadouts/TESTING.md
  - docs/tools/_audit_hotfix_003.py
  - docs/tools/README.md
  - docs/design/legion-loadouts.md
  - docs/specs/active/JAZZ-HOTFIX-003.md
  - docs/technical/systems/combat-cth-actions.md
  - docs/technical/systems/legion-units-equipment-tiers.md
  - docs/technical/systems/ui-audio-fx.md
  - docs/technical/weapons/combat-actions.md
  - docs/wiki/combat-actions.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-actions.md
  - docs/showcase/en/combat-actions.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
  - docs/showcase/ru/legion-units.md
  - docs/showcase/en/legion-units.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - metadata.lua
  - ../jazz-units/items.lua
  - ../jazz-units/metadata.lua
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/Strings.csv
  - jazz-units/items.lua
  - jazz-units/metadata.lua
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-006
  - JAZZ-UNITS-003
  - JAZZ-UNITS-004
  - JAZZ-COMBAT-003
approved_by: project-owner
---

# JAZZ-HOTFIX-003: action bar, pinned overwatch, shotgun FX and Legion loadouts

## Проблема

После нескольких playtest-правок остался незакоммиченный набор и обнаружены новые регрессии:

- `Unjam` принудительно помещён в `SignatureAbilities` и исчезает с обычной панели действий;
- максимальная ступень подавления `suppressionPinned` ограничивает контратаки, но не прерывает уже подготовленные overwatch/pindown/bombard, включая постоянный пулемётный overwatch;
- контракт UnitData для `JAZZ_Legion_GunnerT2_AssaultGunner` обещает мачете и Molotov, а рецепт `AssaultGunner_Inventory` их не создаёт;
- ранее подготовленная правка `Skirmisher_Inventory` переводит застрельщика на ветку battle rifle, но generated data ещё не закоммичены;
- pellet pack дробовика воспроизводит action FX для каждого pellet вместо одного FX на пакет.

## Цели

- Вернуть `Unjam` на штатную поверхность action bar при заклинившем активном оружии.
- При наложении `suppressionPinned` прерывать все штатные prepared attacks через vanilla API.
- Дать Commando гарантированные Machete и Molotov и доказать соответствие всех 37 рецептов их generated-инвентарям и UnitData Equipment.
- Завершить найденные shotgun-FX и Skirmisher loadout fixes без изменения остальных формул/ролей.
- Синхронизировать generated data, локализацию и current-state документацию.

## Non-goals

- Менять пороги накопления/спада подавления, AP cap или поведение ступеней ниже `suppressionPinned`.
- Переписывать `Unit:InterruptPreparedAttack`, правила постоянного пулемёта либо расчёт overwatch.
- Перебалансировать все Legion-роли по старым комментариям: канон инвентарей — `docs/design/legion-loadouts.md` + `recipes.json`; UnitData проверяется на ссылку `Equipment`.
- Менять firearm tier tables, weapon availability, squad composition или карты.
- Массово форматировать/regenerate файлы вне declared write set.

## Требования

- `JAZZ-HOTFIX-003-REQ-001` — `Unjam` сохраняет vanilla `group = "Default"` и `SortKey = 10`, имеет `ShowIn = "CombatActions"` (не `SignatureAbilities`); `GetUIState` gate по jammed firearm с учётом `WeaponResource` (не ложного `IsCondition("Broken")` по stale `Condition`) и AP.
- `JAZZ-HOTFIX-003-REQ-002` — `suppressionPinned.OnAdded` вызывает `obj:InterruptPreparedAttack()` до смены стойки/укрытия и дополнительно снимает residual `g_Overwatch` / `StationedMachineGun`; `OnBeginTurn` и `ApplySuppressionStatus` (уже pinned) повторяют interrupt; Jazz `Unit:BeginTurn` не сохраняет permanent MG OW при `suppressionPinned`.
- `JAZZ-HOTFIX-003-REQ-003` — `AssaultGunner_Inventory` для каждого arch гарантированно содержит `Machete` и `Molotov`; `CustomEquipGear` продолжает экипировать melee в `Handheld B`.
- `JAZZ-HOTFIX-003-REQ-004` — статический аудитор для всех 37 рецептов проверяет существование inventory/firearm LootDef, связь UnitData `Equipment`, ссылку root inventory на firearm и материализацию recipe sidearm/melee/utility.
- `JAZZ-HOTFIX-003-REQ-005` — `Skirmisher_Inventory` использует `battle` + rifle packages + Match ammo по design-контракту.
- `JAZZ-HOTFIX-003-REQ-006` — shotgun pellet pack задаёт `single_fx`/`WeaponBuckshot` один раз и после первого `FireBullet` очищает `attackArg.fx_action`, не изменяя CTH, recoil или число pellets.
- `JAZZ-HOTFIX-003-REQ-007` — RU/EN tooltip `suppressionPinned` одинаково сообщает о срыве подготовленных атак; обе runtime CSV имеют одинаковое множество активных mod-only ID.

## Инварианты и ограничения

- Public IDs `Unjam`, `suppressionPinned`, `AssaultGunner_Inventory`, `Skirmisher_Inventory` сохраняются.
- Нижние четыре ступени подавления не снимают prepared attacks.
- `InterruptPreparedAttack` вызывается штатным методом Unit; локальная копия vanilla/CommonLib логики не создаётся.
- Save fields, network payload и RNG order вне добавленных loadout entries не меняются.
- Generated transaction: recipe/design/test → `jazz-units/items.lua`; CharacterEffect companion ↔ `jazz/items.lua`; metadata обоих владельцев.
- Canonical profile и no-maps profile получают одинаковый loadout contract через `jazz-units`.

## Acceptance criteria

- `JAZZ-HOTFIX-003-AC-001` — static diff показывает `ShowIn = "CombatActions"`, Default/SortKey, jam/`WeaponResource`/AP gates; runtime: action появляется только при jammed active firearm.
- `JAZZ-HOTFIX-003-AC-002` — static test подтверждает `InterruptPreparedAttack` в OnAdded (оба слоя), OnBeginTurn, residual MG strip, BeginTurn/ApplySuppressionStatus hooks; runtime: переход в pinned и ход под pinned снимают обычный и постоянный MG overwatch, pindown и bombard.
- `JAZZ-HOTFIX-003-AC-003` — dry-run генератора и статический аудитор проходят 37/37; `AssaultGunner_Inventory` содержит Machete для трёх arch bands с `generate_chance = 100` и один безусловный Molotov без `generate_chance`.
- `JAZZ-HOTFIX-003-AC-004` — все 37 UnitData с рецептами ссылаются через `Equipment` на recipe inventory, root inventory ссылается на recipe firearm, materialized optional/guaranteed entries соответствуют recipe.
- `JAZZ-HOTFIX-003-AC-005` — `Skirmisher_Firearm` материализует battle/rifle contract без старой SMG/flanker ветки.
- `JAZZ-HOTFIX-003-AC-006` — static shotgun harness/diff подтверждает один непустой `fx_action` на pellet pack; runtime: один muzzle/shot FX на действие.
- `JAZZ-HOTFIX-003-AC-007` — generated-data sync по всем пакетам не сообщает stale-layer/duplicate orphan для затронутых ID; package audits проходят.
- `JAZZ-HOTFIX-003-AC-008` — localization audit/targeted CSV check подтверждает RU+EN для ID `890000000001235`, отсутствие новых collision и нулевую разницу множеств mod-only ID.
- `JAZZ-HOTFIX-003-AC-009` — technical + wiki + showcase RU/EN описывают актуальные Unjam, pinned и Commando contracts.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ удаляет лишнее отличие Unjam от vanilla; вызывает подтверждённый vanilla `Unit:InterruptPreparedAttack`; свежий CommonLib `1.11 build 1059` совпадающих overrides не содержит.
- Saves: совместимо; существующие units получают новое поведение при следующем наложении статуса, новые loadouts — при следующем создании/regen gear.
- Network/determinism: prepared-attack cleanup использует существующий синхронный Unit path; loadout RNG следует существующему генератору.
- Generated data: да, два владельца (`jazz`, `jazz-units`).
- Cross-package references: `jazz` recipe/generator → `jazz-units/items.lua`; UnitData остаётся в `jazz-units`.
- Rollback/recovery: revert обоих package-коммитов вместе; не сохранять Mod Editor поверх ручного diff до sync-аудита.

## План и ownership

- Пакеты-владельцы: `jazz` (CombatAction, CharacterEffect, generator/docs/loc) и `jazz-units` (LootDef generated data).
- Исполнитель / Reviewer: project-owner.
- Declared write set: frontmatter.
- Exclusive resources: frontmatter.

## Решение владельца

- Статус: `approved`.
- Кто подтвердил: project-owner — явный запрос исправить и закоммитить 2026-08-06.
- Дата: 2026-08-06.

## Evidence

- `JAZZ-HOTFIX-003-AC-001`: `PASS` (static) — `python docs/tools/_audit_hotfix_003.py`: Unjam `ShowIn = CombatActions`, Default/SortKey=10, jam/`WeaponResource`/AP gates; `FirearmBase:IsCondition` follows resource %. `BLOCKED` (runtime) — jam/unjam action-bar smoke requires JA3.
- `JAZZ-HOTFIX-003-AC-002`: `PASS` (static) — auditor confirms OnAdded interrupt + residual MG strip, OnBeginTurn interrupt, BeginTurn pinned permanent-OW cancel, ApplySuppressionStatus re-interrupt; vanilla `InterruptPreparedAttack` clears Overwatch/`StationedMachineGun`, Pin Down and Bombard. `BLOCKED` (runtime) — ordinary/permanent MG overwatch, Pin Down and Bombard smoke requires JA3.
- `JAZZ-HOTFIX-003-AC-003`: `PASS` (static) — generator dry-run and apply report `37/37`; `run_static_tests.py` confirms three Machete arch entries at 100%, one unconditional Molotov and `Handheld B` melee equip.
- `JAZZ-HOTFIX-003-AC-004`: `PASS` (static) — `HOTFIX-003 recipe/inventory/UnitData contracts 37/37`: UnitData `Equipment`, inventory→firearm and sidearm/melee/utility/armor/night/flare/misc/valuables materialization.
- `JAZZ-HOTFIX-003-AC-005`: `PASS` (static) — Skirmisher recipe is battle-only with rifle packages/Match cap; generated firearm references rifle packages and upgraded-ammo combos, no flanker package.
- `JAZZ-HOTFIX-003-AC-006`: `PASS` (static) — auditor confirms `single_fx`, `WeaponBuckshot`, post-first-`FireBullet` clear and BuckshotBurst argument copy. `BLOCKED` (runtime) — one muzzle/shot FX smoke requires JA3.
- `JAZZ-HOTFIX-003-AC-007`: `PASS` (targeted static) — quick structural checks and Lupa load pass for `jazz` and `jazz-units`; generated loadout suite passes. Full read-only sync auditor remains `BLOCKED` by suite baseline (488 unrelated companion/orphan reports); no HOTFIX-003 target is reported, and targeted companion/generated parity passes. Mod Editor round-trip is runtime-blocked.
- `JAZZ-HOTFIX-003-AC-008`: `PASS` (static/localization) — ID `890000000001235` is complete and collision-free in catalog + RU/EN runtime; all `5963` catalog `new-id` values have identical RU/EN runtime ID sets. Full non-strict baseline audit: `needs Russian=51`, `needs English=4142`, active collisions=4 (pre-existing; target absent from all lists).
- `JAZZ-HOTFIX-003-AC-009`: `PASS` (docs) — technical + wiki + showcase RU/EN describe Unjam, pinned prepared-attack cleanup, Commando Machete/Molotov and Skirmisher battle-rifle contract.

## Documentation delta

- Technical: combat/suppression, combat actions, Legion equipment tiers, shotgun FX.
- Player wiki: `combat-actions.md`, `combat-and-accuracy.md`.
- Showcase: RU/EN versions of combat actions and combat/accuracy; Legion unit pages receive Commando loadout note only if the role is already listed there.
