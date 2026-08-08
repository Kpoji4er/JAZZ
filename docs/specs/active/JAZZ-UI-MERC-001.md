---
id: JAZZ-UI-MERC-001
status: approved
owner: project-owner
systems:
  - assets-and-ui
  - units-progression-specializations
  - localization
repositories:
  - jazz
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/System_MERC_*.lua
  - Code/System_AME_Browser.lua
  - Code/System_AimHiringFilters.lua
  - items.lua
  - metadata.lua
  - English.csv
  - Russian.csv
  - Icons/PDA/
  - docs/design/_merc-logo/
  - docs/specs/active/JAZZ-UI-MERC-001.md
  - docs/design/merc-recruiting-center.md
  - docs/design/mercs-ja12/biff.md
  - docs/technical/systems/file-coverage.md
  - docs/technical/systems/units-progression-specializations.md
  - docs/wiki/
  - docs/showcase/
  - ../jazz-units/UnitData/Jazz_*.lua
  - ../jazz-units/items.lua
  - ../jazz-units/metadata.lua
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz-units/items.lua
  - jazz-units/metadata.lua
related_decisions:
  - none
related_specs:
  - JAZZ-UNITS-005
  - JAZZ-UI-AME-001
  - JAZZ-UNITS-002
  - JAZZ-QUESTS-002
approved_by: project-owner
---

# JAZZ-UI-MERC-001: M.E.R.C. — сайт и найм (JA2-style)

## Проблема

Именные бойцы с `affiliation: MERC` в `docs/design/mercs-ja12/` либо сидят в AIM без отдельного бренда, либо у UnitData нет `Affiliation = "MERC"`. Нет JA2-опыта **More Economic Recruiting Center**: сайт, Speck, кредитный счёт, просьба найти Биффа.

**A.M.E.** ([`JAZZ-UNITS-005`](JAZZ-UNITS-005.md)) остаётся отдельным локальным рынком.

## Цели

- PDA browser **M.E.R.C.** (mode `merc`).
- Найм MERC только с сайта MERC (AIM All без Available MERC).
- Speck — UI/mail persona.
- Credit account (долг → Pay → reminder → quit).
- Unlock сайта: письмо Speck **«найдите Биффа»** (+ проза «контора снова открыта»).
- Shelf-immediate design MERC (без Biff) Available после unlock; world-gated → после встречи.
- **Все нужные PDA/бренд-картинки** генерирует агент в том же wave (не ждать owner art).

## Non-goals

- Ребрендинг AME; патронаж tiers; Speck hireable; роспуск конторы.
- `Flay` / `Pierre` в пуле MERC (Locals).
- Дублировать vanilla NPC `Biff` как второго hireable рядом с `Jazz_Biff`.
- Новые карты/сектора под Biff (hook существующий RescueBiff / meet; при необходимости только glue в `jazz`/`jazz-maps` без нового level design).
- Анонимный AME-пул / JoinedLegion; rewrite AIM/AME prepaid; новые portrait/voice banks.

## Owner decisions (locked 2026-08-08)

| # | Решение |
| --- | --- |
| D1 | Credit account — да |
| D2 | Вкладка **locked** до письма Speck; письмо = unlock |
| D3–D5 | После unlock: весь shelf-immediate Available; patronage — later |
| D6 | Speck только UI/mail |
| D7 | World-gated: `Jazz_Biff`, `Larry`/`Larry_Clean`, `Smiley`. **Не** Flay, **не** Pierre |
| D8 | Один wave |
| D9 | Welcome/unlock mail: художественная проза «M.E.R.C. снова открыт» + **просьба найти Биффа**; JA3 lore-safe |
| D10 | **Ассеты:** агент сам генерит все PDA chrome / logo / banner / backdrop (и прочие UI-картинки, нужные сайту); стиль JA3 PDA, визуально **не** AIM и **не** AME ochre |

### Пул v1 (канон)

