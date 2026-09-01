# Тактический AI и awareness

## Назначение и эффект для игрока

JAZZ существенно меняет выбор действий AI, оценку позиций, укрытия и флангов, применение гранат/осветительных средств/пулемётов, а также обнаружение, suspicion и alert. Это одна из самых конфликтных с CommonLib зон. Игроку: [тактический ИИ](../../wiki/tactical-ai.md), аура и порядок хода — [officer-aura](../../wiki/officer-aura.md).

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | `AIActions`, `CombatAI`, generated AI policies/classes, `UnitAwareness` и tactical alerts |
| CommonLib | `Code/FixAI.lua` меняет выбор/targeting/policies/awareness; эти функции затем частично заменяются JAZZ |
| JAZZ | Крупные варианты AiActions/CombatAI/UnitAwareness, новые policies, grenade/flare/MG/cover logic и AI data в units |

## Реализация и load-state

Загружаемые core-файлы:

- `Code/AiActions.lua` — attacks, targeting, aim/reload и action helpers;
- `Code/AiAction_ThrowFlare.lua` — night/underground illumination: throwable `Flare` sticks **and** `FireFlare` signal pistol (`FlareHandgun`);
- `Code/AiFastForward.lua` — auto fast-forward / PoV visibility на вражеском ходе; **союзники (Rebels `side=ally`)** при Running/Always всегда на Fast (иначе PoV их почти всегда видит и FF не срабатывал);
- `Code/System_AI_VanillaBeasts.lua` — loaded **before** `AiActions.lua` / `CombatAI.lua`: `JazzAI_UsesJazzCombatAI` (`species == "Human"`) and vanilla copies (`JazzAI_VanillaCreateContext`, `PlayAttacks`, `FindDestinations`, `PrecalcDamageScore`, …). Non-human units (Crocodile / Hyena / Hen) dispatch here and do **not** run JAZZ Dump, dest caps, firearm Ensure, cover-disengage, scout recontact, act-slots, or sniper/path wraps;
- `Code/AIBehaviours.lua` — behavior voice + **Deserter** `RetreatAI:CanDespawn` proximity gate (DES-001) + **CMD-002** `AIBehavior:GetTurnPhase` (act-slot Early/Normal/Late, then Threatened→Late; animals keep vanilla phase);
- `Code/AIPolicy.lua` — позиционные политики (cover/threat, ScoreMode, role anchor, anti-peek, ally spacing — POL-001…003 code loaded; POL-003 global additive spacing superseded by POL-004 crowd modifier; XYZ dibs + authored `AIPolicyAllySpacing` remain);
- `Code/AIContextProfiles.lua` — context profiles / officer directives / aura lifecycle (CTX/CMD code loaded); team directive in `MapVar JazzAI_TeamDirectives` (`directive` / `source` / `radius` / `focus_target` / **`semi_sniper` / `pseudo_mg` / `pusher` / `smoke`** / **`recontact_probes`**); **CMD-002** `MapVar JazzAI_TeamActSlots` + `JazzAI_AssignTeamActSlots` on `Combat:AITurn`; explosive throw budget `JazzAI_TeamExplosiveThrows`; **fatigue** in `MapVar JazzAI_TeamDirectiveFatigue`; **score-picker** `JazzAI_PickOfficerDirective`; Influence buffs by directive; FocusFire bias **×2**; OccupyHeights / FallBack / rear-guard; loc **6100–6125** (FocusFire tooltip **Цель** / **Target** from `focus_target`); **GoHidden** `JazzAI_TryUnitGoHidden` always `CreateGameTimeThread` for `Unit:Hide()` (BeginTurn `UnitBeginTurn` is procall: `IsGameTimeThread` true, `CanYield` false → `PlayTransitionAnims` Sleep asserts); **JAZZ-AI-007** `MapVar JazzAI_TeamFallBackState` (chance start + merge cancel), recontact standoff 14–20 / farm dest / peek-exit helpers;
- `Code/System_AI_CombatBarks.lua` — **JAZZ-AI-BARK-001** (loaded): `CreateFloatingText` over a **visible** enemy after a decision. Caps: **2**/team/AI-turn, **1**/unit/activation, same event once/team/turn. Fast-forward silent. Events: officer directive **change** (all CMD-001, FocusFire with `<name>` or anon), archetype once/combat (panic/desert/berserk/medic/melee), grenade `aoeType` (via the single `AiActions.lua` `AIActionThrowGrenade:Execute` wrap, not a second wrap), weapon-class **swap** (not empty-hands→gun), MGSetup, dest press/flank/long. Does not change scores or dest. Bank loc **20157–20596**.
- `Code/CombatAI.lua` — crowd/casualty POL-004; SNIPER-001 hold + **optic-aware range**; dynamic semi-sniper (aura-assigned) uses same hold/optics path; ACT-003 MG half-cover; **MG squad tether** (`jazz_mg_tether`: −30/tile beyond 12 from nearest ally); **mortar outdoor bias** (`jazz_need_outdoors`: Indoors −400 / Outdoors +120; rear-guard ignores indoor allies as front); **PERF-003** AI `CombatPath:RebuildPaths` bbox via `g_Classes` wrap (AP reach +8 tiles, cap 64; **Scout_LastLocation / recontact margin 24**; **skipped for animals**) + `StartAI` `Sleep(1)` only on game-time thread; gated `RebuildPaths` log; **`AIPickScoutLocation` radius `5*guim`** (not 80 m) and AOE target points skip scout-scan when enemies already supply points; **JAZZ-AI-007** wrap `UnitProperties:SelectArchetype` (humans: PickCustom before scout; animals: vanilla base, no `Scout_LastLocation`);
- `Code/UnitAwareness.lua` — suspicion, alerts и переходы awareness;
- `Code/InfiniteLoopFix.lua` — увеличивает защитные thresholds от зависания;
- `Code/System_OR_Unit.lua`, `CombatActions.lua`, `System_OR_Weapons.lua` — действия/состояние/оружие, используемые AI.

