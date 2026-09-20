---
name: export-jazz-character-element
description: Создавать элемент внешности юнита (Hat, Body, Pants, Armor, Chest, Hip, Hair, Head) из Blender в jazz_assets через официальный HG Blender Exporter и AssetsProcessor. Использовать при добавлении собственной одежды, головных уборов или снаряжения на риг мерков, при ошибке "skeleton was not found", при потере весов после экспорта и при регистрации entity класса Character*. Не использовать для оружия и props — там нет наследования анимаций торса.
---

# Character element: Blender → jazz_assets

Официальный маршрут Haemimont: Blender + `HG Blender Exporter` → FBX → `AssetsProcessor` → `ExportedEntities` → мод. Агент проходит его headless; Mod Editor остаётся за владельцем.

## Что должно быть на машине

| Что | Где |
|---|---|
| Экспортёр (реализация) | `<JA3_ROOT>/ModTools/BlenderExport.py` |
| Аддон-загрузчик | `<JA3_ROOT>/ModTools/HGBlenderExporter.zip`, установлен в `%APPDATA%/Blender Foundation/Blender/<ver>/scripts/addons/HG Blender Exporter` |
| AssetsProcessor | `<JA3_ROOT>/ModTools/AssetsProcessor/AssetsProcessor.exe` (вызывается экспортёром сам) |
| Риг-сэмплы | `<JA3_ROOT>/ModTools/Samples/Assets/SampleMaleModel/BlenderScene_Appearance.blend`, `SampleFemaleModel/BlenderMOD_Apperance_Female.blend` |
| Доки | `<JA3_ROOT>/ModTools/Docs/ModItemEntity.md.html`, `ModItemAppearancePreset.md.html` |

Аддон читает путь к `ModTools` из реестра `HKCU\SOFTWARE\Haemimont Games\Jagged Alliance 3`, поэтому в headless он поднимается сам. Сэмплы из установки игры — только на чтение; работать в копии внутри `jazz_assets/Sources/Character/<Entity>/`.

## Маршрут

1. **Сборка сцены** на базе сэмпла: `scripts/build_sh68_helmet.py` — эталон для нового элемента.
2. **Превью**: `scripts/preview_character_element.py` — посадка проверяется по рендерам, а не в вьюпорте.
3. **Экспорт**: `scripts/export_character_element.py` — вызывает `hge.export_dialog` в `EXEC_DEFAULT`.
4. **Установка в мод**: `scripts/install_character_element.py` — копирует из `ExportedEntities` и переименовывает текстуры под `JAZZ-ASSETS-002`.
5. **Регистрация**: `ModItemEntity` в `items.lua` + `entities` + `code` в `metadata.lua`.
6. **Human-шаги владельца**: Mod Editor — проверить entity, пересобрать `mtlbin`, убедиться в наличии элемента в нужном dropdown `AppearancePreset`; прогон в игре.

```powershell
$B = "C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"
& $B -b "<sample>.blend" -P scripts/build_sh68_helmet.py -- --out "<assets>/Sources/Character/<Entity>"
& $B -b "<assets>/Sources/Character/<Entity>/<Entity>.blend" -P scripts/preview_character_element.py -- --object <Entity> --out <preview_dir>
& $B -b "<assets>/Sources/Character/<Entity>/<Entity>.blend" -P scripts/export_character_element.py -- --object <Entity>
python scripts/install_character_element.py --entity <Entity> --mesh mesh --mod-dir "<assets>"
```

## Контракт экспортёра

Имя объекта на время экспорта заменяется на `hgm:<entity>:<mesh>:<lod>:<lod_distance>[:s=<state>][:i=<Male|Female> mesh]`. Общая длина — **не больше 55 символов**, иначе экспорт падает на валидации.

Обязательные `hge_obj_settings` для **одежды** (Body/Pants/Armor — skinned):

| Поле | Значение | Почему |
|---|---|---|
| `entity` | `[A-Za-z0-9_]+` | попадает в имя `.ent` |
| `mesh` | обычно `mesh` | несколько мешей одного entity разделяются как `mesh&body`, `mesh&hands` |
| `state` | `_mesh` для LOD1 | уникальность state проверяется, но `_mesh` из проверки исключён |
| `lod` / `lod_distance` | `1` / `0` | для LOD1 distance обязан быть 0; для LOD ≥ 2 — строго больше 0 |
| `inherit_animation` | `Male` или `Female` | без наследования skinned-меш без своей анимации не проходит валидацию |

Для **CharacterHat** (и очков/сигар того же класса) наследование и веса **не нужны**: шапка — жёсткий attach. `AppearancePreset.HatSpot` по умолчанию `"Head"`, поэтому origin пустышки должен стоять на кости `Bip001 Head` (только location, без поворота кости: спот Head миро-ориентирован, иначе купол ляжет набок). `inherit_animation = None`, `state = idle`. Экспортёр `axis_forward=Y`: **+Y — лицо**, затылок в −Y.

Роли выводятся из иерархии: EMPTY без родителя = ORIGIN, MESH под ORIGIN или ARMATURE = MESH, MESH под MESH = SURFACE. Одежду вешать на `Origin_top` (ноги). Шапку — на отдельный empty в точке Head.

## Три грабли, на которых ломается результат

