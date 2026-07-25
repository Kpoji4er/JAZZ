# Броня, повреждения, ранения и воля

## Назначение и эффект для игрока

JAZZ разделяет физическую защиту по покрытию, типу урона, penetration, состоянию и съёмной пластине. Попадания в части тела дают отдельные последствия; ранения, bleeding, slowed и inaccurate связаны с тактическим лечением и стратегической операцией. Дополнительная шкала Will участвует в подавлении и боевой устойчивости.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | Armor, damage pipeline, body parts, CharacterEffect, wounds, Bandage/Heal и unit stats |
| CommonLib | Прямой одноимённой коллизии с центральными armor/wound functions в проверенном срезе не подтверждено; используются общие hooks/helpers dependency |
| JAZZ | Добавляет рейтинги по типу урона, покрытие, пластины, ресурс брони, весовые классы, body-part effects, Will Points и переработанное лечение |

## Реализация и load-state

Загружаемые файлы `jazz`:

- `Code/System_ArmorRating.lua` — выбор покрытия, penetration и рейтинг защиты;
- `Code/UnitPropertiesStats.lua` — свойства юнита, Will и связанные derived values;
- `Code/System_OR_Unit.lua` — damage/status/unit runtime;
- `Code/System_Vest.lua` — классы/поведение vest, хотя отдельный Vest slot в текущем inventory-коде закомментирован;
- `Code/GritOnStart.lua` — временное здоровье на старте боя;
- `Code/Systems_Wounds_HealWounds.lua` — лечение ран;
- `Code/System_Wounds_OperationHeal.lua` — стратегическая операция лечения;
- `Code/WillPointsBar.lua` — UI шкалы воли;
- `Code/System_GasMask.lua` — защитный предмет для газовых зон;
- generated Armor, ArmorPlate, CharacterEffect, TargetBodyPart и GameRule ModItems.

## Модель брони

JAZZ добавляет/использует свойства:

- `Coverage` и `ArmorRating`;
- `MeleeArmorRating` и `ExplosiveArmorRating`;
- `CamouflagePercent`;
- `CanHoldPlate`, `ArmorPlate` и ресурс пластины;
- `BlockFaceSlot`;
- `Weight` и весовой класс;
- `NightVision`, `Vision`, `DustStormProtection`, `StunGrenadeProtection`;
- `ArmorResource`, `ArmorResourceMax`, `Repairability`.

При атаке сначала определяется, покрывает ли предмет поражённую часть тела. Затем рейтинг масштабируется penetration class и состоянием предмета; для пули, melee и explosion используются разные ratings. Если установлена пластина, её защита и деградация рассматриваются отдельно. Броня теряет ресурс при поглощении урона.

## Вес и слоты

Весовые эффекты: `WeightClass1`–`WeightClass5`, соответствующие Light, Medium, Heavy, Super-Heavy и дополнительной градации системы; отсутствие эффекта означает `None`. Штраф должен учитывать силу бойца и фактически надетые предметы.

Экипировка использует `Head`, `HeadGear`, `Torso`, `Legs`, `ArmorPlate` и face/head-совместимость. `InventoryVest` как класс существует, но отдельный `Vest` slot в `System_UnitInventory.lua` сейчас закомментирован. Не считать систему vest полностью активной только по наличию класса.

## Части тела и эффекты

Шесть target body parts: `Arms`, `Groin`, `Head`, `Legs`, `Neck`, `Torso`. Среди 56 CharacterEffect definitions находятся:

- локальные последствия `Armsshot`, `Headshot`, `Legsshot`, `Torsoshot`, `Groinshot`;
- `Bleeding`, `Wounded`, `Inaccurate`, `Slowed`;
- `Blinded`, `Burning`, `Choking`;
- уровни suppression и weight class;
- perks и прочие status effects.

27 effects наследуют `Perk`, 22 — `StatusEffect`, остальные — базовый `CharacterEffect` или специализированные родители. IDs являются публичным контрактом actions, UI, unit presets и лечения.

## Ранения и лечение

Тактическое и стратегическое лечение объединяет набор связанных состояний. Текущая operation heal снимает `Wounded`, `Inaccurate`, `Slowed` и `Bleeding` вместе. Это значимое правило, а не косметический cleanup: разделение вызовов может изменить стоимость/время операции и сохранённые статусы.

`Bandage` остаётся CombatAction, а стратегические sector operations используют отдельный runtime. Проверять оба пути и переход между ними.

## Grit и временное здоровье

На старте боя `GritOnStart.lua` выдаёт временное здоровье в размере 25% Health. Базовая часть HP построена вокруг 75% здоровья; для villains применяется отдельный constant modifier. Временное здоровье не должно незаметно сериализоваться как постоянный MaxHitPoints или переживать неверную фазу завершения боя.

## Will Points и подавление

JAZZ добавляет unit attribute `Will` и derived `WillPoints`/`MaxWillPoints`. Взрывы и suppressive fire уменьшают Will и переводят цель по уровням подавления вплоть до `Pinned`. `WillPointsBar.lua` обновляет UI на `CombatEnd` и `TurnEnd` и при runtime-изменениях состояния.

Will связан одновременно с damage, AI, effects и UI. Любое изменение формулы должно проверять не только число, но и пороги статусов, действия AI и очистку в конце боя.

## Межпакетные зависимости

- `jazz` владеет классами, effects, armor items и runtime;
- `jazz-units` назначает броню, stats, perks и loot юнитам;
- `jazz-maps` размещает armor/plates и запускает бои/операции;
- `jazz_assets` предоставляет entities экипировки и визуальные attachments.

## Проверка

- каждую body part с покрытием/без покрытия;
- bullet, melee и explosion при разных penetration classes;
- новую, повреждённую и разрушенную броню/пластину;
- face/head slot conflict и gas mask;
- весовые классы на бойцах с разной Strength;
- получение/лечение каждого wound-related status;
- Bandage против operation heal, save/load между стадиями;
- Grit на старте и очистка после боя;
- Will loss, suppression tiers, UI bar, end-turn/end-combat;
- сетевой бой и загрузка старого сохранения.

## Сопровождение

При изменении armor properties, body parts, status IDs, Will или лечения обновлять эту страницу, inventory и gameplay docs. Активация Vest slot должна быть явно отмечена в coverage и compatibility как изменение схемы инвентаря/savegame.