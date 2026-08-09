---
id: JAZZ-QUESTS-003
status: approved
owner: project-owner
systems:
  - maps-quests
  - strategy-squads
repositories:
  - jazz
  - jazz-maps
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - docs/specs/active/JAZZ-QUESTS-003.md
  - docs/design/ernie-garrison-baseline.md
  - docs/technical/systems/maps-quests-content-catalog.md
  - docs/tools/_purge_k4_house_ambushers.py
  - docs/tools/_add_villa_attackers_ernie.py
  - docs/tools/_tighten_villa_squads.py
  - docs/tools/_dump_villa_squads.py
  - docs/tools/README.md
  - ../jazz-units/items.lua
  - ../jazz-units/metadata.lua
  - ../jazz-maps/items.lua
  - ../jazz-maps/metadata.lua
  - ../jazz-maps/Code/System_VillaCounterAttack.lua
  - ../jazz-maps/Maps/gsSMikN/objects.lua
  - ../jazz-maps/docs/content/quests-locations-enemies.md
exclusive_resources:
  - jazz-units/items.lua
  - jazz-maps/items.lua
  - jazz-maps/Maps/gsSMikN/objects.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-QUESTS-003: Flag Hill villa counterattack (move squads)

## Проблема

На K4 (Flag Hill) старая on-map осада (`HouseAmbushers`+`Legion` AdvanceTo)
раздувает ForceConflict до диалога с Emma. Лагерные `VillaAttackers_*` сидят
как обычный Init вместе с Sentry, без квестовой контратаки. Нужна большая
контратака: после разговора Emma+Corazon двигать живые sat-волны на K4,
AdvanceTo к Emma, Wave2 по `CombatTurn`, опоздавшие колонны — на том же таймере.

## Цели

- Sentry = охрана лагеря; VillaAttackers = movable siege waves.
- После «гости» живые Attackers route → K4; Ernie pack 30 всегда.
- Старые HouseAmbushers+Legion AdvanceTo с K4 удалены.
- Атакующие на тактике сразу AdvanceTo `EmmaAndCorazon`.
- Wave2 ~25 на `CombatTurn` ≥ 3 только в бою после Emma guests.
- Опоздавшие sat-колонны материализуются на Wave2 TCE без двойного входа.

## Non-goals

- Difficulty UI ±10 (authored base + docs only).
- Прореживание Raiders/AL_Raiders.
- Ernie_CounterAttack (I7→I5).
- NoMaps villa.

## Требования

- `JAZZ-QUESTS-003-REQ-001` — Init лагерей: Sentry + VillaAttackers_*; Sentry не уходит в осаду.
- `JAZZ-QUESTS-003-REQ-002` — `Jazz_VillaCounterAttack_Start` двигает существующие sat-squads по `enemy_squad_def`, не Guardpost spawn.
- `JAZZ-QUESTS-003-REQ-003` — `JAZZ_Legion_VillaAttackers_Ernie` base 30 всегда стартует.
- `JAZZ-QUESTS-003-REQ-004` — K4 purge HouseAmbushers+Legion AdvanceTo; keep guests/WorldFlip Adonis/Rebels/Bastien/Raiders.
- `JAZZ-QUESTS-003-REQ-005` — Tactical AdvanceTo EmmaAndCorazon for attacking sat units only.
- `JAZZ-QUESTS-003-REQ-006` — Wave2 ~25 markers gated by quest; TCE CombatTurn≥3 after SiegeCombat.
- `JAZZ-QUESTS-003-REQ-007` — Late columns materialize on same TCE; cancel sat route.
- `JAZZ-QUESTS-003-REQ-008` — FlagHill_Emma_1 guests interrupt → quest + lock ~2h + Start().

## Инварианты и ограничения

- Не ломать `02_LiberateErnie` / `03A_PresidentNotes` выдачу.
- Не трогать World Flip Adonis ambush markers.
- Cleared camp (no Attacker squad) → that wave skips.
- No `TriggerGuardPostAttack` for this siege.

