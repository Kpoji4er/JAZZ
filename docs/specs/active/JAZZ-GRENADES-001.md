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
- float→integer уже починили для MP, но единого контракта и technical/wiki описания нет;
- нет жёсткого cap на величину отклонения — исторический риск «улетела на другую сторону карты».

## Цели

- одна каноническая integer-модель: **базовый scatter всегда** + **крупный mishap по роллу**;
- один shared resolver для ручных гранат и `HeavyWeapon` (parabola/line/bombard где применимо);
- честный `results.mishap` только на провале ролла; notification только тогда;
- шанс и величина учитывают дистанцию и боевые штрафы по явному контракту;
- hard cap отклонения; item defaults выровнены; docs/wiki отражают player-facing поведение;
- в area-aim **визуальное кольцо отклонения** (тот же tile/CRM пайплайн, что у колец прицеливания/AoE);
- **цвет кольца** читается **как шанс попасть на кольце прицела**: та же шкала `GetCTHColor` / те же пороги, по «шансу удачного приземления» (`100 − mishap%`); размер/слои при этом показывают scatter vs mishap envelope.

## Non-goals

- полный ребаланс чисел `Min/MaxMishapChance` и радиусов AoE по всему каталогу;
- изменение bounce/`CanBounce`, Colby AoE perk, gas mask, trap pipeline;
- отдельный 3D-asset / новая entity-модель кольца (только procedural tiles + CRM, как aim);
- rewrite CTH огнестрела; CommonLib bump.

## Рекомендуемая модель (к утверждению)

### Режимы

1. **Scatter (всегда, не prediction)** — небольшое отклонение через band `Min`.
2. **Mishap (ролл fail / AlwaysMiss)** — крупное отклонение через band `Max` + `ShowMishapNotification`.

Prediction / `explosion_pos` задан снаружи — без RNG отклонения.

### Величина (оба band)

```text
dist_eff = physical_dist
         + WeaponRange_or_ThrowMax × suppression_debuff%
         + WeaponRange_or_ThrowMax × Inaccurate.stacks × 20%

dist_tiles = DivRound(dist_eff, SlabSizeX)
skill_x100 = Clamp(100 - Explosives, 10, 100)

Min band: range ∈ [1, MinMishapRange] tiles
  dist_mod_x100 = Clamp(MulDivRound(dist_tiles, 100, 8), 50, 300)

Max band: range ∈ [MinMishapRange, MaxMishapRange] tiles
  dist_mod_x100 = Clamp(MulDivRound(dist_tiles, 100, 8), 100, 400)

dev = RandRange(min_dev, max_dev)  — integer MulDivRound
dev = Min(dev, CapTiles × SlabSizeX)
направление — равномерный угол (как сейчас)
```

`CapTiles` по умолчанию: `Max(MaxMishapRange × 2, 8)` (не больше ~16 тайлов без отдельного item override). Точное число — см. REQ / решение владельца.

### Шанс mishap

Override `MishapProperties:GetMishapChance`:

1. базовый vanilla-интерполяционный шанс от Explosives / Min–MaxMishapChance;
2. если `dist > half_range`: линейно поднимать к 100% к `full_range` (как в dormant `MishapChanceByDist`);
3. `half_range` / `full_range` = `WeaponRange` для HeavyWeapon/FlareGun, иначе `ThrowMaxRange` (fallback `BaseRange`/`WeaponRange`/`12`);
4. suppression / Inaccurate увеличивают **effective dist** тем же правилом, что и для величины.

UI area-aim продолжает показывать итоговый `%` через тот же метод (`async`).

### Визуал area-aim (кольцо отклонения)

Центр — **точка прицеливания** (`aim_pt` / intended impact), не сдвинутая prediction-RNG (prediction по-прежнему без roll).

Пайплайн — тот же procedural tile / `GrenadeAOEVisuals` / `CRM_SphereAOETilesMaterial`, что у колец прицеливания AoE.

**Цвет — аналог кольца прицела (CTH):**

- источник: async `mishap_chance = weapon:GetMishapChance(attacker, aim_pt, "async")`;
- `success_chance = 100 - mishap_chance` (шанс «удачного» броска / остаться в scatter-band, не уйти в mishap);
- tint = `GetCTHColor(success_chance)` — **те же пороги и RGB**, что у `idAimTarget` в crosshair (`≥60` зелёный … `>0` красный);
- цвет **индицирует риск scatter→mishap** тем же языком, что CTH на кольце прицеливания: зелёный = надёжно, красный = почти наверняка улетит в mishap.

