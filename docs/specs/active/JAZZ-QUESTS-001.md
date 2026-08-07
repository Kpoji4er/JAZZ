---
id: JAZZ-QUESTS-001
status: approved
owner: project-owner
systems:
  - ernie-quests
  - conversations
  - map-markers
  - localization
  - merc-recruitment
repositories:
  - jazz
  - jazz-maps
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - docs/specs/active/JAZZ-QUESTS-001.md
  - Localization/Strings.csv
  - Localization/RussianManual.csv
  - Localization/EnglishManual.csv
  - Russian.csv
  - English.csv
  - metadata.lua
  - docs/tools/_apply_maps_quest_repairs.py
  - docs/tools/_audit_maps_quest_contract.py
  - docs/tools/README.md
  - docs/technical/systems/maps-quests-dialogue.md
  - docs/technical/systems/maps-quests-content-catalog.md
  - docs/wiki/grand-chien-map.md
  - docs/showcase/ru/ernie-campaign.md
  - docs/showcase/en/ernie-campaign.md
  - docs/showcase/ru/grand-chien-map.md
  - docs/showcase/en/grand-chien-map.md
  - ../jazz-maps/items.lua
  - ../jazz-maps/metadata.lua
  - ../jazz-maps/ModTextsMaps.csv
  - ../jazz-maps/InventoryItem/JazzQuestItem_AmmoBox.lua
  - ../jazz-maps/InventoryItem/JazzQuestItem_MinesBox.lua
  - ../jazz-maps/UnitData/JAZZ_Ernie_Locals_M2_SaveMyFamily_Woman.lua
  - ../jazz-maps/Maps/YWtYj6q/objects.lua
  - ../jazz-maps/Maps/qTn3d4w/objects.lua
  - ../jazz-maps/Maps/cd6xgVh/objects.lua
  - ../jazz-maps/Maps/bVp47D/objects.lua
  - ../jazz-maps/Maps/qJApdx/objects.lua
  - ../jazz-maps/Maps/gsSMikN/objects.lua
exclusive_resources:
  - jazz-maps/items.lua
  - jazz-maps/metadata.lua
  - jazz-maps/ModTextsMaps.csv
  - jazz-maps/map-YWtYj6q-K5
  - jazz-maps/map-qTn3d4w-I2
  - jazz-maps/map-cd6xgVh-M4
  - jazz-maps/map-bVp47D-K6
  - jazz-maps/map-qJApdx-J7
  - jazz-maps/map-gsSMikN-K4
  - quest-RebelsSavior
  - quest-Jazz_Doctor_need_Help
  - quest-Jazz_ClearTheWay
  - quest-RescueTeam
  - quest-JAZZ_REBELS_0_MeetTheRebels
  - quest-JAZZ_REBELS_1_SeizeTheOutlook
  - quest-Jazz_DeadPigs
  - quest-Jazz_Alkatraz
  - quest-JAZZ_Ernie_Locals_M2_SaveMyFamily
  - quest-RescueHerMan
  - quest-ReduceCrocodileCampStrength
  - inventory-item-JazzQuestItem_AmmoBox
  - inventory-item-JazzQuestItem_MinesBox
  - conversation-BarrySeal_Recruit
related_decisions:
  - JAZZ-LOC-002
approved_by: project-owner
---

# JAZZ-QUESTS-001: ремонт квестов карт и найм Barry Seal

## Проблема

Статический аудит десяти кастомных квестов `jazz-maps` нашёл несколько
нарушений состояния квестов, выдачи и удаления предметов, условий завершения,
связей с картами и текста журнала:

- `RebelsSavior` завершается уже при принятии, поэтому поиск четырёх винтовок и
четырёх аптечек не является реальным условием завершения.
- Финальная реплика `RebelsSavior` обещает потерявшего память наёмника у палаток
K5, однако на карте и в разговоре награда не подключена.
- `Jazz_Doctor_need_Help` пытается удалить два квестовых ящика из инвентаря
доктора, а все три раненых повстанца используют один общий флаг лечения.
- `Jazz_ClearTheWay` может повторно считать один сектор после потери и
перезахвата.
- `RescueTeam` считает заложника спасённым по смерти палачей, не проверяя самого
заложника.
- `JAZZ_REBELS_0_MeetTheRebels` можно завершить у лидера без нормальной выдачи
квеста.
- `JAZZ_REBELS_1_SeizeTheOutlook` допускает отчёт без подтверждённого захвата M4,
а союзные маркеры в M4 используют M3 в условии despawn.
- `Jazz_DeadPigs` оставляет ветку принятия повторяемой, обещает отсутствующее
подкрепление и не даёт в журнале ясную цель K6.
- `Jazz_Alkatraz` не имеет отображаемого имени и записей журнала.
- Несколько RU/EN строк содержат смысловые ошибки, неканоничные названия
локаций, пустую реплику или повреждённый UI-тег.
- `ReduceCrocodileCampStrength` создаёт locked-конфликт в P17, но по прибытии
подкрепления снимает `locked` у H14; P17 может остаться навсегда
заблокированным после победы.
- `RescueHerMan.TCE_RaidersConversation` одновременно требует J7 в condition и
I3 в `requiredSectors`, поэтому автодиалог `Herman_1` недостижим.
- Psycho-ветка `JAZZ_Ernie_Locals_M2_SaveMyFamily` обещает игроку большой
алмаз, но устанавливает только failure/loyalty effects и ничего не выдаёт.
- Иконки двух квестовых ящиков подтверждённо назначены наоборот:
`JazzQuestItem_AmmoBox` показывает `MinesBox.png`, а
`JazzQuestItem_MinesBox` — `AmmoCrate.png`.
- После исправления sector gate `RescueHerMan` всё ещё не запускается
  полностью: J7-маркер Германа не входит в группу `Herman`, а обе custom
  sector-копии J7 потеряли vanilla `SE_OnEnterMapVisual`, запускавший
  `EncounterHerman`.
