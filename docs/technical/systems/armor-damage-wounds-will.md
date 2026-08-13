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
- `Code/GritOnStart.lua` — только `GetInitialMaxHitPoints` (**100%** Health / villain / BeefedUp); **Temp HP grit на CombatStart отключён** (JAZZ-MED-001);
- `Code/Systems_Medicine.lua` — тиры крови, Pain/Analgesia helpers, зональные травмы API, бинт/морфий;
- `Code/Systems_Wounds_HealWounds.lua` — лечение ран;
- `Code/System_Wounds_OperationHeal.lua` — стратегическая операция лечения;
- `Code/WillPointsBar.lua` — UI шкалы воли;
- `Code/System_GasMask.lua` — защитный предмет для газовых зон;
- `Code/System_EnergyLadder.lua` — JAZZ-COMBAT-007/008: лестница энергии Fit→Exhausted, gradual Free Move, satellite warn/times; Legs foot-travel slow + Ribs tiredness threshold;
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

**`ignore_armor`** (KalynaPerk Inevitable Strike, `JAZZ_Bullseye`, и т.п.): если `PrecalcDamageAndStatusEffects` передал `ignore_armor`/`data.ignore_armor`, `ApplyHitDamageReduction` **не** вычитает `CalculateArmorRating*` и не деградирует броню (только `armor_pen`). Раньше jazz ставил pierce, но всё равно снимал DR — из‑за этого перк Калины «не работал» по JazzArmor (в т.ч. при тесте огнём по своим).

`IsArmorPiercedBy` (криты и т.п.) сравнивает `damage − DR` с `Min(damage/2, 10)` по тому же `GetAttackPenetrationClass` и **не** использует тот же pierce-флаг, что статусы. Для `KalynaPerk` / `JAZZ_Bullseye` сразу `true, "ignored"`.

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

`Unit:CalculateArmorWeight` (JAZZ-COMBAT-005) на `BeginTurn` / `OnGearChanged`:

1. Сырой FreeMove по надетым `Armor` (`Weight` 2/3/4/5 → +0.5/+1/+2/+3; слот ≠ Inventory; плиты с Weight входят).
2. Сырой start AP: raw_FM &lt; 4 → 0; 4…&lt;8 → 1; ≥ 8 → 2.
3. **Ironclad** или **KillingWind** → FM ÷2 **один раз** (Fauda с обоими не получает ÷4). **Ironclad** дополнительно ÷2 AP. При `using_cumbersome` AP-штраф брони = 0 (FM брони не half от cumbersome). Strength &gt; 60: `MulDivRound(STR−60,1,20)` сначала снимает AP, остаток — FM.
4. Floor + cap FM ≤ 12, AP ≤ 2; списание `ConsumeAP(FM|AP * const.Scale.AP)` (Move / обычные ОД).
5. Статусы `Weight_1Class`…`Weight_5Class`: стаки = floor(FM), класс иконки = **max Weight** экипа (не PenetrationClass). `OnCalcMoveModifier` → `JazzArmorWeightPainOnMove`: при FM ≥ 6 первое перемещение за ход даёт +1 Pain (≤1 стек/ход от веса; Analgesia блокирует).

### Энергия / Tiredness (JAZZ-COMBAT-007)

Шкала `Tiredness` −1…4 (Unconscious **не** на лестнице):

| Level | CE | Start AP | Free Move |
|---|---|---|---|
| −1 | `WellRested` | +2 | ×120%; opening **+2 FM AP** on combat turns 1–3 |
| 0 | `Fit` | +1 | ×120%; opening **+2 FM AP** on combat turn 1 |
| 1 | `Winded` | 0 | ×100% |
| 2 | `Fatigued` | 0 | ×75% |
| 3 | `Tired` | −1 | ×50% |
| 4 | `Exhausted` | −2 (BeginTurn ConsumeAP) | 0 + FreeMove immunity + travel stop |

Runtime: `Code/System_EnergyLadder.lua` remaps `const.ut*` / `UnitTirednessEffect`, wraps `UnitProperties.SetTired`, patches satellite travel≈½ / rest≈¾ vanilla per step, multi-stage warn 50%/20% (`JazzEnergyTravelWarn`) + step CombatLog. `FreeMove` Condition: `Tiredness < utExhausted`. Armor-weight FM (COMBAT-005) stacks separately on top of mul/add.

