# Patch kit: jazz-nomaps (NoMaps)

**Пакет-владелец:** `JAZZ-nomaps` (`7MsJ2Eq`).

Cloud agent часто получает **403** на push в `Kpoji4er/JAZZ-nomaps` — apply владельцем из снапшотов/патчей ниже.

## Версии

| Rev | Что |
| --- | --- |
| **0.5** | cut loot scrub — [PR #1](https://github.com/Kpoji4er/JAZZ-nomaps/pull/1) на `main` |
| **0.6** | `ARMOR_REMAP` Flak/Kevlar→JazzArmor (`GEAR_REV=2`) — локальный commit `fbe5e44` |
| **0.7** | Global AI economy + clear `ErnieIsland.Sectors` (`AI_ECONOMY_REV=2`) — commit `6e824cd` / `0003-*.patch` |

Актуальные снапшоты в этой папке = **0.7** (включают 0.6 armor + 0.7 AI).

## Apply (0.7)

В клоне `JAZZ-nomaps` на `main` (после 0.5):

```bash
# предпочтительно: скопировать снапшоты
cp docs/patches/jazz-nomaps-0.4/NoMaps_Autonomy.lua Code/
cp docs/patches/jazz-nomaps-0.4/items.lua .
cp docs/patches/jazz-nomaps-0.4/metadata.lua .

# или патч поверх ветки с 0.6:
git apply docs/patches/jazz-nomaps-0.4/0003-nomaps-global-ai-economy.patch
```

`version_minor` → **7**.

Спека: [JAZZ-COMPAT-003](../../specs/active/JAZZ-COMPAT-003.md).  
Баг-заметки: [nomaps playtest](../../technical/bugs/nomaps-playtest-2026-07-30.md).
