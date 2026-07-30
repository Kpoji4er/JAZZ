---
id: JAZZ-COMBAT-002
status: draft
owner: project-owner
systems:
  - combat-cth-actions
  - armor-damage-wounds-will
  - weapons-ammo-components
  - visibility-weather-appearance
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/ExecFirearmAttacks.lua
  - jazz/Code/CrossHairUI.lua
  - jazz/Code/MeleeWeapon.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Localization/Russian.csv
  - jazz/Localization/English.csv
  - jazz/docs/specs/active/JAZZ-COMBAT-002.md
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/technical/systems/visibility-weather-appearance.md
  - jazz/docs/technical/weapons/accuracy-model.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
related_decisions:
  - none
approved_by: pending
---

# JAZZ-COMBAT-002: grazing только от CTH-кривой и укрытия

## Проблема

Сейчас grazing приходит из нескольких «магических» источников, часть из которых не видна в Lua:

1. **Near-miss band** — плоский порог `+3` / `+6` point-blank над `shot_cth`.
2. **Fog / DustStorm** — `IsConcealedFrom` / `IsObscuredFrom` + `FogGrazeChance` / `DustStormGrazeChance`.
3. **Дым / газ на LoF** — C++ LoF помечает `hit.grazing` / `target_grazing_hit` при проходе через `SmokeObj` (`cfSmokeObj`); в Lua только читается результат. Официальные тексты гранат обещают graze через газ.
4. **Cover / Taking Cover (`Protected`)** — осмысленный тактический источник, но завязан на отдельный `base_chance`, а не на фактический бонус укрытия в CTH.

Итог для игрока: снайпер с высоким CTH всё равно может «поцарапать» из-за погоды/дыма/полосы промаха, а graze от укрытия плохо читается относительно CTH-штрафа укрытия.

## Цели

- Убрать все grazing-источники кроме двух явных.
- **Miss→graze:** шанс превратить промах в grazing растёт **обратно** `shot_cth`, **нелинейно**, **cap 50%**.
- **Cover→graze:** шанс превратить попадание в grazing **пропорционален бонусу укрытия** (тому же cover CTH modifier), **вплоть до 100%** при полном укрытии.
- Дым/газ **всегда** игнорируются для graze (`ignore_smoke` + снятие `target_grazing_hit` у throws/ножей).
- Сохранить эффект grazing: `GrazingHitDamage`, без crit, без hit-level status effects.
- Синхронизировать technical / wiki / showcase и тексты smoke/gas.

## Non-goals

- Менять формулу CTH, recoil, BDR или `GrazingHitDamage` (кроме явного follow-up).
- Менять AI BunkerDown flow (`JAZZ-AI-002`).
- Переписывать C++ LoF.
- Баланс перков/компонентов вне `IgnoreGrazingHitsWhenFullyAimed` (см. открытые решения).

## Решения владельца (зафиксировано 2026-07-30)

| # | Решение | Статус |
| --- | --- | --- |
| Cover | Graze **пропорционален бонусу укрытия** (cover CTH modifier), потолок 100% | принято |
| Дым/газ | **Всегда** `ignore_smoke` для graze-path; ножи/throws тоже снять `target_grazing_hit` | принято |
| Ножи | Smoke-graze снять так же, как у Firearm | принято |
| Кривая miss→graze | Цель: при **CTH 20%** graze ≈ **30–40%**; точная степень ещё на столе | **открыто** (рабочий кандидат ниже) |
| Thermal | `IgnoreGrazingHitsWhenFullyAimed` — scope не зафиксирован | **открыто** |

## Предлагаемая модель

### A. Miss→graze

Условие: валидный выстрел (`shot_cth > 0`), roll промаха (`roll > shot_cth`).

**Рабочий кандидат** (уже попадает в цель «20% CTH → ~32% graze»):

```text
miss_graze_chance = min(50, floor( 50 * ((100 - shot_cth) / 100) ^ 2 ))
```

Опорные точки:

| shot_cth | ^2 (кандидат) | ^1.5 (мягче) | linear `0.5×(100−cth)` |
| ---: | ---: | ---: | ---: |
| 100 | 0 | 0 | 0 |
| 90 | 0 | 1 | 5 |
| 80 | 2 | 4 | 10 |
| 70 | 4 | 8 | 15 |
| 50 | 12 | 17 | 25 |
| 30 | 24 | 29 | 35 |
| **20** | **32** | **35** | **40** |
| 10 | 40 | 42 | 45 |

Заметка для тюнинга: `^2` уже даёт **32%** на CTH 20 (внутри 30–40). Если «бесит» mid-range (CTH 50–70) — оставить `^2` или жёстче; если на низком CTH мало царапин — смягчить к `^1.5` / linear. Cap **50%** сохраняется.

Плоский `+3/+6` и `GetShotGrazeTheshold` для этого path **не используются**.

### B. Cover → graze (пропорционально бонусу укрытия)

Берётся тот же cover CTH modifier, что даёт штраф попадания за укрытие (геометрия + `InterpolateCoverEffect(coverage, Cover, ExposedCover)`, включая dust-storm cover deepening, если оно уже вошло в modifier).

```text
cover_cth_value = InterpolateCoverEffect(coverage, full_cover, exposed_cover)  -- обычно отрицательный
cover_full      = full_cover   -- e.g. -20 (или усиленный dust)

cover_graze_chance = Clamp( MulDivRound( -cover_cth_value, 100, -cover_full ), 0, 100 )
```

Следствия:

- полное укрытие → **100%** graze;
- половина бонуса → **~50%** graze;
- только «exposed cover» (−5 при full −20) → **25%** graze;
- нет cover CTH modifier → **0%** cover-graze.

