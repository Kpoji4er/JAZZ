# Как сделать свой slab в JA3

How-to по движку Jagged Alliance 3: что такое slab, какие куски комнаты существуют и с какими именами их искать. Это **не** current-state JAZZ: своих `SlabMaterials` в комплекте пока нет.

Источники: установленный `<JA3_ROOT>\ModTools\Src` (`CommonLua/Libs/Volumes/Slab.lua`, `RoomRoof.lua`, `Classes/Destroyable.lua`, `Data/SlabPreset.lua`) и официальный `ModTools/Docs` (Entity, Map Editor). Подтверждение: **static**. Editor/runtime приёмка — после первого импорта набора.

Ниже `{id}` — токен материала, например `JazzBrick`. Без пробелов и дефисов.

## Что это такое

**Slab — клетка комнаты, не свободный проп.**

Проп ставится мышкой куда угодно. Слаб комната (`Room`, в Map Editor: **Ctrl-Shift-N**) расставляет сама: вы выбираете материал стен/пола/крыши, движок заполняет воксели.

Движок **не хранит путь к модели в пресете**. Он **склеивает имя entity** из `id` материала + роли куска + варианта + суффикса `01` / `02` / …

```text
Room.wall_mat = "JazzBrick"
        ↓
Presets.SlabPreset.SlabMaterials.JazzBrick
        ↓  ComposeEntityName()
WallExt_JazzBrick_Wall_ExEx_01
        ↓
EntityData["WallExt_JazzBrick_Wall_ExEx_01"] + .ent + mesh + .mtl + DDS
```

Если пресет есть, а entity с ожидаемым именем нет — клетка станет InvisibleObject, в логе missing entity. Переименовать entity «для красоты» нельзя: имя и есть контракт.

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
| `SlabWallObject` | окно / дверь (вырезает дыру в стене) |

Пресет задаёт только `id`, список суффиксов и боевые свойства (`obj_material`, `strength`). Модель к пресету вручную не привязывается.

## Как комната собирается

Коробка 3×3 клетки. На каждую клетку — свой меш с каноническим именем:

```text
        крыша Roof_*
   ┌────┬────┬────┐
   │Cap │Wall│Cap │   углы: Corner
   │ L  │    │ T  │
   ├────┼────┼────┤
   │Wall│пол │Wall│   пол: Floor_*
   │    │    │    │
   ├────┼────┼────┤
   │    │    │CapX│   крест стен: CapX
   └────┴────┴────┘
        дверь/окно вырезает дыру в Wall
```

Без угла и крышек две стены встречаются, а столбика/затычки торца нет — комната дырявая, даже если фасад нарисован.

## Как читается имя

```text
WallExt_JazzBrick_Wall_ExEx_01
│      │         │    │    └─ субвариант (01, 02, …)
│      │         │    └────── какие стороны: ExEx / ExIn / InIn
│      │         └─────────── роль куска: Wall / Corner / CapL
│      └───────────────────── id материала = id пресета
└──────────────────────────── семья: наружная стена
```

Суффикс субварианта — две цифры. Пустой `SlabMaterialSubvariant` в пресете = `suffix = "01"`, `chance = 100`.

В Blender объект должен называться **уже** полным игровым именем (`WallExt_JazzBrick_Wall_ExEx_01`), не коротким `JazzBrick` или `wall_slab_brick`. После экспорта игра это имя не переименует.

## Каталог кусков

### 1. Стена — `Wall`

Плоский фасад на одну клетку (типично ящик ~1.2 × 0.2 × 0.7 м).

Три варианта — сколько сторон у меша «улица / комната»:

| Вариант комнаты | Токен | Что это |
|---|---|---|
| `Outdoor` | `ExEx` | Две наружные стороны. Забор, сарай, стена без внутренней обшивки. |
| `OutdoorIndoor` | `ExIn` | Снаружи свой меш; внутрь движок вешает аттач `WallInt_*`. Обычный дом. |
| `IndoorIndoor` | `InIn` | Две внутренние стороны. Перегородка между комнатами. |

```text
WallExt_{id}_Wall_ExEx_01
WallExt_{id}_Wall_ExIn_01
WallExt_{id}_Wall_InIn_01
```

