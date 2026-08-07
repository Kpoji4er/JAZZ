---
id: JAZZ-QUESTS-002
status: approved
owner: project-owner
systems:
  - maps-quests
  - sector-transfer
repositories:
  - jazz
  - jazz-maps
risk: high
generated_data: true
runtime_validation: required
write_set:
  - docs/specs/active/JAZZ-QUESTS-002.md
  - docs/tools/_audit_maps_vanilla_quest_sectors.py
  - docs/tools/_apply_maps_vanilla_quest_sector_remap.py
  - docs/tools/README.md
  - docs/technical/maps/sector-transfer.md
  - docs/technical/maps/data/sector-transfer.csv
  - docs/technical/systems/maps-quests-dialogue.md
  - docs/technical/systems/maps-quests-content-catalog.md
  - docs/wiki/grand-chien-map.md
  - docs/showcase/ru/grand-chien-map.md
  - docs/showcase/en/grand-chien-map.md
  - ../jazz-maps/items.lua
  - ../jazz-maps/metadata.lua
  - ../jazz-maps/ModTextsMaps.csv
exclusive_resources:
  - jazz-maps/items.lua
  - jazz-maps/metadata.lua
  - jazz-maps/ModTextsMaps.csv
  - localization write set for remapped SectorName / journal strings that change SourceText
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-QUESTS-002: ванильные квесты под sector remap (maps-only)

## Проблема

Профиль **с maps** переносит ванильные landmark-сектора на новую сетку
(`docs/technical/maps/sector-transfer.md`, `sector_bottomright = P32`).
В `jazz-maps` лежит полный clone vanilla `ModItemQuestsDef` / conversations /
sector events, но многие квесты всё ещё ссылаются на **старые HotDiamonds ID**.

Следствия:

- journal / `SectorName('…')` / `QuestBadgePlacement.Sector` указывают на чужой
  или пустой сектор;
- TCE / `PlayerIsInSectors` / `requiredSectors` / `sector_id` не срабатывают на
  фактической карте;
- игрок в профиле maps не может нормально пройти материковые vanilla-цепочки.

Baseline inventory (`docs/tools/_audit_maps_vanilla_quest_sectors.py`,
2026-08-07): **32** vanilla quest clone’а с stale landmark refs, плюс отдельные
overload-кейсы (crocodile journal `H14` → `P17`).

`JAZZ-QUESTS-001` уже починил узкий Ernie-срез (`RescueHerMan`→J7,
`ReduceCrocodileCampStrength`→P17) и явно оставил «переработку всех
vanilla-квестов» вне scope. Этот спек закрывает отложенный remap-контракт.

## Цели

- Все **логико-секторные** ссылки затронутых vanilla quest’ов в `jazz-maps`
  указывают на authored maps-сектора из канонической таблицы трансфера (+
  известные runtime overrides).
- Journal / badge / `SectorName` тексты согласованы с теми же ID в RU и EN
  runtime (через `ModTextsMaps.csv` и при необходимости jazz loc tables).
- Правки живут **только в `jazz-maps`** (+ docs/tools в `jazz`), чтобы профиль
  **jazz-nomaps** продолжал использовать vanilla HotDiamonds ID без поломки.
- Wave A и Wave B закрываются **одним** change set.
- Появится идемпотентный apply + static audit, повторяемый после editor dump.

## Non-goals

- Любые правки `jazz-nomaps`, vanilla HotDiamonds ID или core `jazz` runtime
  ради remap (кроме уже существующего shared crocodile crash-guard — не
  переоткрывать).
- Новые custom Ernie-квесты, Barry Seal, smoke matrix `JAZZ-QUESTS-001`.
- Полная переработка сюжета / диалогов / баланса квестов «по вкусу».
- Полный redesign World Flip / расширение баз фракций (отдельный будущий
  scope; этот спек только sector-ID remap).
- Массовый обход `Maps/**/objects.lua` без точечного адреса на конкретный
  quest/marker.
- Remap Ernie-local **maps I2** и custom `Jazz_*` / `JAZZ_*` квестов
  (доктор / дорога). Исключение: vanilla `04_Betrayal` I3 → J7 по решению
  владельца (временный долг до redesign World Flip).
- Слепое превращение всех `H14` в `P17`: Fleatown mine — это `H7→H14`;
  Camp du Crocodile — отдельный `H14→P17`.
- Sheet stub `I3→M7` (использовать runtime Emerald Coast `J7`).
- Strategy / Global AI region defs (`STRATEGY-020+`), кроме случая, когда quest
  gate буквально зависит от sector ID внутри QuestsDef.

