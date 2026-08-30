---
id: JAZZ-COMBAT-009
status: approved
owner: project-owner
systems:
  - combat-cth-actions
  - weapons-ammo-components
  - ui-audio-fx
  - ai-awareness
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/IModeCombatAreaAim.lua
  - jazz/Code/AccuracyRangeCTH.lua
  - jazz/Code/System_OR_Unit.lua
  - jazz/Code/CombatAI.lua
  - jazz/Code/AiActions.lua
  - jazz/Code/CrossHairUI.lua
  - jazz/docs/tools/_test_combat_009_ow_cone.py
  - jazz/docs/tools/README.md
  - jazz/docs/specs/active/JAZZ-COMBAT-009.md
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/technical/weapons/combat-actions.md
  - jazz/docs/technical/weapons/accuracy-model.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/wiki/combat-actions.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-actions.md
  - jazz/docs/showcase/en/combat-actions.md
exclusive_resources:
  - none
related_decisions:
  - none
related_specs:
  - JAZZ-CTH-001
  - JAZZ-GRENADES-001
  - JAZZ-AI-009
  - JAZZ-AI-OW-001
approved_by: project-owner
---

# JAZZ-COMBAT-009: Overwatch — ширина от дистанции и цвет CTH

## Проблема

Сектор Overwatch сейчас **фиксированной** ширины: `Firearm.OverwatchAngle` (минуты дуги, 360° = 21600) не зависит от того, куда игрок ставит конус. Пистолет с authored **5400 (90°)** одинаково широк в упор и на 12 клетках. Нет рычага «держать дверь в трёх клетках широким веером / стрелять коридор узко».

При прицеливании Overwatch конус одноцветный (`WeaponAOE`). У гранат зона уже красится `GetCTHColor` (GRENADES-001). Игрок не видит, насколько сектор ещё «попадает», пока не выйдет живая цель. Живая цель плюс боль/подавление/укрытие часто даёт **0%** — бесполезный сигнал на этапе постановки.

## Цели

- Чем дальше точка постановки сектора — тем **уже** конус; ближе — шире.
- Authored `OverwatchAngle` — ширина **на BDR** (resolved `BulletDropRange` после ствола), не константа на любой дистанции.
- На `WeaponRange` сектор сжимается в **минимальную полоску** (винтовки и пулемёты — **2°**).
- Пистолет / револьвер на **ближайшей постановке** (`MinRange` = 50% BDR) — широкий веер, **не шире 155°** (треугольник aim-меша; ≥160° + растущий `d` давали «сначала шире, потом уже»). Для BDR=6 это 3 клетки; для Glock BDR=8 / CZ75 BDR=7 — 4 клетки.
- Дробовик ближе BDR — не уже **100° × d_min / d**. ПП на `d_min` — inverse (MP5 72° → **144°**). Штурмовая / снайперка — inverse ×2 на 50% BDR. Пулемёт / ЛП — **(BDR/d)²** (ПКМ 10°→**40°**), иначе наземный клин не толстеет.
- Постановка ближе BDR **разрешена**, но не ближе **50% BDR** (пол 2 клетки). Текущий clamp `MinRange = BDR` снимается.
- Authored `OverwatchAngle` и обвес (оптика, лазер) остаются базой кривой, не переписываются в `items.lua`.
- Пока целишься Overwatch / MGSetup / MGRotate — конус красится `GetCTHColor` как гранаты: один tint на весь сектор.
- Цвет считается по **виртуальной стоячей цели в полный рост** на клетке прицела, **без CTH-дебафов** атакующего и без укрытия/crouch цели, чтобы валидный сектор не показывал 0%.

## Non-goals

- Переписывать каталог `OverwatchAngle` у оружия.
- Менять AP, число interrupt, aim-ступени OW, HawksEye 1 ОД, PinDown.
- Дистанционный скейл и CTH-tint для `BulletHell`, `DanceForMe`, `JAZZ_TargetSweep`, `JAZZ_VovaVist`, `EyesOnTheBack`.
- Потайловый градиент CTH (у гранат один цвет на зону — так же).
- Менять **боевой** CTH interrupt: реальная цель, укрытие, стойка и дебафы остаются как сейчас.
- Новый percent-label на конусе (только цвет).
- Новые localization ID.
- CommonLib bump.