Для первой комнаты достаточно `ExEx_01`. Без ExIn/InIn нельзя сделать «дом с обоями внутри», но коробку с улицы уже видно.

База без суффикса (её движок дополняет `_01`):

```text
WallExt_{id}_Wall_{вариант}
```

Источники в коде: `Slab:GetBaseEntityName`, `variantToVariantName`.

### 2. Угол — `Corner`

Вертикальная стойка на стыке двух стен.

```text
WallExt_{id}_Corner_01
WallInt_{id}_Corner_01      только если есть indoor-обшивка
```

Функция: `ComposeCornerBeamName`.

### 3. Крышки стыков — `CapL` / `CapT` / `CapX`

Это не карниз крыши. Это **затычки торца**, когда стены стыкуются буквой:

| Имя | Стык | Когда появляется |
|---|---|---|
| `CapL` | Г-образный | угол здания, две стены |
| `CapT` | Т-образный | третья стена врезается в середину |
| `CapX` | крест | четыре стены в одном вокселе |

```text
WallExt_{id}_CapL_01
WallExt_{id}_CapT_01
WallExt_{id}_CapX_01
```

Функция: `ComposeCornerPlugName`.

### 4. Пол и потолок — `Floor`

Одна плитка 1.2 × 1.2. Потолок (`CeilingSlab`) берёт **те же** entity; отдельные `Ceiling_*` не нужны.

```text
Floor_{id}_01
```

Свой пол не обязателен: стенам можно дать свой материал, а полу оставить ванильный `Planks` / `Adobe`.

### 5. Внутренняя обшивка — `WallInt`

Отдельный пресет группы `SlabIndoorMaterials` (Inner Wall Material у комнаты), **не** тот же `id`, что у фасада. Ваниль: `CityTiles`, `Colonial`, `Concrete`, `Planks`, `Wood`.

```text
WallInt_{indoor_id}_Wall_01
```

Вешается аттачем на стену `OutdoorIndoor` / `ExIn`. Без этого набора внутри дома пусто или missing entity. Комната с `Outdoor` / ExEx живёт без обоев.

### 6. Крыша — `Roof`

Имя строится от поля пресета **`EntitySet`**, не от `id` (у ванили они часто совпадают; display name может врать — у Adobe крыши подпись «Concrete»).

```text
Roof_{EntitySet}_{компонент}_{NN}
```

| Компонент | Что это |
|---|---|
| `Plane` | скат, основная плоскость |
| `Eave` | карниз / свес |
| `Rake` | торец ската |
| `Ridge` | конёк |
| `Gable` | фронтон |
| `RakeEave` / `RakeRidge` / `RakeGable` | стыки этих кусков |
| `GableCrest`, `GableSlope`, `RakeGableCrestTop` / `Bot`, `RakeGableSlopeTop` / `Bot` | гребень и уклон фронтона |

Примеры: `Roof_Adobe_Plane_01`, `Roof_Adobe_Eave_02`.

Полный набор — много мешей. Комната без крыши в редакторе нормальна. Делать после того, как стены стыкуются.

Fallback в коде, если у пресета нет `EntitySet` / субвариантов: `Roof_{id}_{компонент}_01` (смотрит на `self.material`). Надёжнее сразу задать `EntitySet` равным `id`.

### 7. Лестница — `Stairs`

Отдельный пресет `StairsSlabMaterials`. Не появляется из стенового материала.

```text
Stairs_{id}_01
```

### 8. Окно и дверь

Отдельные entity (`SlabWallObject`). Они **вырезают дыру** в `Wall`. Пока нет entity этого имени — в стену этого материала окно не вставить. Ванильное `Window_Adobe_Single_01` к вашему `JazzBrick` не приклеится.

Шаблон: `{Тип}_{id}_{ширина}_{NN}`  
Функция: `SlabWallObjectName`.

| Высота клетки | Окно | Дверь |
|---|---|---|
| 1 | `WindowVent` | `WindowVent` |
| 2 | `Window` | `Window` |
| 3 | `WindowBig` | `Door` |
| 4 | `TallWindow` | `TallDoor` |