- Пять обещанных бойцов Призрака на K4 одновременно удовлетворяют spawn и
  despawn conditions из-за stale-сектора M4, поэтому никогда не создаются.
- Кики в M3 смертна, находится рядом с боевыми Legion-маркерами, а
  `SaveMyFamily` не имеет death/failure fallback; её гибель оставляет
  `WomenSaved` недостижимым.

Аудит подтвердил, что `Merc_BarrySeal` не является одной картинкой. В
`jazz-units` уже загружен полноценный `UnitData` с `IsMercenary = true`,
характеристиками, внешностью, экипировкой, портретами и VoiceResponse. В
`jazz-maps` отсутствует именно квестовая привязка, маркер и действие найма.

## Цели

- Сделать выдачу, прогресс, завершение и награды затронутых квестов
однократными и проверяемыми.
- Подключить существующего `Merc_BarrySeal` как бесплатного локального рекрута,
открывающегося после настоящей сдачи снабжения повстанцам.
- Устранить подтверждённые расхождения между разговорами, журналом и картами.
- Сохранить авторский тон диалогов и дать естественный согласованный RU/EN текст.
- Оставить воспроизводимые apply/audit-инструменты и синхронизировать
player-facing документацию.

## Non-goals

- Создание второго `UnitData`, новых портретов или полного нового голосового
набора для Barry Seal.
- Перебалансировка характеристик, перков и экипировки `Merc_BarrySeal`.
- Переписывание bio, stats или реальных биографических подробностей Barry
  Seal: в этом change set меняются только квестовые реплики и локальный найм.
- Переработка всех vanilla-квестов или всех карт материка.
- Массовая редактура незатронутых разговоров либо смягчение взрослого тона
персонажей.
- Изменение наград и боевого баланса квестов, кроме явно описанного
подкрепления `Jazz_DeadPigs` и подключения Barry Seal.
- Изменение `SetTimer.Name` у обороны маяка: это внутренний ключ; игроку
показывается локализуемый `Label`.
- Автоматическое исправление неоднозначного состояния уже завершённых квестов
в старых сохранениях.

## Требования