CE companions: `CharacterEffect/{Fit,Winded,Fatigued,Tired,Exhausted,WellRested,FreeMove}.lua`.

### Травмы → travel / энергия (JAZZ-COMBAT-008)

| Источник | Эффект | Где |
|---|---|---|
| `TraumaLegs{Light\|Medium\|Heavy}` | пеший `GetSectorTravelTime` ×1.10 / 1.20 / 1.30 (худший в отряде; кап 30%) | wrap в `System_EnergyLadder.lua` |
| `TraumaRibs{Light\|Medium\|Heavy}` | порог `UnitTirednessTravelTime` ×0.85 / 0.70 / 0.55 на мерка | `JazzGetTirednessTravelThreshold` → `ReachSectorCenter` |
| HP (`GetHPAdditionalTiredTime`) | всегда **0** | `SatelliteSquad.lua` |

Skip Legs-slow: Water terrain/passability, shortcut, river special, `JAZZ_vehicle` mounted. Breakdown UI: T `890000000013121`.


Cumbersome на оружии по-прежнему может не выдавать FreeMove в BeginTurn (**KillingWind** всегда получает FreeMove с cumbersome; иначе Ironclad path).

Экипировка использует `Head`, `HeadGear`, `Torso`, `Legs`, `ArmorPlate` и face/head-совместимость. `InventoryVest` как класс существует, но отдельный `Vest` slot в `System_UnitInventory.lua` сейчас закомментирован. Не считать систему vest полностью активной только по наличию класса.

## Части тела и эффекты

Шесть target body parts: `Arms`, `Groin`, `Head`, `Legs`, `Neck`, `Torso`. Среди 56 CharacterEffect definitions находятся:

- локальные роллеры `Armsshot`, `Headshot`, `Legsshot`, `Torsoshot`, `Groinshot` (скрытые; **только** `JazzTryRollTraumaFromBodyPart` — без legacy Numbness/Inaccurate/Slowed/Blinded/Unconscious/`Bleeding` из `*shot`);
- зональные травмы `Trauma{Arms|Legs|Ribs|Head|Burn}{Light|Medium|Heavy}` (Eye folded into Head; Burn: `Burning` OnRemoved → Light stub);
- `Bleeding` / `BleedingMedium` / `BleedingHeavy` (3/6/12 ОЗ за стак/ход, кап суммы ~30; полевой бинт за одно применение тратит `Min(стаки крови, запас бинтов)` и столько же раз делает −1 тир худшему стаку; JHP→тяжёлое; травмы ↑ шанс крови; центральный `JazzTryRollBleedFromHit`; legacy `BleedingChance` OnAdded = no-op);
- `Pain` / `Analgesia`: Pain сохраняет точный штраф ОД, применённый на `OnCalcStartTurnAP`, вместе с номером хода; `Analgesia.OnAdded` через `JazzRefundPainStartTurnAP` один раз возвращает только этот штраф и обнуляет маркер, затем **снимает все стаки Pain**. Пока Analgesia активна, `JazzAddPainStacks` = no-op. Повторное обезболивание и Pain, полученная после начала хода, ОД не дают. В бою Pain −1 стак/`OnEndTurn`; **`RemoveOnEndCombat`** снимает Pain/Analgesia при конце боя. `Wounded` от HP **off** (`HpLossToAddStack` sentinel + `UnitProperties:AccumulateDamageTaken`/`AddWounds` no-op). `OnMsg.UnitDowned` немедленно вызывает `JazzApplyDownedHeavyTrauma`: одна физическая Heavy trauma +3 Pain, с upgrade уже выпавшей Light/Medium; более лёгкий same-hit эффект и повторный `Unconscious` не дублируют пакет;
- **`WoundInfected`** (MED-002): отдельный Debuff рядом с Heavy (Trauma* не заменяются). Untreated Heavy progress, не improve → `JazzApplyWoundInfected` (пишется и на `Unit`, и на `UnitData`; UI props `Shown`/`Icon`/`ShownSatelliteView` штампуются с Def). Infected progress (**16h**, survive **40%**): успех снимает Infected; провал → `JazzKillMercFromInfection`. TreatWounds/`jazz_healing` на Heavy improve 100% → вход в Infected невозможен. Иконка в бою (`GetUIVisibleStatusEffects`) и на глобалке (`JazzGetPartyPortraitStatusEffects`, приоритет над клипом MaxHeight).
- **`BloodLoss50`…`BloodLoss1`** (MED-002): при HP% &lt;50/40/30/20/10/5/1 (−1…−7 start AP); 1 HP → `BloodLoss1` («критическая кровопотеря, ещё в сознании»). Sync `JazzSyncBloodLossStatus`. **`GetMaxActionPoints`** считает от attribute `Health`, не от текущих `HitPoints`.
- `Blinded`, `Burning`, `Choking` (среда/газ; не от `*shot`); knockout merc → `JazzApplyKnockoutTraumaPackage` (heavy + Pain);
- уровни suppression и weight class;
- perks и прочие status effects.

