# Как сделать свой slab в JA3

How-to по движку Jagged Alliance 3. Это **не** current-state JAZZ: своих slab-материалов в комплекте пока нет.

Источники: установленный `<JA3_ROOT>\ModTools\Src` (`CommonLua/Libs/Volumes/Slab.lua`, `RoomRoof.lua`, `Classes/Destroyable.lua`, `Data/SlabPreset.lua`) и официальный `ModTools/Docs` (Entity, Map Editor). Подтверждение: **static**. Editor/runtime приёмка — после первого импорта набора.

## Идея

Slab — не свободный проп, а **клетка комнаты**. Комната (`Room`, в Map Editor: Ctrl-Shift-N) задаёт материалы стен/пола/крыши. Движок **не хранит путь к модели в пресете**. Он **склеивает имя entity** из `id` материала + варианта + суффикса `01`/`02`/…

Если пресет есть, а entity с ожидаемым именем нет — стена будет InvisibleObject, в логе missing entity.

Воксель:

| Константа | Размер |
|---|---|
| `const.SlabSizeX` / `Y` | **1.2 м** |
| `const.SlabSizeZ` | **0.7 м** |

| Класс | Что строит |
|---|---|
| `WallSlab` | стена 1.2 × 0.7 |
| `FloorSlab` / `CeilingSlab` | пол / потолок 1.2 × 1.2 |
| `RoofSlab` | скат, карниз, конёк крыши |
| `RoomCorner` | угловая стойка + крышки стыков |
| `StairSlab` | лестница |
| `SlabWallObject` | окно / дверь (вырезает дыру) |

## Два слоя, которые обязаны совпасть

```
Room.wall_mat = "Adobe"
        ↓
Presets.SlabPreset.SlabMaterials.Adobe
        ↓  ComposeEntityName()
WallExt_Adobe_Wall_ExEx_01
        ↓
EntityData["WallExt_Adobe_Wall_ExEx_01"] + .ent + mesh + .mtl + DDS
```

`id` материала = токен в имени entity. Без пробелов и дефисов: `JazzBrick`, не `Jazz Brick`.

Пресет задаёт только `id`, список суффиксов и боевые свойства. Модель к пресету не привязывается вручную.

## Формулы имён entity

Суффикс субварианта — две цифры (`01`, `02`, …). Пустой `SlabMaterialSubvariant` в пресете = `suffix = "01"`, `chance = 100`.

### Стены (наружный набор)

База (ещё без суффикса):

```text
WallExt_{id}_Wall_{вариант}
```

Полное имя: `{база}_{NN}`.

| `variant` на slab / в комнате | токен |
|---|---|
| `Outdoor` | `ExEx` — две наружные стороны |
| `OutdoorIndoor` | `ExIn` — снаружи + indoor-аттач |
| `IndoorIndoor` | `InIn` — две внутренние |

Примеры: `WallExt_Adobe_Wall_ExEx_01`, `WallExt_Brick_Wall_ExIn_02`.

### Indoor-обшивка

Отдельный пресет группы `SlabIndoorMaterials`. Имя:

```text
WallInt_{id}_Wall_{NN}
```

Пример: `WallInt_CityTiles_Wall_01`.

`OutdoorIndoor` вешает indoor-entity аттачем на наружную стену. Без indoor-набора внутренность комнаты будет пустой или missing.

### Углы и крышки стыков

```text
WallExt_{id}_Corner_{NN}
WallInt_{id}_Corner_{NN}
WallExt_{id}_CapL_{NN}     L-стык
WallExt_{id}_CapT_{NN}     T-стык
WallExt_{id}_CapX_{NN}     крест
```

Функции: `ComposeCornerBeamName`, `ComposeCornerPlugName`.

### Полы и потолки

```text
Floor_{id}_{NN}
```

`CeilingSlab` берёт те же `Floor_*` entity. Пример: `Floor_Adobe_01`.