- `JAZZ-QUESTS-001-REQ-001` — использовать существующий публичный ID
`Merc_BarrySeal` из `jazz-units`; не создавать дубликат UnitData. До правки
карты в Mod Editor подтвердить загрузку `UnitData/Merc_BarrySeal.lua`, обоих
портретов и VoiceResponse preset с тем же ID.
- `JAZZ-QUESTS-001-REQ-002` — принятие `RebelsSavior` должно устанавливать
только `Given`; `Completed` устанавливается только в ветке фактической сдачи
ровно четырёх `ZastavaM76` и четырёх `Medkit`. Предметы удаляются из
инвентаря игрока, а отдельный однократный флаг `SuppliesDelivered`
фиксирует выполненную сдачу.
- `JAZZ-QUESTS-001-REQ-003` — после `SuppliesDelivered` у палаток K5 появляется
один маркер группы `BarrySeal_Recruit` с `UnitDataDefId = Merc_BarrySeal`.
Отдельный разговор `BarrySeal_Recruit` должен предлагать бесплатное
присоединение через `UnitJoinAsMerc { TargetUnit = "BarrySeal_Recruit", Merc = "Merc_BarrySeal" }`. После успешного присоединения выставляется
`BarryJoined`, повторный маркер и повторный найм невозможны. Полный отряд
обрабатывается штатным созданием нового player squad. В разговоре Barry —
спокойный американский пилот-контрабандист с сухим юмором; он не называется
агентом ЦРУ/DEA, разведчиком или участником реальной политики. Не использовать
экспозицию про картели, наркотики, Кастро, Арулько или потерю памяти.
- `JAZZ-QUESTS-001-REQ-004` — в `Jazz_Doctor_need_Help` квестовые
`JazzQuestItem_AmmoBox` и `JazzQuestItem_MinesBox`, а также `Meds` удаляются
через player-targeting `UnitTakeItem { AnySquad = true }`; доктор не обязан
владеть этими предметами. Финальная hand-in ветка повторно проверяет текущее
наличие всех трёх ресурсов и не полагается только на когда-либо выставленные
TCE-флаги.
- `JAZZ-QUESTS-001-REQ-005` — три раненых повстанца I2 получают независимые
флаги `InjuredRebel1_Healed`, `InjuredRebel2_Healed` и
`InjuredRebel3_Healed`; общий итог лечения устанавливается только после всех
трёх. Лечение одного не заменяет и не скрывает остальных. Запись журнала
остаётся видимой, пока не выполнены и сдача снабжения, и лечение троих.
- `JAZZ-QUESTS-001-REQ-006` — `Jazz_ClearTheWay` считает каждый из пяти целевых секторов один раз. Для каждого сектора используется отдельный one-shot флаг; повторный захват того же сектора не увеличивает `SectorsCaptured`, а завершение остаётся на `>= 5`. Реплика отчёта и
`GrantExperienceSector` также исполняются только один раз.
- `JAZZ-QUESTS-001-REQ-007` — `RescueTeam.Rescued` устанавливается только если
палачи мертвы и `Rebel_Hostage` жив. Смерть заложника переводит квест в
явный failed/outcome state и не открывает благодарственную реплику.
- `JAZZ-QUESTS-001-REQ-008` — финальная ветка лидера в
`JAZZ_REBELS_0_MeetTheRebels` требует `Given = true` и
`Completed = false`; обход выдающего разговор в M1 не позволяет завершить
квест или получить награду. Каждая ветка согласия, включая `+5` loyalty,
является one-shot и недоступна после завершения.
- `JAZZ-QUESTS-001-REQ-009` — состояние захвата в
`JAZZ_REBELS_1_SeizeTheOutlook` называется `M4_UnderControl`, выставляется
только при контроле M4 и обязательно для финального отчёта. Все маркеры
`Rebels_Help` и Ghost в M4 используют M4, а не M3, в sector-dependent
despawn conditions.
- `JAZZ-QUESTS-001-REQ-010` — `Jazz_DeadPigs` сбрасывает legacy
`NotStarted`/использует однократный `Accepted`, поэтому принятие и выдача
40-мм боеприпасов не повторяются. `DiamondBriefcase` сохраняется как один
аванс при первом разговоре и защищается one-shot флагом `AdvancePaid`.
После принятия в K6 один раз появляются четыре союзника Балумбы:
два `ThugCutter`, один `ThugGoon_Stronger` и один `ThugSniper`; все входят в
группу `DeadPigs_Reinforcements`, имеют сторону `ally`, не входят в
вражескую группу `Pigs` и не блокируют завершение.
- `JAZZ-QUESTS-001-REQ-011` — `Jazz_Alkatraz` получает локализованные
`DisplayName` «Зачистить бункер / Clear the Bunker» и записи журнала:
зачистить подземный L6, вернуться к выдавшему квест NPC и зафиксировать
outcome. Контроль сектора не подменяет условие уничтожения врагов без
runtime-подтверждения. Отказ не уничтожает единственную briefing-ветку:
последующий разговор предоставляет явное «мы передумали» до `Given`.
- `JAZZ-QUESTS-001-REQ-012` — исправить и синхронно локализовать минимум
следующий целевой набор:
  - `805716788538`: «Мы в спасатели не нанимались» /
  `We didn't sign up to be rescuers`;
  - `191474319874`: «Приговорённый повстанец находится на пирсе» /
  `The condemned rebel is on the pier`;
  - `724348814002`: «Спасённый повстанец возвращается в лагерь…» /
  `The rescued rebel is returning to camp…`;
  - `995472785344`: «Снабжение для повстанцев» /
  `Supplies for the Rebels`;
  - `484530953168`: явно потребовать четыре `Zastava M76` и четыре `Medkit`;
  - `555833394027`: явно перечислить 50 `Meds`, оба ящика из I3 и трёх
  раненых повстанцев;
  - `890000000000795`: заменить сломанный `<L3>` на валидный выделенный текст
  сектора L3;
  - во всех затронутых строках использовать M4 как
  «Смотровая площадка / The Outlook»;
  - `Jazz_DeadPigs`: добавить прямую цель зачистить лагерь перебежчиков K6 и
  вернуться к Балумбе, сохранив стих как flavour;
  - `706580608154`: заменить неверный `<SectorName('M7')>` на
  `<SectorName('J7')>`;
  - удалить пустую `ConversationLine` в ветке Kiki `Goodbye2`;
  - добавить естественные RU/EN строки разговора найма Barry Seal и нового
  журнала `Jazz_Alkatraz`.
