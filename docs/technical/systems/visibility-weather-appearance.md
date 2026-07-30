# Видимость, погода и внешний вид

## Назначение и эффект для игрока

Система связывает освещение, дым, погодные циклы, камуфляж, защиту от среды и визуальные состояния экипировки. Результат влияет на обнаружение, CTH, AI, аудио/FX и читаемость боя, а не только на картинку.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | Weather, lightmodels, visibility/LOS, smoke, appearance/attachments и camera APIs |
| CommonLib | Вводит/определяет `IsLineInSmoke` в `Code/_Utils.lua`; JAZZ позже заменяет эту функцию |
| JAZZ | Заменяет weather scheduling, smoke check, appearance states и часть visibility modifiers; добавляет protection properties и entity states |

## Реализация и load-state

Загружаются:

- `Code/Weather.lua` — погодные циклы и выбор явлений;
- `Code/System_OR_Unit.lua` — visibility, smoke и unit conditions, включая `IsLineInSmoke`;
- `Code/UnitAwareness.lua` — применение видимости к suspicion/alerts;
- `Code/System_UnitAppearance.lua` — attachments, gas mask и weapon component states;
- `Code/System_ArmorRating.lua` и `System_GasMask.lua` — camo/защита;
- `Code/Camera.lua` — camera zoom/config;
- `Code/NoSoundsInRooms.lua` — загружается, но вся содержательная логика закомментирована; сейчас inert;
- generated LightmodelPreset, ObjMaterial, ParticleSystemPreset, armor/items и EntityData.

`jazz_assets` предоставляет фактические meshes/materials/textures/entities; `jazz-maps` — geometry, rooms, light placement, weather/sector context.

## Погодные циклы

`Weather.lua` задаёт режимы `Wet`, `Dry` и `CursedForest`. Внутри выбираются rain, fog, heat, dust и firestorm-состояния. Выбор использует детерминированный `BraidRandom`, что важно для multiplayer и повторяемости сохранений.

Погодные constants находятся среди 46 `ConstDef` core: camo/darkness/weather, point-blank, rain jam, sight/unaware и другие параметры. Дождь дополнительно повышает риск jam оружия; dust storm и night vision взаимодействуют с armor properties.

Изменение расписания должно сохранять:

- seed/random stream;
- границы времени и переходы lightmodel;
- sector/region restrictions;
- очистку предыдущих эффектов;
- согласованность tactical и satellite времени.

## Дым, LOS и обнаружение

`IsLineInSmoke` не найден как экспортированный глобальный символ в просмотренном vanilla source, появляется в CommonLib и затем заменяется JAZZ. Это dependency-owned API, поверх которого JAZZ строит собственную семантику. В `System_OR_Unit.lua` линия `self → other` режется по voxel-шагам; при попадании в `g_SmokeObjs` дальность обнаружения получает **−70** к sight modifier.

Smoke участвует в:

- расчёте линии видимости/атаки и `GetSightRadius`;
- CTH modifiers;
- suspicion и awareness;
- AI targeting и позиции;
- gas/smoke protective equipment.

После обновления CommonLib проверять сигнатуру, тип результата и используемые call sites. Простое совпадение имени не гарантирует совместимость тел.

## Радиус обнаружения (`Unit:GetSightRadius`)

Канонический override: `Code/System_OR_Unit.lua`. Call sites: `UnitAwareness.lua`, `CombatAI.lua` и vanilla visibility pipeline.

### Формула

```text
sight = base_sight
      or (IsAware → AwareSightRange else UnawareSightRange)
      + (Jazz_Perk_Lynx ? 8 : 0)

modifier = 100 + Σ(сдвиги), затем Clamp(modifier, SightModMinValue, SightModMaxValue)

sightAmount = MulDivRound(sight, modifier, 100) × SlabSizeX
            + (IdleSuspicious ? SlabSizeX/4 : 0)
```

Возврат: `sightAmount, hidden, night_time`.

В отличие от vanilla, **aware база не сбрасывается в Unaware**, когда цель `Hidden`: aware наблюдатель всегда стартует с `AwareSightRange`.

### ConstDef (JAZZ `items.lua` vs vanilla)

