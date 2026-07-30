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
| `SightModMinValue` | Combat | **9** | 40 |
| `SightModMaxValue` | Combat | **150** | 120 |
| `SightModHiddenProne` | Combat | **30** | 10 |
| `SightModStealthStatDiff` | Combat | 50% | 50% |
| `CamoSightPenalty` | Combat | 60% | (vanilla bool camo path) |
| `BrushSightMod` | EnvEffects | **−10** | −15 |
| `IndoorSightMod` | EnvEffects | **−5** | — |
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
7. Brush (`vsFlagTallGrass`): малый `BrushSightMod` (**−10**), затем camo ×**3** (Hidden) / ×**100%** (видимо); вне кустов Hidden ×1 / видимо ×25%. Prone в траве **без** ×2 (тот же `SightModHiddenProne`, что на открытом) — `JAZZ-AI-006`.
8. **Prone** режет sight всегда: `−SightModHiddenProne` (в кустах тоже ×1).
9. Indoors (цель): `IndoorSightMod` (**−5**), независимо от Hidden/camo.
10. Smoke на линии: **−70**.
11. Night / Fog / Dust / FireStorm / rain. Пол modifier = ConstDef `SightModMinValue` (**9** ≈ **4** тайла Aware).
12. Разница высоты: выше цели → `SightHeightDiffMod`; ниже → `−2×` mod.

Камуфляж влияет на detection через modifier, не отключает LOS. Night vision: `HasNightVision()` + стек `NightVision` брони уменьшают `DarknessSightMod`.

Таблицы Aware / Unaware / Hidden / без Hidden — ниже (`JAZZ-AI-005`/`006`). Exploration suspicion rear-кап 10 тайлов — `JAZZ-AI-004`.

### Hot path (perf)

На каждый вызов максимум **два** `ForEachItem("Armor")`: один по наблюдателю (Vision + при необходимости NightVision / DustStormProtection), один по цели (Camouflage). Cover/camo/dust — integer `MulDivRound`; финальный `Clamp` без float. Масштаб брони для Vision/NV/camo идёт через `GetDegradationMultiplierPermille` (без float `GetDegradationMultiplier`). `DustStormProtection` по-прежнему масштабируется через `item.Condition` (не degradation mult). Smoke LOS пропускается, если modifier уже на полу или `g_SmokeObjs` пуст.

Сводка по vanilla/CLib узким местам visibility/AI: [performance-vanilla-report.md](../performance-vanilla-report.md).

### Таблицы видимости (`GetSightRadius`)

`tiles ≈ base × Clamp(modifier, SightModMinValue=9 … Max) / 100`.

| | Aware | Unaware |
|---|---:|---:|
| Base | **46** | **22** |
| Пол modifier (`SightModMinValue` **9**) | **~4** | **~2** |

Ночь: `DarknessSightMod −65`, без NV / illumination. High cover = coverage 100%. Camo-пул полный носимый ≈ **45**; Shadow **+20**. Stealthy **−25** только Hidden. Brush flat **−10**, Hidden camo ×3 / видимо ×100%; prone без ×2 в траве. Indoors цель: **−5** всегда. Static model (`JAZZ-AI-005`/`006`).

#### Hidden — Aware / Unaware

| Профиль (цель Hidden) | Aware день | Aware ночь | Unaware день | Unaware ночь |
|---|---:|---:|---:|---:|
| Без перков / без camo, открыто | **46** | **~16** | **22** | **~8** |
| Тяжёлая броня camo −15 | **~53** | **~23** | **~25** | **~11** |
| Форма camo 20 | **~37** | **~7** | **~18** | **~3** |
| Форма+штаны camo 40 | **~28** | **~4** | **~13** | **~2** |
| Stealthy, без camo | **~35** | **~5** | **~17** | **~2** |
| Stealthy + форма 20 | **~25** | **~4** | **~12** | **~2** |
| Stealthy + camo 40 | **~16** | **~4** | **~8** | **~2** |
| Shadow only | **~37** | **~7** | **~18** | **~3** |
| Shadow + camo 40 | **~18** | **~4** | **~9** | **~2** |
| Shadow + camo 45 | **~16** | **~4** | **~8** | **~2** |
| **Shadow + camo 45 + high cover** | **~9** | **~4** | **~4** | **~2** |
| **Shadow + camo 45 + трава** | **~4** | **~4** | **~2** | **~2** |
| Stealthy + camo 40 + high cover | **~9** | **~4** | **~4** | **~2** |
| Без всего + high cover | **~39** | **~9** | **~19** | **~4** |
| Без всего + prone открыто | **~32** | **~4** | **~15** | **~2** |
| Без всего + standing в траве | **~41** | **~12** | **~20** | **~6** |
| Без всего + prone в траве | **~28** | **~4** | **~13** | **~2** |
| Без всего, в помещении (−5) | **~44** | **~14** | **~21** | **~7** |
| Shadow + camo 45, в помещении | **~14** | **~4** | **~7** | **~2** |

Ориентиры: Shadow+стена **~9**; Shadow+трава **~4**; Stealthy+camo open **~16**; голый open **46**; голая трава **~41**.

#### Без Hidden (цель видима)

| Профиль | Aware день | Aware ночь | Unaware день | Unaware ночь |
|---|---:|---:|---:|---:|
| Открыто standing | **46** | **~16** | **22** | **~8** |
| Форма camo 20 | **~44** | **~14** | **~21** | **~7** |
| Форма+штаны camo 40 | **~41** | **~12** | **~20** | **~6** |
| Shadow-пул camo 65 (×25% open) | **~39** | **~9** | **~18** | **~4** |
| High cover standing | **~32** | **~4** | **~15** | **~2** |
| Prone открыто | **~32** | **~4** | **~15** | **~2** |
| Standing в траве | **~41** | **~12** | **~20** | **~6** |
| Prone в траве | **~28** | **~4** | **~13** | **~2** |
| Camo-пул 65 + high cover | **~25** | **~4** | **~12** | **~2** |
| Camo-пул 65 + трава (×100%) | **~12** | **~4** | **~6** | **~2** |
| В помещении (−5) | **~44** | **~14** | **~21** | **~7** |

#### Среда (добавки)

| Сценарий | ≈ modifier | Aware день | Unaware день |
|---|---:|---:|---:|
| Fog (−30) | 70 | **~32** | **~15** |
| Smoke (−70) | 30 | **~14** | **~7** |
| Fog + smoke | clamp 9 | **~4** | **~2** |
| Lynx (+8 base), открыто | 100 | **54** | **30** |

Exploration suspicion rear-кап 10 тайлов — `JAZZ-AI-004`.

Замечания: camo×3 в траве и Shadow+укрытие часто упираются в пол **9**; cover от фактического coverage; ConstDef в `items.lua`; smoke/rain/Lynx/cover scale/indoors — `System_OR_Unit.lua`.

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