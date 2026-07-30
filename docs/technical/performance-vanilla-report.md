# Отчёт: узкие места производительности (vanilla / CommonLib / JAZZ)

Срез аудита: **30 июля 2026**. Источники: установленный/upstream `JaggedAlliance3Modding` Lua, CommonLib `main` (1.11 / build 1059), runtime-код `jazz/Code`.

Цель: зафиксировать hot path’ы, что уже починено в JAZZ, и **непофикшенные** проблемы ванили (и частично CLib), которые мод не должен или не может безопасно закрыть без риска desync/геймплея.

## Краткий вердикт

| Зона | Главный симптом | Владелец фикса |
|---|---|---|
| AI turn (Dest LOS + LoF + CTH) | Долгий ход врага | Vanilla engine + JAZZ overrides (частично) |
| Visibility O(n²) | Просадки FPS / stalls на больших картах | **Vanilla** (sync-hard) |
| Suspicion ally×enemy | Stealth exploration hitch | Vanilla + CLib early-outs; JAZZ владеет телом |
| Satellite Dijkstra | Лаг при наведении маршрута | **Vanilla** (UI preview можно кэшировать в моде) |
| Interactable highlight | Лаг при удержании highlight | **Vanilla UI** (безопасно патчить модом) |
| Approach banters 500 ms | Exploration CPU | **Vanilla** |

`#MapGet(...)` anti-pattern в текущем vanilla Lua **не найден** (уже подчищен).

---

## Что починено в JAZZ (этот change set)

Поведенчески эквивалентные микро-оптимизации в `jazz` (без смены публичного combat-контракта):

1. **`GetCTHByAimLevels` cache** (`CombatAI.lua`) — сетка CTH по `(enemy, action, max_aim)` внутри одного `AICreateContext` / Dump / dest score. Убирает повторные полные `CalcChanceToHit` на одном и том же враге.
2. **Ранний `unit.ai_context`** — кэш доступен уже во время первого прохода врагов в `AICreateContext`.
3. **`AIUpdateDestLosCache` compact** — один проход вместо серии `table.remove` (O(n²) → O(n)).
4. **Sight armor integer path** — `GetDegradationMultiplierPermille` вместо float `GetDegradationMultiplier` в `GetSightRadius`.
5. **Suppression idle Sleep(200)** — поток очереди WP не крутится каждые 10 ms на пустой очереди.
6. **`UpdateSuspicion` hoist** — `max_sight_radius` / локали `HasVisibilityTo` / `IsCloser` один раз на тик (паттерн CLib).

Уже существовавшие (не регрессировать): один observer-pass брони в sight, smoke early-out, suppression enemy list once/attack, `damage_score_precalced`, flank/surrounded caches, AI dest LOS batch+yield, crosshair `cached_results`, auto fast-forward unseen AI.

---

## Непофикшенные проблемы ванили (приоритет)

### P0 — Combat AI turn time

#### V-AI-001 — `AIUpdateDestLosCache`: dest × enemy `CheckLOS` + `Sleep(10)`
- **Где:** `Lua/Tactical/CombatAI.lua` (~862–970)
- **Частота:** каждый aware AI unit на старте хода
- **Почему болит:** сотни dest × враги, батчи по 100, yield каждые 10 ms
- **JAZZ:** override есть; компакция dests ускорена; сам объём `CheckLOS` остаётся ванильным контрактом
- **Фикс ванили/engine:** spatial shortlist (в радиусе оружия/sight); bitset visible-dest; меньше yield при spare budget

#### V-AI-002 — `AIPrecalcDamageScore`: `GetLoFData` на все destinations × targets
- **Где:** `CombatAI.lua` (~1418–1705), callers в `AIBehaviors.lua`
- **Частота:** каждый AI think + повторно при retarget
- **JAZZ:** override (`AiActions.lua`); CTH cache снижает вторичную стоимость `PickBestAttack`, но LoF matrix остаётся
- **Фикс ванили:** shortlist reachable dests; reuse LoF по `(step_pos, stance)`; не пересчитывать полный matrix после move

#### V-AI-003 — Двойной `CombatPath:RebuildPaths` + OptLoc по `all_destinations`
- **Где:** `AIBuildArchetypePaths` / `AIFindOptimalLocation` (~1009–1315)
- **Частота:** каждый AI unit think
- **JAZZ:** частично (MoveStance==PrefStance); OptLoc radius — sync/AI-behavior sensitive
- **Фикс ванили:** один PF run; score только AP-reachable voxels

#### V-AI-004 — `AIScoreDest`: fire/gas `GetVisualVoxels` на каждый dest
- **Где:** `CombatAI.lua` (~1135–1170)
- **Частота:** сотни dest × policies
- **Фикс ванили:** occupancy grid раз на AI phase; skip если на карте нет fire/gas

#### V-AI-005 — Emplacement: `MapGet("map", "MachineGunEmplacement")`
- **Где:** `CombatAI.lua` (~2501–2558)
- **Частота:** team AI assignment
- **Фикс ванили:** кэш списка на load / spatial query

### P0 — Visibility / LOS (FPS + stalls)

#### V-VIS-001 — `UpdateUnitsLOS` строит O(n²) пары для `CheckLOS`
- **Где:** `Lua/Tactical/Visibility.lua` (~521–565), `ComputeUnitsVisibility`
- **Частота:** combat invalidation; exploration dirty + 500 ms tick (комментарий ванили: *«Visibility in exploration can be a big performance hit»*)
- **JAZZ patch?** **Очень рискованно** — `NetUpdateHash`, stealth/combat start
- **Фикс ванили/engine:** spatial buckets; incremental dirty units; reuse edges если никто не двигался