`jazz-units` загружает `Code/AIKeywords.lua`, `Code/AICombatStance.lua` (medic/regroup/role stance; **aura-assigned** semi-sniper / pseudo-MG via `JazzAI_TeamDirectives`) и generated AI archetypes (в т.ч. `Legion_Flanker` / `Rebels_Flanker`, `OptLocSearchRadius = 55`), enemy roles/squads и UnitData. `JazzAI_PickCombatStance` резолвит faction stance-id через `JazzAI_ResolveKnownArchetype`: отсутствующий preset (исторический gap `Rebels_Flanker`) → `*_Assaulter` / `*_Frontliner`. Soft Precalc prune gate: `JAZZ_AI_PERF_PRECALC_TARGET_SOFT = 12`; DestLos CheckLOS cap **200**; **OptLoc `all_destinations` cap `JAZZ_AI_PERF_OPTLOC_DEST_CAP = 200`** (humans only; animals use vanilla `JazzAI_VanillaEnumValidDests` / `JazzAI_VanillaFindOptimalLocation` without dest-cap) (`JAZZ_AICapOptLocCandidates`: stay/important/behavior, then Strategy reserve 48 — high ground / role anchors / 8-compass ring — then nearest threat; DestLos/Precalc still nearest-threat via `JAZZ_AICapDestLosCandidates`); Precalc dest cap **48**; TakeCover scores at most **8** nearest visible threats per dest (`JAZZ_AI_PERF_TAKECOVER_ENEMY_CAP`) with full POL-001 `GetCoverPercentage`; **PERF-003** AI path rebuild `restrict_area` AP-bbox (`JAZZ_AI_PERF_PATH_RESTRICT_MARGIN_TILES` **8**, max **64**); scout/AOE `ForEachPassSlab` stays at vanilla **5 m** (Dump signature Precalc on 513 maps hung at `80*guim`) — `OptLocSearchRadius` unchanged (jazz `CombatAI.lua` / `AiActions.lua` / `AIPolicy.lua`). `jazz-maps/Code/AIMechanism.lua` существует, но metadata его не загружает: его stealth/AIM option overrides не участвуют в runtime.

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

