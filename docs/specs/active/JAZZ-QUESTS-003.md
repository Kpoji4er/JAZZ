---
id: JAZZ-QUESTS-003
status: approved
owner: project-owner
systems:
  - maps-quests
  - strategy-squads
repositories:
  - jazz
  - jazz-maps
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - docs/specs/active/JAZZ-QUESTS-003.md
  - docs/design/ernie-garrison-baseline.md
  - docs/technical/systems/maps-quests-content-catalog.md
  - docs/tools/_purge_k4_house_ambushers.py
  - docs/tools/_add_villa_attackers_ernie.py
  - docs/tools/_tighten_villa_squads.py
  - docs/tools/_dump_villa_squads.py
  - docs/tools/README.md
  - docs/tools/_check_villa_effect_dispatch.py
  - docs/tools/_check_villa_conflict_order.py
  - docs/wiki/grand-chien-map.md
  - docs/showcase/ru/grand-chien-map.md
  - docs/showcase/en/grand-chien-map.md
  - ../jazz-units/items.lua
  - ../jazz-units/metadata.lua
  - ../jazz-maps/items.lua
  - ../jazz-maps/metadata.lua
  - ../jazz-maps/Code/System_VillaCounterAttack.lua
  - ../jazz-maps/Maps/gsSMikN/objects.lua
  - ../jazz-maps/docs/content/quests-locations-enemies.md
  - docs/tools/_fix_k4_feedback.py
  - docs/tools/_export_k4_localization.ps1
  - docs/tools/_check_villa_waiting_recovery.py
  - Localization/Strings.csv
  - Localization/EnglishManual.csv
  - Russian.csv
  - English.csv
  - docs/specs/active/JAZZ-FEEDBACK-001.md
  - Code/SatelliteSquad.lua
exclusive_resources:
  - jazz-units/items.lua
  - jazz-maps/items.lua
  - jazz-maps/Maps/gsSMikN/objects.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-QUESTS-003: Flag Hill villa counterattack (move squads)

## Проблема

На K4 (Flag Hill) старая on-map осада (`HouseAmbushers`+`Legion` AdvanceTo)
раздувает ForceConflict до диалога с Emma. Лагерные `VillaAttackers_*` сидят
как обычный Init вместе с Sentry, без квестовой контратаки. Нужна большая
контратака: после разговора Emma+Corazon двигать живые sat-волны на K4,
AdvanceTo к Emma, Wave2 по `CombatTurn`, опоздавшие колонны — на том же таймере.

## Цели

- Sentry = охрана лагеря; VillaAttackers = movable siege waves.
- После «гости» живые Attackers route → K4; Ernie pack 30 всегда.
- Старые HouseAmbushers+Legion AdvanceTo с K4 удалены.
- Атакующие на тактике сразу AdvanceTo `EmmaAndCorazon`.
- Wave2 ~25 на `CombatTurn` ≥ 3 только в бою после Emma guests.
- Опоздавшие sat-колонны материализуются на Wave2 TCE без двойного входа.

## Non-goals

- Difficulty UI ±10 (authored base + docs only).
- Прореживание Raiders/AL_Raiders.
- Ernie_CounterAttack (I7→I5).
- NoMaps villa.

## Требования

- `JAZZ-QUESTS-003-REQ-001` — Init лагерей: Sentry + VillaAttackers_*; Sentry не уходит в осаду.
- `JAZZ-QUESTS-003-REQ-002` — `Jazz_VillaCounterAttack_Start` двигает существующие sat-squads по `enemy_squad_def`, не Guardpost spawn.
- `JAZZ-QUESTS-003-REQ-003` — `JAZZ_Legion_VillaAttackers_Ernie` base 30 всегда стартует.
- `JAZZ-QUESTS-003-REQ-004` — K4 purge HouseAmbushers+Legion AdvanceTo; keep guests/WorldFlip Adonis/Rebels/Bastien/Raiders.
- `JAZZ-QUESTS-003-REQ-005` — Tactical AdvanceTo EmmaAndCorazon for attacking sat units only.
- `JAZZ-QUESTS-003-REQ-006` — Wave2 ~25 markers gated by quest; TCE CombatTurn≥3 after SiegeCombat.
- `JAZZ-QUESTS-003-REQ-007` — Late columns materialize on same TCE; cancel sat route.
- `JAZZ-QUESTS-003-REQ-008` — FlagHill_Emma_1 guests interrupt → quest + lock ~2h + Start().
- `JAZZ-QUESTS-003-REQ-009` — три ExecuteCode-вызова контратаки действительно исполняют текст (`SaveAsText=true`) и обращаются к функциям через environment пакета maps; глобальный CompileFunc не должен искать функции в чужом `_ENV`.

