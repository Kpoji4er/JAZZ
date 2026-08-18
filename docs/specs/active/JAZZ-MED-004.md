---
id: JAZZ-MED-004
status: implemented
owner: project-owner
systems:
  - armor-damage-wounds-will
  - explosives-traps-heavy-weapons
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/Systems_Medicine.lua
  - Code/System_ArmorRating.lua
  - InventoryItem/FragGrenade.lua
  - InventoryItem/HE_Grenade.lua
  - items.lua
  - metadata.lua
  - Russian.csv
  - English.csv
  - docs/specs/active/JAZZ-MED-004.md
  - docs/specs/active/JAZZ-MED-001.md
  - docs/design/medicine.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/technical/systems/explosives-traps-heavy-weapons.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
  - docs/tools/_audit_med004.py
  - docs/tools/_apply_med004_grenade_shot.py
  - docs/tools/README.md
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
related_decisions:
  - none
related_specs:
  - JAZZ-MED-001
  - JAZZ-GRENADES-002
approved_by: project-owner
---

# JAZZ-MED-004: trauma from hit damage + same-zone step-up

## Проблема

`JazzTryRollTraumaFromBodyPart` вешает тир по d100 (Light &lt;55, Medium &lt;12, Heavy &lt;2) и не читает нанесённый урон. Мелкий хит и крупный снайперский хит дают почти один и тот же ролл. Blast в эпицентре применяет несколько `*shot` из `CenterAppliedEffects` плюс отдельный concussion/trauma gate — несколько зональных травм с одного взрыва.

Прогресс травм на глобалке делает **одну** проверку за `NewHour` и ставит следующий таймер от **текущего** `CampaignTime`. Скип суток даёт максимум один шаг (или ни одного, если таймер не был записан). Игроки видят «скипнул 24ч — лёгкая на месте».

MED-001: лёгкая = боль при юзе зоны без zone-специфика; средняя = специфик + боль; тяжёлая = небоеспособный специфик. Нок (`UnitDowned`) по-прежнему гарантирует одну Heavy. BAT уже отсекает `energy < 8`.

## Цели

- Тир травмы с хита считается по урону **этого попадания** в зону (после брони).
- Ниже порога травмы нет.
- Повторный квалифицирующий хит в ту же зону поднимает тир.
- Blast даёт не больше одной зональной травмы по тем же правилам.
- Одинаковые правила для игрока и ИИ.
- Лёгкая сохраняет +1 Pain при юзе зоны (`Analgesia` глушит боль).
- Пропущенные часы на глобалке догоняют проверки травмы (несколько шагов за один скип).

## Non-goals

- Отдельные пулы HP по конечностям.
- Новый satellite progress UI / иконка «лечится» (тултип + CombatLog improve остаются).
- Снимать zone-дебаф у `jazz_healing` или сбрасывать заживление новым хитом.
- Instant hospital clear (MED-002 **deferred / not loaded**).
- Менять Pain-on-hit, bleed, graze, knockback, **гарантированную контузию** (GRENADES-002, в т.ч. flashbang 0 dmg).
- Burn (`Burning` → `TraumaBurnLight`) через пулевой порог.
- BAT (`energy < 8`).

## Модель

Урон хита = HP, прошедшие в `ApplyDamageAndEffects` / `hit.damage`. Graze — без травмы. `MaxHP` = `MaxHitPoints` цели.

Утверждённые пороги: абсолютный пол **20**; тяжёлая с одного хита при уроне **≥ 50%** MaxHP или при нокдауне.

| Условие | Тир |
| --- | --- |
| урон &lt; 20 | нет травмы |
| урон ≥ 20, зона без травмы | Light |
| урон ≥ 20, в зоне уже травма | +1 тир (Light→Medium→Heavy) |
| урон ≥ 50% MaxHP | не ниже Heavy, без промежуточных тиров |
| нокдаун (`UnitDowned`) | одна физическая Heavy, без промежуточных тиров |

Итог хита: `max(накопленный тир, полоса этого хита)`. Кап Heavy. Голова без отдельного d100.

| Тир | Специфик зоны | Боль |
| --- | --- | --- |
| Light | нет | +1 при юзе зоны |
| Medium | да | +2 при юзе |
| Heavy | да, жёсткий | +3; unused +1 / ход |

Blast (`aoeType none`): **Concussion** как GRENADES-002 (в том числе flashbang 0 dmg). Одна зональная травма по полосе урона (`spot_group`, иначе Ribs). `CenterAppliedEffects` Frag/HE не содержат `*shot`.

`JazzApplyDownedHeavyTrauma` — одна Heavy без порога урона и без Light/Medium. BAT без изменений (`energy < 8`). `JazzGetTraumaArmorChanceFactor` на этом пути не используется: броня уже уменьшает `damage`.

Прогресс: `JazzTraumaProgressOnNewHour` крутит проверки, пока `CampaignTime >= next_check_time` (кап итераций). Следующий таймер = **due time + interval**, не «сейчас + interval». Нет таймера → проверка сразу.

## Требования

