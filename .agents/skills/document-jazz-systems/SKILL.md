---
name: document-jazz-systems
description: Обновлять и проверять техническую документацию JAZZ как current-state источник истины по реализации и синхронизировать с ней игроковую docs/wiki для заметного игроку поведения. Использовать при изменении runtime behavior, generated data, load-state, public IDs, dependencies, compatibility, тестового контракта или границ пакетов, а также при documentation-only аудите.
---

# Техническая документация JAZZ

`docs/technical/` описывает фактически загруженную реализацию. `docs/wiki/` объясняет игроку наблюдаемое поведение без внутренних деталей и не может противоречить technical. Будущее или только утверждённое поведение хранить в `docs/specs/`, архитектурные причины — в `docs/decisions/`.

## Workflow

1. Определить затронутую систему, implementation files, load-state и observable effect.
2. Прочитать `docs/technical/systems/README.md`, профильную страницу и [documentation-map.md](references/documentation-map.md).
3. Обновить профильную страницу по [system-template.md](references/system-template.md), не копируя общий engine manual.
4. Разделить вклад установленной vanilla, подтверждённой CommonLib и JAZZ. Snapshot зависимости ссылать из одного канонического документа, а не копировать между страницами.
5. Обновить условно:
   - `file-coverage.md` — файл или load-state;
   - `override-matrix.md` — новое или изменённое пересечение;
   - `compatibility.md` — saves, network, dependency или public contract;
   - `testing.md` — общий validation profile;
   - `technical-debt.md` — подтверждённый долг.
6. Для изменённого icon, preview, sprite, portrait, entity или sound asset указать repository-relative media path либо явно отметить, что asset contract не менялся.
7. Сопоставить technical diff с фактическим diff реализации и spec. Не описывать approved, но ещё не реализованное поведение как текущее.
8. Если изменение заметно игроку, обновить профильную `docs/wiki/`-страницу. Оружейные числа и компоненты менять в канонических CSV и пересобирать `scripts/docs/weapons-docs.mjs`, а не редактировать generated pages вручную.
9. Если затронут аспект публичной витрины, в том же change set обновить `docs/showcase/ru/` и `docs/showcase/en/` (ADR-0003). Не править GitHub Wiki вручную — публикация через `scripts/docs/publish-github-wiki.ps1` / workflow.
10. Запустить `.agents/skills/document-jazz-systems/scripts/check-system-docs.ps1`.

## Definition of Done

- изменённый current-state contract описан на одной канонической системной странице;
- technical, wiki и showcase (RU+EN) не противоречат друг другу; все внутренние ссылки существуют;
- новый/удалённый/перемещённый/dormant файл отражён в coverage;
- compatibility и validation обновлены только при реальном impact;
- документация фиксирует уровень подтверждения: static, editor, runtime или human;
- каждый documentation delta связан со spec ID, если изменение требовало spec.
