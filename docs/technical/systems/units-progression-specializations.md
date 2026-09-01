# Юниты, прогрессия и специализации

## Назначение и эффект для игрока

Пакет `jazz-units` задаёт составы фракций, ~239 UnitData (в т.ч. 60 AME), внешность, экипировку, loot, squads и AI archetypes. Ручной код core/units назначает специализации, расширяет уровни, меняет рост характеристик и создаёт имена элитных противников. AIM UI фильтрует наёмников по новой ролевой модели.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | UnitData, Mercenary, enemy squads, AI archetypes, experience/stat gain, AIM hiring UI и appearance systems |
| CommonLib | Даёт общую mod infrastructure; прямых одноимённых коллизий с восемью units Code modules в проверенном срезе не подтверждено |
| JAZZ | Массово заменяет/generated UnitData и squads, добавляет роли/keywords, опыт до 21 уровня, stat gain, имена и AIM filters |

## Реализация и load-state

Все восемь `jazz-units/Code` файлов загружаются:

- `AIKeywords.lua` — новые AI keyword definitions;
- `EliteEnemyNamesFuncs.lua` — генерация имён;
- `ExperienceSys.lua` — runtime опыта;
- `ExperienceTable.lua` — пороги уровней;
- `Legion.lua`, `Mercenary.lua`, `Rebels.lua` — faction/unit-specific setup;
- `StatGainRework.lua` — очки и рост характеристик.

В `jazz` загружаются:

- `Code/SpecializationGiver.lua` — назначение специализаций на `DataLoaded`;
- `Code/System_AimHiringFilters.lua` — фильтры AIM и детерминированный offline randomization;
- `Code/System_HireContractDuration.lua` — AIM/AME messenger `MaxDuration` 14→30;
- `Code/System_AME_Filters.lua`, `System_AME_Browser.lua`, `System_AME_Market.lua`, `System_AME_Mail.lua`, `System_AME_Browser_Template.lua`, `System_AME_Nationalities.lua` — African Mercenary Exchange (UNITS-005 / UI-AME-001): PDA mode `ame`, market tick, welcome/listing Email, tab lock until welcome read, nationality flags;
- `Code/System_MERC_Filters.lua`, `System_MERC_Account.lua`, `System_MERC_Browser.lua`, `System_MERC_Mail.lua`, `System_MERC_World.lua`, `System_MERC_Browser_Template.lua` — M.E.R.C. (UI-MERC-001 / UI-MERC-002): PDA mode `merc` locked until Day-2 Speck mail, credit account (wrap `PDAMessengerClass:CanAffordMerc` for MERC so Offer works without prepaid cash; refund prepaid on `MercHired` + waive medical deposit flag; **Pay Account** via ActionBar `P` + roster strip button → `JAZZ_MERC_PayAccount`), world-gated Biff/Larry/Smiley; unpaid clock 7d + 3d grace; satellite chip `idJazzMERCDebt` next to money (`MERC $X`, yellow then red); day-7 / day-9 `WaitPopupChoice` (Pay / Later); quit CombatLog names + `MERC_QuitWarning`; wrap `PDAMoneyText:Open` install-once; `JAZZ_MERC_OpenSite`; time track `jazz_merc_debt` (`jazz-merc-reminder` + `jazz-merc-quit`, AIM contract icon, RMB opens site);
- `Code/System_OR_Unit.lua`, `System_UnitInventory.lua`, `System_UnitAppearance.lua` — runtime schema;
- `Code/System_IMP_StartingGear.lua` — JA2-style динамический стартовый экип IMP (`JazzBuildImpStartingGear` / `JazzApplyImpStartingGear`);
- `Code/System_IMP_Perks.lua` — Mimicry/Veteran dialogue+skill hooks, `ImpGetPersonalPerks` wrap (Mimicry+Veteran only), sanitize `ImpCalcAnswers` tactical (drop `perk=false` slots), personal row HList spacing 12 (not HWrap — stole clicks from tactical Grid), tactical specialization Grid **6 columns** + HSpacing 18 so Sniper stays on 2 rows (no Prev/Done overlap).
- AIM PDA filters: `System_AimHiringFilters` stores `Specialization.icon`; `PDAAIMBrowser` uses `item.icon` (avoids missing `UI/Icons/hf_<specId>`).

