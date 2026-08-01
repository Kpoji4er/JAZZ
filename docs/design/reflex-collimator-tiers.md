# Коллиматоры JAZZ — архетипы и тиры

Канон для текущих `JAZZ_Reflex_*` и для будущих **отдельных InventoryItem**-коллиматоров (loot / магазины / уникалы).  
Связанный rebalance: `docs/design/attachments-rebalance.md` (Phase C).  
Apply: `docs/tools/_rebalance_reflex_tiers.py`.  
Калибровка цели: `docs/tools/_cmp_optic_cth.py --weapon DragunovSVD` (СВД — канон для mid/long; АКМ только для CQB-оценки ШВ).

**Статус:** settled 2026-08-01 (owner: оставляем числа; специализация зафиксирована).

## Специализация семейства

Прицелы **меняют роль оружия**, а не дают плоский CTH.

| Семейство | Специализация |
| --- | --- |
| **Коллиматор** | выше эффективность **относительно irons** (CQB / быстрый aim) |
| **Боевая оптика** | **средняя** дистанция, ранний unlock |
| **Полноценная оптика** | баф **максимального** прицеливания (поздний unlock, far reach) |

Коллем: не конкурирует с ACOG/ПСО на mid/full — делает то же оружие заметно лучше irons вблизи и на коротком aim.

## Инварианты

- У всех: `DecreaseMaxAimActions=1`, `MinAim`, **`CloseRangeFactorIncrease`** (смягчение hip-deadzone оружия).
- Нет ShotAP tax, нет Handling, нет плоского ScopeCTH.
- **Precision** → `AimAccuracyPercent` @ `AimAccuracyAimLevel=1` (парам на `MinAim`, не always-on Multiply) + close soft; без OW-баффа.
- **Overwatch** → OW сектор / extra shots / OA; close soft; без AimAccuracy%.
- **Universal** (Eotech T4) → mid AimAccuracy + mid OW + mid close soft.
- Топ Overwatch T2+ (Open / Pistol): `extra_attacks=2`.

## Цель ощущения (АКМ, Dex70/Mrk70)

Топ Precision на близкой (полный aim колема vs irons snap): примерно **×1.20**.  
Same-mode full vs full намеренно не раздуваем — колемы режут MaxAim.

## Таблица

| ID | Архетип | Тир | AimAccuracy% | CloseFactor+ | Extra OW | OW× | OA | Cost | Diff |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `JAZZ_Reflex_Garand` | Precision | T1 | 120 | 15 | — | — | — | 30 | −15 |
| `JAZZ_Reflex_Aimpoint5000` | Precision | T1 | 120 | 15 | — | — | — | 35 | −10 |
| `JAZZ_Reflex_Closed` | Precision | T2 | 135 | 20 | — | — | — | 50 | 0 |
| `JAZZ_Reflex_M68` | Precision | T3 | 150 | 25 | — | — | — | 75 | 10 |
| `JAZZ_Reflex_PKAS` | Precision | T4 | 160 | 35 | — | — | — | 100 | 15 |
| `JAZZ_Reflex_Cobra` | Overwatch | T1 | — | 15 | 1 | 140 | — | 35 | −10 |
| `JAZZ_Reflex_Open` | Overwatch | T2 | — | 15 | 2 | 150 | 8 | 50 | 0 |
| `JAZZ_Reflex_Pistol` | Overwatch | T2 | — | 15 | 2 | 150 | 8 | 45 | 0 |
| `JAZZ_Reflex_Eotech` | Universal | T4 | 135 | 20 | 1 | 145 | 8 | 90 | 10 |

`CloseFactor+` = параметр `CloseRangeFactorIncrease` (Add на `CloseRangeFactor` оружия; на АКМ 85 → 100…120).

## Заметки

1. Новый loot-коллиматор → строка сюда до кода.
2. `comment`: `Reflex <Archetype> T<n> — …`.
3. Script ↔ эта страница: страница канон.
