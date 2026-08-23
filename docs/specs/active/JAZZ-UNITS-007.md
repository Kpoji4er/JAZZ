---
id: JAZZ-UNITS-007
status: approved
owner: project-owner
systems:
  - enemy-squads
  - ernie-garrison
  - legion-global-ai
repositories:
  - jazz
  - jazz-units
  - jazz-maps
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-UNITS-007.md
  - jazz/docs/design/ernie-garrison-baseline.md
  - jazz/docs/technical/systems/maps-quests-content-catalog.md
  - jazz/docs/tools/_rewrite_legion_ernie_village.py
  - jazz/docs/tools/_ernie_init_dump.py
  - jazz/docs/tools/_apply_ernie_overflow_inits.py
  - jazz/docs/tools/README.md
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz-maps/items.lua
  - jazz-maps/metadata.lua
exclusive_resources:
  - jazz-units/items.lua
  - jazz-maps/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-UNITS-007: Ernie Init — срезать перегибы (size × band × preset)

## Проблема

На Эрни Init часто собран из стека Easy/Extra/Shooters → суммы **50–65** на filler-секторах, без size/band/preset. Taxonomy уже в `docs/design/ernie-garrison-baseline.md` (S/M/L/XL × A–E × Forest/Urban/Outpost/Fort/Coast + Extra). I5/J5/villa/CounterAttack/частично I7 **locked**; остальной остров — бардак и перегиб.

## Цели

- Срезать **перегибы** Init (сектора ниже) до целевых size; один базовый пак (+0…1 Extra S), без тройных стеков.
- На Эрни **в основном band A (T1–T2)**; **ключевые** сектора — band **B (T1–T2–T3)** с **немного** T3.
- Пресеты по локации (Coast / Forest / Outpost / Urban / Fort).
- Широкие class pools; офицеры/медики Init по Legion AI density (STRATEGY-005/015); quest packs — исключение.
- Зафиксировать целевую таблицу в этой спеке + baseline; apply скриптом.
- Старые Init-стеки Эрни, ставшие **неиспользуемыми** после ревайра, — в `ModItemFolder` **Deprecated** (jazz-units), не оставлять «мёртвыми» в LegionSquads.

## Non-goals

- Global AI living army / Patrol pools на I7 (сами пулы не чистить в этой спеке; в Deprecated только то, что **нигде** не referenced после Init rewire).
- Map-only M1–M3 / J4 / J6 marker pass (Roughneck→Recruit) — отдельный follow-up.
- Hard-delete Id паков (если save/quest/NoMaps ещё ссылается — Id остаётся, объект в Deprecated).
- Полный apply `FortressDefenders` 48 composition slots (контракт уже locked) — **в scope этой спеки** как I7 Init shape (Pierre + Defenders, drop Ordnance), даже если composition apply идёт тем же change set. **Не сделано:** dump всё ещё `FortressDefenders(12)` + `LegionAttackers_Ordnance_Easy(30)`.
- Переписывать уже locked I5/J5/villa размеры.
- **I5 / J5 officer density** — **исключение**: не подтягивать SGT/LT/CPT под STRATEGY-005 (авторский meat/rifle ok).
- **M1–M3** — **исключение**: 0 Init, map markers only (Roughneck→Recruit pass — отдельный follow-up, не UNITS-007).
- **J4 / J6** — **исключение Init**: нет `InitialSquads`. J4 дорога ~markers; **J6 owner OK** (аванпост контрабандистов, map fight) — не трогать.

## Locked island class policy (owner 2026-08-10)

| Band | Где |
| --- | --- |
| **A** T1–T2 | Большинство Init Эрни (coast, road, forest, thin outpost) |
| **B** T1–T2–T3 (мало T3) | Ключевые ближе к форту: **I7**, **L1**, **I2**, **L6_UG**; **J5** rifle hub |
| C–E | Не для обычного Init Эрни (story/elite точечно: villa L5 Headsman, Pierre suite) |

