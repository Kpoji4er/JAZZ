---
id: JAZZ-UI-AME-001
status: approved
owner: project-owner
systems:
  - assets-and-ui
  - units-progression-specializations
  - localization
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - Code/System_AME_Market.lua
  - Code/System_AME_Browser.lua
  - Code/System_AME_Browser_Template.lua
  - Code/System_AME_Filters.lua
  - Code/System_AME_Mail.lua
  - items.lua
  - metadata.lua
  - English.csv
  - Russian.csv
  - docs/specs/active/JAZZ-UI-AME-001.md
  - docs/design/ame-mercenary-exchange.md
  - docs/technical/systems/file-coverage.md
  - docs/technical/systems/units-progression-specializations.md
  - docs/wiki/
  - docs/showcase/
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-UI-AME-001: AME — почта и разблокировка сайта

## Проблема

Живой рынок AME (`JAZZ_AME_MarketTick` каждые 14 дней, init на NewGame) уже крутит витрину, но игрок **не получает оповещений**: нет письма о том, что такое биржа, нет письма о смене листинга, вкладка PDA `ame` принудительно `locked = false` с первого дня ([`Code/System_AME_Browser.lua`](../../Code/System_AME_Browser.lua)). Игрок может не заметить AME или ротацию.

Канал **не** связан с R.I.S. (см. [`JAZZ-UI-RIS-001`](JAZZ-UI-RIS-001.md)).

## Цели

- Письмо AME **сразу после загрузки** (NewGame / LoadGame с init market), объясняющее **что такое биржа**, как нанимать, и кратко перечисляющее текущую витрину.
- Письмо после каждого **реального** 14-дневного tick со сменой витрины (кто появился приблизительно; ушедшие — мягко).
- Вкладка PDA `ame` **всегда открыта** с первого дня (welcome mail информационный; не gate — иначе конфликт со стартовым наймом без почты).
- Sender / тон / бренд — **African Mercenary Exchange**, не R.I.S.

## Non-goals

- Бренд или тексты R.I.S. / Легион / досье / after-action ([`JAZZ-UI-RIS-001`](JAZZ-UI-RIS-001.md)).
- Изменение размера пула, tick interval, specialist soft-guarantee, зарплат, UnitData roster ([`JAZZ-UNITS-005`](JAZZ-UNITS-005.md)).
- Письмо на каждый Load без смены состояния (replay welcome).
- Quest-gated unlock отдельным квестом (вкладка всегда open).
- Отдельный messenger / новый Hire pipeline.

## Требования

### Welcome mail

- `JAZZ-UI-AME-001-REQ-001` — при успешной инициализации рынка (`JAZZ_AME_InitMarket` / первый Load с init) один раз отправить Email от AME **сразу** (без задержки часов). Не повторять, если `welcome_sent` уже true в `gv_JAZZ_AME_Market`.
- `JAZZ-UI-AME-001-REQ-002` — тело welcome **объясняет биржу** человеческим языком RU+EN: локальный рынок бойцов без AIM-бренда; дешевле из‑за отсутствия имени/репутации; рост на службе — продукт; витрина ротируется примерно раз в две недели; как открыть вкладку AME в PDA.
- `JAZZ-UI-AME-001-REQ-003` — welcome включает **рекламные** хайлайты текущих Available (не сухой список): ник + 1–2 продающих тезиса по роли/статам (стреляет / лечит / механик / сила / …) + категория. Слоты `NotMet` не раскрывать. Динамический блок через Email `context.listing`.

### Tick mail

- `JAZZ-UI-AME-001-REQ-004` — после `JAZZ_AME_MarketTick`, если витрина реально изменилась (новые Available и/или terminal departures), отправить Email обновления листинга: кто появился (приблизительно); ушедших — мягко («контракты закрыты / ушли к другим работодателям»), без обязательного dump всех MIA reasons.
- `JAZZ-UI-AME-001-REQ-005` — не слать tick-письмо, если состав Available и terminal-слоты не изменились относительно предыдущего mailed snapshot.

### Site lock

- `JAZZ-UI-AME-001-REQ-006` — вкладка PDA `ame` **всегда unlocked** с первого дня (welcome mail информационный; lock мешал стартовому найму без доступа к почте). Убрать force-lock из browser ensure.
- `JAZZ-UI-AME-001-REQ-007` — welcome Email по-прежнему отправляется на init; `welcome_read` трекается для аналитики/будущего UI, но **не** гейтит вкладку. Повторные Load сохраняют `ame.locked = false`.

### Presets и state

