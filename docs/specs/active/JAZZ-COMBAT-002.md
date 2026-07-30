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
4. **Cover / Taking Cover (`Protected`)** — единственный осмысленный тактический источник, но шанс не дотягивает до «бункер = почти всегда царапина».

Итог для игрока: снайпер с высоким CTH всё равно может «поцарапать» из-за погоды/дыма/полосы промаха, а укрытие не даёт предсказуемого потолка защиты.

## Цели

- Убрать все grazing-источники кроме двух явных.
- **Miss→graze:** шанс превратить промах в grazing растёт **обратно** `shot_cth`, **нелинейно**, **cap 50%** — высокий CTH почти не царапает.
- **Cover / BunkerDown (`Protected`):** шанс превратить попадание в grazing растёт с coverage **вплоть до 100%** при полном укрытии со стороны атаки.
- Сохранить текущий эффект grazing: урезанный урон (`GrazingHitDamage`), без crit, без hit-level status effects.
- Синхронизировать technical / wiki / showcase и тексты smoke/gas, чтобы больше не обещали magically graze.

## Non-goals

- Менять формулу CTH, recoil, BDR или `GrazingHitDamage` (кроме явного follow-up).
- Менять AI BunkerDown flow (`JAZZ-AI-002`) — только потребление `Protected` / cover geometry.
- Переписывать C++ LoF; достаточно нейтрализовать smoke-graze на Lua-границе.
- Менять melee/AOE урон вне огнестрельного ranged pipeline, кроме явного снятия smoke `target_grazing_hit` у throws если он остаётся.
- Баланс отдельных перков/компонентов вне `IgnoreGrazingHitsWhenFullyAimed` (см. открытые решения).

## Предлагаемая модель (кандидат на approve)

### A. Miss→graze (единственный non-cover источник)

Условие: валидный выстрел (`shot_cth > 0`), roll промаха (`roll > shot_cth`).

```text
miss_graze_chance = min(50, floor( 50 * ((100 - shot_cth) / 100) ^ 2 ))
```

Отдельный roll `0..99` (или эквивалент deterministic RNG атаки): при успехе — `sfAllowGrazing` / `hit.grazing` + `grazed_miss` как сейчас.

Опорные точки (^2, cap 50):

| shot_cth | miss_graze_chance |
| ---: | ---: |
| 100 | 0 |
| 90 | 0 |
| 80 | 2 |
| 70 | 4 |
| 50 | 12 |
| 30 | 24 |
| 10 | 40 |
| 0 | n/a (выстрел невалиден) |

Плоский порог `+3/+6` и `GetShotGrazeTheshold` / `OnCalcShotGrazeThreshold` для этого path **не используются** (реакции либо удалить из path, либо оставить no-op до отдельного follow-up).

### B. Cover / BunkerDown → graze

Условие (как сейчас по смыслу): цель `Unit`, aware, не `Exposed`, имеет `Protected` (Taking Cover / BunkerDown), атака не melee/aoe, cover со стороны `attack_pos`.

```text
cover_graze_chance = InterpolateCoverEffect(coverage, 100, 0)
```

То есть при полном укрытии со стороны атаки — **100%** grazing hit. Частичное укрытие — пропорционально coverage. Без `Protected` cover **не** даёт graze (только BunkerDown/Take Cover), если владелец не решит иначе.

Ветки Fog / DustStorm / env graze **удаляются** из `PrecalcDamageAndStatusEffects`.

### C. Нейтрализация дыма/газа (C++ LoF)

На любой ranged атаке, где сейчас возможен engine smoke-graze:

- выставлять `attack_args.ignore_smoke = true` **только для цели «не превращать LoF в graze»**, **если** это не ломает smoke LOS/detection (проверить runtime); **или**
- после `GetLoFData` снимать `lof.target_grazing_hit` и предустановленный `hit.grazing` у unit-хитов, пришедших из smoke, до `BulletCalcDamage` / Precalc.

Предпочтительный путь выбрать в approve после static+runtime проверки `ignore_smoke` (не должен обходить штраф видимости/CTH дыма, если тот живёт отдельно от LoF-graze).

Тексты smoke/teargas/toxicgas и связанные mod-only строки больше не обещают «атаки через газ становятся grazing».

### D. Эффект grazing (без изменений)

- `hit.critical = nil`
- `hit.effects = {}`
- `damage = Max(1, MulDivRound(damage, const.Combat.GrazingHitDamage, 100))` (сейчас JAZZ **40%**)
- floating text / UI: cover → reason `cover`; miss-graze → без fog/dust labels (обычный Grazed)

## Требования