**Role coverage (owner):** на острове в сумме Init должны встречаться **все T1–T2 роли** Легиона (line/assault/flank/marks/gun/grenade + Recruit meat). Градиент к **I7**: дальше от форта — **T1-lean** пулы; ближе к аванпосту/форту — **T2-lean**. **Редкие T3** (Veteran / Punisher / Skull / Recon / Pathfinder) — только сложные сектора (I2/L1/L6_UG/I7), не размазывать по побережью.

## Целевые Init (перегибы + ключи) — Normal base

**Size × difficulty (owner, InitialSquads):** Small **5/10/15** · Medium **20/25/40** · Large **30/40/70** (Easy/Normal/Hard). **Authored сразу E/N/H** (difficulty-gated slots в пресете; `UnitCountMin`/`Max` = variance внутри сложности, не замена E/H). I5/J5/villa — исключения размера.

| Sector | Was (approx) | Target Normal | Size | Band | Preset | Init shape |
| --- | ---: | ---: | --- | --- | --- | --- |
| **M5** | 53 | **25+Mixed** | Medium+Extra | **A** | Coast | coastal + Mixed |
| **M6** | 54 | **25+Gunners** | Medium+Extra | **A** | Coast/port | port + Gunners |
| **M4** | 30 Outlook | **25+Marksmen** | Medium+Extra | **A** | Outpost | Outlook + Marksmen |
| **I2** | ~36–52 stack | **25+Veterans light** | Medium+Extra | **B** | Outpost | lighthouse + Veterans (~5–7) |
| **I3** | Balanced stack | **25+Flankers** | Medium+Extra | **A** | Road | road/bridge + Flankers |
| **I4** | Entrenched stack | **25+Mixed** | Medium+Extra | **A** | Road | cliff-road + Mixed |
| **L1** | 65 | **40** | Large | **B** | Outpost | rebel-base; no Extra |
| **L2** | 27 / 25+Melee | **25** | Medium | **A** | Forest | forest only (transit; Extra Melee dropped) |
| **L6** | 30 | **25+Flankers** | Medium+Extra | **A** | Forest | bunker approach + Flankers |
| **L6_UG** | 37 | **25+Grenadiers** | Medium+Extra | **A/B** | Fort | bunker + Grenadiers/Gunners |
| **I7** | Pierre+Def12+Ordnance | Pierre+**48** | Fort special | **B** | Fort | Pierre + FortressDefenders(48); drop Ordnance |

Already OK / locked (не трогать размер в этой спеке):

| Sector | N | Note |
| --- | ---: | --- |
| I5 | 60 | XL Urban A — locked |
| J5 | 40 | L Urban A/B — locked |
| K3/K5/L3/L4/L5 | 22–26 | villa Sentry+Attackers — locked |
| ErnieCounterAttack | 30 | quest exception |

## Требования

