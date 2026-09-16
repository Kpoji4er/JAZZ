---
id: JAZZ-WEAPON-ROLLOUT-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/InventoryItem/{AK74,AK74M,AK105,SR3M,L42A1}.lua
  - jazz/items.lua
  - jazz/docs/tools/*weapon*rollout*
  - jazz/docs/tools/_check_sr3m.py
  - jazz/docs/tools/_check_weapon_imports.py
  - jazz/docs/tools/README.md
  - jazz/docs/specs/active/JAZZ-WEAPON-*.md
  - jazz/docs/technical/weapons/data/*.csv
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/wiki/weapons*
  - jazz/docs/showcase/*/weapons-and-ammo.md
  - jazz/scripts/legion-loadouts/data/weapon_tag_overrides.json
  - jazz-units/items.lua
  - jazz-units/metadata.lua
exclusive_resources:
  - jazz/items.lua
  - jazz-units/items.lua
  - jazz-units/metadata.lua
related_decisions:
  - JAZZ-WEAPON-AK-FAMILY-001
approved_by: project-owner, conversation 2026-09-16
---

# JAZZ-WEAPON-ROLLOUT-001: тестовый баланс и выдача оружия

## Проблема

Новые модели установлены, но прототипы исключены из витрины и отсутствуют в штатных рецептах выдачи. CSV отстаёт от предметов.

## Цели

- Ввести AK74M, AK105, SR3M и L42A1 в кампанию с предварительными ценами и проверенными настройками.

## Non-goals

- Публикация, изменение моделей, принудительная замена оружия уже созданных юнитов, полный ребаланс всего арсенала.

## Требования

- `JAZZ-WEAPON-ROLLOUT-001-REQ-001` — AK105 Damage=27 как AKSU; AK74/AK74M номинальный CyclicRPM=600, AK105=600, AKSU=700, AKM=600, SR3M=900. Ручные затворы сохраняют CyclicRPM=0; этот параметр описывает автоматику, а не практическую скорострельность.
- `JAZZ-WEAPON-ROLLOUT-001-REQ-002` — заменить AK74 на AK74M только в Ivan10, сохранив совместимые компоненты и условия сложности.
- `JAZZ-WEAPON-ROLLOUT-001-REQ-003` — добавить новые образцы в существующие подходящие рецепты Легиона: AK74M/AK105 T3-1, SR3M T3-2, L42A1 T2-1. Синхронизировать CSV и установленные LootDef; не перегенерировать посторонние пулы.
- `JAZZ-WEAPON-ROLLOUT-001-REQ-004` — Bobby in: AK74M BR4/RW45/16000, AK105 BR4/RW40/14500, SR3M BR4/RW20/22000, L42A1 BR2/RW35/10000. MaxStock=1. Mosin остаётся существующим магазинным предметом BR1/RW110/1100; варианты — его компоненты, без новых IDs.
- `JAZZ-WEAPON-ROLLOUT-001-REQ-005` — по отдельному «поправь» владельца 2026-09-16 восстановить только Knife-записи Crusher_Inventory из существующего рецепта: 40/55/70 процентов по трём взаимоисключающим диапазонам прогрессии. Прочий инвентарь не регенерировать.

## Инварианты и ограничения

- Сохранить старый предмет Mosin, PU, M38 и обрез; правила выдачи T1-2 и ранний PU, минимальные веса обреза и отдельный редкий Roughneck не меняются.
- GP и сошки AK105 оставлены по решению пользователя. Модели и текстуры в этой транзакции не меняются.
- Задача «Изучить мод JAZZ» имеет приоритет при пересечении записей; сохранять чужие изменения и проверять исходные байты перед записью.

## Acceptance criteria

