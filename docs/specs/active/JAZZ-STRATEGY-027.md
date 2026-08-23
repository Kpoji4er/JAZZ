---
id: JAZZ-STRATEGY-027
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - legion-tier
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: not-required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-027.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/docs/tools/_check_strategy027_tier_retake.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - jazz/Code/Guardpost_Patrols.lua JAZZ_LegionAIOnTierRaised
related_decisions:
  - none
approved_by: project-owner chat 2026-08-24
---

# JAZZ-STRATEGY-027: tier-pulse retakes on player-captured outposts

## Проблема

STRATEGY-026 кормит живые форты при росте тира, но Майор не отвечает на уже потерянные аванпосты. Обычное возмездие ждёт Heat 800 и кулдаун 72h; QRF идёт с живого форта на key-сектора, не как волна « Magor бьёт по вашим фортам ».

## Цели

- На **переходе на T2** (`old < 21`, `new >= 21`), на **T2-3** (`23`) и на **T2-5** (`25`) штаб Майора шлёт **возмездие** (`major`) на **каждый** managed-аванпост, захваченный игроком.
- Рейс **не** ест суточный пул STRATEGY-019, не ждёт Heat/кулдаун обычного `lTryMajorResponse`, не списывает казну штаба.
- Один raise, перескочивший несколько порогов (например 22→25), даёт **одну** волну, не две.

## Non-goals

- Менять обычное возмездие (Heat 800, 72h, один active major на регион).
- Quest `Ernie_CounterAttack` / `ForceSetNextSpawnTimeAndSector`.
- Контратака на сектора Адонис/Армии или на обычные города (только managed outposts).
- Новые loc ID (текст задачи — существующий assault).
- Логистика 026 (деньги/люди).

## Locked defaults

| Param | Value |
| --- | --- |
| Triggers | T2 crossing; raise that reaches **23** (T2-3); raise that reaches **25** (T2-5) |
| Multi-threshold jump | one wave |
| Target | `root.outposts` with player Side or `owner_faction==player` |
| Role | `major` (Retribution), task `major_response` |
| Origin | Major HQ if Legion Side |
| Daily spawn pool | skip |
| Treasury | not deducted (off-map reserve; generator budget 1000000 / 200) |
| Heat / cooldown | ignored; do not write `next_response_time` |
| No HQ | skip the wave |
| No captured outposts | no attacks |

## Требования

- `JAZZ-STRATEGY-027-REQ-001` — `JAZZ_LegionAIOnTierRaised` fires a retake wave when T2 is crossed or the raise reaches 23 or 25.
- `JAZZ-STRATEGY-027-REQ-002` — one `major` squad per player-captured managed outpost; `skip_global_spawn`; no Heat/cooldown/treasury.
- `JAZZ-STRATEGY-027-REQ-003` — logistics 026 still runs (living outposts); retake runs even if no living outposts remain.
- `JAZZ-STRATEGY-027-REQ-004` — player-facing docs: technical + wiki + showcase RU/EN.

## Инварианты и ограничения

- Regular `lTryMajorResponse` unchanged.
- `major` still does not avoid player sectors (STRATEGY-018).
- Deterministic walk: `sorted_pairs` / sector id.
- Save schema v3, no bump. Existing saves: waves on future raises only.
- Not Ernie quest punitive pack.

## Acceptance criteria

- `JAZZ-STRATEGY-027-AC-001` — static: trigger gates for 21 / 23 / 25 in `JAZZ_LegionAIOnTierRaised`.
- `JAZZ-STRATEGY-027-AC-002` — static: per-captured `major` pulse, `skip_global_spawn`, no `next_response_time` / major treasury write in the pulse helper.
- `JAZZ-STRATEGY-027-AC-003` — static: retake not gated on `#living == 0`.
- `JAZZ-STRATEGY-027-AC-004` — static: technical + wiki + showcase RU/EN mention T2 / T2-3 / T2-5 retakes.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: jazz director only.
- Saves: additive; no schema bump.
- Network/determinism: existing `lSetRoute` / composition rand context.
- Generated data: none.
- Cross-package: none.
- Rollback: revert Guardpost_Patrols.lua pulse + docs.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: frontmatter `write_set`
- Exclusive resources: frontmatter `exclusive_resources`

## Решение владельца

- Статус: implemented
- Кто подтвердил: project-owner
- Дата: 2026-08-24
- Формулировка: при переходе на T2 и на T2-3 / T2-5 — контратаки на захваченные игроком аванпосты.

## Evidence

- `JAZZ-STRATEGY-027-AC-001`: `PASS` — static `docs/tools/_check_strategy027_tier_retake.py` (21 / 23 / 25 gates)
- `JAZZ-STRATEGY-027-AC-002`: `PASS` — static: `lPulseSpawnMajorRetake` uses `skip_global_spawn`, no cooldown/treasury write
- `JAZZ-STRATEGY-027-AC-003`: `PASS` — static: retake runs after empty-living log; no early `return false` on `#living == 0`
- `JAZZ-STRATEGY-027-AC-004`: `PASS` — technical + wiki + showcase RU/EN mention T2 / T2-3 / T2-5 retakes

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md`
- `docs/wiki/legion-global-ai.md`
- `docs/showcase/ru/legion-strategy.md` + `en/legion-strategy.md`
- `docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md`
