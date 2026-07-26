# Локализация

## Назначение и эффект для игрока

Система связывает numeric localization ID из Lua и ModItem с языковыми CSV.
`Russian.csv` и `English.csv` содержат полные runtime-наборы активных строк
JAZZ, отсутствующих в базовом `Game.csv`. Ванильные строки не дублируются:
их перевод для выбранного языка предоставляет сама игра. Рабочий каталог
отделяет аудит ID от русской и английской памяти переводов.

## Владелец и runtime-слои

| Слой | Вклад |
|---|---|
| Установленная vanilla | Загружает базовую таблицу языка, затем таблицы активных модов; формат CSV — `ID,Text,Translation,VoiceActor,Context` в UTF-8 |
| CommonLib | В debug-сборке перехватывает `T` и сообщает об одном ID с разными исходными текстами; snapshot 26 июля 2026: 1.11 build 1056, commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c` |
| JAZZ | Определяет строки в пакетах `jazz`, `jazz-maps` и `jazz-units`; основной пакет поставляет mod-only переводы через `Russian.csv` и `English.csv` |

## Файлы реализации и load-state

- `Russian.csv` — loaded runtime для языка Russian через `metadata.loctables`;
- `English.csv` — loaded runtime для языка English через `metadata.loctables`;
- `Localization/Strings.csv` — development-only рабочий каталог;
- `Localization/RussianManual.csv` — development-only память осознанных русских
  переводов и допустимых технических копий;
- `Localization/EnglishManual.csv` — development-only английская память
  перевода; ручные строки имеют приоритет над каталогом, машинные черновики
  явно помечены в `Notes`;
- `Localization/Collisions.csv` — development-only отчёт коллизий;
- `Localization/IdMigration.csv` — applied manifest миграции ID;
- `Localization/IdAmbiguities.csv` — отчёт неоднозначностей clone-aware Plan;
- `scripts/localization/audit-localization.ps1` — development-only статический
  аудитор и контролируемый экспортёр;
- `scripts/localization/translate-english-google.ps1` — development-only
  opt-in переводчик недостающих mod-only строк с защитой игровых токенов;
- `scripts/localization/migrate-localization-ids.ps1` — development-only
  clone-aware Plan/Apply для восстановления vanilla ID и выделения mod-only ID;
- `items.lua` и пути из `metadata.code` трёх пакетов — активные источники
  вызовов `T`; dormant Lua анализируется отдельно;
- `jazz-maps/Maps/` не входит в обзорный аудит и миграцию.

## Модель данных и публичные IDs

`ID` является глобальным ключом перевода. Повтор ID допустим только с тем же
исходным текстом. Разные тексты под одним ID — коллизия независимо от пакета
или generated-представления. ID хранится как строка цифр и не преобразуется в
IEEE-754.

Редактор JA3 способен при клонировании ModItem случайно заменить localization ID
неизменённого поля. Такая строка не считается новой строкой мода. Мигратор
сопоставляет её с vanilla по `Game.csv.Text` или `Translation`, generated
`Context` и, для одинаковых повторов, по порядку в актуальном
`<JA3_ROOT>\ModTools\Src`, затем возвращает original vanilla ID и canonical
English source text. Единица решения — `старый ID + SourceText + generated
Context`.

Новые ID выдаются только mod-only строкам, настоящим коллизиям и небезопасным
числовым ID без vanilla-соответствия. Зарезервирован диапазон
`890000000000000..890000000099999`, который меньше `2^53`; перед Apply он
проверяется против `Game.csv`, Lua и CSV.

## Каталог и приоритеты перевода

`Localization/Strings.csv` хранит одну рабочую запись на ID. Для русского
текста аудитор использует порядок:

1. текущий `Russian.csv`;
2. сохранённое ручное поле `Strings.csv`;
3. `RussianManual.csv` с `Notes=manual-translation`;
4. русскоязычный `SourceText`;
5. единственный русский перевод точного `Game.csv.Text`;
6. `RussianManual.csv` с `Notes=technical-copy`.

`technical-copy` разрешён для моделей оружия, калибров, адресов, служебных
токенов и placeholder-only строк. Сюжетные и интерфейсные фразы должны иметь
осознанный перевод.

Для английского текста порядок источников:

1. `EnglishManual.csv`, кроме `Notes=technical-copy`;
2. сохранённое поле `Strings.csv.English`;
3. пустой или уже английский `SourceText`;
4. однозначное обратное совпадение `Game.csv.Translation -> Game.csv.Text`;
5. `EnglishManual.csv` с `Notes=technical-copy`;
6. единственный canonical English из строки vanilla с тем же ID.

Google Translate используется только по явному `-AllowExternalTranslation`
после согласия владельца. Перед отправкой защищаются placeholders, управляющие
последовательности и переносы; результат сохраняется как `google-draft` и может
быть переопределён ручной строкой.

## Runtime flow

1. JA3 загружает базовый `Game.csv` выбранного языка.
2. Моды обходятся в установленном порядке.
3. Подходящий `metadata.loctables` загружается поверх текущей таблицы.
4. `Russian.csv` или `English.csv` JAZZ добавляет только активные mod-only ID,
   которых нет в базовом `Game.csv`.

`Text` нужен для аудита происхождения и должен соответствовать строке в `T`.
Vanilla ID не дублируются в runtime CSV: их перевод приходит из игры.

## Зависимости и пересечения

Lua не должен переиспользовать vanilla ID для другого исходного текста.
Аудитор сравнивает активные JAZZ-вызовы как между собой, так и с переданным
`Game.csv`. `Russian.csv` считается более новым и приоритетным источником
русского текста JAZZ, но не разрешает конфликтующий ID.

## Чек-лист проверки

- выполнить clone-aware Plan и убедиться, что `IdAmbiguities.csv` пуст;
- проверить manifest: `restore-vanilla` существует в `Game.csv`, а mod-only ID
  отсутствуют там и меньше `2^53`;
- выполнить Apply и идемпотентный повтор без новых замен;
- запустить аудитор с актуальным `Game.csv` и просмотреть `Collisions.csv`;
- требовать ноль `active-id-collision`, `game-id-collision` и
  `russian-csv-collision`;
- проверить UTF-8, пять экспортных колонок, уникальность ID и CSV round-trip;
- сохранить placeholders, теги, кавычки и многострочные поля;
- проверить точное совпадение множеств ID русского и английского экспортов,
  отсутствие видимой кириллицы в английском и отсутствие нетехнических пустых
  переводов;
- загрузить изменённые generated data и таблицу через Mod Editor, проверить
  панель сообщений и reload;
- выполнить smoke-тест русского и английского интерфейса на clean start и
  существующем save.

## Известные ограничения и долг

- 2 896 действительно новых английских строк остаются машинным черновиком и
  требуют редакторской вычитки терминологии и стиля;
- regex-аудит извлекает numeric ID из обычных строковых форм `T(...)` и
  `T{...}`; вычисляемые T-таблицы требуют runtime-проверки;
- содержимое `jazz-maps/Maps/` не проиндексировано;
- массовая миграция подтверждена статически; Mod Editor round-trip, clean start
  и существующее сохранение остаются обязательной ручной проверкой.

## Контракт сопровождения

При клонировании или изменении локализуемого поля сначала определить, является
ли строка неизменённой vanilla-копией. После изменения кода/ModItem запустить
Plan/Apply, generated sync-аудит и localization-аудит, обновить
`Strings.csv` и соответствующую ручную память, затем экспортировать оба
runtime CSV. Они содержат только активные mod-only ID; английский экспорт
нельзя обновлять при `needs-english`, повреждённых токенах или видимой
кириллице.

Новая или изменённая mod-only строка не допускает одноязычного change set:
русский и английский переводы, `Russian.csv` и `English.csv` обновляются
синхронно. Definition of Done требует `needs Russian=0`, `needs English=0` и
точного совпадения множеств активных mod-only ID обеих runtime-таблиц.
