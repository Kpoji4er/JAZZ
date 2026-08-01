# Стволы (Barrel) — эффективная дистанция

Канон для `JAZZ_Barrel*`.  
Apply: `docs/tools/_rebalance_barrel_tiers.py`.  
Связано: [`attachments-rebalance.md`](attachments-rebalance.md), `accuracy-model.md`.

**Статус:** applied 2026-08-01 — **BDR в %** (Multiply), чтобы револьверы/пистолеты не ломались абсолютными −6.

## Специализация

Ствол **сдвигает эффективную дистанцию**, не даёт плоский CTH и не съедает AP-бюджет выстрела.

| Роль | Ощущение |
| --- | --- |
| **Short** | лучше **вблизи**; короче плато (**BDR ×%**); отдача ↑ |
| **Normal** | база оружия |
| **Long** | лучше **вдали** (**BDR ×%**); хуже в упор; отдача ↓ |
| **Heavy** | контроль: Recoil**−5** + умеренный +BDR% + near-tax |
| **Improved** | то же + Reliability |

`WeaponRange` (**R**) — **±1** абсолютно (слабо). **BDR** — только **процент** от базы оружия.

## Инварианты

1. `BarrelBulletDropIncrease` / `Reduce` = `ModificationType = Multiply` + `PresetParamPercent`.
2. Param names = имена эффекта (`BulletDropIncrease`/`Reduce`, `BarrelRange*`, `BarrelRecoil*`, `CloseRange*`).
3. Нет AA / flat CTH / ShootAP на rifle-стволах.
4. Pistol/revolver short: `CloseRangeIncrease` + Factor↑ (база Close=0 — иначе Factor мёртв) + мягкий BDR%.
5. Shotgun / Auto5 — soft-pass; Auto5 вне этого скрипта.

## Таблица

| ID | Роль | BDR% | R | CloseΔ | FactorΔ | Recoil | Extra |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Short / Short+ / AUG / RnG | short | **70** | −1 | −3 | +12 | +2 | Rel−10 на base; RnG Grouping↑ |
| `JAZZ_BarrelShort_Pistol` | pistol | **85** | 0 | **+3** | +15 | +1 | CQB-зона (база Close=0) |
| Long / Long+ / AUG | long | **130** | +1 | +3 | −8 | −2 | Rel+ на improved |
| Heavy | heavy | **115** | 0 | +2 | −8 | **−5** | |
| Short shotgun | sg | **80** | −1 | −1 | +12 | — | Buckshot↑ |
| Long shotgun | sg | **120** | +1 | −1† | +10 | — | |
| Benelli short | sg | — | −1 | −1 | +12 | — | Mag−, no BDR% |

APS (без стат-модов): `JAZZ_BarrelNormal_Sil` / `JAZZ_BarrelNormal_noSil` — гейт слота Muzzle + UI-эффекты `ThreadedForSuppressor` / `BlocksMuzzleSlot`.

†Long shotgun: soft close (spread tube), не rifle near-tax.

### Примеры плато

| Оружие | base BDR | Short 70% | Long 130% |
| --- | ---: | ---: | ---: |
| SW Model 10 (рев) | 5 | **4** | **7** |
| Peacemaker | 6 | **4** | **8** |
| FN-FAL | 19 | **13** | **25** |
| SVD | 17 | **12** | **22** |

## Цель ощущения

На FAL short vs normal: заметный выигрыш @5, проигрыш после бывшего BDR.  
На револьвере short: −1 BDR и Factor↑ — не обнуление плато.
