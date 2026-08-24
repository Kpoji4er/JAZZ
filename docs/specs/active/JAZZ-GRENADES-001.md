---
id: JAZZ-GRENADES-001
status: implemented
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
approved_by: project-owner
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
- governing skill: throw → Dexterity+Explosives; GL/ракета/подствол → Marksmanship+Explosives; пайпы/демо → Explosives-heavy; гранаты уверенно уже ~с **50** (thr 50);
- suppression/Inaccurate влияют на **шанс и величину**;
- CapTiles по расчёту; item defaults/hints; docs/wiki;
- цвет существующих колец **зоны поражения** = `GetCTHColor(reliability)`, где `reliability = (100 − mishap%) × (100 − scatter_risk%) / 100`, `scatter_risk` = mid(Min-band) / CapTiles.

## Non-goals

- полный ребаланс чисел `Min/MaxMishapChance` и радиусов AoE по всему каталогу;
- изменение bounce/`CanBounce`, Colby AoE perk, gas mask, trap pipeline;
- отдельный UI-слой «кольцо радиуса разброса»;
- смена `UnitStat` XP-атрибута предметов (runtime blend отделён; UnitStat может остаться Explosives);
- rewrite CTH огнестрела; CommonLib bump.

## Модель (решения владельца зафиксированы)

### Режимы

1. **Scatter (всегда, не prediction)** — band `Min`, плавная кривая (см. ниже).
2. **Mishap (ролл fail / AlwaysMiss)** — band `Max` + `ShowMishapNotification`.

Prediction / внешний `explosion_pos` — без RNG отклонения.

### Governing skill

Три профиля. **Blend без competence remap** (порог 50 давал обрыв: 49 и 50 жили как разные миры).

Величина отклонения **лёгкого scatter (Min-band)** использует **raw blend** в `skill_x100 = Clamp(100 - blend, 10, 100)` (пол **10%**). **Mishap (Max-band)** навыком **не** ужимается: skill режет только шанс; если провал выпал — это промах (пол нижней границы ≥ **4** тайла, не 1–2 клетки у элиты).

| Профиль | Кто | Blend |
|---|---|---|
| **ThrowGrenade** | `Grenade` / `GrenadeItem` / thrown `Flare` (не demo) | `DivRound(Strength + Dexterity×2 + Explosives×2, 5)` |
| **AimedHeavy** | `GrenadeLauncher`, Underslung, `RocketLauncher`, `Mortar`, `FlareGun` | `DivRound(Marksmanship×2 + Explosives, 3)` |
| **Demo** | `PipeBomb`, `ShapedCharge`, `ThrowableTrapItem` (TNT/C4/PETN timed/remote/proximity) | `DivRound(Explosives×3 + Dexterity, 4)` |

**Дальность броска** — ванильный `GetMaxAimRange`: интерполяция `BaseRange`→`ThrowMaxRange` по **Силе** (+ перк Throwing). Ловкость и Взрывчатка дальность не тянут, они (вместе с Силой) тянут чистоту броска.

Item data для Demo в этом spec: **усилить** Explosives-зависимость — поднять `MaxMishapChance` у `PipeBomb` / `ShapedCharge` / TNT-линейки (ориентир +15..+25 к текущему Max, без трогания C4/PETN professional line если уже низкий Max≤18 — там достаточно высокого Threshold). Конкретные числа в реализации + hints.

### Effective distance

```text
full_range = WeaponRange                                      — HeavyWeapon / FlareGun
           | GetMaxAimRange(attacker) [+ Throwing perk]       — Grenade (Strength: BaseRange→ThrowMaxRange)
           | ThrowMaxRange                                    — fallback if no attacker
ref = full_range * SlabSizeX

dist_eff = physical_dist
         + ref × suppression_debuff%   (тот же tier table, что был в ByDist)
         + ref × Inaccurate.stacks × 20%

dist_tiles = DivRound(dist_eff, SlabSizeX)

-- magnitude remapping (не chance):
full_tiles = DivRound(ref, SlabSizeX)
half_tiles = full_tiles / 2
if dist_tiles <= half_tiles:
  scatter_tiles = dist_tiles * full_tiles / half_tiles   -- half → old full intensity
else:
  scatter_tiles = full_tiles + (dist_tiles - half_tiles) * (0.25 * full_tiles) / half_tiles
  -- full → ~1.25× old full intensity (≈80% accuracy vs pre-tune for blend 90)
```

Suppression/Inaccurate входят и в chance, и в величину через `dist_eff`. **ThrowMaxRange не режем:** дальний бросок доступен; у середняка неэффективен, у 90/90 на макс всё ещё рабочий (~80% прежней точности).

### Шанс mishap