`GetCTHByAimLevels` вызывает тот же `Unit:CalcChanceToHit`, что UI и фактическая атака, **но без LOF/stuck** (`NoLineOfFire` ставится только в `GetAttackResults`). `AIGetAttackTargetingOptions` для Dump считает CTH через `CalcChanceToHit`, не `GetActionResults` (JAZZ-AI-PERF-003). Перед DumpFire один дешёвый луч (`Jazz_DumpCheapLineOfFire`): heightmap `IntersectSegment`, **первые 3 непроходимые плиты** по линии (entity/slab-скала, не яма) или тело союзника → не `AIPlayCombatAction`, выход в Disengage (JAZZ-AI-002 / PERF-004). Dump в модель при **командном** `HasVisibilityTo(unit.team, target)` и чистом LoF; личный LOS не обязателен (как `PickBestAttack` по `enemy_visible_by_team`). Team vis без LoF (скала перед дулом) — abort cheap ray, не выстрел. Без team vis в модель не бить (007 last-known). Чистая линия на execute заполняет `hits` целью, иначе Dump CTH-попадание давало 0 урона. Внутри одного AI think сетка aim кэшируется в `context.cth_by_aim_cache` по `(enemy.handle, action.id, max_aim)`. `PredictCTH` больше не вычитает линейный recoil: он строит общий `JAZZ_CTHGetRecoilProfile` и суммирует `JAZZ_CTHGetBulletChance` для той же последовательности пуль. Поэтому отдельная правка AI-точности должна считаться изменением общего CTH-контракта.

**Empty active hands (humans only):** before context creation and before Dump, `JAZZ_AIEnsureActiveFirearm` switches to a normal firearm in the other Handheld slot, or moves one from Inventory into an empty Handheld slot and reloads it. `HolsterSlot` is visual-only. Heavy weapons and flare guns remain excluded. `JAZZ_AIResolveContextWeapon` then keeps a real melee item if present and only falls back to virtual `UnarmedWeapon` for empty-handed humans.

**Animals (`species ~= "Human"`):** JAZZ combat AI does not apply. `JazzAI_UsesJazzCombatAI` is false; `AICreateContext` / `AIFindDestinations` / `AIPlayAttacks` / `AIPrecalcDamageScore` / `AIUpdateDestLosCache` / targeting / `SelectArchetype` / path-restrict / ScoreReachable wraps dispatch to vanilla copies in `System_AI_VanillaBeasts.lua` (or the pre-wrap `SelectArchetype` base). **Target is always the nearest living enemy** (`JazzAI_BeastLockNearestEnemy`: `GetDist`, handle tie-break, no score pool / `TargetScoreRandomization`). Dest is the reachable slab closest to that enemy (`JazzAI_BeastScoreNearestEnemyDest` / `JazzAI_BeastFindOptimalLocation`) — no 80% band, no weighted pick. Crocodiles bite via `CrocodileBite` on `CrocodileJaws`; hyenas use vanilla `HyenaCharge` / bite. Dump, dest-cap, cover-disengage, ChangeStance, act-slots, and scout-recontact are human-only.

Wiki and showcase do not describe animal combat AI (vanilla JA3 behavior).

`AIUpdateDestLosCache` компактует уже видимые dest одним проходом (без серии `table.remove`). Полный объём `CheckLOS` dest×enemy остаётся ванильным; см. [performance-vanilla-report.md](../performance-vanilla-report.md).

`AIPrecalcDamageScore` для повторной цели (`GetLastAttack`) добавляет SameTarget через `AICalcSameTargetScoreBonus`: `CalcValue` + `GatherCTHModifications` (включая перк **Пристрелка** / `TakeAim`) и `AccuracyBonusSameTarget` с компонентов оружия — не только плоский preset Bonus.

В Dump (`AIPlayAttacks`) `PickBestAttack` липкий по режиму огня на той же цели: `context.dump_attack_mode` предпочитается, пока score режима ≥ `AIDecisionThreshold`% от best и режим влезает в AP; смена/потеря цели сбрасывает sticky. Для `MGBurstFire` score использует фактическую длину `weapon:GetAutofireShots(action)` вместо `BurstShots` и фактический `action:GetAPCost(unit)`, включая authored наценку +1/+2 AP.

