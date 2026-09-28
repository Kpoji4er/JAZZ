# Entities и ресурсы

## Оружейная приёмка 28.09.2026

`JAZZ_M14_OpticsMount` зарегистрирован в jazz_assets: items.lua, metadata.entities/code, `Entities/JAZZ_M14_OpticsMount.lua/.ent`, `Entities/Meshes/JAZZ_M14_OpticsMount_Mesh.m.hgm`. Использует существующий материал `JAZZ_M14_Mesh.mtl`; новых DDS/материалов нет. 742 грани выделены из корпуса M14 и включаются Scope visuals. Также заменены HGM AKR_AK103, JAZZ_M14, JAZZ_VZ58_GripWood и spots JAZZ_M14/MK14EBR. Контракт и evidence: [оружие](weapons-ammo-components.md). Офлайн compiled/winding/normals проверки пройдены, runtime/editor acceptance открыта.


## АК-74М / АК-105: тон материалов 27.09.2026

Локально скорректированы существующие `jazz_assets/Entities/Textures/AKR_AK74M_{2_Base,3_RM,5_Base,6_RM}.dds`, `AKR_AK105_{2_Base,3_RM,5_Base,6_RM,8_Base,9_RM,11_Base,12_RM}.dds` и их одноимённые `Fallbacks/` (24 файла). Asset contract, ссылки материалов, геометрия и регистрации не менялись.

АК-74М: roughness +0.08 на металле / +0.16 на пластике, base color ×0.85 / ×0.90. АК-105: roughness −0.035 на металле / +0.08 на пластике; base color ×1.30 +4/255 / ×1.12 +2/255. Плавная маска определяется каналом metallic; сам metallic сохранён. Это приближение общего тона по скриншотам владельца, не подтверждённое совпадение в игре.

Инструмент: `docs/tools/_tune_ak_polymer_materials.py`, backup/staging/report: `tmp/ak-material/tune-v1/`. Коррекция BC1 endpoints во всех mip-уровнях без повторного сжатия; заголовки, размеры, mip-цепочки и alpha сохранены. Static PASS: 24 DDS, неизменные G/B RM, ссылки только из материалов этих двух семейств. Проверка в игре, в руках и на земле не выполнялась; runtime/human acceptance открыта. Повторный export исходных моделей потребует повторного переноса этой коррекции: исходные Blender/TGA не изменялись.

## Связанные specs

- `JAZZ-ASSETS-001` — исправление collision-регрессии `HMMWV` и structural quality gate для Entity.
- `JAZZ-ASSETS-003` — первый собственный character element (`JazzHat_SSh68`) и воспроизводимый маршрут Blender → entity.

## АК-103: native-ресурсы от 26.09.2026

**Текущий вариант 27.09.2026 — оригинальная крышка `ksk` и перепечённые normal maps:** после уточнения владельца восстановлена крышка `model_9` с родным комплектом `ksk`. Исходный шейдинг перепечён под пересчитанные экспортные нормали пяти модулей; оба положения приклада используют одну карту. В экспортной сцене custom normals отсутствуют. Сборка 33514 треугольников с одним прикладом, body 19000; прежние spots и ID. Шесть HGM geometry/winding PASS, максимальная ошибка вершин 0.02590 мм. Оба бока и крупные планы проверены offline: ложные волны вокруг углубления приклада исчезли. Установлены и сверены по SHA256 58 файлов, включая две иконки; backup: `Weapons/_ak103_rebake_20260927/rebased/repair-install-backup`. Установка выполнена после закрытия игры владельцем; свежая runtime/editor-приёмка ещё не выполнена.

Предыдущие варианты того же дня — однотонная восстановленная крышка и подогнанная крышка АК-74М — заменены оригиналом с подтверждённой картой `ksk`. Ограничение чрезмерного блеска (roughness floor 0.44, магазин/приклад 0.52) сохранено. `items.lua`, `metadata.lua` и контракт EntityData эта установка не меняет; заменены ресурсы существующих entity.

Оптимизация внутренней геометрии отменена по решению владельца 26.09.2026: исходная native-сборка до замены крышки имела 33514 треугольников с одним прикладом. Удаление внутренних деталей не возвращалось. Испытания оптимизации остаются историческими evidence в `JAZZ-WEAPON-AK103-001`.

