# V-UI-003 — Nested inventory `ForEachItem` (Take All / free space)

| Field | Value |
| --- | --- |
| Severity | P1 — Medium (UI stalls, not combat FPS) |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/XTemplates/Inventory.lua` (~564–584); `Inventory.lua` `InventoryTakeAllNet` (~2949+) |
| Frequency | Action-state checks / Take All |

## Problem

Free-space / Take All paths nest container item walks inside per-unit inventory walks (containers × items × units).

```lua
local result = container:ForEachItemInSlot(container_slot_name, false, function(item, ...)
    for _, unit in ipairs(units) do
        local res = unit:ForEachItemInSlot("Inventory", item.class, function(itm, ...)
```

Combat hit resolution is **not** the primary nested-ForEachItem cost; loot/UI is.

## Why CommonLib does not cover it

Recipe ingredient caches exist in CommonLib; inventory Take All / free-space nesting does not.

## Suggested vanilla / engine fix

- Index stacks by class.
- Single-pass free-space estimate.
- Keep net transfer order for Take All.

## Mod notes

UI enable checks are safe to optimize. `InventoryTakeAllNet` must preserve transfer order for sync.
