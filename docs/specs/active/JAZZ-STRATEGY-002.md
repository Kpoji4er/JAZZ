---
id: JAZZ-STRATEGY-002
status: approved
owner: project-owner
systems:
  - legion-global-ai
  - enemy-squads
  - satellite-ui
repositories:
  - jazz
  - jazz-maps
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-002.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/items.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/Strings.csv
  - jazz/Localization/RussianManual.csv
  - jazz/Localization/EnglishManual.csv
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/technical/testing.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/units-progression-specializations.md
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz/docs/wiki/README.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz-maps/items.lua
  - jazz-units/items.lua
  - jazz-units/metadata.lua
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
  - ModItemRegion:ErnieIsland
  - SatelliteSector:I7
  - EnemySquads:LegionGlobalAI_Garrison
  - EnemySquads:LegionGlobalAI_Patrol
  - EnemySquads:LegionGlobalAI_Recon
  - EnemySquads:LegionGlobalAI_Convoy
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-002: видимые задачи и ролевые отряды Global AI Легиона

## Проблема

Runtime-приёмка пилота `JAZZ-STRATEGY-001` выявила два UI-дефекта:

- `SquadWindow:CreateRolloverWindow` строит контекст напрямую из `self.context`, поэтому override `SquadWindow:GetRolloverText` не изменяет штатный `SquadRolloverMap`;
- позднее загружаемый `Code/POI Extension.lua` заменяет `GetSatelliteIconImages`, а role-image пути не содержат фактическое расширение `.png`, поэтому на карте остаётся стандартная иконка.

Кроме того, пилот переиспользует общие EnemySquad presets, размеры и составы которых не выражают стратегическую роль отряда. Владелец потребовал отдельные Legion-only составы: patrol 10–20, recon 8–12, convoy 10–30 и garrison 20–50 бойцов, с различающейся стоимостью.

## Цели

- показывать live-задачу managed-отряда в штатном rollover без изменения постоянного `SatelliteSquad.Name`;
- показывать семь существующих role icons на карте, после save/load и после `ReloadLua`;
- добавить четыре отдельные EnemySquad definitions только из `JAZZ_Legion_*`;
- привязать I7 к новым garrison/patrol/recon presets, а supply/diamond convoy — к общему convoy preset;
- развести цены ролей пропорционально размеру и назначению;
- при завершении разведки без контакта один раз снижать Heat наблюдаемого сектора;
- показывать caps и active counts в `JAZZ_LegionAIGetDiagnostics()`;
- локализовать новые player-facing строки одновременно на русский и английский;
- добавить игроковую wiki и воспроизводимый runtime smoke test.

## Non-goals

- изменение 37 существующих `JAZZ_Legion_*` UnitData, их характеристик или экипировки;
- изменение карт, `jazz-maps/Maps/**`, autoresolve-формул или tactical AI;
- включение Global AI вне `ErnieIsland`/`I7`;
- новые QRF и Major-response presets: они продолжают использовать существующие `LegionJAZZSquadT2/T3`, уже состоящие из нового Legion pool;
- изменение общего cap регулярных отрядов или role caps.

## Утверждённый контракт

### Составы

| ID | Роль | Итоговый диапазон | Ограничение пула |
|---|---|---:|---|
| `LegionGlobalAI_Recon` | recon | 8–12 | только `JAZZ_Legion_Flanker*`, стрелки и один командир |
| `LegionGlobalAI_Patrol` | patrol | 12–18 | только `JAZZ_Legion_*`, мобильное смешанное отделение |
| `LegionGlobalAI_Convoy` | supply/shipment | 15–25 | только `JAZZ_Legion_*`, охрана колонны |
| `LegionGlobalAI_Garrison` | garrison | 25–40 | только `JAZZ_Legion_*`, усиленная оборона с тяжёлой поддержкой |

Каждый `EnemySquadUnit` использует только public ID с префиксом `JAZZ_Legion_`. Минимумы и максимумы всех строк preset в сумме обязаны давать указанный итоговый диапазон.

### Экономика и лимиты

| Параметр | Значение |
|---|---:|
| Starting supply / capacity | 250 / 500 |
| Recon cost | 50 |
| Patrol cost | 90 |
| QRF cost | 140 |
| Garrison cost | 180 |
| Supply convoy cargo/reserve cost | 150 |
| Major response cost | 300 |
| Recon no-contact sector Heat reduction | 50 |
| Regular squad cap | 6 |
| Role caps | garrison 2, patrol 2, recon 1, qrf 1 |