**Weapon attacks / mobile (JAZZ-AI-ACT-005):** `AISignatureAction:MatchUnit` больше не смотрит `unit.ui_actions`. Gate = `JazzAI_IsAttackActionAvailable` (`AvailableAttacks` или `EnableRunNGun`→`RunAndGun`, плюс `GetUIState == "enabled"`). `AIActionMobileShot` резолвит ID через `JazzAI_ResolveMobileAttackId` (приоритет `JAZZ_MobileShotgun` → `RunAndGun` → `RunAndGun_Carbine` → `MobileShot`). `Unit:GetBasicAttackModes` кладёт в `result.all` все enabled ID из `AvailableAttacks`, кроме mobile set и positional/utility (`MGSetup`/`Overwatch`/`Reload`/…). Dump `PickBestAttack` scoring знает class techniques (Zipper, ControllableBurst, LargeAutoFire, DoubleTap, …) через `JazzAI_EstimateAttackShots`; mobile ID в Dump не выбираются. Perk-unlock / tier weights class techniques — follow-up.

## Policies и тактические расширения

JAZZ оценивает attack AP, cover, anti-flank, proximity, high ground, enemy Will и безопасность позиции. Machine gun setup согласован с AP, action availability и visual/entity state.

**OptLoc TakeCover weights (POL-001, locked 2026-08-18):** Legion/Rebels Frontliner **20** (team vis) **+ 40** (unscoped); Assaulter **10** (team); Flanker **15** (team), radius **55**. Not the design 80–150 band — owner: intentional after PERF dest-cap 200 and TakeCover enemy cap 8. Flank-branch EndTurn TakeCover Weight **1**.

**AllyRoleAnchor / AvoidPeekVoxel (POL-002):** classes in `Code/AIPolicy.lua`; **wired** in Frontliner + Assaulter Legion/Rebels **OptLoc** (`screen`/`Sniper` Weight 35, `retinue`/`Leader` Weight 25, AvoidPeek Penalty 80 / Radius 1 / Weight 40). Flanker OptLoc does not get these policies.

**Weak Flanker AI on Assault/Front (ROLE-001 REQ-005, 2026-08-18):** Assaulter/Frontliner keep a Flank/Nova «Flanker AI» branch, but behavior Weight **80** and `AIPolicyFlanking` **150** (was 500–1000 / 1000). `Legion_Flanker` / `Rebels_Flanker` stay **500 / 1000**. Assaulter POS keyword `Flanks` → `Flank`.

**Casualty-aware anti-stack (JAZZ-AI-POL-004 + MED-002):** hard same-XYZ dibs из POL-003 сохраняется. После policies, sniper stay, bombard и BiasMarker положительный `AIScoreDest` умножается на `JazzAI_CrowdDangerModifier` (25–100%), затем non-medic dest с cover — на `JazzAI_CoverSpacingModifier` (100 / 55 / 30 при 0 / 1 / ≥2 живых союзниках с cover dest в `<2` тайла). Живой союзник даёт −60/−25/−10 percentage points в диапазонах `<1`/`<2`/`<3` тайлов; dead/downed/incapacitated союзник — −45/−30/−15, а каждая casualty после первой в радиусе 3 добавляет −10. Для melee (`EffectiveRange <= 1` или keyword `Melee`) floor = 55%. **Medic / `can_heal` / archetype Medic|Medic_Low crowd modifier = 100** (игнор скученности, MED-002). Живой ally использует planned `ai_destination`, casualty — фактическую snapshot-позицию. Трупы не становятся impassable, RNG и persistent state не добавляются; explicit `AIPolicyAllySpacing` остаётся отдельным authored additive policy.

**Sniper / Marksman hold (JAZZ-AI-SNIPER-001 + JAZZ-AI-008):** `ExtremeRange = weapon.WeaponRange`; stay-hold если `dest_target_score[stay] > 0`. Если выстрела нет, но юнит — line perch holder (Sniper/Marksman / semi-sniper / `*_Frontliner` / `*_Machinegunner` / aura `OccupyHeights`; не Assaulter/Flanker/Medic/Deserter/Regroup/melee/pusher) на высоте ≥1 slab над `last_known`, без личного vis, не farm, и `CheckLOS` dest→egress (тот же якорь, что Fallback OW) в `WeaponRange` — **остаётся** (`JazzAI_ApplySniperHoldDestination` → stay) и `JazzAI_ScoreRecontactDest` даёт stay **+180** без бонуса «ближе к звуку». Useless streak на perch **не** растёт. Assaulter у подножия без LOS на выход не hold. `MapVar JazzAI_SniperUselessStreak`: бесполезные ходы **мягко** режут вес высоты — полный HighGround на 0–1 ход; ×40% на 2-й; ×0% на 3+; soft stay penalty 0 / 0 / 300 / 600+. Без hard escape dest. Clear на CombatStart.

