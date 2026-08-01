# Аттачи: рефакторинг Handling → живые рычаги + ребаланс

Канон контракта: `docs/specs/active/JAZZ-ATTACH-001.md` (**approved; один большой спек на весь Phase C**).  
Статус 2026-08-01: Handling/ID/static green; Scope/Barrel/Muzzle/Mag/Stock/Under-grips/**Bipod**/**Side** applied; absolute MagSize (docs-only); Bayonet **distant backlog**; AC-004 editor / AC-006 smoke human.

## Жёсткие лимиты (от владельца)

1. **ShootAP от аттачей суммарно не больше ±1.**  
   `-2` к стоимости выстрела (сложенный приклад + короткий ствол + …) слишком сильно поднимает темп.  
   ReloadAP магазинов — отдельный бюджет (цена ёмкости).  
   Сейчас `JAZZ_Scope_8x_SCROME` выровнен до ShotAP=1; leftover `LROptics*` удалены из unused.
2. **`WeaponRange` / `BulletDropRange` — только ствол.**  
   Оптика двигает окно через `optic_reach` / AimLevel / near-factor, не через R/BDR.
3. **Ближняя зона** — база оружия (`CloseRange` / `CloseRangeFactor`); **ствол сдвигает**:
   - короткий на пистолете → стрельба в упор;
   - короткий на винтовке → комфортное окно **ближе**;
   - длинный → окно **дальше**, вблизи больнее.
   Оптика: `OpticMinRange` / `OpticNearFactor` поверх. `PointBlankBonus` оставить до миграции.
4. **Ствол двигает BDR** (и R): короткий −BDR/−R, длинный +BDR/+R — длина плато «всё хорошо».
5. **После BDR:** полный эффект на плато; дальше падение **с ускорением** к ~**25%** на `WeaponRange` (не в 0). Урон идёт через `GetRangeDamageReduction`; runtime использует `floor + (1-floor)×(1-t^p)`, где `p=max(1.25, BDR×0.05+Grouping/100)`.

## График «CTH с учетом эрго» vs текущая модель

Старый график (CAR15, «с эрго»): рост 0→10, плато ~10–16, обвал к 0 к ~40. Aim-клики дают почти параллельный сдвиг вверх (~+3–4% за клик). Ближний dip и «золотое окно» жили в ветке Handling / старой кривой.

**Сейчас** (`accuracy-model.md`): до границы эффективной зоны `E` множитель дистанции = **1** (плато без ближнего штрафа от ствола), потом спад к `WeaponRange`. Ближняя «неэффективность» уже заложена у **оптики** (`OpticMinRange` / `OpticNearFactor`). Handling в CTH не участвует — подпись на старом графике устарела.

Идея «на золотой дистанции при макс навыках ~100%» — здравая **калибровка базы оружия**, не задача каждого обвеса. Аттачи должны:

- сдвигать / сужать / расширять окно;
- не раздувать AP-экономику;
- не подменять профиль плоским CTH.

Пока пик CAR15 на графике ~70% на 3 кликах — либо навык/ситуация не max, либо база ещё не дотянута до цели 100%. Это отдельный weapons-base pass (можно параллельно, не смешивать commit с strip Handling).

## Ближняя зона + ствол (реализованная модель)

Вместо булевого `PointBlankBonus` — пара полей на Firearm (канон имён):

| Поле | Смысл |
| --- | --- |
| `CloseRange` | тайлы ближней неэффективности (0 = нет, пистолет) |
| `CloseRangeFactor` | множитель CTH на `d=0` (1.0 = без штрафа) |

```text
close = weapon.CloseRange + barrel_delta
factor0 = weapon.CloseRangeFactor * barrel_factor_mod
# d < close: lerp factor0 → 1.0
optic: OpticMinRange / OpticNearFactor поверх
```

| База | Пример | CloseRange |
| --- | --- | --- |
| Пистолет / SMG CQB | Glock, MP5 | 0 или крошечный |
| Карабин / AR | CAR15, AK | умеренный |
| Винтовка / DMR | M14, SVD | заметный |
| Снайперская база | PSG, M24 | сильный |

| Ствол | Пистолет | Винтовка |
| --- | --- | --- |
| Short | упор ok | комфорт ближе |
| Normal | база | база |
| Long | редко | комфорт дальше; +BDR/+R |