Ширина: `Small` (0), `Single`, `Double`, `Triple`, `Quadruple`.

```text
WindowVent_{id}_Single_01
Window_{id}_Single_01
WindowBig_{id}_Single_01
TallWindow_{id}_Single_01
Door_{id}_Single_01
TallDoor_{id}_Double_01
```

### 9. Облом — `Broken` / `BrokenDec` / `Damaged`

Когда соседнюю клетку выбили, движок **меняет entity**, а не деформирует меш. База = `GetBaseEntityName()` **без** `_{NN}`.

| Суффикс | Что это |
|---|---|
| `_Broken_T` | облом сверху |
| `_Broken_B` | снизу |
| `_Broken_R` | сбоку (лево/право — зеркалом) |
| `_Broken_RT` / `_Broken_RB` | угол: верх+бок / низ+бок |
| `_BrokenDec_T` / `_B` / `_R` | декаль/аттач облома на соседней целой стене |
| `_Damaged` | побитая, но ещё целая (если в пресете `use_damaged`) |

```text
WallExt_{id}_Wall_ExEx_Broken_T_01
WallExt_{id}_Wall_ExEx_Broken_B_01
WallExt_{id}_Wall_ExEx_Broken_R_01
WallExt_{id}_Wall_ExEx_Broken_RT_01
WallExt_{id}_Wall_ExEx_Broken_RB_01
WallExt_{id}_Wall_ExEx_BrokenDec_T_01
WallExt_{id}_Wall_ExEx_BrokenDec_B_01
WallExt_{id}_Wall_ExEx_BrokenDec_R_01
WallExt_{id}_Wall_ExEx_Damaged_01
```

Пол и indoor ломаются так же: `Floor_{id}_Broken_R_01`, `WallInt_{id}_Wall_Broken_R_01`, `Roof_{EntitySet}_Plane_Broken_T_01`.

Без этих мешей выстрел → missing entity в логе. Для прототипа нормально. Боевой набор — десятки мешей на один материал (у ванильного Brick ещё `_02` / `_03` на многие стороны).

В пресете перечисляют существующие суффиксы: `subvariants`, `corner_subvariants`, `broken_*_subvariants`, `broken_attaches_*`, `damaged_subvariants`. Флаги `use_damaged` / `use_damaged_first_floor` — вместо облома показывать Damaged.

### 10. Декор — не slab

`WallDec_*`, фризы, цоколь — обычные пропы. Линкуются к стене коллекцией (C). В пресет материала не входят и из него не появляются.

## Какие имена нужны по волнам

Пример `id = JazzBrick`. Подставьте свой токен.

### MVP — увидеть коробку комнаты

Пресеты: `SlabMaterials` с `id = "JazzBrick"`; по желанию `FloorSlabMaterials` с тем же `id`.

```text
WallExt_JazzBrick_Wall_ExEx_01      стена
WallExt_JazzBrick_Corner_01         угловая стойка
WallExt_JazzBrick_CapL_01           Г-стык
WallExt_JazzBrick_CapT_01           Т-стык
WallExt_JazzBrick_CapX_01           крест
Floor_JazzBrick_01                  пол (если свой)
```

Этого хватит: Map Editor → комната → Wall Material = JazzBrick → коробка без дыр на углах.

### Волна 2 — дом с внутренней отделкой

```text
WallExt_JazzBrick_Wall_ExIn_01
WallExt_JazzBrick_Wall_InIn_01
WallInt_{indoor_id}_Wall_01
WallInt_{indoor_id}_Corner_01
```

### Волна 3 — разрушение в бою

`Broken_*` / `BrokenDec_*` / опционально `Damaged_*` для каждой используемой базы (`ExEx`, потом ExIn/InIn, пол, indoor).

### Волна 4 — крыша

`Roof_{EntitySet}_Plane_01` и остальные компоненты из таблицы выше.

### Волна 5 — проёмы именно этого материала

`Window_*` / `Door_*` / `WindowVent_*` нужной высоты и ширины.

### Волна 6 — субварианты

`_02`, `_03` и запись в `subvariants` пресета, чтобы стены не клонировались один в один.

## Что нужно в файлах на одно имя