- `JAZZ-QUESTS-001-REQ-013` — все новые и изменённые mod-only строки проходят
единый каталог `Localization/Strings.csv`, обе manual memories и синхронный
экспорт `Russian.csv`/`English.csv`; numeric ID, placeholders и игровые теги
не переиспользуются между разными source strings.
- `JAZZ-QUESTS-001-REQ-014` — изменения generated data выполняются
source-aware транзакцией: `jazz-maps/items.lua`, затронутые map
`objects.lua`, companion/editor exports и `metadata.lua` должны описывать
один контракт. Apply и статический аудит сохраняются в `docs/tools/` и
документируются в `docs/tools/README.md`.
- `JAZZ-QUESTS-001-REQ-015` — в
`ReduceCrocodileCampStrength.TCE_ReinforcementsArrived` снимать
`conflict.locked` только у `gv_Sectors.P17`, где
`TCE_ReinforcementsConflict` создал locked-конфликт. H14 не изменяется.
- `JAZZ-QUESTS-001-REQ-016` —
`RescueHerMan.TCE_RaidersConversation.requiredSectors` содержит J7 и
согласован с `PlayerIsInSectors { "J7" }`; I3 из этой TCE удаляется.
J7-маркер `UnitDataDefId = Herman` входит одновременно в группы
`HermanShaking` и `Herman`. Обе generated-копии сектора J7 получают
remapped `SE_OnEnterMapVisual` из vanilla I3: при
`RescueHerMan.Failed = false` и `HermanRescued = false` сначала выполняется
`NeutralNPCDontMove { TargetUnit = "Herman" }`, затем
`PlaySetpiece { setpiece = "EncounterHerman" }`.
- `JAZZ-QUESTS-001-REQ-017` — Psycho-ветка
`JAZZ_Ernie_Locals_M2_SaveMyFamily`, в которой реплики однозначно говорят о
присвоении алмаза, выдаёт ровно один `BigDiamond` до установки `Failed`;
текст и normal-completion reward не подменяются.
- `JAZZ-QUESTS-001-REQ-018` — поменять местами icon/subicon refs:
`JazzQuestItem_AmmoBox` использует `AmmoCrate.png`, а
`JazzQuestItem_MinesBox` — `MinesBox.png`; синхронизировать
`jazz-maps/items.lua` и оба companion Lua.
- `JAZZ-QUESTS-001-REQ-019` — все reward-bearing conversation paths в
`Jazz_ClearTheWay`, `JAZZ_REBELS_0_MeetTheRebels` и `Jazz_DeadPigs`
защищены комбинацией `AutoRemove` и явных `Given`/`Completed`/one-shot
conditions; повторный вход в разговор не дублирует XP, loyalty, гранату,
loot table или квестовую награду.
- `JAZZ-QUESTS-001-REQ-020` — пять payoff-маркеров Призрака в K4
(`gsSMikN`) используют K4 в sector-dependent despawn condition, а пять
маркеров в M4 (`cd6xgVh`) используют M4. После
`RebelGhostAgreedToHelp = true` группа `Rebels_Help` появляется на K4 один
раз и не удаляется в тот же spawn tick.
- `JAZZ-QUESTS-001-REQ-021` — локальный UnitData Кики
`JAZZ_Ernie_Locals_M2_SaveMyFamily_Woman` получает `immortal = true` и
`ImportantNPC = true`; до разговора, выставляющего `WomenSaved`, случайный
бой не может сделать completion недостижимым.

### Канонический диалог найма Barry Seal

Диалог использует образ пилота-контрабандиста как свободное художественное
вдохновение, не пересказывает биографическую статью и не делает персонажа
сотрудником спецслужб.

Сержант после сдачи снабжения:

- RU: «Вы нас здорово выручили. У палаток ждёт один американец — Берриман Сил,
  пилот и контрабандист. Его последний рейс закончился здесь не по плану. Он
  ищет новую команду; думаю, вы найдёте общий язык».
- EN: “You did us a real favor. There’s an American waiting by the tents —
  Berriman Seal, a pilot and smuggler. His last run ended here badly. He’s
  looking for a new crew; I think you’ll understand each other.”

Приветствие Barry:

- RU: «Сержант сказал, это вы доставили винтовки. Хороший знак. В моём деле
  люди чаще теряют груз, деньги или голову — иногда всё сразу».
- EN: “The sergeant says you delivered the rifles. That’s a good sign. In my
  line of work, people usually lose the cargo, the money, or their heads —
  sometimes all three.”

