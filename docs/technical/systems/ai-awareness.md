# Тактический AI и awareness

## Назначение

Эта страница описывает текущий runtime-контракт тактического AI: как vanilla JA3 выбирает поведение, позицию, цель и действие; какие части этого конвейера заменяет JAZZ; какие archetype, policies и actions реально настроены в `jazz-units`; как awareness передаёт AI известные и предполагаемые цели.

Пользовательское написание `AIBehaviour` здесь относится к слою поведения. В API игры класс называется `AIBehavior`, vanilla-файл — `Lua/Tactical/AIBehaviors.lua`, а JAZZ-файл — `Code/AIBehaviours.lua`.

## Связанные specs

- [JAZZ-AI-001](../../specs/active/JAZZ-AI-001.md) — удаление заимствованного policy-слоя и перевод `GuardArea` на `AIPolicyTakeCover`.
- [JAZZ-QOL-001](../../specs/active/JAZZ-QOL-001.md) — auto fast-forward скрытых AI и свободная камера на чужом ходе.

## Граница и доказательная база

Документ составлен статическим сравнением:

- `<JA3_ROOT>\ModTools\Src\Lua\Tactical\AIBase.lua`;
- `<JA3_ROOT>\ModTools\Src\Lua\Tactical\AIBehaviors.lua`;
- `<JA3_ROOT>\ModTools\Src\Lua\Tactical\AIActions.lua`;
- `<JA3_ROOT>\ModTools\Src\Lua\Tactical\CombatAI.lua`;
- `<JA3_ROOT>\ModTools\Src\Lua\Tactical\UnitAwareness.lua`;
- `<JA3_ROOT>\ModTools\Src\Lua\Tactical\Unit.lua` и `CombatCamera.lua`;
- `<JA3_ROOT>\ModTools\Src\Lua\ClassDefs\ClassDef-AI.generated.lua`;
- загружаемых AI-файлов `jazz` и generated-конфигурации `jazz-units`.

Проверка не является runtime-профилированием боя. Раздел «Известные риски» отделяет подтверждённое устройство кода от дефектов, найденных статически.

## Владение и слои

| Слой | Владелец | Ответственность |
| --- | --- | --- |
| Vanilla | JA3 | Базовые классы, turn controller, выбор behavior, pathing, policies, actions, awareness |
| CommonLib | `JA3_CommonLib` | Исправления отдельных AI-функций до загрузки JAZZ |
| Core | `jazz` | Замены алгоритмов в `AiActions`, `CombatAI`, `AIPolicy`, `UnitAwareness` |
| Units | `jazz-units` | Keywords, 33 `AIArchetype`, `UnitData`, инвентарь и привязка юнита к archetype |
| Maps | `jazz-maps` | Геометрия, размещение, patrol/guard объекты и tactical context; `Code/AIMechanism.lua` лежит на диске, но metadata его не загружает |
| Assets | `jazz_assets` | Entity и visual state оружия/юнитов; тактические решения не определяет |

Основной код не должен переносить generated `AIArchetype` из `jazz-units`: владелец данных — пакет units.

## Активные файлы и порядок JAZZ

`jazz/metadata.lua` загружает AI-слой в следующем порядке:

1. `Code/UnitAwareness.lua`;
2. `Code/InfiniteLoopFix.lua`;
3. `Code/AIBehaviours.lua`;
4. `Code/AiFastForward.lua` (JAZZ-QOL-001);
5. `Code/AiActions.lua`;
6. `Code/CombatAI.lua`;
7. `Code/AiAction_ThrowFlare.lua`;
8. `Code/AIPolicy.lua`;
9. `Code/PushUnitAlert.lua`.

Load-state важен: одинаковое глобальное имя предоставляет последняя загруженная реализация. `PushUnitAlert.lua` пуст. `Code/AIPolicyAttackAP.lua` тоже пуст и metadata его не загружает; активный класс `AIPolicyAttackAP` переопределён в `Code/AIPolicy.lua`.

### QoL: auto fast-forward и свободная камера (JAZZ-QOL-001)

`Code/AiFastForward.lua`:

