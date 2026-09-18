# Броня и одежда Легиона: рабочий пайплайн и QA

Область: JAZZ Torso, сначала Male Legion. Это инструкция производства, а не заявление, что все семейства готовы. `qa-pass` ниже проверяет только явно перечисленные свойства; визуальная приёмка и JA3-анимации остаются отдельными этапами.

## Источники и уровень проверки

1. Официальный ролик [Blender exporter for Character Elements](https://www.youtube.com/watch?v=Gnx2LFTD51Q), предоставлен владельцем. Повторная попытка успешна: английские автосубтитры всего ролика получены и прочитаны. Разбор ниже основан на речи, кадры отдельно не проверены.
2. Локальная официальная документация: `<JA3_ROOT>/ModTools/Docs/ModItemEntity.md.html`, разделы Armature Weight Transfers, A Note on Materials, Sample Assets; `ModItemAppearancePreset.md.html`, Classes. Прочитана 2026-09-15.
3. Реальная сцена разработчиков: `<JA3_ROOT>/ModTools/Samples/Assets/SampleMaleModel/BlenderScene_Appearance.blend`. Проверена скриптом `_audit_legion_armor_sample.py`; это пригодный редактируемый донор скелета/весов.
4. Vanilla: адресно распакованы `Faction_Legion_Top_01..10` с двумя LOD, Male skeleton и соответствующие бинарные материалы. 71 файл, 3 633 750 байт; manifest с SHA256. Из штатного AppearancePreset получено 44 использования этих Body. Распаковка подтверждена, визуальный импорт HGM в Blender ещё не выполнен.
5. [HGM Viewer](https://github.com/mxtsdev/hgm-viewer) — найденный открытый просмотрщик/экспортёр HGM. Его README оставляет разбор hgacl и entities.dat в списке незавершённого. Не обещать автоматический перенос ванильных анимаций или восстановление всех материалов без проверки экспортированного GLB.

## 1. Выбрать правильную appearance-часть

| Тип предмета | Часть и класс Male | Что сохранять |
| --- | --- | --- |
| Кираса, отдельный жилет поверх одежды | Armor / CharacterArmorMale | Существующий Body, руки и кисти |
| Куртка, кольчужная рубаха, цельный шинный костюм | Body / CharacterBodyMale | Необходимые открытые руки/кисти/шея должны входить в новый комплект Body |
| Штаны | Pants / CharacterPantsMale | Совпадение шва с Body |

Официальный Shirt/CharacterShirtMale не используется для верхней одежды; документация предписывает Body. Не смешивать Male/Female inheritance в одном appearance. Бригантина может быть Armor при достаточном зазоре либо Body-комплектом; выбирать после проверки конкретного силуэта, не по названию предмета.

Body replacement должен сохранять исходный Body и восстанавливать его при снятии. Не оставлять прежнюю рубашку под плотной кольчугой. Нельзя удалить весь Body и ожидать, что голые руки появятся сами: в sample `top_hands` и `top_suit` — отдельные meshes под общим `Origin_top`.

## 2. Донор, масштаб, геометрия

- Работать в копии developer sample. Скелет `Bip001` сохранять; не переименовывать/перестраивать кости.
- Sample rig имеет `hgskeleton = Suit_mesh|BP_mesh`. Для нового экспорта указывать его собственные Entity_mesh; в нашей кирасе `JAZZ_ImprovisedCuirass_Male_mesh`.
- У `M_BaseMesh Skin_BIP` исходный Scale примерно 0.01, у rig 1.0. Сырые локальные координаты сравнивать нельзя: учитывать matrix_world и применять transforms на рабочих копиях до переноса весов. Слепое сравнение vertex.co ранее уже давало неправильную посадку.
- Донор одежды `top_suit`: 3559 vertices; LOD1 1800. `top_hands`: 1710 и LOD1 900. Один UV map, один Armature modifier к Bip001. Это факты sample-аудита, не универсальные бюджеты.
- Верхняя одежда должна иметь выкройку: горловина, проймы, длина рукава, низ и стык с Pants. Простая обрезка голого тела плоскостью — только блокинг; её края и плечи нельзя считать готовой одеждой.
- Для Armor учитывать толщину существующего Body. Проверять на реальных Legion tops, а не только голом sample. Размеры грудной пластины кирасы сохранять: владелец её посадку предварительно одобрил.
- Ремень заканчивается на пластине с нахлёстом и заклёпкой. Его конец нельзя повторно проецировать на голое тело: этим мы отрывали ремни от кирасы.
- Нижняя окантовка, края листа и приваренные детали должны иметь согласованные веса и достаточно близкую разбивку поверхности; иначе в наклоне возникают разрывы и светлые зубцы.
- Геометрические пересечения одежды исправляются формой, разделением Body/Armor и skinning. Collision surface их не исправляет: официальные Surface не анимируются.

## 3. Веса и движение

Официальный базовый метод: применить Scale обоим meshes; выделить source с Armature, затем target; Weight Paint → Transfer Weights; Source Layer Selection By Name, Vertex Mapping Nearest Vertex. Target должен получить тот же rig и группы.

Наш barycentric nearest-surface перенос — дополнительный метод, а не дословная инструкция разработчиков. На плечах важны clavicle и upper-arm twist; приклеивание всего наплечника к Spine2 недостаточно. Проверять веса до и после переноса. В sample встречаются 12–15 ненулевых групп на вершину, поэтому факт «взяли sample» не заменяет экспортную нормализацию. Наш QA требует максимум 4 влияния, сумму 1 и существующие кости.

Плотная ткань/кольчуга следует телу; жёсткие листы не должны складываться как ткань. Для кирасы нижний край спины сейчас использует общий непрерывный torso field. Это локальное исправление эталона, не универсальный skinning всех доспехов.

Проверять исходную позу, наклон, сильный наклон, скручивание, подъём плеча. Автоматический тест измеряет реальные полигоны пластин/лямок и растяжение нижней кромки. Потом обязательны игровые crouch/prone/aim/run/turn: локальные Euler-тесты не воспроизводят штатные JA3-анимации полностью.

## 4. Материалы и читаемость

Экспорт использует Haemimont Material. Произвольный Blender shader не переносится сам: Base/Normal/RM необходимо запечь и подключить в HGE. Одна UV-развёртка; исходные текстуры uncompressed TGA 24/32 bit. RM: R=roughness, B=metalness. DDS и fallback пары проверять после процессора. Альфа требует отдельного Use Alpha Test; не включать его без нужды.

Для кирасы: железо с толщиной, умеренный металлический отблеск, сварные швы, потёртые грани, ржавчина в стыках; кожа остаётся диэлектриком. Для резины: матовая выгоревшая поверхность и настоящий рельеф протектора, а не металлические плитки. Не превращать все края в одинаковую ярко-белую кайму. Проверять запечённый материал и модель в игре, а не только красивый procedural render.

Кольца кольчуги — high-poly bake source; не отправлять весь wire mesh в игру. Нужны low-poly garment, bake и проверка мелкого плетения с игрового расстояния.

## 5. Референс и кустарный африканский Legion

Основной силуэт — `ArmorIcons/Chainmail.png`, `TireBrigantine.png`, `TireArmor.png`; для реально существующего прототипа дополнительно брать реальные фото из первичного источника. Пользователь просит Mad Max: старые грузовые шины, проволока, неодинаковые ремни, ремонтные заплаты, грубая клёпка, пыль, выгорание. Асимметрия должна объясняться ремонтом/креплением; случайные шипы не заменяют конструкцию.

Бригантина: широкие горизонтальные полосы с коричневыми вертикальными креплениями/клёпкой. Предыдущая сетка 3×3 поверх кольчуги отвергнута. Шинная броня: глубокий протектор охватывает корпус, выражены плечи и защита рук; предыдущие плоские плитки отвергнуты. У кольчуги предварительно принят общий вид, но не пересечения и края.

## 6. Автоматический QA-pass

Команда и параметры: `docs/tools/_qa_legion_armor.py` в docs/tools/README.md. Выход — новый каталог на каждый запуск:

1. Model source с QA-разметкой компонентов и креплений.
2. Веса, существование костей, конечность координат; четыре CPU-позы × два ракурса.
3. Крепления до реальных полигонов железа и наличие кожи в креплении; растяжение нижней кромки.
4. Иконка из модели, bake Base/Norm/RM, HGE export и AssetsProcessor.
5. Проверка свежести compiled .ent, очистка src-путей при staging, DDS/fallback.
6. Lua mocks экипировки и lifecycle; ModItem/metadata/companion, класс, Male inheritance, mesh/material graph, PNG RGBA 110×110.
7. Только после gates: адресная установка существующих файлов с backup, повторный graph check, сверка SHA256.

Полный проход пока реализован для кирасы. Для каждой новой entity нужен такой же собственный отчёт и тестовый юнит. `PASS_OFFLINE` не означает human/style acceptance. Первый сбой QA остановил установку из-за отсутствующей QA-разметки; второй — из-за неверного ожидаемого ExportedEntities. Это исправлено, третий полный проход PASS.

AssetsProcessor выбирает ExportedEntities относительно экспортируемого FBX/конфигурации. Не брать старый .ent из похожего каталога: проверять путь из лога и свежесть. Ошибка FBX/SDK version может сопровождать успешный выход, поэтому проверять выходные файлы и последующий runtime отдельно.

Разработчики предупреждают: импортированный ресурс после re-export автоматически не обновляется. Здесь не использовать hot reload/AsyncLoadAdditionalEntities для приёмки: прежняя попытка предшествовала native crash. Пользователь запускает игру самостоятельно; не запускать JA3 напрямую.

## 7. Пакетная игровая приёмка

В манифесте различать source-only, staged, installed, runtime-checked, accepted. Сейчас установлен только `JAZZ_Legion_ArmorTest` для кирасы; 37 остальных test definitions staged, не зарегистрированы. Не создавать видимость готового набора через один общий mesh.

Для каждого готового предмета: собственный JAZZ Tests unit, нужная броня в Torso, MP40 + 120 подходящих патронов, без добавления в боевые пулы. Проверить несколько реальных Body Легиона, а не только один Goon. Осмотр standing/crouch/prone/aim/run, снятие/надевание, appearance rebuild, сохранение/загрузка, отсутствие дубликатов и восстановление прежнего Body/Armor. Записывать конкретный item/entity/body/pose и скриншот дефекта.

Открыто: визуальный разбор кадров developer tutorial; импорт извлечённых HGM с проверкой скелета/весов/материалов; окончательная выкройка остальных семейств; QA и игровые тесты каждого нового семейства.

## Уточнение по JAZZ и ролику, 2026-09-15

Внешность Легиона в JAZZ переделана пресетами из существующих игровых моделей. Список проверки строить из `jazz-units/UnitData/JAZZ_Legion_*.lua`, разрешая Preset сначала из vanilla AppearancePreset, затем с приоритетом ModItemAppearancePreset из jazz-units/items.lua. Не использовать только стандартные Faction_Legion_Top. `_audit_legion_armor_presets.py` нашёл 222 пары unit/preset, 117 пресетов, 53 Body; unresolved 0. Это статический список для будущей примерки, НЕ 53 проверенных посадки.

Подтверждения из речи [developer tutorial](https://www.youtube.com/watch?v=Gnx2LFTD51Q):

- 02:15–03:43: rig, reference body, отдельные Origin для верха/низа; Armature и группы вершин.
- 07:39–09:26: одного Armature недостаточно; выбрать donor, затем vest, Transfer Weights → By Name, проверить движение.
- 09:34–11:26: устранить ошибки экспортёра, выбрать Male inheritance; для показанного жилета Mesh назвать `mesh`.
- 12:13–13:28: импорт entity, save/test, класс CharacterArmorMale и назначение в appearance preset.
- 13:49–14:06: экспортированный пример ещё не подогнан; посадку доводят изменением mesh и повторным импортом.

v7: задние концы лямок подняты над железом, оба края ленты повторяют поверхность пластины. QA измеряет также знак расстояния крепления: близость к поверхности изнутри больше не считается успехом. Полный offline pass выполнен, v7 установлена на диск с backup; runtime ещё не проверен.

## Реальная геометрия пресетов: следующий offline этап

Из Meshes.hpk адресно извлечены все 53 Body из нашего roster (54 файла LOD0 из-за дополнительных mesh). Сохранён headless HGM JSON reader, использующий внешний MIT parser `mxtsdev/hgm-viewer` commit bbcd41c6d1416fcfe8e98dd3a75ffa6e90a9904c. Сравнение compiled кирасы с исходником даёт среднюю ошибку 0.040 мм, максимум 0.092 мм на выбранных вершинах: bbox center + (x,y,z) → (-y,-x,z).

В Blender импортированы 53 Body; сохранены сцена и по два ракурса пяти показательных верхов. Это только исходная поза и однотонный материал геометрии; не восстановление штатных текстур/анимаций. Root group Bip001 из части HGM не совпадает с костями sample: веса сохраняются, но Armature для таких мешей отключён до корректного сопоставления. Не выдавать их за готовые анимированные доноры.

Визуальные findings: NPCCostumeMale_Shirt_08 (наш тестовый LegionGoon) приемлем по нагруднику в исходной позе; наплечник/перемычки проверять на рукаве. EquipmentBiff_Top пересекает нагрудник и лямки. Faction_Rebels_Top_Heavy содержит собственные ленты/экипировку и существенно перекрывает спину. Требуются варианты посадки или сохранная замена Body; единый overlay нельзя объявить совместимым со всеми 53 верхами.

Ресурсы активной игры на этом этапе не менялись; установлена v7. Процедура `_preview_armor_jazz_bodies.py` дополняет базовый QA эталона проверкой реальных форм одежды.

## Снятый full-body прототип

`JAZZ_SpecOpsBody_Male` и `JAZZ_Legion_SpecOpsTest` сняты (плохой риг, REQ-023). Не ставить эти ID снова без нового утверждения полного Body.

## Heavy Armor Vest: подготовка донора

После отклонения деформаций heavy-rig-v3 владелец запросил только девять чистых Blender-вариантов. Использовать `_prepare_clean_hav_blends.py` от `heavy-armor-variants/modular-source.blend`, без fitting/rebind/export цепочки. Выход `HAV_Blender_Clean`: три комплектации × три материала, компоненты отдельными объектами, текстуры packed, исходная геометрия и UV сохранены; никаких armature, shape keys или деформирующих модификаторов. Это исходники для ручной доработки, не новая игровая установка.

Дополнение владельца: нужны сцены на тестовом теле в одежде, пригодные для последующего рига. `_prepare_hav_rig_scenes.py` создаёт подпапку `RigReady`: официальный Bip001 в REST, тело sample с исходными весами, статическая геометрия LegionGoon Shirt08 без прежних приблизительных весов. Armor остаётся неизменённой, отдельными unbound-объектами; сцены показывают исходные зазоры/пересечения и ещё требуют ручной посадки. В каждом blend есть START_HERE.txt. Не выдавать подготовку сцены за завершённый риг.

`docs/tools/_preview_armor_vest_source.py --textured` восстанавливает отсутствующие MTL: model_0 (пояс) Base3/Normal1/Rough0G/Metal0B; model_1 (жилет) Base7/Normal5/Rough4G/Metal4B; model_2 (дополнительная защита) Base10/Normal9/Rough8G/Metal8B. UV-соответствие проверено рендером; PNG упакованы в blend. Это реконструкция по атласам и названиям каналов, не исходный MTL.

`docs/tools/_prepare_heavy_armor_variants.py` делит связанные острова на vest/belt/collar/groin/arms/thighs/shins, сохраняя UV и материалы. Ремни бёдер находятся в том числе близко к центральной оси: одной проверки abs(x) недостаточно; нижние острова ремней должны остаться с thighs. Проверять Legs отдельно. Комплектации общие у Twaron/Guardian/Zylon; между семействами только текстуры, как явно уточнил владелец. Не создавать разные меши семейства ради отличий.

## Экспорт кольчуги, бригантины и шинной брони

`_qa_soft_legion_armor.py` последовательно запускает модель, `_check_soft_armor_poses.py`, общий `_build_legion_armor.py` с `--entity/--mesh-prefix/--icon`, штатный AssetsProcessor и staging. Только затем `_install_soft_legion_armor.py --apply`, `_check_soft_legion_armor.py` и общий lifecycle mock. Дальнейшая игровая приёмка остаётся за владельцем; программа не запускает игру и не выполняет live reload.

Основа оболочки — геометрия футболки NPCCostumeMale_Shirt_08, с весами, интерполированными по ближайшему треугольнику официального тела. Панели и их крепления получают веса по треугольникам самой оболочки через радиальный луч: nearest-vertex по всему телу ошибочно захватывает руки. Отдельное аналитическое распределение Spine для ремней тоже отклонено — расходилось с движением ткани. Продольные ремни подразделять по высоте (шаг до 15 мм), иначе длинный quad не сгибается вместе с корпусом.

Первые soft-production и soft-production-v2 не устанавливать: рендеры выявили отрыв ремней и чрезмерное растяжение. PASS только нормализованных весов недостаточен. Сохранять восемь ракурсов на модель, p99 растяжения, status/runtime и журнал компиляции. Wire high-poly остаётся опциональным bake reference; игровые материалы запекаются в 1024 atlases, не экспортировать физические кольца как тысячи отдельных объектов.

Опциональный `--body` импортирует точную геометрию JAZZ Body для первоначальной примерки Light спереди/сзади. Пока без весов и анимации, без установки в игру. Финальная посадка, остальные две текстуры и экспорт остаются отдельными этапами.

`_fit_heavy_armor_vest.py` сохраняет отдельный кандидат Light: исходный HAV выше плеч LegionGoon, низ пересекает живот. Первичная подгонка: корпус шире/глубже, ниже на 75 мм, верхняя передняя часть вынесена наружу, плечи подняты относительно корпуса на 25 мм. Эти значения относятся только к NPCCostumeMale_Shirt_08 в исходной позе; не распространять автоматически на все Body или остальные защитные модули. Модульный донор остаётся неизменным.

### HAV woodland material correction

Use `_model_heavy_legion_armor.py` for all three material families. Zylon requires `--woodland` pointing to the owner-provided classic four-colour pattern, packed unchanged into the source blend. Physical X/Z projection preserves reference aspect ratio at 1.8 m width; retain donor fabric details and normal/roughness maps. Preview is not runtime acceptance. Twaron/Guardian/Zylon of a given configuration must have identical geometry hashes. Medium examples are under the external armor-prototype/heavy-production/<family>Medium/source directory. Remaining work: pose QA, baking/export, runtime registration and test units for all 15 variants.

HAV torso QA: `_qa_heavy_legion_armor.py` builds nine Light/Medium/Full configurations. Update the view layer after appending the official skeleton before reading body world coordinates; otherwise transferred weights incorrectly select the feet. Torso plates use broad normalized spine/pelvis transitions; disconnected arm guards use their nearest arm bone, with an additional elbow pose for Full. `_install_soft_legion_armor.py --heavy-torso` stages/registers all nine with the runtime map atomically and preserves icons. Verify with `_check_soft_legion_armor.py --heavy-torso`. These CPU checks do not prove clothing clearance in game.

### HAV rear-gap correction, 2026-09-18

Follow-up rig QA: `_rebind_heavy_armor.py` and `_qa_heavy_rebind.py` work from fitted v2 sources, never from their own output. Bind torso after morph; lower torso sides must not inherit nearby arm weights. Nearest-surface transfer on thick sleeves can select ribs and independently animated twist helpers: it failed synthetic lean checks. Keep disconnected rigid limb panels on their existing main arm bones; use cuirass-like front/back fields for torso and smooth shoulder transitions. Geometry adjustments lower the collar above 1.49 m and reduce upper shoulder width/depth, rather than scaling the full shell through the garment. Synthetic PASS is not game fit acceptance.

Twaron/Guardian/Zylon are material variants of just three torso geometries. The rebinding runner executes pose QA/renders once per Light/Medium/Full, then requires exact geometry and skin signatures (weights, topology, skeleton rest matrices and object transforms) before reusing that report for another color. Store report provenance; do not repeat nine identical pose suites. Baking material variants and validating their installed references remain separate tasks. The legacy full donor builder predates this optimization; use the rebinding runner for fitted-source updates.

Live refresh is allowed only when explicitly requested: `_refresh_heavy_armor_fit.py --apply --live` retains backups and changes existing resource graphs only. Obtain the actual mount from `Mods[id].content_path`; the official `CommonLua/Classes/ModItem.lua` import path calls `ReloadEntityResource(dest_filename, "modified")` after copying each mesh/material/texture. Use a game-time thread and inspect the result. Do not use `AsyncLoadAdditionalEntities` for this update (a previous attempt accompanied a native crash). Entity/state/phase equality was observed for existing HAV and cuirass test units before rebinding; equality alone does not prove correct skeletal weights.

**Последующая игровая обратная связь:** владелец показал отрыв верха спины/плечевых частей HAV в боевой позе и оценил риг кирасы как существенно лучший. Морфинг исходной позы не закрыл проблему skinning. Не считать HAV принятым по offline PASS. Эталон для сравнения — сохранённая кираса v7 (`qa-v7-01/source/improvised_cuirass_v7.blend`) и `_model_legion_armor.py`, без перезаписи эталона.

Подтверждённые различия в коде: у кирасы `sample_bind` интерполирует веса ближайшего треугольника официального sample (с clavicle/twist, до четырёх влияний). Грудь использует `torso_bind`; спинка — `back_bind`: Spine1 до z=1.15, плавный переход к sample до z=1.24, выше sample. Нижняя кромка и пластина используют согласованное поле. Лямки получают веса пластины в точках крепления, веса sample на плече и интерполяцию между ними; наплечник использует surface binding. HAV вместо этого назначает torso/воротнику Gaussian-поле четырёх костей по одной высоте, а островам защиты рук — одну доминирующую кость. Это кандидаты на причину отрывов, а не доказанный единственный источник ошибки. Следующая правка должна сравнить результат в той же игровой позе; не копировать численные высоты кирасы на другую геометрию без проверки.

Owner rejected the installed HAV rear fit. Uniform depth scale 1.16 had left a median 93 mm gap to the actual LegionGoon shirt; front-only previews and no-render pose checks missed it. `_morph_heavy_armor_fit.py` samples the original Light inner shell against the calibrated NPCCostumeMale_Shirt_08 garment, constructs a smoothed radial displacement field, and applies it to all torso components while preserving thickness and UVs. Fade outside the torso keeps arm guards out of the morph cage. Do not apply the morph twice: always start from the original modular build.

Require four clothed rest views (front/back/side/oblique), two approximate clothed lean views, and rear inner clearance gates (minimum > -3 mm, p95 < 35 mm). Shirt pose weights are transferred from the official sample and explicitly do not claim recovered native shirt weights. `_qa_heavy_legion_armor.py --shirt ... --reference-armor ...` enables this gate for all nine configurations; `_refresh_heavy_armor_fit.py` updates existing resources only after all pass. Keep original builds and a resource backup. These checks do not cover every Legion body.
