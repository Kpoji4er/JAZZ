---
id: JAZZ-AI-ROLE-004
status: approved
owner: project-owner
systems:
  - tactical-ai
  - jazz-units-archetypes
  - legion-loadouts
  - ris-intelligence
repositories:
  - jazz
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-ROLE-004.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/design/legion-loadouts.md
  - jazz/docs/design/ris-legion-dossiers.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz/docs/tools/_audit_ris_ai_claims.py
  - jazz/docs/tools/README.md
  - jazz/docs/tools/_ris_copy_bank.py
  - jazz/scripts/legion-loadouts/data/recipes.json
  - jazz/Code/CombatAI.lua
  - jazz/Code/AIPolicy.lua
  - jazz/docs/tools/_check_role004_roofs.py
  - jazz-units/Code/AICombatStance.lua
  - jazz-units/UnitData/JAZZ_Legion_HeavyT1_Rocketeer.lua
  - jazz-units/UnitData/JAZZ_Legion_FlankerT3_Pathfinder.lua
  - jazz-units/UnitData/JAZZ_Legion_FlankerT4_Ranger.lua
  - jazz-units/UnitData/JAZZ_Legion_AssaultT1_Crusher.lua
  - jazz-units/UnitData/JAZZ_Legion_AssaultT2_Pyro.lua
  - jazz-units/UnitData/JAZZ_Legion_HeavyT2_Grenadier.lua
  - jazz-units/items.lua
  - jazz-units/metadata.lua
exclusive_resources:
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz/scripts/legion-loadouts/data/recipes.json
  - jazz/Code/CombatAI.lua
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/design/ris-legion-dossiers.md
  - docs/specs/active/JAZZ-AI-ROLE-002.md
  - docs/specs/active/JAZZ-AI-SNIPER-001.md
  - docs/specs/active/JAZZ-AI-CMD-001.md
  - docs/specs/active/JAZZ-AI-POL-004.md
  - docs/specs/active/JAZZ-AI-008.md
approved_by: pending
---

# JAZZ-AI-ROLE-004: Семьи ролей, фланговые снайпера, кит, переключение, крыши

## Проблема

Аудит 2026-09-08 (`docs/tools/_audit_ris_ai_claims.py`) и сверка 38 `JAZZ_Legion_*` с досье R.I.S., editor comment и `recipes.json`.

1. **`JazzAI_InferRoleFamily`** ищет `"Assault"` раньше `"Gunner"`. `JAZZ_Legion_GunnerT2_AssaultGunner` становится **Pusher**: каждый think `PickCombatStance` ставит `Legion_Assaulter` / `Flanker` вместо `Legion_Machinegunner`. Коммандо теряет MGSetup (ACT-003/004). Мачете срабатывает только из‑за этой ошибки (`NeverMelee` для MG не применяется).
2. Владелец (2026-09-08): **Застрельщик и Рейнджер — фланговые снайпера**. Это приоритет досье, не «убрать hold». Сейчас:
   - Застрельщик: kit (battle + Match) и keywords (`Flank`+`Marksman`) уже верные; hold SNIPER-001 + `Legion_Flanker` уже держатся.
   - Рейнджер: comment и `CustomEquip` ждут `SniperRifle` + ближний ствол, а recipe `primary_tags` = `carbine`/`smg`. `TryEquip(..., "SniperRifle")` часто не находит ствол. Досье говорит только «карабин/ПП» — это отстаёт от задумки флангового снайпера.
   - Следопыт на винтовочной ветке диаграммы (`Warden → Skirmisher → Pathfinder → Ranger`), comment «винтовка с глушителем и оптикой», keyword `Sniper`, но recipe = `carbine`/`smg`. Досье тоже пишет карабин/ПП и нож; нож ИИ не берёт (`NeverMelee` из `Sniper`, Handheld B = Firearm).
