---
id: JAZZ-UI-RIS-001
status: approved
owner: project-owner
systems:
  - assets-and-ui
  - legion-units-equipment-tiers
  - localization
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/System_RIS_*.lua
  - Code/LegionTierProgression.lua
  - Code/System_AME_Browser.lua
  - items.lua
  - metadata.lua
  - English.csv
  - Russian.csv
  - docs/specs/active/JAZZ-UI-RIS-001.md
  - docs/design/ris-legion-tier-briefs.md
  - docs/design/ris-battle-report-templates.md
  - docs/design/ris-legion-dossiers.md
  - docs/technical/systems/file-coverage.md
  - docs/technical/systems/ris-intelligence.md
  - docs/technical/systems/legion-units-equipment-tiers.md
  - docs/wiki/
  - docs/showcase/
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-UI-RIS-001: R.I.S. — разведподписка, почта, сайт, AAR

## Проблема

`JAZZ_Legion_Tier` растёт из [`Code/LegionTierProgression.lua`](../../Code/LegionTierProgression.lua), но игрок не видит человеческих оповещений. В `items.lua` лежат stub Email `LegionTier1`…`5` (sender «JAZZ», body «Тир1-1»), **`ReceiveEmail` не вызывается**. Нет PDA-сайта разведки, досье по встреченным бойцам Легиона и after-action сводок боёв.

Канал **отделён от AME** ([`JAZZ-UI-AME-001`](JAZZ-UI-AME-001.md)).

## Цели

- Бренд **R.I.S.** / **Recon Intelligence Services**: бесплатная подписка разведки в рамках кампании.
- Welcome-письмо через **несколько часов** campaign time; сайт `ris` locked до прочтения welcome.
- На каждый рост снаряжения Легиона — письмо с **художественным** брифом (хайлайт предметов вроде «майор скупает ППШ…»), без «тир 1-2».
- PDA-сайт R.I.S.: bulletin, досье юнитов Легиона после **3** убийств типа, квестовые NPC/фракции по встрече, лента **after-action** из шаблонных параграфов (несколько заголовков; погода; интенсивность/Heat; силы; потери; **история каждого elite+named** с корректным именем).

## Non-goals

- AME mail, AME listing, бренд AME ([`JAZZ-UI-AME-001`](JAZZ-UI-AME-001.md)).
- Сырые числа `JAZZ_Legion_Tier`, LootDef id, AI archetype id, session_id в player-facing тексте.
- Письмо на каждый бой (AAR только на сайте).
- Discord / out-of-game notify.
- Изменение формул progression tier / Heat economy (только **чтение** сигналов для текстов).
- Allowlist только story-NPC для elite-историй (критерий — любой `elite` + имя).

## Требования

### Бренд и state

- `JAZZ-UI-RIS-001-REQ-001` — публичный бренд: **R.I.S.** / полное имя **Recon Intelligence Services** (RU/EN локализация). Обоснование в мире: бесплатная подписка разведки в кампании.
- `JAZZ-UI-RIS-001-REQ-002` — GameVar `gv_JAZZ_RIS` хранит минимум: `welcome_sent`, `welcome_read`, `last_mailed_tier`, `mod_awake_at`, `mail_queue`, `next_dispatch_at`, `kills`, `battles`, dossier unlock flags.

### Welcome mail и site lock

- `JAZZ-UI-RIS-001-REQ-003` — welcome Email **не** сразу: ставится в `mail_queue` с `ready_at = mod_awake_at + 3h` (NewGame / первый awake на старом сейве). Отправка через общий desk-drain (REQ-007a), один раз (`welcome_sent`).
- `JAZZ-UI-RIS-001-REQ-004` — welcome prose: подписка активирована; что ждать (оценки снабжения Легиона; позже досье и сводки боёв); тон деловой/человеческий.
- `JAZZ-UI-RIS-001-REQ-005` — PDA browser mode `ris` с вкладкой; `PDABrowserTabState.ris.locked = true` до `welcome_read`; после прочтения welcome — unlock. Chrome «R.I.S.» / Recon Intelligence Services.
- `JAZZ-UI-RIS-001-REQ-006` — AME **не** появляется на сайте R.I.S. и наоборот по контенту.

### Legion equipment briefs (mail)

