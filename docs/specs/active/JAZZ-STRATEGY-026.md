---
id: JAZZ-STRATEGY-026
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - legion-tier
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: not-required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-026.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/Code/LegionTierProgression.lua
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/docs/tools/_check_strategy026_tier_convoys.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - jazz/Code/Guardpost_Patrols.lua pulse spawn
  - jazz/Code/LegionTierProgression.lua raise Msg
related_decisions:
  - none
approved_by: project-owner chat 2026-08-24
---

# JAZZ-STRATEGY-026: Legion sub-tier money pulse; T2 all-outpost money+people

## Проблема

Рост подтира Легиона меняет лут и будит материк (T2), но штаб Майора не реагирует логистикой. Обычные supply/manpower ждут нужды (40% казны / manpower=0), neediest-очереди и суточного пула STRATEGY-019 (1/2/3 новых отряда). Игрок не видит «Майор подбросил ресурсы» в момент смены тира.

## Цели

- Каждый **реальный** рост подтира (`JAZZ_Legion_Tier` увеличивается) сразу пускает со штаба Майора **денежный** караван (`supply`, стандартный cargo) на один живой незахваченный аванпост.
- Этот рейс **не** ест суточный пул `lSpawnManaged` / STRATEGY-019.
- Переход на major **T2** (`old < 21` и `new >= 21`) шлёт на **каждый** живой незахваченный аванпост пару караванов: **деньги** (`supply`) и **люди** (`manpower`).
- На том же T2-переходе отдельный одиночный денежный импульс **не** дублируется.

## Non-goals

- Менять формулу тира, caps подтиров, Maps/NoMaps триггеры.
- Менять обычные supply/manpower ворота (40%, manpower=0, neediest, 12h loading, treasury deduct).
- Менять размер суточного пула 1/2/3.
- Dual-payload в одном отряде (деньги+люди в одном squad).
- Новый InventoryItem / Bobby Ray.
- Пакеты `jazz-units` / `jazz-maps` / `jazz-nomaps`.
- Импульс на NewGame запись T1-1 (`11`) и на LoadGame без фактического raise.

## Locked defaults

| Param | Value |
| --- | --- |
| Sub-tier pulse | one `supply` from Major HQ |
| Sub-tier target | living uncaptured outposts; `MajorSupplyPriority` desc, then lowest `$`, then sector id |
| T2 crossing | `old < 21` and `new >= 21` |
| T2 pulse | one `supply` **and** one `manpower` per living uncaptured outpost |
| Supply cargo | `SupplyConvoyCargo` default **$12000** |
| Manpower cargo | `ManpowerConvoyCargo` default **16** |
| Daily spawn pool | **not** consumed (`skip_global_spawn`) |
| Major treasury / manpower | **not** deducted (off-map Major reserve) |
| 12h HQ loading | skipped when avoid-player route exists; else spawn at HQ and retry via existing hourly loading tick |
| Idle reuse | not used (always new spawn) |
| Living uncaptured | `outpost.enabled`, Legion Side, `owner_faction` empty or `legion`; not Major HQ itself |

## Требования

- `JAZZ-STRATEGY-026-REQ-001` — `lApplyTierRaise` after a real increase fires `Msg("JAZZ_LegionTierRaised", old, new)`; NewGame write of `11` does not fire.
- `JAZZ-STRATEGY-026-REQ-002` — `lSpawnManaged` accepts `opts.skip_global_spawn`; pulse uses it and does not call `lConsumeGlobalSpawn`.
- `JAZZ-STRATEGY-026-REQ-003` — non-T2 raise: one HQ→priority living outpost `supply` pulse; skip 40% trigger, neediest-wait, treasury deduct, daily pool.
- `JAZZ-STRATEGY-026-REQ-004` — T2 crossing: `supply` + `manpower` pulse to every living uncaptured outpost; no extra single-money pulse; skip manpower==0 and neediest gates; skip pool and treasury/manpower deduct.
- `JAZZ-STRATEGY-026-REQ-005` — pulse leaves immediately if avoid-player path exists; otherwise holds at HQ (`phase=loading`, `hold_until=now`) instead of silent skip/retire.
- `JAZZ-STRATEGY-026-REQ-006` — player-facing docs: technical + wiki + showcase RU/EN + roadmap row.

