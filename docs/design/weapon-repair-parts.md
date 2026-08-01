# Ремонт и запчасти оружия (design)

Канон: `docs/specs/active/JAZZ-WEAPONS-002.md` (resource/jam/BarrelParts/ScopeParts/ModifyWeapon+DnD; runtime wave pending).

## Расходники

| ID | RU | EN | Статус |
| --- | --- | --- | --- |
| `Parts` | Запчасти | Parts | **оставить** |
| `JAZZ_BarrelParts` | **Ствольные запчасти** | **Barrel Parts** | только **Barrel** slot (+ repair); не Stock/Muzzle/Scope |
| `JAZZ_ScopeParts` | **Детали прицелов** | **Scope Parts** | лом Scope при провале снятия; repair surcharge если на стволе remountable Scope |
| `FineSteelPipe` / `OpticalLens` / `Microchip` | — | — | **удалены из quoted costs** в `items.lua` (migrate → BarrelParts / Parts; orphan companions могут остаться до editor purge) |

Оставить в экономике также InventoryItem **аттачей** (removable). Permanent barrel craft — только `JAZZ_BarrelParts` (+ `Parts`).

## Removable / toggle

| Класс | Что |
| --- | --- |
| Removable (DnD, Mech≥30; GL≥40) | Scope, suppressor, compensator, light/laser, grip, bipod, mag, GL — Mech = **лучший в отряде** (как кабинет моддинга) |
| Toggle | Folding stock |
| Permanent | Barrel, non-fold stock, handguard structural, irons, **интегрированный глушитель** (`*SuppressorIntegrated`) |

Mag-as-ammo-container — **backlog**. Failed mount: **−1% max**, current clamp.

### Remove fail → break

После провала Mech на **снятии** (всегда −1% max):

`P(break|fail) = Clamp(100 - resourcePct, 0, 95)`  
`resourcePct = MulDivRound(current, 100, max)`

| Исход | Эффект |
| --- | --- |
| Не break | Аттач остаётся на оружии |
| Break + Scope (не Iron*) | Слот очищается; в сумку **`JAZZ_ScopeParts` × 1** |
| Break + прочий remountable | Слот очищается; предмет не выдаётся |

Install fail: только −1% max (аттач в сумке / на стволе не ломается этим броском).

### v1 InventoryItem scheme

Each removed module is a `JAZZ_RemovableAttachment` (or subclass) InventoryItem with
`RemovableComponentId = <live WeaponComponent ID>`. **Editor/loot catalog:** one
`ModItemInventoryItemCompositeDef` per remountable component, `Id == component id`
(folder `RemovableAttachments` in `items.lua`; companions `InventoryItem/<id>.lua`).
Generic `JAZZ_RemovableAttachment` remains the fallback base class. Generate/refresh via
`docs/tools/_gen_removable_attachment_items.py --apply`. Presentation (Icon / DisplayName /
rollover) syncs from `WeaponComponent` at create and via `GetItemUIIcon` /
`GetRolloverTitle` / `GetRolloverHint`. Install/DnD resolves vanilla↔`JAZZ_` twins.
UI drop mirrors ammo reload (`CanDropAt` / equip `_IsDropTarget`). Slots: Scope, Muzzle,
Side, Under, Bipod, Magazine, GrenadeLauncher; GL Mech **≥40**, others **≥30**.
`CanAppearInShop = true` (временный pass: Bobby Ray restock; `RestockWeight=10`, `MaxStock=1`, `Tier=1`). Исключения: `*SuppressorIntegrated`, `FlashlightOff`. Полный economy/loot plan — later. API:
`JAZZ_RemoveRemovableAttachment` / `JAZZ_InstallRemovableAttachment` /
`JAZZ_CreateRemovableAttachment` (prefers catalog class when present). Enable shop: `docs/tools/_enable_remountable_bobby_ray.py --apply`.

## Repair

`restoredPct = MulDivRound(restoredCurrent, 100, GetFactoryResource())`

| Resource | Cost |
| --- | --- |
| `JAZZ_BarrelParts` | `CeilDiv(restoredPct, 10)` — всегда при ремонте current |
| `JAZZ_ScopeParts` | `CeilDiv(restoredPct, 20)` — только если установлен remountable Scope |
| `Parts` | как vanilla RepairItems tick |

## Jam

| Тип | −max |
| --- | ---: |
| Обычный | 0.5% |
| Критический | 3% |

```
resourcePct = MulDivRound(current, 100, max)
P_crit = Clamp(5 + MulDivRound(100-resourcePct, 35, 100) + MulDivRound(Max(0,100-Mech), 25, 100), 5, 65)
```

UI: rollover карточки → `GetDisplayJamChancePercent`.

## Max / выстрел

Шанс **0.5%** −max за выстрел; при hit loss **≤ 1** unit.  
Также: jam, failed unjam, failed mount (−1% max). Ремонт max не поднимает.
