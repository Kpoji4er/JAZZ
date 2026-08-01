# Боевые прицелы (Combat) — средняя дистанция

Канон для `JAZZ_CombatScope_*` (+ `JAZZ_G36Scope` как 3×-класс).  
Apply: `docs/tools/_rebalance_combat_scopes.py`.  
Калибровка: `docs/tools/_cmp_optic_cth.py --weapon DragunovSVD` (СВД). АКМ — только sanity для ШВ.

**Статус:** settled 2026-08-01 (owner: mid ~+20–30%; оставляем числа).

## Специализация семейства

Прицелы **меняют роль оружия**. Combat — специализация на **средней** дистанции: ранний AimLevel, мягкий near, AA% на unlock, без ShotAP/Crit. Не CQB-колем и не «полный снайперский aim».

| Семейство | Специализация |
| --- | --- |
| Коллиматор | эффективность ↑ vs irons |
| **Боевая оптика** | **mid** |
| Полноценная оптика | баф max aim |

## Роль

- Универсал **средней** дистанции: Mag 2–4, низкий AimLevel, мягкий near.
- Mild OW↓ с зумом. Без ShotAP+/Crit/flat ScopeCTH.
- **`AimAccuracy%`** — главный рычаг mid-CTH на плато; применяется **только при `aim ≥ ScopeAimLevel`** (парам на `ScopeMagnification`, не always-on Multiply).
- Vs ПСО: ACOG unlock раньше (AimLevel 2) → сильнее без max aim; на полном aim ПСО с AA% 155 ≈ ACOG.
- Цель: топ T3 full@20 vs irons +1@20 ≈ **×1.25–1.30**; vs irons full ≈ **×1.15–1.20**.

## Таблица

| ID | Тир | Mag | AimLevel | OpticMinRange | Near% | OW×% | AimAccuracy% | Cost | Diff |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `JAZZ_CombatScope_2x` | T1 | 2 | 1 | 6 | 92 | 85 | 125 | 50 | 0 |
| `JAZZ_CombatScope_3x` | T2 | 3 | 2 | 9 | 90 | 78 | 140 | 60 | 0 |
| `JAZZ_G36Scope` | T2 | 3 | 2 | 9 | 90 | 78 | 140 | (weapon) | — |
| `JAZZ_CombatScope_ACOG` | T3 | 4 | 2 | 12 | 88 | 70 | 155 | 100 | 0 |
| `JAZZ_CombatScope_1P29` | T3 | 4 | 2 | 12 | 88 | 70 | 155 | 100 | 0 |
| `JAZZ_CombatScope_FeroZ24` | T3 | 4 | 2 | 12 | 88 | 70 | 155 | 100 | 0 |

`OpticMinRange ≈ Mag×3`. На 5 клетках T3 чуть слабее irons (near); на 20 full — сильнее.

## Заметки

1. Не раздувать reach ради mid на АКМ — plateau уже с 4×.
2. Длинная оптика — отдельная калибровка (дальше 25+ + near-tax).