- `JAZZ-COMBAT-002-REQ-001` — grazing возникает только из (A) miss→graze по формуле от `shot_cth` с cap **50%** и (B) cover/`Protected` graze с потолком **100%**.
- `JAZZ-COMBAT-002-REQ-002` — fog, dust storm и дым/газ **не** добавляют grazing (ни Lua env-веткой, ни через C++ LoF `target_grazing_hit` / pre-set `hit.grazing`).
- `JAZZ-COMBAT-002-REQ-003` — miss→graze использует нелинейную кривую от `shot_cth` (кандидат: квадрат, см. таблицу); плоский `+3/+6` threshold удалён.
- `JAZZ-COMBAT-002-REQ-004` — при `Protected` + full cover со стороны атаки `cover_graze_chance = 100`; при меньшем coverage — монотонно меньше через `InterpolateCoverEffect`.
- `JAZZ-COMBAT-002-REQ-005` — эффект grazing (урон/crit/effects) сохраняет текущий JAZZ контракт `GrazingHitDamage`.
- `JAZZ-COMBAT-002-REQ-006` — player-facing тексты smoke/gas и combat docs больше не утверждают magically graze через газ/погоду.
- `JAZZ-COMBAT-002-REQ-007` — deterministic RNG / NetUpdateHash для нового miss-graze roll согласован с multiplayer (тот же stream, что shot rolls, либо явный documented stream).

## Инварианты и ограничения

- Публичные ID `Protected`, `GrazingHitDamage` не переименовываются без отдельного spec.
- Prediction не мутирует status effects цели; UI cover-graze prediction остаётся честной (как сейчас при `chance ~= 0`).
- `JAZZ-AI-002` BunkerDown по-прежнему выдаёт `Protected`; меняется только graze-математика потребления.
- Не активировать dormant код; не трогать sibling-пакеты.
- До approve **не** менять runtime.

## Acceptance criteria

- `JAZZ-COMBAT-002-AC-001` — static: в `PrecalcDamageAndStatusEffects` нет Fog/DustStorm graze-веток; нет использования плоского `graze_threshold` 3/6 для miss→graze.
- `JAZZ-COMBAT-002-AC-002` — static/runtime: таблица miss_graze_chance для CTH 100/80/50/30/10 совпадает с утверждённой формулой (±1 из-за floor).
- `JAZZ-COMBAT-002-AC-003` — runtime: выстрел через smoke/teargas/toxicgas при открытой цели **без** `Protected` не форсирует grazing (при том же CTH/roll, что без дыма, modulo допустимый CTH/LOS side-effect дыма).
- `JAZZ-COMBAT-002-AC-004` — runtime: цель с `Protected` + full cover со стороны атаки получает grazing на hit с шансом 100% (prediction и бой).
- `JAZZ-COMBAT-002-AC-005` — runtime: при `shot_cth ≥ 90` miss→graze практически не проявляется (≤1% по формуле); при низком CTH (≈30) miss→graze заметно выше, но ≤50%.
- `JAZZ-COMBAT-002-AC-006` — docs/wiki/showcase + RU/EN строки smoke/gas обновлены; auditor `needs Russian=0` / `needs English=0` для затронутых ID.
- `JAZZ-COMBAT-002-AC-007` — human playtest: снайпер на высоком CTH не «бесит царапинами»; бункер в полном укрытии стабильно режет урон до graze.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: override graze path в `System_OR_Weapons.lua` / attack args; C++ LoF не патчится — только нейтрализация флагов/`ignore_smoke`.
- Saves: новых persistent fields нет.
- Network/determinism: новый miss-graze roll должен быть sync-safe.
- Generated data: возможны ConstDef (`FogGrazeChance`/`DustStormGrazeChance` deprecate или value 0), `Protected.base_chance` → 100, правки texts; editor round-trip.
- Cross-package: нет.
- Rollback: один change set runtime + docs + loc.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent / project-owner
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: `items.lua`, `metadata.lua`

## Открытые решения владельца (блокируют approve)

1. **Кривая miss→graze:** принять кандидат `50 × ((100−cth)/100)^2`, или другой показатель (`^2.5` / `^3`), или иную яявную формулу.
2. **Cover без `Protected`:** graze только после BunkerDown/Take Cover, или любая cover geometry тоже?
3. **Thermal / `IgnoreGrazingHitsWhenFullyAimed`:** игнорировать только cover-graze, или также miss→graze?
4. **Способ выключить smoke-graze:** всегда `ignore_smoke` vs post-LoF strip флагов (после runtime проверки side-effects).
5. **Melee thrown knives:** снимать `target_grazing_hit` от дыма так же, как у Firearm?

## Решение владельца

- Статус: `draft`
- Кто подтвердил: pending
- Дата: pending

## Evidence

- `JAZZ-COMBAT-002-AC-001` … `AC-007`: `BLOCKED` — spec draft; runtime не начат.

## Documentation delta

После реализации обновить:

- `docs/technical/systems/combat-cth-actions.md` — источники grazing;
- `docs/technical/systems/visibility-weather-appearance.md` — дым больше не graze;
- `docs/technical/weapons/accuracy-model.md` — если описывает graze/cover;
- `docs/wiki/combat-and-accuracy.md` + showcase RU/EN — player-facing;
- тексты smoke/gas в localization / InventoryItem hints.
