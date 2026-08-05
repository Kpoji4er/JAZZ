# Бой, CTH и боевые действия

## Связанные specs

- `JAZZ-HOTFIX-001` — устранение runtime/UI assert-ошибок без изменения формул CTH и баланса.

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

- `Code/AccuracyRangeCTH.lua` — общее fixed-point ядро CTH, дальности, оптики и отдачи;
- `Code/CombatActions.lua` — действия юнитов, включая Run and Gun;
- `Code/ExecFirearmAttacks.lua` — выполнение firearm attack и последовательность выстрелов;
- `Code/IModeCombatAreaAim.lua` — UI-режим зонального прицеливания;
- `Code/CrossHairUI.lua` — crosshair, разбивка модификаторов и отображение CTH;
- `Code/CombatBadge_DeathRoll.lua` — состояние цели, LOS/LOF, боевые предупреждения, счётчики; critical icons у ника + party status parity helpers;
- `Code/UnitPropertiesStats.lua` — дополнительные характеристики, используемые боевыми расчётами;
- `Code/Camera.lua` — zoom + restore tac pitch/control после боя и ванильных Max-setpiece (иначе угол может «залипнуть» до save/load);
- generated `CombatAction` и `CTHModifier` ModItems — данные действий и модификаторов.

## Формула попадания в текущем runtime

Огнестрельный `Unit:CalcChanceToHit` строит два канала навыка:

```text
snap_raw      = (Dexterity × 4 + Marksmanship + Level × 5) / 6
precision_raw = (Marksmanship × 4 + Dexterity + Level × 5) / 6
skill(x)      = 20 + x^1.25 × 0.25
```

Нулевой aim преимущественно использует Dexterity. С ростом `aim_progress` результат монотонно движется к Marksmanship-каналу, а `AimAccuracy` добавляет пользу кликов через нелинейный aim mastery. Стат `Handling` удалён. Для неогнестрельных действий сохраняется прежний совместимый путь.

После cap ядра CTH presets, status effects, component effects, реакции, укрытие и остальные ситуационные поправки преобразуются в именованные fixed-point факторы и применяются одним детерминированным произведением. Физически возможный выстрел ограничивается `2..100%`; невозможная атака возвращает `0%`. Опытный стрелок может получить `100%` по открытой цели в полный рост при полном aim и оптимальной дистанции, но любой применимый штраф снижает этот результат. Полная формула находится в [модели стрельбы и точности](../weapons/accuracy-model.md).

Укрытие (`RangeAttackTargetStanceCover`, owner-soften 2026-08-05): `Cover −45` → factor `×0.55`, `ExposedCover −12` → `×0.88`, crouch/prone без укрытия `−12/−23` → `×0.88/×0.77`; частичное — `InterpolateCoverEffect`. Runtime: preset `CalcValue` → `JAZZ_CTHPercentToFactor` в `Unit:CalcChanceToHit` (firearm pipeline). Проверка: `docs/tools/_calc_cover_cth_gewehr.py`, `_check_cover_params_items.py`.

**Cover-graze (не трогали):** при полном укрытии cover→graze ≈100% — любой CTH-hit становится царапиной (~40% урона). Вместе с miss→graze при низком CTH это даёт частые «чипы», даже когда solid hit почти невозможен. Owner intent был снизить CTH; graze слой оставлен.

## Дальность и кучность в текущем runtime

`JAZZ_CTHGetRangeProfile` совместно использует:

- `WeaponRange` — физический предел;
- `BulletDropRange` — базовую границу эффективной зоны;
- `Grouping` — форму падения после эффективной зоны;
- aim progress и профиль установленной оптики — сдвиг эффективной зоны.

До эффективной границы range factor равен `1`. Затем непрерывная степенная кривая приходит к нулю на физическом пределе; последний ещё возможный выстрел сохраняет общий floor. Оптика не меняет `WeaponRange` и `BulletDropRange`, а сильное увеличение может штрафовать близкую дистанцию.

`GetRangeDamageReduction` использует тот же range profile, но рассчитывает процент сохраняемого урона. Вызывающая сторона передаёт `attacker` и `action`, поэтому `GetMaxAimRange` и реакция `OnUnitGetWeaponRange` участвуют в расчёте фактического damage range.

Результат `GetRangeDamageReduction` ограничен диапазоном `0..100`: дальний выстрел не может увеличить исходный урон выше 100% и не может дать отрицательный урон. `DamageReduction` используется только как подпись строки breakdown, а не как status effect.

## Отдача и специальные действия

`Firearm:GetAttackResults` получает шанс первой пули из общего CTH pipeline, строит один recoil profile и применяет `recoil_retention` к каждой последующей пуле. `PredictCTH` использует тот же профиль. Strength, стойка, сошки/развёртывание, resolved component `Recoil`, `AutoWeapons`, класс оружия и действие входят в effective recoil множителями.

Для non-pellet очередей true-miss LoF после protected-окон уводится нарастающим climb’ом вверх (`JAZZ-WEAPONS-007`, якорь `/400` от `effective_recoil`); hit placement и CTH не меняются. Дробовый `pellet_pack` остаётся пакетным конусом без queue-climb.

