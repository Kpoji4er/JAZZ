# V-UI-001 — Interactable highlight full-map scan every 200 ms

| Field | Value |
| --- | --- |
| Severity | P1 — Medium–High (UI while highlight held) |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/UI/IModeCommonUnitControl.lua` (~759–855) |
| Frequency | Realtime thread every **200 ms** while highlight is active |

## Problem

```lua
local interactables = MapGet("map", "Interactable", function(o)
    return not IsKindOf(o, "Door") and not o.spawned_by_explosive_object
end)
while true do
    ...
    highlight, action = haveSelection:CanInteractWith(o, false)
    ...
    Sleep(interactableHighlightUpdateInterval) -- 200
```

Builds a full-map Interactable list once, then repeatedly runs `CanInteractWith` without spatial / on-screen culling.

## Why CommonLib does not cover it

No CommonLib override of the interactable highlight thread.

## Suggested vanilla / engine fix

- Spatial index / only on-screen interactables.
- Reuse a `g_` registry updated on spawn/despawn.
- Skip off-screen objects before `CanInteractWith`.

## Mod notes

**Safe UI-only override** for mods: cull by camera/frustum, cache the list, keep gameplay interaction rules unchanged.
