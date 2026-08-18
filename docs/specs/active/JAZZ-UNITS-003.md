---
id: JAZZ-UNITS-003
status: approved
owner: project-owner
systems:
  - units-progression-specializations
  - localization
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/CharacterEffect/Jazz_Perk_*.lua
  - jazz/CharacterEffect/Jazz_OrderCTH.lua
  - jazz/Code/System_OR_Weapons.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/design/mercs-ja12/_named-perks-plan.md
  - jazz/docs/showcase/ru/perks.md
  - jazz/docs/showcase/en/perks.md
exclusive_resources:
  - jazz/items.lua
  - localization ID range 890000000006200-890000000006299
related_decisions:
  - none
related_specs:
  - JAZZ-UNITS-006
approved_by: project-owner chat 2026-07-31 «Подготовь реализацию» + defaults from _named-perks-plan.md §5.1/§10
---

# JAZZ-UNITS-003: Named perks Wave A (EASY + hygiene)

> **Supersede (partial):** Mechanics для Ids §A из Wave A (**Henning, Laura, Lucky, Dynamo, Nervous, Madman, Blade, Shank, Steiger, Vince**; плюс целевой контракт **Mike**) заменены контрактом [`JAZZ-UNITS-006`](JAZZ-UNITS-006.md). Hygiene / Lynx / Vicious / Eskimo / Vilde / orphan / HUD-hide из этой спеки остаются в силе, пока 006 их явно не трогает.

## Проблема

После JAZZ-UNITS-002 у ~43 мерков слот `Jazz_Perk_*` есть, но `unit_reactions = {}` / WIP-текст — фирменного эффекта нет. План уточнения: `docs/design/mercs-ja12/_named-perks-plan.md`. Нужна первая реализуемая волна.

## Цели

- Phase 0 hygiene: орфан `Jazz_Perk_44840`; скрыть ложные HUD-кнопки Lynx/Buzz/Spider/Colby; Lynx CTH-range.
- Wave A v1: Madman, Blade, Nervous, Henning, Vicious, Dynamo, Eskimo, Lucky, Shank, Vilde, Laura, Vince, Steiger.
- Descriptions = фактический эффект (RU+EN).
- HARD/остальной MEDIUM — вне scope.

## Non-goals

- Wave B/C (Grom, Mike, Ira, Biff, Rothman, shop/mine/militia ops, …) — Flo shop остаётся в Wave C / HARD, не в Wave A.
- **Разгрузки:** personal loadout / unit inventory slots / stack UI в разгрузке / bag↔разгрузка — inventory (`JAZZ-INV-*`), не named-perk scope.
- Charge +2 для Blade; Vicious Fox-double / melee-kill AP; Dynamo groin; Cougar noise; Hitman active.
- Push/release.
- jazz-units UnitData (StartingPerks уже ссылаются на perk id).

## Требования

- `JAZZ-UNITS-003-REQ-001` — Wave A perks из таблицы §Mechanics wired; **§A Ids superseded 006** (не требовать v1 Nervous +2 / Inspired Madman и т.д.).
- `JAZZ-UNITS-003-REQ-002` — companion + `items.lua` ModItemCharacterEffectCompositeDef синхронны для затронутых Id.
- `JAZZ-UNITS-003-REQ-003` — RU+EN Descriptions обновлены; `needs Russian=0` / `needs English=0` для затронутых строк.
- `JAZZ-UNITS-003-REQ-004` — CombatAction у Lynx/Buzz/Spider/Colby не показывается как toggle `Jazz_Perk_00` (UIState hidden); `Jazz_Perk_00` остаётся рабочим toggle Фрага.
- `JAZZ-UNITS-003-REQ-005` — `Jazz_Perk_44840` не загружается (файл удалён / не в metadata).
- `JAZZ-UNITS-003-REQ-006` — Lynx: `Jazz_LynxSightBonus` (+8) drives both daytime sight and Range CTH soften (vision → accuracy).

## Mechanics (locked v1)

Канон §A (Henning / Laura / Lucky / Dynamo / **Nervous** / Madman / Blade / Shank / Steiger / Vince / Mike) — [`JAZZ-UNITS-006`](JAZZ-UNITS-006.md). Ниже v1 003 **только** как история; не реализовывать заново.

