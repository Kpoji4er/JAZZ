---
id: JAZZ-WEAPONS-010
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/System_Firearm_AddProperties.lua
  - jazz/docs/tools/_audit_weapon_jam_balance.py
  - jazz/docs/tools/README.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/specs/active/JAZZ-WEAPONS-001.md
  - jazz/docs/specs/active/JAZZ-WEAPONS-008.md
  - jazz/docs/specs/active/JAZZ-WEAPONS-010.md
exclusive_resources:
  - none
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-001
  - JAZZ-WEAPONS-008
approved_by: project-owner
---

# JAZZ-WEAPONS-010: мягкие ступени клина по состоянию и износу

## Проблема

Формула WEAPONS-001/008 умножает весь базовый риск оружия и патронов на
`3/6/12/18`. Поэтому один переход порога резко разгоняет клин, а плохие
патроны умножаются второй раз. В runtime-примере Mosin с текущим ресурсом
`3280/6507` и заводским `7000` показывает 100%, хотя ожидаемый порядок —
около 30%. У MP40 целевые ориентиры: 5% при 100% состояния, 6% при 90%,
10% при 80% и 100% только при нулевом состоянии.

## Цели

- вернуть мягкую ступенчатую кривую без умножения базового риска;
- считать текущее состояние и постоянный износ раздельно и одинаково;
- сохранить влияние `Reliability`, `BaseJamChance`, патронов и компонентов;
- ограничить базовый риск исправного оружия 10% даже для плохой платформы
  с плохими патронами.

## Non-goals

- массовый ребаланс `Reliability` / `BaseJamChance` в generated data;
- смена Mechanical `/120` и `/150`, single-shot `/2` или RNG `0..999`;
- изменение износа ресурса за выстрел, jam damage или Unjam.

## Требования

- `JAZZ-WEAPONS-010-REQ-001` — базовый JamScore учитывает надёжность:
  `reliability_score = max(0, 100 - Reliability)`. Положительный
  `BaseJamChance` задаёт альтернативный минимум риска
  `max(reliability_score, BaseJamChance)`, отрицательный уменьшает
  `reliability_score`; результат ограничен `0..100` JamScore (0..10%).
- `JAZZ-WEAPONS-010-REQ-002` — текущее состояние =
  `current_resource / max_resource`, постоянный остаток =
  `max_resource / factory_resource`; обе величины считаются отдельно в
  целых процентах и получают одну таблицу аддитивной надбавки:

| Остаток | Надбавка к JamScore | Надбавка к шансу |
|---:|---:|---:|
| 100% | 0 | +0% |
| 90–99% | 10 | +1% |
| 80–89% | 50 | +5% |
| 70–79% | 100 | +10% |
| 60–69% | 150 | +15% |
| 50–59% | 250 | +25% |
| 40–49% | 350 | +35% |
| 30–39% | 500 | +50% |
| 20–29% | 650 | +65% |
| 10–19% | 800 | +80% |
| 1–9% | 950 | +95% |
| 0% | итог 1000 | 100% |

- `JAZZ-WEAPONS-010-REQ-003` — raw score до погоды =
  `base + condition_penalty + permanent_wear_penalty`. Если оба остатка
  не ниже 80%, raw score ограничен 100 (10%). Дождь применяется после
  этого базового потолка; итог ограничен `0..1000`.
- `JAZZ-WEAPONS-010-REQ-004` — MP40 с базовыми свойствами
  (`Reliability=50`, `BaseJamChance=30`) и исправными патронами даёт
  5%/6%/10% при 100%/90%/80% текущего состояния и 100% при 0%;
  постоянный ресурс при этом 100%.
- `JAZZ-WEAPONS-010-REQ-005` — Mosin `3280/6507`, factory `7000`
  даёт порядок десятков процентов, а не 100%: 27% без повышающей
  ammo/component поправки и не более 36% при capped base 10%.
- `JAZZ-WEAPONS-010-REQ-006` — Mechanical, вторичный merc skill term,
  single-shot `/2`, JamScore display `/10` и deterministic RNG не меняются.

## Инварианты и ограничения

- только integer math (`MulDivRound`, `DivRound`, `Clamp`);
- никаких новых RNG-вызовов и изменений порядка roll;
- save/network schema и публичные IDs не меняются;
- `items.lua`, companions и metadata не меняются.

## Acceptance criteria

- `JAZZ-WEAPONS-010-AC-001` — static audit подтверждает MP40
  `100→5%`, `90→6%`, `80→10%`, `0→100%`.
- `JAZZ-WEAPONS-010-AC-002` — static audit подтверждает одинаковую
  таблицу для condition и permanent wear.
- `JAZZ-WEAPONS-010-AC-003` — static audit подтверждает cap 10% при
  condition/wear ≥80 для extreme weapon+ammo base.
- `JAZZ-WEAPONS-010-AC-004` — static audit подтверждает Mosin
  `3280/6507/7000`: 27% при base 1% и 36% при base cap 10%.
- `JAZZ-WEAPONS-010-AC-005` — runtime/human: rollover после ReloadLua
  больше не показывает 100% для предоставленного Mosin и следует
  ожидаемому порядку около 30%.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: меняется только JAZZ override jam formula.
- Saves: существующие resource/current/max и ammo modifiers читаются без
  миграции; меняются только будущие расчёты.
- Network/determinism: RNG и порядок вызовов не меняются.
- Generated data: отсутствует.
- Cross-package references: отсутствуют.
- Rollback/recovery: revert перечисленного write set.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner/runtime playtest.
- Declared write set: frontmatter.
- Exclusive resources: none.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner (ориентиры MP40, cap 10%, отдельный
  постоянный износ, Mosin около 30%, Reliability обязателен).
- Дата: 2026-08-07.

## Evidence

- `JAZZ-WEAPONS-010-AC-001`: `PASS` — static:
  `_audit_weapon_jam_balance.py`; MP40 100/90/80/0 anchors match.
- `JAZZ-WEAPONS-010-AC-002`: `PASS` — static: audit parses the runtime
  helper and verifies the shared 11-step condition/permanent-wear table.
- `JAZZ-WEAPONS-010-AC-003`: `PASS` — static: all 150 compatible
  Poor/Crafted pairs stay ≤10% at normal resource; extreme base cap = 10%.
- `JAZZ-WEAPONS-010-AC-004`: `PASS` — static: Mosin
  `3280/6507/7000` = 27% base / 36% with capped bad-ammo base.
- `JAZZ-WEAPONS-010-AC-005`: `BLOCKED` — runtime/human: DAP probe on
  `127.0.0.1:8165` was not listening; ReloadLua and rollover check remain.

status note: code/static/docs complete; keep `approved` until AC-005 runtime
smoke, then mark `implemented`.

## Documentation delta

- `docs/technical/systems/weapons-ammo-components.md` — current-state formula.
- `docs/wiki/weapons-and-ammo.md` — player-facing condition/wear behavior.
- `docs/showcase/ru/weapons-and-ammo.md` и
  `docs/showcase/en/weapons-and-ammo.md` — двуязычная витрина.