**Shelf-immediate (14):** `Jazz_Flo`, `Jazz_Cougar`, `Jazz_Madman`, `Jazz_Blade`, `Jazz_Conrad`, `Jazz_Dynamo`, `Jazz_Gaston`, `Jazz_Nervous`, `Jazz_Ricochet`, `Jazz_Cord`, `Jazz_Hobbit`, `Jazz_Horg`, `Jazz_Meat`, `Jazz_Shank`.

**World-gated:**

| id | Notes |
| --- | --- |
| `Jazz_Biff` | Наш Biff. До find — не на витрине. Meet/rescue (предпочтительно vanilla **RescueBiff** pipeline) → hire на месте **или** `Available` на MERC. |
| `Larry` / `Larry_Clean` | Vanilla F7 + Metaviron; оба persona id. |
| `Smiley` | Vanilla Smiley questline. |

**Исключены:** `Flay`, `Pierre` (местные); отдельный vanilla hireable `Biff`, если он есть — не второй слот (используем `Jazz_Biff`).

## Требования

### Сайт и chrome

- `JAZZ-UI-MERC-001-REQ-001` — mode `merc`, отдельный skin; URL `http://www.merc.com/`.
- `JAZZ-UI-MERC-001-REQ-002` — паттерн AME browser; Loadout **с** Traits/Perks.
- `JAZZ-UI-MERC-001-REQ-003` — вкладка `merc` **locked** до unlock-mail; после — `locked = false`; AIM/AME/Bobby/IMP/R.I.S. без регрессий.
- `JAZZ-UI-MERC-001-REQ-003a` — сгенерировать и зашить runtime PNG (минимум, зеркало AME-набора):
  - `Icons/PDA/MERC_Mark.png` — mark / HazOS-замена;
  - `Icons/PDA/MERC_BannerPad.png` — баннер вместо AIM;
  - `Icons/PDA/MERC_PdaBackdrop.png` — backdrop;
  - concept-итерации в `docs/design/_merc-logo/` (необязательно в runtime).
  Бренд: дешёвый конкурент AIM (Speck/MERC), **без** африканского щита AME и без vanilla AIM blue chrome clone. Owner art не блокирует ship.

### Roster и affiliation

- `JAZZ-UI-MERC-001-REQ-004` — roster table shelf vs world-gated; ids → `Affiliation = "MERC"` (`Larry`/`Smiley`/`Jazz_*` по списку).
- `JAZZ-UI-MERC-001-REQ-005` — AIM не показывает Available MERC; Hired могут быть в AIM My Team.
- `JAZZ-UI-MERC-001-REQ-006` — все 14 shelf + `Jazz_Biff` UnitData: `Affiliation = "MERC"`.
- `JAZZ-UI-MERC-001-REQ-007` — visibility: Available; world-gated до meet hidden; Hired My Team; Dead/MIA grayed.
- `JAZZ-UI-MERC-001-REQ-008` — после unlock: shelf-immediate → Available; world-gated → not listed until meet.
- `JAZZ-UI-MERC-001-REQ-009` — meet без hire → MERC Available; world hire → Hired.
- `JAZZ-UI-MERC-001-REQ-010` — `Jazz_Biff` связан с существующим RescueBiff/meet (не параллельный клон vanilla Biff на полке).

### Credit account

- `JAZZ-UI-MERC-001-REQ-011` — `gv_JAZZ_MERC_Account`: `balance`, `paid_total`, `last_reminder_day`, `warning_stage`.
- `JAZZ-UI-MERC-001-REQ-012` — Hire без полной предоплаты; daily → `balance`.
- `JAZZ-UI-MERC-001-REQ-013` — Pay Account: −balance, +paid_total.
- `JAZZ-UI-MERC-001-REQ-014` — reminder ~7d при balance>0; grace **+3d** → quit hired MERC.
- `JAZZ-UI-MERC-001-REQ-015` — AIM/AME prepaid не трогать.

### Mail / persona

