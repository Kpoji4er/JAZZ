---
id: JAZZ-STRATEGY-015
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - enemy-squads
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-015.md
  - jazz/Code/LegionSquadComposition.lua
  - jazz/Code/LegionSquadGenerator.lua
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-units.md
  - jazz/docs/showcase/en/legion-units.md
  - jazz/docs/tools/_test_legion_medic_density.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-015: Legion medic density (Bonemaker)

## Проблема

Playtest (Sergej / Discord 2026-08-02): за несколько боёв с легионом не выпало ни одной аптечки. Единственный гарантированный `Medkit` у Legion — `Bonemaker_Inventory` (`JAZZ_Legion_FrontT1_Bonemaker`). Офицеры медикаментов не несут. Generator берёт костоправа только случайно как line → часто 0 медиков в патруле → нельзя перевязаться без найма медика.

## Цели

- Зарезервировать костоправов по density, аналогично офицерам (STRATEGY-005).
- Combat composition generator (`garrison`/`patrol`/`recon`/`qrf`/`reinforce`/`major`) соблюдает density.
- Костоправ доступен combat-ролям даже если allow-list режет `FrontT1` (qrf/retribution T2+).

## Non-goals

- FAK на офицерах / бинты в MiscGear (отложено).
- Logistics roles (`tax`/`recruiter`/`supply`/`shipment`/`manpower`) — пока EnemySquadDef presets, не generator.
- Плотность патрулей / размер / cargo inventory (сейв + отдельные follow-up).
- Новые UnitData медиков выше T1.

## Locked defaults (owner 2026-08-02; difficulty delta 2026-08-10)

«Условно 1 врача на 10–20 человек легиона.» Bonemaker = основной источник Medkit/Meds с врагов → на **Easy больше** медиков, на **Hard меньше** (обратно body-count ±10).

| Constant | Value | Meaning |
|---|---:|---|
| `MedicPerMen` | **15** | mid band 10–20; `floor(n / 15)` |
| `MedicMinSquadSize` | **10** | при `n >= 10` минимум **1** медик (после difficulty clamp) |
| `EasyMedicBonus` | **+1** | Easy / VeryEasy |
| `HardMedicPenalty` | **−1** | Hard / VeryHard (после сдвига всё ещё ≥1 если `n≥10`) |
| Unit | `JAZZ_Legion_FrontT1_Bonemaker` | единственный Legion medic slot |

Формула max medics (Normal base, затем difficulty):

```text
base:
  if n < 1: 0
  elif n < 10: floor(n / 15)   -- обычно 0
  else: max(1, floor(n / 15))
delta: Easy/VeryEasy +1; Hard/VeryHard −1; else 0
result: if n >= 10: max(1, base+delta) else max(0, base+delta)
```

`JAZZ_GetLegionMaxMedics(n[, difficulty])` — второй аргумент опционален (тесты); иначе `Game.game_difficulty`.

Примеры (Normal / Easy / Hard):

| n | Normal | Easy | Hard |
|---:|---:|---:|---:|
| 8 | 0 | 1 | 0 |
| 12 | 1 | 2 | 1 |
| 30 | 2 | 3 | 1 |
| 40 | 2 | 3 | 1 |
| 60 | 4 | 5 | 3 |

## Требования

- `JAZZ-STRATEGY-015-REQ-001` — helpers/constants отражают таблицу выше (вкл. Easy/Hard delta).
- `JAZZ-STRATEGY-015-REQ-002` — `lTryBuild` резервирует medic slots после офицеров; Bonemaker не дублируется случайным line-pick сверх cap.
- `JAZZ-STRATEGY-015-REQ-003` — combat generator roles всегда могут взять Bonemaker для reserved medic (даже без `FrontT1` в allow_prefixes).
- `JAZZ-STRATEGY-015-REQ-004` — top-up предпочитает добрать медиков до density, если роль/бюджет позволяют.
- `JAZZ-STRATEGY-015-REQ-005` — technical + roadmap + wiki/showcase обновлены; logistics non-goal явно.
- `JAZZ-STRATEGY-015-REQ-006` — medic count реагирует на `Game.game_difficulty` (Easy+/Hard−) при generate/top-up.

## Инварианты

- Не менять UnitData / LootDef Bonemaker (Medkit уже guaranteed).
- Officer density STRATEGY-005 без изменений (офицерский ±difficulty — out of scope).
- Soft caps MG/sniper/heavy/specialist без изменений.
- Deterministic `InteractionRand` contexts сохраняются для non-medic slots.
- Authored Ernie Init packs пишут **Normal** counts; Easy/Hard authored сдвиг — follow-up с difficulty settings для EnemySquadDef (generator уже живой).

## Acceptance criteria

- `JAZZ-STRATEGY-015-AC-001` — static: Normal `JAZZ_GetLegionMaxMedics(8)=0`, `(12)=1`, `(18)=1`, `(30)=2`, `(40)=2`, `(60)=4`.
- `JAZZ-STRATEGY-015-AC-001b` — static: Easy `(12)=2`, `(40)=3`, `(60)=5`; Hard `(12)=1`, `(40)=1`, `(60)=3`; Easy `(8)=1`.
- `JAZZ-STRATEGY-015-AC-002` — static: generated patrol/garrison composition includes Bonemaker count matching formula when budget covers price.
- `JAZZ-STRATEGY-015-AC-003` — static: qrf recipe without FrontT1 still places reserved Bonemaker.
- `JAZZ-STRATEGY-015-AC-004` — runtime/human: в бою с Legion combat-отрядом ≥10 тел есть костоправ с Medkit (или BLOCKED до playtest).

## Impact

- **Runtime:** новые combat squads чаще с костоправом → чаще Medkit loot + AI Heal; Easy щедрее, Hard скупее по медикам.
- **Saves:** уже заспавненные отряды без регенерации; новые spawn/top-up — да. `[no new game]` достаточно для появления на новых отрядах.
- **Network:** InteractionRand only for remaining line slots.
- **Rollback:** revert composition/generator + docs.

## Решение владельца

2026-08-02: добавить ~1 врача на 10–20 человек; остальной playtest feedback — после загрузки сейва.  
2026-08-10: Easy +1 / Hard −1 medic vs Normal (loot); quest authored packs остаются исключением из officer density; Init Ernie медики = Normal formula.

## Evidence

- `JAZZ-STRATEGY-015-AC-001` / `001b`: `PASS (static)` — `docs/tools/_test_legion_medic_density.py`.
- `JAZZ-STRATEGY-015-AC-002`: `PASS (static)` — `lMedicPlan` + Bonemaker excluded from random line; wiring markers in generator.
- `JAZZ-STRATEGY-015-AC-003`: `PASS (static)` — `JAZZ_LegionUnitAllowedForRole` allows medic for `qrf`/`retribution`/`major`.
- `JAZZ-STRATEGY-015-AC-004`: `BLOCKED` — human/runtime (новый combat spawn ≥10 тел).

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — medic density + difficulty.
- `docs/technical/systems/legion-units-equipment-tiers.md` — Bonemaker density + Easy/Hard.
- `docs/wiki/legion-global-ai.md` + showcase `legion-units` RU/EN.
- `docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md` — 6b medic line.
- `docs/design/ernie-garrison-baseline.md` — medic × difficulty.
- `docs/tools/_test_legion_medic_density.py` + README.
