---
id: JAZZ-AI-SNIPER-001
status: implemented
owner: project-owner
systems: [tactical-ai]
repositories: [jazz]
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-SNIPER-001.md
  - jazz/Code/CombatAI.lua
  - jazz/Code/AIContextProfiles.lua
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/tools/_check_sniper_hold_001.py
  - jazz/docs/tools/README.md
  - jazz/docs/technical/override-matrix.md
exclusive_resources: [none]
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/specs/active/JAZZ-AI-CTX-001.md
approved_by: project-owner
---

# JAZZ-AI-SNIPER-001: Sniper hold when shot exists

## Проблема

ИИ-снайперы (keyword `Sniper` / `Marksman`) часто сходят с высотных позиций «ближе увидеть» врага, хотя с текущей клетки уже есть валидный выстрел. Причины:

1. `context.ExtremeRange` схлопнут в `EffectiveRange` (половина `WeaponRange`) → окна `AIPolicyWeaponRange` тянут в mid-close.
2. EndTurn `DealDamage` Weight 400 + OptLocWeight перекрывают `HighGround`, даже когда `dest_target_score[stay] > 0`.

## Цели

- Снайпер **остаётся** на текущей (в т.ч. высотной) позиции, если с неё уже можно кого-то поразить (`dest_target_score[stay] > 0` после Precalc).
- Если выстрела нет (нет LOS / out of range / AP) — **не** сидеть бесполезно: обычный OptLoc/EndTurn (можно спуститься и сблизиться).
- Если позиция **бесполезна несколько ходов подряд** — **мягко** снижать вес `AIPolicyHighGround` и штрафовать stay (не hard teleport): streak≤1 полный HighGround; streak2 HighGround×40% + stay−300; streak3+ HighGround×0% + stay−600(+). OptLoc/EndTurn сами выбирают уход.

## Non-goals

- Новые archetype ID; полный ребаланс Frontliner policies в `items.lua`.
- Менять night `SniperHold` profile (CTX-001) сверх общего hold-правила.
- Ломать `EffectiveRange` low-vis clamp (sight).

## Требования

- `JAZZ-AI-SNIPER-001-REQ-001` — `AICreateContext`: для firearm `ExtremeRange = weapon.WeaponRange` (или 1); `EffectiveRange` остаётся half / BulletDrop average и low-vis sight clamp как сейчас.
- `JAZZ-AI-SNIPER-001-REQ-002` — после `AIScoreReachableVoxels` (EndTurn dest): если unit имеет keyword `Sniper` или `Marksman` и `dest_target_score[stay] > 0`, выбранный dest заменяется на stay (тот же XY/stance pack), кроме случая когда выбранный dest — тот же stay.
- `JAZZ-AI-SNIPER-001-REQ-003` — если `dest_target_score[stay] == 0` / nil — hold не применяется; dest от policies без изменений.
- `JAZZ-AI-SNIPER-001-REQ-004` — без нового RNG; deterministic.
- `JAZZ-AI-SNIPER-001-REQ-005` — `MapVar JazzAI_SniperUselessStreak`: +1 за combat turn с stay_score≤0 (не чаще 1×/turn); reset при stay_score>0; clear на CombatStart.
- `JAZZ-AI-SNIPER-001-REQ-006` — по streak: `jazz_sniper_highground_pct` (100/100/40/0 for streak 0/1/2/3+) умножает `AIPolicyHighGround` в `AIScoreDest`; `jazz_sniper_stay_penalty` (0/0/300/600+) вычитает со stay. Без hard escape dest.

## Инварианты и ограничения

- Не менять сигнатуру `AIScoreReachableVoxels` для не-снайперов (прозрачный wrap).
- Не трогать `EffectiveRange` clamp Night/Fog/Dust/Underground/FireStorm.
- Burning / reposition paths без hold override (только обычный EndTurn path через wrap).

## Acceptance criteria

- `JAZZ-AI-SNIPER-001-AC-001` — static: `ExtremeRange` assigned from `weapon.WeaponRange`; wrap `AIScoreReachableVoxels` + sniper/marksman stay-hold helper.
- `JAZZ-AI-SNIPER-001-AC-002` — static: hold gated on `dest_target_score[stay] > 0`; no-op when 0.
- `JAZZ-AI-SNIPER-001-AC-003` — runtime/human: sniper on high ground with LOS+in-range enemy stays; without shot relocates.
- `JAZZ-AI-SNIPER-001-AC-004` — static: useless streak → HighGround weight pct + soft stay penalty; no hard escape dest. Runtime: after useless turns sniper leaves roof via scoring.
## Impact и совместимость

- Vanilla/CommonLib/JAZZ: wrap поверх vanilla `AIScoreReachableVoxels`; ExtremeRange ближе к Rato/vanilla split Effective≠Extreme.
- Saves / network: нет; AI dest selection deterministic.
- Generated data: нет.
- Cross-package: keywords живут в `jazz-units` UnitData; runtime в `jazz`.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (intent: «сидеть наверху если может попасть, не сидеть бесполезно»)
- Дата: 2026-08-05

## Evidence

- `JAZZ-AI-SNIPER-001-AC-001`: `PASS` — static: `python docs/tools/_check_sniper_hold_001.py`; ExtremeRange from WeaponRange; wrap + hold helper in `CombatAI.lua`
- `JAZZ-AI-SNIPER-001-AC-002`: `PASS` — static: hold gated on `stay_score <= 0`; force-leave path separate
- `JAZZ-AI-SNIPER-001-AC-003`: `BLOCKED` — runtime/human: roof sniper with LOS stays; without shot relocates
- `JAZZ-AI-SNIPER-001-AC-004`: `PASS` (static) / `BLOCKED` (runtime) — HighGround pct + stay penalty; human: useless streak leaves via weights

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — ExtremeRange + sniper hold + useless streak
- `docs/design/tactical-ai-archetypes.md` — hold-if-shot note
- Wiki/showcase: no dedicated tactical-AI player page; skip until one exists
