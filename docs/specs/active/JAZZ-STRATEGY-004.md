---
id: JAZZ-STRATEGY-004
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - units-progression
repositories:
  - jazz
risk: low
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-004.md
  - jazz/Code/LegionUnitPrices.lua
  - jazz/metadata.lua
  - jazz/items.lua
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
exclusive_resources:
  - jazz/metadata.lua
  - jazz/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-004: strategic prices ($) for JAZZ_Legion_* units

## Проблема

Roadmap п.6a требует per-unit `$` для будущей генерации составов. Сейчас нет каталога цен; spawn списывает плоские role costs.

## Цели

- Data-driven таблица цен на все `JAZZ_Legion_*` combat/logistics UnitData (current: **38**, включая `JAZZ_Legion_Recruit`).
- Runtime accessors; spawn wiring — в последующих STRATEGY-008+ (не в scope 004).
- Technical docs + ссылка из roadmap.
- Шкала привязана к экономики: **полный дорогой отряд ≈ полный пул аванпоста ≈ 10 шипментов Майора**.

## Non-goals

- Подключение цен к recipes / balance caps в этом change (сделано позже в 008).
- Полная миграция abstract supply → money ledger runtime (roadmap п.0) — только целевые якоря в docs/roadmap.
- Изменение UnitData companions в `jazz-units`.

## Экономический якорь

| Величина | $ | Смысл |
|---|---:|---|
| `DiamondBriefcase` / полный shipment | 12000 | единичный «шипмент» |
| Целевой `OutpostCapacity` (п.0) | **120000** | ≈ **10** шипментов Майора → I7 |
| Полный дорогой garrison (~40, T3/T4 mix) | **≈120000** | спавн только при почти полном пуле |
| Poor/light составы | ≪ capacity | доступны без полного бака |

Целевой cargo одного Major→I7 supply-конвоя при миграции на $ — **12000**, чтобы десяток рейсов заполнял пул. Runtime capacity в этом change не меняется.

## Утверждённая шкала

| Class tier | Line | Specialist (MG/demo/medic/arty/sniper) | Leader |
|---|---:|---:|---:|
| T1 | 500 | 800 | 800 |
| T2 | 1000 | 1500 | 1500 |
| T3 | 2000 | 2800 | 2500 |
| T4 | 3500 | 4500 | 4000 |

## Полная таблица цен ($)

### Assault

| ID | $ |
|---|---:|
| JAZZ_Legion_Recruit | 200 |
| JAZZ_Legion_AssaultT1_Roughneck | 300 |
| JAZZ_Legion_AssaultT1_Grenadier | 800 |
| JAZZ_Legion_AssaultT1_Crusher | 400 |
| JAZZ_Legion_AssaultT2_Pillager | 800 |
| JAZZ_Legion_AssaultT2_ShockTrooper | 1000 |
| JAZZ_Legion_AssaultT2_Pyro | 1500 |
| JAZZ_Legion_AssaultT3_Punisher | 2000 |
| JAZZ_Legion_AssaultT3_SkullCrusher | 2000 |
| JAZZ_Legion_AssaultT4_Headsman | 3500 |

### Front

| ID | $ |
|---|---:|
| JAZZ_Legion_FrontT1_Rifleman | 500 |
| JAZZ_Legion_FrontT1_Bonemaker | 800 |
| JAZZ_Legion_FrontT1_Marauder | 500 |
| JAZZ_Legion_FrontT2_Ambusher | 1000 |
| JAZZ_Legion_FrontT2_Raider | 1000 |
| JAZZ_Legion_FrontT2_Marksman | 1000 |
| JAZZ_Legion_FrontT3_Sniper | 2800 |
| JAZZ_Legion_FrontT3_Veteran | 2000 |
| JAZZ_Legion_FrontT4_Mercenary | 3500 |
| JAZZ_Legion_FrontT4_MercenarySniper | 4500 |

### Flanker

| ID | $ |
|---|---:|
| JAZZ_Legion_FlankerT1_Warden | 500 |
| JAZZ_Legion_FlankerT2_Scout | 1000 |
| JAZZ_Legion_FlankerT2_Skirmisher | 1000 |
| JAZZ_Legion_FlankerT3_Recon | 2000 |
| JAZZ_Legion_FlankerT3_Pathfinder | 2000 |
| JAZZ_Legion_FlankerT4_Ranger | 3500 |

### Gunner

| ID | $ |
|---|---:|
| JAZZ_Legion_GunnerT1_Gunner | 800 |
| JAZZ_Legion_GunnerT2_GMPG | 1500 |
| JAZZ_Legion_GunnerT2_AssaultGunner | 1500 |
| JAZZ_Legion_GunnerT3_VeteranGunner | 2800 |
| JAZZ_Legion_GunnerT4_MercGunner | 4500 |

