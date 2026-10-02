---
id: JAZZ-WEAPON-MOSIN-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
  - jazz_assets
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/tools/_weapon_feedback_*
  - jazz/docs/design/*visual-feedback*
  - jazz/docs/design/references/*feedback*/*
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/InventoryItem/JAZZ_MosinModular.lua
  - jazz/InventoryItem/Mosin.lua
  - jazz/scripts/legion-loadouts/data/early_variants.json
  - jazz/scripts/legion-loadouts/data/weapon_tag_overrides.json
  - jazz/scripts/legion-loadouts/data/recipes.json
  - jazz/scripts/legion-loadouts/generate.py
  - jazz/docs/technical/weapons/data/weapon-component-options.csv
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz/Code/Weapon_MosinModular.lua
  - jazz/WeaponIcons/MOSIN*.png
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/tools/*rifle*
  - jazz/docs/tools/*mosin*
  - jazz/docs/tools/*l42a1*
  - jazz/docs/tools/_runtime_weapon_imports.lua
  - jazz/.agents/docs/playbooks/assets-and-ui.md
  - jazz/.agents/docs/playbooks/units-squads.md
  - jazz/docs/tools/README.md
  - jazz/scripts/legion-loadouts/run_static_tests.py
  - jazz/docs/tools/_gen_legion_weapon_availability_map.py
  - jazz/docs/design/legion-weapon-availability-by-tier.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-units.md
  - jazz/docs/showcase/en/legion-units.md
  - jazz/docs/design/weapons-import-queue.md
  - jazz/docs/specs/active/JAZZ-WEAPON-MOSIN-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/MOSIN*
  - jazz_assets/Entities/Meshes/MOSIN*
  - jazz_assets/Entities/Materials/MOSIN*
  - jazz_assets/Entities/Textures/MOSIN*
  - jazz_assets/Entities/Textures/Fallbacks/MOSIN*
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - MOSIN localization IDs and Blender build
related_decisions:
  - none
approved_by: project-owner in conversation 2026-09-15
---

# JAZZ-WEAPON-MOSIN-001: Мосинка с тремя вариантами длины

## Классы конфигураций, 03.10.2026

Решение владельца в текущей беседе: М38 и обрез получают класс и способности боевой винтовки; длинная Mosin остаётся снайперской. Scope approved. Владелец реализации — jazz; текущий write set: `Code/Weapon_MosinModular.lua`, `docs/tools/_check_mosin_configurations.py`, `docs/tools/README.md`, эта spec и профильные weapons-and-ammo technical/wiki/showcase RU+EN. Generated data, public item ID, модели и выдача не меняются; exclusive resources этой итерации — none.

- `JAZZ-WEAPON-MOSIN-001-REQ-011` — при смене Barrel обратимо менять WeaponType, object_class, эффективное ancestry экземпляра, ImpactForce и AvailableAttacks. M38/Obrez: BattleRifle, SingleShot + JAZZ_Salvo; 1891: SniperRifle / Sniper, SingleShot + JAZZ_JokerShot + JAZZ_Bullseye. Не менять общую таблицу Mosin и другие экземпляры. Сохранить ID Mosin, состояние, патроны и численный баланс конфигураций.
- `JAZZ-WEAPON-MOSIN-001-AC-012` — static/offline Lua: прямые и обратные переходы восстанавливают класс/атаки/ImpactForce; два экземпляра независимы; прежние проверки характеристик и блокировки ПУ проходят.
- `JAZZ-WEAPON-MOSIN-001-AC-013` — runtime: native IsKindOf, hotbar/tooltip и save/load отражают выбранную конфигурацию. Проверка отдельно от offline Lua; без игрового evidence не объявлять PASS.

Совместимость: тот же экземпляр и публичный ID, профиль восстанавливается при установке компонентов и обновлении визуального объекта. Общая spec остаётся approved, пока прежние и новые runtime/human AC не закрыты.

## Проблема

Исходные OBJ и текстуры есть в локальном архиве Weapons/Sniper; MTL отсутствуют, экспорт и предмет пока отсутствуют.

## Цели

- Подготовить рабочую сборку и добавить тестовый предмет непосредственно в JAZZ.

## Non-goals

- Публикация, изменение тиров Легиона, изменение остальных семейств оружия.

## Требования

- `JAZZ-WEAPON-MOSIN-001-REQ-001` — Существующий предмет Mosin (уточнение владельца заменяет отдельный тестовый JAZZ_MosinModular) с вариантами 1891, M38 и Obrez. Согласованные ствол и ложа каждого варианта; единый патрон 7.62x54R, базовые урон/крит от калибра с поправками на вариант. Звуки от Mosin. Сохранить публичный ID Mosin, прежний магазин/тир/доступность; отдельный тестовый ModItem убрать.
- `JAZZ-WEAPON-MOSIN-001-REQ-002` — сохранить исходники; экспортировать отдельные entities с attachment spots, согласовать ModItem, metadata, companion и локализацию.
- `JAZZ-WEAPON-MOSIN-001-REQ-003` — иконка из Blender, направление слева направо, прозрачный фон и обводка.
- `JAZZ-WEAPON-MOSIN-001-REQ-004` — уточнение владельца: Obrez является уникальным вариантом слота Barrel, одновременно изображающим короткий ствол и отсутствие полноценного приклада. Отдельную покупку/установку приклада для него не требовать. Снизить стоимость выстрела в AP, улучшить ближнюю стрельбу без прицеливания, существенно ухудшить прицельную стрельбу и дальность. Урон/крит остаются производными от 7.62x54R с поправкой на конфигурацию.
- `JAZZ-WEAPON-MOSIN-001-REQ-005` — уточнение владельца 2026-09-15: объединить старую и новую мосинки, сохранить прежний ПУ и предпочитаемый вид материалов. Длинная конфигурация использует существующие mesh/material Mosin через MOSIN_1891; M38 и Obrez сохраняют новые модели. Вернуть необязательный Scope/JAZZ_Scope_PU и точки крепления; исправить точки удержания. Исходную новую геометрию 1891 сохранить в build для дальнейшей работы.

- `JAZZ-WEAPON-MOSIN-001-REQ-006` — уточнение владельца: оставить старый item Mosin, убрать отдельный тестовый item; новые конфигурации раздать Легиону через существующий генератор и подходящие слоты. длинная Mosin — только sniper для выдачи; M38 — battle/rifle, как MAS36; Obrez — carbine/smg (в том числе Marauder), без pistol-тега; Obrez весит 100 на T1 и 10 на T2, ниже остальных ПП/карабинов; у Roughneck ещё ниже: 10 на T1 и 1 на T2; без смены класса оружия на автоматический ПП. Сохранить существующие тиры и границы прогрессии; по явному решению владельца обычная винтовка/M38/Obrez используют старый порог T1-2 (12), остаточное оружие T2 (20–29); снайперская PU сохраняет прежний ранний допуск. Каталожный тир самого предмета не меняется.

## Инварианты и ограничения

- Уточнение владельца 2026-09-16: ПУ только на длинной снайперской конфигурации JAZZ_Mosin1891. M38/Obrez блокируют Scope через штатный BlockSlots, как блокировка Muzzle у APS. При установленном ПУ интерфейс требует сначала снять его, затем сменить ствол; при прямой установке короткого ствола штатный setter очищает заблокированный слот. ПУ не переносится на короткие варианты.

- Чужие изменения сохранять. Общие файлы не записывать при пересечении с задачей «Изучить мод JAZZ»; при прерывании дождаться освобождения ресурса.
- Существующий Mosin сохраняет прежние CanAppearInShop, Tier, RestockWeight и стоимость.
- Рабочие копии хранятся отдельно в Weapons/_mosin_jazz_build.

## Acceptance criteria

- `JAZZ-WEAPON-MOSIN-001-AC-001` — static: материалы восстановлены, геометрия и точки крепления согласованы; исходники сохранены.
- `JAZZ-WEAPON-MOSIN-001-AC-002` — static: Lua и ссылки проходят проверки; RU/EN, иконка и граф ресурсов присутствуют.
- `JAZZ-WEAPON-MOSIN-001-AC-003` — editor/runtime: загрузка, предмет в руках/на земле, смена доступных компонентов, выстрел/перезарядка со звуком и save/reload без ошибок.
- `JAZZ-WEAPON-MOSIN-001-AC-004` — static/runtime: выбор Obrez в Barrel одновременно меняет ствол и ложу; по сравнению с длинным вариантом выстрел дешевле, ближний профиль без aim лучше, максимальный aim и дальность хуже. Обратная смена возвращает исходные параметры без накопления модификаторов.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: штатные числовые эффекты компонентов; методы только Mosin выбирают цельную визуальную конфигурацию по Barrel и размер Long/Carbine/Compact. Глобальные классы не оборачиваются. Разные исходные ложи и ствольные коробки не подменяются искусственной общей невидимой геометрией.
- Saves: публичный ID Mosin сохраняется; старый экземпляр без Barrel получает длинную визуальную конфигурацию по умолчанию. Промежуточный тестовый JAZZ_MosinModular удаляется из каталога по указанию владельца.
- Network/determinism: штатные данные компонентов.
- Generated data: items + metadata + companions.
- Cross-package references: jazz -> jazz_assets через существующую зависимость.
- Rollback/recovery: удалить только новые записи и ресурсы; исходные ZIP/OBJ сохранены.

## План и ownership

- Пакет-владелец: jazz — предмет и компоненты; jazz_assets — геометрия и текстуры.
- Исполнитель: текущая оружейная задача.
- Reviewer: владелец проекта.
- Declared write set: frontmatter.
- Exclusive resources: frontmatter; перед записью перепроверить параллельную задачу.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец поручил L42A1 с собственным прицелом, затем «продолжай работу, в том числе над мосинками».
- Дата: 2026-09-15.

## Evidence

- Уточнение ПУ 2026-09-16: static PASS — реальные JAZZ setter и vanilla `GetComponentBlocksAnyOfAttachedSlots`/`GetNumModifySlotOptions` в Lupa: смена на короткий ствол требует снятия ПУ в UI, Scope недоступен на M38/Obrez, снова доступен на длинной конфигурации; прямой setter очищает заблокированный слот. Визуальный smoke обновлён под новые AP 7/5 без ПУ у коротких конфигураций, но не запускался в новом runtime. Metadata/companion без delta, меняются только два WeaponComponent в items.lua.
- Восстановление 2026-09-20: три `ModItemWeaponComponent` пропали из грязного `items.lua` (оружие и metadata их ещё перечисляли) — слот Barrel в кабинете пустел. Вернул HEAD-определения `JAZZ_Mosin1891` / `JAZZ_MosinM38` / `JAZZ_MosinObrez` перед `JAZZ_BarrelsDefs`; у коротких снова `BlockSlots = { "Scope" }`. Static PASS: `_check_mosin_configurations.py --game-root` — 7 переходов setter и штатный UI-блок ПУ. Runtime после перезагрузки мода.

- `JAZZ-WEAPON-MOSIN-001-AC-001`: `BLOCKED` — подготовка геометрии продолжается.
- `JAZZ-WEAPON-MOSIN-001-AC-002`: `BLOCKED` — интеграция ещё не выполнена.
- `JAZZ-WEAPON-MOSIN-001-AC-003`: `BLOCKED` — требуется игровая проверка.
- `JAZZ-WEAPON-MOSIN-001-AC-004`: `BLOCKED` — конфигурации ещё не подключены.

## Documentation delta

- После интеграции обновить профильные страницы; непроверенное игровое поведение отмечать явно.

### Исправление W11, 2026-09-22

По разрешению владельца восстановлены отсутствовавшие определения трёх Barrel-компонентов; M38/Obrez снова блокируют Scope. Существующий Mosin:SetWeaponComponent также отклоняет Scope на короткой конфигурации, включая slot=nil/is_init. Проверены оба порядка PU/короткий ствол, снятие, возврат длинного и семь переходов характеристик настоящим JAZZ setter. Это offline проверка, не игровая приёмка. CanAppearInShop и общий generated baseline не менялись.


## Уточнение ремонта 2026-09-26

Владелец разрешил исправление подтверждённых находок («правь», «да»). W01: сместить IK-точку левой руки обреза на 70 мм назад от установленного положения, чтобы пальцы не выходили перед дульным срезом. Геометрию и игровые характеристики не менять. Это корректировка существующего требования хвата. Проверка точки и сохранности остальных ресурсов — static; визуальная приёмка после запуска владельцем — BLOCKED.

Evidence 2026-09-26: PASS static — изменён только Hand_l_grip в существующем .ent; восстановление старой строки даёт побайтное совпадение с backup. Mesh/material/registration не менялись. Runtime BLOCKED до повторной проверки владельцем.


## Визуальная корректировка 2026-09-27

Решение владельца в текущей беседе: сблизить дерево M38 с полноразмерной винтовкой; «короткая» уточнена как обрез без приклада. Scope approved: существующая BaseColor-текстура M38 и её fallback, Hand_l_grip обреза, документация. Полноразмерная винтовка — эталон, её ресурсы не изменяются.

- `JAZZ-WEAPON-MOSIN-001-REQ-007` — приглушить красно-рыжее дерево M38 до коричневого тона длинной Mosin, сохранить UV и металлические детали. Сместить левую руку обреза на 30 мм вперёд (X 5 → 8), сохранив остальные точки и геометрию.
- `JAZZ-WEAPON-MOSIN-001-AC-005` — static: DDS и fallback читаются, размеры/формат/полная mip-цепочка сохранены; ссылки материала прежние; единственная delta entity — X точки Hand_l_grip обреза.
- `JAZZ-WEAPON-MOSIN-001-AC-006` — human/runtime: дерево M38 близко длинной винтовке; руки обреза разделены, пальцы не выходят за дульный срез. До осмотра в игре BLOCKED.

Baseline: игра/редактор закрыты. Generated sync jazz_assets до изменений: 142 ошибки, 13 предупреждений, включая прежнее отсутствие ModItemEntity MOSIN_* при наличии metadata/companion. Это существующий блокер полного editor round-trip; регистрации в текущем визуальном scope не меняются.


### Evidence визуальной корректировки 2026-09-27

Владелец явно разрешил точную Python-цветокоррекцию после проверки imagegen-кандидата: генератор слегка перерисовал детали и его output не установлен. Установлена коррекция исходных BC1 color endpoints, без замены UV и без генеративной перерисовки.

- `JAZZ-WEAPON-MOSIN-001-AC-005`: PASS static — основная DDS 2048×2048 / 12 mips, fallback 64×64 / 7 mips, DXGI 72, headers и размеры файлов сохранены. Нейтральные блоки 184266 / 144 побайтно прежние. Изменён только цвет дерева; entity отличается от pre-task backup только Hand_l_grip X=5→8. Полноразмерная модель, mesh/material, normal/AO/RM и регистрации прежние.
- `JAZZ-WEAPON-MOSIN-001-AC-006`: BLOCKED human/runtime — игра не запускалась; требуется осмотр M38 рядом с длинной винтовкой и хвата обреза в idle/aim/fire/reload. Общая spec остаётся approved: старые runtime AC и generated baseline не закрыты этим визуальным ремонтом.

Изменения записаны в technical, wiki и showcase RU/EN как локальная правка с непроверенным игровым видом. Скрипт и восстановительные копии сохранены; публикация не выполнялась.

### Повторная коррекция дерева, 2026-09-27

Владелец показал три конфигурации и сообщил, что тон дерева всё ещё различается. Это разрешение продолжить визуальное исправление M38 и Obrez; длинная винтовка остаётся эталоном. Вопрос о сравнении с MAS36 — аудит, без изменения баланса. Прежнее разрешение точной Python-коррекции DDS сохраняется.

- `JAZZ-WEAPON-MOSIN-001-REQ-008` — согласовать светлоту и оттенок деревянных участков M38 и Obrez с материалом длинной винтовки. Разделять дерево и металл по существующим RM-картам; учитывать linear/sRGB и диффузную долю эталонного материала. Сохранить текстурные детали, UV, mip-цепочки и fallback. Write set этой итерации: MOSIN_7_Base.dds, MOSIN_11_Base.dds и их Fallbacks, инструмент и связанные документы из frontmatter. RM, геометрию, хват, регистрации и игровые числа не менять.
- `JAZZ-WEAPON-MOSIN-001-AC-007` — static: четыре DDS читаются, заголовки/формат/mips прежние; блоки вне маски дерева побайтно прежние; повторный запуск не накапливает коррекцию. Полноразмерная модель и карты RM прежние.
- `JAZZ-WEAPON-MOSIN-001-AC-008` — human/runtime: три конфигурации под одинаковым светом имеют близкий тон дерева. BLOCKED до повторного осмотра в игре; скриншоты владельца показывают, что предыдущая итерация AC-006 не прошла по тону M38.

Evidence повторной итерации: AC-007 PASS static — изменены ровно четыре Base DDS среди 48 проверенных MOSIN-ресурсов; 2048×2048/12 mips и fallback 64×64/7 mips, BC1 sRGB и заголовки прежние. Блоки вне маски побайтно прежние: M38 185791/83, Obrez 298764/266 (основная/fallback). Повторный `--apply` дал идентичные SHA256. Preview просмотрены, backup/report сохранены в локальном `tmp/mosin-wood-match/`. RM/normal/AO/mesh/entity/material и эталонная длинная винтовка побайтно прежние. Документационный local gate PASS (4 страницы). AC-008 BLOCKED human/runtime: игра не запускалась, полного совпадения BRDF не заявляем. Общая spec остаётся approved из-за незакрытой игровой приёмки.

Баланс проверен без правок: `_check_mosin_configurations.py --build tmp --game-root <JA3_ROOT>` PASS — семь переходов настоящего setter, обратимость AP/урона/крита/прицеливания/дальности/массы и штатный UI-блок ПУ. Длинная: 40 урона / 66 дальность / 13 AimAccuracy / 8 ОД / масса 55; M38: 38/52/11/7/34; обрез: 32/24/4/5/18. MAS36 companion: 38/57/11/8/36. MAS36 и Mosin зарегистрированы в metadata; боевой баланс этой итерацией не меняется.

- `JAZZ-WEAPON-MOSIN-001-AC-007`: PASS static — DDS/headers/mips, защищённые блоки, ресурсный diff и идемпотентность проверены выше.
- `JAZZ-WEAPON-MOSIN-001-AC-008`: BLOCKED human/runtime — повторного осмотра нет.

Общий Done gate не пройден: исторические AC-001–004/006 и текущая игровая приёмка остаются незакрытыми; status approved сохранён. Локальные проверки этой итерации не заменяют общий DoD.

## Пороги выдачи, уточнение владельца 2026-09-27

Прямое указание владельца заменяет прежние пороги REQ-006 и исключение раннего ПУ: обрез — ПП/карабин с T1-1, далее реже; M38 — battle/rifle вместе с MAS36 с T1-1; длинная — sniper с T1-3, включая ПУ. Каталожный tier и характеристики предмета не меняются. Игра закрыта владельцем.

- `JAZZ-WEAPON-MOSIN-001-REQ-009` — применять пороги 11/11/13 в генераторе и действующих Legion LootDef. Сохранить остаточные диапазоны 20–29 и веса: Obrez 100→10, Roughneck 10→1; M38 101000→1400. Удалить дубли и безусловные Mosin fallback, обходящие диапазоны. Именные инвентари наёмников и награды не являются прогрессией Легиона и остаются прежними.
- `JAZZ-WEAPON-MOSIN-001-AC-009` — static: реальные Lua LootDef и план генератора совпадают по конфигурациям, тегам, min/max и весам; нет безусловных Mosin в Legion class pools; обрез редеет на T2 и отсутствует на T3. Legacy Legion-ссылки на длинную Mosin также не открываются до 13.
- `JAZZ-WEAPON-MOSIN-001-AC-010` — editor/runtime: save/reload и выдача новых экземпляров по границам 11/12/13/20/30. До игрового прогона BLOCKED.

Транзакция: source JSON/generate.py в jazz, существующие ModItemLootDef в jazz-units/items.lua. LootDef не имеют отдельного companion; существующие ID сохраняются, metadata только проверяется. Применение точечное, посторонние изменения generated-блоков сохраняются. Baseline generated-sync jazz-units: 81 ошибка, 0 предупреждений (прежние отсутствующие ModItem UnitData).

- `JAZZ-WEAPON-MOSIN-001-AC-009`: PASS static — 33 пула исправлены точечно; 68 фактических generated Mosin-записей проверены по порогам 11/13, диапазону 20–29 и весам. Нет безусловных Mosin. Legacy RifleBolt/RifleSniper также gate=13. `_retier_mosin_loot.py --check`, полный `run_static_tests.py`, generator dry-run 37/37 и `_validate_items_quick.py ../jazz-units` PASS; повторное применение без delta. Немосинские записи сохраняются поблочным Counter; замена Mosin fallback — единственное добавление немосинской записи. Source role tags прежние. Существующий отсутствующий Ranger_CQB не создавался.
- `JAZZ-WEAPON-MOSIN-001-AC-010`: BLOCKED editor/runtime — игра закрыта, round-trip и выдача в игре не выполнялись. После правки sync остаётся 81 ошибка/0 предупреждений, как baseline; локальная правка не закрывает общий DoD и не готова к релизной приёмке.

### Частота M38 внутри T1, 2026-09-27

Владелец попросил M38 реже на T1-1 и чаще на T1-2. Утверждённое уточнение REQ-009: на Amount=11 вес 20000 (примерно пятая часть прежнего), на 12–19 — прежние 101000; остаточная выдача 20–29 сохраняет 1400. Это относительные веса, не абсолютная вероятность. ID combo, категории и остальные варианты прежние.

- `JAZZ-WEAPON-MOSIN-001-REQ-010` — source variant поддерживает ступени веса внутри своего диапазона, генератор создаёт непересекающиеся условия 11–11 и 12–19 для одного существующего M38 combo.
- `JAZZ-WEAPON-MOSIN-001-AC-011` — static: во всех пулах с M38 ровно одна активная запись на границах 11/12/19/20/29, веса 20000/101000/101000/1400/1400; на 10/30 записей нет. Точечное применение и повторный запуск не меняют другие LootEntry. Runtime остаётся непроверенным (AC-010).

- `JAZZ-WEAPON-MOSIN-001-AC-011`: PASS static — 7 существующих пулов изменены, границы 10/11/12/19/20/29/30 проверены по установленным Lua-записям: одна активная запись внутри диапазонов, вне диапазонов нет. Полный static suite, structural gate и точечный check/idempotence PASS. Metadata и ID прежние; runtime не выполнялся.


## Повторная приёмка 28.09.2026, второй проход

Решение владельца: после сбора замечаний и паузы команда «делай» разрешает реализацию сохранённого списка, без commit/push. Пауза снята.

- `JAZZ-WEAPON-MOSIN-001-REQ-FEEDBACK-028B` — Проверить хват обреза по новому скриншоту. Менять отображаемое имя по конфигурации без замены экземпляра; патроны, состояние, модификации сохраняются, обратное переключение возвращает имя.
- `JAZZ-WEAPON-MOSIN-001-AC-FEEDBACK-028B` — static/compiled: корректный граф ресурсов и отсутствие регрессий; offline: сравнение до/после; runtime/human: повторить показанный владельцем сценарий.

Evidence `JAZZ-WEAPON-MOSIN-001-AC-FEEDBACK-028B`: BLOCKED — реализация и повторная приёмка в работе. Установка только после подготовки кандидатов, проверок и закрытия игры. Новые рабочие скрипты `_weapon_feedback_*`, материалы приёмки и исходные write sets входят в этот проход.


Второй проход 28.09: [отчёт staging и открытых пунктов](../../design/weapon-visual-feedback-20260928-round2.md). Проверенные кандидаты подготовлены отдельно; установка/runtime/editor NOT_RUN. Статус approved сохранён. HAV и 6Б3 не приняты по эксперименту с весами и исключены из транзакции.

28.09.2026, после «игра закрыта, применяй»: проверенный пакет второго прохода установлен, 27 файлов и backup SHA256 PASS; installed graph/structural PASS. Новых generated ERROR нет; общий baseline остаётся FAILED. HAV/6Б3 исключены из установки, runtime/editor/human остаются NOT_RUN. По последующему запросу разрешены локальные коммиты; push не разрешён.

03.10.2026 evidence: AC-012 PASS static/offline Lua — реальный JAZZ setter, семь переходов и прежние характеристики/ПУ; классы, ancestry data, ImpactForce, атаки, изоляция экземпляров и Setcomponents восстановлены. AC-013 BLOCKED runtime — DAP 8165 не слушает; native IsKindOf, hotbar/tooltip и полное save/load не проверены. Реализация итерации завершена; общий status approved сохраняется из-за незакрытых runtime/human AC.