- `JAZZ-UI-AME-001-REQ-008` — `ModItemEmail` presets с публичными id `AME_Welcome` и `AME_ListingUpdate` (или эквивалент с префиксом `AME_`); sender/title/body RU+EN; без бренда R.I.S.
- `JAZZ-UI-AME-001-REQ-009` — dedup/state в `gv_JAZZ_AME_Market`: минимум `welcome_sent`, `welcome_read`, `last_tick_mail_day` / snapshot hash витрины для REQ-005.
- `JAZZ-UI-AME-001-REQ-010` — локализация: все player-facing строки Email в `Russian.csv` и `English.csv` в том же change set (`needs Russian=0`, `needs English=0`).

## Инварианты и ограничения

- Не ломать AIM / Bobby Ray / IMP browser tabs.
- Не ломать вкладку / mode `ame` (найм, chrome, фильтры, Loadout без Perks, Hire pipeline) — mail информационный; вкладка всегда доступна как в [`JAZZ-UNITS-005`](JAZZ-UNITS-005.md).
- Не менять market tick math и HireStatus pipeline UNITS-005.
- Deterministic: отправка писем не должна ломать sync; не использовать недетерминированный RNG для «слать / не слать».
- R.I.S. lock/welcome не зависят от AME и наоборот (кроме общего PDA chrome).

## Acceptance criteria

- `JAZZ-UI-AME-001-AC-001` — runtime NewGame: сразу после загрузки есть unread AME welcome; вкладка `ame` **unlocked** и сайт открывается без почты.
- `JAZZ-UI-AME-001-AC-002` — human: welcome prose объясняет биржу (не только «зайдите на сайт») и читается нормальным языком RU и EN.
- `JAZZ-UI-AME-001-AC-003` — runtime: после 14-дневного tick со сменой витрины приходит listing-update Email; без смены витрины — нет.
- `JAZZ-UI-AME-001-AC-004` — runtime LoadGame: welcome не дублируется; `ame` остаётся unlocked.
- `JAZZ-UI-AME-001-AC-005` — static: Email presets + code load в `items.lua`/`metadata.lua`; `_validate_items_quick.py` OK.
- `JAZZ-UI-AME-001-AC-006` — static/human: ни одно AME-письмо не подписано R.I.S. / Recon Intelligence Services.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: `ReceiveEmail`, `PDABrowserTabState.locked`, Email read hooks; AME browser уже в JAZZ.
- Saves: старые сейвы без mail-флагов получают одно welcome на первом Load с модом; `ame.locked` сразу и повторно устанавливается в `false`, чтение письма не gate.
- Network/determinism: mail flags в GameVar; без лишнего InteractionRand.
- Generated data: `ModItemEmail` в `items.lua` + metadata sync.
- Cross-package: только `jazz` runtime; UnitData AME уже в jazz-units.
- Rollback: удалить mail code + presets; always-open `ame.locked = false` оставить частью базового AME browser contract.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent / owner
- Reviewer: project-owner
- Declared write set: frontmatter `write_set`
- Exclusive resources: `jazz/items.lua`, `jazz/metadata.lua`
- Порядок: после approve — implement **до** [`JAZZ-UI-RIS-001`](JAZZ-UI-RIS-001.md) phase-1 mail (последовательность плана)

## Решение владельца

- Статус: `approved`
- Кто подтвердил: project-owner (chat: приступай к реализации)
- Дата: 2026-08-06

## Evidence

- `JAZZ-UI-AME-001-AC-001`: `BLOCKED` (runtime) — static wiring и always-open state готовы; нужен NewGame PDA/email playtest.
- `JAZZ-UI-AME-001-AC-002`: `PASS` (human/static) — welcome отдельно отредактирован на RU/EN, объясняет репутационную цену, рост и двухнедельную ротацию без lock-инструкции.
- `JAZZ-UI-AME-001-AC-003`: `BLOCKED` (runtime) — snapshot dedup реализован; нужен +14d mail playtest.
- `JAZZ-UI-AME-001-AC-004`: `BLOCKED` (runtime) — old-save state migration и idempotent read wrap покрыты static harness; нужен LoadGame playtest.
- `JAZZ-UI-AME-001-AC-005`: `PASS` (static) — Email presets/Code load присутствуют; `_validate_items_quick.py` и `_test_ame_contract.py` проходят.
- `JAZZ-UI-AME-001-AC-006`: `PASS` (static/human) — sender/body/title и pitch bank используют только A.M.E.; R.I.S. branding отсутствует.

## Documentation delta

- Реализовано: `docs/design/ame-mercenary-exchange.md`, `docs/technical/systems/units-progression-specializations.md`, `docs/technical/systems/file-coverage.md`, `docs/wiki/african-mercenary-exchange.md`, `docs/showcase/ru/ame.md`, `docs/showcase/en/ame.md`.
- Связь: [`JAZZ-UNITS-005`](JAZZ-UNITS-005.md) (рынок); [`JAZZ-UI-RIS-001`](JAZZ-UI-RIS-001.md) (отдельный канал).
