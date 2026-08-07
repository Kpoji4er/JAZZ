---
id: JAZZ-UI-RIS-002
status: approved
owner: project-owner
systems:
  - ris-intelligence
  - localization
  - combat-reporting
  - legion-global-ai
  - save-compatibility
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/System_RIS_Mail.lua
  - Code/System_RIS_Content.lua
  - Code/System_RIS_Combat.lua
  - Code/System_RIS_Browser.lua
  - Code/System_RIS_Strategy.lua
  - items.lua
  - metadata.lua
  - English.csv
  - Russian.csv
  - Localization/Strings.csv
  - Localization/EnglishManual.csv
  - Localization/RussianManual.csv
  - docs/specs/active/JAZZ-UI-RIS-001.md
  - docs/specs/active/JAZZ-UI-RIS-002.md
  - docs/tools/_ris_copy_bank.py
  - docs/tools/_apply_ris_editorial.py
  - docs/tools/_audit_ris_copy.py
  - docs/tools/_test_ris_contract.py
  - docs/tools/_ris_dossier_copy.py
  - docs/tools/_apply_ris_dossier_copy.py
  - docs/tools/_apply_ris_mail_emails.py
  - docs/tools/_apply_ris_phase_b.py
  - docs/tools/_rewrite_ris_legion_briefs.py
  - docs/tools/_apply_ris_queue_field_mails.py
  - docs/tools/_fix_ris_brief11_ru_calque.py
  - docs/tools/_fix_ris_sighting_loc.py
  - docs/tools/_fix_ris_english_csv_text_keys.py
  - docs/tools/README.md
  - docs/design/ris-editorial-style.md
  - docs/design/ris-legion-tier-briefs.md
  - docs/design/ris-legion-dossiers.md
  - docs/design/ris-battle-report-templates.md
  - docs/design/ris-major-strategy.md
  - docs/technical/systems/ris-intelligence.md
  - docs/technical/systems/file-coverage.md
  - docs/technical/compatibility.md
  - docs/technical/testing.md
  - docs/wiki/ris.md
  - docs/wiki/legion-global-ai.md
  - docs/showcase/ru/ris.md
  - docs/showcase/en/ris.md
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Localization/Strings.csv
  - localization-ids:890000000011322-890000000011349
  - email-ids:RIS_MajorStrategy_*
  - GameVar:gv_JAZZ_RIS
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-UI-RIS-002: полная редактура и локализация R.I.S.

## Проблема

R.I.S. уже объединяет почту, оценки снабжения, досье и сводки после боя, но тексты создавались несколькими волнами и сейчас не образуют один качественный продукт.

- Голос расходится от спокойной полевой аналитики до газетных заголовков и технических уведомлений.
- В player-facing тексте встречаются кальки, слова интерфейса, внутренние термины и сырой английский.
- Шаблоны некрологов содержат `<field_note>`, которого runtime не передаёт.
- Строка auto-resolve в AAR зашита только по-английски.
- Русская строка прогресса досье неверно передаёт смысл confirmed kills.
- Источники текста размножены между Python-банками, generated Lua, `items.lua`, runtime CSV и `Localization/Strings.csv`; повторный прогон старого инструмента может вернуть устаревшую редакцию.
- AAR и часть контекста полевых писем сохраняются уже переведёнными строками. После смены языка архив остаётся на прежнем языке.
- AAR может потерять смерти из ранних фаз одного конфликта и неверно описать победу, если на карте ещё остались живые противники.
- Утверждённая серия [`docs/design/ris-major-strategy.md`](../../design/ris-major-strategy.md) пока не подключена к почте и сайту.

JAZZ-UI-RIS-001 сохраняет функциональный контракт R.I.S. Эта спека проводит единую редакторскую и локализационную волну, исправляет связанные дефекты представления и добавляет постепенную серию «Стратегия Майора».

## Цели

- Сделать весь R.I.S. единым по голосу: грамотная человеческая полевая аналитика без ощущения интерфейса, патчноута или скрытой игровой системы.
- Провести human review каждого RU- и EN-текста, а не только новых строк.
- Свести изменяемый корпус R.I.S. к одному каноническому copy bank и воспроизводимому apply/audit pipeline.
- Обеспечить полную двуязычность, совпадение placeholder-ов и корректное переключение языка для почты и архива AAR.
- Исправить сломанные и вводящие в заблуждение шаблоны.
- Подключить девять утверждённых материалов «Стратегии Майора» с постепенным событийным раскрытием.
- Сохранить действующие игровые формулы, темп Legion AI и очередь R.I.S., кроме отдельно утверждённого интервала серии.