Одно игровое имя = один Entity:

| Файл | Зачем |
|---|---|
| `Entities/WallExt_{id}_Wall_ExEx_01.ent` | меш + states (`idle` обязателен) |
| `Entities/WallExt_{id}_Wall_ExEx_01.lua` | `EntityData` (`fade_category = Never`, `material_type`) |
| `.mtl` + DDS | Base / Norm / RM / AO / Colorization |
| Collision surface в `.ent` | пули, LOS, укрытие |
| строка в `items.lua` | `ModItem` Entity |
| пресет `SlabMaterials` с тем же `id` | комната видит материал в списке |

Текстуры можно шарить между стеной, углом и крышками, если UV общий. Имена entity — нет, каждое своё.

## Vanilla-материалы (не занимать id)

Стены (`SlabMaterials`): `Adobe`, `Brick`, `City`, `Colonial`, `ColonialFence1`, `ColonialFence2`, `Concrete`, `ConcreteThin`, `MetalScaff`, `Planks`, `RedBrick`, `Shanty`, `Sticks`, `Tin`, `Warehouse`, `Wood`, плюс `PalmLeaves`.

Полы (`FloorSlabMaterials`): `Adobe`, `Colonial`, `ColonialTiles`, `Concrete`, `MetalScaff`, `Planks`, `WoodScaff`.

Крыши (`RoofSlabMaterials`): `Adobe`, `Concrete`, `PalmLeaves`, `Plywood`, `Sticks`, `Straw`, `Tiles`, `Tin`, `Wood`.

Indoor (`SlabIndoorMaterials`): `CityTiles`, `Colonial`, `Concrete`, `Planks`, `Wood`.

Свой пресет с таким `id` — это override ванили, не новый материал.

## Пресет в Mod Editor

Правый клик в дереве мода → **New → Buildings**:

| Пункт редактора | Класс | Кто читает |
|---|---|---|
| Slab material | `SlabMaterials` | стены, `Room.wall_mat` |
| Floor material | `FloorSlabMaterials` | пол / потолок |
| Roof material | `RoofSlabMaterials` | крыша (`EntitySet`!) |
| Stairs material | `StairsSlabMaterials` | лестницы |
| Shelter material | `ShelterSlabMaterials` | укрытия |

Indoor стены: пресет группы `SlabIndoorMaterials`.

Поля:

- **id** — токен в имени entity.
- **display_name** — подпись в редакторе.
- **obj_material** — боевой `ObjMaterial` (`Brick`, `Wood`, `ConcreteThin`, `Planks`, `ClayBrick`, `Metal_Inv_Penetrable`, …): HP, пробитие, FX попадания.
- **strength** — какая стена «побеждает», если две комнаты делят воксель.
- **subvariants** — `{suffix, chance}` для рандома.
- крыша: **EntitySet**, **roof_additional_height**.

Новый `ObjMaterial` не нужен, если хватает ванили. Если нужен — отдельный пресет (HP, impenetrable, noise).

Save мода пишет `items.lua` + companion. Это generated data: одна транзакция с `metadata.lua`.

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

## Модель, материал, текстуры

### Пайплайн entity

1. Blender 2.93+ и аддон `ModTools/HGBlenderExporter.zip` (панель **HGE Tools**). Файл, записанный в Blender 5.x, в 4.5 открывается с потерей данных — лучше сидеть на одной версии.
2. Origin (empty/armature) → mesh parented к origin. Состояние **idle** обязательно.
3. Размер строго под воксель: стена 1.2 × 0.7, пол 1.2 × 1.2. Пивот как у ванили (**стена на грани вокселя**, не в центре тайла). Иначе комната «поплывёт» или даст двойную толщину на стыке.
4. Collision surface (тип Collision) — без неё пули, укрытие и LOS не видят стену.
5. С референсов (человек, сетка земли) снять `hge_export`, иначе Export All утащит их в мод.
6. PBR в Haemimont Material (не Principled как источник правды):

   | Карта | Файл | Назначение |
   |---|---|---|
   | Base color | TGA 24/32 | albedo; alpha → Use Alpha Test |
   | Normal | TGA | нормали |
   | Roughness/Metallic | TGA | R = roughness, B = metalness |
   | AO | TGA grayscale | окклюзия |
   | Colorization | TGA | до 4 масок (R/G/B/A) → Color1/2/3 комнаты |

   Colorization: чёрный = игнор; R/G/B/A = части 1–4; без градиентов на стыках. Красимые зоны в BaseColor — серые (~190–220). UV лучше держать в 0–1.

