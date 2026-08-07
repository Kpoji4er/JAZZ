# R.I.S. (Recon Intelligence Services)

## Статус и наблюдаемый эффект

На 7 августа 2026 года реализация
[`JAZZ-UI-RIS-002`](../../specs/active/JAZZ-UI-RIS-002.md) статически применена:
код и generated Email-данные зарегистрированы в `metadata.lua`, а все пять
R.I.S.-файлов входят в load graph. Это **не runtime PASS**: приёмка в живой
кампании и через JA3/DAP для AC-004…011 ещё не выполнена, поэтому spec остаётся
`approved`.

Игрок получает один разведывательный канал: welcome-письмо, оценки снабжения
Легиона, полевые заметки, двухступенчатые досье, архив сводок после боя и
постепенно открывающиеся материалы «Стратегии Майора». Player-facing текст
следует спокойному голосу полевого аналитика и не показывает внутренние тиры,
очереди, preset ID или метатермины.

## Связанные specs и каноны

- [`JAZZ-UI-RIS-001`](../../specs/active/JAZZ-UI-RIS-001.md) — исходный
  функциональный контур почты, PDA и AAR.
- [`JAZZ-UI-RIS-002`](../../specs/active/JAZZ-UI-RIS-002.md) — единый
  двуязычный корпус, schema 3, AAR v2 и «Стратегия Майора».
- [`ris-editorial-style.md`](../../design/ris-editorial-style.md) — голос,
  терминология и human-review contract.
- [`ris-legion-tier-briefs.md`](../../design/ris-legion-tier-briefs.md),
  [`ris-legion-dossiers.md`](../../design/ris-legion-dossiers.md),
  [`ris-battle-report-templates.md`](../../design/ris-battle-report-templates.md)
  и [`ris-major-strategy.md`](../../design/ris-major-strategy.md) — содержательные
  каноны.

## Владелец и runtime-слои

| Слой | Вклад |
| --- | --- |
| Vanilla JA3 | `Email`/`ReceiveEmail`, `GetReceivedEmails`, PDA browser, `ConflictStart`/`CombatStart`/`UnitDiedOnSector`/`ConflictEnd`, campaign time, sector/quest display data |
| CommonLib | В JAZZ-UI-RIS-002 нет нового прямого R.I.S.-override; итоговый порядок общих handlers всё равно зависит от общего load graph |
| JAZZ | Core-пакет владеет состоянием, очередью, UI, AAR и generated Email; `jazz-units` предоставляет стабильные `JAZZ_Legion_*` UnitData ID, Legion Global AI только наблюдается |

R.I.S. не меняет формулы, ресурсы, частоту решений или экономику Legion Global
AI. `System_RIS_Strategy.lua` читает уже синхронизированное состояние и сигналы
директора, но фиксирует squad-событие только когда колонна видима на
стратегической карте, находится в раскрытом секторе или уже вошла на территорию
игрока. Пишет observer только в `gv_JAZZ_RIS`.

## Файлы реализации и load-state

| Файл | Load-state | Роль |
| --- | --- | --- |
| `Code/System_RIS_Mail.lua` | loaded | `gv_JAZZ_RIS` schema 3, идемпотентная миграция, общая отправка писем, unlock PDA |
| `Code/System_RIS_Content.lua` | loaded, generated | Досье, AAR-банки, UI и материалы Strategy; генерируется `_apply_ris_editorial.py` |
| `Code/System_RIS_Combat.lua` | loaded | Контакты/убийства, cumulative combat snapshot v3 и language-neutral AAR v2 |
| `Code/System_RIS_Browser.lua` | loaded | Bulletin, Dossiers, After-action reports и рендер на текущем языке |
| `Code/System_RIS_Strategy.lua` | loaded | Read-only observer Legion AI; загружается после `Code/Guardpost_Patrols.lua`, от которого получает состояние и сообщения |
| `items.lua` | generated and loaded | 24 `Email`: welcome, 11 supply briefs, 3 полевые заметки и 9 Strategy |
| `metadata.lua` | generated and loaded | Порядок пяти code-файлов и 9 `ModResourcePreset` Strategy Email |

`System_RIS_Mail`, generated Content, Combat и Browser загружаются в ранней
R.I.S.-группе. Strategy намеренно стоит отдельно сразу после
`Guardpost_Patrols`, чтобы его observer устанавливался после производителя
Legion AI.

## Корпус текста и generated pipeline

