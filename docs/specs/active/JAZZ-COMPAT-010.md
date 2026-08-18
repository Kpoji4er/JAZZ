---
id: JAZZ-COMPAT-010
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
  - jazz/docs/specs/active/JAZZ-COMPAT-010.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/technical/bugs/nomaps-playtest-2026-07-30.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/docs/tools/_verify_nomaps_story_quest_skip.py
  - jazz/docs/tools/_verify_nomaps_globals_predeclare.py
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

# JAZZ-COMPAT-010: NoMaps — не ломать квестовые спавны A2/F5/G6

## Проблема

Профиль **JAZZ Vanilla Maps** (`jazz-nomaps`) ремапит generic vanilla Legion
UnitData в `JAZZ_Legion_*` (COMPAT-004). Playtest Discord (Firestarter, 2026-08-18):

1. **G6 колодец** — вечером радио + Satellite conflict, на тактике пусто.
   Vanilla `ReduceSavannaCampStrength` вешает конфликт `G6_WaterWell` с
   `no_exploration_resolve` на группу маркеров `LegionWaterWell`. Remap через
   `UnitMarker:SpawnObjects` (in-place `UnitDataDefId`) и последующий
   `lRemapEnemyUnitTemplates` пересоздаёт UnitData и сбрасывает квестовую группу.
2. **F5 Côte d'Azur** — капитан Жак Пьеро пропадает, операция спустить лодку /
   открыть порт недоступна. Ваниль при `CheckIsPersistentUnitDead(NPC_CaptainPierrot)`
   снимает `AbandonedBeach_EnablePort` и закрывает порт. Пьеро — civilian с
   `neutral_retaliate` на `ForceConflict`; стартовый отряд
   `LegionDefenders_Balanced_Easy` после class-remap бьёт как JAZZ T1.
3. **A2 Diamond Red** — журнал «0 выживших рабочих» после убийства Graaf.
   `DiamondRedSquad` ремапится в JAZZ-классы; шахтёры (`Miners`) гибнут, доход
   шахты падает до 50% базы.

Именной skip COMPAT-004 (`_Jose` / Hyena) эти пути не покрывает.

## Цели

- Сохранить vanilla UnitData и marker groups у колодца G6 (`LegionWaterWell`).
- Не ремапить class стартового отряда F5 `LegionDefenders_Balanced_Easy` и
  выставить Пьеро `conflict_ignore`, чтобы ForceConflict его не убивал.
- Не ремапить class состава `DiamondRedSquad` (A2), чтобы легион у шахты не
  был JAZZ-летальным относительно шахтёров.
- Оставить generic remap для обычных Legion/Thug спавнов.

## Non-goals

- Воскрешение уже мёртвого Пьеро / уже погибших шахтёров в текущем save.
- Изменение ванильных квестов `DiamondRed`, `SavannaSideQuest`,
  `ReduceSavannaCampStrength`.
- Отказ от class-remap на всех `LegionDefenders_Balanced_Easy` (B3, L8 и др.).
- Изменение `EnemySquadDef` / UnitData в `jazz-units`.
- Профиль с `jazz-maps`.

## Требования

- `JAZZ-COMPAT-010-REQ-001` — при активном NoMaps marker с группой
  `LegionWaterWell` не меняет `UnitDataSpawnDefs.UnitDataDefId` и не ремапит
  class через `CreateUnitData` / `lRemapEnemyUnitTemplates`.
- `JAZZ-COMPAT-010-REQ-002` — `GenerateEnemySquad("DiamondRedSquad")` не
  ремапит squad id и не ремапит class юнитов этого def; batch remap по
  `squad.enemy_squad_def` тоже пропускает.
- `JAZZ-COMPAT-010-REQ-003` — `GenerateEnemySquad` с `sector_id=="F5"` и def
  `LegionDefenders_Balanced_Easy` не ремапит class; прочие сектора с тем же
  def ремапятся как раньше.
- `JAZZ-COMPAT-010-REQ-004` — живой `Captain_Pierrot` / `NPC_CaptainPierrot`
  на тактике получает `conflict_ignore` при спавне маркера и на
  Exploration/Combat start.
- `JAZZ-COMPAT-010-REQ-005` — skip-флаг `_G` predeclare + `rawset`; при
  `FhNNYd` wrappers no-op как сейчас.
- `JAZZ-COMPAT-010-REQ-006` — generic Legion stem-remap (Bastien skip,
  WeakFlagHill, Tutorial, Early T1) не меняется.

## Инварианты и ограничения