## Канон remap (нормативный)

Источник: `docs/technical/maps/sector-transfer.md` + runtime overrides.
Apply использует **пары таблицы как есть** (включая `B16→D22`, `D10→F23`).

| vanilla | maps | Landmark / note |
| --- | --- | --- |
| A2 | A4 | Diamond Red |
| A11 | B15 | Nowhere farm |
| A20 | B28 | Eagle’s Nest / Major HQ |
| B2 | C6 | Port near Diamond Red |
| B12 | A25 | Drachenberg mine |
| B13 | A26 | Landsbach |
| B16 | D22 | Rift outpost (sheet; sector may be stub/missing until authored) |
| C5 | D9 | Poacher camp |
| C7 | E15 | Pantagruel outskirts |
| D7 | E15 | Pantagruel hub |
| D8 | E16 | Pantagruel hospital / carnival |
| D10 | F23 | Grand Prix outpost (sheet; not runtime `D18` substitute) |
| E9 | F13 | Refugee camp |
| F5 | G9 | Côte d’Azur |
| H2 | I5 | Ernie village |
| H3 | I6 | The Rust |
| H4 | I7 | Fort L’Eau Bleu |
| H7 | H14 | Fleatown-area mine |
| I3 | **J7** | Emerald Coast runtime (sheet M7 — stub; не использовать) |
| H14*(crocodile)* | **P17** | Camp du Crocodile (suite/Global AI; не mine H14) |

### Overload / keep rules

1. **H14 overload:** mine (`H7→H14`) ≠ crocodile (`H14→P17`). Применять только
   по quest-контексту (`TreasureHunting` / mine income → H14; `Elliot` /
   crocodile journal → P17; `ReduceCrocodile*` уже в QUESTS-001).
2. **I1 overload:** sheet Flag Hill `I1→K4`; suite start `I1→M1`. Не смешивать.
3. **Custom Ernie keep:** `Jazz_*` / `JAZZ_*` с maps-local `I2`/`I3` не
   трогать. Vanilla `04_Betrayal`: owner-approved temporary `I3→J7` даже если
   соседний World Flip уже спавнит Emerald на J7; полный World Flip / faction
   bases — отдельный будущий спек.
4. **Sheet targets `D22`/`F23`:** remap quest refs по таблице. Не подменять на
   runtime `D18`. Если `ModItemSector` отсутствует — зафиксировать в evidence
   и technical notes как known gap / stub debt, не откатывать remap на
   vanilla ID.

## Scope delivery

Wave A и Wave B выполняются **вместе** в одном change set.

### Wave A — landmark quests

- `DiamondRed` (A2→A4)
- `RefugeeBlues`, `FaithHealing`, `JoseFamily`, `Evidence`, `Sanatorium` (E9→F13)
- `HunterHunted`, `NeverHitAGirl` (C5→D9; Flay outpost `A20→B28`)
- `MiddleOfNowhere`, `MiddleOfXWhere` (A11→B15)
- `Landsbach`, `U-Bahn`, `U-Bahn_Helpers` (B12→A25, B13→A26; diesel/outpost
  refs `D10→F23` где это vanilla Grand Prix landmark)
- `TreasureHunting` (H7→H14 mine)
- `Elliot` crocodile texts leftover H14→P17 if any remain
- `05_TakeDownMajor` (A20→B28; outpost list D10→F23 where applicable)
- Pantagruel cluster: `YoungHearts`, `RebelManifesto`, `PantragruelWatch`,
  `PantagruelRebels`, `PantagruelLostAndFound`, `PantagruelDramas`,
  `PantagruelClinic`, `Smiley`, `RescueBiff` (C7/D7/D8 → E15/E16)

### Wave B — campaign / helpers / mail

- `04_Betrayal` (E9→F13; I3→J7 temporary; keep already-correct I5/I6/I7/J7/M*
  where already remapped)
- `CorazonCaptureMine`, `PierreDefeated`, `Larry`, `TheTwelveChairs`,
  `GlobalCivilians`, `_GroupsAttacked`, `Emails`
- Любые conversation lines в тех же квестах с `SectorName` / sector gates

### Docs + smoke

- technical / wiki / showcase sync
- targeted runtime smoke по ключевым landmarks Wave A/B

После apply: audit exit 0 для in-scope vanilla quest IDs, кроме явного
allowlist residual (только custom Ernie keep / documented stub debt).

## Требования