27 effects наследуют `Perk`, 22 — `StatusEffect`, остальные — базовый `CharacterEffect` или специализированные родители. IDs являются публичным контрактом actions, UI, unit presets и лечения.

`hit.effects` содержит только непустые строковые ID CharacterEffect. Обычный эффект попадания применяется, если закрывающая точку броня не участвовала в расчёте либо хотя бы один участвовавший предмет присутствует в `hit.armor_pen`. Поэтому непробитая броня блокирует `Bleeding`, body-part `*shot` и другие физические статусы из `hit.effects`, даже когда минимальный урон попадания остался ненулевым.

**Исключение — blast (`hit.explosion`):** статусы из `hit.effects` (в т.ч. `*shot` → trauma) применяются **без** требования pierce; bleed всё ещё только при pierce. BAT на explosion не вызывается. Отдельно `JazzTryApplyExplosionConcussionAndTrauma` **гарантированно** вешает `Concussion` и, при отсутствии `*shot` в effects, роллит зональную травму (шанс). Затем `JazzTryBlastKnockback` (JAZZ-GRENADES-002): только во внутреннем кольце `CenterAreaOfEffect` (Dist2D); skill roll Strength+Health vs pre-armor force → Steroid-style отлёт — см. [explosives-traps-heavy-weapons.md](explosives-traps-heavy-weapons.md).

**Заброневое (BAT):** если был `armor_decay` и **нет** `armor_pen` (**и не explosion**), `ApplyDamageAndEffects` вызывает `JazzTryBehindArmorTrauma` — шанс Light (редко Medium) травмы зоны попадания + `Pain`, без крови. Шанс ~`15 + energy/2` (cap 65), `energy = armor_prevented + residual damage`; порог energy ≥ 8.

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

Тактическое и стратегическое лечение объединяет набор связанных состояний. Текущая operation heal снимает `Wounded`, `Inaccurate`, `Slowed` и bleed tiers вместе. Зональные `Trauma*` **не** снимаются полевой перевязкой/бинтом и **не** снимаются мгновенно полевой операцией: `PatientAddHealWoundProgress` (TreatWounds) ставит на каждую `Trauma*` флаг `jazz_healing` → ускоренные проверки с **гарантированным** improve (100%) и **блок worsen** до clear/downgrade. Мгновенный hospital clear — MED-002. `HealWounds` (script Effect) кровь/Pain/`Wounded` чистит, но **не** помечает травмы healing.

**TreatWounds eligibility / assign UI (`System_Wounds_OperationHeal.lua`):** без стеков `Wounded` vanilla `FilterAvailable`/`IsEnabled` не видели пациентов — JAZZ ставит `JazzUnitNeedsTreatWounds` (неполное HP или untreated `Trauma*`), `PatientGetWoundedStacks` = 1 synthetic unit. Vanilla `XTemplates.OperationMerc` Patient branch всё ещё делает `merc:GetStatusEffect("Wounded").stacks` без nil-check → Assert при открытии списка пациентов; `JazzPatchOperationMercPatientWoundsUI` на `DataLoaded`/`ModsReloaded` оборачивает `idContent.OnContextUpdate` и на время update подставляет synthetic `{stacks}` (из `PatientGetWoundedStacks`, иначе `{stacks=0}`).

`Bandage` остаётся CombatAction, а стратегические sector operations используют отдельный runtime. Проверять оба пути и переход между ними.

### Зональные травмы (MED-001)

Публичные ID: `Trauma{Arms|Legs|Ribs|Head|Burn}{Light|Medium|Heavy}`.

