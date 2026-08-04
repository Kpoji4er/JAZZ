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
- `Code/System_AME_Filters.lua`, `System_AME_Browser.lua`, `System_AME_Market.lua`, `System_AME_Browser_Template.lua`, `System_AME_Nationalities.lua` — African Mercenary Exchange (UNITS-005): PDA mode `ame`, market tick, nationality flags;
- `Code/System_OR_Unit.lua`, `System_UnitInventory.lua`, `System_UnitAppearance.lua` — runtime schema;
- `Code/System_IMP_StartingGear.lua` — JA2-style динамический стартовый экип IMP (`JazzBuildImpStartingGear` / `JazzApplyImpStartingGear`);
- `Code/System_IMP_Perks.lua` — Mimicry/Veteran dialogue+skill hooks, `ImpGetPersonalPerks` wrap, sanitize `ImpCalcAnswers` tactical (drop `perk=false` slots), personal row HList spacing 12 (not HWrap — stole clicks from tactical Grid).

`Code/AimHiringScreen_Template.lua` существует в core, но не указан в metadata и не загружается. Не считать его активным XTemplate. Фактический UI изменяется generated XTemplate/загруженным кодом.

## IMP (JAZZ-IMP-001)

Hire path: `CreateImpMercData(sync)` после статов/перков очищает инвентарь и собирает кит по таблице [docs/design/imp-starting-gear.md](../../design/imp-starting-gear.md). Campaign-init `IMP_equipment_basic` (jazz-units) — только placeholder (бинты).

Personality pool extras: `Jazz_Perk_Mimicry` (dialogue Negotiator/Scoundrel/Psycho), `Jazz_Perk_Veteran` (+10 SkillCheck/RollSkillCheck/UnitHasStat), `Jazz_Perk_Sniper` (`OnCalcMaxAimActions` +1).

## Снимок generated data

`jazz-units`:

- ~239 `UnitData` (включая `JAZZ_AME_01`…`60`);
- ~261 appearance presets (Legion/handcrafted + **41** generated `JAZZ_JA12` + 60 AME; snapshot);
- 73 enemy squad definitions (включая четыре `LegionGlobalAI_*` role presets пилота Global AI);
- 40 AI archetypes;
- 1257 `LootDef`;
- 10 voice response presets и 2 translated voice presets;
- 2 enemy roles, 3 effects, combat action, banter и localization table.

Грубая faction taxonomy UnitData: 38 JAZZ Legion, 24 Army, 23 Adonis/Corazon, 22 Rebels/Militia, 22 Thugs; остальные относятся к mercenary, civilian, named/boss и служебным группам. Эти числа — snapshot и должны пересчитываться после Mod Editor regeneration.

## Прогрессия

`ExperienceTable.lua` расширяет таблицу уровней до 21. `ExperienceSys.lua` применяет опыт и level transitions. `StatGainRework.lua` использует систему points/thresholds и учитывает Wisdom при росте характеристик.

Публичные контракты:

- level и experience должны корректно сериализоваться;
- переход через несколько порогов не должен терять уровни/очки;
- max-level поведение не должно обращаться за отсутствующим порогом;
- random stat gain обязан использовать детерминированный механизм движка;
- UnitData initial stats и runtime instance stats нельзя смешивать.

## Специализации и AIM

Три specialization definitions: `Autoriflemen`, `HeavyWeapons`, `Stealth`. `SpecializationGiver.lua` назначает их указанным merc IDs после `DataLoaded`. AIM filters используют специализации для отбора/представления кандидатов.

Offline merc randomization детерминирован. Это означает, что замена RNG или порядка списка изменит состав доступных наёмников при том же seed/save. Любое изменение специализации требует обновить merc assignments, UI filters и локализацию вместе.

## African Mercenary Exchange (JAZZ-UNITS-005)

Отдельный PDA hire site (не вкладка внутри AIM):