`Code/AimHiringScreen_Template.lua` существует в core, но не указан в metadata и не загружается. Не считать его активным XTemplate. Фактический UI изменяется generated XTemplate/загруженным кодом.

## IMP (JAZZ-IMP-001)

Hire path: `CreateImpMercData(sync)` после статов/перков очищает инвентарь и собирает кит по таблице [docs/design/imp-starting-gear.md](../../design/imp-starting-gear.md). Campaign-init `IMP_equipment_basic` (jazz-units) — только placeholder (бинты).

Personal (Personality) pool extras: `Jazz_Perk_Mimicry` (dialogue Negotiator/Scoundrel/Psycho), `Jazz_Perk_Veteran` (+10 SkillCheck/RollSkillCheck/UnitHasStat; icon `OldDog`). Tactical (`Perk-Specialization`) extra: `Jazz_Perk_Sniper` (`OnCalcMaxAimActions` +1; icon `Deadeye`). Certificate UI lists all `Perk-Specialization` presets in the tactical grid (vanilla Teacher/MrFixit/Throwing/… plus Sniper).

## Named perks (JAZZ-UNITS-006)

Loaded code: `System_NamedPerks.lua` (UNITS-006 batches 1–6 merged; ModItemCode `System_NamedPerks`). Tunables live on ModItem `Parameters` (editor); runtime reads via `Jazz_NamedPerkParam` / `ResolveValue`. Vanilla Gus `WeGotThis` (`OnUnitKill`) indexes `gv_Squads[target.Squad]` with no nil check; NPC villains (Ghost / MercenaryCaptain / ErnyVillage_Boss) copy the perk with `Squad=false` → debug assert. JAZZ patches the handler: satellite squad if present, else living `team.units`, and skips missing `g_Units[id]`.

§B batch4 (static): Flo/Static/Cougar + Grace/Kulba/Grom/Ricochet/Highball (see `_units006_batch4_notes.md`).

§ HARD/satellite batch5 (static):