- `JAZZ_UpdateAutoFastForward(unit, phase)` — по mod option `AutoFastForward` (`Off` / `Running` / `Always`, default `Always`) ставит `g_FastForwardGameSpeed` в Fast/Normal через `HasVisibilityTo(GetPoVTeam(), unit)`; Fast только если PoV не видит юнита; скорость меняется только при смене значения.
- `const.Combat.FastForwardGameSpeed` = 300% (vanilla 200%).
- `EnemyTurnFreeCamera` (default on): `LockCameraMovement` no-op на чужом ходе / при `g_AIExecutionController`; на `ExecutionControllerActivate` снимает movement-locks. Action camera не отключается.

## Модель vanilla AI

### `AIArchetype`

Archetype — конфигурация тактической роли, а не исполняемый алгоритм. Он задаёт:

- список `Behaviors`;
- предпочтительные стойки и радиус поиска позиции;
- `OptLocPolicies` и `TargetingPolicies`;
- базовые веса атаки и движения;
- политику смены цели `TargetChangePolicy`;
- fallback (`revert` или `overwatch`);
- доступные `SignatureActions`.

Keywords юнита фильтруют behaviors и actions. Archetype связывает один `UnitData` с общим набором тактических правил.

### `AIBehavior`

Behavior управляет одной попыткой хода юнита. Базовый класс содержит keywords, score, phase хода, вес оптимальной позиции, end-turn policies, signature actions и вероятность укрыться. Основные vanilla-типы:

- `StandardAI` — обычный позиционно-атакующий ход;
- `RetreatAI` — отход;
- `PositioningAI` — выход к заданной позиции;
- `HoldPositionAI` — удержание;
- `ApproachInteractableAI` — движение к interactable;
- `CustomAI` — сценарно заданная логика.

`Behavior:Think()` строит намерение: destination, движение, стойку и attack context. `Behavior:Play()` исполняет подготовленное намерение.

### `AIPositioningPolicy` и `AITargetingPolicy`

Positioning policy оценивает destination. Для каждой позиции `AIScoreDest` суммирует вклад policies с учётом их `Weight`.

- `Required = true` и неположительная оценка отбрасывают позицию.
- `optimal_location` применяется при выборе тактически лучшей точки.
- `end_of_turn` применяется к точке завершения хода.
- fire, gas, bombardment, bias markers и запрещённые voxels добавляют отдельные ограничения/модификаторы.

Targeting policy добавляет вес цели: здоровье, оружие, роль и другие свойства. Итоговая оценка цели соединяется с прогнозом урона/попадания.

### `AISignatureAction` и обычная атака

Vanilla `AISignatureAction` задаёт notification, keywords и ограничения `AvailableInState`/`ForbiddenInState`. Выбор проходит три стадии:

1. `PrecalcAction()` строит данные конкретного действия;
2. `IsAvailable()`/`MatchUnit()` проверяет состояние, AP, оружие и keywords;
3. `Execute()` запускает выбранное действие.

К стандартным действиям относятся basic attack, grenade, bandage, stim, charge, mobile shot, pin down, shoot landmine, MG setup/burst, heavy weapon и зональные атаки.

### `CombatAI`

`CombatAI.lua` — вычислительное ядро. Оно создаёт `ai_context`, строит path/LOS cache, перечисляет reachable voxels, оценивает позиции, прогнозирует damage и friendly fire, выбирает target/action и передаёт результат behavior для исполнения.

`ai_context` живёт в рамках AI-хода. Это расчётное состояние, а не публичная схема сохранения.

### Awareness

`UnitAwareness.lua` определяет, кого команда считает видимым, известным или предполагаемым противником, хранит last known position, обрабатывает noise, suspicion и alerts. Combat AI не «видит карту сам»: он получает набор доступных целей и точек из awareness/team visibility.

## Vanilla-конвейер одного хода

1. Vanilla `Unit:StartAI()` перезаряжает/подготавливает оружие и выбирает `AIArchetype`.
2. Behaviors archetype фильтруются по keywords, bias и условиям `MatchUnit()`.
3. Priority может принудительно выбрать behavior; иначе выполняется взвешенный детерминированный выбор через `InteractionRand("AIBehavior", unit)`.
4. Создаётся `ai_context`, затем вызывается `behavior:OnStart()`.
5. `Think()` перечисляет destinations, строит пути и оценивает optimal/end-turn positions через `AIScoreDest()`.
6. Для позиций вычисляются доступные цели, атаки, aim levels, прогноз damage и targeting policies.
7. Кандидаты в пределах `const.AIDecisionThreshold` от лучшей оценки выбираются детерминированно через `InteractionRand`.
8. Combat turn controller в `CombatCamera.lua` вызывает `AIExecuteUnitBehavior()` и `behavior:Play()`.
9. Signature action проходит `PrecalcAction → IsAvailable → Execute`; затем возможны basic attacks и fallback cover/overwatch.
10. При `TargetChangePolicy = "restart"` юнит остаётся в очереди, пересчитывает context и продолжает, если ещё может действовать.
11. Damage, sight, noise и завершение боя обновляют awareness для следующих решений.

