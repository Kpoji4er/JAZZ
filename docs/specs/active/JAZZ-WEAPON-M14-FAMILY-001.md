---
id: JAZZ-WEAPON-M14-FAMILY-001
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
  - jazz/docs/technical/systems/assets-entities.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/technical/override-matrix.md
  - jazz_assets/Entities/Materials/JAZZ_M14_OpticsMount*
  - jazz/docs/design/references/weapon-feedback-20260928/*
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/.agents/docs/playbooks/model-export-qa-handoff.md
  - jazz_assets/Entities/Textures/Fallbacks/MK14EBR*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_M14*
  - jazz/docs/tools/_weapon_feedback_*
  - jazz/docs/design/weapon-visual-feedback-20260927.md
  - jazz/Code/System_WeaponComponent_Set.lua
  - jazz/docs/tools/_m14_render_culling.py
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/InventoryItem/M14SAW.lua
  - jazz/InventoryItem/M21.lua
  - jazz/InventoryItem/MK14EBR.lua
  - jazz/InventoryItem/JAZZ_M14_MkIII.lua
  - jazz/WeaponIcons/MK14EBR.png
  - jazz/WeaponIcons/JAZZ_M14_MkIII.png
  - jazz/WeaponIcons/M14.png
  - jazz/WeaponIcons/M21.png
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/*
  - jazz/docs/specs/active/JAZZ-WEAPON-M14-FAMILY-001.md
  - jazz/docs/design/weapons-import-plan-jaweapons.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/weapons/data/*
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/wiki/weapons/battle-rifle.md
  - jazz/docs/wiki/weapons/sniper-rifle.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/tools/_m14_*
  - jazz/docs/tools/_export_m14_family_assets.py
  - jazz/docs/tools/_integrate_m14_family.py
  - jazz/docs/tools/_ar15_revision_test.py
  - jazz/docs/tools/README.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/JAZZ_M14*
  - jazz_assets/Entities/MK14EBR*
  - jazz_assets/Entities/Meshes/JAZZ_M14*
  - jazz_assets/Entities/Meshes/MK14EBR*
  - jazz_assets/Entities/Materials/JAZZ_M14*
  - jazz_assets/Entities/Materials/MK14EBR*
  - jazz_assets/Entities/Textures/JAZZ_M14*
  - jazz_assets/Entities/Textures/MK14EBR*
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - M14 localization IDs and Blender build
related_decisions:
  - none
approved_by: project-owner in conversation 2026-09-20
---

# JAZZ-WEAPON-M14-FAMILY-001: линейка M14 — классика, M21, EBR и уник

## Проблема

Дополнение 27.09.2026: владелец возобновил отложенный визуальный ремонт словами «можнго править». Основание и скриншоты: `docs/design/weapon-visual-feedback-20260927.md`. Немного затемнить дерево M14, заменить модель сошек обычного M14 на модель АК с проверкой посадки, исправить материалы/нормали Mk14 EBR. Переснять M14/M21/EBR иконки.

- `JAZZ-WEAPON-M14-FAMILY-001-REQ-VISUAL-027`: Немного затемнить дерево M14, заменить модель сошек обычного M14 на модель АК с проверкой посадки, исправить материалы/нормали Mk14 EBR. Переснять M14/M21/EBR иконки. Игровой баланс, публичные ID и регистрация сохраняются; работа только в jazz/jazz_assets, отдельная сборка и backup перед установкой при закрытой игре.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-VISUAL-027`: static/offline — проверены точечные изменения, карты/меши и сборки, иконки 324×165 RGBA, исходные ресурсы сохранены. Runtime/human — подтверждение владельцем после нового запуска; offline PASS его не заменяет.


Семья M14 в моде сведена к трём почти одинаковым ванильным силуэтам и одному уже импортированному гражданскому M1A.

- `M14SAW` и `M21` делят сущность `Weapon_M14`. M21 собран из M14: те же слоты, тот же меш, отличие в атаках и дефолтном `JAZZ_StockHeavy`.
- `JAZZ_StockHeavy` на M14/M21 вешает `WeaponAttA_StockM14_Heavy` — ванильный приклад с более вертикальным хватом. Иконка M21 рисует дерево и оптику, в мире видна чужая ложа. `JAZZ_StockLight` ставит `WeaponAttA_StockM14_Plastic` с иконкой AR-15.
- У `M14SAW` и `M21` нет `ModifyRightHandGrip`, хотя Gold Fever на той же геометрии флаг имеет, как Мосин.
- Отдельной винтовки с шасси и пистолетной рукоятью нет. Архив `Mk 14 Custom.zip` её даёт.
- Уник из `M14 UNIQ.zip` не должен затирать Gold Fever.

Доноры проверены офлайн, без записи в пакеты. Счётчики OBJ в zip — повторы одной геометрии, не нарезка.

## Цели

- Классический M14 и M21 читаются как USGI-ложка без отдельной пистолетной рукояти.
- M21 отличается от M14 оптикой и ролью, а не ванильным Heavy-прикладом.
- Появляется Mk 14 EBR на своём шасси.
- Появляется отдельный уник из UNIQ.zip. Gold Fever остаётся ванильным золотым M14.
- M1A не переимпортируется.

## Non-goals

- Замена вида или ID `GoldenGun` / Gold Fever.
- Повторный импорт `M1A Rifle.zip`: сущность `M1A` уже в `jazz_assets`.
- Третья современная винтовка из `M14 DMR Designated Marksman Rifle (DMR, Stock).zip`. Архив остаётся донором сошек или глушителя для EBR/уника, отдельный ID не заводится.
- Короткий SOC-16 из Lego как отдельный предмет.
- Общий магазин M14 с FAL или AR.
- Планки Mk14 на классическом M14 в дефолте.
- Выдача новых стволов в лут Легиона.
- Коммит, push, Steam, запуск `JA3.exe` в обход Steam.

## Требования



- `JAZZ-WEAPON-M14-FAMILY-001-REQ-014` — решение владельца 2026-09-27: на M14SAW слегка снизить roughness только дерева, исправить посадку оптики и сошек; в Under оставить только `JAZZ_Bipod_Under` и пустой вариант. Удалить визуальные нижние/боковые планки M14SAW; фонари и лазеры крепить непосредственно у ствола без `WeaponAttA_SideMountM14`. Старые недопустимые Under-компоненты снимать существующим setter и load/new-game проходом. Общий материал деревянной ложи разделяется с M21. Новый облик или удаление M21 пока не утверждены.
- `JAZZ-WEAPON-M14-FAMILY-001-REQ-015` — решение владельца 2026-09-27: исправить аналогичные дефекты граней JAZZ_M14_MkIII, сохраняя геометрию, UV, ID, компоненты и характеристики. Проверить отдельные активные детали семейства.



- `JAZZ-WEAPON-M14-FAMILY-001-REQ-013` — решение владельца 2026-09-27: MK14EBR относится к Т3-1; comment редактора и companion должны содержать `Tier 3-1`. Отдельный магазинный `Tier = 4` не является тиром оружия и этой правкой не меняется. Исправить повторно предъявленные на скриншоте дефекты корпуса EBR: проверить сварку совпадающих вершин, ориентацию граней, отсутствие custom normals и соответствие compiled HGM исходнику. Геометрия и UV сохраняются, кроме соединения совпадающих вершин; новые ID не вводятся.



- `JAZZ-WEAPON-M14-FAMILY-001-REQ-012` — при сочетании `JAZZ_FlashlightOff` и `JAZZ_GrenadeLauncher_M14` сохранять `Mountside` (`WeaponAttA_SideMountM14`) у M14SAW, MK14EBR и JAZZ_M14_MkIII, как у M21. Исправление подтверждённых W03–W05 приёмки 2026-09-26; прочие компоненты и характеристики не менять.

- `JAZZ-WEAPON-M14-FAMILY-001-REQ-011` — решение владельца 2026-09-23: убрать выбор длины ствола на четырёх импортированных предметах M14SAW/M21/MK14EBR/JAZZ_M14_MkIII. Оставить штатный BarrelNormal как фиксированный технический компонент, без морфинга; M1A/GoldenGun не затрагивать. Это заменяет сохранение доступных вариантов Barrel из REQ-009. Исправить пропадание деревянной ложи JAZZ_M14 при взгляде с одного бока, подтверждённое в runtime 2026-09-23.

- `JAZZ-WEAPON-M14-FAMILY-001-REQ-001` — `M14SAW` сохраняет ID и класс `BattleRifle`. Хост — новая сущность `JAZZ_M14` из корпуса Lego 112 см с albedo `T_M14_D` (дерево). Отдельной пистолетной рукояти на хосте нет. `ModifyRightHandGrip` равен true. Слот Stock остаётся `Modifiable = false`; визуалы `ApplyTo` для `M14SAW` у `JAZZ_StockHeavy` и `JAZZ_StockLight` не используют `WeaponAttA_StockM14_Heavy` и `WeaponAttA_StockM14_Plastic`.
- `JAZZ-WEAPON-M14-FAMILY-001-REQ-002` — `M21` сохраняет ID и класс `SniperRifle`. Хост тот же `JAZZ_M14`. Дефолтный вид — дерево плюс ART из `M14 Lego.zip` (`model_0`), а не `WeaponAttA_StockM14_Heavy`. `ModifyRightHandGrip` равен true. Автоматический огонь не добавляется.
- `JAZZ-WEAPON-M14-FAMILY-001-REQ-003` — `M1A` сохраняет ID, сущность `M1A` и текущие слоты. Меняются только общие `ApplyTo` семьи, если без них не садятся магазины или дульник.
- `JAZZ-WEAPON-M14-FAMILY-001-REQ-004` — новый предмет `MK14EBR`, класс `BattleRifle`, DisplayName «Mk 14 EBR». Сущности из `<WEAPON_SOURCE_ROOT>\Weapons\M14\Mk 14 Custom.zip`: ресивер, шасси Sage EBR, пистолетная рукоять, складной AR-приклад, ствол. Оружие **Т3-1**. Bobby Ray **in**, shop Tier 4, `Cost` 20000, `RestockWeight` 25, `Reliability` 70, `Damage` 33, `Recoil` 28. Атаки: одиночный, очередь, авто. Калибр `JAZZ_Caliber_762x51`.
- `JAZZ-WEAPON-M14-FAMILY-001-REQ-005` — новый предмет `JAZZ_M14_MkIII`, класс `SniperRifle`, DisplayName «M14 Mk III». Сущности из `<WEAPON_SOURCE_ROOT>\Weapons\M14\M14 UNIQ.zip`. Свой камуфляж и рельса MK III, масштаб семьи M14. Bobby Ray **out**: `CanAppearInShop = false`, `RestockWeight` 0. `GoldenGun` не редактируется.
- `JAZZ-WEAPON-M14-FAMILY-001-REQ-006` — магазины: `M14SAW`, `M21` и `M1A` остаются на `JAZZ_MagSmall20_10_M14` и `JAZZ_MagNormalFine_M14`. `MK14EBR` и `JAZZ_M14_MkIII` получают собственные `ApplyTo`-визуалы этих же ID либо отдельные `JAZZ_Mag*_M14EBR` / `JAZZ_Mag*_M14MkIII`, без веток `_FAL` / `_G3` / AR.
- `JAZZ-WEAPON-M14-FAMILY-001-REQ-007` — иконки `MK14EBR` и `JAZZ_M14_MkIII` — 324×165 с обводкой серии. Иконки `M14` и `M21` переснимаются только если новый силуэт расходится с текущим рисунком.
- `JAZZ-WEAPON-M14-FAMILY-001-REQ-008` — масштаб новых хостов садится на ванильный `Weapon_M14` по длине ствольной коробки и губкам магазина. Архивы не затираются; распаковка только во временный каталог вне пакетов.
- `JAZZ-WEAPON-M14-FAMILY-001-REQ-009` — исправить дефекты приёмки 2026-09-22 последовательно по предметам: EBR собирается целиком из согласованных деталей Sage, магазин/рукоять снизу, без второго ванильного ствола; классика/M21 без висящих ствола/ART/сошек; Mk III без второго ствола и наложенной оптики. Сохранять игровые характеристики и доступные ID компонентов; визуальные варианты согласовать с собственным хостом. Экспорт только через `prepare_export_mesh`, без custom normals, установка при закрытой игре.
- `JAZZ-WEAPON-M14-FAMILY-001-REQ-010` — Mk III использует винтовочный хват (`ModifyRightHandGrip = true`): у фактического донора UNIQ деревянная шейка ложи, отдельной пистолетной рукояти нет. Запечённый scope/suppressor заменяются штатными сменными `JAZZ_Scope_12x` / `JAZZ_Suppressor` в default; их штатные эффекты применяются согласно компонентам. Базовые численные характеристики предмета не меняются. Scope/Muzzle UI должен соответствовать видимым деталям.

## Инварианты и ограничения

- Публичные ID `M14SAW`, `M21`, `M1A`, `GoldenGun` не переименовываются.
- Gold Fever остаётся на `Weapon_M14_GoldEquip` и ванильной иконке.
- Классика и M1A могут делить магазин и близкий ствол; шасси Mk14 и уник — нет.
- На классический M14 в дефолте не ставятся рейки Troy SASS / Sage EBR.
- В рабочей копии `jazz` есть посторонний незакоммиченный рефактор. Правки точечные, без mass regen.
- `InventoryItem/vanillunique/GoldenGun.lua` в этом изменении не трогается.

## Acceptance criteria

- `JAZZ-WEAPON-M14-FAMILY-001-AC-012` — static/offline: MkIII после подготовки без degenerate/custom normals, треугольники и UV сохранены, compiled HGM совпадает с подготовленным source, оба бока проверены с culling. Runtime/human: подтверждение нового экспорта в игре.

- `JAZZ-WEAPON-M14-FAMILY-001-AC-011` — static: M14SAW Under содержит только сошки/пусто, Side не создаёт планку и имеет собственный spot, недопустимые старые Under снимаются с эффектами; roughness уменьшена только на дереве. Offline: сравнение посадки оптики/сошек/фонаря по геометрии. Runtime/human: визуальная проверка и переключение компонентов после reload.

- `JAZZ-WEAPON-M14-FAMILY-001-AC-010` — static: MK14EBR имеет comment `Tier 3-1` в items/companion/интеграторе; Bobby Tier/RW/Cost прежние. Геометрия: количество треугольников и loop UV не потеряны, нет degenerate/custom normals, compiled HGM соответствует подготовленному мешу; render обоих боков с backface culling. Runtime/human: новый процесс игры показывает цельный корпус EBR; offline PASS не закрывает runtime.

- `JAZZ-WEAPON-M14-FAMILY-001-AC-009` — static: выключенный фонарь имеет отдельный Mountside visual для всех четырёх предметов; runtime: после переключения фонаря и установки GL в обоих порядках кронштейн виден и GL не висит отдельно. Runtime требует нового запуска владельцем.

- `JAZZ-WEAPON-M14-FAMILY-001-AC-001` — static: `M14SAW` и `M21` имеют `ModifyRightHandGrip = true`; визуалы Stock для этих ID не ссылаются на `WeaponAttA_StockM14_Heavy` и `WeaponAttA_StockM14_Plastic`; `_validate_items_quick.py` exit 0.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-002` — static: в `jazz_assets` есть хост `JAZZ_M14` и ART-сущность для M21; `M14SAW` и `M21` ссылаются на `JAZZ_M14`.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-003` — static: `MK14EBR` зарегистрирован в `items.lua`, `metadata.lua` и companion; иконка 324×165 на месте; оружие Т3-1; Bobby in BR4 / RW 25 / Cost 20000.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-004` — static: `JAZZ_M14_MkIII` зарегистрирован так же; `CanAppearInShop = false`; `GoldenGun` в diff отсутствует.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-005` — static: магазинные компоненты семьи не содержат ApplyTo на FAL/AR ID в новых визуалах; EBR и уник не делят меш магазина с деревом.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-006` — runtime: классика и M21 в руках без пистолетной рукояти; M21 несёт ART; EBR и уник берутся, стреляют и перезаряжаются; save/reload чистые.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-007` — human: иконки четырех силуэтов читаются как разные винтовки.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-008` — static/editor/runtime: исправленные сборки проходят строгий mesh-аудит; компоненты не дублируют запечённые детали; после чистого запуска владелец/агент проверяет aim/crouch/prone, стрельбу, перезарядку и save/reload. Offline-сборка не закрывает runtime.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: новые сущности в `jazz_assets`, существующие классы оружия. Ванильный `Weapon_M14` остаётся у Gold Fever.
- Saves: ID `M14SAW`/`M21` сохраняются. Смена Entity на экземплярах в сейве подхватывается из класса. Экземпляры с визуалом Heavy после смены ApplyTo показывают дерево.
- Network/determinism: штатные данные компонентов, собственного RNG нет.
- Generated data: `items.lua`, `metadata.lua` и companion в `jazz` и `jazz_assets` — одна транзакция.
- Cross-package references: `jazz` зависит от `jazz_assets`. `jazz-units` в этом scope не меняется.
- Rollback/recovery: вернуть Entity `Weapon_M14` у M14SAW/M21, удалить записи `MK14EBR` и `JAZZ_M14_MkIII` и новые сущности. Исходные zip не изменялись.

## План и ownership

- Пакет-владелец: `jazz` для предметов и локализации, `jazz_assets` для сущностей.
- Исполнитель: агент сессии.
- Reviewer: project-owner.
- Declared write set: frontmatter `write_set`.
- Exclusive resources: frontmatter `exclusive_resources`.

## Решение владельца

- 2026-09-26: «правь», затем «да» разрешают исправления подтверждённой приёмки, включая W03–W05. АК-103 исключён: заменён другим агентом. Игра закрыта; commit/push запрещены.

- 2026-09-22: владелец поручил исправить находки приёмки, оружие первым, броню последней; игру закрыл для экспорта. Начать с MK14EBR, далее по одному предмету. 6Б3 переделывается последним по референсу. Повторный запуск игры запрашивается после готовности всего пакета к проверке. Это разрешение на исправления, без commit/push.

- Статус: approved.
- Кто подтвердил: project-owner, фраза «наверное надо делать» в беседе 2026-09-20 после разбора архивов M14, M21, EBR и уника.
- Дата: 2026-09-20.
- Основание: M21 собран из M14 и выглядит чужим из-за Heavy-приклада; пистолетная рукоять должна жить на EBR и унике; Gold Fever не затирать.

## Evidence

Повторная визуальная правка 27.09.2026 по команде «можнго править»: `JAZZ-WEAPON-M14-FAMILY-001-AC-VISUAL-027` — PASS static/offline: M14 wood RGB ×0.85 по маске; сошки M14SAW = WeaponAttA_BipodAK47 на собственном Under (56,0,9.5) см, M21 не изменён. EBR: жёсткие стыки 40°, normal strength 0.55, 48366 треугольников вместо 48372. Удалены шесть схлопывавшихся при квантовании микрограней (общая исходная площадь 0.12215 мм²), остальные позиции/UV сохранены. Compiled geometry/winding/strict normals и посадка сошек в двух ракурсах PASS. Иконки M14/M21/EBR обновлены. BLOCKED runtime/editor/human. Сборка `jazz_weapon_feedback_20260927`: `compiled-report.json`, `components/component-report.json`, `install-manifest.json`, `installation.json`. В общей транзакции установлены 21 существующий файл, backup и SHA256 проверены; изменения jazz/jazz_assets незакоммичены. Допускается только удаление измеренных микрограней, которые становятся вырожденными в HGM; это не оптимизация видимой геометрии. Подробности — `docs/design/weapon-visual-feedback-20260927.md`.


После установки strict generated-sync: FAIL (6385 errors, 1649 warnings). Сравнение ERROR-строк с исходным аудитом: единственное добавление — сторонняя временная копия `tmp/vz58-r4-material/optics/backup/InventoryItem/VZ58.lua`, отсутствующая в metadata.code; новых ошибок по изменённым M14-файлам нет. DoD validator остаётся FAIL из-за незакрытых runtime/editor/human AC; это не acceptance. Бэкап всех 17 исходных файлов проверен по SHA-256.


- `JAZZ-WEAPON-M14-FAMILY-001-AC-010`: `PASS` static/offline — Т3-1 синхронен в items/companion/интеграторе; shop Tier/RW/Cost сохранены; меши EBR проверены и установлены. `BLOCKED` runtime/editor/human — требуется новый запуск и save/reload.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-011`: `PASS` static/offline — Under только сошки/пусто, 13 M14 visual overrides, посадка проверена на геометрии; RM median 203→191, линейный формат BC7, mip chain/fallback. Lua migration и снятие эффектов PASS. `BLOCKED` runtime/editor/human.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-012`: `PASS` static/offline — корпус, штатный ствол и оба магазина MkIII установлены после проверки геометрии/winding и сохранения UV. `BLOCKED` runtime/editor/human.

Установка 2026-09-27: владелец подтвердил закрытие игры; 17 файлов установлены с backup и проверкой исходных хэшей. `AC-010/011/012` — PASS static/offline; runtime/editor/human остаются BLOCKED. Т3-1 присутствует в установленных items/companion и интеграторе. Корпуса EBR/MkIII: 48372/8859 треугольников; исправлено направление 17293/1516 граней. Дополнительно подготовлены штатные стволы EBR/MkIII и оба магазина MkIII. Все шесть compiled HGM совпали с подготовленной геометрией и winding; loop UV сохранены, custom normals и degenerate отсутствуют. Lua harness проверил Under (сошки/пусто), снятие старых эффектов через setter и LoadGame, сохранение M21 и AR15 ограничений. Structural checker, Lua parse и behavioral harness PASS до и после установки; локальный docs-check PASS. Итоговые M14 ModItem/visuals совпадают со staging, остальные 16 файлов совпадают по SHA-256; параллельные изменения STG44/другой оптики сохранены. Исходный общий generated-sync аудит до изменения данных: FAIL (6384 errors, 1650 warnings, включая многочисленные копии под tmp и существующие entity-регистрации); этот фон не объявляется исправленным данной правкой.

- 2026-09-23: PASS static/executable для REQ-011 — у четырёх M14 фиксированный normal Barrel, старые варианты нормализуются существующим LoadGame/NewGame обходом инвентарей через setter. M14 и ART сварены до recalc normals: двусторонний culling больше не теряет ложу/крепление, compiled HGM сохраняет грани (<0.03 мм). M21 Flashlight/FlashlightDot/Off сохраняют общий Mountside с GL. MkIII Hand_l_grip поднят к нижней поверхности. Runtime/editor/human остаются BLOCKED; offline исправление не закрывает игровые AC.

- Исправления 2026-09-22, **offline**, runtime повторно не запускался: EBR пересобран из правильных шести деталей Sage (старый экспорт пропускал две и путал карты), корпус/ART классики развёрнуты, MkIII отделён от запечённого обвеса. Собственные barrel normal/short/long, magazine у классики/MkIII, новые spots. Визуалы второго ванильного barrel/muzzle/mount убраны; M21 GL получил два отсутствовавших ApplyTo. `prepare_export_mesh` strict и AssetsProcessor прошли; quick items/metadata jazz+assets PASS. `AC-006` и `AC-008` остаются BLOCKED до чистой игровой проверки. Старые family-export/integrate не запускать поверх исправлений; использовать `_m14_repair_ebr.py`, `_m14_repair_classic.py` и `_m14_install_ebr_repair.py`.

- `JAZZ-WEAPON-M14-FAMILY-001-AC-001`: `PASS` static — `ModifyRightHandGrip` у `M14SAW`/`M21`; Stock visuals для этих ID пустые (ложка запечена в `JAZZ_M14`). `_validate_items_quick.py` exit 0.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-002`: `PASS` static — в `jazz_assets` хост `JAZZ_M14` и ART `JAZZ_M14_ART`; `M14SAW` и `M21` ссылаются на `JAZZ_M14`.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-003`: `PASS` static — `MK14EBR` в items/metadata/companion; Bobby in BR4 / RW 25 / Cost 20000. Иконка рендерится в том же change set.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-004`: `PASS` static — `JAZZ_M14_MkIII` зарегистрирован; `CanAppearInShop = false`; `GoldenGun` не менялся.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-005`: `PASS` static — новые ApplyTo магазинов EBR/уника с `Entity = ""`, без FAL/AR.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-006`: `BLOCKED` — runtime.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-007`: `BLOCKED` — human.

## Documentation delta

- После загрузки runtime обновить `docs/technical/weapons/data/*` генератором, wiki battle-rifle/sniper-rifle и showcase RU/EN. Пока runtime не загружен, current-state страницы не объявляют новые стволы существующими.

Дополнительный контроль 2026-09-22: compiled HGM round-trip для EBR, M14, ART и MkIII прошёл (<0.03 мм по центрам граней). Исправлена повреждённая иконка EBR прямым рендером восстановленной модели. Новые 13 Entity-записей приведены к читаемому аудитором многострочному формату: новых ошибок generated-sync относительно baseline нет. Старый AC-005 про пустой magazine у уника исторический: текущий MkIII имеет собственные MagazineNormal/Short; EBR сохраняет запечённый магазин.


Evidence 2026-09-26: AC-009: PASS static — Lua компилируется, Mountside присутствует у всех четырёх предметов; BLOCKED runtime/editor round-trip.

## Повторная игровая приёмка 2026-09-28

Решение владельца: approved; «дальше делай, вроде пока все».

- `JAZZ-WEAPON-M14-FAMILY-001-REQ-VISUAL-028` — М14: выделить встроенную планку в отдельную сущность JAZZ_M14_OpticsMount, показывать только с прицелом; M21 сохраняет крепление с ART. Сошки центрировать на газовой трубке. EBR: посадить Side/Under на RIS, убрать JAZZ_GrenadeLauncher_M14 из вариантов (старые экземпляры корректно снять через существующий setter). Переснять цветную иконку MkIII. Общая система покупных планок не входит в этот проход.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-VISUAL-028` — адресные static/compiled проверки и сопоставление до/после; игровая приёмка и editor save/reload отдельно.

Evidence: `JAZZ-WEAPON-M14-FAMILY-001-AC-VISUAL-028`: `BLOCKED` — изменения ещё готовятся; runtime не подтверждён.

Установка 28.09.2026: 19 файлов в jazz/jazz_assets, SHA256 исходников/backup/установленных файлов проверены. PASS static/compiled: планка 742 грани отдельно, lifecycle Scope/ART/remove/reinstall PASS; центр сошек на газовой трубке и EBR RIS проверены крупными планами. M203 удалён из items+companion и снят setter/migration harness. MkIII RGBA-иконка цветная (871 цветной непрозрачный пиксель). Полная сводка и ссылки — `docs/design/weapon-visual-feedback-20260927.md`. `AC-VISUAL-028`: static PASS; editor/runtime/human BLOCKED до новой приёмки владельца.


## Повторная приёмка 28.09.2026, второй проход

Решение владельца: после сбора замечаний и паузы команда «делай» разрешает реализацию сохранённого списка, без commit/push. Пауза снята.

- `JAZZ-WEAPON-M14-FAMILY-001-REQ-FEEDBACK-028B` — М14: исправить отсутствующую планку при установленной оптике, проверить реальные attachment spots. MkIII: отдельный прицел из исходного UNIQ (маркировка Truesight Mk IV 8x50), корректное крепление; это уточняет прежнюю замену донорской оптики штатной. Сохранить баланс до отдельного решения.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-FEEDBACK-028B` — static/compiled: корректный граф ресурсов и отсутствие регрессий; offline: сравнение до/после; runtime/human: повторить показанный владельцем сценарий.

Evidence `JAZZ-WEAPON-M14-FAMILY-001-AC-FEEDBACK-028B`: BLOCKED — реализация и повторная приёмка в работе. Установка только после подготовки кандидатов, проверок и закрытия игры. Новые рабочие скрипты `_weapon_feedback_*`, материалы приёмки и исходные write sets входят в этот проход.


Второй проход 28.09: [отчёт staging и открытых пунктов](../../design/weapon-visual-feedback-20260928-round2.md). Проверенные кандидаты подготовлены отдельно; установка/runtime/editor NOT_RUN. Статус approved сохранён. HAV и 6Б3 не приняты по эксперименту с весами и исключены из транзакции.

28.09.2026, после «игра закрыта, применяй»: проверенный пакет второго прохода установлен, 27 файлов и backup SHA256 PASS; installed graph/structural PASS. Новых generated ERROR нет; общий baseline остаётся FAILED. HAV/6Б3 исключены из установки, runtime/editor/human остаются NOT_RUN. По последующему запросу разрешены локальные коммиты; push не разрешён.

## Уточнение владельца 03.10.2026

Approved: «у м14 не хватает металика ... чутка», «у м14 мк3 ... дырки в прицеле», «да».
- `JAZZ-WEAPON-M14-FAMILY-001-REQ-FINISH-031`: проверить и адресно восстановить поверхности прицела MkIII по исходному OBJ, сохранив UV/посадку/материал; немного усилить metallic только металлических частей обычного M14, сохранив дерево, Base и Normal. Скрипт `_weapon_feedback_scope*` и `_weapon_feedback_finish*`, существующие mesh/RM/fallback входят в write set.
- `JAZZ-WEAPON-M14-FAMILY-001-AC-FINISH-031`: исходный/экспортированный mesh и winding сопоставлены; RM проверен по каналам с backup; игровая приёмка отдельно. Пока NOT_RUN.
