---
id: JAZZ-APPEAR-001
status: approved
owner: project-owner
systems:
  - visibility-weather-appearance
  - assets-entities
repositories:
  - jazz
  - jazz_assets
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/.agents/docs/playbooks/model-export-qa-handoff.md
  - jazz/docs/tools/_audit_blender_normals.py
  - jazz/docs/tools/*leather_armor*
  - jazz/docs/design/leather-armor-production.md
  - jazz_assets/Entities/JAZZ_LeatherArmor*
  - jazz_assets/Entities/Meshes/JAZZ_LeatherArmor*
  - jazz_assets/Entities/Materials/JAZZ_LeatherArmor*
  - jazz_assets/Entities/Textures/JAZZ_LeatherArmor*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_LeatherArmor*
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_LeatherArmor.lua
  - jazz/docs/tools/_weapon_feedback_*
  - jazz/docs/design/*visual-feedback*
  - jazz/docs/design/references/*feedback*/*
  - jazz_assets/Entities/Textures/[0-9]*.dds
  - jazz_assets/Entities/Textures/Fallbacks/[0-9]*.dds
  - jazz/docs/tools/*camo*
  - jazz/docs/tools/*specops*
  - jazz_assets/Entities/JAZZ_SpecOpsBody_Male.*
  - jazz_assets/Entities/Meshes/JAZZ_SpecOpsBody*
  - jazz_assets/Entities/Materials/JAZZ_SpecOpsBody*
  - jazz_assets/Entities/Textures/JAZZ_SpecOpsBody*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_SpecOpsBody*
  - jazz-units/UnitData/JAZZ_Legion_SpecOpsTest.lua
  - jazz-units/AppearancePreset/JAZZ_Legion_SpecOpsTest.lua
  - jazz/items.lua
  - jazz/Code/System_LegionArmorVisuals.lua
  - jazz/metadata.lua
  - jazz/ArmorIcons/ImprovisedCuirass.png
  - jazz/ArmorIcons/Chainmail.png
  - jazz/ArmorIcons/TireBrigantine.png
  - jazz/ArmorIcons/TireArmor.png
  - jazz/docs/specs/active/JAZZ-APPEAR-001.md
  - jazz/docs/design/equipped-armor-appearance-map.md
  - jazz/docs/design/legion-armor-production.md
  - jazz/docs/technical/systems/visibility-weather-appearance.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-units.md
  - jazz/docs/showcase/en/legion-units.md
  - jazz/docs/tools/*armor*
  - jazz/docs/tools/armor-hgm-reader/**
  - jazz/docs/tools/README.md
  - jazz/.agents/docs/index.md
  - jazz/.agents/docs/playbooks/legion-armor-modeling.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/JAZZ_ArmorFitV5*
  - jazz_assets/Entities/Meshes/JAZZ_ArmorFitV5*
  - jazz_assets/Entities/Materials/JAZZ_ArmorFitV5*
  - jazz_assets/Entities/Textures/JAZZ_ArmorFitV5*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_ArmorFitV5*
  - jazz_assets/Entities/JAZZ_ImprovisedCuirass_Male.*
  - jazz_assets/Entities/Meshes/JAZZ_ImprovisedCuirass_Male*
  - jazz_assets/Entities/Materials/JAZZ_ImprovisedCuirass_Male*
  - jazz_assets/Entities/Textures/JAZZ_ImprovisedCuirass*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_ImprovisedCuirass*
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_Chainmail.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_TireBrigantine.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_TireArmor.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_Twaron*.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_Guardian*.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_Zylon*.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_Flak*.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_IBA*.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_6B3.lua
  - jazz/docs/tools/_model_6b3_vest.py
  - jazz/docs/tools/_rig_6b3_vest.py
  - jazz/docs/tools/_qa_6b3_vest.py
  - jazz/docs/tools/_install_6b3_vest.py
  - jazz/docs/tools/_fit_meshy_6b3_armor.py
  - jazz_assets/Sources/Character/JAZZ_6B3_Male/**
  - jazz_assets/Entities/JAZZ_6B3*
  - jazz_assets/Entities/Meshes/JAZZ_6B3*
  - jazz_assets/Entities/Materials/JAZZ_6B3*
  - jazz_assets/Entities/Textures/JAZZ_6B3*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_6B3*
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_UniformCap.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_ConstructionHelmet.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_AdrianHelmet.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_SovietHelm.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_M1Helm.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_Stahlhelm.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_PASGTHelm.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_6b7Helm.lua
  - jazz-units/UnitData/JAZZ_Legion_ArmorTest_*Helm*.lua
  - jazz/docs/tools/_install_vanilla_armor_visuals.py
  - jazz_assets/Entities/JAZZ_Twaron*
  - jazz_assets/Entities/JAZZ_Guardian*
  - jazz_assets/Entities/JAZZ_Zylon*
  - jazz_assets/Entities/Meshes/JAZZ_Twaron*
  - jazz_assets/Entities/Meshes/JAZZ_Guardian*
  - jazz_assets/Entities/Meshes/JAZZ_Zylon*
  - jazz_assets/Entities/Materials/JAZZ_Twaron*
  - jazz_assets/Entities/Materials/JAZZ_Guardian*
  - jazz_assets/Entities/Materials/JAZZ_Zylon*
  - jazz_assets/Entities/Textures/JAZZ_Twaron*
  - jazz_assets/Entities/Textures/JAZZ_Guardian*
  - jazz_assets/Entities/Textures/JAZZ_Zylon*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_Twaron*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_Guardian*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_Zylon*
  - jazz_assets/Entities/JAZZ_Chainmail_Male.*
  - jazz_assets/Entities/JAZZ_TireBrigantine_Male.*
  - jazz_assets/Entities/JAZZ_TireArmor_Male.*
  - jazz_assets/Entities/Meshes/JAZZ_Chainmail*
  - jazz_assets/Entities/Meshes/JAZZ_TireBrigantine*
  - jazz_assets/Entities/Meshes/JAZZ_TireArmor*
  - jazz_assets/Entities/Materials/JAZZ_Chainmail*
  - jazz_assets/Entities/Materials/JAZZ_TireBrigantine*
  - jazz_assets/Entities/Materials/JAZZ_TireArmor*
  - jazz_assets/Entities/Textures/JAZZ_Chainmail*
  - jazz_assets/Entities/Textures/JAZZ_TireBrigantine*
  - jazz_assets/Entities/Textures/JAZZ_TireArmor*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_Chainmail*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_TireBrigantine*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_TireArmor*
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - editor state
approved_by: project-owner (current conversation, 2026-09-15; vanilla torso+helmets + test units, 2026-09-19; withdraw SpecOpsBody, 2026-09-19; 6B3 flatten+rig+install+test unit, 2026-09-20)
---

# JAZZ-APPEAR-001: броня на теле Легиона и тестовый юнит

## Полная переделка кустарного сета, 2026-09-26

Решение владельца в текущей беседе: кираса сделана хорошо; остальные три модели полностью переделать. Владелец отдельно подтвердил конструкцию ниже ответом «Да, делай так». Это разрешение реализации, не художественная приёмка будущего результата. Старые иконки этих трёх предметов больше не являются обязательным силуэтом; REQ-020 сохраняет IDs, mapping и тестовые юниты.

- JAZZ-APPEAR-001-REQ-026 — Пересобрать Chainmail, TireBrigantine, TireArmor: кольчуга с читаемым проволочным плетением, двумя самостоятельными грудными пластинами и напашником; бригантина из широких шинных полос на кожаных креплениях; тяжёлая шинная броня из крупных сегментов протектора с защитой плеч и предплечий. Различимые силуэты, функциональные крепления, износ по материалам. Кираса и её rig/source/resources/icon сохраняются без изменений. Прежнюю регулярную сетку блоков, рамку на груди и общую форму рубашки не воспроизводить как конечный дизайн.
- JAZZ-APPEAR-001-AC-026 — human: отдельная художественная приёмка трёх новых моделей по крупным front/back/side/oblique рендерам и игровому масштабу; static/executable: нормали, валидные веса до четырёх костей, CPU-позы и свежий экспорт; runtime: посадка на LegionGoon в standing/crouch/prone/aim, сохранение конечностей и штатных частей. Offline PASS не закрывает human/runtime.

Ownership и write set: существующие три семейства ресурсов jazz_assets и три ArmorIcons из заголовка; новый генератор и инструменты проверки в jazz/docs/tools/*armor*, README, эта spec и design/legion-armor-production.md. Исходные blend, рендеры и отчёты — в отдельной внешней папке armor-prototype; исходники кирасы не перезаписывать. На первом этапе создаются reviewable модели, затем bake/export/backup/install существующих ресурсов. Новые ID, баланс, локализация, юниты и load order не требуются. Exclusive: исходные и выходные файлы этих трёх моделей; общие items/metadata не менять при сохранении resource graph.

Evidence AC-026: PASS static/executable/export/install для пробной `rebuilt-20260926-v8`: 30 файлов с backup/hash verification; 23260/31092/48656 triangles, Base/Norm/RM 2048, strict normals, 4 CPU poses + elbows для TireArmor, Male export, согласованный ресурсный graph и test loadouts. Рендеры front/back/side/oblique и posed views сохранены вместе с editable/compiled sources. BLOCKED human/runtime — окончательная художественная и игровая приёмка не выполнена; крайний синтетический наклон показывает зазоры у части креплений, веса reference-shirt приблизительные. Spec остаётся approved, а не accepted/implemented. Общий read-only audit assets до установки: 144 errors / 13 warnings, вне точечной проверки трёх доспехов; их registration/loadouts PASS до и после замены. Cross-repo изменения не закоммичены.

Уточнение владельца после первых превью 2026-09-26: пояс кольчуги выглядит странно; грудные пластины должны иметь несущие ремни и явные крепления. Остальные модели выглядят слишком простыми, нужны конструктивные детали и последующий осмотр в игре. REQ-026 дополнен мягким прилегающим поясом, ременной подвеской пластин, пряжками/строчкой/боковой стяжкой и деталями крепления шин. Первые рендеры не приняты как финал. Варианты v1–v5 остаются внешними кандидатами, не устанавливать их как завершённую работу.

Повторный круговой аудит v8 по запросу владельца: **AC-026 FAIL visual уже в rest pose**. Ремни проходят сквозь плечи/спину одежды, кольчуга имеет открытые щели на плечевых/рукавных швах, её нижняя подвеска не сходится с поясом; у шинных моделей рукава пересекают верхние боковые кромки, есть чрезмерные зазоры и отделённый крепёж. Прежнее описание дефектов только как зазоров при крайнем наклоне неполно. Доказательства: внешняя партия `rebuilt-20260926-v8/VISUAL-AUDIT.md`, по четыре дополнительных ракурса `all-side-audit/`. Численный PASS структуры/экспорта не отменяет FAIL визуальной сборки. Аудит не изменял установленные модели.

## Проблема

Надетая кираса не представлена на теле. Созданный Blender-прототип ещё не является игровой entity. Старый неутверждённый scope Head/Wardrobe заменён текущим решением владельца.

## Цели

Показывать модель предмета из Torso в appearance-части Armor только для UnitData ID с префиксом JAZZ_Legion_. Импортировать новую самодельную кирасу, поставить её рендер на существующую иконку, добавить тестового юнита с кирасой и MP40.

## Non-goals

Все мерки, vanilla Legion без префикса JAZZ_Legion_, AME, незамапленные шлемы, очки/NVG/маски, штаны, бронеплиты; Female; Scale/Offset/Steroid; автоматическая подгонка всех тел; включение тестовых юнитов в кампанию; изменение баланса; покупка или установка Wardrobe. Полное отсутствие пересечений с произвольной одеждой не заявляется.

## Требования

- JAZZ-APPEAR-001-REQ-021 — Явное напоминание владельца 2026-09-16 сохраняет в установочном scope Twaron/Guardian/Zylon. Для каждой семьи: Light/Medium/Full из Torso и Legs/HeavyLegs из Legs; 15 entities `JAZZ_<family><variant>_Male`, 15 одноимённых `JAZZ_Legion_ArmorTest_<family><variant>`. Только текстуры различаются между семьями; пять общих наборов геометрии из Heavy Armor Vest. Уточнение владельца: Zylon использует классический четырёхцветный woodland по предоставленному образцу; процедурный шумовой камуфляж заменён. Twaron — оливковый, Guardian — тёмно-серый. Существующие иконки этих предметов уже сделаны с донора и сохраняются. Нагрудник использует parts.Armor, поножи — свободную штатную анимируемую часть parts.Shirt (Origin); baseline сохраняется независимо для каждой части. Штатные Pants/Body/оружие не заменяются. В тесте поножей также надет Light-нагрудник той же семьи, MP40 и 120 FMJ. Runtime/editor acceptance остаётся обязательной открытой проверкой владельца. Текущая установка по уточнению владельца: сначала 9 нагрудников Light/Medium/Full; Light без шеи/пояса/напашника, Medium с ними, Full дополнительно с наплечниками. 6 поножей остаются следующей партией.

- JAZZ-APPEAR-001-REQ-020 — 2026-09-16 владелец явно поручил доработать Chainmail, TireBrigantine, TireArmor, установить их и подготовить разные тестовые юниты. Для этой партии добавить три Torso→Armor mapping к одноимённым JAZZ_*_Male entities, три тестовых юнита с существующим LegionGoon/MP40/120 патронов. Сохранить кирасу. Текстуры и геометрия следуют текущим иконкам; физические high-poly кольца не экспортировать. Проверка модели/весов/экспорта и согласованности регистрации обязательна; runtime/editor приёмка остаётся открытой до ручного запуска владельцем. Twaron/Guardian/Zylon остаются отдельной незавершённой партией, не регистрировать неготовые meshes.

- JAZZ-APPEAR-001-REQ-023 — 2026-09-19 владелец снял LDW full-body прототип: `JAZZ_SpecOpsBody_Male` плохо заригован. Удалить entity и ресурсы из `jazz_assets`, тестовые `JAZZ_Legion_SpecOpsTest` UnitData/AppearancePreset из `jazz-units`, и все записи items/metadata/companion. Не оставлять orphan. Не регистрировать заново, пока не будет отдельно утверждённый полный Body. `_rig_specops_model.py` оставить как source-only tooling, не как установленный ассет.

- JAZZ-APPEAR-001-REQ-022 — 2026-09-19 владелец утвердил ванильные строки из design-таблицы для JAZZ_Legion_ Male: пять Torso (FlakM1955/M69, IBALight/IBA/IBAFull) и четырнадцать mapped Head (UniformCap, ConstructionHelmet, AdrianHelmet, SovietHelm, M1Helm, Stahlhelm, PASGTHelm, 6b7Helm, Twaron/Zylon/Guardian Helm и Heavy). Torso остаётся parts.Armor/Origin; шлемы — parts.Hat со штатным Head-spot и Hide Hair; mesh лица parts.Head, Shirt, оружие и статы не заменяются. Общие меши различаются C1/C2/C3 из таблицы. Без AttachEntries, без мод-опции, без Female/Scale/Offset. По тестовому юниту на предмет, группа JAZZ Tests, MP40, вне боевых пулов.

- JAZZ-APPEAR-001-REQ-024 — 2026-09-20 владелец поручил уплощить магазинные подсумки 6Б3, заригать жилет и установить его. Entity `JAZZ_6B3_Male` (`CharacterArmorMale`, `parts.Armor` / Origin), mapping `JazzArmor_6B3` → эта entity только для `JAZZ_Legion_` Male, тестовый `JAZZ_Legion_ArmorTest_6B3` с LegionGoon / MP40 / 120 FMJ, группа JAZZ Tests, вне боевых пулов. Существующая иконка `ArmorIcons/6b3.png` сохраняется. Colorization mask в эту установку не входит: запечённая олива. Предмет и баланс не меняются. Runtime/editor приёмка остаётся открытой.

- JAZZ-APPEAR-001-REQ-001 — gate по unitdatadef_id с точным префиксом JAZZ_Legion_, а не affiliation или appearance. Стартовый mapping: JazzArmor_ImprovisedCuirass → JAZZ_ImprovisedCuirass_Male, Male; только Torso. Остальные предметы/пол безопасно сохраняют baseline.
- JAZZ-APPEAR-001-REQ-002 — обновление при смене экипировки, appearance, spawn/load; отсутствие дубликатов; снятие или перенос в Inventory восстанавливает исходную Armor-часть. Голова, оружие, одежда и статы не заменяются.
- JAZZ-APPEAR-001-REQ-003 — использовать штатную AppearanceObjectPart в parts.Armor с Origin и синхронизацией скелетных состояний. Интеграция в CommonLib UpdateItemAppearance с единственным JAZZ-wrap. При отсутствии API или entity безопасный no-op.
- JAZZ-APPEAR-001-REQ-004 — импорт из прототипа v2: текстуры запечены, skeleton inheritance Male, EntityData class_parent CharacterArmorMale, все слои ModItem/metadata/resources согласованы.
- JAZZ-APPEAR-001-REQ-005 — отдельный JAZZ_Legion_ArmorTest в jazz-units: фиксированный male appearance, надетая JazzArmor_ImprovisedCuirass, MP40, совместимый боезапас. Не добавлять его в encounter/squad/loot pools. Имя теста использует существующую строку Recruit, технический ID и comment отличают его в редакторе.
- JAZZ-APPEAR-001-REQ-006 — заменить содержимое ArmorIcons/ImprovisedCuirass.png рендером модели с прозрачностью и прежним размером; сохранить существующие Icon/T ID.

## Инварианты и ограничения

Нет новых мод-зависимостей, боевых RNG, изменений баланса или persistent save state. Старый draft option default-off не активируется. AttachEntries на предметах не добавляются. Замапленные ванильные шлемы используют parts.Hat, не parts.Head. Файлы других задач сохраняются. Исходники и пути локальной установки игры не попадают в runtime metadata.

- JAZZ-APPEAR-001-REQ-007 — По запросу владельца от 2026-09-15 заменить мелкие пластины и круглый наплечник крупными сваренными листами железа, угловатым наплечником, швами и заплатами; улучшить посадку и обновить иконку с рендера. Доступна проверка через DAP без перезапуска игры. Пригодность для всех тел и анимаций Легиона требует отдельной проверки.

## Acceptance criteria

- JAZZ-APPEAR-001-AC-020 — три новые кустарные брони проходят CPU skin/pose QA, штатный экспорт, проверку ресурсов и согласованную установку; три уникальных тестовых UnitData имеют правильные armor/MP40/120 FMJ в companion и ModItem. Результат 2026-09-16: PASS static/executable/install, `soft-final-v5`, installed-check.json; 40 файлов установлены с backup и SHA256. Runtime/editor/human остаются NOT_RUN, поэтому общая игровая приёмка spec не закрыта.

- JAZZ-APPEAR-001-AC-023 — после удаления нет `JAZZ_SpecOpsBody_Male` / `JAZZ_Legion_SpecOpsTest` в items.lua, metadata.lua, companion, entities/code/resources трёх пакетов; бинарные mesh/mtl/dds удалены; runtime/code не ссылается на эти ID. Историческая запись в этом spec и `_rig_specops_model.py` не считаются установкой.

- JAZZ-APPEAR-001-AC-024 — offline: уплощённые магазинные подсумки, CPU skin QA, bake/export/AssetsProcessor, согласованная установка `JAZZ_6B3_Male` и `JAZZ_Legion_ArmorTest_6B3`; executable mock применяет entity на `JAZZ_Legion_` Male и не трогает merc; items/metadata/companion совпадают; иконка `6b3.png` не перезаписана. Runtime/editor/human остаются обязательными.

- JAZZ-APPEAR-001-AC-022 — executable mocks и isolated generated-graph: пять ванильных Torso и четырнадцать Head применяют нужные Male-entity и цвета; смена предметов с общим мешем меняет tint; снятие восстанавливает baseline Armor/Hat и Hair; merc/AME/vanilla Legion/Female не меняются; 19 тестовых UnitData имеют Head или Torso loadout, MP40 и 120 FMJ, группа JAZZ Tests, записи items/metadata/companion совпадают.

- JAZZ-APPEAR-001-AC-001 — executable mock tests: только JAZZ_Legion_ prefix, Male и Torso; invalid/missing entities, merc/vanilla/AME исключены.
- JAZZ-APPEAR-001-AC-002 — executable mock tests: повторное обновление, equip/unequip, перенос в Inventory, пересоздание appearance, baseline restore и цепочка CommonLib без рекурсии.
- JAZZ-APPEAR-001-AC-003 — static/export: compiled entity mesh + baked textures, inheritance, metadata/items/companion, icon size/alpha, UnitData и loadout.
- JAZZ-APPEAR-001-AC-004 — runtime/editor/human: тестовый юнит спавнится с кирасой и MP40, броня двигается в standing/crouch/prone/aim; снятие восстанавливает baseline; save/reload.

## Impact и совместимость

Runtime-владелец jazz, меши jazz_assets, юнит jazz-units. Latest CommonLib main проверяется в текущей задаче. Wrapper не меняет поведение его стандартных AttachEntries. Vanilla AppearanceObjectPart синхронизирует Armor с телом. Save-friendly, без добавления юнита на карты. Cross-package изменения незакоммиченные.

## План и ownership

Spec/аудит → bake/export/entity → runtime map → test UnitData → icon → static checks → доступные editor/runtime проверки. Exclusive ресурсы указаны выше. Reviewer: project-owner; game/editor закрыты на момент ручной транзакции.

## Решение владельца

2026-09-15: «надо сделать визуализатор брони на теле в слот брони ... пока только для юнитов jazz_legion»; дополнено просьбами о тестовом юните с этой бронёй и MP40 и об иконке с рендера. Это явное разрешение реализации текущего scope.

2026-09-19: владелец утвердил ванильный Torso-набор из design-таблицы, отдельно поручил добавить замапленные шлемы, оставить gate только для Легиона и сделать тестовые юниты. Это разрешение REQ-022.

2026-09-19: «SpecOpsBody кстати надо будет удалить - оно плохо заригалось». Это разрешение REQ-023: снять установленный full-body прототип и тестовый юнит.

2026-09-20: «подсумки кстати эти они ж под магазины / у тебя как будто слишком выпуклые / поправь и ригай в игру и делай юнита для теста». Это разрешение REQ-024.

## Evidence

- JAZZ-APPEAR-001-AC-024: PASS offline — `vest-6b3-v6-10`: подсумки 28 мм / power 6.5; 14 312 triangles, 4 influences; CPU pose PASS; bake/AssetsProcessor/stage PASS; installed 16 files with backup. `_check_legion_armor.py` PASS для mapping/entity/test unit; `ArmorIcons/6b3.png` не перезаписана. Runtime/editor/human NOT_RUN.

- JAZZ-APPEAR-001-AC-023: PASS — static: `JAZZ_SpecOpsBody_Male` / `JAZZ_Legion_SpecOpsTest` отсутствуют в items/metadata/companion jazz, jazz_assets, jazz-units; 11 файлов entity/mesh/dds/UnitData удалены; Code не ссылается. Editor/runtime reload NOT_RUN.
- JAZZ-APPEAR-001-AC-022: PASS — `python docs/tools/_check_legion_armor.py`: ванильные Flak/IBA tint и смена общего меша, хат PASGT→6b7, Hide Hair, restore, merc exclusion; 19 UnitData items/companion/metadata и Head/Torso loadouts. Runtime/editor/human NOT_RUN.
- JAZZ-APPEAR-001-AC-001: PASS — `python docs/tools/_check_legion_armor.py`: executable Lua mocks покрывают prefix, Male, Torso, invalid entity, unmapped, AME/merc/vanilla exclusions.
- JAZZ-APPEAR-001-AC-002: PASS — тот же тест: equip/unequip, Inventory, baseline restore, новая appearance, потеря weak cache при загрузке, повторный install/reload, возврат результатов CommonLib. Это mock evidence, не игровой прогон.
- JAZZ-APPEAR-001-AC-003: PASS — AssetsProcessor exit 0, 16 452 triangles, animated mesh, `Skeletons/Male_mesh.hgskel`; baked Base/Norm/RM 1024² и DDS/fallback pairs. Isolated executable graph check: ModItem/metadata/companion, exact UnitData gear, icon RGBA 110². `_validate_items_quick.py` PASS для трёх пакетов; wrap-cycle PASS. Процессор печатает диагностику несовпадения FBX/SDK versions, но завершает импорт и выдаёт HGM; runtime остаётся обязательным. Общий sync-аудит имел до изменения 891/22/81 ошибок для jazz/assets/units (в том числе tmp-копии и нераспознанные старые записи); исправление этого baseline не входит в задачу.
- JAZZ-APPEAR-001-AC-004: BLOCKED — запуск Steam дал retail `JA3.exe`, DAP :8165 отсутствует. Спавн/анимации/save/reload и editor round-trip не подтверждены. Spec остаётся approved до игрового acceptance; отсутствие пересечений не заявляется.

CommonLib main проверен: `f1e02404abcbfb5ba489a61f54bfdd8c26921912`, 1.11 build 1065; `FixAppearanceItems.lua` совпадает с ранее извлечённой Workshop-копией. Все три пакета незакоммичены.

## Documentation delta

Текущий mapping и ограничения в design/technical; уровень подтверждения отделён от runtime acceptance. Tooling сохранён в docs/tools. Player-facing страницы обновляются с явным указанием экспериментального покрытия Легиона.

## Итерация посадки 2026-09-15

Владелец подтвердил сварной вид; массовый выпуск остальных броней и юнитов отложен до хорошей посадки одного образца. Уточнение: грудную часть преждевременно считали проваливающейся по ракурсу; по замечанию владельца её размеры сохранены. Следующая итерация меняет ремни, неглубокий наплечник, профиль спины и снижает пятнистость материала.

DAP live eval на JA3Debug :8165 подтвердил двух JAZZ_Legion_ArmorTest, Armor entity, синхронизацию standing idle. Горячая замена через ReloadEntityResource требует виртуальный content_path Mod/<id>/, а не абсолютный путь диска. Визуально v3 загрузилась без перезапуска. Старый BLOCKED по отсутствию DAP снят; AC-004 остаётся частично проверенным: crouch/prone/equip/save/reload пока не подтверждены.

## Расширение по поручению владельца 2026-09-15

«Как доделаешь с этой броней — бери ее за образец и делай остальную броню», «часов 6». Куртки и кольчуга могут заменять одежду; реальные прототипы требуют реальных референсов. Это разрешение расширения. Сначала исправляется эталон, затем последовательные семейства Torso; по тестовому юниту на предмет, без боевых пулов. Конкретные новые файлы заносятся в write set до регистрации.

- JAZZ-APPEAR-001-REQ-008 — skinning эталона по официальному sample: ключицы/twist для лямок и наплечника, поверхность торса для спины; передний объём и материал сохраняются. Добавить пряжки лямкам.
- JAZZ-APPEAR-001-REQ-009 — каталог остальных Torso, пригодные существующие ассеты перед новыми, реальные референсы. Clothing replacement восстанавливает исходный Body/Shirt при снятии.
- JAZZ-APPEAR-001-AC-005 — веса нормализованы, максимум 4 влияния; CPU pose preview и отдельно runtime наклоны/руки. Blender preview не заменяет runtime.
- JAZZ-APPEAR-001-AC-006 — готовность и тестовые юниты по каждому семейству отдельно, без объявления всего каталога завершённым по эталону.

GPU crashes: причина не установлена; рендеры CPU, один Blender за раз. Без автоматического запуска/закрытия игры и горячей перезагрузки до выбора безопасного способа проверки.

v5: 11 452 triangles, source skin barycentric interpolation для спины/лямок/наплечника, до 4 весов; гладкие нормали панелей, пряжки лямок, CPU preview PASS. Установлена каноническая v5 с backup; игровая посадка v5 НЕ подтверждена. Попытка AsyncLoadAdditionalEntities отдельной копии предшествовала завершению JA3Debug: Access violation, read 0x8. Отдельная копия удалена адресно, без регистрации и сейва. Дальнейший runtime import запрещён в этой проверке; продолжение offline. Это не доказательство причины предыдущих GPU crashes.

JAZZ-APPEAR-001-AC-005: PARTIAL — v5 skin validation PASS, CPU synthetic lean preview PASS; actual JA3 runtime blocked after Access violation. JAZZ-APPEAR-001-AC-006: PARTIAL — catalog 38 Torso, 37 new staged test definitions execute loadouts; no new family installed. Source prototypes chainmail/brigantine/tire require art refinement, bake, skin validation and game acceptance.

## Offline QA-pass по поручению владельца 2026-09-15

Владелец запросил автоматизировать весь проход кирасы и затем самостоятельно запустить игру для пакетной проверки брони. Разрешены offline build, CPU renders, skin/attachment checks, bake/export/staging и адресная установка существующей кирасы с backup. Игра не запускается и ресурсы на ходу не загружаются.

- JAZZ-APPEAR-001-REQ-010 — воспроизводимый `docs/tools/_qa_legion_armor.py`: последовательные стадии с exit-code gating, JSON-отчёт, логи, хеши ресурсов и список ручной игровой приёмки. Нет PASS для непроверенных JA3-поз; source-only семейства не объявляются установленными.
- JAZZ-APPEAR-001-AC-007 — offline QA-pass сохраняет результаты skin/геометрии/креплений в нескольких синтетических позах, baked resource graph и icon; ошибочная стадия останавливает установку. Исправления нижней кромки и лямок проверяются отдельно.

Latest human evidence: владелец показал v5 в игре, в целом принял внешний вид, указал светлый артефакт нижнего края спины и оторванные крепления лямок. Это не полная приёмка всех анимаций. Семейства: сохранить вид кольчуги, устранить пересечения; бригантина и шинная броня должны следовать ArmorIcons и кустарному африканскому Legion/Mad Max направлению, без принятия текущих заготовок.

JAZZ-APPEAR-001-AC-007: PASS offline — qa-v6-03 completed model/4 CPU pose regressions/bake/export/compile/stage/graph/install/hash checks; canonical v6 installed on disk with backup. 11 528 triangles, 6030 source vertices, max4 weights; maximum tested anchor gap 0.00776 m, bottom-rim stretch 0.9997–1.0004. Runtime NOT_RUN. Earlier failed passes stopped before install. Guide/extraction/sample audit authorized by latest owner request for developer tutorial + vanilla research; video contents remain unavailable, local developer docs and sample verified.

2026-09-15 continuation: user reported rear straps on v6 and clarified Legion appearance overrides reuse vanilla models. v7 rear ribbon rails follow the back plate, anchor signed-distance gate added. qa-v7-01 PASS_OFFLINE, installed on disk with backup, runtime NOT_RUN. JAZZ appearance roster: 222 unit/preset pairs, 117 presets, 53 Body, unresolved 0; no all-body fit claim. Developer video automatic captions obtained/read; guide updated with timestamps and distinction from frame inspection.

Offline continuation: all 53 JAZZ Body geometries imported through calibrated HGM parser; 5 front/back reference renders. Real clothing intersections found on EquipmentBiff_Top and Faction_Rebels_Top_Heavy. Full body/pose acceptance remains NOT_RUN; Bip001 root group mapping unresolved for imported animation, so affected reference meshes are rest-only. No active assets changed after v7.

## Heavy Armor Vest: утверждённый донор

Owner-approved LDW follow-up (superseded 2026-09-19 by REQ-023): supplied LDW generic military archive was a continuous soldier mesh with balaclava and tactical vest. It was briefly bound as `JAZZ_SpecOpsBody_Male` + isolated `JAZZ_Legion_SpecOpsTest`. Owner withdrew it: the rig is not acceptable. Do not reinstall these IDs. Keep the US Soldier 2 archive for a separate uniform task.

Latest owner direction: stop further fit/rig iterations and prepare nine clean Blender files only. Approved source-only deliverable: original donor geometry in Light/Medium/Full, Twaron/Guardian/Zylon materials, packed textures, separate editable components, no deformation/rig or game installation. Completed with `_prepare_clean_hav_blends.py`; nine files saved in the owner's HAV_Blender_Clean asset directory. Existing game fit acceptance remains open; this deliverable does not replace installed resources.

Владелец предоставил Heavy Armor Vest.zip и явно назначил его основой всех нагрудников и поножей Twaron, Guardian, Zylon: разные комплектации через нарезку и отдельные цветовые варианты. Это расширяет прежний Torso-only производственный scope на поножи этих трёх семейств; перед runtime-регистрацией новые IDs/файлы должны быть добавлены в write set. AIM не входит.

Кольчуга, бригантина и шинная броня должны быть близки к существующим иконкам по конструкции и силуэту. Остальную броню также сверять с иконками; реальные прототипы — дополнительно с реальными референсами.

Donor archive inspected: 3 OBJ (1520 / 3874 / 9640 triangles) + 14 PNG. OBJ reference model_0/1/2.mtl, but MTL files are absent; materials require reconstruction and rigging requires JA3 sample weights. Imported/read does not mean game-ready.

2026-09-18: owner rejected HAV rear clearance and authorized morphing existing models. Correct all nine torso configurations against actual LegionGoon shirt geometry; retain existing entity/item/test IDs and material families. Mandatory front/back/side/oblique fitting views, posed views with explicitly approximate reference-shirt weights, numerical rear inner-surface clearance and existing skin/export gates. Game acceptance remains open. Initial measurement: original rear median 92.8 mm, p95 128.4 mm; candidate median 23.3 mm, p95 29.0 mm. This is rest-pose evidence on NPCCostumeMale_Shirt_08, not approval for every Legion body or game animation.

Evidence 2026-09-18: heavy-fit-v2 nine models PASS rest rear clearance, skin and shared geometry hashes across material families; 81 existing binary resources replaced with backup and verified hashes. Installed registration/loadout checks PASS for all nine IDs; metadata and companions unchanged. Runtime NOT_RUN. Full guard/sleeve overlap remains visible in approximate clothed lean rendering and requires native animation verification; this pass fixes torso rear clearance, not every clothing intersection.

2026-09-18 follow-up: heavy-rig-v3 installed at owner's explicit request to replace entities on disk and restart the game manually. All nine torso variants rebuilt; 81 resources backed up and replaced; installed hashes, entity registration, skin and test loadouts PASS. Torso binding now follows cuirass-style front/back transitions after morph, preserving rigid arm guards; collar height and upper shoulder volume reduced. Live read before installation found body/armor scale 100 and matching animation states/phases. New resources were not hot-reloaded; runtime acceptance remains NOT_RUN pending owner restart. Backup and installation manifest are in the external armor-prototype/heavy-rig-v3 output. IDs, icons, metadata and companions unchanged.


## Советская каска СШ-68 и комплект тестового 6Б3, 2026-09-22

Повторное исправление 2026-09-23 разрешено владельцем после дефекта A01 в игре. Продолжение REQ-024: тоньше чехол/плечи, тканевая вариация и швы, три карты 2048, skin от реальной Shirt08 со сглаживанием и проверкой rest skeleton по v7. Бюджет 17000 треугольников допускает непрерывные геометрические швы; финал 16520. Установлена сборка `vest-6b3-revision-20260923-v3`, девять ресурсов с backup; ID, icon и тестовый loadout с СШ68 сохранены. PASS static: четыре синтетические позы, веса не более четырёх, HGM round-trip <0.1 мм. BLOCKED runtime/human: отрыв спины и плеч в настоящих анимациях, соответствие референсу и пересечения ещё требуют игры. HAV не изменялся в этом проходе и не принят.

Решение владельца в текущей беседе: использовать установленную `JazzHat_SSh68` для советской каски и добавить каску тестовому юниту 6Б3. Это утверждённое уточнение REQ-022/024. Scope: existing runtime mapping, existing UnitData и документация; исходный mesh 6Б3 только осматривается, не исправляется. Новые ID, баланс, локализация, экспорт и общий generated-sync baseline не входят. Ресурс уже получен в jazz_assets `ca0db8f`.

- JAZZ-APPEAR-001-REQ-025 — `JazzArmor_SovietHelm` использует `JazzHat_SSh68` (CharacterHat, Head-local, без Male inherit) через parts.Hat только у JAZZ_Legion_ Male, с hide_hair и собственной текстурой без старого tint. `JAZZ_Legion_ArmorTest_6B3` экипирует также этот предмет в Head; 6Б3, MP40, 120 FMJ и LegionGoon сохранены. Одинаковое изменение в items.lua и UnitData companion; metadata registration уже существует.
- JAZZ-APPEAR-001-AC-025 — static/executable: mapping и ресурс доступны, serialized и companion loadouts совпадают и экипируют Torso+Head+MP40/120 FMJ; runtime/human: посадка шлема, hide/restore Hair и снятие после reload модов остаются отдельной проверкой владельца.

Write set этого уточнения: `jazz/Code/System_LegionArmorVisuals.lua`, `jazz-units/UnitData/JAZZ_Legion_ArmorTest_6B3.lua`, `jazz-units/items.lua`, текущая spec, design mapping, technical visibility-weather-appearance, wiki legion-global-ai и showcase ru/en legion-units; профильный существующий `_check_legion_armor.py` и его README при адаптации проверок. Exclusive: jazz-units/items.lua. Нового editor save нет: игра закрыта, применяется контролируемая ручная транзакция; round-trip пока недоступен.

- JAZZ-APPEAR-001-AC-025: PASS static/executable — `_check_legion_armor.py` проверил mapping СШ-68 без tint, Hide Hair, и оба представления Head+Torso/MP40/120 FMJ; `_validate_items_quick.py ../jazz-units` PASS. Runtime/editor/human BLOCKED: игра не запускается по указанию владельца; посадка и round-trip не проверены. Общая spec остаётся approved: незавершённую приёмку остальных моделей не закрываем этим локальным изменением.

### Разрешённое исправление приёмки, 2026-09-22

Владелец разрешил исправление подтверждённых дефектов после оружия: отрыв спины/плеч HAV, высокая посадка СШ68, полная переделка 6Б3 по присланному фронтальному фото с новыми материалами. Эталон рига — сохранённая кираса v7. Работа по одному предмету, без возврата SpecOps; исходники и backup отдельно. Offline gate не закрывает runtime. Приоритет удалённого HAV соблюдён при pull; теперь правятся только согласованные дефекты текущих моделей.

Результат offline 2026-09-22: девять HAV установлены с изменёнными весами верхней спины/плеч, геометрия/UV не изменены; кости сверены с v7. СШ68 получает additive Hat offset −40 game units (4 см), lifecycle mock без накопления и утечки на другие шлемы. 6Б3 пересобран под фото: горловина, верхние виниловые усиления, длинные подсумки, уклон плеч по Shirt08; новые Base/Norm/RM, плавный skin field. Финальная сборка `vest-6b3-reference-20260922-v4`, 15624 треугольника; strict normals, четыре CPU pose и HGM round-trip PASS (<0.1 мм). Установлено девять ресурсов; тестовый 6Б3 остаётся с СШ68. Все runtime AC, включая HAV, остаются BLOCKED до чистого запуска владельцем.


## Ремонт после приёмки 2026-09-26

Решение владельца: «правь», для Guardian/Twaron/Zylon только текстуры; 6Б3 переделать целиком последним. АК-103 заменён другим агентом и исключён. Геометрию и веса девяти HAV сохранить из remote b485065.

- JAZZ-APPEAR-001-REQ-027: исправить упаковку RM 21 DDS девяти HAV: R=roughness исходного G, B=metalness исходного B. Подтверждено сравнением пикселей: Guardian ошибочно дублирует metalness в RGB, Twaron/Zylon — roughness. Сохранить albedo, normal, UV и авторскую геометрию. Добавить отсутствующие fallback для 84 DDS, на которые ссылаются эти девять entities. Числовой write_set ограничен данным графом ссылок, без массовой правки других текстур.
- JAZZ-APPEAR-001-AC-027: static — соответствие R/B исходникам, mipmaps и 64px fallback, неизменность geometry/material/normal/base; runtime — новые материалы в тех же Aim-позах без прежнего глянца. Runtime BLOCKED до нового запуска владельцем.
- JAZZ-APPEAR-001-REQ-028: полная переработка 6Б3 под присланное фото: тканевый чехол, усиления и длинные плоские подсумки; материал и риг по проверенным принципам v7 с примеркой Shirt08. Offline не закрывает игровую посадку.


Evidence 2026-09-26: AC-027: PASS static — 21 RM заменены из исходных G/B, 84 fallback созданы, 92 защищённых файла сохранили SHA256. Ошибка BC7 относительно исходного канала менее 0.48/255; полные mip chains 12/13 уровней. BLOCKED runtime: игру не запускали.

Уточнение владельца 2026-09-26: силуэт 6Б3 уже похож, основной дефект — жёваные плечи. Не расширять корпус вслед за промежуточным замечанием о квадратной форме; переделать плечевые накладки и регулируемые ремни с люверсами по последнему фото. Фото пользователя является главным образцом; дополнительные фотографии https://forum.guns.ru/forummessage/374/2811504.html использованы только для устройства ремня/пряжки.

Evidence REQ-028 / existing AC-003, AC-004 (6Б3 only): shoulders-v3-20260926 installed, 9 resources with backup. 16856 triangles, custom normals absent, four synthetic poses PASS (deep lean p99 1.721 < 1.8), compiled geometry <0.1 mm from source. Continuous interpolated shirt skin field, skeleton rest checked against v7. Human/runtime BLOCKED; other armour work in this shared spec is not marked complete.


### Исправление кустарной партии v19, 2026-09-26

Продолжение REQ/AC-026 по указанию владельца «правь кустарные моделки». Установлена `rebuilt-20260926-v19`: 30 файлов трёх прежних сущностей и иконок, backup и SHA256 до/после. Исправлены разомкнутые швы, UV низа кольчуги, подвеска щитка/пояса, утопленные лямки, посадка крепежа и верхние кромки шинных моделей. Веса одежды взяты из настоящей Shirt_08; детали используют общий поверхностный skin field.

PASS static/export/install: 22300/33744/49840 triangles, Base/Norm/RM 2048, strict normals, CPU pose structure, HGM round-trip <0.1 мм, registration/loadouts. По 16 clothed diagnostic views. Полная визуальная приёмка **не закрыта**: у кольчуги в twist_back сохраняется дефект левого рукава, на крайних позах есть отставание ремней/плечевых деталей. Runtime NOT_RUN, human PENDING. Численные проверки не означают отсутствие клиппинга. Evidence: внешние `rebuilt-20260926-v19/REPAIR-REPORT.md`, visual-review.json и installation.json. Кираса и 6Б3 не изменялись в этом проходе. Контракт ID/mapping/поведения/баланса не менялся; wiki/technical не требуют изменения. Spec остаётся approved.


## Уточнение 6Б3 по четырём ракурсам 2026-09-27

Владелец дал https://sbox.game/mapperskai/ar_6b3 и четыре изображения, затем «сделай также». Утверждённое продолжение REQ-028: цельные тонкие плечи, округлая горловина, мягкие передние детали; широкий верхний задний карман с клапаном, поясной ремень и небольшие боковые задние подсумки вместо нижнего центрального кармана. Согласованный общий силуэт сохранить. Материалы с тканевой вариацией и складками. Авторская сборка по визуальным референсам; существующий ID, loadout и иконка сохранены. По одному предмету, без запуска игры, commit/push; runtime/human acceptance отдельно от offline.

Evidence 2026-09-27 для REQ-028 / AC-003, AC-004 (только 6Б3): reference-v6 установлена, 9 ресурсов с backup и проверкой SHA256; 16460 triangles, max 4 skin influences, v7 rest skeleton, 4 CPU poses PASS (deep_lean p99=1.71855), strict normals 0 fatal, HGM round-trip max 0.09335 мм. Четыре studio-вида и отдельные baked front/back просмотрены. SourceUV сохраняется при rig/atlas bake; prepare_export_mesh выполняется перед bake и export; на выходе одна ExportUV. На увеличенном bake есть мелкие тёмные стыки кромок — runtime/human не закрыты. Assets generated baseline 142/13 до и после. Игра закрыта по прежнему разрешению владельца, не запускалась. Отчёт: внешний model-repair-20260927/repair-report.md.

Write set уточнения: _model_6b3_vest.py, _rig_6b3_vest.py, адресные ветки JAZZ_6B3_Male в _build_legion_armor.py, новый read-only _preview_baked_armor.py, tools README, QA handoff, эта spec и девять существующих ресурсов JAZZ_6B3 в jazz_assets. IDs/mapping/loadout/icon и asset paths не меняются; runtime contract не меняется, нового current-state wiki/showcase утверждения нет. Другие требования общей спеки не объявляются завершёнными.

## Цвета брони по обратной связи владельца, 2026-09-27

Явный запрос владельца утверждает продолжение визуального scope: кольчуга должна читаться светлее; Guardian — чёрный, Twaron — зелёный, Zylon — woodland. Применить к Light/Medium/Full.

- JAZZ-APPEAR-001-REQ-029: исправить только albedo существующих девяти HAV и Chainmail; кольца светлее промежутков, сохранить тканевые детали и прежний woodland-reference. Геометрия, UV, риг, Normal/RM, IDs и mapping неизменны.
- JAZZ-APPEAR-001-AC-029: static — адресный граф материалов, полные DDS mipmaps и fallback, backup/hash и неизменность защищённых ресурсов; offline — просмотр материалов/кольчуги; runtime/human — новая приёмка в игре, остаётся открытой до проверки владельцем.

Write set: существующие BaseColor DDS и Fallbacks этих десяти entity в jazz_assets; docs/tools/*armor*color*, _model_rebuilt_legion_armor.py (цвет исходных колец), tools README, эта spec и профильный playbook. Asset contract/path и gameplay не меняются. Нового утверждения о runtime acceptance в wiki/showcase нет.

Evidence AC-029, 2026-09-27: PASS static/offline — установлены 22 albedo DDS + 22 fallback (10 entity); сохранены SHA256 162 защищённых mesh/entity/material/Normal/RM ресурсов. Полные mip chains, sRGB и размеры сохранены, fallback ≤64 px. Средняя ошибка BC7 относительно native bake ≤0.254/255. Просмотрены Guardian/Twaron/Zylon на HAV vest и Chainmail на исходной геометрии с запечённым albedo. Backup, plan, installation, verification и четыре preview: `tmp/armor-colors-v1/`. Runtime NOT_RUN, human PENDING; игра не запускалась. Другие AC общей спеки не закрываются, status остаётся approved. Tools: _audit_armor_color_maps.py, _stage_armor_colors.py, _bake_armor_colors.py, _preview_armor_colors.py; docs README/playbook обновлены, локальная проверка документации PASS.


## Повторная приёмка 28.09.2026, второй проход

Решение владельца: после сбора замечаний и паузы команда «делай» разрешает реализацию сохранённого списка, без commit/push. Пауза снята.

- `JAZZ-APPEAR-001-REQ-FEEDBACK-028B` — Исправить пересечения спины HAV (общие формы Guardian/Twaron/Zylon), конструктивно соединить задние ремни кольчуги с креплениями, исправить отходящие плечи 6Б3. Проверять одетую модель в позах, не считать прошлый offline PASS игровой приёмкой.
- `JAZZ-APPEAR-001-AC-FEEDBACK-028B` — static/compiled: корректный граф ресурсов и отсутствие регрессий; offline: сравнение до/после; runtime/human: повторить показанный владельцем сценарий.

Evidence `JAZZ-APPEAR-001-AC-FEEDBACK-028B`: BLOCKED — реализация и повторная приёмка в работе. Установка только после подготовки кандидатов, проверок и закрытия игры. Новые рабочие скрипты `_weapon_feedback_*`, материалы приёмки и исходные write sets входят в этот проход.

### Кожаный нагрудник-плитник, 2026-09-28

Решение владельца: «мы из кустарной брони забыли ... кожанный нагрудник-плитник, делай)», приложена карточка существующего JazzArmor_LeatherArmor. Разрешена собственная Male Armor модель по ArmorIcons/LeatherArmor.png: округлый кожаный нагрудник, обод, карман под плиту, плечевые лямки, боковые ремни, грубая клёпка и потёртая коричневая кожа. Это продолжение кустарной партии, без изменения баланса, ID предмета, иконки или локализации.

- JAZZ-APPEAR-001-REQ-030: создать JAZZ_LeatherArmor_Male (CharacterArmorMale), сохранить Body, подключить существующий предмет через armor_entities и создать отдельный JAZZ_Legion_ArmorTest_LeatherArmor с MP40/120 FMJ, без боевых пулов. Изменения generated data одной транзакцией при закрытой игре; backup, контроль конкурентных правок. До этого staging вне runtime.
- JAZZ-APPEAR-001-AC-030: static/offline — clean/rigged sources, четыре вида, skin/pose QA, normals gate, штатный export, HGM round-trip, resource graph, согласованные ModItem/companion/metadata и mapping; editor/runtime/human — reload и осмотр на Легионе, стоя/пригнувшись/лёжа, снятие/надевание. Последний уровень отдельно, offline не означает игровую приёмку.

Exclusive resources: jazz_assets/items.lua и metadata.lua, jazz-units/items.lua и metadata.lua, существующая таблица armor_entities. Новых T IDs нет. Ownership: геометрия в jazz_assets, mapping/tools/docs в jazz, тестовый UnitData в jazz-units. Save/network/load-order и характеристики неизменны. Все изменения незакоммиченные; публикация не запрошена.

Уточнение владельца 2026-09-28: «Пока только подготовить модель». Текущий deliverable REQ-030 ограничен clean/rigged моделью, превью и offline QA в staging. Регистрация entity, mapping, тестовый UnitData и установка отложены по явному указанию владельца; игру не закрывать. AC-030 в текущем scope: геометрия, материалы, нормали, skin/pose QA; runtime части остаются NOT_RUN и не требуются для выдачи подготовленной модели.

Evidence AC-030, 2026-09-28, уточнённый source-only scope: `tmp/leather-armor-v3/`, clean 49 частей / 12126 triangles; rigged 6494 vertices, unweighted=0, max influences=4. Normals gate авторского TEST_LeatherArmor PASS (0 fatal), неизменённый reference body исключён из export audit. Rest/lean/deep_lean/twist PASS, p99=1.0002/1.2644/1.6857/1.4548 (<1.8). Первые кандидаты выявили угловатые лямки и влияние рукавов на боковые ремни; текущий smooth torso field исправляет оба источника. Materials/clothed исходные виды просмотрены; диагностический круговой осмотр выполняется отдельно. Состояние — source prepared; export/install/editor/runtime NOT_RUN по уточнению владельца, human acceptance PENDING. Generated/runtime пакеты не изменены. Общая spec остаётся approved из-за незавершённой приёмки остальных моделей.

- JAZZ-APPEAR-001-AC-030: PASS static/source/skin для уточнённого scope — финальный кандидат `tmp/leather-armor-v4/`, 12126 tri / 6494 vertices, normals 0 fatal, четыре позы PASS. Концы лямок посажены непосредственно на кожу с плавным переходом; anchor и panel используют единое поле весов. Export/install/editor/runtime NOT_RUN по указанию владельца. Текущая карточка: `docs/design/leather-armor-production.md`.

Общий Done validator 2026-09-28 не проходит для JAZZ-APPEAR-001: у прежних AC остаётся незакрытая приёмка, статус общей спеки approved. Это не подменяется успешным offline результатом кожаного исходника. Ready validator PASS.

Финальный offline visual review AC-030: v4 material views и clothed side/deep_lean_back/twist_front просмотрены после исправления anchor; 16 диагностических PNG сохранены. `qa-report.json`: PASS_SOURCE_OFFLINE, visual review со SHA256 исходника. Нормали/skin и подготовка модели завершены в согласованном scope; общая игровая приёмка не заявляется.

### Доработка и установка LeatherArmor, 2026-09-28

Владелец принял общий силуэт, указал плохой стык лямок и попросил повысить качество кожи. Разрешил установку, затем уточнил: «не запущена» (игра закрыта). Source-only ограничение REQ-030 снято для этой модели. Сохраняются форма, предмет, иконка, характеристики. Исправить всю площадку нахлёста лямок, добавить контактный QA на реальных pose-деформациях, улучшить skin grain/crease/roughness и запечь PBR 2048. Затем штатный экспорт, compiled audit и установка JAZZ_LeatherArmor_Male + isolated ArmorTest_LeatherArmor в ранее объявленные пути. Ручная транзакция при закрытой игре разрешена запросом установки; backup/hash/concurrent checks обязательны. Новая runtime/editor/human приёмка остаётся отдельной, игру не запускать автоматически.

- JAZZ-APPEAR-001-AC-030: PASS static/offline/install, 2026-09-28 — v5 установлен (16 файлов), весь нахлёст лямок пересчитан по mesh панелей; контакт 58 точек <0,5 мм во всех позах, skin/normals PASS. 11966 triangles, 6422 source vertices, 2048 Base/Norm/RM, одна ExportUV, HGM max error 0,0959 мм, winding PASS. Source detail и отдельные baked front/back просмотрены. Entity/ModItem/metadata/Male inheritance, serialized + companion loadout MP40/120 FMJ и mock equip/unequip/rebuild PASS. Backup/hash и сохранность предмета/иконки PASS. Assets baseline 142/13, units 81/0 до/после, новых ERROR нет. Локальный docs-check 7 Markdown PASS; handoff содержит 9 прежних абсолютных путей вне нового раздела, отдельная его проверка FAIL baseline. Editor round-trip/runtime/human NOT_RUN; запуск игры не выполнялся, релизная приёмка не заявлена. Общий статус approved сохранён для незакрытых AC остальных моделей. Все изменения незакоммиченные.


Второй проход 28.09: [отчёт staging и открытых пунктов](../../design/weapon-visual-feedback-20260928-round2.md). Проверенные кандидаты подготовлены отдельно; установка/runtime/editor NOT_RUN. Статус approved сохранён. HAV и 6Б3 не приняты по эксперименту с весами и исключены из транзакции.

28.09.2026, после «игра закрыта, применяй»: проверенный пакет второго прохода установлен, 27 файлов и backup SHA256 PASS; installed graph/structural PASS. Новых generated ERROR нет; общий baseline остаётся FAILED. HAV/6Б3 исключены из установки, runtime/editor/human остаются NOT_RUN. По последующему запросу разрешены локальные коммиты; push не разрешён.

## Meshy low-poly 6Б3, 2026-10-02

Уточнение после запуска в игре: владелец просит «плечи бы отвязать — а то странно смотрится». Разрешена правка skin плечевых лямок существующего Meshy 6Б3: исключить clavicle/arm/twist, продолжить плавное поле торса до верха. Геометрия, UV и внешний вид материалов сохраняются. Write set дополнен опцией `_rig_6b3_vest.py --torso-shoulders`, source/staging `meshy-20261002-torso-shoulders/`, README и этим evidence. Проверить четыре позы и изолированное движение рук/ключиц: броня не должна двигаться от этих костей; compiled audit и backup обязательны. Установка только после закрытия игры. Runtime/human повторная приёмка открыта.

QA tooling этого уточнения: `_check_soft_armor_poses.py --torso-only` и профильный playbook входят в write set. Пять поз PASS, isolated arms movement 0 м относительно evaluated rest; HGM 14802 triangles, max vertex error 0,09247 мм, winding PASS. DDS/fallback в staging скопированы из установленной версии для сохранения материалов. Подготовлен кандидат `meshy-20261002-torso-shoulders`; установка ожидает закрытия игры, runtime/editor/human новой правки NOT_RUN. Исходный внешний каталог armor-prototype исчез во время работы; повторный clothed audit недоступен без Shirt08 JSON, доступна проверка на sample body. HGM reader восстановлен из закреплённого исходника parser; исходник подготовленного кандидата сохранён в Sources.

Решение владельца: «импортни в игру» после просмотра multi-view Meshy-кандидата (task `01a0f974-6ad9-7565-80ab-cd96f804dfe3`, 14802 triangles). Это разрешение на подготовку, rig/export и обновление существующей entity, без новых ID, баланса, commit/push.

- JAZZ-APPEAR-001-REQ-MESHY-6B3: заменить геометрию и Base/Norm/RM существующей `JAZZ_6B3_Male` кандидатом Meshy; подогнать к Male/реальной Shirt08, сохранить полость, UV и характерные детали. Веса — штатный Male, максимум четыре влияния. Снять custom normals; проверить экспорт через официальный AssetsProcessor.
- JAZZ-APPEAR-001-AC-MESHY-6B3: PASS требует clothed rest/pose review, структурный skin gate, HGM round-trip, backup и hashes установки. Runtime/editor/human отдельно; синтетические позы не закрывают игровую приёмку.
- Scope/write set: `_fit_meshy_6b3_armor.py`, tools README, эта spec, текущие девять ресурсов `jazz_assets/Entities/**/JAZZ_6B3*`, редактируемые исходники `jazz_assets/Sources/Character/JAZZ_6B3_Male/`. Иконка, Item, test unit, mapping, metadata/items и прежние public paths сохраняются. Asset contract не меняется; загруженный runtime не объявлять обновлённым до перезапуска.
- Exclusive resource: только `JAZZ_6B3_Male` resource graph. Игра и debug сейчас открыты; владелец сообщил «Пока готовь, закрою позже». До закрытия — только source/staging, без установки и hot reload.
- Evidence: подготовка начата; export/install/runtime/editor/human NOT_RUN. Общая spec остаётся approved.

Evidence AC-MESHY-6B3, 2026-10-02: владелец сообщил «закрыл игру»; отсутствие JA3/JA3Debug подтверждено. Установлены девять существующих ресурсов с backup/hash, регистрация, item, icon, test unit сохранены. Build-root: `jazz_assets/Sources/Character/JAZZ_6B3_Male/meshy-20261002/`; `refresh-installation.json` содержит SHA256, `refresh-backup/` — предыдущую версию. 14802 triangles, 7257 welded source vertices, максимум четыре skin-влияния, четыре позы PASS (наибольший p99 stretch 1,63668), strict normals 0 fatal. Clothed rest/deep lean/twist и финальный baked front/back просмотрены; исходная UV сохранена после исправления тёмной точки от перепаковки. HGM geometry/winding PASS: max vertex error 0,09479 мм, все 14802 triangles сохранены. AssetsProcessor завершён с exit 0; лог содержит предупреждение несовпадения FBX/SDK и два сообщения о zero-length normals, при этом независимые source normals и compiled geometry/winding gates прошли. Generated audit до/после: тот же FAILED STRICT baseline из 14 warnings, новых предупреждений нет. Runtime/editor/human NOT_RUN; общая spec остаётся approved до игровой приёмки. Текущие technical/wiki/showcase обновлены с явным статусом ожидания проверки.

После «игру закрыл — включай, потом коммит» установлен torso-shoulders: девять ресурсов, backup и SHA256 PASS; материалы сохранены побайтно. Пять поз и compiled audit PASS; sample-body twist/deep-lean просмотрены. Повторная игровая приёмка NOT_RUN. Разрешены локальные коммиты jazz/jazz_assets с Revision +1, push не разрешён.
