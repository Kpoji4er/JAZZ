---
id: JAZZ-STRATEGY-002
status: implemented
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

- изменение существующих `JAZZ_Legion_*` UnitData, их характеристик или экипировки;
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
| Regular squad cap | 7 (current; pilot was 6) |
| Role caps | garrison dynamic (important Legion sectors + 1), patrol 2, recon 1, qrf 1 |

> Экономика `$` / caps после пилота пересмотрены в [JAZZ-STRATEGY-006](JAZZ-STRATEGY-006.md)+; historical pilot values 250/500 и flat role costs выше сохранены только как контекст 002. Current Region defaults: start **12000**, capacity **120000**, role costs в `$` (Recon 8000 / Patrol 18000 / QRF 40000 / Garrison 120000).

Supply / shipment / tax / recruiter / manpower не входят в regular combat cap; logistics используют свои caps/cooldowns. Major response также вне regular cap (один active + cooldown).

Если recon завершает полный observation timeout и не обнаруживает player squad, Heat из `task.observed_sector` уменьшается на `ReconNoContactHeatReduction` ровно один раз с clamp `0..1000`. При обнаружении игрока создаётся report и это снижение не применяется. Region Heat этим событием напрямую не меняется.

### UI

- Role icon берётся по managed state role, а не только из потенциально устаревшего `squad.image`.
- Raw PNG path содержит `.png`; vanilla `_2`/`_s` к нему не добавляются.
- Поздний wrapper `GetSatelliteIconImages` устанавливается после загрузки остальных mod code и делегирует unmanaged context фактической предыдущей реализации.
- Текст задачи показывается отдельным сворачиваемым блоком под составом в `SquadRolloverMap`; заголовок отряда остаётся vanilla.
- Wrapper фактического `SquadWindow:CreateRolloverWindow` добавляет блок только для managed squad и обновляет его при `CycleSquadsInRollover`; unmanaged squad и rollover без ожидаемого контейнера остаются без изменений.
- `ReloadLua` не создаёт recursive wrapper chain.

## Требования

- `JAZZ-STRATEGY-002-REQ-001` — исправить фактические UI extension points без мутации persistent squad name: задача managed squad отображается отдельным блоком под составом, а не частью заголовка.
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
- `JAZZ-STRATEGY-002-AC-002` — rollover показывает отдельным блоком под составом локализованную роль, задачу, state и target; блок обновляется при переключении нескольких squad, unmanaged rollover не изменён.
- `JAZZ-STRATEGY-002-AC-003` — `ReloadLua`, повторное открытие satellite view и save/load не теряют icon/task и не создают recursion/error.
- `JAZZ-STRATEGY-002-AC-004` — четыре новых presets имеют диапазоны 8–12, 12–18, 15–25 и 25–40 и не содержат UnitData вне `JAZZ_Legion_*`.
- `JAZZ-STRATEGY-002-AC-005` — I7 создаёт новые garrison/patrol/recon, оба convoy role используют новый convoy, QRF/Major остаются на Legion JAZZ T2/T3.
- `JAZZ-STRATEGY-002-AC-006` — при regular cap **7** и role caps (garrison dynamic / patrol 2 / recon 1 / qrf 1) дополнительный spawn не списывает money.
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
7. после runtime-проверки подтвердил, что title-hook не показывает задачу, и потребовал отдельный task-блок рядом с составом отряда.

Статус: approved.

## Evidence

- `JAZZ-STRATEGY-002-AC-001`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-STRATEGY-002-AC-002`: `PASS (static vanilla hook audit)` / `PASS (runtime/human) - owner playtest accepted 2026-07-28` — `CreateRolloverWindow` добавляет отдельный сворачиваемый task-блок под `idCurrentSquadCont`, wrapper `UpdateMultiSquadSection` обновляет его при cycle; нужен runtime hover.
- `JAZZ-STRATEGY-002-AC-003`: `PASS (static wrapper ownership)` / `PASS (runtime/human) - owner playtest accepted 2026-07-28` — vanilla CreateRollover сохранён один раз через `rawget`, а install всегда ставит один JAZZ wrapper; нужен ReloadLua/save-load.
- `JAZZ-STRATEGY-002-AC-004`: `PASS (static)` — четыре presets в `jazz-units`, суммы слотов 8–12 / 12–18 / 15–25 / 25–40, только `JAZZ_Legion_*`.
- `JAZZ-STRATEGY-002-AC-005`: `PASS (static binding)` / `PASS (runtime/human)` — owner playtest accepted 2026-07-28; I7 и ErnieIsland ссылаются на новые ID; QRF/Major не переведены на новые presets.
- `JAZZ-STRATEGY-002-AC-006`: `PASS (static)` — `RegularSquadCap` default 7 in `Regions_Sectors.lua`; runtime owner playtest 2026-07-28 (cap was 6 at pilot; current=7) / docs sync 2026-07-29
- `JAZZ-STRATEGY-002-AC-007`: `PASS (static)` — diagnostics отдаёт caps/costs/active_counts; runtime чтение не подтверждено.
- `JAZZ-STRATEGY-002-AC-008`: `PASS (static audit jazz-units/jazz-maps)` / `PASS (editor)` — owner accepted 2026-07-28; strict generated sync: units/maps errors=0 warnings=0; 6 pre-existing warnings только в `jazz` (не STRATEGY-002).
- `JAZZ-STRATEGY-002-AC-009`: `PASS (static for STRATEGY-002 IDs)` / `OPEN (suite debt)` — 28 ID `1424`–`451` в обоих runtime CSV с переводами; suite-wide audit: needs Russian=26, needs English=24, collisions against Game.csv=66 (pre-existing, не эти ID).
- `JAZZ-STRATEGY-002-AC-010`: `PASS (static)` — technical + wiki delta записаны; human review wiki открыт.
- `JAZZ-STRATEGY-002-AC-011`: `PASS (static state-machine)` / `PASS (runtime/human) - owner playtest accepted 2026-07-28` — `lTickRecon` снижает Heat без контакта один раз; нужен игровой тест contact/no-contact.

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — фактический rollover task-блок, caps, цены и recon Heat transition.
- `docs/technical/systems/units-progression-specializations.md` — четыре role-specific EnemySquad presets.
- `docs/technical/systems/legion-units-equipment-tiers.md` — использование Legion UnitData pool новыми составами (38 IDs incl. Recruit after 004).
- `docs/technical/compatibility.md` — save/reload и late-wrapper contract.
- `docs/technical/override-matrix.md` — фактические UI collision surfaces.
- `docs/technical/testing.md` — runtime smoke profile I7.
- `docs/wiki/legion-global-ai.md` — наблюдаемые игроком роли, задачи, размеры, лимиты и Heat.