По `JAZZ-WEAPON-AK103-001` установлены шесть существующих `AKR_AK103*` entity в `jazz_assets/Entities`, оригинальные PBR-текстуры из архива владельца и две иконки в `jazz/WeaponIcons` и `jazz/WeaponComponents/Magazine`. Native UV перепакованы в атласы; каждый entity использует один материал. ID, баланс, pivot и spots сохранены.

Граф материалов, DDS/fallback, привязки компонентов и иконки прошли static-проверку. Strict mesh-audit сообщает degenerate для прежней почти коллинеарной грани корпуса: индекс 1964 вместо 1708 донорского варианта, расхождение вершин после квантования 0.00203 мм. Общий normals PASS не заявляется. Runtime A/B старой сборки подтвердил влияние normal map, но не приёмку новых ресурсов. Общий sync-gate assets до/после: 142 blocking / 14 warnings; не считать этот gate пройденным. Его regex пропускает однострочные AK103 ModItemEntity, хотя все шесть записей присутствуют.

## Назначение и эффект для игрока

`jazz_assets` хранит визуальный слой JAZZ: weapon/equipment/prop entities, meshes, materials и textures. Он не содержит `Code/` и не должен владеть балансной логикой, но его стабильные имена являются публичным контрактом для остальных трёх пакетов.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | EntityData schema, resource pipeline, states/spots, materials и rendering APIs |
| CommonLib | Прямого владения ресурсами JAZZ в проверенном срезе нет |
| JAZZ | 491 зарегистрированный Entity ModItem и несколько тысяч custom resources |

## Снимок ресурсов

Текущий `jazz_assets` содержит:

- 491 зарегистрированный `ModItemEntity`;
- 504 `.ent` и 504 entity Lua-файла на диске;
- **1370** top-level `Entities/Textures/*.dds` + **1356** `Textures/Fallbacks/*.dds` (у трёх DDS из `JAZZ-ASSETS-003` fallback появится после Mod Editor SaveWholeMod) (после JAZZ-ASSETS-002: numeric→`Entity_MapType`, unused purge, content-dedupe **только внутри одного map-suffix**; unused=0);
- 523 `.mtl` materials;
- 517 `.hgm` meshes;
- 511 `.mtlbin` compiled materials → после JAZZ-ASSETS-002 **16** оставшихся (без numeric paths); **495** stale `mtlbin` с путями на удалённые numeric DDS сняты, чтобы runtime читал актуальные `.mtl`. Полный rebuild `mtlbin` по-прежнему рекомендуется через Mod Editor SaveWholeMod;
- 114 folder ModItems;
- 22 `.bak` файла, требующие отдельной проверки как технический долг.

Контракт имён DDS (JAZZ-ASSETS-002): `<EntityOrPart>_{Base|Norm|RM|AO|SPEC|SI|Color}[_N].dds`. Инструмент: `$rename-jazz-weapon-textures` / `texture-audit-rename.ps1`. Отчёты: `jazz_assets/docs/texture-*.csv|txt`.

Разница 504 entity-файла на диске против 491 зарегистрированного означает 13 unlisted/orphan-candidate definitions. Это не доказательство мусора: они могут быть parent/variant/source remnants или использоваться непрямо. Удалять только после проверки metadata, inheritance и ссылок четырёх пакетов.

Structural audit дополнительно фиксирует 19 предупреждений в dormant/unlisted Entity:

- 18 ссылок на отсутствующие mesh/material-файлы;
- один коллинеарный collision-треугольник в `Entities/Chevy_S10_SM.ent`.

Шесть незарегистрированных имён при этом используются generated weapon visuals core-пакета: `M60E3BipodUnfld`, `M60E4BipodUnfld`, `M60_OldBipodFld`, `PKMDefMuzzle`, `PKMFoldBipod`, `PKMDefHandGrip`. Их нельзя активировать простым добавлением в metadata: M60-кандидаты ссылаются на отсутствующие material paths, а PKM-кандидаты — на отсутствующие mesh и material. Исправление требует отдельной согласованной транзакции core weapon presets + assets, editor round-trip и проверки оружия в руках/на земле.

## Контракт entity

Другие пакеты могут ссылаться на:

- entity name;
- state name;
- spot name;
- material/texture;
- путь `Mod/pDGDhr/...`;
- weapon component/attachment state;
- appearance или map prop variant.

Переименование entity/state/spot опаснее перемещения исходного арт-файла: ссылки хранятся в generated Lua, items, UnitData, appearances, maps и FX.

## Runtime flow

