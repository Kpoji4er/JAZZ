# Правила работы с JAZZ

JAZZ состоит из четырёх репозиториев:

| Репозиторий | Локальный каталог | Что он содержит |
| --- | --- | --- |
| `jazz` | `..\jazz` | Код оверхола, предметы, эффекты, UI |
| `jazz_assets` | `..\jazz_assets` | Сущности, модели, материалы, текстуры |
| `jazz-maps` | `..\jazz-maps` | Карты, квесты, диалоги, сектора, патчи |
| `jazz-units` | `..\jazz-units` | UnitData, AI-архетипы, отряды, прогрессия |

Перед любым изменением определяй пакет-владельца данных и не переноси файлы между репозиториями ради удобства.

## Быстрый путь чтения

Новый корень — это не источник всех правил целиком, а индекс по ролям.
Сначала открой `.agents/docs/index.md`, затем выбирай релевантный документ:

- Общий контур проекта: `.agents/docs/reference/project-scope.md`
- Сложные runtime/потоки/сообщения: `.agents/docs/reference/runtime-model.md`
- Generated data (`items.lua`, `metadata.lua`, companion): `.agents/docs/reference/generated-data-sync.md`
- Проверки, git- и release-рутины: `.agents/docs/reference/checklists-and-release.md`
- Документационный контракт (technical/wiki): `.agents/docs/reference/documentation-contract.md`

## Ролевые playbookы

- AI / CTH / боеприпасы в тактике: `.agents/docs/playbooks/ai-system.md`
- Оружие и баланс: `.agents/docs/playbooks/weapons-balance.md`
- Карты, квесты, диалоги, контент: `.agents/docs/playbooks/maps-content.md`
- Юниты, отряды и прогрессия: `.agents/docs/playbooks/units-squads.md`
- Ассеты, интерфейс, звук, FX: `.agents/docs/playbooks/assets-and-ui.md`

## Основные источники

- Vanilla/источники `JA3`: `<JA3_ROOT>\ModTools\Src`
- Official docs: `<JA3_ROOT>\ModTools\Docs\index.md.html`
- Official samples: `<JA3_ROOT>\ModTools\Samples`
- Официальная история: <https://github.com/THQNordic/JaggedAlliance3Modding>
- CommonLib: <https://gitlab.com/injto4ka/ja3_commonlib>

`<JA3_ROOT>` — локальный путь к установленной игре, **не коммитится** и не пишется в документацию в виде абсолютного значения.

## Минимальные обязательства

1. Перед началом сверять актуальный upstream CommonLib (`main`/Workshop) и работать с ним как с текущей базой.
2. Любое изменение кода/данных: читать исходный контракт в релевантных playbook/ссылках и фиксировать в diff вместе с проверками.
3. Для generated data всегда поддерживать синхронизацию `items.lua` + `metadata.lua` + companion-файла и проверять через read-only `sync`-skill.
4. Не делать маскирующий рефакторинг: не смешивать перепаковку/перегенерацию с логическим код-рефакторингом.
5. Не запускать общий обход `jazz-maps/Maps/` без прямого запроса на конкретную карту/сектор/patch.
