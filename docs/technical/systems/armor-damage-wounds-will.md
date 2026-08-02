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
- `Code/GritOnStart.lua` — только `GetInitialMaxHitPoints` (75% Health / villain / BeefedUp); **Temp HP grit на CombatStart отключён** (JAZZ-MED-001);
- `Code/Systems_Medicine.lua` — тиры крови, Pain/Analgesia helpers, зональные травмы API, бинт/морфий;
- `Code/Systems_Wounds_HealWounds.lua` — лечение ран;
- `Code/System_Wounds_OperationHeal.lua` — стратегическая операция лечения;
- `Code/WillPointsBar.lua` — UI шкалы воли;
- `Code/System_GasMask.lua` — защитный предмет для газовых зон;
- generated Armor, ArmorPlate, CharacterEffect и TargetBodyPart ModItems.

## Модель брони

JAZZ добавляет/использует свойства:

- `Coverage` и `ArmorRating`;
- `MeleeArmorRating` и `ExplosiveArmorRating`;
- `CamouflagePercent`;
- `CanHoldPlate`, `ArmorPlate` и ресурс пластины;
- `BlockFaceSlot`;
- `Weight` и весовой класс;
- `NightVision`, `Vision`, `DustStormProtection`, `StunGrenadeProtection`;
- `ArmorResource`, `ArmorResourceMax`, `Repairability`;
- `PenetrationClass` (целый класс защиты 1–5 на броне/плите; та же шкала, что у оружия/патрона).

При атаке сначала определяется, покрывает ли предмет поражённую часть тела. Затем рейтинг масштабируется penetration class и состоянием предмета; для пули, melee и explosion используются разные ratings. Если установлена пластина, её защита и деградация рассматриваются отдельно. Броня теряет ресурс при поглощении урона.

Уровень подтверждения формул ниже: **static** (`Code/System_ArmorRating.lua`, companion armor/ammo). Runtime smoke по дробному пробитию не закрыт.

## Пять классов и дробное пробитие

Шкала общая для брони, плит и атаки: целые классы **1–5**. У оружия дополнительно есть `PenetrationBonus` (десятые доли класса). Эффективный pen атаки собирает `GetAttackPenetrationClass(weapon)`:

```text
weapon_pen = PenetrationClass + 0.1 × PenetrationBonus
```

Патрон через `CaliberModification` обычно:

- множит `PenetrationClass` (`mod_mul`, база `1000` = ×1; типичный FMJ промежуточного калибра `2000` → класс 2 при базовом оружии `1`);
- задаёт `PenetrationBonus` (`mod_add`, единицы «десятых»: `+2` → `+0.2` к классу).

Снимок данных (static): у `JazzArmor*` преобладают классы 2–3, реже 4–5; `ArmorRating` по классам в среднем ~18–27. У JAZZ-ammo эффективный display-диапазон примерно **0.1–4.0** (соль/дробь → .50 BMG APIT).

Связанный UI патрона: `FormatAmmoPenetrationDisplay` / `Ammo:GetRolloverHint` в [оружии/боеприпасах](weapons-ammo-components.md). Skill: `.agents/skills/jazz-penetration-scales/SKILL.md` (не класть float в `T{}` number-slot).

### Расчёт DR по пуле (`Armor:CalculateArmorRating`)

`degrade = GetDegradationMultiplier()` (состояние ресурса + износ max относительно factory).

Обычная броня (`Armor`, не плита):

| Условие | Формула |
|---|---|
| `armor.PenetrationClass > weapon_pen` | `(ArmorRating + 3 × class / weapon_pen) × degrade` |
| иначе (класс брони ≤ pen) | `ArmorRating × (class / weapon_pen)² × degrade` |

Плита (`ArmorPlates`):

| Условие | Формула |
|---|---|
| `plate.PenetrationClass >= weapon_pen` | `ArmorRating × degrade` |
| иначе | `ArmorRating × (class / weapon_pen)² × degrade` |

