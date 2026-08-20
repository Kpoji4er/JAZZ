---
id: JAZZ-COMPAT-011
status: implemented
owner: project-owner
systems:
  - strategy-squads-sectors
  - package-compatibility
  - maps-quests-dialogue
repositories:
  - jazz-nomaps
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz-nomaps/Code/NoMaps_Autonomy.lua
  - jazz-nomaps/metadata.lua
  - jazz/Code/System_RIS_Combat.lua
  - jazz/docs/specs/active/JAZZ-COMPAT-011.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/ris-intelligence.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/technical/bugs/nomaps-playtest-2026-07-30.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/docs/tools/_verify_nomaps_story_quest_skip.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - Code:NoMaps_Autonomy.lua
  - Code:System_RIS_Combat.lua
  - Global:CreateUnitData
  - Global:GenerateEnemySquad
  - Global:UnitMarker.SpawnObjects
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMPAT-011: NoMaps — Пьер на H4; пустой I1 чинится wrap-ом, не skip

## Проблема

Профиль **JAZZ Vanilla Maps** (`jazz-nomaps`). Discord papasa44 (2026-08-20), ваниль + nomaps:

1. **I1 Flag Hill** — на глобалке значок боя, на тактике нет врагов. Ванильный I1:
   `ForceConflict` + `CustomConflictDescr=InitialConflict`, **без** `InitialSquads`.
   Враги только с UnitMarker. Первый диагноз (class-remap как G6) был неверен.
   Assert: `Call stack too big` / `C stack overflow` между
   `NoMaps_Autonomy.lua` `UnitMarker:SpawnObjects` и
   `System_RIS_Combat.lua` `lWrappedMarkerSpawn`. RIS при повторном
   `lInstallUnitMarkerWrap` перезаписывал base на обёртку nomaps, а nomaps
   уже хранил RIS wrap как base.
2. **Пьер пропал.** На ванили босс форта — **H4** `Fort L'Eau Bleu`
   (`FortressPierre` + `FortressDefenders`), не I1. Squad-id remap на
   `LegionJAZZSquadT2` уже выключен; `Pierre` / `PierreGuard` всё ещё попадают
   под Legion gear refresh (`Affiliation=Legion`) и могут потерять кит/спавн.

I1 ≠ форт: Пьер никогда не стоит на Flag Hill.

Owner 2026-08-20: откатить I1 sector-keep; чинить рекурсию wrap.

## Цели

- `UnitMarker:SpawnObjects`: RIS wrap install-once; не перезаписывать base
  чужой обёрткой (NoMaps).
- Не ремапить class и не регеарить `FortressPierre`, `Pierre`, `PierreGuard`,
  persist `NPC_Pierre`.
- I1 снова идёт через обычный marker remap (`WeakFlagHill`→T1 Roughneck).
- Оставить generic remap на прочих секторах, включая гарнизон
  `FortressDefenders` → `FortressDefenders_NoMaps` на H4.

## Non-goals

- Воскрешение уже исчезнувшего Пьера в текущем save.
- Профиль с `jazz-maps` (форт там I7; I1 не Flag Hill).
- Whole-sector keep-vanilla на I1 (superseded).
- Изменение `jazz-units` UnitData `PierreGuard`.

## Требования

- `JAZZ-COMPAT-011-REQ-001` — **superseded**. Whole-sector I1 skip снят
  owner 2026-08-20. Пустой I1 — wrap cycle, не class-remap.
- `JAZZ-COMPAT-011-REQ-002` — `FortressPierre` в
  `STORY_SQUAD_KEEP_VANILLA_UNITS`; `Pierre` / `PierreGuard` /
  `PierreGuard_Ordnance` / `NPC_Pierre` keep-vanilla (class + gear).
- `JAZZ-COMPAT-011-REQ-003` — **superseded** вместе с REQ-001 (ограничение
  I1 skip на live-only больше не нужно).
- `JAZZ-COMPAT-011-REQ-004` — COMPAT-010 skip (G6/A2/F5/Pierrot) не ломается.
- `JAZZ-COMPAT-011-REQ-005` — NoMaps wrappers no-op при `FhNNYd`.
- `JAZZ-COMPAT-011-REQ-006` — RIS `lInstallUnitMarkerWrap` не перезаписывает
  `g_JAZZ_RIS_UnitMarkerSpawnBase` / `Orig`, если `SpawnObjects` уже чужая
  обёртка; повторный вход в wrap зовёт orig, не next-wrap.

