---
id: JAZZ-ASSETS-001
status: implemented
owner: project-owner
systems:
  - assets-entities
  - generated-data-validation
repositories:
  - jazz
  - jazz_assets
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-ASSETS-001.md
  - jazz/.agents/skills/sync-jazz-generated-data/scripts/check-asset-integrity.ps1
  - jazz/.github/workflows/suite-package-gate.yml
  - jazz/docs/technical/systems/assets-entities.md
  - jazz_assets/Entities/HMMWV.ent
exclusive_resources:
  - jazz_assets/Entities/HMMWV.ent
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-ASSETS-001: целостность Entity и collision HMMWV

## Проблема

В `jazz_assets` опубликовано изменение `Entities/HMMWV.ent`, в котором один collision-треугольник стал вырожденным: первая и третья вершины совпадают, а сохранённый `surf_hash` относится к прежней геометрии. Существующий suite gate проверяет generated graph и whitespace, но не разбирает Entity XML и не обнаруживает вырожденные collision-треугольники или отсутствующие mesh/material-файлы.

Аудит также выявил незарегистрированные M60/PKM Entity, на которые ссылается core JAZZ. Их исправление требует выбора визуального контракта, синхронной правки занятых `jazz/items.lua`/`metadata.lua`, editor round-trip и runtime-проверки; эти файлы уже содержат незавершённые изменения владельца и не входят в текущий write set.

## Цели

- восстановить невырожденный collision-треугольник `HMMWV`, не меняя публичный Entity ID и добавленные state IDs;
- добавить read-only structural audit для Entity XML и resource references;
- включить structural audit в reusable suite gate для `jazz_assets`;
- зафиксировать границу между исправленной регрессией и M60/PKM долгом, который нельзя безопасно чинить без editor/runtime evidence.

## Non-goals

- изменение `jazz/items.lua`, `jazz/metadata.lua` или weapon component presets;
- регистрация, переименование или удаление 13 dormant/orphan-candidate Entity;
- массовая замена legacy absolute `<src file>` путей;
- перепаковка meshes, materials, textures или BinAssets;
- обход `jazz-maps/Maps/`;
- изменение save, network, localization, dependency или load-order contract.

## Требования

- `JAZZ-ASSETS-001-REQ-001` — `HMMWV` сохраняет IDs `idle`, `Idle`, `idle_Combat`, `walk`, `Walk`, `run`, `Run`, `death`, `Death`, а collision surface не содержит треугольников с повторяющимися вершинами.
- `JAZZ-ASSETS-001-REQ-002` — structural audit разбирает каждый корневой `Entities/*.ent`, проверяет XML, duplicate state IDs, локальные `mesh_ref`, mesh/material paths, case-sensitive paths и collision triangles.
- `JAZZ-ASSETS-001-REQ-003` — дефект активной зарегистрированной Entity блокирует аудит; дефект dormant/unlisted Entity остаётся явным warning до отдельного ownership-решения.
- `JAZZ-ASSETS-001-REQ-004` — suite package gate запускает structural audit только для `jazz_assets`, не обходя `jazz-maps/Maps/`.
- `JAZZ-ASSETS-001-REQ-005` — M60/PKM references и существующий legacy debt документируются, но generated weapon data не меняется поверх текущего dirty state.

## Инварианты и ограничения

- Entity ID `HMMWV`, resource paths, state IDs и metadata registration не меняются.
- Правка collision восстанавливает опубликованную до регрессии вершину; новый hash не вычисляется по догадке.
- `items.lua`, `metadata.lua`, Entity Lua companions и бинарные ресурсы не изменяются.
- Structural audit является read-only и не удаляет orphan/dormant файлы.
- Legacy absolute source paths считаются известным долгом и не блокируют quality gate.
- Посторонние незакоммиченные изменения во всех репозиториях не входят в change set.

## Acceptance criteria