- `_ris_copy_bank.py` — единый изменяемый RU+EN банк welcome, UI, AAR,
  полевых писем, досье и Strategy; `_ris_dossier_copy.py` только compatibility
  facade.
- 214 уникальных двуязычных пар проходят editorial audit; apply проецирует
  **217 projected active localization IDs**.
- 11 supply briefs остаются отдельным каноном
  `_rewrite_ris_legion_briefs.py`, но проходят тот же editorial review и аудит.
- `_apply_ris_editorial.py` синхронизирует Content Lua, 24 Email, metadata,
  `Localization/Strings.csv`, обе manual memory и runtime `Russian.csv` /
  `English.csv`.
- `_audit_ris_copy.py` проверяет ожидаемые категории, ID, placeholder parity,
  подписи, запрещённые термины и девять Strategy-текстов.

## Модель данных и миграция сохранений

`gv_JAZZ_RIS.schema_version = 3`. Состояние содержит:

- welcome и последний отправленный supply brief;
- `mail_queue` и `next_dispatch_at`;
- подтверждённые типы, kills, досье, некрологи и ключевые встречи;
- `battles`, FIFO не более **20**;
- observed/delivered/order, cooldown и baseline для Strategy.

`JAZZ_RIS_MigrateState()` идемпотентно нормализует старые таблицы на load/reload.
Старый AAR, в котором сохранились уже переведённые `title`/`body`, не показывает
текст прежнего языка: необратимая проза отбрасывается, а Browser восстанавливает
локализованные outcome, sector, quest, силы и потери из сохранившихся полей.
Если фактов недостаточно, остаётся краткая локализованная архивная сводка.
Миграция охватывает не только очередь, но и уже полученные sighting/obit:
стабильные `type_id`, `npc_id` и T-ссылки пересобирают context, прежние
`Untranslated`-обёртки ID нормализуются обратно в raw ID, а фактически
полученные письма восстанавливают `met_types`/`obits_sent`. Pending sighting и
obit, напротив, снимают старые enqueue-time flags; для Strategy фактический inbox
является источником истины delivery state. Невосстановимый contact получает
локализованное общее обозначение. Strategy archive хранит material ID и исходный
`email.time`, а не готовую прозу или время повторной миграции.

Новые AAR v2 сохраняют только language-neutral keys, counts, sector/quest ID и
стабильные ссылки на именных противников. Сектор, задание, имя элиты, auto-resolve
и все абзацы разрешаются заново при каждом показе на выбранном сейчас языке.

## Почта и темп

- Welcome становится готов через **2 campaign hours** после пробуждения стола.
- Стартовая оценка снабжения — через **7 campaign hours**.
- Повышение снабжения, первое sighting и оба вида некролога получают
  `ready_at = event + 5h`.
- Общий стол отправляет не больше одного R.I.S. Email каждые **5 campaign
  hours**. На load догоняется одна актуальная оценка, без пачки старых писем.
- Между двумя Strategy Email дополнительно проходит не меньше **24 campaign
  hours**.
- Во время tactical combat стол не снимает due-row. Unlock контакта, Strategy и
  отметка некролога записываются только после появления Email в полученном inbox;
  после `CombatEnd` очередь обрабатывается повторно.

Значения 2h / 7h / 5h и общий 5h desk contract не менялись относительно
JAZZ-UI-RIS-001.

## Досье

Первый подтверждённый контакт ставит `RIS_UnitSighting` в общую отправку.
Краткая карточка становится видна только после доставки этого письма. Полный
текст для конкретного `JAZZ_Legion_*` открывается после **трёх** подтверждённых
убийств бойцов этого типа. Досье ключевых фигур/Легиона открываются по их
существующим встречам и quest state.

## AAR v2

`g_JAZZ_RIS_CombatSnaps` хранит отдельный cumulative snapshot schema 3 для
каждого активного `sector_id`:

- повторный `CombatStart` в том же секторе дополняет snapshot и не обнуляет
  ранние фазы;
- параллельный auto-resolve в другом секторе не заменяет loaded tactical
  snapshot и не импортирует units с текущей карты;
- `GetAllUnits` включает map-placed units без satellite squad;
- diplomacy flags объединяют mercs и союзников на стороне игрока и отделяют
  живых hostiles; для уже замеченного участника исходная сторона сохраняется
  даже после post-conflict перехода в `enemyNeutral`; `conflict_ignore` и
  defeated villains не считаются активными участниками;
- стабильный `session_id` имеет приоритет над временным map handle и
  дедуплицирует одного участника между satellite и tactical; смерть удаляет тот
  же ключ из WIA;
