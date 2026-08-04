---
id: JAZZ-WEAPONS-007
status: implemented
owner: project-owner
systems:
  - combat-cth-actions
  - weapons-ammo-components
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/VanillaDesyncFixes.lua
  - jazz/Code/AccuracyRangeCTH.lua
  - jazz/docs/specs/active/JAZZ-WEAPONS-007.md
  - jazz/docs/technical/weapons/accuracy-model.md
  - jazz/docs/technical/weapons/combat-actions.md
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/wiki/combat-actions.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-actions.md
  - jazz/docs/showcase/en/combat-actions.md
exclusive_resources:
  - none
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-003
  - JAZZ-WEAPONS-006
  - JAZZ-CTH-001
  - JAZZ-COMBAT-002
approved_by: project-owner
---

# JAZZ-WEAPONS-007: нарастающий climb промахов очереди (визуал + LoF miss)

## Проблема

1. Отдача очереди (JAZZ-WEAPONS-003) корректно снижает **CTH** последующих пуль через `effective_recoil` → `retention`, но **визуальное / LoF-распределение** пуль очереди почти не связано с этим профилем.
2. `GetAttackResults` (`System_OR_Weapons.lua`) после hit/miss rolls вызывает `CalcShotVectors` с **зашитым** конусом (`20*guic`, `guim`) и сортирует `precalc_shots` по `idx` → fire-order **отвязан** от CTH-индекса пули; ось разлёта — **случайный** луч, не увод ствола.
3. `Firearm:GetMaxDispersion` масштабирует fallback `CalcMissVectors` через `Recoil * 2`, но основной burst-path это почти не использует → высокий/низкий Recoil слабо читается на трассерах.
4. Игрок не видит, что контроль (Str/Mark, стойка, bipod, compensator, AutoWeapons) «воюет» с уводом: картинка и collateral промахов не отражают тот же расчёт, что UI «Отдача».

## Цели

1. Для **нарезных очередей** (не дробовый пакет) каждый следующий выстрел после protected-окон получает **плавно нарастающее** отклонение промаха (climb вверх + лёгкий боковой jitter).
2. Амплитуда и скорость роста читают **тот же** `JAZZ_CTHGetRecoilProfile` / `effective_recoil` / `shots_before_recoil`, что CTH — контроль отдачи одновременно держит % и сжимает climb.
3. **Hit-roll и размещение успешных попаданий** остаются как сейчас: пуля, прошедшая CTH, бьёт в accurate hit-vector цели; climb **не** смещает hit и **не** снижает CTH повторно.
4. Исключить **дробовые пакеты** (`pellet_pack`: `Buckshot` / `DoubleBarrel` / `CancelShotCone` / `BuckshotBurst`) — у них остаётся пакетный конус / choke (JAZZ-WEAPONS-006), без queue-climb.
5. Синхронизировать fire-order с индексом пули CTH (без sort, ломающего соответствие «i-я пуля retention ↔ i-й трассер»).
6. Docs: technical + wiki + showcase RU/EN (player-facing читаемость очереди / промахов).

## Non-goals

- Смена формулы `retention` / `P_bullet(i)` / floor 2% (JAZZ-WEAPONS-003 остаётся).
- Второй штраф CTH от величины miss offset (запрещено инвариантом WEAPONS-003 / accuracy-model).
- FPS-симуляция импульса/камеры; достаточно читаемого climb в плоскости цели.
- Смещение **успешных** hit-точек climb’ом (намеренный «размазанный hit» — out of scope).
- Изменение pellet count, choke, `BuckshotConeAngle`, slug path.
- Ребаланс authored `Recoil` / Mass / RPM (числа WEAPONS-003).
- Новые перки, UI-цифры retention, debug-only overlays (опционально later).
- Generated data / `items.lua` / CSV companion rewrite.

## Контракт climb

Источник профиля — уже существующий `JAZZ_CTHGetRecoilProfile(weapon, attacker, stance, action, attack_args)`:

```text
er = effective_recoil          # float/number из профиля
prot = shots_before_recoil     # в т.ч. action + bipod prone bonus
k(i) = max(0, i - 1 - prot)    # i = 1-based shot index в очереди
```

Отклонение **только для miss** (и для true-miss ветки; graze/inaccurate-on-target остаётся near-target как сейчас, без полного climb в небо):

