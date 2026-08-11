---
id: JAZZ-COMBAT-003
status: implemented
owner: project-owner
systems:
  - armor-damage-wounds-will
  - combat-cth-actions
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - Code/System_OR_Unit.lua
  - Code/CombatActions.lua
  - items.lua
  - CharacterEffect/suppressionPinned.lua
  - metadata.lua
  - Russian.csv
  - English.csv
  - Localization/Strings.csv
  - docs/specs/active/JAZZ-COMBAT-003.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/technical/systems/combat-cth-actions.md
  - docs/technical/override-matrix.md
  - docs/technical/testing.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - items.lua
  - metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMBAT-003: suppression retaliation, Lightning Reaction, Psycho Will

## Проблема

Из playtest/Discord (Sergej 1973 / owner triage):

1. Полностью подавленные (`suppressionPinned`) всё ещё могут контратаковать (Retaliate / Hotblood / Shatterhand / HaveABlast). Частичное подавление не даёт согласованного штрафа на ответный огонь — CTH-модификатор `Suppression` срабатывал только дальше 5 клеток.
2. `LightningReaction` / `LightningReactionNPC` срабатывают на скрытные/stealth-kill атаки; у NPC-версии из‑за precedence `and`/`or` handler заходит на unaware-цели даже после `used`. Шанс для перка без параметра `chance` фактически 100%.
3. `Psycho` каждый `BeginTurn` теряет 8 Will без regen-path и не получает CombatEnd restore (у него нет suppression-эффектов с `OnCombatEnd` restore) → срыв/Berserk уже на первом ходу следующего боя.

## Цели

- `suppressionPinned` блокирует `Unit:Retaliate`; частичное подавление режет шанс Retaliate той же шкалой, что Lightning Reaction (`×90/×80/×70/×60`, pinned = 0).
- Частичное подавление режет CTH ответного/обычного огня по той же шкале (−10/−20/−30/−50/−70), без дистанции ≥5.
- Lightning Reaction: default chance **50%**; не срабатывает, если атакующий в `Hidden` / `stealth_attack` / есть `stealth_kill_chance`; шанс режется тиром подавления цели (см. REQ-003), на `suppressionPinned` = **0**.
- Psycho: drain Will за ход снижен (8→4); после боя Will восстанавливается до max у всех живых human units.

## Non-goals

- Перебаланс всей suppression ladder / AI pinned behavior.
- Удаление перков Hotblood / Shatterhand / HaveABlast.
- Смена Berserk-порога Psycho или иммунитета к Will damage от огня.
- Generated round-trip Mod Editor для новых CharacterEffect IDs (только текст `suppressionPinned` + CTH CalcValue).

## Требования

- `JAZZ-COMBAT-003-REQ-001` — `Unit:Retaliate` (Hotblood / Shatterhand / HaveABlast / Killzone и др.): шанс прохождения gate = множитель тира подавления цели (`Light×90` / `Medium×80` / `Heavy×70` / `Heavy2×60`); при `suppressionPinned` сразу `false` без roll.
- `JAZZ-COMBAT-003-REQ-002` — CTH modifier `Suppression` применяет tier-штрафы атакующего независимо от дистанции (в т.ч. opportunity/retaliation).
- `JAZZ-COMBAT-003-REQ-003` — `Unit:LightningReactionCheck`: chance по умолчанию 50, если параметр отсутствует; skip при Hidden / stealth_attack / stealth_kill_chance>0 у текущей firearm-атаки; после base chance применяется мягкий множитель тира подавления цели (`Light×90` / `Medium×80` / `Heavy×70` / `Heavy2×60`); при `suppressionPinned` итоговый chance = **0** (roll не нужен).
- `JAZZ-COMBAT-003-REQ-004` — `Unit:RecalcWillPoints` для Psycho без Berserk вычитает **4** Will (не 8).
- `JAZZ-COMBAT-003-REQ-005` — на `CombatEnd` у живых human `WillPoints = MaxWillPoints` (после `RecalcMaxWillPoints`).

## Инварианты и ограничения

- Публичные ID эффектов/перков не меняются.
- Deterministic RNG: Retaliate — один `self:Random(100)` на partial suppression gate (pinned без roll); LR по-прежнему `self:Random(100)` после mul; CTH без нового RNG.
- Save/network: новых persistent fields нет; MapVar только на время FirearmAttack.
- Psycho по-прежнему не получает suppression tiers и Will damage от огневого подавления.

## Acceptance criteria

- `JAZZ-COMBAT-003-AC-001` — static: `Unit:Retaliate` early-out на `suppressionPinned` + partial mul gate (`×90/80/70/60`).
- `JAZZ-COMBAT-003-AC-002` — static: `Suppression` CTH CalcValue без порога 5 slabs.
- `JAZZ-COMBAT-003-AC-003` — static: `LightningReactionCheck` default chance 50 + stealth skip + suppression multipliers / pinned=0; FirearmAttack stashes attacker/args до CallReactions.
- `JAZZ-COMBAT-003-AC-004` — static: Psycho drain = 4; `OnMsg.CombatEnd` восстанавливает Will.
- `JAZZ-COMBAT-003-AC-005` — docs: technical + wiki + showcase RU/EN описывают контракт.
- `JAZZ-COMBAT-003-AC-006` — runtime/human: pinned не отвечает; stealth kill не даёт LR float; Psycho не стартует следующий бой с пустым Will.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: overrides `Unit:Retaliate`, `Unit:LightningReactionCheck`; правит JAZZ CTH modifier и Will regen. CommonLib 1.11 не владеет этими символами.
- Saves: без миграции.
- Network/determinism: сохраняется.
- Generated data: `items.lua` CTH CalcValue + `suppressionPinned` Description text + CSV.
- Cross-package: нет.
- Rollback: откатить listed write set.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: items.lua, metadata.lua

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (Discord triage «Немного багов» / cloud task)
- Дата: 2026-07-31

## Evidence

- `JAZZ-COMBAT-003-AC-001`: `PASS` — static: `Unit:Retaliate` suppression mul gate (pinned=0) in `Code/System_OR_Unit.lua`
- `JAZZ-COMBAT-003-AC-002`: `PASS` — static: `Suppression` CalcValue in `items.lua` without 5-slab gate
- `JAZZ-COMBAT-003-AC-003`: `PASS` — static: `LightningReactionCheck` default 50 + stealth skip + suppression mul (pinned=0); FirearmAttack MapVar stash
- `JAZZ-COMBAT-003-AC-004`: `PASS` — static: Psycho drain `−4`; `OnMsg.CombatEnd` Will restore
- `JAZZ-COMBAT-003-AC-005`: `PASS` — docs: armor-damage-wounds-will, combat-cth-actions, override-matrix, testing, wiki + showcase RU/EN
- `JAZZ-COMBAT-003-AC-006`: `BLOCKED` — runtime/human playtest pending owner

## Documentation delta

- `docs/technical/systems/armor-damage-wounds-will.md` — Will restore, Psycho drain, retaliation vs pinned
- `docs/technical/systems/combat-cth-actions.md` — Suppression CTH always-on; Lightning Reaction rules
- `docs/technical/override-matrix.md` — Retaliate / LightningReactionCheck
- `docs/technical/testing.md` — playtest bullets
- `docs/wiki/combat-and-accuracy.md` + showcase RU/EN — player-facing