`Protected` / BunkerDown **не** единственный gate: graze следует за фактическим бонусом укрытия. `Protected` по-прежнему влияет на UI InCover / AP / AI, но не подменяет шкалу отдельным `base_chance`, если cover modifier уже посчитан.

Ветки Fog / DustStorm **env graze** (`FogGrazeChance` / `DustStormGrazeChance`) **удаляются**. Dust может косвенно поднять cover-graze только если усиливает cover CTH penalty — это следствие «пропорционально бонусу», не отдельный magic graze.

### C. Дым / газ / ножи

- На Firearm (и прочих ranged LoF-атаках): **всегда** `attack_args.ignore_smoke = true` (не только thermal full-aim).
- На thrown knives / ranged melee path: после `GetLoFData` принудительно `target_grazing_hit = false` (и не ставить `hit.grazing` из дыма).
- Тексты smoke/teargas/toxicgas больше не обещают grazing через газ.

Проверка: `ignore_smoke` не должен отключать smoke sight/−70 / CTH visibility side-effects, которые живут вне LoF-graze. Если runtime покажет иное — fallback: strip `target_grazing_hit` / pre-set `hit.grazing` при сохранении обычного smoke collision semantics.

### D. Эффект grazing (без изменений)

- `hit.critical = nil`
- `hit.effects = {}`
- `damage = Max(1, MulDivRound(damage, const.Combat.GrazingHitDamage, 100))` (JAZZ **40%**)
- floating text: cover → `cover`; miss-graze → обычный Grazed (без Fog/Dust labels)

## Требования

- `JAZZ-COMBAT-002-REQ-001` — grazing только из (A) miss→graze (cap 50%) и (B) cover-graze пропорционально cover CTH bonus (cap 100%).
- `JAZZ-COMBAT-002-REQ-002` — fog/dust **env** graze и smoke/gas LoF-graze отсутствуют; `ignore_smoke` всегда; throws/knives без `target_grazing_hit` от дыма.
- `JAZZ-COMBAT-002-REQ-003` — miss→graze: нелинейная кривая от `shot_cth`; плоский `+3/+6` удалён; при CTH 20 итоговый шанс в диапазоне **30–40** после выбора формулы владельцем.
- `JAZZ-COMBAT-002-REQ-004` — cover-graze = нормализованный `|cover_cth_value| / |cover_full|` × 100, Clamp 0..100.
- `JAZZ-COMBAT-002-REQ-005` — эффект grazing сохраняет `GrazingHitDamage`.
- `JAZZ-COMBAT-002-REQ-006` — player-facing тексты smoke/gas и combat docs без magic graze через газ/погоду.
- `JAZZ-COMBAT-002-REQ-007` — miss-graze roll sync-safe / deterministic.

## Инварианты и ограничения

- Публичные ID `Protected`, `GrazingHitDamage` не переименовываются без отдельного spec.
- Prediction не мутирует status effects цели.
- `JAZZ-AI-002` BunkerDown не ломается.
- До approve / выбора формулы **не** менять runtime (кроме docs/spec).

## Acceptance criteria

- `JAZZ-COMBAT-002-AC-001` — static: нет Fog/DustStorm env graze; нет плоского threshold 3/6; `ignore_smoke` выставляется не только thermal.
- `JAZZ-COMBAT-002-AC-002` — static/runtime: таблица miss_graze_chance совпадает с утверждённой формулой (±1 floor); при CTH 20 ∈ [30, 40].
- `JAZZ-COMBAT-002-AC-003` — runtime: выстрел/бросок ножа через smoke/gas не форсирует grazing на открытой цели.
- `JAZZ-COMBAT-002-AC-004` — runtime: full cover → cover-graze 100%; half cover bonus → ~50%; no cover modifier → 0% cover-graze.
- `JAZZ-COMBAT-002-AC-005` — runtime: CTH ≥ 90 → miss→graze ≤ 1% по `^2` (или согласованной формуле); CTH 20 → 30–40%.
- `JAZZ-COMBAT-002-AC-006` — docs/wiki/showcase + RU/EN smoke/gas; auditor needs RU/EN = 0.
- `JAZZ-COMBAT-002-AC-007` — human: снайпер на высоком CTH не бесит царапинами; укрытие читается через силу cover-бонуса.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: override graze path + always `ignore_smoke`; C++ LoF не патчится.
- Saves: новых fields нет.
- Network/determinism: новый miss-graze roll sync-safe.
- Generated data: ConstDef fog/dust graze → 0/remove; texts; возможен отказ от `Protected.base_chance` как graze source; editor round-trip.
- Rollback: один change set.

## План и ownership

- Пакет-владелец: `jazz`
- Declared write set: см. frontmatter (добавлен `MeleeWeapon.lua` под ножи)
- Exclusive resources: `items.lua`, `metadata.lua`

## Открытые решения (блокируют approve)

1. **Точная кривая miss→graze:** оставить `^2` (32% @ CTH20), смягчить `^1.5` (36%), или linear half (40%)?
2. **Thermal / `IgnoreGrazingHitsWhenFullyAimed`:** только cover-graze, или ещё miss→graze?

## Решение владельца

- Статус: `draft` (частично решено; формула и thermal ещё открыты)
- Кто подтвердил: project-owner (частично, 2026-07-30)
- Дата: 2026-07-30

## Evidence

- `JAZZ-COMBAT-002-AC-001` … `AC-007`: `BLOCKED` — draft; runtime не начат.

## Documentation delta

После реализации: `combat-cth-actions.md`, `visibility-weather-appearance.md`, accuracy-model (если нужно), wiki + showcase RU/EN, тексты smoke/gas.