## Модель

Углы в **минутах** (1° = 60).

```text
authored = weapon.OverwatchAngle              -- после Scope/Laser/etc.
bdr      = max(resolved BulletDropRange, 2)  -- ствол множит BDR; оптика E не двигает якорь
R        = WeaponRange                       -- физический maxrange; OW ставится до R
d_min    = Max(2, DivRound(bdr, 2))          -- 50% BDR; «3 клетки» = 50% только при BDR=6
d        = Clamp(клетки step_pos → aim point, d_min, R)
```

Почему 50%, не 30% и не фиксированные 3 клетки: inverse на 50% BDR у пистолета 90° даёт **180°**, затем clamp **155°** (меш — треугольник, `tan(θ/2)`; зона 160–210° на playtest CZ75 сначала расширяла клин, потом сужала). У Makarov/Luger (BDR=6) ближайшая клетка — 3. У Glock (BDR=8) / CZ75 (BDR=7) — **4**. Винтовка (BDR=16) не ставится ближе **8**.

Сейчас `MinRange` = BDR — ближе эффективной зоны сектор не ставится. В этом spec:

- `MinRange` = **`Max(2, 50% BDR)`** (включая M2; emplacement `min_distance_2d` не трогать);
- `MaxRange` = **`WeaponRange`**, не 80% WR.

Якорь authored угла — **BDR**. Дальше BDR — спад к полоске на R.

### Ширина конуса

Чистый inverse на 50% BDR даёт винтовке/ПП ровно ×2 authored (АК 22°→44°, ПП 72°→144°), затем clamp 155°. Оптика `E` не участвует. Пулемёт / ЛП после playtest: ещё один `× BDR/d` (квадрат), иначе `tan` клина держит полоску одной ширины.

```text
if d <= bdr:
  angle = MulDivRound(authored, bdr, d)
  if MachineGun or LightMachineGun:
    angle = MulDivRound(angle, bdr, d)
else:
  strip = class_strip(weapon)
  angle = authored + MulDivRound(strip - authored, d - bdr, max(R - bdr, 1))

if Shotgun and d < bdr:
  angle = Max(angle, 100° × d_min / d)

angle = Clamp(angle, 120, 155 * 60)
```

CQB-extra от `CloseRange` и пистолетный пол 200° **сняты** (playtest 2026-08-30): они держали угол в 160–210° несколько клеток подряд, и треугольный меш визуально рос. На BDR угол снова ровно authored (если authored ≤ 155°).

`class_strip` на `WeaponRange`:

| Классы | strip |
| --- | --- |
| `SniperRifle`, `AssaultRifle`, `BattleRifle`, `MachineGun`, `LightMachineGun` | **2° (120)** |
| `SubmachineGun`, `Shotgun` | **8° (480)** |
| `Pistol`, `Revolver` | **20° (1200)** |
| прочее firearm | **4° (240)** |

Карабин / `Firearm` без узкого класса — «прочее». Оптика не меняет strip, она уже ужала `authored`.

Ориентир без обвеса (целые °, после clamp 155°):

| Ствол | CR / BDR / R | d_min | @d_min | @BDR | @R |
| --- | --- | --- | --- | --- | --- |
| Makarov 90° | 0 / 6 / 15 | 3 | **155°** cap (inv 180°) | 90° | 20° |
| Glock 90° | 0 / 8 / 19 | 4 | **155°** cap (inv 180°) | 90° | 20° |
| CZ75 90° | 0 / 7 / 20 | 4 | **155°** cap (inv 157.5°) | 90° | 20° |
| Colt 1911 90° | 0 / 4 / 14 | 2 | **155°** cap | 90° | 20° |
| MP5 72° | 3 / 10 / 30 | 5 | **144°** | 72° | 8° |
| M1897 36° | 5 / 7 / 21 | 4 | **100°** (пол) | 36° | 8° |
| M4 26° | 5 / 15 / 42 | 8 | **49°** | 26° | 4° |
| AK-74 22° | 8 / 16 / 48 | 8 | 44° | 22° | **2°** |
| Мосин 7° | 16 / 16 / 66 | 8 | 14° | 7° | **2°** |
| ПКМ 10° | 8 / 18 / 60 | 9 | **40°** (квадрат) | 10° | **2°** |

