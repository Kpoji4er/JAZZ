---
id: JAZZ-ATTACH-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
  - combat-cth-actions
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/InventoryItem/*.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Code/AccuracyRangeCTH.lua
  - jazz/Code/System_Firearm_AddProperties.lua
  - jazz/Code/System_OR_Unit.lua
  - jazz/English.csv
  - jazz/Russian.csv
  - jazz/Localization/Strings.csv
  - jazz/docs/technical/weapons/data/weapon-component-*.csv
  - jazz/docs/technical/weapons/data/weapons.csv
  - jazz/docs/design/attachments-by-category.md
  - jazz/docs/design/attachments-rebalance.md
  - jazz/docs/design/reflex-collimator-tiers.md
  - jazz/docs/design/combat-scope-tiers.md
  - jazz/docs/design/long-scope-tiers.md
  - jazz/docs/design/barrel-tiers.md
  - jazz/docs/design/muzzle-tiers.md
  - jazz/docs/design/magazine-tiers.md
  - jazz/docs/design/stock-tiers.md
  - jazz/docs/tools/_write_attach_design_human.py
  - jazz/docs/tools/_build_attachments_catalog.py
  - jazz/docs/tools/_export_attach_csv.py
  - jazz/docs/tools/_apply_attach_001.py
  - jazz/docs/tools/_promote_vanilla_refs.py
  - jazz/docs/tools/_remove_handling_stat.py
  - jazz/docs/tools/_rebalance_reflex_tiers.py
  - jazz/docs/tools/_rebalance_combat_scopes.py
  - jazz/docs/tools/_rebalance_long_scopes.py
  - jazz/docs/tools/_rebalance_barrel_tiers.py
  - jazz/docs/tools/_rebalance_muzzle_tiers.py
  - jazz/docs/tools/_rebalance_magazine_tiers.py
  - jazz/docs/tools/_rebalance_stock_tiers.py
  - jazz/docs/tools/_split_mag_families.py
  - jazz/docs/tools/_union_mag_family_options.py
  - jazz/docs/tools/_remove_mag_50_ak.py
  - jazz/docs/tools/_cut_muzzle_booster.py
  - jazz/docs/tools/_audit_mag_multiplier.py
  - jazz/docs/tools/_list_mag_profiles.py
  - jazz/docs/tools/README.md
  - jazz/docs/tools/_audit_attach_effects.py
  - jazz/docs/tools/_audit_attach_ids.py
  - jazz/docs/specs/active/JAZZ-ATTACH-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/weapons/accuracy-model.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/wiki/weapons/**
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-001
  - JAZZ-CTH-001
approved_by: project-owner
---

# JAZZ-ATTACH-001: Handling→живые рычаги, CloseRange, гигиена ID, ребаланс слотов

**Один большой спек.** Весь pass по обвесам (оптика, стволы, дуло, магазины, stock/under/bipod/side, абсолютные ёмкости) живёт здесь. Отдельные SPEC-ID на слоты Phase C **не** заводить, пока владелец явно не разрежет.

## Проблема

После `JAZZ-WEAPONS-001` / `JAZZ-CTH-001` поле `Handling` на оружии **inert в CTH**, но ~73 живых `WeaponComponent` всё ещё вешают `*Handling*` эффекты. Игрок видит «цену/бонус», который не бьёт по попаданию. Четыре обвеса (`TacGrip`, `Handgrip_Ergo`, `SigErgoHandGrip`, `HandlingWrap`) — **только** Handling → мёртвые апгрейды. Non-goal `JAZZ-WEAPONS-001` («не перепрошивать `*Handling*` effects») закрыт — пора отдельным изменением.

## Цели

1. **Рефакторинг данных/инструментов**: единый реестр «живой рычаг / legacy / visual-only»; каталог и design-doc помечают dead Handling; генератор human-описаний не продаёт Handling как боевой эффект.
2. **Замена устаревших параметров**: все `*Handling*` / `Cumbersome` на **active** обвесах либо сняты, либо заменены на живые рычаги по матрице ниже; Firearm property `Handling` **удалён** (owner follow-up 2026-08-01).
3. **Ребаланс аттачей (Phase C, один pass):** роли и числа по слотам — Scope / Barrel / Muzzle / Magazine / Stock / Under / Bipod / Side — всё в этом SPEC; каноны в `docs/design/*-tiers.md`. Mag size — **абсолютный Set**; mag-well **families** (REQ-017).
4. **Гигиена ID**: нужным live-обвесам — префикс `JAZZ_` (как у оптики); ненужные/неиспользуемые comps и Mount-слоты (ошибка импорта — mount только в Visuals) — удалить.

## Non-goals

- Удаление GameTerm/локализационных строк «Эргономика» вне weapon property (исторические T-ID могут остаться в CSV).
- Возврат Handling в CTH или overwatch.
- Rewrite формулы CTH / optic_reach (контракт `accuracy-model.md` остаётся).
- Массовый ребаланс базовых статов стволов (`weapons.csv` base Accuracy/Damage) вне эффекта обвесов.
- Новые механики «snap shooting» / отдельный hip-fire stat (если понадобится — отдельный spec).
- Иконки / chips UI (`JAZZ-UI-001`) кроме обновления путей Icon/ChipIcon при rename и текстов эффектов в hints при необходимости.
- Сохранение vanilla component id «на всякий случай» без live wiring.

## Матрица замены (норматив)

| Legacy effect | Бывший смысл | Замена по умолчанию | Когда снимать без замены |
| --- | --- | --- | --- |
| `ScopeHandlingReduce` | «тяжёлая оптика» | уже есть цена: `IncreaseShotAP` / `ScopeOverwatchAngleDecrease*` / `MinAim` / `IncreaseMaxAimActions` — **снять** Handling; при дыре в цене усилить существующий рычаг (AP или OW), не плоский CTH | коллиматор с мелким Handling (−1…−3) → снять |
| `MagazineHandlingDecrease` | тяжёлый магазин | оставить/усилить `IncreaseReloadAP`, `ReduceReliability`, `ReduceAimAccuracy15Percent` | если магазин уже имеет reload+jam+AA — снять Handling |
| `MagazineHandlingIncrease` | лёгкий магазин | оставить/усилить `ReduceReloadAP`, `IncreaseReliability` | то же |
| `BarrelHandlingIncrease` (короткий) | «удобный коротыш» | снять Handling; −R/−BDR; near↓ (пистолет → упор; винтовка → окно ближе); ShootAP− только в budget ±1 | не дублировать ShootAP− |
| `BarrelHandlingReduce` (длинный) | «тяжёлый ствол» | снять Handling; +R/+BDR/Grouping; near↑; Recoil↓; **не** ShotAP+ за тяжесть | если оптика уже +1 AP — ствол без ShotAP |
| `SilencerHandlingReduce` / `Decrease` | неудобный глушитель | оставить jam / Grouping / Silent — снять Handling | — |
| `GripHandlingIncrease` | эрго рукоять | **`RecoilDecrease` (Recoil=1..2)** | visual-only если слот нужен только под меш |
| `StockHandlingIncrease` | лёгкий приклад | уже есть Recoil+/ShootAP− / AimAccuracy− на folded — снять Handling | — |
| `GLHandlingDecrease` | тяжёлый ГП | `IncreaseShotAP` на носителе **или** оставить только `GrenadeLauncher` (открытие режима = цена сама) | предпочтительно снять без AP, если ГП и так situational |
| `BipodsHandlingDecrease` | сошки тяжёлые | оставить prone bonuses; снять Handling | — |
| `Cumbersome` | громоздкий | `IncreaseReloadAP` и/или `ReduceAimAccuracy15Percent` / `RecoilIncrease` | — |

Инвариант: **не** компенсировать снятый Handling плоским `+CTH` / `MinorAccuracyBonus` / `LaserCTH`-style на оптике.

## Фазы

### Phase A — рефакторинг (без изменения баланса чисел)

- Классификатор эффектов в tools: `live` / `legacy_handling` / `legacy_flat` / `visual`.
- Design doc + catalog: бейдж «legacy Handling (не в CTH)».
- Audit TSV: список comps с Handling и proposed replacement (dry-run).
- Spec table выше = канон замены.

### Phase B — замена параметров (generated data)

- Companion `InventoryItem` + `items.lua` + CSV sync для всех затронутых components.
- Снять все `*Handling*` / `Cumbersome` с **live** options; применить матрицу.
- Pure-Handling comps (`TacGrip`, `Handgrip_Ergo`, `SigErgoHandGrip`, `HandlingWrap`): либо `RecoilDecrease`, либо visual-only (решение владельца в approve).
- Поле `Handling` на Firearm **удалить** вместе с WeaponPropertyDef / GameTerm / ChanceToHitModifier presets (owner 2026-08-01).

### Phase B2 — удаление лишних `ModItemWeaponComponentEffect`

После того как comps больше не ссылаются на эффект — удалить **mod-owned** preset из `items.lua` (+ metadata sync), если он не нужен иначе.

**Уже orphan (0 comps) — кандидаты сразу:**  
`ScopeCTHBonus`, `ScopeAccuracyIncreace`, `ScopeAccuracyReduce`, `ReduceRange50Percent`, `ReduceAuto50Percent`, `ReduceAimAccuracy50Percent`, `ReduceAimAccuracy80Percent`.

**Оставить (не удалять):**  
`PointBlankBonus`, `TwoHanded` — свойства/флаги оружия; effect-preset тоже оставить, пока не мигрируем PointBlank → `CloseRange*`.

**После strip Handling — удалить presets:**  
`ScopeHandlingReduce`, `SilencerHandlingReduce`, `SilencerHandlingDecrease` (если есть), `MagazineHandlingDecrease/Increase`, `BarrelHandlingIncrease/Reduce`, `GripHandlingIncrease`, `StockHandlingIncrease`, `GLHandlingDecrease`, `BipodsHandlingDecrease`, `Cumbersome` (если Cumbersome только как component effect и не property).

**Не удалять:** vanilla/CommonLib effects; живые рычаги (Recoil, ShotAP, Mag, Silent, optic mag…); `PointBlankBonus`, `TwoHanded`.

### Именование ближней зоны (вместо PointBlank)

Старый `PointBlankBonus` — булевый/legacy «можно в упор». Целевая модель — непрерывный профиль. Канон имён (Firearm + barrel modifiers):

| Поле | Смысл |
| --- | --- |
| `CloseRange` | тайлы: ниже этого — ближняя неэффективность (0 = нет зоны, типичный пистолет) |
| `CloseRangeFactor` | множитель CTH на `d = 0` (1.0 = без штрафа; &lt;1 хуже в упор); к `CloseRange` поднимается до 1.0 |

Ствол сдвигает эти поля (short → меньше `CloseRange` / выше factor; long → наоборот).  
Оптика отдельно: `OpticMinRange` / `OpticNearFactor` — поверх, не вместо.  
`PointBlankBonus` пока **не удалять**; после ввода `CloseRange*` — отдельным micro-pass deprecate/скрыть.

### Phase C — ребаланс ролей (единый pass, один спек)

Числа — в `docs/design/*-tiers.md` + `attachments-rebalance.md`. Новые слоты/идеи → дописывать сюда (REQ/AC), **не** плодить `JAZZ-ATTACH-00N` на каждый слот.

| Слот | Статус | Канон |
| --- | --- | --- |
| Reflex / Combat / Long / Night | **settled** | `reflex-collimator-tiers.md`, `combat-scope-tiers.md`, `long-scope-tiers.md`; optic AA% только при активной оптике |
| Barrel | **applied** | `barrel-tiers.md` — BDR **Multiply %**, R ±1, CloseRange*, Recoil |
| Muzzle | **applied** | `muzzle-tiers.md` — Recoil vs Silent; SK↑ с тиром; FlashHider без Silent; `MuzzleBooster` cut; Improvised wide mount by design |
| Magazine | **applied** (size + families) | `magazine-tiers.md` — roles + ReloadAP + `MagazineSizeSet`; mag-well **families** (`…_AK` / `…_AR15` / …); АК expanded = **40** (`MagLarge_30_40`) |
| Stock / Under / Bipod / Side | **applied** | Stock + grips + bipod + side tier docs; Bayonet **distant backlog** |

Целевые роли (рычаги):

| Слот | Роль | Живые рычаги |
| --- | --- | --- |
| Reflex | CQB vs irons | MinAim, −MaxAim, CloseRange soft, AimAccuracy% @ aim≥1; OW без AA% |
| CombatScope 2–4× | mid | AimAccuracy% @ AimLevel, mild near, OW; без ShotAP/crit |
| Scope 6–12× / long | max aim + даль | AimAccuracy% @ high AimLevel, ShotAP, crit, near-tax |
| Night | dark | IgnoreInTheDark* + mild tax |
| Barrel short/long/heavy | дистанция | BDR%, R±1, CloseRange*, Recoil, Grouping |
| Mag small/std/exp/large | ёмкость vs цена | **абсолютный Set** N; ReloadAP −1/+1/+2; Rel/AA только large; **семья mag well** (REQ-017) |
| Muzzle | отдача vs тишина | Recoil vs Silent+jam+Grouping; FlashHider = StealthKill без Silent |
| Under grip | Vertical / Tac·Wrap / Ergo | см. `under-grip-tiers.md` |
| Under GL | режим | GrenadeLauncher (без ShotAP) |
| Bipod | prone | см. `bipod-tiers.md`: один `JAZZ_Bipod` + Under; CTH+10 / +1 shot |
| Side | light / laser / UV | см. `side-tiers.md`: Laser CTH+falloff@5 (исключение); UV night+SK |
| Stock | плечо vs folded | см. `stock-tiers.md` |

Ребаланс не ломает optic_reach контракт (кратность + AimLevel).

### Mag absolute size (Phase C continuation) — data applied; runtime validation pending

Owner 2026-08-01 initially locked the canon as docs-only. The later MagSizeSet data migration adds the preset/resource and rewires `items.lua` plus companions; it does not claim editor/game acceptance.

- Live magazine comps **не** должны использовать `MagazineSizeMultiplier` (после data-pass).
- Канон: эффект **`MagazineSizeSet`** — `ModificationType = "Set"` → `AddModifier(id, "MagazineSize", mul=0, add=N)` (vanilla `SetWeaponComponent` знает только Add/Multiply/Subtract; JAZZ патчит ветку `Set`).
- Display «Магазин на 45» ⇒ параметр **`MagazineSize = 45`** (перезапись), не `+15` и не `×150%`.
- `MagNormal` — без size-эффекта (база оружия).
- Shared `JAZZ_MagLarge` (×166) **разрезать** по целевой ёмкости (50 / 28 / …), не один Multiply.
- Evidence AC-010: static data pass; editor/runtime smoke remains `BLOCKED`.

### Mag families / mag well (Phase C continuation) — owner 2026-08-01

Съёмный магазин — InventoryItem с `Id == component id`. Один shared id на несовместимых платформах (АК + M16) = один предмет ставится на оба — **запрещено**.

- Канон семей: `docs/design/magazine-tiers.md` § «Семьи магазинов».
- Public id: `JAZZ_Mag*_<Family>` для expanded/large/quick/small/fine/drum, которые иначе шарились бы между семьями (`_AK`, `_AR15`, `_SIG`, `_MP5`, …).
- Внутри семьи — union options (`_union_mag_family_options.py`): магазин АК ставится на **РПК**, не на AR15.
- АК expanded ёмкость: **40** (`JAZZ_MagLarge_30_40`); **не** заводить `MagLarge_50_AK`.
- `JAZZ_MagNormal` остаётся универсальным заводским placeholder (не remountable-каталог семей).
- Apply: `_split_mag_families.py` (+ InventoryItem companions); accepted save break на rename component id (как Phase D).
- Tools: `_split_mag_families.py`, `_union_mag_family_options.py`, `_remove_mag_50_ak.py`.

### Phase D — префикс `JAZZ_`, удаление мусора, Mount → только Visual

Аудит сейчас (`docs/tools/_audit_attach_ids.py`): ~178 live comps; **36** уже с `JAZZ_`/`Jazz_`; **~142** без префикса; **~55** comps ни разу не в options; Mount-слот на active: AUG / M60E3 / M60E4 / PKM (ошибка импорта).

**Правила:**

1. **Нужный live-обвес** (modifiable или default на active, не Mount) → id с префиксом **`JAZZ_`** (канон как оптика: `JAZZ_BarrelLong`, `JAZZ_MagLarge`, …). Уже `JAZZ_*` не трогать без нужды; `Jazz_*` (iron/G36) → выровнять на `JAZZ_*` в том же pass или следом.
2. **Неиспользуемые** — нет ни одной строки в `weapon-component-options` (и не единственный Visual-якорь, который нельзя заменить Entity на оружии) → **удалить** component + ссылки из items/companions. Список стартовый: orphan ~55 (`LROptics*`, `CAR15Mount`, `AdvancedHOLO`, …) — финальный TSV в Phase A.
3. **Mount не слот обвеса.** Убрать `ComponentSlots` / `AvailableComponents` с `Slot=Mount`. Меш крепежа живёт только в **Visuals** нужного боевого/дефолтного компонента (или дефолтном visual оружия). Comps `slot=Mount` (`AUGMount`, `CAR15Mount`, `G3Mount`, `M60E3HandGrip`, `M60E4ModernMount`, `PKMModern`, …) — либо удалить, либо перевести visual на владельца и удалить как отдельный attach.
4. **Empty/broken ids** (например `component_id=","`) — вычистить.
5. Rename = транзакция: `UndefineClass`/`DefineClass` id, все `AvailableComponents`, defaults, Visuals ApplyTo, Icon/ChipIcon paths если завязаны на id, CSV, chips wiring, localization id refs если есть.
6. **Saves:** смена component id ломает экипированные обвесы в старых сейвах — зафиксировать в Impact как accepted break (или one-shot migrate map — non-goal, если не запросим отдельно).

Порядок относительно B/C: Phase D может идти **после** B (меньше двойной правки effects) или **вместе** с B в одном generated commit, если write set один; не смешивать с несвязанным base-weapon retune.

## Требования

- `JAZZ-ATTACH-001-REQ-001` — ни один компонент, доступный на `catalog_status=active` оружии (modifiable или default), не содержит effects из множества Handling-legacy после Phase B.
- `JAZZ-ATTACH-001-REQ-002` — Firearm property `Handling` **удалён** из defs/данных/UI presets; CTH/overwatch без Handling (`JAZZ-WEAPONS-001-REQ-005` / `JAZZ-CTH-001`). Accepted save break: старые сейвы с полем Handling игнорируют неизвестное поле.
- `JAZZ-ATTACH-001-REQ-003` — замена следует матрице; отклонения только с явной строкой в `attachments-rebalance.md`.
- `JAZZ-ATTACH-001-REQ-004` — Phase C: каждый слот имеет documented tier table (роль + ключ чисел) в `docs/design/*-tiers.md` / `attachments-rebalance.md` до merge в main. Все слоты Phase C — scope этого SPEC-ID.
- `JAZZ-ATTACH-001-REQ-015` — Magazine: ReloadAP ladder small **−1** / expanded **+1** / large **+2**; Rel−/AA− только large; Fine expanded может быть без Reload+.
- `JAZZ-ATTACH-001-REQ-016` — Magazine size: live mag comps без `MagazineSizeMultiplier`; ёмкость — **абсолютный Set** («на 45» ⇒ `MagazineSize=45`); Small тоже Set; shared `%`-MagLarge разрезан по target. Runtime: `MagazineSizeSet` + `ModificationType=Set` → `AddModifier(..., mul=0, add=N)` (`Code/System_WeaponComponent_Set.lua`). Data+Code applied; runtime smoke still in wave test.
- `JAZZ-ATTACH-001-REQ-017` — Magazine **families** (mag well): remountable/expanded/large/quick/small/fine/drum ids не шарятся между несовместимыми платформами; public id `JAZZ_Mag*_<Family>`; внутри семьи (АК↔РПК) — общие options; АК expanded = **40** (`JAZZ_MagLarge_30_40`, без `MagLarge_50_AK`); InventoryItem `Id == component id` на каждый live family mag; канон в `magazine-tiers.md`. Accepted save break на rename id.
- `JAZZ-ATTACH-001-REQ-005` — generated sync: companion + `items.lua` + weapons CSV export согласованы; human design doc пересобран.
- `JAZZ-ATTACH-001-REQ-006` — UI/hints не обещают «Эргономику» как боевой бонус обвеса (если такие строки есть — RU/EN sync).
- `JAZZ-ATTACH-001-REQ-007` — суммарный ShootAP-модификатор от аттачей ∈ [−1, +1]; ни один live comp не даёт `|ShotAP| > 1`.
- `JAZZ-ATTACH-001-REQ-008` — изменения `WeaponRange` / `BulletDropRange` только от Barrel; live short/long barrels **сдвигают BDR** (и обычно R) в ожидаемую сторону.
- `JAZZ-ATTACH-001-REQ-009` — ближняя зона: база на Firearm как `CloseRange` + `CloseRangeFactor`; Barrel только модифицирует. Документировать в `accuracy-model.md` до runtime merge. `PointBlankBonus` сохранить до отдельной миграции.
- `JAZZ-ATTACH-001-REQ-010` — дальностное падение урона/CTH-factor: плато до BDR (урон) / E (CTH); после — ускоряющаяся кривая к полу ~25% у R (не 0). Runtime + `accuracy-model` согласованы; evidence: numeric table на CAR15-классе.
- `JAZZ-ATTACH-001-REQ-011` — лишние mod-owned `WeaponComponentEffect` удалены: (a) orphan flat/legacy кроме whitelist; (b) Handling/Cumbersome presets после снятия с comps. **Whitelist оставить:** `PointBlankBonus`, `TwoHanded`. Property `Handling` **удалён**.
- `JAZZ-ATTACH-001-REQ-012` — каждый live (active, mod|def, non-Mount) component id имеет префикс `JAZZ_`.
- `JAZZ-ATTACH-001-REQ-013` — нет `Slot=Mount` в ComponentSlots/AvailableComponents на active оружии; mount-меши только в Visuals.
- `JAZZ-ATTACH-001-REQ-014` — comps без ссылок в options (и без единственной visual-роли) удалены; audit `unused_components == 0` (whitelist только явный, если понадобится).

## Инварианты и ограничения

- Не возвращать Handling в CTH.
- Не давать оптике плоский CTH взамен Handling.
- **AP budget:** суммарный модификатор стоимости **выстрела** (`IncreaseShotAP` / `ReduceShootAP` и аналоги) от всех экипированных аттачей ∈ **[−1, +1]**. Отдельный компонент не ставит `|ΔShootAP| > 1`. ReloadAP магазинов **не** входит в этот бюджет (это цена ёмкости, не DPS-мультипликатор хода). `ShotAP=2+` на leftover/vanilla optic (`LROptics*`, `ThermalScope`, `JAZZ_Scope_8x_SCROME`) — выровнять до ≤1 или вывести из live.
- **WeaponRange / BulletDropRange** меняют **только** компоненты слота `Barrel` (и явные barrel-меши). Scope/Muzzle/Stock/Mag **не** трогают R/BDR. Ствол **обязан** сдвигать BDR (короткий −, длинный +) — это длина «полного» плато до падения.
- **Кривая после BDR (урон и дальностный CTH-factor):** полный эффект до якоря (урон → BDR; CTH → E = BDR+optic); далее нелинейное падение **с ускорением** (`p > 1`) к полу около **25%** у `WeaponRange`, не к 0. Точные `p`/`floor` — в `accuracy-model.md` до merge runtime. Не компенсировать плоским ±CTH/±Damage на аттачах вне этой кривой.
- **Ближняя зона (`CloseRange` / `CloseRangeFactor`)** — **базовое** свойство оружия (класс/роль): пистолеты ≈ `CloseRange=0` или factor≈1; карабин/AR — умеренно; винтовка/DMR/снайпер — сильнее. Ствол **сдвигает** профиль:
  - короткий на **пистолете** → упор ok (`CloseRange`↓ / factor↑);
  - короткий на **винтовке** → комфортное окно **ближе**;
  - длинный → комфорт **дальше**, вблизи больнее (плюс +BDR/+R).
  Оптика: `OpticMinRange` / `OpticNearFactor` поверх. `PointBlankBonus` не удалять в этом change set.
- Сдвиг профиля стволом — через CloseRange*/BDR/R/Grouping, **не** через плоский ±CTH.
- Не смешивать Phase C mass-tune с несвязанным weapon base retune в одном commit без пометки.
- Cut stubs / dormant — удалять только если unused; не разносить cut-weapon wiring без нужды.
- `ExtraBurstShots` noop policy из WEAPONS-001 не реанимировать без отдельного решения.
- Калибровка «пик ~100% CTH при макс навыках на золотой дистанции» — цель **базового** профиля оружия (`accuracy-model` / weapons base), не обязанность каждого аттача; аттачи сдвигают окно, не ломают потолок.