- `Jazz_Perk_Rothman` — mine garrison loyalty-scaled income (`_GetMineIncome` +10…+40%).
- `Jazz_Perk_Miguel` — aura 30 via `Jazz_MiguelAuraUp`/`Down` (±15 CTH, ±30 Will).
- `DesignerExplosives` (Barry) — homemade **vanilla** `ShapedCharge`: every **168 h** produce **2×**; craft via Craft Explosives; CraftAmmo/CraftExplosives **Parts −30%** (recipe list, enable-check, queued total, and consume) if Barry is in the sector (assigned to craft **or** Idle). TNT/C4/BlackPowder/Meds unchanged. Helpers in `System_NamedPerks.lua`; consume/UI wraps in `System_SectorOperations.lua`.
- `Jazz_Perk_Meat` — Will dmg → Grit; skip suppression queue.
- `Jazz_Perk_Carlos` — detection −33%; failed SK 50% keep Hidden.
- `Jazz_Perk_Cord` / `Jazz_Perk_Conrad` — city repair time/Parts; trainer Leadership floor 90.
- В бою `Leadership` союзника в радиусе **&lt; 11** клеток ускоряет восстановление `WillPoints` в начале хода цели (`Unit:RecalcWillPoints`; берётся Max-вклад, не сумма). Формула — [броня и воля](armor-damage-wounds-will.md).
- Soft: Biff trooper economy, Ira militia call-site, Livewire money op (ECON-001) — `_units006_batch5_notes.md`.
- **Igor `Nazdarovya`:** signature (2 AP, `recharge_on_kill=1`): clear Pain, heal 15–20 HP, `Drunk` stacks ≤5 (−15 ranged CTH / +20 flat melee per stack); sat `OnNewHour` removes 1 stack / 3 h (`RemoveOnEndCombat=false`).
- **Thor `NaturalHealing`:** every **48 h** produce **1× HerbalMedicine** (joints); same sat squad — trauma/burn check intervals and HP/TreatWounds debt recovery **+15%** faster (`sat_debt_speed_percent`; **not** `WoundInfected`); bandage by Thor restores patient **WillPoints 20–25**.
- **Scope `HawksEye`:** sniper Overwatch **1 AP** (keep leftover); PinDown min 1 AP + `Exposed`; sniper Will suppress **×2**; biscuits every **96 h ×7** (`Cookie`) plus hire Cookies × days.
- **Fauda `KillingWind`:** `Jazz_KillingWindTryGrit` once on aggregate firearm `results` (`ExecFirearmAttacks` after per-shot `OnAttack`) and CE `OnUnitAttack` for melee/other — count enemies via `unit_damage` / `hit_objs` (Unit or `{obj=…}`) / `area_hits` / `killed_units` / nested `attacks` (≥2 → **+8 Grit × count**; default if ResolveValue nil; **not** gated on `results.miss`); armor FM penalty −50% (with Ironclad: 0); BeginTurn grants FreeMove even with cumbersome; MGPack refreshes FreeMove then re-taxes armor once.
- **Fidel `DoubleToss`:** signature throws two from the same grenade stack (≥2); hands (`DoubleTossA–D`) **or** grenade pockets `GrenadesInventory` (`DoubleTossAG–DG`).
- **Grunty `GruntyPerk_JAZZ`:** Passive CA + HUD `perk_grunty_perk`; combat start → `Grunty_AdditionalAP` (+50% max AP, one turn); later turns proc at `10% × max(0, GetPersonalMorale())` with CombatLog of morale/chance/roll.
- **Lynx / Buzz / Spider / Colby Passive CA icons:** hotbar `CombatAction.Icon` → `Perks/SignatureAbilities/Jazz_Perk_*.png` (**54×54** cool blue, `SetColumns(1)`). CE perk tiles stay `Perks/Personal/*.png`. Lynx keeps glowing eyes (`docs/tools/_build_lynx_sig_icon_glow.py`); siblings via `_build_passive_signature_icon_54.py`.
- **DrQ `ExplodingPalm`:** Passive hotbar (54×54); **`Unit:OnAttack` wrap** + CE `OnUnitAttack` → HP-tier statuses on unarmed hit (≤20 KO, ≤35 Concussion, ≤50 Ribs Med, ≤65 Arms Med, ≤80 Legs Med, else Ribs Light+Pain); sat squad trauma/burn/HP debt **+30%**; **blocks** `WoundInfected`. Combat start refreshes perk reactions (stale vanilla CE).
- **Flay `MakeThemBleed`:** +10% damage per **visible enemy** with any `Bleeding`/`BleedingMedium`/`BleedingHeavy` (not stacks), cap +50%; HUD buff `Jazz_MakeThemBleedBuff` shows count (1…5 stacks).
- **Larry / Larry_Clean `DangerClose`:** explosives (grenade/ordnance) impact ≥**8** tiles → **+40%** explosion damage; every unit hit by his blast gets **+2** light `Bleeding` stacks; `OnCalcStimmedTiredness=0` + clears Stimmed CTH penalty. Runtime replaces vanilla `ExplosionPrecalcDamageAndStatusEffects` (nil-safe; grenade aim no longer dies on missing `rangeThreshold`). HUD “in range” at ≥8.
- **PierreMerc `GloryHog`:** vanilla machete **Charge** (non-straight path via `action_id == "GloryHog"`) +**15** Grit (`Unit:GloryHogCharge`); List2 active `Jazz_PierreRecruit` (4 AP): once/combat convert a **visible** non-boss (`villain`/`ImportantNPC`) enemy to side `ally` (AI). Hotbar inject when `HasPerk(GloryHog)`. Recruit: **one** signature button → HUD `ShowCombatActionTargetChoice` (talk icon; one visible enemy auto-executes). Not `IModeCombatAttack` (that left a stuck command layer). Icon `UI/Icons/Hud/talk` (Charge keeps `perk_glory_hog`).
- **Smiley `RecklessAssault`:** improved mobile attack — **4** volleys (`mobile_num_shots`), weapons **SMG / Carbine / AssaultRifle** (`Jazz_RecklessAssaultGetWeapon`); **+15** CTH via CE `OnCalcChanceToHit`; `Unit:RecklessAssault` no longer calls `SetTired`; **`recharge_on_kill=1`** (same as JAZZ `RunAndGun` — `Unit:RunAndGun` → `AddSignatureRechargeTime`).
- **Reaper `TheGrim`:** stock crit + Panic ≤8 on signature kill; CD needs **5** kills (`Jazz_TheGrimKillsToRecharge`; `g_PresetParamCache.recharge_on_kill=5` via `Jazz_EnsureTheGrimRechargeOnKill`; multi-kill hold in `UpdateSignatureRecharges`). Tooltip shows `done/need`.
- **Vicki `WeaponPersonalization` (Elbow Grease):** vanilla `OnNewHour` still writes `Condition` +1%/h on equipped armor and handheld repairables. JAZZ `Jazz_WeaponPersonalizationTick` also restores **current** `WeaponResource` / `ArmorResource` by the same percent of max (does not restore lost max). Inventory `%` uses `GetConditionPercent`, not the stale `Condition` field. The wear keyword (изношенное / rusty) stays max-vs-factory.

