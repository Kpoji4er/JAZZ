# Чек-лист изменений

## Любое изменение

- Прочитать все применимые `AGENTS.md`.
- Запросить официальные ветку CommonLib `main` и metadata, записать текущие commit/version и не использовать устаревшую локальную копию как базу совместимости.
- Найти затронутые публичные символы в четырёх репозиториях, установленном vanilla source и последней CommonLib.
- Зафиксировать владельца и runtime-слой поведения.
- Сохранить посторонние незакоммиченные изменения.
- Если commit отдельно разрешён, написать его заголовок и пояснение на русском языке.
- Обновить профильную системную страницу и file coverage в той же задаче.
- Сопоставить diff кода/generated data с diff technical/wiki: изменение и его описание должны попасть в один согласованный change set, без отложенного документирования и описания ещё не реализованного поведения.
- Если change set разделён между репозиториями, перечислить связанные коммиты в итоговом отчёте и убедиться, что ни один пакет не оставляет документацию или реализацию заведомо позади.

## Dependencies, metadata и релиз

- Сверить `version_major`/`version_minor` каждого объявленного `JA3_CommonLib` с текущим upstream `metadata.lua`.
- Учитывать, что dependency ограничивает минимальную пару major/minor, а автоматически увеличиваемый revision/build не входит в проверку; после выбора dependency в Mod Editor повторно просмотреть version fields.
- Обновить объявленную версию до последней перед релизом или изменением dependency metadata; старую CommonLib не сохранять как поддерживаемую цель.
- Запустить `scripts/audit-project.ps1 -RequireCurrentCommonLibDependency` и устранить все несовпадения.
- Проверить, какие пакеты должны объявлять CommonLib напрямую, а какие получают её транзитивно; решение отразить в `docs/technical/compatibility.md`.
- Не менять dependency values, если upstream не удалось подтвердить.

## Runtime-логика Lua

- Проверить коллизии глобальных функций, методов классов, `OnMsg`, reactions, `NetSyncEvents`, `GameVar`, `MapVar` и `GlobalVar`.
- Зафиксировать lifecycle-stage; не читать ModItem на file scope, если данные не гарантированно готовы.
- Проверить clean start и hot reload: `ReloadLua` сохраняет Lua-state.
- Проверить registration order handlers по `metadata.code`; `OnMsg` не должен спать, `MsgClear` не должен удалять чужие handlers.
- Зафиксировать game-time/real-time clock, точки sleep/wait/wakeup и отсутствие busy loop.
- Проверить existing save со спящим game-time thread: он может продолжить старый bytecode.
- Для periodic map work оценить `MapGameTimeRepeat`/`MapRealTimeRepeat` как update-safe вариант.
- Проверить lifecycle/defaults `GameVar`, `MapVar`, `GlobalVar`; не присваивать `nil` GameVar/MapVar.
- Не хранить persistent state только во временной Lua-таблице обычного `CObject`.
- Для map enumeration использовать узкие area/class/flags, `MapCount` и dedicated operations; отдельно проверить Z, если нужен 3D-критерий.
- Для UI mutation вызвать метод на настоящем объекте, не на `SubContext()`; проверить lifetime XWindow threads.
- При рефакторинге сохранить сигнатуры, возвращаемые значения, побочные эффекты, ordering, lifecycle, поток RNG и сетевой детерминизм.
- Подтвердить регистрацию файла для загрузки и отсутствие ошибок/asserts в панели сообщений Mod Editor.

## Presets и ModItems

- Сохранять IDs и цепочки родителей, если миграция не является целью задачи.
- До изменения properties, categories, components, recipes или localization IDs найти все ссылки.
- Для generated definitions предпочитать Mod Editor.
- Использовать `$sync-jazz-generated-data`; проверить `items.lua`, `metadata.lua` и companion одним diff и выполнить строгий аудит после editor round-trip.
- Проверить панель сообщений Mod Editor после load/save/reload; ignored mod, load/runtime error или assert блокирует round-trip.
- Проверить дубли definitions и порядок override между пакетами.

## Карты и сектора

- Проверить sector IDs, campaign links, travel routes, spawners, guardposts, quests, banters, conversations, loot, setpieces и ссылки на units.
- Протестировать новую игру, существующее сохранение, strategic/tactical entry, разрешение конфликта и возврат на satellite view.

## Юниты, отряды и AI

- Проверить UnitData, appearances, equipment, loot, archetype, role, keyword, squad, voice и progression references.
- Протестировать spawn, autoresolve, tactical AI, death/despawn, recruitment/hiring, save/load и детерминированную генерацию имён.

## Assets, audio и FX

- Проверить entity/resource IDs, регистр, зависимости materials/textures, fallback и порядок загрузки пакетов.
- После re-export/re-import учесть инкрементальный export, очистить согласованный export state и проверить Entity после перезапуска игры.
- Не переносить локальные source paths в tracked-инструкции; legacy absolute paths документировать как технический долг без личных корней.

## Изменение, чувствительное к совместимости

- Сравнить один и тот же символ в vanilla, последней CommonLib и JAZZ.
- Обновить `docs/technical/override-matrix.md` и `docs/technical/compatibility.md`.
- Протестировать без устаревших caches и, когда применимо, с сохранением до изменения.