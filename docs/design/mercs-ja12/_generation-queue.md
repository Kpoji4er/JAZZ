# Очередь генерации наёмников JA12

Канон: [generation-plan.md](../../.agents/skills/create-jazz-merc/references/generation-plan.md)  
Spec волны: [JAZZ-UNITS-002](../specs/active/JAZZ-UNITS-002.md)  
Порядок: **priority High → Medium → Low**, внутри — как в README.  
Готовые вне волны: lynx, tosca, spider, spouke.

Статусы: `pending` | `design` | `codegen` | `portraits` | `loc` | `done` | `blocked`

Снимок слотов: [`_generation-status.txt`](_generation-status.txt) — **44/44** `exec/ud/perk/portrait/big = True`.

| # | Priority | Slug | unit_id | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | high | colby | Jazz_Colby | done | Full: perk hooks AoE+panic, loot, appearance, VR, loc, portraits |
| 2 | high | blade | Jazz_Blade | done | UnitData/perk/loot/portraits/loc |
| 3 | high | ira | Jazz_Ira | done | UnitData/perk/loot/portraits/loc |
| 4 | high | dimitri | Jazz_Dimitri | done | UnitData/perk/loot/portraits/loc |
| 5 | high | madman | Jazz_Madman | done | UnitData/perk/loot/portraits/loc |
| 6 | high | conrad | Jazz_Conrad | done | UnitData/perk/loot/portraits/loc |
| 7 | high | mike | Jazz_Mike | done | UnitData/perk/loot/portraits/loc |
| 8 | high | grom | Jazz_Grom | done | UnitData/perk/loot/portraits/loc |
| 9–24 | medium | rothman→henning | Jazz_* | done | UnitData/perk/portraits; perk stub; AIM chat stub |
| 25–44 | low | static→eskimo | Jazz_* | done | UnitData/perk/portraits; perk stub; AIM chat stub |

## Definition of Done (каждый slug)

- [x] Статья `executable: true`, gaps закрыты
- [x] `Jazz_Perk_*` companion + UnitData companion + portraits 300/2000
- [ ] Полный editor layer: ModItemUnitDataCompositeDef / AppearancePreset / rich VR в `items.lua` (частично — High богаче)
- [ ] Именной перк с combat hooks (только Colby полностью; остальные stubs)
- [ ] Loot tiers для всех (High/частично Medium; Low часто minimal)
- [ ] Rich AIM chat / VoiceResponse из статьи
- [ ] Loc audit `needs Russian=0` / `needs English=0`
- [ ] Sync audit `check-generated-sync.ps1`
- [ ] Runtime smoke: hire + portrait + Colby perk

## Известные gaps (post-wave)

1. Medium/Low perks — `unit_reactions = {}` stubs.
2. AppearancePreset: Colby/High богаче; Medium/Low часто без полного preset / без ModItem в `items.lua`.
3. AIM Offline/Greeting часто EN stubs, не полные фразы из статей.
4. Возможны дубли loot/loc ID после параллельных агентов — нужен loc + sync audit.
5. `metadata.lua` `code[]` + **ModItem UnitData** для всех 44 волны (Medium/Low wired 2026-07-29); Appearance клоны male/female; loot Knife stub где не было тиров.
6. Colby trap AoE bump не wired (`System_OR_Traps` без radius hook) — только grenade radius + panic.
7. Не регенерировать успешные портреты без запроса.
