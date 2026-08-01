# Длинная оптика (Scope) — баф максимального прицеливания

Канон для `JAZZ_Scope_*` (день) и лёгкий pass night.  
Связано: Combat mid [`combat-scope-tiers.md`](combat-scope-tiers.md), Reflex CQB [`reflex-collimator-tiers.md`](reflex-collimator-tiers.md).  
Apply: `docs/tools/_rebalance_long_scopes.py`.  
Калибровка: `docs/tools/_cmp_optic_cth.py --weapon DragunovSVD` (СВД); лоутир-винтовки — `Mosin` / `Springfield`.

**Статус:** settled 2026-08-01 (owner: оставляем числа; max-aim роль зафиксирована).

## Специализация семейства

Прицелы **меняют роль оружия**. Полноценная оптика — награда за **максимальное** (или достаточное по AimLevel) прицеливание: поздний unlock AA%/reach, ShotAP, CritFullAim, far plateau, harsh near.

| Семейство | Специализация |
| --- | --- |
| Коллиматор | эффективность ↑ vs irons |
| Боевая оптика | mid, ранний unlock |
| **Полноценная оптика** | **баф max aim** (+ дальняя зона) |

## Роль

- Главный payoff на **полном / высоком aim**, не на коротком.
- **Дальше mid**: plateau через `optic_reach` после AimLevel.
- **Цена:** `IncreaseShotAP` +1, поздний `ScopeAimLevel`, узкий OW (`…DecreaseBig`), **CritFullAim**, **near**.
- **T1** — старые/лоутир прицелы (ПУ, Springfield, Garand): слабый зум + лёгкий AA% 110…112 @ AimLevel.
- **T2** — классика 4× (ПСО, ZF4): AA% **155** @ AimLevel **3** — на полном aim ≈ ACOG; без max aim ACOG (unlock 2) сильнее.
- **T3+** — 6× и выше; лёгкий AimAccuracy% 115→125 (ниже Combat T3 155).
- Топ 9–10×: `IncreaseMaxAimActions` +1 (ещё сильнее max-aim роль).
- Оптический AA% **не** через `IncreaseAimAccuracy15Percent` — только в CTH при `aim ≥ AimAccuracyAimLevel`.

## Цель ощущения (СВД / Мосин, Dex70/Mrk70, full aim)

| Дистанция | Ожидание |
| --- | --- |
| 5 | Near-tax растёт с тиром; T1 почти нейтрален |
| 20–25 | Combat T3 ≥ long T2; T1 чуть выше irons |
| 40–50 | T3+ выше Combat; T5 держит плато дольше |

## Таблица

| ID | Тир | Mag | AimLevel | ShotAP | OW×% | Crit | MaxAim+ | AA% | OpticMin | Near% | Cost |
| --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| `JAZZ_Scope_PU` | **T1** | 3 | 2 | +1 | 75 | yes | — | **112** | 6 | 85 | 40 |
| `JAZZ_Scope_Garand` | **T1** | 2 | 2 | +1 | 82 | yes | — | **110** | 5 | 88 | 40 |
| `JAZZ_Scope_Springfield` | **T1** | 2 | 2 | +1 | 80 | yes | — | **110** | 5 | 88 | 45 |
| `JAZZ_Scope_PSO` | **T2** | 4 | 3 | +1 | 65 | yes | — | **155** | 8 | 78 | 60 |
| `JAZZ_Scope_ZF4` | **T2** | 4 | 3 | +1 | 65 | yes | — | **155** | 8 | 78 | 60 |
| `JAZZ_Scope_6x` | **T3** | 6 (low 1) | 3 | +1 | 55 | yes | — | **115** | 10 | 62 | 80 |
| `JAZZ_Scope_DA15_6x` | **T3** | 6 (low 1.5) | 3 | +1 | 55 | yes | — | **115** | 10 | 62 | 80 |
| `JAZZ_Scope_Scout` | **T4** | 7 (low 2) | 3 | +1 | 52 | yes | — | **120** | 12 | 55 | 100 |
| `JAZZ_Scope_8x_SCROME` | **T4** | 8 | 3 | +1 | 48 | yes | — | **120** | 13 | 50 | 100 |
| `JAZZ_Scope_3x_9x` | **T4** | 9 (low 3) | 4 | +1 | 45 | yes | +1 | **120** | 13 | 48 | 110 |
| `JAZZ_Scope_12x` | **T5** | 10 | 4 | +1 | 42 | yes | +1 | **125** | 14 | 40 | 130 |

`comment`: `Long Scope T<n> — …`.

### Night (лёгкий pass)

| ID | Mag | AimLevel | ShotAP | OpticMin | Near% | Extra |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `JAZZ_NightScope_NSPU` | 3 | 3 | +1 | 7 | 80 | IgnoreInTheDarkWhenFullyAimed |
| `JAZZ_NightScope` | 5 | 3 | +1 | 9 | 70 | IgnoreInTheDarkWhenFullyAimed |

Night: без Crit/без AA%; OW mild decrease 70%/60%.

## Инварианты

1. Новый long → строка сюда до кода.
2. Reach по умолчанию `(mag-1)×3` при AimLevel.
3. Script ↔ эта страница: страница канон.
4. Переменная кратность (`1-6x`, `1.5-6x`, `2-7x`, `3-9x`) → эффект `SmallMagnification` + `SmallAimLevel` (и `SmallSubMagnification` при дробной нижней кратности).