- `JAZZ-MED-004-REQ-001` — нет травмы, если урон хита &lt; 20, хита нет, или graze.
- `JAZZ-MED-004-REQ-002` — первый хит с уроном ≥ 20: Light, если не сработал порог Heavy от доли MaxHP.
- `JAZZ-MED-004-REQ-002b` — если урон ≥ 50% MaxHP цели: тир не ниже Heavy, минуя Light/Medium если зоны ещё не было.
- `JAZZ-MED-004-REQ-002c` — `UnitDowned` → одна физическая Heavy (`JazzApplyDownedHeavyTrauma`), минуя Light/Medium.
- `JAZZ-MED-004-REQ-003` — при существующей травме зоны и уроне ≥ 20: тир не ниже current + 1, затем max с REQ-002b.
- `JAZZ-MED-004-REQ-004` — blast: максимум одна зональная травма по REQ-001…003; нет второго ролла в `JazzTryApplyExplosionConcussionAndTrauma`, если травма уже с этого хита (`*shot` leftover). Concussion без изменения GRENADES-002.
- `JAZZ-MED-004-REQ-005` — `CenterAppliedEffects` FragGrenade и HE_Grenade без `*shot` rollers.
- `JAZZ-MED-004-REQ-006` — публичные ID `Trauma*` и нок-Heavy без изменений; Head d100 из MED-001 REQ-010 superseded правилом урона.
- `JAZZ-MED-004-REQ-007` — Light сохраняет `JazzTraumaPainOnZoneUse` +1; `Analgesia` глушит Pain; у Light нет zone-специфика.
- `JAZZ-MED-004-REQ-008` — те же полосы для игрока и ИИ.
- `JAZZ-MED-004-REQ-009` — technical + wiki + showcase RU/EN описывают пол 20, накопление тира, Heavy от доли MaxHP и одну blast-травму.
- `JAZZ-MED-004-REQ-010` — satellite catch-up: все due-проверки травмы за пропущенное время; таймер от due, не от конца скипа.

## Инварианты и ограничения

- Companions `*shot` остаются входом для огнестрела; OnAdded читает урон хита (`jazz_pending_trauma_hit`).
- Save schema не расширяется.
- Новые `_G` имена только top-level.

## Acceptance criteria

- `JAZZ-MED-004-AC-001` — static: пол 20; нет `thr_light = 55` в `JazzTryRollTraumaFromBodyPart`; Heavy при уроне ≥ 50% MaxHP.
- `JAZZ-MED-004-AC-002` — static: same-zone +1 тир, затем max с порогом доли MaxHP.
- `JAZZ-MED-004-AC-003` — static: blast ≤ 1 trauma; Frag/HE center без тройки `*shot`.
- `JAZZ-MED-004-AC-004` — static: Light zone-use Pain +1 сохранён.
- `JAZZ-MED-004-AC-005` — docs: wiki/showcase RU/EN + technical medicine/explosives.
- `JAZZ-MED-004-AC-006` — runtime: урон 5–7 (и любой &lt; 20) без зональной травмы; хит ≥ 20 в пустую зону → Light; второй в ту же зону → Medium; хит ≥ 50% MaxHP или нокдаун → Heavy без Light/Medium.
- `JAZZ-MED-004-AC-007` — static: `JazzTraumaProgressOnNewHour` ловит несколько due-проверок; `JazzInitTraumaProgressTimer` принимает due time.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ владеет `*shot` OnAdded, `ApplyDamageAndEffects`, blast package.
- Saves: существующие травмы остаются; новые хиты — новые правила. Старые таймеры догоняются при следующем `NewHour`.
- Network: тир с пули детерминирован уроном.
- Generated data: да (`CenterAppliedEffects` Frag/HE).
- Cross-package: нет.
- Rollback: revert коммита `jazz`.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель / Reviewer: project-owner.
- Declared write set / exclusive resources: frontmatter.

## Решение владельца

- Статус: `approved`.
- Пол **20**, Heavy при ≥ **50%** MaxHP. BAT `energy < 8` не трогаем. Concussion flashbang не режем порогом 20. Catch-up заживления при скипе — в этом же change set.
- Кто подтвердил: project-owner (chat 2026-08-13: «пороги надо выше»; «делай и пушься»).
- Дата: 2026-08-13.

## Evidence

- `JAZZ-MED-004-AC-001`: `PASS` — static `_audit_med004.py` (floor 20, no `thr_light`, Heavy 50% MaxHP).
- `JAZZ-MED-004-AC-002`: `PASS` — static: `JazzWantedTraumaTierFromDamage` same-zone +1 then max with MaxHP band.
- `JAZZ-MED-004-AC-003`: `PASS` — static: blast one zone; Frag/HE `CenterAppliedEffects` without `*shot`.
- `JAZZ-MED-004-AC-004`: `PASS` — static: `JazzTraumaPainOnZoneUse` unchanged.
- `JAZZ-MED-004-AC-005`: `PASS` — technical + wiki + showcase RU/EN + design medicine.
- `JAZZ-MED-004-AC-006`: `BLOCKED` — runtime/human (5–7 no trauma; ≥20 Light; second hit Medium; ≥50% or downed Heavy).
- `JAZZ-MED-004-AC-007`: `PASS` — static: NewHour `while` catch-up; timer from due time.

## Documentation delta

`armor-damage-wounds-will.md`, `explosives-traps-heavy-weapons.md`, wiki/showcase `combat-and-accuracy` RU/EN, `docs/design/medicine.md`; MED-001 Head d100 — superseded.