**FallBack peel Overwatch (JAZZ-AI-009):** при директиве `FallBack`, если игроки сейчас видят стрелка и 008 perch нет, dest с `CheckLOS` на vacated stay, разрывом LoS от этих игроков, дальше от nearest enemy, `dest_ap ≥` Overwatch, дистанция в поясе `Max(4, OW_max−4)…OW_max` (`GetOverwatchConeParam("MaxRange")`, иначе max среди qualifying) получает **+220** и wrap заменяет выбранный dest. Якорь `context.jazz_break_los_ow_anchor` = stay slab; Disengage **не** TakeCover и ставит Fallback OW на якорь, не 007 peek-exit. Нет qualifying dest — обычный Отход + peek-exit. Без `GetLoFData`. Medic/Deserter/Melee/Regroup/stationed MG не peel.

**MG half-cover setup (JAZZ-AI-ACT-003):** `AIActionMGSetup` после выбора зоны проверяет тот же предикат, что игрок (`CoverLow`, `coverage > 80` vs `target_pos`, оценка в `Crouch`). При halfcover Execute сначала ставит Crouch, затем `MGSetup` → `BipodUnfolded` без forced Prone; иначе prone-deploy как раньше. `AIScoreDest` даёт скромный bonus (+45) reachable dest с usable low cover для не-stationed MG/LMG. Rotate/Pack ветка без изменения.

**MG Dump + close fire (JAZZ-AI-ACT-004):** permanent MG/emplacement OW **не** блокирует Dump (`JAZZ_AICanDump` пропускает `g_Overwatch.permanent` / `HasPreparedAttack` для этого случая) — иначе после `MGSetup` gunner никогда не выбирал `AIActionMGBurstFire` (vanilla `AIPlayAttacks` такого gate нет). Временный OW по-прежнему стопит Dump. Близкая видимая угроза (≤ `JazzAI_MGCloseFireTiles` = 8): не-stationed пропускает первый `MGSetup` и стреляет; `PositioningAI` Label/Bias `MGSetup` score → 0; scoring зон MGSetup даёт bonus за близких в конусе и penalty за пропуск близких (rotate/pack вместо дальнего сектора).

**MGPack after Dump:** recovery если `StationedMachineGun` без OW; **и** vanilla pack+`restart` если Dump с живым permanent OW **не** атаковал (`not did_attack`) — иначе тыловой сектор залипает до конца боя. Не паковать сразу после `MGSetup` в той же секвенции (`did_attack` от setup). Intentional pack также через `AIActionMGSetup` Precalc при пустой зоне.

**Smoke (JAZZ-AI-ACT-002):** signature `SmokeGrenade` считает curtain на `g_Overwatch` / fire lane → ally `ai_destination` (угол выхода); прямое накрытие союзника только если он в `JazzAI_TeamActed` (после `AIPlayAttacks`). Дым режет sight (−70 `IsLineInSmoke`) и урон сквозь облако — не шапка на ещё не ходивших.

**Team turn sequencer (JAZZ-AI-CMD-002):** `JazzAI_AssignTeamActSlots` на `Combat:AITurn` (после refresh ауры стороны) пишет `MapVar JazzAI_TeamActSlots` `{ phase, kind, source }`. Kind→phase: heal / flare / smoke / mg_setup → **Early**; line → **Normal**; press (Assaulter/Flanker / aura `pusher`) → **Late**. Unique assign только **smoke** (`JazzAI_TeamDirectives[side].smoke`); flare — все носители с Night/Underground и unlit threat. `AIBehavior:GetTurnPhase` читает слот, затем ваниль `IsThreatened()` → Late. Обычные гранаты: мягкий бюджет `JazzAI_TeamExplosiveThrows` по `Game.game_difficulty` — Первая кровь (`Normal`) 1 полный + далее ×25%; Коммандос (`Hard`) 3 полных + 4+ ×25%; Миссия невыполнима (`VeryHard`) без лимита. Smoke/flare в бюджет не входят.