- `JAZZ-UNITS-007-REQ-001` — таблица целевых Init выше = канон; baseline + catalog синхронизированы.
- `JAZZ-UNITS-007-REQ-002` — каждый перегиб-сектор: Init = 1 base pack (+ optional Extra **5–10** specialized if map feels empty); запрет стека 2×Extra_T2 / 2× полных Easy без тега.
- `JAZZ-UNITS-007-REQ-011` — Extra = spice **5–10**: либо узкая specialty (`Gunners`/`Marksmen`/`Grenadiers`/`Veterans`/`Melee`/`Flankers`), либо **`LegionExtra_Ernie_Mixed`**. Specialty остаётся тематическим пулом, но **каждый боец — отдельный weighted roll** (`EnemySquadUnit` Count 1, optional слоты 0–1). Не один слот `UnitCount` 6–8: ванильный `GenerateRandEnemySquadUnits` берёт тип один раз и клонирует группу. Mixed — пул специальностей, тот же per-unit контракт. Расклад по секторам — baseline Extra column; max 1 Extra на Init.
- `JAZZ-UNITS-007-REQ-012` — на Эрни Init не использовать толстый `LegionExtraSquadFireArms`(15) / `_T2`(18); заменить на Ernie Extra 5–10.
- `JAZZ-UNITS-007-REQ-003` — новые/переписанные паки: band A или B per table; B = немного T3 в пулах, не T3 majority; **no T4** в ordinary Init (story anchors separately).
- `JAZZ-UNITS-007-REQ-004` — preset pools: Coast/Forest/Outpost/Fort отличаются ролями (не копипаст Urban meat на L2).
- `JAZZ-UNITS-007-REQ-005` — wide weighted class pools; officer/medic anchors по STRATEGY-005/015 на Init (quest exception).
- `JAZZ-UNITS-007-REQ-006` — I7 Init shape: Pierre + FortressDefenders(48); Ordnance removed from InitialSquads.
- `JAZZ-UNITS-007-REQ-007` — `items.lua` validate OK; dump script показывает target sums.
- `JAZZ-UNITS-007-REQ-008` — technical catalog + baseline updated; player wiki only if garrison sizes become player-facing beyond existing Ernie pages (prefer technical+baseline).
- `JAZZ-UNITS-007-REQ-009` — body Easy/Hard **authored now**: Small 5/10/15 · Medium 20/25/40 · Large 30/40/70 via difficulty-gated EnemySquad slots (not flat ±10; not deferred).
- `JAZZ-UNITS-007-REQ-010` — within one difficulty: meat/line slots `UnitCountMin`/`Max` **±10…20%** around that difficulty’s role target; anchors Min=Max; Normal mean ≈ size Normal.
- `JAZZ-UNITS-007-REQ-013` — после rewire Init: audit refs (`InitialSquads`, Patrol/Strong/Extra sector fields, quests, NoMaps `SQUAD_REMAP`, code strings). Паки, заменённые Ernie base/Extra и **без оставшихся refs**, перенести в `ModItemFolder` **Deprecated** (как `LegionFortressDefenders` retire). Не трогать locked I5/J5/villa/CounterAttack/Pierre/active Extra. Кандидаты типичные: `LegionAttackers_*_Easy` / `LegionDefenders_*_Easy` стеки с overflow-секторов, толстый `LegionExtraSquadFireArms`(+`_T2`) если снят с Init и нигде не нужен.

## Инварианты и ограничения

- Не ломать QUESTS-003 villa siege IDs / ErnieCounterAttack quest id.
- Не включать maps+nomaps как обязательную пару.
- Living pressure = Global AI, не раздувать Init.
- Deprecated = folder move + comment «retired»; Id сохраняем если есть хоть один внешний ref.

## Acceptance criteria

- `JAZZ-UNITS-007-AC-001` — static: overflow Init Normal sums = targets in table (±1); Easy/Hard gated slot sums match E/H columns (±1) for Medium/Large base packs.
- `JAZZ-UNITS-007-AC-002` — static: I7 InitialSquads only FortressPierre + FortressDefenders; FortressDefenders UnitCountMin sum = 48.
- `JAZZ-UNITS-007-AC-003` — static: no ExtraFireArms_T2 double-stack on M6; no Assault35+Extra on M5.
- `JAZZ-UNITS-007-AC-004` — static: band A packs have no T4 in weightedList; band B packs T3 share is minority of slots.
- `JAZZ-UNITS-007-AC-005` — `_validate_items_quick.py` OK jazz-units + jazz-maps.
- `JAZZ-UNITS-007-AC-006` — runtime/human: smoke enter M5/L1/I7 new game — BLOCKED until playtest.
- `JAZZ-UNITS-007-AC-007` — static: каждый пак из retire-list лежит под `Deprecated`; zero refs вне Deprecated на retired Ids (или Id оставлен с явным «still referenced» note в comment).
- `JAZZ-UNITS-007-AC-008` — static: каждый `LegionExtra_Ernie_*` — только слоты `UnitCountMin`∈{0,1} и `UnitCountMax`=1 (нет клона группы).