## Acceptance criteria

- `JAZZ-ATTACH-001-AC-001` — static: audit script `legacy_handling_on_live == 0`.
- `JAZZ-ATTACH-001-AC-002` — static: pure-dead set либо имеет live effect, либо помечен visual-only и не в player upgrade list.
- `JAZZ-ATTACH-001-AC-003` — static: CTH path still ignores Handling (regression vs WEAPONS-001).
- `JAZZ-ATTACH-001-AC-004` — editor: Mod Editor round-trip sample (1 optic, 1 mag, 1 grip) без потери effects.
- `JAZZ-ATTACH-001-AC-005` — human: design doc + catalog показывают живые эффекты словами; нет продажи Handling как CTH.
- `JAZZ-ATTACH-001-AC-006` — runtime/human: 3 smoke kits (reflex CQB, 4× mid, 8×+suppressor) — выбор читается, нет «пустых» эрго-апов.
- `JAZZ-ATTACH-001-AC-007` — static: orphan/legacy flat/Handling effect presets removed per REQ-011; property `Handling` **absent**; `PointBlankBonus`/`TwoHanded` kept.
- `JAZZ-ATTACH-001-AC-008` — static: live non-Mount comps all `JAZZ_*`; no Mount slots on active weapons; unused comps purged per audit.
- `JAZZ-ATTACH-001-AC-009` — static: Phase C tier canons present for Scope/Barrel/Muzzle/Magazine; Stock/Under/Side documented before their apply merge.
- `JAZZ-ATTACH-001-AC-010` — static/runtime: live Magazine without `MagazineSizeMultiplier`; `MagazineSizeSet` absolute; smoke «на 45» → `MagazineSize==45`.
- `JAZZ-ATTACH-001-AC-011` — static/runtime: no cross-family shared remountable mag id (АК expanded ≠ AR15); АК↔РПК share `MagLarge_30_40` / family union; no live `JAZZ_MagLarge_50_AK`; InventoryItem companions exist for family-suffixed mag ids; smoke: `…_AK` item installs on RPK, rejected on M16.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: только JAZZ WeaponComponent data + docs/tools.
- Saves: **Handling property removed** (accepted break / ignored unknown field); **rename component id** — старые сейвы могут потерять/сбросить экипированный обвес (accepted break unless migrate requested).
- Network/determinism: без изменения RNG API.
- Generated data: да, транзакция items + companions + CSV (+ icon paths при rename).
- Cross-package: нет (chips/icons в jazz).
- Rollback: revert write set; WEAPONS-001 Handling-hide остаётся.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive resources: `items.lua`