Вариант игрока «Пойдёшь с нами? / Coming with us?»:

- RU: «Почему бы и нет? Самолёта у меня больше нет, груз сгорел, а сидеть без
  дела я не умею. Оставьте место в отряде — маршрут обсудим по дороге».
- EN: “Why not? My plane is gone, the cargo burned, and I’ve never been good
  at sitting still. Save me a place — we’ll discuss the route on the way.”
- После этой реплики выполняется `UnitJoinAsMerc`, затем устанавливается
  `BarryJoined`.

Вариант игрока «Не сейчас / Not now»:

- RU: «Как скажете. Я пока здесь».
- EN: “Your call. I’ll be here for now.”
- Разговор остаётся доступен до успешного найма.

## Инварианты и ограничения

- Пакет-владелец квестов, разговоров и объектов карт — `jazz-maps`;
`jazz-units` остаётся владельцем `Merc_BarrySeal`.
- Публичные ID существующих квестов, предметов, секторов и `Merc_BarrySeal`
не меняются.
- Не затрагивать посторонние незакоммиченные изменения в трёх репозиториях.
- Не переписывать `jazz-maps/items.lua` целиком и не принимать шумную
регенерацию несвязанных ModItem.
- В K6 группа `Pigs` остаётся единственным боевым target group квеста;
союзники не должны получить этот group ID.
- Locked-конфликт P17 должен разблокироваться до штатного разрешения боя;
H14 не является частью этого квестового перехода.
- `UnitJoinAsMerc` выполняется раньше установки `BarryJoined`, чтобы изменение
spawn condition не удалило map-unit до преобразования в merc.
- Новые quest vars считаются `false` при `nil`; код не должен создавать
несинхронные Lua-глобалы или недетерминированный RNG.
- Полная исправленная цепочка гарантируется на новой кампании. Старые
`Completed`/`Failed` не сбрасываются автоматически.
- Действующие взрослые реплики сохраняют авторский смысл; исправляются
грамматика, фактическая точность, теги и терминология.

## Acceptance criteria