§D batch6: `Jazz_Perk_Benny` / `Jazz_Perk_Simon` CE + StartingPerks; CombatAction soft-cut (`_units006_batch6_notes.md`).

## Снимок generated data

`jazz-units`:

- ~239 `UnitData` (включая `JAZZ_AME_01`…`60`);
- 263 appearance presets (Legion/handcrafted + **45** generated `JAZZ_JA12` + 60 AME; snapshot);
- 73 enemy squad definitions (включая четыре `LegionGlobalAI_*` role presets пилота Global AI);
- 40 AI archetypes;
- 1257 `LootDef`;
- 10 voice response presets и 2 translated voice presets;
- 2 enemy roles, 3 effects, combat action, banter и localization table.

Грубая faction taxonomy UnitData: 38 JAZZ Legion, 24 Army, 23 Adonis/Corazon, 22 Rebels/Militia, 22 Thugs; остальные относятся к mercenary, civilian, named/boss и служебным группам. Эти числа — snapshot и должны пересчитываться после Mod Editor regeneration.

## Прогрессия

`ExperienceTable.lua` расширяет таблицу уровней до 21. `ExperienceSys.lua` применяет боевой/квестовый XP только к **уровню** (`ReceiveStatGainingPoints` больше не наполняет `statGainingPoints`). `StatGainRework.lua` (JAZZ-UNITS-009, static): у каждого навыка свой skill XP. Порог `T(s)`: 150 / 250 / 400 / 800 до 80, далее геометрия ×1.5 (`T(80)=1600`, `T(90)=92267`, `T(99)=3547083`). Мудрость линейно 0…100 (`MulDivRound(awarded, Clamp(Wis,0,100), 60)`; Wis 0 = 0 практики). Книги (`Studying`) и секторный тренинг (`Training`) — прямой ванильный `GainStat` в `jazz/Code/System_OR_Unit.lua` (лог «Обучение» / «Практический опыт»); jazz-units **не** оборачивает `GainStat`. Overflow практики зовёт `GainStat(..., "FieldExperience")`. Капли Wisdom и сброс шкалы после книги/тренинга — `OnMsg.StatIncreased`. UI v1: у нанятого в ролловере стата `Практика: xp / T(s)` (ванильный help не заменяется). AIM-карточки найма — `function MercStatsItems` (help сплющивается в `Untranslated`, иначе вложенный `T` в `<help>` не доходит до игрока). Анкета с полосками (`PDAAttributeBar` / `PDAAttributeRollover`) — `XContextWindow:GetRolloverText`; ряды Обучение / Studying / Практический опыт не трогаются. Повторная установка: file-load, `Autorun`, delayed RealTimeThread. Боевой скейл капель ×3.5/×4 **не** включён (открытый выбор владельца). Runtime AC ещё не закрыты.