## Non-goals

- Перебалансировка Legion Global AI, его экономики, размеров отрядов, тревоги, маршрутов или частоты стратегических решений.
- Исправление владения сектором и завершения vanilla/карточного конфликта при оставшихся на карте врагах. R.I.S. обязан правдиво описать такую ситуацию, но владелец сектора исправляется отдельной map/conflict spec.
- Изменение порога полного досье: требуется три подтверждённых убийства бойцов одного типа.
- Изменение задержек действующей почты: welcome остаётся через 2 часа, стартовая оценка снабжения — через 7 часов, рост снабжения и полевые заметки — через 5 часов, общий интервал стола — 5 часов.
- Новые портреты, логотипы, звуки или иные медиа.
- Ручное редактирование GitHub Wiki.

## Требования

### Единый редакторский контракт

- `JAZZ-UI-RIS-002-REQ-001` — создать `docs/design/ris-editorial-style.md`: голос R.I.S., RU/EN терминология, подпись, степень уверенности, запрещённые мета-термины, правила чисел, имён, квестов и placeholder-ов. Тональная база — спокойный полевой аналитик из «Стратегии Майора».
- `JAZZ-UI-RIS-002-REQ-002` — human review покрывает все player-facing категории: UI и empty states; welcome; 11 оценок снабжения; sighting mail; два вида некрологов; 38 досье типов; 4 досье ключевых фигур/фракции; все AAR headline/body banks; auto-resolve; metadata строки отчёта; подписи и отправителей; 9 материалов «Стратегии Майора».
- `JAZZ-UI-RIS-002-REQ-003` — каждый текст строится по схеме «наблюдение → вывод → практическое значение». Не использовать `archetype`, `catalog`, `site`, `tab`, `subscription`, `tier`, `Heat`, `QRF`, `spawn`, имена preset-ов, raw quest/session/unit IDs и прямые указания интерфейса.
- `JAZZ-UI-RIS-002-REQ-004` — каноническое полное имя используется одинаково: `Recon Intelligence Services` / `Разведывательно-информационная служба R.I.S.`. Каноническая подпись писем: `— R.I.S. Field Desk` / `— Полевой отдел R.I.S.`.
- `JAZZ-UI-RIS-002-REQ-005` — RU и EN пишутся как самостоятельная проза с одинаковыми фактами и степенью уверенности; дословная калька не требуется.

### Канонический источник и generated data

- `JAZZ-UI-RIS-002-REQ-006` — `docs/tools/_ris_copy_bank.py` является единственным каноническим RU+EN банком для welcome, UI, sighting/obit, досье, AAR и «Стратегии Майора». `_ris_dossier_copy.py` становится совместимым импортным фасадом без второй редактируемой копии тех же строк.
- `JAZZ-UI-RIS-002-REQ-007` — оценки снабжения остаются в `_rewrite_ris_legion_briefs.py`, потому что их отдельный канон привязан к карте unlock-ов оружия; этот файл также проходит полный редакторский review.
- `JAZZ-UI-RIS-002-REQ-008` — `_apply_ris_editorial.py` идемпотентно генерирует/синхронизирует `System_RIS_Content.lua`, R.I.S. Email ModItems в `items.lua`, RU/EN поля R.I.S. в `Localization/Strings.csv`, translation memory и оба runtime CSV. Старые apply/fix-скрипты импортируют новый банк либо явно помечены как superseded и не содержат расходящейся прозы.
- `JAZZ-UI-RIS-002-REQ-009` — `_audit_ris_copy.py` проверяет полный ожидаемый набор из 218 R.I.S. ID, включая identity/sender, и Email id, совпадение English `Text` с исходным `T()`, RU/EN placeholder parity, отсутствие неизвестных placeholder-ов, запрещённых player-facing токенов, retired factual phrases, пустых переводов, raw ID и нескольких вариантов текста на один ID.
- `JAZZ-UI-RIS-002-REQ-010` — диапазон `890000000011322…890000000011349` зарезервирован за заголовками, телами и UI-строками «Стратегии Майора». Другие подсистемы его не используют.

