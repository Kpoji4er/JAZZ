---
id: JAZZ-COMPAT-008
status: approved
owner: project-owner
systems:
  - units-progression
  - strategy-squads-sectors
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-COMPAT-008.md
  - jazz/Code/LegionTierProgression.lua
  - jazz/items.lua
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/design/legion-loadouts.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-units.md
  - jazz/docs/showcase/en/legion-units.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
exclusive_resources:
  - Quest:JAZZ_LegionTier
  - Code:LegionTierProgression.lua
  - GameVar:gv_JAZZ_LegionTierMaps
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMPAT-008: Maps Legion gear tier (time + mainland + mines)

## Проблема

На профиле **с maps** `JAZZ_Legion_Tier` двигают TCE по `PlayerControlSectors`. На Эрни не все сектора обязательны к захвату: можно застрять на раннем тире или, наоборот, набрать порог `21` ещё на острове до высадки на материк. Сеточная прогрессия не отражает темп кампании (остров → большая земля → шахты).

## Цели

- Maps-профиль: time/event прогрессия снаряжения Легиона вместо sector-count TCE.
- T1: до `13` за ~**2 недели** кампании (sub каждые **7** дней).
- T2-1 (`21`): при **занятии** первого non-Ernie surface-сектора (смена `Side` на player), не при найме мерков / простом присутствии отряда.
- T2/T3 sub: каждые **~30** дней.
- T3-1 (`31`): при **5** player-owned шахтах.
- Потолок на острове без материка: `13`.
- NoMaps (COMPAT-003) без регрессии.
- Тир только вверх; реген лута как раньше.

## Non-goals

- Смена LootDef bands / UNITS-003 generator.
- Смена NoMaps формулы (mine+3d / WorldFlip / 3d·14d).
- Class-weight / COMPAT-005 remap.
- Авто-T2 по квесту вывоза без занятия материкового сектора.

## Требования

- `JAZZ-COMPAT-008-REQ-001` — при **не** `JAZZ_NoMapsIsActive()` quest TCE `JAZZ_LegionTier` по `PlayerControlSectors` **не** меняют `JAZZ_Legion_Tier` (gate `false` / dead).
- `JAZZ-COMPAT-008-REQ-002` — Maps progression в `Code/LegionTierProgression.lua` + `gv_JAZZ_LegionTierMaps`; только вверх; смена → `RegenerateLegionLoot()`.
- `JAZZ-COMPAT-008-REQ-003` — major/sub (Maps):

| Major | Как открывается | Sub step | Max encoded |
| ---: | --- | --- | ---: |
| 1 | старт | каждые **7** дней | `11`→`12`→`13` |
| 2 | первая **оккупация** non-Ernie **surface** сектора (`SectorSideChanged` → player1/player2) | каждые **30** дней | `21`…`25` |
| 3 | **5** player-owned `Mine` (surface) | каждые **30** дней | `31`→`32`→`33` |

- `JAZZ-COMPAT-008-REQ-004` — Ernie geography: Sector Id из Region preset `ErnieIsland.Sectors` (fallback: WeatherZone `Erny` / City `ErnieVillage`|`Rebels_Ernie`|`SmugglersErnie` / Label1 `Ernie`). Underground / water / blocked не считаются mainland-триггером.
- `JAZZ-COMPAT-008-REQ-005` — найм AIM/импорт мерка, travel через чужой сектор **без** смены `Side` **не** открывают major 2.
- `JAZZ-COMPAT-008-REQ-006` — без mainland occupation потолок `13` (даже после долгого времени на острове).
- `JAZZ-COMPAT-008-REQ-007` — existing maps save: не понижать tier; при уже player-owned non-Ernie surface latch `mainland_at`; NoMaps path неизменен.
- `JAZZ-COMPAT-008-REQ-008` — docs: technical + wiki/showcase RU/EN; design L2 note; COMPAT-003 maps-TCE clause superseded by this spec.

## Инварианты и ограничения

- Public quest/var IDs: `JAZZ_LegionTier` / `JAZZ_Legion_Tier`.
- Deterministic; без лишнего NetSync.
- Не ломать NoMaps time formula / WorldFlip T3.

## Acceptance criteria

- `JAZZ-COMPAT-008-AC-001` — static: все TCE `JAZZ_Legion_*` gated `false` (или эквивалент never-fire).
- `JAZZ-COMPAT-008-AC-002` — static: Maps formulas (7d / mainland Side / 5 mines / 30d) + Ernie sector helper.
- `JAZZ-COMPAT-008-AC-003` — static: NoMaps functions/hooks still present and gated to `JAZZ_NoMapsIsActive`.
- `JAZZ-COMPAT-008-AC-004` — runtime/human: Ernie stay → max `13` ~day 14; occupy mainland → `≥21`; 5 mines → `≥31`; AIM hire alone → no T2.
- `JAZZ-COMPAT-008-AC-005` — docs delta applied; `_validate_items_quick.py` OK if `items.lua` touched.

## Impact и совместимость

- Vanilla/CommonLib: только чтение `SectorSideChanged` / sector flags.
- Saves: GameVar `gv_JAZZ_LegionTierMaps`; tier never decreases.
- Network/determinism: CampaignTime + side changes.
- Generated data: quest TCE expressions in `items.lua`.
- Cross-package: `jazz-units` LootDef consumers unchanged.
- Rollback: restore TCE gate + remove Maps branch.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. front-matter
- Exclusive resources: quest + LegionTierProgression + GameVar maps

## Решение владельца

- Статус: **approved**
- Кто подтвердил: project-owner (chat 2026-08-05)
- Дата: 2026-08-05
- Решения: mainland = SectorSide change only (A); T3 = **5** mines; island cap `13`; never-leave-Ernie cap `13`.

## Evidence

- `JAZZ-COMPAT-008-AC-001`: `PASS (static)` — 11 TCE `CheckExpression` → `return false` in `items.lua`.
- `JAZZ-COMPAT-008-AC-002`: `PASS (static)` — Maps formulas 7d / mainland Side / 5 mines / 30d; `JAZZ_IsErnieIslandSector` + `JAZZ_NoteMapsMainlandOccupation`.
- `JAZZ-COMPAT-008-AC-003`: `PASS (static)` — NoMaps path preserved behind `JAZZ_NoMapsIsActive`.
- `JAZZ-COMPAT-008-AC-004`: `BLOCKED (runtime/human)` — Ernie cap / mainland / 5 mines / AIM hire smoke.
- `JAZZ-COMPAT-008-AC-005`: `PASS (static)` — technical + wiki + showcase RU/EN + design L2; `_validate_items_quick.py` OK.

## Documentation delta

- `docs/technical/systems/legion-units-equipment-tiers.md` — Maps time/event table; TCE retired.
- `docs/design/legion-loadouts.md` — L2 trigger note.
- `docs/wiki/legion-global-ai.md` + showcase RU/EN `legion-units` / `legion-strategy`.
- `docs/specs/active/JAZZ-COMPAT-003.md` — note maps TCE superseded (optional one-liner).