- `JAZZ-QUESTS-002-REQ-001` — пакет-владелец всех quest/conversation/sector
  remap-правок — `jazz-maps`. Core `jazz` и `jazz-nomaps` не получают remap
  sector ID’ов для vanilla quests.
- `JAZZ-QUESTS-002-REQ-002` — канон пар vanilla→maps фиксируется в
  `sector-transfer.md` / CSV; runtime override Emerald Coast `I3→J7` и
  crocodile `H14→P17` документируются там же явными notes. Пары
  `B16→D22` и `D10→F23` применяются по таблице без substitute на `D18`.
- `JAZZ-QUESTS-002-REQ-003` — для каждого in-scope `ModItemQuestsDef` заменить
  stale landmark ID в: `QuestBadgePlacement.Sector`, `PlayerIsInSectors`,
  `requiredSectors`, `sector_id` / `SectorID`, quest `custom_code` /
  `gv_Sectors.*`, и связанных conversation effects/conditions.
- `JAZZ-QUESTS-002-REQ-004` — журнальные и UI-строки с `<SectorName('OLD')>` /
  hardcoded old ID обновляются до maps ID; RU/EN остаются согласованными
  (ModTextsMaps + jazz runtime CSV при изменении SourceText).
- `JAZZ-QUESTS-002-REQ-005` — overload rules соблюдаются apply/audit:
  H14 mine vs crocodile; custom Ernie I2/I3 keep; Betrayal I3→J7 temporary;
  table pairs including D22/F23; запрет blind global replace без quest scope.
- `JAZZ-QUESTS-002-REQ-006` — публичные quest ID (`DiamondRed`, `Landsbach`, …)
  не переименовываются; меняются только sector references и тексты.
- `JAZZ-QUESTS-002-REQ-007` — идемпотентный
  `_apply_maps_vanilla_quest_sector_remap.py` + inventory/contract audit;
  `--check` проходит после apply.
- `JAZZ-QUESTS-002-REQ-008` — один change set закрывает Wave A **и** Wave B:
  0 stale landmark refs для in-scope vanilla quest list (кроме documented
  allowlist).
- `JAZZ-QUESTS-002-REQ-009` — documentation delta: technical maps/quests +
  player wiki/showcase grand-chien-map отражают maps-only remap ownership,
  table pairs и temporary World Flip debt.

## Инварианты и ограничения

- Профиль nomaps не должен начать требовать maps sector IDs.
- Не ломать уже исправленные QUESTS-001 контракты (J7 Herman, P17 crocodile
  unlock, Ernie custom quests `Jazz_*`).
- Не создавать полноценный mainland content «заодно»; отсутствие
  `ModItemSector` у D22/F23 — documented debt, не повод вернуть vanilla ID.
- Generated transaction: `items.lua` + `metadata.lua` + `ModTextsMaps.csv`
  (+ companions только если editor dump их держит для затронутых preset’ов).
- Старые сохранения с уже записанными quest vars не обязаны «починить»
  прошедшие outcomes; новая кампания — канон acceptance.
- Не смешивать этот remap с redesign World Flip / faction bases.

## Acceptance criteria

- `JAZZ-QUESTS-002-AC-001` — `_audit_maps_vanilla_quest_sectors.py` после
  apply показывает 0 stale landmark refs для Wave A+B vanilla quest IDs;
  custom Ernie keep и crocodile special-case роутятся корректно.
- `JAZZ-QUESTS-002-AC-002` — `DiamondRed`: badges/gates/journal указывают A4;
  вход/контроль шахты на A4 продвигает квест (runtime smoke).
- `JAZZ-QUESTS-002-AC-003` — `RefugeeBlues` (+ связанные E9 notes): F13; нет
  активных badge/TCE на E9.
- `JAZZ-QUESTS-002-AC-004` — `Landsbach`: A25/A26 вместо B12/B13; Grand Prix /
  diesel landmark refs используют F23 по таблице.
- `JAZZ-QUESTS-002-AC-005` — `HunterHunted`: C5→D9; `TCE_FlayHunting`
  Major HQ `A20→B28` (Орлиное гнездо).
- `JAZZ-QUESTS-002-AC-006` — `Elliot`/crocodile использует P17; mine quests
  (`TreasureHunting` и аналоги) используют H14 как mine.
- `JAZZ-QUESTS-002-AC-007` — Pantagruel cluster: C7/D7→E15, D8→E16 в logic и
  journal; нет регрессии уже валидных E15/E16 ссылок.