Асимметрия намеренная в коде: при **равных** классах плита даёт полный `ArmorRating`, жилет уже идёт по «пробитой» квадратичной ветке. Melee/explosion не сравнивают классы — только `MeleeArmorRating` / `ExplosiveArmorRating` × degrade.

### `Unit:ApplyHitDamageReduction`

1. Собрать все надетые `Armor` с `ProtectedBodyParts[hit_body_part]`.
2. Вычислить `weapon_pen` через `GetAttackPenetrationClass(weapon)`.
3. Флаг pierce для `hit.armor_pen`: `weapon_pen < item.PenetrationClass` → непробито; иначе пробито (равенство = пробито для статусов).
4. Промах по `Coverage` (один `Random(100)` на hit): если `Coverage <= roll`, локально `weapon_pen += 1` для последующего DR этого предмета.
5. Суммировать DR по всем покрывающим предметам; `hit.damage = max(1, damage − dr)`.
6. Деградация ресурса: `MulDivRound(item.Degradation, hit.damage, 100)` в `hit.armor_decay`.

`IsArmorPiercedBy` (криты и т.п.) сравнивает `damage − DR` с `Min(damage/2, 10)` по тому же `GetAttackPenetrationClass` и **не** использует тот же pierce-флаг, что статусы.

Урон по не-юнитам (`System_OR_Weapons.lua`) использует ту же `GetAttackPenetrationClass(self)` против `target.armor_class`.

### Известные оговорки реализации (static)

1. Legacy: `AdditionalReduction` / старый pierce-branch в `ApplyHitDamageReduction` закомментированы; актуальный DR — только через `CalculateArmorRating*`.
2. Часть vanilla/ранних жилетов без явного `PenetrationClass`/`ArmorRating` в companion (например часть `Flak*`) опирается на defaults шаблона — проверять перед балансными правками.
3. Исправлено (2026-07-30): unit/object path на `GetAttackPenetrationClass`; ammo UI сначала вернули float в `T{}` (`.45ACP` **0.9** показывалось как **0** из‑за усечения), затем — целые десятые + `Untranslated` (`FormatAmmoPenetrationDisplay`).

### Аудит дизайна и кода (static, 2026-07-30)

**Геймплей.** Пять классов + десятые — хороший язык: AP vs soft, плита vs жилет, покрытие vs дыры (`Coverage`). Квадратичный штраф при недопробитии даёт плавный, а не бинарный «пробил/нет». Слабое место данных: почти все `JazzArmor` сидят в классах 2–3 при похожем среднем `ArmorRating` (~18–21), так что дифференциация часто идёт через вес/покрытие/плиту, а не через «толщину». После починки wiring дробная калибровка патронов снова должна работать на unit DR — нужен runtime smoke.

**Код.** Ядро формул (`CalculateArmorRating*`, degrade, plates) локально согласовано; `GetAttackPenetrationClass` — единая точка для unit DR, crit pierce и object armor. `ApplyHitDamageReduction` всё ещё перегружен legacy-комментариями и смешивает два определения «pierce» (статусы vs криты).

Asset contract не менялся.

## Вес и слоты

Весовые эффекты: `WeightClass1`–`WeightClass5`, соответствующие Light, Medium, Heavy, Super-Heavy и дополнительной градации системы; отсутствие эффекта означает `None`. Штраф должен учитывать силу бойца и фактически надетые предметы.

Экипировка использует `Head`, `HeadGear`, `Torso`, `Legs`, `ArmorPlate` и face/head-совместимость. `InventoryVest` как класс существует, но отдельный `Vest` slot в `System_UnitInventory.lua` сейчас закомментирован. Не считать систему vest полностью активной только по наличию класса.

## Части тела и эффекты

Шесть target body parts: `Arms`, `Groin`, `Head`, `Legs`, `Neck`, `Torso`. Среди 56 CharacterEffect definitions находятся:

