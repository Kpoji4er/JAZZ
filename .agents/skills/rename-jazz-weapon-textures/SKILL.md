---
name: rename-jazz-weapon-textures
description: >-
  Нормализовать DDS текстуры оружия в jazz_assets: Entity_MapType.dds,
  unused purge, content-dedupe, sync .mtl и items.lua. Использовать после
  editor import новой пушки с numeric DDS, при texture rename, unused
  textures, JAZZ-ASSETS-002.
---

# Rename weapon textures (jazz_assets)

Пакет: `jazz_assets` → `Entities/Textures/` (+ `Fallbacks/`), `Entities/Materials/*.mtl`, `items.lua`.  
Скрипт: [`../sync-jazz-generated-data/scripts/texture-audit-rename.ps1`](../sync-jazz-generated-data/scripts/texture-audit-rename.ps1).  
Spec: `docs/specs/active/JAZZ-ASSETS-002.md`.

## Когда

- После Mod Editor import нового оружия/attachment с **цифровыми** DDS.
- Массовый cleanup numeric → читаемые имена.
- Поиск/удаление unused DDS.

**Не** для mesh/FBX import и **не** для ручного patch `BinAssets/*.mtlbin`.

## Контракт имён

| MTL slot | Suffix |
| --- | --- |
| BaseColorMap | `Base` |
| NormalMap | `Norm` |
| RMMap | `RM` |
| AOMap | `AO` |
| SpecialMap | `SPEC` |
| SIMap | `SI` |
| ColorizationMap | `Color` |

Имя: `<EntityOrPart>_<Suffix>.dds`, коллизии → `…_2`, `…_3`.  
Owner: body entity предпочтительнее Mag/Barrel/Bipod/…  
Байт-идентичные used → один файл **только если тот же map-suffix** (не склеивать Norm с Base).  
Fallbacks переименовывать/удалять **парой** с Textures.

## Workflow (новый ствол)

```text
- [ ] 1. Entity уже в jazz_assets (editor import), numeric DDS на диске
- [ ] 2. DryRun с -EntityFilter <Name>
- [ ] 3. Проверить docs/texture-rename-map.csv (owner/suffix)
- [ ] 4. Apply с тем же -EntityFilter
- [ ] 5. Mod Editor: Save materials / SaveWholeMod → пересобрать mtlbin
- [ ] 6. Runtime: оружие в руках/на земле; лог без missing …dds
```

```powershell
# Из корня jazz/
.agents/skills/sync-jazz-generated-data/scripts/texture-audit-rename.ps1 `
  -AssetsRoot ..\jazz_assets `
  -EntityFilter AA52 `
  -DryRun

.agents/skills/sync-jazz-generated-data/scripts/texture-audit-rename.ps1 `
  -AssetsRoot ..\jazz_assets `
  -EntityFilter AA52 `
  -Apply
```

Полный пакет (все numeric): тот же скрипт **без** `-EntityFilter`.

## Отчёты

Пишутся в `jazz_assets/docs/`:

- `texture-rename-map.csv`
- `texture-unused-candidates.txt` / `texture-unused-deleted.txt`
- `texture-content-dupes.csv`
- `texture-audit-summary.txt`

## Запреты

- Не патчить содержимое `BinAssets/*.mtlbin` вручную (hex/string replace).
- После Apply: если `mtlbin` ещё ссылается на удалённые numeric DDS — **удалить эти stale mtlbin** (движок читает `.mtl`) либо SaveWholeMod в Mod Editor для полной регенерации.
- Не удалять DDS, пока basename есть в `.mtl`.
- Не смешивать rename с mass FBX re-export в одном change set.
- После Apply: `check-asset-integrity.ps1`; delimiter check `items.lua`.

## Ссылки

- Current-state: `docs/technical/systems/assets-entities.md`
- Sync skill: `$sync-jazz-generated-data`
