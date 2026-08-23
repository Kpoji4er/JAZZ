---
id: JAZZ-WEAPONS-013
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
  - jazz/Code/AccuracyRangeCTH.lua
  - jazz/scripts/test-shooting-model.ps1
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/technical/weapons/accuracy-model.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/specs/active/JAZZ-WEAPONS-013.md
exclusive_resources:
  - none
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-012
approved_by: project-owner
---

# JAZZ-WEAPONS-013: пулемёт — короткий спад после BDR

## Проблема

`WeaponRange` лёгких и тяжёлых пулемётов 40–62 клетки растягивает пост-BDR кривую. На типичной «дальней» улице (20–24 клетки) range factor остаётся ~88–95% (ПКМ на 24 ≈ 94%, как у СВД). Вместе с очередью и опорой это даёт снайперское выкашивание. Hipfire уже режет JAZZ-WEAPONS-012; жалоба про дальнюю точность **с упора**. Обрезка плато до 75% BDR бьёт T1 (MAC / ДП-27) сильнее, чем поздний ПКМ.

## Цели

- После эффективной зоны `E` (BDR + optic reach × aim) спад `MachineGun` и `LightMachineGun` доходит до floor **0.25** за **16** клеток, либо за оставшееся расстояние до `WeaponRange`, если оно короче.
- Плато до `E` не режется. Authored `BulletDropRange` / `WeaponRange` / урон / длина очереди не меняются.
- Дальше  `E+16` до физического предела выстрел остаётся возможным на floor.
- Непулемётные классы сохраняют растяжку до `WeaponRange`.

## Non-goals

- Схема A (плато 75% BDR).
- Правка authored стволов, AP, Recoil, BurstShots, штрафа без опоры.
- Отдельный CTH-фактор в breakdown (тот же «Bullet Drop»).
- Смена AI ExtremeRange / hard cutoff стрельбы.

## Требования

- `JAZZ-WEAPONS-013-REQ-001` — для `MachineGun` и `LightMachineGun`: `falloff_end = min(R, E + 16)`; `t = clamp((d − E) / (falloff_end − E), 0, 1)`; та же floor/power кривая.
- `JAZZ-WEAPONS-013-REQ-002` — прочие классы: `falloff_end = R` без изменений.
- `JAZZ-WEAPONS-013-REQ-003` — `GetRangeDamageReduction` использует тот же profile (урон на дальке падает вместе с CTH).
- `JAZZ-WEAPONS-013-REQ-004` — оптика по-прежнему двигает `E`; 16 клеток считаются от текущего `E` (в т.ч. unassisted-ветка от чистого BDR).
- `JAZZ-WEAPONS-013-REQ-005` — technical + wiki + showcase RU/EN в том же change set.

## Инварианты и ограничения

- `d >= R` → невозможный выстрел (`0`), не floor.
- До `E` range factor = 1 (средняя дистанция с упора как сейчас).
- `Grouping` и `p = max(1.25, BDR×0.05 + G/100)` не переписываются.
- Публичные ID CombatAction / property не меняются.
- RNG order атаки не меняется.

## Acceptance criteria

- `JAZZ-WEAPONS-013-AC-001` — static/automated: ПКМ без оптики, `d = BDR` → factor 1; `d = 24` → ≈0.79; `d = BDR+16` → ≈0.25; `d >= 60` → impossible.
- `JAZZ-WEAPONS-013-AC-002` — static/automated: MAC 24/29 без оптики, `d = 14` → 1; `d = 20` → ≈0.78 (тот же классный горизонт, что у MG).
- `JAZZ-WEAPONS-013-AC-003` — static/automated: АК-47 на 24 клетках не использует 16-клеточный горизонт (factor выше сжатой MG-кривой).
- `JAZZ-WEAPONS-013-AC-004` — automated: `scripts/test-shooting-model.ps1` PASS.
- `JAZZ-WEAPONS-013-AC-005` — docs: accuracy-model + combat-cth-actions + wiki/showcase combat-and-accuracy и weapons-and-ammo согласованы.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: только JAZZ `JAZZ_CTHGetRangeProfile` и зеркало в shooting-model test.
- Saves: миграция не нужна.
- Network/determinism: без нового RNG; тот же pipeline UI/AI/атаки.
- Generated data: нет.
- Cross-package: нет.
- Rollback: откат change set.
- Playtest: желателен на Эрни (MAC / ДП) и позднем ПКМ; не блокирует static DoD.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: front matter.
- Exclusive resources: none.

## Решение владельца

- Статус: `implemented`
- Кто подтвердил: project-owner («и да и легкие и тяжелые» — схема B, оба класса)
- Дата: 2026-08-23

## Evidence

- `JAZZ-WEAPONS-013-AC-001`: `PASS` — automated: `scripts/test-shooting-model.ps1` PKM at BDR factor 1; at 24 in 0.75–0.82; at BDR+16 ≈ 0.25.
- `JAZZ-WEAPONS-013-AC-002`: `PASS` — automated: MAC 24/29 at BDR factor 1; at 20 in 0.74–0.82.
- `JAZZ-WEAPONS-013-AC-003`: `PASS` — automated: AK-47 at 24 keeps stretched falloff (factor > 0.55).
- `JAZZ-WEAPONS-013-AC-004`: `PASS` — automated: `scripts/test-shooting-model.ps1`.
- `JAZZ-WEAPONS-013-AC-005`: `PASS` — docs: accuracy-model + combat-cth-actions + wiki/showcase combat-and-accuracy and weapons-and-ammo.

## Documentation delta

- `docs/technical/systems/combat-cth-actions.md`
- `docs/technical/weapons/accuracy-model.md`
- `docs/wiki/combat-and-accuracy.md`, `docs/wiki/weapons-and-ammo.md`
- `docs/showcase/ru|en/combat-and-accuracy.md`, `docs/showcase/ru|en/weapons-and-ammo.md`
