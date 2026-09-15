---
id: JAZZ-MED-008
status: approved
owner: project-owner
systems:
  - armor-damage-wounds-will
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - Code/Systems_Medicine.lua
  - CharacterEffect/WoundInfected.lua
  - items.lua
  - Russian.csv
  - English.csv
  - Localization/Strings.csv
  - docs/specs/active/JAZZ-MED-008.md
  - docs/specs/active/JAZZ-MED-002.md
  - docs/specs/active/JAZZ-FEEDBACK-001.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
  - docs/tools/_check_infection_nonlethal.py
  - docs/tools/README.md
exclusive_resources:
  - jazz/items.lua
  - jazz/Localization/Strings.csv
related_decisions:
  - JAZZ-MED-002
approved_by: project-owner
---

# JAZZ-MED-008: защита квестовых NPC от смерти при инфекции

## Проблема

JazzKillMercFromInfection напрямую вызывает Die либо обнуляет HitPoints и меняет HireStatus на Dead, обходя immortal. Квестовые NPC могут погибнуть вне боя и заблокировать квест.

## Цели

Сохранить смерть от инфекции у бойцов игрока и обычных врагов; защитить immortal и важных сюжетных NPC (ImportantNPC/villain), пока они не входят в отряд игрока и не являются наёмниками. Бессмертие имеет приоритет над принадлежностью.

## Non-goals

Воскрешение уже умерших NPC, ремонт квестовых флагов, госпитализация, изменение боевого урона, кровотечения и лечения травм.

## Требования

- `JAZZ-MED-008-REQ-001` — проверять immortal на Unit/UnitData; ImportantNPC/villain защищены, кроме наёмников и членов player1/player2 отрядов. Провал защищённого NPC оставляет инфекцию и переносит проверку на 16 часов у обоих представлений. У обычных врагов и бойцов игрока смертельная ветка и RNG остаются прежними.
- `JAZZ-MED-008-REQ-002` — сам JazzKillMercFromInfection также проверяет защиту до сообщения о смерти, Die, изменения HP/HireStatus/отряда; прямой вызов безопасен для защищённого NPC.
- `JAZZ-MED-008-REQ-003` — документация отражает исключение. Описание WoundInfected «может быть смертельно» остаётся верным; generated data и локализация не меняются. Уточняет MED-002 REQ-003.

## Инварианты и ограничения

Лечение инфекции и её возникновение не меняются. Сохранения не редактировать. Существующий dirty state сохранить.

## Acceptance criteria

- `JAZZ-MED-008-AC-001` — Lua-harness: неудачная проверка важных NPC и immortal сохраняет состояние/переносит таймер обоих представлений; обычные враги и бойцы игрока умирают как раньше; успешная проверка очищает инфекцию; прямой kill-helper соблюдает защиту.
- `JAZZ-MED-008-AC-002` — Lua syntax и документация согласованы, generated/локализация не изменены.
- `JAZZ-MED-008-AC-003` — игровой прогон через Steam: защищённый NPC переживает срок инфекции; проверяется таймер после save/load.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: меняется только JAZZ infection path, новые hooks отсутствуют.
- Saves: существующие инфекции продолжаются; мёртвые не воскрешаются.
- Network/determinism: прежний RNG-вызов сохранён, новый случайный выбор не добавляется.
- Generated data: не меняются.
- Cross-package references: нет изменений.
- Rollback/recovery: откат только собственного diff.

## План и ownership

- Пакет-владелец: jazz.
- Исполнитель: текущий агент; reviewer: владелец проекта.
- Declared write set: frontmatter.
- Exclusive resources: items и каталог локализации.

## Решение владельца

- Статус: approved.
- Кто подтвердил: пользователь — «смерти от заражения надо убрать, особенно у тех кто помечен бессмертным … квестовые нпц не должны так умирать».
- Дата: 2026-09-15.

## Evidence

- `JAZZ-MED-008-AC-001`: `PASS` — _check_infection_nonlethal.py: live/data flags, стратегический NPC, twin timers, direct helper, обычная смерть live/data, наёмник/отряд игрока, приоритет immortal, recovery/dead guard.
- `JAZZ-MED-008-AC-002`: `PASS` — изменённый Lua исполняется в harness; документация обновлена. Generated data и локализация не менялись.
- `JAZZ-MED-008-AC-003`: `BLOCKED` — runtime/editor ещё не проверены.

## Documentation delta

Медицинский раздел technical, wiki и showcase RU/EN; MED-002 получает явную ссылку на замену смертельного исхода, FB-06 — новое состояние.

Уточнение владельца: смерть остаётся у юнитов игрока и легионеров; главная цель — квестовые NPC. Широкая отмена смертей не реализовывалась.
