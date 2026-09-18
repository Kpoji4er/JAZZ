---
id: JAZZ-AI-CMD-003
status: approved
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
  - jazz-units
risk: high
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-CMD-003.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/wiki/officer-aura.md
  - jazz/docs/showcase/ru/officer-aura.md
  - jazz/docs/showcase/en/officer-aura.md
  - jazz/Code/AIContextProfiles.lua
  - jazz/Code/CombatAI.lua
exclusive_resources:
  - none
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/specs/active/JAZZ-AI-CMD-001.md
  - docs/specs/active/JAZZ-AI-008.md
approved_by: project-owner
---

# JAZZ-AI-CMD-003: ролевой фильтр директив (высоты / поджатие / переход в Push)

## Проблема

Офицер пишет **одну** team-директиву. На K5 (playtest 2026-09-03, сейв Сергея) весь отряд получил «Занять высоты» и сбился в угол у скалы. Стрелкам высота нужна; штурмовикам / фланкерам / медикам — нет.

Сейчас `context.jazz_occupy_heights` даёт **всем** в ауре `HighGround ×175%`. `JazzAI_UnitIsLinePerchHolder` ещё и считает perch-holder’ом любого с этой аурой — Assaulter у подножия лезет на ту же коробку.

Picker: OccupyHeights **520**, Push **500** при враге ≤12. На mid-range (13–23) Push не кандидат; Heights держится **~3 хода** (fatigue −80/ход), пока не упадёт ниже HoldLine. Игрок со снайперской огневой точкой зажимает толпу, а ИИ не переходит в агр.

Владелец в Discord: стрелкам — высоты; остальным поджаться к стрелкам **без** высоты; в какой-то момент толпой пушить и стрелять.

## Цели

- Одна видимая директива на команду (UI не размножать).
- Эффект `OccupyHeights` только у **line perch holders** (Sniper / Marksman / semi-sniper / Frontliner / MG). Не Assaulter / Flanker / Medic / Deserter / melee / aura `pusher`.
- Остальные в ауре: **cling** к ближайшему perch-holder’у (или офицеру), укрытие, **без** HighGround ×175% и без perch-hold.
- Срывать Heights в давление, когда perch **уже стреляет**, а не когда игрока только забайтили на сектор или сняли одного издалека.

## Non-goals

- Новые имена директив в UI.
- Менять FocusFire targeting bias (×2 на `focus_target` остаётся на всю ауру).
- GOAP / общий pathfind за отряд.
- Мины на ступеньках K5, дымка, квест заложника.
- Переписывать SNIPER-001 stay-hold, кроме снятия ложного perch через aura-флаг.

## Зафиксировано владельцем (2026-09-06)

Контракт утверждён («делай», чат 2026-09-06). Реализация в `AIContextProfiles.lua` + `CombatAI.lua`.

- Одна директива на команду в UI («Занять высоты»), без отдельных статусов ролям.
- Высоты только **line perch**: Sniper / Marksman / semi-sniper / Frontliner / MG. Не Assaulter / Flanker / Medic / Deserter / melee / aura `pusher`.
- `JazzAI_UnitIsLinePerchHolder` **не** становится true из-за ауры `OccupyHeights`.
- Perch считается по **семье / UnitData / keywords** (`JazzAI_InferRoleFamily`: Line / MG / Leader со Sniper|Marksman). **Не** по `current_archetype` после stance-switch: `OccupyHeights` уже гоняет Scout/Pusher/Recruit/Line → Frontliner (K5 DAP: скауты на Frontliner из‑за этого проходили как perch).
- `HighGround ×175%` только у perch; остальные **100%**.
- Не-perch: **cling 2–10** тайлов к ближайшему живому perch-holder’у в ауре (иначе к офицеру) + TakeCover; не лезть выше якоря без LOS-нужды.
- **Медик:** если есть живой раненый, которого лечит [JAZZ-AI-MED-001](JAZZ-AI-MED-001.md) (bleed / HP&lt;85% в радиусе OptLoc), cling к **пациенту** важнее cling к стрелку. Нет такого раненого — как остальные не-perch (к perch-holder / офицеру).
- **Срыв Heights:** не от первой смерти и не от last_known «в дальности». Пока снайперы не видят и не могут стрелять — Heights (игрока нельзя переснайперить издалека, его вынуждают подойти). Как только ≥1 снайпер/охотник **реально видит** и **может выстрелить** — UI «Давить», **остальные** идут в контратаку, снайперы остаются на высоте. Нельзя оставить только пулемётный OW.

## Требования

