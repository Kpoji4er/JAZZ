---
id: JAZZ-WEAPONS-009
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
  - combat-cth-actions
  - combat-ai
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/items.lua
  - jazz/Code/AccuracyRangeCTH.lua
  - jazz/Code/CombatAI.lua
  - jazz/scripts/test-shooting-model.ps1
  - jazz/docs/technical/weapons/combat-actions.md
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/testing.md
  - jazz/docs/wiki/combat-actions.md
  - jazz/docs/showcase/ru/combat-actions.md
  - jazz/docs/showcase/en/combat-actions.md
  - jazz/docs/specs/active/JAZZ-WEAPONS-009.md
  - jazz/metadata.lua
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - CombatAction:MGBurstFire
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-003
  - JAZZ-WEAPONS-008
approved_by: project-owner
---

# JAZZ-WEAPONS-009: цена и отдача MGBurstFire

## Проблема

`MGBurstFire` сейчас получает длинную очередь без собственной AP-наценки и одновременно снижает authored `Recoil` оружия множителем `0.8`. На ручных пулемётах с `AutoShots` это даёт слишком много ожидаемого урона на ОД, а AI оценивает такую атаку как короткий `BurstShots` и не видит её фактическую длину.

## Цели

- Вернуть обычному `MGBurstFire` различимую цену за burst-length и auto-length очередь.
- Убрать общий скрытый бонус `0.8 × Recoil`, сохранив уже существующую ценность стойки, опоры, сошек и именной атаки Гризли.
- Синхронизировать AI-прогноз с фактическими выстрелами `GetAutofireShots`.

## Non-goals

- Изменение `Suppression`/suppression bonus, включая его текущее суммирование.
- Изменение постоянного пулемётного сектора и бесплатных interrupt-атак.
- Изменение Damage, ShootAP, Recoil, BurstShots, AutoShots или других базовых характеристик оружия.
- Изменение количества дополнительных пуль именных перков Buzz/Nervous.

## Требования

- `JAZZ-WEAPONS-009-REQ-001` — `MGBurstFire:GetAPCost` добавляет 1 AP к базовой атаке, если authored очередь равна `BurstShots`, и 2 AP, если `GetAutofireShots` выбирает более длинный `AutoShots`.
- `JAZZ-WEAPONS-009-REQ-002` — AP-наценка определяется authored длиной очереди до runtime-добавок именных перков; дополнительные пули Buzz/Nervous не повышают стоимость.
- `JAZZ-WEAPONS-009-REQ-003` — обычный `MGBurstFire` начинает расчёт отдачи с полного authored `weapon.Recoil`; stance/support/bipod/Strength/AutoWeapons продолжают применять общий профиль.
- `JAZZ-WEAPONS-009-REQ-004` — `GrizzlyPerk` сохраняет собственную пулемётную severity `0.8 × Recoil` и персональный action factor `0.55`, даже когда использует executor `MGBurstFire`.
- `JAZZ-WEAPONS-009-REQ-005` — AI для `MGBurstFire` прогнозирует фактическое число выстрелов через `weapon:GetAutofireShots(action)` и использует реальную стоимость action.
- `JAZZ-WEAPONS-009-REQ-006` — suppression wrappers, бесплатные sector attacks, базовые оружейные характеристики и число выпущенных пуль не меняются.

## Инварианты и ограничения

- AP хранится в тысячных: `1000 == 1 AP`.
- Длина очереди для цены читается только из authored `BurstShots`/`AutoShots`; временные эффекты персонажа не должны менять UI reservation.
- CombatAction id, публичные ID, save/network contract и порядок RNG не меняются.
- Источник generated CombatAction остаётся в `items.lua`; нового companion-файла не создаётся.

## Acceptance criteria

