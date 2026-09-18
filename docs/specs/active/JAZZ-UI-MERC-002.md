---
id: JAZZ-UI-MERC-002
status: approved
owner: project-owner
systems:
  - assets-and-ui
  - units-progression-specializations
  - localization
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - Code/System_MERC_Account.lua
  - Code/System_MERC_Browser.lua
  - English.csv
  - Russian.csv
  - docs/tools/_append_merc_debt_alarm_loc.py
  - docs/tools/_check_merc_debt_alarm.py
  - docs/tools/README.md
  - docs/specs/active/JAZZ-UI-MERC-002.md
  - docs/design/merc-recruiting-center.md
  - docs/technical/systems/units-progression-specializations.md
  - docs/technical/override-matrix.md
  - docs/wiki/merc-recruiting-center.md
  - docs/showcase/ru/merc.md
  - docs/showcase/en/merc.md
exclusive_resources:
  - none
related_decisions:
  - none
related_specs:
  - JAZZ-UI-MERC-001
approved_by: project-owner
---

# JAZZ-UI-MERC-002: аларм долга MERC (чип + popup)

## Проблема

Кредитный счёт [JAZZ-UI-MERC-001](JAZZ-UI-MERC-001.md) уже шлёт `MERC_AccountReminder` через ~7 дней и через +3 дня увольняет всех нанятых MERC. Напоминание живёт только во входящих PDA; письмо об уходе приходит в тот же тик, что и `ReleaseMerc`. Игрок (NOMAPS, Ларри с F7) не видит долг, пока наёмник не исчезает из отряда. Платить за world-rescued MERC игрок согласен — нужен заметный аларм, не бесплатный Ларри.

## Цели

- Пока `balance > 0`, на сателлите рядом с деньгами виден чип `MERC $X` (жёлтый до reminder, красный на grace). Клик открывает вкладку MERC.
- Сохранить часы **7d + 3d grace**. На day 7: письмо Спека **и** popup с суммой и «3 дня». На day 9 (за день до ухода): второй popup «завтра уходят». Кнопки **Оплатить счёт** / **Позже**.
- На day 10: CombatLog со списком ушедших + существующее `MERC_QuitWarning`.
- Пока долг висит — иконки на сателлитном **time track** (как истечение контракта AIM): reminder на +7d, quit на дедлайне ухода.

## Non-goals

- Бесплатные Larry / Smiley / Biff после спасения.
- Откладывать quit из боя или операции; не менять, оставляют ли ушедшие лут (это не пункт 3).
- Ежедневный спам писем или новые Email presets.
- Голос Спека, fork `PDADialogSatellite` XTemplate.
- Менять ставки, Pay Account на сайте, AIM/AME prepaid.

## Требования

- `JAZZ-UI-MERC-002-REQ-001` — часы UI-MERC-001 без сдвига: reminder при `balance > 0` и `day - last_reminder_day >= 7` (stage 0→1); quit при stage 1 и `day - last_reminder_day >= 3`.
- `JAZZ-UI-MERC-002-REQ-002` — сателлитный чип `idJazzMERCDebt` в HList рядом с `PDADialogSatellite.idMoney`: текст `MERC $<balance>`; виден только при `balance > 0`; жёлтый при `warning_stage == 0`, красный при `warning_stage >= 1`; клик → `JAZZ_MERC_OpenSite` (`PDADialog` browser `merc`).
- `JAZZ-UI-MERC-002-REQ-003` — day 7: `MERC_AccountReminder` как сейчас **и** одноразовый `ZuluChoiceDialog` (pause кампании): сумма, «уйдут через 3 дня», Pay / Later. Pay зовёт `JAZZ_MERC_PayAccount`. Later закрывает диалог.
- `JAZZ-UI-MERC-002-REQ-004` — day 9 (`stage == 1`, `day - clock >= 2`, ещё не quit): одноразовый eve-popup «уйдут завтра», те же кнопки. Флаг `eve_popup_sent` в `gv_JAZZ_MERC_Account`; сбрасывается при `balance <= 0`.
- `JAZZ-UI-MERC-002-REQ-005` — day 10 quit: CombatLog `important` со списком Nick ушедших Hired MERC + существующий `MERC_QuitWarning`.
- `JAZZ-UI-MERC-002-REQ-006` — popup не из боевого `g_Combat` (очередь до сателлита / следующего тика без боя). Один открытый MERC-debt popup за раз.
- `JAZZ-UI-MERC-002-REQ-007` — loc RU+EN для чипа, ролловера, двух popup, CombatLog и timeline (`890000000009944`–`009957`). Pay переиспользует `890000000009919`.
- `JAZZ-UI-MERC-002-REQ-008` — technical + wiki + showcase RU/EN + design companion описывают чип, time track и 7/9/10, не «только письмо».
- `JAZZ-UI-MERC-002-REQ-009` — пока `balance > 0` и stage &lt; 2: `AddTimelineEvent` `jazz-merc-reminder` (stage 0, due = clock+7d) и `jazz-merc-quit` (due = quit day). Тип `jazz_merc_debt` в `SatelliteTimelineEvents` (иконка как AIM contract). Pay / quit / balance 0 → `RemoveTimelineEvent` обоих id. ПКМ по иконке → `JAZZ_MERC_OpenSite`. Не wrap `SatelliteTimeline`.