- `JAZZ-QUESTS-001-AC-001` — на новой кампании принятие `RebelsSavior` оставляет
`Completed = false`; без полного набора сдача недоступна, а с полным набором
ровно четыре винтовки и четыре аптечки удаляются и квест завершается один раз.
- `JAZZ-QUESTS-001-AC-002` — после настоящей сдачи снабжения Barry Seal
появляется у палаток K5, говорит с игроком и присоединяется как
`Merc_BarrySeal`; после найма нет второго маркера или повторной ветки.
RU/EN реплики соответствуют каноническому диалогу: пилот-контрабандист, без
ЦРУ/DEA, Арулько и амнезии.
- `JAZZ-QUESTS-001-AC-003` — портреты, внешний вид, экипировка и имеющиеся
субтитры VoiceResponse Barry Seal работают после локального найма; полный
исходный отряд создаёт новый player squad без потери рекрута.
- `JAZZ-QUESTS-001-AC-004` — доктор принимает 50 `Meds` и оба ящика из
инвентаря player squad; предметы исчезают один раз, ошибок из-за пустого
инвентаря NPC нет. Если любой ресурс после срабатывания acquisition TCE был
потрачен или выложен, hand-in снова недоступен до восстановления количества.
- `JAZZ-QUESTS-001-AC-005` — лечение каждого из трёх повстанцев меняет только
его состояние; общий objective и скрытие записи происходят после третьего,
а не после первого.
- `JAZZ-QUESTS-001-AC-006` — последовательность
`захват L2 -> потеря L2 -> повторный захват L2` увеличивает
`Jazz_ClearTheWay.SectorsCaptured` только на один; пять разных целевых
секторов завершают objective и выдают XP ровно один раз.
- `JAZZ-QUESTS-001-AC-007` — живой заложник после смерти палачей даёт
`Rescued`; мёртвый заложник даёт failure/outcome и никогда не открывает
благодарность за спасение.
- `JAZZ-QUESTS-001-AC-008` — лидер L1 не завершает
`JAZZ_REBELS_0_MeetTheRebels`, если квест не был выдан; нормальный маршрут
M1 -> L1 завершается и выдаёт награду/+5 loyalty один раз.
- `JAZZ-QUESTS-001-AC-009` — отчёт по The Outlook недоступен до контроля M4;
наличие другой player squad в M3 не удаляет союзников с карты M4.
- `JAZZ-QUESTS-001-AC-010` — повторный разговор с Балумбой не дублирует
`DiamondBriefcase` или 40-мм боеприпасы; в принятом бою K6 ровно четыре
заявленных союзника появляются один раз и не мешают смерти всей группы
`Pigs`.
- `JAZZ-QUESTS-001-AC-011` — `Jazz_Alkatraz` имеет корректный заголовок,
активную цель и outcome; фактическое завершение требует подтверждённой
зачистки L6 Underground и отчёта. После первого отказа квест можно принять
при повторном разговоре.
- `JAZZ-QUESTS-001-AC-012` — RU и EN runtime показывают согласованный текст без
пустой реплики, `<missing translation>`, повреждённого `<L3>` и смешения
`Lookout`/`Overlook`/`Outlook Point`; журнал `RescueHerMan` показывает J7,
а не морской M7.
- `JAZZ-QUESTS-001-AC-013` — `_audit_maps_quest_contract.py`,
локализационный аудит, `_validate_items_quick.py` для `jazz-maps` и
профильный generated-data sync завершаются без новых ошибок; фактический
diff не выходит за declared write set.
- `JAZZ-QUESTS-001-AC-014` — полный ручной smoke matrix ниже пройден на новой
кампании; существующее сохранение с частично начатыми квестами загружается
без Lua/assert ошибок, но ему не обещается автоматическое исправление уже
записанного неоднозначного outcome.
- `JAZZ-QUESTS-001-AC-015` — сценарий P17
`бой закончился -> подкрепление прибыло -> подкрепление уничтожено`
оставляет `gv_Sectors.P17.conflict.locked = false` и позволяет штатно
завершить конфликт; состояние H14 не меняется.
- `JAZZ-QUESTS-001-AC-016` — при входе игрока в J7 и приближении к
`TriggerConversation` вне боя сначала воспроизводится `EncounterHerman`, затем
один раз запускается `Herman_1`; actor/group assignments разрешаются, вход в
I3 для этого не требуется.
- `JAZZ-QUESTS-001-AC-017` — повторный запуск трёх reward-bearing разговоров
не меняет XP, loyalty и количество выданных предметов после первого
успешного результата.
- `JAZZ-QUESTS-001-AC-018` — Psycho outcome `SaveMyFamily` кладёт один
`BigDiamond` в player inventory; одновременно получить этот алмаз и
normal-completion reward невозможно.
- `JAZZ-QUESTS-001-AC-019` — в inventory UI ammo box показывает визуально
проверенный `AmmoCrate.png`, mines box — `MinesBox.png`; Icon и SubIcon
совпадают в generated и companion слоях.
- `JAZZ-QUESTS-001-AC-020` — после обещания помощи и первого входа в K4 пять
юнитов `Rebels_Help` существуют на карте и не despawn в тот же tick; выход из
K4 очищает их по ожидаемому условию. Отдельная player squad в M3 не влияет на
маркеры M4.
- `JAZZ-QUESTS-001-AC-021` — Кики переживает бой рядом с мостом, остаётся
доступной для разговора и выставляет `WomenSaved`; зелёный important-NPC badge
виден игроку.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: используются штатные `QuestSetVariable*`,
`UnitTakeItem`, `UnitJoinAsMerc`, group/sector conditions и map markers;
vanilla ID не заменяются.
- Saves: добавляются quest vars и map spawn conditions. `nil` трактуется как
false. Уже записанные `Completed`/`Failed` сохраняются; для полной цепочки
выпуск помечается `new game recommended`.
- Network/determinism: эффекты и маркеры должны исполняться host-authoritative
штатными сетевыми путями; новый произвольный RNG не добавляется.
- Generated data: изменение затрагивает `jazz-maps/items.lua`, два
  InventoryItem companion, один UnitData companion и шесть `objects.lua`;
  Mod Editor не должен регенерировать несвязанные ModItem.
- Cross-package references: `jazz-maps` получает runtime-зависимость на уже
загруженный `jazz-units` ID `Merc_BarrySeal`; порядок профильных пакетов
assets + units + maps + jazz сохраняется.
- Rollback/recovery: откат всех связанных generated/map/localization файлов
выполняется одним логическим revert; apply/audit-скрипты позволяют
воспроизвести и проверить целевой diff.

## План и ownership

- Пакет-владелец: `jazz-maps` для runtime-квестов и карт; `jazz` для spec,
локализации, инструментов и документации; `jazz-units` для существующего
Barry Seal, без ожидаемой правки его UnitData.
- Исполнитель: Cursor-agent для source-aware правок и генерации; project-owner
для ручных Mod Editor/Map Editor действий и runtime acceptance.
- Reviewer: независимый агент для generated diff и project-owner для
editor/runtime/human evidence.
- Declared write set: frontmatter этой спецификации.
- Exclusive resources: затронутые QuestDef/Conversation, `jazz-maps/items.lua`
  и шесть карт; параллельная работа с ними запрещена до завершения change set.
- `JAZZ-LOC-002` сейчас также объявляет `jazz-maps/items.lua`; реализацию этой
спецификации начинать после фиксации/освобождения его текущего generated diff
либо выполнять как явно согласованную последовательную source-aware транзакцию.