#### V-VIS-002 — `IsOnFadedSlab` → `MapGetFirst` на юнит в ApplyVisibility
- **Где:** `Visibility.lua` (~842–862)
- **Частота:** каждый ApplyUnitVisibility
- **JAZZ:** только visual path, осторожно
- **Фикс ванили:** grid faded floors, не MapGet per unit

#### V-VIS-003 — Suspicion: allies × enemies каждые 100 ms
- **Где:** `UnitAwareness.lua` (~1211–1340); JAZZ/CLib переопределяют
- **Частота:** stealth exploration
- **JAZZ:** early-outs (`IsCloser`, skip `GetSightRadius`) уже на месте; sight всё ещё тяжелее ванили по броне/camo
- **Фикс ванили:** spatial query; только nearby enemies

### P1 — Satellite

#### V-SAT-001 — `GenerateRouteDijkstra` без кэша + O(n²) extract через `sorted_pairs`
- **Где:** `Satellite/SatelliteSquad.lua` (~2566–2747); UI hover в `XSatelliteMap.lua`
- **Частота:** rollover сектора при выборе маршрута; travel/join/retreat
- **Замечание:** `GenerateRouteDijkstraSimplified` (`DiamondBriefcase.lua`) **уже** использует caches — основной путь нет
- **JAZZ:** файл скопирован; реальный travel sync-sensitive; **UI preview memoize** — безопасный follow-up
- **Фикс ванили:** те же caches + heap/bucket вместо линейного min-extract; hover не звать Dijkstra дважды

### P1 — UI / exploration

#### V-UI-001 — Interactable highlight: `MapGet("map","Interactable")` + цикл 200 ms
- **Где:** `UI/IModeCommonUnitControl.lua` (~759–855)
- **Частота:** пока зажат highlight
- **JAZZ patch?** **Безопасно** (UI-only): spatial cull / on-screen only
- **Фикс ванили:** spatial index; кэш списка

#### V-UI-002 — Approach banters на каждом exploration visibility tick
- **Где:** `Exploration.lua` → `Banter.lua` `UpdateApproachBanters` (~2854–2943)
- **Частота:** каждые 500 ms, O(units²) distance + filter
- **Фикс ванили:** 2–5 s throttle; spatial hash

#### V-UI-003 — Nested `ForEachItem` в Inventory Take All / free-space
- **Где:** `XTemplates/Inventory.lua`, `Inventory.lua`
- **Частота:** UI actions (не combat FPS)
- **Фикс ванили:** index stacks; single-pass free-space

### P2 — AmbientLife / GC

#### V-AL-001 — AmbientLife full-map sweeps на spawn/despawn / conflict
- **Где:** `AmbientLife.lua`
- **Фикс ванили:** registry маркеров вместо `MapForEach("map", …)`

#### V-AI-GC-001 — Temp `point()` / `CombatPath:new()` / cover tables в AI loops
- **Где:** `AIPrecalcDamageScore`, `Cover.lua` `GetCoversAt`
- **Фикс ванили:** packed positions; recycle buffers

#### V-VIS-DBG-001 — `g_ExperimentalModeLOS` ветка в shipped LOS
- **Где:** `Visibility.lua` (~251–272), TODO remove
- **Severity:** low

---

## CommonLib: что уже помогает / риски

| Оптимизация CLib | Статус под JAZZ |
|---|---|
| Suspicion early-outs (`FixAI.lua`) | JAZZ владеет `UpdateSuspicion` — early-outs **репортированы** в этом change set |
| Overwatch visual hash (`GeneralFixes.lua`) | JAZZ не override — **активно** |
| `IsLineInSmoke` empty early-out | JAZZ заменяет; empty-smoke early-out сохранён |
| `_Stubs` тяжёлых mod-conflict scans | Активно (load/editor) |
| Appearance delayed batch | Активно |
| `GetCursorPosEx` cursor cache | JAZZ пока не использует — follow-up |

**Замечание (не perf-fix этого PR):** в JAZZ `UpdateSuspicion` условие «behind plane» использует `abs(angle) < 90*60`, тогда как CLib/vanilla — `> 90*60`. Это расхождение **поведения** stealth cut-off; править только после явного решения владельца (spec sync).

---

## Рекомендуемый порядок фикса ванили (для Asphalt/THQ / engine)

1. Incremental / spatial `UpdateUnitsLOS` (**V-VIS-001**)
2. Dest LOS + LoF shortlist в AI (**V-AI-001/002**)
3. Cached Dijkstra + heap (**V-SAT-001**)
4. Faded-slab grid (**V-VIS-002**)
5. Interactable highlight spatialization (**V-UI-001**)

## Безопасные follow-up в JAZZ (не сделано здесь)

| Идея | Риск |
|---|---|
| Memoize satellite **preview** route (не travel) | Низкий |
| UI interactable highlight override | Низкий |
| Gear-change cache vision/camo ints (invalidate on condition dmg) | Средний (stale cache) |
| Collapse `PickBestAttack` aim sampling (0/mid/max) | Средний (меняет AI scores) |
| Исправить behind-plane `abs(angle)` в suspicion | Геймплей / нужен OK владельца |

---

## Связанные документы

- [runtime-editor-integration.md](systems/runtime-editor-integration.md) — правила map enumeration
- [visibility-weather-appearance.md](systems/visibility-weather-appearance.md) — sight hot path
- [ai-awareness.md](systems/ai-awareness.md) — AI pipeline / CTH
- [override-matrix.md](override-matrix.md) — коллизии с CommonLib