3. **Переключение оружия.** Рейнджер (и любой фланговый снайпер с CQB-вторичкой) не меняет ствол вблизи: `is_sniper` отсекает melee, а смена на alt CQB есть только у Line+aura pusher. Comment Рейнджера («переходит на карабин/ПП вблизи») мёртв.
4. **`JAZZ_Legion_HeavyT1_Rocketeer`**: в companion и `items.lua` нет `archetype`. `ResolveKnownArchetype(nil)` падает в `Legion_Assaulter` — ракетчик **пушит с РПГ**. Таблица тиров ошибочно пишет Assaulter. Владелец: не Assaulter; **`Artillery` тоже нельзя** — это миномёт (`Bombard` / `MortarShot`, без LOS, дистанция 20–50). Ракетчик несёт **РПГ** (прямой огонь, `RocketLauncherFire` range 40). Норматив: **`Legion_Frontliner`** (держать линию и стрелять, не пушить). `Artillery` остаётся у `HeavyT3_Mortarman`.
5. Мелкий drift кита vs comment/keywords: Пироман (`Melee` + Handheld B melee при `melee: null` — ложный Melee); Громила (`Melee` + comment «дробовик + пистолет», recipe `melee: null`, sidearm 55% с unlock 12) — владелец: раньше был **шанс на нож или пистолет**, `Melee` не ложный; Гранатомётчик несёт keyword `Sniper` и ловит SNIPER-001 hold на РПГ/ГП.
6. **Крыши (владелец 2026-09-08).** `AIPolicyHighGround` даёт `100*(z-uz)` за любой подъём. `JazzAI_CoverSpacingModifier` = 100, если на dest нет укрытия — голая кровля не штрафуется за скученность сильнее земли. После спуска HighGround на следующем ходе снова тянет наверх: юнит прыгает крыша↔земля. SNIPER-001 streak сбрасывается от одного выстрела и не держит гистерезис.

## Цели

- Семья роли по **намеренному** токену (`Gunner`/`Flanker`/`Heavy` раньше общего `Assault`).
- Канон **флангового снайпера**: default `Legion_Flanker`, SNIPER-001 hold если есть выстрел, без Press в Assaulter, без 008 line-perch; при CQB и живом alt-стволе — смена оружия, stance остаётся Flanker.
- Recipe + `CustomEquip` + keywords + досье R.I.S. совпадают на винтовочной ветке фланкеров.
- Коммандо остаётся MG и может взять мачете по AP-reach (исключение F4).
- Ракетчик явно **`Legion_Frontliner`** (РПГ с линии). Не Assaulter, не `Artillery` (миномёт).
- Static gate не даёт регрессии семьи и кита фланговых снайперов.
- Голая крыша: не складываться пачкой; не забираться без выстрела. После спуска не возвращаться наверх два хода (кроме укрытой клетки с выстрелом).

## Non-goals

- Новые public archetype ID.
- Смена ROLE-001 весов / OptLoc 55/80 / слабый Flanker 80/150.
- CMD-003 / JAZZ-AI-008 perch для семьи Scout (фланговый снайпер **не** line perch: без выстрела уходит, это «сменил позицию / ушёл»).
- Ночной CTX `SniperHold` сверх SNIPER-001.
- Револьвер во вторичке FrontT3_Sniper (comment vs редкий sidearm) — отдельный follow-up.
- Новые письма «Стратегии Майора» / Global AI.
- Mass regen всех 37 recipe, кроме Pathfinder, Ranger и Crusher (плюс validate generate).
- Менять формулу `100*(z-uz)` у ванильного `AIPolicyHighGround` для всех модов вне JAZZ score path: только множители/гейты в `AIScoreDest` / тонкий wrap EvalDest.
- Командное назначение «один на всю крышу-остров» flood-fill; достаточно same-Z <2 тайла.

## Канон ролей фланкеров

Диаграмма (design, не runtime upgrade):

- CQB-ветка: `Warden → Scout → Recon` (и элита той же идеи в других составах).
- Винтовочная ветка: `Warden → Skirmisher → Pathfinder → Ranger`.