| Id | Effect (003 v1) | Live |
| --- | --- | --- |
| `Jazz_Perk_Madman` | Kill Dist≤1 → `Inspired` | **006:** melee crit/kill → −10 Will ≤5 |
| `Jazz_Perk_Blade` | Melee +20 CTH; crit 0 | **006:** Brutalize extra hit |
| `Jazz_Perk_Nervous` | Autofire/Burst **+2** (`GetAutofireShots`) | **006:** хит очереди стекает +1 пулю на следующую, **cap +10**; не flat +2 |
| `Jazz_Perk_Henning` | OrderCTH +5 @5 | **006:** +3 AP aura @10 |
| `Jazz_Perk_Lucky` | 1×/combat miss→hit | **006:** CTH≥70% miss → reroll |
| `Jazz_Perk_Dynamo` | Head 25% Blinded | **006:** lockpick skips lock traps |
| `Jazz_Perk_Laura` | Heal → remain Hidden | **006:** +15 CTH & crit after heal |
| `Jazz_Perk_Vince` | First heal → +4 AP | **006:** squad −25% med cost |
| `Jazz_Perk_Steiger` | Night OrderCTH @5 | **006:** night/UG +5 CTH @10 |
| `Jazz_Perk_Shank` | Melee vs him −50 CTH | **006:** 50% melee def + knife counter ≤8 |
| `Jazz_Perk_Vicious` | +1 start AP / female ally (cap 3) | **003 live** (006 не трогает) |
| `Jazz_Perk_Eskimo` | HP&lt;50%: no new Panic; rifle ignores Wounded | **003 live** |
| `Jazz_Perk_Vilde` | Night/UG Burst/Auto +15 CTH | **003 live** |
| `Jazz_Perk_Lynx` | `Jazz_LynxSightBonus` (+8) sight + Range CTH | **003 live** (hygiene) |
| `Jazz_OrderCTH` | +5 CTH next attack | leftover status; Henning/Steiger 006 больше не опираются на v1 @5 |

## Инварианты и ограничения

- Не ломать Colby/Buzz/Spider/Spouke shipped hooks.
- Не добавлять HUD-кнопки пассивам.
- Deterministic RNG: `InteractionRand` / existing attack rolls only.
- Не трогать HARD perks.

## Acceptance criteria

- `JAZZ-UNITS-003-AC-001` — static: Wave A companions имеют non-empty `unit_reactions` (Nervous/Lucky могут опираться на Code).
- `JAZZ-UNITS-003-AC-002` — static: hygiene Lynx Range reaction; **Nervous shot count — 006** (stack cap 10, не flat +2).
- `JAZZ-UNITS-003-AC-003` — static: CombatAction Lynx/Buzz/Spider/Colby → UIState `"hidden"`.
- `JAZZ-UNITS-003-AC-004` — static: no `Jazz_Perk_44840` in metadata/items; file absent or unlisted.
- `JAZZ-UNITS-003-AC-005` — static: loc audit for touched IDs; Descriptions без WIP.
- `JAZZ-UNITS-003-AC-006` — runtime/human: Madman/Shank/hygiene; **Nervous +2 bullets superseded** (006 stack).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: новые reactions на существующих perk ids; новый status `Jazz_OrderCTH`.
- Saves: ok (status RemoveOnEndCombat).
- Network/determinism: InteractionRand keys named; Lucky uses existing shot roll path.
- Generated data: yes.
- Cross-package: UnitData StartingPerks уже содержат ids.
- Rollback: revert commit.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive resources: items.lua; loc 890000000006200–6299 (`Jazz_OrderCTH`)

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner («Подготовь реализацию»); defaults §10 плана: Lynx CTH дописать; **Nervous = +2 bullets — superseded 006 cap 10**; HARD defer; Mike/etc вне Wave A
- Дата: 2026-07-31
- 2026-08-18: Mechanics §A table lock → [JAZZ-UNITS-006](JAZZ-UNITS-006.md); не возвращать flat +2 Nervous.

## Evidence

- `JAZZ-UNITS-003-AC-001`: `PASS (static)` — Wave A companions have reactions (Nervous/Lucky Code-backed)
- `JAZZ-UNITS-003-AC-002`: `PASS (static)` — Lynx Range reaction; Nervous live path is 006 stack (`Jazz_ApplyNamedPerkAutofireShots`, cap 10), not 003 +2
- `JAZZ-UNITS-003-AC-003`: `PASS (static)` — Lynx/Buzz/Spider/Colby CombatAction GetUIState → `"hidden"`
- `JAZZ-UNITS-003-AC-004`: `PASS (static)` — `Jazz_Perk_44840.lua` removed; not in metadata/items
- `JAZZ-UNITS-003-AC-005`: `PASS (static)` — Descriptions updated RU/EN (CSV + companions); WIP cleared for Wave A
- `JAZZ-UNITS-003-AC-006`: `BLOCKED` — runtime/human; Nervous smoke follows 006 (stack cap 10)

## Documentation delta

- `_named-perks-plan.md` — Wave A implementation started under JAZZ-UNITS-003
- `docs/showcase/ru|en/perks.md` — Wave A wired list
- `metadata.lua` version_minor 48