### Почта, UI и досье

- `JAZZ-UI-RIS-002-REQ-011` — welcome объясняет назначение канала внутри мира и не говорит игроку читать письмо ради открытия вкладки. Фактический unlock после прочтения сохраняется.
- `JAZZ-UI-RIS-002-REQ-012` — sighting mail говорит о впервые подтверждённом типе бойца без слов «архетип», «сайт» и «каталог». Только после фактического появления письма в inbox открывается краткая карточка контакта; combat-deferred row не меняет unlock. Полный текст досье показывается только после трёх подтверждённых убийств этого типа.
- `JAZZ-UI-RIS-002-REQ-013` — прогресс досье формулируется как подтверждение наблюдений по конкретному типу и не выдаёт общее число потерь Легиона.
- `JAZZ-UI-RIS-002-REQ-014` — `RIS_EliteObit` и `RIS_NpcObit` содержат законченный текст с корректным `<name>` и не содержат `<field_note>`. Русские фразы не требуют знания пола персонажа.
- `JAZZ-UI-RIS-002-REQ-015` — заголовки, empty states, отправители, подписи и faction label читаются как часть R.I.S.; `Legion (faction)` и аналогичные служебные уточнения player-facing не показываются.

### Сводки после боя

- `JAZZ-UI-RIS-002-REQ-016` — все AAR headlines и абзацы приведены к тону полевой аналитики. Варианты остаются различимыми по исходу и интенсивности, но не переходят в таблоид, браваду или буквальную кальку.
- `JAZZ-UI-RIS-002-REQ-017` — auto-resolve, сектор, POI, квесты, параметры quest-note, силы, потери и именные противники локализуются через T-контракт. В отчёте нет literal вложенного placeholder, raw quest id, raw sector id при доступном имени и жёстко зашитой английской строки.
- `JAZZ-UI-RIS-002-REQ-018` — русские шаблоны используют нейтральную грамматику: `погибших: N`, `раненых: N` и конструкции с `<name>`, не требующие пола. Все числовые значения корректны для 0/1/2–4/5+ без runtime-склонения.
- `JAZZ-UI-RIS-002-REQ-019` — каждый активный `sector_id` имеет отдельный накопительный snapshot; параллельный remote conflict не заменяет loaded tactical conflict и не сканирует его карту. Повторные `CombatStart` не обнуляют уже учтённые смерти и ранения. В силы и потери входят валидные map-placed units без satellite squad; baseline HP исключает старые травмы из WIA и named fate, а context только действительно связанных с сектором заданий вместе со scalar quest params фиксируется до возможного завершения задания боем. Для auto-resolve состав фиксируется на `ConflictStart`, а KIA/WIA — по satellite UnitData.
- `JAZZ-UI-RIS-002-REQ-020` — перед формулировкой исхода AAR проверяет живых враждебных units на карте. При `playerWon=true`, но оставшихся противниках, текст сообщает о выполненной цели и продолжающемся вражеском присутствии, а не о полностью очищенном секторе.

### Переключение языка и сохранения

- `JAZZ-UI-RIS-002-REQ-021` — новые AAR сохраняются как versioned language-neutral snapshot: template keys/bands, параметры, sector/quest ids, counts и stable named-unit data. `title` и `body` строятся в `System_RIS_Browser.lua` на текущем языке при каждом показе.
- `JAZZ-UI-RIS-002-REQ-022` — sighting/obit и strategy queue/received items хранят или восстанавливают stable type/NPC/material ids и локализуемые значения, а не заранее переведённые title/body. Полученные материалы и очередь после смены языка показываются на текущем языке; Strategy migration сохраняет исходный inbox timestamp.
- `JAZZ-UI-RIS-002-REQ-023` — `gv_JAZZ_RIS` получает `schema_version` и идемпотентную миграцию. Старые AAR по возможности разбираются в структурный вид; если прежний body невозможно восстановить без догадки, он заменяется краткой локализованной архивной сводкой из сохранённых `outcome`, `sector`, `quest_ids`, `quest_linked` и времени. Старый текст на другом языке player-facing не остаётся.
- `JAZZ-UI-RIS-002-REQ-024` — миграция старых queued и received sighting/obit удаляет заранее переведённые поля и восстанавливает их по сохранённому `type_id`, `npc_id`, `obit_key` или stable T-reference с numeric localization ID; невосстановимый contact и pending sighting удалённого archetype получают локализованное общее обозначение, не блокируя desk queue. Миграция не дублирует письма, снимает прежние enqueue-time flags с ещё ожидающих строк и восстанавливает delivery state только по фактически полученному inbox.

