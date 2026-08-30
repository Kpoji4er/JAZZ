# Бой, CTH и боевые действия

## Связанные specs

- `JAZZ-HOTFIX-001` — устранение runtime/UI assert-ошибок без изменения формул CTH и баланса.
- `JAZZ-COMBAT-002` — grazing (miss→graze / cover-graze).
- `JAZZ-COMBAT-003` — suppression retaliation / Lightning Reaction / Psycho Will.
- `JAZZ-COMBAT-004` — избыток ядра CTH → crit.
- `JAZZ-WEAPONS-013` — пулемёт: спад после E за 16 клеток, не на весь WeaponRange.
- `JAZZ-COMBAT-009` — Overwatch: ширина от дистанции (якорь BDR; inverse до BDR, пулемёт/ЛП квадрат; полоска на WeaponRange, cap 155°); aim-конус `GetCTHColor` на `CRM_AOETilesMaterial`, не `SetColorModifier`.

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
- `Code/IModeCombatAreaAim.lua` — UI-режим зонального прицеливания; Overwatch/MGSetup/MGRotate: `GetOverwatchConeAngle`, aim-band 50% BDR…`WeaponRange` (не sight), tint `CRM_AOETilesMaterial` (COMBAT-009);
- `Code/CrossHairUI.lua` — crosshair, разбивка модификаторов и отображение CTH;
- `Code/CombatBadge_DeathRoll.lua` — состояние цели, LOS/LOF, боевые предупреждения, счётчики; critical icons у ника + party status parity helpers; снятие CombatBadge с трупов (`JazzHideCombatBadgeForDeadUnit`);
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

Нулевой aim преимущественно использует Dexterity. С ростом `aim_progress` результат монотонно движется к Marksmanship-каналу, а `AimAccuracy` добавляет пользу кликов через нелинейный aim mastery. Стат `Handling` удалён. Для неогнестрельных действий сохраняется прежний совместимый путь: skill + CTH presets + `weapon:GetAccuracy`, затем **после** clamp 0–100 применяются `OnCalcChanceToHit` (`Pain`, `TraumaArms*`, `TraumaHead*`, `Concussion`). Иначе запас точности рукопашной съедал штрафы боли/травм.

После cap ядра CTH presets, status effects, component effects, реакции, укрытие и остальные ситуационные поправки преобразуются в именованные fixed-point факторы и применяются одним детерминированным произведением. `OpportunityAttack` (interrupt / OW): **−30…0** от Dex+Mark+уровень×5; `OpportunityAttackBonusCth` с коллиматора добавляется сверху. Физически возможный выстрел ограничивается `2..100%`; невозможная атака возвращает `0%`. Опытный стрелок может получить `100%` по открытой цели в полный рост при полном aim и оптимальной дистанции, но любой применимый штраф снижает этот результат. Полная формула находится в [модели стрельбы и точности](../weapons/accuracy-model.md).

Укрытие (`RangeAttackTargetStanceCover`, owner-soften 2026-08-05): `Cover −45` → factor `×0.55`, `ExposedCover −12` → `×0.88`, crouch/prone без укрытия `−12/−23` → `×0.88/×0.77`; частичное — `InterpolateCoverEffect`. В пылевой буре (`CheckSightCondition` obscured) к Cover и ExposedCover добавляется **`DustStormCoverCTHPenalty = −40`** (один `ConstDef`; раньше дубли −10/−50). Runtime: preset `CalcValue` → `JAZZ_CTHPercentToFactor` в `Unit:CalcChanceToHit` (firearm pipeline). Проверка: `docs/tools/_calc_cover_cth_gewehr.py`, `_check_cover_params_items.py`.

**Cover-graze:** при полном укрытии cover→graze ≈100% — любой CTH-hit становится царапиной (~40% урона). **Miss→graze** base cap **25%**; в упоре (&lt;8 клеток) cap плавно поднимается до **50%** (скрыто от UI) — меньше «воздушных» промахов вплотную.

## Дальность и кучность в текущем runtime

`JAZZ_CTHGetRangeProfile` совместно использует:

- `WeaponRange` — физический предел;
- `BulletDropRange` — базовую границу эффективной зоны;
- `Grouping` — форму падения после эффективной зоны;
- aim progress и профиль установленной оптики — сдвиг эффективной зоны.