Supply и shipment не входят в regular cap; одновременно разрешено не более одного отряда каждой convoy-role на регион/аванпост. Major response также живёт вне regular cap и ограничен одним active response и cooldown.

Если recon завершает полный observation timeout и не обнаруживает player squad, Heat из `task.observed_sector` уменьшается на `ReconNoContactHeatReduction` ровно один раз с clamp `0..1000`. При обнаружении игрока создаётся report и это снижение не применяется. Region Heat этим событием напрямую не меняется.

### UI

- Role icon берётся по managed state role, а не только из потенциально устаревшего `squad.image`.
- Raw PNG path содержит `.png`; vanilla `_2`/`_s` к нему не добавляются.
- Поздний wrapper `GetSatelliteIconImages` устанавливается после загрузки остальных mod code и делегирует unmanaged context фактической предыдущей реализации.
- Текст задачи добавляется через `TFormat.SquadNameColored`, который реально вызывается `SquadRolloverMap`; unmanaged squad делегируется vanilla/JAZZ predecessor.
- `ReloadLua` не создаёт recursive wrapper chain.

## Требования

- `JAZZ-STRATEGY-002-REQ-001` — исправить фактические UI extension points без мутации persistent squad name.
- `JAZZ-STRATEGY-002-REQ-002` — все семь role icons используют существующие файлы `SquadsIcons/Enemy/*.png`.
- `JAZZ-STRATEGY-002-REQ-003` — четыре новых EnemySquad IDs принадлежат `jazz-units` и содержат только `JAZZ_Legion_*`.
- `JAZZ-STRATEGY-002-REQ-004` — размеры новых presets находятся внутри утверждённых диапазонов.
- `JAZZ-STRATEGY-002-REQ-005` — I7 и ErnieIsland ссылаются на новые role presets без изменения Maps content.
- `JAZZ-STRATEGY-002-REQ-006` — цены и starting supply соответствуют утверждённой таблице.
- `JAZZ-STRATEGY-002-REQ-007` — diagnostics сообщает caps и active counts.
- `JAZZ-STRATEGY-002-REQ-008` — task rollover имеет полные Russian/English runtime translations с одинаковым множеством mod-only ID.
- `JAZZ-STRATEGY-002-REQ-009` — generated layers `items.lua`/`metadata.lua` согласованы и не перезаписывают новую конфигурацию при editor round-trip.
- `JAZZ-STRATEGY-002-REQ-010` — recon без контакта один раз снижает Heat наблюдаемого сектора на data-driven величину, а recon с контактом Heat не снижает.

## Acceptance criteria

- `JAZZ-STRATEGY-002-AC-001` — managed squad каждого role показывает свой PNG вместо `enemy_squad`.
- `JAZZ-STRATEGY-002-AC-002` — rollover показывает локализованную роль, задачу, state и target; unmanaged rollover не изменён.
- `JAZZ-STRATEGY-002-AC-003` — `ReloadLua`, повторное открытие satellite view и save/load не теряют icon/task и не создают recursion/error.
- `JAZZ-STRATEGY-002-AC-004` — четыре новых presets имеют диапазоны 8–12, 12–18, 15–25 и 25–40 и не содержат UnitData вне `JAZZ_Legion_*`.
- `JAZZ-STRATEGY-002-AC-005` — I7 создаёт новые garrison/patrol/recon, оба convoy role используют новый convoy, QRF/Major остаются на Legion JAZZ T2/T3.
- `JAZZ-STRATEGY-002-AC-006` — при regular cap 6 и role caps 2/2/1/1 дополнительный spawn не списывает supply.
- `JAZZ-STRATEGY-002-AC-007` — diagnostics возвращает конфигурационные caps и фактические active counts.
- `JAZZ-STRATEGY-002-AC-008` — strict generated audit не добавляет ошибок/warnings в `jazz-units` и `jazz-maps`; editor round-trip отдельно зафиксирован.
- `JAZZ-STRATEGY-002-AC-009` — localization audit сообщает `needs Russian=0`, `needs English=0`, без ID collisions и с одинаковыми ID в `Russian.csv`/`English.csv`.
- `JAZZ-STRATEGY-002-AC-010` — wiki и technical docs описывают фактические роли, размеры, цены, лимиты и шаги проверки.
- `JAZZ-STRATEGY-002-AC-011` — после observation timeout без player squad Heat наблюдаемого сектора уменьшается на 50 ровно один раз; при обнаружении player squad значение не уменьшается.