`InfiniteLoopFix.lua` не выбирает тактику, а меняет protective thresholds. Слишком низкое значение вернёт зависание; слишком высокое может скрыть бесконечный цикл дольше.

## Keywords, archetypes и roles

AI keywords в units: `Melee`, `CQB`, `Soldier`, `Marksman`, `Sniper`, `Leader`, `MG`, `Control`, `Explosives`, `Ordnance`, `Smoke`, `Flank`, `MobileShot`, `RunAndGun`, `Stim`, `Nova`, `Heal`.

Archetypes охватывают artillery, berserk/brute/melee, emplacement/turret, grenadier, guard area, heavy/machine gunner, medic, panicked/pinned, scout/skirmisher/soldier/sniper, Major и faction-specific варианты Legion/Rebels (`Rebels_Assaulter` / `Rebels_Flanker` / `Rebels_Frontliner` / `Rebels_Machinegunner`; `Rebels_Flanker` — clone `Legion_Flanker` для `RebelFlanker` / Scout stance; оба Flanker OptLoc **55**, не 80). Generated UnitData связывает archetype с инвентарём, stats и actions. Editor `items.lua` PickCustom for `JAZZ_Legion_*` / `Rebel*` calls `JazzAI_PickCombatStance` (Bonemaker `{ allow_medic = true }`); Flanker UnitData `archetype`/`RepositionArchetype` = `Legion_Flanker` / `Rebels_Flanker`.

**Deserter despawn (JAZZ-AI-DES-001):** vanilla `RetreatAI:CanDespawn` (`DespawnAllowed`, default true у `Deserter`) снимает юнита либо в зоне `Entrance`, либо когда с текущей клетки нет LOS к врагам. JAZZ override в `Code/AIBehaviours.lua`: LOS-ветка разрешена только если нет живого `team.player_team` юнита в **`JazzAI_DeserterSafeDespawnTiles = 16`** (`GetDist` ≤ 16×`SlabSizeX`). Entrance-despawn без этого gate. `Panicked` по-прежнему `DespawnAllowed=false`.

**Fallback Overwatch aim (JAZZ-AI-OW-001 + 007 + 008):** override `AIPlaceFallbackOverwatch` в `Code/AiActions.lua`. Vanilla no-sight path целился random 360° / дверь / лицо союзника. JAZZ: якорь `last_known_enemy_pos` / ближайший enemy. Если якорь сам с LOS (открытое) — сдвиг **1–3** тайла (`JazzAI_SoundOffsetPos`). Иначе цель = **первая проходимая плита по BFS** от якоря (≤8 тайлов / 40 клеток) с LOS — куда враг может выйти в обзор (угол дома, дверь, камень), не стена и не клетка за ней. Ночь/Underground: как OW-001 (lit / night-sight / lit scan ±4). Иначе **`false` (revert)**. Dump в модель без **командного** LOS не идёт. `JazzAI_HasLosToPos` / `JazzAI_FallbackOverwatchTargetPos` / `JazzAI_DestSeesPos` — generic (dest-score и OW делят якорь). Без RNG на aim. Вызывается из `JAZZ_AIDisengage` и vanilla no-sight bunker fail при `FallbackAction=overwatch`.

**Recontact / FallBack chance (JAZZ-AI-007 + 008):** ванильный scout-gate в `SelectArchetype` больше не ставит `Scout_LastLocation` до `PickCustom`. Скаут только если нет видимых, есть last known, не Medic/Deserter/Melee/Regroup/FallBack, и last known дальше **20** тайлов. Линия идёт в пояс **14–20** от звука (не на клетку игрока); до **2** probe (`Flank` / Flanker / aura pusher) могут ближе. **Исключение 008:** line perch (высота + LOS на egress) stay **+180**, без «идти к звуку». Кого игрок видит, а боец игрока нет — stay штрафуется (обязан сдвинуться; farm отменяет perch). Отход: порог dead≥2 и ≥30% — только *допуск*; старт `InteractionRand` со шансом = % потерь на порогах 30/50/70; срыв если у офицера ≥3 живых в 8 тайлах. Не стартовать без `GetNearestEnemy`. `JazzAI_InferRoleFamily` читает `unitdatadef_id` (live `class` всегда `Unit`). Isolated `Legion_Regroup` не берёт Heavy/Ordnance — ракетчик остаётся сзади и стреляет; AI `RocketLauncherFire` `MaxTargetRange` = WeaponRange **40**.