До эффективной границы range factor равен `1`. Затем непрерывная степенная кривая идёт к floor **~25%** на `falloff_end` (для большинства классов это `WeaponRange`; для `MachineGun` / `LightMachineGun` — `min(R, E + 16)`, JAZZ-WEAPONS-013). Дальше до физического предела выстрел остаётся возможным на floor. Оптика не меняет `WeaponRange` и `BulletDropRange`, а сильное увеличение может штрафовать близкую дистанцию.

`GetRangeDamageReduction` использует тот же range profile, но рассчитывает процент сохраняемого урона. Вызывающая сторона передаёт `attacker` и `action`, поэтому `GetMaxAimRange` и реакция `OnUnitGetWeaponRange` участвуют в расчёте фактического damage range.

Результат `GetRangeDamageReduction` ограничен диапазоном `0..100`: дальний выстрел не может увеличить исходный урон выше 100% и не может дать отрицательный урон. `DamageReduction` используется только как подпись строки breakdown, а не как status effect.

## Отдача и специальные действия

`Firearm:GetAttackResults` получает шанс первой пули из общего CTH pipeline, строит один recoil profile и применяет `recoil_retention` к каждой последующей пуле. `PredictCTH` использует тот же профиль. Strength, стойка, сошки/развёртывание, resolved component `Recoil`, `AutoWeapons`, класс оружия и действие входят в effective recoil множителями.

**Без опоры (JAZZ-WEAPONS-012):** для `MachineGun` / `LightMachineGun` без setup/permanent OW / `BipodUnfolded` / prone+bipod первая пуля получает CTH-фактор «Без опоры»: base **−50** / **−25**, масштабируется Силой `×(100−Str)/100` (Str 100 → 0). Одновременно recoil `class_factor` **×2.0** / **×1.5** (вместо прежних 1.35/1.15). Сигнатурный CombatAction `GrizzlyPerk` игнорирует оба штрафа и даёт **2×** длину длинной очереди / **полный** урон / **2×** suppression; обычный `MGBurstFire` у Гризли — нет.

Для non-pellet очередей true-miss LoF после protected-окон уводится нарастающим climb’ом вверх (`JAZZ-WEAPONS-007`, якорь `/400` от `effective_recoil`); hit placement и CTH не меняются. Дробовый `pellet_pack` остаётся пакетным конусом без queue-climb.

**Dump / AI targeting (JAZZ-AI-PERF-003 / PERF-004):** `AIGetAttackTargetingOptions` берёт CTH из `CalcChanceToHit`, без `GetActionResults`/`GetLoFData` (M3 PickBest вис на луче body-part). `AIActionDump` ставит `args.jazz_ai_dump`: `PrepareAttackArgs` и execute `GetAttackResults` не зовут `GetLoFData`; синтетический LoF / miss `stuck_pos`; `step_pos` и fire `anim` (`GetAttackAnim`) заполняются без GetLoFData; `ProjectileFly` без vegetation `Collide`. **Execute hits:** дешёвый луч muzzle/torso — `terrain.IntersectSegment`, первые **3** непроходимые плиты по 2D линии (entity/slab-скала; яму не считать) и другие юниты на сегменте (`SegmentIntersectsSphere`). Чистая линия — в `hits` цель, CTH-попадание наносит урон. Непробиваемый террайн/скала/плита или тело на луче — `stuck`, DumpFire не стреляет. Dump в модель при командном LOS и чистом LoF; личный LOS не обязателен. Игровой Fanning и не-Dump выстрелы — ванильный пайплайн. Перед `collision.Collide` обёртка `Firearm:ProjectileFly` / `FireBullet` поднимает 2D `attack_pos`/`stuck_pos` через `SetTerrainZ` (`Jazz_EnsurePointHasZ`): стоячие юниты часто без Z, JA3Debug иначе ассертит `z != nInvalidZ`.

**LOS vs LoF:** `HasVisibilityTo` (sight: дальность, тьма, дым −70, stealth) и `GetLoFData` / cheap ray (геометрия пули) — разные проверки. Командный LOS (`HasVisibilityTo(team, target)`) даёт право выбрать модель цели; выстрел идёт только если LoF чистый. Личный LOS только бонус к score (`×1.2` в `PickBestAttack`). Движок **может** посчитать LoF без LOS (луч не знает «вижу/не вижу»), но AI обычно не зовёт его: нет team vis → нет цели-модели; dest без `CheckLOS` в DestLos cache → skip `GetLoFData` (PERF-001); Dump targeting CTH без LoF, execute — cheap ray. Дом/стена чаще режут и LOS и LoF; дым режет LOS, LoF сквозь дым в JAZZ есть (без smoke-graze); за дальностью зрения team vis нет — в модель не бьют, даже если геометрический луч был бы чистым.