### «Стратегия Майора»

- `JAZZ-UI-RIS-002-REQ-025` — реализовать 9 Email `RIS_MajorStrategy_Network|Roads|Villages|Recon|Response|Cargo|Recovery|Retribution|Awakening` с утверждённым текстом из copy bank и [`ris-major-strategy.md`](../../design/ris-major-strategy.md).
- `JAZZ-UI-RIS-002-REQ-026` — `System_RIS_Strategy.lua` наблюдает существующее synced-состояние Legion AI, не меняя его. Оно фиксирует восемь событий: патруль на территории игрока; замеченный сборщик/вербовщик; видимый отход разведгруппы с донесением; замеченный местный ответ/усиление; видимый конвой; наблюдаемый отход на пополнение; встреченное возмездие; новая наблюдаемая активность материкового округа после помощи штаба. Скрытые task, гарнизон, уже доставленный внутренний отчёт и неизменившийся видимый до доставки отряд сами по себе ничего не открывают.
- `JAZZ-UI-RIS-002-REQ-027` — `Network` всегда доставляется первым после welcome и первого подтверждённого контакта/брифа. При доступном inbox его фактическое содержимое, а не старый `last_mailed_tier`, подтверждает доставку brief. Остальные материалы становятся eligible независимо и только после соответствующего события.
- `JAZZ-UI-RIS-002-REQ-028` — действует общий интервал стола 5 часов и дополнительный интервал не меньше 24 campaign hours между двумя strategy mails. При нескольких событиях порядок определяется временем первого наблюдения.
- `JAZZ-UI-RIS-002-REQ-029` — старое сохранение ставит в очередь не больше одного заслуженного strategy mail; остальные соблюдают 24-часовой интервал. Load/ReloadLua не создают дублей.
- `JAZZ-UI-RIS-002-REQ-030` — раздел «Стратегия Майора» скрыт до первого письма, затем показывает только доставленные материалы в порядке получения. Нет счётчика, пустых карточек и названий будущих тем.

### Локализация и документация

- `JAZZ-UI-RIS-002-REQ-031` — множества активных mod-only ID в `Russian.csv` и `English.csv` совпадают; все R.I.S. строки заполнены в `Localization/Strings.csv`; `needs Russian=0`, `needs English=0`, collision=0.
- `JAZZ-UI-RIS-002-REQ-032` — English runtime CSV хранит английский source `Text` и английский `Translation`; Russian runtime CSV хранит тот же английский `Text` и русский `Translation`.
- `JAZZ-UI-RIS-002-REQ-033` — technical, wiki и showcase RU/EN описывают фактическое состояние: двухступенчатое досье, текущий язык архива, исправленные AAR и постепенную «Стратегию Майора». Approved-only scope не описывается как shipped до runtime acceptance.

## Инварианты и ограничения

- R.I.S. и A.M.E. остаются разными брендами и browser modes.
- Общая очередь R.I.S. отправляет не больше одного письма каждые 5 campaign hours.
- `JAZZ_Legion_Tier`, Heat и Legion AI только читаются; эта спека не меняет их формулы.
- FIFO AAR сохраняет максимум 20 записей.
- Выбор вариантов AAR остаётся детерминированным и MP-safe.
- Существующие public Email IDs и локализационные IDs не переименовывать; новые IDs только из зарезервированного диапазона.
- `System_RIS_Content.lua` и R.I.S. Email blocks в `items.lua` считаются generated outputs и вручную не редактируются.
- В Lua Email body переносы записываются как escape `\n`, без raw newline внутри строк.
- Изменение не удаляет полученные письма, unlock-флаги, kills или quest state старого сохранения.

## Acceptance criteria

