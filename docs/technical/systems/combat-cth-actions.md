# Бой, CTH и боевые действия

## Назначение и эффект для игрока

JAZZ заменяет основной цикл расчёта попадания и существенную часть выполнения атак. Навык обращения с оружием, вторичная характеристика, уровень, прицеливание, дистанция, кучность, состояние оружия, положение цели, погода и статусы соединяются в один CTH pipeline. Автоматический огонь дополнительно накапливает отдачу между пулями; набор действий расширен специальными очередями, манёврами и именными способностями.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | `Unit:CalcChanceToHit`, CTH modifiers, `CombatActions`, `UnitActions`, crosshair, area-aim и выполнение firearm attacks дают базовый API и жизненный цикл атаки |
| CommonLib | Исправляет AI/боевые функции; прямое пересечение с JAZZ подтверждено для `Unit:RunAndGun`. UI actions CommonLib пересекаются с `Unit:EnumUIActions` в другой части боевого контура |
| JAZZ | Заменяет формулу CTH/дальности, часть действий и исполнения выстрелов, визуализацию прицела и боевого badge; добавляет собственные CombatAction presets |

Точные прямые коллизии перечислены в [матрице переопределений](../override-matrix.md). Для установленного билда vanilla сравнивать с `<JA3_ROOT>\ModTools\Src`, а не только с более старым GitHub source drop.

## Реализация и load-state

Все перечисленные файлы `jazz` загружаются:

- `Code/AccuracyRangeCTH.lua` — итоговый CTH и range accuracy;
- `Code/CombatActions.lua` — действия юнитов, включая Run and Gun;
- `Code/ExecFirearmAttacks.lua` — выполнение firearm attack и последовательность выстрелов;
- `Code/IModeCombatAreaAim.lua` — UI-режим зонального прицеливания;
- `Code/CrossHairUI.lua` — crosshair, разбивка модификаторов и отображение CTH;
- `Code/CombatBadge_DeathRoll.lua` — состояние цели, LOS/LOF, боевые предупреждения и счётчики;
- `Code/UnitPropertiesStats.lua` — дополнительные характеристики, используемые боевыми расчётами;
- `Code/Camera.lua` — небольшая настройка камеры, влияющая на представление боя;
- generated `CombatAction` и `CTHModifier` ModItems — данные действий и модификаторов.

## Формула базового навыка попадания в текущем runtime

`Unit:CalcChanceToHit` начинает с базового навыка оружия. Вторичная характеристика — `Strength` для `MachineGun`, иначе `Dexterity`. Для огнестрельной атаки исходная смесь:

```text
raw_skill = (weapon_skill × 4 + secondary_stat × 2 + level × 5) / 6
skill_cth = 20 + raw_skill^1.2 × 0.25
```

Результат округляется через `floor(value + 0.5)`. Для melee веса основной и вторичной характеристики меняются местами: 2 и 4 вместо 4 и 2. Затем последовательно применяются CTH presets, status effects, component effects, реакции и поправка дальности. Порядок важен: перестановка стадий является изменением баланса даже при тех же числах.

Целевой дизайн из финальной вкладки `Пист` использует степень `1.25`, нелинейный коэффициент Marksmanship для каждого клика и кусочную дистанционную кривую. Вкладка `ЭЭЭксперименты` не является источником. До синхронизации Lua это документированный runtime mismatch; точный контракт и нерешённый расчёт `EffectiveRange1/2` описаны в [канонической модели точности](../weapons/accuracy-model.md).

## Дальность и кучность в текущем runtime

`GetRangeAccuracy` использует:

- `WeaponRange` — рабочую дальность;
- `BulletDropRange` — точку/масштаб падения эффективности;
- `Grouping` — кучность;
- нелинейную экспоненциально-логарифмическую кривую;
- множитель кривой `1.8`.

Поэтому два оружия с одинаковым `WeaponRange` могут иметь разную дальнюю эффективность. Износ оружия ухудшает `Grouping`, а значит влияет на CTH косвенно, до попадания.

## Данные действий

В snapshot зарегистрировано 53 `CombatAction`. Базовые семейства переопределены или расширены: `SingleShot`, `BurstFire`, `AutoFire`, `MGBurstFire`, `Buckshot`, `BuckshotBurst`, `AttackShotgun`, `Overwatch`, `PinDown`, `RunAndGun`, `RunAndGun_Carbine`, `MobileShot`, `MeleeAttack`, `Bandage`, `Unjam`, `MGSetup`, несколько `ThrowGrenade`.

Собственные действия JAZZ включают:

- `JAZZ_ControllableBurst`, `JAZZ_LargeAutoFire`, `JAZZ_MGSuppressionFire`, `JAZZ_Salvo`, `JAZZ_TargetSweep`;
- `JAZZ_DoubleTap`, `JAZZ_Mozambique`, `JAZZ_Fanning`, `JAZZ_Zipper`, `JAZZ_JokerShot`, `JAZZ_Bullseye`;
- `JAZZ_SmgStorm`, `JAZZ_RunAndSMGStorm`, `JAZZ_MobileShotgun`, `JAZZ_ManeuverAR`;
- именные perk-actions `Jazz_Perk_00`, `Jazz_Perk_Buzz`, `Jazz_Perk_Lynx`, `Jazz_Perk_Spider`, `JAZZ_VovaVist`, `GrizzlyPerk`;
- режимы компонентов `FoldStock`, `UnFoldStock`, `FlashlightOn`, `FlashlightOff`;
- уникальные `AbakanBurst`, `AbakanAutoFire`, `DoubleBarrel`, `CancelShotCone`.

## Runtime flow

1. UI или AI выбирает `CombatAction` и собирает targeting parameters.
2. Crosshair/area-aim вычисляет доступность, AP, цель, траекторию и модификаторы.
3. `Unit:CalcChanceToHit` строит базовый навык и применяет модификаторы/дальность.
4. firearm executor формирует последовательность выстрелов; для очередей последующие пули получают recoil/разброс.
5. попадания передаются damage/armor/wound и suppression системам.
6. UI обновляет боевой badge, CTH breakdown, ammo/reload, overwatch и очереди действий.

## Публичные контракты и риски

- IDs `CombatAction` и `CTHModifier` используются generated items, AI и UI.
- `Unit:RunAndGun` заменён после CommonLib; обновление CLib требует ручного merge исправлений.
- Crosshair и area-aim являются изменёнными аналогами крупных vanilla-файлов и чувствительны к обновлению игры.
- Изменение порядка `metadata.lua` может заменить финальную реализацию функции другой копией.
- CTH, recoil и RNG должны оставаться детерминированными в сетевой игре.

## Проверка

- одиночный выстрел без aim и с максимальным aim на ближней, рабочей и дальней дистанции;
- одинаковое оружие при высоком/низком навыке, уровне и Dexterity/Strength;
- melee и MachineGun для проверки выбора вторичной характеристики;
- короткая/длинная очередь, первый и последующие выстрелы;
- shotgun/area aim, grenade area, overwatch, PinDown и Run and Gun;
- повреждённое оружие с ухудшенной Grouping;
- совпадение CTH breakdown с фактическим pipeline;
- AI-выполнение тех же действий и сетевой повтор.

## Ограничения и сопровождение

Крупные модули частично происходят из vanilla-кода и должны сравниваться трёхсторонним diff после обновления игры. При изменении формулы, действий или UI одновременно обновлять эту страницу, [каноническую модель точности](../weapons/accuracy-model.md), [гайд по бою и точности](../../wiki/combat-and-accuracy.md), `docs/technical/testing.md`, а при коллизии — `docs/technical/override-matrix.md`.
