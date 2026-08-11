# Магазины — четыре роли

Канон для `JAZZ_Mag*`.  
Apply (ReloadAP/roles): `docs/tools/_rebalance_magazine_tiers.py`.  
Связано: [`attachments-rebalance.md`](attachments-rebalance.md), `JAZZ-ATTACH-001` REQ-015/016.

**Статус ёмкости:** data-pass применён: live `JAZZ_Mag*` используют `MagazineSizeSet` с абсолютным N, а shared `JAZZ_MagLarge` разрезан по целевым ёмкостям. Runtime smoke/editor round-trip остаётся обязательным.

**Статус ролей/ReloadAP:** applied 2026-08-01 (small −1 / expanded +1 / large +2).

## Ёмкость — текущий data-контракт

Игрок видит «Магазин на 45» → на оружии должно быть **`MagazineSize = 45`**, не «база+Δ» и не «×%».

| Подход | Вердикт |
| --- | --- |
| `MagazineSizeMultiplier` (%) | **запрещён** на live Mag |
| `MagazineSizeAdd` / `ReduceMagazineSize` (± от базы) | **устаревает** для named mag |
| **`MagazineSizeSet`** | **канон** — перезапись абсолютным N |

### Runtime

Vanilla `SetWeaponComponent` знает только `Add` / `Multiply` / `Subtract`.  
`ModificationType = "Set"` → `AddModifier(id, "MagazineSize", mul=1000, add=N−base)`  
(формула движка `MulDivRound(base + mod_add, mod_mul, 1000)`; `mul=0` давал MagSize 0/1).  
Data содержит effect preset `MagazineSizeSet`; heal на `LoadGame`/`NewGame` в `Code/System_WeaponComponent_Set.lua`.

### Правила данных

| Компонент | Size |
| --- | --- |
| `MagNormal` / Fine / Quick | **нет** size-эффекта (база `Firearm.MagazineSize`) |
| Named («на 10/20/40/45…») | `MagazineSizeSet` = **то число из имени** |
| Small | тоже **Set** на целевой N (не Subtract) |
| Drum / belt / generic Large | Set на целевую ёмкость; shared `%`-`MagLarge` **разрезать** по target (50 / 100 / …) |

Пример: `JAZZ_MagLarge_30_45` → `MagazineSizeSet` **45** (имя можно позже упростить до `…_45`; сейчас ID не трогаем до data-pass).

## Специализация (applied)

| Роль | Смысл | ID-паттерн |
| --- | --- | --- |
| **Маленький** | меньше патронов, **баф** (ReloadAP↓, Rel↑) | `JAZZ_MagSmall*` |
| **Стандарт** | база / качество без смены ёмкости | `MagNormal`, `MagNormalFine`, `MagQuick`, `MagNormalG18` |
| **Увеличенный** | больше патронов; Reload **+1**; без Rel/AA | `MagLarge_*` (named size), Fine |
| **Большой** | сильно больше; Reload **+2** + Rel− / AA− | `MagLarge`, `MagDrum*`, `MagBelt*` |

ReloadAP магазинов — цена ёмкости, **не** входит в ShotAP-бюджет аттачей.

## ReloadAP ladder (applied)

| Роль | ReloadAP |
| --- | ---: |
| Маленький | **−1** |
| Стандарт / Quick / Fine-tuned | 0 / −1 (Quick) / 0 |
| Увеличенный (`MagLarge_*`) | **+1** |
| Увеличенный Fine (`MagLargeFine`) | **0** (premium) |
| Большой | **+2** |

## Применённый data-pass

- `MagSmall*`, named `MagLarge_*`, `MagLargeFine`, `MagNormalG18`, drum и belt используют `MagazineSizeSet`.
- Generic `JAZZ_MagLarge` удалён после rewrite на `_50`, `_28`, `_27`, `_25`, `_13` и `_8`.
- `PSG1` использует `_8`; premium `MagLargeFine` удалён из его options.
- Auto5 barrel-specific `JAZZ_Auto5_*_LMag` остаётся отдельным TODO с `MagazineSizeMultiplier=150`.

## Таблица боевых эффектов (кроме size)

### Маленький

| Рычаг | Значение |
| --- | ---: |
| ReloadAP | **−1** |
| Reliability | **+15** |
| Cost | 15 |

### Стандарт

| ID | Эффект |
| --- | --- |
| `JAZZ_MagNormal` | нет |
| `JAZZ_MagNormalFine` | Rel **+10** |
| `JAZZ_MagQuick` | ReloadAP **−1** |

### Увеличенный

ReloadAP **+1**, без Rel/AA. Fine — без Reload+.

### Большой

| Рычаг | Значение |
| --- | ---: |
| ReloadAP | **+2** |
| Reliability | **−15** |
| AimAccuracy | **−15%** |
| Cost | MagLarge **40**; drum/belt **50** / belt-xl **100** |

`MagDrum_30_75` сохраняет `ExtraOverwatchShots` (`extra_shots=5`).

## Семьи магазинов (platform / mag well)

Съёмный `InventoryItem` магазина ставится только на оружие, у которого этот **component id** в `AvailableComponents`.  
Общий `JAZZ_MagLarge_50` на АК и M16 означал бы один предмет на обе платформы — **запрещено**.

| Семья | Примеры стволов | Пример id |
| --- | --- | --- |
| **AK 7.62×39** | AK47, AKM, Type56, **RPK**, Zastava M70/M92 | **`JAZZ_MagLarge_30_40`** (на 40); drum `30_75`; `JAZZ_MagQuick_AK` |
| **AK 5.45×39** | AK74, AKSU, **RPK74**, AN94 | **`JAZZ_MagLarge_30_45`** (на 45); `JAZZ_MagQuick_AK` |
| **AR15** | AR15, M16*, M4*, CAR15 | `…_AR15` |
| **SIG** | Sig550/552* | `…_SIG` |
| **MP5** / **UZI** / … | свои линейки | суффикс семьи |
| **MP40** | только заводской **32** (`JAZZ_MagNormal`); expanded family **нет** | — |
| **VAL** / **SVD** | 9×39 vs 7.62×54 | раздельно |

**Не** ставить `MagLarge_30_45` на АКМ/АК47 и `MagLarge_30_40` на АК74 — разный патрон (калибр), даже при общей форме шахты.

**Пистолеты 9×19:** один увеличенный слот, реалистичный N (для базы 15–17 → **20**, не два «больших» 25+28). Роль Large с Rel/AA-tax — только если отдельно задумана «палка» (Glock 33 и т.п.).

Apply: `docs/tools/_split_mag_families.py` (клоны component + InventoryItem), затем `docs/tools/_union_mag_family_options.py` (union options внутри семьи — магазин АК на РПК).

`JAZZ_MagNormal` остаётся универсальным заводским слотом (не remountable-каталог).

## Инварианты

1. ReloadAP: small −1 / expanded +1 / large +2 (**applied**).
2. Ёмкость: абсолютный Set; имя ↔ число (data applied; runtime smoke pending).
3. Generic `MagLarge` не используется: большая роль представлена target-specific variants/drum/belt.
4. **Семьи mag well:** expanded/large/quick/small/fine не шарятся между несовместимыми платформами (АК≠AR15; АК↔РПК ок). Id: `JAZZ_Mag*_<Family>`.
5. Script apply ReloadAP и MagSizeSet ↔ эта страница; family split ↔ `_split_mag_families.py`.