| UnitData | Роль | Keywords (норматив) | Default archetype |
| --- | --- | --- | --- |
| `FlankerT1_Warden` | фланговый стрелок | `Flank`, `Control`, `Marksman` | `Legion_Flanker` |
| `FlankerT2_Scout` | CQB-фланкер | `Flank`, `RunAndGun`, `CQB` | `Legion_Flanker` |
| `FlankerT2_Skirmisher` | **фланговый снайпер T2** | `Flank`, `RunAndGun`, `Marksman` | `Legion_Flanker` |
| `FlankerT3_Recon` | CQB-фланкер / ночь | `Flank`, `RunAndGun`, `CQB` | `Legion_Flanker` |
| `FlankerT3_Pathfinder` | **фланговый снайпер T3** | `Flank`, `Sniper`, `Control` | `Legion_Flanker` |
| `FlankerT4_Ranger` | **фланговый снайпер T4** | `Sniper`, `Flank`, `Control`, `RunAndGun` | `Legion_Flanker` |

Фланговый снайпер = Scout-семья **и** (`Sniper` или `Marksman`). Сейчас это Застрельщик, Следопыт, Рейнджер; Дозорный — стрелок с `Marksman`, не полный снайпер-кит.

## Матрица переключения (норматив)

`JazzAI_PickCombatStance` после записи ауры лидера. Без нового RNG.

| Кто | Default | FallBack / TakeCover / Occupy* / GoHidden | Aura Push / NeedPush | Melee (F9 AP-reach) | Смена на alt CQB-ствол | SNIPER-001 |
| --- | --- | --- | --- | --- | --- | --- |
| Scout без Sniper/Marksman | Flanker | Frontliner | **Assaulter только если aura `pusher`** | да, если alt melee | не требуется | нет |
| **Фланговый снайпер** | Flanker | **остаётся Flanker** | **никогда Assaulter** (не кандидат в `pusher`) | нет | **да**, если alt = Pistol/Revolver/SMG/Carbine-или-AR и дистанция ≤ 10 тайлов; stance Flanker | да |
| Pusher (Assault*) | Assaulter | Frontliner | NeedFlank / Envelop → Flanker | да, если alt melee | нет | нет |
| Line без оптики | Frontliner | Frontliner | Assaulter только aura pusher | да, если alt melee | как сейчас (pusher + NeedPush) | нет |
| Line Sniper/Marksman | Frontliner | Frontliner | нет Assaulter | нет | нет | да |
| MG кроме Коммандо | Machinegunner | Machinegunner | нет | нет | нет | Marksman на T3/T4 допустим |
| **Коммандо** | Machinegunner | Machinegunner | нет | **да**, если alt melee | нет | нет |
| Ракетчик (RPG) | **`Legion_Frontliner`** | база | нет | нет | нет | нет |
| Гранатомётчик T2 | `Artillery` (как сейчас) | база | нет | нет | нет | нет |
| Миномётчик | **`Artillery`** | база | нет | нет | нет | нет |
| Leader | база (Sgt Assaulter, остальные Frontliner) | — | пишет ауру, return базы | нет | нет | Captain/optics допустим |
| Medic | Medic если `ShouldBecomeMedic` | иначе Frontliner | нет | нет | нет | Marksman только когда не лечит |

Это **сужает** `JAZZ-AI-ROLE-002-REQ-002` для Scout: голый `NeedPush` больше не переводит каждого фланкера в Assaulter. CQB-скауты жмут только по назначению ауры. Фланговые снайпера не жмут.

F4 «MG без flag не режет»: flag Коммандо = keyword `CQB` + `JazzAI_FindAltMeleeWeapon`. Остальные MG остаются NeverMelee.

## Крыши: скученность и гистерезис

Для всех human `JazzAI_UsesJazzCombatAI`. Животные — ваниль.

**Высокий dest:** voxel Z dest ≥ voxel Z stay + 1 `SlabSizeZ`.  
**Голый dest:** `JazzAI_PackedHasCover(dest)` = false.