| Const | Группа | JAZZ | Vanilla |
|---|---|---|---|
| `AwareSightRange` | Combat | **46** | 24 |
| `UnawareSightRange` | Combat | **22** | 12 |
| `SightModMinValue` | Combat | **20** | 40 |
| `SightModMaxValue` | Combat | **150** | 120 |
| `SightModHiddenProne` | Combat | **30** | 10 |
| `SightModStealthStatDiff` | Combat | 50% | 50% |
| `CamoSightPenalty` | Combat | 60% | (vanilla bool camo path) |
| `BrushSightMod` | EnvEffects | **−50** | −15 |
| `DarknessSightMod` | EnvEffects | **−65** | −10 |
| `DustStormSightMod` | EnvEffects | **−40** | −10 |
| `FireStormSightMod` | EnvEffects | **−40** | −10 |
| `FogSightMod` | EnvEffects | −30 | −30 |
| `SightHeightDiffMod` | EnvEffects | **−20** | −15 |

Hardcoded в override (не ConstDef): smoke **−70**; rain light **−5**, heavy **−15**; observer `Protected` **−10**; `Blinded` **−100**; Lynx **+8** к base sight.

### Сдвиги modifier (порядок логики)

1. Reactions `OnCalcSightModifier` (наблюдатель и цель).
2. Hidden: `max(0, (Agility−Wisdom) × SightModStealthStatDiff/100)`.
3. Camo цели: сумма экипированного `CamouflagePercent` × condition×degradation; `FleetingShadow` **+20** к camo-пулу.
4. Vision наблюдателя: сумма `Vision` брони (днём в modifier; ночью через NightVision / darkness).
5. Укрытие цели: `GetCoverPercentage` × коэффициент стойки через `MulDivRound(coverage, mul%, 100)`:

   | Cover | Standing | Crouch | Prone |
   |---|---|---|---|
   | High | 30% | 35% | 50% |
   | Low | 15% | 20% | 35% |

   Hidden: `coverage × 35%` до расчёта, затем `coverbuff × 150%`; цель с `Protected` → `coverbuff × 125%`. Без бинарных порогов camo/kit — camo, Stealthy и Shadow складываются в modifier непрерывно.
6. Observer `Protected` / `Blinded`.
7. Brush (`vsFlagTallGrass`): `BrushSightMod`, затем camo ×3 (Hidden) / ×50% (видимо) или вне кустов ×1 / ×25%.
8. **Prone всегда** режет sight: `−SightModHiddenProne` вне кустов, `×2` в кустах. Это намеренно шире vanilla (там prone-штраф только при Hidden).
9. Smoke на линии: **−70** (пропуск `IsLineInSmoke`, если modifier уже на полу или на карте нет smoke).
10. Night / Fog / Dust (+`DustStormProtection` брони) / FireStorm / rain. Ночной пол modifier **12** (`JAZZ_NightSightModMinValue`) vs дневной ConstDef **20** → Shadow optimal ~5–6 тайлов ночью, ~9 днём.
11. Разница высоты: выше цели → `SightHeightDiffMod`; ниже → `−2×` mod (в JAZZ всегда, не только exploration).

Камуфляж влияет на detection через modifier, не отключает LOS. Night vision: `HasNightVision()` + стек `NightVision` брони уменьшают `DarknessSightMod` как `MulDivRound(darkness, 100−penaltyReduce, 100)`.

Целевые дистанции Hidden (`JAZZ-AI-005`): таблицы Aware / Unaware / без Hidden ниже. Exploration suspicion: realtime rear-кап **10 тайлов** в `UpdateSuspicion` (`JAZZ-AI-004`) — не меняет `GetSightRadius`.

### Hot path (perf)

На каждый вызов максимум **два** `ForEachItem("Armor")`: один по наблюдателю (Vision + при необходимости NightVision / DustStormProtection), один по цели (Camouflage). Cover/camo/dust — integer `MulDivRound`; финальный `Clamp` без float. `DustStormProtection` по-прежнему масштабируется через `item.Condition` (не degradation mult).

### Таблицы видимости (`GetSightRadius`)

`tiles ≈ base × Clamp(modifier) / 100`.