`cth_loss_per_shot` и `shots_before_recoil` сохранены как совместимые входы существующих CombatAction, но больше не означают линейное вычитание CTH. Первый задаёт action recoil severity, второй — число дополнительных пуль после первой до начала retention. `AbakanBurst`, `AbakanAutoFire` и `JAZZ_ControllableBurst` защищают вторую пулю; `MGBurstFire` снижает тяжесть отдачи до `0.8` от оружейной; `GrizzlyPerk` дополнительно использует action factor `0.55`; `JAZZ_Fanning` получает собственную severity.

## Данные действий

В snapshot зарегистрировано 53 `CombatAction` (+ medicine split). Базовые семейства переопределены или расширены: `SingleShot`, `BurstFire`, `AutoFire`, `MGBurstFire`, `Buckshot`, `BuckshotBurst`, `AttackShotgun`, `Overwatch`, `PinDown`, `RunAndGun`, `RunAndGun_Carbine`, `MobileShot`, `MeleeAttack`, `Bandage`, `JazzBandage`, `JazzMorphine`, `Unjam`, `MGSetup`, несколько `ThrowGrenade`.

`AttackShotgun` остаётся мета-действием, но использует `AimType = "line"`: его `GetAimParams` делегирует фактическому firing member (`Buckshot`, `BuckshotBurst` или `DoubleBarrel`), и эти действия возвращают line-compatible параметры. Мета-действие открывает `IModeCombatAttack`; передавать его скалярный результат в cone area-aim как таблицу нельзя.

Собственные действия JAZZ включают:

- `JAZZ_ControllableBurst`, `JAZZ_LargeAutoFire`, `JAZZ_MGSuppressionFire`, `JAZZ_Salvo`, `JAZZ_TargetSweep`;
- `JAZZ_DoubleTap`, `JAZZ_Mozambique`, `JAZZ_Fanning`, `JAZZ_Zipper`, `JAZZ_JokerShot`, `JAZZ_Bullseye`;
- `JAZZ_SmgStorm`, `JAZZ_RunAndSMGStorm`, `JAZZ_MobileShotgun`, `JAZZ_ManeuverAR`;
- именные perk-actions `Jazz_Perk_00`, `Jazz_Perk_Buzz`, `Jazz_Perk_Lynx`, `Jazz_Perk_Spider`, `JAZZ_VovaVist`, `GrizzlyPerk`;
- режимы компонентов `FoldStock`, `UnFoldStock`, `FlashlightOn`, `FlashlightOff`;
- уникальные `AbakanBurst`, `AbakanAutoFire`, `DoubleBarrel`, `CancelShotCone`.

Фактическое поведение каждого стрелкового ID, совместимость с классами оружия, AP, пакеты пуль, отдача, подавление, perk hooks и известные расхождения собраны в [справочнике стрелковых Combat Actions](../weapons/combat-actions.md).

Текущее распределение специальных ID по `AvailableAttacks` фиксирует совместимость оружия и исходное намерение роли, но не является окончательной системой прогрессии. Базовые физические режимы остаются у совместимого оружия, классовые техники открываются или улучшаются перками, а именные способности персонажей и уникальные действия оружия образуют отдельный слой.

Перк может влиять не только на доступность кнопки: он вправе менять AP, расход патронов, подавление, выбор целей, удержание отдачи либо явный `PerkFactor`. Его CTH-вклад всегда множительный, применяется ровно один раз и проходит через общий pipeline UI/AI/атаки. Полный контракт одиннадцати классов и их action-групп находится в [ролях классов оружия](../weapons/class-roles.md).

Один только класс оружия не гарантирует AI наличие специального действия: AI обязан проверять совместимость конкретного оружия, реально открытые перки и остальные условия CombatAction.

## Runtime flow

1. UI или AI выбирает `CombatAction` и собирает targeting parameters.
2. Crosshair/area-aim вычисляет доступность, AP, цель, траекторию и модификаторы.
3. `Unit:CalcChanceToHit` строит skill/aim core, range profile и произведение ситуационных факторов.
4. firearm executor формирует последовательность выстрелов; для очередей последующие пули получают recoil/разброс.
5. попадания передаются damage/armor/wound и suppression системам; трассерный маркер ставится отдельно на уровне каждого произведённого выстрела с итоговым CTH больше нуля.
6. UI обновляет боевой badge, CTH breakdown, ammo/reload, overwatch и очереди действий.

## Подавление в CTH и контратака (JAZZ-COMBAT-003)

- ModItem `Suppression`: штрафы атакующего `−10/−20/−30/−50/−70` по tier (`suppressionLight` … `suppressionPinned`) на **любой** дистанции, включая opportunity/retaliation.
- `Unit:Retaliate` (Hotblood / Shatterhand / HaveABlast и др.): при `suppressionPinned` сразу `false` — прижатый не контратакует.

## Lightning Reaction (JAZZ-COMBAT-003)

