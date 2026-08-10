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
  - `$create-jazz-squad-icons` — сателлитные PNG ролей отрядов в `SquadsIcons/Enemy`;
  - `$create-jazz-component-icons` — полная `WeaponComponent.Icon` (`Icons/Upgrades/Full/`);
  - `$create-jazz-chip-icons` — `ChipIcon` миниатюры чипов (`Icons/Upgrades/Chips/`);
  - `$create-jazz-merc-portraits` — PNG Portrait/BigPortrait мерков и NPC в `jazz-units/MercPortraits` и `NPCPortraits`;
  - `$create-jazz-merc` — полный наёмник из `docs/design/mercs-ja12/<slug>.md` (UnitData, perk, loot, portraits, loc, VR);
  - `$rename-jazz-weapon-textures` — numeric DDS → `Entity_MapType`, unused purge/dedupe в `jazz_assets` (после editor import ствола);
  - `$jazz-penetration-scales` — дробное пробитие (класс + десятые), ammo UI / `GetAttackPenetrationClass`;
  - `$jazz-lua-globals` — объявление/`rawset` глобалов, wrap flags, early `SetQuestVar` vs `Groups`;
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
6. Полезные миграционные/audit-скрипты из сессии **сохранить** в `docs/tools/` и описать в `docs/tools/README.md` (`.agents/docs/reference/agent-tooling.md`). Не чистить их «для порядка».

## Discord-новости по пакетам

Push в `main` **может** дать player-сводку на пакет. Не склеивать разные **независимые** фичи разных реп в одно сообщение.

При **одном** логическом change set на несколько пакетов (пример: NoMaps remap + `jazz-units` pack + docs в `jazz`):

1. **Один** Discord-пост с **primary** пакета (player-facing runtime/items).
2. Sibling (docs, remap-only, tools, metadata): commit с **`[skip discord]`**.
3. После одобренного push диспатчить `_dispatch_discord_player_update.ps1` **только** для primary — не `-Force -AlwaysDispatch` на каждый репозиторий.
4. Если правка ломает текущий сейв или требует новой кампании — ставить в commit message `[new game]` (или `[new game recommended]` / `[no new game]`). Discord-сводка всегда показывает поле «Новая игра»; маркер владельца важнее AI-оценки.

Независимые фичи в разных пакетах в разных push — отдельные новости ок.