`PointBlankBonus` / `TwoHanded` **не удалять**. Runtime применяет базовый профиль Firearm и barrel-shift `CloseRange*` отдельным множителем; `OpticMinRange` / `OpticNearFactor` складывается с ним отдельным фактором.

## Ствол: R/BDR и ближняя зона

| Ствол | R / BDR / G | CloseRange* |
| --- | --- | --- |
| Long | **+BDR**, +R, +Grouping, Recoil↓ | CloseRange↑ / Factor↓ |
| Short | **−BDR**, −R, Grouping↓, Recoil↑ | CloseRange↓ / Factor↑; пистолет → упор |

ShootAP± только в рамках суммарного ±1. Без плоского ±CTH.

### Целевая кривая после BDR (урон + range factor)

Сейчас (`AccuracyRangeCTH.lua`):

```text
E_cth ≈ BDR + optic_reach × aim   // для CTH
E_dmg ≈ BDR                       // GetRangeDamageReduction(..., aim=0)
t = (d - E) / (R - E)
factor = 1 - t^curve_power        // на d→R даёт ~0
curve_power = BDR×0.05 + Grouping/100   // CAR15 ≈ 1.25 — слабое ускорение
```

**Цель:**

```text
до BDR (урон) / до E (CTH):  factor = 1
после:  factor = floor + (1 - floor) × (1 - t^p)
floor ≈ 0.25 на R (последний валидный тайл; атака при d≥R по-прежнему невозможна)
p > 1  // падение с ускорением: сначала почти плато, потом круче
```

Пример при floor=25%, p=2: 100% → 95% → 81% → 58% → 25% на четвертях отрезка BDR…R.

Калибровка `p` / `floor` — в `accuracy-model` + ATTACH/CTH follow-up; стволы влияют, **двигая BDR** (длина плато), не отдельным плоским % урона.

## 1. Рефакторинг (Phase A)

| Артефакт | Что сделать |
| --- | --- |
| Классификатор эффектов | `live` / `legacy_handling` / `legacy_flat` / `visual` в tools |
| Audit | TSV: `component_id`, slot, handling effects, other effects, proposed replace |
| Catalog HTML | бейдж «legacy Handling» пока Phase B не закрыт |
| Human design MD | Handling не описывать как боевой бонус; пометка legacy |
| Effect registry | Phase B2: удалить orphan + Handling presets после снятия с comps (см. ниже) |

Не трогать: сейвовую совместимость вне явного accepted break; не возвращать Handling в CTH.

## 2. Замена устаревших параметров (Phase B)

### 2.1 Снять без замены (цена уже есть)

- Почти все `ScopeHandlingReduce` на Combat/Scope/Night — цена = ShotAP + OW + AimLevel.
- `MagazineHandling±` если уже есть ReloadAP + Reliability ± AimAccuracy%.
- `BarrelHandling±` если уже есть Range/BDR/Grouping/Recoil/ShootAP.
- `SilencerHandling*` при jam + Silent + Grouping.
- `StockHandlingIncrease` на folded/no-stock.
- `BipodsHandlingDecrease`, `GLHandlingDecrease` (по умолчанию).

### 2.2 Заменить на живой рычаг

| Comp / класс | Было | Станет |
| --- | --- | --- |
| `TacGrip`, `Handgrip_Ergo`, `SigErgoHandGrip` | только GripHandling↑ | `RecoilDecrease` Recoil=1 (или visual-only — решение approve) |
| `HandlingWrap` | BarrelHandling↑ | `RecoilDecrease` Recoil=1 **или** visual |
| Крупный mag без достаточной цены | MagHandling↓ | усилить ReloadAP / Reliability (не оба сразу +15 если уже жёстко) |
| Коротыш без ShootAP− | BarrelHandling↑ | `ReduceShootAP` =1 только в budget ±1 |
| Длинный ствол | BarrelHandling↓ | **не** ShotAP+; near/BDR |

### 2.3 Запрещено как замена

Плоский CTH на оптике, возврат Handling в CTH, новый hip-fire stat в этом spec.

### 2.4 Удалить лишние effect-пресеты (Phase B2)

Audit сейчас (`docs/tools/_tmp_audit_effects.py`):

**Уже 0 comps (можно выкинуть как effect):**  
`ScopeCTHBonus`, `ScopeAccuracyIncreace`, `ScopeAccuracyReduce`, `ReduceRange50Percent`, `ReduceAuto50Percent`, `ReduceAimAccuracy50Percent`, `ReduceAimAccuracy80Percent`.