Публичные контракты:

- level и experience должны корректно сериализоваться;
- переход через несколько порогов не должен терять уровни/очки;
- max-level поведение не должно обращаться за отсутствующим порогом;
- рост навыка с практики детерминирован (нет `InteractionRand` на +1); книги/тренинг остаются плоским +1;
- UnitData initial stats и runtime instance stats нельзя смешивать.

## Специализации и AIM

Три specialization definitions: `Autoriflemen`, `HeavyWeapons`, `Stealth`. `SpecializationGiver.lua` назначает их указанным merc IDs после `DataLoaded`. AIM filters используют специализации для отбора/представления кандидатов.

Offline merc randomization детерминирован. Это означает, что замена RNG или порядка списка изменит состав доступных наёмников при том же seed/save. Любое изменение специализации требует обновить merc assignments, UI filters и локализацию вместе.

**Срок контракта (AIM + AME chat):** vanilla `AIMHiringScreen` / messenger slider `MaxDuration = 14`. JAZZ `System_HireContractDuration.lua` wraps `GetNextMercConversation` **and** `PDAMessengerClass:SetupUIForChat` (resume path) и поднимает `MaxDuration` **14 → 30** сразу (с day 1); min остаётся 3, default offer по-прежнему ~7 via `GetMercMinDaysCanAfford`. Duration-refusal ветки с `MaxDuration = 7` не трогаются. AME и AIM делят один `StartMercChat` path — отдельного AME hire-duration cap нет. Это **не** AME market tick (`AME_TICK_DAYS = 14`).

**Скидка за срок (`GetMercDurationDiscountPercent`):** vanilla линейно 3–14 → до 25% (`normal`) / 7–14 → до 35% (`long only`); при `days > 14` возвращает **0%**. Тот же `System_HireContractDuration.lua` подменяет функцию: окно растянуто до **30** дней (те же пики %), чтобы длинный контракт не откатывался на полную суточную ставку.

## African Mercenary Exchange (JAZZ-UNITS-005)

Отдельный PDA hire site (не вкладка внутри AIM):

