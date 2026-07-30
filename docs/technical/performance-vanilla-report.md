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

## Непофикшенные проблемы ванили (карточки EN)

Каждая проблема ванили, которую **CommonLib не закрывает**, вынесена в отдельный англоязычный файл:

**Каталог:** [`performance/vanilla-unfixed-by-commonlib/`](performance/vanilla-unfixed-by-commonlib/README.md)

| ID | Карточка |
|---|---|
| V-AI-001 | [dest LOS cache](performance/vanilla-unfixed-by-commonlib/V-AI-001-dest-los-cache.md) |
| V-AI-002 | [precalc damage LoF](performance/vanilla-unfixed-by-commonlib/V-AI-002-precalc-damage-lof.md) |
| V-AI-003 | [dual path + OptLoc](performance/vanilla-unfixed-by-commonlib/V-AI-003-dual-path-optloc.md) |
| V-AI-004 | [score dest fire/gas](performance/vanilla-unfixed-by-commonlib/V-AI-004-score-dest-fire-gas.md) |
| V-AI-005 | [emplacement MapGet](performance/vanilla-unfixed-by-commonlib/V-AI-005-emplacement-mapget.md) |
| V-VIS-001 | [UpdateUnitsLOS O(n²)](performance/vanilla-unfixed-by-commonlib/V-VIS-001-update-units-los.md) |
| V-VIS-002 | [faded slab MapGet](performance/vanilla-unfixed-by-commonlib/V-VIS-002-faded-slab-mapget.md) |
| V-SAT-001 | [satellite Dijkstra](performance/vanilla-unfixed-by-commonlib/V-SAT-001-satellite-dijkstra.md) |
| V-UI-001 | [interactable highlight](performance/vanilla-unfixed-by-commonlib/V-UI-001-interactable-highlight.md) |
| V-UI-002 | [approach banters](performance/vanilla-unfixed-by-commonlib/V-UI-002-approach-banters.md) |
| V-UI-003 | [inventory nested ForEach](performance/vanilla-unfixed-by-commonlib/V-UI-003-inventory-nested-foreach.md) |
| V-AL-001 | [AmbientLife map sweeps](performance/vanilla-unfixed-by-commonlib/V-AL-001-ambient-life-map-sweeps.md) |
| V-AI-GC-001 | [AI temp allocations](performance/vanilla-unfixed-by-commonlib/V-AI-GC-001-ai-temp-allocations.md) |
| V-VIS-DBG-001 | [experimental LOS branch](performance/vanilla-unfixed-by-commonlib/V-VIS-DBG-001-experimental-los-branch.md) |

**Не входит в каталог (CLib уже смягчает):** suspicion ally×enemy early-outs (`FixAI.lua`), overwatch visual hash, empty-smoke `IsLineInSmoke`, editor/mod-load stubs. Структурный O(allies×enemies) suspicion остаётся, но это не «полностью непофикшено CLib».

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

- [performance/vanilla-unfixed-by-commonlib/](performance/vanilla-unfixed-by-commonlib/README.md) — EN-карточки проблем ванили без фикса CLib
- [runtime-editor-integration.md](systems/runtime-editor-integration.md) — правила map enumeration
- [visibility-weather-appearance.md](systems/visibility-weather-appearance.md) — sight hot path
- [ai-awareness.md](systems/ai-awareness.md) — AI pipeline / CTH
- [override-matrix.md](override-matrix.md) — коллизии с CommonLib
