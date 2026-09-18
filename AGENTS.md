# Правила работы с JAZZ

Четыре канонических репозитория (+ опциональный пятый без maps):

| Репозиторий | Каталог | Что содержит |
| --- | --- | --- |
| `jazz` | `..\jazz` | Код оверхола, предметы, эффекты, UI |
| `jazz_assets` | `..\jazz_assets` | Сущности, модели, материалы, текстуры |
| `jazz-maps` | `..\jazz-maps` | Карты, квесты, диалоги, сектора, патчи |
| `jazz-units` | `..\jazz-units` | UnitData, AI-архетипы, отряды, прогрессия |
| `jazz-nomaps` | `..\jazz-nomaps` | Опционально вместо maps (display: **JAZZ Vanilla Maps**) |

Профили: **канон** = assets+units+maps+jazz; **без maps** = assets+units+nomaps+jazz. Не включать maps и nomaps как обязательную пару. Не переносить файлы между репозиториями.

## Когда что читать

Не открывать все `.cursor/rules` и skills. Только строка, которая совпала с задачей:

| Задача | Открыть |
| --- | --- |
| Новое поведение, public ID, generated data, load order, смена scope | `$specify-jazz-change` |
| Несколько пакетов, ownership, impact | `$work-on-jazz-mod` |
| `items.lua` / `metadata.lua` / ModItem / companion | `$sync-jazz-generated-data` + `.cursor/rules/jazz-items-metadata-validate.mdc` |
| Новый shoppable item, Bobby Ray, ECON-004, shop Tier/RW | `.cursor/rules/jazz-bobby-ray-new-items.mdc` |
| Коммит, Revision, `last_changes` | `.cursor/rules/jazz-commits-versioning.mdc` + `.cursor/rules/jazz-metadata-last-changes.mdc` |
| `git push`, Discord после push | `.cursor/rules/jazz-git-push-chunks.mdc` |
| Player-facing бой/CTH/wiki/showcase или drift technical | `.cursor/rules/jazz-docs-sync.mdc` + `$document-jazz-systems` |
| Runtime разошёлся со spec | `.cursor/rules/jazz-spec-sync.mdc` |
| Lua wrap / `g_JAZZ_*Base` / второй хук | `.cursor/rules/jazz-lua-wrap-no-cycle.mdc` |
| Новый Lua global / `rawset` / GameVar | `$jazz-lua-globals` |
| Скрипт в `docs/tools` или `.agents` | `.cursor/rules/jazz-agent-tooling.mdc` |
| Лёгкий / нормальный / сложный, `GameDifficulty` | `.cursor/rules/jazz-game-difficulty.mdc` |
| `Russian.csv` / `English.csv` / `T()` | `$manage-jazz-localization` |
| Релиз, теги, Steam upload | `$release-jazz-suite` |
| «Проверь в игре», DAP, live Lua | `.cursor/rules/jazz-dap-runtime-debug.mdc` |
| Красные/жёлтые пометки Mod Editor / Ged | `$diagnose-jazz-mod-editor` |
| Броня/одежда Легиона, equipped appearance, `ArmorTest` | `.agents/docs/playbooks/legion-armor-modeling.md` |
| Portrait мерка/NPC | `.cursor/rules/jazz-merc-portraits.mdc` + `$create-jazz-merc-portraits` |
| Полный мерк из generation-статьи | `$create-jazz-merc` |

Дальше — `.agents/docs/index.md` и **один** профильный playbook. Не грузить весь набор документов.

## Всегда (коротко)

1. Не `git push` / force-push / теги / релизы / PR без явного одобрения на **эту** публикацию. «Закоммить» push не разрешает.
2. Не обходить `jazz-maps/Maps/` целиком без запроса на конкретную карту/сектор.
3. Не смешивать логическое изменение с mass regen / formatting.
4. Один wrap на `Class:Method` / глобал; новый хук вшивать в существующий.
5. Абсолютный `<JA3_ROOT>` не коммитить.
6. Речь про сложность игры: **лёгкий** = `Normal`, **нормальный** = `Hard`, **сложный** = `VeryHard`. Игрового Easy нет.
7. **JA3 запускать через Steam**, например `Start-Process 'steam://rungameid/1084160'`, не напрямую через `JA3.exe` / `JA3Debug.exe`. Прямой запуск здесь даёт «Unable to start the game. Please restart». Для DAP отдельно проверить debug-сборку и порт 8165; обычный запуск Steam сам по себе DAP не гарантирует.
8. Overlay `AGENTS.md` каждого sibling-пакета держать согласованным с этой таблицей: те же имена правил/skills, актуальные пути. Обязательные маршруты suite-gate: `../jazz/AGENTS.md`, `../jazz/docs/specs/active/`, `../jazz/.agents/skills/work-on-jazz-mod/SKILL.md`, `../jazz/.cursor/rules/jazz-docs-sync.mdc`. Player-facing слой ведётся из `jazz`; в overlay не писать, что wiki отключён. Проверка: `python docs/tools/_check_suite_agents_overlays.py`.

## Источники

- Runtime JA3: `<JA3_ROOT>\ModTools\Src`
- Официальная документация: `<JA3_ROOT>\ModTools\Docs`
- CommonLib: <https://gitlab.com/injto4ka/ja3_commonlib>
