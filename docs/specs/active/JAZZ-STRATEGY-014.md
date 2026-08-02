---
id: JAZZ-STRATEGY-014
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - enemy-squads
  - satellite-conflict
repositories:
  - jazz
  - jazz-units
  - jazz-nomaps
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-014.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/Code/FactionOverlay.lua
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/WorldFlipSpawnUnits.lua
  - jazz/Code/SatelliteSquad.lua
  - jazz/metadata.lua
  - jazz/items.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz/docs/tools/_audit_faction_overlay_static.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - GameVar:gv_JAZZ_FactionOverlay
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner chat 2026-08-02 — approve STRATEGY-014 (sat=tactical hostility matrix + ownership)
---

# JAZZ-STRATEGY-014: faction hostility overlay + outpost ownership

## Проблема

JA3 не даёт матрицы фракций: runtime по сути делит мир на player / enemy / ally. Отряды «врагов» не умеют планово воевать друг с другом на sat, а на тактике часто схлопываются в одну сторону — даже если на стратегии они враги. Дизайн кампании требует развести **Legion / Adonis / Army / Rebels**, владение аванпостами после World Flip, разные отношения к игроку **до** и **после** Betrayal, и **одинаковую** вражду на sat и на тактической карте.

Текущий Legion Global AI (`gv_JAZZ_LegionAI`, `JAZZ_Auto_*`) и `SpawnWorldFlipAttackSquads` живут отдельно: flip не передаёт ownership форта, Легион продолжает спавнить с `enemy1`-аванпостов, Adonis/Army — только скриптовые полосы.

## Цели

- Свой **faction overlay** (не надеяться на vanilla Side как на единственный источник истины).
- Матрица отношений фракций друг с другом и с игроком (ниже — locked owner answers).
- **Одна матрица на оба слоя:** кто `hostile` на стратегической карте — тот же `hostile` на тактической (и в autoresolve); кто `ally`/`neutral` — не стреляет друг в друга на тактике из‑за «все красные = одна сторона».
- **Владелец аванпоста** = кто захватил; на World Flip форт не «автоматически остаётся Легионом».
- Базовая способность фракций **воевать друг с другом** на sat (минимум: захват/штурм чужого managed outpost) **и** корректные стороны в tactical/autoresolve — без этого матрица только лейбл.

## Non-goals

- Полная дипломатия / торговля / квестовые ветки всех фракций.
- Одновременная война Адонис↔Армия за один форт (они **не** враждебны друг другу).
- Замена всего vanilla `Side` во всех системах игры за один спек.
- Реализация кода — после `approved` + DoR; этот файл — контракт, не shipped runtime.
- Отдельная «тактическая» матрица, отличная от стратегической (запрещено).

## Locked defaults (owner 2026-08-02)

Фракции overlay (полные): `player`, `legion`, `adonis`, `army`, `rebels`.  
`smugglers` — **минифракция** (иконки/тема есть); полноценный director/ownership **не** в scope 014, пока owner не решит иначе.

| Отношение | Правило |
| --- | --- |
| Rebels → player | **союз** |
| Rebels → legion / adonis / army | **всегда враг** |
| Adonis ↔ Army | **мир** (не воюют) |
| Adonis / Army → Legion | **враг** |
| Legion → player | **враг** (как сейчас) |
| Adonis / Army → player | **нейтрал до World Flip**; **враг с момента** `04_Betrayal` `TriggerWorldFlip` / `WorldFlipDone` |
| Outpost ownership | **кто захватил — тот владеет**; смена владельца только захватом (или явным script effect в дочернем спеке) |
| World Flip | не сбрасывает ownership к Легиону; скриптовые полосы Adonis/Army могут **захватывать** и становиться owner |
| Sat ↔ tactical | `JAZZ_GetFactionRelation` — **единый** источник; hostile на sat ⇒ hostile на tactical map / autoresolve; ally/neutral ⇒ не атакуют друг друга на тактике |

Сигнал World Flip для hostility player↔adonis/army: тот же, что `JAZZ_IsWorldFlipProgressionActive()` (COMPAT-003 / Bobby Ray T3).

## Visual identity (щиты `SquadsIcons/Enemy`)

Канон UI/docs: те же подложки, что squad-role icons ([squad-role-icons.md](../../technical/systems/squad-role-icons.md), skill `create-jazz-squad-icons`).  
Общий стиль: щит 64×64, прозрачный canvas, ivory-символ ≈ `#E6DECA`, outline ≈ `#301C1C`.

