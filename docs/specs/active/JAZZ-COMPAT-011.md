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
  - jazz/docs/specs/active/JAZZ-COMPAT-011.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
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
  - Global:CreateUnitData
  - Global:GenerateEnemySquad
  - Global:UnitMarker.SpawnObjects
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMPAT-011: NoMaps — I1 Flag Hill и Пьер на H4

## Проблема

Профиль **JAZZ Vanilla Maps** (`jazz-nomaps`). Discord papasa44 (2026-08-20), ваниль + nomaps:

1. **I1 Flag Hill** — на глобалке значок боя, на тактике нет врагов. Ванильный I1:
   `ForceConflict` + `CustomConflictDescr=InitialConflict`, **без** `InitialSquads`.
   Враги только с UnitMarker (`LegionRaider_WeakFlagHill`, Бастьен). Class-remap
   маркеров / `lRemapEnemyUnitTemplates` на CombatStart ломает стартовый бой
   (тот же класс, что G6 без группы).
2. **Пьер пропал.** На ванили босс форта — **H4** `Fort L'Eau Bleu`
   (`FortressPierre` + `FortressDefenders`), не I1. Squad-id remap на
   `LegionJAZZSquadT2` уже выключен; `Pierre` / `PierreGuard` всё ещё попадают
   под Legion gear refresh (`Affiliation=Legion`) и могут потерять кит/спавн.

I1 ≠ форт: Пьер никогда не стоит на Flag Hill.

## Цели

- Не ремапить class и не регеарить маркеры на **I1** (ванильный opening).
- Не ремапить class и не регеарить `FortressPierre`, `Pierre`, `PierreGuard`,
  persist `NPC_Pierre`.
- Оставить generic remap на прочих секторах, включая гарнизон
  `FortressDefenders` → `FortressDefenders_NoMaps` на H4.

## Non-goals

- Воскрешение уже исчезнувшего Пьера в текущем save.
- Профиль с `jazz-maps` (форт там I7; I1 не Flag Hill).
- Отказ от WeakFlagHill→Roughneck **вне** I1 (на ванили этот id только Flag Hill).
- Изменение `jazz-units` UnitData `PierreGuard`.

## Требования

- `JAZZ-COMPAT-011-REQ-001` — при активном NoMaps и `gv_CurrentSectorId=="I1"`
  `UnitMarker:SpawnObjects` не мутирует DefId и спавн идёт с skip-флагом;
  live юниты на этой карте не class-ремапятся и не регеарятся.
- `JAZZ-COMPAT-011-REQ-002` — `FortressPierre` в
  `STORY_SQUAD_KEEP_VANILLA_UNITS`; `Pierre` / `PierreGuard` /
  `PierreGuard_Ordnance` / `NPC_Pierre` keep-vanilla (class + gear).
- `JAZZ-COMPAT-011-REQ-003` — skip I1 не применяется ко всем `gv_UnitData`
  только потому, что игрок сейчас на Flag Hill (satellite Legion вне карты
  ремапится как раньше).
- `JAZZ-COMPAT-011-REQ-004` — COMPAT-010 skip (G6/A2/F5/Pierrot) не ломается.
- `JAZZ-COMPAT-011-REQ-005` — wrappers no-op при `FhNNYd`.

## Инварианты и ограничения

- ModDef `7MsJ2Eq`, public IDs, save schema не меняются.
- `FortressPierre` по-прежнему отсутствует в `SQUAD_REMAP`.
- H4 `FortressDefenders` по-прежнему ремапится в `FortressDefenders_NoMaps`.
- Existing save: пустой I1 — новая кампания или повторный вход после фикса;
  Пьер не ретрофитится, если persist уже мёртв/отсутствует.

## Acceptance criteria

- `JAZZ-COMPAT-011-AC-001` — static: `SECTORS_KEEP_VANILLA_UNITS.I1`,
  `STORY_SQUAD_KEEP_VANILLA_UNITS.FortressPierre`, keep по class `Pierre` /
  `PierreGuard` / persist `NPC_Pierre`.
- `JAZZ-COMPAT-011-AC-002` — static: `_verify_nomaps_story_quest_skip.py` exit 0
  (включая COMPAT-010); `_verify_nomaps_fortress_pierre_squad.py` exit 0.
- `JAZZ-COMPAT-011-AC-003` — static: technical + wiki + showcase RU/EN: I1 Flag
  Hill ванильный opening; Пьер на H4.
- `JAZZ-COMPAT-011-AC-004` — runtime/human: новая кампания nomaps — I1 есть
  враги при ForceConflict; H4 есть Пьер.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: узкие skip в существующих nomaps wrappers.
- Saves: schema без изменений. Пустой I1 / отсутствующий Пьер не чинятся
  ретроактивно.
- Network/determinism: новых RNG нет, если skip до `InteractionRand` пула.
- Generated data: нет (кроме nomaps `metadata.lua` revision при коммите).
- Cross-package: runtime `jazz-nomaps`; docs `jazz`.
- Rollback/recovery: убрать `I1` из sector-keep и `FortressPierre` из story-keep.

## План и ownership

- Пакет-владелец: `jazz-nomaps`.
- Docs: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: см. front matter.

## Решение владельца

- Статус: **implemented**.
- Кто подтвердил: project-owner (chat «чини», 2026-08-20, после разбора I1/H4).
- Дата: 2026-08-20.

## Evidence

- `JAZZ-COMPAT-011-AC-001`: `PASS (static)` — `SECTORS_KEEP_VANILLA_UNITS.I1`, `STORY_SQUAD_KEEP_VANILLA_UNITS.FortressPierre`, `lIsPierreStoryUnit` (`Pierre` / `PierreGuard` / `NPC_Pierre`).
- `JAZZ-COMPAT-011-AC-002`: `PASS (static)` — `python docs/tools/_verify_nomaps_story_quest_skip.py`; `_verify_nomaps_fortress_pierre_squad.py`.
- `JAZZ-COMPAT-011-AC-003`: `PASS (static)` — strategy-squads-sectors, compatibility, override-matrix, nomaps-playtest B24–B25, wiki `legion-global-ai`, showcase RU/EN `legion-strategy`, tools README.
- `JAZZ-COMPAT-011-AC-004`: `BLOCKED (runtime/human)` — New Game nomaps: I1 ForceConflict with enemies on Flag Hill; H4 Pierre present.
  `test-change-spec.ps1 -Phase Done` stays red on this BLOCKED (same as COMPAT-010).

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md`
- `docs/technical/compatibility.md`
- `docs/technical/override-matrix.md`
- `docs/technical/bugs/nomaps-playtest-2026-07-30.md` — B24–B25
- `docs/wiki/legion-global-ai.md` + showcase RU/EN `legion-strategy`
- `docs/tools/_verify_nomaps_story_quest_skip.py` + README