- `JAZZ-UI-RIS-002-AC-001` — human: полный RU/EN корпус из REQ-002 построчно рассмотрен по `ris-editorial-style.md`; все категории имеют PASS, ни одна строка не содержит кальку, debug/meta лексику или расходящийся смысл.
- `JAZZ-UI-RIS-002-AC-002` — static: `_audit_ris_copy.py` и локализационный аудитор дают полный ожидаемый набор R.I.S. IDs, placeholder parity, `needs Russian=0`, `needs English=0`, collision=0 и одинаковые множества runtime IDs.
- `JAZZ-UI-RIS-002-AC-003` — static: повторный `_apply_ris_editorial.py` не меняет файлы; старые apply-скрипты не содержат второй расходящийся copy bank.
- `JAZZ-UI-RIS-002-AC-004` — runtime RU+EN: welcome, sighting и оба obit приходят с правильными заголовками, абзацами, именами и подписями; literal placeholder, raw id и UI-инструкция отсутствуют.
- `JAZZ-UI-RIS-002-AC-005` — runtime: первое sighting открывает краткую карточку, 0–2 kills не показывают полное досье, третье убийство открывает полный текст.
- `JAZZ-UI-RIS-002-AC-006` — runtime: бой с двумя боевыми фазами и map-placed enemies даёт накопительные силы/потери; ни одна смерть первой фазы не потеряна, старая травма не считается новым WIA/named wound, завершённое боем задание и параметры его note сохраняются, параллельный сектор не смешивается.
- `JAZZ-UI-RIS-002-AC-007` — runtime: при `playerWon=true` и живом hostile на карте AAR не сообщает, что сектор полностью очищен, и явно отмечает сохраняющуюся угрозу.
- `JAZZ-UI-RIS-002-AC-008` — runtime RU+EN: auto-resolve, сектор, квест с подставленными quest-note params, силы, потери и два named elites отображаются без literal placeholder, raw id, английской вставки в RU и грамматической зависимости от пола.
- `JAZZ-UI-RIS-002-AC-009` — runtime old-save: после переключения RU↔EN существующие AAR, queued/received sighting и obit, strategy archive отображаются на текущем языке; старый AAR восстанавливает доступные outcome/quest provenance/time/counts, а невосстановимая часть заменяется локализованной краткой формой.
- `JAZZ-UI-RIS-002-AC-010` — runtime: серия Strategy доставляет `Network` первой, затем только наблюдённые темы; stale `last_mailed_tier` без brief в inbox, скрытый squad/task/report и неизменившийся уже видимый squad не открывают материал; между двумя strategy mails ≥24h от фактического inbox time, общий desk spacing ≥5h, Load/ReloadLua не создают дублей.
- `JAZZ-UI-RIS-002-AC-011` — runtime: после первого strategy mail раздел появляется в Bulletin и показывает только доставленные записи в порядке получения; до него раздел отсутствует.
- `JAZZ-UI-RIS-002-AC-012` — generated/static: `_validate_items_quick.py` OK; generated-sync audit без нового RIS-рассогласования; один активный `System_RIS_Strategy.lua` в load graph; ровно 9 Strategy Email resources и ни одного старого `LegionTier1…5`; metadata `last_changes` не содержит raw newline.
- `JAZZ-UI-RIS-002-AC-013` — docs: `ris-intelligence.md`, `file-coverage.md`, wiki и showcase RU/EN согласованы с принятым runtime и не выдают BLOCKED scope за shipped.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: Email/`ReceiveEmail`, PDA browser, `AutoResolveChoice`/`AutoResolvedConflict`, `ConflictStart`/`CombatStart`/`UnitDiedOnSector`/`ConflictEnd`, squad/outpost state Legion AI, localization T-values.
- Saves: `gv_JAZZ_RIS` получает versioned schema и миграцию plain-text AAR/queued/received context. MapVar `g_JAZZ_RIS_CombatSnaps` schema 3 хранит snapshots по sector, объединяет satellite/tactical участника по `session_id` и перестраивает временные handles schema 1/2. Старые архивные данные не удаляются без локализованной fallback-сводки.
- Network/determinism: strategy observer читает synced GameVar/squad state; AAR хранит deterministic keys и параметры; локальный язык не записывается в synced gameplay decisions.
- Generated data: меняются Email ModItems в `items.lua`, code registration в `metadata.lua`, generated content bank и две runtime localization tables.
- Cross-package references: читаются стабильные `JAZZ_Legion_*` UnitData IDs из `jazz-units`; sibling repository не изменяется.
- Rollback/recovery: новый strategy code можно снять из load graph; неизвестные поля GameVar безопасно игнорируются. Generated outputs восстанавливаются повторным применением зафиксированного copy bank.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Этап 1: канонический style guide/copy bank, полный RU+EN editorial pass и автоматический аудит.
- Этап 2: generated apply для UI, писем, досье, AAR и runtime CSV; исправление obit/sighting/two-stage dossier.
- Этап 3: language-neutral AAR/queue schema, old-save migration и корректный накопительный combat snapshot.
- Этап 4: `System_RIS_Strategy.lua`, девять Email и Bulletin archive.
- Этап 5: localization/generated validators, runtime RU/EN/old-save acceptance, technical/wiki/showcase sync.
- Declared write set и exclusive resources указаны во frontmatter.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner (chat: «утверждаю… целиком сделать RIS с хорошими грамотными текстами»; timing 2h/7h; архивы перерисовывать на текущем языке).
- Дата: 2026-08-07.