`d` — клетка, куда **ставят** сектор. Тот же угол в `g_Overwatch.cone_angle`, UI и interrupt-LOS.

Cap **155° < 180°** — ванильный `circular_overwatch` (доворот на контакт при `cone_angle > 180°`) **не** включается. Ближний пистолет — широкий веер, не полный круг.

### Где считается

Один helper (имя реализации свободное, смысл фиксирован): `Firearm:GetOverwatchConeAngle(dist_tiles)` / эквивалент. Вызывается из:

- `Firearm:GetAreaAttackParams` для `Overwatch`, `MGSetup`, `MGRotate` — когда известны attacker и `target_pos`;
- `IModeCombatAreaAim` после известного `attack_distance` (GetAimParams часто без точки — угол **пересчитать** до `GetAOETiles`);
- AI-постановка Fallback / peel / обычный OW — та же функция от дистанции до якоря.

`GetOverwatchConeParam("Angle")` без дистанции возвращает **authored** (карточка / «Overwatch Width» = ширина **на BDR**). Не писать, что это ширина «всегда».

### Цвет CTH (aim-time)

Как GRENADES-001: один `GetCTHColor(cth)` на `CRM_AOETilesMaterial` сектора (`FillColor` / `BorderColor` / `PulseColor` / LOS / `GridColor`), не `SetColorModifier` и не `WeaponAOE`.

`cth` — превью, не боевой interrupt:

1. Виртуальная цель на aim-плите: **Standing**, body part **Torso**, полный рост, **без укрытия**, без Hidden/stealth, без размера «сидит/лежит».
2. Aim-ступени — те же, что `Unit:GetOverwatchAttacksAndAim` для этого ствола (база `min+1`; AR/Carbine/BR/MG/LMG ещё `+1`; снайперка = `maxAim`). Без модификатора Opportunity Attack (он только у боевого interrupt).
3. **Пропускаются** attacker status CTH: `Pain`, `TraumaArms*`, `TraumaHead*`, `Concussion`, ступени suppression, `Inaccurate`, опьянение/`Nazdarovya`, Stimmed CTH-штраф и прочие `OnCalcChanceToHit` статусы атакующего.
4. **Остаются:** ствол/патрон/обвес, range/close-range/оптика, стойка стрелка, освещение, дым, погода, пылевая буря.
5. Нет LoF до стоячего торса на этой клетке (стена) → **0%**, чёрный tint — это геометрия, не дебаф.
6. Физически возможный выстрел — тот же пол **2%**, что у боевого CTH, чтобы дальний открытый тайл не красился чёрным.

Точка расчёта — **aim point** (дальняя кромка / клетка курсора). Дальше ставишь — уже конус и, как правило, холоднее цвет.

После confirm поставленный сектор **не** красим: ванильный Confirm / Deployed / Activated. CTH-tint только пока целишься.

Пересчёт — в том же кадре, что перерисовка конуса (`moved`), не каждый mousemove без сдвига плиты.

## Требования

