---
name: work-on-jazz-mod
description: >-
  Использовать при смене пакета-владельца, load order или правке сразу
  нескольких репозиториев JAZZ. Не для однофайлового фикса в одном пакете.
---

# Работа с JAZZ

Рассматривать `jazz`, `jazz_assets`, `jazz-maps` и `jazz-units` как один runtime-продукт с отдельными Git-границами.

## Маршрутизация

1. Следовать таблице «Когда что читать» в `AGENTS.md`. Index — только нужный playbook.
2. Для изменения поведения, архитектуры, generated data, dependencies, load order, публичных ID или save/network contract сначала `$specify-jazz-change` и DoR.
3. Определить пакет-владелец данных, runtime-владельца и exact target ID/path. Не определять ownership только по имени файла.
4. Прочитать только профильный playbook и системную technical-страницу.
5. Подключить **только совпавший** skill (иконки/портреты — `.agents/docs/index.md`):
   - `$sync-jazz-generated-data` — ModItem, `items.lua`, `metadata.lua`, companion;
   - `$document-jazz-systems` — documentation delta под loaded runtime;
   - `$jazz-lua-globals` — новый global / `rawset` / GameVar;
   - `$diagnose-jazz-mod-editor` — красные/жёлтые пометки Ged и вложенные GetError/GetWarning;
   - `$release-jazz-suite` — релиз, теги, Steam.
6. Не выполнять recursive scan `jazz-maps/Maps/` без прямого картографического scope.

## Исследование

- Начинать с narrow `rg`, exact ID и диапазонов строк; не загружать целиком `items.lua` или большие metadata/data-каталоги.
- Проверять `git status --short` только в затронутых репозиториях и сохранять посторонний dirty state.
- Сравнивать один и тот же символ в установленной vanilla, подтверждённой CommonLib и JAZZ только для compatibility-sensitive изменения. Повторно использовать свежий CommonLib snapshot аудитора.
- Проверять фактическую регистрацию в `metadata.lua.code`; наличие файла на диске не доказывает загрузку.
- Для изменённого визуального или звукового представления синхронизировать repository-relative media path в technical docs либо явно зафиксировать отсутствие изменения asset contract.

## Реализация

- Работать в пакете-владельце и в declared write set утверждённой spec.
- Не смешивать логическое изменение, mass regeneration, formatting и migration.
- Сохранять публичные IDs, signatures, load order, save/network state и deterministic RNG, если spec явно не меняет контракт.
- Generated data менять одной транзакцией и проверять editor round-trip.
- Не активировать dormant/unlisted код неявно.

Runtime guardrails читать в `.agents/docs/reference/runtime-model.md`; полный change checklist — в [change-checklist.md](references/change-checklist.md).

## Завершение

1. Выполнить профильные static/generated/editor/runtime проверки.
2. Обновить current-state docs по `.cursor/rules/jazz-docs-sync.mdc` (player-facing → technical + wiki + showcase RU/EN).
3. Записать evidence для каждого `AC-*` и выполнить DoD validator.
4. Просмотреть diff каждого затронутого репозитория и перечислить непроверенные риски.
5. Если runtime недоступен, не заменять его статическим выводом: оставить соответствующий `AC-*` незакрытым.
6. Полезные миграционные/audit-скрипты из сессии **сохранить** в `docs/tools/` и описать в `docs/tools/README.md` (`.agents/docs/reference/agent-tooling.md`). Не чистить их «для порядка».

## Discord / push

Процедура push и Discord — только `.cursor/rules/jazz-git-push-chunks.mdc` (один primary на логическую фичу; sibling с `[skip discord]`). Ломает сейв → `[new game]` / `[new game recommended]` / `[no new game]` в commit message.
