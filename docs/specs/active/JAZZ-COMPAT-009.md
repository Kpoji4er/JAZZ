---
id: JAZZ-COMPAT-009
status: implemented
owner: project-owner
systems:
  - strategy-squads-sectors
  - package-compatibility
repositories:
  - jazz-nomaps
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz-nomaps/Code/NoMaps_Autonomy.lua
  - jazz/docs/specs/active/JAZZ-COMPAT-009.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/docs/tools/_verify_nomaps_squad_size_cap.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - Code:NoMaps_Autonomy.lua
  - Global:GenerateEnemySquad
  - Global:GenerateUnitsFromTemplates
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMPAT-009: максимум 30 бойцов в стартовом satellite-отряде NoMaps

## Проблема

В профиле `jazz-nomaps` стартовые отряды, уже расставленные по vanilla-карте через
`SatelliteSector.InitialSquads`, создаются из `EnemySquadDef`, которые подменяет
`jazz-units`. После такой подмены стартовый отряд не должен превышать 30 бойцов.

## Цели

- Ограничить 30 бойцами создаваемые на старте `InitialSquad*` профиля NoMaps.
- Применить потолок к окончательному списку шаблонов после генерации и `BodyCount`.
- Не менять размеры и генерацию профиля с `jazz-maps`.

## Non-goals

- Изменение количества стартовых отрядов/иконок на satellite-карте.
- Изменение `StartingManpower`, `ManpowerCapacity` или темпа рекрутинга.
- Увеличение меньших managed-size bands NoMaps до 30.
- Ограничение будущих патрулей, конвоев, QRF и иных динамических отрядов.
- Принудительное удаление бойцов из уже существующих отрядов сохранения.
- Изменение `EnemySquadDef` или generated data в `jazz-units`.

## Требования

- `JAZZ-COMPAT-009-REQ-001` — при активном `JAZZ Vanilla Maps` вызов
  `GenerateUnitsFromTemplates` с `base_session_id`, начинающимся на `InitialSquad`,
  получает не более первых 30 `unit_template_ids`.
- `JAZZ-COMPAT-009-REQ-002` — cap стоит после `GenerateRandEnemySquadUnits` и
  `GameRuleBodyCountModifier`, поэтому ограничивает окончательный создаваемый состав.
- `JAZZ-COMPAT-009-REQ-003` — усечение детерминировано, сохраняет первые 30
  элементов и не мутирует исходную таблицу вызывающего кода.
- `JAZZ-COMPAT-009-REQ-004` — при загруженном `jazz-maps` (`FhNNYd`) wrapper
  делегирует базовой функции без изменения состава; не-`InitialSquad*` вызовы тоже неизменны.
- `JAZZ-COMPAT-009-REQ-005` — существующие отряды сохранения не уменьшаются
  принудительно; ограничение действует при создании стартовых отрядов новой кампании.

## Инварианты и ограничения

- ModDef `7MsJ2Eq`, squad IDs, UnitData IDs и save schema не меняются.
- Порядок RNG-вызовов базового генератора не меняется; усечение выполняется после генерации.
- Базовая `GenerateUnitsFromTemplates` и wrap flags объявляются по strict `_G` contract.
- Текущие managed-size bands NoMaps (максимум 22) остаются без изменений.

## Acceptance criteria

- `JAZZ-COMPAT-009-AC-001` — static: `GenerateUnitsFromTemplates` имеет
  NoMaps- и `InitialSquad*`-gated cap `30` после всех модификаторов состава.
- `JAZZ-COMPAT-009-AC-002` — static: capped copy сохраняет порядок, не мутирует
  исходный список и базовая функция вызывается ровно один раз.
- `JAZZ-COMPAT-009-AC-003` — static: `FhNNYd` сохраняет no-op, динамические
  отряды, экономика и `JAZZ_LegionRoleSizeOverrideNoMaps` не меняются.
- `JAZZ-COMPAT-009-AC-004` — runtime/human: стартовый NoMaps squad из
  `SatelliteSector.InitialSquads` с диапазоном выше 30 и вариант с `BodyCount`
  дают не более 30 units на satellite; динамический squad не затрагивается.
- `JAZZ-COMPAT-009-AC-005` — static: technical, wiki, showcase RU/EN и override
  matrix описывают потолок и его границы.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: `jazz-nomaps` дополняет существующий wrapper
  `GenerateEnemySquad` узким wrapper для `GenerateUnitsFromTemplates`; сигнатуры
  и возвращаемые значения сохраняются. CommonLib 1.11 build 1059, commit
  `f023a0310e8e3c4dd2a8e5769fdb4ab09fd696ce`, эти символы не переопределяет.
- Saves: schema не меняется; уже созданные отряды не усекать.
- Network/determinism: новые RNG-вызовы отсутствуют; порядок результата сохраняется.
- Generated data: нет.
- Cross-package references: runtime-функции определяет `jazz/Code/Guardpost.lua`;
  data остаются в `jazz-units`.
- Rollback/recovery: удалить wrapper/cap helper из `NoMaps_Autonomy.lua`.

## План и ownership

- Пакет-владелец: `jazz-nomaps`.
- Runtime-владелец базовой генерации: `jazz` (`Code/Guardpost.lua`).
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: см. front matter.
- Exclusive resources: wrappers генерации стартового состава NoMaps.

## Решение владельца

- Статус: **approved**.
- Кто подтвердил: project-owner (chat 2026-08-06).
- Дата: 2026-08-06.
- Уточнение: речь о стартовых отрядах `InitialSquads`, которые подменяет
  `jazz-units`, не о manpower и не обо всех динамических отрядах.

## Evidence

- `JAZZ-COMPAT-009-AC-001`: `PASS (static)` — `python docs/tools/_verify_nomaps_squad_size_cap.py`: cap=30, `InitialSquad*` gate, wrapper после BodyCount.
- `JAZZ-COMPAT-009-AC-002`: `PASS (static)` — verifier подтверждает capped copy; diff review подтверждает один вызов base и отсутствие мутации input.
- `JAZZ-COMPAT-009-AC-003`: `PASS (static)` — verifier подтверждает отсутствие wrappers random/BodyCount и сохранение `StartingManpower=40`; `lShouldRun()` сохраняет maps no-op.
- `JAZZ-COMPAT-009-AC-004`: `BLOCKED (runtime/human)` — игра не запущена; нужен New Game smoke стартового состава >30 с обычным режимом и `BodyCount`.
- `JAZZ-COMPAT-009-AC-005`: `PASS (static)` — technical, override matrix, wiki, showcase RU/EN и tooling README синхронизированы; `git diff --check` PASS.
  Repository-wide `check-system-docs.ps1` остаётся `BLOCKED` на pre-existing baseline errors вне write set (missing skill manifests, file coverage и broken links).

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — current-state cap и save boundary.
- `docs/technical/override-matrix.md` — wrapper генерации InitialSquads в NoMaps.
- `docs/wiki/legion-global-ai.md` — игроковый потолок 30 для стартовых отрядов.
- `docs/showcase/ru/legion-strategy.md` и `docs/showcase/en/legion-strategy.md` — RU/EN витрина.
