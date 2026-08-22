# Entities и ресурсы

## Связанные specs

- `JAZZ-ASSETS-001` — исправление collision-регрессии `HMMWV` и structural quality gate для Entity.

## Назначение и эффект для игрока

`jazz_assets` хранит визуальный слой JAZZ: weapon/equipment/prop entities, meshes, materials и textures. Он не содержит `Code/` и не должен владеть балансной логикой, но его стабильные имена являются публичным контрактом для остальных трёх пакетов.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | EntityData schema, resource pipeline, states/spots, materials и rendering APIs |
| CommonLib | Прямого владения ресурсами JAZZ в проверенном срезе нет |
| JAZZ | 490 зарегистрированных Entity ModItems и несколько тысяч custom resources |

## Снимок ресурсов

Текущий `jazz_assets` содержит:

- 490 зарегистрированных `ModItemEntity`;
- 503 `.ent` и 503 entity Lua-файла на диске;
- **1367** top-level `Entities/Textures/*.dds` + **1356** `Textures/Fallbacks/*.dds` (после JAZZ-ASSETS-002: numeric→`Entity_MapType`, unused purge, content-dedupe **только внутри одного map-suffix**; unused=0);
- 522 `.mtl` materials;
- 516 `.hgm` meshes;
- 511 `.mtlbin` compiled materials → после JAZZ-ASSETS-002 **16** оставшихся (без numeric paths); **495** stale `mtlbin` с путями на удалённые numeric DDS сняты, чтобы runtime читал актуальные `.mtl`. Полный rebuild `mtlbin` по-прежнему рекомендуется через Mod Editor SaveWholeMod;
- 114 folder ModItems;
- 22 `.bak` файла, требующие отдельной проверки как технический долг.

Контракт имён DDS (JAZZ-ASSETS-002): `<EntityOrPart>_{Base|Norm|RM|AO|SPEC|SI|Color}[_N].dds`. Инструмент: `$rename-jazz-weapon-textures` / `texture-audit-rename.ps1`. Отчёты: `jazz_assets/docs/texture-*.csv|txt`.

Разница 503 entity-файла на диске против 490 зарегистрированных означает 13 unlisted/orphan-candidate definitions. Это не доказательство мусора: они могут быть parent/variant/source remnants или использоваться непрямо. Удалять только после проверки metadata, inheritance и ссылок четырёх пакетов.

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

Гайд по **новым building slab** (стена/пол/крыша, контракт имён, MVP отдельного мода) — [RU](../../design/ja3-how-to-custom-slabs.md) / [EN](../../design/ja3-how-to-custom-slabs.en.md). Это процедура автора, не loaded runtime JAZZ: своих `SlabMaterials` в комплекте нет.