- `JAZZ-UI-RIS-001-REQ-007` — при каждом реальном raise `JAZZ_Legion_Tier` поставить в `mail_queue` бриф для **нового** тира с `ready_at = now + 5h` (не слать мгновенно). Текст из канона [`docs/design/ris-legion-tier-briefs.md`](../../design/ris-legion-tier-briefs.md).
- `JAZZ-UI-RIS-001-REQ-007a` — **desk queue**: не чаще одного R.I.S. письма раз в **5** campaign hours (`next_dispatch_at`). Из очереди берётся первый элемент с `ready_at ≤ now`. Baseline (стартовый тир, обычно 11 / T1-1): enqueue при awake с `ready_at = awake + 2h`.
- `JAZZ-UI-RIS-001-REQ-008` — канон briefs покрывает каждое runtime-значение `11`…`13`, `21`…`25`, `31`…`33`. Major jump (13→21, 25→31) использует более сильный тон в том же брифе целевого значения.
- `JAZZ-UI-RIS-001-REQ-009` — заменить/удалить stub `LegionTier1`…`5` (sender JAZZ / «Тир1-1»); новые Email id с префиксом `RIS_`.
- `JAZZ-UI-RIS-001-REQ-010` — LoadGame catch-up: если текущий тир ещё не mailed / нет brief в inbox — **одно** место в очереди по текущему тиру (не пачка); отправка через desk-drain, не dump на Load.

### Сайт: bulletin и досье

- `JAZZ-UI-RIS-001-REQ-011` — на сайте R.I.S. секция Bulletin: доступ к текущей/последней оценке снабжения и архиву релевантных R.I.S. писем (или эквивалент readable history).
- `JAZZ-UI-RIS-001-REQ-012` — досье на **тип** юнита Легиона (`JAZZ_Legion_*` / согласованный unitData id) открывается после того, как игрок **убил ≥ 3** бойцов этого типа в кампании. Счётчик в `gv_JAZZ_RIS.kills`.
- `JAZZ-UI-RIS-001-REQ-013` — текст досье художественный (канон [`docs/design/ris-legion-dossiers.md`](../../design/ris-legion-dossiers.md) или per-id entries): как **Майор** набирает и учит; что умеют; как действуют в бою; какая сила. Не статблок / не AI id.
- `JAZZ-UI-RIS-001-REQ-014` — досье квестовых NPC / фракций по факту встречи / IsMet / quest flag (короткая карточка: кто, сторона, зачем важно игроку). Scope списков — design appendix в том же change set сайта.

### After-action reports (сайт)

- `JAZZ-UI-RIS-001-REQ-015` — на `CombatEnd` (или эквивалентный надёжный хук) снять snapshot и добавить запись в `gv_JAZZ_RIS.battles` (FIFO cap **20**). Письмо на бой **не** слать.
- `JAZZ-UI-RIS-001-REQ-016` — текст AAR собирается из шаблонных параграфов ([`docs/design/ris-battle-report-templates.md`](../../design/ris-battle-report-templates.md)), слоты минимум:
  1. **Заголовок** — банк **нескольких** вариантов (≥3 на intensity/outcome band); один выбирается детерминированно (`Game.id` + combat seed + slot).
  2. Погода / время суток.
  3. Интенсивность (bands от Heat delta / shots / turns / casualty rate — те же идеи, что «жара за пульку»).
  4. Силы сторон (counts).
  5. Характер боя (win/loss, ambush, retreat).
  6. Потери сторон (KIA/WIA).
  7. Заключение / шум (Heat note опционально).
- `JAZZ-UI-RIS-001-REQ-017` — для **каждого** врага в бою с `elite == true` **и** непустым отображаемым именем (Name/Nick как в UI): отдельный абзац-история с **корректной подстановкой имени** (`T{…, name = …}`). Это **любой** такой юнит, не allowlist. Безымянный elite — только в общих силах/потерях. Несколько — по абзацу на каждого, стабильный порядок. Исходы: убит / тяжело ранен / ушёл / угроза остаётся — разные шаблоны.
- `JAZZ-UI-RIS-001-REQ-018` — сайт показывает ленту battle reports (заголовок + тело); без raw debug ids.

### Локализация и docs-as-canon