- `JAZZ-COMBAT-009-REQ-001` — ширина `Overwatch` / `MGSetup` / `MGRotate`: при `d ≤ BDR` — `authored × BDR / d` (пулемёт/ЛП ещё `× BDR / d`); при `d > BDR` — линейно `authored → class_strip` на `WeaponRange`. Пол только `Shotgun` `100° × d_min / d` при `d < BDR`. Clamp `[120, 9300]` (155°). Без CQB-extra и без пистолетного пола 200°.
- `JAZZ-COMBAT-009-REQ-002` — `GetOverwatchConeParam`: `MinRange = Max(2, DivRound(BDR, 2))` (50% BDR, включая M2); `MaxRange = WeaponRange` (не 80% WR и не sight в aim UI). Emplacement `min_distance_2d` не менять.
- `JAZZ-COMBAT-009-REQ-003` — якоря: Glock на BDR → 5400; на `d_min=4` → 9300 (155° cap). CZ75 `d=5` → 7560 (уже, чем `d_min`). MP5A4 4320, `d_min=5` → 8640 (144°). AK-74 `d_min=8` → 2640 (44°). M1897 на `d_min` → не ниже 6000 (100°). ПКМ на `d_min` → 2400 (40°); на BDR → 600; на R → 120. Обвес, режущий `OverwatchAngle` или BDR, двигает кривую.
- `JAZZ-COMBAT-009-REQ-004` — confirm пишет в `g_Overwatch.cone_angle` уже скалированный угол; interrupt и LOS читают его.
- `JAZZ-COMBAT-009-REQ-005` — AI (Fallback OW, AI-009 peel) ставит сектор тем же helper по дистанции до якоря.
- `JAZZ-COMBAT-009-REQ-006` — aim-конус Overwatch/MGSetup/MGRotate красится `GetCTHColor(preview_cth)` **только в IMode**; preview = виртуальный Standing/Torso без укрытия и без attacker CTH-дебафов; геометрия 0% остаётся 0%; возможный выстрел ≥ 2%. После confirm сектор игрока и врага — ванильный материал, без CTH-fill.
- `JAZZ-COMBAT-009-REQ-007` — боевой interrupt CTH не использует preview-флаг: живая цель, укрытие, стойка, дебафы как сейчас.
- `JAZZ-COMBAT-009-REQ-008` — карточка / `Overwatch Width` = authored = ширина **на BDR**. Player docs объясняют скейл и полоску на maxrange.

## Инварианты и ограничения

- Не второй wrap на `GetAreaAttackParams` / area-aim: скейл вшить в существующий JAZZ override. Перед сдачей wrap: `python docs/tools/_check_lua_wrap_cycles.py`.
- Новые `_G` имена — через `$jazz-lua-globals` / `rawset`, не голое присвоение.
- `BulletHell` / `DanceForMe` / `JAZZ_TargetSweep` / `JAZZ_VovaVist` / `EyesOnTheBack` не меняют угол от `d`.
- Suppression pinned по-прежнему снимает OW (HOTFIX-003); preview это не обходит.
- Save: в `g_Overwatch` уже есть `cone_angle`; пишется новое значение, схема не меняется. Старый сейв со старым углом до перепостановки сектора остаётся со старой шириной.
- Network: угол детерминирован от authored + целочисленный `d`; тот же helper на клиенте/хосте.
- Не трогать `items.lua` / `metadata.lua` в этом change set, кроме revision при коммите по правилам пакета.
- Якорь угла — property `BulletDropRange` (после barrel multiply), не optic `E`. Короткий ствол двигает кривую через BDR (×70%), не через CloseRange-надбавку к углу.

## Acceptance criteria

