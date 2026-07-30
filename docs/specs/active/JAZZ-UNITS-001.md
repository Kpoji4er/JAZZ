---
id: JAZZ-UNITS-001
status: implemented
owner: project-owner
systems:
  - units-progression-specializations
  - localization
repositories:
  - jazz-units
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz-units/Code/EliteEnemyNamesFuncs.lua
  - jazz-units/Code/Mercenary.lua
  - jazz-units/English.csv
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/Strings.csv
  - jazz/Localization/EnglishManual.csv
  - jazz/Localization/RussianManual.csv
  - jazz/docs/technical/systems/units-progression-specializations.md
  - jazz/docs/technical/compatibility.md
exclusive_resources:
  - localization ID 890000000001650
related_decisions:
  - none
approved_by: project-owner chat request 2026-07-28
---

# JAZZ-UNITS-001: Elite enemy names localization and Foreigners pool

## Проблема

`AddEliteEnemyNames` пишет в `EliteEnemyName.name` результат `_InternalTranslate`, а `BuildNameCombos` склеивает уже переведённые строки в `Untranslated`. Vanilla хранит `translate=true` поле как `T(...)`, и `GenerateEliteUnitName` копирует его в `unit.Name`. Из‑за запекания английские переводы first/last/nickname из CSV не попадают в имена элитных юнитов.

`eliteCategory = "Foreigners"` используется Adonis/Corazon elite UnitData, но пул `Foreigners` не регистрируется.

`jazz-units` metadata/`ModItemLocTable` ссылается на отсутствующий `English.csv`.

## Цели

- Сохранять локализуемые `T`/`T{}` в `EliteEnemyName.name`.
- Составные имена собирать через общий формат `<first> <last>` с вложенными T first/last.
- Не вводить отдельный Adonis/`Foreigners` пул.
- Сохранить `jazz-units/English.csv` для units loctable; канон переводов — главный `jazz/English.csv`.

## Non-goals

- Сокращение combinatorial размера пулов (~38k presets).
- Полная замена vanilla `GenerateEliteUnitName` (допускается **тонкая обёртка** после вызова — см. REQ-006).
- Вычитка google-draft английских имён.
- Отдельный Russian loctable для jazz-units.
- Алиас Maquis → Rebels.
- Миграция уже запечённых имён в existing saves (кроме sanitize при GatherSessionData для T-with-args в текущей сессии).

## Требования

- `JAZZ-UNITS-001-REQ-001` — `EliteEnemyName.name` остаётся T или T{} с вложенными T, без `_InternalTranslate`/`Untranslated` bake **на регистрации PlaceObj**.
- `JAZZ-UNITS-001-REQ-002` — составные имена используют один shared format ID `890000000001650` = `<first> <last>`.
- `JAZZ-UNITS-001-REQ-003` — nicknames проходят через тот же dedup, что и остальные имена.
- `JAZZ-UNITS-001-REQ-004` — отдельный пул `Foreigners`/Adonis не вводится в этом change set.
- `JAZZ-UNITS-001-REQ-005` — канонические `jazz/English.csv` и `jazz/Russian.csv` содержат format ID и все mod-only ID пулов имён; `jazz-units/English.csv` существует как loctable units и согласован с каталогом.
- `JAZZ-UNITS-001-REQ-006` — после `GenerateEliteUnitName` (и в `GatherSessionData`) `unit.Name` с `THasArgs` запекается в `Untranslated(_InternalTranslate(...))`, потому что `TToLuaCode` / save assert `not THasArgs(T)`. Пресет `EliteEnemyName.name` остаётся T/T{}.

## Инварианты и ограничения

- Префиксы id `JazzMerc_<Group>_NNN` и группы Legion/Rebels/Mercenary сохраняются.
- Deterministic порядок preset id по индексу списка сохраняется.
- Не менять save schema `gv_UsedEliteNames` (по-прежнему id пресета).
- Save/load: `unit.Name` не должен содержать T with format args.

## Acceptance criteria

- `JAZZ-UNITS-001-AC-001` — static: `EliteEnemyNamesFuncs.lua` не вызывает `_InternalTranslate` при PlaceObj name.
- `JAZZ-UNITS-001-AC-002` — static: `Mercenary.lua` не регистрирует `Foreigners`.
- `JAZZ-UNITS-001-AC-003` — static: `jazz/English.csv` содержит format ID и все mod-only ID пулов; `jazz-units/English.csv` существует под units loctable.
- `JAZZ-UNITS-001-AC-004`: `PASS (runtime/human)` — owner playtest accepted 2026-07-28; English UI — English elite names; Russian UI — Russian.
- `JAZZ-UNITS-001-AC-005` — static: обёртка `GenerateEliteUnitName` + `OnMsg.GatherSessionData` sanitize T-with-args; save path не получает `THasArgs` на `unit.Name`.
- `JAZZ-UNITS-001-AC-006` — runtime/human: save after elite spawn / hire session does not assert `(not THasArgs(T))` in `TToLuaCode`.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: восстанавливает контракт translate-able **preset** name как у vanilla EliteEnemyName; **assigned** `unit.Name` для combo T{} становится Untranslated (язык UI на момент выдачи/сейва).
- Saves: без bake save ломался на combo T{}; после bake — loadable. Already-baked strings remain.
- Network/determinism: порядок пула и InteractionRand("EliteName") не меняются намеренно.
- Generated data: нет.
- Cross-package: format ID и dual-language строки в jazz CSV; units English.csv.

## План и ownership

- Пакет-владелец: jazz-units (код имён, English.csv); jazz (shared loc ID + docs/catalog).
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: localization ID `890000000001650`

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (запрос сделать сразу, вопросы после)
- Дата: 2026-07-28
- Amend 2026-07-31: owner — обновить spec под save-bake обёртку (`REQ-006` / `AC-005`/`AC-006`).

## Evidence

- `JAZZ-UNITS-001-AC-001`: `PASS (static)` — `EliteEnemyNamesFuncs.lua` stores `name = EnemyName` (T/T{}); no bake in PlaceObj.
- `JAZZ-UNITS-001-AC-002`: `PASS (static)` — `Mercenary.lua` only registers `Mercenary`.
- `JAZZ-UNITS-001-AC-003`: `PASS (static)` — jazz English/Russian have format ID + mod-only name pools; 6 latin IDs absent are vanilla-overlap sources (Blood/Phantom/Combat/Ivan/Miner/Luc); units English.csv present for loctable.
- `JAZZ-UNITS-001-AC-004`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-UNITS-001-AC-005`: `PASS (static)` — `MakeSaveableUnitName` / `SanitizeEliteUnitNamesForSave` / wrap `GenerateEliteUnitName` + `GatherSessionData` in `EliteEnemyNamesFuncs.lua`.
- `JAZZ-UNITS-001-AC-006`: `BLOCKED (runtime/human)` — owner retest save after reload with elite/hired session.

## Documentation delta

- `docs/technical/systems/units-progression-specializations.md` — контракт T/T{} на пресете + bake на `unit.Name` для save.
- `docs/technical/compatibility.md` — units English.csv больше не missing.