- `JAZZ-QUESTS-003-REQ-010` — диалог Guests не создаёт конфликт до отправки колонн: создание/блокировка конфликта остаётся в Start после route. Дублирующий ранний SectorEnterConflict удалить. Восстановление уже застрявших сейвов и завершение PrepTimer требуют отдельной проверки.

## Инварианты и ограничения

- Не ломать `02_LiberateErnie` / `03A_PresidentNotes` выдачу.
- Не трогать World Flip Adonis ambush markers.
- Cleared camp (no Attacker squad) → that wave skips.
- No `TriggerGuardPostAttack` for this siege.

## Acceptance criteria

- `JAZZ-QUESTS-003-AC-001` — До диалога Attackers на лагерях; Sentry отдельно. Static.
- `JAZZ-QUESTS-003-AC-002` — После «гости» живые Attackers route → K4. Runtime/human.
- `JAZZ-QUESTS-003-AC-003` — Зачищенный лагерь → Attacker не в осаде. Runtime/human.
- `JAZZ-QUESTS-003-AC-004` — Ernie 30 всегда стартует. Static + runtime.
- `JAZZ-QUESTS-003-AC-005` — ~2h prep lock на K4. Runtime/human.
- `JAZZ-QUESTS-003-AC-006` — Нет TGPA в этой осаде. Static.
- `JAZZ-QUESTS-003-AC-007` — HouseAmbushers+Legion AdvanceTo purged. Static map audit.
- `JAZZ-QUESTS-003-AC-008` — Attackers AdvanceTo EmmaAndCorazon. Runtime/human.
- `JAZZ-QUESTS-003-AC-009` — Wave2 на CombatTurn≥3 after Emma siege combat only. Runtime/human.
- `JAZZ-QUESTS-003-AC-010` — Late sat dump on Wave2 TCE, no double spawn. Runtime/human.
- `JAZZ-QUESTS-003-AC-011` — items validate OK. Static.
- `JAZZ-QUESTS-003-AC-012` — из глобального окружения ExecuteCode вызывает Start, OnWave2 и PushAdvanceToEmma ровно по одному разу. Lua harness с установленным vanilla ExecuteCode; отдельно game/editor round-trip.

- `JAZZ-QUESTS-003-AC-013` — harness с установленным EnterConflict и реальным порядком эффектов Guests: после route конфликт получает waiting=true и не останавливает время; воспроизведение прежнего порядка даёт waiting=false. Runtime отдельно.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: maps quest + Code; units EnemySquad; K4 objects.lua.
- Saves: mid-campaign Flag Hill may miss new quest if already past Emma — new game recommended for full siege.
- Network/determinism: NetSyncEvent for routes; CustomCode must be sync-safe.
- Generated data: items.lua / metadata.lua units+maps.
- Cross-package: jazz-units squad IDs referenced from jazz-maps Code/quest.
- Rollback: restore objects.lua HouseAmbushers; remove quest/Code.

## План и ownership

- Пакет-владелец: jazz-maps (quest/map/Code), jazz-units (Ernie squad), jazz (docs/spec/tools).
- Declared write set: see frontmatter.
- Exclusive resources: items.lua units/maps, gsSMikN/objects.lua.

## Решение владельца

- Статус: approved (plan implement request 2026-08-10).
- Кто подтвердил: project-owner.
- Дата: 2026-08-10.
- 2026-09-15: владелец поручил автономный разбор и исправление подтверждённых багов («начинай»). REQ-009 восстанавливает уже утверждённые REQ-002/005/006/008; состав волн, баланс и новые правила не меняются.

## Evidence