**Medic / Bandage (JAZZ-AI-MED-001 + MED-002):** vanilla `AISelectHealTarget` учитывал только `hpp ≤ MaxHp` (default 70%) и статус `"Bleeding"`, поэтому лёгкая кровь при HP выше порога и все `BleedingMedium`/`BleedingHeavy` не набирали score — Priority `AIActionBandage` на Healer не планировался (Standard держал Priority `MobileShot`). JAZZ override в `CombatAI.lua`: любой Jazz bleed bypass MaxHp + вес по тирам; self-bleed не режется `SelfHealMod`; `AIActionBandage` Precalc/Execute в `AiActions.lua` требует score&gt;0 и может сыграть `JazzBandage`, если нет kit medicine. Field-bandage affordance в voxel score берёт `JazzBandage:GetAPCost(unit)` (MED-005 Medical ladder), не preset `ActionPoints`. `Medic`/`Medic_Low`: при bleed/HP&lt;85% Healer **exclusive** (`JazzAI_MedicHealBehaviorScore` / combat behaviors → 0), `turn_phase` **Early**, Priority Bandage перед MobileShot, `MaxHp` 85 / `BleedingWeight` 300 / `SelfHealMod` 100. Stance `JazzAI_ShouldBecomeMedic`: dedicated (Bonemaker / family Medic / `allow_medic`) плюс не больше одного fill-in с medicine, если dedicated в команде нет; blanket «бинты + кровь в отряде → все Medic» снят.

## Awareness и внешние условия

`UnitAwareness.lua` заменяет крупную vanilla-систему. На обнаружение влияют LOS, light/darkness, smoke, night/weather, camo, noise и team state. `IsLineInSmoke` дополнительно переопределён JAZZ поверх функции CommonLib в `System_OR_Unit.lua`.

Heat-alarm (`JazzRaisedAlarm` MapVar): при высоком Heat exploration tick поднимает suspicion-пороги (80 vs 160) и сужает distance mod; пороги считаются внутри `UpdateSuspicion`, не при load. Обход врагов для AlarmNoise — `ipairs` (порядок + InteractionRand).

Realtime rear detection cap (`JAZZ-AI-004`): в exploration (`not g_Combat`), если союзник в **задней полусфере** наблюдателя (`abs(angle) ≥ 90°`), эффективный радиус для suspicion = `Min(GetSightRadius, 10 × SlabSizeX)`. Спереди и в бою кап не действует; `GetSightRadius` / LOS не меняются — только пузырь накопления suspicion. Константа: `lSuspicionRearSightCap` в `UnitAwareness.lua`.

Hidden sight (`JAZZ-AI-005`/`006`): укрытие Hidden ×35%; трава flat −10 + camo×3; indoors −5 всегда; `SightModMinValue` 9 (~4 Aware). Подробности — [видимость](visibility-weather-appearance.md).

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
- low/high AP и необходимость reload/unjam (`AIReloadWeapons` clears jam via `RepairJammed(nil)` — no WeaponResource write);
- разные keywords/archetypes и weapon roles;
- sight/noise/smoke/night/rain/camo suspicion;
- exploration: подход сзади за пределами 10 тайлов не копит suspicion; спереди дальний пузырь сохраняется;
- переход exploration → conflict → turn → combat end;
- отсутствие зацикливания и разумное время AI turn;
- **PERF-002 / CMD-002:** static PASS (OptLoc Strategy reserve; act-slot sequencer + grenade budget); runtime/human smoke у владельца (K1–K2, Q1–Q6);
- разрешение текущего upstream CommonLib перед каждой задачей и повторное сравнение всех AI-коллизий при изменении HEAD;
- deterministic multiplayer/replay;
- совпадение выбранного aim-level и predicted multishot CTH с crosshair/фактической атакой для одинакового контекста.

## Сопровождение

Любое изменение AI code, generated archetype, role или keyword обновляет эту страницу и тесты. Новая/удалённая коллизия с CommonLib немедленно обновляет `docs/technical/override-matrix.md` и `docs/technical/compatibility.md`. Dormant/empty files нельзя считать активными fix-модулями.
