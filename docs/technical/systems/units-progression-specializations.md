# Юниты, прогрессия и специализации

## Назначение и эффект для игрока

Пакет `jazz-units` задаёт составы фракций, 179 UnitData, внешность, экипировку, loot, squads и AI archetypes. Ручной код core/units назначает специализации, расширяет уровни, меняет рост характеристик и создаёт имена элитных противников. AIM UI фильтрует наёмников по новой ролевой модели.

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
- `Code/System_OR_Unit.lua`, `System_UnitInventory.lua`, `System_UnitAppearance.lua` — runtime schema.

`Code/AimHiringScreen_Template.lua` существует в core, но не указан в metadata и не загружается. Не считать его активным XTemplate. Фактический UI изменяется generated XTemplate/загруженным кодом.

## Снимок generated data

`jazz-units`:

- 179 `UnitData`;
- 158 appearance presets;
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

## Имена элитных противников

`EliteEnemyNamesFuncs.lua` комбинирует first/last-name pools (`Legion.lua`, `Rebels.lua`, `Mercenary.lua`) и nicknames, затем регистрирует presets `EliteEnemyName` через `PlaceObj`. Группы JAZZ: `Legion`, `Rebels`, `Mercenary`. Bare first-name без last — намеренная часть пула. Отдельного пула `Foreigners`/Adonis пока нет (Adonis elite остаются на vanilla-группе `Foreigners`).

Контракт имени совпадает с vanilla: поле `EliteEnemyName.name` имеет `translate = true`, а `GenerateEliteUnitName` копирует его в `unit.Name`. Поэтому name хранится как `T(...)` или составной `T{ 890000000001650, "<first> <last>", first = ..., last = ... }` с вложенными T first/last. Нельзя запекать `_InternalTranslate`/`Untranslated` на этапе регистрации — иначе английский CSV не применяется к элитным именам.

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