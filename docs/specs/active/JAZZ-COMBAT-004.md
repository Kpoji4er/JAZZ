---
id: JAZZ-COMBAT-004
status: implemented
owner: project-owner
systems:
  - combat-cth-actions
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Unit.lua
  - jazz/docs/specs/active/JAZZ-COMBAT-004.md
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/technical/weapons/accuracy-model.md
  - jazz/docs/technical/testing.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMBAT-004: избыток ядра CTH → шанс крита

## Проблема

Ядро навыка/aim (`JAZZ_CTHGetShooterCore`) перед ситуационными множителями режется до 100. Всё «сверху» отбрасывалось: опытный стрелок с полным прицелом не получал награды за запас точности, хотя укрытие по-прежнему должно резать попадание.

## Цели

- Избыток **некапнутого** ядра (`uncapped_core − 100`, floor через `JAZZ_CTHRound`) 1:1 добавляется к `Unit:CalcCritChance` для `Firearm`.
- Попадание по-прежнему строится из `Clamp(core, 0, 100)` × factors → финальный clamp 2..100 (укрытие/дым/suppression не пробиваются запасом ядра).
- Итоговый крит остаётся `Clamp(..., 0, 100)`.

## Non-goals

- Перелив after-factors (`before_clamp`); melee/legacy CTH; смена `GrazingHitDamage` / miss→graze (см. tune в JAZZ-COMBAT-002); UI breakdown строки «overflow→crit» (достаточно итогового crit %).

## Решения владельца

| Решение | Итог |
| --- | --- |
| Модель | вариант 1 — избыток ядра до множителей |
| Коэффициент | 1:1 |
| Кап крита | существующий 0..100 |

## Требования

- `JAZZ-COMBAT-004-REQ-001` — `CalcCritChance` для Firearm: `crit += Max(0, Round(uncapped_core) − 100)` до финального clamp.
- `JAZZ-COMBAT-004-REQ-002` — opportunity / `guaranteed_noncrit` по-прежнему 0; `guaranteed_crit` 100; grazing по-прежнему не критует.
- `JAZZ-COMBAT-004-REQ-003` — pipeline попадания не меняет pre-cap ядра и factor product.

## Acceptance criteria / Evidence

- `JAZZ-COMBAT-004-AC-001`: `PASS (static)` — wiring в `Unit:CalcCritChance` + `uncapped_core` в `CalcChanceToHit`.
- `JAZZ-COMBAT-004-AC-002`: `BLOCKED (runtime)` — элитный aim: crit UI/ролл выше базы на величину overflow; с укрытием CTH падает, overflow-крит сохраняется.
- `JAZZ-COMBAT-004-AC-003`: `PASS (static)` — technical + wiki + showcase RU/EN.

## Impact

- Сильные Marksmanship / AimAccuracy билды чаще упираются в кап крита 100% на открытой цели с полным aim — ожидаемо.
- Saves/network: тот же детерминированный `CalcCritChance` path.

## Documentation delta

`combat-cth-actions.md`, `accuracy-model.md`, `testing.md`, wiki + showcase RU/EN.
