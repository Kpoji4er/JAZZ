---
id: JAZZ-GRENADES-001
status: draft
owner: project-owner
systems:
  - explosives-traps-heavy-weapons
  - combat-cth-actions
  - weapons-ammo-components
  - ui-audio-fx
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Grenade.lua
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/IModeCombatAreaAim.lua
  - jazz/Code/CrossHairUI.lua
  - jazz/InventoryItem/*.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/specs/active/JAZZ-GRENADES-001.md
  - jazz/docs/technical/systems/explosives-traps-heavy-weapons.md
  - jazz/docs/wiki/**
  - jazz/docs/showcase/ru/**
  - jazz/docs/showcase/en/**
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
related_decisions:
  - none
approved_by: pending
---

# JAZZ-GRENADES-001: нормализация отклонения гранат и тяжёлых снарядов

## Проблема

Механика отклонения (mishap/scatter) гранат, подствольников, GL, ракет и миномётов собрана «на коленке»:

- бросок **всегда** отклоняется (Min при «успехе», Max при провале) — намерение сохраняем, но код дублирован в `Grenade:GetAttackResults` и `HeavyWeapon:GetAttackResults` с разным retry/validate;
- `results.mishap` почти всегда `true`, UI-нотификация только на Max — семантика флага сломана;
- helpers `MishapChanceByDist` / `MishapDeviationVectorByDist` (дистанция, suppression, Inaccurate) **не подключены**, при этом у M79 hint говорит, что шанс промаха растёт с дистанцией;
- у части GL/`UnderslungGrenadeLauncher` нет явного `MinMishapRange`; формулы Min/Max разъехались по делителям и clamp;
- шанс всегда от Explosives, хотя throw ощущается от ловкости, а прицельный GL/ракета — от меткости;
- float→integer уже починили для MP, но единого контракта и technical/wiki описания нет;
- нет жёсткого cap на величину отклонения — исторический риск «улетела на другую сторону карты»;
- цвет зоны поражения не отражает риск mishap (в отличие от CTH-кольца прицела).

## Цели

- always-scatter + крупный mishap по роллу; scatter **плавнее** текущего (мягче Min-band);
- один shared resolver для ручных гранат и `HeavyWeapon`;
- честный `results.mishap` только на провале ролла; notification только тогда;
- на близкой/оптимальной дистанции **только scatter** (mishap% = 0); дальше шанс растёт;
- governing skill: throw → Dexterity; GL/подствол/ракета/миномёт → Marksmanship;
- suppression/Inaccurate влияют на **шанс и величину**;
- CapTiles по расчёту; item defaults/hints; docs/wiki;
- цвет существующих колец **зоны поражения** = `GetCTHColor(100 − mishap%)`.

## Non-goals

- полный ребаланс чисел `Min/MaxMishapChance` и радиусов AoE по всему каталогу;
- изменение bounce/`CanBounce`, Colby AoE perk, gas mask, trap pipeline;
- отдельный UI-слой «кольцо радиуса разброса»;
- смена `UnitStat` XP-атрибута предметов (только runtime mishap skill; UnitStat может остаться Explosives);
- rewrite CTH огнестрела; CommonLib bump.

## Модель (решения владельца зафиксированы)

### Режимы

1. **Scatter (всегда, не prediction)** — band `Min`, плавная кривая (см. ниже).
2. **Mishap (ролл fail / AlwaysMiss)** — band `Max` + `ShowMishapNotification`.

Prediction / внешний `explosion_pos` — без RNG отклонения.

### Governing skill

| Класс | Атрибут для chance и skill_mod величины |
|---|---|
| Thrown `Grenade` / `GrenadeItem` / flare-throw | `Dexterity` |
| `HeavyWeapon` (GL, Underslung, Rocket, Mortar) и `FlareGun` | `Marksmanship` |

Выбор Marksmanship для тяжёлых (а не Explosives): прицельная доставка, согласовано с CTH-языком UI. `UnitStat` предметов в этом spec не обязательно менять.

### Effective distance

```text
full_range = WeaponRange           — HeavyWeapon / FlareGun
           | ThrowMaxRange         — Grenade (fallback BaseRange, else 12)
ref = full_range * SlabSizeX

dist_eff = physical_dist
         + ref × suppression_debuff%   (тот же tier table, что был в ByDist)
         + ref × Inaccurate.stacks × 20%

dist_tiles = DivRound(dist_eff, SlabSizeX)
```

Suppression/Inaccurate входят и в chance, и в величину через `dist_eff`.

### Шанс mishap

```text
attr = governing skill (выше)
base = vanilla-style interp MinMishapChance..MaxMishapChance по attr
half = ref / 2                         — граница «оптимальной/близкой»

if dist_eff <= half:
  chance = 0                           — только scatter
else:
  -- от 0 у half к 100% у full (skill задаёт base-пол после half)
  t_x100 = Min(100, MulDivRound(dist_eff - half, 100, half))
  chance = Min(100, MulDivRound(Max(base, 1), t_x100, 100)
                     + MulDivRound(100 - Max(base, 1), Max(0, t_x100 - 50), 50))
```

Упрощённая эквивалентная форма для реализации (integer-only, та же семантика):

```text
if dist_eff <= half: return 0
-- линейный подъём: у half → 0, у full → 100, сжимаемый skill через base
raw = Min(100, MulDivRound(dist_eff - half, 100, half))
-- смешать raw с base: низкий attr → ближе к raw; высокий attr → медленнее растёт
-- Практическая формула:
chance = Min(100, MulDivRound(raw, 100 + Max(base, 0), 200) + MulDivRound(raw, Max(base, 0), 200))
```

**Канон для кода (зафиксировать одну формулу без двусмысленности):**

```text
if dist_eff <= half then return 0 end
t_x100 = Min(100, MulDivRound(dist_eff - half, 100, Max(half, 1)))
-- t=0 у half, t=100 у full_range
-- при t=100 цель = 100; при малых t шанс мал; base (от attr) задаёт кривизну:
-- chance = MulDivRound(t_x100, Clamp(base, 0, 100) + MulDivRound(100 - Clamp(base,0,100), t_x100, 100), 100)
-- → у full всегда 100%; у mid высокий attr даёт ниже шанс, чем низкий attr
chance = Min(100, MulDivRound(t_x100,
  Clamp(base, 0, 100) + MulDivRound(100 - Clamp(base, 0, 100), t_x100, 100),
  100))
```

UI async path = тот же `GetMishapChance`.

### Величина

```text
skill_x100 = Clamp(100 - attr, 10, 100)   -- attr = governing skill

Min band (scatter, плавнее):
  tile_lo, tile_hi = 1, MinMishapRange (default 2)
  dist_mod_x100 = Clamp(MulDivRound(dist_tiles, 100, 10), 40, 200)   -- было /8 и 50..300

Max band (mishap):
  tile_lo, tile_hi = MinMishapRange, MaxMishapRange
  dist_mod_x100 = Clamp(MulDivRound(dist_tiles, 100, 8), 100, 400)

dev = RandRange(min_dev, max_dev)
dev = Min(dev, CapTiles * SlabSizeX)
угол равномерный
```

### CapTiles (расчёт)

Без cap worst-case Max band: `MaxMishapRange × 4 × 1.0` → frag 8×4=**32** тайла, GL 6×4=**24** тайла (через карту).

| Cap | Frag (Max=8) | GL (Max=6) | Эффект |
|---|---|---|---|
| `2 × MaxMishapRange` | 16 | 12 | режет worst ×2, mishap всё ещё тяжёлый |
| `Max + 4` | 12 | 10 | жёстче |
| fixed 12 | 12 | 12 | единообразно |

**Зафиксировано расчётом:** `CapTiles = Max(2 × MaxMishapRange, 8)`.  
Frag ≤16, GL ≤12, default Max=4 → 8. Отдельный item override не вводится в этом spec.

### Визуал area-aim

- **Радиус** = зона поражения (текущие blast/cone tiles).
- **Цвет** = `GetCTHColor(100 − mishap%)` — шкала кольца прицела.
- Отдельных колец разброса нет.
- Trajectory arc: optional тот же tint; blast/cone обязательны.

### Shared API

- `MishapProperties:GetMishapGoverningSkill(attacker)` → число attr  
- `MishapProperties:GetEffectiveMishapDist(attacker, target)`  
- `MishapProperties:GetMishapChance` — override с half-range zero + distance ramp + suppression  
- `MishapProperties:GetMishapDeviationVectorMin/Max` — integer, governing skill, smoother Min  
- `MishapProperties:ApplyImpactDeviation(...)` → `target_pos, mishap_flag`  
- `Grenade` / `HeavyWeapon` GetAttackResults → Apply*; ValidatePos retry для parabola  
- `Targeting_AOE_ParabolaAoE` (+ cone path) — tint AoE materials через `GetCTHColor`

Удалить free `MishapChanceByDist` / `MishapDeviationVectorByDist` после переноса.

### Данные предметов

- явные `MinMishapRange` + `MaxMishapRange` у всех GL/Underslung/mortar/rocket с Mishap;
- hints: шанс и разброс растут с дистанцией; на близкой — только разброс; throw↔ловкость, GL↔меткость (RU/EN).

## Требования

- `JAZZ-GRENADES-001-REQ-001` — always-scatter (Min) + mishap (Max) только при fail/AlwaysMiss; prediction без RNG.
- `JAZZ-GRENADES-001-REQ-002` — `results.mishap` и notification только на Max band.
- `JAZZ-GRENADES-001-REQ-003` — один shared resolver; integer math; RNG через attacker/unit.
- `JAZZ-GRENADES-001-REQ-004` — `GetMishapChance`: Dexterity для throw, Marksmanship для HeavyWeapon/FlareGun; `dist_eff ≤ half_range → 0`; далее ramp по канон-формуле; suppression/Inaccurate в `dist_eff`; UI async совпадает.
- `JAZZ-GRENADES-001-REQ-005` — величина от governing skill + `dist_eff`; Min-band плавнее (`/10`, clamp 40..200); CapTiles = `Max(2×MaxMishapRange, 8)`.
- `JAZZ-GRENADES-001-REQ-006` — item Min/MaxMishapRange + честные RU/EN hints.
- `JAZZ-GRENADES-001-REQ-007` — technical + showcase/wiki sync.
- `JAZZ-GRENADES-001-REQ-008` — tint зоны поражения `GetCTHColor(100 − mishap%)`; радиусы = AoE; без колец разброса.

## Инварианты и ограничения

- MP: без float в `RandRange` bounds; согласованный порядок RNG;
- prediction/UI не крутят mishap RNG / toast;
- семантика радиусов AoE не меняется;
- публичные class/ID предметов не менять;
- generated transaction companion + `items.lua` + `metadata.lua`.

## Acceptance criteria

- `JAZZ-GRENADES-001-AC-001` — static: один Apply/resolver; ByDist free functions удалены/без callers; Min/Max integer-only; smoother Min clamps.
- `JAZZ-GRENADES-001-AC-002` — static: `results.mishap` / notification только Max-ветка.
- `JAZZ-GRENADES-001-AC-003` — static/editor: GL/Underslung Min+Max ranges; hints RU/EN.
- `JAZZ-GRENADES-001-AC-004` — runtime: близкая/≤half → mishap% 0, только малый scatter; дальняя → выше % и Max band; отклонение ≤ CapTiles; throw реагирует на Dexterity, GL на Marksmanship.
- `JAZZ-GRENADES-001-AC-005` — runtime: suppression/Inaccurate поднимают % и разброс (могут вытолкнуть из «только scatter» зоны).
- `JAZZ-GRENADES-001-AC-006` — runtime/MP smoke без десинха на throw и underslung.
- `JAZZ-GRENADES-001-AC-007` — docs technical + showcase/wiki.
- `JAZZ-GRENADES-001-AC-008` — human aim: цвет зоны поражения = `GetCTHColor(100−mishap%)`; радиусы = AoE; нет лишних колец разброса.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: overrides GetAttackResults / GetMishapChance / deviation / area-aim tint; перепроверить CLib snapshot перед merge.
- Saves: новых persistent fields нет.
- Network/determinism: critical — integer RNG на attacker.
- Generated data: InventoryItem mishap fields / hints.
- Cross-package: нет обязательных units/maps/assets.
- Rollback: один change set code+items+docs.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: cloud agent
- Reviewer: project-owner
- Declared write set: см. front matter
- Exclusive resources: `items.lua`, `metadata.lua`

## Решение владельца

- Статус: `draft` — решения по развилкам зафиксированы ниже; ждать явного **approve** на реализацию
- Кто подтвердил (решения): project-owner (chat 2026-07-30)
- Дата approve реализации: pending

### Развилки

1. **Always-scatter** — **да**, ощущение ок; Min-band сделать плавнее.
2. **CapTiles** — **расчёт:** `Max(2 × MaxMishapRange, 8)` (frag≤16, GL≤12).
3. **Chance×дистанция** — **да**; на ≤half только scatter (chance 0); throw skill = **Dexterity**; GL/ракета/подствол = **Marksmanship**.
4. **Suppression/Inaccurate** — **и шанс, и разброс**.
5. **UI** — радиусы = зона поражения; цвет = `GetCTHColor(100 − mishap%)`.

## Evidence

- `JAZZ-GRENADES-001-AC-001`–`008`: `BLOCKED` — ожидает approve на реализацию.

## Documentation delta

- `docs/technical/systems/explosives-traps-heavy-weapons.md` — scatter/mishap/UI tint;
- `docs/wiki/` + `docs/showcase/ru|en`;
- spec этот файл.
