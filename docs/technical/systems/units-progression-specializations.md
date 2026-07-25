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
- 69 enemy squad definitions;
- 33 AI archetypes;
- 1257 `LootDef`;
- 10 voice response presets и 2 translated voice presets;
- 2 enemy roles, 3 effects, combat action, banter и localization table.

Грубая faction taxonomy UnitData: 37 JAZZ Legion, 24 Army, 23 Adonis/Corazon, 22 Rebels/Militia, 22 Thugs; остальные относятся к mercenary, civilian, named/boss и служебным группам. Эти числа — snapshot и должны пересчитываться после Mod Editor regeneration.

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

`EliteEnemyNamesFuncs.lua` комбинирует first/last-name pools и специальные presets. Генерация должна быть детерминированной, не создавать пустые/повторные комбинации сверх ожидаемого и сохраняться в unit instance/save. Localization и склонение являются пользовательски заметной частью системы.

## Роли, keywords и экипировка

AI keywords перечислены в [AI-системе](ai-awareness.md). UnitData связывает faction, archetype, role, stats, perks, appearance, voice, inventory, loot и equipment. Изменение любого item/entity/action ID может сломать spawn unit даже без прямого Lua import.

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
- squad spawn/autoresolve/death/despawn;
- отсутствие missing item/entity/voice/archetype IDs.

## Ограничения и сопровождение

Generated UnitData/appearance/loot править через Mod Editor. Новый unit/archetype/keyword/specialization должен быть отражён в этой странице и профильной AI/strategy документации. `AimHiringScreen_Template.lua` остаётся dormant, пока metadata явно не изменена.