## Impact и совместимость

- **Runtime/UI:** меняются late-bound UI wrappers и recon state transition, но persistent GameVar schema и public squad IDs не переименовываются.
- **Generated data:** добавляются четыре `EnemySquads` resource presets в `jazz-units`; Region и I7 получают новые cross-package ссылки.
- **Saves:** существующие managed squads получают исправленную role image при reconciliation; task/state сохраняются без миграции schema.
- **Network/determinism:** no-contact Heat mutation выполняется только на существующем hourly deterministic scheduler; weighted lists остаются generated preset data.
- **Localization:** новые player-facing T IDs входят одновременно в русскую и английскую runtime-таблицы.
- **Assets:** бинарные PNG не меняются; исправляется только exact repository-relative path.

## Инварианты и ограничения

- Не изменять `jazz-maps/Maps/**`.
- Не переименовывать существующие UnitData/EnemySquad IDs.
- Не включать vanilla Legion UnitData в новые role presets.
- Не менять GameVar schema: составы и цены являются static config.
- Сохранить детерминированный выбор squad definition и unit weighted lists.
- Не закрывать runtime/human AC статическим анализом.
- Existing save reconciles role image и продолжает ссылаться на squad state по `UniqueId`.

## План и ownership

1. `jazz` — исправить UI extension points, diagnostics, цены и recon no-contact Heat.
2. `jazz-units` — добавить четыре EnemySquad resource presets только из `JAZZ_Legion_*`.
3. `jazz` + `jazz-maps` — связать Region/I7 с новыми public squad IDs.
4. `jazz` — обновить Russian/English localization, technical и wiki.
5. Выполнить static, generated, localization и documentation audits; runtime/human evidence оставить открытым до повторного теста владельца.

Runtime-владелец — `jazz`; владелец EnemySquads/UnitData — `jazz-units`; владелец sector authoring I7 — `jazz-maps`; владелец PNG — `jazz`.

## Решение владельца

26 июля 2026 года владелец проекта:

1. подтвердил наличие лимитов и потребовал сделать их проверяемыми;
2. сообщил runtime-дефект: managed squads имеют стандартные иконки, а задача в rollover не видна;
3. потребовал отдельные фракционные составы ролей только из нового Legion pool;
4. утвердил диапазоны patrol 10–20, recon 8–12, convoy 10–30 и garrison 20–50;
5. потребовал различающуюся стоимость ролей.
6. уточнил, что разведка без обнаруженного врага должна снижать Heat сектора.

Статус: approved.

## Evidence

- `JAZZ-STRATEGY-002-AC-001`: `BLOCKED` — ожидает реализацию и повторный runtime screenshot.
- `JAZZ-STRATEGY-002-AC-002`: `BLOCKED` — ожидает реализацию и runtime hover.
- `JAZZ-STRATEGY-002-AC-003`: `BLOCKED` — ожидает ReloadLua/save-load test.
- `JAZZ-STRATEGY-002-AC-004`: `BLOCKED` — ожидает generated presets и статический подсчёт.
- `JAZZ-STRATEGY-002-AC-005`: `BLOCKED` — ожидает cross-package binding и runtime spawn.
- `JAZZ-STRATEGY-002-AC-006`: `BLOCKED` — runtime cap test обязателен.
- `JAZZ-STRATEGY-002-AC-007`: `BLOCKED` — ожидает diagnostics change.
- `JAZZ-STRATEGY-002-AC-008`: `BLOCKED` — ожидает generated audit/editor round-trip.
- `JAZZ-STRATEGY-002-AC-009`: `BLOCKED` — ожидает localization audit/export.
- `JAZZ-STRATEGY-002-AC-010`: `BLOCKED` — ожидает documentation delta.
- `JAZZ-STRATEGY-002-AC-011`: `BLOCKED` — ожидает static state-machine check и runtime no-contact/contact test.

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — фактические UI hooks, caps, цены и recon Heat transition.
- `docs/technical/systems/units-progression-specializations.md` — четыре role-specific EnemySquad presets.
- `docs/technical/systems/legion-units-equipment-tiers.md` — использование 37-unit pool новыми составами.
- `docs/technical/compatibility.md` — save/reload и late-wrapper contract.
- `docs/technical/override-matrix.md` — фактические UI collision surfaces.
- `docs/technical/testing.md` — runtime smoke profile I7.
- `docs/wiki/legion-global-ai.md` — наблюдаемые игроком роли, задачи, размеры, лимиты и Heat.