Turn controller делит юнитов на `Early`, `Normal` и `Late`; угрожаемое/изменившееся состояние может перенести исполнение на позднюю фазу.

## Что меняет JAZZ

### `AIBehavior`

`Code/AIBehaviours.lua` заменяет только базовый `AIBehavior:OnStart()`:

- при непустом `VoiceResponse` воспроизводит реплику;
- затем вызывает `OnActivate(unit)`.

Выбор behavior и `Unit:StartAI()` остаются vanilla. Поскольку отдельные vanilla behaviors также проигрывают `VoiceResponse`, конфигурация `PositioningAI` и `HoldPositionAI` может дать повторную реплику; это статический риск, который надо подтверждать в игре.

### Policies

| Policy | Текущее изменение JAZZ |
| --- | --- |
| `AIPolicyAttackAP` | Полная замена класса: 120 при AP выше стоимости лучшей атаки, 110 при равенстве; fallback 100/90 по default attack cost |
| `AIPolicyTakeCover` | Укрытие оценивается по реальному percentage: none 0, low 40, high 100; слабое перекрытие получает резкое снижение |
| `AIPolicyFlanking` | Учитывает планируемые позиции союзников и непрерывный `GetFlankThreat`; результат кэшируется в context |
| `AIPolicyProximity` | Исправляет minimum/average accounting, добавляет этаж и indoor/outdoor; при менее чем трёх подходящих units не даёт оценки |
| `AIPolicyHighGround` | Сохраняет высотный бонус и штрафует скопление живых союзников на том же уровне в радиусе шести тайлов |
| `AIPolicyIndoorsOutdoors` | Возвращает числовой вес при совпадении типа позиции |
| `AIPolicyAvoidDeathZones` | Новая отрицательная оценка рядом с погибшими союзниками, по умолчанию в радиусе пяти тайлов |
| `AITargetingEnemyWill` | Новая targeting policy для целей выше/ниже заданного процента Will |

Generated archetype `GuardArea` использует `AIPolicyTakeCover` с `visibility_mode = "team"` и в `CustomAI.EndTurnPolicies`, и в `OptLocPolicies`. Поэтому удерживающий область юнит оценивает укрытие по видимости всей команды, не вводя отдельный policy-класс.

Некоторые policy-методы раньше возвращали значение уже с `self.Weight`, после чего `AIScoreDest()` ещё раз умножал на `Weight / 100` (квадратично). JAZZ-AI-002: Flanking / HighGround / IndoorsOutdoors возвращают raw (канон ×100 при Weight=100); единственный множитель — `AIScoreDest`.

### `AIActions`

`Code/AiActions.lua` меняет подготовку и исполнение действий:

- `AIActionThrowGrenade:PrecalcAction()` перебирает десять grenade action slots и принимает grenade, ordnance, flare, Molotov и совместимые grenade items;
- target points включают last attack position; smoke/fire/gas оцениваются через прогноз области распространения, обычные боеприпасы — через ожидаемые hits;
- `AIReloadWeapons()` чинит jam активного оружия, поднимает `Mechanical` на 1, пополняет AI-магазины и поддерживает `AmmoInventory` (всегда валидный `ammo` object перед reload);
- `AICalcAttacksAndAim()` распределяет оставшиеся AP по aim levels к CTH 100, списывая `aim_cost` один раз на шаг;
- `AIExecuteUnitBehavior()` пропускает `Unconscious` и `suppressionPinned`; auto fast-forward делегирован в `JAZZ_UpdateAutoFastForward` (`Code/AiFastForward.lua`);
- **`AIPlayAttacks()` (JAZZ-AI-002):** модель **Commit → Dump → Disengage/BunkerDown** — локальный dump до `SoftDumpCap=4` / `max_attacks`, одно действие за step с retarget; `"restart"` только target-change / MGPack / explicit status; без leftover-Think restart;
- **Disengage/BunkerDown:** optional один cover-move, затем TakeCover → crouch-low → prone-open → PrefStance (`GetStanceToStanceAP`); `TryChangeStance` — alias на bunker; `AITakeCover` no-op если `context.bunker_used`;
- `AIActionMGSetup` выбирает crouch при хорошем low cover, иначе prone, и умеет развернуть/свернуть уже установленный MG;
- `AIGetAttackTargetingOptions()` симулирует body parts и взвешивает их по текущему CTH;
- `AISignatureAction:MatchUnit()` читает `GameState[state]`.