- локальные роллеры `Armsshot`, `Headshot`, `Legsshot`, `Torsoshot`, `Groinshot` (скрытые; **только** `JazzTryRollTraumaFromBodyPart` — без legacy Numbness/Inaccurate/Slowed/Blinded/Unconscious/`Bleeding` из `*shot`);
- зональные травмы `Trauma{Arms|Legs|Ribs|Head|Burn}{Light|Medium|Heavy}` (Eye folded into Head; Burn: `Burning` OnRemoved → Light stub);
- `Bleeding` / `BleedingMedium` / `BleedingHeavy` (3/6/12 ОЗ за стак/ход, кап суммы ~30; бинт −1 тир худшему стаку; JHP→тяжёлое; травмы ↑ шанс крови; центральный `JazzTryRollBleedFromHit`; legacy `BleedingChance` OnAdded = no-op);
- `Pain` / `Analgesia`; `Wounded` от HP **off** (`HpLossToAddStack` sentinel + `UnitProperties:AccumulateDamageTaken`/`AddWounds` no-op; strip on knockout/`UnitDowned`);
- `Blinded`, `Burning`, `Choking` (среда/газ; не от `*shot`); knockout merc → `JazzApplyKnockoutTraumaPackage` (heavy + Pain);
- уровни suppression и weight class;
- perks и прочие status effects.

27 effects наследуют `Perk`, 22 — `StatusEffect`, остальные — базовый `CharacterEffect` или специализированные родители. IDs являются публичным контрактом actions, UI, unit presets и лечения.

`hit.effects` содержит только непустые строковые ID CharacterEffect. Обычный эффект попадания применяется, если закрывающая точку броня не участвовала в расчёте либо хотя бы один участвовавший предмет присутствует в `hit.armor_pen`. Поэтому непробитая броня блокирует `Bleeding`, body-part `*shot` и другие физические статусы из `hit.effects`, даже когда минимальный урон попадания остался ненулевым.

**Заброневое (BAT):** если был `armor_decay` и **нет** `armor_pen`, `ApplyDamageAndEffects` вызывает `JazzTryBehindArmorTrauma` — шанс Light (редко Medium) травмы зоны попадания + `Pain`, без крови. Шанс ~`15 + energy/2` (cap 65), `energy = armor_prevented + residual damage`; порог energy ≥ 8.

`MarkedTraccers` является исключением из damage pipeline: он не применяется из `hit.effects`, а ставится на выбранную цель один раз за каждый фактически произведённый выстрел трассерным боеприпасом с итоговым `shot_cth > 0`. Фактическое попадание и пробитие брони для маркера не требуются; при `shot_cth == 0` эффект не ставится.

### Намеренная замена `DamageReduction`

CharacterEffect `DamageReduction` намеренно сохраняет имя vanilla-класса и одноимённый preset ID. JAZZ не создаёт параллельный effect с собственным namespace, а полностью заменяет vanilla-определение:

```lua
UndefineClass('DamageReduction')
DefineClass.DamageReduction = {
```

Эта пара является обязательной частью generated companion `CharacterEffect/DamageReduction.lua`: первый вызов удаляет уже построенный vanilla-класс, второй регистрирует реализацию JAZZ под тем же именем. Переименование в `JAZZ_DamageReduction`, наследование под новым ID или сохранение обоих классов не эквивалентны полной замене, поскольку runtime и presets обращаются к точному имени `DamageReduction`. Правило о префиксе `JAZZ_` здесь неприменимо; отсутствие префикса не является дефектом.

