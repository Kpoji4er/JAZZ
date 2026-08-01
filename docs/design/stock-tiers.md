# Приклады (Stock) — плечо vs мобильность

Канон для `JAZZ_Stock*`.  
Apply: `docs/tools/_rebalance_stock_tiers.py`.  
Связано: [`attachments-rebalance.md`](attachments-rebalance.md), `JAZZ-ATTACH-001`.

**Статус:** applied 2026-08-01.

## Роли

| Роль | Смысл |
| --- | --- |
| **Normal** | дефолт — **ничего не меняет** (база оружия уже «в плече») |
| **Heavy** | апгрейд контроля + aim |
| **Light** ≡ **Unfolded** | одинаковый бой (Recoil+2); Light **не** складывается; Unfolded — пара fold |
| **Folded / No** | темп + OW ценой отдачи/aim |

### Зачем складывать (только Unfolded → Folded)

| Разложен (Light/Unfolded) | Сложен / No |
| --- | --- |
| Recoil **+2** | Recoil **+5** |
| Aim база / 100% | AimAccuracy **85%** |
| ShootAP база | ShootAP **−1** |
| OW база | Extra OW **+2** |
| Full MaxAim | Folded ещё **−1 MaxAim** |

Light = тот же каркасный профиль, но без fold/unfold.

## Таблица

| ID | Recoil | AimAccuracy% | ShootAP | MaxAim | OW | Extra | Cost |
| --- | ---: | --- | ---: | ---: | ---: | --- | ---: |
| `StockNormal` | — | — | — | — | — | полный приклад | **25** |
| `StockHeavy` | **−5** | **115%** | — | — | — | | 40 |
| `StockLight` | **+2** | — | — | — | — | no fold | **20** |
| `StockLightUnFolded` | **+2** | — | — | — | — | `zzStockEquipped` | **20** |
| `StockLightFolded` | **+5** | **85%** | **−1** | **−1** | **+2** | `zzStockEquipped`; **не в кабинете** (toggle) | **20** (= UnFolded) |
| `StockNo` | **+5** | **85%** | **−1** | — | **+2** | | 15 |
| `StockFolded` | **+5** | **85%** | **−1** | — | **+2** | legacy; **не в кабинете** | **20** |

**Кабинет:** сложенный half fold-пары (`*Folded` без `UnFolded`) скрыт — ставится разложенный; сложить/разложить = combat toggle. Unfolded↔Folded swap в кабинете **бесплатно**.

Visual: `JAZZ_PKMModStock`, `JAZZ_UnfoldStocks` — без боя.

## Инварианты

1. Normal = empty default.
2. Light combat ≡ Unfolded combat; fold только у Unfolded/Folded pair.
3. Нет R/BDR / flat CTH.
4. `|ShootAP| ≤ 1`; только Folded/No.
5. Script ↔ эта страница.
