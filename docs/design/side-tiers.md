# Side — фонарь / тактик / лазер / UV

Канон. Apply: `docs/tools/_rebalance_side_tiers.py`, `_fix_flashlight_off_opts.py`.  
Связано: `attachments-rebalance.md`, `JAZZ-ATTACH-001`.

**Статус:** applied 2026-08-01.

## Роли

| Роль | ID | Эффект |
| --- | --- | --- |
| **Flashlight** | `JAZZ_Flashlight*` | `IgnoreInTheDark` + `EnableAimFX` (свет); toggle ↔ `JAZZ_FlashlightOff` |
| **Flashlight Off** | `JAZZ_FlashlightOff` | пусто (выкл.) |
| **Tac Device (Dot)** | `JAZZ_FlashlightDot*` | свет (`IgnoreInTheDark` + AimFX) + OW↑ + Mark + mild SK |
| **Laser** | `JAZZ_LaserDot*` | flat CTH (`LaserMark`) до `LaserDistance`; **полный** до `LaserFullRange=5`, дальше спад ~до 40%; OW + Mark + mild Crit |
| **UV** | `JAZZ_UVDot*` | ночной лазер: `NightOnly=1` + LaserCTH + SK↑; **только** Night/Underground |
| **Wrap** | `JAZZ_HandlingWrap` | уже grips: CloseFactor+5 |

## Числа (канон)

| Роль | Ключ | Value | Cost |
| --- | --- | ---: | ---: |
| Flashlight | — | — | 20 |
| Dot | OW% / SK% | 130 / 2 | 35 |
| Laser | LaserCTH / Dist / Full | **15** / **10** / **5** | 40 |
| UV | LaserCTH / Dist / Full / SK% | **12** / **8** / **5** / **5** | 25 |

Runtime: CTH-модификатор `Laser` в `items.lua` (falloff + NightOnly).

## Инварианты

1. Laser flat CTH — **явное исключение** (owner); лимит по дистанции + falloff после 5.
2. UV не даёт CTH днём.
3. Dot: свет всегда через AimFX (отдельный off-toggle не обязателен).
4. Flashlight toggle: `FlashlightOn`/`Off` actions + `JAZZ_FlashlightOff` в AvailableComponents.
5. HandlingWrap не трогать здесь.

## Distant backlog

Bayonet — не в этом slice.