**Оставить:** `PointBlankBonus`, `TwoHanded`.

**После strip с comps — удалить Handling presets:**  
`ScopeHandlingReduce`, `SilencerHandlingReduce`, `MagazineHandling*`, `BarrelHandling*`, `GripHandlingIncrease`, `StockHandlingIncrease`, `GLHandlingDecrease`, `BipodsHandlingDecrease`, `Cumbersome` (если не property).

Не трогать vanilla effects и живые рычаги.

## 3. Ребаланс (Phase C) — целевые роли

Числа ниже — **стартовая таблица для approve**, не финальный patch set. После approve правятся comps + CSV + design doc.

### Прицелы

**Специализация оружия (owner):** колемы → эффективность ↑ vs irons; боевая → mid; полноценная → баф max aim. Канон-страницы ниже. **Scope Phase C — settled 2026-08-01** (числа не трогать без нового pass).

| Тир | Примеры | Хотим | Не хотим |
| --- | --- | --- | --- |
| Reflex | см. матрицу ниже | эффективность ↑ vs irons: −1 MaxAim, MinAim, close soft, AA%@aim≥1 / OW; Handling **off** | ShotAP tax, сильный OW narrow, плоский CTH |
| Combat 2–4× | CombatScope_2x/3x/ACOG/1P29… | **mid**, ранний AimLevel, мягкий near, AA% @ unlock; см. [`combat-scope-tiers.md`](combat-scope-tiers.md) | CritFullAim; снайперский near; payoff только на max aim |
| Scope (long) | PU…PSO…6x…12x | **баф max aim**: поздний AimLevel, far reach, ShotAP, Crit, harsh near, AA% @ unlock; см. [`long-scope-tiers.md`](long-scope-tiers.md) | широкий OW; mid-payoff раньше Combat |
| Night | NightScope, NSPU | dark + mild near/OW; см. long-scope-tiers | бесплатный dark без AimLevel |

#### Коллиматоры

Канон тиров/архетипов: **[`docs/design/reflex-collimator-tiers.md`](reflex-collimator-tiers.md)** (Precision / Overwatch / Universal).  
Apply: `docs/tools/_rebalance_reflex_tiers.py`.

#### Боевые прицелы

Канон: **[`docs/design/combat-scope-tiers.md`](combat-scope-tiers.md)**. Apply: `docs/tools/_rebalance_combat_scopes.py`.


### Стволы

Канон: **[`docs/design/barrel-tiers.md`](barrel-tiers.md)**. Apply: `docs/tools/_rebalance_barrel_tiers.py`.

| Роль | Рычаги |
| --- | --- |
| Short | **BDR ×70%**, R **−1**, CloseRange↓ / Factor↑, Recoil↑, Grouping↓; Rel− на base short |
| Long | **BDR ×130%**, R **+1**, CloseRange↑ / Factor↓, Recoil↓, Grouping↑ |
| Heavy | Recoil**−5** + BDR ×115% + near-tax; **без** flat CTH |
| Improved | то же + Reliability |
| Pistol short | BDR ×85% + CQB-зона Close+3 @ Factor+15 |

`WeaponRange` почти не двигаем. **BDR только Multiply %** (револьвер BDR5 → short 4, не −6). Нет AA / ShootAP / flat CTH на rifle-стволах.

### Магазины

Канон: **[`docs/design/magazine-tiers.md`](magazine-tiers.md)**. Apply: `docs/tools/_rebalance_magazine_tiers.py`.

| Роль | Рычаги |
| --- | --- |
| Маленький (`MagSmall*`) | size↓, ReloadAP−1, Rel+15 |
| Стандарт | baseline / Fine Rel+ / Quick Reload− |
| Увеличенный (`MagLarge_*`, Fine) | size↑; Reload **+1** (Fine = 0); без Rel/AA |
| Большой (`MagLarge`, drum, belt) | size↑↑, Reload **+2**, Rel−15, AA−15% |

### Дуло

Канон: **[`docs/design/muzzle-tiers.md`](muzzle-tiers.md)**. Apply: `docs/tools/_rebalance_muzzle_tiers.py`.