1. Entity ModItem регистрирует name и resource files.
2. Core InventoryItem/WeaponComponent/Appearance/FX указывает entity и state.
3. Unit/map создаёт объект.
4. `System_UnitAppearance.lua` переключает attachments, bipod, stock, magazine, mask и другие состояния.
5. Engine разрешает mesh → material → textures и spots для FX.

Ошибка на любом этапе может проявиться как invisible object, fallback material, missing state/spot или неверный attachment, не обязательно как Lua exception.

## Generated workflow

- Entity Lua и metadata генерируются/обновляются через Mod Editor и asset pipeline.
- Не править одну копию entity definition без проверки items/metadata.
- Не выполнять массовую нормализацию `.mtl`, `.ent` или generated Lua вместе с функциональным изменением.
- Проверять case-sensitive имена, даже на файловой системе Windows.
- Legacy absolute paths к исходным FBX присутствуют как технический долг. Не копировать личные корни в новую документацию; использовать `<ASSET_SOURCE_ROOT>` или относительную структуру.

## Межпакетные зависимости

- core использует entities оружия, брони, предметов, FX и UI icons;
- units использует appearances, equipment и voice-facing portraits/resources;
- maps использует props, environment resources, items и unit appearances.

Core metadata объявляет assets обязательной dependency (`pDGDhr`). Все entity ID должны оставаться стабильными для сохранений и generated maps.

## Проверка

- structural audit:

  ```powershell
  .agents/skills/sync-jazz-generated-data/scripts/check-asset-integrity.ps1 -SuiteRoot . -AssetsRoot ../jazz_assets
  ```

- audit блокирует XML/resource/collision дефекты зарегистрированных Entity; те же дефекты dormant/unlisted Entity остаются warnings до ownership-решения;
- self-test checker:

  ```powershell
  .agents/skills/sync-jazz-generated-data/scripts/check-asset-integrity.ps1 -SelfTest
  ```

- открыть/проверить все изменённые entities в Mod Editor;
- предмет в руках, на земле, в inventory и на unit appearance;
- attachment states: scope, magazine, bipod, folded stock, muzzle, mask;
- materials/textures в разных lightmodels/weather;
- map props и collision/spots;
- поиск `missing entity/state/spot/material/texture` в runtime log;
- проверить, что новые resources зарегистрированы, а удаляемые не имеют ссылок;
- отдельно аудировать `.bak` и 13 unlisted definitions без автоматического удаления.

Для `JAZZ-ASSETS-001` / `JAZZ-ASSETS-002` (`status: implemented`, 2026-07-31): `HMMWV.ent` — девять Unit-compatible state IDs, без вырожденных collision-треугольников; texture rename/purge/dedupe — unused=0, numeric DDS=0; human/runtime acceptance владельца (HMMWV + weapon texture smoke). M60/PKM dormant debt и полный Mod Editor `mtlbin` rebuild остаются отдельным сопровождением.

## Сопровождение

Изменение entity/resource обновляет эту страницу и профильную weapon/unit/map/UI-FX документацию. Изменение количества registered/on-disk entities требует обновить snapshot и причину расхождения.

## Character elements

С `JAZZ-ASSETS-003` в пакете есть один собственный элемент внешности: `JazzHat_SSh68`, класс `CharacterHat` (без суффикса пола, как vanilla `EquipmentBlood_Hat`). 827 вершин / 1374 треугольника, LOD1, state `idle`, без `<inherit>`. Не назначен ни одному юниту: существует как entity в dropdown Hat.

`CharacterHat` — жёсткий attach на спот `Head` (`AppearancePreset.HatSpot` default `"Head"`). Одежда (Body/Pants/Armor) — skinned, с `<inherit entity="Male">` и `hgskeleton`. Путать эти два маршрута нельзя: шапка в координатах тела плюс attach к Head улетает на рост выше черепа. Origin шапки — location кости `Bip001 Head`, без поворота кости. Экспортёр `axis_forward=Y`: +Y лицо, −Y затылок.

Исходники — `jazz_assets/Sources/Character/<Entity>/`, вне Steam-пака (`ignore_files` `*Sources/*`). Маршрут — skill `$export-jazz-character-element`.

Гайд по **новым building slab** (стена/пол/крыша, контракт имён, MVP отдельного мода) — [RU](../../design/ja3-how-to-custom-slabs.md) / [EN](../../design/ja3-how-to-custom-slabs.en.md). Это процедура автора, не loaded runtime JAZZ: своих `SlabMaterials` в комплекте нет.
