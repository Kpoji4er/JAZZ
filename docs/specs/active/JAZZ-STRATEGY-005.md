---
id: JAZZ-STRATEGY-005
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - units-progression
repositories:
  - jazz
risk: low
generated_data: true
runtime_validation: not-required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-005.md
  - jazz/Code/LegionSquadComposition.lua
  - jazz/metadata.lua
  - jazz/items.lua
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
exclusive_resources:
  - jazz/metadata.lua
  - jazz/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-005: officer density and tier complementarity for Legion squads

## Проблема

Roadmap 6b/6c нуждается в утверждённых лимитах командиров и политике class-tier. Черновик «≤1 officer» слишком груб; тиры не должны вытеснять друг друга при эскалации.

## Цели

- Зафиксировать density-правила для Sergeant / Lieutenant / Captain и роль MercenaryCaptain.
- Зафиксировать: class-tiers **дополняют**, а не заменяют друг друга.
- Дать runtime constants/helpers для будущего generator (без подключения к spawn).

## Non-goals

- Role recipes allow-lists (остаток 6b).
- Generator poor/full и wiring в `Guardpost_Patrols`.
- Изменение UnitData / EnemySquad presets.
- Campaign equipment tier (`JAZZ_Legion_Tier`) — отдельный контракт.

## Утверждённые правила офицеров

Лимиты — **max allowed** по размеру состава `n` (число бойцов после сборки / целевой размер):

| Leader | Правило | Формула max |
|---|---|---|
| `JAZZ_Legion_LeaderT1_Sergeant` | 1 на каждые **8** человек | `floor(n / 8)` |
| `JAZZ_Legion_LeaderT2_Lieutenant` | 1 на каждые **15–20** человек | `floor(n / 15)` (нижняя граница плотности); не плотнее 1/15 |
| `JAZZ_Legion_LeaderT3_Captain` | 1 на каждые **30** человек | `floor(n / 30)` |
| `JAZZ_Legion_LeaderT4_MercenaryCaptain` | нужен для **T4-отрядов** | не density; `required = 1` если squad class-band = T4 |

Примеры:

| n | Sgt | Lt | Capt |
|---:|---:|---:|---:|
| 8–12 (recon) | 1 | 0 | 0 |
| 15–18 (patrol) | 1–2 | 1 | 0 |
| 30–40 (garrison) | 3–5 | 2 | 1 |

Несколько уровней офицеров могут сосуществовать (Sergeant + Lieutenant + Captain), в пределах своих caps. MercCaptain — маркер/обязательный слот T4-состава, не «замена всех младших».

## Class-tier complementarity

- Tier в ID (`T1`…`T4`) — **класс бойца**, не взаимоисключающие поколения.
- Более высокий tier **сильнее**, но generator **дополняет** состав старшими, а не вычищает младших.
- Poor-бюджет: больше T1/T2. Full/elite-бюджет: добавляет T3/T4 **рядом** с line, а не «только T4».
- Отдельно от campaign equipment tier (`JAZZ_Legion_Tier`).

## Требования

- `JAZZ-STRATEGY-005-REQ-001` — constants/helpers отражают officer density выше.
- `JAZZ-STRATEGY-005-REQ-002` — MercCaptain requirement keyed off T4 squad band, not headcount.
- `JAZZ-STRATEGY-005-REQ-003` — docs/roadmap фиксируют complementarity и officer table.
- `JAZZ-STRATEGY-005-REQ-004` — spawn/generator в этом change не меняется.

## Инварианты и ограничения

- Не менять `Guardpost_Patrols.lua` spawn costs/composition.
- Не менять `jazz-units` UnitData.
- Soft caps специалистов (MG/sniper) остаются в roadmap 6c; этот spec не отменяет их.

## Acceptance criteria

- `JAZZ-STRATEGY-005-AC-001` — static: helpers дают таблицу примеров (8→1 sgt, 15→1 lt, 30→1 capt).
- `JAZZ-STRATEGY-005-AC-002` — static: code registered in metadata/items.
- `JAZZ-STRATEGY-005-AC-003` — docs/roadmap обновлены.
- `JAZZ-STRATEGY-005-AC-004` — no spawn wiring.

## Impact и совместимость

- **Runtime:** новый loaded module; никто не вызывает helpers до generator.
- **Saves/network:** none.
- **Generated:** metadata/items code registration.
- **Rollback:** удалить модуль + регистрацию + docs.

## План и ownership

1. `jazz` — STRATEGY-005, `LegionSquadComposition.lua`, docs.
2. Generator wiring — отдельный change после 6b recipes / п.0.

## Решение владельца

28 июля 2026: 1 Sgt / 8; 1 Lt / 15–20; 1 Capt / 30; MercCaptain для T4-отрядов; тиры дополняют, не заменяют.

## Evidence

- `JAZZ-STRATEGY-005-AC-001`: `PASS (static)` — `floor(8/8)=1`, `floor(15/15)=1`, `floor(30/30)=1`; MercCaptain only when tier≥4.
- `JAZZ-STRATEGY-005-AC-002`: `PASS (static)` — `LegionSquadComposition.lua` in `metadata.code` + `items.lua`.
- `JAZZ-STRATEGY-005-AC-003`: `PASS (static)` — roadmap 6b + technical tiers note.
- `JAZZ-STRATEGY-005-AC-004`: `PASS (static)` — spawn не в write set / не изменён.

## Documentation delta

- `docs/specs/active/JAZZ-STRATEGY-005.md`
- `docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md`
- `docs/technical/systems/legion-units-equipment-tiers.md`