## Решение владельца

- Статус: **approved**
- Кто подтвердил: project-owner (фиксация в чате 2026-07-31: «пока кажется что хорошо» + явный «зафиксируй спеку»)
- Дата: 2026-07-31
- Зафиксированные решения:
  1. Pure-ergo initially → `RecoilDecrease`; **superseded** grip pass (`under-grip-tiers.md`): Vertical=`RecoilDecrease`; Tac/Wrap=`CloseRangeFactor+5`; Ergo=`AimAccuracy%105`; **без** `FreeWeaponSwap`.
  2. Phase C → **tiered pass** по слотам (не только strip Handling).
  3. GL → Handling off **без** `IncreaseShotAP` (бюджет AP ±1 бережём под оптику/ствол).
  4. Ближняя зона: `CloseRange` + `CloseRangeFactor`; `PointBlankBonus` / `TwoHanded` **оставить**.
  5. После BDR: ускорение к полу **~25%** на R (`p>1`); точные p/floor — в `accuracy-model` при реализации.
  6. Phase D: live → `JAZZ_`; unused удалить; Mount только Visual; rename = accepted save break.
  7. Цель «золотая ~100% при max skill» → **вне** обязательного scope; отдельный base-weapons pass (не блокирует ATTACH-001).
  8. Firearm property `Handling` (WeaponPropertyDef / GameTerm / CTH modifier preset / weapon data) → **удалить** (owner follow-up 2026-08-01).
  9. Phase C = **один большой pass внутри ATTACH-001** (owner 2026-08-01): Scope/Barrel/Muzzle/Magazine/Stock… — не отдельные SPEC.
  10. Optics: specialization (reflex CQB / combat mid / long max-aim); optic AimAccuracy% только при активной оптике.
  11. Muzzle: SK ladder↑; sil без Recoil; FlashHider = StealthKill без Silent; MuzzleBooster cut; Improvised wide = by design.
  12. Magazine: four roles; ReloadAP −1/+1/+2; ёмкость = **абсолютный Set** («на 45» → `MagazineSize=45`) — **data+Code applied** (REQ-016 / AC-010 static PASS; editor/runtime smoke в общем тесте).
  13. Magazine **families** (owner 2026-08-01): mag-well split public ids (`…_AK` / `…_AR15` / …); АК mag на РПК, не на M16; АК expanded = **40** (`MagLarge_30_40`); REQ-017 / AC-011; tools `_split_mag_families.py` / `_union_mag_family_options.py`.
