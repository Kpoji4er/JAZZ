---
id: JAZZ-PROGRESSION-001
status: approved
owner: project-owner
systems:
  - units-progression
  - new-game-ui
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/LegionTierProgression.lua
  - jazz/Code/GameRules_HideAdvanced.lua
  - jazz/metadata.lua
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/specs/active/JAZZ-PROGRESSION-001.md
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/technical/compatibility.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-units.md
  - jazz/docs/showcase/en/legion-units.md
  - jazz/docs/tools/test_legion_newgame.py
  - jazz/docs/tools/export_legion_newgame_localization.ps1
  - jazz/docs/tools/README.md
  - jazz/release/manifests/*
  - jazz/release/notes/*
exclusive_resources:
  - Code:LegionTierProgression.lua
  - Code:GameRules_HideAdvanced.lua
  - Localization:718927001001-718927001010
  - metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-PROGRESSION-001: стартовый тир мира и скорость прогрессии

## Проблема

Новая игра всегда начинает с T1-1. Простая замена quest var не сдвигает таймер и major-state, но меняет потребителей стратегии. Нужны явные настройки начала и времени роста.

## Цели

- Выбирать стартовый тир всего мира и прохождение всей лестницы по времени.
- Сохранить исходный режим кампании по умолчанию и старые сохранения.

## Non-goals

- Не завершать сюжетные квесты, не выдавать шахты, деньги или стартовое снаряжение наёмникам.
- Не менять независимые шкалы магазина и difficulty, loot bands, состав авторских гарнизонов.
- Не публиковать посторонние dirty changes и не загружать Steam Workshop без отдельного запроса.

## Требования

- `JAZZ-PROGRESSION-001-REQ-001` — два циклических селектора в правилах новой игры: старт 11,12,13,21,22,23,24,25,31,32,33; рост Campaign / Time ×1 / ×2 / ×4. Defaults 11/Campaign.
- `JAZZ-PROGRESSION-001-REQ-002` — выбранный старт применяется к общей quest var и обоим профильным состояниям до последующих NewGame-потребителей. Начальная установка не выдаёт события роста за пропущенные тиры. При отложенном появлении квеста установка повторяется до успешной инициализации.
- `JAZZ-PROGRESSION-001-REQ-003` — временная лестница 11→12→13→21→22→23→24→25→31→32→33. Интервал исходящего шага: Maps 7 дней из T1, 30 из T2/T3; NoMaps 3 и 14. Время делится на множитель. CampaignTimeStart/сохранённый старт таймера, без wall clock и RNG. События кампании не ускоряют временную лестницу. Потолок 33.
- `JAZZ-PROGRESSION-001-REQ-004` — Campaign сохраняет gates/интервалы COMPAT-003/008; повышенный старт задаёт major/sub baseline, не откатывается, следующий подшаг через полный интервал. При естественном переходе в следующий major таймер начинается с первого sub.
- `JAZZ-PROGRESSION-001-REQ-005` — выбор хранится штатными скрытыми GameRuleDef JAZZ_LegionStart<value>/JAZZ_LegionClock<multiplier>. UI очищает соседние значения группы, guest не редактирует; lobby-info передаёт те же game_rules. Старые сейвы без правил используют прежнее поведение.
- `JAZZ-PROGRESSION-001-REQ-006` — RU/EN локализация, technical/wiki/showcase, commit/push/центральный release. Runtime без подтверждения допускает только явно помеченный prerelease.

## Инварианты и ограничения

- Общая quest var и существующие strategic consumers сохраняются; «весь мир» означает все существующие зависимости от Legion tier, не принудительное завершение сюжета.
- NoMaps bootstrap не сбрасывает старт; исходные saves не получают новый старт задним числом.
- Единственный реальный raise вызывает прежние loot/RIS/AI механизмы; повторный tick не повторяет событие.
- Чужие изменения сохраняются; коммит содержит только diff этой задачи.

## Acceptance criteria

- `JAZZ-PROGRESSION-001-AC-001` — executable: все 11 стартов × 3 скорости × 2 профиля, граничные моменты, большой time jump, потолок.
- `JAZZ-PROGRESSION-001-AC-002` — executable: Campaign defaults, повышенный старт, переход major, старое сохранение, отложенный quest, старт без raise, raise без повторов.
- `JAZZ-PROGRESSION-001-AC-003` — runtime: видимость двух селекторов, настройки NewGame, сохранение/загрузка; кооператив host/guest требует отдельной проверки при наличии двух клиентов.
- `JAZZ-PROGRESSION-001-AC-004` — static: RU/EN parity, docs, generated consistency, только task diff в commit.

## Impact и совместимость

- Vanilla: расширение NewGameMenuGameRules; hidden GameRuleDef используют штатный ApplyNewGameOptions, Game.game_rules и lobby-info.
- Saves: дополнительные поля в существующих gv_JAZZ_LegionTierMaps/NoMaps; absent fields сохраняют старую формулу.
- Network/determinism: стандартный host-owned game_rules, только CampaignTime.
- Generated data: metadata Revision/changelog и RU/EN; items.lua и companion не меняются.
- Cross-package: consumers units/maps/nomaps читают прежний ID; изменения только в jazz.
- Rollback: выключение фичи требует версии, знающей сохранённые GameRule IDs; удаление правил из активного сейва не является поддерживаемой миграцией.

## План и ownership

- Пакет-владелец: jazz. Исполнитель: Codex. Reviewer: project-owner.
- Declared write set и exclusive resources — frontmatter; baseline сохранён отдельно до правок.

## Решение владельца

- Статус: approved. project-owner, 2026-09-27.
- Chat: добавить стартовый тир; «Весь мир стартует с выбранного тира»; «Вся лестница по времени; скорость ×1, ×2, ×4»; «как доделаешь сразу коммит + пуш + релиз».
- Сохранение Campaign по умолчанию и интервалы профилей — решение реализации, сообщённое в чате.

## Evidence

- `JAZZ-PROGRESSION-001-AC-001`: PASS (executable Lua via lupa) — 352 boundary/campaign checks, все старты/скорости/профили, clamp и time jumps; `python docs/tools/test_legion_newgame.py`.
- `JAZZ-PROGRESSION-001-AC-002`: PASS (executable Lua via lupa) — lazy quest before initial squads, delayed quest/bootstrap, старое состояние без опций, raised Campaign baseline, major reset, no retroactive/double events; тот же тест.
- `JAZZ-PROGRESSION-001-AC-003`: BLOCKED (runtime/human) — DAP 127.0.0.1:8165 refused connection. Живой UI, save/load и двухклиентный co-op не проверены; выпуск только prerelease. Static vanilla NewGameSession ordering и Lua UI callbacks подтверждены, не заменяют runtime.
- `JAZZ-PROGRESSION-001-AC-004`: PASS (task-scope static) — 8 canonical-export IDs, RU/EN parity, needs translation=0, collisions=0; docs local check PASS (6 Markdown), clean generated audit PASS before Revision bump. После разрешённого Revision +1 strict выдаёт только mtime warning metadata newer than items; это ожидаемая version/changelog транзакция без изменения ModItem. Рабочий каталог имеет посторонний RussianManual конфликт ID 890000000020255 и tmp-copy audit noise; release собирается отдельно от него.

## Documentation delta

- Канон: legion-units-equipment-tiers; wiki legion-global-ai; showcase legion-units RU/EN; совместимость сохранений и vanilla UI extension.

CommonLib release snapshot: upstream main `a1a5f4819d60b4d410d515f926ef45646c6989e7`, metadata 1.11-1067, проверен 2026-09-27. Пакеты/зависимости не менялись. Independent project-owner review and human acceptance pending.

Full clean localization audit is not clean: existing 11 active-ID and 606 base-ID collisions, 101 missing Russian / 522 missing English under task-only translation memory, one pre-existing wide row per runtime CSV. These unrelated records were preserved; task-scoped export has no missing translations or collisions. No claim of global localization acceptance.

DoD validator was run and correctly rejected AC-003 BLOCKED. Status remains approved until runtime/human acceptance; the code is available in a prerelease, not declared accepted.
