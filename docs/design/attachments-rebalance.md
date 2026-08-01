# Аттачи: рефакторинг Handling → живые рычаги + ребаланс

Канон контракта: `docs/specs/active/JAZZ-ATTACH-001.md` (**approved; static acceptance green**).  
Статус 2026-07-31: runtime + generated-data migration + CSV/docs sync выполнены; до `implemented` остались Mod Editor round-trip (AC-004) и игровой smoke трёх китов (AC-006).

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

| Тир | Примеры | Хотим | Не хотим |
| --- | --- | --- | --- |
| Reflex | Closed, Eotech, M68, Open, Cobra… | −1 MaxAim, +1 OW shot, +OW angle, OA; MinAim; Handling **off** | ShotAP tax, сильный OW narrow |
| Combat 2–4× | CombatScope_2x/3x/ACOG/1P29… | Mag N×, AimLevel 1–2, ShotAP +1, mild OW↓ | CritFullAim (это для длинной) |
| Scope 6–12× | 6x, Scout, 12x, PSO… | Mag, AimLevel 3–4, ShotAP +1(+), strong OW↓, CritFullAim; +MaxAim на 9–12× | широкий OW как у коллиматора |
| Night | NightScope, NSPU, M3 | как combat/mid + dark rule | бесплатный dark без AimLevel |

Проверить после снятия Handling: не стали ли 2× «строго лучше» Reflex на всём — если да, оставить ShotAP на combat и/или чуть сильнее OW↓.

### Стволы

| Роль | Рычаги |
| --- | --- |
| Short | −Range, −BDR, Grouping↓, Recoil↑; CloseRange↓ (пистолет → упор; винтовка → окно ближе); ShootAP− только в budget ±1 |
| Long | +Range, +BDR, Grouping↑, Recoil↓; CloseRange↑; без ShotAP+ «за тяжесть» |
| Improved | Reliability↑ ± лёгкий accuracy |

`WeaponRange`/`BDR` не ставить на Scope/Muzzle/Stock. `CloseRange*` — база на Firearm, ствол только двигает.

### Магазины

| Роль | Рычаги |
| --- | --- |
| Expanded | size↑, ReloadAP↑, Reliability↓, optional AA−15% |
| Compact | size↓, ReloadAP↓, Reliability↑ |
| Drum/belt | size↑↑, ReloadAP↑↑, Reliability↓, optional Cumbersome→Reload/Recoil |

### Дуло

| Роль | Рычаги |
| --- | --- |
| Compensator | Recoil↓, same-target |
| Suppressor | Silent + StealthKill + jam + Grouping tax; **без** Handling |
| Flash hider | лёгкий пакет (не копировать полный suppressor) |

### Under / grip / bipod / stock

| Роль | Рычаги |
| --- | --- |
| Vertical/Tac grip | Recoil↓ only |
| GL | open mode; optional +1 ShotAP если playtest «бесплатно» |
| Bipod | prone only |
| Stock normal/heavy | Recoil↓ / AimAccuracy↑ |
| Folded / no stock | ShootAP−, Recoil↑, AimAccuracy−−, OW+ |

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

Не смешивать с несвязанным base-weapon retune.

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

## 6. Открыто для владельца

1. Pure-ergo: всем Recoil=1 или поштучно / visual?
2. Phase C глубина: только замена vs полный tier pass?
3. GL: Handling off only vs +1 ShotAP (съедает весь +1 budget вместе с оптикой)?
4. Ближняя зона: `CloseRange` + `CloseRangeFactor`; `PointBlankBonus`/`TwoHanded` оставить — **approved**.
5. Падение после BDR → ~25% на R с ускорением — **approved**; p/floor при реализации.
6. Phase D: `JAZZ_` + delete unused + Mount→Visual — **approved**.
7. Золотая ~100% — **вне** ATTACH-001 (отдельный base pass).
8. Pure-ergo → Recoil=1; Phase C tiered; GL без +ShotAP — **approved**.

Spec status: **approved; implementation in progress** (`JAZZ-ATTACH-001`). Новые идеи — дописывать REQ или новый SPEC.
