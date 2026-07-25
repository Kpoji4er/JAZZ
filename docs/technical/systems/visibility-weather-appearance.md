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

`IsLineInSmoke` не найден как экспортированный глобальный символ в просмотренном vanilla source, появляется в CommonLib и затем заменяется JAZZ. Это dependency-owned API, поверх которого JAZZ строит собственную семантику.

Smoke участвует в:

- расчёте линии видимости/атаки;
- CTH modifiers;
- suspicion и awareness;
- AI targeting и позиции;
- gas/smoke protective equipment.

После обновления CommonLib проверять сигнатуру, тип результата и используемые call sites. Простое совпадение имени не гарантирует совместимость тел.

## Камуфляж и защита от среды

Armor properties `CamouflagePercent`, `NightVision`, `Vision`, `DustStormProtection` и `StunGrenadeProtection` меняют tactical условия. Gas mask отдельно защищает от toxic/tear gas и зависит от состояния ресурса.

Камуфляж должен влиять на detection pipeline, а не напрямую скрывать unit независимо от LOS. Night vision/vision обязаны согласоваться с light/darkness modifiers и UI-индикацией.

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
- LOS через smoke, на границе дыма и без дыма;
- AI detection/suspicion с camo, night vision и плохой погодой;
- rain jam и dust protection;
- gas mask новая/сломанная, toxic/tear gas;
- bipod, stock, magazine, scope и mask entity states;
- отсутствие `missing entity/state/spot/material` в логе;
- подтверждение, что `NoSoundsInRooms.lua` остаётся inert до намеренной активации.

## Сопровождение

При изменении weather, smoke, visibility property или appearance state обновлять эту страницу, AI/weapon/assets docs и тесты. Активация `NoSoundsInRooms.lua` считается новым runtime-поведением и должна отдельно документироваться.