- `JAZZ-AI-CMD-003-REQ-001` — **locked.** `JazzAI_UnitIsLinePerchHolder` без aura-short-circuit и без «perch потому что сейчас Frontliner». Perch = семья Line/MG или Leader+Sniper|Marksman / dedicated Front|MG UnitData. Scout/Pusher/Medic/Heavy/Recruit — не perch, даже если stance = `*_Frontliner`.
- `JAZZ-AI-CMD-003-REQ-002` — **locked.** `HighGround ×175%` при `jazz_occupy_heights` только у perch (после REQ-001). Остальные в ауре: **100%**.
- `JAZZ-AI-CMD-003-REQ-003` — **locked.** Не-perch при `OccupyHeights`: proximity к ближайшему живому perch-holder’у в той же ауре (иначе к офицеру), окно **2–10** тайлов, плюс TakeCover. Не лезть на Z выше якоря больше чем на **0** slab без LOS-нужды.
- `JAZZ-AI-CMD-003-REQ-004` — **locked** (чат 2026-09-06). Переход Heights → давление. Цель: **нельзя переснайперить** издалека и **нельзя забайтить** на пулемётные OW; игрок вынужден подойти, после этого — жёсткая контратака, не ещё три хода в углу.
  1. **Дальний фарм / нет живого выстрела у perch:** Heights остаётся. Первая смерть или входящий огонь **сами по себе не** срывают Heights (отклонён черновик «потеря + nearest ≤20 → Push 600»). Last_known в `WeaponRange` без vis/выстрела — не триггер.
  2. **Живой выстрел perch:** если ≥1 живой **Sniper / Marksman / dedicated semi-sniper** в ауре **видит** живого врага (`HasVisibilityTo` / team vis) **и** может по нему стрелять (`GetUIState` атаки enabled, цель в `WeaponRange`, не stuck LoF) — picker даёт **Push** вес **600** (бьёт Heights 520). UI → «Давить». Снайперы **остаются** на высоте и стреляют (stance Sniper/Marksman, не Assaulter). **Остальные** (Scout / Pusher / Recruit / Line без оптики) идут в Push/press. MG остаётся Machinegunner, но не держит команду в cling/OW вместо штурма.
  3. Враг ≤12 — Push **500**, как сейчас (доп. к п.2, не вместо).
- `JAZZ-AI-CMD-003-REQ-005` — **locked.** UI: один приказ на командире/ауре. Отдельных статусов ролям нет. Пока perch не имеют живого выстрела — «Занять высоты»; после REQ-004.2 — «Давить».
- `JAZZ-AI-CMD-003-REQ-006` — **locked.** Медик при Heights: если есть живой пациент по [JAZZ-AI-MED-001](JAZZ-AI-MED-001.md) (bleed или HP&lt;85% в OptLoc), якорь cling = пациент, не perch-holder. Иначе REQ-003. На Push после REQ-004.2 медик всё ещё лечит пациента, если он есть.

## Остаток (не блокирует REQ-004)

Игрок уже близко (мертвая зона, 13–25 клеток), а снайперы **всё ещё** без vis/выстрела. Тогда срабатывает только ≤12. Если на playtest снова «подошли, а штурма нет» при слепых снайперах — отдельный порог (например nearest ≤15 + team vis у любого perch, не только оптики). Пока не вводить.

## Инварианты и ограничения

- Одна директива на команду; ephemeral MapVar без новых save-полей.
- Deterministic: без нового RNG в picker (кроме уже существующего FallBack chance).
- Не ломать CMD-002 слоты Early/Normal/Late.
- Не давать Assaulter perch-hold через ауру.

## Acceptance criteria

- `JAZZ-AI-CMD-003-AC-001` — static: `JazzAI_UnitIsLinePerchHolder` без aura-short-circuit; HighGround ×175% только у perch.
- `JAZZ-AI-CMD-003-AC-002` — runtime K5-подобный склон: снайперы/фронт на высоте, штурм/фланк внизу у них, не вся пачка в одном углу.
- `JAZZ-AI-CMD-003-AC-003` — runtime: (a) снайпер на высоте без vis/выстрела — директива Heights, штурм не бежит через поле; (b) тот же снайпер видит и может стрелять — со следующего хода ИИ UI «Давить», не-perch идут вперёд, снайпер остаётся и стреляет; (c) нельзя оставить только MG-OW без штурма в этом кадре.
- `JAZZ-AI-CMD-003-AC-004` — docs: archetypes + ai-awareness + officer-aura wiki/showcase.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: только JAZZ dest score + perch predicate.
- Saves: ок.
- Network/determinism: без нового RNG в фильтре ролей.
- Cross-package: jazz-units stance/keywords уже есть; код фильтра — `jazz`.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent (чат 2026-09-06)
- Reviewer: project-owner
- Declared write set: см. front matter

## Решение владельца

- Статус: `approved`
- Кто подтвердил: project-owner («делай», чат 2026-09-06).
- Дата: 2026-09-06

## Evidence

- `JAZZ-AI-CMD-003-AC-001`: `PASS` (static) — `python docs/tools/_check_cmd003_perch_filter.py`; perch без aura/Frontliner; HighGround только perch/spotter.
- `JAZZ-AI-CMD-003-AC-002`: `BLOCKED` — runtime K5-склон, human.
- `JAZZ-AI-CMD-003-AC-003`: `BLOCKED` — runtime live-shot → Push, human.
- `JAZZ-AI-CMD-003-AC-004`: `PASS` (static) — `ai-awareness.md`, `tactical-ai-archetypes.md` §6, wiki + showcase RU/EN `officer-aura`.

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — CMD-003 perch/cling/live-shot.
- `docs/design/tactical-ai-archetypes.md` §6 — Heights/Push rows.
- `docs/wiki/officer-aura.md`, `docs/showcase/ru/officer-aura.md`, `docs/showcase/en/officer-aura.md`.
