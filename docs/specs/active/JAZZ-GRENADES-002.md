---
id: JAZZ-GRENADES-002
status: implemented
owner: project-owner
systems:
  - explosives-traps-heavy-weapons
  - armor-damage-wounds-will
repositories:
  - jazz
risk: high
generated_data: false
runtime_validation: required
write_set:
  - jazz/Code/System_ArmorRating.lua
  - jazz/Code/Systems_Medicine.lua
  - jazz/Code/System_OR_Unit.lua
  - jazz/docs/specs/active/JAZZ-GRENADES-002.md
  - jazz/docs/technical/systems/explosives-traps-heavy-weapons.md
  - jazz/docs/technical/systems/armor-damage-wounds-will.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-GRENADES-002: blast knockback (skill roll Strength+Health vs pre-armor damage)

## Проблема

Ванильный `SteroidPunch` реально отбрасывает цель по slab’ам (`ResolveSteroidPunch` → `Punched`). У гранат/blast в текущем билде ванили `ExplosionFly` заглушен («not flying anymore»), а JAZZ-оверрайд `Unit:ApplyDamageAndEffects` вообще не вызывает fly-реакцию. Игрок ожидает, что сильный blast может отшвырнуть юнита, но не всех подряд — нужна skill-проверка от атрибутов тела.

## Цели

- На blast-хите живой Human проходит **skill roll**: тело (`Strength + Health`) против силы взрыва (`force` = урон **до брони**, множитель **×1**).
- `Strength` / `Health` — атрибуты юнита (1..100), не `HitPoints`.
- Провал ролла → radial knockback как у SteroidPunch (`Punched` → prone), направление от эпицентра.
- Успех → стоим (concussion/trauma/Will без изменений контракта).
- Без mock-`SteroidPunchGrenade` / повторного `ExplosionDamage`.

## Non-goals

- Менять `SteroidPunch` / signature Анаболика.
- Восстанавливать ванильный cartoon `ExplosionFly` как death-ragdoll.
- Knockback от дыма / tear / toxic / fire (`aoeType != "none"`).
- Масштаб `pushSlabs` от margin of failure (v1 = фиксированный 1).
- UI floating text resist/fly (debug CombatLog ок; player text — wiki/showcase).
- Отдельный CharacterEffect ID.
- Generated items / Bobby (loc CSV — только если появится явная UI-строка).

## Решения владельца

| # | Вопрос | Статус | Решение |
| --- | --- | --- | --- |
| D1 | Модель проверки | **locked** | Skill roll (RNG), не голый порог |
| D2 | Что считать `force` | **locked** | Урон blast **до брони**, множитель **×1** (не ×2) |
| D3 | Scope источников | **locked** | Все `JazzIsBlastExplosiveHit` (frag/HE/40mm/mortar HE/demo / `aoeType none`), center и area |
| D4 | Кто отлетает | **locked** | Любой живой Human (мерки и враги); не-Human — skip |
| D5 | Иммунитеты / skip | **locked** | Dead; Prone; Unconscious; `TempHitPoints > 0`; prediction; `hit.grazing` |
| D6 | Дистанция push | **locked** | `pushSlabs = 1` (паритет Steroid) |
| D7 | Нет свободных slab’ов | **locked** | On-spot knockdown → prone |
| D8 | Mock grenade collateral | **locked** | Нет |
| D9 | Порядок | **locked** | Урон+effects+concussion/trauma, затем knockback roll; fail → `JazzBlastKnocked` |
| D10 | `force <= 0` | **locked** | Ролл не бросаем → всегда pass (flashbang и т.п.) |

Форма skill roll ниже — **locked** владельцем (2026-08-08).

## Модель

### `force` (до брони)

```text
force = Max(0, pre_armor_blast_damage)
```

Канон: номинальный урон hit’а **до** armor DR.

- Если на hit уже есть `armor_prevented`: `force = (hit.damage or 0) + (hit.armor_prevented or 0)`.
- Если blast path ещё не применял DR: `force = hit.damage` (это и есть pre-armor).
- При необходимости реализации — штамп `hit.jazz_pre_armor_damage` в момент фиксации AoE damage, до любого `ApplyHitDamageReduction`.

Не использовать post-armor HP loss как `force`.

### Skill roll (предложение, близко к «Str+Health vs damage»)

Семейство `RollSkillCheck`: d100, успех при `roll < value`.

```text
body   = unit.Strength + unit.Health     -- атрибуты
force  = pre_armor_blast_damage          -- ×1
value  = Clamp(body - force, 0, 100)     -- эффективный «скилл» устоять
roll   = 1 + unit:Random(100)            -- sync-safe unit RNG
-- опционально как RollSkillCheck: +5*morale к value; Veteran +10 (JAZZ-IMP-001)
pass   = (force <= 0) or (roll < value)  -- pass = устоял, без knockback
fail   = not pass                        -- отлёт
```

Примеры (без morale/Veteran):

| body | force | value | P(устоять) ≈ |
| --- | --- | --- | --- |
| 160 | 60 | 100 | ~99% (`roll < 100`) |
| 100 | 60 | 40 | 39% |
| 80 | 80 | 0 | 0% (всегда отлёт) |
| 120 | 40 | 80 | 79% |

Debug CombatLog: body / force / roll / value / Pass|Fail.

### Knockback

`JazzResolveBlastKnockback(unit, epicenter, attacker, pushSlabs=1)`:

