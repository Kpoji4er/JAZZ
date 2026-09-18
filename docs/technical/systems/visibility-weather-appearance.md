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
- `Code/Camera.lua` — camera zoom/config; post-combat / post-setpiece tac angle restore (`JAZZ_RestoreTacCameraControl`);
- `Code/NoSoundsInRooms.lua` — загружается, но вся содержательная логика закомментирована; сейчас inert;
- generated LightmodelPreset, ObjMaterial, ParticleSystemPreset, armor/items и EntityData.

`jazz_assets` предоставляет фактические meshes/materials/textures/entities; `jazz-maps` — geometry, rooms, light placement, weather/sector context.

## Погодные циклы

`Weather.lua` задаёт режимы `Wet`, `Dry` и `CursedForest`. Внутри выбираются rain, fog, heat, dust и firestorm-состояния. Выбор использует детерминированный `BraidRandom`, что важно для multiplayer и повторяемости сохранений.

Погодные constants находятся среди `ConstDef` core: camo/darkness/weather, point-blank, rain jam, sight/unaware и другие параметры. Дождь дополнительно повышает риск jam оружия; dust storm и night vision взаимодействуют с armor properties. **Пылевая буря:** один `DustStormCoverCTHPenalty = −40` (EnvEffects) складывается с Cover/ExposedCover, пока цель obscured; канон CTH — [combat-cth-actions.md](combat-cth-actions.md).

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

**Не** участвует в grazing hits (JAZZ-COMBAT-002): LoF через `SmokeObj` больше не форсирует `hit.grazing` / `target_grazing_hit` (`ignore_smoke` всегда на firearm/thrown knife). Дым по-прежнему режет sight (−70) и влияет на бой через видимость, но не через отдельный magic graze.

После обновления CommonLib проверять сигнатуру, тип результата и используемые call sites. Простое совпадение имени не гарантирует совместимость тел.

## Радиус обнаружения (`Unit:GetSightRadius`)

Канонический override: `Code/System_OR_Unit.lua`. Call sites: `UnitAwareness.lua`, `CombatAI.lua` и vanilla visibility pipeline.

### Формула