| Тир | Специфик | Боль |
| --- | --- | --- |
| Light | нет | **+1** Pain при юзе зоны (`JazzTraumaPainOnZoneUse`) |
| Medium | zone debuff | **+2** Pain при юзе зоны |
| Heavy | жёсткий zone debuff | **+3** Pain при юзе зоны; **+1** Pain/ход за каждую **неиспользованную** heavy-зону (`JazzTraumaHeavyPainRamp`) |

**Hit Pain (отдельно от zone-use):** `Unit:ApplyDamageAndEffects` → `JazzPainOnDamagingHit` — solid hit with **damage > 0** → **+1** Pain (`JazzAddPainStacks`, cap `Pain.max_stacks` **8**). **Graze excluded** (scratch package unchanged). Zone-use / heavy ramp do not share a dedup key with hit Pain (same combat event can still grant both only if the wounded unit also *uses* a zone that turn — different triggers).

Кап `Pain.max_stacks` = **8**. Dedup zone-use: один раз за зону/ход (`unit.jazz_trauma_pain_keys`). Passive heavy: только зоны без zone-use в этом ходу; стаки суммируются по числу unused heavy. **Combat end:** `Pain.RemoveOnEndCombat = true` (как у `Analgesia`) — все стаки боли сбрасываются с окончанием боя; trauma/bleed остаются.

**Zone-use hooks (что считается «юзом»):** Arms/Head — `OnFirearmAttackStart` (атакующий); Legs — `OnCalcMoveModifier`; Ribs/Burn — `OnCalcStartTurnAP`. Heavy-эффекты вызывают те же hooks + `OnEndTurn` → `JazzTraumaHeavyPainRamp`.

Zone specifics (Medium / Heavy params): Arms −20/−50 CTH; Legs +50%/+150% move, no Free Move; Ribs −2/−5 start AP, no Free Move, **no Tired**; Head −15/−40 CTH and −20/−50 sight. Eye folded into Head. Hit wiring: `*shot` OnAdded → `JazzTryRollTraumaFromBodyPart` по **урону этого хита** после брони (`hit.jazz_applied_hp` / `hit.damage`; graze не доходит). Пол **&lt; 20** — нет травмы; ≥ 20 в пустую зону → Light; повтор в ту же зону → +1 тир; ≥ **50%** MaxHP → не ниже Heavy. Голова без отдельного d100. **Armor trauma soft-mitigation (pierced path):** `JazzGetTraumaArmorChanceFactor` больше не режет ролл — броня уже уменьшила `damage`. **BAT (unpierced):** `JazzTryBehindArmorTrauma` from `ApplyDamageAndEffects` — Light/rarely Medium, no bleed; Pain via hit hook when residual damage > 0, else `JazzAddPainStacks(1)` on full absorb. **Grazing / царапина:** no trauma / BAT / `*shot` / Medium+ bleed / **no hit Pain**; `JazzTryRollBleedFromGraze` — **15%** → только `Bleeding`. Downed/knockout merc: `OnMsg.UnitDowned` → идемпотентный `JazzApplyDownedHeavyTrauma`; compatibility wrapper `JazzApplyKnockoutTraumaPackage` делегирует туда же. Burn: `Burning` OnRemoved → `TraumaBurnLight`. Icons: `Icons/StatusEffects/Trauma*.png`.

**Прогресс / UI:** при apply ставится `next_check_time` (CampaignTime). Интервалы (untreated): Light **8** ч (Burn **12**), Medium **24** (Burn **36**), Heavy **48** (Burn **72**). `OnMsg.NewHour` → `JazzTraumaProgressOnNewHour` **догоняет** все due-проверки (`while CampaignTime >= next_t`, кап **96**); следующий таймер = **due + interval**, не конец скипа. Ролл improve/worsen/stay (`JazzTraumaProgressChances`: Light **55/10**, Medium **20/25**, Heavy **8/0**). **После полевой операции** (`PatientAddHealWoundProgress` / TreatWounds): `JazzMarkUnitTraumasHealing` → `jazz_healing=1` на каждой `Trauma*`; interval **×0.5** (floor **2** ч); improve **100%** (гарантированный step-down через `JazzDowngradeTrauma`: Light clear / Medium→Light / Heavy→Medium); worsen **0**. Флаг сохраняется при downgrade тира. `Trauma*` — `object_class` / parent `JazzTraumaEffect` (`Code/System_JazzTraumaEffect.lua`); combat-badge INFO binds `<Description>` → `ResolveValue("Description")` → `JazzFormatTraumaStatusDescription` (effect body + one progress line + healing/untreated flavor). `GetDescription` returns **raw** preset T only: PropertyObject save uses it (`TToLuaCode` asserts `not THasArgs`), and the formatted tooltip contains `T{hours=…}` / TConcat. Base body via `JazzTraumaRawDescription` with a re-entry guard (avoids «Missing text» + duplicated progress). Same ResolveValue-vs-GetDescription split on `Jazz_Perk_OfficerAura` / `Influence`. Полный hospital clear / Medical-quality tiers — MED-002.

