---
id: JAZZ-LOC-001
status: implemented
owner: project-owner
systems:
  - localization
repositories:
  - jazz
  - jazz-maps
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - scripts/localization/migrate-localization-ids.ps1
  - scripts/localization/translate-english-google.ps1
  - .agents/skills/manage-jazz-localization/SKILL.md
  - Localization/IdMigration.csv
  - Localization/IdAmbiguities.csv
  - Localization/Strings.csv
  - Localization/RussianManual.csv
  - Localization/EnglishManual.csv
  - Localization/Collisions.csv
  - Russian.csv
  - English.csv
  - items.lua
  - Code/*.lua
  - InventoryItem/*.lua
  - CharacterEffect/*.lua
  - XTemplate/*.lua
  - ../jazz-maps/items.lua
  - ../jazz-units/items.lua
  - ../jazz-units/UnitData/*.lua
  - docs/specs/active/JAZZ-LOC-001.md
  - docs/technical/systems/localization.md
  - docs/technical/systems/file-coverage.md
  - docs/technical/compatibility.md
  - docs/technical/testing.md
exclusive_resources:
  - localization-id-range-890000000000000-890000000099999
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/items.lua
  - jazz-maps/items.lua
  - jazz-units/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-LOC-001: устранение коллизий localization ID

## Проблема

При клонировании vanilla ModItem редактор JA3 способен выдать новые случайные numeric localization ID даже полям, текст которых не менялся. Такие ID не являются новыми строками JAZZ: для них нужно восстановить исходный vanilla ID и canonical English source text. Одновременно в коде есть настоящие mod-only строки, повторно используемые ID, ID vanilla с иным текстом и значения выше безопасного диапазона IEEE-754. Текущий `Russian.csv` неполон и имеет legacy-формат шире официальных пяти колонок.

## Цели

- Восстановить исходные vanilla ID у неизменённых строк клонированных объектов.
- Назначить свободные ID только действительно новым или конфликтующим строкам JAZZ.
- Синхронно заменить ID в активных non-map Lua-представлениях и generated companion.
- Сохранить проверяемую карту каждой миграции и отдельный отчёт неоднозначностей.
- Нормализовать `Russian.csv` и включить в него активные mod-only ID, отсутствующие в `Game.csv`.
- Подготовить устойчивый двуязычный каталог и полный English.csv только для активных mod-only строк.
- Переиспользовать английский текст vanilla из Game.csv, не дублируя его ID в файлах мода.

## Non-goals

- Перенос ванильных ID и строк в `English.csv`: английскую локализацию vanilla предоставляет сама игра.
- Рекурсивное изменение `jazz-maps/Maps/`.
- Изменение механик, баланса, class/preset/entity ID или порядка загрузки.
- Массовая перегенерация Mod Editor и косметическое форматирование Lua.
- Исправление существующих dormant/orphan warning generated-аудита.

## Требования

- `JAZZ-LOC-001-REQ-001` — перед выделением нового ID сопоставить неизменённую clone-строку с `Game.csv` по `Text`/`Translation`, generated `Context` и, для повторов, по последовательности в актуальном `<JA3_ROOT>\ModTools\Src`; восстановить original vanilla ID и `Game.csv.Text`.
- `JAZZ-LOC-001-REQ-002` — единицей сопоставления считать `старый ID + SourceText + generated Context`, чтобы одинаковый случайный ID у разных объектов не склеивал независимые строки.
- `JAZZ-LOC-001-REQ-003` — новый ID из подтверждённо свободного диапазона меньше `2^53` назначать только mod-only строке, внутренней коллизии или небезопасному числовому ID, для которых vanilla-соответствие отсутствует.
- `JAZZ-LOC-001-REQ-004` — синхронно менять все найденные non-map `T(...)`/`T{...}` в `items.lua`, загружаемом/связанном companion и ручном Lua; разные тексты или контексты старого ID не объединять.
- `JAZZ-LOC-001-REQ-005` — сохранять `Localization/IdMigration.csv` с old/new ID, контекстом, текстом, причиной и местами; до Apply `Localization/IdAmbiguities.csv` должен быть пуст.
- `JAZZ-LOC-001-REQ-006` — нормализовать `Russian.csv` в UTF-8 и официальную схему `ID,Text,Translation,VoiceActor,Context`, сохранив приоритет существующих переводов и добавив активные mod-only ID.
- `JAZZ-LOC-001-REQ-007` — не подставлять пустой или заведомо чужой русский перевод; placeholders, теги, переносы и multiline CSV-поля сохранять без потерь.
- `JAZZ-LOC-001-REQ-008` — повторный запуск Plan/Apply должен быть идемпотентным и не назначать новые ID уже мигрированным строкам.
- `JAZZ-LOC-001-REQ-009` — полный английский перевод хранить в `Localization/EnglishManual.csv`; приоритет источников: существующая ручная память, однозначное точное обратное совпадение `Game.csv.Translation -> Game.csv.Text`, проверенные старые таблицы и ручной перевод действительно новых строк JAZZ.
- `JAZZ-LOC-001-REQ-010` — экспортировать `English.csv` в UTF-8 и официальную схему `ID,Text,Translation,VoiceActor,Context`, ровно по множеству активных mod-only ID, отсутствующих в `Game.csv`; ванильные ID не дублировать.
- `JAZZ-LOC-001-REQ-011` — английский экспорт не создавать неполным: все нетехнические строки должны иметь перевод, а placeholders, теги, переносы и multiline CSV-поля должны сохраняться без потерь.
- `JAZZ-LOC-001-REQ-012` — существующая запись `metadata.loctables` основного пакета должна подключать `Mod/e6L4ECj/English.csv` для языка `English`; порядок загрузки не менять.
- `JAZZ-LOC-001-REQ-013` — внешний машинный перевод разрешать только явным opt-in после согласия владельца; до отправки защищать теги, placeholders и переносы, результаты хранить с `Notes=google-draft` ниже доверенных источников и не экспортировать до локальной структурной проверки.

## Инварианты и ограничения

- Numeric ID хранить и сравнивать как строку цифр, не через IEEE-754.
- Диапазон `890000000000000..890000000099999` использовать только после проверки против `Game.csv`, всех non-map Lua JAZZ, каталога и CSV.
- `Game.csv` приоритетен для vanilla ID и canonical English; актуальный `<JA3_ROOT>\ModTools\Src` приоритетен для порядка одинаковых повторов.
- `Russian.csv` приоритетнее старых источников русской строки JAZZ.
- Не менять `jazz-maps/Maps/`, посторонние незакоммиченные правки и окончания строк.
- CommonLib snapshot: upstream `main` commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c`, version 1.11 build 1056.

## Acceptance criteria

- `JAZZ-LOC-001-AC-001` — перед Apply `Localization/IdAmbiguities.csv` содержит только заголовок.
- `JAZZ-LOC-001-AC-002` — clone-строки из manifest с action `restore-vanilla` используют ID и canonical English text, подтверждённые `Game.csv`/`<JA3_ROOT>\ModTools\Src`.
- `JAZZ-LOC-001-AC-003` — каждый назначенный mod-only ID уникален по финальному тексту, отсутствует в исходном `Game.csv` и меньше `2^53`.
- `JAZZ-LOC-001-AC-004` — localization-аудит сообщает `active=0`, `against Game.csv=0`, `Russian.csv=0` коллизий.
- `JAZZ-LOC-001-AC-005` — generated sync-аудит не добавляет ошибок или warning относительно preflight: 0 errors, 20 известных warnings.
- `JAZZ-LOC-001-AC-006` — `Russian.csv` разбирается без повреждённых записей и содержит ровно одну запись на каждый активный mod-only ID, отсутствующий в `Game.csv`.
- `JAZZ-LOC-001-AC-007` — `git diff --check` проходит отдельно в каждом изменённом репозитории либо отдельно отмечает только существовавшие до задачи посторонние проблемы.
- `JAZZ-LOC-001-AC-008` — Mod Editor загружает, сохраняет и повторно загружает три изменённых пакета без ignored mod, load/runtime error или assert.
- `JAZZ-LOC-001-AC-009` — новая игра и существующее сохранение показывают проверенные русские строки без `<missing translation>` и чужих подмен.
- `JAZZ-LOC-001-AC-010` — аудит каталога сообщает `needs English=0`.
- `JAZZ-LOC-001-AC-011` — `English.csv` содержит ровно по одной строке для каждого активного mod-only ID: duplicates 0, missing 0, extra 0, overlap с `Game.csv` 0, нетехнических пустых переводов 0, tag/placeholder multiset mismatch 0.
- `JAZZ-LOC-001-AC-012` — `metadata.lua` основного пакета содержит английскую loctable, указывающую на существующий корневой `English.csv`.
- `JAZZ-LOC-001-AC-013` — при английском языке новая игра и существующее сохранение показывают строки JAZZ без `<missing translation>`, русского текста и повреждённых форматирующих тегов.
- `JAZZ-LOC-001-AC-014` — машинный draft не содержит потерянных защищённых токенов; итоговый экспорт имеет ноль видимой кириллицы вне сохранённых технических тегов и ноль tag/placeholder mismatch.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: восстановленные ID снова используют базовую локализацию; новые mod-only ID устраняют глобальные пересечения. Определения CommonLib и порядок загрузки не меняются.
- Saves: localization ID не является class/preset ID, но уже сериализованные T-значения требуют проверки существующего сохранения.
- Network/determinism: игровая логика и RNG не меняются.
- Generated data: меняются editor-state `items.lua` и соответствующие companion; требуется Mod Editor round-trip.
- Cross-package: каждый пакет остаётся владельцем своих T-вызовов; central `Russian.csv` и инструменты принадлежат `jazz`.
- Rollback: `Localization/IdMigration.csv` хранит точное old/new/context соответствие; откат выполняется только согласованным revert затронутых репозиториев.

## План и ownership

- Владелец данных: `jazz`, `jazz-maps` и `jazz-units` владеют собственными Lua; `jazz` владеет `Russian.csv`, `English.csv`, памятью перевода, каталогом и инструментами.
- Исполнитель: Codex.
- Reviewer: project-owner.
- Write set ограничен frontmatter и конкретными Lua-файлами, перечисленными в `Localization/IdMigration.csv`.
- Зарезервированы диапазон ID, `Russian.csv` и три `items.lua`.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner прямыми запросами исправить коллизии, вернуть случайные ID неизменённых clone-строк и создать подключённый полный `English.csv`; отдельно подтверждено, что английские vanilla-строки предоставляет игра и дублировать их не надо. Владелец также явно разрешил отправить оставшиеся mod-only строки в Google Translate как машинный черновик после уведомления о передаче данных стороннему сервису.
- Дата: 2026-07-26.

## Evidence

- `JAZZ-LOC-001-AC-013`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`

- `JAZZ-LOC-001-AC-001`: `PASS (static)` — `IdAmbiguities.csv`: 0 data rows.
- `JAZZ-LOC-001-AC-002`: `PASS (static)` — 3 441 manifest rows `restore-vanilla`; 0 отсутствующих ID и 0 несовпадений canonical `Game.csv.Text`.
- `JAZZ-LOC-001-AC-003`: `PASS (static)` — 1 540 строк `assign-mod-id`, 1 424 уникальных новых ID в `890000000000000..890000000001423`; 0 пересечений с `Game.csv`, 0 ID вне диапазона/выше `2^53`, 0 ID с разными текстами.
- `JAZZ-LOC-001-AC-004`: `PASS (static)` — финальный аудит: 13 475 активных вызовов, 9 527 активных ID, 5 648 строк каталога; active 0, against `Game.csv` 0, `Russian.csv` 0 и dormant 0 коллизий, `needs Russian=0`, `needs English=0`.
- `JAZZ-LOC-001-AC-005`: `PASS (static)` — postflight generated sync: 0 errors и те же 20 известных warnings, что на preflight.
- `JAZZ-LOC-001-AC-006`: `PASS (static)` — `Russian.csv`: 5 632 строки/уникальных ID, ровно множество активных mod-only ID; duplicates 0, missing 0, extra 0, `Game.csv` overlap 0, non-technical blank translation 0.
- `JAZZ-LOC-001-AC-007`: `PASS (static, documented exception)` — `jazz-maps` и `jazz-units` exit 0. Основной `jazz` exit 2 только для 573 trailing-whitespace записей: 570 — сохранённые пробелы внутри многострочных CSV-полей `Russian.csv`, ещё 3 — существовавшие в HEAD Lua-строки, где миграция изменила только ID. Иных diff-check ошибок нет; `core.autocrlf` сообщает только предупреждения.
- `JAZZ-LOC-001-AC-008`: `PASS (editor) - owner accepted 2026-07-28`
- `JAZZ-LOC-001-AC-009`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-LOC-001-AC-010`: `PASS (static)` — финальный каталог: `needs English=0`.
- `JAZZ-LOC-001-AC-011`: `PASS (static)` — `English.csv`: 5 632 строки/уникальных ID; duplicates 0, missing 0, extra 0, `Game.csv` overlap 0, non-technical blank translation 0, strict tag/placeholder mismatch 0.
- `JAZZ-LOC-001-AC-012`: `PASS (static)` — `metadata.lua` загружает существующий `Mod/e6L4ECj/English.csv` для `language = "English"`.
- `JAZZ-LOC-001-AC-014`: `PASS (static)` — защищённые токены сохранены, видимая кириллица в английском экспорте 0, strict tag/placeholder mismatch 0; 2 896 строк остаются явно помеченными `google-draft`.
- `JAZZ-LOC-001-REQ-008`: `PASS (static)` — повторный Apply: token replacements 0, changed files 0.
- Дополнительно: PowerShell AST обоих инструментов — 0 ошибок; documentation contract passed; project skill обновлён и проверен вручную, штатный `quick_validate.py` не запустился из-за отсутствующего `PyYAML` в локальном runtime.
### Follow-up 2026-07-28

- `JAZZ-LOC-001-AC-001`: `PASS (static)` — повторный Plan не создал ни одной строки неоднозначности; `IdAmbiguities.csv` содержит только заголовок.
- `JAZZ-LOC-001-REQ-008`: `PASS (static)` — applied-manifest содержит 255 пар и везде `Applied=yes`; повторный Apply дал 0 замен и 0 изменённых файлов, повторный Plan во временные пути дал 0 manifest rows и 0 ambiguities. Для пустого Plan исправлен отчёт по `occurrences=0`.
- `JAZZ-LOC-001-AC-003`: `PASS (static)` — follow-up восстановил 52 vanilla-пары и назначил 203 mod-only пары (318 вхождений) на 179 уникальных ID из диапазона `890000000001452..890000000001630`; пересечений и неоднозначностей нет.
- `JAZZ-LOC-001-AC-004`: `PASS (static)` — финальный аудит: 13 502 активных вызова, 9 625 активных ID, 5 751 строка каталога; active, against `Game.csv`, `Russian.csv` и dormant коллизии равны 0; `needs Russian=0`, `needs English=0`.
- `JAZZ-LOC-001-AC-005`: `PASS (static)` — postflight generated sync: 0 errors и те же 20 известных warnings.
- `JAZZ-LOC-001-AC-006` / `JAZZ-LOC-001-AC-011`: `PASS (static)` — `Russian.csv` и `English.csv` содержат по 5 735 уникальных ID с точным совпадением множеств и без дублей; два намеренно пустых технических T (`486989771291111`, `4869897712911115`) совпадают в обоих языках.
- `JAZZ-LOC-001-AC-008`, `JAZZ-LOC-001-AC-009`, `JAZZ-LOC-001-AC-013`: `PASS (editor/runtime)` — owner playtest accepted 2026-07-28.

## Documentation delta

- `docs/technical/systems/localization.md` обновлён для двуязычного runtime и translation memory.
- `docs/technical/compatibility.md` обновлён для public localization ID и английской таблицы.
- `docs/technical/testing.md` требует совместный русский/английский CSV round-trip и smoke-test.
- `docs/technical/systems/file-coverage.md` учитывает английскую память и opt-in переводчик.
