---
id: JAZZ-UNITS-010
status: approved
owner: project-owner
systems:
  - units-progression-specializations
repositories:
  - jazz
  - jazz-units
risk: low
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-UNITS-010.md
  - jazz/Code/System_JA2_Nationalities.lua
  - jazz/metadata.lua
  - jazz/Icons/Flags/f_belgium.png
  - jazz/Icons/Flags/f_estonia.png
  - jazz/Icons/Flags/f_france.png
  - jazz/Icons/Flags/f_ireland.png
  - jazz/Icons/Flags/f_italy.png
  - jazz/Icons/Flags/f_metavira.png
  - jazz/Icons/Flags/f_romania.png
  - jazz/Icons/Flags/f_australia.png
  - jazz/Localization/Strings.csv
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/technical/systems/units-progression-specializations.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/design/mercs-ja12/flo.md
  - jazz/docs/design/mercs-ja12/gamos.md
  - jazz/docs/design/mercs-ja12/grace.md
  - jazz/docs/design/mercs-ja12/lucky.md
  - jazz/docs/design/mercs-ja12/colby.md
  - jazz-units/UnitData/Jazz_Flo.lua
  - jazz-units/UnitData/Jazz_Gamos.lua
  - jazz-units/UnitData/Jazz_Grace.lua
  - jazz-units/UnitData/Jazz_Lucky.lua
  - jazz-units/UnitData/Jazz_Colby.lua
  - jazz-units/items.lua
exclusive_resources:
  - jazz/metadata.lua
  - jazz-units/items.lua
  - localization-id-allocation
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-UNITS-010: флаги национальностей JA2

## Проблема

Ванильный список `MercNationalities` не содержит Australia, Belgium, Estonia, France, Ireland, Italy, Metavira и Romania. `TFormat.MercFlagImage` берёт иконку только из зарегистрированного пресета, поэтому у наёмников с этими id флаг на карточке пустой. Часть слотов ещё и записана не той страной относительно досье JA2: Лаки числится французом, хотя он бельгиец; Грейс — американкой, хотя она итальянка; Гамос — жителем Арулько, хотя боевое крещение у него на Метавире; Фло — американкой, хотя детство она провела в Коньяке.

## Цели

- Зарегистрировать национальности с флагами из поставленного набора и русскими/английскими названиями, плюс Австралию по отдельному флагу владельца.
- Показать флаг у Знатока, Зануды, Девина, Лоры, Гастона, Саймона, Вишеса, Лаки, Грейс, Гамоса, Фло и Колби.
- Оставить Эскимо на `Arulco`: он повстанец Арулько, отдельного флага для него в наборе нет.

## Non-goals

- Не менять ванильные пресеты и не подменять глобус Арулько.
- Не переписывать биографии, перки и условия найма.
- Не добавлять другие страны из JA2 сверх архива и отдельно присланного флага Австралии.

## Требования

- `JAZZ-UNITS-010-REQ-001` — пресеты `Australia`, `Belgium`, `Estonia`, `France`, `Ireland`, `Italy`, `Metavira`, `Romania` регистрируются в `Code/System_JA2_Nationalities.lua`, файл входит в `metadata.code`. У каждого есть DisplayName RU+EN и иконка `Icons/Flags/f_<id>.png` 128×80.
- `JAZZ-UNITS-010-REQ-002` — `Nationality` в companion и `items.lua` совпадает: Лаки `Belgium`, Грейс `Italy`, Гамос `Metavira`, Фло `France`, Колби `Australia`. Знаток и Зануда остаются `Estonia`, Девин `Ireland`, Лора `Romania`, Гастон, Саймон и Вишес `France`, Эскимо `Arulco`.

## Инварианты и ограничения

- Существующие id `USA`, `Arulco`, `Hungary` и африканский пул AME не переписываются.
- Публичные id юнитов не меняются.
- Сейвы не мигрируют поле `Nationality`: уже нанятый слот хранит старое значение до новой игры.

## Acceptance criteria

- `JAZZ-UNITS-010-AC-001` — static: восемь пресетов с иконками в коде и в `metadata.code`; поправленные национальности совпадают в `UnitData` и `items.lua`.
- `JAZZ-UNITS-010-AC-002` — runtime/human: на карточке найма у Лаки виден флаг Бельгии, у Грейс — Италии, у Гамоса — Метавиры, у Фло и Гастона — Франции, у Девина — Ирландии, у Лоры — Румынии, у Знатока и Зануды — Эстонии, у Колби — Австралии.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: новые id только в JAZZ; ванильные пресеты не трогаются.
- Saves: смена `Nationality` у уже нанятых Фло, Грейс, Гамоса и Лаки не переписывается загрузкой сейва.
- Network/determinism: нет.
- Generated data: `jazz-units/items.lua` и companion UnitData одной правкой поля `Nationality`.
- Cross-package references: пресеты живут в `jazz`, поле юнита в `jazz-units`.
- Rollback/recovery: удалить lua-пресеты, флаги и вернуть четыре строки `Nationality`.

## План и ownership

- Пакет-владелец пресетов и флагов: `jazz`. Поле `Nationality`: `jazz-units`.
- Исполнитель: текущая сессия.
- Reviewer: владелец проекта.
- Declared write set: frontmatter.
- Exclusive resources: `jazz/metadata.lua`, `jazz-units/items.lua`, выдача localization ID.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец проекта, запрос в этой сессии — поставить флаги из `1.zip` наёмникам JA2 без национальности, затем отдельно добавить Австралию.
- Дата: 2026-10-04.

## Evidence

- `JAZZ-UNITS-010-AC-001`: PASS — static. Восемь пресетов в `Code/System_JA2_Nationalities.lua` и строка в `metadata.code`; иконки 128×80; `items.lua` и companion совпадают у Фло, Гамоса, Грейс, Лаки и Колби.
- `JAZZ-UNITS-010-AC-002`: в игре не смотрел. Карточку найма нужно открыть после перезагрузки мода.

## Documentation delta

- `docs/technical/systems/file-coverage.md` и строка национальностей в `units-progression-specializations.md`.
- Frontmatter `flo.md`, `gamos.md`, `grace.md`, `lucky.md`, `colby.md`.
- Wiki и showcase не обещают конкретный флаг страны и не меняются.