| Роль | Рычаги |
| --- | --- |
| Compensator / brake | Recoil↓ (3 / 1); same-target на compensator |
| Flash hider (M2/M3) | Recoil−1 + StealthKill; **без** Silent |
| Suppressor ladder | Silent Noise% + StealthKill↑ с тиром + Grouping/Rel/Jam; **без Recoil**; **без** R/BDR |
| Improvised | шире слотов (**by design**); SK mid, не топ |
| Choke | только BuckshotAngle; FullChoke **без** IncreaseRange |

`JAZZ_MuzzleBooster` — **cut**. Empty defaults — без боя.

### Under / grip / bipod / stock

| Роль | Рычаги |
| --- | --- |
| **Grips** | канон [`under-grip-tiers.md`](under-grip-tiers.md): Vertical Recoil−1; Tac/Wrap CloseFactor+5; Ergo AA%105; дешёвые; без FreeWeaponSwap |
| GL | open mode; optional +1 ShotAP если playtest «бесплатно» |
| **Bipod** | канон [`bipod-tiers.md`](bipod-tiers.md): один `JAZZ_Bipod` + Under; CTH+10 / +1 shot |
| **Side** | канон [`side-tiers.md`](side-tiers.md): Flashlight light+toggle; Dot light+OW/Mark; Laser CTH+falloff@5; UV night+SK |
| **Stock** | канон [`stock-tiers.md`](stock-tiers.md): Normal empty; Heavy Recoil−5+AA%; Light≡Unfolded Recoil+2; Folded/No ShootAP−1+Recoil+5+OW+2 |

## 4. Порядок работ

```text
A   tools + audit + docs badges
B   strip/replace Handling on comps
B2  delete orphan + dead Handling effect presets
D   JAZZ_ rename live comps; delete unused; Mount → Visuals only
C   tier number pass + CloseRange/BDR curve if in scope
    regenerate design MD + catalog
    technical sync + AC evidence
```

### Порядок Phase C (всё внутри `JAZZ-ATTACH-001`)

1. **Scope — settled** (Reflex / Combat / Long, 2026-08-01).
2. **Barrel — applied** (BDR% + CloseRange* + Recoil; R ±1; см. [`barrel-tiers.md`](barrel-tiers.md)).
3. **Muzzle — applied** (Recoil vs Silent; SK ladder; FlashHider без Silent; MuzzleBooster cut; см. [`muzzle-tiers.md`](muzzle-tiers.md)).
4. **Magazine — partial** (ReloadAP applied; ёмкость **Set-канон в доке**, runtime later; см. [`magazine-tiers.md`](magazine-tiers.md)).
5. **Stock — applied** (плечо vs folded; см. [`stock-tiers.md`](stock-tiers.md)).
6. **Under grips — applied** ([`under-grip-tiers.md`](under-grip-tiers.md)).
7. **Bipod — applied** ([`bipod-tiers.md`](bipod-tiers.md)).
8. **Side — applied** ([`side-tiers.md`](side-tiers.md)). Bayonet — distant backlog.

Отдельные SPEC на слоты **не** создавать.

### Phase D кратко

| Действие | Что |
| --- | --- |
| Rename | live non-Mount → `JAZZ_<Id>` (~142 сейчас без префикса; 36 уже ok) |
| Delete unused | ~55 comps без options (`LROptics*`, mounts-only orphans, …) |
| Mount | убрать слот с AUG/M60/PKM; меш только в Visuals |
| Keep effects | `PointBlankBonus`, `TwoHanded` |

Saves: rename ломает экипированный id — accepted break.

## 5. Метрики «готово»

- `legacy_handling_on_live == 0`
- 0 comps с единственным эффектом Handling (кроме явного visual-only списка)
- Human doc без «штраф Handling» как будто он в CTH
- Smoke: Reflex CQB / ACOG mid / 12×+suppressor читаются разными

## 6. Открыто / in-spec backlog

1. Absolute magazine size (`MagazineSizeSet`) — **канон в доке**; Code/data — когда скажет владелец (REQ-016 / AC-010 BLOCKED).
2. Absolute MagSize (AC-010) when owner greenlights. Bayonet — **distant backlog**.
3. AC-004 editor round-trip; AC-006 three-kit smoke.
4. Золотая ~100% CTH — **вне** ATTACH-001 (отдельный base-weapons pass).

Spec status: **approved; Phase C in progress** (`JAZZ-ATTACH-001`). Новые идеи по обвесам — REQ/AC сюда, не новый SPEC.