| Правило | Норматив |
| --- | --- |
| Залезть на голую высоту | HighGround **не даёт плюс**, если `dest_target_score[dest] ≤ 0`. С выстрелом — обычный HighGround. |
| Второй на голой крыше | Живой союзник (planned `ai_destination`, иначе snapshot) на том же Z, дистанция <2 тайла: к POL-004 danger **+50**. Floor 25 как в POL-004. Medic/`can_heal` по-прежнему crowd 100. |
| Укрытая высота | HighGround и POL-004/CoverSpacing без новых штрафов. Можно сидеть вдвоём за парапетом. |
| Спуск | Как сейчас: нет выстрела 2+ хода (SNIPER-001 streak) или melee/threat. Не спускаться в том же ходе, где только что залезли (один dest за think и так). |
| Гистерезис | `MapVar JazzAI_HeightHysteresis` `[handle] = { last_z, descended_turn }`. Если dest_z ≤ last_z − 1 slab — записать `descended_turn = Combat.current_turn`. Пока `current_turn < descended_turn + 2`: HighGround за подъём (`dest_z > stay_z`) = 0. **Исключение:** dest с укрытием **и** `dest_target_score[dest] > 0`. На голую крышу во время окна — никогда. Clear на `CombatStart`. |
| Melee | `EffectiveRange ≤ 1` или keyword `Melee`: можно лезть без выстрела (достать цель). Скученность на голой крыше всё равно +50. |
| Фланговый снайпер | Смещается **по той же высоте** (крыша→укрытие на крыше). Спуск без выстрела + гистерезис, не крыша-земля-крыша. |

`AIPolicyHighGround` anti-ally (30/6 tiles по текущей позе) не считать достаточным: считать planned dest, как POL-004.

## Кит: что менять

Источник задумки: досье R.I.S. (приоритет), затем editor comment, затем текущий recipe. Generate: `python scripts/legion-loadouts/generate.py` только после правки Pathfinder, Ranger и Crusher, одна транзакция с `items.lua`. Новый XOR-хук в `generate.py` не нужен: оба поля уже есть, в руки один слот B.

| UnitData | Сейчас | Надо |
| --- | --- | --- |
| `FlankerT2_Skirmisher` | `battle`, Match, sidearm 35%, `melee: null` | **без смены recipe**. Battle rifle = канон T2. |
| `FlankerT3_Pathfinder` | `carbine`/`smg`, knife, smoke | `primary_tags`: `rifle` + `sniper`; пакеты `rifle_m2` / `sniper_m2` / `flanker` с глушителем; `ammo_cap` Match; smoke оставить; нож только loot (`melee` можно оставить, в руки не экипировать). `CustomEquip`: оба слота Firearm (винтовка), не melee. |
| `FlankerT4_Ranger` | recipe `carbine`/`smg`; `CustomEquip` SniperRifle+Firearm | `primary_tags`: `sniper` (+ опц. `battle`); пакеты `sniper_m2`/`sniper_m3`/`merc_m4`; **гарантированная** CQB-вторичка (carbine или smg в Handheld B, не chance-only sidearm); нож loot optional. `CustomEquip` оставить SniperRifle / Firearm. |
| `GunnerT2_AssaultGunner` | kit верный (LMG, machete 100%, molotov) | kit не трогать; чинится семья + melee exception. |
| `HeavyT1_Rocketeer` | нет `archetype` → fallback Assaulter | `archetype` + `RepositionArchetype` = **`Legion_Frontliner`**. Семья Heavy (NeverMelee, не Press). Не `Artillery`. |
| `AssaultT2_Pyro` | recipe SMG/carbine + 3 молотова (совпадает с досье) | убрать `Melee` из keywords; `CustomEquip` только Firearm (не Handheld B melee). Comment «дробовик» не канон. |
| `AssaultT1_Crusher` | shotgun; sidearm 55% с unlock 12; `melee: null`; keywords `CQB`+`Melee`; `CustomEquip` всегда пистолет | **оставить `Melee`+`CQB`**. Recipe: вернуть `melee` `Weapon_Knife` `chance_by_arch` **[40, 55, 70]**; sidearm оставить unlock 12 / 55. Handheld B — **одно** из двух (нож или пистолет), не оба в руках. `CustomEquip`: A Shotgun; B Pistol, затем MeleeWeapon (если пистолет не выпал). Comment: «дробовик + шанс нож или пистолет». Design-таблица L167: Melee = knife%. Досье — дробовик как угроза, вторичку можно не писать. |
| `HeavyT2_Grenadier` | `Ordnance,Control,Sniper` | убрать `Sniper` (не держать позицию как снайпер). |

