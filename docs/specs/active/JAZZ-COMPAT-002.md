---
id: JAZZ-COMPAT-002
status: implemented
owner: project-owner
systems:
  - strategy-squads-sectors
  - inventory-items-loot
  - units-progression
  - package-architecture
repositories:
  - jazz-nomaps
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-COMPAT-002.md
  - jazz/docs/specs/superseded/JAZZ-COMPAT-001.md
  - jazz/Code/StandaloneNoMapsFallback.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz-nomaps/**
exclusive_resources:
  - ModDef:7MsJ2Eq
  - GameVar:gv_JAZZ_NoMaps
  - Code:NoMaps_Autonomy.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMPAT-002: пакет `jazz-nomaps` (автономия без jazz-maps)

## Решение владельца (направление)

Автономия без maps делается **отдельным модом/репозиторием `jazz-nomaps`**, а не
раздуванием core `jazz`.

| Режим установки | Пакеты |
| --- | --- |
| Полный канон (demo Ernie + authored maps) | `jazz_assets` + `jazz-units` + **`jazz-maps`** + `jazz` (+ CommonLib) |
| Без maps (vanilla HotDiamonds + jazz systems) | `jazz_assets` + `jazz-units` + **`jazz-nomaps`** + `jazz` (+ CommonLib) |

`jazz-maps` и `jazz-nomaps` — **альтернативы**, не ставятся вместе как обязательная пара.
Если оба включены: `jazz-nomaps` обязан быть **полным no-op** (maps wins).

**Реализация одобрена владельцем 2026-07-30.** Пакет `jazz-nomaps` (`7MsJ2Eq`) в GitHub; COMPAT-001 superseded.

## Связь с COMPAT-001

`JAZZ-COMPAT-001` уже влил в `jazz` one-file `Code/StandaloneNoMapsFallback.lua`.

При реализации COMPAT-002:

1. Перенести логику в пакет `jazz-nomaps`.
2. **Удалить** из `jazz`: `StandaloneNoMapsFallback.lua`, ModItemCode, metadata.code entry,
   связанные абзацы «встроенный fallback» в technical (заменить ссылкой на пакет).
3. COMPAT-001 пометить `superseded` этой спекой после миграции.
4. Saves с `gv_JAZZ_StandaloneNoMaps` от phase-1: либо читать тем же GameVar из nomaps,
   либо мигрировать имя в `gv_JAZZ_NoMaps` schema≥1 с совместимым чтением старого ключа.

## Проблема

Без authored `jazz-maps` игрок на vanilla-кампании теряет sector wiring, map loot и
mainland Legion AI regions. Core не должен тащить «режим без maps» как скрытый always-on
хвост: это отдельный продуктный профиль установки.

## Цели

- Новый пакет `jazz-nomaps` (локальный каталог `..\jazz-nomaps`, GitHub-репо по политике suite).
- Весь runtime автономии без maps живёт **только** в этом пакете.
- Gate: no-op при загруженном `FhNNYd` (`jazz-maps`).
- Synthetic Legion AI regions, squad wiring/remap, loot packs, gear refresh.
- Зависимости: `jazz` + `jazz-units` (+ обычно `jazz_assets` / CommonLib); **не** зависит от maps.
- Документировать 5-й пакет в ownership / project-scope / release suite **после** acceptance
  (не раньше coding без approval).

## Non-goals

- Квесты / диалоги / `Maps/**` / vehicles maps.
- Замена `jazz-maps` по контенту Ernie.
- Держать дублирующую логику в core `jazz` после миграции.
- Автоматически включать nomaps в Workshop «полный комплект» (это optional 5-й пакет).
- Реализация до approval.

## Идентичность пакета (зафиксировать при scaffold)

| Поле | Значение |
| --- | --- |
| Каталог / репо | `jazz-nomaps` |
| Mod title | `JAZZ NoMaps` |
| ModDef `id` | **`7MsJ2Eq`** (сгенерён 2026-07-30; Workshop upload позже тем же id) |
| Author | как у suite / owner |
| `lua_revision` | как у остальных пакетов suite |
| Load order | **после** `jazz` и `jazz-units` (Mod Manager / dependency order) |

После первой публикации Workshop/`ModDef.id` не менять.

## Архитектура пакета

### Layout (целевой)

```
jazz-nomaps/
  metadata.lua
  items.lua
  AGENTS.md                 # overlay → ../jazz/AGENTS.md
  Code/
    NoMaps_Bootstrap.lua    # gate, GameVar, NewGame/Load/Init hooks
    NoMaps_Regions.lua      # Voronoi regions, naming, EnsureState
    NoMaps_Squads.lua       # list wiring, GenerateEnemySquad wrap, remap
    NoMaps_Loot.lua         # container inject / LootDef packs
  Const/                    # optional: remap tables
  Localization/             # только если появятся стабильные T-id (не динамические имена округов)
  docs/                     # optional; канон спеки остаётся в jazz/docs/specs
```

Допускается свести Code к 1–2 файлам на старте; split — по мере роста.
**Не** класть UnitData/EnemySquad clones — читать defs из `jazz-units`.

### Слой A — Gate

```
MAPS_ID = "FhNNYd"
if IsModLoaded(MAPS_ID) then return -- every entry point
```

Дополнительно: если maps нет, но нет `jazz` / нет Legion AI symbols — soft disable + log.

### Слой B — Regions

Как в COMPAT-001, владелец кода = nomaps:

- unmanaged `Guardpost` → Region id **`JAZZ_Auto_<sector>`** (префикс `JAZZ_Auto_`, совместим с COMPAT-001);
- географию/ID секторов брать **как в vanilla HotDiamonds** (`CampaignPreset.lua` / `gv_Sectors`), без authored jazz-maps patches;
- Chebyshev ≤ R (default 8);
- **не включать** authored Region `ErnieIsland` из `jazz/items.lua` в no-maps профиле: он ссылается на maps-географию (`ManagedOutposts=I7`, `MajorHQSector=B28`), которой нет в vanilla;
- truncated caps; Tax/Recruiter default 0;
- Major HQ: **vanilla `A20`** (The Eagle's Nest / Major's Camp); если сектора нет — fallback на outpost (REQ-005).

#### Vanilla HotDiamonds evidence (`ModTools/Src/Data/CampaignPreset.lua`)

Источник: установленный JA3 `ModTools/Src` (не jazz-maps).

| Id | display_name | Map | Guardpost |
| --- | --- | --- | --- |
| **A20** | The Eagle's Nest | A-20 - The Majors Camp | **yes** (Major / Boss) |
| D10 | Camp Grand Prix | D-10 - Crossroads Camp | yes |
| E16 | Camp Chien Sauvage | E-16 - River Camp | yes |
| F7 | Camp Savane | F-7 - Savanna Camp | yes |
| F19 | Camp Bien Chien | F-19 - Camp Bien Chan | yes |
| G10 | Camp La Barrière | G-10 - Island Camp | yes |
| H4 | Fort L'Eau Bleu | H-4 - The Fortress | yes (Ernie fortress) |
| H14 | Camp du Crocodile | H-14 - Swamp Camp | yes |

Проверки:

- **`B28` в vanilla отсутствует** (0 вхождений; сетка колонок A–L максимум **20**).
- **`I7` в vanilla = «Savanna Coast»**, без `Guardpost` (не форт).
- **Форт Эрни в vanilla = `H4`**, не `I7` (jazz-maps переносит Fort L'Eau Bleu на `I7`).
- Итого **8** vanilla guardposts → до 8 auto-regions в nomaps.

Ссылка jazz `ErnieIsland` (`I7`/`B28`) валидна **только** с `jazz-maps`.

### Слой C — Squads / units

- Wire empty `EnemySquads*List` → `LegionGlobalAI_*` / `LegionJAZZSquad*`.
- Remap matrix Legion/Army/Adonis/Rebel → jazz defs (Const в nomaps).
- Wrap `GenerateEnemySquad` только пока nomaps active.
- Gear rebuild once per unit id (GameVar); UnitData остаётся в `jazz-units`.

### Слой D — Loot

- LootDef packs внутри `jazz-nomaps` items (или Const + PlaceInventoryItem fallback):
  `JAZZ_NoMaps_Container_Common/Ammo/Weapon`.
- Optional remap vanilla LootTableId → pack.
- Нет quest items из maps.

### Слой E — Dependencies metadata

```
dependencies:
  jazz (e6L4ECj)           required = true
  jazz-units (Dv3mFVN)     required = true
  jazz_assets (pDGDhr)     required = true   # как у канон-suite visuals
  JA3_CommonLib            required = false, min 1.11
  # jazz-maps НЕ указывать
```

Core `jazz` **не** объявляет dependency на nomaps.

### Слой F — Миграция с COMPAT-001

| Шаг | Действие |
| --- | --- |
| 1 | Scaffold `jazz-nomaps` repo + empty ModDef |
| 2 | Перенести/расширить код из `StandaloneNoMapsFallback.lua` |
| 3 | Удалить файл и wiring из `jazz`; bump `jazz` minor notes «moved to jazz-nomaps» |
| 4 | Обновить compatibility / strategy / file-coverage / project-scope (5 пакетов optional) |
| 5 | Release suite / Discord workflows: добавить 5-й caller **только если** owner включает в release |
| 6 | Supersede COMPAT-001 |

### Слой G — Release / docs (после acceptance)

- `AGENTS.md` suite: optional 5-й пакет «вместо maps».
- Showcase about: не смешивать с «ставьте все 4»; отдельная строка «NoMaps profile» только после acceptance.
- `exclusive-resources.yaml`: `jazz-nomaps-generated-root`.

## Требования

- `JAZZ-COMPAT-002-REQ-001` — вся no-maps автономия живёт в пакете `jazz-nomaps`; после миграции
  в `jazz` нет loaded StandaloneNoMaps* кода.
- `JAZZ-COMPAT-002-REQ-002` — при загруженном `FhNNYd` пакет nomaps полностью no-op.
- `JAZZ-COMPAT-002-REQ-003` — без maps: synthetic regions + truncated Legion AI для unmanaged guardposts.
- `JAZZ-COMPAT-002-REQ-004` — squad wiring + faction remap matrix; missing def → skip + one-shot log.
- `JAZZ-COMPAT-002-REQ-005` — `MajorHQSector = "A20"` (vanilla Major's Camp); fallback
  `outpost_id` только если `A20` отсутствует. Сектора/аванпосты — vanilla IDs из
  `CampaignPreset.lua`, не maps-authored (`I7`/`B28` не использовать как HQ/outpost в nomaps).
- `JAZZ-COMPAT-002-REQ-005b` — при активном nomaps authored `ErnieIsland` (`LegionAIEnabled`)
  отключается или не manage'ится (maps-only IDs); управляют только `JAZZ_Auto_*` по vanilla Guardpost.
- `JAZZ-COMPAT-002-REQ-006` — loot через LootDef packs пакета (не только hardcoded list).
- `JAZZ-COMPAT-002-REQ-007` — зависимости: `jazz` + `jazz-units` (+ assets) required; maps не указывать.
- `JAZZ-COMPAT-002-REQ-008` — реализация только после `approved` + idle соседних write sets;
  до этого — только docs/spec.
- `JAZZ-COMPAT-002-REQ-009` — ModDef `id` = `7MsJ2Eq` (Workshop зальёт владелец позже тем же id).
- `JAZZ-COMPAT-002-REQ-010` — COMPAT-001 код удалён из `jazz` в том же change set, что и первая
  играбельная версия nomaps (нет двух активных копий логики).
- `JAZZ-COMPAT-002-REQ-011` — Region id prefix = `JAZZ_Auto_`.

## Инварианты и ограничения

- Не править `jazz-maps/**`.
- Не ломать full-suite с maps.
- Не копировать UnitData/EnemySquad bodies в nomaps.
- Deterministic RNG; минимальный NetSync footprint (предпочтительно ноль).
- Save GameVar backward-compatible с phase-1 ключом или явная one-shot migration.
- Не смешивать с параллельными agent edits в `jazz` Code/Legion до их завершения.

## Acceptance criteria

- `JAZZ-COMPAT-002-AC-001` — пакет `jazz-nomaps` загружается; `metadata.code` указывает только его Code/*.
- `JAZZ-COMPAT-002-AC-002` — install без maps, с nomaps: ≥1 region на unmanaged guardpost; Legion AI tick OK.
- `JAZZ-COMPAT-002-AC-003` — install с maps + nomaps: Regions/sectors не мутируют от nomaps.
- `JAZZ-COMPAT-002-AC-004` — после миграции: в `jazz` metadata.code нет `StandaloneNoMapsFallback.lua`.
- `JAZZ-COMPAT-002-AC-005` — spawn/remap и container loot packs работают (runtime).
- `JAZZ-COMPAT-002-AC-006` — generated sync для `jazz` и `jazz-nomaps` errors=0.
- `JAZZ-COMPAT-002-AC-007` — human: профиль «assets+units+jazz+nomaps» vs «+maps без nomaps» оба стартуют.

## Impact и совместимость

- Suite: 4 пакета канон; `jazz-nomaps` — optional 5-й профиль.
- Workshop: игрок без maps включает nomaps вручную (или отдельный collection).
- Saves: phase-1 GameVar миграция.
- Cross-package: читает `jazz` Legion AI API + `jazz-units` defs; пишет только свой state.
- Rollback: выключить/удалить пакет; core без встроенного fallback после миграции.

## План и ownership

- Пакет-владелец: **`jazz-nomaps`** (новый)
- Миграция/удаление из core: `jazz`
- Исполнитель: TBD
- Reviewer: project-owner
- Declared write set сейчас: эта спека (+ ссылка в COMPAT-001)
- Exclusive resources: none до scaffold

### Порядок после approval

1. Idle соседних агентов.
2. Scaffold repo `jazz-nomaps` с ModDef id `7MsJ2Eq`.
3. Перенос логики + LootDef/remap expansion (vanilla guardposts, HQ **`A20`**, prefix `JAZZ_Auto_`;
   disable authored `ErnieIsland` без maps).
4. Удаление COMPAT-001 из `jazz`.
5. Docs/ownership; release/Discord callers — **позже** (не блокер первой играбельной версии).
6. Runtime AC → implemented → accepted; supersede COMPAT-001.
7. Workshop upload — владелец, тем же `7MsJ2Eq`.

## Решение владельца

- Статус: **implemented** (пакет `jazz-nomaps` создан; COMPAT-001 superseded)
- ModDef `id` = **`7MsJ2Eq`**
- Сектора = vanilla HotDiamonds; Major HQ = **`A20`**; Ernie fortress = **`H4`**
- Authored `ErnieIsland` отключается nomaps runtime
- `jazz-units` required; Region prefix `JAZZ_Auto_`
- Дата: 2026-07-30

## Evidence

- `JAZZ-COMPAT-002-AC-001`: `PASS (static)` — `jazz-nomaps` / `Code/NoMaps_Autonomy.lua` / id `7MsJ2Eq`.
- `JAZZ-COMPAT-002-AC-002`: `BLOCKED (runtime)` — new game без maps.
- `JAZZ-COMPAT-002-AC-003`: `BLOCKED (runtime)` — maps+nomaps no-op.
- `JAZZ-COMPAT-002-AC-004`: `PASS (static)` — `StandaloneNoMapsFallback` удалён из jazz metadata/items.
- `JAZZ-COMPAT-002-AC-005`: `PASS (static)` — LootDef packs `JAZZ_NoMaps_Container_*` + GenerateLoot inject path; runtime BLOCKED.
- `JAZZ-COMPAT-002-AC-006`: `BLOCKED (editor)` — editor round-trip.
- `JAZZ-COMPAT-002-AC-007`: `BLOCKED (human)`.

## Documentation delta

- Technical compatibility / strategy / file-coverage / AGENTS / project-scope / exclusive-resources обновлены.
- COMPAT-001 → `docs/specs/superseded/`.
- Пакет `jazz-nomaps` с LootDef packs.