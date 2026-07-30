# Тактический AI и awareness

## Назначение и эффект для игрока

JAZZ существенно меняет выбор действий AI, оценку позиций, укрытия и флангов, применение гранат/осветительных средств/пулемётов, а также обнаружение, suspicion и alert. Это одна из самых конфликтных с CommonLib зон.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | `AIActions`, `CombatAI`, generated AI policies/classes, `UnitAwareness` и tactical alerts |
| CommonLib | `Code/FixAI.lua` меняет выбор/targeting/policies/awareness; эти функции затем частично заменяются JAZZ |
| JAZZ | Крупные варианты AiActions/CombatAI/UnitAwareness, новые policies, grenade/flare/MG/cover logic и AI data в units |

## Реализация и load-state

Загружаемые core-файлы:

- `Code/AiActions.lua` — attacks, targeting, aim/reload и action helpers;
- `Code/AiAction_ThrowFlare.lua` — grenade/flare action;
- `Code/AiFastForward.lua` — auto fast-forward / PoV visibility на вражеском ходе;
- `Code/AIBehaviours.lua` — небольшой слой behavior registration;
- `Code/AIPolicy.lua` — позиционные политики (cover/threat, ScoreMode, role anchor, anti-peek, ally spacing — POL-001…003 code loaded; specs may still be `approved`);
- `Code/AIContextProfiles.lua` — context profiles / officer directives / aura lifecycle (CTX/CMD code loaded);
- `Code/CombatAI.lua` — выбор действия и tactical execution;
- `Code/UnitAwareness.lua` — suspicion, alerts и переходы awareness;
- `Code/Rato_CustomSeekCover.lua`, `Rato_GrenadeRange.lua`, `Rato_MGSetupAP.lua`, `Rato_TryNotToBeFlanked.lua` — дополнительные scoring/constraints;
- `Code/Rato_MGSetupPosScore.lua` — loaded empty placeholder;
- `Code/PushUnitAlert.lua` — loaded empty placeholder;
- `Code/AIPolicyAttackAP.lua` — empty dormant/unlisted;
- `Code/InfiniteLoopFix.lua` — увеличивает защитные thresholds от зависания;
- `Code/System_OR_Unit.lua`, `CombatActions.lua`, `System_OR_Weapons.lua` — действия/состояние/оружие, используемые AI.

`jazz-units` загружает `Code/AIKeywords.lua`, `Code/AICombatStance.lua` (medic/regroup/role stance — MED/REG/ROLE-002 code loaded) и generated **40** AI archetypes, enemy roles/squads и UnitData. `jazz-maps/Code/AIMechanism.lua` существует, но metadata его не загружает: его stealth/AIM option overrides не участвуют в runtime.

## Подтверждённые коллизии CommonLib

| Символ | Цепочка | Риск |
|---|---|---|
| `AIChooseSignatureAction` | vanilla → `CommonLib/Code/FixAI.lua` → `jazz/Code/CombatAI.lua` | JAZZ может не включить новый CLib fix |
| `AIGetAttackTargetingOptions` | vanilla → CommonLib → `jazz/Code/AiActions.lua` | выбор атаки/цели |
| `AIPolicyIndoorsOutdoors:EvalDest` | vanilla generated class → CommonLib → JAZZ AiActions | позиционная оценка |
| `AIPolicyProximity:EvalDest` | vanilla generated class → CommonLib → JAZZ AIPolicy | дистанционные веса |
| `AISelectAction` | vanilla → CommonLib → JAZZ CombatAI | различаются сигнатуры; высокий риск |
| `UpdateSuspicion` | vanilla → CommonLib → JAZZ UnitAwareness | stealth и обнаружение |

Полный статус — в [override matrix](../override-matrix.md). После обновления CommonLib эти тела надо сравнивать заново, а не считать позднюю JAZZ-версию автоматически правильной.

## AI pipeline

1. Юнит получает archetype, role, keywords, equipment и доступные actions.
2. Awareness определяет known/suspected targets и состояние команды.
3. AI строит возможные destinations и атакующие варианты.
4. Policies оценивают AP, cover, flank, proximity, high ground, enemy Will, danger/death risk и indoor/outdoor.
5. Targeting выбирает оружие, target, aim, shot mode, grenade/flare/MG/signature action.
6. `AISelectAction` запускает действие; execution проходит общие combat/weapon systems.
7. Noise, damage, sight и события боя обновляют alerts/suspicion.