```text
sight = base_sight
      or (IsAware → AwareSightRange else UnawareSightRange)
      + (Jazz_Perk_Lynx ? Jazz_LynxSightBonus : 0)  -- same bonus softens Range CTH

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
9. Indoors (цель): `IndoorSightMod` (**−5**), независимо от Hidden/camo. Детект: packed `stance_pos` number → `AICheckIndoors`; `Point` (напр. `RevealUnitBeforeMove` `goto_pos`) → `EnumVolumes`; иначе `other.indoors`. Нельзя кормить Point в `AICheckIndoors` (`stance_pos_unpack` ожидает number).
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

### Надетая кираса Легиона (JAZZ-APPEAR-001)

Локальная установленная партия от 2026-09-16 расширяет этот механизм на `JazzArmor_Chainmail`, `JazzArmor_TireBrigantine`, `JazzArmor_TireArmor` → соответственно `JAZZ_Chainmail_Male`, `JAZZ_TireBrigantine_Male`, `JAZZ_TireArmor_Male`. Сущности находятся в `jazz_assets/Entities/`, с одноимёнными meshes/materials и `Textures/JAZZ_<item>_*`/Fallbacks. Рендеры — `jazz/ArmorIcons/Chainmail.png`, `TireBrigantine.png`, `TireArmor.png`. Все три entity/ModItem/metadata и companion зарегистрированы; сами предметы и баланс не менялись. Это установлено на диск, но ещё не подтверждено запуском игры/editor round-trip.

Вторая партия содержит девять вариантов HAV-нагрудников: `Twaron`, `Guardian` и `Zylon` в комплектациях `Light`, `Medium`, `Full`. Light оставляет только жилет, Medium добавляет воротник, нижний пояс и напашник, Full добавляет наплечники и защиту рук. Zylon использует классический woodland-рисунок владельца. Все девять entity/ModItem/UnitData зарегистрированы; runtime/editor acceptance ещё не выполнена.

Последующее обновление heavy-rig-v3 установлено на диск для ручного перезапуска владельцем: все девять вариантов получили новую привязку торса после морфинга, более низкий воротник и меньший объём верхней части плеч. Жёсткие щитки рук сохраняют привязки к основным костям рук. 81 ресурс заменён с backup; контроль хешей, регистраций и тестовых loadout пройден. Горячая перезагрузка не выполнялась, игровая посадка новой версии ещё не принята. Asset contract и repository-relative пути ниже сохранены.

Проверка владельца 2026-09-18 выявила чрезмерный зазор сзади у HAV. Статическое измерение на NPCCostumeMale_Shirt_08 подтвердило медиану 92,8 мм и p95 128,4 мм. Исправленная версия морфит общую оболочку по реальной одежде: задняя медиана около 23 мм, p95 около 29 мм. Все девять вариантов установлены на диск (81 ресурс, backup и SHA256, heavy-fit-v2); runtime acceptance остаётся открытой. Сборка теперь требует clothed front/back/side/oblique и два наклона с приближёнными весами reference-shirt; наличие этих рендеров не заменяет игровые анимации. Пакет обновления сохраняет существующие имена `Entities/JAZZ_{Twaron,Guardian,Zylon}{Light,Medium,Full}_Male.ent`, meshes/materials/textures и тестовые UnitData IDs; новые ModItem не создаются.

Три новых теста: `JAZZ_Legion_ArmorTest_Chainmail`, `JAZZ_Legion_ArmorTest_TireBrigantine`, `JAZZ_Legion_ArmorTest_TireArmor`. Они используют LegionGoon, соответствующую Torso-броню, MP40 и 120 патронов 9×19 FMJ; находятся только в группе JAZZ Tests. Кираса и `JAZZ_Legion_ArmorTest` сохранены. 2026-09-19 добавлены 19 тестовых `JAZZ_Legion_ArmorTest_*` для ванильных Flak/IBA и mapped шлемов: тот же LegionGoon/MP40/120 FMJ, Head или Torso по слоту предмета. AIM/женские модели/ванильный Легион не включены. Утерянный после загрузки ownership cache восстанавливается для управляемых Armor/Hat entities; переключение между комплектами сохраняет исходный baseline.

Evidence партии: `_check_soft_legion_armor.py` — installed hashes, resources/ModItem/metadata/companion и исполнение обоих loadout PASS; `_check_legion_armor.py` — lifecycle всех четырёх комплектов PASS. CPU QA: четыре синтетические позы × два ракурса каждого нового комплекта; веса до четырёх нормализованных влияний и существующие Male bones. Основа подогнана к NPCCostumeMale_Shirt_08; совместимость со всеми 53 Body и анимациями игры не заявлена. Полный generated-аудит имеет ранее существовавшие ошибки вне этой партии; локальная проверка не означает чистый аудит всего комплекта.

`Code/System_LegionArmorVisuals.lua` зарегистрирован после `System_UnitAppearance.lua` в metadata и ModItemCode. Единственный JAZZ-wrap `Unit:UpdateItemAppearance` вызывает CommonLib и для `unitdatadef_id = JAZZ_Legion_*` обновляет `parts.Armor` (Torso) и `parts.Hat` (Head). Источник — `GetItemInSlot` соответствующего слота; custom JAZZ-меши плюс ванильные Flak/Interceptor и 14 mapped шлемов. Общие ванильные меши получают C1/C2/C3 из design-таблицы; шлемы прячут Hair. Вещь в рюкзаке, female, AME, AIM и vanilla Legion не включают визуал. Missing entity и unmapped item возвращают baseline; mesh лица, Shirt и игровые характеристики не меняются.

Часть `AppearanceObjectPart` прикреплена к Origin, наследует Male-анимации и штатный `gofSyncState`; физические collision/walkable/apply-to-grids флаги сняты. Weak cache отслеживает принадлежащую модулю часть; outfit rebuild сбрасывает baseline, unequip восстанавливает прежнюю Armor с цветами preset. При потерянном кэше saved attachment узнаётся по entity и baseline берётся из appearance. Голова, Shirt, Chest, Hip и оружие не заменяются. CommonLib обеспечивает outfit/EnterSector updates; ItemAdded/ItemRemoved/InventoryChange и LoadGame дополнительно обновляют Torso. Никаких polling loops, новых save/network-полей или combat RNG.

Ассет: `jazz_assets/Entities/JAZZ_ImprovisedCuirass_Male.ent`, `Meshes/JAZZ_ImprovisedCuirass_Male_mesh.m.hgm`, `Materials/JAZZ_ImprovisedCuirass_Male_mesh.mtl`, `Textures/JAZZ_ImprovisedCuirass_*` и Fallbacks. Иконка: `jazz/ArmorIcons/ImprovisedCuirass.png`, прозрачный рендер 110×110. Тестовый `jazz-units/UnitData/JAZZ_Legion_ArmorTest.lua`: фиксированный `LegionGoon`, кираса, MP40, заряженный магазин и 120 FMJ; не состоит в campaign pools. Проверка через spawn этого ID в редакторе. Новый material cache создаётся игровым pipeline; editor round-trip ещё не подтверждён.

Уровень evidence: AssetsProcessor выпустил animated HGM с Male skeleton, executable Lua mocks и isolated generated-graph PASS (`docs/tools/_check_legion_armor.py`). Retail Steam launch не предоставил DAP; игровой spawn/standing/crouch/prone/aim и save/reload остаются непроверенными. Подгонка под произвольную одежду Легиона не заявляется; расширение mapping требует отдельной проверки моделей. [Карта соответствий](../../design/equipped-armor-appearance-map.md).

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