**Satellite HP regen:** vanilla `UnitData:Tick` adds `const.Satellite.NaturalHealPerTick` / `PatientHealPerTick` every `Satellite.Tick` (**15** мин) → Natural **4** HP/ч, Patient **20** HP/ч. JAZZ overrides `UnitData:Tick` in `Systems_Medicine.lua`: те же ConstDef числа читаются как **HP/час** через аккумулятор (`jazz_sat_hp_heal_progress`) → Natural **~1** HP/ч, Patient **~5** HP/ч; R&R по-прежнему × `RandRActivityHealingMultiplier` (**2**). Один путь — без параллельного NewHour-heal.

**Hotbar medicine:** all treat stacks are `JazzStackableMedicine` (1 use = −1 `Amount`): `JAZZ_Bandage` **30**, `JAZZ_Morphine` **10**, Small Medkit/`FirstAidKit` **5**, Medium Medkit/`Medkit` **10**, Large Medkit/`Reanimationsset` **15**. `JazzBandage` (one action: spend `Min(bleed stacks, bandages)` and apply −1 tier that many times, AP 1000); kit `Bandage` via `JazzGetEquippedKitMedicine` / `GetUnitEquippedMedicine` (excludes field bandage/morphine). `JazzBandage` / `JazzMorphine` `Run` → `SetActionCommand("Bandage", …)` into `g_Classes.Unit.Bandage` wrap (`Systems_Medicine.lua`): same vanilla `Unit:Bandage` crouch/`nw_Bandaging_*` Start→Idle path, then a short `CombatBandage`-style Idle hold + one-shot apply (`JazzApplyBandageAction` / `JazzApplyMorphineAction`) and `EndCombatBandage`-style exit — not kit `Halt()` channeling. Melee UI hooks (`CanBandageUI`, `Targeting_Melee` id-spoof→`Bandage`, Confirm) resolve engine globals via `_G` metatable (`lG`) — bare `rawget(_G, "CanBandageUI")` is always nil in JA3 and previously skipped install (morphine could not click downed allies). **Morphine** downed: `EvalTarget` allows downed (not Pain-only); apply = Analgesia + consume + `SetCommand("DownedRally")` with no medic/medicine (vanilla get-up). Field path skips `BandageInCombat` when rallying. Wrap rebinds by function identity on `ClassesBuilt`/`ModsReloaded`; install must not call bare `debug.getinfo` (nil in JA3 → aborted before Bandage rebind → silent field anim). No Meds-refill charges on kits. Targeting: `JazzGetFieldBandageTargets` / `JazzGetMorphineTargets`; vanilla `GetBandageTargets` wrapped for Medium/Heavy bleed. **Free-aim UX:** vanilla `CombatActionAttackStart` excludes only `id=="Bandage"` from the melee «no enemies → Free Aim» confirm; `JazzBandage`/`JazzMorphine` set `RequireTargets = true` (+ AttackStart hook) so ally medicine opens `IModeCombatMelee` without that prompt. **Melee UI:** vanilla `Targeting_UnitInMelee` / `CanBandageUI` / healing cursor hardcode `Bandage`; Jazz wraps targeting (spoof id only inside targeting), `CanBandageUI`, `UpdateCursorImage`, `IModeCombatMelee:SetTarget` (skip `CanAttack` eject — ActionType Other always fails), and Confirm/`StartMoveAndAttack`. Self or already-in-melee-range treat **skips Move entirely** (no `goto_pos`): returning current `GetPassSlab` still triggered a one-tile Move when visual pos was >½ slab from slab center; portrait `GetClosestMeleeRangePos` is ignored unless approach is required. Kit `CanBandageUI` FullHP also accepts all Jazz bleed tiers. Intentional attack free-aim unchanged. Legs `TargetBodyPart.applied_effect` = `Legsshot`. `Wounded` companion: `HpLossToAddStack=999999`. MedicalInventory floor: `Max(3, (Medical-20)/20)`.