Канон: `Unit:LightningReactionCheck` в `Code/System_OR_Unit.lua`; `Unit:FirearmAttack` в `Code/CombatActions.lua` выставляет `g_JAZZ_FirearmAttacker` / `g_JAZZ_FirearmAttackArgs` на время `OnFirearmAttackStart`.

- Шанс: параметр `chance` перка, иначе **50%** (`self:Random(100) < chance`).
- Не срабатывает, если атакующий в `Hidden`, или в args есть `stealth_attack` / `stealth_kill_chance > 0` (тихое убийство / stealth attack).
- Как и в vanilla: не на своём ходе команды, не из Prone, не при `ManningEmplacement`.

## Grazing hits (JAZZ-COMBAT-002)

Канон runtime: `Code/System_OR_Weapons.lua` (`JAZZ_CalcMissGrazeChance`, `JAZZ_CalcCoverGrazeChance`, `BaseWeapon:PrecalcDamageAndStatusEffects`), `Code/ExecFirearmAttacks.lua` (`ignore_smoke`), `Code/MeleeWeapon.lua` (thrown knives).

### Только два источника

| Источник | Когда | Формула / правило |
| --- | --- | --- |
| **Miss→graze** | валидный выстрел (`shot_cth > 0`) и proмах | `min(50, floor(50 × ((100 − shot_cth) / 100)²))`; полоса над CTH из **того же** attack roll |
| **Cover→graze** | попадание, цель aware, не Exposed, не aim-shooting, не melee/aoe | `Clamp(MulDivRound(−cover_cth, 100, −Cover_full), 0, 100)` — пропорционально cover CTH bonus (`RangeAttackTargetStanceCover`) |

Опорные точки miss→graze:

| shot_cth | miss_graze % |
| ---: | ---: |
| 100 | 0 |
| 80 | 2 |
| 50 | 12 |
| 30 | 24 |
| 20 | 32 |
| 10 | 40 |

### Снято (больше не даёт grazing)

- плоский near-miss band `+3` / `+6`;
- Fog / DustStorm env (`FogGrazeChance` / `DustStormGrazeChance` = 0, ветки удалены);
- C++ LoF smoke/gas (`ignore_smoke = true` всегда; thrown knives оборачивают `GetLoFData`).

Dust storm может **косвенно** усилить cover-graze только если усиливает cover CTH penalty (`DustStormCoverCTHPenalty`) — это следствие «∝ бонусу укрытия», не отдельный magic graze.

### Эффект и исключения

- урон: `Max(1, damage × GrazingHitDamage / 100)` — JAZZ **40%**;
- нет crit; `hit.effects` очищаются; trauma / BAT / Medium+ bleed не накладываются;
- **лёгкая кровь:** `JazzTryRollBleedFromGraze` — шанс `JazzGrazeLightBleedChance` (**15%**) → только `Bleeding`;
- `IgnoreGrazingHitsWhenFullyAimed` (thermal full aim) игнорирует **только cover-graze**, не miss→graze;
- `IgnoreCoverCtHWhenFullyAimed` → cover-graze 0 (нет cover CTH bonus).

Уровень подтверждения формул: **static**; runtime/human playtest — в evidence `JAZZ-COMBAT-002`.

## Публичные контракты и риски

- IDs `CombatAction` и `CTHModifier` используются generated items, AI и UI.
- `Unit:RunAndGun` заменён после CommonLib; обновление CLib требует ручного merge исправлений.
- Crosshair и area-aim являются изменёнными аналогами крупных vanilla-файлов и чувствительны к обновлению игры.
- Изменение порядка `metadata.lua` может заменить финальную реализацию функции другой копией.
- CTH, recoil и RNG должны оставаться детерминированными в сетевой игре.

## Проверка

- одиночный выстрел без aim и с максимальным aim на ближней, рабочей и дальней дистанции;
- диапазон damage multiplier `0..100` на рабочей, предельной и запредельной дистанции с учётом `attacker`/`action` range modifiers;
- трассерный выстрел по unit-цели: попадание и промах при CTH больше нуля, CTH `0`, jam и серия;
- одинаковое оружие при перекрёстных Dexterity/Marksmanship, уровне и числе aim-кликов;
- MachineGun при разной Strength, стойке, опоре и развёртывании;
- короткая/длинная очередь, первый и последующие выстрелы;
- shotgun/area aim, grenade area, overwatch, PinDown и Run and Gun;
- повреждённое оружие с ухудшенной Grouping;
- совпадение CTH breakdown с фактическим pipeline;
- один и тот же классовый CombatAction без перка, с открывающим перком и с несовместимым оружием; совпадение perk factor в UI, AI и выстреле;
- AI-выполнение тех же действий и сетевой повтор.

## Ограничения и сопровождение

Крупные модули частично происходят из vanilla-кода и должны сравниваться трёхсторонним diff после обновления игры. При изменении формулы, действий или UI одновременно обновлять эту страницу, [модель стрельбы и точности](../weapons/accuracy-model.md), `docs/technical/testing.md`, а при коллизии — `docs/technical/override-matrix.md`. Наблюдаемый current-state контракт фиксируется здесь, а ещё не проверенные в игре условия — в связанной spec.
