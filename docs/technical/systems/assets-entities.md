# Entities и ресурсы

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
- 5119 `.dds` textures;
- 522 `.mtl` materials;
- 516 `.hgm` meshes;
- 511 `.mtlbin` compiled materials;
- 114 folder ModItems;
- 22 `.bak` файла, требующие отдельной проверки как технический долг.

Разница 503 entity-файла на диске против 490 зарегистрированных означает 13 unlisted/orphan-candidate definitions. Это не доказательство мусора: они могут быть parent/variant/source remnants или использоваться непрямо. Удалять только после проверки metadata, inheritance и ссылок четырёх пакетов.

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

- открыть/проверить все изменённые entities в Mod Editor;
- предмет в руках, на земле, в inventory и на unit appearance;
- attachment states: scope, magazine, bipod, folded stock, muzzle, mask;
- materials/textures в разных lightmodels/weather;
- map props и collision/spots;
- поиск `missing entity/state/spot/material/texture` в runtime log;
- проверить, что новые resources зарегистрированы, а удаляемые не имеют ссылок;
- отдельно аудировать `.bak` и 13 unlisted definitions без автоматического удаления.

## Сопровождение

Изменение entity/resource обновляет эту страницу и профильную weapon/unit/map/UI-FX документацию. Изменение количества registered/on-disk entities требует обновить snapshot и причину расхождения.