| Контракт | Current-state |
|---|---|
| Org / Affiliation | `AME` |
| UnitData | `JAZZ_AME_01`…`JAZZ_AME_60` в `jazz-units` (`IsMercenary`, fixed `Loot_JAZZ_AME_NN`) |
| PDA mode | `ame` → `PDAAIMEBrowser` (subclass `PDAAIMBrowser`) |
| PDA URL | `http://www.ame-exchange.net/Roster/<Category>/<Nick>` — ASCII `urlSlug` (не `T`/локаль); wrap всегда поверх AIM `TFormat.PDAUrl` (иначе KindOf→AIM `ActiveFiles` + кириллица specialization) |
| Витрина | ~15 `Available` на старте; `NotListed` скрыты; terminal (`JoinedLegion`/`Killed`/`HiredElsewhere`) — серые карточки с конкретной причиной ухода |
| Tick | **14** дней кампании (2 недели); отдельные missing-cycle counters гарантируют возврат Medic / Instructor / Sniper не позднее следующего tick, пока в пуле есть не-terminal кандидат этой роли; окно после ротации остаётся у цели **15 Available** |
| Mail / lock | `System_AME_Mail.lua` (UI-AME-001): одно welcome-письмо + письма при реальной смене листинга; tab `ame` **always unlocked** (mail informational) |
| Hire | reuse `MercCanContact` → chat → `HireMerc` / `LocalHireMerc`; AME вне AIM contact-cap; contract slider max **30** days + duration discount peak at **30** (`System_HireContractDuration`, shared with AIM) |
| VR | Pool: Jazz remesh majority (`Male_Low`/`Male_Hard`/`Female`) + `PierreMerc` (~10%) + small IMP minority (~12%; VR→`IMP_male_01`/`IMP_female_01`); Fallback remesh→Legion/Army/Anne, IMP/PierreMerc→self (not Ice/Fox). Shared banks отбрасывают Legion/Major/Grand Chien faction calls; EN subtitle совпадает с audible donor line, RU переводит именно услышанную фразу через `_ame_voice_subtitles_ru.py`, а не gameplay slot. |
| Heads | Safe Af bank only: `Chimurenga`/`Pierre`/`Jackhammer`/`Head_M_IMP_01`/`Faction_Rebels_M_HeadMedic` + female `Head_F_Af_NPC_*`; **not** Flay/Fidel/Magic/Blood/Fauda/Omryn; no `Faction_Legion_Head_*` ([ame-appearance-assets.md](../../design/ame-appearance-assets.md)) |
| Appearance | per-slot clone `JAZZ_AME_NN`; **Legion clothing canon** = jazz-units handcrafted `Legion*` (not vanilla `Legion_*`); shuffle Rebels + `Legion*` + GrandChien + keep (Irregulars lean `Legion*`); **1** blue accent on **shirt/torso** (not Hat/Hat2); preserve Af Head + BodyC1 + HeadColor; no war-paint heads/tops / no `GrandChien_Top_05`; strip helmets/turbans/`FactionMale_Hat`/`Equipment*_Hat` (keep mask/scarf/glasses/headband); ♀ Hair = `NPCFemale_Hair_*` only, empty if Hat/Hat2 set; map [ame-appearance-map.json](../../design/ame-appearance-map.json); policy [ame-appearance-assets.md](../../design/ame-appearance-assets.md) |
| Personality | sparse **12/60**: one of `Negotiator`/`Scoundrel`/`Psycho`/`Stealthy`/`Optimist`/`Pessimist`/`Loner` in `StartingPerks` (map in `_gen_ame_roster_60.py` / `_apply_ame_personality_traits.py`); no Mimicry/Veteran; Loadout Traits strip still hidden |
| PDA chrome | Savannah/ochre panel tints; `Icons/PDA/AME_Mark` (logo v4) instead of HazOS; AME banner pad (not AIM hiring banner); backdrop watermark. Edit `System_AME_Browser_Template.lua` → `_install_ame_xtemplate_moditem.py`. Профиль показывает `AMECategory` и вычисляемый из Wisdom `Potential`; Loadout omits Traits/Perks strip (Equipment/Backpack only); AIM unchanged. |
| My Team | AME-фильтр считает и показывает только нанятых с `Affiliation == "AME"`; общий AIM `My Team` по-прежнему может показывать любого наёмника игрока |
| Specialization | Line troops (`Irregulars`/`Fighters`/`Hardened`): only `AllRounder` · `Autoriflemen` · `HeavyWeapons` · `Marksmen`. Soft icons `Doctor`/`Mechanic`/`ExplosiveExpert`/`Leader` only on Specialists. Patch helper: `_patch_ame_specializations.py`. |
| Nationality | reuse `GrandChien`/`SouthAfrica` + new `Nigeria`…`Ethiopia` (`System_AME_Nationalities.lua`, flags `Icons/Flags/f_*.png`) |
| Portraits | unique `MercPortraits/JAZZ_AME_NN.png` + `_Big` (300/2000) |
| Copy / localization | `Bio`, hire-chat и nationality defaults — English source; `Russian.csv` / `English.csv` держат полные RU/EN проекции. 60 биографий — отдельные 3–4-фразовые портреты без названий статов/тиров; канон и применение: `_ame_copy_bank.py` + `_apply_ame_editorial.py`. |
| Portrait prompt bank | developer-only `jazz-units/MercPortraits/_ame_face_refs/`: 60 identity prompts generated by `docs/tools/_gen_ame_portrait_prompts.py`; excluded from the Steam package by `metadata.ignore_files` |
| Generator | `docs/tools/_gen_ame_unitdata.py` (+ roster/flags/portrait tools) |
| Salary (playtest 2026-08-05) | `StartingSalary` ≈ daily; **week ≈ ×7**. Irregular floor ~**$50**/wk; typical ~**$100–$1000**/wk; specialists up to ~**$2000**/wk and **below** Igor (`450`→`$3150`/wk) / Barry (`470`→`$3290`/wk). Current roster daily **7–286** (wk **~49–2002**). Apply/sync: `_apply_ame_weekly_salaries.py`, `_sync_ame_salary_items.py` |
| Starting level | Все 60 слотов начинают с **Level 1**; категория описывает исходный опыт, kit и stat profile, но не даёт бесплатные уровни |