### Что сделать вручную в Mod Editor

1. Загрузить канонический профиль `assets + units + maps + jazz` и убедиться,
  что `Merc_BarrySeal` доступен в выборе `UnitData` и `UnitJoinAsMerc.Merc`.
2. В Quest/Conversation Editor применить требования REQ-002, REQ-004,
  REQ-006--REQ-012 и REQ-015--REQ-019.
3. Добавить `SuppliesDelivered` и `BarryJoined` в `RebelsSavior`, создать
  `BarrySeal_Recruit`, сохранить новые localization IDs через редактор.
4. В I2 (`qTn3d4w`) развести три wounded-marker contract на три индивидуальных
  healed-флага.
5. В M4 (`cd6xgVh`) заменить M3 на M4 в despawn conditions всех затронутых
  Ghost/`Rebels_Help` markers.
6. В K6 (`bVp47D`) расставить четыре союзных маркера из REQ-010 в разумных
  точках входа, не внутри вражеских spawn clusters.
7. В K5 (`YWtYj6q`) поставить `Merc_BarrySeal` у палаток, назначить группу
  `BarrySeal_Recruit` и условия появления/исчезновения из REQ-003.
8. В J7 (`qJApdx`) добавить `Herman` к группе маркера Германа и вернуть
  remapped on-enter setpiece event в обе копии sector preset.
9. В K4 (`gsSMikN`) заменить stale M4 на K4 в despawn conditions пяти
  payoff-маркеров Призрака.
10. В UnitData Кики выставить `immortal` и `ImportantNPC`, не меняя её
  характеристики, appearance или conversation ID.
11. Сохранить редактором один раз и отдельно проверить diff каждого
  `objects.lua`, InventoryItem companion, `items.lua` и `metadata.lua`;
  отклонить несвязанный editor churn.

### Что сделать вручную с текстами

1. Просмотреть новые и изменённые реплики в реальном Conversation UI на русском
  и английском, включая длину кнопок и переносы строк.
2. Подтвердить единое название `The Outlook` и канонические item names
  `Zastava M76`, `Medkit`, `Meds`.
3. Проверить, что новые ID появились в центральном каталоге и обеих runtime
  таблицах, а package-local таблицы не перекрывают их старым текстом.

### Ручной runtime smoke matrix

1. L1: попытка прийти к лидеру без выдачи в M1; затем нормальный маршрут M1 -> L1.
2. M4: отчёт до и после захвата; отдельная player squad остаётся в M3.
3. K6: первый и повторный разговор с Балумбой, одноразовый аванс/боеприпасы,
  появление четырёх союзников и смерть всей `Pigs`.
4. I3/I2: подобрать оба ящика, собрать 50 `Meds`, лечить раненых в порядке
  2 -> 1 -> 3 и сдать доктору.
5. K5: принять `RebelsSavior`, проверить незавершённое состояние, собрать и
  сдать 4+4 предмета, поговорить с Barry, повторно войти на карту и проверить
   отсутствие дубля; повторить с полным player squad.
6. K5: отдельные ветки с живым и погибшим `Rebel_Hostage`.
7. `Jazz_ClearTheWay`: потерять и перезахватить один сектор, затем взять пять
  разных целевых секторов.
8. L6 Underground: проверить условие зачистки и сдачу `Jazz_Alkatraz`.
9. P17: воспроизвести прибытие патруля после окончания исходного боя и
  проверить разблокировку/завершение конфликта.
10. J7: подойти к `TriggerConversation` и подтвердить автозапуск `Herman_1`
    после `EncounterHerman`, без посещения I3.
11. M2: пройти Psycho outcome `SaveMyFamily`, проверить ровно один
  `BigDiamond` и отсутствие normal-completion reward.
12. Открыть оба квестовых ящика в inventory UI и визуально сверить иконки.
13. K4: после согласия Призрака проверить появление всех пяти союзников и
    отсутствие немедленного despawn.
14. M3: провести бой рядом с Кики, затем завершить её разговор.
15. Повторить ключевые UI-проходы в RU и EN; один host/client smoke для найма
  Barry и квестовых переменных.

## Решение владельца

- Статус: approved; реализация и правка шести перечисленных карт разрешены.
- Кто подтвердил: project-owner запросил спецификацию исправлений и уточнил,
что обещанный наёмник — Barry Seal, подтвердил отдельный естественный диалог
найма и образ пилота-контрабандиста без ЦРУ; меняется только квестовый диалог,
не UnitData bio. Командой «Реализуй и коммит» владелец также утвердил состав
четырёх разведчиков, briefcase как одноразовый аванс и весь остальной
нормативный scope этой версии спека.
- Дата: 2026-08-07.

## Evidence

