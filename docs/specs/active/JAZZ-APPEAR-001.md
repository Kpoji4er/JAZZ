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
approved_by: project-owner (current conversation, 2026-09-15; vanilla torso+helmets + test units, 2026-09-19; withdraw SpecOpsBody, 2026-09-19)
---

# JAZZ-APPEAR-001: броня на теле Легиона и тестовый юнит

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

## Evidence

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