- Новые идеи после approve → новый REQ/AC **в этом** SPEC или явный split; не молча расширять write set без строки здесь.

## Evidence

| AC | Result | Evidence |
| --- | --- | --- |
| AC-001 | `PASS` (static) | `_audit_attach_effects.py`: Handling-ish still on comps: `[]`. |
| AC-002 | `PASS` (static) | Dead-ergo set live per `under-grip-tiers.md`: Vertical Recoil−1; Tac/Wrap CloseRangeFactor+5; Ergo AA%105; `FreeWeaponSwap` off TacGrip_M14. |
| AC-003 | `PASS` (static) | No Firearm `Handling` property/data; CTH path has no Handling (`AccuracyRangeCTH` / WEAPONS-001 regression). |
| AC-004 | `BLOCKED` (editor) | Mod Editor round-trip sample (optic, magazine, grip) — отложено на общий тест волны. |
| AC-005 | `PASS` (human/static) | Catalog + tier docs (Scope…Side); Handling not sold as CTH. |
| AC-006 | `BLOCKED` (runtime/human) | Three-kit in-game smoke — отложено на общий тест волны. |
| AC-007 | `PASS` (static) | Handling/legacy flat orphans removed; whitelist `PointBlankBonus`/`TwoHanded` kept; Firearm `Handling` property/UI presets **removed** (owner 2026-08-01). |
| AC-008 | `PASS` (static) | `_audit_attach_ids.py`: live WITHOUT jazz prefix `0`; Mount `0`; unused `0`. Promoted 9 vanilla_ref → `JAZZ_*` with Visuals (`_promote_vanilla_refs_visuals.py`). |
| AC-009 | `PASS` (static) | Phase C tier canons: Scope/Barrel/Muzzle/Magazine/Stock/Under-grips/Bipod/Side. Bayonet distant backlog (out of AC-009). |
| AC-010 | `PASS` (static) / `BLOCKED` (runtime) | `_apply_mag_size_set.py`: live `JAZZ_Mag*` → `MagazineSizeSet`; generic MagLarge split `_50/_28/…`; `_30_45=45`; `Code/System_WeaponComponent_Set.lua` registered. Runtime smoke «на 45» → в общем тесте. Auto5 barrel LMag multiplier = tracked exception. |
| AC-011 | `PASS` (static) / `BLOCKED` (runtime) | `_split_mag_families.py` + `_union_mag_family_options.py`: family-suffixed mag ids; AK options use `MagLarge_30_40` (40), no `MagLarge_50_AK`; RPK lists AK family mags; AR15 uses `…_AR15`. InventoryItem companions for family ids. Runtime DnD smoke (АК item → RPK / not M16) — wave test. |

