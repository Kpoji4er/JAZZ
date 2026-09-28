---
id: JAZZ-WEAPON-VZ58-001
status: implemented
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz_assets
  - jazz-units
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/design/references/weapon-feedback-20260928/*
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/.agents/docs/playbooks/model-export-qa-handoff.md
  - jazz/docs/tools/_weapon_feedback_*
  - jazz/docs/design/weapon-visual-feedback-20260927.md
  - jazz/.agents/docs/playbooks/mesh-export-normals.md
  - jazz/InventoryItem/VZ58.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/WeaponIcons/VZ58.png
  - jazz/docs/tools/*vz58*
  - jazz/docs/tools/*r4*
  - jazz/docs/tools/*weapon*
  - jazz_assets/Entities/Textures/JAZZ_VektorR4*
  - jazz_assets/Entities/Meshes/JAZZ_VektorR4*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_VektorR4*
  - jazz/docs/tools/README.md
  - jazz/docs/specs/active/JAZZ-WEAPON-VZ58-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/technical/weapons/data/weapons.csv
  - jazz/docs/wiki/weapons/*
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz_assets/Entities/JAZZ_VZ58*
  - jazz_assets/Entities/Meshes/JAZZ_VZ58*
  - jazz_assets/Entities/Materials/JAZZ_VZ58*
  - jazz_assets/Entities/Textures/JAZZ_VZ58*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_VZ58*
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz-units/items.lua
  - jazz-units/metadata.lua
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - localization VZ58
related_decisions:
  - none
approved_by: project-owner current conversation 2026-09-26
---

# JAZZ-WEAPON-VZ58-001: классическая база и современный обвес

## Проблема

Дополнение 27.09.2026: владелец возобновил отложенный визуальный ремонт словами «можнго править». Основание и скриншоты: `docs/design/weapon-visual-feedback-20260927.md`. Исправить плохой вид металла коробки и магазина Vz.58, сохранить дерево. Обновить иконку по исправленным материалам.

- `JAZZ-WEAPON-VZ58-001-REQ-VISUAL-027`: Исправить плохой вид металла коробки и магазина Vz.58, сохранить дерево. Обновить иконку по исправленным материалам. Игровой баланс, публичные ID и регистрация сохраняются; работа только в jazz/jazz_assets, отдельная сборка и backup перед установкой при закрытой игре.
- `JAZZ-WEAPON-VZ58-001-AC-VISUAL-027`: static/offline — проверены точечные изменения, карты/меши и сборки, иконки 324×165 RGBA, исходные ресурсы сохранены. Runtime/human — подтверждение владельцем после нового запуска; offline PASS его не заменяет.


Владелец предоставил VZ.58P_VZ.58V.zip и VZ.58 (Modernized).zip и разрешил добавление: классическая модель как база, детали Modernized как сменные компоненты.

## Цели

- Один VZ58 с классической базовой конфигурацией и видимыми взаимозаменяемыми компонентами из обоих архивов.
- Начальный баланс Tier 2-2: лёгкая альтернатива АК под существующий 7.62x39, 30 патронов, 800 RPM.

## Non-goals

- Новая механика стрельбы, новый калибр, массовая регенерация, публикация, штык как отдельное оружие.

## Требования

- `JAZZ-WEAPON-VZ58-001-REQ-001`: сохранить исходники, восстановить родные UV/PBR, выделить одну классическую сборку без демонстрационных дублей, нормали пересчитать без custom normals. Масштаб классической сборки 0.845 м, общая система координат компонентов.
- `JAZZ-WEAPON-VZ58-001-REQ-002`: штатный фиксированный приклад; альтернативные штатный металлический и современный скелетный приклады; штатные/современные цевьё и пистолетная рукоять; родной магазин 30 и вариант с петлёй; родные глушитель, передняя рукоять, коллиматор. Штатное цевьё блокирует Scope/Under. Использовать существующие эффекты компонентов и новый частный компонент лишь для локальной блокировки слотов.
- `JAZZ-WEAPON-VZ58-001-REQ-003`: Damage 27, ShootAP 5000, ReloadAP 6000, Recoil 23, Reliability 85, WeaponMass 29, RPM 800, BurstShots 4, AutoShots 8, Range 38, BDR 14, Grouping 60, AimAccuracy 10. Bobby in: Tier 2, RW 55, MaxStock 2, Cost 6000, AssaultRifles. Обычные пулы Легиона от T2-2 через существующий генератор; без редких/уникальных пулов. Это стартовый баланс для плейтеста.
- `JAZZ-WEAPON-VZ58-001-REQ-004`: синхронная регистрация предмета, визуалов, сущностей, иконки, RU/EN, каталога оружия и документации.

## Инварианты и ограничения

- Существующие оружие и компоненты меняются только добавлением ApplyTo=VZ58. Чужой dirty state сохраняется. Игра/редактор должны быть закрыты для ручной транзакции.
- Обвес не запечён в базовый меш; магазин не становится совместимым с АК по геометрии только из-за общего эффекта quick-mag.

- `JAZZ-WEAPON-VZ58-001-REQ-005`: по запросу владельца «сделай складывание сразу» добавить сложенный визуал штатного приклада VZ.58V, пару JAZZ_StockLightUnFolded/JAZZ_StockLightFolded и штатные FoldStock/UnFoldStock. Новых действий, локализации и runtime hooks нет.

## Acceptance criteria

- `JAZZ-WEAPON-VZ58-001-AC-001`: static — базовая и современная сборки экспортируются, карты/UV/нормали/стыки проверены, демонстрационные дубли отсутствуют.
- `JAZZ-WEAPON-VZ58-001-AC-002`: static — items/metadata/companion согласованы, все варианты имеют свои визуалы, зависимости соблюдаются, RU/EN завершены, Bobby/loot и docs согласованы.
- `JAZZ-WEAPON-VZ58-001-AC-003`: editor/runtime — save/reload и проверка оружия в руках, модификаций, стрельбы и магазина.

- `JAZZ-WEAPON-VZ58-001-AC-004`: static/offline — оба состояния имеют визуалы, штатные действия переключают пару, проверены disabled/hidden состояния и сложенная геометрия.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: используем действующие AssaultRifle, WeaponComponentVisual и BlockSlots без нового runtime hook.
- Saves: добавление IDs; существующие экземпляры не мигрируются.
- Network/determinism: общий штатный контракт, новых случайных вызовов нет.
- Generated data: items.lua, metadata.lua и InventoryItem/Entities companions одной транзакцией.
- Cross-package references: jazz -> jazz_assets; jazz-units -> VZ58.
- Rollback/recovery: ограниченные резервные копии затронутых файлов в build, незакоммиченное изменение.

## План и ownership

- Пакет-владелец: jazz — предмет/компоненты/docs; jazz_assets — бинарные модели; jazz-units — пулы.
- Исполнитель: основной агент.
- Reviewer: статический аудит; human/editor acceptance остаётся владельцу.
- Declared write set: перечислен в front matter.
- Exclusive resources: перечислены в front matter.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner, сообщения «основа первый, модификации второго» и «добавляй» с двумя архивами.
- Дата: 2026-09-26. Повторное подтверждение не требуется.

## Evidence

Повторная визуальная правка 27.09.2026 по команде «можнго править»: `JAZZ-WEAPON-VZ58-001-AC-VISUAL-027` — PASS static/offline: стыки 40° у корпуса и магазина, 9640/4254 треугольника без изменения поверхности/UV, compiled geometry/winding/strict normals PASS. Текстуры Vz.58 сохранены: подтверждённая коррекция касается сглаживания геометрии. Иконка обновлена. BLOCKED runtime/editor/human. Сборка `jazz_weapon_feedback_20260927`: `compiled-report.json`, `components/component-report.json`, `install-manifest.json`, `installation.json`. В общей транзакции установлены 21 существующий файл, backup и SHA256 проверены; изменения jazz/jazz_assets незакоммичены. Допускается только удаление измеренных микрограней, которые становятся вырожденными в HGM; это не оптимизация видимой геометрии. Подробности — `docs/design/weapon-visual-feedback-20260927.md`.


- `JAZZ-WEAPON-VZ58-001-AC-001`: `PASS` — static/offline visual: 14 сущностей, native UV/PBR, recalc-only normals; классическая, V и Modernized сборки осмотрены. Все HGM v14 совпадают с Blender по числу граней и поверхности, максимальная погрешность вершины 0.026 мм. Для приклада V восстановлен нейтральный gunmetal при отсутствующем albedo; единственная scalar-карта использована как AO.
- `JAZZ-WEAPON-VZ58-001-AC-002`: `PASS` — static: `_check_vz58.py`, Lua-компиляция всех шести core-файлов, items/companion equality, 160 допустимых сочетаний, 14 entity/resource graphs, 3 новых RU/EN ID, 8 loot pools, Legion static suite, weapons-docs build/check и scoped docs check. Ввод предмета additive; дополнение складывания заменяет доступный StockLight штатной парой в слоте Stock.
- `JAZZ-WEAPON-VZ58-001-AC-003`: `BLOCKED` — editor/runtime не выполнялись; нет save/reload, подтверждения материалов/хвата/анимаций/звука/стрельбы в игре. Не считать релизно принятым.

## Documentation delta

- weapons-ammo-components, file-coverage, weapons.csv/generated wiki, showcase RU/EN, README инструментов.

### Источники и диагностические ограничения

- `VZ.58P_VZ.58V.zip` SHA256 `cd71a2ffdf02aa4841fb3ee73b95833ae17dab8cc26151d8cf10a97484cb4e3c`; исходник не изменён.
- `VZ.58 (Modernized).zip` SHA256 `570583ec8d08c1e6f96d6e80910b395b4e788bbe3ddb18c5fb4372e6839ef1a0`; исходник не изменён.
- Полный sync-аудит имеет прежние проблемы: jazz 6241 errors / 1635 warnings; assets 142 / 13. Они не исправлялись этим вводом; scoped VZ58 gate проходит.
- Канонический общий localization audit: active IDs 15357, staged catalog 12120, needs-Russian 101, needs-English 17, active collisions 11, Game collisions 606 — существующий общий долг. Для трёх VZ58 ID оба языка заполнены, collisions отсутствуют; экспорт выполнен штатным экспортёром из одного снимка, прежние runtime CSV строки сохранены.
- Локальные build-report/compiled-audit/validation-report/loot-report и резервные копии находятся в рабочем build `_vz58_jazz_20260926`; абсолютный путь игры в tracked-файлы не добавлен.
- Три пакета изменены локально и не закоммичены. Независимое human review и игровой AC остаются открытыми.

- Финальный sync: jazz 6241/1635, assets 142/13, units 81/0; VZ58-specific errors отсутствуют. DoD validator ожидаемо не проходит из-за AC-003 BLOCKED, статус implemented не означает accepted.

- Дополнение владельца: складывание штатного приклада разрешено текущим сообщением.
- `JAZZ-WEAPON-VZ58-001-AC-004`: `PASS` — `_check_vz58_folding.py`: реальные Lua FoldStock/UnFoldStock и HUD переключают пару, стоимость 4000, нехватка AP disabled, фиксированные приклады hidden, folded скрыт в кабинете. Сложенный HGM совпадает с Blender (1422 треугольника); осмотрен рендер, крепление неподвижно, 475 вершин подвижной части повёрнуты на 180°. Новый визуал использует карты разложенного приклада. Доказательства и бэкапы в `_vz58_fold_20260926`. Игровую анимацию и списание AP проверка не имитирует.

## Коррекция экспорта 27.09.2026

Запрос владельца: исправить исчезающие поверхности (скриншоты VZ58/R4), сделать материал мебели VZ58 спокойнее, проверить открытую игру. Прежняя offline проверка AC-001 не обнаруживала неверную сторону граней: её вывод о визуальной корректности не распространялся на backface culling.

- Исправлены совпадающие UV-швы и пересчёт наружу; открытым островам оставлена авторская сторона. Нет custom normals, изменения количества треугольников или position/UV пар.
- `PASS` offline: `_check_weapon_surface_uv.py`, донорский winding audit (расхождение менее 0.1% площади с учётом мелких ошибок самого OBJ), HGM surface + winding audit, native Blender previews. У VZ58 обновлены две atlas BaseColor и wood roughness floor 0.72.
- Существующие mesh/DDS и иконки установлены через `_refresh_weapon_surfaces.py`, с резервными копиями и сохранением всех имён/регистраций. Это ресурсное обновление; items/metadata/companion не переписывались.
- `BLOCKED` для повторной визуальной runtime-приёмки AC-003: DAP read-only probe подтвердил debug / ModEditor, но Computer Use был остановлен владельцем через Escape. К попытке штатного reload ресурсов порт 8165 уже возвращал ConnectionRefused; reload в игре не выполнен. На диске исправления установлены и будут загружены при следующем запуске. Не считать полным игровым PASS.

## Дополнение владельца 27.09.2026: материалы, оптика и иконка

Явно разрешено текущей беседой: дерево VZ58 приблизить к АКМ, исправить неровные блики VZ58 и Vektor R4, добавить коллиматоры VZ58, выровнять иконку. Исходные архивы повторно предоставлены владельцем.

- `JAZZ-WEAPON-VZ58-001-REQ-005`: тёмное продольное дерево по референсу установленного АКМ, сохранить UV/крепления; устранить подтверждённые ошибки normal/PBR VZ58 и R4 без изменения игрового баланса.
- `JAZZ-WEAPON-VZ58-001-REQ-006`: существующие совместимые коллиматоры в Scope VZ58 с разными штатными визуалами; сохранить требование RIS для установки оптики.
- `JAZZ-WEAPON-VZ58-001-REQ-007`: иконка VZ58 324x165 в горизонтальном боковом ракурсе.
- `JAZZ-WEAPON-VZ58-001-AC-005`: offline: карты сохраняют размеры/UV и корректное кодирование; визуально сравнить дерево с АКМ, освещение с исходником.
- `JAZZ-WEAPON-VZ58-001-AC-006`: static: Scope items/companion равны, у каждой опции разрешается визуал, metadata сохраняет регистрации; editor/runtime round-trip явно зафиксировать.
- `JAZZ-WEAPON-VZ58-001-AC-007`: offline: иконка RGBA 324x165, боковой горизонтальный ракурс.

Уточнённый write set: существующие VZ58 Scope/WeaponComponent records в jazz/items.lua и InventoryItem/VZ58.lua; существующие DDS VZ58/R4 и их fallbacks в jazz_assets; VZ58 icon и профильные инструменты/документы. Runtime/редактор заняты параллельной проверкой АК; не сохранять поверх их состояния. Asset paths/public IDs/load order не менять.

### Evidence повторной коррекции

- `JAZZ-WEAPON-VZ58-001-AC-005`: `PASS` static/offline — исходные PNG сверены побайтно с предоставленными архивами (VZ58 18, R4 5); 26 файлов установлены с backup; DDS hash/size/encoding/fallback и normal RMS audit PASS. Две ImageGen-развёртки дерева сравнены с AKM и на модели. R4: 13508 треугольников, удалена одна почти коллинеарная грань 1.57e-9 м², оставшаяся поверхность/UV сохранены, HGM winding PASS, предупреждения о нулевых нормалях больше нет. Дополнение write set допускает коррекцию R4 HGM и source-only scripts.
- `JAZZ-WEAPON-VZ58-001-AC-006`: `PASS` static — владелец подтвердил закрытие игры, процессы проверены. Четыре коллиматора установлены в items/companion, semantic equality/visuals и структурный Lua gate PASS; metadata не менялась. Каталог 16 опций, 352 допустимые конфигурации, generated wiki build/check PASS. Editor/runtime round-trip не выполнен (открытый AC-003).
- `JAZZ-WEAPON-VZ58-001-AC-007`: `PASS` offline — WeaponIcons/VZ58.png RGBA 324×165, боковая ортографическая камера.
- Общий preflight sync: 6383 blocking / 1649 warnings до изменений, отдельные VZ58 resource/companion gates PASS. Межпакетная правка локальная, без коммита/публикации. Новые материалы в живой игре не принимались.
- Evidence/build: `_vz58_material_20260927`, `_r4_material_20260927`; scoped backup и audit в `tmp/vz58-r4-material/install`. Статус implemented: запрошенные материалы, R4 HGM, иконка и оптика установлены. Игровая приёмка AC-003 остаётся открытой.

- Дополнительная проверка: R4 corner normals все ненулевые. Старый общий `_check_r4.py` остановился на отсутствии explicit BurstShots в неизменявшемся InventoryItem/VektorR4.lua; проверки текущего HGM/UV/материалов прошли отдельно.

- Финальный strict sync после установки оптики: 6383 blocking / 1649 warnings, набор ошибок совпадает с preflight; новых и VZ58/R4-specific ошибок нет. DoD остаётся незакрытым только по AC-003 (editor/runtime acceptance). Review/backup snapshots сохранены с суффиксом .txt, чтобы аудитор не принимал их за активные companion Lua.

## Повторная игровая приёмка 2026-09-28

Решение владельца: approved; «дальше делай, вроде пока все».

- `JAZZ-WEAPON-VZ58-001-REQ-VISUAL-028` — Устранить светлую кайму деревянной рукояти, исправив источник/UV материала. Переместить запись VZ58 в папку редактора к автоматам. Улучшение остаточной мятости опционально: владелец разрешил сохранить текущий улучшенный металл, если дальнейшее изменение не обосновано.
- `JAZZ-WEAPON-VZ58-001-AC-VISUAL-028` — адресные static/compiled проверки и сопоставление до/после; игровая приёмка и editor save/reload отдельно.

Evidence: `JAZZ-WEAPON-VZ58-001-AC-VISUAL-028`: `BLOCKED` — изменения ещё готовятся; runtime не подтверждён.

Установка 28.09.2026: 19 файлов в jazz/jazz_assets, SHA256 исходников/backup/установленных файлов проверены. PASS static/compiled: 99 граней деревянной оболочки переназначены на деревянный участок atlas; геометрия, верхняя накладка и винт сохранены. Кайма отсутствует на крупном нижнем ракурсе. Editor ancestry совпадает с AK47; игровые свойства неизменны. Металл сохранён по разрешению владельца. Полная сводка и ссылки — `docs/design/weapon-visual-feedback-20260927.md`. `AC-VISUAL-028`: static PASS; editor/runtime/human BLOCKED до новой приёмки владельца.