### Крыша

Имя строится не от `id` пресета, а от поля **`EntitySet`**:

```text
Roof_{EntitySet}_{компонент}_{NN}
```

Компоненты (`roof_comp`): `Plane`, `Eave`, `Rake`, `Ridge`, `Gable`, `RakeEave`, `RakeRidge`, `RakeGable`, плюс crest/slope-варианты (`GableCrest`, `RakeGableCrestTop`, …).

Примеры: `Roof_Adobe_Plane_01`, `Roof_Adobe_Eave_02`. У vanilla Adobe крыши `id` и `EntitySet` оба `Adobe`, а display name при этом «Concrete» — подпись в редакторе и токен в имени могут расходиться.

### Лестницы

```text
Stairs_{id}_{NN}
```

Пример: `Stairs_Adobe_01`.

### Окна и двери (не SlabMaterials)

Отдельные entity. Шаблон:

```text
{Тип}_{материал}_{ширина}_{NN}
```

Тип по высоте (индекс 1…4):

| height | окно | дверь |
|---|---|---|
| 1 | `WindowVent` | `WindowVent` |
| 2 | `Window` | `Window` |
| 3 | `WindowBig` | `Door` |
| 4 | `TallWindow` | `TallDoor` |

Ширина: `Small` (0), `Single`, `Double`, `Triple`, `Quadruple`.

Примеры: `Window_Adobe_Single_01`, `WindowVent_Adobe_Single_01`. Пока нет entity этого имени, в стену материала нельзя вставить окно.

## Разрушение

После дыр у соседей движок подменяет entity. База = `GetBaseEntityName()` **без** `_{NN}`:

| Назначение | Шаблон |
|---|---|
| Облом | `{база}_Broken_{T\|B\|R\|RB\|RT}_{NN}` |
| Декаль облома | `{база}_BrokenDec_{T\|B\|R}_{NN}` |
| Побитый, но целый | `{база}_Damaged_{NN}` |

Примеры:

- `WallExt_Adobe_Wall_ExEx_Broken_T_01`
- `WallExt_Adobe_Wall_ExEx_BrokenDec_R_02`
- `Floor_Adobe_Broken_R_01`
- `Roof_Adobe_Plane_Broken_T_01`
- `WallInt_CityTiles_Wall_Broken_R_01`

Полный боевой набор — десятки мешей. Для прототипа достаточно целых `*_01` (стена ExEx + угол + крышки + пол). Без Broken/Damaged разрушение уйдёт в missing entity.

В пресете перечисляют существующие суффиксы: `subvariants`, `corner_subvariants`, `broken_*_subvariants`, `broken_attaches_*`, `damaged_subvariants`. Флаги `use_damaged` / `use_damaged_first_floor` — вместо облома показывать Damaged.

## Vanilla-материалы (ориентир id)

Стены (`SlabMaterials`): `Adobe`, `Brick`, `City`, `Colonial`, `ColonialFence1`, `ColonialFence2`, `Concrete`, `ConcreteThin`, `MetalScaff`, `Planks`, `RedBrick`, `Shanty`, `Sticks`, `Tin`, `Warehouse`, `Wood`, плюс `PalmLeaves`.

Полы (`FloorSlabMaterials`): `Adobe`, `Colonial`, `ColonialTiles`, `Concrete`, `MetalScaff`, `Planks`, `WoodScaff`.

Крыши (`RoofSlabMaterials`): `Adobe`, `Concrete`, `PalmLeaves`, `Plywood`, `Sticks`, `Straw`, `Tiles`, `Tin`, `Wood`.

Indoor (`SlabIndoorMaterials`): `CityTiles`, `Colonial`, `Concrete`, `Planks`, `Wood`.

Не занимать эти id своим пресетом — это override vanilla, не новый материал.

## Пресет в Mod Editor

Правый клик в дереве мода → **New → Buildings**:

| Пункт редактора | Класс | Кто читает |
|---|---|---|
| Slab material | `SlabMaterials` | стены, `Room.wall_mat` |
| Floor material | `FloorSlabMaterials` | пол / потолок |
| Roof material | `RoofSlabMaterials` | крыша (`EntitySet`!) |
| Stairs material | `StairsSlabMaterials` | лестницы |
| Shelter material | `ShelterSlabMaterials` | укрытия |

Indoor стены: пресет группы `SlabIndoorMaterials` (Inner Wall Material у комнаты).

Поля:

- **id** — токен в имени entity.
- **display_name** — подпись в редакторе.
- **obj_material** — боевой `ObjMaterial` (`Brick`, `Wood`, `ConcreteThin`, `Planks`, `ClayBrick`, `Metal_Inv_Penetrable`, …): HP, пробитие, FX попадания.
- **strength** — какая стена «побеждает», если две комнаты делят воксель.
- **subvariants** — `{suffix, chance}` для рандома.
- крыша: **EntitySet**, **roof_additional_height**.

Новый `ObjMaterial` не нужен, если хватает vanilla. Если нужен — отдельный пресет (HP, impenetrable, noise).

Save мода пишет `items.lua` + companion. Это generated data: одна транзакция с `metadata.lua`.

## Модель, материал, текстуры

### Пайплайн entity

1. Blender 2.93+ и аддон `ModTools/HGBlenderExporter.zip` (панель **HGE Tools**).
2. Origin (empty/armature) → mesh parented к origin. Состояние **idle** обязательно.
3. Размер строго под воксель: стена 1.2 × 0.7, пол 1.2 × 1.2. Пивот как у vanilla (стена на грани вокселя, не в центре тайла). Иначе комната «поплывёт».
4. Collision surface (тип Collision) — без неё пули, укрытие и LOS не видят стену.
5. PBR в Haemimont Material (не Principled как источник правды):

   | Карта | Файл | Назначение |
   |---|---|---|
   | Base color | TGA 24/32 | albedo; alpha → Use Alpha Test |
   | Normal | TGA | нормали |
   | Roughness/Metallic | TGA | R = roughness, B = metalness |
   | AO | TGA grayscale | окклюзия |
   | Colorization | TGA | до 4 масок (R/G/B/A) → Color1/2/3 комнаты |

   Colorization: чёрный = игнор; R/G/B/A = части 1–4; без градиентов на стыках. Красимые зоны в BaseColor — серые (~190–220).

6. Export All → `%AppData%/Jagged Alliance 3/ExportedEntities`.
7. Mod Editor → New → Assets → Entity → Import `.ent`.
8. Имя entity в Blender = **полное** игровое имя (`WallExt_JazzBrick_Wall_ExEx_01`), не короткое `JazzBrick`.
9. После реэкспорта entity **не подхватывается на лету** — рестарт игры или новое имя.

Текстуры после import: нормализовать DDS (`Entity_MapType`), затем Save materials / SaveWholeMod, чтобы пересобрать `mtlbin`. Numeric DDS не оставлять. В JAZZ для оружия это `$rename-jazz-weapon-textures`; для slab тот же принцип имён.

В Entity: `fade_category = Never` (как vanilla slabs), `material_type` согласован с `obj_material`, debris по желанию (`Debris_Wooden_*`, `Debris_ConcreteBrick_*`).

### Практичный путь: ретекстур vanilla

Полный набор Adobe — десятки мешей. Для нового «кирпича» обычно:

1. Скопировать геометрию vanilla (`Brick` / `Planks`) в Blender с теми же габаритами и пивотом, свой UV/текстуры.
2. Экспортировать под **новыми именами** со своим `id`.
3. Не рассчитывать на `inherit_entity` у vanilla slab: `can_be_inherited` у стен обычно выключен.

Минимум для прототипа стены:

- `WallExt_{id}_Wall_ExEx_01`
- `WallExt_{id}_Corner_01`
- `WallExt_{id}_CapL_01`, `CapT_01`, `CapX_01` (иначе углы комнаты дырявые)
- `Floor_{id}_01`, если нужен пол

ExIn/InIn и indoor можно отложить.

## Пример состава мода

```text
MySlabMod/                          (в JAZZ — пакет jazz_assets)
  Entities/
    WallExt_JazzBrick_Wall_ExEx_01.lua
    WallExt_JazzBrick_Wall_ExEx_01.ent
    Materials/....mtl
    Textures/WallExt_JazzBrick_*_Base.dds
  items.lua                         -- ModItem Entity + ModItem SlabMaterials
  metadata.lua
```

Смысл пресета (не копипаста 1:1 из редактора):

```lua
PlaceObj('SlabMaterials', {
  id = "JazzBrick",
  display_name = T(...),
  obj_material = "Brick",
  strength = 3,
  subvariants = {
    PlaceObj('SlabMaterialSubvariant', nil), -- 01
    PlaceObj('SlabMaterialSubvariant', { suffix = "02", chance = 40 }),
  },
  corner_subvariants = {
    PlaceObj('SlabMaterialSubvariant', nil),
  },
})
```

Движок будет искать `WallExt_JazzBrick_Wall_ExEx_01` и `_02`.

## Проверка в Map Editor

1. Включить мод с entity **и** пресетом, перезапустить игру.
2. Открыть карту / patch.
3. Ctrl-Shift-N — комната; в Properties: Wall Material = ваш `id`.
4. Alt-G — сетка вокселей; Ctrl-Shift-K — коллизии; Ctrl-Shift-X — укрытие.
5. Сломать стену в бою — Broken/Damaged или missing entity в логе.
6. Сменить Inner Wall Material — появляется ли `WallInt_*`.

Искать в логе: `Failed to load` / missing entity с **полным** именем, которое движок ждал.

## Ограничения и типичные ошибки

- Имя entity = контракт. Пресет не содержит путь к модели.
- Крыша смотрит на `EntitySet`, не на `id`.
- Indoor ≠ Outdoor: `WallExt_*` и `WallInt_*` — разные семьи пресетов.
- Окна и двери не появляются из SlabMaterials.
- Декор (`WallDec_*`, фризы, цоколь) — пропы, линкуются к стене коллекцией (C). Не часть пресета.
- После re-import entity — рестарт.
- Пивот и толщина — частая причина «стена в полу» / двойная толщина на стыке.
- Без Collision surface стена красивая, но простреливается и не даёт cover.

## JAZZ: куда класть, если делать в комплекте

Пока набора нет. Когда появится:

- entity, `.ent`, `.mtl`, DDS — пакет **`jazz_assets`**;
- пресет материала — там же (чтобы карты могли выбрать материал), либо в моде, который грузится до `jazz-maps`;
- комнаты на картах — **`jazz-maps`** только выбирают `id`;
- новый публичный `id` — spec + DoR;
- generated data — одна транзакция `items.lua` + `metadata.lua` + companion;
- не тащить entity в `jazz` или `jazz-maps`.

## Чеклист

1. Короткий `id` (например `JazzBrick`), не пересекается с vanilla.
2. Scope: только ExEx-прототип или полный набор (ExIn/InIn, indoor, broken, крыша, окна).
3. Меш под 1.2 × 0.7 (стена) / 1.2 × 1.2 (пол), пивот как vanilla, Collision surface.
4. PBR TGA → Blender HGE export → Import Entity.
5. Имена entity строго по формулам выше.
6. ModItem Slab/Floor/Roof material с тем же `id`.
7. `obj_material` на существующий боевой материал, если нет причины плодить новый.
8. Save мода, рестарт, комната в Map Editor, коллизии, один выстрел на разрушение.
9. Нормализовать DDS и пересобрать `mtlbin`.