- `JAZZ-QUESTS-001-AC-001`: `PASS` (static), `BLOCKED` (runtime) — delivery
gate, one-shot state и удаление 4+4 предметов из player squad реализованы.
- `JAZZ-QUESTS-001-AC-002`: `PASS` (static/editor export), `BLOCKED` (runtime)
— K5 marker, conversation, RU/EN copy, `UnitJoinAsMerc` и `BarryJoined` связаны.
- `JAZZ-QUESTS-001-AC-003`: `PASS` (static), `BLOCKED` (runtime) — UnitData,
портреты и VoiceResponse существуют; full-squad join требует playtest.
- `JAZZ-QUESTS-001-AC-004`: `PASS` (static), `BLOCKED` (runtime) — hand-in
повторно проверяет player inventory и использует `UnitTakeItem`.
- `JAZZ-QUESTS-001-AC-005`: `PASS` (static/editor export), `BLOCKED` (runtime)
— три I2-маркера используют раздельные healed-флаги и общий агрегатор.
- `JAZZ-QUESTS-001-AC-006`: `PASS` (static), `BLOCKED` (runtime) — пять
sector TCE переведены в one-shot state и итоговая награда защищена.
- `JAZZ-QUESTS-001-AC-007`: `PASS` (static), `BLOCKED` (runtime) — living
hostage gate и `TCE_HostageDead` разделяют success/failure.
- `JAZZ-QUESTS-001-AC-008`: `PASS` (static), `BLOCKED` (runtime) — final
branch требует `Given` и остаётся одноразовым.
- `JAZZ-QUESTS-001-AC-009`: `PASS` (static/editor export), `BLOCKED` (runtime)
— state переименован в `M4_UnderControl`, M4-маркеры больше не зависят от M3.
- `JAZZ-QUESTS-001-AC-010`: `PASS` (static/editor export), `BLOCKED` (runtime)
— аванс one-shot; четыре союзных K6-маркера имеют отдельную группу.
- `JAZZ-QUESTS-001-AC-011`: `PASS` (static), `BLOCKED` (runtime) — Alkatraz
получил title/journal/given gate и одноразовый clear transition.
- `JAZZ-QUESTS-001-AC-012`: `PASS` (static localization), `BLOCKED`
(human/runtime) — RU/EN ID sets совпадают, missing/collision = 0.
- `JAZZ-QUESTS-001-AC-013`: `PASS` (static) — Lua compile + quest audit,
localization audit и quick validators прошли; generated-sync сохранил baseline
489 core/units errors, `jazz-maps` = 0 новых errors.
- `JAZZ-QUESTS-001-AC-014`: `BLOCKED` (runtime/human) — smoke matrix и
старое сохранение ещё не проверены в JA3.
- `JAZZ-QUESTS-001-AC-015`: `PASS` (static), `BLOCKED` (runtime) — P17
unlock теперь пишет P17, не H14.
- `JAZZ-QUESTS-001-AC-016`: `PASS` (static/editor export), `BLOCKED`
(runtime) — J7 event/setpiece и Herman groups восстановлены без I3 gate.
- `JAZZ-QUESTS-001-AC-017`: `PASS` (static), `BLOCKED` (runtime) —
reward-bearing branches получили one-shot gates.
- `JAZZ-QUESTS-001-AC-018`: `PASS` (static), `BLOCKED` (runtime/human) —
Psycho outcome выдаёт один `BigDiamond` отдельно от normal reward.
- `JAZZ-QUESTS-001-AC-019`: `PASS` (static), `BLOCKED` (human) — generated и
companion Icon/SubIcon пары исправлены; финальная UI-сверка не выполнена.
- `JAZZ-QUESTS-001-AC-020`: `PASS` (static/editor export), `BLOCKED`
(runtime) — пять K4-маркеров используют K4, M4-маркеры используют M4.
- `JAZZ-QUESTS-001-AC-021`: `PASS` (static/editor export), `BLOCKED`
(runtime/human) — Кики помечена `immortal`/`ImportantNPC`.

## Documentation delta

- Обновлены `docs/technical/systems/maps-quests-dialogue.md` и
`docs/technical/systems/maps-quests-content-catalog.md`: state contracts,
P17/J7 remap repairs, секторные связи и Barry recruitment flow.
- Обновлены `docs/wiki/grand-chien-map.md` и обе витрины
`docs/showcase/ru/ernie-campaign.md`,
`docs/showcase/en/ernie-campaign.md`,
`docs/showcase/ru/grand-chien-map.md`,
`docs/showcase/en/grand-chien-map.md`: исправленные цели, The Outlook,
подкрепление Балумбы, P17/J7 progression fixes и бесплатный квестовый рекрут
Barry Seal.
- `docs/tools/README.md` описывает apply/audit-скрипты.

