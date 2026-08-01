# Рукоятки (Under / Handgrip / Side wrap) — мелкие дешёвые роли

Канон для grip-comps.  
Apply: `docs/tools/_rebalance_under_grip_tiers.py`.  
Связано: [`attachments-rebalance.md`](attachments-rebalance.md), `JAZZ-ATTACH-001`.

**Статус:** applied 2026-08-01 (owner roles).

## Роли

| Роль | ID | Смысл |
| --- | --- | --- |
| **Vertical** | `VerticalGrip*` (Under/Handguard), Commando | **контроль очереди** — Recoil↓ |
| **Tac / Wrap** | `TacGrip*`, `HandlingWrap` | **небольшой бонус вблизи** — CloseRangeFactor↑ |
| **Ergo** | `Handgrip_Ergo`, `SigErgoHandGrip` | **небольшой общий AimAccuracy%** |
| **Default** | `Handgrip_Default`, PKM handgrips, `VerticalGripFld` | visual / empty |

**Не используем:** `FreeWeaponSwap` (снят с `TacGrip_M14`).

Принцип: **очень мало** эффекта, **дешево** поставить.

## Таблица

| ID | Роль | Эффект | Param | Cost | Diff |
| --- | --- | --- | ---: | ---: | ---: |
| `JAZZ_VerticalGrip` | vertical | `RecoilDecrease` | Recoil **1** | **15** | 0 |
| `JAZZ_VerticalGrip_M14` | vertical | то же | 1 | 15 | 0 |
| `JAZZ_VerticalGrip_Commando` | vertical | то же (было FirstAim) | 1 | 15 | 0 |
| `JAZZ_AKSU_VerticalGrip` | vertical | то же | 1 | 15 | 0 |
| `JAZZ_RPK74_VerticalGrip` | vertical | то же | 1 | 15 | 0 |
| `JAZZ_TacGrip` | close | `CloseRangeFactorIncrease` | Factor **+5** | **10** | 0 |
| `JAZZ_TacGrip_M14` | close | то же (**без** FreeWeaponSwap) | +5 | 10 | 0 |
| `JAZZ_HandlingWrap` | close | то же (Side) | +5 | 10 | 0 |
| `JAZZ_Handgrip_Ergo` | ergo | `IncreaseAimAccuracy15Percent` | AA% **105** | **15** | 0 |
| `JAZZ_SigErgoHandGrip` | ergo | то же | 105 | 15 | 0 |
| `JAZZ_Handgrip_Default` | empty | — | — | 5 | 0 |
| `JAZZ_PKMDefHandGrip` | empty | — | — | — | — |
| `JAZZ_PKMModHandGrip` | empty | — | — | — | — |
| `JAZZ_VerticalGripFld` | empty | — (сложенный visual) | — | 10 | 0 |

## Инварианты

1. Нет flat CTH / Handling / FreeWeaponSwap.
2. Vertical = только Recoil (не AA, не close).
3. Tac/Wrap = только CloseRangeFactor (не Recoil, не AA%).
4. Ergo = только AimAccuracy% (малый Multiply, не оптика-gate).
5. `|Recoil|≤1`, Factor≤+5, AA%≤105 на этом слое.
6. Script ↔ эта страница.

## Не в этом pass

- Bayonet (`Type56Bayo*`) — отдельный Under fix (`EnableWeapon` + fold actions).
- GL / Bipod / Side lasers — следующие слоты.
