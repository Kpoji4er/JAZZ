---
id: JAZZ-LOC-002
status: approved
owner: project-owner
systems:
  - localization
  - player-facing-copy
repositories:
  - jazz
  - jazz-units
  - jazz-maps
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Localization/Strings.csv
  - Localization/RussianManual.csv
  - Localization/EnglishManual.csv
  - Localization/CopyReview.csv
  - Russian.csv
  - English.csv
  - Code/Regions_Sectors.lua
  - Code/System_RIS_Browser.lua
  - Code/SatelliteSquad.lua
  - CharacterEffect/*.lua
  - CharacterEffect/TraumaHeadMedium.lua
  - CharacterEffect/TraumaHeadHeavy.lua
  - InventoryItem/Reanimationsset.lua
  - InventoryItem/Sig550Custom.lua
  - ModTextsJazz.csv
  - items.lua
  - metadata.lua
  - Localization/Collisions.csv
  - ../jazz-units/items.lua
  - ../jazz-units/UnitData/Raider.lua
  - scripts/localization/audit-localization.ps1
  - ../jazz-units/English.csv
  - docs/tools/_audit_localization_copy_quality.py
  - docs/tools/_apply_localization_copy_edit.py
  - ../jazz-units/UnitData/*.lua
  - docs/tools/localization-copy-edits/*.csv
  - ../jazz-maps/items.lua
  - docs/tools/README.md
  - docs/specs/active/JAZZ-LOC-002.md
  - docs/tools/_pour_ja12_design_identity_bio.py
  - docs/technical/systems/localization.md
  - docs/technical/compatibility.md
  - docs/technical/testing.md
  - docs/technical/systems/strategy-squads-sectors.md
exclusive_resources:
  - jazz/Localization/Strings.csv
  - jazz/Localization/RussianManual.csv
  - jazz/Localization/EnglishManual.csv
  - jazz/Localization/CopyReview.csv
  - jazz/Russian.csv
  - jazz/English.csv
  - localization-id-range-890000000012000-890000000012099
  - jazz-units/English.csv
  - jazz-maps/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-LOC-002: редакторская вычитка игровых текстов

## Проблема

После массовой нормализации локализации все активные mod-only строки получили
русский и английский runtime-перевод, однако значительная часть английской
памяти осталась машинным черновиком. В русских и английских игровых текстах
также встречаются кальки, канцелярит, буквальные машинные конструкции, опечатки
и описания, которые трудно читать без знания внутренних терминов мода.

## Цели

- Проверить все активные player-facing строки рабочего каталога, не ограничиваясь
  заранее известными экранами или последними изменениями.
- Переписать неестественные русские и английские формулировки живым,
  контекстным языком без потери авторского голоса.
- Сверить фактические утверждения в подсказках, описаниях и досье с текущей
  реализацией и утверждёнными спецификациями.
- Оставить воспроизводимый реестр проверки и синхронные runtime-таблицы RU/EN.

## Non-goals

- Изменение механик, чисел баланса, AI, лута, состава юнитов или порядка загрузки.
- Изменение numeric localization ID, class/preset/entity ID либо исходного
  `SourceText` в Lua и generated data.
- Рекурсивный обход или правка `jazz-maps/Maps/`.
- Переписывание имён моделей оружия, калибров, placeholders и иных намеренных
  технических копий только ради отличия языков.
- Унификация авторских голосов персонажей в один нейтральный стиль.

## Требования

- `JAZZ-LOC-002-REQ-001` — единицей редакторской проверки считать активную
  строку `Localization/Strings.csv`; учитывать её контекст, пакет и locations.
- `JAZZ-LOC-002-REQ-002` — каждую активную строку с английской памятью
  `google-draft` проверить вручную: переписать либо явно принять и пометить
  `manual-reviewed-google`.
- `JAZZ-LOC-002-REQ-003` — проверить остальные активные строки автоматическими
  style-флагами и вручную разобрать каждый сработавший флаг; ложное срабатывание
  фиксировать в реестре проверки, а не исправлять слепой заменой.
- `JAZZ-LOC-002-REQ-004` — русский и английский текст должны звучать естественно
  в своём языке, сохранять смысл, тон, юмор и различимый голос говорящего.
- `JAZZ-LOC-002-REQ-005` — player-facing утверждения о возможностях, оружии,
  эффектах и правилах должны соответствовать текущему runtime и утверждённым
  спецификациям; при конфликте приоритет имеет фактическая реализация.
- `JAZZ-LOC-002-REQ-006` — не менять ID и `SourceText`; правки ограничить
  переводческими полями, памятью перевода, реестром проверки и синхронным
  экспортом `Russian.csv`/`English.csv`.
- `JAZZ-LOC-002-REQ-007` — сохранить точные множества placeholders, игровых
  тегов, управляющих последовательностей и значимых переносов строк.
- `JAZZ-LOC-002-REQ-008` — обе runtime-таблицы экспортировать из одного снимка
  каталога; множества активных mod-only ID должны совпадать.
- `JAZZ-LOC-002-REQ-009` — полезные инструменты аудита и применения правок
  сохранить в `docs/tools/` и описать в `docs/tools/README.md`.

## Инварианты и ограничения

- `Russian.csv` остаётся приоритетным источником русского runtime-текста;
  осознанные решения дублируются в русской памяти, когда это нужно для
  воспроизводимости.
- `EnglishManual.csv` остаётся приоритетной английской памятью; принятые
  машинные черновики больше не имеют статус `google-draft`.
- Технические токены, markup и имена параметров не переводятся без доказательства,
  что движок воспринимает их как обычный текст.
- Нельзя затрагивать посторонние незакоммиченные изменения, включая текущие
  правки `items.lua`.
- Каталог может содержать development-only или неактивную память; в обязательный
  проход входят активные строки текущего снимка.

## Acceptance criteria

- `JAZZ-LOC-002-AC-001` — реестр `Localization/CopyReview.csv` содержит решение
  для каждого активного ID текущего снимка и не содержит дубликатов ID.
- `JAZZ-LOC-002-AC-002` — среди активных строк нет английской памяти со статусом
  `google-draft`; каждая такая строка переписана либо помечена
  `manual-reviewed-google` после контекстной проверки.
- `JAZZ-LOC-002-AC-003` — style-аудитор сообщает ноль неразобранных флагов;
  принятые исключения перечислены в реестре.
- `JAZZ-LOC-002-AC-004` — локализационный аудит сообщает ноль коллизий,
  `needs Russian=0` и `needs English=0`.
- `JAZZ-LOC-002-AC-005` — `Russian.csv` и `English.csv` содержат одинаковое
  множество уникальных активных mod-only ID без лишних и пропущенных строк.
- `JAZZ-LOC-002-AC-006` — tag/placeholder/newline-аудит не находит повреждений
  относительно `SourceText`, кроме явно документированных языковых различий,
  не меняющих игровые токены.
- `JAZZ-LOC-002-AC-007` — независимый reviewer не находит блокирующих кальк,
  машинных конструкций или фактических расхождений в изменённых строках.
- `JAZZ-LOC-002-AC-008` — русский и английский UI smoke-test на clean start и
  существующем сохранении не показывает `<missing translation>`, обрезанных
  тегов или повреждённых многострочных полей.
- `JAZZ-LOC-002-AC-009` — фактический diff не выходит за declared write set и
  не включает посторонние изменения рабочего дерева.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: меняется только отображаемый перевод mod-only строк;
  ID, call sites и load order сохраняются.
- Saves: сохранённые class/preset IDs и игровое состояние не меняются.
- Network/determinism: игровая логика и RNG не меняются.
- Generated data: `items.lua` changes stay source-aware; companion pairs remain synchronized; `metadata.lua` changes only revision and `last_changes` per commit policy.
- Cross-package references: центральные runtime-таблицы продолжают обслуживать
  строки `jazz`, `jazz-units` и top-level `jazz-maps`; ownership Lua не меняется.
- Rollback/recovery: правки воспроизводимы из батчей `localization-copy-edits`
  и откатываются обычным revert файлов локализации.

## План и ownership

- Пакет-владелец: `jazz` владеет каталогом, памятью, runtime CSV и инструментами.
- Исполнитель: Codex.
- Reviewer: независимый Codex-agent и project-owner для runtime acceptance.
- Declared write set: frontmatter этой спецификации.
- Exclusive resources: центральный каталог, память и обе runtime-таблицы.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner прямым запросом пройти по всем игровым текстам
  мода, проверить качество человеческого языка и исправить проблемные места.
- Дата: 2026-08-06.

## Scope amendment after preflight

The initial inventory found structural runtime-table damage and active ID/source
collisions that would make a copy-only export lossy. This amendment supersedes the
blanket non-goal that prohibited all localization-ID, SourceText, and generated-data
changes. Only the enumerated repairs below are authorized; class, preset, entity,
gameplay, save, network, and load-order contracts remain unchanged.

- `JAZZ-LOC-002-REQ-010` - build the working catalog from the complete active graph
  (`items.lua` plus loaded `metadata.code` in all four canonical packages), excluding
  `jazz-maps/Maps/`; do not treat the old `Strings.csv` snapshot as complete.
- `JAZZ-LOC-002-REQ-011` - resolve the four active collisions and three Game.csv findings:
  use canonical R.I.S. UI IDs `890000000011000..011003`; allocate a separate free
  mod-only IDs for the Morphine queue badge and the corrected `Awaiting deployment`
  status; preserve the vanilla ` (Empty)` ID by parsing Game.csv without trimming source
  whitespace; align both trauma item/companion pairs;
  and match Raider's canonical vanilla source whitespace in both generated and
  companion copies.
- `JAZZ-LOC-002-REQ-012` - make `Region.DisplayName` a translatable editor property
  and provide RU/EN text for every active region without changing region IDs or any
  gameplay property.
- `JAZZ-LOC-002-REQ-013` - export structurally clean runtime CSV files containing only
  `sep=,` followed by five-column data records: no embedded headers, merge markers,
  two/three-column fragments, or continuation debris.
- `JAZZ-LOC-002-REQ-014` - synchronize the loaded package-local
  `../jazz-units/English.csv` so it cannot override the central approved English text.
- `JAZZ-LOC-002-REQ-015` - replace active WIP/player-facing placeholders from approved
  design sources; an unresolved placeholder must be recorded as owner-blocked rather
  than silently accepted.
- `JAZZ-LOC-002-REQ-016` - correct the factual SIG 500 source typo to SIG 550
  in the companion, generated ModItem, editor text export, catalog, and both
  languages without changing the localization ID or weapon behavior.

Additional invariants:

- Source-aware edits must preserve unrelated dirty hunks in shared generated files.
- New localization IDs are restricted to the declared `890000000012000..012099` range
  and must be absent from Game.csv and every loaded JAZZ package before allocation.
- The broad generated-data audit baseline is 488 errors and 27 warnings before this
  change; targeted pairs must synchronize and the broad baseline must not increase.
- Package metadata registration fields stay unchanged; package revision and `last_changes` follow the repository commit policy.

Additional acceptance criteria:

- `JAZZ-LOC-002-AC-010` - active, Game.csv, and Russian priority collisions are zero.
- `JAZZ-LOC-002-AC-011` - both runtime tables have exactly one separator record and
  only five-column localization rows; embedded headers/markers/malformed rows are zero.
- `JAZZ-LOC-002-AC-012` - targeted `items.lua`/companion source pairs match; the broad
  sync baseline does not exceed 488 errors and 27 warnings.
- `JAZZ-LOC-002-AC-013` - every active region name has RU and EN output while region
  IDs and gameplay properties are byte-for-byte unchanged.
- `JAZZ-LOC-002-AC-014` - Sig550Custom companion, `items.lua`, and
  `ModTextsJazz.csv` use SIG 550 and the source-aware RU/EN rows match it.

Preflight evidence: 20,893 active `T` uses, 15,160 active IDs, 11,465 in-memory
mod-only catalog rows, `needs Russian=126`, `needs English=4,367`, collisions
`active=4`, `Game=3`, `Russian=0`, `dormant=15`. Runtime inspection found 331 shared
malformed records plus one extra malformed Russian record. These counts are the
before-state, not acceptance evidence.

## Evidence

- `JAZZ-LOC-002-AC-001`: `BLOCKED` — будет заполнено после полного прохода.
- `JAZZ-LOC-002-AC-002`: `BLOCKED` — будет заполнено после полного прохода.
- `JAZZ-LOC-002-AC-003`: `BLOCKED` — будет заполнено после полного прохода.
- `JAZZ-LOC-002-AC-004`: `BLOCKED` — будет заполнено после экспорта.
- `JAZZ-LOC-002-AC-005`: `BLOCKED` — будет заполнено после экспорта.
- `JAZZ-LOC-002-AC-006`: `BLOCKED` — будет заполнено после token-аудита.
- `JAZZ-LOC-002-AC-007`: `BLOCKED` — будет заполнено после независимого ревью.
- `JAZZ-LOC-002-AC-008`: `BLOCKED` — требуется ручной runtime smoke-test.
- `JAZZ-LOC-002-AC-009`: `BLOCKED` — будет заполнено по финальному diff.

## Documentation delta

- `docs/technical/systems/localization.md` получит текущие counts, контракт
  редакторской памяти и ссылку на воспроизводимый copy-quality аудит.
