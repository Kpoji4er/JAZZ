# Patch: jazz-nomaps 0.4 — cut loot / ammo sanitize

Cloud agent **не имеет push** в `Kpoji4er/JAZZ-nomaps` (403). Коммит собран локально; применить вручную в репо nomaps.

## Что чинит

- LootDef / fallback: `JAZZ_AMMO_*` вместо `_9mm_Basic`/…; `MP5A2` вместо cut `MP5`
- Deny cut / `_*` / `TEST.png` при inject
- `lSanitizeUnitAmmo` после gear refresh
- `version_minor` → **4**

## Применить

```bash
cd ../jazz-nomaps   # или clone Kpoji4er/JAZZ-nomaps
git am /path/to/jazz/docs/patches/jazz-nomaps-0.4/0001-fix-cut-loot.patch
# либо скопировать файлы ниже поверх корня пакета:
#   items.lua → items.lua
#   metadata.lua → metadata.lua
#   NoMaps_Autonomy.lua → Code/NoMaps_Autonomy.lua
git push
```

Снимок файлов в этой папке соответствует коммиту `3758a58` на ветке `cursor/nomaps-cut-loot-fix-88b8` (локально у агента).

См. также: [nomaps playtest bugreport](../technical/bugs/nomaps-playtest-2026-07-30.md), [cut-content](../technical/weapons/cut-content.md).