Досье (банк `_ris_copy_bank.py`, apply editorial):

- **Рейнджер:** первичная снайперская / оптическая винтовка; вблизи карабин или ПП; «ударил с фланга и сместил позицию, если выстрела нет». Не писать, что основной ствол — карабин/ПП.
- **Следопыт:** глушёная винтовка / оптика, дым, удерживает скрытую линию. Нож не подавать как боевую угрозу.
- Застрельщик — без правки смысла (боевая винтовка, смена фланговых позиций = hold при выстреле + уход без выстрела).

## Остальные 38 — кит совпадает

Без смены recipe/keywords: Recruit, Roughneck, Grenadier, Pillager, ShockTrooper, Punisher, SkullCrusher, Headsman, Warden, Scout, Recon, Bonemaker, Marauder, Rifleman, Ambusher, Marksman, Raider, Front Sniper, Veteran, Mercenary, MercSniper, Gunner, GMPG, VeteranGunner, MercGunner, все Leader, Mortarman, Skirmisher (см. выше).

## Требования

- `JAZZ-AI-ROLE-004-REQ-001` — `JazzAI_InferRoleFamily` (и fallback `JazzAI_UnitRoleFamily` в `CombatAI.lua`): `Gunner`/`Machinegun` **до** `Assault`; `Flanker` до остальных; `Heavy`/`Mortar`/`Rocketeer` до общих токенов. `AssaultGunner` → семья `MG`.
- `JAZZ-AI-ROLE-004-REQ-002` — `PickCombatStance` для семьи `MG` не переписывает archetype в Assaulter/Flanker. Коммандо остаётся `Legion_Machinegunner`, пока не Melee по REQ-003.
- `JAZZ-AI-ROLE-004-REQ-003` — `JazzAI_NeverMelee`: MG/Heavy/Leader как сейчас, **кроме** юнита с keyword `CQB` и alt melee (Коммандо). Фланговый снайпер остаётся NeverMelee.
- `JAZZ-AI-ROLE-004-REQ-004` — фланговый снайпер: default Flanker; cover-hold не схлопывает в Frontliner; не становится Assaulter; SNIPER-001 без изменения предиката keywords; 008 perch не расширять на Scout.
- `JAZZ-AI-ROLE-004-REQ-005` — фланговый снайпер с alt CQB-стволом и ближайшим врагом ≤ 10 тайлов: `ChangeWeapon` на этот ствол, вернуть `Legion_Flanker` (не Melee, не Assaulter). Дальше 10 тайлов — активный снайперский/винтовочный ствол.
- `JAZZ-AI-ROLE-004-REQ-006` — Scout без Sniper/Marksman: Assaulter только при aura `pusher`. Сужает ROLE-002-REQ-002.
- `JAZZ-AI-ROLE-004-REQ-007` — recipe+generate Pathfinder, Ranger и Crusher по таблице кита; `CustomEquip` Рейнджера находит `SniperRifle` в сгенерированном луте.
- `JAZZ-AI-ROLE-004-REQ-008` — Rocketeer `archetype`/`RepositionArchetype` = `Legion_Frontliner` в companion и `items.lua`. Семья Heavy: `PickCombatStance` не ставит Assaulter/Flanker. Resolve при дыре: Rocketeer → `Legion_Frontliner`, Mortarman → `Artillery`, **не** Assaulter. `Artillery` не назначать ракетчику.
- `JAZZ-AI-ROLE-004-REQ-009` — Pyro/Crusher/HeavyGrenadier keywords+CustomEquip по таблице кита; Crusher recipe `melee` не `null`; items+companions одна транзакция.
- `JAZZ-AI-ROLE-004-REQ-010` — досье Рейнджер и Следопыт в `_ris_copy_bank.py` + editorial apply; RU/EN тот же смысл.
- `JAZZ-AI-ROLE-004-REQ-011` — `_audit_ris_ai_claims.py`: FAIL если `AssaultGunner` не MG; если Pathfinder/Ranger recipe без sniper/rifle primary; если Rocketeer не `Legion_Frontliner` или стоит `Artillery`.
- `JAZZ-AI-ROLE-004-REQ-012` — голый высокий dest без выстрела: вклад HighGround в `AIScoreDest` ≤ 0 (не лезть «посмотреть»).
- `JAZZ-AI-ROLE-004-REQ-013` — голый высокий dest + живой союзник same-Z <2 тайла: POL-004 danger +50 (после обычных живых/casualty). Medic exempt как POL-004.
- `JAZZ-AI-ROLE-004-REQ-014` — `MapVar JazzAI_HeightHysteresis`: 2 хода после спуска без положительного HighGround на подъём, кроме укрытого dest с выстрелом. Без RNG. Clear CombatStart. Не сейвится между боями.