- `JAZZ-COMBAT-009-AC-001` — static: Glock `d_min=4` → 9300, `d=BDR` → 5400. CZ75 `d=5` → 7560 (< `d_min`). MP5A4 `d_min=5` → 8640. AK-74 `d_min=8` → 2640. M1897 `d_min` ≥ 6000. Мосин `d=66` → 120. ПКМ `d_min=9` → 2400, `d=BDR` → 600. Меньший BDR на том же `d` внутри обеих зон — уже угол.
- `JAZZ-COMBAT-009-AC-002` — runtime/human: пистолет/`d_min` — широкий веер (~155°), при уводе курсора **только сужается** (не растёт). ПП на `d_min` заметно шире АК (≈144° vs ≈44°); дробовик в дверном проёме ≥100°. Пулемёт MGSetup на `d_min` заметно толще, чем на BDR (ПКМ 40° vs 10°). Винтовка/пулемёт на maxrange — полоска. Клик ближе 50% BDR отщёлкивается на `d_min`.
- `JAZZ-COMBAT-009-AC-003` — runtime: confirm на `d_min` и на R пишет разные `g_Overwatch.cone_angle`; враг на краю широкого ближнего конуса ловит interrupt, на том же азимуте у дальней полоски — нет.
- `JAZZ-COMBAT-009-AC-004` — human: aim Overwatch красит конус шкалой `GetCTHColor` (белый ≥100 / синий ≥85 / зелёный ≥60 / жёлтый ≥40 / оранжевый ≥20 / красный >0 / чёрный 0). Дальняя открытая клетка холоднее близкой. Стрелок с Pain/suppression видит **не** чёрный конус на открытой клетке в BDR. Клетка за глухой стеной — чёрная.
- `JAZZ-COMBAT-009-AC-005` — runtime: interrupt по реальной цели в укрытии / под Pain всё ещё считает обычный CTH (может быть 0%); preview на постановке на ту же плиту без юнита — ненулевой, если LoF стоячему торсу есть.
- `JAZZ-COMBAT-009-AC-006` — static/runtime: `DanceForMe` / `BulletHell` угол не зависит от `d`; `GetOverwatchConeParam("Angle")` = authored; `MinRange = Max(2, 50% BDR)`, `MaxRange = WeaponRange`.
- `JAZZ-COMBAT-009-AC-007` — docs: technical combat-cth-actions + combat-actions; wiki + showcase RU/EN описывают скейл, якорь на BDR, полоску на maxrange и цвет; «Overwatch Width» на карточке = ширина на BDR.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ уже override `GetAreaAttackParams`, `IModeCombatAreaAim`, `CalcChanceToHit`. Меняется только OW/MG cone + aim tint. Vanilla фиксированный угол и `WeaponAOE` цвет уходят для этих трёх action id.
- Saves: старый поставленный сектор сохраняет записанный `cone_angle` до отмены/перепостановки. Новый tint не обязан сериализоваться (можно пересчитать от `target_pos`).
- Network/determinism: integer `MulDivRound`; без float в угле.
- Generated data: нет.
- Cross-package: нет. `jazz-units` AI архетипы не меняются; runtime AI в `jazz` читает тот же угол.
- Rollback/recovery: выключить скейл в helper → authored константа; убрать tint → `WeaponAOE`.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent after `approved`
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner
- Дата: 2026-08-30

## Evidence

- `JAZZ-COMBAT-009-AC-001`: `PASS` (static) — `python docs/tools/_test_combat_009_ow_cone.py` (после playtest: cap 155°, MG квадрат, M2 min = 50% BDR). `BLOCKED` (runtime) — живой helper в JA3.
- `JAZZ-COMBAT-009-AC-002`: `BLOCKED` — runtime/human.
- `JAZZ-COMBAT-009-AC-003`: `BLOCKED` — runtime.
- `JAZZ-COMBAT-009-AC-004`: `BLOCKED` — human.
- `JAZZ-COMBAT-009-AC-005`: `BLOCKED` — runtime.
- `JAZZ-COMBAT-009-AC-006`: `PASS` (static) — DanceForMe/BulletHell по-прежнему сырой `OverwatchAngle`; `GetOverwatchConeParam` Angle/Min/Max в helper. `BLOCKED` (runtime).
- `JAZZ-COMBAT-009-AC-007`: `PASS` (static) — technical + wiki + showcase RU/EN.

## Documentation delta

Обновлено: `docs/technical/systems/combat-cth-actions.md`, `docs/technical/weapons/combat-actions.md`, `accuracy-model.md`; `docs/wiki/combat-and-accuracy.md`, `combat-actions.md`, `weapons-and-ammo.md`; showcase RU/EN `combat-and-accuracy` + `combat-actions`. Generated `docs/wiki/weapons/*` не трогались.
