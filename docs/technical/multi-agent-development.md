# Параллельная работа AI-агентов

## Когда нужен coordinator

Coordinator обязателен, если выполняется хотя бы одно условие:

- одновременно работают более трёх исполнителей;
- изменение затрагивает два и более репозитория;
- затронут `items.lua`, `metadata.lua`, editor state, map или release manifest;
- write sets потенциально пересекаются.

## Изоляция

- Один агент — один Git worktree/branch на репозиторий.
- Shared dirty working tree используется только для одиночной локальной работы, не для параллельной интеграции.
- Coordinator назначает spec ID, исполнителя, reviewer и declared write set.
- Агент не меняет файл вне write set; расширение сначала утверждается в spec.

## Exclusive resources

Ресурсы из [`../ownership/exclusive-resources.yaml`](../ownership/exclusive-resources.yaml) имеют одного владельца в момент времени. В первую очередь это:

- `items.lua` + `metadata.lua` одного пакета;
- открытое состояние Mod/Map/Entity Editor;
- конкретная карта или map patch;
- localization ID allocation;
- release manifest и tag.

Изменения независимых companion-файлов одного пакета могут выполняться параллельно только до editor round-trip. Сведение в `items.lua`/`metadata.lua` выполняет один integration owner.

## Роли

- Architect/human: утверждает spec, ADR, scope expansion и субъективный/runtime результат.
- Coordinator: раздаёт write sets, exclusive resources и порядок интеграции.
- Implementer: меняет только выделенный scope и пишет evidence.
- Reviewer: read-only проверяет соответствие `REQ-*`/`AC-*` diff-у и evidence.
- Documenter: синхронизирует current-state docs по accepted diff, не повторяя полный runtime-аудит.
- Integrator: связывает SHA четырёх репозиториев и запускает suite smoke.

## Review packet

Reviewer получает:

1. approved spec и связанные ADR;
2. diff объявленного write set;
3. результаты профильных checks;
4. evidence по `AC-*`;
5. список непроверенных рисков.

Полный repository dump и несвязанные system docs в review packet не включаются.

## Интеграция четырёх репозиториев

Межрепозиторная поставка фиксирует spec ID, repo, branch/commit и package owner. Для незакоммиченного локального результата явно писать `working-tree`, не изобретая SHA. Перед release exact commits переносятся в release manifest.

CI-контракт публикуется в порядке: сначала reusable workflow `JAZZ/.github/workflows/suite-package-gate.yml` в `main`, затем caller workflows пакетов. Пока первый шаг не завершён, sibling PR нельзя считать защищённым suite gate.
