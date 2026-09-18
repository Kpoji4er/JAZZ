---
id: JAZZ-AGENT-SKILLS-001
status: implemented
owner: project-owner
systems:
  - agent-tooling
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: not-required
write_set:
  - docs/specs/active/JAZZ-AGENT-SKILLS-001.md
  - .agents/skills/*/SKILL.md
  - .agents/skills/*/references/*.md
  - .agents/skills/document-jazz-systems/scripts/check-system-docs.ps1
  - .agents/docs/index.md
  - .agents/docs/reference/agent-tooling.md
  - docs/tools/_check_agent_docs_validation.py
  - docs/tools/README.md
exclusive_resources:
  - .agents/skills/document-jazz-systems/scripts/check-system-docs.ps1
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-AGENT-SKILLS-001: оптимизация навыков агентов

## Проблема

Аудит по запросу владельца выявил повторное чтение общих инструкций, несогласованные процедуры и проверки, которые расширяют локальную задачу на весь комплект. Это увеличивает контекст и число действий, а иногда даёт ложный сигнал о незавершённости работы.

Подтверждённые примеры на 2026-09-15:

| Источник | Наблюдение | Последствие |
| --- | --- | --- |
| `sync-jazz-generated-data/SKILL.md`, начало задачи | Безусловное чтение work-on-jazz-mod, проверка последнего CommonLib и аудит четырёх пакетов | Даже правка одного свойства требует действий вне её impact; противоречит узкой маршрутизации work-on-jazz-mod |
| `document-jazz-systems/scripts/check-system-docs.ps1` | Единственный входной параметр SuiteRoot; отсутствие agents/openai.yaml считается ошибкой | Нельзя отделить локальную проверку от полного аудита; стандарт skill-creator допускает отсутствие UI metadata |
| `create-jazz-merc/SKILL.md`, завершение | Отдельная Discord-новость на каждый пакет | Противоречит каноническому jazz-git-push-chunks.mdc: один primary на логическое изменение |
| Навыки иконок и портретов | GenerateImage, reference_image_paths и aspect_ratio записаны как параметры вызова | Эти имена не соответствуют доступному сейчас image_gen; агенту приходится восстанавливать интерфейс самостоятельно |
| `create-jazz-action-icons/SKILL.md` | Passive имеет отдельный контракт 54×54, но общий workflow/finalize/QA требует 108×54 | Есть риск применить active-конвейер к passive-иконке |
| `create-jazz-chip-icons/SKILL.md` | Ревью пользователем указано обязательным шагом, хотя вход допускает «сразу вставь» | Возможна повторная остановка после уже полученного разрешения |

Это аудит инструкций, а не подтверждение дефектов всех вспомогательных скриптов. Полный построчный аудит всех references и исполнения генераторов ещё не выполнен; новые находки вне требований ниже требуют обновления scope.

## Цели

- Сохранить работу через спецификации и реальные критерии приёмки.
- Сократить обязательное чтение и проверки до затронутого контракта.
- Устранить подтверждённые противоречия без изменения визуального канона и игровых механик.
- Сделать локальную проверку документации пригодной для работы при существующем постороннем dirty state.

## Non-goals

- Игровые баги K4/K5, ИИ, оружие, UI и ранее подготовленные игровые изменения.
- Запуск JA3, загрузка сохранений, редактор, DAP, runtime-проверки.
- Правки Code, items.lua, metadata.lua, локализации, карт и ресурсов любого пакета.
- Коммит, push, релиз, публикация и установка плагинов.
- Удаление навыков, массовое форматирование, переписывание всех reference-файлов или создание UI metadata для каждого навыка.
- Отмена approved spec, DoR/DoD, human acceptance либо требований к runtime evidence в игровых задачах.

## Требования

- `JAZZ-AGENT-SKILLS-001-REQ-001` — сохранить lifecycle draft → approved → implemented → accepted. Явное согласование конкретного scope в текущей беседе можно зафиксировать в spec без повторного вопроса; разрешение только написать draft не разрешает реализацию. Новое поведение вне утверждённого scope требует обновления spec и решения владельца.
- `JAZZ-AGENT-SKILLS-001-REQ-002` — в generated-data workflow определять пакет и тип изменения до проверок. Локальный аудит запускать с существующим -Package; полный комплект проверять для межпакетного impact или явно заказанного общего аудита. Проверку upstream CommonLib выполнять для dependency/compatibility-sensitive изменений, повторно используя подтверждённый snapshot в пределах задачи. Сохранить транзакцию items/metadata/companion и требования к editor round-trip.
- `JAZZ-AGENT-SKILLS-001-REQ-003` — сократить повторяющиеся инструкции ссылками на канонический источник; читать references по типу операции, сохранив обязательные инварианты в entrypoint. Проверить затронутые относительные ссылки. Не устанавливать произвольный лимит строк ради сокращения.
- `JAZZ-AGENT-SKILLS-001-REQ-004` — заменить локальный пересказ Discord/push в create-jazz-merc ссылкой на каноническое правило. Никаких публикаций в рамках этого изменения.
- `JAZZ-AGENT-SKILLS-001-REQ-005` — в навыках изображений отделить требования к результату от API: обращаться к доступному imagegen skill/tool и его актуальной схеме. Пропорции и референсы описывать без несуществующих параметров. Сохранить размеры, цвета, пути, identity/style references и существующие разрешённые процедуры финализации; учитывать инструкции применяемого инструмента. Active 108×54 и Passive 54×54 должны иметь раздельные ветки workflow и QA.
- `JAZZ-AGENT-SKILLS-001-REQ-006` — различать самостоятельную визуальную QA и запрошенное пользователем согласование draft. Ранее явное разрешение на вставку не требует повторного согласования, а запрос только draft не разрешает wiring.
- `JAZZ-AGENT-SKILLS-001-REQ-007` — добавить в check-system-docs.ps1 необязательный -Paths для явного набора repository-relative файлов. Без параметра сохранить полный аудит. Локальный режим проверяет выбранные документы/навыки и их ссылки; глобальные coverage-проверки не маскирует под выполненные. Неизвестный путь даёт ошибку. Отсутствие optional agents/openai.yaml само по себе не ошибка; существующий файл продолжает проверяться. Полный режим сохраняет проверки реальных broken links, coverage и повреждённых файлов.
- `JAZZ-AGENT-SKILLS-001-REQ-008` — подтвердить изменения примерами маршрутизации и изолированными проверками валидатора. Отдельно отчитываться о локальном результате и существующих ошибках полного аудита, не исправляя посторонние документы для получения зелёного статуса.

## Инварианты и ограничения

- До отдельного согласования этого draft изменяется только данный файл спецификации.
- Ранее существующие правки, включая правки других задач и сохранённое правило запуска через Steam, не откатываются и не включаются автоматически в реализацию этого spec.
- Расширение write set не разрешает игровые изменения. Wildcard навыков ограничен перечисленными требованиями; фактически изменённые пути перечислить в evidence.
- Ни один workflow не запускает игру сам по себе в задаче аудита навыков. В будущем JA3 запускается через Steam; обычный Steam-запуск не гарантирует DAP.
- Изменение не ослабляет запрет обхода jazz-maps/Maps целиком и запрет публикаций без явного разрешения.

## Acceptance criteria

- `JAZZ-AGENT-SKILLS-001-AC-001` — сценарии «только draft», «утверждённый scope», «новое требование» дают соответственно: подготовку spec без реализации, выполнение разрешённой работы, обновление spec до реализации нового требования. Соответствует REQ-001.
- `JAZZ-AGENT-SKILLS-001-AC-002` — для правки Icon существующего ModItem маршрут выбирает нужный пакет и связанные представления без обязательного upstream-аудита всего комплекта; изменение зависимости сохраняет compatibility-проверку; rename публичного ID сохраняет проверку межпакетных ссылок. Соответствует REQ-002/003.
- `JAZZ-AGENT-SKILLS-001-AC-003` — в merc workflow нет альтернативной политики Discord; ссылки на канонические правила существуют. Соответствует REQ-004.
- `JAZZ-AGENT-SKILLS-001-AC-004` — маршруты active, passive и chip сохраняют разные размеры/поля; инструкции не требуют неподдерживаемых параметров инструмента. Сценарий «сразу вставь» не блокируется обязательным повторным ревью; «покажи draft» не делает wiring. Генерация платных изображений для проверки не требуется. Соответствует REQ-005/006.
- `JAZZ-AGENT-SKILLS-001-AC-005` — изолированные fixtures валидатора: skill без optional YAML проходит; повреждённый имеющийся YAML и broken link выбранного файла проваливаются; посторонний дефект вне -Paths не проваливает локальный режим, но выявляется полным; несуществующий выбранный файл проваливается. Локальный вывод явно указывает scope. Соответствует REQ-007/008.
- `JAZZ-AGENT-SKILLS-001-AC-006` — изменённые навыки проходят применимую структурную проверку skill-creator; diff укладывается в write set, игровые файлы не изменены этой работой. Оставшиеся ошибки полного аудита перечислены отдельно. Соответствует REQ-003/008 и ограничениям.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: меняется процедура работы агента, игровой контракт не меняется.
- Saves: без изменений.
- Network/determinism: без изменений.
- Generated data: без изменений.
- Cross-package references: только ссылки в инструкциях; sibling repositories не изменяются.
- Validator compatibility: существующий вызов без -Paths сохраняет полный scope; optional YAML перестаёт быть ложной ошибкой в обоих режимах.
- Rollback/recovery: откатить только собственный diff навыков/валидатора, сохранив предшествующий dirty state. Старые вспомогательные скрипты не удалять.

## План и ownership

- Пакет-владелец: jazz, агентские инструкции и инструменты.
- Исполнитель: текущий агент после утверждения draft.
- Reviewer: владелец проекта; независимое ревью кода валидатора перед закрытием DoD.
- Этап 1: согласовать требования и границы, пройти Ready.
- Этап 2: исправить противоречия API, active/passive, разрешений и публикации; сузить generated-data preflight.
- Этап 3: реализовать локальный режим валидатора и проверки на временных fixtures; зарегистрировать новый audit helper.
- Этап 4: проверить навыки, примеры маршрутизации, ссылки и полный diff; заполнить evidence, пройти Done.
- Declared write set: frontmatter. Reference-файлы менять только если без этого сохраняется противоречие с исправленным entrypoint.
- Exclusive resources: check-system-docs.ps1; не допускать одновременной записи другим исполнителем.

## Решение владельца

- Статус: approved; реализация разрешена 2026-09-15.
- Кто подтвердил: пользователь, «эту спецификацию делай, потом пиши по нашему фидбеку ранее».
- Дата: 2026-09-15.
- Основание: «мы через спецификации работаем, поэтому свои изменения через спецификации делай тоже; пока можешь ее написать — файлы игры пока трогать не стоит».

## Evidence

- `JAZZ-AGENT-SKILLS-001-AC-001`: `PASS` — static review — draft-only не разрешает реализацию; явное разрешение scope фиксируется без повторного вопроса; новое требование требует решения владельца. Проверено по specify-jazz-change.
- `JAZZ-AGENT-SKILLS-001-AC-002`: `PASS` — static review — Icon: пакет-владелец и связанные generated layers; dependency: CommonLib compatibility; rename: межпакетные ссылки. Round-trip и ограничения maps сохранены.
- `JAZZ-AGENT-SKILLS-001-AC-003`: `PASS` — static — create-jazz-merc теперь ссылается на существующее каноническое правило push; публикаций не выполнялось.
- `JAZZ-AGENT-SKILLS-001-AC-004`: `PASS` — static review — Active 108×54 и Passive 54×54 имеют отдельные finalize/QA; chip остаётся 64×64/ChipIcon. Актуальный инструмент определяется через imagegen; draft и разрешённый wire различены. Изображения не генерировались.
- `JAZZ-AGENT-SKILLS-001-AC-005`: `PASS` — tool execution — python docs/tools/_check_agent_docs_validation.py: 11 PASS на изолированном комплекте, включая полный чистый прогон, optional YAML, повреждённый default_prompt, broken links, отсутствующий/внешний/пустой/неподдерживаемый Paths.
- `JAZZ-AGENT-SKILLS-001-AC-006`: `PASS` — static/tool execution — 12 изменённых SKILL.md прошли python -X utf8 quick_validate.py. Собственный diff сверён с исходным снимком .tmp/skills-audit-baseline.json; игровые файлы этой работой не менялись. Ограничения общего аудита описаны ниже.

## Documentation delta

Документация игрового runtime, wiki и showcase не требует изменения: этот spec не меняет игру. После реализации обновить агентский reference и вызов валидатора в document-jazz-systems; индекс менять только при изменении маршрутизации. Реализованы перечисленные изменения навыков, адресный валидатор и регрессионный helper; индекс не требовал изменения маршрутизации.


### Ограничения проверки и ревью

Полный аудит выполнен, но не прошёл по существующим ошибкам: абсолютные пути в двух how-to-custom-slabs, coverage для LegionMedicineLoadouts/System_ReloadStyle/System_WeaponComponent_Set/System_WeaponRemovableModify, ссылки в design/mercs-ja12, trailing whitespace. Вывод: `.tmp/skills-full-validation.txt`. Локальная проверка изменённых Markdown сохраняет прежние ошибки trailing whitespace (включая Markdown hard breaks); правила форматирования не ослаблялись, массовая очистка не выполнялась. Вывод: `.tmp/skills-local-validation.txt`. Это не ошибки регрессионных fixtures.

Проверка openai.yaml сохраняет существующий ограниченный текстовый контракт interface/default_prompt/encoding; это не полноценный YAML parser. Самопроверка выполнена, независимое ревью и human acceptance ещё не выполнены: статус implemented означает готовность к ревью, не accepted. Коммитов и публикаций нет.

### Фактический write set

- `.agents/skills/create-jazz-action-icons/SKILL.md`
- `.agents/skills/create-jazz-chip-icons/SKILL.md`
- `.agents/skills/create-jazz-component-icons/SKILL.md`
- `.agents/skills/create-jazz-merc/SKILL.md`
- `.agents/skills/create-jazz-merc-portraits/SKILL.md`
- `.agents/skills/create-jazz-perk-icons/SKILL.md`
- `.agents/skills/create-jazz-squad-icons/SKILL.md`
- `.agents/skills/create-jazz-status-icons/SKILL.md`
- `.agents/skills/document-jazz-systems/SKILL.md`
- `.agents/skills/frame-jazz-merc-ui-portrait/SKILL.md`
- `.agents/skills/specify-jazz-change/SKILL.md`
- `.agents/skills/sync-jazz-generated-data/SKILL.md`
- `.agents/skills/create-jazz-component-icons/references/style-and-naming.md`
- `.agents/skills/create-jazz-merc-portraits/references/style-and-naming.md`
- `.agents/skills/create-jazz-squad-icons/references/style-and-naming.md`
- `.agents/skills/sync-jazz-generated-data/references/generated-data-contract.md`
- `.agents/skills/document-jazz-systems/scripts/check-system-docs.ps1`
- `.agents/docs/reference/agent-tooling.md`
- `docs/tools/README.md`
- `docs/tools/_check_agent_docs_validation.py`
- `docs/specs/active/JAZZ-AGENT-SKILLS-001.md`