| Контракт | Current-state |
|---|---|
| Org / Affiliation | `AME` |
| UnitData | `JAZZ_AME_01`…`JAZZ_AME_60` в `jazz-units` (`IsMercenary`, fixed `Loot_JAZZ_AME_NN`) |
| PDA mode | `ame` → `PDAAIMEBrowser` (subclass `PDAAIMBrowser`) |
| PDA URL | `http://www.ame-exchange.net/Roster/<Category>/<Nick>` — ASCII `urlSlug` (не `T`/локаль); wrap всегда поверх AIM `TFormat.PDAUrl` (иначе KindOf→AIM `ActiveFiles` + кириллица specialization) |
| Витрина | ~15 `Available` на старте; `NotListed` скрыты; terminal (`JoinedLegion`/`Killed`/…) — серые карточки |
| Tick | 30 дней кампании; specialist soft-guarantee |
| Hire | reuse `MercCanContact` → chat → `HireMerc` / `LocalHireMerc`; AME вне AIM contact-cap |
| VR | Pool: Jazz remesh (~1/4) + all 6 IMP UnitData (VR→`IMP_male_01`/`IMP_female_01`); Fallback remesh→Legion/Army/Anne, IMP→self (not Ice/Fox) |
| Heads | Safe Af bank only: `Chimurenga`/`Pierre`/`Jackhammer`/`Head_M_IMP_01`/`Faction_Rebels_M_HeadMedic` + female `Head_F_Af_NPC_*`; **not** Flay/Fidel/Magic/Blood/Fauda/Omryn; no `Faction_Legion_Head_*` ([ame-appearance-assets.md](../../design/ame-appearance-assets.md)) |
| Appearance | per-slot clone `JAZZ_AME_NN` ← Rebels/Militia/Legion (+ GrandChien Hardened/Spec); **1** blue cloth accent; `BodyColor` C1 dark African + `HeadColor` black; no Legion war-paint / no `GrandChien_Top_05` (pale hands); map [ame-appearance-map.json](../../design/ame-appearance-map.json) |
| PDA chrome | Savannah/ochre panel tints; `Icons/PDA/AME_Mark` (logo v4) instead of HazOS; AME banner pad (not AIM hiring banner); backdrop watermark. Edit `System_AME_Browser_Template.lua` → `_install_ame_xtemplate_moditem.py` |
| Nationality | reuse `GrandChien`/`SouthAfrica` + new `Nigeria`…`Ethiopia` (`System_AME_Nationalities.lua`, flags `Icons/Flags/f_*.png`) |
| Portraits | unique `MercPortraits/JAZZ_AME_NN.png` + `_Big` (300/2000) |
| Generator | `docs/tools/_gen_ame_unitdata.py` (+ roster/flags/portrait tools) |

Design roster: [ame-roster-60.md](../../design/ame-roster-60.md), companion [ame-mercenary-exchange.md](../../design/ame-mercenary-exchange.md). AIM mode `aim` не заменяется AME-скином.

## JA12 merc appearances (JAZZ-UNITS-002 gap fill)

Hireable `Jazz_*` UnitData уже ссылались на preset ids (`Colby`, `Blade`, `Ira`, …), многие из которых не были shipped. Current-state:

| Контракт | Current-state |
|---|---|
| Folder | `JA12_Appearances` в `jazz-units/items.lua` (`JAZZ-UNITS-002-JA12-APP-*`) |
| Group | `JAZZ_JA12` |
| Count | **41** generated + handcrafted (`Lynx`, `Buzz`, `Spider`, `Mike`, `Horg`, `Ivanov`, `JAZZ_Spouke`) + vanilla reuse (`Biff`, `Hitman`, `Shadow` for Simon) |
| Method | Prefer **faction/NPC/Thug/Civ body** + head swap, or pure AIM clone. **Avoid AIM×AIM** body/head mixes (poor mesh/neck compat). Same-gender only. |
| Hard gate | ♂/♀ Body/Head meshes never mixed |
| Map | [ja12-appearance-map.json](../../design/mercs-ja12/ja12-appearance-map.json) |
| Generator | `docs/tools/_gen_ja12_appearances.py` (+ `_audit_ja12_appearance_links.py`) |

`Jazz_Benny` → preset `Benny` (Fox female; previously wrongly pointed at `Lynx`).

## Имена элитных противников

`EliteEnemyNamesFuncs.lua` комбинирует first/last-name pools (`Legion.lua`, `Rebels.lua`, `Mercenary.lua`) и nicknames, затем регистрирует presets `EliteEnemyName` через `PlaceObj`. Группы JAZZ: `Legion`, `Rebels`, `Mercenary`. Bare first-name без last — намеренная часть пула. Отдельного пула `Foreigners`/Adonis пока нет (Adonis elite остаются на vanilla-группе `Foreigners`).

Контракт имени: поле `EliteEnemyName.name` имеет `translate = true` и хранится как `T(...)` или составной `T{ 890000000001650, "<first> <last>", first = ..., last = ... }` с вложенными T (без bake на регистрации — иначе английский CSV не применяется). При выдаче имени `GenerateEliteUnitName` копирует preset в `unit.Name`; **T с args нельзя сериализовать** (`TToLuaCode` → `assert(not THasArgs(T))`), поэтому jazz-units сразу после выдачи (и ещё раз в `GatherSessionData`) запекает такие имена в `Untranslated(_InternalTranslate(...))`. Пресеты остаются локализуемыми; уже выданные имена фиксируются на языке UI на момент выдачи/сейва.

Дедуп пула идёт по localization id / структуре `T{...}` (не по `_InternalTranslate`), чтобы размер пула не зависел от языка загрузки. Порядок preset id `JazzMerc_<Group>_NNN` детерминирован индексом списка. Уже выданные имена в existing save могут остаться старыми запечёнными строками до нового elite spawn.

Канонический runtime-перевод — `jazz/English.csv` и `jazz/Russian.csv` (все active mod-only ID комплекта, включая пулы имён и format ID). `jazz-units/English.csv` — файл, на который указывает units `metadata.loctables`; содержимое согласовано с каталогом основного пакета.

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