- `JAZZ-WEAPON-ROLLOUT-001-AC-001` — static: предметы равны ModItem, CSV содержит новые образцы и актуальные числа, магазинные параметры согласованы.
- `JAZZ-WEAPON-ROLLOUT-001-AC-002` — static: Ivan10 выдаёт AK74M; новые LootDef имеют корректные компоненты, калибры, tier gates и metadata, остальные записи сохранены.
- `JAZZ-WEAPON-ROLLOUT-001-AC-003` — runtime/editor: загрузка предметов и LootDef без ошибок, save/reload; проверка выдачи и магазина.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: существующие классы предметов и LootDef, без новых hooks.
- Saves: новая выдача действует на новые генерации; текущие экземпляры не мигрируют принудительно.
- Network/determinism: штатный генератор loot и магазина.
- Generated data: jazz items/companions; units items/metadata. LootDef не имеет companion.
- Cross-package references: units ссылается на предметы jazz как существующие пулы.
- Rollback/recovery: хешированные резервные копии каждого изменяемого файла.

## План и ownership

- Пакет-владелец: jazz — статы/CSV, jazz-units — выдача.
- Исполнитель: текущая оружейная задача.
- Reviewer: project-owner.
- Declared write set и exclusive resources: frontmatter.

## Решение владельца

- Approved 2026-09-16: «вывери все значения и вставляй в игру ... ак74м в один из пресетов ивана ... остальное в пулы легиона и в бобби рея ... цену ... выстави сам».
- Это решение расширяет прежние прототипные ограничения AK/SR3M/L42 на отсутствие магазина/выдачи.

## Evidence

- `JAZZ-WEAPON-ROLLOUT-001-AC-001`: PASS static — _validate_items_quick.py, _check_weapon_imports.py (27 graphs/58 DDS pairs + SR3M), weapons-docs.mjs build/check (168 weapons), повторный rollout без смысловых изменений.
- `JAZZ-WEAPON-ROLLOUT-001-AC-002`: PASS static — _audit_weapon_rollout.py: сохранены 2276 прежних LootDef; изменены только 29 одобренных (27 firearm pools, Ivan10, Crusher_Inventory), добавлены 23 комбинации. Все старые записи пулов, включая Mosin, сохранены. run_static_tests.py: PASSED, 37/37 recipe contracts.
- `JAZZ-WEAPON-ROLLOUT-001-AC-003`: BLOCKED runtime/editor — DAP подтвердил, что текущие классы ещё имели старые RPM/Cost; guarded reload не отправлен из-за ConnectionRefused (процесс завершился). Следующая штатная загрузка читает новые файлы, но пока не подтверждена. Save/reload round-trip не выполнен.

Проверка источников темпа: [АК74М — Росгвардия](https://rosguard.gov.ru/ru/page/index/avtomat-ak74m) 600; [АК105 — Росгвардия](https://www.rosguard.gov.ru/page/index/avtomat-ak105) 600; [СР3М — Росгвардия](https://rosguard.gov.ru/page/index/malogabaritnyj-avtomat-sr3m-vixr) 900; [АК74 — музей](https://www.moscowarmsmuseum.ru/collections/assault-rifles/ak74) 600–650 и [АКС74У — музей](https://moscowarmsmuseum.ru/collections/assault-rifles/aks74u) 650–700. Для АК74 выбран номинал 600, а не верхняя граница диапазона. Это CyclicRPM; BurstShots/AutoShots остаются 3/6 для AK74/74M/105, 4/7 у AKSU, 4/9 у SR3M. У L42A1/Mosin ручной затвор, RPM=0 означает отсутствие автоматического темпа, одиночный выстрел регулируется ShootAP.

Тестовый баланс: AK105 Damage27/Range40/Aim11/Shot4AP даёт промежуточную роль относительно AKSU 27/38/7/4 и AK74 26/48/12/5. AK74M сохраняет Damage26/Range50/Aim12/Shot5, SR3M — 32/26/10/4, L42A1 — 37/72/14/8 базовых AP (+1 обязательный прицел). Эти числа являются игровым балансом, не физическими измерениями. Цены новых АК выше AK74 8500/AKSU 9000; SR3M 22000 дешевле AS_Val 32000 без его глушителя; L42A1 10000 ниже FRF2 11500 и M24 19250.

Общий generated-sync audit не чист: исходный jazz audit захватил копии companion из tmp/integration-20260916/audit-suite, units сообщил 81 прежнее расхождение. Это не заменяет PASS адресной проверки и не исправлялось массовой перегенерацией.

## Documentation delta

- Адресный CSV, генерация оружейной wiki, technical и showcase RU/EN; результаты сверки темпа и балансное обоснование добавляются после проверки.
