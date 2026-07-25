# Релизы и версионирование

## Назначение и границы

Система определяет версию и воспроизводимый выпуск JAZZ как комплекта из четырёх независимых Git-репозиториев. Она относится к developer/release tooling и не меняет игровые правила, поэтому отдельная wiki-страница игрока не требуется.

## Источник и отображение версии

Единственный источник центральной версии — `jazz/metadata.lua` в exact commit core-пакета.

В установленном vanilla JA3 `ModDef` определяет:

- `version_major`;
- `version_minor`;
- read-only `version` с именем `Revision`.

`ModDef:GetVersionString()` выводит значения в формате `%d.%02d-%03d`. Например, metadata `0 / 11 / 5899` даёт:

- отображение в JA3 и release title: `0.11-5899`;
- нормализованный GitHub tag: `v0.11.5899`;
- путь manifest: `release/manifests/v0.11.5899.json`.

Release tooling читает metadata через `git show <core-sha>:metadata.lua`. Working tree, отдельный `VERSION` и вручную переданный PATCH источниками версии не являются.

Нормализованный tag сохраняет трёхчисловую форму для GitHub tooling, но третье число остаётся editor revision. При изменении major/minor revision не сбрасывается искусственно.

## Значение major/minor/revision

| Поле | Когда меняется |
|---|---|
| `version_major` | Несовместимое поколение после стабилизации публичного контракта |
| `version_minor` | Новый совместимый функционал; до `1.0` также breaking change |
| `version` | Автоматический revision Mod Editor; новое третье число release tag |

Для совместимого исправления major/minor остаются прежними. Conventional Commits помогают классифицировать изменение и сформировать changelog, но не определяют номер версии.

Поверхность совместимости включает saves, package IDs, dependencies/load order, Lua/API/IDs, generated data, межпакетные paths и структуру установки.

## Правило изменения metadata

`metadata.lua` является generated data и изменяется через Mod Editor.

1. `version_major`/`version_minor` менять только по классификации совместимости.
2. `version`, `saved`, `code_hash` и generated arrays не редактировать вручную.
3. Изменения `code`, dependencies, loctables, resources и registrations коммитить вместе с соответствующими файлами-владельцами.
4. После сохранения сравнить `metadata.lua`, `items.lua` и отдельные generated definitions и удалить случайный editor noise.
5. Не создавать необъяснённый metadata-only commit.
6. Допустимое metadata-only исключение — сохранение core ModDef через Mod Editor как явный release marker, если релиз меняет только assets/maps/units.
7. Не синхронизировать revisions пакетов и не менять metadata неизменившегося sibling-пакета.
8. Не включать номер версии в `title` или `description`: версия отображается из полей metadata.

Каждый новый центральный release должен получить новый committed core revision относительно предыдущего manifest.

## Версии четырёх пакетов

Core metadata определяет имя центрального release. Assets, maps и units сохраняют собственные версии Mod Editor.

Release manifest фиксирует для каждого пакета:

- `version_major`, `version_minor`, `version`;
- engine display;
- exact SHA;
- mod ID;
- artifact и SHA-256.

Разные package metadata versions не являются ошибкой и не требуют искусственного выравнивания.

## Публичный релизный контракт

- Канонический tag создаётся только в `Kpoji4er/JAZZ`.
- Центральный GitHub Release содержит четыре package archives.
- Exact SHA и metadata version каждого repo фиксируются в неизменяемом manifest.
- Release title использует engine display из core metadata.
- Опубликованный tag, manifest и assets не заменяются; исправление получает новый editor revision.

## Поток выпуска

1. Проверить `git status`, ветки, remotes и актуальный CommonLib.
2. Выбрать четыре exact SHA из `origin/main`.
3. Получить central display/tag из committed core metadata.
4. Проверить правило изменения metadata и новый revision относительно предыдущего manifest.
5. Подготовить и закоммитить manifest.
6. Выполнить статические и игровые проверки.
7. Создать metadata-derived tag.
8. GitHub Actions повторно выводит tag из metadata, checkout каждого SHA, загружает LFS и собирает четыре архива.
9. Workflow создаёт draft release; после повторной проверки assets draft публикуется.

Ветка `main` не является источником сборки после начала workflow: используются только SHA из manifest.

## Безопасность рабочего дерева

Незакоммиченные и untracked-файлы никогда не являются источником архива. Release tooling не выполняет `stash`, `clean`, `reset` и не создаёт release-коммит из пользовательских изменений без отдельного запроса.

`jazz-maps` содержит development source `Images/GrandChienMap.psd`, превышающий лимит обычного GitHub blob. До миграции он переводится в Git LFS и исключается из runtime archive. После checkout проверяется, что в архив не попали LFS pointer-файлы.

## Владельцы и файлы

- Процесс: `.agents/skills/release-jazz-suite/SKILL.md`.
- Политика: `.agents/skills/release-jazz-suite/references/versioning-policy.md`.
- Контракт GitHub/manifest: `.agents/skills/release-jazz-suite/references/release-contract.md`.
- Read-only preflight: `.agents/skills/release-jazz-suite/scripts/test-release-state.ps1`.
- Центральный владелец release metadata и workflow: core repository `JAZZ`.

## Проверка

```powershell
& .agents/skills/release-jazz-suite/scripts/test-release-state.ps1
& .agents/skills/release-jazz-suite/scripts/test-release-state.ps1 -ExpectedTag $env:GITHUB_REF_NAME
& .agents/skills/document-jazz-systems/scripts/check-system-docs.ps1
git diff --check
```

Перед stable release дополнительно обязательны профильные проверки из `docs/technical/testing.md`, загрузка существующего save, старт новой игры, проверка четырёх archives и SHA-256.

## Источники

- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) — семантика совместимости major/minor и неизменяемость релиза
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) — рекомендуемая классификация commit history
- установленный `<JA3_ROOT>/ModTools/Src/CommonLua/Classes/Mod.lua` — фактический формат версии ModDef