Status remains **`approved`** (не `implemented`): закрыть AC-004 / AC-006 + runtime AC-010/AC-011 в общем тесте волны. MagSizeSet + mag families data shipped.

## Documentation delta

- `docs/design/attachments-rebalance.md` — матрица + Phase C status.
- `docs/design/*-tiers.md` — Scope / Barrel / Muzzle / Magazine (incl. **families** + AK=40) / Stock / Under-grip / Bipod / Side + apply scripts.
- `docs/design/attachments-by-category.md` — пересбор после B/C/D.
- `docs/technical/systems/weapons-ammo-components.md` — Handling removed; CloseRange*; JAZZ_ ids; tier pointers.
- `docs/technical/weapons/accuracy-model.md` — floor ~25% after BDR/E; CloseRange*; optic AA% gate; Handling **removed**; Laser falloff/`LaserFullRange`.
- `docs/technical/weapons/data/*.csv` — working-tree export (wiki rebuild: `node scripts/docs/weapons-docs.mjs build` when node on PATH).
- `docs/wiki/` + `docs/showcase/ru|en` — player-facing attachment tradeoffs.
- Tools: `docs/tools/README.md` — apply/rebalance/audit + `_split_mag_families.py` / `_union_mag_family_options.py` / `_remove_mag_50_ak.py`.
