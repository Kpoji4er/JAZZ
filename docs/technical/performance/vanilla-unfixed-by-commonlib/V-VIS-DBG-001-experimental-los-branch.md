# V-VIS-DBG-001 — Experimental LOS branch left in shipped path

| Field | Value |
| --- | --- |
| Severity | P2 — Low (branch cost unless debug left on) |
| CommonLib | **Not fixed** |
| Vanilla path | `Lua/Tactical/Visibility.lua` (~251–272) |
| Frequency | LOS computation when `g_ExperimentalModeLOS` is consulted |

## Problem

Vanilla still carries `g_ExperimentalModeLOS` / TODO-to-remove experimental LOS branching on the shipped visibility path.

## Why CommonLib does not cover it

CommonLib does not strip experimental LOS from retail builds.

## Suggested vanilla / engine fix

- Remove experimental LOS from retail/shipping builds.
- Gate any remaining experiments behind editor/debug-only compilation.

## Mod notes

Not worth a mod override unless a specific debug mode is stuck enabled in the field.