## Инварианты и ограничения

- ModDef `7MsJ2Eq`, public IDs, save schema не меняются.
- `FortressPierre` по-прежнему отсутствует в `SQUAD_REMAP`.
- H4 `FortressDefenders` по-прежнему ремапится в `FortressDefenders_NoMaps`.
- Нет `SECTORS_KEEP_VANILLA_UNITS` / `lSectorKeepsVanillaUnits`.
- Existing save: пустой I1 — ReloadLua / повторный вход / новая кампания после
  wrap-fix; Пьер не ретрофитится, если persist уже мёртв/отсутствует.

## Acceptance criteria

- `JAZZ-COMPAT-011-AC-001` — static: нет `SECTORS_KEEP_VANILLA_UNITS.I1`;
  `STORY_SQUAD_KEEP_VANILLA_UNITS.FortressPierre`; keep по class `Pierre` /
  `PierreGuard` / persist `NPC_Pierre`; RIS wrap stores `Orig` and returns
  early when another wrap owns the slot.
- `JAZZ-COMPAT-011-AC-002` — static: `_verify_nomaps_story_quest_skip.py` exit 0
  (включая COMPAT-010 + «I1 not keep»); `_verify_nomaps_fortress_pierre_squad.py` exit 0.
- `JAZZ-COMPAT-011-AC-003` — static: technical + wiki + showcase RU/EN: I1 не
  обещает ванильный opening-skip; Пьер на H4; B24 = wrap cycle.
- `JAZZ-COMPAT-011-AC-004` — runtime/human: новая кампания nomaps — I1 есть
  враги при ForceConflict без C stack overflow; H4 есть Пьер.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: RIS wrap + узкие Pierre skip в nomaps wrappers.
- Saves: schema без изменений. Пустой I1 / отсутствующий Пьер не чинятся
  ретроактивно без повторного спавна маркеров.
- Network/determinism: новых RNG нет.
- Generated data: нет (кроме nomaps/jazz `metadata.lua` revision при коммите).
- Cross-package: runtime `jazz` + `jazz-nomaps`; docs `jazz`.
- Rollback/recovery: вернуть I1 sector-keep нельзя без возврата overflow;
  rollback Pierre — убрать `FortressPierre` из story-keep.

## План и ownership

- Пакет-владелец wrap: `jazz`. Pierre keep: `jazz-nomaps`.
- Docs: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: см. front matter.

## Решение владельца

- Статус: **implemented**.
- Кто подтвердил: project-owner (chat «чини и откати изменения на i1», 2026-08-20).
- Дата: 2026-08-20.

## Evidence

- `JAZZ-COMPAT-011-AC-001`: `PASS (static)` — I1 sector-keep removed; `FortressPierre` + `lIsPierreStoryUnit`; RIS `g_JAZZ_RIS_UnitMarkerSpawnOrig` + no re-base when another wrap owns the slot.
- `JAZZ-COMPAT-011-AC-002`: `PASS (static)` — `python docs/tools/_verify_nomaps_story_quest_skip.py`; `_verify_nomaps_fortress_pierre_squad.py`.
- `JAZZ-COMPAT-011-AC-003`: `PASS (static)` — strategy-squads-sectors, ris-intelligence, compatibility, override-matrix, nomaps-playtest B24–B25, wiki `legion-global-ai`, showcase RU/EN `legion-strategy`.
- `JAZZ-COMPAT-011-AC-004`: `BLOCKED (runtime/human)` — New Game / ReloadLua nomaps: I1 ForceConflict with enemies on Flag Hill, no wrap overflow; H4 Pierre present.

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md`
- `docs/technical/systems/ris-intelligence.md`
- `docs/technical/systems/file-coverage.md`
- `docs/technical/compatibility.md`
- `docs/technical/override-matrix.md`
- `docs/technical/bugs/nomaps-playtest-2026-07-30.md` — B24 wrap cycle; B25 Pierre
- `docs/wiki/legion-global-ai.md` + showcase RU/EN `legion-strategy`
- `docs/tools/_verify_nomaps_story_quest_skip.py` + README