```text
attr_blend = GetMishapSkillBlend(attacker)   -- throw: (Str + Dex×2 + Expl×2)/5
ref = GetMishapFullRange(attacker)           -- personal throw / WeaponRange
t = Clamp(dist_eff / ref, 0, 1)
s = smoothstep(t)                            -- 3t²−2t³, без ступеньки на ¼/½
far_c = Clamp(100 − blend×60/100, 25, 100)  -- 100 → 40% на краю; 50 → 70%; 0 → 100%
chance = s × far_c
```

UI async path = тот же `GetMishapChance`.

**Owner playtest (2026-08-24):** quarter→half + t² + threshold 50 + сырой `ThrowMaxRange` — чёрное на mid при 100/100, Сила/Ловкость/Взрывчатка почти не видны. Замена: personal range, throw blend Str+Dex+Expl, smoothstep 0→full.

### Величина

```text
scatter_tiles = remap(dist_tiles)               -- half ≈ old max; full ≈ 1.25× old max

Min band (scatter):
  skill_x100 = Clamp(100 - attr_blend, 10, 100) -- raw blend; floor 10%
  tile_lo, tile_hi = 1, MinMishapRange (default 2)
  dist_mod_x100 = Clamp(MulDivRound(scatter_tiles, 100, 10), 40, 200)

Max band (mishap):
  skill_x100 = 100                              -- no skill shrink (owner 2026-08-24)
  tile_lo = Max(4, MinMishapRange, MaxMishapRange/2)  -- clamp ≤ MaxMishapRange
  tile_hi = MaxMishapRange
  dist_mod_x100 = Clamp(MulDivRound(scatter_tiles, 100, 8), 100, 400)

dev = RandRange(min_dev, max_dev)
dev = Min(dev, CapTiles * SlabSizeX)
угол равномерный
```

**Owner playtest (2026-08-11):** D (thr 50) + ранний chance-ramp (¼→½); magnitude half≈old max, full≈+25% на **scatter**. Пол skill 40% на scatter отвергнут — душил элиту на дальнем броске. `ThrowMaxRange` не режем.

**Owner (2026-08-24):** mishap при высоком навыке садился в 1–2 клетки (`skill_x100=10%` на Max-band). Mishap = промах: Max-band без skill shrink, нижняя граница ≥4 тайла.

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
- **Цвет** = `GetCTHColor(reliability)` — шкала кольца прицела.
  - `reliability = (100 − mishap%) × (100 − scatter_risk%) / 100`
  - `scatter_risk` = mid(Min-band deviation) / CapTiles (0..100), без RNG
  - до quarter-range (`mishap% = 0`) цвет всё равно меняется от величины scatter
- Отдельных колец разброса нет.
- Trajectory arc: тот же tint; blast/cone обязательны.

### Shared API

- `MishapProperties:GetMishapSkillProfile()` → `ThrowGrenade` | `AimedHeavy` | `Demo`
- `MishapProperties:GetMishapSkillBlend(attacker)` → integer blend  
- `MishapProperties:GetEffectiveMishapDist(attacker, target)`  
- `MishapProperties:GetMishapChance` — override: Str+Dex+Expl throw blend, smoothstep 0→full personal range, suppression  
- `MishapProperties:GetMishapDeviationBounds(unit, target, band)` → `min_dev, max_dev` (no RNG)
- `MishapProperties:GetMishapDeviationVectorMin/Max` — integer, raw blend, smoother Min  
- `MishapProperties:GetMishapAimReliability(attacker, target)` → `reliability, chance, scatter_risk`
- `MishapProperties:ApplyImpactDeviation(...)` → `target_pos, mishap_flag`  
- `Grenade` / `HeavyWeapon` GetAttackResults → Apply*; ValidatePos retry для parabola  
- `Targeting_AOE_ParabolaAoE` (+ cone path) — tint через `GetMishapAimReliability` + `GetCTHColor`

Удалить free `MishapChanceByDist` / `MishapDeviationVectorByDist` после переноса.

### Данные предметов

- явные `MinMishapRange` + `MaxMishapRange` у всех GL/Underslung/mortar/rocket с Mishap;
- Demo (`PipeBomb`, `ShapedCharge`, TNT-линейка): поднять `MaxMishapChance` (+15..+25 ориентир), hints про сильную зависимость от Explosives;
- hints гранат/GL: близко — только разброс; навыки Dex+Expl / MS+Expl; с ~**50** уже уверенно для обычных гранат (RU/EN).

## Требования