**Размер — два радиуса (детерминированные max band, без RNG):**

| Слой | Радиус | Роль |
|---|---|---|
| **Scatter** | max Min-band | зона обычного always-scatter |
| **Mishap** | max Max-band после CapTiles | оболочка провала |

Оба слоя красятся **одним** `GetCTHColor(success_chance)`; отличие scatter/mishap — радиус (и при необходимости alpha/intensity mishap-оболочки), не отдельная «холодная/тёплая» палитра. При `mishap_chance == 0` mishap-слой можно приглушить/скрыть.

Дополнительно:

1. Blast AoE (inner/outer урон) остаётся отдельным слоем и **не** перекрашивается CTH-шкалой отклонения.
2. Cone-shaped: deviation — круги вокруг aim; cone mesh урона не подменяется.
3. Cleanup на `delete` / invalid aim — как у `blackboard.meshes`.
4. CRM: Clone `GrenadeTilesCast` (или эквивалент) + tint из `GetCTHColor`; не плодить отдельную произвольную палитру.
5. Helper: `MishapProperties:GetDeviationPreviewRadii(attacker, target) → scatter_radius, mishap_radius`.

Публичный контракт цвета: **не дублировать пороги** — вызывать существующий `GetCTHColor` из `CrossHairUI.lua` (или вынести в shared helper только если понадобится load-order; поведение RGB/пороги не менять).

### Shared API

- `MishapProperties:GetEffectiveMishapDist(attacker, target)`  
- `MishapProperties:GetMishapDeviationVectorMin/Max` — только integer, используют effective dist  
- `MishapProperties:GetDeviationPreviewRadii(attacker, target)` — async-safe max радиусы для UI  
- `MishapProperties:ApplyImpactDeviation(attacker, target_pos, attack_args) → target_pos, mishap_flag`  
- `Grenade` и `HeavyWeapon` GetAttackResults вызывают Apply*; гранаты сохраняют ValidatePos retry (до 5); HeavyWeapon — тот же retry для parabola, line получает уже смещённый `target_pos` до LoF.
- `Targeting_AOE_ParabolaAoE` (и при необходимости line/bombard aim path) рисует scatter+mishap кольца с разным цветом.

Удалить свободные `MishapChanceByDist` / `MishapDeviationVectorByDist` после переноса в методы. Неиспользуемый «средний» `GetMishapDeviationVector` либо делегирует в Max (совместимость), либо удаляется, если нет внешних callers.

### Данные предметов

- у всех `GrenadeLauncher` / `UnderslungGrenadeLauncher` / mortar/rocket с Mishap явно задать `MinMishapRange` и `MaxMishapRange`;
- hint M79/аналоги привести к факту: «шанс и разброс растут с дистанцией»;
- без массового ребаланса chance чисел, кроме явных дыр (отсутствие Min range).

## Требования

- `JAZZ-GRENADES-001-REQ-001` — любой non-prediction бросок/выстрел с `MishapProperties` без заданного `explosion_pos` применяет scatter band Min; mishap band Max только при fail ролла / AlwaysMiss.
- `JAZZ-GRENADES-001-REQ-002` — `results.mishap == true` только для Max band; UI notification только тогда; scatter без notification.
- `JAZZ-GRENADES-001-REQ-003` — один shared resolver для `Grenade` и `HeavyWeapon`; integer math; RNG только через `attacker`/`unit` Random/RandRange.
- `JAZZ-GRENADES-001-REQ-004` — `GetMishapChance` учитывает effective dist (throw/weapon range, suppression, Inaccurate) и совпадает с UI async path.
- `JAZZ-GRENADES-001-REQ-005` — величина отклонения использует effective dist; hard cap не даёт улететь дальше `CapTiles`.
- `JAZZ-GRENADES-001-REQ-006` — item defaults GL/underslung имеют явные Min/MaxMishapRange; player-facing hints не врут.
- `JAZZ-GRENADES-001-REQ-007` — technical + showcase/wiki (если заметно игроку) описывают always-scatter / mishap / distance / цвет колец.
- `JAZZ-GRENADES-001-REQ-008` — area-aim показывает кольца отклонения (scatter + mishap envelope radii); **цвет = `GetCTHColor(100 − mishap%)`** — та же шкала, что у кольца прицела; радиусы async max band без RNG; blast AoE не перекрашивается этой шкалой.

