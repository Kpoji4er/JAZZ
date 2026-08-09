---
id: JAZZ-STRATEGY-025
status: implemented
owner: project-owner
systems:
  - legion-global-ai
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-025.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/RussianManual.csv
  - jazz/Localization/EnglishManual.csv
  - jazz/Localization/Strings.csv
  - jazz/docs/tools/_check_legion_rest_025.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - jazz/Code/Guardpost_Patrols.lua rest/return path
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-025: local rest at cities/bunkers; outpost for replenishment

## Проблема

После mission budget / wounded retreat regular-отряды всегда едут на `home_sector` (аванпост). Нельзя отдохнуть в уже занятом Legion-городе или бункере; лишние поездки на форт.

## Цели

- Regular combat roles могут **отдыхать** (`resting` / heal) на Legion-controlled **городе**, **бункере** или **своём аванпосте** (аванпост — нормальное место отдыха).
- Если отряд **уже стоит** на валидном local rest site — остаётся там (не едет на аванпост «просто отдохнуть»).
- Если в поле — едет на **ближайший** local rest site в регионе (город ближе аванпоста → город; аванпост ближе → аванпост).
- Поездка на аванпост за **пополнением** — только если отряд **сильно поредел/ранен** (`lSquadNeedsWoundedRetreat`) **и** на аванпосте есть `$`/manpower, достаточные чтобы top-up хоть кого-то добавить.
- Top-up (докуп юнитов) по-прежнему только на аванпосте (`home_sector` outpost pools).

## Non-goals

- Rest на фермах/шахтах/портах (только city / bunker / outpost).
- Top-up в городе/бункере.
- Смена `home_sector` на город (home остаётся managed outpost).
- Logistics roles (tax/recruiter/supply/…) — без изменения (по-прежнему home outpost / HQ).
- Garrison skip-rest (STRATEGY-013) без изменений.

## Locked defaults

### Local rest site

Sector qualifies if Legion Side and any of:

| Kind | Detection |
| --- | --- |
| Outpost home | `root.outposts[id].enabled` for this squad’s `home_sector` |
| City | `City ~= "none"` (surface or underground) |
| Bunker | truthy `sector.Bunker` |

### Rest return (`reason ~= "wounded"`)

1. If `CurrentSector` is local rest site (city / bunker / home outpost) → rest in place.
2. Else pick **nearest** (by `GetSectorDistance`) among city / bunker / home outpost in the region; fallback `home_sector`. Closer city beats farther outpost; outpost remains valid when it is nearest or equal-distance wins by stable id tie-break.
3. At non-outpost rest: heal + rest timer; **no** top-up. At home outpost: heal + optional top-up as before.

### Wounded / understrength return

1. If home outpost can afford a non-empty top-up toward optimal → target `home_sector` (`return_wounded`).
2. Else if current (or nearest) local rest site exists → rest/heal there; state `wounded` if still under optimal after heal.
3. Else fallback `home_sector`.

### Scheduler

`lAssignReadySquads` finishes `resting` and may assign orders when squad is at **any** valid rest site for that squad (not only outpost tile). Top-up attempts only when `CurrentSector == home_sector`.

## Требования

- `JAZZ-STRATEGY-025-REQ-001` — `lSectorIsLocalRestSite` + pick/nearest helpers.
- `JAZZ-STRATEGY-025-REQ-002` — budget rest prefers local city/bunker/outpost; no forced outpost trip if already local.
- `JAZZ-STRATEGY-025-REQ-003` — wounded trip to outpost gated by affordable top-up; else local rest.
- `JAZZ-STRATEGY-025-REQ-004` — top-up only at home outpost; rest finish works off-outpost.
- `JAZZ-STRATEGY-025-REQ-005` — docs wiki/showcase/technical + optional task UI wording.

## Инварианты и ограничения

- STRATEGY-012 retreat thresholds unchanged.
- STRATEGY-013 rest duration / garrison skip unchanged.
- Deterministic InteractionRand for rest duration only (path pick uses sorted distance + stable id tie-break).
- Saves: additive task targets; old saves OK.

## Acceptance criteria

- `JAZZ-STRATEGY-025-AC-001` — static: helpers + return path branches wired.
- `JAZZ-STRATEGY-025-AC-002` — static: top-up still requires home outpost; rest finish off-outpost.
- `JAZZ-STRATEGY-025-AC-003` — docs/wiki/showcase updated.
- `JAZZ-STRATEGY-025-AC-004` — runtime/human: squad rests in city/bunker; wounded only rides to fort when outpost can refill.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: Guardpost_Patrols only; medium.
- Saves: additive.
- Network/determinism: sorted sector picks.
- Generated data: none.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Declared write set: см. frontmatter

## Решение владельца

- Статус: **approved** (owner 2026-08-10: rest in cities/bunkers; outpost for replenishment when badly wounded and resources exist)
- Дата: 2026-08-10

## Evidence

- `JAZZ-STRATEGY-025-AC-001`: `PASS` — static `docs/tools/_check_legion_rest_025.py`
- `JAZZ-STRATEGY-025-AC-002`: `PASS` — static: top-up home gate + AssignReady `at_rest`
- `JAZZ-STRATEGY-025-AC-003`: `PASS` — technical/wiki/showcase RU+EN updated
- `JAZZ-STRATEGY-025-AC-004`: `BLOCKED` — runtime/human playtest

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md`
- `docs/wiki/legion-global-ai.md`
- `docs/showcase/ru|en/legion-strategy.md`
- roadmap row
