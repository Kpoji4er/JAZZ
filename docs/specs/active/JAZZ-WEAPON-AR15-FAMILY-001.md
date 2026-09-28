---
id: JAZZ-WEAPON-AR15-FAMILY-001
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
  - jazz/WeaponComponents/Optics/JAZZ_CarryHandle_AR15.png
  - jazz/docs/tools/_weapon_feedback_*
  - jazz/docs/design/*visual-feedback*
  - jazz/docs/design/references/*feedback*/*
  - jazz/docs/technical/systems/assets-entities.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/design/references/weapon-feedback-20260928/*
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/.agents/docs/playbooks/model-export-qa-handoff.md
  - jazz/docs/tools/_weapon_feedback_*
  - jazz/docs/design/weapon-visual-feedback-20260927.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/Code/System_WeaponComponent_Set.lua
  - jazz/Code/System_WeaponRemovableModify.lua
  - jazz/docs/tools/_ar15_revision_*
  - jazz/docs/tools/_repair_ar15_geometry.py
  - jazz/items.lua
  - jazz/InventoryItem/M16A4.lua
  - jazz/InventoryItem/M4A1.lua
  - jazz/InventoryItem/CAR15.lua
  - jazz/docs/specs/active/JAZZ-WEAPON-AR15-FAMILY-001.md
  - jazz/docs/design/weapons-import-plan-jaweapons.md
  - jazz/docs/design/weapon-3d-model-map.md
  - jazz/docs/design/magazine-tiers.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/weapons/data/weapon-component-options.csv
  - jazz/docs/tools/README.md
  - jazz/docs/tools/_audit_ar15_slots.py
  - jazz/docs/tools/_build_ar15_assets.py
  - jazz/WeaponIcons/M16A1.png
  - jazz/WeaponIcons/M16A2.png
  - jazz/WeaponIcons/M16A4.png
  - jazz/WeaponIcons/M4A1.png
  - jazz/WeaponIcons/CAR15.png
  - jazz_assets/Entities/M16A1.ent
  - jazz_assets/Entities/M16A2.ent
  - jazz_assets/Entities/M16A4.ent
  - jazz_assets/Entities/M4A1.ent
  - jazz_assets/Entities/CAR15.ent
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/M16R_*
  - jazz_assets/Entities/M4R_*
  - jazz_assets/Entities/Meshes/M16R_*
  - jazz_assets/Entities/Meshes/M4R_*
  - jazz_assets/Entities/Materials/M16R_*
  - jazz_assets/Entities/Materials/M4R_*
  - jazz_assets/Entities/Textures/M16R_*
  - jazz_assets/Entities/Textures/M4R_*
  - jazz_assets/Entities/Textures/Fallbacks/M16R_*
  - jazz_assets/Entities/Textures/Fallbacks/M4R_*
exclusive_resources:
  - jazz/items.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - AR15 family entity graph and Blender build
related_decisions:
  - none
approved_by: project-owner in conversation 2026-09-19; visual-fix pass 2026-09-20
---

Evidence 2026-09-23, AC-008: PASS static/executable — установка разделённых FrontSight M4/M16, fixed Handgrip и M16 Stock, прямые ванильные MagazineCAR15_02; M4 Long сохраняет цевьё, VerticalGrip использует Under. Все десять пересобранных meshes проходят HGM round-trip; `_ar15_revision_test.py` проверяет реальные setter/CanModifySlot для обоих порядков RIS, снятия, Scope и незатронутых семейств. `_audit_ar15_slots.py` PASS. BLOCKED runtime/editor/human: игра закрыта; настоящая посадка, сохранения и кабинет следующей сессией. Статус approved сохраняется до завершения обязательной приёмки.

# JAZZ-WEAPON-AR15-FAMILY-001: модульность и ремастер семьи AR15

## Проблема

Дополнение 27.09.2026: владелец возобновил отложенный визуальный ремонт словами «можнго править». Основание и скриншоты: `docs/design/weapon-visual-feedback-20260927.md`. У M4 короткий ствол должен визуально отличаться от обычного вместе с дульником; проверить и исправить привязки. Обновить иконку M4.

- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-VISUAL-027`: У M4 короткий ствол должен визуально отличаться от обычного вместе с дульником; проверить и исправить привязки. Обновить иконку M4. Игровой баланс, публичные ID и регистрация сохраняются; работа только в jazz/jazz_assets, отдельная сборка и backup перед установкой при закрытой игре.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-VISUAL-027`: static/offline — проверены точечные изменения, карты/меши и сборки, иконки 324×165 RGBA, исходные ресурсы сохранены. Runtime/human — подтверждение владельцем после нового запуска; offline PASS его не заменяет.


Решение владельца 2026-09-23 (approved): на M4A1 длина ствола не меняет цевьё; мушка принадлежит механическому прицелу вместе с целиком и отсутствует при установленной оптике на планке. Handgrip с одинаковыми моделями у M4A1/M16A4 не предлагается как модификация: оставить фиксированный default. Навесное, требующее RIS цевья, запрещено при обычном цевье в обоих порядках установки; верхняя штатная планка ресивера сохраняет возможность установки оптики. Дополнительно владелец потребовал ванильные плоские магазины на 20 у обоих предметов и фиксированный штатный приклад M16A4. Новые глобалы и дополнительные wraps не нужны: проверки в существующих setter и CanModifySlot.

- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-012` — выполнить перечисленные исправления приёмки; старые Handgrip/Stock нормализовать через setter, снимающий прежние эффекты. Мушка использует новые entity `M4R_M4A1_FrontSight` / `M16R_M16A4_FrontSight` в штатном визуальном слоте Gassblock; новых предметов или семейств нет. Остальные семейства не менять.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-008` — offline behavioral: оба порядка установки RIS/аттача, снятие аттача, независимость Scope, fixed slots и отсутствие изменений M1A/GoldenGun/AK74 проверены на настоящих функциях Lua с заглушками движка. Отдельно runtime: кабинет, сохранённые экземпляры, видимость мушки/целика и посадка магазинов после чистого запуска. Offline PASS не закрывает runtime.

Пять предметов семьи (`M16A1`, `M16A2`, `M16A4`, `M4A1`, `CAR15`) выросли из двух исходных FBX (`M4_16 Complex.fbx` для четырёх, `CAR15.fbx` для CAR-15). Read-only разбор 2026-09-19 показал три расхождения.

Хай-тир беднее лоу-тира по модульности: у `M16A1` есть съёмное цевьё, вариант с M203, отдельный магазин и холстер, а у `M16A4` только мебель и мушка, слотов `Handguard`, `Stock`, `Barrel` нет. У `M4A1` из модулей только магазин и фиксированный fold-слот приклада.

`M4A1` ниже дом-стандарта по материалам: пять подматериалов и только `BaseColorMap`, без `NormalMap`, `RMMap` и `SpecialMap`, тогда как у остальных четырёх полный набор 1024.

Масштаб семьи выпадает из линейки комплекта. При реальных длинах 99–100.6 см box-длины мешей составляют 116.4 (`M16A1`), 112.6 (`M16A2`), 118.7 (`M16A4`), то есть k = 1.12…1.18, при k = 0.98 у `G3A3` и 0.96 у `MP5A2` (оружие с несъёмным прикладом) и правиле «АК ≈ 0.9 м» из `docs/design/weapons-import-plan-jaweapons.md`. Отремастеренный `AKR_AK74` даёт ресивер 64.4 см плюс приклад 21.8 см. Перемасштабировать существующие меши нельзя: исходных FBX нет ни на одной локальной директории, `_decode_weapon_reference_meshes.py` переносит только геометрию без UV и материалов, а у `.ent` нет атрибута масштаба сущности — единственный scale в формате это `attach@spot_scale`, масштабирующий навесное, а не хост.

## Цели

- Довести модульность `M16A4` и `M4A1` до уровня хай-тира на существующих component ID.
- Пересобрать геометрию семьи из полноценных исходников в единой линейке масштаба комплекта.
- Сохранить пять ID предметов, статы и совместимость сейвов.

## Non-goals

- Новые ID предметов. Ванильный `AR15` остаётся отключённой заглушкой, `M4Commando` и прочие AR вне scope.
- Ремастер `M16A1`, `M16A2` и `CAR15` в фазе 1: их меши и материалы соответствуют дом-стандарту, замена нужна только ради линейки масштаба и выполняется в фазе 3.
- Массовое сведение визуалов 30-местных магазинов и пакетная простановка `spot_scale`: при выбранной линейке это расходная работа, выполняется внутри фазы 2–3 вместе с новой геометрией.
- Правка общих компонентов ради косметики (`JAZZ_VerticalGrip` с `Entity = false` для `M4A1`, дремлющие визуалы `Stock` у `M16A2`, визуал глушителя у `M16A1` без слота `Muzzle`). Зафиксировано как наблюдение, поведение не меняется.
- Изменение статов пятёрки помимо эффектов подключаемых модулей.

## Требования

- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-001` — публичные ID пяти предметов, их `Entity`-имена в фазе 1 и базовые статы не меняются; ванильный `AR15` остаётся отключённым.
- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-002` — `M16A4` получает слоты `Barrel` (норма и короткий), `Stock` (норма, тяжёлый, лёгкий), `Handgrip` (штатная и эргономичная), `Trigger` (пустой по умолчанию, `JAZZ_Autofire`) и `Handguard` (`JAZZ_Handguard` дефолт, `JAZZ_Handguard_RIS`). `M4A1` получает `Barrel` (норма, короткий, длинный), `Handgrip` и `Handguard` (то же плюс RIS). Варианта без приклада нет. Fold-слот приклада `M4A1` не трогается.
- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-003` — с фазы 2 стволы и цевья видимые: каждая длина — отдельная сущность со спотом `Muzzle`. Пустой слот приклада не вводится.
- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-004` — линейка масштаба: **реальная длина** оружия (k = 1.0), приклад в разложенном положении. Ориентир задают уже установленные стволы: `G3A3` k = 0.98, `MP5A2` 0.96, `CAR15` 1.04; шипованные `M16*`/`M4A1` были выбросом на 1.12…1.18. Целевые длины: `M16A1` 99, `M16A2` и `M16A4` 100.6, `M4A1` 84, `CAR15` 79 см. Прежняя редакция требовала 0.87 от реальной длины по неустановленному графу `AKR_*`; владелец в игре увидел, что карабин выглядит слишком мелким, и линейка исправлена на установленную.
- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-005` — источники геометрии: `tigg_ar15_2015_with_lod` для `M16A2`, `M16A4`, `M4A1`; `Milspec AR15s - Phase 1 (Vietnam Era)` для `M16A1` и `CAR15`. Не смешивать текстурные семьи двух паков в одном меше. Хост `m16` даёт `M16A2` со съёмной ручкой и `M16A4` без неё; `CAR15` не делается из `mk18`, `M16A4` не делается из `M16A1`.
- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-006` — модули вырезаются целыми связными частями (loose parts). Плоскостной разрез запрещён: по `JAZZ-WEAPON-AK-FAMILY-001-AC-001` он уже дал отклонённую владельцем посадку магазина. Меши tigg распадаются на 74–177 отдельных шеллов, включая лоуер, магазин, цевьё, ствол, дульник, приклад, буферную трубу и пистолетную рукоять.
- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-007` — новая геометрия ложится в отдельные графы сущностей (`M16R_*`, `M4R_*`) по образцу `AKR_*`, с `.ent` без `<src>` и картами не более 2048. Существующие `.ent` пяти предметов очищаются от чужого абсолютного `<src>`.
- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-008` — вводятся два новых component ID и только они: рейловое цевьё и съёмная ручка для переноски как вариант слота `Scope`. Оба появляются вместе с геометрией в фазе 2.
- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-011` — после игрового прогона владельца (2026-09-20): рукоять и короткий ствол видимы; прицелы сдвинуты чуть вперёд на рейловую планку; `JAZZ_CarryHandle_AR15` — дефолт `Scope`, пустой слот скрыт; дульник посажен на резьбу (штатный пламегаситель = `JAZZ_DefMuzzle`, компенсатор не стопкается на такой же); цевьё RIS у `M16A4` закрывает винтовочное окно; 20-местный магазин — укороченный STANAG той же семьи, не `M16A1Stanag20`; приклад `M16A4` меняется визуально; metalness в RM слегка поднят по ID-маске, без хрома.
- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-009` — источники моделей и требуемый credit автора tigg фиксируются в `docs/design/weapon-3d-model-map.md` по образцу `docs/design/armor-3d-model-map.md`.
- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-010` — иконки пятёрки перерисовываются одним сетапом 324×165 с обводкой, с сохранением относительных длин внутри семьи (фаза 3).

## Инварианты и ограничения

- Чужой незакоммиченный diff в `jazz` сохраняется: `items.lua` правится точечно, без переформатирования и массовой перегенерации.
- Семьи магазинов не смешиваются: `…_AR15` остаётся отдельной от АК линейкой.
- Верх соответствует индексу: `M16A1` и `M16A2` с ручкой для переноски, `M16A4` и `M4A1` с планкой. RIS не появляется на `M16A1`.
- Винтовочного рейлового цевья в источниках нет; для `M16A4` карбинный RAS растягивается вдоль ствола до окна A2-цевья, чтобы рейл не сидел заглушкой на 20″. `BlockSlots` на общем `JAZZ_Handguard_RIS` по-оружейно не вешается.
- Слот `Scope` у `M16A4` и `M4A1` не бывает пустым: дефолт — `JAZZ_CarryHandle_AR15`. Пустой вариант скрыт, потому что целиться нечем.
- Fold-слот приклада `M4A1` по-прежнему не трогается. У `M16A4` приклад видимый: норма/тяжёлый — A2, лёгкий — складной с `m4`.
- Предсуществующее состояние аудита не приписывается этому изменению: 6235 блокирующих сообщений приходят из копий комплекта в `jazz/tmp/`, шесть — из quest-companion (`Auto5_quest`, `Galil_FlagHill`, `GoldenGun`, `LionRoar`, `TexRevolver`, `Winchester_Quest`), не зарегистрированных в `metadata.code` ещё на HEAD.

## Acceptance criteria

- `JAZZ-WEAPON-AR15-FAMILY-001-AC-001` — static: слоты из REQ-002 присутствуют в `items.lua` и в companion `M16A4`/`M4A1`, ссылаются только на существующие компоненты, `python docs/tools/_validate_items_quick.py` даёт exit 0.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-002` — static: `check-generated-sync.ps1 -Package jazz` не добавляет новых блокирующих сообщений по сравнению с зафиксированной базой (6241), `_check_weapon_imports.py` проходит.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-003` — static: в пяти `.ent` нет элемента `<src>`; ни один tracked-файл не содержит абсолютного локального пути.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-004` — editor/runtime: кабинет модификации показывает новые слоты у `M16A4` и `M4A1`; смена ствола, приклада, рукояти и установка автоспуска применяют эффекты; `JAZZ_Autofire` открывает автоматический огонь у `M16A4`; save/reload без ошибок и assert.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-005` — static: собранная геометрия фазы 2 соответствует линейке REQ-004 в пределах 2 см и собрана из целых связных частей.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-006` — human: владелец подтверждает посадку модулей и внешний вид в руках и на земле для каждого изменённого предмета. Без этого подтверждения фаза 2 не считается принятой.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-007` — human: иконки пятёрки приняты владельцем, размер 324×165, относительные длины сохранены.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: только штатные данные компонентов, новых hooks и Lua-глобалов нет.
- Saves: ID предметов и компонентов не меняются, существующие экземпляры получают новые слоты пустыми либо с дефолтным компонентом; новая игра не требуется.
- Network/determinism: штатные данные, RNG не затрагивается.
- Generated data: `jazz/items.lua` плюс companion `M16A4`, `M4A1`, `CAR15`; в фазе 2 добавляется `jazz_assets/items.lua` и `metadata.lua`.
- Cross-package references: `jazz` ссылается на сущности `jazz_assets` через существующую зависимость.
- Rollback/recovery: фаза 1 откатывается удалением добавленных слотов; исходные архивы в `<WEAPON_SOURCE_ROOT>` неизменны, новые графы фазы 2 удаляются целиком без влияния на текущие сущности.

## План и ownership

- Фаза 1 (данные): слоты REQ-002, очистка `<src>`, `CanBeEmpty` для слота `Side` у `CAR15`, доковые правки. Пакет-владелец `jazz`, для `.ent` — `jazz_assets`.
- Фаза 2 (геометрия хай-тира): `M16A4` и `M4A1` из tigg в графы `M16R_*`/`M4R_*`, два новых компонента REQ-008, визуалы для слотов фазы 1.
- Фаза 3 (остальная семья и иконки): `M16A2` из tigg, `M16A1` и `CAR15` из Milspec, единый сетап иконок.
- Исполнитель: текущая задача по семье AR15.
- Reviewer: владелец проекта.
- Declared write set и exclusive resources: frontmatter.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец выбрал линейку АК и порядок data-first, подтвердил два новых компонента и дал «да, делай» на реализацию. 2026-09-20: игровой прогон — видимые рукоять/короткий ствол, carry handle дефолтом, скрыть пустой Scope, сдвинуть прицелы вперёд, не стопкать компенсатор, растянуть RIS A4, поменять приклад A4, заменить 20-местный магазин, аккуратно поднять metalness.
- Дата: 2026-09-19, уточнение 2026-09-20.

## Evidence

Повторная визуальная правка 27.09.2026 по команде «можнго править»: `JAZZ-WEAPON-AR15-FAMILY-001-AC-VISUAL-027` — PASS static: штатный UpdateVisualObj в Lua-harness выбирает разные barrel entity при пяти переключениях и переносит дульник; short короче на 10.828 см. Иконка M4 переснята. BLOCKED runtime/human: одинаковый вид в игре не воспроизведён офлайн; геометрия и код M4 не изменялись. Сборка `jazz_weapon_feedback_20260927`: `compiled-report.json`, `components/component-report.json`, `install-manifest.json`, `installation.json`. В общей транзакции установлены 21 существующий файл, backup и SHA256 проверены; изменения jazz/jazz_assets незакоммичены. Допускается только удаление измеренных микрограней, которые становятся вырожденными в HGM; это не оптимизация видимой геометрии. Подробности — `docs/design/weapon-visual-feedback-20260927.md`.


### Фаза 1, 2026-09-19

Слоты добавлены в `items.lua` и зеркально в companion: `M16A4` получил `Barrel`, `Stock`, `Handgrip`, `Trigger` (итого 9 слотов), `M4A1` — `Barrel` и `Handgrip` (итого 8), у `CAR15` слот `Side` стал `CanBeEmpty`. `M16A1` и `M16A2` не изменялись. Правки точечные, чужой незакоммиченный diff в `items.lua` сохранён, переформатирования нет.

Из пяти `.ent` удалён элемент `<src file="<OTHER_USER_HOME>">`; `jazz_assets` содержит ровно пять однострочных удалений, XML разбирается, `findall('.//src')` пуст.

- `JAZZ-WEAPON-AR15-FAMILY-001-AC-001`: `PASS` static — `python docs/tools/_audit_ar15_slots.py` → PASS (парность items/companion, все компоненты существуют с тем же `Slot`, дефолты входят в свои опции); `python docs/tools/_validate_items_quick.py` → exit 0; `scripts/check-lua-quoted-strings.ps1` → OK на 1143 файлах.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-002`: `FAIL` — первая половина выполнена: `check-generated-sync.ps1 -Package jazz` даёт те же 6241 блокирующих сообщения до и после правок, новых нет, ни одно предупреждение не касается файлов из write set (6235 сообщений — копии комплекта в `jazz/tmp/`, 6 — quest-companion, все предсуществующие на HEAD; счётчик warning 1635→1636 относится к снимкам в `tmp/`). Вторая половина не выполнена: `_check_weapon_imports.py` падает на `KeyError: 'CanAppearInShop'` для `Mosin`. Проверено, что у `Mosin` нет shop-полей ни в рабочей копии, ни в `HEAD:items.lua`, и `InventoryItem/Mosin.lua` их тоже не содержит, то есть отказ предсуществующий и не связан с семьёй AR15. Нужно отдельное решение владельца по Mosin.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-003`: `PASS` static — `<src>` отсутствует во всех пяти `.ent`, абсолютных локальных путей в затронутых tracked-файлах нет.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-004`: `BLOCKED` runtime — игра не запускалась, кабинет модификации и `EnableFullAuto` у `M16A4` не проверены. Статический анализ этот AC не закрывает.
### Фаза 2, геометрия хай-тира, 2026-09-19

`docs/tools/_build_ar15_assets.py` собирает из сохранённого tigg-источника 12 сущностей: `M16R_M16A4` + `_Magazine`, `_CarryHandle`, `_RearSight`; `M4R_M4A1` + `_Magazine`, `_Handguard`, `_HandguardRIS`, `_Stock`, `_StockFolded`, `_CarryHandle`, `_RearSight`. Нарезка — только целые острова; `keep_only` падает по assert, если разрез пересёк бы полигон, поэтому плоскостной разрез невозможен по построению.

Особенности источника, которые пришлось снять: варианты стоят в витринном ряду и несут layout-офсет (первый прогон увёл споты `M4A1` на 2.9 м — снимается переводом в систему хоста); у tigg зариггированы подвижные части, и vertex groups (`bolt`, `trigger`, `magazine`, `charging handle`, `safety`, `dust cover`, `railcovers`, `stock`, `bullet`, `bolt release`) заставляли официальный экспортёр считать меши skinned и требовать анимированное состояние; квад-рейл состоит из тела и четырёх отдельных планок, которые generic-классификатор относил к телу варианта, поэтому RIS берётся по X-окну цевья.

- `JAZZ-WEAPON-AR15-FAMILY-001-AC-005`: `PASS` static — собранные длины `M16A4` 88.0 см (цель 88) и `M4A1` 73.1 см (цель 73.1), обе в пределах 0.1 см; высота ствола 5.60 и 5.46 см, `Trigger` на z ≈ 0, то есть фрейм совпадает с пропорциями заменяемых `.ent`. `hge_obj_settings.is_valid()` = true и пустой `get_errors()` у всех 12 сущностей. `AssetsProcessor.exe` exit 0 для обоих FBX: 12 `.ent`, 12 `.m.hgm`, 12 `.mtl`, 36 `.dds`; карты 2048 (корпус), 1024 (ручка), 512 (мушка) — в потолке 2048. Диагностика `Missmatched FBX file and SDK versions` та же, что зафиксирована в `JAZZ-APPEAR-001-AC-003`, импорт при ней завершается. Не закрыто: metalness в RM плоский (источник даёт только specular), это осознанное упрощение под пересмотр после игрового прогона.
### Фаза 2, установка, 2026-09-19

`docs/tools/_prepare_rifle_assets.py` (штатный staging) снял `<src>`, переименовал карты в `M16R_*`/`M4R_*`, собрал 21 текстуру и 64-пиксельные fallback'и. `docs/tools/_integrate_ar15_family.py --apply` перевёл `Entity` обоих предметов на новые графы, добавил `M4A1` слот `Handguard`, перевёл 11 визуалов (магазин, fold-пара приклада, цевьё, мушки) и зарегистрировал 12 сущностей в `jazz_assets`. Backup исходных файлов в `<build>/integration-backup`.

Дефект, найденный собственным аудитом и исправленный: вставка слота `Handguard` прошла в companion, но не в `items.lua`, потому что файлы отличаются переводом строки; скрипт теперь сопоставляет `\r?\n` и падает по assert, если правка не легла.

- `JAZZ-WEAPON-AR15-FAMILY-001-AC-006`: `BLOCKED` — требуется human acceptance владельца: игра ещё не запускалась, посадка модулей в руках и на земле не подтверждена.

### Фаза 2, исправление по игровому прогону, 2026-09-19

Владелец проверил в игре и сообщил два дефекта: у `M16A4` левая рука стояла у магазина вместо цевья, а `M4A1` выглядел заметно мелким. Причины найдены и устранены.

Масштаб: линейка 0.87 была снята с `AKR_*`, который в игре не установлен; фактически установленные стволы сидят на реальной длине (`G3A3` 0.98, `MP5A2` 0.96, `CAR15` 1.04, старые `M16*`/`M4A1` 1.12…1.18). REQ-004 переписан на k = 1.0, пересборка дала `M16A4` 100.6 см и `M4A1` 84.0 см в сборе (корпус 78.2 плюс отдельный приклад).

Споты: геометрические эвристики заменены на позиции из заменяемых `.ent`, пересчитанные тем же ratio. `Hand_l_grip` у `M16A4` встал на 31.3 см, то есть на относительную позицию 0.623 длины — ровно как у шипованной сущности, вместо прежних 22.6 см у магазинного окна. Восстановлен спот `Mountfront` у `M4A1`, без которого `JAZZ_VerticalGrip` не имел точки крепления. У `M4A1` больше не создаётся `Hand_l_grip`, которого нет у шипованной сущности. `spot_rot` для `Side` теперь экспортируется как `1,0,0,90`, а не зеркальный `-1,0,0,90`.

Ассеты обновлены на месте через `_integrate_ar15_family.py --refresh-assets --apply` (90 файлов, backup в `<build>/refresh-backup`); Lua не трогался, имена сущностей и текстур не менялись.

Проверки установки: `_audit_ar15_slots.py` PASS (парность items/companion сохранилась), `_audit_ar15_entity_graph.py` PASS (12 сущностей, 21 текстура, `<src>` нет, карты ≤ 2048, fallback'и ≤ 64), `_validate_items_quick.py` exit 0. `check-generated-sync.ps1 -Package jazz`: 6242 блокирующих против базы 6241; единственная новая запись — `InventoryItem/JAZZ_FNFAL_Tactical.lua` из параллельной работы редактора над FAL, к семье AR15 не относится. `-Package jazz_assets`: 90 блокирующих, из них 22 приходятся на `AKR_*` с тем же текстом «активный Entity companion не имеет ModItemEntity в items.lua», то есть это существующее свойство дома для `ModItemEntity` внутри `ModItemFolder`, а не регрессия установки; 12 записей AR15 попадают в ту же категорию.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-007`: `BLOCKED` — фаза 3 не начата.

### Фаза 2, видимые стволы и цевьё, 2026-09-19

Решение владельца: без варианта «без приклада»; ствол видимый; цевьё `M16A4` меняется модами; спот `Muzzle` едет со стволом.

`_build_ar15_assets.py` выносит дульник+трубу+мушку в модули, дельта-кольцо оставляет на хосте, альтернативные длины берёт с `m4` / `mk18` / `m16` в той же локальной рамке. `M16A4` получил `_Handguard` и `_HandguardRIS`; `M4A1` — три ствола и `_HandguardRifle` как второй визуал `JAZZ_BarrelLong`. Два новых ID: `JAZZ_Handguard_RIS` (строка 266664626516 «Цевьё с рельсой», reuse) и `JAZZ_CarryHandle_AR15` (новый ID 890000000020597, RU/EN). Установка: `_wire_ar15_visible_modules.py --apply`. Хосты пересобраны без впечённого ствола.

- `JAZZ-WEAPON-AR15-FAMILY-001-AC-001`: `PASS` static — `_audit_ar15_slots.py` PASS; A4 слоты включают `Handguard`; компоненты резолвятся.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-005`: `PASS` static — собранные длины 100.6 / 84.0 см; 20 сущностей `hge_obj_settings` valid; `AssetsProcessor` exit 0; `_audit_ar15_entity_graph.py` PASS (20 сущностей, `<src>` нет).
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-006`: `BLOCKED` — нужна приёмка владельца в игре.

### Фаза 2, правки по второму игровому прогону, 2026-09-20

Владелец: рукоять и короткий ствол не видны; прицелы слишком сзади; пластиковый металл; дульник высоковат и компенсатор садится на такой же; RIS A4 мелкий; carry handle должен быть дефолтом, пустой Scope скрыть; 20-местный магазин уродливый; приклад A4 не меняется.

Исправлено в сборке: `Barrel` = дельта-кольцо; короткий A4 больше не в координатах мушки (bbox 2.4…35.4 см вместо −29…+8); пламегаситель вынесен в `_*_DefMuzzle`; RIS A4 растянут до 29.2 см; рукоять и приклад A4 — отдельные сущности; 20-местный — укороченный STANAG той же семьи (высота 13.4 см); Scope +3 см вперёд; RM metalness по ID-маске ≤ 0.45. Слоты: `Scope` CanBeEmpty false, дефолт `JAZZ_CarryHandle_AR15`; `Muzzle` дефолт `JAZZ_DefMuzzle`, компенсатор `WeaponAttA_CompensatorM4`. Fold `M4A1` не тронут.

- `JAZZ-WEAPON-AR15-FAMILY-001-AC-001`: `PASS` static — `_audit_ar15_slots.py` PASS (A4/M4 Scope default CarryHandle, CanBeEmpty false; Muzzle default DefMuzzle).
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-005`: `PASS` static — длины 100.6 / 84.0 см; 28 сущностей; `_audit_ar15_entity_graph.py` PASS; `_validate_items_quick.py` OK.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-006`: `BLOCKED` — нужна повторная приёмка в игре после reload модов.

## Documentation delta

- `docs/technical/systems/weapons-ammo-components.md` — слоты и модули семьи AR15 в текущем загруженном состоянии.
- `docs/technical/weapons/data/weapon-component-options.csv` — **не обновлён**: файл генерируется `scripts/docs/weapons-docs.mjs`, а `node` в системе отсутствует. Руками генерируемый CSV не правился; регенерация остаётся задолженностью фазы 1.
- `docs/design/weapons-import-plan-jaweapons.md` — AR15 больше не «вне плана», ссылка на эту spec.
- `docs/design/magazine-tiers.md` — пометка, что `AR15` в строке семьи является отключённой заглушкой.
- `docs/design/weapon-3d-model-map.md` — источники моделей и credit автора tigg.
- Player-facing слой (`docs/wiki/`, `docs/showcase/ru|en/`) обновляется, когда новые слоты становятся видимы игроку в фазе 2.

### Разрешённые исправления приёмки, 2026-09-22

Владелец разрешил устранить выявленные дефекты оружия до брони. M16A4: короткий ствол сохраняет rifle-position мушку, выступающая труба короче на 10 см (примерно 16 дюймов), обычное цевьё и RIS не пересекают мушку. M4A1: origin перенесён в верхнюю часть рукояти; host и spots сдвинуты вместе, локальные рамки модулей сохранены. Новых компонентов/статов нет. `_repair_ar15_geometry.py`: strict mesh и round-trip HGM PASS для обоих; runtime после полного перезапуска обязателен. Диагностическая пересборка донора не экспортировалась целиком: старое длинное цевьё отклоняется strict gate по длинным узким граням. Установлены только исправленные BarrelShort и M4 host.

## Приёмка M16A4: посадка магазина и короткий ствол, 2026-09-27

Решение владельца в текущей беседе (approved): немного увеличить M16A4 под существующий магазин; короткий ствол должен выступать ближе к цевью. Это адресная корректировка REQ-004 для M16A4 и, по следующему сообщению владельца, M4A1.

- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-013` — увеличить собственные детали M16A4/M4A1 равномерно на 10%, включая их attachment spots; существующие магазины сохранить в исходном масштабе и посадить в шахту. Другие семейства не менять; общие ванильные модули и общий RearSight сохранить в исходном масштабе.
- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-014` — восстановить трубу BarrelShort из обычного ствола, укоротить её выступающую часть на 10 см до масштабирования; Muzzle следует новому дульному срезу. Сохранить цевьё и отдельную мушку. Никаких новых entity/ModItem/статов.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-009` — static/offline: все изменённые HGM совпадают с подготовленной геометрией и winding; материалы/UV сохранены, короткий ствол с трубой и Muzzle на её конце; визуальная примерка магазина и обеих длин.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-010` — runtime/human: магазин не торчит сквозь шахту, переключение ствола передвигает дульник к цевью, штатное/RIS цевьё и хваты не расходятся. BLOCKED до проверки в игре.

Владение: jazz_assets — только существующие M16R_M16A4/M4R_M4A1 ent/HGM; jazz — адресный `_ar15_revision_fit.py`, документация и эта spec. items/metadata/localization не изменяются; сборка из сохранённого assembled source, установка с backup после compiled audit.

- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-015` — M4A1: аналогичная подгонка магазина и проверка всех трёх длин. Scope сдвинуть вперёд на 3.5 см после масштабирования; геометрией CarryHandle компенсировать этот сдвиг, чтобы ручка сохраняла посадку на ресивере. Явно одобрено владельцем в текущей беседе. AC-009/010 распространяются на обе модели.

Evidence 2026-09-27: JAZZ-WEAPON-AR15-FAMILY-001-AC-009 PASS static/offline — 27 HGM, одинаковое число подготовленных/compiled граней, max vertex error <0.026 мм, winding error area 0. Магазины 20/30 проверены отдельными примерками. Длинные узкие полосы A2-цевья разбиты без перемещения поверхности, UV интерполированы. Установлены только 54 существующих ent/HGM с резервными копиями; регистрации, DDS, материалы и баланс не менялись.

JAZZ-WEAPON-AR15-FAMILY-001-AC-010 BLOCKED human acceptance; runtime subcheck PASS: debug ModEditor, evaluate-only DAP. После AsyncLoadAdditionalEntities ограниченного списка 27 ent новая точка Scope M4=(47,3,121) мм; Muzzle M16 normal/short x=711/601 мм; M4 normal/short/long x=534/426/681 мм. У всех конфигураций Muzzle parent=Barrel; CarryHandle разрешается в правильную entity. Human visual/hand poses BLOCKED: свежий кабинет не осмотрен. Статус approved сохраняется до обязательной визуальной приёмки.

DoD validator 2026-09-27: BLOCKED, поскольку общий spec всё ещё содержит незавершённую игровую/human приёмку. Scoped documentation check PASS. Это не мешает установленной адресной коррекции ресурсов.

## Повторная игровая приёмка 2026-09-28

Решение владельца: approved; «дальше делай, вроде пока все».

- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-VISUAL-028` — М4 и М16А4: устранить одинаковый вид standard/short в полной сборке и при переключении, включая дульные насадки. Подтвердить разные установленные модели и посадку; прежний узкий harness не закрывает жалобу.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-VISUAL-028` — адресные static/compiled проверки и сопоставление до/после; игровая приёмка и editor save/reload отдельно.

Evidence: `JAZZ-WEAPON-AR15-FAMILY-001-AC-VISUAL-028`: `BLOCKED` — изменения ещё готовятся; runtime не подтверждён.

Уточнение причины REQ-VISUAL-028: штатный GetComponentBlocksAnyOfAttachedSlots сравнивает отсутствующий components.Side2 (nil) с пустой строкой и ошибочно возвращает blocked. Исправить существующую функцию: отсутствующий компонент равен пустому; не снимать реальные ограничения занятых слотов. Проверить UI CanModifySlot, затем полный визуальный граф.

Установка 28.09.2026: 19 файлов в jazz/jazz_assets, SHA256 исходников/backup/установленных файлов проверены. PASS static: исходный UI blocked воспроизведён для обоих AR15; исправленный helper пропускает отсутствующий/пустой/default Side2 и сохраняет блокировку занятого. Полный setter/UpdateVisualObj normal-short-normal-short PASS. Полная сводка и ссылки — `docs/design/weapon-visual-feedback-20260927.md`. `AC-VISUAL-028`: static PASS; editor/runtime/human BLOCKED до новой приёмки владельца.


## Повторная приёмка 28.09.2026, второй проход

Решение владельца: после сбора замечаний и паузы команда «делай» разрешает реализацию сохранённого списка, без commit/push. Пауза снята.

- `JAZZ-WEAPON-AR15-FAMILY-001-REQ-FEEDBACK-028B` — М16: по уточнению владельца «лучше цевье у м16 продли» закрыть разрыв удлинением цевья до переднего узла, ствол не менять; новая иконка. М4: подствольник вперёд. На показанных RIS М4/М16 фонарь и аналогичные устройства сверху. CarryHandle получает собственную иконку. Обычные иконки согласованы по свету со старым набором. Общая система иконок с установленными модулями для всего арсенала вынесена владельцем в отдельную задачу; в текущий проход не входит.
- `JAZZ-WEAPON-AR15-FAMILY-001-AC-FEEDBACK-028B` — static/compiled: корректный граф ресурсов и отсутствие регрессий; offline: сравнение до/после; runtime/human: повторить показанный владельцем сценарий.

Evidence `JAZZ-WEAPON-AR15-FAMILY-001-AC-FEEDBACK-028B`: BLOCKED — реализация и повторная приёмка в работе. Установка только после подготовки кандидатов, проверок и закрытия игры. Новые рабочие скрипты `_weapon_feedback_*`, материалы приёмки и исходные write sets входят в этот проход.


Второй проход 28.09: [отчёт staging и открытых пунктов](../../design/weapon-visual-feedback-20260928-round2.md). Проверенные кандидаты подготовлены отдельно; установка/runtime/editor NOT_RUN. Статус approved сохранён. HAV и 6Б3 не приняты по эксперименту с весами и исключены из транзакции.

28.09.2026, после «игра закрыта, применяй»: проверенный пакет второго прохода установлен, 27 файлов и backup SHA256 PASS; installed graph/structural PASS. Новых generated ERROR нет; общий baseline остаётся FAILED. HAV/6Б3 исключены из установки, runtime/editor/human остаются NOT_RUN. По последующему запросу разрешены локальные коммиты; push не разрешён.
