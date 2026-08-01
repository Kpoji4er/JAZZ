# Дуло (Muzzle) — отдача vs тишина

Канон для `JAZZ_*` muzzle.  
Apply: `docs/tools/_rebalance_muzzle_tiers.py`.  
Связано: [`attachments-rebalance.md`](attachments-rebalance.md).

**Статус:** applied 2026-08-01 (SK ladder + sil без Recoil; FlashHider = стелс без Silent; MuzzleBooster **cut**).

## Специализация

| Семейство | Роль |
| --- | --- |
| **Compensator / brake** | контроль **отдачи** (очередь); same-target ok |
| **Flash hider** (M2/M3 carbine) | Recoil−1 + **StealthKill**; **без** Silent (звук остаётся) |
| **Suppressor** | **тишина** + StealthKill; цена Grouping / Rel / Jam; **без Recoil** (не конкурирует с compensator) |
| **Choke** | только buckshot-паттерн |

**Improvised** — шире слотов, чем штатный глушитель (**by design**); не топ по SK.

**Инвариант:** Muzzle **не** трогает `WeaponRange` / BDR.

## Таблица

| ID | Роль | Noise% | Recoil | Grouping | Rel / Jam | SK% | Extra | Cost |
| --- | --- | ---: | ---: | --- | --- | ---: | --- | ---: |
| `JAZZ_Compensator` | recoil | — | **−3** | — | — | — | SameTarget | 30 |
| `JAZZ_Galil_Brake_Default` | recoil def | — | **−1** | — | — | — | | 2 |
| `JAZZ_FlashHider` | flash/stealth | — | **−1** | — | — | **25** | no Silent | 10 |
| `JAZZ_ImprovisedSuppressor` | sil T0 | **40** | — | ×50 + Jam | Rel%−50 | **40** | AA−15%; wide mount | 20 |
| `JAZZ_Suppressor` | sil T1 | **33** | — | ×70 + Jam | Rel−10 | **55** | | 40 |
| `JAZZ_SuppressorImproved` | sil T2 | **25** | — | ×90 | Rel−5 | **80** | no Jam | 75 |
| `JAZZ_PistolSuppressor` | sil pistol | **20** | — | ×90 | Rel−5 | **70** | | 35 |
| `JAZZ_SuppressorIntegrated` | sil integ | **30** | — | — | — | **50** | Silent, no tax | 10 |
| `JAZZ_DuckbillChoke` | choke wide | — | — | — | — | — | Angle 120 | 20 |
| `JAZZ_FullChoke` | choke tight | — | — | — | — | — | Angle 80; no Range | 20 |

`JAZZ_MuzzleBooster` — **удалён** (не нужен).

## Инварианты

1. Нет R/BDR на muzzle.
2. SK% растёт с тиром глушителя (T0→T2); не перевёрнутая лестница.
3. Глушители без `RecoilDecrease`.
4. FlashHider ≠ Silent.
5. Script ↔ эта страница.