- ModDef `7MsJ2Eq`, public UnitData/squad IDs, save schema не меняются.
- `FortressPierre` по-прежнему отсутствует в `SQUAD_REMAP`.
- Gear refresh **не** регеарит keep-vanilla class (A2/F5); class и
  квестовые Groups не пересоздаются.
- Existing save: G6 — следующий заход на карту вечером; F5 — только если
  Пьеро ещё жив; A2 после боя с нулём шахтёров доход уже зафиксирован
  (новая игра для этой шахты).

## Acceptance criteria

- `JAZZ-COMPAT-010-AC-001` — static: в `NoMaps_Autonomy.lua` есть
  `QUEST_MARKER_GROUPS_KEEP_VANILLA.LegionWaterWell`,
  `STORY_SQUAD_KEEP_VANILLA_UNITS.DiamondRedSquad`, skip F5+`LegionDefenders_Balanced_Easy`,
  `g_JAZZ_NoMapsSkipUnitRemap` на top-level, `conflict_ignore` для Pierrot.
- `JAZZ-COMPAT-010-AC-002` — static: `docs/tools/_verify_nomaps_story_quest_skip.py` exit 0;
  `_verify_nomaps_globals_predeclare.py` и named-skip/Pierre verifiers exit 0.
- `JAZZ-COMPAT-010-AC-003` — static: technical + wiki + showcase RU/EN описывают
  исключения A2/F5/G6 / Пьеро.
- `JAZZ-COMPAT-010-AC-004` — runtime/human: G6 на закате — юниты группы
  `LegionWaterWell` на тактике; F5 — Пьеро жив после ForceConflict, операция
  лодки доступна; A2 — после быстрого убийства Graaf живые шахтёры > 0 при
  отсутствии дружественного огня (new game).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: узкие skip в существующих nomaps wrappers;
  ванильные квесты не патчатся. CommonLib эти символы не переопределяет.
- Saves: schema без изменений. Мёртвый Пьеро / нулевой `MinersAlive` не
  ретрофитятся. G6 пустой конфликт текущего визита может потребовать выйти
  и зайти на следующем закате.
- Network/determinism: новых RNG нет, если skip срабатывает до
  `InteractionRand` пула class.
- Generated data: нет.
- Cross-package: runtime только `jazz-nomaps`; docs в `jazz`.
- Rollback/recovery: удалить skip-таблицы и Pierrot `conflict_ignore`.

## План и ownership

- Пакет-владелец: `jazz-nomaps`.
- Docs: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: см. front matter.

## Решение владельца

- Статус: **implemented**.
- Кто подтвердил: project-owner (chat «чини», 2026-08-18, после разбора A2/F5/G6).
- Дата: 2026-08-18.

## Evidence

- `JAZZ-COMPAT-010-AC-001`: `PASS (static)` — `QUEST_MARKER_GROUPS_KEEP_VANILLA.LegionWaterWell`, `STORY_SQUAD_KEEP_VANILLA_UNITS.DiamondRedSquad`, F5+`LegionDefenders_Balanced_Easy` skip, `g_JAZZ_NoMapsSkipUnitRemap` predeclare+rawset, Pierrot `conflict_ignore`.
- `JAZZ-COMPAT-010-AC-002`: `PASS (static)` — `python docs/tools/_verify_nomaps_story_quest_skip.py`; `_verify_nomaps_globals_predeclare.py`; named-skip and FortressPierre verifiers OK.
- `JAZZ-COMPAT-010-AC-003`: `PASS (static)` — strategy-squads-sectors, compatibility, override-matrix, nomaps-playtest B21–B23, wiki `legion-global-ai`, showcase RU/EN `legion-strategy`, tools README.
- `JAZZ-COMPAT-010-AC-004`: `BLOCKED (runtime/human)` — нужна новая кампания / живой Пьеро: G6 закат с `LegionWaterWell` на тактике; F5 ForceConflict Пьеро жив; A2 быстрый Graaf с живыми шахтёрами.
  `test-change-spec.ps1 -Phase Done` остаётся красным из‑за этого BLOCKED (как COMPAT-009); accepted — после human smoke.

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — skip A2/F5/G6.
- `docs/technical/compatibility.md` — COMPAT-010.
- `docs/technical/override-matrix.md` — CreateUnitData / UnitMarker / GenerateEnemySquad skips.
- `docs/technical/bugs/nomaps-playtest-2026-07-30.md` — B21–B23.
- `docs/wiki/legion-global-ai.md` + showcase RU/EN `legion-strategy`.
- `docs/tools/_verify_nomaps_story_quest_skip.py` + README.
