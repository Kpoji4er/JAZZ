# Ged / Mod Editor: как собираются ошибки

Канон — установленный `<JA3_ROOT>/ModTools/Src`. GitHub `THQNordic/JaggedAlliance3Modding` — история, не замена installed source.

## Конвейер

```text
OpenGedApp("ModEditor") + WarningsUpdateRoot="root"
        ↓
InitializeWarningsForGedEditor
        ↓ for_each_subobject(root, "GedEditedObject")
GetDiagnosticMessage(obj)
        ↓ cache → ! в дереве и status bar
```

Кэш: `PropertyObjectWarningsCache.lua`. Живой панели у агента нет.

## `GetDiagnosticMessage` (PropertyObject)

1. `procall(self.GetError)` — красное; crash → `GetError has crashed`.
2. Иначе `procall(self.GetWarning)` — жёлтое; crash → `GetWarning has crashed`.
3. Иначе `GetProperties` + для каждого свойства `ValidateProperty`.
4. Затем ipairs-дети объекта как subitems.

`GetError` / `GetWarning` по умолчанию пустые (`empty_func`). Класс сам объявляет проверки.

Не-verbose родитель для nested/subitem схлопывает текст в:

- `One or more nested objects have errors!` / `… warnings!`
- `One or more subitems have errors!` / `… warnings!`

Verbose (редко в UI) печатает `Property '…' of type '…':` + исходное сообщение.

## `ValidateProperty`

Пропускает `no_edit` / `no_validate`. Дальше по `editor`:

| editor | Типичная претензия |
| --- | --- |
| `text` + translate | T() на не-translate или сырая строка на translate |
| `preset_id` / `preset_id_list` | `Missing preset '…'` |
| `number` | вне min/max |
| `choice` / `dropdownlist` / `set` | значение не в `items` |
| `string_list` | элемент не в `items` |
| `func` / `expression` | код не компилируется |
| `nested_obj` | не PropertyObject **или рекурсивный GetDiagnosticMessage** |
| `nested_list` | то же по каждому элементу |
| `script` | тип, params mismatch, затем рекурсия |
| `ui_image` | нет png/tga/dds/jpg по пути |

`prop_meta.validate` на combo (например Sector ID) срабатывает **при смене поля**, не как фоновый GetError.

## ModItem / preset

`ModItemPreset:GetError`: пустой `id`; иначе `GetError` класса пресета (`ModdedPresetClass`).

`ModItemPreset:GetWarning`: warning пресета или dirty + code file → Save/Test.

`ModItemFolder:GetDiagnosticMessage` пустой — папка не наследует ошибки детей.

## ModItemSector

Файл: `Lua/ModItemSector.lua`.

**GetError**

- `ShouldHideProp()` (нет campaignId или sectorId) → `Campaign and Sector ID should not be empty!`
- нет `SatelliteSectorObj` и в `CampaignPresets[campaign].Sectors` нет `Id == sectorId` → `Missing Satellite sector for %s`
- нет `mod.content_path .. Maps/<mapName>/mapdata.lua` → `Missing map data …`
- `SatelliteSectorObj.GroundSector` задан, сектора нет как duplicate в моде и `DoesSectorExist` ложно → нет ground sector. `DoesSectorExist` требует запись в campaign **с непустым Map**.

**GetWarning**

- dirty, или в campaign нет сектора с `Map == SatelliteSectorObj.Map` → `Save the mod item to add the sector in the campaign preset.`

**IsDuplicateMap** (validate campaign/sector fields): другой `ModItemSector` с той же парой campaign+sector.

**ValidateSectorId**: `^[A-Z]{1,2}-?\d{1,2}$` или с суффиксом `_Underground`.

`AddToCampaign` при наличии `SatelliteSectorObj` **подменяет** слот campaign этим объектом. Тонкий nested-объект без WeatherZone затирает leftover campaign-поля после load.

## SatelliteSector:GetError

ClassDef Satellite View:

- `Guardpost` без `EnemySquadsList`, или `""` в списке;
- `MusicCombat` / `MusicConflict` / `MusicExploration` отсутствуют в `Presets.RadioStationPreset["Default"]`;
- `MapData[self.Map].Region` и `GameStateDefs[region].WeatherCycle` и пустой `WeatherZone`.

Пустые дефолтные радио ванили обычно валидны. Кастомные имена вроде несуществующей станции — красное на **вложенном** объекте.

## Что Ged не проверяет

- Полноту файлов карты (`height_xor.grid`, `markers.debug.lua`).
- Согласованность `items.lua` ↔ `metadata.lua` ↔ companion (`$sync-jazz-generated-data`).
- Синтаксис `items.lua` до загрузки (лог игры / `_validate_items_quick.py`).
- Квестовые ссылки, setpiece companions, межпакетные `Mod/<id>/`.
- Состояние на диске, если редактор не Reload.

## Практика JAZZ

После правки generated data снаружи: закрыть или Reload редактор, не Save из памяти. Затем читать панель. Точный текст → этот skill. Нет текста → не закрывать editor AC как «ок».