1. `angle = CalcOrientation(epicenter, unit)`; нет epicenter → skip (не fallback на attacker).
2. Свободные slab’ы как `ResolveSteroidPunch`.
3. Команда эквивалента `Punched` **без** `SteroidPunchExplosion`.
4. Path queries детерминированы engine; единственный RNG — skill roll выше.

Хук: после blast package в `ApplyDamageAndEffects`, только если юнит ещё жив / не Die|Downed от этого hit’а.

## Требования

- `JAZZ-GRENADES-002-REQ-001` — для `JazzIsBlastExplosiveHit` + живой Human без skip D5: skill roll `body − force` (d100); fail → knockback; pass → без смены позиции.
- `JAZZ-GRENADES-002-REQ-002` — `force` = pre-armor blast damage ×1; не post-armor applied damage.
- `JAZZ-GRENADES-002-REQ-003` — knockback = Steroid-style push от эпицентра, `pushSlabs = 1`, без mock grenade.
- `JAZZ-GRENADES-002-REQ-004` — smoke/tear/toxic/fire, grazing, prediction не роллят.
- `JAZZ-GRENADES-002-REQ-005` — `force <= 0` → без ролла и без отлёта.
- `JAZZ-GRENADES-002-REQ-006` — SteroidPunch path не меняется.
- `JAZZ-GRENADES-002-REQ-007` — technical + wiki + showcase RU/EN: формула skill roll, pre-armor force, мерки тоже могут отлететь.

## Инварианты и ограничения

- MP: только `unit:Random` (как прочие combat rolls); команда knockback синхронна на всех клиентах после одного apply.
- Нет рекурсии через `SteroidPunchGrenade`.
- Урон/concussion уже применены до knockback; fail их не откатывает.
- Dead-from-this-hit: living knockback не запускать.
- Занятые slab’ы — как ваниль (`IsOccupiedExploration`).

## Acceptance criteria

- `JAZZ-GRENADES-002-AC-001` — static: формула, pre-armor `force`, hook; non-blast aoe не вызывают helper.
- `JAZZ-GRENADES-002-AC-002` — runtime: body 100, force 60 → часть хитов даёт отлёт (~1 slab / prone), часть — нет (стат. по серии или debug log roll/value).
- `JAZZ-GRENADES-002-AC-003` — runtime: body 160, force 60 → почти всегда устоять; concussion/trauma всё ещё могут примениться.
- `JAZZ-GRENADES-002-AC-004` — runtime: body 80, force 80 → всегда отлёт (если не skip).
- `JAZZ-GRENADES-002-AC-005` — runtime: prone / unconscious / grit → нет knockback.
- `JAZZ-GRENADES-002-AC-006` — runtime: броня снижает HP damage, но `force` остаётся pre-armor (одинаковый roll input в броне и без, при том же номинальном blast).
- `JAZZ-GRENADES-002-AC-007` — runtime: нет прохода → on-spot prone, не через стену.
- `JAZZ-GRENADES-002-AC-008` — runtime: SteroidPunch без регрессии (в т.ч. kill collateral mock grenade).
- `JAZZ-GRENADES-002-AC-009` — human: wiki + showcase RU/EN = формула.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: новый JAZZ blast reaction; ванильный stub `ExplosionFly` не поднимаем.
- Saves: без новых полей.
- Network: unit RNG + sync command.
- Generated data: нет (кроме optional loc).
- Cross-package: `jazz` only.
- Rollback: снять hook/helper.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: front matter
- Exclusive resources: none

## Решение владельца

- Статус: `approved`
- Кто подтвердил: project-owner
- Дата: 2026-08-08
- Locked: D1–D10 + skill roll `value = Clamp(body − force, 0, 100)` / `roll < value`

## Evidence

- `JAZZ-GRENADES-002-AC-001`: `PASS (static)` — `JazzTryBlastKnockback` / `JazzResolveBlastKnockback` / `Unit:JazzBlastKnocked` in `Systems_Medicine.lua`; hook after concussion in `System_ArmorRating.lua`; `GetAreaAttackResults` stamp wrap; `JazzIsBlastExplosiveHit` gates non-blast.
- `JAZZ-GRENADES-002-AC-002`: `BLOCKED (runtime)` — body 100 / force 60 series
- `JAZZ-GRENADES-002-AC-003`: `BLOCKED (runtime)` — body 160 / force 60
- `JAZZ-GRENADES-002-AC-004`: `BLOCKED (runtime)` — body 80 / force 80 always fly
- `JAZZ-GRENADES-002-AC-005`: `BLOCKED (runtime)` — prone / unconscious / grit skip
- `JAZZ-GRENADES-002-AC-006`: `BLOCKED (runtime)` — pre-armor force with armor
- `JAZZ-GRENADES-002-AC-007`: `BLOCKED (runtime)` — blocked path on-spot
- `JAZZ-GRENADES-002-AC-008`: `BLOCKED (runtime)` — SteroidPunch regression
- `JAZZ-GRENADES-002-AC-009`: `PASS (static)` — technical + wiki + showcase RU/EN updated; human skim pending

## Documentation delta

- `docs/technical/systems/explosives-traps-heavy-weapons.md` — blast knockback section
- `docs/technical/systems/armor-damage-wounds-will.md` — hook note
- `docs/wiki/combat-and-accuracy.md`
- `docs/showcase/ru/combat-and-accuracy.md`
- `docs/showcase/en/combat-and-accuracy.md`