```text
# плоскость у цели: та же семья max_offset, что CalcShotVectors
max_offset_ref = Max(guim, MulDivRound(guim, dist, 8 * guim))

# линейный рост; er=50, k=8 → полный max_offset_ref (калибровочный якорь)
offset_len(i) = Min(max_offset_ref, MulDivRound(max_offset_ref, k(i) * Round(er), 400))

climb_dir = unit vector «вверх» в плоскости, ортогональной LoF
            (предпочтительно world +Z, спроецированный; fallback — стабильная ось ⊥ LoF)
lateral   = малый jitter ⊥ climb_dir, |lateral| ≤ MulDivRound(offset_len(i), 25, 100)
            (детерминированный attacker Random / тот же sync braid, что miss vectors)

miss_target_pos(i) = aim_pos + climb_dir * offset_len(i) + lateral_vec
```

Константа **400** в знаменателе — калибровочный якорь spec (er×k); менять только ревизией spec после playtest, не скрытым magic в другом файле без delta.

Контроль отдачи «воюет» с climb так же, как с CTH: ниже `er` (Str/Mark, stance, support, perk, action, class, components→Recoil) → медленнее рост `offset_len` и выше `retention`.

### Что не меняется

| Слой | Поведение |
| --- | --- |
| Hit/miss roll | `JAZZ_CTHGetBulletChance` + attack_roll как сейчас |
| Успешный hit | accurate / part hit vectors как сейчас |
| Miss LoF | идёт в `miss_target_pos(i)` (новое направление) |
| Pellet pack | без climb; текущий packet / scatter path |
| Prediction UI | не обязан симулировать miss cone (как сейчас: prediction не гоняет synced miss RNG) |

### Fire order

После назначения векторов **не** сортировать `precalc_shots` по `dispersion`/`idx` так, чтобы i-я запись переставала соответствовать i-й пуле CTH. Хронологический индекс пули = индекс анимации/LoF для этой атаки.

## Требования

- `JAZZ-WEAPONS-007-REQ-001` — для non-`pellet_pack` multishot атак miss-точки очереди используют нарастающий climb по контракту выше, с `er`/`prot` из `attack_results.recoil_profile` (тот же профиль, что для `shot_cth`).
- `JAZZ-WEAPONS-007-REQ-002` — успешный hit не смещается climb’ом; CTH/retention/floor не меняются этим spec.
- `JAZZ-WEAPONS-007-REQ-003` — `pellet_pack` actions (`Buckshot`, `DoubleBarrel`, `CancelShotCone`, `BuckshotBurst`) **исключены**: без queue-climb и без привязки pellet miss к `effective_recoil` retention-модели.
- `JAZZ-WEAPONS-007-REQ-004` — fire-order / `precalc_shots[i]` соответствует CTH-индексу пули `i` (нет decoupling sort hit-outcome ↔ visual idx).
- `JAZZ-WEAPONS-007-REQ-005` — при `k(i)=0` (первая пуля и protected window) miss без принудительного climb-offset (допустим только текущий минимальный miss-clearance / fallback, не ступень `er`).
- `JAZZ-WEAPONS-007-REQ-006` — technical (`accuracy-model`, combat-cth/actions) + wiki + showcase RU/EN описывают: промахи очереди уводятся climb’ом; контроль сжимает и CTH-decay, и увод; дробовый пакет исключён.

## Инварианты и ограничения

- Одна application отдачи на CTH пули; miss vector / climb **не** второй penalty к шансу (JAZZ-WEAPONS-003).
- Determinism: те же sync random / `NetUpdateHash` точки, что burst miss path; без UI-prediction desync.
- Не трогать `items.lua` / authored Recoil numbers в этом change set.
- Graze (JAZZ-COMBAT-002): roll/chance без изменений; размещение graze остаётся near-target inaccurate, не полный climb.
- SingleShot / одна пуля: поведение miss как fallback path; climb-ступени нет (`k=0`).
- DualShot / Abakan protected / bipod `ShotsBeforeRecoilProne` уважают `shots_before_recoil`.

## Acceptance criteria

