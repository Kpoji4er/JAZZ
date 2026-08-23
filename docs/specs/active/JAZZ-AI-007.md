---
id: JAZZ-AI-007
status: approved
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
  - jazz-units
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-007.md
  - jazz/docs/specs/active/JAZZ-AI-CMD-001.md
  - jazz/Code/AIContextProfiles.lua
  - jazz/Code/CombatAI.lua
  - jazz/Code/AiActions.lua
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/wiki/officer-aura.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/officer-aura.md
  - jazz/docs/showcase/en/officer-aura.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - none
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/specs/active/JAZZ-AI-CMD-001.md
  - docs/specs/active/JAZZ-AI-OW-001.md
  - docs/specs/active/JAZZ-AI-REG-001.md
approved_by: project-owner
---

# JAZZ-AI-007: Recontact, FallBack chance, peek-exit Overwatch

## Проблема

На L4 (ход 13, 18 живых Легиона против 8) офицер брал `FallBack` при 31% потерь без LOS. Ванильный `SelectArchetype` ставил всем `Scout_LastLocation` **до** `PickCustom`. Скаут не доходил (path-bbox 2–5 клеток). Игрок видел часть кучи и расстреливал. Fallback OW целился в last known за скалой — в камень, не в выход.

## Цели

- Не сидеть мишенью в углу и не чарджить всей кучей на клетку last known.
- `PickCustom` всегда после hard-state (panic / deserter / emplacement / reposition / pinned).
- Ванильный scout-gate не перебивает JAZZ.
- Отход: шанс на пороге, срыв при слиянии (≥3 живых в 8 тайлах).
- Нет LOS + last known: линия идёт в пояс 14–20 тайлов; 1–2 пробы ближе.
- Кого игрок видит, а боец игрока нет — обязан сдвинуться.
- OW по звуку: конус на выход из-за укрытия, не в камень и не в клетку за ним.
- Dump по звуку: якорь last known ±1–3 тайла. В непробиваемый камень не бить (уже PERF-004).

## Non-goals

- Полный peek_streak / AntiPeekOW bias (design §7).
- Смена `FallbackAction` на archetypes.
- Правка REG-001 порогов `NeedsRegroup`.
- Новые archetype ID.
- Новые строки локализации.
- Стрельба по звуку как таковая (оставляем).

## Требования

- `JAZZ-AI-007-REQ-001` — wrap `UnitProperties:SelectArchetype`: hard-state ванили; без блока `can_scout → Scout_LastLocation`; затем `PickCustom`; `Scout_LastLocation` только если `JazzAI_ShouldRecontactScout`.
- `JAZZ-AI-007-REQ-002` — `JazzAI_ShouldRecontactScout`: нет видимых врагов; есть `last_known_enemy_pos` (не создавать через `AIPickScoutLocation`); picked не Medic/Deserter/Melee/Legion_Regroup; directive не FallBack; дистанция до last known > 20 тайлов.
- `JAZZ-AI-007-REQ-003` — FallBack eligibility по-прежнему dead≥2 и ≥30%. Старт: один `InteractionRand(100, "JazzAI_FallBack")` на команду на порог 30/50/70; шанс = текущий процент потерь. Не стартовать без `GetNearestEnemy` у офицера. Состояние в `MapVar JazzAI_TeamFallBackState`. Повторный бросок только на более высоком пороге.
- `JAZZ-AI-007-REQ-004` — срыв Отхода: у офицера-источника ≥3 живых союзника в 8 тайлах (включая себя). Тогда `committed=false`, picker не добавляет FallBack.
- `JAZZ-AI-007-REQ-005` — `AIScoreDest`: линия (не probe) вне пояса 14–20 получает бонус за сближение с last known и штраф за отход/стойку; внутри пояса штраф за dest < 14 (не наезжать на звук). Probe (`Flank` keyword / aura `pusher` / Flanker archetype, не больше двух на команду) может идти ближе. Край карты (8 тайлов от bbox), если last known не у края — штраф.
- `JAZZ-AI-007-REQ-006` — farm: игрок имеет LOS на юнита, юнит не имеет LOS ни на одного player_team. Stay dest штраф; dest с большим cover / дальше от spotter — бонус.
- `JAZZ-AI-007-REQ-007` — `Scout_LastLocation` / recontact: path-bbox margin 24 тайла (cap 64), чтобы ход сокращал дистанцию, а не 2 клетки.
- `JAZZ-AI-007-REQ-008` — `JazzAI_FallbackOverwatchTargetPos`: якорь last known / nearest enemy; цель = ближайшая проходимая плита в кольце 1–2 вокруг якоря с `JazzAI_PosOWViable` (выход из-за укрытия). Если кольцо пусто и сам якорь viable — якорь. Иначе `false`. Ночные правила OW-001 сохраняются.
- `JAZZ-AI-007-REQ-009` — Dump/point по звуку без LOS: aim pos = last known со сдвигом 1–3 тайла (детерминированно от handle, проходимая плита). Не целить в модельку на клетке last known.
- `JAZZ-AI-007-REQ-010` — CombatStart/End чистит `JazzAI_TeamFallBackState`. Docs: technical + wiki + showcase RU/EN.