- `JAZZ-QUESTS-003-AC-001`: `PASS` — static: camp Init Sentry+Attackers (dump script).
- `JAZZ-QUESTS-003-AC-002`: `BLOCKED` — runtime/human route after Guests.
- `JAZZ-QUESTS-003-AC-003`: `BLOCKED` — runtime/human wipe camp.
- `JAZZ-QUESTS-003-AC-004`: `PASS` — static: Ernie squad sum=30 in items + metadata.
- `JAZZ-QUESTS-003-AC-005`: `BLOCKED` — runtime/human lock.
- `JAZZ-QUESTS-003-AC-006`: `PASS` — static: Start uses SendSatelliteSquadOnRoute / GenerateEnemySquad, no TGPA.
- `JAZZ-QUESTS-003-AC-007`: `PASS` — static: `_verify_villa_counterattack_static.py` old siege remaining=0; Wave2=25.
- `JAZZ-QUESTS-003-AC-008`: `BLOCKED` — runtime AdvanceTo.
- `JAZZ-QUESTS-003-AC-009`: `BLOCKED` — runtime Wave2 CombatTurn.
- `JAZZ-QUESTS-003-AC-010`: `BLOCKED` — runtime late dump.
- `JAZZ-QUESTS-003-AC-011`: `PASS` — `_validate_items_quick.py` OK jazz-units + jazz-maps.

## Documentation delta

- `JAZZ-QUESTS-003-AC-012`: `PASS` (Lua-harness) — `_check_villa_effect_dispatch.py`: три FAIL до исправления, три PASS после. `_validate_items_quick.py ../jazz-maps` и strict generated-sync PASS. `BLOCKED` (game/editor): JA3Debug останавливается при запуске с «Unable to start the game. Please restart». Полный сценарий и обработка PrepTimer остаются незакрытыми.

- `docs/design/ernie-garrison-baseline.md`
- `docs/technical/systems/maps-quests-content-catalog.md`
- `jazz-maps/docs/content/quests-locations-enemies.md`
- `docs/tools/README.md`

- 2026-09-15: пользователь возобновил автономную обработку игрового фидбека; REQ-010 восстанавливает уже утверждённый маршрут подкреплений, без изменения баланса.

- `JAZZ-QUESTS-003-AC-013`: `PASS` (Lua-harness) — прежний порядок воспроизведён как waiting=false/paused=true, после удаления раннего SectorEnterConflict новый порядок waiting=true/paused=false. `_check_villa_effect_dispatch.py` 3 PASS; `_validate_items_quick.py ../jazz-maps` PASS; strict generated-sync errors=0/warnings=0. Runtime и старые сейвы не проверены.


## Дополнение по живому фидбеку K4, 2026-09-15

Владелец подтвердил: коллизия реплик Emma/Corazon со статусами энергии, награда 2000 вместо желаемых 40000, конфликт без противника блокирует время. Автономное исправление разрешено; игру и редактор владелец закрыл перед ручной транзакцией.

- `JAZZ-QUESTS-003-REQ-011` — развести шесть ID контратаки с COMBAT-007, новые ID 761915400101–761915400106. Старые ID статусов энергии сохраняются. Русский и английский экспортируются из одного снимка каталога.
- `JAZZ-QUESTS-003-REQ-012` — Reward_Money и три выдачи Emma составляют 40000; пять rollover показывают актуальную сумму через три новых ID 761915400107–761915400109. Уже полученные деньги не выдавать повторно.
- `JAZZ-QUESTS-003-REQ-013` — пустой оборонительный конфликт K4 до SiegeCombat явно waiting независимо от ванильного порога ожидания подкреплений; время доступно, выход из сектора остаётся запрещён. Другие активные конфликты и реальный бой не разблокировать.
- `JAZZ-QUESTS-003-REQ-014` — LoadGame восстанавливает теги атакующих из сохранённых squads/custom IDs и запускает незапущенные маршруты. Start повторяем без дублирования Ernie. После начала SiegeCombat новые отряды не создавать.
- `JAZZ-QUESTS-003-REQ-015` — подготовка длится до прихода реальной колонны. Это уточняет REQ-008 / AC-005: фиксированные 2h ранее не реализованы. Удалить неиспользуемую установку PrepTimer и обещание пары часов из реплики; скорость маршрутов не менять.

- `JAZZ-QUESTS-003-AC-014` — isolated Lua: далеко идущие подкрепления, старый waiting=false, повторный Start, восстановление тегов после загрузки, реальные враги/другой конфликт/завершённый квест.
- `JAZZ-QUESTS-003-AC-015` — static/generated: значения награды и строки RU/EN, отсутствие ID-коллизии квеста со статусами, valid items и generated sync.
- `JAZZ-QUESTS-003-AC-016` — live/human: старое сохранение K4, корректные реплики, время идёт до прихода врага, контратака начинается.

