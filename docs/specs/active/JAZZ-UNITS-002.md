---
id: JAZZ-UNITS-002
status: approved
owner: project-owner
systems:
  - units-progression-specializations
  - localization
  - merc-portraits
repositories:
  - jazz
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/CharacterEffect/Jazz_Perk_*.lua
  - jazz/Code/System_OR_Grenade.lua
  - jazz/Code/System_OR_Traps.lua
  - jazz/Code/System_OR_Weapons.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/**
  - jazz-units/UnitData/Jazz_*.lua
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz-units/MercPortraits/**
  - jazz/docs/design/mercs-ja12/**
  - jazz/docs/technical/systems/units-progression-specializations.md
exclusive_resources:
  - jazz/items.lua
  - jazz-units/items.lua
  - localization ID range 890000000001700-890000000002999
related_decisions:
  - none
approved_by: project-owner chat 2026-07-28 generate-all-mercs-by-priority
---

# JAZZ-UNITS-002: JA12 merc generation wave (priority queue)

## Проблема

В `docs/design/mercs-ja12/` 44 planned-статьи (`executable: false`) без UnitData/perk/loot/портретов/loc. Ready только lynx/tosca/spider/spouke. Нужна полная генерация по приоритету High→Medium→Low.

## Цели

- Сгенерировать всех 44 мерков из [`_generation-queue.md`](../../design/mercs-ja12/_generation-queue.md) в порядке приоритета.
- Каждый slug: executable article → UnitData + named perk + loot + Appearance + VR + Portraits 300/2000 + RU/EN loc.
- Портреты входят в DoD каждого мерка (JA2 face match при наличии `*.ja2-face.*`).
- После общего генерационного прохода исправить подтверждённые владельцем дефекты likeness, 3D appearance и AIM-озвучки без custom mesh/texture scope.

## Non-goals

- Push/release/tags.
- Полный custom mesh/texture appearance (клон существующего preset).
- Mass format unrelated Lua.
- Генерация уже Ready (lynx/tosca/spider/spouke).
- Любые изменения `JAZZ_Spouke`: его 2D/3D appearance подтверждены владельцем и остаются нетронутыми.

## Требования

- `JAZZ-UNITS-002-REQ-001` — очередь High→Medium→Low; следующий slug только после DoD предыдущего (или явного parallel batch без пересечения exclusive write в один момент).
- `JAZZ-UNITS-002-REQ-002` — каждый мерк: `unit_id`, `Jazz_Perk_*`, `Loot_JAZZ_*`, Portrait/BigPortrait на диске, AIM chat + VR минимум.
- `JAZZ-UNITS-002-REQ-003` — новые loc-строки в том же change set в `Russian.csv` и `English.csv` (needs=0).
- `JAZZ-UNITS-002-REQ-004` — именной перк с combat Mechanics получает Code hook или явно помеченный stub+follow-up AC; Colby Chain Panic — полный hook (+20% AoE, 20% panic).
- `JAZZ-UNITS-002-REQ-005` — sync transaction: companion + items.lua + metadata.lua для затронутых пакетов.
- `JAZZ-UNITS-002-REQ-006` — портреты: no weapons, class kit, no rank chevrons, soft alpha, JA3 color grade, `#FF00FF` soft-cut, proportions, Big без crop головы/стоп; style-refs только `MercPortraits/References/`.
- `JAZZ-UNITS-002-REQ-007` — **3 варианта** портретов на мерка в `MercPortraits/wip-regen/`:
  - `v1_appearance_backstory_bio/` — APPEARANCE + BACKSTORY/LOOK + BIO
  - `v2_appearance_only/` — только APPEARANCE (внешность)
  - `v3_bio_backstory/` — BIO + BACKSTORY/LOOK
  Источник: [`_appearance-sheet.md`](../../design/mercs-ja12/_appearance-sheet.md) / Google Sheet. Огнестрел из sheet не рисовать.
- `JAZZ-UNITS-002-REQ-008` — post-generation face QA: Spider, Highball, Flo, Grace, Rothman, Vilde, Horg и Blade получают face-only кандидаты с JA2 identity ref; текущие pose/kit сохраняются, promotion только после human review.
- `JAZZ-UNITS-002-REQ-009` — `Jazz_Biff` использует vanilla Biff visual contract: appearance preset `Biff`, portrait `UI/NPCsPortraits/Biff`, BigPortrait `UI/NPCs/Biff`.
- `JAZZ-UNITS-002-REQ-010` — JA12 3D recipes исправляются только существующими same-gender asset donors; не ship pure AIM hireable clones, не изобретать mesh IDs, спорные mixes подтверждать runtime screenshot.
- `JAZZ-UNITS-002-REQ-011` — owner-provided JA2 voice bank используется для замены устранимой тишины/случайных combat-proxy в AIM chat; exact source предпочтительнее proxy, неоднозначные identity/text mappings остаются на human ear-check.

## Инварианты и ограничения

- Не перезаписывать Ready merc UnitData/portraits вне явно согласованного correction scope.
- Исключение по решению владельца 2026-08-07: разрешён face-only QA восьми мерков из `REQ-008`; Spouke остаётся hard keep.
- Не пушить без отдельного одобрения.
- Loc IDs волны: `890000000001700`–`890000000002999`.
- Appearance — клон близкого gender/role preset.

## Acceptance criteria

- `JAZZ-UNITS-002-AC-001` — static: все 44 slug в очереди `done`; статьи `status: ready`.
- `JAZZ-UNITS-002-AC-002` — static: UnitData/perk/loot ids существуют в jazz-units/jazz; portraits существуют.
- `JAZZ-UNITS-002-AC-003` — static: loc audit needs Russian=0, needs English=0 для волны.
- `JAZZ-UNITS-002-AC-004` — static: Colby perk hooks присутствуют в Code.
- `JAZZ-UNITS-002-AC-005` — human/runtime: AIM hire + portrait display + perk smoke (owner playtest accepted 2026-07-28 for shipped Colby).
- `JAZZ-UNITS-002-AC-006` — static: в `wip-regen` для каждого slug очереди есть пары 300/2000 во всех трёх вариантах v1/v2/v3.
- `JAZZ-UNITS-002-AC-007` — static: `Jazz_Biff` ссылается на оба vanilla portrait path; `JAZZ_Spouke` не изменён.
- `JAZZ-UNITS-002-AC-008` — human: восемь face-only кандидатов сверены с JA2 face refs и только принятые пары 300/2000 promoted в shipping slots.
- `JAZZ-UNITS-002-AC-009` — static/runtime: 3D link/gender audit PASS; изменённые own-preset recipes подтверждены в живой сессии или явно остаются BLOCKED human.
- `JAZZ-UNITS-002-AC-010` — static/human: AIM chat coverage повторно посчитан по фактическим `.opus`; неоднозначные source mappings перечислены для ear-check, а не выданы за exact.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: новые AIM/MERC hire ids; не ломают существующие Jazz_* Ready.
- Saves: новые unit types; старые сейвы без этих мерков ок.
- Network/determinism: loot weights фиксированы.
- Generated data: да (items/metadata/companions).
- Cross-package: jazz perk ↔ jazz-units UnitData; portraits Mod/Dv3mFVN.
- Rollback: revert wave commits / удалить новых UnitData ids.

## План и ownership

- Пакет-владелец: jazz-units (UnitData/loot/portraits), jazz (perks/loc/combat).
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: items.lua обоих пакетов; loc ID range

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner («Генерируй всех мерков по порядку»; «+ учитывай приоритеты»; «это касается и генерации картинок»)
- Дата: 2026-07-28
- Post-generation correction: project-owner 2026-08-07 — «Лица ... надо переделать», вернуть vanilla-иконку Biff, Spouke не трогать, улучшить 3D в пределах доступных assets, проверить owner-provided JA2 sound bank.

## Evidence

- `JAZZ-UNITS-002-AC-001`: `PASS (static)` — 44/44 queue `done`; articles `status: ready`; snapshot `_generation-status.txt`
- `JAZZ-UNITS-002-AC-002`: `PARTIAL` — UnitData + perk + portraits 300/2000 на всех 44; loot/Appearance/rich VR неполны на Medium/Low
- `JAZZ-UNITS-002-AC-003`: `BLOCKED` — loc audit волны ещё не закрыт (`needs=0`)
- `JAZZ-UNITS-002-AC-004`: `PARTIAL` — Colby Chain Panic hooks в Code; остальные `Jazz_Perk_*` stubs (`unit_reactions = {}`)
- `JAZZ-UNITS-002-AC-005`: `PASS (runtime/human)` — owner playtest accepted 2026-07-28 (Colby); полный hire-smoke волны — на review владельца
- `JAZZ-UNITS-002-AC-007`: `PASS (static)` — `Jazz_Biff.lua` и `items.lua` ссылаются на `UI/NPCsPortraits/Biff` + `UI/NPCs/Biff`; Spouke отсутствует в write set.
- `JAZZ-UNITS-002-AC-008`: `BLOCKED (human)` — восемь пар 300/2000 и contact sheet готовы в `MercPortraits/_wip/ja12-facefix/`; runtime-slot копии в рабочем дереве не считаются accepted/shipped до review владельца.
- `JAZZ-UNITS-002-AC-009`: `PASS (static) / BLOCKED (runtime/human)` — семь clone-prone recipes разделены, Simon переведён с `Shadow` на собственный preset; audit: 45/45 links, 0 gender errors, 0 exact duplicate recipes. Нужны in-game screenshots/seam review.
- `JAZZ-UNITS-002-AC-010`: `PASS (static) / BLOCKED (human ear)` — `ja2mercs (1)` inventory: 63 banks; actual chat audit: 50 mercs, 0 fully silent, 1 missing slot (manual Lynx preserved). Blade/Flo/Miguel/Ricochet/Benny/Simon/Meat/Shank filled from their own source banks; all eight use semantic fallback stems and remain on ear-check.

## Documentation delta

- `docs/design/mercs-ja12/_generation-queue.md` — очередь
- `docs/design/mercs-ja12/README.md` — Ready переносы
- `docs/design/mercs-ja12/_appearance-donor-visual-catalog.md` — текущие anti-clone donor mixes и runtime QA gate
- `docs/technical/systems/units-progression-specializations.md` — current-state JA12 portraits, appearances и voice coverage
- `docs/showcase/ru/mercenaries.md` + `docs/showcase/en/mercenaries.md` — игроковый контракт по classic portraits/voices, vanilla Biff и неизменённому Spouke