## Инварианты и ограничения

- Deterministic: `InteractionRand` только для броска Отхода; aim/dest без нового RNG.
- Panic / Deserter / Berserk / emplacement / RepositionArchetype не менять.
- Не создавать last known через `AIPickScoutLocation` в scout-gate.
- Cheap LoF / непробиваемый камень — без изменений контракта PERF-004.
- Saves: ephemeral MapVar, clear on combat end.

## Acceptance criteria

- `JAZZ-AI-007-AC-001` — static: wrap `SelectArchetype` без vanilla scout-before-PickCustom; `ShouldRecontactScout` как REQ-002.
- `JAZZ-AI-007-AC-002` — static: FallBack roll/bands/cancel + MapVar.
- `JAZZ-AI-007-AC-003` — static: dest standoff / farm / map-edge + path margin 24 для scout.
- `JAZZ-AI-007-AC-004` — static: peek-exit OW + sound offset 1–3.
- `JAZZ-AI-007-AC-005` — static: docs technical + wiki/showcase RU/EN + override-matrix.
- `JAZZ-AI-007-AC-006` — runtime/human: нет LOS + last known далеко → линия идёт в пояс, не стоит в углу; кого видит игрок — сдвигаются; OW на выход из-за камня.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: late wrap `UnitProperties:SelectArchetype`; FallBack picker сужает CMD-001 auto-order; OW-001 aim order меняется на peek-exit.
- Saves: ephemeral combat MapVar.
- Network/determinism: InteractionRand только FallBack start; dest/OW детерминированы.
- Generated data: нет.
- Cross-package: jazz-units PickCustom без изменений порогов; overlay в jazz SelectArchetype.
- Rollback/recovery: снять wrap + вернуть `JazzAI_TeamNeedsFallBack` / OW aim.

## План и ownership

- Пакет-владелец: jazz (runtime); jazz-units только если stance helper понадобится — в этом change set не требуется.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: см. frontmatter.
- Exclusive resources: none.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner (чат 2026-08-23: recontact пояс + farm move; FallBack шанс/слияние; OW на выход из-за камня; звук ±1–3).
- Дата: 2026-08-23.
- CMD-001 REQ-005 «FallBack = dead≥2 & ≥30%» остаётся порогом допуска; старт/срыв — этот spec.

## Evidence

- `JAZZ-AI-007-AC-001`: `PASS` (static) — `JazzAI_SelectArchetype` wrap; vanilla scout-gate removed; `JazzAI_ShouldRecontactScout`.
- `JAZZ-AI-007-AC-002`: `PASS` (static) — `JazzAI_TeamFallBackState` + band roll + merge cancel.
- `JAZZ-AI-007-AC-003`: `PASS` (static) — `JazzAI_ScoreRecontactDest` + path margin 24.
- `JAZZ-AI-007-AC-004`: `PASS` (static) — `JazzAI_PeekExitAimPos` / `JazzAI_SoundOffsetPos`; Dump skips unseen model.
- `JAZZ-AI-007-AC-005`: `PASS` (static) — technical + override-matrix + wiki + showcase RU/EN.
- `JAZZ-AI-007-AC-006`: `BLOCKED` — runtime/human (L4 / peek-exit OW).

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — SelectArchetype wrap, FallBack chance, recontact band, peek-exit OW.
- `docs/technical/override-matrix.md` — `UnitProperties:SelectArchetype`.
- `docs/design/tactical-ai-archetypes.md` — FallBack / scout note.
- `docs/wiki/officer-aura.md`, `docs/wiki/combat-and-accuracy.md`.
- `docs/showcase/ru|en/officer-aura.md`, `docs/showcase/ru|en/combat-and-accuracy.md`.
