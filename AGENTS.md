# Правила работы с JAZZ

JAZZ состоит из четырёх канонических репозиториев (+ опциональный пятый профиль без maps):

| Репозиторий | Локальный каталог | Что он содержит |
| --- | --- | --- |
| `jazz` | `..\jazz` | Код оверхола, предметы, эффекты, UI |
| `jazz_assets` | `..\jazz_assets` | Сущности, модели, материалы, текстуры |
| `jazz-maps` | `..\jazz-maps` | Карты, квесты, диалоги, сектора, патчи |
| `jazz-units` | `..\jazz-units` | UnitData, AI-архетипы, отряды, прогрессия |
| `jazz-nomaps` | `..\jazz-nomaps` | **Опционально вместо maps** (display: **JAZZ Vanilla Maps**): vanilla HotDiamonds + Legion AI (`7MsJ2Eq`) |

Профили: **канон** = assets+units+maps+jazz; **без maps** = assets+units+nomaps+jazz. Не включать maps и nomaps как обязательную пару.

Перед любым изменением определяй пакет-владельца данных и не переноси файлы между репозиториями ради удобства.

## Быстрый путь чтения

Сначала открыть `.agents/docs/index.md`, затем только релевантный reference/playbook:

- Spec/DoR/DoD: `.agents/skills/specify-jazz-change/SKILL.md`, `docs/specs/README.md`
- Общий контур: `.agents/docs/reference/project-scope.md`
- Runtime/потоки/сообщения: `.agents/docs/reference/runtime-model.md`
- Generated data: `.agents/docs/reference/generated-data-sync.md`
- Проверки и release: `.agents/docs/reference/checklists-and-release.md`
- Current-state документация: `.agents/docs/reference/documentation-contract.md`
- Agent tooling (скрипты не выкидывать): `.agents/docs/reference/agent-tooling.md`, `docs/tools/README.md`

## Ролевые playbookы

- AI / CTH / боеприпасы: `.agents/docs/playbooks/ai-system.md`
- Оружие и баланс: `.agents/docs/playbooks/weapons-balance.md`
- Карты, квесты, диалоги: `.agents/docs/playbooks/maps-content.md`
- Юниты и прогрессия: `.agents/docs/playbooks/units-squads.md`
- Assets, UI, звук, FX: `.agents/docs/playbooks/assets-and-ui.md`

## Минимальные обязательства

1. Изменение поведения, архитектуры, generated data, dependencies, load order, публичных ID или save/network contract начинается с approved spec и прошедшего DoR.
2. Перед compatibility-sensitive изменением использовать свежий CommonLib snapshot аудитора; обновлять upstream при истёкшем snapshot или dependency/release scope.
3. Generated data изменять транзакцией `items.lua` + `metadata.lua` + companion и проверять профильным sync-аудитом.
4. Не смешивать логическое изменение с перепаковкой, массовой регенерацией или форматированием.
5. Не запускать общий обход `jazz-maps/Maps/` без прямого запроса на конкретную карту/сектор/patch.
6. Полная замена vanilla-класса сохраняет исходные class name/ID и пару `UndefineClass('<Id>')` → `DefineClass.<Id> = { ... }`; подробности живут в generated-data contract.
7. `docs/technical/` описывает текущее состояние для разработчика, `docs/wiki/` — текущее состояние для игрока, `docs/showcase/` — двуязычная публичная витрина (GitHub Wiki), а `docs/specs/` — утверждённое намерение; затронутые уровни документации входят в DoD. Для player-facing боя/CTH/grazing/укрытия/дыма обновлять technical + wiki + showcase RU/EN **в том же change set** (`.cursor/rules/jazz-docs-wiki-sync.mdc`).
8. Не выполнять `git push`, force-push, публикацию тегов, релизов или PR без отдельного явного одобрения пользователя на конкретную публикацию. Запрос на commit, merge или перенос в ветку не разрешает push. При **одобренном** push разбивать ahead-коммиты на чанки **≤8** и после push в `main` обеспечивать Discord через `docs/tools/_dispatch_discord_player_update.ps1` (agent push часто не триггерит Actions; см. `.cursor/rules/jazz-git-push-chunks.mdc`).
9. При добавлении или изменении mod-only строки локализации в том же change set обновлять обе runtime-таблицы — `Russian.csv` и `English.csv`. Изменение не завершено, пока для активной строки не заполнены оба языка, множества mod-only ID таблиц не совпадают и аудитор сообщает `needs Russian=0` и `needs English=0`.
10. При коммите изменений пакета в том же change set обновлять его `metadata.lua`: обычный коммит поднимает `version` (Revision) на `+1`; `version_minor` — только на большой мульти-spec фиче/волне. Не править вручную `saved`, `code_hash`. Sibling-пакеты без изменений не трогать. `last_changes` при коммите **дописывать**, полностью перезатирать только при Steam upload. Подробности: `.cursor/rules/jazz-commits-versioning.mdc`, `docs/technical/systems/release-versioning.md`, `$release-jazz-suite`.
11. Новый shoppable `InventoryItem` (оружие/броня/ammo/медицина/тулзы/аттач…): в том же change set решить **Bobby Ray in|out** и выставить shop-поля (или явный out + причина). Не откладывать «потом в каталог». См. `.cursor/rules/jazz-bobby-ray-new-items.mdc`, ECON-004.

## Источники

- Runtime JA3: `<JA3_ROOT>\ModTools\Src`
- Официальная документация: `<JA3_ROOT>\ModTools\Docs`
- CommonLib: <https://gitlab.com/injto4ka/ja3_commonlib>

Абсолютное значение `<JA3_ROOT>` не коммитить.