Важно: vanilla `AIReloadWeapons()` уже создаёт подходящие боеприпасы для non-merc AI и заполняет магазин. JAZZ расширяет этот механизм jam-repair и `AmmoInventory`; «бесконечные патроны AI» не являются исключительно механикой мода.

`Code/AiAction_ThrowFlare.lua` добавляет `AIActionThrowFlare`: действие доступно ночью или под землёй; `TargetLastAttackPos` уважается; noise sources всегда могут добавлять точки (с инициализацией `target_pts`).

### `CombatAI`

JAZZ заменяет большую часть вычислительного слоя:

- `PredictCTH()` и `GetCTHByAimLevels()` прогнозируют шанс попадания по aim;
- `PickBestAttack()` сравнивает firearm modes и aim levels по ожидаемому урону на AP; выбор top-K через `InteractionRand`; допускает `total_cost <= AP`;
- лучший mode записывается в context как `best_attack`, вместе с `attack_AP_reserved` и эффективной дальностью;
- effective range ограничивается sight radius в `Dust`, `FireStorm`, `Underground`, ночью и в тумане;
- `AIFindDestinations()` считает team visibility и резервирует SoftDisengageTiles (2 AP-тайла) под post-attack bunker/cover-move;
- `AIPrecalcDamageScore()` объединяет текущий CTH, лучшую атаку/aim, targeting policies и hysteresis позиции; friendly fire имеет нулевой score modifier и отбрасывает вариант;
- `AISelectAction()` выбирает по весу конкретного кандидата, а не по суммарному весу списка;
- low-cover destination преобразуется в crouch с вычетом AP на стойку;
- при отсутствии найденной destination AI остаётся на текущей позиции;
- `AIGetWeaponCheckRange()` использует `WeaponRange - 1`;
- scout, cone/AOE, interactable и custom behavior calculations также заменены локальными версиями.

Policies Flanking / HighGround / IndoorsOutdoors возвращают raw score без встроенного `Weight` (множитель только в `AIScoreDest`), чтобы Weight не был квадратичным.

Стабилизация позиции использует два механизма: переход стоит делать только при выигрыше примерно от 10%, а предыдущая destination сохраняется, если остаётся в пределах `const.AIDecisionThreshold` от лучшей.

`GetCTHByAimLevels()` вызывает тот же `Unit:CalcChanceToHit`, что UI и фактическая атака. `PredictCTH()` больше не вычитает линейный recoil: он строит общий `JAZZ_CTHGetRecoilProfile` и суммирует `JAZZ_CTHGetBulletChance` для той же последовательности пуль. Поэтому отдельная правка AI-точности должна считаться изменением общего CTH-контракта.

### Awareness и alert

JAZZ не заменяет весь vanilla awareness-файл. Активный `Code/UnitAwareness.lua` определяет handlers `ConflictEnd`, `TurnStart`, `ExplorationTick` и заменяет `PushUnitAlert()`, `AIUpdateScoutLocation()` и `UpdateSuspicion()`; остальные alert/propagation функции остаются vanilla.

Основные изменения:

- после конфликта sector получает базовый heat 20 плюс 10% `CombatHeat`;
- heat распространяется в region и соседние сектора: 40% в первое кольцо и 10% во второе;
- поражение/отступление добавляет дополнительный heat;
- при `Heat + CombatHeat > 500` враги переводятся в suspicious и получают последнюю известную enemy/noise position;
- шум под дождём имеет изменённый радиус и увеличивает `CombatHeat` за затронутых units;
- suspicion учитывает LOS, дистанцию, направление взгляда, `Hidden`, prone, `Darkness`, projector и decay;
- exploration path выставляет локальный `raisedAlarm = true`, а turn-start path этого не делает.