`cth_loss_per_shot` и `shots_before_recoil` сохранены как совместимые входы существующих CombatAction, но больше не означают линейное вычитание CTH. Первый задаёт action recoil severity, второй — число дополнительных пуль после первой до начала retention. `AbakanBurst`, `AbakanAutoFire` и `JAZZ_ControllableBurst` защищают вторую пулю; обычный `MGBurstFire` использует полный authored `Recoil`; только `GrizzlyPerk` задаёт пулемётную severity `0.8` и затем action factor `0.55`; `JAZZ_Fanning` получает собственную severity. Сигнатура Спайка `BulletHell` имеет **нулевую** action recoil (`effective_recoil = 0`, retention 1): все 15–30 пуль идут с CTH первой; `cth_loss_per_shot` её не возвращает.

## Данные действий

В snapshot зарегистрировано 53 `CombatAction` (+ medicine split). Базовые семейства переопределены или расширены: `SingleShot`, `BurstFire`, `AutoFire`, `MGBurstFire`, `Buckshot`, `BuckshotBurst`, `AttackShotgun`, `Overwatch`, `PinDown`, `RunAndGun`, `RunAndGun_Carbine`, `MobileShot`, `MeleeAttack`, `Bandage`, `JazzBandage`, `JazzMorphine`, `Unjam`, `MGSetup`, несколько `ThrowGrenade`.

`AttackShotgun` остаётся мета-действием, но использует `AimType = "line"`: его `GetAimParams` делегирует фактическому firing member (`Buckshot`, `BuckshotBurst` или `DoubleBarrel`), и эти действия возвращают line-compatible параметры. Мета-действие открывает `IModeCombatAttack`; передавать его скалярный результат в cone area-aim как таблицу нельзя.

Собственные действия JAZZ включают:

- `JAZZ_ControllableBurst`, `JAZZ_LargeAutoFire`, `JAZZ_MGSuppressionFire`, `JAZZ_Salvo`, `JAZZ_TargetSweep`;
- `JAZZ_DoubleTap`, `JAZZ_Mozambique`, `JAZZ_Fanning`, `JAZZ_Zipper`, `JAZZ_JokerShot`, `JAZZ_Bullseye`;
- `JAZZ_SmgStorm`, `JAZZ_RunAndSMGStorm`, `JAZZ_MobileShotgun`, `JAZZ_ManeuverAR`;
- именные perk-actions `Jazz_Perk_00`, `Jazz_Perk_Buzz`, `Jazz_Perk_Lynx`, `Jazz_Perk_Spider`, `JAZZ_VovaVist`, `GrizzlyPerk`;
- режимы компонентов `FoldStock`, `UnFoldStock`, `FlashlightOn`, `FlashlightOff` (JAZZ-UI-002: не hotbar — вторая колонка у иконки оружия в `UIWeaponDisplay`);
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
- `Unit:Retaliate` (Hotblood / Shatterhand / HaveABlast / Killzone и др.): тот же множитель подавления, что у Lightning Reaction (`×90/×80/×70/×60`); при `suppressionPinned` сразу `false` — прижатый не контратакует.
- При наложении `suppressionPinned` его `OnAdded` вызывает `Jazz_StripPinnedPreparedAttacks` (Interrupt + residual `g_Overwatch` / `g_Pindown` / `StationedMachineGun` / bombard) до смены стойки и **повторно** после `SetActionCommand` (гонка со stance/cover). `OnBeginTurn` повторяет strip; Jazz `Unit:BeginTurn` **всегда** interrupt+strip при pinned (раньше PinDown/Bombard ветки могли сохранить prepared); `ProvokeOpportunityAttack_Overwatch` при pinned снимает сектор и не стреляет; `ApplySuppressionStatus` при уже активном pinned снова зовёт strip. Более слабые ступени подготовленные атаки не прерывают.
- `Unjam`: `ShowIn = "CombatActions"`, `group = Default`, SortKey 10. `GetAPCost` = **4…1 AP** от Mechanical (`4 - MulDivRound(Clamp(Mechanical,0,100), 3, 100)`); `MrFixit` сохраняет perk AP. `GetUIState` и `FirearmBase:IsCondition` опираются на `WeaponResource` %, чтобы jam не скрывался ложным `Broken` по stale `Condition`.