## Инварианты и ограничения

- `warning_stage` 0 / 1 / 2 сохраняет смысл UI-MERC-001 (quit = 2). Eve — отдельный boolean, не новая stage, чтобы старые сейвы со stage 2 не считались «накануне ухода».
- `PDAMoneyText:Open` — один wrap, install-once, без re-base на чужой слот.
- Новых GameVar / NetSync / Email id нет; только поля на существующем `gv_JAZZ_MERC_Account`.
- AIM/AME money header без чипа (только `PDADialogSatellite`).

## Acceptance criteria

- `JAZZ-UI-MERC-002-AC-001` — static: `MERC_REMINDER_DAYS = 7`, `MERC_GRACE_DAYS = 3`, eve при `>= 2` до quit; `eve_popup_sent` / `reminder_popup_sent` сбрасываются с долгом.
- `JAZZ-UI-MERC-002-AC-002` — static: chip id `idJazzMERCDebt`; wrap `PDAMoneyText:Open`; `JAZZ_MERC_OpenSite` ставит `browser_page = "merc"`.
- `JAZZ-UI-MERC-002-AC-003` — static: reminder и eve зовут `WaitPopupChoice` / `ZuluChoiceDialog` с Pay (`JAZZ_MERC_PayAccount`) и Later; skip если `g_Combat`.
- `JAZZ-UI-MERC-002-AC-004` — static: quit пишет `CombatLog("important", …)` с именами.
- `JAZZ-UI-MERC-002-AC-005` — static: loc `890000000009944`–`009957` в `Russian.csv` и `English.csv`; `_check_lua_wrap_cycles.py` exit 0.
- `JAZZ-UI-MERC-002-AC-006` — runtime/human: сателлит, `balance > 0` → чип у денег; клик открывает MERC; day 7 popup+mail; day 9 popup; day 10 CombatLog+уход; Pay с чистого popup гасит долг и чип.
- `JAZZ-UI-MERC-002-AC-007` — static: `AddTimelineEvent` / `RemoveTimelineEvent` с id `jazz-merc-reminder` / `jazz-merc-quit`, typ `jazz_merc_debt`; def регистрируется в `SatelliteTimelineEvents`. Runtime/human: при долге иконка на time track (или future-events, если quit дальше 7d); после оплаты иконки нет.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: wrap `PDAMoneyText:Open` (satellite header only); `CreateZuluPopupChoice` / `WaitPopupChoice`; `OpenDialog("PDADialog")`; `AddTimelineEvent` / `SatelliteTimelineEvents.jazz_merc_debt` (runtime PlaceObj, не items.lua).
- Saves: existing campaigns — новые флаги `false` через `JAZZ_MERC_EnsureAccount`. Уже stage 2 не показывает eve. `[no new game]`.
- Network/determinism: popup UI как ванильный `ZuluChoiceDialog`; Pay тот же `AddMoney` path, что кнопка на сайте.
- Generated data: нет (Code + runtime CSV).
- Cross-package: только `jazz`.
- Rollback/recovery: вырезать chip/popup блоки; часы 7+3 и письма остаются.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: как во frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: `approved`
- Кто подтвердил: project-owner (chat: «1+2 давай», 2026-09-01)
- Дата: 2026-09-01

## Evidence

- `JAZZ-UI-MERC-002-AC-001`: `PASS` (static) — `python docs/tools/_check_merc_debt_alarm.py`: 7/3/2 clocks, `eve_popup_sent` / `reminder_popup_sent`, `lClearDebtAlarm`.
- `JAZZ-UI-MERC-002-AC-002`: `PASS` (static) — chip `idJazzMERCDebt`, `lInstallMoneyOpenWrap` / `g_JAZZ_MERC_MoneyOpenFn`, `JAZZ_MERC_OpenSite` + `browser_page = "merc"`.
- `JAZZ-UI-MERC-002-AC-003`: `PASS` (static) — `WaitPopupChoice` reminder/eve, Pay → `JAZZ_MERC_PayAccount`, Later, skip `g_Combat`.
- `JAZZ-UI-MERC-002-AC-004`: `PASS` (static) — `lLogQuitCombatLog` + loc `890000000009952`.
- `JAZZ-UI-MERC-002-AC-005`: `PASS` (static) — loc `890000000009944`–`009957` in both CSV; `python docs/tools/_check_lua_wrap_cycles.py` exit 0.
- `JAZZ-UI-MERC-002-AC-006`: `BLOCKED` (runtime/human) — satellite chip, popups, quit CombatLog.
- `JAZZ-UI-MERC-002-AC-007`: `PASS` (static) — `_check_merc_debt_alarm.py`: `AddTimelineEvent` / `RemoveTimelineEvent`, ids `jazz-merc-reminder` / `jazz-merc-quit`, typ `jazz_merc_debt`, `SatelliteTimelineEvents`. `BLOCKED` (runtime/human) — icons on the satellite time track.

## Documentation delta

- `docs/design/merc-recruiting-center.md`, `docs/technical/systems/units-progression-specializations.md`, `docs/technical/override-matrix.md`, `docs/wiki/merc-recruiting-center.md`, `docs/showcase/ru/merc.md`, `docs/showcase/en/merc.md`.