## Инварианты и ограничения

- deterministic MP: без float в bounds `RandRange`; порядок RNG grenade vs heavy согласован на хосте;
- prediction / UI preview не крутит mishap RNG и не показывает ложный mishap toast;
- UI radius helpers чисто async-safe (можно звать из targeting каждый кадр);
- bounce, jam/condition heavy, AoE Colby, gas — без регрессий;
- blast AoE visuals не ломаются; цвет deviation rings не подменяет цвет blast-колец;
- не менять публичные class/ID предметов;
- generated transaction: companion InventoryItem + `items.lua` + `metadata.lua` вместе.

## Acceptance criteria

- `JAZZ-GRENADES-001-AC-001` — static: один Apply/resolver; нет живых callers удалённых ByDist free functions; Min/Max integer-only.
- `JAZZ-GRENADES-001-AC-002` — static: `results.mishap` выставляется только в Max-ветке; Min-ветка не вызывает `ShowMishapNotification`.
- `JAZZ-GRENADES-001-AC-003` — static/editor: GL/Underslung имеют Min+Max MishapRange; hint текст RU/EN согласован.
- `JAZZ-GRENADES-001-AC-004` — runtime: Explosives высокий / близкая дистанция → малый scatter, редкий mishap; низкий / дальняя → чаще mishap и больше разброс, но ≤ CapTiles.
- `JAZZ-GRENADES-001-AC-005` — runtime: suppression/Inaccurate повышают displayed mishap % и наблюдаемый разброс.
- `JAZZ-GRENADES-001-AC-006` — runtime/MP smoke: одинаковый seed path не десинхронит на броске гранаты и выстреле underslung.
- `JAZZ-GRENADES-001-AC-007` — docs technical + showcase/wiki обновлены под фактическое поведение.
- `JAZZ-GRENADES-001-AC-008` — human/runtime aim: кольца отклонения видны; цвет совпадает с `GetCTHColor(100−mishap%)` на тех же порогах, что crosshair; при росте mishap% цвет уходит зелёный→красный; радиусы растут с дистанцией/штрафами; cleanup при смене/отмене aim.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ override `GetAttackResults` / `GetMishapChance` / deviation vectors; CLib коллизий по этим символам в текущем срезе не ожидается — перепроверить snapshot перед merge.
- Saves: новых persistent fields нет; изменится только будущий roll outcome.
- Network/determinism: critical — только integer RNG на attacker.
- Generated data: да, при правке InventoryItem mishap fields / hints.
- Cross-package: нет обязательных units/maps/assets.
- Rollback: один change set code+items+docs.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: cloud agent
- Reviewer: project-owner
- Declared write set: см. front matter
- Exclusive resources: `items.lua`, `metadata.lua`

## Решение владельца

- Статус: `draft` — ждать approval по развилкам ниже
- Кто подтвердил: pending
- Дата: pending

### Развилки (нужен ответ владельца)

1. **Always-scatter** — оставить (рекомендация) / вернуть vanilla «только при mishap»?
2. **CapTiles** — `max(2×MaxMishapRange, 8)` (рекомендация) / фиксированные 8 / 12 / своё число?
3. **Chance×дистанция** — включить в `GetMishapChance` (рекомендация, чинит hint) / только величина, chance skill-only?
4. **Suppression/Inaccurate** — в chance+величину (рекомендация) / только величину / игнор в этом spec?
5. **UI** — **зафиксировано владельцем**: кольца как aim/AoE tiles; **цвет как у шанса попасть на кольце прицела** (`GetCTHColor(100 − mishap%)`); радиусы показывают scatter vs mishap envelope.

## Evidence

- `JAZZ-GRENADES-001-AC-001`–`008`: `BLOCKED` — ожидает approval и реализацию.

## Documentation delta

- `docs/technical/systems/explosives-traps-heavy-weapons.md` — секция scatter/mishap;
- player-facing: `docs/wiki/` + `docs/showcase/ru|en` по затронутому аспекту боя/взрывчатки;
- spec этот файл.
