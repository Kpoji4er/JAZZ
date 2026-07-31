---
name: release-jazz-suite
description: Планировать, проверять и публиковать релизы JAZZ из четырёх GitHub-репозиториев с версией, полученной из committed jazz/metadata.lua. Использовать при изменении metadata, выборе major/minor, подготовке release manifest и changelog, создании тегов и GitHub Releases, упаковке четырёх мод-пакетов, настройке release workflow и проверке release-кандидата.
---

# Релизы комплекта JAZZ

Вести JAZZ как один продукт с четырьмя независимыми Git-источниками. Публиковать один центральный GitHub Release в `Kpoji4er/JAZZ` и прикладывать четыре пакета, собранные только из зафиксированных коммитов.

Версию релиза всегда получать из committed `jazz/metadata.lua`:

- отображение JA3 и release title: `version_major.version_minor-version`;
- GitHub tag и имена assets: нормализованное `vMAJOR.MINOR.REVISION`;
- отдельный version-файл или независимо выбранный PATCH не создавать.

## Обязательный контекст

Перед любой релизной задачей:

1. Прочитать все применимые `AGENTS.md`.
2. Использовать `$work-on-jazz-mod` для аудита четырёх пакетов и актуального CommonLib.
3. Прочитать [политику версий и metadata](references/versioning-policy.md).
4. Для упаковки, тегов, GitHub Actions или публикации дополнительно прочитать [релизный контракт](references/release-contract.md).
5. Если меняются tooling, metadata, зависимости или документация, использовать `$document-jazz-systems` и обновить technical-источник истины в той же задаче.

Не считать локальный каталог `jazz` единственным репозиторием. Проверять `jazz`, `jazz_assets`, `jazz-maps` и `jazz-units` как единый комплект.

## Выбрать режим работы

- **Аудит:** выполнять read-only проверки и показывать версию из metadata выбранного commit.
- **Подготовка release-кандидата:** обновлять metadata через Mod Editor, manifest, release notes и workflow, но не публиковать без запроса пользователя.
- **Публикация:** создавать тег и GitHub Release только когда пользователь явно попросил выпустить релиз и все блокирующие проверки пройдены.

Не расширять разрешение на релиз до commit, stash, clean или публикации чужих незакоммиченных изменений.

## Получить версию

1. Выбрать точный core SHA из `origin/main`.
2. Прочитать `metadata.lua` командой `git show <sha>:metadata.lua`, а не из активного working tree.
3. Получить `version_major`, `version_minor` и read-only `version`.
4. Сформировать engine display по контракту JA3 `%d.%02d-%03d`.
5. Сформировать tag без ведущих нулей: `vMAJOR.MINOR.REVISION`.
6. Проверить, что title/description не содержат отдельный захардкоженный номер версии.

Например, metadata `0 / 11 / 5899` даёт display `0.11-5899` и tag `v0.11.5899`. Оба значения происходят из одного источника.

Версии metadata трёх соседних пакетов не выравнивать с core. Записывать их собственные engine versions и exact SHA в центральный manifest.

## Применить правило изменения metadata

- Считать `metadata.lua` generated data и менять его через Mod Editor.
- `version_major` менять только для несовместимого поколения после стабилизации публичного контракта.
- `version_minor` менять для нового совместимого функционала; до `1.0` также для breaking changes.
- Read-only `version` не редактировать вручную: Mod Editor увеличивает revision при сохранении.
- Для исправления оставить major/minor прежними; новый editor revision становится третьим числом release tag.
- Если релиз меняет только assets/maps/units, сохранить core ModDef через Mod Editor как явный release marker, чтобы committed core metadata дала новый уникальный номер.
- Не создавать metadata-only commit ради произвольного числа. Допустим только объяснённый release marker или намеренное изменение ModDef.
- Изменения `code`, dependencies, localization, resources и generated registries в metadata коммитить вместе с соответствующими файлами-владельцами и документацией.
- Не включать случайный editor noise и не синхронизировать revisions четырёх пакетов.

### `last_changes` (Mod Manager / Steam)

Поле `last_changes` в `metadata.lua` каждого пакета — накопительный changelog для игрока в Mod Manager.

| Когда | Действие |
| --- | --- |
| Обычный коммит / feature / hotfix (не Steam upload) | **Дописать** в конец краткий буллет/строку по сути изменения. Существующий текст **не** удалять и **не** заменять целиком. |
| Заливка пакета в **Steam Workshop** (явный запрос пользователя на upload) | **Полностью перезатереть** `last_changes` свежим текстом только этого upload (что уйдёт игрокам как «последние изменения» Workshop). |

Не путать с GitHub Release notes / `CHANGELOG.md`: те живут отдельно. Не перезаписывать `last_changes` «на всякий случай» при GitHub tag/release, если Steam upload в том же шаге не делается.

## Зафиксировать состав релиза

1. Выбрать точный SHA из `origin/main` каждого репозитория.
2. Записать metadata-derived release version, четыре SHA, четыре package metadata versions, mod IDs, версию игры и проверенный CommonLib в новый manifest.
3. Не использовать содержимое рабочего дерева как источник архива.
4. Не менять и не переиспользовать уже опубликованный tag/manifest.
5. Убедиться, что в каждом репозитории существует только remote `origin` и он указывает на ожидаемый GitHub-репозиторий.

Локальные незакоммиченные и untracked-файлы никогда не включать. Для сборки использовать чистый checkout точного SHA в отдельном временном каталоге или GitHub Actions.

## Проверить release-кандидат

Локальная проверка сама получает версию из committed core metadata:

```powershell
& .agents/skills/release-jazz-suite/scripts/test-release-state.ps1
```

В GitHub Actions дополнительно проверить тег:

```powershell
& .agents/skills/release-jazz-suite/scripts/test-release-state.ps1 -ExpectedTag $env:GITHUB_REF_NAME
```

Для диагностического отчёта, который не завершится ошибкой из-за найденных блокеров:

```powershell
& .agents/skills/release-jazz-suite/scripts/test-release-state.ps1 -ReportOnly
```

Затем выполнить проверки из `docs/technical/testing.md`, проверить save/new game, LFS objects, структуру архивов, manifest, SHA-256, release notes и contributors.

Если runtime-тест невозможен, остановить публикацию стабильного релиза либо явно выпустить prerelease с указанием непроверенного пункта.

## Опубликовать

1. Создать draft GitHub Release из metadata-derived tag.
2. Назвать release по engine display из core metadata.
3. Приложить четыре архива, manifest и файл SHA-256.
4. Проверить скачанные assets повторно.
5. Опубликовать draft и сообщить display version, tag, четыре SHA и выполненные проверки.

Не создавать отдельные GitHub Releases в asset/maps/units-репозиториях. Их metadata versions и SHA остаются частью центрального неизменяемого manifest.

## Ограничения безопасности

- Не добавлять в релиз незакоммиченные изменения пользователя.
- Если пользователь отдельно разрешил release commit, писать его заголовок и пояснение на русском языке; Git-теги, версии, SHA и технические идентификаторы не переводить.
- Не выполнять `git clean`, `git reset`, автоматический stash или массовую нормализацию строк.
- Не форсировать теги и не заменять assets уже опубликованной версии.
- Не править read-only metadata revision вручную.
- Не публиковать архив с blob больше лимита GitHub или с невыгруженным Git LFS.
- Не считать release успешным, пока GitHub workflow и checksums не подтверждены.