## Стационарный пулемёт после load (JAZZ-HOTFIX-004)

Vanilla `Unit:GameInit` может вызвать `EnterEmplacement` до создания `weapon`/visual орудия. JAZZ wrap не делает `SetPos(nil)` и не падает на `obj.weapon.owner`; `LoadGame`/`EnterSector` reseat привязывает ствол, пересчитывает HUD и при `Idle` без permanent overwatch восстанавливает конус `MGTarget`. `GetActiveWeapons` при manning повторяет `Update()`, если ствол ещё nil. `ResolveDefaultFiringModeAction` / `RecalcUIActions` не падают при отсутствии оружия.

`RecalcUIActions` под двухстрочный `CombatActionBar` (`HWrap`): **24** боевых слота, signature на **25** (ваниль 12+13). Сами кнопки — UIAction-пресеты `Action1`–`Action24` плюс `Action25` для signature-strip (`Jazz_RegisterExtraCombatBarSlots`); одного расширения массива недостаточно. Переполнение по-прежнему сворачивает item-skills в `ItemSkills`.

`Firearm:GetBaseAttack` (рядом с `CanAutofire`/`CanBurstfire`): если на стволе `EnableBurst`/`EnableFullAuto` и этих ID нет в preset `AvailableAttacks`, в эффективный список сначала идут `BurstFire` и `AutoFire`. Overwatch (`GetDefaultAttackAction` ungrouped) на M2Carbine / Mini14 с `JAZZ_Autofire` стреляет очередью, не одиночным. Порядок baked-in списков не трогается.

## Lightning Reaction (JAZZ-COMBAT-003)

Канон: `Unit:LightningReactionCheck` в `Code/System_OR_Unit.lua`; `Unit:FirearmAttack` в `Code/CombatActions.lua` выставляет `g_JAZZ_FirearmAttacker` / `g_JAZZ_FirearmAttackArgs` на время `OnFirearmAttackStart`.

- Базовый шанс: параметр `chance` перка, иначе **50%**.
- Подавление цели мягко режет шанс: `Light ×90%` / `Medium ×80%` / `Heavy ×70%` / `Heavy2 ×60%` (при base 50 → **45 / 40 / 35 / 30**). `suppressionPinned` → итоговый chance **0** (без roll).
- Не срабатывает, если атакующий в `Hidden`, или в args есть `stealth_attack` / `stealth_kill_chance > 0` (тихое убийство / stealth attack).
- Как и в vanilla: не на своём ходе команды, не из Prone, не при `ManningEmplacement`.

## Grazing hits (JAZZ-COMBAT-002)

Канон runtime: `Code/System_OR_Weapons.lua` (`JAZZ_CalcMissGrazeCap`, `JAZZ_CalcMissGrazeChance`, `JAZZ_CalcCoverGrazeChance`, `BaseWeapon:PrecalcDamageAndStatusEffects`), `Code/ExecFirearmAttacks.lua` (`ignore_smoke`), `Code/MeleeWeapon.lua` (thrown knives).

### Только два источника

| Источник | Когда | Формула / правило |
| --- | --- | --- |
| **Miss→graze** | валидный выстрел (`shot_cth > 0`) и промах | `cap = JAZZ_CalcMissGrazeCap(dist_tiles)`; `min(cap, floor(cap × ((100 − shot_cth) / 100)²))`; полоса над CTH из **того же** attack roll |
| **Cover→graze** | попадание, цель aware, не Exposed, не aim-shooting, не melee/aoe | `Clamp(MulDivRound(−cover_cth, 100, −Cover_full), 0, 100)` — пропорционально cover CTH bonus (`RangeAttackTargetStanceCover`) |

`JAZZ_CalcMissGrazeCap`: base **25**; при `dist_tiles < 8` линейно к **50** на 0 клетках (`50 − MulDivRound(25, dist, 8)`). UI / ACCURACY % не показывает этот подъём.

Опорные точки miss→graze (**≥8** клеток, cap 25):

| shot_cth | miss_graze % |
| ---: | ---: |
| 100 | 0 |
| 80 | 1 |
| 50 | 6 |
| 30 | 12 |
| 20 | 16 |
| 10 | 20 |

В упоре (**0** клеток, cap 50): CTH 20 → **32%**, CTH 50 → **12%**, CTH 10 → **40%** (как старый кап).

### Снято (больше не даёт grazing)