## Инварианты и ограничения

- Determinism: только уже используемые `unit:Random` / `InteractionRand`; смена ствола без нового RNG.
- Не ломать ROLE-001 Flanker presets и POL-001 TakeCover weights.
- Не второй wrap на `SelectArchetype` / `PickCustom`.
- Generate не трогает чужие 34 recipe.
- Public UnitData ID без rename.
- Сейвы: следующий StartAI; новый лут — новая генерация отряда / `[no new game]` для stance, `[new game recommended]` если уже заспавненный Рейнджер без снайперки.
- `JazzAI_HeightHysteresis` только на время боя; не GameVar.

## Acceptance criteria

- `JAZZ-AI-ROLE-004-AC-001` — static: `AssaultGunner` → family `MG`; в `PickCombatStance` нет ветки Pusher для этого id; `_audit_ris_ai_claims.py` exit 0 по семье.
- `JAZZ-AI-ROLE-004-AC-002` — static: `NeverMelee` false для MG+CQB+alt melee; true для GMPG/Gunner/фланговых снайперов.
- `JAZZ-AI-ROLE-004-AC-003` — static: helper смены CQB для Scout+Sniper/Marksman; порог 10 тайлов; return Flanker.
- `JAZZ-AI-ROLE-004-AC-004` — static: Pathfinder/Ranger recipe primary содержит `sniper` или `rifle`; Ranger `CustomEquip` SniperRifle; Crusher recipe `melee` не `null` и sidearm 55/unlock 12; generate `--validate-only` зелёный на этих id.
- `JAZZ-AI-ROLE-004-AC-005` — static: Rocketeer archetype `Legion_Frontliner` в companion и items; не `Artillery`; Mortarman остаётся `Artillery`.
- `JAZZ-AI-ROLE-004-AC-006` — static: Pyro без `Melee`; Crusher **с** `Melee`+`CQB` и `CustomEquip` Shotgun / Pistol затем MeleeWeapon; HeavyGrenadier без `Sniper`.
- `JAZZ-AI-ROLE-004-AC-007` — static: банк досье Рейнджер/Следопыт — оптическая/глушёная винтовка, без «основной ствол = ПП/карабин»; `_audit_ris_copy.py` editorial OK.
- `JAZZ-AI-ROLE-004-AC-008` — runtime/human: Застрельщик на фланге с LOS держит клетку (SNIPER-001); без выстрела смещается по Flanker OptLoc, не в толпу Assaulter.
- `JAZZ-AI-ROLE-004-AC-009` — runtime/human: Рейнджер начинает со снайперки; враг ≤10 тайлов → карабин/ПП, archetype всё ещё `Legion_Flanker`.
- `JAZZ-AI-ROLE-004-AC-010` — runtime/human: Коммандо ставит LMG (MGSetup), в AP-reach мачете; не бегает как Assaulter весь бой.
- `JAZZ-AI-ROLE-004-AC-011` — docs: `ai-awareness.md` + `legion-units-equipment-tiers.md` отражают семью MG для Коммандо, кит Pathfinder/Ranger/Crusher, матрицу переключения и крыши.
- `JAZZ-AI-ROLE-004-AC-012` — static: HighGround climb gate (голый + нет выстрела → ≤0); +50 danger same-Z <2; hysteresis MapVar + CombatStart clear. Gate `docs/tools/_check_role004_roofs.py`.
- `JAZZ-AI-ROLE-004-AC-013` — runtime/human: два стрелка не встают рядом на голой крыше; после спуска тот же юнит не лезет обратно на следующий ход (без укрытия+выстрела).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: правка порядка токенов в jazz-units + зеркало fallback в jazz `CombatAI.lua`; generate лута в jazz-units.
- Saves: stance `[no new game]`; лут Рейнджера/Следопыта/Громилы — уже заспавненные отряды со старым китом до регена.
- Network/determinism: без нового RNG.
- Generated data: recipe → generate → `items.lua` LootDef + UnitData/items sync.
- Cross-package: RIS copy в `jazz`; UnitData в `jazz-units`. Maps не трогаем.
- Rollback: revert ROLE-004 diff + recipe generate revert.

