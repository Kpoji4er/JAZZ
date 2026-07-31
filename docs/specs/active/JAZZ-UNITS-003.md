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
approved_by: project-owner chat 2026-07-31 «Подготовь реализацию» + defaults from _named-perks-plan.md §5.1/§10
---

# JAZZ-UNITS-003: Named perks Wave A (EASY + hygiene)

## Проблема

После JAZZ-UNITS-002 у ~43 мерков слот `Jazz_Perk_*` есть, но `unit_reactions = {}` / WIP-текст — фирменного эффекта нет. План уточнения: `docs/design/mercs-ja12/_named-perks-plan.md`. Нужна первая реализуемая волна.

## Цели

- Phase 0 hygiene: орфан `Jazz_Perk_44840`; скрыть ложные HUD-кнопки Lynx/Buzz/Spider/Colby; Lynx CTH-range.
- Wave A v1: Madman, Blade, Nervous, Henning, Vicious, Dynamo, Eskimo, Lucky, Shank, Vilde, Laura, Vince, Steiger.
- Descriptions = фактический эффект (RU+EN).
- HARD/остальной MEDIUM — вне scope.

## Non-goals

- Wave B/C (Grom, Mike, Ira, Biff, Rothman, mine/militia ops, …).
- **Магазин:** shop buy/sell цены, BobbyRay/`ShopStackSize`, перк Фло «Барахольщица» — **CUT**, не реализовывать в perk-waves.
- **Разгрузки:** personal loadout / unit inventory slots / stack UI в разгрузке / bag↔разгрузка — inventory (`JAZZ-INV-*`), не named-perk scope.
- Charge +2 для Blade; Vicious Fox-double / melee-kill AP; Dynamo groin; Cougar noise; Hitman active.
- Push/release.
- jazz-units UnitData (StartingPerks уже ссылаются на perk id).

## Требования

- `JAZZ-UNITS-003-REQ-001` — Wave A perks из таблицы §Mechanics ниже wired через `unit_reactions` и/или точечный `Code/` hook.
- `JAZZ-UNITS-003-REQ-002` — companion + `items.lua` ModItemCharacterEffectCompositeDef синхронны для затронутых Id.
- `JAZZ-UNITS-003-REQ-003` — RU+EN Descriptions обновлены; `needs Russian=0` / `needs English=0` для затронутых строк.
- `JAZZ-UNITS-003-REQ-004` — CombatAction у Lynx/Buzz/Spider/Colby не показывается как toggle `Jazz_Perk_00` (UIState hidden); `Jazz_Perk_00` остаётся рабочим toggle Фрага.
- `JAZZ-UNITS-003-REQ-005` — `Jazz_Perk_44840` не загружается (файл удалён / не в metadata).
- `JAZZ-UNITS-003-REQ-006` — Lynx: `Jazz_LynxSightBonus` (+8) drives both daytime sight and Range CTH soften (vision → accuracy).

## Mechanics (locked v1)

| Id | Effect |
| --- | --- |
| `Jazz_Perk_Madman` | Kill at Dist≤1 slab → `Inspired` |
| `Jazz_Perk_Blade` | Melee Attack: +20 CTH; crit chance forced 0 |
| `Jazz_Perk_Nervous` | Autofire/Burst shot count +2 (`GetAutofireShots`) |
| `Jazz_Perk_Henning` | OnBeginTurn: allies ≤5 slabs get `Jazz_OrderCTH` (+5 CTH, until end of their next attack / end turn) |
| `Jazz_Perk_Vicious` | OnCombatStarted: +1 start-turn AP per female ally in squad (cap 3) |
| `Jazz_Perk_Dynamo` | On head hit: 25% `Blinded` 1 turn |
| `Jazz_Perk_Eskimo` | While HP&lt;50%: immune to new `Panicked`; rifle CTH ignores `Wounded` mod id if present |
| `Jazz_Perk_Lucky` | 1×/combat: first firearm shot that would miss becomes a hit |
| `Jazz_Perk_Shank` | Melee attacks targeting Shank: −50 CTH |
| `Jazz_Perk_Vilde` | Night/Underground: Burst/Auto +15 CTH |
| `Jazz_Perk_Laura` | If Hidden when healing ally, remain/reapply Hidden after heal |
| `Jazz_Perk_Vince` | 1×/combat: first heal/bandage on ally → target `GainAP(4 * const.Scale.AP)` |
| `Jazz_Perk_Steiger` | Night/Underground OnBeginTurn: allies ≤5 slabs get `Jazz_OrderCTH` |
| `Jazz_Perk_Lynx` | `Jazz_LynxSightBonus` (+8) sight + same value on Range CTH (vision is the accuracy buff) |
| `Jazz_OrderCTH` | Status: +5 CTH on next attack; RemoveOnEndCombat; Shown |

## Инварианты и ограничения

- Не ломать Colby/Buzz/Spider/Spouke shipped hooks.
- Не добавлять HUD-кнопки пассивам.
- Deterministic RNG: `InteractionRand` / existing attack rolls only.
- Не трогать HARD perks.

## Acceptance criteria

- `JAZZ-UNITS-003-AC-001` — static: Wave A companions имеют non-empty `unit_reactions` (Nervous/Lucky могут опираться на Code).
- `JAZZ-UNITS-003-AC-002` — static: `GetAutofireShots` учитывает Nervous; Lucky miss-save в firearm shot loop; Lynx Range modifier reaction.
- `JAZZ-UNITS-003-AC-003` — static: CombatAction Lynx/Buzz/Spider/Colby → UIState `"hidden"`.
- `JAZZ-UNITS-003-AC-004` — static: no `Jazz_Perk_44840` in metadata/items; file absent or unlisted.
- `JAZZ-UNITS-003-AC-005` — static: loc audit for touched IDs; Descriptions без WIP.
- `JAZZ-UNITS-003-AC-006` — runtime/human: smoke hire+combat for Madman Inspired, Nervous +2 bullets, Shank melee penalty (owner).

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
- Кто подтвердил: project-owner («Подготовь реализацию»); defaults §10 плана: Lynx CTH дописать; Nervous = +2 bullets; HARD defer; Mike/etc вне Wave A
- Дата: 2026-07-31

## Evidence

- `JAZZ-UNITS-003-AC-001`: `PASS (static)` — Wave A companions have reactions (Nervous/Lucky Code-backed)
- `JAZZ-UNITS-003-AC-002`: `PASS (static)` — `Jazz_ApplyNamedPerkAutofireShots` + Lucky miss-save + Lynx Range reaction
- `JAZZ-UNITS-003-AC-003`: `PASS (static)` — Lynx/Buzz/Spider/Colby CombatAction GetUIState → `"hidden"`
- `JAZZ-UNITS-003-AC-004`: `PASS (static)` — `Jazz_Perk_44840.lua` removed; not in metadata/items
- `JAZZ-UNITS-003-AC-005`: `PASS (static)` — Descriptions updated RU/EN (CSV + companions); WIP cleared for Wave A
- `JAZZ-UNITS-003-AC-006`: `BLOCKED` — runtime/human smoke pending owner

## Documentation delta

- `_named-perks-plan.md` — Wave A implementation started under JAZZ-UNITS-003
- `docs/showcase/ru|en/perks.md` — Wave A wired list
- `metadata.lua` version_minor 48
