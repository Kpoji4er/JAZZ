---
id: JAZZ-WEAPON-AK103-001
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
  - jazz/docs/tools/_weapon_feedback_*
  - jazz/docs/design/*visual-feedback*
  - jazz/docs/design/references/*feedback*/*
  - jazz/docs/design/references/weapon-feedback-20260928/*
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/.agents/docs/playbooks/model-export-qa-handoff.md
  - jazz/docs/tools/_weapon_feedback_*
  - jazz/docs/design/weapon-visual-feedback-20260927.md
  - jazz/docs/tools/_diagnose_ak103_shading.py
  - jazz/docs/tools/_rebake_ak103_tangent_basis.py
  - jazz/docs/tools/_fit_ak103_donor_cover.py
  - jazz/docs/tools/_restore_ak103_materials.py
  - jazz/docs/tools/_diagnose_ak103_material_uv.py
  - jazz/docs/tools/_compare_weapon_quality_renders.py
  - jazz/docs/tools/_audit_ak103_hidden_geometry.py
  - jazz/docs/tools/_strip_ak103_hidden_geometry.py
  - jazz/docs/tools/_optimize_ak103_mesh.py
  - jazz/docs/tools/_import_ak103_native_maps.py
  - jazz/docs/tools/_check_ak103_native_stage.py
  - jazz/docs/technical/systems/assets-entities.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz_assets/BinAssets/Materials/AKR_AK103*
  - jazz/docs/tools/_audit_compiled_weapon_mesh.py
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/InventoryItem/AK103.lua
  - jazz/WeaponIcons/AK103.png
  - jazz/WeaponComponents/Magazine/AK103_Native30.png
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/tools/_build_ak103_assets.py
  - jazz/docs/tools/_build_ak103_archive.py
  - jazz/docs/tools/_rebake_ak103_archive.py
  - jazz/docs/tools/_lift_ak103_albedo.py
  - jazz/docs/tools/_export_ak103_assets.py
  - jazz/docs/tools/_integrate_ak103.py
  - jazz/docs/tools/_check_ak103.py
  - jazz/docs/tools/_fix_ak103_roughness.py
  - jazz/docs/tools/_audit_weapon_rm_maps.py
  - jazz/docs/tools/_inspect_ak103_frostoise.py
  - jazz/docs/tools/_inspect_ak103_archive.py
  - jazz/docs/tools/_inspect_weapon_source.py
  - jazz/docs/tools/_repair_ak103_export.py
  - jazz/docs/tools/_repair_ak103_visuals.py
  - jazz/docs/tools/_build_weapon_scale_overlay.py
  - jazz/docs/tools/_build_weapon_attachment_fit_scene.py
  - jazz/docs/tools/_render_ak103_icon.py
  - jazz/docs/tools/_compose_icon_review.py
  - jazz/docs/tools/README.md
  - jazz/docs/design/weapons-import-plan-jaweapons.md
  - jazz/docs/specs/active/JAZZ-WEAPON-AK103-001.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/AKR_AK103*
  - jazz_assets/Entities/Meshes/AKR_AK103*
  - jazz_assets/Entities/Materials/AKR_AK103*
  - jazz_assets/Entities/Textures/AKR_AK103*
  - jazz_assets/Entities/Textures/Fallbacks/AKR_AK103*
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - localization IDs 761915304101-761915304103
  - AK103 Blender build state
related_decisions:
  - JAZZ-WEAPON-AK-FAMILY-001
  - JAZZ-WEAPON-ROLLOUT-001
approved_by: project-owner in conversation 2026-09-19
---

# JAZZ-WEAPON-AK103-001: АК-103 из очереди локального архива

## Ремонт normal map и проверка приклада 2026-09-27

Владелец разрешил «делай» после runtime A/B: отключение NormalMap корпуса убирает
пожёванные блики, восстановление карты возвращает их. Дополнение владельца:
«на прикладе с обратной стороны как будто текстура неправильная».
REQ-NORMAL-001: проверить каналы, UV и согласование карт с текущим мешем;
исправлять подтверждённую причину в отдельной сборке с rollback, сохраняя ID,
баланс, spots и геометрию, если её изменение не обосновано диагностикой.
REQ-NORMAL-002: отдельно проверить обе стороны приклада и его исходную UV/PBR-привязку.
REQ-NORMAL-003: владелец уточнил, что родная карта оригинальной крышки — `ksk`.
Проверить исходную крышку model_9 с этим набором и вернуть её вместо временного
донора AK74M при успешной визуальной проверке. Перепечь normal maps из исходного
шейдинга под экспортный меш без custom/split normals; исходные normals только
читать для bake, не переносить custom-слой в экспорт.
AC-NORMAL-001: static — сравнить исходные карты с установленным BC5, зафиксировать
причину и проверку сохранности остальных ресурсов.
AC-NORMAL-002: visual — одинаковые ракурсы normal-on/off/candidate, оба бока и
приклад; отсутствие ложных вмятин при сохранении мелкого рельефа.
AC-NORMAL-003: runtime — проверить исправленный материал в открытом осмотре;
временные пробы восстанавливать, persistent-установку делать с backup и последующей
проверкой после перезапуска модов. Не объявлять диагностику готовым ремонтом.
Исходный A/B: runtime PASS (JA3Debug, evaluate-only); отчёт вне репозитория
`ak103-normal-ab-20260927/report.md`. Общая игровая приёмка остаётся открытой.

### Сборка после проверки 27.09.2026 — установлена, runtime открыт

Внешняя сборка `Weapons/_ak103_rebake_20260927/rebased`: оригинальная крышка
`model_9` с `ksk`, пять перепечённых tangent normal maps; сложенный приклад
использует материал разложенного. Подготовленные geometry/normals/UV до и после
bake совпадают по хешам, target custom normals отсутствуют. Исходные custom normals
читаются только у доноров bake, которые удаляются из экспортной сцены.

Диагностика BC5: XY установленной карты совпадают с исходной в пределах компрессии
(средняя ошибка около 0.72/255, корреляция около 0.995). Переворот каналов не подтверждён.
У совпадающих углов меша исходные и экспортные нормали отличаются: медиана корпуса
около 26°, приклада около 23°. После rebake в одинаковом offline-свете исчезли
ложные волны вокруг углубления на обратной стороне приклада; осмотрены оба бока,
крупные планы и сборка целиком. Runtime-пробы новых файлов с AppData-путями не
считать доказательством загрузки: положительный игровой A/B относится только
к отключению/восстановлению установленной NormalMap.

AssetsProcessor завершился; шесть HGM geometry/winding PASS, максимум отклонения
вершин 0.02590 мм. Stage graph/прежние spots/DDS≤2048/fallback≤64/иконки PASS.
Strict mesh gate всё ещё FAIL: прежняя почти коллинеарная грань корпуса, теперь
face 1964 вместо 1708 донорского варианта; ближайшие вершины отличаются на 0.00203 мм
из-за квантования. Общий normals PASS не заявляется. Generated-sync baseline:
142 errors / 14 warnings; все шесть AK103 ModItemEntity реально присутствуют,
но regex-аудитор пропускает однострочные записи. Общий gate не объявляется пройденным.

После сообщения владельца «игру закрыл» подтверждено отсутствие JA3/JA3Debug,
установлены 58 файлов из проверенного stage и созданы 58 резервных копий в
`rebased/repair-install-backup`. Все установленные файлы совпали со stage по SHA256.
Assets sync до/после: 142 errors / 14 warnings, новых ошибок нет. Во время установки
другой процесс изменил `jazz/items.lua`; установщик туда не пишет, внешняя правка
сохранена. Отчёт: `rebased/installation-verification.json`.
Игра не запускалась; свежая загрузка, оба бока и движущиеся блики ещё не проверены.
Runtime AC-NORMAL-003 и editor round-trip остаются открытыми.

## Осторожная оптимизация 2026-09-26

Владелец разрешил: «попробуй, но очень аккуратно контролируй качества. Пожеванное оружие это reject».
REQ-OPT-001: работать от установленной native-сборки в отдельном внешнем каталоге; сохранить исходник, UV, материалы, scale, pivots/spots и игровые данные. Цель 18–22 тыс. треугольников мягкая: качество важнее числа.
AC-OPT-001 (static): отчёт до/после по частям, двунаправленные расстояния поверхностей и контроль UV; нормали без custom/split, нет вырожденных граней.
AC-OPT-002 (visual offline): одинаковые ракурсы/свет до/после, оба бока, три четверти и крупные планы. Замятые грани, нарушения силуэта и текстур — REJECT; отклонённый вариант не устанавливать.
AC-OPT-003 (static): при принятом offline-варианте сверить compiled HGM с blend, сохранить material/spot-контракт и backup перед заменой при закрытой игре. Runtime остаётся NOT_RUN; игру не запускать.

## Новый архив владельца 2026-09-26

Прямой запрос «давай этот импортнем ак103» разрешает замену визуала существующего AK103
из `Downloads/AK-103 (6П45).zip`. SHA256:
`3a1d87265d73715937a9e9914b24decfa1ca45e743abe005d1498508d5927085`.
Все 13 OBJ совпадают с прежним архивом побайтно; новый архив содержит родные BaseColor,
Roughness, Metallic, Normal и две AO-карты. Использовать оригинальные UV и карты вместо
выпечки Frostoise/временных процедурных материалов. Сохранить шесть entity, pivot/spot-контракт,
длину 0.943 м, баланс, ID и игровые данные. Подготовка в отдельном внешнем build-каталоге
`Weapons/_ak103_native_20260926`; backup перед установкой. Игру не запускать.
Новая static-приёмка требует сравнения декодированного HGM с подготовленным mesh, графа
материалов/DDS, двух вариантов приклада и иконок. Runtime/editor AC остаётся открытым.

## Разрешённое исправление приёмки 2026-09-22

Владелец разрешил исправить все оружейные дефекты, сравнить присланный Izhmash AK-103.zip и самостоятельно выбрать геометрию/материалы. Все 13 OBJ архива побайтно совпали с текущим source; донор сохраняется. Декодированный установленный HGM воспроизводит пропавший ствол/рукоять и полосы над коробкой, которых нет в blend. Требуется уменьшить сложность экспортного меша, проверить уже скомпилированный HGM и обновить материалы при необходимости; исправить optics anchor и отсутствующие ApplyTo ГП25/сошек/40-местного магазина. Все публичные ID и базовые характеристики сохранить, экспорт без custom normals, игра закрыта. Offline не закрывает runtime AC. Это продолжение разрешённого исправления, без commit/push.

## Проблема

Дополнение 27.09.2026: владелец возобновил отложенный визуальный ремонт словами «можнго править». Основание и скриншоты: `docs/design/weapon-visual-feedback-20260927.md`. Устранить пожёванные блики АК-103, диагностировать normal map совместно с экспортными нормалями; сохранить силуэт, UV, spots и обновить иконку.

- `JAZZ-WEAPON-AK103-001-REQ-VISUAL-027`: Устранить пожёванные блики АК-103, диагностировать normal map совместно с экспортными нормалями; сохранить силуэт, UV, spots и обновить иконку. Игровой баланс, публичные ID и регистрация сохраняются; работа только в jazz/jazz_assets, отдельная сборка и backup перед установкой при закрытой игре.
- `JAZZ-WEAPON-AK103-001-AC-VISUAL-027`: static/offline — проверены точечные изменения, карты/меши и сборки, иконки 324×165 RGBA, исходные ресурсы сохранены. Runtime/human — подтверждение владельцем после нового запуска; offline PASS его не заменяет.


В комплекте есть АК-74, АКМ, АК-74М, АК-105 и АКСУ, но нет полноразмерного современного автомата
под 7,62x39. Архив владельца `Weapons/AK/Izhmash AK-103.zip` оказался непригоден: это геометрия,
снятая с недоступной для скачивания Sketchfab-модели «AK-103 (6П45)» (Andruxa-snajper,
uid `1f754cabaedb47b78d2feefe683e580f`) — без лицензии, с тегом `noai` и **без единой текстуры**.

## Цели

- Ввести АК-103 как полноразмерный 7,62x39 между АКМ и АК-74М, на легально пригодной геометрии.
- Сохранить совместимость с существующими магазинами и аттачами АКМ.

## Non-goals

- Ремастер АК-74/АКМ, изменение чужих предметов, выдача в отряды Легиона, публикация.

## Требования

- `JAZZ-WEAPON-AK103-001-REQ-001` — геометрия и родные карты из нового архива владельца
  `AK-103 (6П45).zip`, оригинальные UV. Это заменяет прежнюю выпечку
  с CC-BY «AK 103» (Frostoise). Публичный ID `AK103` не меняется. Bogdanzloy
  и голая установка Frostoise отклонены владельцем как плоский силуэт.
- `JAZZ-WEAPON-AK103-001-REQ-002` — игровая длина равна паспортным 943 мм и не меньше принятого АК.
- `JAZZ-WEAPON-AK103-001-REQ-003` — структура entity повторяет `AKR_AK105`: тело, `_Handguard`,
  `_Magazine`, `_Muzzle`, `_Stock`, `_StockFolded`.
- `JAZZ-WEAPON-AK103-001-REQ-004` — `object_class = AssaultRifle`, `Damage = 29`, `fxClass = "AKM"`,
  набор слотов от АКМ, складной приклад как у АК-74М. Пистолетная рукоять есть, поэтому
  `ModifyRightHandGrip` не ставится, `HolsterSlot = Shoulder`.
- `JAZZ-WEAPON-AK103-001-REQ-005` — иконка 324x165 с тёмной обводкой по геометрии `AK74.png`.
- `JAZZ-WEAPON-AK103-001-REQ-006` — Bobby in: Tier 4, RestockWeight 40, MaxStock 1, Cost 15000,
  CategoryPair AssaultRifles.

## Инварианты и ограничения

- Магазинный интерфейс совпадает с `AKM.ent`, чтобы общие магазины 7,62x39 садились без правок.
- Существующие предметы, ID и спот-контракты других стволов не меняются.
- Чужой незакоммиченный dirty state (в частности `InventoryItem/Mosin.lua` от 02:53 2026-09-19)
  не исправляется в рамках этой задачи.

## Acceptance criteria

- `JAZZ-WEAPON-AK103-001-AC-001` — static: длина 0.943 м, оверлей с AK74M/AK74 в отчёте.
- `JAZZ-WEAPON-AK103-001-AC-002` — static: Lua компилируется, ModItem равен companion, все entity
  разрешаются в mesh/material/DDS/fallback, пять visual bindings на месте, иконка соответствует AK74.
- `JAZZ-WEAPON-AK103-001-AC-003` — static: посадка ГП-30/ГП-45/сошек/ПСО/Кобры/НСПУ проверена на
  реальной декодированной геометрии по нашим спотам.
- `JAZZ-WEAPON-AK103-001-AC-004` — runtime/editor: предмет грузится, виден в инвентаре, руках и на
  земле; приклад складывается; стрельба, перезарядка и save/reload работают.
- `JAZZ-WEAPON-AK103-001-AC-005` — локализация RU/EN присутствует в каталоге.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: штатный `AssaultRifle`, без новых hooks.
- Saves: новый предмет; существующие экземпляры не меняются.
- Generated data: два пакета, одна транзакция; backup в `<build>/integration-backup`.
- Rollback: удалить добавленные записи AK103 и 44 новых файла, вернуть четыре core-файла из backup.

## План и ownership

- Пакет-владелец: `jazz_assets` — геометрия; `jazz` — предмет, визуалы, иконка, локализация.
- Declared write set и exclusive resources: frontmatter.

## Решение владельца

- Approved 2026-09-19 в текущем разговоре: очередь из `weaponslist.txt`, первым АК-103; далее
  «ак103 это assault rifle», «можешь даже 29 урона сделать», «fx class от акм видимо целиком»,
  выбор гибридного источника после отказа исходного архива, «вид ок», «импорти».
- 2026-09-19: после установки «ак103 ужасная получилась» (шероховатость 0.70–0.77) и затем
  «мне кажется там моделька не очень». Владелец выбрал пересборку геометрии из Frostoise;
  публичный ID `AK103`, баланс и слоты не меняются.
- 2026-09-20: «ак103 все еще плоский» + «самый первый вариант из архива модели был сильно лучше,
  но там надо текстуры восстановить». Геометрия архива, карты — выпечка с Frostoise.

## Evidence

Повторная визуальная правка 27.09.2026 по команде «можнго править»: `JAZZ-WEAPON-AK103-001-AC-VISUAL-027` — PASS static/offline: явные жёсткие стыки 40°, родной normal atlas с strength 0.5; 18999 треугольников вместо 19000. Единственная удалённая микрогрань схлопывалась после квантования (площадь исходника 0.02447 мм²); остальные позиции/UV сохранены. Compiled geometry/winding/strict normals PASS; оба бока и новая иконка проверены. BLOCKED runtime/editor/human. Сборка `jazz_weapon_feedback_20260927`: `compiled-report.json`, `components/component-report.json`, `install-manifest.json`, `installation.json`. В общей транзакции установлены 21 существующий файл, backup и SHA256 проверены; изменения jazz/jazz_assets незакоммичены. Допускается только удаление измеренных микрограней, которые становятся вырожденными в HGM; это не оптимизация видимой геометрии. Подробности — `docs/design/weapon-visual-feedback-20260927.md`.


### Примерка крышки АК-74М разрешена 27.09.2026

Установлен `fit-v3` при закрытой игре. AC-COVER-003: шесть HGM round-trip + winding PASS, body max 0.02612 мм, stage graph/DDS/fallback/spots и две иконки PASS; 58 файлов, stale=0, backup `fit-v3/repair-install-backup`. Lua/ModItem/компоненты и structural checks PASS. Strict compiled normals остаётся PARTIAL: единственная прежняя малая грань сменила индекс 1794→1708, но её три координаты в HGM точно совпали; новых проблем нет. Generated-sync до/после одинаков: 142 blocking / 14 warnings. Runtime/editor/human acceptance NOT_RUN, игра не запускалась.

Владелец: «можно крышку от ак74м поставить если она будет адекватно выглядеть». REQ-COVER-002: извлечь крышку из существующего AK74M вместе с её родными UV/PBR; подогнать только крышку к AK103, без изменения остальных частей, игровых данных и spots. Работать в отдельной сборке, сохранить установленную реконструкцию как rollback. AC-COVER-002 (offline): осмотреть оба бока, верх, стыки и окно затвора при одинаковом свете; неверная посадка, сильное растяжение или потеря вида — reject без установки. AC-COVER-003 (static): подготовка normals, сравнение compiled HGM, graph/DDS/spots и backup при закрытой игре перед установкой. Игру не запускать; human/runtime acceptance остаётся открытой.

AC-COVER-002: offline PASS для `Weapons/_ak103_cover74_20260927/fit-v3`. Донор AK74M, component 1, 827 triangles вместо 416; корпус 19411, сборка 33925 (+411 / +1.23%). Масштаб XYZ: 1.08128 / 0.98678 / 0.98963; передняя левая кромка опущена до 8 мм с плавным переходом, чтобы закрыть щель над коробкой. Base gain 0.65 под более тёмный AK103; родные normal/roughness/metallic и потёртости сохранены, roughness floor 0.44. UV-crop занимает свободный блок 2×2 ячеек body-атласа, один материал. Поверхность/UV остальных 18584 граней корпуса точно совпадают; геометрия пяти отдельных модулей неизменна. `prepare_export_mesh` донора и итогового корпуса: 0 issues. Проверены оба бока, receiver, quarter, top, folded; trial с неверной ориентацией и v2 со щелью не устанавливались. Runtime NOT_RUN.

### Реконструкция установлена 27.09.2026 — runtime NOT_RUN

Сборка `Weapons/_ak103_material_20260927/rebuilt`, инструмент `_restore_ak103_materials.py`. Крышка (component 11, 416 triangles) перенесена в свободный tile (2,1) body-атласа. Краска взята из plain receiver patch (225,443)-(405,482) на 1024px preview, контраст фактуры ослаблен до 6%; tangent normal нейтральная, исходный bake отсутствует. Первый вариант с растянутыми полосами отвергнут до установки. Roughness floor: 0.44 для металла/цевья, 0.52 магазин/приклад, 0.56 крышка; остальные Base/Normal сохранены.

Проверки: geometry + corner normal SHA256 совпали для всех шести частей; 33514 triangles с одним прикладом; семь clay before/after пар дают нулевую разницу, alpha не менялась во всех 14 парах. PBR крупный план, оба бока, верх и folded осмотрены. AssetsProcessor завершён `Done`; шесть HGM round-trip PASS, spots совпадают, stage graph/DDS/fallback и иконки PASS. Strict decoded normals: прежняя очень малая face 1794 корпуса даёт `zero-length normal`, повторено на native HGM; compiled vertices/faces до/после точно совпадают. Не объявлять strict normals или общую приёмку PASS.

Установка `--replace-assets --apply`: 58 файлов, 6 entity, 16 текстур, stale=0; backup в `rebuilt/repair-install-backup`. Lua/ModItem/компоненты и structural items/metadata PASS. Общий generated-sync assets имеет 142 blocking / 14 warnings; прежний suite debt не исправлялся. Игра не запускалась, runtime/editor save-reload и human acceptance остаются открытыми. Реконструкция материала не равна восстановлению отсутствующего авторского MTL.

### Ручное восстановление материалов разрешено 27.09.2026

У владельца нет иных исходников. На предложение восстановить материал крышки вручную под её UV, используя подходящие участки родных текстур, и отдельно исправить блеск получено «угу». Это разрешение на реконструкцию, а не заявление об исходной авторской привязке. Сохранить все 33514 треугольников, координаты, нормали меша, spots, ID и баланс. Крышке выделить собственный участок атласа и перенести только её UV; родные карты остальных частей сохранить с ограниченной настройкой roughness. Проверки: одинаковые PBR-ракурсы до/после, отсутствие чужих деталей на крышке, неизменные геометрия/нормали/slots, компиляция и проверка HGM; backup перед установкой при закрытой игре. Runtime остаётся NOT_RUN до приёмки владельцем.

### Выполненная правка папки редактора 2026-09-27

Владелец указал, что АК-103 находится вне папки остальных штурмовых винтовок. Перенести существующий ModItem в `Items / Weapons / JAZZ - Firearm - Rifles-Assault`, рядом с AK74M; Group исправить с `JAZZ - Firearm - Rifles-AK` на `JAZZ - Firearm - Rifles-AR`. Public ID, runtime companion, игровые свойства и metadata не менять: это исправление дерева и editor-only Group. Исправить также исходный importer, который добавлял предмет в корень.

Выполнено после завершения JA3/JA3Debug: перенесён один существующий блок AK103 рядом с AK74M, изменён только Group; companion/metadata и игровые свойства прежние. Backup: `Weapons/_ak103_material_20260927/editor-folder-backup/items.lua`. Quick structural validator и `_check_ak103.py` — PASS, editor round-trip — NOT_RUN. Importer исправлен аналогично. Native builder теперь отклоняет неуказанный verified `--cover-prefix`; материалы существующего предмета не заменялись.

### Материалы отклонены владельцем 2026-09-27

Скриншот `codex-clipboard-43f78b18-2afe-4ac8-83c4-b066425f6f3f.png`: чрезмерный блеск и чужой рисунок на крышке. Предыдущие offline-проверки НЕ являются приёмкой материалов. AC-004 visual human: FAIL для показанного вида.

Подтверждено: `model_9.obj` — крышка; при native-импорте ей без подтверждённого material mapping назначено `Weapon_AK-103`, как и `model_0`. Изолированный рендер крышки, UV-overlay и baseline PBR показывают несовпадение рисунка с UV крышки. В архиве нет отдельных текстур крышки и файлов `.mtl`, на которые ссылаются OBJ. Восстановление корректной исходной привязки требует дополнительных исходных данных; слепое назначение корпуса крышке — REJECT. Вариант flip-V для всех деталей также REJECT: ломает правильные участки приклада/магазина/цевья.

Roughness/metallic в исходных TGA не перепутаны (R/B), средние совпадают с исходными PNG; это НЕ объясняет и НЕ закрывает избыточный блеск в JA3. BC5 normal DDS содержит XY; нулевой B при декодировании не означает испорченную normal map. Общие средние atlas DDS включают расширение цвета в незанятые области и не должны использоваться как измерение материала на оружии.

Диагностика: `Weapons/_ak103_material_20260927/` (UV-overlay, изолированная крышка, 28 before/flip-V PNG, decoded DDS). На момент диагностики работают JA3/JA3Debug; активные ресурсы не менялись, игра агентом не запускалась. Геометрия остаётся восстановленной 33514 тр., runtime-исправление не заявлено.

### Оптимизация отменена владельцем 26.09.2026 — текущее состояние

Прямое решение «я б вернул как было тогда» выполнено: при закрытой игре восстановлены оба HGM из `strip2/install-backup`, их полные SHA256 сверены с `preinstall-hashes.json`. Все 58 ресурсов (включая обе иконки) побайтно совпали с `Weapons/_ak103_native_20260926/mod-assets-stage` и native PNG. Текущее число треугольников снова **33514** на сборку с одним прикладом. Родные материалы/текстуры, spots, баланс и игровые ID сохранены. Оптимизированные HGM сохранены отдельно в `strip2/reverted-optimized-backup`; пробные инструменты и отчёты оставлены для истории. Игра не запускалась. Запись об установке strip2 ниже — историческая, она отменена этим решением.

### Внутренняя оптимизация установлена 2026-09-26 — strip2

- Общий sync-gate assets до/после побайтно одинаков: 142 blocking / 15 warnings. Новых ошибок не добавлено; полный gate не считается пройденным.

- AC-OPT-001: PASS static. Все шесть entity проверены изолированно (192 направления, до 7 точек на грань). Дубли треугольников не найдены. Удалены 2078 тр. корпуса и 175 тр. цевья; сборка 33514 → 31261 (−6.72%, один приклад). В том числе 13 полностью скрытых островов корпуса, 902 тр. Запас двух колец граней защищает внешний вид. Retained positions/UV exact; visible corner normals max 0°. Strip1 REJECT: часть нормалей после recalc переворачивалась.
- AC-OPT-002: PASS offline. 140 пар сравнений: 14 обзорных PBR/clay + 126 sweep по всем отдельным деталям и трём сборкам (обычная, сложенный приклад, без магазина). Пиксельный анализ всех пар: alpha-delta >16/255 — 0 пикселей; RGB-delta >8/255 максимум 10 пикселей в обзоре, 6 в sweep. Выборочный визуальный осмотр общего вида и крупных планов не показал новых деформаций. Это не human/runtime acceptance.
- AC-OPT-003: PASS static install. Оба compiled HGM декодированы и сверены с blend: 16922/7311 тр., ошибка ≤0.0262 мм. Оригинальные .ent сохранены после проверки bounds/refs/spots (компилятор опускал некоторые identity rotations). Игра закрыта перед заменой; backup `Weapons/_ak103_opt_20260926/strip2/install-backup`. Hash-проверка: изменились только два HGM; материалы, DDS, .ent, Lua и другие части прежние. `_check_ak103.py`, quick structure jazz+assets — PASS. Runtime/editor — NOT_RUN.
- Полный внешний отчёт: `Weapons/_ak103_opt_20260926/installed-optimization-report.md`, исходные маски/числа: `all-parts/all-parts-audit.json`, `strip2/strip-report.json`, сравнения изображений `review/pixel-diff.json` и `sweep/pixel-diff.json`. Цель 18–22 тыс. остаётся мягкой и не достигнута ради сохранения качества.

### Разрешение на внутреннюю оптимизацию 2026-09-26

Владелец: «проверь все ... внутри куча деталей», затем «и попробуй оптимизировать сразу». В scope AC-OPT-001/002/003 добавлена проверка всех шести независимых entity, целых внутренних островов, совпадающих треугольников и закрытых стенок. Создавать отдельный кандидат без decimate и перемещения оставшихся вершин/UV. Съёмные модули не могут служить единственной преградой для удаляемых граней. Проверять исходные и очищенные сборки/отдельные модули с одинаковыми камерой и светом; после offline PASS компилировать, сверять HGM и устанавливать с backup при закрытой игре. Runtime не запускать, его AC остаётся открытым.

### Read-only аудит внутренней геометрии 2026-09-26

По вопросу владельца о внутренних деталях выполнен `_audit_ak103_interior.py`; внешний отчёт `Weapons/_ak103_opt_20260926/interior/interior-audit.json` и шесть диагностических рендеров. В установленной геометрии есть `Bolt_group` (1238 тр.): центры 1102 тр. не видны по 96 пробным направлениям в собранном оружии. `ksk` (3551 тр.) содержит как внутренние, так и видимые наружные элементы (спуск/скоба/шомпол/крепёж); удалять группу целиком нельзя. Выделенные рендеры подтверждают геометрию затворной группы со штоком под оболочкой, но часть группы видна снаружи. Это кандидаты для отдельной проверки, не разрешённый объём удаления: проверка всех поверхностей/состояний модулей, анимации и теней не выполнена. Ресурсы не менялись.

### Осторожная оптимизация 2026-09-26 — варианты REJECT, исходник сохранён

- Решения и до/после: внешний `Weapons/_ak103_opt_20260926/quality-review.md`, `decisions.json`; воспроизводимый `_optimize_ak103_mesh.py` сохранён в tools.
- AC-OPT-001: FAIL для planar (нулевая нормаль приклада). Collapse-варианты прошли гейт нормалей и выборочные расстояния, однако это не визуальная приёмка. Полная количественная UV-приёмка остановлена после visual FAIL.
- AC-OPT-002: FAIL / REJECT. Weighted collapse: 33030 тр. (−1.44%), отклонение цевья до 2.273 мм. Unweighted 80% корпуса/цевья: 28215 тр. (−15.81%), меняются блики и мелкие грани корпуса/газовой трубки. Только цевьё 50%: 29770 тр. (−11.17%), заметно меняются округлости и блики крупным планом. Парные PBR/clay рендеры (семь ракурсов) сохранены; визуально подтверждённых дефектов достаточно для REJECT, остальные ракурсы не объявлены принятыми.
- AC-OPT-003: BLOCKED by visual REJECT — компиляция и установка проб не выполнялись. В моде остаётся native-сборка 33514 тр.; прежние ресурсы сверены побайтно со staging. Новых материалов, иконок, регистраций, игровых данных и runtime-действий нет.
- Цель 18–22 тыс. не достигнута. Текущие technical/wiki/showcase остаются верными: установленный визуал не менялся. Это результат испытаний, не обещание невозможности ручной ретопологии.

### Новый архив, 2026-09-26 — установлен, игровая приёмка ожидается

- Native source SHA256 и совпадение всех 13 OBJ проверены. Build: `Weapons/_ak103_native_20260926`.
- Native UV перепакованы в атласы без проекционной выпечки с чужого оружия. Прямой экспорт нескольких материалов успешно компилировался, но не читался текущим HGM reader; финальный экспорт использует один материал на entity.
- `JAZZ-WEAPON-AK103-001-AC-001`: PASS static — 0.943 м, AK74M 0.9418 м; `scale/scale-overlay.json`, side/top PNG.
- `JAZZ-WEAPON-AK103-001-AC-002`: PASS static для установленной сборки — все шесть HGM декодированы и совпадают с подготовленной геометрией; максимум ошибки вершин 0.0262 мм. Корпус 19000 тр., 57000 corners. `compiled-body-audit.json` и пять `AKR_AK103_*-audit.json`; native staged graph, DDS/fallback headers и иконки проверены `_check_ak103_native_stage.py`.
- `JAZZ-WEAPON-AK103-001-AC-003`: PASS static для сохранения контракта spots — staged `.ent` имеет те же attach attributes, что установленный; 18 новых fit PNG созданы, характерный GP30/оптика вид осмотрен. Это не runtime-acceptance.
- После команды владельца «ставь» и проверки отсутствия JA3/JA3Debug выполнен `--replace-assets --apply`: 58 файлов, шесть entity, 16 DDS + fallback, обе иконки. Прежние ресурсы сохранены в `Weapons/_ak103_native_20260926/repair-install-backup`. Все 58 установленных файлов побайтово совпадают с проверенной сборкой. `_check_ak103.py` — PASS; игровые ID, баланс и регистрации не менялись.
- Общий исходный sync assets: 142 blocking / 14 warnings; среди них ложные отсутствия AK103 ModItem при наличии шести inline-записей в `items.lua`. Эти записи и metadata не менялись. Quick validate jazz и recalc-only normals — PASS.
- Общий sync после установки: те же 142 blocking, 15 warnings вместо 14. Новое предупреждение — шесть заменённых Entity companion новее `items.lua`; это ожидаемый результат обновления ресурсов без правки регистрации, editor round-trip ещё не выполнен. Общий gate не считается пройденным.
- `JAZZ-WEAPON-AK103-001-AC-004`: NOT_RUN — новая сборка установлена, игровая приёмка не выполнена; игру по просьбе владельца не запускали.
- Technical, wiki и showcase RU/EN обновлены по установленному состоянию с явной отметкой об отсутствии игровой приёмки.

### Историческая приёмка предыдущих сборок

- `AC-001`: PASS static — `_build_weapon_scale_overlay.py` после архивной геометрии: AK103 0.943 м,
  AK74M 0.942 м, AK74 0.847 м.
- `AC-002`: PASS static — `_check_ak103.py` после `--replace-assets`: ModItem не менялся, шесть entity
  с mesh/material/DDS/fallback, 15 текстур, иконка 324x165 с тёмной обводкой.
- `AC-003`: PASS static — `_build_weapon_attachment_fit_scene.py`: 18 кадров, семь конфигураций.
  Это проверка геометрии, не игровых привязок.
- Geometry remaster 2026-09-20: архивный меш (Andruxa OBJ, ~75k тр. после drop exploded),
  PBR выпечен с Frostoise (EMIT selected-to-active). Body 60444 тр.
- `AC-004`: BLOCKED — запуск JA3 не выполнялся.
- `AC-005`: BLOCKED — `T()` с русским литералом уже в companion, строки собраны в
  `<build>/mod-data-stage/texts.json`, но строки в `Russian.csv`/`English.csv` ещё не экспортированы,
  поэтому английская локаль пока покажет русское имя.

Общий `_check_weapon_imports.py` не проходит по прежней причине: в рабочей копии у `Mosin` удалён
`CanAppearInShop` правкой от 02:53 2026-09-19, вне этой задачи. Это не исправлялось и не маскировалось.

## Documentation delta

- `docs/tools/README.md` и `docs/design/weapons-import-plan-jaweapons.md` обновлены.
- Профильная technical-страница, wiki и showcase RU/EN отражают установку native-ресурсов 26.09.2026; игровая приёмка и ранее открытая локализация остаются отдельными незавершёнными проверками.

Исправление 2026-09-22 установлено: 6 entity, Base/Norm/RM, иконки, 3 missing ApplyTo. Body HGM: 19327 треугольников, расхождение центров <0.03 мм; старый HGM эту проверку не проходит. Quick validate jazz+assets PASS; runtime NOT_RUN.

## Повторная игровая приёмка 2026-09-28

Решение владельца: approved; «дальше делай, вроде пока все».

- `JAZZ-WEAPON-AK103-001-REQ-VISUAL-028` — Устранить оставшееся жёваное освещение АК-103 по новому игровому скриншоту. Проверять геометрическое сглаживание и tangent-space отдельно; сохранить UV, силуэт и детали.
- `JAZZ-WEAPON-AK103-001-AC-VISUAL-028` — адресные static/compiled проверки и сопоставление до/после; игровая приёмка и editor save/reload отдельно.

Evidence: `JAZZ-WEAPON-AK103-001-AC-VISUAL-028`: `BLOCKED` — изменения ещё готовятся; runtime не подтверждён.

Установка 28.09.2026: 19 файлов в jazz/jazz_assets, SHA256 исходников/backup/установленных файлов проверены. PASS static/compiled: angle 20°, 18999 треугольников, исходные позиции/UV сохранены, custom normals нет. Сравнительный рендер коробки заметно ровнее. Иконка переснята. Полная сводка и ссылки — `docs/design/weapon-visual-feedback-20260927.md`. `AC-VISUAL-028`: static PASS; editor/runtime/human BLOCKED до новой приёмки владельца.


## Повторная приёмка 28.09.2026, второй проход

Решение владельца: после сбора замечаний и паузы команда «делай» разрешает реализацию сохранённого списка, без commit/push. Пауза снята.

- `JAZZ-WEAPON-AK103-001-REQ-FEEDBACK-028B` — Исправить только магазин АК-103: корпус принят владельцем и больше не меняется.
- `JAZZ-WEAPON-AK103-001-AC-FEEDBACK-028B` — static/compiled: корректный граф ресурсов и отсутствие регрессий; offline: сравнение до/после; runtime/human: повторить показанный владельцем сценарий.

Evidence `JAZZ-WEAPON-AK103-001-AC-FEEDBACK-028B`: BLOCKED — реализация и повторная приёмка в работе. Установка только после подготовки кандидатов, проверок и закрытия игры. Новые рабочие скрипты `_weapon_feedback_*`, материалы приёмки и исходные write sets входят в этот проход.


Второй проход 28.09: [отчёт staging и открытых пунктов](../../design/weapon-visual-feedback-20260928-round2.md). Проверенные кандидаты подготовлены отдельно; установка/runtime/editor NOT_RUN. Статус approved сохранён. HAV и 6Б3 не приняты по эксперименту с весами и исключены из транзакции.

28.09.2026, после «игра закрыта, применяй»: проверенный пакет второго прохода установлен, 27 файлов и backup SHA256 PASS; installed graph/structural PASS. Новых generated ERROR нет; общий baseline остаётся FAILED. HAV/6Б3 исключены из установки, runtime/editor/human остаются NOT_RUN. По последующему запросу разрешены локальные коммиты; push не разрешён.