`GetCTHByAimLevels` вызывает тот же `Unit:CalcChanceToHit`, что UI и фактическая атака. Внутри одного AI think результаты кэшируются в `context.cth_by_aim_cache` по `(enemy.handle, action.id, max_aim)` — повторные `PickBestAttack` / Dump / dest score не пересчитывают полную сетку aim. `PredictCTH` больше не вычитает линейный recoil: он строит общий `JAZZ_CTHGetRecoilProfile` и суммирует `JAZZ_CTHGetBulletChance` для той же последовательности пуль. Поэтому отдельная правка AI-точности должна считаться изменением общего CTH-контракта.

`AIUpdateDestLosCache` компактует уже видимые dest одним проходом (без серии `table.remove`). Полный объём `CheckLOS` dest×enemy остаётся ванильным; см. [performance-vanilla-report.md](../performance-vanilla-report.md).

`AIPrecalcDamageScore` для повторной цели (`GetLastAttack`) добавляет SameTarget через `AICalcSameTargetScoreBonus`: `CalcValue` + `GatherCTHModifications` (включая перк **Пристрелка** / `TakeAim`) и `AccuracyBonusSameTarget` с компонентов оружия — не только плоский preset Bonus.

В Dump (`AIPlayAttacks`) `PickBestAttack` липкий по режиму огня на той же цели: `context.dump_attack_mode` предпочитается, пока score режима ≥ `AIDecisionThreshold`% от best и режим влезает в AP; смена/потеря цели сбрасывает sticky.

## Policies и тактические расширения

JAZZ оценивает attack AP, cover, anti-flank, proximity, high ground, enemy Will и безопасность позиции. Rato-модули добавляют custom seek-cover, grenade range, MG setup AP и запрет очевидного подставления под фланг. Machine gun требует согласованности setup position, AP, action availability и visual/entity state.

`InfiniteLoopFix.lua` не выбирает тактику, а меняет protective thresholds. Слишком низкое значение вернёт зависание; слишком высокое может скрыть бесконечный цикл дольше.

## Keywords, archetypes и roles

AI keywords в units: `Melee`, `CQB`, `Soldier`, `Marksman`, `Sniper`, `Leader`, `MG`, `Control`, `Explosives`, `Ordnance`, `Smoke`, `Flank`, `MobileShot`, `RunAndGun`, `Stim`, `Nova`, `Heal`.

**40** archetypes охватывают artillery, berserk/brute/melee, emplacement/turret, grenadier, guard area, heavy/machine gunner, medic, panicked/pinned, scout/skirmisher/soldier/sniper, Major и faction-specific варианты Legion/Rebels. Generated UnitData связывает archetype с инвентарём, stats и actions.

## Awareness и внешние условия

`UnitAwareness.lua` заменяет крупную vanilla-систему. На обнаружение влияют LOS, light/darkness, smoke, night/weather, camo, noise и team state. `IsLineInSmoke` дополнительно переопределён JAZZ поверх функции CommonLib в `System_OR_Unit.lua`.

Heat-alarm (`JazzRaisedAlarm` MapVar): при высоком Heat exploration tick поднимает suspicion-пороги (80 vs 160) и сужает distance mod; пороги считаются внутри `UpdateSuspicion`, не при load. Обход врагов для AlarmNoise — `ipairs` (порядок + InteractionRand).

События conflict/turn/exploration переводят units между состояниями. Неправильная очистка suspicion/alerts может пережить бой или сломать переход exploration ↔ combat.

## Межпакетные зависимости

- `jazz-units`: archetypes, keywords, squads, equipment и stats;
- `jazz-maps`: позиции, zones, patrols, guardposts, spawners и tactical geometry;
- `jazz_assets`: weapon/attachment entities и visual states;
- core: algorithms, actions, effects, weather и UI.

## Проверка

- signature action и обычная атака на разных дистанциях;
- grenade/flare/smoke, MG setup и suppression;
- indoor/outdoor, cover, high ground, flank и no-safe-position;
- low/high AP и необходимость reload/unjam;
- разные keywords/archetypes и weapon roles;
- sight/noise/smoke/night/rain/camo suspicion;
- переход exploration → conflict → turn → combat end;
- отсутствие зацикливания и разумное время AI turn;
- разрешение текущего upstream CommonLib перед каждой задачей и повторное сравнение всех AI-коллизий при изменении HEAD;
- deterministic multiplayer/replay;
- совпадение выбранного aim-level и predicted multishot CTH с crosshair/фактической атакой для одинакового контекста.

## Сопровождение

Любое изменение AI code, generated archetype, role или keyword обновляет эту страницу и тесты. Новая/удалённая коллизия с CommonLib немедленно обновляет `docs/technical/override-matrix.md` и `docs/technical/compatibility.md`. Dormant/empty files нельзя считать активными fix-модулями.