Design roster: [ame-roster-60.md](../../design/ame-roster-60.md), companion [ame-mercenary-exchange.md](../../design/ame-mercenary-exchange.md). AIM mode `aim` не заменяется AME-скином.

> **Spec:** `JAZZ-UNITS-005-REQ-014` aligned to these weekly bands (2026-08-05); tick `REQ-011` = **14** days.

## JA12 merc appearances (JAZZ-UNITS-002 gap fill)

Hireable `Jazz_*` UnitData уже ссылались на preset ids (`Colby`, `Blade`, `Ira`, …), многие из которых не были shipped. Current-state:

| Контракт | Current-state |
|---|---|
| Folder | `JA12_Appearances` в `jazz-units/items.lua` (`JAZZ-UNITS-002-JA12-APP-*`) |
| Group | `JAZZ_JA12` |
| Count | **45** generated + external handcrafted (`Lynx`, `Buzz`, `Spider`, `Ivanov`, `JAZZ_Spouke`) + vanilla reuse `Biff` |
| Method | Prefer **faction/NPC/Thug/Civ body** + head swap; avoid pure hireable clones and AIM×AIM body/head mixes (poor mesh/neck compat). Same-gender only. |
| Hard gate | ♂/♀ Body/Head meshes never mixed; current static audit: `link_bad=0`, `gender_bad=0`, exact duplicate recipes `0` |
| Map | [ja12-appearance-map.json](../../design/mercs-ja12/ja12-appearance-map.json) |
| Generator | `docs/tools/_gen_ja12_appearances.py` (+ `_audit_ja12_appearance_links.py`) |
| 2026-08-07 correction | Distinct recipes for `Benny`/`Laura`, `Colby`/`Hobbit`, `Cougar`/`Vilde`; `Simon` now links to its own jacket/glasses/binocular preset rather than vanilla `Shadow` |
| Biff visual | Vanilla preset and assets: `Biff`, `UI/NPCsPortraits/Biff`, `UI/NPCs/Biff` |
| Portrait QA | Eight JA2-reference face corrections are in working-tree review; 300/2000 candidates and contact sheet live under `MercPortraits/_wip/ja12-facefix/`; owner acceptance remains pending |
| Hire chat | Actual opus audit: 50 mercs, 0 fully silent, 1 missing manual Lynx slot; eight repaired fallback mappings remain on human ear-check |

`Jazz_Benny` → preset `Benny` (female IMP tactical body + Fox head/hair; previously wrongly pointed at `Lynx`). `Jazz_Simon` → preset `Simon`; `JAZZ_Merc_Spouke` remains unchanged.

## Имена элитных противников