| Faction id | Щит | Тема | Avg fill (sampled) | Dominant / accents |
| --- | --- | --- | --- | --- |
| `legion` | `legion.png` | сплошной madder-red / burgundy | `#B5424B` | `#B84048`, dark rim `#303038` |
| `army` | `army.png` | красно-коричневый camo | `#89524D` | `#884848`, `#805048`, `#784040` |
| `adonis` | `adonis.png` | purple / violet mottled | `#503770` | `#482870`, `#503878` |
| `rebels` | `rebels.png` | green woodland camo | `#46865E` | `#388058`, `#509068` |
| `smugglers` | `smugglers.png` | money / orange (купюры) | `#CB5C27` | `#E06828`, `#D86020` — **reserved**, mini-faction |

Player в overlay без отдельного щита в этом каталоге (vanilla player UI); в docs/matrix не красить «как пятый враг».

При UI ownership / faction labels в wiki/showcase — использовать эти темы (не придумывать новую палитру).

## Требования

- `JAZZ-STRATEGY-014-REQ-001` — публичный API матрицы: `JAZZ_GetFactionRelation(a, b)` → `ally` / `neutral` / `hostile` по locked defaults; детерминированно; save/network-safe; **один** API для sat и tactical.
- `JAZZ-STRATEGY-014-REQ-002` — у managed outpost хранится `owner_faction` (не только `Side`); спавн директора идёт от владельца (Legion AI / будущий Adonis-Army director / rebels — по owner).
- `JAZZ-STRATEGY-014-REQ-003` — захват аванпоста игроком или враждебной фракцией меняет `owner_faction`; прежний директор парализуется / передаёт state; retake только если новый owner враждебен старому по матрице.
- `JAZZ-STRATEGY-014-REQ-004` — до World Flip отряды Adonis/Army **не** инициируют sat-атаки на player-controlled сектора; после Flip — могут (в рамках своих directors / lanes).
- `JAZZ-STRATEGY-014-REQ-005` — sat-слой: враждебные non-player фракции могут планировать конфликт/захват **чужого** outpost (минимум Legion↔Adonis/Army); Adonis↔Army конфликтов нет.
- `JAZZ-STRATEGY-014-REQ-006` — tactical / autoresolve: пары с `hostile` в матрице **стреляют друг в друга** на тактической карте (не схлопываются в одного `enemy`); пары `ally`/`neutral` (в т.ч. Adonis↔Army, Rebels↔player) **не** враждуют на тактике. До World Flip Adonis/Army не враждебны player и на тактике.
- `JAZZ-STRATEGY-014-REQ-007` — NoMaps и maps: один контракт ownership; география Ernie `I7` vs mainland `JAZZ_Auto_*` не ломает матрицу.
- `JAZZ-STRATEGY-014-REQ-008` — Documentation: technical + wiki/showcase player-facing (кто владеет фортом; когда Адонис/Армия враги; что вражда sat = вражда на тактике).

## Инварианты и ограничения

- Vanilla `Side` остаётся для player control / militia / legacy quests; overlay — канон для faction AI ownership **и** для «кто враг кому» в combat targeting.
- Не ломать текущий Legion Global AI на pre-Flip playtest до подключения ownership migration.
- Deterministic RNG / NetSync для любых новых sat-атак.
- GameVar schema: additive migration; старые сейвы без `owner_faction` → infer Legion если `enemy1` + managed, иначе `unknown` + repair pass.
- Полная «война всех со всеми» вне матрицы — out of scope.
- Запрещено: sat говорит «враги», а на тактике они в одной команде / игнорируют друг друга.

## Acceptance criteria