В файле значения `SuspicionThreshold`, внешней дистанции и night tick rate вычисляются локально один раз при загрузке. Поэтому смена `raisedAlarm` после загрузки не меняет уже рассчитанные 160/4, а night rate отражает состояние `GameState.Night` в момент загрузки, а не обязательно текущую погоду/время.

## Как AI настроен в `jazz-units`

### Keywords

`jazz-units/Code/AIKeywords.lua` задаёт 17 значений:

`Melee`, `CQB`, `Soldier`, `Marksman`, `Sniper`, `Leader`, `MG`, `Control`, `Explosives`, `Ordnance`, `Smoke`, `Flank`, `MobileShot`, `RunAndGun`, `Stim`, `Nova`, `Heal`.

Keywords — capability tags. Они не запускают действие сами: behavior/action должны одновременно присутствовать в archetype и пройти runtime-проверки.

### Зарегистрированные archetypes

В metadata зарегистрированы 33 ID:

- faction templates: `Legion_Assaulter`, `Legion_Frontliner`, `Legion_Machinegunner`, `Rebels_Assaulter`, `Rebels_Frontliner`, `Rebels_Machinegunner`;
- общие боевые: `Melee`, `Soldier`, `Soldier_Sniper`, `Skirmisher`, `Brute`, `HeavyGunner`;
- специалисты: `Artillery`, `Grenadier`, `Medic`, `Medic_Low`, `TheMajor`, `PierreGuard`;
- scenario/state: `Beast_Hyena`, `Turret`, `TurretBoss`, `Scout_LastLocation`, `__Scout_LastLocation`, `PinnedDown`, `Panicked`, `GuardArea`, `EmplacementGunner`, `Deserter`, `Berserk`;
- зарегистрированные legacy-варианты: `Soldier_old`, `Skirmisher_old`, `HeavyGunner_old`, `Brute_old`.

Регистрация означает доступность preset ID. Фактическое участие зависит от ссылки из `UnitData`, сценария или runtime-переключения archetype.

### Faction templates Legion/Rebels

| Роль | Behaviors | Основные positioning policies | Targeting | Характерные actions |
| --- | --- | --- | --- | --- |
| Assaulter | `PositioningAI`, `StandardAI` | avoid death, damage, flank, indoor/outdoor, LOS, proximity, cover, weapon range | health, weapon | basic, cancel, charge, mobile shot, landmine, flare, grenade, overwatch/run-and-gun |
| Frontliner | `PositioningAI`, `StandardAI` | как Assaulter плюс high ground | health, weapon | basic, heavy weapon, mobile shot, landmine, flare, grenade, overwatch/run-and-gun |
| Machinegunner | `PositioningAI`, `StandardAI` | damage, range, cover, flank/position constraints | health, weapon, enemy Will | basic, MG setup, MG burst, landmine, flare, grenade |

Legion и Rebels используют зеркальные role templates. Конкретные stats, вооружение и переходы tiers принадлежат `UnitData` и описаны в [схеме юнитов Legion и тирах снаряжения](legion-units-equipment-tiers.md). AI archetype не выбирает tier предметов; он работает с уже выданным текущему юниту инвентарём.

## Randomness, save и network

Большинство vanilla/JAZZ-развилок использует `InteractionRand`, что даёт воспроизводимый выбор при одинаковом tactical state. `PickBestAttack()` top-K также на `InteractionRand("AIDecision")`.

`ai_context`, path/LOS caches и damage predictions пересоздаются для решения. `g_AIDest` и `g_AIBiases` являются map-scoped состоянием. Локальный `raisedAlarm` — Lua-upvalue файла, не объявленный `GameVar`; его значение и рассчитанные рядом константы не имеют явного save-schema JAZZ. Флаги `bunker_used` / `disengage_used` ephemeral в `ai_context`.

Обновление AI-кода во время существующей тактической сессии требует нового боя/карты для чистой проверки: сохранённые game-time threads могут продолжить старый байткод до завершения.

## CommonLib и порядок override