## Acceptance criteria

- `JAZZ-QUESTS-003-AC-001` — До диалога Attackers на лагерях; Sentry отдельно. Static.
- `JAZZ-QUESTS-003-AC-002` — После «гости» живые Attackers route → K4. Runtime/human.
- `JAZZ-QUESTS-003-AC-003` — Зачищенный лагерь → Attacker не в осаде. Runtime/human.
- `JAZZ-QUESTS-003-AC-004` — Ernie 30 всегда стартует. Static + runtime.
- `JAZZ-QUESTS-003-AC-005` — ~2h prep lock на K4. Runtime/human.
- `JAZZ-QUESTS-003-AC-006` — Нет TGPA в этой осаде. Static.
- `JAZZ-QUESTS-003-AC-007` — HouseAmbushers+Legion AdvanceTo purged. Static map audit.
- `JAZZ-QUESTS-003-AC-008` — Attackers AdvanceTo EmmaAndCorazon. Runtime/human.
- `JAZZ-QUESTS-003-AC-009` — Wave2 на CombatTurn≥3 after Emma siege combat only. Runtime/human.
- `JAZZ-QUESTS-003-AC-010` — Late sat dump on Wave2 TCE, no double spawn. Runtime/human.
- `JAZZ-QUESTS-003-AC-011` — items validate OK. Static.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: maps quest + Code; units EnemySquad; K4 objects.lua.
- Saves: mid-campaign Flag Hill may miss new quest if already past Emma — new game recommended for full siege.
- Network/determinism: NetSyncEvent for routes; CustomCode must be sync-safe.
- Generated data: items.lua / metadata.lua units+maps.
- Cross-package: jazz-units squad IDs referenced from jazz-maps Code/quest.
- Rollback: restore objects.lua HouseAmbushers; remove quest/Code.

## План и ownership

- Пакет-владелец: jazz-maps (quest/map/Code), jazz-units (Ernie squad), jazz (docs/spec/tools).
- Declared write set: see frontmatter.
- Exclusive resources: items.lua units/maps, gsSMikN/objects.lua.

## Решение владельца

- Статус: approved (plan implement request 2026-08-10).
- Кто подтвердил: project-owner.
- Дата: 2026-08-10.

## Evidence

- `JAZZ-QUESTS-003-AC-001`: `PASS` — static: camp Init Sentry+Attackers (dump script).
- `JAZZ-QUESTS-003-AC-002`: `BLOCKED` — runtime/human route after Guests.
- `JAZZ-QUESTS-003-AC-003`: `BLOCKED` — runtime/human wipe camp.
- `JAZZ-QUESTS-003-AC-004`: `PASS` — static: Ernie squad sum=30 in items + metadata.
- `JAZZ-QUESTS-003-AC-005`: `BLOCKED` — runtime/human lock.
- `JAZZ-QUESTS-003-AC-006`: `PASS` — static: Start uses SendSatelliteSquadOnRoute / GenerateEnemySquad, no TGPA.
- `JAZZ-QUESTS-003-AC-007`: `PASS` — static: `_verify_villa_counterattack_static.py` old siege remaining=0; Wave2=25.
- `JAZZ-QUESTS-003-AC-008`: `BLOCKED` — runtime AdvanceTo.
- `JAZZ-QUESTS-003-AC-009`: `BLOCKED` — runtime Wave2 CombatTurn.
- `JAZZ-QUESTS-003-AC-010`: `BLOCKED` — runtime late dump.
- `JAZZ-QUESTS-003-AC-011`: `PASS` — `_validate_items_quick.py` OK jazz-units + jazz-maps.

## Documentation delta

- `docs/design/ernie-garrison-baseline.md`
- `docs/technical/systems/maps-quests-content-catalog.md`
- `jazz-maps/docs/content/quests-locations-enemies.md`
- `docs/tools/README.md`