| | Aware | Unaware |
|---|---:|---:|
| Base | **46** | **22** |
| Пол modifier день (`SightModMinValue` 20) | **~9** | **~4** |
| Пол modifier ночь (`JAZZ_NightSightModMinValue` 12) | **~6** | **~3** |

Ночь: `DarknessSightMod −65`, без NV / без illumination цели. High cover = coverage 100%. Camo-пул: форма+штаны+балаклава ≈ **45**; Shadow **+20** к пулу. Stealthy **−25** к modifier **только если Hidden**. Без Hidden: camo ×25% открыто / ×50% в траве; укрытие без Hidden-scale 35% и без ×150%. Static model; coverage/condition могут сдвигать на 1–2 тайла.

#### Hidden — Aware (46)

| Профиль (цель Hidden) | День | Ночь |
|---|---:|---:|
| Без перков / без camo, открыто standing | **46** | **~16** |
| Тяжёлая броня camo −15, открыто | **~53** | **~23** |
| Форма camo 20, открыто | **~37** | **~7** |
| Форма+штаны camo 40, открыто | **~28** | **~6** |
| Stealthy, открыто без camo | **~35** | **~6** |
| Stealthy + форма 20 | **~25** | **~6** |
| Stealthy + форма+штаны 40 | **~16** | **~6** |
| Shadow only (+20 camo) | **~37** | **~7** |
| Shadow + camo 40 | **~18** | **~6** |
| Shadow + полный носимый camo 45 | **~16** | **~6** |
| **Shadow + camo 45 + high cover standing** | **~9** | **~6** |
| **Shadow + camo 45 + prone в траве** | **~9** | **~6** |
| Stealthy + camo 40 + high cover | **~9** | **~6** |
| Без всего + high cover standing | **~39** | **~9** |
| Без всего + prone открыто | **~32** | **~6** |
| Без всего + standing в траве | **~23** | **~6** |
| Без всего + prone в траве | **~9** | **~6** |

Ориентиры: Shadow full + стена/трава **8–10** день / **5–6** ночь; Stealthy + лёгкий camo open **~15**; неподготовленный открыто — край Aware (**46**).

#### Hidden — Unaware (22)

Те же профили, база **22** (типичный патруль / не алертнут).

| Профиль (цель Hidden) | День | Ночь |
|---|---:|---:|
| Без перков / без camo, открыто standing | **22** | **~8** |
| Тяжёлая броня camo −15, открыто | **~25** | **~11** |
| Форма camo 20, открыто | **~18** | **~3** |
| Форма+штаны camo 40, открыто | **~13** | **~3** |
| Stealthy, открыто без camo | **~17** | **~3** |
| Stealthy + форма 20 | **~12** | **~3** |
| Stealthy + форма+штаны 40 | **~8** | **~3** |
| Shadow only (+20 camo) | **~18** | **~3** |
| Shadow + camo 40 | **~9** | **~3** |
| Shadow + полный носимый camo 45 | **~8** | **~3** |
| **Shadow + camo 45 + high cover standing** | **~4** | **~3** |
| **Shadow + camo 45 + prone в траве** | **~4** | **~3** |
| Stealthy + camo 40 + high cover | **~4** | **~3** |
| Без всего + high cover standing | **~19** | **~4** |
| Без всего + prone открыто | **~15** | **~3** |
| Без всего + standing в траве | **~11** | **~3** |
| Без всего + prone в траве | **~4** | **~3** |

#### Без Hidden (цель видима)

Stealthy не действует. Camo слабее (×25% / ×50% в траве). Укрытие — полный coverage × stance mul (без Hidden 35%/150%).

| Профиль | Aware день | Aware ночь | Unaware день | Unaware ночь |
|---|---:|---:|---:|---:|
| Открыто standing | **46** | **~16** | **22** | **~8** |
| Форма camo 20 | **~44** | **~14** | **~21** | **~7** |
| Форма+штаны camo 40 | **~41** | **~12** | **~20** | **~6** |
| Shadow-пул camo 65 (×25% open) | **~39** | **~9** | **~18** | **~4** |
| High cover standing | **~32** | **~6** | **~15** | **~3** |
| Prone открыто | **~32** | **~6** | **~15** | **~3** |
| Standing в траве | **~23** | **~6** | **~11** | **~3** |
| Prone в траве | **~9** | **~6** | **~4** | **~3** |
| Camo-пул 65 + high cover | **~25** | **~6** | **~12** | **~3** |
| Camo-пул 65 + prone в траве | **~9** | **~6** | **~4** | **~3** |