Evidence: AC-014/015/016 `BLOCKED` до проверок. Editor round-trip отдельно не выполнен. Ручная транзакция затрагивает ModItemConversation/ModItemQuestsDef в items.lua; отдельных companions этих классов нет, состав metadata неизменен. Exclusive resources дополнены диапазоном 761915400101–761915400109 и runtime CSV; один исполнитель.


- `JAZZ-QUESTS-003-AC-014`: `PASS` — isolated Lua harness `_check_villa_waiting_recovery.py` using installed EnterConflict and actual module; not live evidence.
- `JAZZ-QUESTS-003-AC-015`: `PASS` — canonical nine-row RU/EN export, `_validate_items_quick.py`, strict maps generated sync (0 errors/0 warnings), three dispatch cases. Full localization audit separately reports existing unrelated collisions/missing translations; no global clean bill.
- `JAZZ-QUESTS-003-AC-016`: `BLOCKED` — live verification pending. Editor round-trip pending.


## Уточнение владельца: без конфликта до прибытия

2026-09-15: владелец требует убрать подготовительный конфликт, использовать штатный запрет движения до прибытия атаки и скриптово ускорить только колонну Эрни. Live-тест выполняет владелец; агент игру не запускает.

- `JAZZ-QUESTS-003-REQ-016` — заменяет REQ-013 и прежний prep conflict: до врагов K4 не находится в конфликте. Только пустой старый искусственный конфликт InitialConflict/defend снимается без ResolveConflict (без наград/победы/побочных квестов). Реальный бой и чужие причины паузы сохраняются.
- `JAZZ-QUESTS-003-REQ-017` — пока живые атакующие идут в K4, player squads в K4 удерживаются штатным SatelliteSquadWaitInSector. Ожидание обновляется по SatelliteTick до прибытия первой колонны; снимается при прибытии, отмене/завершении квеста или исчезновении всех маршрутов. Собственные ожидания и прежние значения сохраняются в GameVar gv_JAZZ_VillaDepartureWaits, чужие изменения ожидания не затираются.
- `JAZZ-QUESTS-003-REQ-018` — время пути только JAZZ_Legion_VillaAttackers_Ernie к K4 при активной осаде делится на 5 перед округлением до минуты в существующем GetSectorTravelTime. Лидерство, прочие отряды, транспорт и общие константы не меняются; новых wraps нет.
- `JAZZ-QUESTS-003-AC-017` — isolated Lua: нет prep conflict; старый пустой конфликт снимается без победы; ожидание дольше двух часов и release по прибытии/отмене; иные ожидания и конфликты сохраняются; путь Эрни ускорен x5, прочие пути неизменны.
- `JAZZ-QUESTS-003-AC-018` — human: старое сохранение K4, время идёт без конфликта, выйти нельзя до прибытия врага; колонна Эрни подходит быстрее. Проверяет пользователь.

AC-014/013 относятся к предыдущему варианту и не доказывают новую механику. AC-017 `BLOCKED` до harness, AC-018 `BLOCKED` до проверки владельцем. Write set дополнен Code/SatelliteSquad.lua; scope одобрен прямым запросом владельца.


- `JAZZ-QUESTS-003-AC-017`: `PASS` — isolated Lua `_check_villa_waiting_recovery.py`: actual module + vanilla EnterConflict + core GetSectorTravelTime, отсутствие prep conflict, old-save cleanup, ожидание более 2h/отмена/чужое ожидание/реальные враги, x5 только Эрни.
- `JAZZ-QUESTS-003-AC-018`: `BLOCKED` — ожидает human проверки владельцем; запуск игры агентом запрещён владельцем.


## Уточнение блокировки прибытия, 2026-09-16

Владелец подтвердил выход ровно в момент прибытия врага и разрешил исправление («поправь все»).
- `JAZZ-QUESTS-003-REQ-019` — ожидание не снимается при появлении противника: пока квест активен, держать его при колоннах в пути, живых врагах в K4, конфликте K4 или бою K4. По окончании/отмене квеста либо исчезновении всех этих причин вернуть предыдущее ожидание. Явный Retreat сохраняет штатное поведение.
- `JAZZ-QUESTS-003-AC-019` — offline: arrival до EnterConflict, после EnterConflict и CombatStart не создаёт окна выхода; завершение квеста и исчезновение угрозы освобождает ожидание. Ручная проверка владельца остаётся необходимой.

2026-09-16: AC-019 PASS offline — hold до регистрации конфликта, после регистрации и при SiegeCombat; release по Completed и отмене угрозы. Ручная проверка перехода в боевой UI остаётся за владельцем.