- `JAZZ-WEAPONS-009-AC-001` — static/model: burst-length MG получает `+1000`, auto-length MG получает `+2000`; BAR 7→8 AP, RPK 8→10 AP, PKM 9→10 AP.
- `JAZZ-WEAPONS-009-AC-002` — static/model: обычный `MGBurstFire` использует action recoil factor `1.0`, `GrizzlyPerk` сохраняет `0.8`, а prone/support продолжают улучшать retention.
- `JAZZ-WEAPONS-009-AC-003` — static: AI-ветка `MGBurstFire` вызывает `GetAutofireShots(action)`; для RPK прогнозируется 7, а не 4 выстрела.
- `JAZZ-WEAPONS-009-AC-004` — static diff: suppression wrappers/constants, `MGFreeInterruptAttacks`, weapon stats и shot-count executor не изменены.
- `JAZZ-WEAPONS-009-AC-005` — automated: `scripts/test-shooting-model.ps1` и проверки документации завершаются успешно.
- `JAZZ-WEAPONS-009-AC-006` — generated-data audit не показывает новых рассинхронизаций; `MGBurstFire` остаётся единственным активным ModItem данного id.
- `JAZZ-WEAPONS-009-AC-007` — human/runtime: tooltip/reservation и фактическое списание AP совпадают для burst-length и auto-length MG; очередь, suppression и сектор работают как до изменения.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: меняется только JAZZ override `MGBurstFire` и его JAZZ CTH/AI-модель; внешние сигнатуры не меняются.
- Saves: миграция не нужна; CombatAction и оружейные class ids сохранены.
- Network/determinism: новых RNG-вызовов нет, порядок симуляции не меняется.
- Generated data: точечная транзакция существующего `ModItemCombatAction` в `items.lua`; metadata registration без новых путей.
- Cross-package references: изменений в `jazz-assets`, `jazz-maps`, `jazz-units`, `jazz-nomaps` нет.
- Rollback/recovery: откатить change set целиком; прежние AP/recoil/AI-контракты возвращаются вместе.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: front matter `write_set`.
- Exclusive resources: `items.lua`, `metadata.lua`, `CombatAction:MGBurstFire`.

## Решение владельца

- Статус: approved — реализовать и запушить.
- Кто подтвердил: project-owner.
- Дата: 2026-08-06.

## Evidence

- `JAZZ-WEAPONS-009-AC-001`: `PASS` — shooting model: BAR 8 AP, RPK 10 AP, PKM 10 AP; burst/auto surcharge 1000/2000.
- `JAZZ-WEAPONS-009-AC-002`: `PASS` — shooting model: обычный MGBurst factor 1.0, Grizzly `0.8 × 0.55`, prone/support retention выше standing.
- `JAZZ-WEAPONS-009-AC-003`: `PASS` — source/model: AI вызывает `weapon:GetAutofireShots(action)`; fixture RPK = 7 выстрелов.
- `JAZZ-WEAPONS-009-AC-004`: `PASS` — scoped runtime diff: forbidden changes suppression/free-interrupt/weapon stats/shot helpers = 0; MGBurst id count = 1.
- `JAZZ-WEAPONS-009-AC-005`: `BLOCKED` — shooting model и `git diff --check` PASS; общий docs-аудит падает на 1529 pre-existing diagnostics, при этом changed-path hits = 0.
- `JAZZ-WEAPONS-009-AC-006`: `PASS` — strict `check-generated-sync.ps1 -Package jazz`: errors=0, warnings=0; CommonLib upstream 1.11 build 1059 (`f023a031…`), dependency 1.11 актуальна.
- `JAZZ-WEAPONS-009-AC-007`: `BLOCKED` — требуется runtime/human playtest в JA3.

status note: static implementation complete; keep `approved` until runtime/human playtest and repository-wide docs baseline are green.

## Documentation delta

- `docs/technical/weapons/combat-actions.md` и `docs/technical/systems/combat-cth-actions.md` — AP/recoil contract и исключение Grizzly.
- `docs/technical/systems/ai-awareness.md`, `docs/technical/testing.md` — AI parity и статические проверки.
- `docs/wiki/combat-actions.md`, showcase RU/EN combat-actions — player-facing цена длинной очереди и отсутствие общего recoil-discount.