Актуальный CommonLib 1.11, build 1056, commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c` не содержит одноимённого определения. При обновлении vanilla необходимо заново сравнить родителя, properties, reactions, lifetime и обращения к preset. При синхронизации generated data обе строки заголовка должны сохраняться вместе с definition в `items.lua` и metadata-записью; отсутствие `UndefineClass` или `DefineClass.DamageReduction` означает неполную generated-транзакцию, а не основание вводить новое имя.

В damage breakdown `DamageReduction` используется только как источник локализованного `DisplayName`. Объект preset/class запрещено помещать в `hit.effects`: `EffectTableAdd` и `Unit:AddStatusEffect` принимают строковый effect ID.

## Ранения и лечение

Тактическое и стратегическое лечение объединяет набор связанных состояний. Текущая operation heal снимает `Wounded`, `Inaccurate`, `Slowed` и bleed tiers вместе. Зональные `Trauma*` **не** снимаются полевой перевязкой/бинтом (MED-002: госпиталь / заживление).

`Bandage` остаётся CombatAction, а стратегические sector operations используют отдельный runtime. Проверять оба пути и переход между ними.

### Зональные травмы (MED-001)

Публичные ID: `Trauma{Arms|Legs|Ribs|Head|Burn}{Light|Medium|Heavy}`.

| Тир | Специфик | Боль |
| --- | --- | --- |
| Light | нет | при юзе зоны (`JazzTraumaPainOnZoneUse`) |
| Medium | zone debuff | при юзе зоны |
| Heavy | жёсткий zone debuff | +1 Pain/ход к капу (`JazzTraumaHeavyPainRamp`) |

Zone specifics (Medium / Heavy params): Arms −20/−50 CTH; Legs +50%/+150% move, no Free Move; Ribs −2/−5 start AP, no Free Move, **no Tired**; Head −15/−40 CTH and −20/−50 sight. Eye folded into Head. Hit wiring: `*shot` OnAdded → `JazzTryRollTraumaFromBodyPart` on **d100** (не `Random(HP)` — иначе при низком HP почти всегда Medium+). Limb/Ribs/Burn thresholds: Heavy **&lt;3**, Medium **&lt;12**, Light **&lt;55**; Head **8 / 28 / 48**. **Armor trauma soft-mitigation (pierced path):** `JazzGetTraumaArmorChanceFactor` — worn `Armor` with `ProtectedBodyParts` for the zone, Condition > 0, scales roll thresholds (floor factor **40**). **BAT (unpierced):** `JazzTryBehindArmorTrauma` from `ApplyDamageAndEffects` — Light/rarely Medium + Pain, no bleed. **Grazing / царапина:** no trauma / BAT / `*shot` / Medium+ bleed; `JazzTryRollBleedFromGraze` — **15%** → только `Bleeding`. Knockout merc: `JazzApplyKnockoutTraumaPackage`. Burn: `Burning` OnRemoved → `TraumaBurnLight`. Icons: `Icons/StatusEffects/Trauma*.png`.

**Прогресс / UI:** при apply ставится `next_check_time` (CampaignTime). Интервалы: Light **8** ч (Burn **12**), Medium **24** (Burn **36**), Heavy **48** (Burn **72**). `OnMsg.NewHour` → `JazzTraumaProgressOnNewHour` роллит improve/worsen/stay (`JazzTraumaProgressChances`). `GetDescription` на `Trauma*` через hook (base `JazzTraumaBaseGetDescription`, без stack при ReloadLua) дописывает один блок «Next progress check…» + tier flavor. Полный hospital clear / ускорение лечением — MED-002.

**Hotbar medicine:** `JazzBandage` (stack `JAZZ_Bandage`, −1 bleed tier, AP 1000); `Bandage` (kits via `JazzGetEquippedKitMedicine` only); `JazzMorphine` (`RequireWeapon=false`). Targeting: `JazzGetFieldBandageTargets` / `JazzGetMorphineTargets` (all Jazz bleed tiers / Pain); vanilla `GetBandageTargets` wrapped to include Medium/Heavy bleed. Legs `TargetBodyPart.applied_effect` = `Legsshot` (не `Slowed`). `Wounded` companion: `HpLossToAddStack=999999` (sentinel synced with items.lua).

## Grit и временное здоровье

**JAZZ-MED-001:** на старте боя Temp HP grit (~25% Health) **не выдаётся**. Базовая часть HP по-прежнему вокруг 75% Health (`GetInitialMaxHitPoints`); для villains — отдельный constant modifier. Перк `TrueGrit` не связан с отключённым CombatStart grit.

## Will Points и подавление

JAZZ добавляет unit attribute `Will` и derived `WillPoints`/`MaxWillPoints`. Взрывы и suppressive fire уменьшают Will и переводят цель по уровням подавления вплоть до `Pinned`. `WillPointsBar.lua` обновляет UI на `CombatEnd` и `TurnEnd` и при runtime-изменениях состояния.

### Уровни и контратака (JAZZ-COMBAT-003)

| Эффект | Смысл | CTH атакующего | Контратака (`Unit:Retaliate`) |
| --- | --- | --- | --- |
| `suppressionLight` | Обстрелян | −10 | да, со штрафом CTH |
| `suppressionMedium` | Под огнем | −20 | да, со штрафом CTH |
| `suppressionHeavy` | Под плотным огнем | −30 | да, со штрафом CTH |
| `suppressionHeavy2` | Подавлен | −50 | да, со штрафом CTH |
| `suppressionPinned` | Прижат | −70 | **нет** |

CTH-модификатор `Suppression` применяется на любой дистанции (в т.ч. opportunity / retaliation), не только дальше 5 клеток.

### Psycho и восстановление Will

- `Psycho` не получает Will damage от огневого подавления и не получает suppression tiers; при низком Will может уйти в `Berserk`.
- Каждый `BeginTurn` без `Berserk`: drain **−4** Will (раньше −8) и ранний выход из обычного leadership-regen.
- На `CombatEnd` у всех живых human `WillPoints` сбрасываются на `MaxWillPoints` (`OnMsg.CombatEnd` в `System_OR_Unit.lua`), чтобы срыв не переносился в следующий бой.

Will связан одновременно с damage, AI, effects и UI. Любое изменение формулы должно проверять не только число, но и пороги статусов, действия AI и очистку в конце боя.

## Межпакетные зависимости

- `jazz` владеет классами, effects, armor items и runtime;
- `jazz-units` назначает броню, stats, perks и loot юнитам;
- `jazz-maps` размещает armor/plates и запускает бои/операции;
- `jazz_assets` предоставляет entities экипировки и визуальные attachments.

## Проверка

- каждую body part с покрытием/без покрытия;
- bullet, melee и explosion при разных penetration classes **и** дробном `PenetrationBonus` (ожидание: `class + 0.1×bonus` в unit DR);
- патрон с `PenetrationBonus ≠ 0` против брони на границе класса (например pen 2.8 vs armor 3);
- новую, повреждённую и разрушенную броню/пластину;
- face/head slot conflict и gas mask;
- весовые классы на бойцах с разной Strength;
- получение/лечение каждого wound-related status;
- обычные effects при непробитой броне, пробитой броне и отсутствии покрытия;
- трассерный выстрел при попадании/промахе с CTH больше нуля и невозможный выстрел с CTH `0`;
- после чистого запуска `g_Classes.DamageReduction` и preset `DamageReduction` разрешаются в реализацию JAZZ, без параллельного класса под новым ID;
- Bandage против operation heal, save/load между стадиями;
- Grit на старте и очистка после боя;
- Will loss, suppression tiers, UI bar, end-turn/end-combat;
- сетевой бой и загрузка старого сохранения.

## Сопровождение

При изменении armor properties, body parts, status IDs, Will или лечения обновлять эту страницу, inventory и gameplay docs. Активация Vest slot должна быть явно отмечена в coverage и compatibility как изменение схемы инвентаря/savegame.