- плоский near-miss band `+3` / `+6`;
- Fog / DustStorm env (`FogGrazeChance` / `DustStormGrazeChance` = 0, ветки удалены);
- C++ LoF smoke/gas (`ignore_smoke = true` всегда; thrown knives оборачивают `GetLoFData`).

Dust storm может **косвенно** усилить cover-graze: obscured цель получает extra cover CTH **`DustStormCoverCTHPenalty = −40`** (складывается с Cover −45 / Exposed −12) — graze растёт потому что cover bonus больше, не отдельный env-graze.

### Эффект и исключения

- урон: `Max(1, damage × GrazingHitDamage / 100)` — JAZZ **40%**;
- нет crit; `hit.effects` очищаются; trauma / BAT / Medium+ bleed не накладываются;
- **лёгкая кровь:** `JazzTryRollBleedFromGraze` — шанс `JazzGrazeLightBleedChance` (**15%**) → только `Bleeding`;
- `IgnoreGrazingHitsWhenFullyAimed` (thermal full aim) игнорирует **только cover-graze**, не miss→graze;
- `IgnoreCoverCtHWhenFullyAimed` → cover-graze 0 (нет cover CTH bonus).

Уровень подтверждения формул: **static**; runtime/human playtest — в evidence `JAZZ-COMBAT-002`.

## Избыток ядра → крит (JAZZ-COMBAT-004)

Канон: `Unit:CalcCritChance` + `JAZZ_CTHGetShooterCore` в `Code/System_OR_Unit.lua` / `AccuracyRangeCTH.lua`.

- `uncapped_core` = skill/aim ядро **до** `Clamp(..., 100)` и **до** situational factors (укрытие, видимость, …).
- `core_overflow = Max(0, Round(uncapped_core) − 100)` → **+1:1** к crit chance.
- Попадание строится из капнутого ядра × factors; запас не «съедает» укрытие.
- Итоговый crit `Clamp(0, 100)`. Opportunity / `guaranteed_noncrit` → 0; grazing по-прежнему не критует.
- Диагностика: `args.jazz_cth.uncapped_core` / `core_overflow` после `CalcChanceToHit`.

Сильные Marksmanship + высокий `AimAccuracy` на полном aim часто дают заметный overflow (десятки пунктов) и упираются в кап крита — ожидаемо.

## Публичные контракты и риски

- IDs `CombatAction` и `CTHModifier` используются generated items, AI и UI.
- `Unit:RunAndGun` заменён после CommonLib; обновление CLib требует ручного merge исправлений.
- Crosshair и area-aim являются изменёнными аналогами крупных vanilla-файлов и чувствительны к обновлению игры.
- Изменение порядка `metadata.lua` может заменить финальную реализацию функции другой копией.
- CTH, recoil и RNG должны оставаться детерминированными в сетевой игре.

## Overwatch / MGSetup cone (JAZZ-COMBAT-009)

`Firearm:GetOverwatchConeAngle(d)` — authored `OverwatchAngle` на BDR. Ближе BDR: `authored × BDR / d`; пулемёт и ЛП ещё раз `× BDR / d` (иначе наземный клин `CreateAOETilesSector` почти не толстеет). Дальше BDR — lerp к class strip на `WeaponRange`. Clamp `[2°, 155°]`. `MinRange` = 50% BDR для всех стволов, включая M2. Aim UI берёт min/max из `GetOverwatchConeParam`, не из sight-clamp `GetAimParams`. После confirm `Unit:OnOverwatchPlaced` / `OverwatchChanged` переписывает `g_Overwatch.cone_angle` и `dist` от поставленной точки — ванильный `GetAimParams` без target писал бы сырой `OverwatchAngle`.

Цвет aim-конуса **только пока целишься**: после `CreateAOETilesSector` красятся поля `CRM_AOETilesMaterial` в `GetCTHColor(preview)` (белый ≥100 / синий ≥85 / зелёный ≥60 / жёлтый ≥40 / оранжевый ≥20 / красный >0 / чёрный 0). Поставленный сектор не тинтим — ванильный Confirm / Deployed / Activated (сплошная заливка CTH на уже стоящем OW была косяком). Preview CTH — `JazzOwPreviewCTH`: виртуальный Standing/Torso, `aim` из `GetOverwatchAttacksAndAim`, без укрытия, без attacker CTH-дебафов и без Opportunity Attack (боевой interrupt OA оставляет). Якорь на `SnapToPassSlab`; чёрный только если нет LoS ни на одной пробе **и** CTH=0.

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