### Leader

| ID | $ |
|---|---:|
| JAZZ_Legion_LeaderT1_Sergeant | 800 |
| JAZZ_Legion_LeaderT2_Lieutenant | 1500 |
| JAZZ_Legion_LeaderT3_Captain | 2500 |
| JAZZ_Legion_LeaderT4_MercenaryCaptain | 4000 |

### Heavy

| ID | $ |
|---|---:|
| JAZZ_Legion_HeavyT1_Rocketeer | 800 |
| JAZZ_Legion_HeavyT2_Grenadier | 1500 |
| JAZZ_Legion_HeavyT3_Mortarman | 2800 |

## Sanity-band (static)

| Состав | Оценка | Доля от capacity 120000 |
|---|---:|---:|
| Recon ~10× T1/T2 light | ~8000 | ~7% |
| Patrol ~15× mixed T2 | ~18000 | ~15% |
| Poor garrison ~25× T1/T2 | ~20000 | ~17% |
| Full expensive garrison ~40× T3/T4 | **≈120000** | **~100%** |

## Требования

- `JAZZ-STRATEGY-004-REQ-001` — таблица содержит все ключи каталога `JAZZ_Legion_*` с ценой (current **38**, включая Recruit); без orphan keys.
- `JAZZ-STRATEGY-004-REQ-002` — `JAZZ_GetLegionUnitPrice` / `JAZZ_GetLegionSquadUnitPriceSum` доступны runtime.
- `JAZZ-STRATEGY-004-REQ-003` — файл загружается через `metadata.code` и `items.lua` ModItemCode.
- `JAZZ-STRATEGY-004-REQ-004` — technical docs и roadmap ссылаются на STRATEGY-004.
- `JAZZ-STRATEGY-004-REQ-005` — шкала согласована с якорем: дорогой full garrison ≈ 10×$12000; целевой outpost capacity в roadmap = 120000.

## Инварианты и ограничения

- Не менять spawn costs в `Guardpost_Patrols.lua` **в рамках 004** (spawn charging — 008).
- Не менять `jazz-units` UnitData.
- Цены — strategic `$`, не InventoryItem.Cost.
- Runtime outpost capacity/supply в этом change не трогать (только docs/roadmap targets).

## Acceptance criteria

- `JAZZ-STRATEGY-004-AC-001` — static: price keys ⊇ combat Legion UnitData + Recruit; no orphan keys (current 38/38).
- `JAZZ-STRATEGY-004-AC-002` — static: accessors определены; code registered.
- `JAZZ-STRATEGY-004-AC-003` — docs updated; якорь 10×shipment / capacity 120000 зафиксирован.
- `JAZZ-STRATEGY-004-AC-004` — static: sample expensive ~40 T3/T4 sum в полосе 100000–130000.
- `JAZZ-STRATEGY-004-AC-005`: `PASS (runtime/human)` — owner playtest accepted 2026-07-28.

## Impact и совместимость

- **Runtime:** новый loaded code module only; spawn costs не меняются.
- **Saves/network:** none.
- **Generated:** `metadata.lua` + `items.lua` code registration transaction.
- **Downstream:** п.0 должен принять OutpostCapacity=120000 и supply cargo=12000.
- **Rollback:** удалить `LegionUnitPrices.lua` и регистрацию; откатить docs.

## План и ownership

1. `jazz` — spec, `Code/LegionUnitPrices.lua`, metadata/items registration, technical docs, roadmap pointer.
2. Runtime smoke accessor — владелец (опционально).
3. Money ledger capacity/cargo — отдельный spec п.0.

## Решение владельца

28 июля 2026 — план «Legion unit prices» утверждён; шкала подогнана так, что один дорогой отряд требует почти полный пул аванпоста ≈ десяток шипментов Майора ($120000).

## Evidence

- `JAZZ-STRATEGY-004-AC-001`: `PASS (static)` — 38 price keys including `JAZZ_Legion_Recruit` @200; docs sync 2026-07-29
- `JAZZ-STRATEGY-004-AC-002`: `PASS (static)` — `LegionUnitPrices.lua` registered; accessors present; consumed by generator/spawn after 008
- `JAZZ-STRATEGY-004-AC-003`: `PASS (static)` — technical docs + roadmap 6a/п.0 anchor (capacity 120000 = 10×$12000)
- `JAZZ-STRATEGY-004-AC-004`: `PASS (static)` — sample expensive 40-man T3/T4 mix ≈ $105k–$122k band vs capacity $120000
- `JAZZ-STRATEGY-004-AC-005`: `PASS (runtime/human)` — owner playtest accepted 2026-07-28

## Documentation delta

- `docs/specs/active/JAZZ-STRATEGY-004.md`
- `docs/technical/systems/legion-units-equipment-tiers.md`
- `docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md`