- baseline HP фиксируется при первом появлении бойца: WIA означает новое
  повреждение/падение в этом конфликте, а не старую рану до боя;
- sector context и только задания, действительно связанные с этим сектором,
  фиксируются в начале и объединяются с финальным снимком, поэтому завершённое
  самим боем задание не пропадает, а постороннее выбранное задание в AAR не
  попадает;
- при заявленной победе и живом hostile отчёт предупреждает о сохраняющемся
  присутствии, а не объявляет сектор очищенным;
- `ConflictStart` фиксирует состав satellite squads до auto-resolve,
  `UnitDiedOnSector` считает его KIA/confirmed kills, а финальный проход по
  `gv_UnitData` считает выживших WIA; если lifecycle-сигнал старта был пропущен,
  финализация восстанавливает хотя бы ещё доступный состав вместо гарантированного
  отчёта `0/0`;
- tactical и auto-resolve используют локализованные шаблоны; поздний
  `AutoResolvedConflict` исправляет survivor-retreat branch, где vanilla
  `ConflictEnd` передаёт false. Именной противник, всё ещё находящийся в секторе,
  получает `threat`/`wounded`, а `escaped` оставлен отсутствующему выжившему;
- в `battles` хранится не больше 20 записей, новые идут первыми.

## «Стратегия Майора»

Девять materials открываются постепенно по уже случившимся событиям. `Network`
всегда идёт первым после прочитанного welcome и либо первого подтверждённого
контакта, либо полученного supply brief. В очереди одновременно остаётся только
одна Strategy-row; после Network выбирается самое раннее ещё не выданное
наблюдение.

Observer фиксирует:

1. patrol, уже вошедший в сектор игрока;
2. видимого collector/recruiter;
3. видимый возвращающийся отряд с non-generic recon report;
4. видимый QRF/reinforce;
5. видимый supply/shipment/manpower convoy;
6. наблюдаемый отход wounded squad;
7. видимый major response;
8. наблюдаемую активность late-awaken region после доставки Майора.

Существование скрытого гарнизона, конвоя или внутреннего task само по себе не
открывает материал. Для `Awakening` флаг `major_delivery_done` лишь запускает
новый baseline: уже видимый отряд не считается доказательством, пока после
доставки не появится новая колонна или не изменится наблюдаемое движение.
Доставленный разведотчёт в `root.regions[].reports` также остаётся
внутренним состоянием Legion AI: `First, they look` открывается по видимой
возвращающейся разведгруппе, а не по сканированию скрытого отчёта.

В Bulletin отдельный раздел Strategy отсутствует до первого доставленного
материала. После этого он показывает только уже полученные записи и сохраняет
порядок доставки; будущие темы и счётчик не выводятся.

## Проверка

Статически подтверждено:

- copy audit: 214 RU+EN pairs, все категории, 9 Strategy;
- apply check: 8/8 outputs unchanged, 217 localization ID, 24 Email;
- strict localization audit: `needs Russian=0`, `needs English=0`, active
  collisions 0; множества mod-only ID runtime RU/EN совпадают;
- quick structural check `items.lua` + `metadata.lua`: PASS;
- targeted lupa contract: **7/7 PASS** — mail/inbox migration и stable-ID
  re-resolution, delivery gate, Strategy observability, concurrent/same-time
  satellite conflicts, two-phase tactical KIA/WIA/quest/hostile state и legacy
  AAR reconstruction;
- один активный `System_RIS_Strategy.lua` в load graph после
  `Guardpost_Patrols`.

Общий generated-sync пока не является PASS: suite-аудит сообщает 489 не
связанных с R.I.S. companion errors и 27 warnings; из них core-пакет `jazz`
даёт 409/12. R.I.S.-совпадений в отчёте нет.

Targeted runtime profile находится в
[`docs/technical/testing.md`](../testing.md). До проверки RU/EN mail, two-stage
dossier, multi-phase/map-placed AAR, surviving hostile, old-save language switch,
Strategy cadence и Bulletin visibility все runtime AC-004…011 остаются
`BLOCKED`.

## Контракт сопровождения

Изменение схемы, сроков, Email/localization ID, threshold, AAR record или
Strategy signals требует синхронно обновить эту страницу,
[`file-coverage.md`](file-coverage.md), compatibility/testing, spec evidence,
[`docs/wiki/ris.md`](../../wiki/ris.md) и showcase RU+EN. Generated Content и
Email не редактировать вручную: источник — copy/apply pipeline.
