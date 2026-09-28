---
id: JAZZ-WEAPON-SR3M-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
  - jazz_assets
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/InventoryItem/SR3M.lua
  - jazz/WeaponIcons/SR3M.png
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/tools/*sr3m*
  - jazz/docs/tools/_apply_weapon_geometry_update.py
  - jazz/docs/tools/_render_weapon_icons.py
  - jazz/docs/tools/_finalize_weapon_icons.py
  - jazz/docs/tools/README.md
  - jazz/docs/specs/active/JAZZ-WEAPON-SR3M-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/SR3M*
  - jazz_assets/Entities/Meshes/SR3M*
  - jazz_assets/Entities/Materials/SR3M*
  - jazz_assets/Entities/Textures/SR3M*
  - jazz_assets/Entities/Textures/Fallbacks/SR3M*
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - localization SR3M strings
  - SR3M Blender export state
related_decisions:
  - none
approved_by: project-owner in conversation 2026-09-15
---

# JAZZ-WEAPON-SR3M-001: СР-3М из исходной Blender-сцены

## Проблема

В Weapons/SMG/SR_3M/SR_3M.blend есть 10 mesh-объектов и пять упакованных текстур. Игровые SR3M entities не найдены. Нет spots, у Barrel нет материала. Подготовленные UMP45 и AS_Val служат локальными образцами структуры.

## Цели

- Собрать СР-3М и добавить его непосредственно в JAZZ по образцу существующего оружия.

## Non-goals

- Отдельный мод отменён владельцем. Массовая обработка оружейного архива, публикация и изменение отрядов не входят в задачу.

## Требования

- `JAZZ-WEAPON-SR3M-001-REQ-001` — исходник сохраняется; новая сборка получает отдельные корпус, магазин, приклад и дульный модуль с согласованными spots.
- `JAZZ-WEAPON-SR3M-001-REQ-002` — предмет SR3M — предварительно SubmachineGun Т3, JAZZ_Caliber_9x39; компоненты подключаются штатными WeaponComponentVisual. Без интегрированного глушителя. Тестовый под-тир 3-2, Compact, SMG attacks; FX от AK74. Последнее уточнение владельца оставляет выбор ПП/карабин за игровыми потребностями: класс ПП — проверяемая гипотеза, а не окончательное утверждение.
- `JAZZ-WEAPON-SR3M-001-REQ-003` — items, metadata, companions и ресурсы синхронны; название и описание RU/EN, иконка из модели.
- `JAZZ-WEAPON-SR3M-001-REQ-004` — обвес садится только на верхнюю RIS. У штатной крышки ресивера планки нет, поэтому в `clean` добавляется низкополигональная Picatinny на гребни крышки, и корпус переэкспортируется. Слот `Scope` — `CanBeEmpty`, без `DefaultComponent`, чтобы модельные целик и мушка оставались видны; состав ограничен оптикой, которая садится на планку без утопания и без свеса больше пары сантиметров. Слот `Side` — `CanBeEmpty`, девайс сидит на собственной боковой Picatinny-площадке цевья, а не на коробке. Боковой кронштейн и «ласточкин хвост» запрещены: `JAZZ_Scope_PSO`, `JAZZ_CombatScope_1P29`, `JAZZ_NightScope_NSPU`, `JAZZ_Reflex_Cobra`, `JAZZ_Reflex_PKAS` и любой `AKSeriaMount` в слоты не входят. Новые `WeaponComponentVisual ApplyTo="SR3M"` не пишутся: перечисленные компоненты уже несут дефолтный визуал на spot `Scope` / `Side`, как на прочих Picatinny-хостах вроде M4A1.
- `JAZZ-WEAPON-SR3M-001-REQ-006` — у сгенерированной планки нормали направлены наружу, что проверяется знаковым объёмом замкнутой поверхности, а не обмоткой граней на глаз. UV планки берутся проекцией по ближайшей точке крышки ресивера, чтобы она наследовала настоящие normal, roughness и AO и совпадала по материалу с крышкой; режим одного текселя остаётся доступен как `--rail-uv flat`.
- `JAZZ-WEAPON-SR3M-001-REQ-005` — слот `Muzzle` снимается с `Modifiable = false` и сохраняет `JAZZ_DefMuzzle` как `DefaultComponent`. Глушителя 9А-91 в комплекте нет, и он не выдумывается. Когда компонент глушителя 9А-91 появится, его добавляют в `AvailableComponents` слота `Muzzle` вместе с `WeaponComponentVisual ApplyTo="SR3M"`; до этого слот остаётся с одним компонентом, и `_check_sr3m.py` это утверждение охраняет.

## Инварианты и ограничения

- Исходные .blend и чужой dirty state сохраняются. Existing IDs и зависимости пакетов не меняются.
- Первоначальное ограничение Bobby out / без автоматической выдачи заменено одобренным вводом 2026-09-16 в JAZZ-WEAPON-ROLLOUT-001.
- Базовые числа берутся относительно AS_Val, с явным обычным шумом без глушителя. Это первый тестовый баланс.

## Acceptance criteria

- `JAZZ-WEAPON-SR3M-001-AC-001` — static: исходник сохранён, новая сцена и экспорт содержат все выбранные детали, текстуры и attachment spots; модульная сборка геометрически совпадает.
- `JAZZ-WEAPON-SR3M-001-AC-002` — static: все runtime-ссылки разрешаются, generated sync и Lua validation проходят для добавленных данных.
- `JAZZ-WEAPON-SR3M-001-AC-003` — editor/runtime: save/reload сохраняет предмет; модель видна в инвентаре, руках и на земле; магазин и приклад не пропадают; стрельба и перезарядка работают.
- `JAZZ-WEAPON-SR3M-001-AC-004` — static: у entity `SR3M` есть spots `Scope` и `Side`; `Scope` лежит на верхней плоскости планки по линии ствола, `Side` смещён вбок на площадку цевья и имеет поворот вокруг канала ствола. Каждый компонент обоих слотов разрешается либо адресным `ApplyTo="SR3M"`, либо своим дефолтным визуалом, и целится в существующий spot. Ни одной dovetail-оптики в слотах нет. `Muzzle` модифицируем и содержит ровно один компонент.
- `JAZZ-WEAPON-SR3M-001-AC-005` — human: на CPU-рендерах видно, что коллиматор и боевой прицел сидят на планке зубьями в пазах, а не утопают в крышке и не висят; side-девайс стоит на площадке цевья, а не на коробке слева.
- `JAZZ-WEAPON-SR3M-001-AC-006` — runtime: в игре прицел из слота `Scope` появляется над планкой, side-девайс — на цевье, штатные целик и мушка видны при пустом слоте `Scope`, поворот `Side` даёт девайс сбоку, а не поперёк.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: существующая модель SubmachineGun без новых hooks. Для теста выбран ближний штурм в движении с RunAndGun и JAZZ_Zipper; альтернативный Carbine предполагает роль ближняя–средняя дистанция, RunAndGun_Carbine и JAZZ_TargetSweep. Выбор сверяется с docs/technical/weapons/class-roles.md.
- Saves: новый предмет, существующие экземпляры не изменяются.
- Network/determinism: штатные presets и components.
- Generated data: два пакета, полная транзакция.
- Cross-package references: jazz -> jazz_assets по существующей зависимости.
- Rollback/recovery: убрать только добавленные SR3M записи и файлы; исходники сохранены.

## План и ownership

- Пакет-владелец: jazz_assets — геометрия; jazz — предмет и визуалы компонентов.
- Исполнитель: текущая задача Codex.
- Reviewer: владелец проекта, визуальная приёмка.
- Declared write set: перечислен в frontmatter; Blender-рабочая копия в отдельном каталоге Weapons/_sr3m_jazz_build вне канонических репозиториев.
- Exclusive resources: перечислены в frontmatter.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец в текущем разговоре: «давай сразу по образу и подобию в игору втсорем» после выбора СР-3М.
- Дата: 2026-09-15.

## Evidence

- `JAZZ-WEAPON-SR3M-001-AC-001`: частично проверено — отдельная Blender-сборка экспортирована официальным AssetsProcessor; шесть entities, пять привязок визуалов, четыре пары DDS/fallback. Исходник сохранён. Компилятор завершился успешно, но сообщил о двух нулевых нормалях корпуса; вид в игровом renderer ещё не принят.
- `JAZZ-WEAPON-SR3M-001-AC-002`: `PASS` для добавленных данных — python docs/tools/_check_sr3m.py: равенство ModItem/companion, Lua, ссылки entities/materials/textures, spots и RU/EN. Общая проверка пакетов имеет прежние ошибки; глобальный generated sync не объявляется пройденным.
- `JAZZ-WEAPON-SR3M-001-AC-003`: `BLOCKED` — успешный editor/runtime тест пока отсутствует; руки, земля, звук, стрельба, перезарядка и save/reload требуют проверки.
- `JAZZ-WEAPON-SR3M-001-AC-004`: `PASS` static — `python docs/tools/_check_sr3m.py`: шесть слотов, пять адресных и десять унаследованных привязок визуалов, spots `Scope` (6.0, 0, 10.95) и `Side` (25.6, 3.736, 7.61) с поворотом, запрет dovetail-оптики, `Muzzle` модифицируем с одним компонентом. Верхняя RIS добавлена в `clean`: 20 пазов, шаг 9.9 мм, ширина 21.2 мм, +252 треугольника к корпусу (5911 → 6163); bounding box entity не изменился, так как планка ниже блока целика.
- `JAZZ-WEAPON-SR3M-001-AC-005`: `PASS` human — `docs/tools/_build_sr3m_attachment_fit_scene.py`, рендеры в `Weapons/_sr3m_jazz_build/attach_renders`. Зазоры: Eotech и M68 без свеса, прикус −1.3 и −0.3 мм; ACOG свес назад 1.1 см; 2x свес назад 2.3 см, прикус 1.4 мм; Reflex_Closed прикус 0.8 мм. Отклонены: Aimpoint5000 (интегральный кронштейн утопает на 14.1 мм), NightScope (свес 3.6/4.0 см), Scope_Scout (свес 5.3/6.4 см). Реальная декодированная HGM-геометрия была доступна для Eotech, 2x и side-девайсов; остальные посчитаны по `box` из `.ent`.
- `JAZZ-WEAPON-SR3M-001-AC-006`: `BLOCKED` — в игре не проверялось. Под наибольшим сомнением ориентация `Side`: поворот задан как `-1,0,0,90` и подтверждён только эмуляцией в Blender, а не движком.
- `JAZZ-WEAPON-SR3M-001-REQ-006`: `PASS` static, после отчёта владельца из игры 2026-09-19. Первая версия планки была намотана внутрь: все шесть граней каждого из 20 зубьев и базовой плиты имели нормаль внутрь, в Blender-превью это маскировалось трёхсторонним светом, а игровой рендерер показал сразу. Исправлено `bmesh.ops.recalc_face_normals` плюс утверждение о положительном знаковом объёме; проверка от общего центра для набора отдельных зубьев даёт ложные срабатывания и не используется. UV переведены на проекцию с крышки: базовый цвет и прежде совпадал со средним по крышке (0.22 против 0.235), но один константный тексель лишал планку детали normal и roughness, и она читалась светлее и площе. После проекции планка совпадает по материалу. Остаточный артефакт: планка подхватывает нарисованные рёбра крышки как светлые полосы, что вблизи читается как износ; откат — `--rail-uv flat`. Меш переустановлен трижды, актуальный `SR3M_Mesh.m.hgm` — `540318677f5f`.

Тестовый профиль: урон 32, дальность 26, магазин 30, выстрел 4 AP, перезарядка 5 AP, отдача 20, очереди 4/9, темп 900. Усиленный патрон компенсируется короткой дистанцией и отдачей; превосходство над другими ПП ещё не проверено в бою.

## Documentation delta

- После реализации: профильная technical-страница, file coverage и краткое описание тестового предмета RU/EN; непроверенный runtime помечается явно.