- `JAZZ-WEAPONS-007-AC-001` — static: non-pellet multishot miss path читает `recoil_profile.effective_recoil` и `shots_before_recoil`; формула `offset_len` с якорем `/400` присутствует в Code (или одном helper в `AccuracyRangeCTH.lua`).
- `JAZZ-WEAPONS-007-AC-002` — static: ветка `pellet_pack` не вызывает queue-climb helper / не масштабирует pellet targets через `effective_recoil` climb.
- `JAZZ-WEAPONS-007-AC-003` — static: нет `table.sort(precalc_shots, … dispersion …)` (или эквивалента), нарушающего соответствие shot index ↔ CTH index для non-pellet очередей.
- `JAZZ-WEAPONS-007-AC-004` — runtime/human: Burst/Auto на высоком Recoil без опоры — поздние **промахи** читаемо уходят вверх относительно ранних; hits по силуэту цели при тех же условиях всё ещё возможны по CTH.
- `JAZZ-WEAPONS-007-AC-005` — runtime/human: тот же ствол prone+bipod / сильный контроль — climb хвоста заметно короче при сопоставимой длине очереди.
- `JAZZ-WEAPONS-007-AC-006` — runtime/human: Buckshot / DoubleBarrel — прежний пакетный разлёт, без «очереди вверх» по номеру дробины.
- `JAZZ-WEAPONS-007-AC-007` — docs: technical + wiki + showcase RU/EN обновлены в том же change set, что runtime.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: override `GetAttackResults` / `CalcShotVectors` (или post-assign) в `jazz`; vanilla burst sort/random-axis заменяется для non-pellet.
- Saves: нет новых полей; поведение miss LoF меняется → возможны другие collateral в старых сейвах (приемлемо).
- Network/determinism: обязателен тот же random braid; hash inputs при смене порядка назначения — обновить `NetUpdateHash` если меняется последовательность Random.
- Generated data: false.
- Cross-package: none.
- Rollback/recovery: revert Code + docs; CTH path не затрагивается.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent / project-owner
- Reviewer: project-owner
- Declared write set: см. frontmatter `write_set`
- Exclusive resources: `none` (нет `items.lua`)

## Решение владельца

- Статус: `implemented` (runtime/human AC-004..006 ещё на playtest)
- Кто подтвердил: project-owner
- Дата: 2026-08-04
- Примечание: approve implicit («делай») после согласования контракта climb.

## Evidence

- `JAZZ-WEAPONS-007-AC-001`: `PASS` — static: `JAZZ_CTH_RECOIL_CLIMB_SCALE = 400`, `JAZZ_CTHGetRecoilClimbOffsetLen` / `JAZZ_CTHBuildRecoilClimbMissPos` in `AccuracyRangeCTH.lua`; wired from `GetAttackResults` with `effective_recoil` / `shots_before_recoil`
- `JAZZ-WEAPONS-007-AC-002`: `PASS` — static: climb gated `if not pellet_pack …`; pellet_pack keeps dispersion sort only
- `JAZZ-WEAPONS-007-AC-003`: `PASS` — static: sole `table.sort(precalc_shots)` under `if pellet_pack then`
- `JAZZ-WEAPONS-007-AC-004`: `BLOCKED` — human/runtime playtest (high Recoil Burst/Auto climb readability)
- `JAZZ-WEAPONS-007-AC-005`: `BLOCKED` — human/runtime playtest (prone+bipod shorter climb)
- `JAZZ-WEAPONS-007-AC-006`: `BLOCKED` — human/runtime playtest (Buckshot packet unchanged)
- `JAZZ-WEAPONS-007-AC-007`: `PASS` — docs: accuracy-model, combat-cth-actions, combat-actions technical + wiki + showcase RU/EN

## Documentation delta

- `docs/technical/weapons/accuracy-model.md` — climb miss subsection
- `docs/technical/systems/combat-cth-actions.md` — climb note on GetAttackResults
- `docs/technical/weapons/combat-actions.md` — Burst/Auto/Buckshot bullets
- `docs/wiki/combat-and-accuracy.md`, `docs/wiki/combat-actions.md`
- `docs/showcase/ru|en/combat-and-accuracy.md`, `docs/showcase/ru|en/combat-actions.md`

Note: `VanillaDesyncFixes.lua` (`CalcShotVectors`) unchanged — climb applied post-assign in `GetAttackResults`; declared write set path unused.