`EliteEnemyNamesFuncs.lua` комбинирует first/last-name pools (`Legion.lua`, `Rebels.lua`, `Mercenary.lua`) и nicknames, затем регистрирует presets `EliteEnemyName` через `PlaceObj`. Группы JAZZ: `Legion`, `Rebels`, `Mercenary`. Bare first-name без last — намеренная часть пула. Отдельного пула `Foreigners`/Adonis пока нет (Adonis elite остаются на vanilla-группе `Foreigners`).

Контракт имени: поле `EliteEnemyName.name` имеет `translate = true` и хранится как `T(...)` или составной `T{ 890000000001650, "<first> <last>", first = ..., last = ... }` с вложенными T (без bake на регистрации — иначе английский CSV не применяется). При выдаче имени `GenerateEliteUnitName` копирует preset в `unit.Name`; **T с args нельзя сериализовать** (`TToLuaCode` → `assert(not THasArgs(T))`), поэтому jazz-units сразу после выдачи (и ещё раз в `GatherSessionData`) запекает такие имена в `Untranslated(_InternalTranslate(...))`. Пресеты остаются локализуемыми; уже выданные имена фиксируются на языке UI на момент выдачи/сейва.

Дедуп пула идёт по localization id / структуре `T{...}` (не по `_InternalTranslate`), чтобы размер пула не зависел от языка загрузки. Порядок preset id `JazzMerc_<Group>_NNN` детерминирован индексом списка. Уже выданные имена в existing save могут остаться старыми запечёнными строками до нового elite spawn.

Канонический runtime-перевод — `jazz/English.csv` и `jazz/Russian.csv` (все active mod-only ID комплекта, включая пулы имён и format ID). `jazz-units` грузит `Russian.csv` и `English.csv` через `metadata.loctables`; содержимое — mod-only ID, согласованные с каталогом основного пакета. Ванильные фразы AIM (Raven/Thor/Vicki/Wolf) остаются на исходных T-ID `Game.csv`.

## Роли, keywords и экипировка

AI keywords перечислены в [AI-системе](ai-awareness.md). UnitData связывает faction, archetype, role, stats, perks, appearance, voice, inventory, loot и equipment. Изменение любого item/entity/action ID может сломать spawn unit даже без прямого Lua import.

### Легион

Current-state каталог 37 классов Легиона, шесть линий дизайна и независимая от класса прогрессия equipment tier описаны отдельно: [Легион: схема юнитов и тиры снаряжения](legion-units-equipment-tiers.md). Диаграмма задаёт таксономию и стрелки эскалации, а загружаемые UnitData/LootDef остаются runtime-источником истины.

## Межпакетные зависимости

- core предоставляет item/effect/action/class/slot IDs;
- assets предоставляет appearances, equipment entities и textures;
- maps размещает UnitData, squads, conversations и banters;
- units предоставляет core/strategy фактические squad/unit IDs.

Maps имеют прямые ссылки на units package; неполная установка не поддерживается.

## Проверка

- spawn по одному UnitData каждой faction/role/archetype;
- appearance, voice, inventory, loot и action availability;
- опыт на каждом пороге и скачок через несколько уровней до 21;
- stat gain при low/high Wisdom и около threshold;
- save/load level, XP, gained stats и generated elite name;
- специализации named mercs после new game/load/mod reload;
- AIM filters online/offline и повторяемость seed;
- все 37 `JAZZ_Legion_*` ID, их root equipment и ветви схемы;
- пороги `JAZZ_Legion_Tier`, deferred regeneration и non-Legion side effect текущей реализации;
- squad spawn/autoresolve/death/despawn;
- отсутствие missing item/entity/voice/archetype IDs.

## Ограничения и сопровождение

Generated UnitData/appearance/loot править через Mod Editor. Новый unit/archetype/keyword/specialization должен быть отражён в этой странице и профильной AI/strategy документации. `AimHiringScreen_Template.lua` остаётся dormant, пока metadata явно не изменена.