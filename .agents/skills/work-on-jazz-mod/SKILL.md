---
name: work-on-jazz-mod
description: Маршрутизировать безопасную разработку, диагностику и ревью JAZZ как комплекта из четырёх репозиториев. Использовать для изменений runtime Lua, generated data, карт, юнитов, assets, dependencies, load order и межпакетных контрактов, а также для impact analysis по vanilla, CommonLib и JAZZ. Подключает только профильные references и специализированные skills.
---

# Работа с JAZZ

Рассматривать `jazz`, `jazz_assets`, `jazz-maps` и `jazz-units` как один runtime-продукт с отдельными Git-границами.

## Маршрутизация

1. Прочитать применимые `AGENTS.md` и `.agents/docs/index.md`.
2. Для изменения поведения, архитектуры, generated data, dependencies, load order, публичных ID или save/network contract сначала использовать `$specify-jazz-change` и пройти DoR.
3. Определить пакет-владелец данных, runtime-владельца и exact target ID/path. Не определять ownership только по имени файла.
4. Прочитать только профильный playbook и системную technical-страницу.
5. Подключить специализированный skill:
   - `$sync-jazz-generated-data` — ModItem, `items.lua`, `metadata.lua`, companion, Entity или editor-owned data;
   - `$document-jazz-systems` — фактическое изменение реализации, load-state или technical contract;
   - `$release-jazz-suite` — release candidate, version, manifest, tag или публикация.
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
2. Обновить technical current-state docs без требования отсутствующей wiki.
3. Записать evidence для каждого `AC-*` и выполнить DoD validator.
4. Просмотреть diff каждого затронутого репозитория и перечислить непроверенные риски.
5. Если runtime недоступен, не заменять его статическим выводом: оставить соответствующий `AC-*` незакрытым.