1. **Шапку нельзя экспортировать как одежду.** `CharacterHat` не в `animated_parts`. Движок вешает её на спот `Head` (дефолт `HatSpot`). Меш в координатах всего тела (вершины на z≈170 см) плюс attach к Head даёт каску на полтора человеческих роста над черепом. Origin — на Head, в `.ent` нет `<inherit entity="Male">`.
2. **`hgskeleton`.** Для skinned Body/Pants/Armor: custom property на арматуре `Bip001` со списком `<entity>_<mesh>` через `|` (пример: `GuardianMedium_mesh`). Без записи AssetsProcessor пишет `Bones: 0`. Не оставлять sample-строку `Suit_mesh|BP_mesh` и не включать чужие entity. К шапке не относится.
3. **Headless не даёт GUI-контекста.** `hge.export_dialog` собирает список мешей в `invoke()` и переключает workspace. В фоне: выставить `obj.hge_export` вручную, подменить `BlenderExport.WorkspaceContext` заглушкой и вызывать оператор как `EXEC_DEFAULT`.

## Blender 5.2 и community JA3 Exporter (`hge_tools`)

Официальный аддон `HG Blender Exporter` на Blender 5.2 часто **не грузится** (`No module named 'HG Blender Exporter'`). На этой машине рабочий путь — community `hge_tools` (`%APPDATA%/Blender Foundation/Blender/5.2/extensions/user_default/hge_tools`). Сэмпл и headless-скрипты skill рассчитаны на **Blender 4.4**; blend, сохранённый в 5.2, 4.4 не открывает.

Имя `hgm:<entity>:<mesh>:<lod>:<lod_distance>[:s=<state>][:i=Male mesh]`: официальный лимит **55** символов, community exporter проверяет **75**. Короткое `entity` (`GuardianMedium`, не `JAZZ_GuardianMedium_male`) безопаснее. После смены имени — File → Save, иначе на диске остаётся старый отчёт.

Экспортировать **только** целевой mesh + Origin + арматуру. У sample `Suit`/`BP`/`HAV_arms`/`M_BaseMesh Skin_BIP` снять `hge_export`. Иначе в FBX уходят лишние меши, bbox жилета падает до z=0.

### Custom Split Normals → `[Error] OptimizeElementNormals … 0 length`

glTF-одежда часто несёт битый слой custom split normals. AP пишет в **stdout** (не в `ModAssets/FBX/logs/*.log`):

`[Error] FBXImporter::OptimizeElementNormals Mesh: hgm:<entity>:mesh:… has normals with 0 length`

Сообщение повторяется по числу материалов. Дальше AP **не падает**: merge, DDS, `Bones: > 0`, `*** Done! ***`, exit 0, `.ent` с заполненным `name=` и `Meshes/*.m.hgm`. Это не фатал.

Перед экспортом на целевом mesh, затем **сохранить .blend**:

1. Object Data → Geometry Data → Clear Custom Split Normals Data (`has_custom_normals` должен стать False на диске).
2. Edit Mode → Merge By Distance.
3. Mesh → Normals → Recalculate Outside.
4. Apply Scale, если не 1,1,1.

Успех смотреть по артефактам, не по красному попапу community exporter:

- `ExportedEntities/<Entity>.ent` — `name="<Entity>"` и для одежды `<inherit entity="Male" …/>`;
- рядом `Meshes/<Entity>_mesh.m.hgm`;
- stdout AP: `Bones:` > 0 и `*** Done! ***`.

Ложный попап: exporter ждёт в stdout `*** Done! ***`, а краткий лог-файл AP содержит только `*** Debug::Done()`. Если stdout пуст, addon считает прогон провалом даже при готовом `.ent`. Команда для сверки stdout:

```powershell
$ap = "<JA3_ROOT>\ModTools\AssetsProcessor\AssetsProcessor.exe"
$fbx = "$env:APPDATA\Jagged Alliance 3\ModAssets\FBX\<blend>.fbx"
& $ap $fbx -globalappdirs -gamepath "<JA3_ROOT>"
```

Не править `ModTools` в установке игры. Локальный патч `hge_tools/blender_export.py` (считать `Debug::Done` / exit 0 успехом, 0-length normals как warning) живёт только в AppData Blender, не в git JAZZ.

## Классы entity и dropdown AppearancePreset

Класс задаётся в `ModItemEntity.class_parent` (не путать со списком `ClassParents`). Vanilla шляпы — `CharacterHat` **без** суффикса пола; топы/штаны — `CharacterBodyMale` / `CharacterPantsMale`. HTML-дока `ModItemAppearancePreset.md.html` пишет `CharacterHatMale` — это не сходится с `_EntityData.generated.lua`. Dropdown Hat строится из `GetEntityClassInherits("CharacterHat")`. Смешивать male и female **одежду** в одном `AppearancePreset` нельзя.

## Проверка

- для шапки: в `.ent` **нет** `<inherit entity="Male">`, bbox по Z около 0..20 см, не 160..180;
- для одежды: `Bones:` > 0 и `<inherit entity="Male" mesh_ref="mesh"/>`;
- `.ent` ссылается на существующие `Meshes/*.m.hgm` и `Materials/*.mtl`;
- текстуры названы `<Entity>_{Base|Norm|RM|AO|SPEC|SI|Color}.dds`, без числовых имён от AssetsProcessor;
- `check-asset-integrity.ps1` без новых ошибок;
- `Textures/Fallbacks` для новых DDS появляются только после Mod Editor SaveWholeMod — это human-шаг.

## Границы

- Не редактировать сэмплы и `ModTools` в установке игры.
- Не патчить `mtlbin` вручную.
- Не привязывать элемент к appearance мерков без отдельной спецификации: это контракт `jazz-units`.
- Исходные `.blend` и `.tga` держать в `jazz_assets/Sources/`, исключённой из Steam-пака через `ignore_files`.