- `JAZZ-STRATEGY-014-AC-001` — static: матрица + API покрывают все пары из locked defaults (включая Adonis/Army→player pre/post Flip); один API для sat+tactical.
- `JAZZ-STRATEGY-014-AC-002` — runtime/human: до Flip Adonis/Army squad не открывает sat conflict на player sector; после Flip — может по правилам director.
- `JAZZ-STRATEGY-014-AC-003` — runtime/human: захват managed outpost меняет `owner_faction`; прежний Legion AI с этого форта не спавнит.
- `JAZZ-STRATEGY-014-AC-004` — runtime/human: World Flip lane / faction capture оставляет форт за захватчиком, не reset на Legion.
- `JAZZ-STRATEGY-014-AC-005` — runtime/human или BLOCKED→follow-up: Legion vs Adonis sat-захват чужого форта возможен; Adonis vs Army — нет.
- `JAZZ-STRATEGY-014-AC-006` — runtime/human: на тактической карте (и autoresolve) Legion vs Adonis/Army/Rebels **воюют**; Adonis vs Army **не** воюют; Rebels vs player **не** воюют; до Flip Adonis/Army vs player **не** воюют на тактике.
- `JAZZ-STRATEGY-014-AC-007` — docs delta technical + wiki/showcase обновлены в том же change set, что runtime (в т.ч. sat=tactical hostility).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: новый overlay; затронет Satellite conflict, squad Side assignment, **combat targeting / team assignment / autoresolve**; высокий риск десинков.
- Saves: нужна миграция `owner_faction` / relation epoch (pre/post Flip).
- Network/determinism: все атаки/владение через NetSync / InteractionRand contexts.
- Generated data: возможно UnitData/EnemySquad Side или markers — уточнить в implementation plan.
- Cross-package: `jazz` (runtime), `jazz-units` (squad defs), `jazz-nomaps` (WorldFlip wrap / Auto regions).
- Rollback: feature flag / dormant until approved wave ships.

## План и ownership

- Пакет-владелец: `jazz` (overlay + sat directors + tactical hostility wiring); `jazz-nomaps` / `jazz-units` — wiring.
- Исполнитель: agent after `approved`.
- Reviewer: project-owner.
- Declared write set: см. frontmatter (расширится при реализации).
- Exclusive resources: `gv_JAZZ_FactionOverlay`, пересечение с `gv_JAZZ_LegionAI` — одна волна / один агент.
- Рекомендуемые фазы после approve:
  1. Matrix API + GameVar + migration (sat+tactical contract в API с первого дня).
  2. Outpost `owner_faction` + stop Legion spawn when not owner.
  3. Flip hostility gate for Adonis/Army vs player (sat **и** tactical).
  4. Faction-vs-faction sat capture (Legion↔Adonis/Army).
  5. Tactical dual-side / targeting (часть того же контракта; вынос в STRATEGY-015 только если объём ломает DoR — тогда 015 обязан ссылаться на ту же матрицу).

## Решение владельца

- Статус: **implemented** (static wave; runtime/human AC still open)
- Ответы owner (2026-08-02): (1) hostility Adonis/Army→player с World Flip; (2) Rebels всегда враг остальным AI-фракциям; (3) кто взял форт — тот владеет.
- Уточнение: вражда матрицы едина для **стратегии и тактики** (не две разные таблицы).
- Утверждение: `approved_by` project-owner chat 2026-08-02.

## Evidence

- `JAZZ-STRATEGY-014-AC-001`: `PASS (static)` — `docs/tools/_audit_faction_overlay_static.py`; `JAZZ_GetFactionRelation` locked pairs + flip gate.
- `JAZZ-STRATEGY-014-AC-002`: `BLOCKED (runtime/human)` — pre/post Flip Adonis sat gate wired in `SatelliteReachSectorCenter`; needs playtest.
- `JAZZ-STRATEGY-014-AC-003`: `BLOCKED (runtime/human)` — `owner_faction` + Legion `enabled` gate in `lEnsureOutpost` / `lSetOutpostControlState`; needs capture playtest.
- `JAZZ-STRATEGY-014-AC-004`: `BLOCKED (runtime/human)` — World Flip stamps Adonis/Army ownership; needs Flip playtest.
- `JAZZ-STRATEGY-014-AC-005`: `BLOCKED (runtime)` — sat Legion↔Adonis capture director beyond Flip stamp not shipped; Flip ownership stamp only.
- `JAZZ-STRATEGY-014-AC-006`: `BLOCKED (runtime/human)` — `Team:IsEnemySide` wrap + sat hostile gate present; needs combat evidence.
- `JAZZ-STRATEGY-014-AC-007`: `PASS (static)` — technical + wiki + showcase RU/EN updated.

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md`, `file-coverage.md`
- `docs/wiki/legion-global-ai.md`
- `docs/showcase/ru|en/legion-strategy.md`
- `docs/tools/_audit_faction_overlay_static.py` + README
- Roadmap §8 remains the queue pointer; runtime acceptance pending.