## Статус реализации

- `STATIC IMPLEMENTED / LOADED`: пять R.I.S. code-файлов, generated Content,
  24 Email, 9 Strategy resources, обе runtime localization tables и metadata
  load order применены. `System_RIS_Strategy.lua` загружается после
  `Guardpost_Patrols.lua`.
- `RUNTIME ACCEPTANCE PENDING`: AC-004…011 не проверены в живой JA3/DAP и
  остаются `BLOCKED`. Статическая загрузка в metadata не считается runtime
  PASS.
- Попытка runtime smoke 2026-08-07 остановилась до attach: `JA3Debug.exe`
  показал `Unable to start the game. Please restart.`, Steam process отсутствовал,
  DAP `127.0.0.1:8165` не открылся. Это environment blocker, не evidence AC.
- Статус spec остаётся `approved` до завершения RU/EN, old-save, combat и
  Strategy/Bulletin acceptance.

## Evidence

- `JAZZ-UI-RIS-002-AC-001`: `PASS (human/editorial)` — рассмотрены 218
  двуязычных локализуемых строк в 156 content records: identity/sender 3,
  welcome 3, UI 13, AAR
  60, field mail 7, unit dossiers 38, quest dossiers 4, supply briefs 11,
  Strategy 9, reserved extras 8. Records с title+body дают по две строки.
  Supply briefs отдельно вычитаны в их loadout-bound каноне;
  `_audit_ris_copy.py` подтверждает полное category coverage и guards против
  фактически опровергнутых формулировок о позиции, погоде, снаряжении и
  несуществующей красной отметке маршрута.
- `JAZZ-UI-RIS-002-AC-002`: `PASS (static/localization)` —
  `_audit_ris_copy.py` сообщает 218/218 bilingual IDs, exact placeholders и
  ожидаемые категории. Актуальный strict localization audit завершился с exit
  0: `needs Russian=0`, `needs English=0`, active/Game/Russian collisions 0.
  Runtime mod-only ID sets совпадают, разница 0/0. Аудитор отдельно видит 185
  dormant collisions вне active R.I.S. scope.
- `JAZZ-UI-RIS-002-AC-003`: `PASS (static)` — второй apply и следующий
  `_apply_ris_editorial.py --check` дали `changed=0`, `unchanged=8`; check
  файлов не записал. Compatibility wrappers используют тот же банк/apply и не
  содержат второй редакции.
- `JAZZ-UI-RIS-002-AC-004`: `BLOCKED (runtime)` — требуется JA3 RU+EN mail
  smoke. Targeted lupa-regression подтверждает, что combat-deferred row не
  меняет delivery state, а obituary отмечается только после inbox receipt.
- `JAZZ-UI-RIS-002-AC-005`: `BLOCKED (runtime)` — требуется JA3 two-stage
  dossier smoke. Targeted lupa-regression подтверждает delivery gate и переход
  short→full на третьем убийстве.