- `JAZZ-QUESTS-002-AC-008` — `05_TakeDownMajor` / Major HQ refs: A20→B28.
- `JAZZ-QUESTS-002-AC-009` — `04_Betrayal`: E9→F13; I3→J7 (temporary owner
  debt); уже корректные I5/I6/I7/J7/M* не откатываются.
- `JAZZ-QUESTS-002-AC-010` — localization: нет `<missing translation>` /
  active ID collisions на изменённых строках; RU/EN ID sets совпадают.
- `JAZZ-QUESTS-002-AC-011` — `_validate_items_quick.py` для `jazz-maps` OK;
  apply `--check` idempotent; dirty Lua syntax на затронутых файлах OK.
- `JAZZ-QUESTS-002-AC-012` — в профиле **jazz-nomaps** (без maps) vanilla
  quest sector IDs не изменены этим change set.
- `JAZZ-QUESTS-002-AC-013` — docs/wiki/showcase grand-chien-map и technical
  quest catalog описывают maps-only remap ownership, table pairs включая
  D22/F23 debt и temporary Betrayal I3→J7.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: публичные quest ID сохраняются; меняются только
  sector bindings внутри maps clone’ов.
- Saves: новая кампания обязательна для полной проверки материковых цепочек;
  старые saves могут иметь badges/notes на старых ID до re-eval.
- Network/determinism: без нового RNG; host/client должны грузить один и тот
  же `jazz-maps` revision.
- Generated data: да — `jazz-maps` items/metadata/ModTexts.
- Cross-package: docs/tools в `jazz`; runtime quest data только `jazz-maps`.
  `jazz-units` / `jazz_assets` / `jazz-nomaps` вне write set.
- Rollback/recovery: git revert maps package + docs; nomaps профиль не
  затрагивается.
- Known debt: D22/F23 могут не иметь полного authored sector/map; World Flip
  Ernie I3→J7 временный до redesign фракционных баз.

## План и ownership

- Пакет-владелец: `jazz-maps` (quest/sector/conversation data).
- Docs/tools owner: `jazz`.
- Исполнитель: agent + owner approval.
- Reviewer: project-owner.
- Declared write set: см. frontmatter.
- Exclusive resources: `jazz-maps/items.lua`, `metadata.lua`,
  `ModTextsMaps.csv` на время apply; не параллелить с другими maps generated
  transactions.

### Manual / editor

1. После scripted apply — при необходимости один Mod Editor save, если editor
   state расходится с companion dump.
2. Runtime smoke ключевых landmarks Wave A/B на новой кампании (maps profile).
3. Sanity: nomaps profile boot + один vanilla quest landmark (H4/A20/H14
   crocodile) без maps remap.

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner
- Дата: 2026-08-07
- Решения:
  1. Wave A и Wave B — **одним** change set.
  2. `04_Betrayal` I3 → **J7** (Emerald Coast) временно; полный World Flip /
     расширение баз фракций — позже.
  3. Орлиное гнездо / Flay Major HQ: **A20 → B28**.
  4. Remap строго **по таблице** transfer, включая `B16→D22` и `D10→F23`
     (без substitute на runtime `D18`).

## Evidence

- `JAZZ-QUESTS-002-AC-001`: `PASS` (static) — `_audit_maps_vanilla_quest_sectors.py
  --strict` OK after Wave A+B apply (2026-08-07).
- `JAZZ-QUESTS-002-AC-002`…`AC-009`: `BLOCKED` — runtime/editor smoke.
- `JAZZ-QUESTS-002-AC-010`: `PASS` (static) — ModTextsMaps SectorName remapped
  with items.lua; no new jazz runtime CSV ID set change required (maps-owned
  texts).
- `JAZZ-QUESTS-002-AC-011`: `PASS` (static) — `_validate_items_quick.py
  ../jazz-maps` OK; apply `--check` idempotent (0 replacements).
- `JAZZ-QUESTS-002-AC-012`: `PASS` (static) — `jazz-nomaps` not in write set /
  no remapped quest IDs there.
- `JAZZ-QUESTS-002-AC-013`: `PASS` (docs) — sector-transfer, maps-quests
  technical pages, wiki + showcase RU/EN grand-chien-map, tools README.

## Documentation delta

- После реализации: `sector-transfer.md` (+ CSV notes для J7/P17 и
  D22/F23 debt), `maps-quests-dialogue.md`,
  `maps-quests-content-catalog.md`, `docs/wiki/grand-chien-map.md`,
  `docs/showcase/ru|en/grand-chien-map.md`, `docs/tools/README.md`.
- Не обещать в витрине «все mainland квесты polished» — только корректные
  sector bindings на maps grid и известный stub debt.