## Инварианты и ограничения

- Regular command-window logistics unchanged (STRATEGY-019 order, 018 no-path skip for **regular** supply/manpower, 021 neediest).
- Pulse is STRATEGY-018 exception: spawn even without a path, then hold/retry (same spirit as reinforce/support).
- Deterministic outpost walk: `sorted_pairs` / stable sector-id ties. No extra `InteractionRand` on target pick (squad-def pick may still use existing spawn rand).
- Save schema stays **v3**. Existing campaigns get pulses only on **future** raises.
- HQ lost (not Legion Side) → no pulse from that raise.
- No living outposts → no pulse.
- T3 crossing (`25→31`) is a sub-tier-style money pulse, not a T2 burst.

## Acceptance criteria

- `JAZZ-STRATEGY-026-AC-001` — static: `Msg("JAZZ_LegionTierRaised"` in `lApplyTierRaise` after a successful increase.
- `JAZZ-STRATEGY-026-AC-002` — static: `skip_global_spawn` gate on `lSpawnManaged`; pulse helpers call it; `lConsumeGlobalSpawn` not on that path.
- `JAZZ-STRATEGY-026-AC-003` — static: T2 branch `old < 21 and new >= 21` sends supply+manpower per living outpost; else one priority supply.
- `JAZZ-STRATEGY-026-AC-004` — static: pulse helpers do not write `root.major.money` / `root.major.manpower`; skip 12h load when routed.
- `JAZZ-STRATEGY-026-AC-005` — static: technical + wiki + showcase RU/EN describe the pulse and that it ignores the daily new-squad cap.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: jazz-only Msg + director pulse. No vanilla symbol rename.
- Saves: additive behavior; no schema bump. Old saves: pulses on later raises only.
- Network/determinism: NetSync travel via existing `lSetRoute`. Target pick has no extra rand.
- Generated data: none.
- Cross-package references: none.
- Rollback/recovery: revert the two Lua files and docs.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: frontmatter `write_set`
- Exclusive resources: frontmatter `exclusive_resources`

## Решение владельца

- Статус: implemented
- Кто подтвердил: project-owner
- Дата: 2026-08-24
- Формулировка: каждый подтир — денежный караван от Майора без очереди; переход на T2 — караваны с людьми и деньгами на каждый живой незахваченный аванпост.

## Evidence

- `JAZZ-STRATEGY-026-AC-001`: `PASS` — static `docs/tools/_check_strategy026_tier_convoys.py` (`Msg` after RIS in `lApplyTierRaise`)
- `JAZZ-STRATEGY-026-AC-002`: `PASS` — static: `skip_global_spawn` gates `lConsumeGlobalSpawn`; pulse helpers pass the flag
- `JAZZ-STRATEGY-026-AC-003`: `PASS` — static: T2 `old < 21 and new >= 21` calls supply+manpower per living outpost; else one priority supply
- `JAZZ-STRATEGY-026-AC-004`: `PASS` — static: pulse helpers do not assign `root.major.money` / `manpower`; no-path hold uses `hold_until = lNow()`
- `JAZZ-STRATEGY-026-AC-005`: `PASS` — technical + wiki + showcase RU/EN describe the pulse and daily-cap exception

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — pulse contract, skip-pool, T2 burst.
- `docs/technical/systems/legion-units-equipment-tiers.md` — raise fires `JAZZ_LegionTierRaised`.
- `docs/wiki/legion-global-ai.md` — player wording.
- `docs/showcase/ru/legion-strategy.md` + `en/legion-strategy.md` — same.
- `docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md` — done row 026.