На проверенном срезе CommonLib 1.11, build 1056, commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c` цепочка имеет вид `vanilla → CommonLib → JAZZ`.

Подтверждённые пересечения:

| Символ | Итоговый provider |
| --- | --- |
| `AIChooseSignatureAction` | `jazz/Code/CombatAI.lua` |
| `AIGetAttackTargetingOptions` | `jazz/Code/AiActions.lua` |
| `AIPolicyIndoorsOutdoors:EvalDest` | `jazz/Code/AiActions.lua` |
| `AIPolicyProximity:EvalDest` | `jazz/Code/AIPolicy.lua` |
| `AISelectAction` | `jazz/Code/CombatAI.lua` |
| `UpdateSuspicion` | `jazz/Code/UnitAwareness.lua` |

Полная цепочка и риски поддерживаются в [override matrix](../override-matrix.md). После обновления JA3 или CommonLib крупные copied overrides надо сравнивать трёхсторонне: старая vanilla, новая vanilla, текущий JAZZ.

## Известные статические риски

Это не результаты runtime-теста; это места, которые текущий код требует проверить или исправить отдельным change scope.

1. ~~MatchUnit `GameState.state`~~ — исправлено в JAZZ-AI-002 (`GameState[state]`).
2. ~~`PickBestAttack` `math.random` / `total_cost == AP`~~ — исправлено (`InteractionRand`, `<= AP`).
3. ~~`AIFindDestinations` `visible = true`~~ — исправлено (team visibility + SoftDisengage reserve).
4. ~~`AICalcAttacksAndAim` double aim_cost~~ — исправлено.
5. ~~`AIReloadWeapons` nil ammo~~ — исправлено.
6. ~~flare `or true` / nil `target_pts`~~ — исправлено.
7. `InfiniteLoopFix.lua` выставляет очень большие global thresholds детектора. Обёртки `PauseInfiniteLoopDetection()` вокруг тяжёлых расчётов дополнительно уменьшают шанс раннего обнаружения зависшего AI-хода.
8. `AIBehavior:OnStart()` может дублировать `VoiceResponse` поведения, которое воспроизводит её самостоятельно.
9. Suspicion threshold/distance/night tick захватываются при загрузке файла и не следуют позднему `raisedAlarm`/смене времени.
10. Крупные замены `CombatAI`/`AiActions` включают локальные копии vanilla-функций для AOE, scout, interactable и custom behavior; они имеют высокий drift-риск после patch игры.
11. Cover-move Disengage опирается на `context.all_destinations` / combat_paths с начала Think — после длинного боя пути могут устареть; One Re-engage / свежий pathing — follow-up.
12. Dynamic archetype transitions — вне JAZZ-AI-002.

## Проверка поведения

Минимальная runtime-матрица после изменения AI:

- по одному unit каждого ключевого archetype: assaulter, frontliner, machinegunner, melee, sniper, grenadier, medic, turret;
- выбор `PositioningAI`/`StandardAI`, restart и переходы `Early/Normal/Late`;
- cover, high ground, proximity, flank, indoor/outdoor и avoid-death;
- basic, burst/auto, grenade, flare, MG setup/burst, heavy weapon, overwatch/run-and-gun;
- ровно достаточные AP, лишние AP, reload, пустой магазин, jam и `AmmoInventory`;
- target state `Day`, `Night`, `RainHeavy`, suppression, unconscious и pinned;
- noise/LOS/darkness/rain, рост suspicion, raised alarm и heat propagation;
- exploration → conflict → turn → conflict end;
- отсутствие friendly fire и разумное время принятия решения;
- одинаковый replay/multiplayer результат на двух peers;
- совпадение выбранного aim-level и predicted multishot CTH с crosshair/фактической атакой для одинакового контекста;
- повторное сравнение всех пересечений с текущим CommonLib HEAD.

Для диагностики фиксировать unit ID, archetype ID, keywords, выбранный behavior, action, target, destination, AP до/после и active `GameState`.

## Сопровождение

Страница обновляется при изменении:

- runtime-функций `AIBehavior`, `AIActions`, `CombatAI`, policies или awareness;
- public ID `AIArchetype`, keyword, signature action или policy class;
- generated `jazz-units/items.lua`/metadata, меняющих AI preset;
- load order/dependencies или пересечений CommonLib;
- save/network/random contract AI.

Новый или удалённый CommonLib override одновременно отражается в `docs/technical/override-matrix.md` и `docs/technical/compatibility.md`. Empty, dormant и unreferenced modules нельзя описывать как активную механику.