**Kit thresholds and effect (MED-003):** Medical gates Small **30** / Medium **50** / Large **80**. Heal modifiers **+0 / +50 / +100%**. All three clear **all** bleeding. Each kit marks **one** unhealed Trauma* with `jazz_healing`: Small → Light only; Medium → Medium or Light; Large → any. All kits apply **Analgesia** (pain), clear **WoundInfected**, and can rally downed. `GetBandaged` / kit targeting also allow Pain, infection, and eligible trauma at full HP.

**Hire starting medicine (MED-003 REQ-015…020):** `jazz-units` Equipment leaves (Mercs/Ernie/AME). Medical **&lt; 20** → `JAZZ_Bandage` only. Kits by usable Medical (≥30/50/80); Doctors/`AMERole=Medic` always ≥ Small on every leaf; non-Doctors need Medical **&gt; 30** and not every preset; AME Small only. Bandages 1–2 floor (scale to 10; Doctors up to 30 spread). Morphine: `Tier=Veteran` ×1 if Medical ≥ 20; Doctors up to 10 spread. Apply/audit: `_apply_merc_med_loot_redistribute.py` / `_audit_merc_med_loot_redistribute.py`.

**Legion field medicine (MED-003 REQ-021…023):** class inventories from `recipes.json` `class_tier`. **T2:** Bandage **1–2**. **T3:** Morphine ×1 at **30%** `generate_chance`. **Medic** (`Bonemaker_Inventory`): Bandage **1–10**, Morphine **0–3**, plus Small kit×5 and Medium **5%**. T1/T4 non-medic: no field bandage/morphine. Generator + `_apply_legion_med_loot_redistribute.py` / `_audit_legion_med_loot_redistribute.py`.

## Grit и временное здоровье

**JAZZ-MED-001:** на старте боя Temp HP grit (~25% Health) **не выдаётся**. Max HP снова = **100% Health** (`GetInitialMaxHitPoints`, как vanilla; villains — `LieutenantHpMod`). Раньше JAZZ держал базу на 75% под grit-подушку — после снятия grit это оставляло дыру −25%; закрыто. Перк `TrueGrit` не связан с отключённым CombatStart grit.

## Will Points и подавление

JAZZ добавляет unit attribute `Will` и derived `WillPoints`/`MaxWillPoints`. Взрывы и suppressive fire уменьшают Will и переводят цель по уровням подавления вплоть до `Pinned`. `WillPointsBar.lua` обновляет UI на `CombatEnd` и `TurnEnd` и при runtime-изменениях состояния.

### Уровни и контратака (JAZZ-COMBAT-003)

| Эффект | Смысл | CTH атакующего | Контратака (`Unit:Retaliate`) | Lightning Reaction (base 50%) |
| --- | --- | --- | --- | --- |
| `suppressionLight` | Обстрелян | −10 | ×90% шанс срабатывания | ×90% → **45%** |
| `suppressionMedium` | Под огнем | −20 | ×80% | ×80% → **40%** |
| `suppressionHeavy` | Под плотным огнем | −30 | ×70% | ×70% → **35%** |
| `suppressionHeavy2` | Подавлен | −50 | ×60% | ×60% → **30%** |
| `suppressionPinned` | Прижат | −70 | **нет** (0%) | **0%** |

CTH-модификатор `Suppression` применяется на любой дистанции (в т.ч. opportunity / retaliation), не только дальше 5 клеток. При переходе в `suppressionPinned` и пока статус активен снимаются подготовленные атаки: обычный и постоянный пулемётный Overwatch, Pin Down и Bombard (`Jazz_StripPinnedPreparedAttacks` + gate в OW provoke); более слабые ступени их не снимают.

**Save caveat:** vanilla `CharacterEffect:__toluacode` emits `PlaceCharacterEffect('Id', )` when the effect has no non-default props (typical for fresh mid-combat `suppressionPinned`). That is invalid Lua and blocks load. JAZZ `Code/Save_CharacterEffectSerialize.lua` writes `{}` instead and sanitizes via `string.gsub` on the session blob (often **pstr**, not `type()=="string"`) on load.

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