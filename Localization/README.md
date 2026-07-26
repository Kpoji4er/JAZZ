# Рабочий каталог локализации

`Strings.csv` — удобный промежуточный источник для русского и будущего
английского перевода JAZZ. Он не загружается игрой напрямую.

Колонки:

- `ID` — неизменяемый numeric localization ID;
- `SourceText` — текст, найденный в активном `T(...)`/`T{...}` либо в
  приоритетном `Russian.csv`;
- `VanillaText` — английский текст того же ID из базового `Game.csv`;
- `Russian` и `English` — рабочие переводы;
- `Status` — коллизии, отсутствие перевода и происхождение строки;
- `Context`, `Packages`, `Locations` — контекст и все активные потребители;
- `Notes` — ручные заметки, сохраняемые при обновлении каталога.

## Приоритет источников

1. Текущий `Russian.csv` мода имеет приоритет над переводом из базового
   `Game.csv`.
2. Активными считаются пути из `metadata.code` и строки ModItem из
   `items.lua`.
3. `jazz-maps/Maps/` намеренно не обходится.
4. Один ID с разными `SourceText` считается коллизией. Такой ID нельзя
   переводить, пока исходники не разведены по уникальным ID.

## Обновление

```powershell
scripts/localization/audit-localization.ps1 `
  -GameCsv "<path-to-Russian/CurrentLanguage/Game.csv>" `
  -UpdateCatalog
```

Аудитор обновляет вычисляемые колонки `Strings.csv`, но сохраняет уже
заполненные `English` и `Notes`. Русская строка из корневого `Russian.csv`
всегда выигрывает у остальных источников.

`Collisions.csv` содержит по одной записи на каждый вариант конфликтующего
текста и пригоден для фильтрации в Excel.

## Экспорт

После устранения всех коллизий и заполнения выбранного языка аудитор может
создать игровой CSV с официальной схемой
`ID,Text,Translation,VoiceActor,Context`:

```powershell
scripts/localization/audit-localization.ps1 `
  -GameCsv "<path-to-Russian/CurrentLanguage/Game.csv>" `
  -ExportEnglishCsv "<temporary-path-to-English.csv>"
```

Экспорт блокируется, если хотя бы одна строка языка не заполнена или имеет
статус `collision`. Полученный файл сначала сравнивается с каталогом и
проверяется в Mod Editor; корневые runtime-таблицы не перезаписываются
аудитором автоматически.