## Impact и совместимость

- **Vanilla/CommonLib/JAZZ:** Ernie sector InitialSquads + EnemySquads only.
- **Runtime / saves:** `[new game]` for Ernie Init (authored squads).
- **Network/determinism:** n/a beyond InteractionRand in pools.
- **Generated data:** jazz-units EnemySquads + jazz-maps sector InitialSquads.
- **Cross-package:** jazz-maps references new/rewritten squad IDs in jazz-units.
- **Rollback:** revert items + packs.

## План и ownership

- Пакет-владелец: jazz-units (packs), jazz-maps (InitialSquads), jazz (spec/docs/tools).
- Apply: `_apply_ernie_overflow_inits.py` (+ reuse rewrite helpers).
- Evidence dump: `_ernie_init_dump.py`.
- Declared write set: see frontmatter.
- Exclusive resources: jazz-units/items.lua, jazz-maps/items.lua.

## Решение владельца

2026-08-10: срезать перегибы; Эрни в основном T1–T2; ключи I7/L1/I2 — B; I5/J5/villa locked.  
**Size×difficulty (InitialSquads):** Small 5/10/15 · Medium 20/**25**/40 · Large 30/**40**/70 — **author E/N/H now** (gated slots).  
**Extra lock:** I3=`Flankers`; I2=`Veterans` light (~5–7); I7 FortressDefenders **applied** (48 + drop Ordnance).  
**Deprecated:** audit done — overflow stacks still referenced elsewhere → no folder move this wave.  
**Extra per-unit (owner 2026-08-21):** усиления рандомят **каждого** бойца, не группу одного типа (ванильный clone `UnitCount`). Status **approved**.  
**L2 Extra drop (owner 2026-08-23):** проходной сектор, карта тесная — снять `LegionExtra_Ernie_Melee`; Init = только `LegionErnie_Medium_Forest_A` (~25). Пак Extra Melee не удалять.

## Evidence

- `JAZZ-UNITS-007-AC-001`: static PASS — `_ernie_init_dump.py` design-Normal: Medium bases 25 (±1), L1 40, Extras 5–9, sector sums ~31 with Extra; **L2 Extra dropped** → Forest_A only (~25).
- `JAZZ-UNITS-007-AC-002`: static PASS — I7 Init = FortressPierre + FortressDefenders; Defenders design-Normal sum 48; Ordnance removed.
- `JAZZ-UNITS-007-AC-003`: static PASS — M5/M6 no ExtraFireArms_T2 / Assault35 stacks.
- `JAZZ-UNITS-007-AC-004`: static PASS — band A packs no T4; B packs minority T3 spice.
- `JAZZ-UNITS-007-AC-005`: static PASS — `_validate_items_quick.py` OK jazz-units + jazz-maps.
- `JAZZ-UNITS-007-AC-006`: `BLOCKED` — runtime playtest.
- `JAZZ-UNITS-007-AC-007`: static PASS (audit) — overflow candidates still referenced outside Init (Patrol/AI/other sectors); none hard-orphaned → no Deprecated move this wave. Missing vanilla-only Balanced/Entrenched Ids not in jazz-units.
- `JAZZ-UNITS-007-AC-008`: static PASS after `--extras-only` apply — Extra packs have no `UnitCount>1` clone slots.

## Documentation delta

- `docs/design/ernie-garrison-baseline.md` — Extra lock + E/N/H + Extra per-unit rolls; L2 Extra Melee dropped.
- `docs/technical/systems/maps-quests-content-catalog.md` — Init lines + Extra per-unit; L2 Forest_A only.
- `docs/tools/README.md` — apply `--extras-only`.
- Spec this file.
