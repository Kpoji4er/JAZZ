---
name: document-jazz-systems
description: Двухконтурный контракт документации для модификации JAZZ из четырёх пакетов. Использовать при изменении кода, generated data, gameplay rules, AI, UI, карт, юнитов, assets, audio, dependencies, load order, совместимости или границ пакетов; при аудите покрытия; при создании технической документации и пользовательской wiki. Требует обновлять technical-источник истины и, для заметных игроку изменений, соответствующий гайд по механике в той же задаче.
---

# Документирование систем JAZZ

Вести два связанных, но разных раздела:

- `docs/technical/` — реализация для разработчиков: слои, файлы, IDs, формулы, runtime flow, compatibility и tests;
- `docs/wiki/` — руководство для игроков: смысл механики, правила, примеры, советы и ограничения без лишних внутренних деталей.

Изменение не завершено, пока нужные аудитории не получили актуальное описание. Код, generated data, technical и wiki рассматриваются как один согласованный change set: ни реализация, ни документация не должны заведомо опережать другую сторону.

## Процесс документирования

1. Определить затронутые системы, implementation-файлы и пользовательские последствия.
2. Прочитать `docs/technical/systems/README.md`, техническую системную страницу, `file-coverage.md` и связанный wiki-гайд.
3. Определить последние commit/version официальной ветки CommonLib `main`, затем сравнить установленную vanilla, историю официальных исходников, релевантные страницы `<JA3_ROOT>/ModTools/Docs`, актуальную CommonLib и JAZZ.
4. Обновить technical-страницу по `references/system-template.md`.
5. Если изменение заметно игроку, обновить wiki по `references/wiki-template.md`.
6. Обновить сводные документы согласно `references/documentation-map.md`.
7. Запустить `scripts/check-system-docs.ps1` и исправить все относящиеся к задаче ошибки.
8. Проверить документацию вместе с diff кода и данных, сопоставив каждое изменение поведения с актуальным описанием.
9. Перед коммитом устранить расхождения: не оставлять обновление документации «на потом» и не выдавать запланированное, но ещё не реализованное поведение за действующее.

## Technical: обязательное происхождение

Разделять реализацию на три слоя:

- **Vanilla:** поведение установленного билда игры; публичный GitHub может быть более старым историческим источником.
- **CommonLib:** replacements, hooks, helpers, classes, presets и constants из последней upstream-версии. Указанный commit является снимком аудита, не pin.
- **JAZZ:** replacements и extensions любого из четырёх пакетов.

Не заявлять override без точного символа, preset ID, property, event или data record. Отличать прямую замену от hooks, inheritance, повторного использования данных и межпакетной ссылки.

Для каждого релевантного файла указывать loaded runtime, generated and loaded, dormant/unlisted, empty, inert/commented или development/editor-only.

Для loaded Lua дополнительно фиксировать, когда применимо:

- lifecycle-stage и доступность ModItem/data при file scope, clean start и hot reload;
- registration order `OnMsg`, допустимость sleep и владение custom message;
- `GameVar`/`MapVar`/`GlobalVar`, save fields, thread clock и риск старого bytecode из existing save;
- устойчивого владельца mutable state вместо временной Lua-таблицы `CObject`;
- стоимость map enumeration, XY/Z-семантику и hot-path ограничения;
- владельца UI mutation, context/SubContext и lifetime XWindow threads;
- editor diagnostics, panel errors/asserts и cache/restart requirements для generated assets.

Не копировать полный engine manual в каждую страницу: ссылаться на `docs/technical/systems/runtime-editor-integration.md` и описывать только контракт конкретной системы.

## Wiki: правила человеческого гайда

- Начинать с короткого объяснения, что меняется для игрока.
- Объяснять причины и практические последствия, а не пересказывать имена Lua-функций.
- Давать примеры, советы, типичные ошибки и связанные механики.
- Указывать ограничения демо, требования к версии и неподдерживаемые сценарии.
- Ссылаться на technical-страницу в конце, не копируя implementation dump.
- Не публиковать нестабильные внутренние IDs, если они не нужны игроку.

## Definition of done

Любое изменение поведения или данных обновляет, когда применимо:

- `docs/technical/systems/*.md`;
- `docs/technical/systems/file-coverage.md` при изменении файла или load-state;
- `docs/technical/override-matrix.md` при пересечении vanilla/CommonLib/JAZZ;
- `docs/technical/compatibility.md`, `architecture.md`, `testing.md` и `technical-debt.md` по типу риска;
- один или несколько гайдов `docs/wiki/*.md` при пользовательском эффекте;
- `docs/wiki/content-and-limitations.md` при изменении поддержки или scope;
- корневой `README.md` и `docs/README.md` при изменении публичных требований или структуры.

Чистый refactor без изменения поведения может не менять wiki, но technical-раздел и тестовый контракт всё равно должны оставаться верными. Documentation-only аудит явно фиксирует неопределённость.

## Общие правила написания

- Использовать repository-relative paths и `<JA3_ROOT>`; не сохранять абсолютный локальный путь автора.
- Снабжать датой или пометкой snapshot изменчивые количества и version/commit CommonLib.
- Не дублировать большие фрагменты между страницами; связывать их ссылками.
- При расхождении technical и wiki исправлять обе стороны в одной задаче.
- При расхождении реализации и документации исправлять обе стороны до завершения задачи; связанные межрепозиторные коммиты перечислять в итоговом отчёте.

## Ресурсы

- `references/documentation-map.md` — какие technical/wiki документы обновлять.
- `references/system-template.md` — структура технической системной страницы.
- `references/wiki-template.md` — структура пользовательского гайда.
- `scripts/check-system-docs.ps1` — read-only проверка покрытия, индексов и гигиены.