- `JAZZ-UI-RIS-002-AC-006`: `BLOCKED (runtime)` — требуется JA3
  multi-phase/map-placed combat smoke. Targeted lupa-regression подтверждает
  две фазы, map-only units, cumulative KIA/WIA, baseline injury и named fate,
  preserved quest с scalar note params, enemyNeutral side и living-hostile
  warning.
- `JAZZ-UI-RIS-002-AC-007`: `BLOCKED (runtime)` — требуется JA3
  surviving-hostile scenario. Двухфазный lupa-сценарий подтверждает
  `hostiles_remain=true` для живого map-placed противника и исключает
  `conflict_ignore`.
- `JAZZ-UI-RIS-002-AC-008`: `BLOCKED (runtime)` — требуется representative
  RU+EN AAR/auto-resolve smoke. Targeted lupa-regression подтверждает
  satellite start forces, KIA/WIA, concurrent-sector isolation, различение
  нового и повторного `ConflictEnd` в ту же campaign minute, surviving-merc
  auto-resolve correction, recovery после пропущенного `ConflictStart`, named
  fates без ложного wound от старой травмы, quest-note substitution и
  confirmed-kill accounting.
- `JAZZ-UI-RIS-002-AC-009`: `BLOCKED (runtime)` — требуется old-save RU↔EN
  migration smoke. Targeted lupa-regression подтверждает received
  sighting/obit re-resolution (включая elite session ID), нормализацию старых
  wrapped IDs с engine-like `Untranslated`, generic fallback для неизвестного
  или удалённого contact, восстановление delivery flags из фактически
  полученного inbox, original Strategy inbox time и legacy AAR reconstruction
  времени и active-quest provenance из preserved fields.
- `JAZZ-UI-RIS-002-AC-010`: `BLOCKED (runtime)` — требуется Strategy
  order/cadence/load smoke. Targeted lupa-regression подтверждает одну pending
  row, 5h/24h desk contract, inbox-authoritative supply-brief gate и отсутствие
  unlock по stale `last_mailed_tier`, скрытому squad-state или доставленному
  внутреннему разведотчёту; Awakening требует post-delivery изменения
  наблюдаемой activity.
- `JAZZ-UI-RIS-002-AC-011`: `BLOCKED (runtime)` — требуется Bulletin
  visibility/archive smoke.
- `JAZZ-UI-RIS-002-AC-012`: `PARTIAL (targeted static) / BLOCKED (broad
  generated-sync)` — `_validate_items_quick.py` PASS для `items.lua` +
  `metadata.lua`, включая отсутствие raw newline в `last_changes`; R.I.S.
  copy/apply checks PASS; obsolete `LegionTier1…5` resources удалены; один
  `System_RIS_Strategy.lua` стоит после `Guardpost_Patrols.lua`;
  `_test_ris_contract.py` даёт 7/7 PASS. Общий generated-sync baseline всё ещё
  падает на 489 не связанных с R.I.S. companion errors и 28 warnings
  (core `jazz`: 409/13); совпадений по R.I.S. в blocking report нет.
- `JAZZ-UI-RIS-002-AC-013`: `PASS (static docs)` — technical, coverage,
  compatibility/testing, wiki, cross-link и showcase RU/EN описывают loaded
  implementation и явно оставляют live acceptance pending. Полный
  `check-system-docs.ps1 -SuiteRoot .` остаётся non-zero на 272
  repository-wide pre-existing findings (coverage/links/trailing spaces/skill
  metadata); изменённые R.I.S.-страницы новых ошибок не добавили. Единственное
  упоминание затронутого `file-coverage.md` — существующая ссылка на
  `JAZZ%20Maps`, не изменённая этой задачей.

## Documentation delta

- Новый канон: `docs/design/ris-editorial-style.md` и существующий `ris-major-strategy.md`.
- Current-state: `docs/technical/systems/ris-intelligence.md` + `file-coverage.md`
  после подключения `System_RIS_Strategy.lua`; save/test contracts в
  `docs/technical/compatibility.md` и `docs/technical/testing.md`.
- Player-facing: `docs/wiki/ris.md`, связь из `docs/wiki/legion-global-ai.md`, `docs/showcase/ru/ris.md`, `docs/showcase/en/ris.md`.
- Tooling: новый copy/apply/audit/test pipeline и compatibility wrappers описаны
  в `docs/tools/README.md`.
