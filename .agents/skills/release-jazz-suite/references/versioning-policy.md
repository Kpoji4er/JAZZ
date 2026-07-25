# Политика версий и metadata JAZZ

## Единственный источник версии

Каноническая версия комплекта берётся из `jazz/metadata.lua` в том exact commit, который выпускается. Не использовать отдельный `VERSION`, вручную выбранный PATCH или номер из working tree.

Официальный JA3 `ModDef:GetVersionString()` выводит:

```text
version_major.version_minor-version
```

с минимальным форматом `%d.%02d-%03d`. Поэтому metadata `0 / 11 / 5899` означает:

- player/release display: `0.11-5899`;
- нормализованный GitHub tag: `v0.11.5899`;
- release title: `JAZZ 0.11-5899`.

В tag числовые части записываются без ведущих нулей. Это SemVer-совместимая трёхчисловая форма для GitHub tooling, но третье число остаётся JA3 editor revision и не заменяется отдельным patch counter.

## Значение чисел

| Поле metadata | Правило |
|---|---|
| `version_major` | Несовместимое поколение после стабилизации публичного контракта |
| `version_minor` | Новый совместимый функционал; до `1.0` также явно объявленный breaking change |
| `version` | Read-only Revision, автоматически обновляемая Mod Editor; третье число tag |

Для совместимого исправления major/minor не менять. Выпуск получает новый tag из нового committed editor revision.

Revision не сбрасывать и не выравнивать вручную при изменении major/minor. Значения metadata имеют приоритет над чистой арифметикой SemVer.

## Публичный контракт JAZZ

При выборе major/minor учитывать:

- загрузку существующих сохранений и сетевую совместимость;
- IDs четырёх пакетов, зависимости и порядок загрузки;
- публичные Lua globals/classes, presets, localization IDs и `Mod/<id>/...` paths;
- формат generated data, карт, юнитов и межпакетных ссылок;
- структуру установки и состав обязательных пакетов;
- заявленные правила игрового поведения.

До `1.0` breaking changes поднимают minor и явно описываются в release notes. `1.0` означает явную фиксацию стабильного публичного контракта.

## Правило изменения metadata

`metadata.lua` является generated data:

1. Менять ModDef и сохранять metadata через Mod Editor.
2. Не редактировать `version`, `saved`, `code_hash` и generated arrays вручную ради версии.
3. Изменение `version_major` или `version_minor` должно быть обосновано совместимостью и отражено в release notes.
4. Изменение `code`, dependencies, loctables, resources или registrations должно сопровождаться изменением соответствующих файлов-владельцев и технической документации.
5. После editor save сравнить `metadata.lua`, `items.lua` и отдельные generated definitions; отделить ожидаемую регенерацию от шума.
6. Не коммитить необъяснённое metadata-only изменение.
7. Единственное штатное metadata-only исключение — сохранение core ModDef через Mod Editor как release marker, когда выпуск содержит только изменения assets/maps/units.
8. Не синхронизировать revisions пакетов и не трогать metadata неизменившегося sibling-пакета.
9. Не включать номер версии в `title` или `description`: Mod UI и release tooling должны отображать поля metadata.

Каждый релиз обязан иметь новый committed core revision. Если core metadata совпадает с предыдущим release manifest, новый tag не создавать.

## Версии четырёх пакетов

Центральный release version определяется только committed core metadata. Metadata каждого sibling-пакета остаётся собственной историей Mod Editor.

Manifest фиксирует для каждого пакета:

- `version_major`, `version_minor`, `version`;
- engine display;
- exact commit;
- mod ID;
- artifact и SHA-256.

Так release остаётся единым, но не приписывает assets/maps/units искусственно синхронизированные версии.

## Первый GitHub-релиз

Первый tag не выбирается отдельно. Он автоматически выводится из committed core metadata выбранного SHA. Перед публикацией:

1. Убедиться, что core metadata сохранена Mod Editor намеренно.
2. Удалить устаревший hard-coded номер из title/description.
3. Проверить уникальность полученного tag.
4. Зафиксировать четыре package metadata versions в manifest.

## Коммиты и changelog

Для новых коммитов рекомендуется [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

- `feat(scope): ...`;
- `fix(scope): ...`;
- `docs:`, `build:`, `ci:`, `refactor:`, `test:`;
- `type(scope)!:` или footer `BREAKING CHANGE:` для несовместимости.

Commit type помогает классифицировать major/minor и release notes, но не является источником номера. Номер всегда читается из committed metadata.

## Неизменяемость

После публикации:

- не двигать и не форсировать tag;
- не заменять архивы под тем же номером;
- не редактировать manifest задним числом;
- исправлять ошибку новым editor revision и новым tag.
