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
`3280/6507` и заводским `7000` показывал 100%, хотя ожидаемый порядок —
низкие десятки процентов. У MP40 целевые ориентиры: 5% при 100% состояния,
6% при 90%, 10% при 80% и 100% только при нулевом состоянии. После первого
среза WEAPONS-010 mid-curve (~27% на том же Mosin) оставалась слишком
жёсткой для playtest; полный double-add mid/mid + rain ×2 снова давал
~29–39%. Follow-up: soft stack (dominant + half secondary) и более
мягкая mid-таблица — mid-якоря около **10%** сухо / **≤20%** под дождём.

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

- `JAZZ-WEAPONS-010-REQ-001` — базовый JamScore учитывает надёжность на
  шкале **5..95** (`Clamp(Reliability, 5, 95)`):
  `reliability_score = max(0, 100 - Reliability)`.
  При **Reliability ≥ 95** базовый риск = **0** даже с Poor/Crafted
  (положительный `BaseJamChance` игнорируется). Ниже 95 положительный
  `BaseJamChance` масштабируется ненадёжностью
  `scaled = MulDivRound(BaseJamChance, reliability_score, 95)`, затем
  `max(reliability_score, scaled)`; отрицательный по-прежнему вычитает из
  `reliability_score`. Результат ограничен `0..100` JamScore (0..10%).
- `JAZZ-WEAPONS-010-REQ-002` — текущее состояние =
  `current_resource / max_resource`, постоянный остаток =
  `max_resource / factory_resource`; обе величины считаются отдельно в
  целых процентах и получают одну таблицу аддитивной надбавки:

| Остаток | Надбавка к JamScore | Надбавка к шансу |
|---:|---:|---:|
| 100% | 0 | +0% |
| 90–99% | 10 | +1% |
| 80–89% | 50 | +5% |
| 70–79% | 55 | +5.5% |
| 60–69% | 60 | +6% |
| 50–59% | 80 | +8% |
| 40–49% | 110 | +11% |
| 30–39% | 160 | +16% |
| 20–29% | 230 | +23% |
| 10–19% | 320 | +32% |
| 1–9% | 450 | +45% |
| 0% | итог 1000 | 100% |

- `JAZZ-WEAPONS-010-REQ-003` — raw score до погоды =
  `base + max(condition_pen, permanent_pen) + DivRound(min(...), 2)`
  (полный худший износ + половина второго). Если оба остатка не ниже
  80%, raw score ограничен 100 (10%). Пока оба остатка >0, raw score
  дополнительно ≤990 (display 100% только при нуле). Дождь после
  этих потолков; итог `0..1000`. `Reliability` и `BaseJamChance`
  через `GetProperty` (ammo/component modifiers).
- `JAZZ-WEAPONS-010-REQ-004` — MP40 с базовыми свойствами
  (`Reliability=50`, `BaseJamChance=30`) и исправными патронами даёт
  5%/6%/10% при 100%/90%/80% текущего состояния и 100% при 0%;
  постоянный ресурс при этом 100%.
- `JAZZ-WEAPONS-010-REQ-005` — mid-resource якоря (без дождя): Mosin
  `3280/6507/7000` и `3080/4830/7000` дают **~10%** без повышающей
  ammo/component поправки; capped base 10% на `3280/6507/7000` —
  **~19%**. Под rain ×2 mid-якоря остаются **≤ ~20%**.
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
  condition/wear ≥80 для extreme weapon+ammo base; **Rel ≥ 95** даёт
  base 0% на идеальном ресурсе даже с extreme `BaseJamChance`.
- `JAZZ-WEAPONS-010-AC-004` — static audit подтверждает Mosin
  `3280/6507/7000`: 10% base / 19% capped; `3080/4830/7000`: 10%.
- `JAZZ-WEAPONS-010-AC-005` — runtime/human: rollover после ReloadLua
  для mid Mosin порядка ~10% сухо / ≤~20% под дождём, не 29–39%.

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
  постоянный износ, Mosin в низких десятках %, Reliability обязателен;
  follow-up: mid-curve softened; Rel 5..95 / Rel95 = 0 base; follow-up:
  soft wear stack + softer mid so rain mid ≤~20%, 100% only at 0).
- Дата: 2026-08-07.

## Evidence

- `JAZZ-WEAPONS-010-AC-001`: `PASS` — static:
  `_audit_weapon_jam_balance.py`; MP40 100/90/80/0 anchors match.
- `JAZZ-WEAPONS-010-AC-002`: `PASS` — static: audit parses the runtime
  helper and verifies the shared soft mid-step condition/permanent-wear table.
- `JAZZ-WEAPONS-010-AC-003`: `PASS` — static: all compatible
  Poor/Crafted pairs stay ≤10% at normal resource; extreme base cap = 10%.
- `JAZZ-WEAPONS-010-AC-004`: `PASS` — static: Mosin
  `3280/6507/7000` = 10% / 19% capped; `3080/4830/7000` = 10%.
- `JAZZ-WEAPONS-010-AC-005`: `BLOCKED` — runtime/human: ReloadLua +
  rollover under dry/rain after soft-stack pass.

status note: code/static/docs complete; keep `approved` until AC-005 runtime
smoke, then mark `implemented`.

## Documentation delta

- `docs/technical/systems/weapons-ammo-components.md` — current-state formula.
- `docs/wiki/weapons-and-ammo.md` — player-facing condition/wear behavior.
- `docs/showcase/ru/weapons-and-ammo.md` и
  `docs/showcase/en/weapons-and-ammo.md` — двуязычная витрина.