7. Export All → `%AppData%/Jagged Alliance 3/ExportedEntities`.
8. Mod Editor → New → Assets → Entity → Import `.ent`.
9. После реэкспорта entity **не подхватывается на лету** — рестарт игры или новое имя.

Текстуры после import: нормализовать DDS (`Entity_MapType`), затем Save materials / SaveWholeMod, чтобы пересобрать `mtlbin`. Numeric DDS не оставлять. В JAZZ для оружия это `$rename-jazz-weapon-textures`; для slab тот же принцип имён.

В Entity: `fade_category = Never` (как vanilla slabs), `material_type` согласован с `obj_material`, debris по желанию (`Debris_Wooden_*`, `Debris_ConcreteBrick_*`).

### Практичный путь: ретекстур ванили

Полный набор Adobe — десятки мешей. Для нового «кирпича» обычно:

1. Скопировать геометрию ванили (`Brick` / `Planks`) в Blender с теми же габаритами и пивотом, свой UV/текстуры.
2. Экспортировать под **новыми именами** со своим `id`.
3. Не рассчитывать на `inherit_entity` у vanilla slab: `can_be_inherited` у стен обычно выключен.

Свой ящик с нуля почти всегда ломает стыки: пивот по центру тайла (`X` ±0.6, `Y` ±0.1) — самая частая ошибка черновика.

## Отдельный мод, не проп-пак и не `jazz_assets`

Слабы лучше держать отдельным пакетом: набор мешей большой, кампании JAZZ они не нужны, пока карты не выберут `id`.

```text
Mods/jazz-slabs/                    (имя пакета своё)
  Entities/
    WallExt_JazzBrick_Wall_ExEx_01.lua
    WallExt_JazzBrick_Wall_ExEx_01.ent
    Materials/....mtl
    Textures/WallExt_JazzBrick_*_Base.dds
  items.lua                         -- ModItem Entity + ModItem SlabMaterials
  metadata.lua                      -- свой mod id, не e6L4ECj / pDGDhr / …
```

- Не пятый обязательный пакет JAZZ.
- `jazz-maps` ставит dependency **только когда** комнаты на карте реально выбирают этот `id`.
- В Steam/Workshop можно ставить отдельно, в том числе без JAZZ.
- Не тащить entity в `jazz` или `jazz-maps`.
- Если всё же класть в комплект: entity + пресет — `jazz_assets` (или мод, который грузится до `jazz-maps`); новый публичный `id` — spec + DoR; generated data — одна транзакция `items.lua` + `metadata.lua` + companion.

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
- Окна и двери не появляются из `SlabMaterials`.
- Декор (`WallDec_*`) — пропы, не часть пресета.
- После re-import entity — рестарт.
- Пивот и толщина — «стена в полу» / двойная толщина на стыке.
- Без Collision surface стена красивая, но простреливается и не даёт cover.
- `hge_export` на референсах — в мод уедут человек и земля.
- Сломанные пути текстур с другой машины (`C:\Users\…`) не переживут перенос Blend-файла.

## Чеклист

1. Короткий `id` (например `JazzBrick`), не пересекается с ванилью.
2. Scope: только ExEx-прототип или полный набор (ExIn/InIn, indoor, broken, крыша, окна).
3. Меш под 1.2 × 0.7 (стена) / 1.2 × 1.2 (пол), пивот как ваниль, Collision surface.
4. PBR TGA → Blender HGE export → Import Entity.
5. Имена entity строго по формулам выше.
6. ModItem Slab/Floor/Roof material с тем же `id`.
7. `obj_material` на существующий боевой материал, если нет причины плодить новый.
8. Save мода, рестарт, комната в Map Editor, коллизии, один выстрел на разрушение.
9. Нормализовать DDS и пересобрать `mtlbin`.