- `JAZZ-UI-RIS-001-REQ-019` — все player-facing Email / UI / шаблоны AAR / briefs / dossiers: RU+EN в том же change set (`needs Russian=0`, `needs English=0`).
- `JAZZ-UI-RIS-001-REQ-020` — design-файлы briefs / AAR templates / dossiers существуют до или в том же merge, что и runtime, который их потребляет.

## Инварианты и ограничения

- Не менять `JAZZ_Legion_Tier` progression math; только наблюдать raise и читать Heat/combat signals.
- Не смешивать бренды AME и R.I.S.
- Deterministic template pick; MP-safe snapshot (только synced combat outcomes).
- Stub LegionTier Emails не должны остаться player-facing после ship mail-phase.

## Acceptance criteria

### Phase A — mail + lock (до сайта)

- `JAZZ-UI-RIS-001-AC-001` — runtime NewGame: welcome и baseline brief в очереди; T1-1 eligible ~+2h, welcome ~+3h; desk шлёт ≤1 письмо / 5h; до прочтения welcome `ris` locked.
- `JAZZ-UI-RIS-001-AC-002` — runtime old save: queue от `mod_awake_at`, не спамит пачкой на Load.
- `JAZZ-UI-RIS-001-AC-003` — runtime: raise tier → brief в очереди с ready +5h; одно письмо за слот desk; catch-up — одно место в очереди, не dump.
- `JAZZ-UI-RIS-001-AC-004` — static/human: stubs `LegionTier*` убраны или недостижимы; sender R.I.S.
- `JAZZ-UI-RIS-001-AC-005` — human: briefs читаются как разведсводка, хайлайтят предметы снаряжения.

### Phase B — site + dossiers + AAR

- `JAZZ-UI-RIS-001-AC-006` — runtime: после 3 убийств одного `JAZZ_Legion_*` типа досье открывается; текст покрывает Майор/учёба/умения/бой/сила.
- `JAZZ-UI-RIS-001-AC-007` — runtime: после боя на сайте появляется AAR с выбранным заголовком из банка (≥3 вариантов на band в design).
- `JAZZ-UI-RIS-001-AC-008` — runtime/human: в бою с двумя elite+named врагами — два абзаца с **их** именами (не id); безымянный elite без отдельного абзаца.
- `JAZZ-UI-RIS-001-AC-009` — runtime: AAR содержит слоты погоды, интенсивности, сил, потерь (когда сигналы доступны).
- `JAZZ-UI-RIS-001-AC-010` — static: `items.lua`/`metadata.lua` sync; `_validate_items_quick.py` OK; file-coverage для новых `Code/System_RIS_*.lua`.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: Email, PDABrowser tabs, CombatEnd, Unit Name/Nick, Heat fields.
- Saves: `gv_JAZZ_RIS` migrate на первом Load; missing fields defaulted.
- Network/determinism: template pick seeded; mail flags GameVar.
- Generated data: Emails, XTemplate mode `ris`, loc CSV.
- Cross-package: читает UnitData/Legion ids из jazz-units; prose в jazz design.
- Rollback: unload RIS code; restore stub emails only if needed (prefer leave removed).

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent / owner
- Reviewer: project-owner
- Declared write set: frontmatter `write_set`
- Exclusive resources: `jazz/items.lua`, `jazz/metadata.lua`
- Порядок implement после approve:
  1. Design briefs + AAR template banks (+ dossier outline)
  2. Phase A mail + lock
  3. Phase B site + dossiers + AAR
  4. Не начинать Phase A, пока [`JAZZ-UI-AME-001`](JAZZ-UI-AME-001.md) не shipped или явно не отложен owner’ом (последовательность плана)

## Решение владельца

- Статус: `approved`
- Кто подтвердил: project-owner (chat: приступай к реализации)
- Дата: 2026-08-06

## Evidence

- `JAZZ-UI-RIS-001-AC-001`…`AC-010`: `BLOCKED` — awaiting approve / implement

## Documentation delta

- При implement Phase A: technical `ris-intelligence.md` (mail), `legion-units-equipment-tiers.md` (ссылка на briefs), file-coverage, wiki/showcase R.I.S. subscription.
- При Phase B: тот же technical + design dossiers/AAR; wiki/showcase battle reports / dossiers.
- Связь: COMPAT-003/008 tier progression; STRATEGY Heat; [`JAZZ-UI-AME-001`](JAZZ-UI-AME-001.md).