- `JAZZ-UI-MERC-001-REQ-016` — Emails: `MERC_Welcome` (unlock), `MERC_AccountReminder`, `MERC_QuitWarning`; sender Speck / M.E.R.C.; RU+EN.
- `JAZZ-UI-MERC-001-REQ-017` — `MERC_Welcome` **открывает** вкладку `merc` (`welcome_sent` / unlock flag; без replay на Load).
- `JAZZ-UI-MERC-001-REQ-018` — тело welcome = **художественная проза**: M.E.R.C. снова открыт **и** просьба **найти Биффа** (сооснователь пропал / не выходит на связь — без спойлера точного квест-маршрута, но с мотивацией открыть сайт и искать). Кратко: PDA-вкладка MERC + credit account.
- `JAZZ-UI-MERC-001-REQ-019` — JA3 lore-safe: AIM жив; без Arulco/Deidranna как факта кампании; без «мы заменили AIM»; тон Speck.
- `JAZZ-UI-MERC-001-REQ-020` — timing unlock-mail: early campaign (**default Day 2** от старта, как JA2 Speck ping; не NewGame-frame spam). Owner может сдвинуть одной константой.
- `JAZZ-UI-MERC-001-REQ-021` — reminder/quit — голос Speck, короче; без R.I.S./AME.

### Localization / docs

- `JAZZ-UI-MERC-001-REQ-022` — RU+EN; welcome — независимая проза, не калька.
- `JAZZ-UI-MERC-001-REQ-023` — design companion + technical + wiki + showcase; обновить `biff.md` Hire/Access (world-gated + Speck mail).

## Инварианты и ограничения

- AME без регрессий; AIM prepaid без регрессий.
- Deterministic mail/quit/unlock.
- Saves: Affiliation migrate; tab locked until unlock; world-gated hidden until meet; **Speck welcome** via `JAZZ_MERC_MigrateWelcomeFromSave` on LoadGame (inbox recover or one-shot send if day≥2).
- Нет R.I.S. branding.

## Acceptance criteria

- `JAZZ-UI-MERC-001-AC-001` — NewGame: `merc` locked; после Day-2 Speck mail — unlocked; сайт открывается.
- `JAZZ-UI-MERC-001-AC-002` — после unlock: 14 shelf Available на MERC, не в AIM All; `Jazz_Biff` ещё нет.
- `JAZZ-UI-MERC-001-AC-003` — hire credit + Pay Account работают.
- `JAZZ-UI-MERC-001-AC-004` — reminder+grace → quit; оплата → нет quit.
- `JAZZ-UI-MERC-001-AC-005` — после find Biff/Larry/Smiley без hire → Available на MERC; Flay/Pierre никогда не в MERC roster.
- `JAZZ-UI-MERC-001-AC-006` — static Affiliation + `_validate_items_quick.py` OK.
- `JAZZ-UI-MERC-001-AC-007` — human: welcome = проза «открыты + найдите Биффа», lore-safe; chrome/mark/banner отличимы от AIM и AME.
- `JAZZ-UI-MERC-001-AC-008` — AME/AIM smoke unchanged.

## Impact и совместимость

- Vanilla: PDA lock, Email, HireMerc, RescueBiff/Larry/Smiley meet, Affiliation.
- Saves: `[new game recommended]` ок.
- Cross-package: `jazz` UI/mail/credit; `jazz-units` Affiliation; maps quests только glue при необходимости.
- Rollback: drop MERC code/mail; revert Affiliation.

## План и ownership

- Approve → design companion → implement → docs → runtime evidence.

## Решение владельца

- Статус: `approved`
- Кто подтвердил: project-owner (chat: «апрув», 2026-08-08)
- Дата: 2026-08-08
- Decisions D1–D10 locked as in table above.

## Evidence

- Все `AC-*`: `BLOCKED`.

## Documentation delta

- Implemented draft: `docs/design/merc-recruiting-center.md`, `docs/wiki/merc-recruiting-center.md`, `docs/showcase/ru|en/merc.md` + `pages.json`, `file-coverage.md`, `units-progression-specializations.md`, `biff.md` Hire access.
- Evidence AC still mostly `BLOCKED` until NewGame/Day2/credit playtest.