- `JAZZ-GRENADES-001-REQ-001` — always-scatter (Min) + mishap (Max) только при fail/AlwaysMiss; prediction без RNG.
- `JAZZ-GRENADES-001-REQ-002` — `results.mishap` и notification только на Max band.
- `JAZZ-GRENADES-001-REQ-003` — один shared resolver; integer math; RNG через attacker/unit.
- `JAZZ-GRENADES-001-REQ-004` — `GetMishapChance`: ThrowGrenade `(Str + Dex×2 + Expl×2)/5`; AimedHeavy `(MS×2+Expl)/3`; Demo `(Expl×3+Dex)/4`; **без** competence threshold; smoothstep 0→full of `GetMishapFullRange(attacker)` (thrown = `GetMaxAimRange` / Strength); far `Clamp(100−blend×60/100, 25, 100)`; suppression/Inaccurate в `dist_eff`; UI async совпадает.
- `JAZZ-GRENADES-001-REQ-005` — scatter (Min) от raw skill blend + `dist_eff`; mishap (Max) **без** skill shrink, `tile_lo ≥ 4`; Min-band плавнее (`/10`, clamp 40..200); CapTiles = `Max(2×MaxMishapRange, 8)`.
- `JAZZ-GRENADES-001-REQ-006` — item Min/MaxMishapRange; Demo MaxMishapChance усилен; честные RU/EN hints (в т.ч. уверенность гранат ~с **50**).
- `JAZZ-GRENADES-001-REQ-007` — technical + showcase/wiki sync.
- `JAZZ-GRENADES-001-REQ-008` — tint зоны поражения/дуги `GetCTHColor(GetMishapAimReliability)`; радиусы = AoE; без колец разброса.

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
- `JAZZ-GRENADES-001-AC-004` — runtime: Strength растёт круг; Dex/Expl/Str меняют цвет без обрыва; 100/100/100 mid не чёрный; Demo при Expl30 рискованнее; GL реагирует на MS+Expl.
- `JAZZ-GRENADES-001-AC-005` — runtime: suppression/Inaccurate поднимают % и разброс (могут вытолкнуть из «только scatter» зоны).
- `JAZZ-GRENADES-001-AC-006` — runtime/MP smoke без десинха на throw и underslung.
- `JAZZ-GRENADES-001-AC-007` — docs technical + showcase/wiki.
- `JAZZ-GRENADES-001-AC-008` — human aim: цвет зоны/дуги = `GetCTHColor(reliability)` (mishap% × scatter_risk mix); радиусы = AoE; нет лишних колец разброса.

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

- Статус: `implemented`
- Кто подтвердил: project-owner (chat 2026-07-30, «Делай»)
- Дата: 2026-07-30

### Развилки

1. **Always-scatter** — **да**, ощущение ок; Min-band сделать плавнее.
2. **CapTiles** — **расчёт:** `Max(2 × MaxMishapRange, 8)` (frag≤16, GL≤12).
3. **Chance×дистанция** — smoothstep 0→full personal range; throw blend **Str+Dex+Expl**; без threshold-обрыва. **AimedHeavy** = MS+Expl; **Demo** = Expl-heavy. Дальность броска = Сила. (2026-08-24 owner: проверить все три стата, без резкого обрыва.)
4. **Suppression/Inaccurate** — **и шанс, и разброс**.
5. **UI** — радиусы = зона поражения; цвет = mix mishap% + Min-band scatter → `GetCTHColor(reliability)`.
6. **Mishap magnitude (2026-08-24)** — Max-band без `skill_x100`; пол `tile_lo ≥ 4`. Навык режет шанс и лёгкий scatter, не величину провала.

## Evidence

- `JAZZ-GRENADES-001-AC-001`: `PASS` — static: shared `ApplyImpactDeviation`; ByDist free functions removed; Min/Max integer path.
- `JAZZ-GRENADES-001-AC-002`: `PASS` — static: mishap flag/notification only on Max band in ApplyImpactDeviation.
- `JAZZ-GRENADES-001-AC-003`: `PASS` — static/editor data: GL MinMishapRange; Demo MaxMishapChance; RU/EN hints updated.
  - **Exception 2026-08-11 (owner):** `ShapedCharge` MaxMishapChance restored to **60** (pre-Demo bump) — Barry homemade charges stay vanilla-shaped identity.
- `JAZZ-GRENADES-001-AC-004`: `BLOCKED` — runtime: Strength range + Dex/Expl/Str color, no cliff. Static: `_check_grenade_mishap_chance_curve.py`.
- `JAZZ-GRENADES-001-AC-005`: `BLOCKED` — runtime: общий playtest (suppression/Inaccurate).
- `JAZZ-GRENADES-001-AC-006`: `BLOCKED` — runtime/MP: общий playtest smoke.
- `JAZZ-GRENADES-001-AC-007`: `PASS` — technical + wiki + showcase ru/en updated.
- `JAZZ-GRENADES-001-AC-008`: `BLOCKED` — human aim tint vs GetCTHColor: общий playtest.

## Documentation delta

- `docs/technical/systems/explosives-traps-heavy-weapons.md` — scatter/mishap/UI tint + playtest checks;
- `docs/technical/testing.md` — playtest bullets for grenade/GL mishap;
- `docs/wiki/combat-and-accuracy.md` + `docs/wiki/README.md` — player-facing grenade/GL section;
- `docs/showcase/ru|en/combat-and-accuracy.md` + `home.md` — витрина в паре с wiki;
- spec этот файл.