## План и ownership

- Пакет-владелец данных: `jazz-units` (stance, UnitData, loot); recipe+RIS+docs: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: см. frontmatter.
- Exclusive resources: `jazz-units/items.lua`, `metadata.lua`, `recipes.json`.

## Решение владельца

- Статус: **draft** — ждёт approve.
- Кто подтвердил: pending.
- Дата: 2026-09-08.
- Уже зафиксировано владельцем до текста спеки: Застрельщик и Рейнджер — фланговые снайпера (досье приоритетнее «убрать hold»).
- 2026-09-08: избегать скученности на крышах без укрытий; не прыгать крыша↔земля.
- 2026-09-08: ракетчик — `Legion_Frontliner` (РПГ с линии). Не Assaulter (не пушить). Не `Artillery` (это миномётчик).
- 2026-09-08: Громила — не снимать `Melee`. Вторичка слота B: **шанс нож или пистолет** (не гарантированный пистолет, не «ложный Melee»).

## Evidence

- `JAZZ-AI-ROLE-004-AC-001`: `BLOCKED` — нет реализации.
- `JAZZ-AI-ROLE-004-AC-002`: `BLOCKED` — нет реализации.
- `JAZZ-AI-ROLE-004-AC-003`: `BLOCKED` — нет реализации.
- `JAZZ-AI-ROLE-004-AC-004`: `BLOCKED` — нет реализации.
- `JAZZ-AI-ROLE-004-AC-005`: `BLOCKED` — нет реализации.
- `JAZZ-AI-ROLE-004-AC-006`: `BLOCKED` — нет реализации.
- `JAZZ-AI-ROLE-004-AC-007`: `BLOCKED` — нет реализации.
- `JAZZ-AI-ROLE-004-AC-008`: `BLOCKED` — runtime.
- `JAZZ-AI-ROLE-004-AC-009`: `BLOCKED` — runtime.
- `JAZZ-AI-ROLE-004-AC-010`: `BLOCKED` — runtime.
- `JAZZ-AI-ROLE-004-AC-011`: `BLOCKED` — docs after implement.
- `JAZZ-AI-ROLE-004-AC-012`: `BLOCKED` — нет реализации.
- `JAZZ-AI-ROLE-004-AC-013`: `BLOCKED` — runtime.

## Documentation delta

После implement (не сейчас): `ai-awareness.md` (семья, матрица switch, flanking sniper, крыши/гистерезис); `legion-units-equipment-tiers.md` (Pathfinder/Ranger tags, Rocketeer archetype, AssaultGunner family, Crusher knife/pistol); `docs/design/legion-loadouts.md` строка Crusher (Melee = knife%); `ris-legion-dossiers.md` review row; `tactical-ai-archetypes.md` F2 + HighGround. Wiki/showcase tactical-ai — крыши без укрытия и отсутствие прыжков крыша↔земля видны игроку.