- `JAZZ-ASSETS-001-AC-001` — XML `HMMWV.ent` разбирается, сохраняет девять требуемых state IDs и не содержит collision-треугольников с повторяющимися вершинами.
- `JAZZ-ASSETS-001-AC-002` — structural audit на текущем `jazz_assets` завершается без blocking errors и выводит dormant resource problems как warnings.
- `JAZZ-ASSETS-001-AC-003` — fixture/self-test доказывает, что duplicate collision vertex и отсутствующий resource активной Entity дают ненулевой exit code.
- `JAZZ-ASSETS-001-AC-004` — reusable workflow вызывает structural audit только при `inputs.package == 'jazz_assets'`; YAML и `git diff --check` проходят.
- `JAZZ-ASSETS-001-AC-005` — generated-data audit не показывает новых errors/warnings относительно зафиксированного baseline.
- `JAZZ-ASSETS-001-AC-006` — в новом процессе игры `HMMWV` загружается без missing entity/state/material сообщений, collision не создаёт assert; runtime evidence подтверждено владельцем.
- `JAZZ-ASSETS-001-AC-007` — technical current-state документация описывает structural gate, исправленный collision и оставшийся editor/runtime долг M60/PKM.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: vanilla schema и CommonLib не переопределяются; изменяется только custom `HMMWV` resource и CI-аудит JAZZ.
- Saves: публичные ID и сериализуемые поля не меняются.
- Network/determinism: Lua/runtime logic и RNG не меняются.
- Generated data: `items.lua`, `metadata.lua` и Entity Lua companions неизменны; `.ent` остаётся editor-owned resource и требует runtime/editor подтверждения.
- Cross-package references: существующие consumers `HMMWV` сохраняют тот же ID и state names. M60/PKM references остаются отдельным незакрытым долгом.
- Rollback/recovery: откат состоит в возврате одной collision vertex и удалении вызова structural audit; generated graph не требует миграции.

## План и ownership

- Пакет-владелец Entity/resource: `jazz_assets`.
- Runtime-владелец quality contract и documentation: `jazz`.
- Исполнитель: Codex.
- Reviewer и runtime acceptance: project-owner.
- Declared write set: только пути из YAML frontmatter.
- Exclusive resource: `jazz_assets/Entities/HMMWV.ent`.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner.
- Дата: 26 июля 2026 года.
- Основание: после диагностического отчёта владелец проекта поручил «поправь что сможешь»; scope ограничен доказанной HMMWV-регрессией и read-only validation, без рискованной правки занятого generated data.

## Evidence

- `JAZZ-ASSETS-001-AC-001`: `PASS` — static: `HMMWV.ent` разобран как XML; найдены все 9 state IDs, отсутствующие states = 0, collision triangles с повторяющимися вершинами = 0.
- `JAZZ-ASSETS-001-AC-002`: `PASS` — static: `check-asset-integrity.ps1` проверил 490 registered / 503 on-disk Entity; blocking errors = 0, dormant warnings = 19, результат `PASSED`.
- `JAZZ-ASSETS-001-AC-003`: `PASS` — static self-test: fixture активной Entity с двумя отсутствующими resources и duplicate collision vertex дал 3 blocking errors.
- `JAZZ-ASSETS-001-AC-004`: `PASS` — static: `js-yaml@4.1.0` разобрал reusable и caller workflows; conditional call присутствует только для `inputs.package == 'jazz_assets'`; package overlay и scoped whitespace прошли.
- `JAZZ-ASSETS-001-AC-005`: `PASS` — generated/static: sync audit сохранил baseline `errors=0`, `warnings=14`; новых generated graph расхождений нет.
- `JAZZ-ASSETS-001-AC-006`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-ASSETS-001-AC-007`: `PASS` — static: `check-system-docs.ps1` завершён, `systems=19`, `skills=6`, `markdown=95`, `repos=4`.

## Documentation delta

- Обновить `docs/technical/systems/assets-entities.md`: structural audit, исправленный collision `HMMWV`, статический уровень подтверждения и M60/PKM debt.
- `file-coverage.md` не меняется: runtime load-state существующих файлов не меняется.
- Wiki не меняется: новое игровое правило или видимый контент не вводится.
