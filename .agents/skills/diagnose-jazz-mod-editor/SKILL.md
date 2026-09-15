---
name: diagnose-jazz-mod-editor
description: Разбирать красные и жёлтые пометки Mod Editor / Ged по официальным GetError, GetWarning и ValidateProperty, включая вложенные nested_obj. Использовать когда владелец видит ошибки в редакторе модов, статусбаре, «One or more nested objects», ignored mod, или спрашивает правила проверки пунктов мода. Агент не видит живую панель Ged.
---

# Диагностика панели Mod Editor

Агент **не видит** окно Ged. Не угадывать текст с панели. Просить точную строку (или скрин) и сопоставлять её с `GetError` / `GetWarning` / `ValidateProperty` в `<JA3_ROOT>/ModTools/Src`.

Это **не** парсер `items.lua` и **не** `check-generated-sync`. Пустое дерево Mod Items при загруженном metadata — лог `Failed to load mod items` (`.cursor/rules/jazz-items-metadata-validate.mdc`), не Ged-диагностика.

Полный обход и таблицы: [ged-diagnostics.md](references/ged-diagnostics.md).

## Когда подключать

- Владелец говорит, что редактор «ругается», подсвечивает пункт, пишет nested errors.
- После ручной правки `items.lua` / сектора / quest / preset и Reload.
- Round-trip `$sync-jazz-generated-data`: шаг «проверить панель сообщений».

## Как отвечает редактор

1. Ged открывает мод с `WarningsUpdateRoot = "root"`.
2. Периодически обходит дерево `GedEditedObject` (`PropertyObjectWarningsCache.lua`).
3. Для каждого объекта: `GetDiagnosticMessage` → сначала `GetError`, иначе `GetWarning`, иначе свойства через `ValidateProperty`.
4. `nested_obj` / `nested_list` (у сектора — **Satellite sector**) проверяются **тем же** алгоритмом рекурсивно.
5. Дети контейнера (подпункты мода) — как subitems.

Если вложенный объект красный, родитель часто показывает только:

```text
One or more nested objects have errors!
```

Точный текст — у вложенного пункта. Просить раскрыть его.

Панель считает **объекты в памяти открытого редактора**, не файлы на диске. После внешней правки без Reload диагностика врёт.

## Сектора (jazz-maps)

`ModItemSector:GetError` / `GetWarning` и вложенный `SatelliteSector:GetError` — частый источник после пересадки карт.

На `ModItemSector`:

- пустые Campaign / Sector ID;
- нет `SatelliteSectorObj` и сектора нет в campaign;
- нет `Maps/<mapId>/mapdata.lua`;
- underground: `GroundSector` не найден как сектор **с картой**;
- warning: dirty или в campaign нет сектора с тем же `Map` → Save.

На вложенном `SatelliteSector`:

- guardpost без отрядов / пустые слоты;
- `MusicCombat` / `MusicConflict` / `MusicExploration` нет в `RadioStationPreset.Default`;
- у `MapData[Map].Region` есть `WeatherCycle`, а `WeatherZone` пустой.

Дубликат `campaignId`+`sectorId` внутри мода ловится при смене поля (`IsDuplicateMap`), не фоновым GetError. Формат ID — `ValidateSectorId` при редактировании (`A18`, `A18_Underground`).

## Чеклист

- [ ] Есть точный текст панели, не пересказ.
- [ ] Отличен load-parse `items.lua` от Ged `GetError`.
- [ ] Если «nested objects» — запрошен текст **вложенного** объекта.
- [ ] Редактор Reload с диска, если файлы менялись снаружи; не Save из старой памяти.
- [ ] Для сектора проверены mapdata на диске, GroundSector, радио, WeatherZone vs Region.
- [ ] Источник найден в `<JA3_ROOT>/ModTools/Src` (приоритет) или GitHub drop; в tracked-файлах путь не писать абсолютно.

## Источники

| Что | Где |
| --- | --- |
| Сбор предупреждений | `<JA3_ROOT>/ModTools/Src/CommonLua/PropertyObjectWarningsCache.lua` |
| Порядок GetError → nested | `<JA3_ROOT>/ModTools/Src/CommonLua/PropertyObject.lua` (`GetDiagnosticMessage`, `ValidateProperty`) |
| Открытие редактора | `<JA3_ROOT>/ModTools/Src/CommonLua/Classes/GedModEditor.lua` |
| Сектор | `<JA3_ROOT>/ModTools/Src/Lua/ModItemSector.lua` |
| Вложенный sat-сектор | `SatelliteSector:GetError` в ClassDef Satellite View |
| Preset-обёртка | `ModItemPreset:GetError` / `GetWarning` в `ModItem.lua` |