#### Среда (добавки к modifier, эталон от 100)

| Сценарий | ≈ modifier | Aware день | Unaware день |
|---|---:|---:|---:|
| Fog (−30) | 70 | **~32** | **~15** |
| Smoke (−70) | 30 | **~14** | **~7** |
| Fog + smoke | clamp 20 | **~9** | **~4** |
| Lynx (+8 к base), открыто | 100 | **54** | **30** |

Exploration suspicion: realtime rear-кап **10 тайлов** в `UpdateSuspicion` (`JAZZ-AI-004`) — не меняет эти числа `GetSightRadius`.

Замечания по тюнингу:

- дым/−70, camo×3 в кустах (Hidden) и Shadow+укрытие часто упираются в пол modifier;
- cover зависит от фактического `coverage`, не всегда от 100%;
- ночной пол **12** — `JAZZ_NightSightModMinValue`; дневной — ConstDef `SightModMinValue`;
- ConstDef в `items.lua`; smoke/rain/Lynx/Hidden cover scale — `System_OR_Unit.lua`.

## Камуфляж и защита от среды

Armor properties `CamouflagePercent`, `NightVision`, `Vision`, `DustStormProtection` и `StunGrenadeProtection` меняют tactical условия через `GetSightRadius` и связанные checks. Gas mask отдельно защищает от toxic/tear gas и зависит от состояния ресурса; типичный `Vision` штраф маски режет дневную дальность.

Примеры порядка величин (носимый InventoryItem): форма/штаны ~`CamouflagePercent = 20`, балаклава ~5, газ-маска `Vision = −20` / `DustStormProtection = 30`. `CrocodileHide` (60) — camo на крокодилах, не эталон для мерков.

## Внешний вид и attachments

`System_UnitAppearance.lua` управляет:

- gas mask и конфликтами head/face equipment;
- weapon attachments;
- bipod visual state;
- folded/unfolded stock;
- состояниями entity в руках и на земле.

Entity/state/spot names приходят из `jazz_assets`. Несовпадение регистра или отсутствующий state обычно проявляется только runtime warning и неверной моделью, поэтому это отдельный контракт совместимости.

## Свет, материалы и FX

Core snapshot содержит 31 `LightmodelPreset`, 10 `ObjMaterial` и particle preset; maps содержат light/objects/grids, assets — materials/textures. FX files связывают оружейные entities и sound/particle moments. Изменение lightmodel или material может одновременно менять видимость и художественный результат.

## Проверка

- день/ночь, indoor/outdoor и переход времени;
- Wet/Dry/CursedForest, rain/fog/heat/dust/firestorm;
- одинаковое сохранение/seed в singleplayer и multiplayer;
- эталон Aware ~46 тайлов днём на открытом standing;
- prone открыто / prone в кустах / full cover prone (см. таблицу сценариев);
- LOS через smoke, на границе дыма и без дыма;
- Hidden + camo в кустах vs без camo; высокий camo упирается в SightModMinValue;
- AI detection/suspicion с camo, night vision и плохой погодой;
- rain jam и dust protection;
- gas mask новая/сломанная, toxic/tear gas, Vision penalty;
- bipod, stock, magazine, scope и mask entity states;
- отсутствие `missing entity/state/spot/material` в логе;
- подтверждение, что `NoSoundsInRooms.lua` остаётся inert до намеренной активации.

## Сопровождение

При изменении weather, smoke, `GetSightRadius`, ConstDef sight/env, armor camo/vision или appearance state обновлять эту страницу (включая таблицы const и сценариев), AI/weapon/assets docs и тесты. Активация `NoSoundsInRooms.lua` считается новым runtime-поведением и должна отдельно документироваться. Уровень подтверждения формул: static по `System_OR_Unit.lua` + `items.lua`; баланс сценариев — human playtest.