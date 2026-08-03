# Глоссарий терминов JAZZ

## Источник терминов и приоритет локализации

Для терминов и текстовых переводов используем порядок:

1) `Russian.csv` (корень мода): **приоритетный источник**
2) `Localization/CurrentLanguage/Game.csv` (локальная копия vanilla, **не в git**): вспомогательный

Если есть расхождение, выбирается значение из `Russian.csv`.

## Базовые игровые термины

- **merc** > **наемник** (основное правило: использовать только это написание)
- **party** / **team** > отряд
- **squad** > отряд
- **unit** > юнит/юниткадр (в контексте UI чаще «юнит»)
- **unitdata** > данные юнита
- **character effect** > эффект персонажа
- **inventory** > инвентарь
- **item** > предмет
- **weapon** > оружие
- **ammo** > боеприпасы
- **bullet drop range** > настильность
- **perk** > черта/перк
- **ability** > способность
- **trait** > черта (при описании персональных свойств)
- **faction** > фракция
- **sector** > сектор
- **region** > регион
- **guardpost** > сторожевой пост
- **map** > тактическая карта
- **world** > стратегическая карта (мир)
- **quest** > квест
- **dialogue** > диалог
- **mission** > миссия/задание
- **operation** > операция
- **cooldown** > перезарядка
- **cover** > укрытие
- **stance** > стойка
- **bleedout** > критическое состояние без сознания
- **wound** > рана
- **will** > воля
- **grit** > стойкость воли

## Технические термины (для code-review и документации)

- **override** > переопределение
- **vanilla JA3** > базовая версия игры/vanilla
- **CommonLib** > общая библиотека модов JA3
- **metadata** > метаданные мода (`metadata.lua`)
- **generated data** > сгенерированные данные редактора
- **ModItem** > ModItem
- **Mod Editor** > редактор мода
- **runtime** > исполняемая среда на запуске
- **reload** > перезагрузка скриптового состояния без полного рестарта
- **thread** > поток
- **savegame** > сохранение
- **network deterministic** > сетевой детерминизм
- **mapdata** > данные карты
- **patch** > карта-патч/патч карты
- **localization** > локализация

## Имена классов Легиона (display Name)

Английский display name совпадает с class-stem в `JAZZ_Legion_*` ID, а не с vanilla `LegionGoon` / `LegionManiac` (там были Goon / Brute).

| RU | EN | UnitData stem |
| --- | --- | --- |
| Головорез | Roughneck | `AssaultT1_Roughneck` |
| Новобранец | Recruit | `JAZZ_Legion_Recruit` (weaker Roughneck clone for recruiter) |
| Громила | Crusher | `AssaultT1_Crusher` |
| Череполом | Skull Crusher | `AssaultT3_SkullCrusher` *(EN пока `Skullbreaker` в CSV — выровнять отдельно)* |
| Грабитель | Pillager | `AssaultT2_Pillager` |
| Штурмовик | Shock Trooper | `AssaultT2_ShockTrooper` |
| Палач | Headsman | `AssaultT4_Headsman` |

Localization IDs для первых двух: `217901684853` (Roughneck), `188332474737` (Crusher); Recruit: `890000000001643`. Память: `Localization/EnglishManual.csv` (`manual-translation;class-id`).

## Правила перевода в этой документации

1. Если термин есть в этом глоссарии, используем его везде одинаково.
2. По умолчанию `merc` = `наемник` даже в коротких технических фрагментах.
3. Для английских ID (`Entity`, `Class`, `metadata.lua`, `ModItem`) оставляем технический формат без перевода.
