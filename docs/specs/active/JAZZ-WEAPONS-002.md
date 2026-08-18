---
id: JAZZ-WEAPONS-002
status: implemented
owner: project-owner
systems:
  - weapons-ammo-components
  - inventory-items-loot-crafting
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/GetScrapParts.lua
  - jazz/Code/Inventory.lua
  - jazz/Code/System_SectorOperations.lua
  - jazz/Code/System_Firearm_AddProperties.lua
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/AmmoRolloverHint.lua
  - jazz/items.lua
  - jazz/InventoryItem/*.lua
  - jazz/metadata.lua
  - jazz/Localization/Russian.csv
  - jazz/Localization/English.csv
  - jazz/docs/specs/active/JAZZ-WEAPONS-002.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/systems/inventory-items-loot-crafting.md
  - jazz/docs/design/weapon-repair-parts.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-001
  - JAZZ-ATTACH-001
approved_by: project-owner
---

# JAZZ-WEAPONS-002: ремонт, запчасти, снимаемые обвесы

## Проблема

1. **Слишком много «запчастей» в экономике обвесов** — `FineSteelPipe` / `OpticalLens` / `Microchip` / `Parts` размазаны по ~100+ components; scrap/бонус за `#components` даёт кучу generic `Parts` с тяжёлого мода; игрок тонет в номенклатуре.
2. **Ремонт после перехода на `WeaponResource`** частично сломан: UI/scrap/rollback всё ещё путают `Condition` (0–100) и абсолютный resource (см. gaps после WEAPONS-001).
3. **Нет политики «снял — получил предмет»** vs «вшитый крафт» — всё ставится через ModifyWeapon с расходом материалов; снятие не возвращает прицел/глушитель/фонарь как item.
4. Оптику/лазеры больше не хотим крафтить; крафт — для **неснимаемых** деталей (стволы и т.п.).

Связь: `JAZZ-ATTACH-001` чистит эффекты/ID обвесов; **этот** spec — экономика установки/снятия/ремонта/scrap. Не смешивать commit’ы без нужды.

## Цели

1. Починить **единый источник истины** состояния оружия = `WeaponResource` / `WeaponResourceMax` (UI %, scrap penalty, repair tick, rollback).
2. Сжать номенклатуру расходников до **маленького набора** gunsmith-деталей (число — решение владельца, предложение ниже).
3. Разделить обвесы на **снимаемые** (возврат InventoryItem без уничтожения) и **неснимаемые** (крафт из деталей / только в моддинге с расходом).
4. **Снимаемые** ставятся и снимаются в т.ч. **drag-and-drop**; пороги Mechanical: обычные removable **≥30** = guaranteed, **&lt;30** = шанс; **ГП ≥40** = guaranteed, **&lt;40** = шанс.
5. Стволы требуют **`JAZZ_BarrelParts`** (установка + ремонт).
6. **Не крафтить** оптику и лазеры; крафт — неснимаемые (`Parts` / `JAZZ_BarrelParts`). Старые craft-расходники (`FineSteelPipe`, `OpticalLens`, `Microchip`) **убрать** из игры.
7. Триада ресурса: **current / max / factory**; max **только убывает**, обычный ремонт **не** поднимает max.
8. Max убывает от: **0.5% шанс/выстрел** (loss ≤1 unit), jam ordinary/crit, failed unjam, failed mount (**−1% max**); аттачам resource не даём.
9. Два типа клина: обычный / критический; jam % в **rollover карточки оружия** = эффективный score (поправить существующий виджет).

## Non-goals

- Полный визуальный redesign ModifyWeaponDlg (кроме совместимости со снимаемыми).
- Возврат Handling в CTH (`ATTACH-001` / `WEAPONS-001`).
- Rename всех component id (`ATTACH-001` Phase D) — координировать порядок, не дублировать.
- Массовый ребаланс loot tables всего мода (только источники новых/старых part IDs).
- Броня / `JazzArmorPlates_Scrap`.

Инвентарный drag-and-drop для removable **входит** в scope (не non-goal).

## Предложение: сколько типов деталей

Рабочая таблица (**2** расходника + снимаемые items отдельно) — после замечаний владельца:

| ID (канон) | Display RU / EN | Роль |
| --- | --- | --- |
| `Parts` | (vanilla / «Запчасти» / Parts) | общий ремонт + крафт мебели/мелочи |
| `JAZZ_BarrelParts` | **Ствольные запчасти** / **Barrel Parts** | установка Barrel + доля ремонта |
| `JAZZ_ScopeParts` | **Детали прицелов** / **Scope Parts** | лом Scope при провале снятия; доля ремонта если на стволе remountable Scope |

Канон id: `JAZZ_BarrelParts`, `JAZZ_ScopeParts` (InventoryItem ResourceItem).

**Не вводим по умолчанию:**
- `JAZZ_GunFurniture` — по сути те же `Parts`, отдельный id не нужен.
- `JAZZ_SpringSet` — нет конкретной игровой петли (что именно чинит/крафтит uniquely); не плодить item «на всякий случай». Если позже появится явный кейс (только restore `WeaponResourceMax` после jam) — отдельный micro-REQ.

**Убрать из экономики (items + craft + loot/shop):** `FineSteelPipe`, `OpticalLens`, `Microchip` — **удалить** как расходники.  
**Оставить в gunsmith-экономике:** `Parts`, `JAZZ_BarrelParts`, `JAZZ_ScopeParts`, плюс **InventoryItem аттачей** (removable).  
**Сейвы:** стеки старых расходников конвертировать при load (`FineSteelPipe` → `JAZZ_BarrelParts` 1:1; `OpticalLens`/`Microchip` → `Parts` 1:1).  
**Снимаемые обвесы** — сами InventoryItem, не расходники.

## Политика обвесов

| Класс | Примеры | Снятие | Получение |
| --- | --- | --- | --- |
| Removable | Scope; suppressor; **Compensator**; Side light/laser; рукоятки; **Bipod**; **Mag** (item); **ГП** | DnD; Mech **≥30** (ГП **≥40**); ниже — шанс; провал → −current/−max | loot/shop; не craft |
| Toggle | **Folding stock** (сложил/разложил) | не item — переключение component/state | на стволе |
| Permanent | Barrel; non-fold Stock; Handguard structural; irons | ModifyWeapon + parts | `Parts` / `JAZZ_BarrelParts` |

**Mag:** removable в этом spec как модуль; полная модель **магазин = контейнер патронов** — **backlog** (отдельный change после).  
**ГП:** InventoryItem без атаки вне слота.

### Mechanical и провал

| Операция | Guaranteed | Ниже порога |
| --- | --- | --- |
| Scope / suppressor / compensator / laser-light / grip / bipod / mag install&remove | Mechanical **≥ 30** | **шанс** |
| Подствольник (GL) install&remove | Mechanical **≥ 40** | **шанс** |
| Folding stock toggle | без roll монтажа item (или лёгкий check — default **свободный toggle**) | — |

При **провале** шанса монтажа/снятия: операция не проходит **и** режется **`WeaponResourceMax` на 1%** (`MulDivRound(max, 1, 100)`, минимум 1 если max≥1); current clamp ≤ new max.

**Дополнение (remove fail → break attach):** после −1% max на **снятии** бросок  
`P(break|fail) = Clamp(100 - resourcePct, 0, 95)` (`resourcePct = MulDivRound(current, 100, max)`).  
- Не break → аттач **остаётся** на оружии.  
- Break → слот очищается; **Scope** (не Iron*): в сумку **`JAZZ_ScopeParts` × 1** вместо InventoryItem прицела; прочий remountable → уничтожен без предмета.  
Install fail: только −1% max (без поломки аттача).

### Убывание max — как сейчас vs цель

**Сейчас в коде (факт):**

| Источник | Что режет |
| --- | --- |
| Каждый выстрел (`ReliabilityCheck` + `DegradePerShot`) | только **current** |
| **Неудачный Unjam** (`FirearmBase:Unjam` fail) | **max** на `MulDivRound(max, condLoss, 100)` где `condLoss` ∈ 1..3; current clamp ≤ new max |
| Обычный RepairItems | чинит current (с багами Condition); **max не восстанавливает** |
| Loot spawn | задаёт стартовые current/max от factory |

Исторически max иногда ещё садился от «кривого» ремонта — **не возвращаем**: обычный ремонт только поднимает current.

То есть max сегодня почти не «потихоньку убивается» от стрельбы — только от **кривых разклинов**.

**Цель (зафиксировать контракт):**

| Источник | Max | Current | Примечание |
| --- | --- | --- | --- |
| Выстрелы / `DegradePerShot` | шанс **0.5%** −max | −current всегда | при hit: **не более 1** единицы max |
| **Обычный jam** | **−0.5% max** | jammed | |
| **Критический jam** | **−3% max** | jammed + clamp | P(crit\|jam) — формула ниже |
| Неудачный Unjam | −max (1–3% max) | clamp | оставить |
| **Провал** install/remove | **−1% max** | clamp ≤ new max | |
| Обычный ремонт | **не +max** | +current до max | |
| Factory | неизменен | — | UI reference |

Итог −max: **(1)** 0.5%/выстрел (≤1 unit), **(2)** jam ordinary/crit, **(3)** failed unjam, **(4)** failed mount (−1% max).

### Два типа клина

При срабатывании jam всегда выбирается тип: обычный или критический.

| Тип | −max (от текущего max) | Прочее |
| --- | ---: | --- |
| **Обычный** | **0.5%** | `jammed`; unjam как сейчас |
| **Критический** | **3%** | `jammed` + clamp current; отдельный log/FX |

**P(crit|jam)** — integer, %:

```
resourcePct = MulDivRound(WeaponResource, 100, WeaponResourceMax)   -- 0..100
wear = 100 - resourcePct
mech = Max(0, 100 - Mechanical)                                    -- Mech 0..100+
P = Clamp(5 + MulDivRound(wear, 35, 100) + MulDivRound(mech, 25, 100), 5, 65)
```

| Состояние | Mech | P(crit\|jam) |
| --- | ---: | ---: |
| 100% current/max | 100 | 5% |
| 100% | 50 | ~17% |
| 50% | 50 | ~35% |
| 20% | 20 | ~53% |
| 0% | 0 | 65% |

Не путать с JamScore и с −max 0.5% за выстрел.

### Триада ресурса оружия

| Слой | Поле / смысл | Можно поднять ремонтом? |
| --- | --- | --- |
| current | `WeaponResource` | **да**, до max (`Parts` ± `JAZZ_BarrelParts`) |
| max | `WeaponResourceMax` | **нет** обычным ремонтом; убывает по матрице выше |
| factory | `GetFactoryResource()` | неизменяемый reference |

### Resource аттачам

**Не делаем (зафиксировано).** Провалы и износ — только на оружии.

## Ремонт (починка resource)

- Tick/UI/scrap: только helpers от resource; не сырой `Condition`.
- Rollback: откат **`WeaponResource`** (current).
- Убрать/`перекалибровать` хак `*3`.
- Обычный ремонт: **`Parts`** (как сейчас по формуле tick) **+ `JAZZ_BarrelParts`**:
  - `restoredPct = MulDivRound(restoredCurrent, 100, GetFactoryResource())`
  - `BarrelPartsCost = CeilDiv(restoredPct, 10)` — **1 шт. на каждые 10% factory** (1–10% → 1; 11–20% → 2; …).
  - Если на оружии установлен remountable **Scope** (не Iron*): дополнительно **`JAZZ_ScopeParts`**: `ScopePartsCost = CeilDiv(restoredPct, 20)`.
  - Только current ≤ max; Max **не** покупается обратно RepairItems.
- Установка Barrel (permanent craft/install): отдельно `JAZZ_BarrelParts` по cost таблицы компонента.

## Scrap

- Не масштабировать выплату только от `#components` так, что «весь арсенал Parts».
- Removable перед scrap: auto-eject в инвентарь, потом scrap корпуса → `Parts` + шанс `JAZZ_BarrelParts`.
- Permanent: доля `Parts` / `JAZZ_BarrelParts`, без Lens/Chip.

## Требования

- `JAZZ-WEAPONS-002-REQ-001` — repair/scrap/UI согласованы с триадой **current / max / factory**; обычный ремонт чинит только current ≤ max; max не поднимается RepairItems.
- `JAZZ-WEAPONS-002-REQ-002` — gunsmith: **`Parts` + `JAZZ_BarrelParts` + `JAZZ_ScopeParts`** + removable attach items; furniture → `Parts`; без SpringSet/GunFurniture.
- `JAZZ-WEAPONS-002-REQ-003` — removable: Scope, suppressor, compensator, light/laser, grip, bipod, mag, GL; DnD; Mech **≥30** (GL **≥40**); ниже шанс; провал −current/−max. Folding stock = **toggle**, не item.
- `JAZZ-WEAPONS-002-REQ-003a` — GL InventoryItem без атаки вне слота.
- `JAZZ-WEAPONS-002-REQ-003b` — снимаемые обвесы без resource-триады.
- `JAZZ-WEAPONS-002-REQ-003c` — матрица −max: **0.5%/выстрел** (loss ≤1 unit); ordinary jam −0.5% max; crit jam −3% max; failed unjam; failed mount **−1% max**. RepairItems не +max.
- `JAZZ-WEAPONS-002-REQ-003d` — Mag-as-ammo-container — **backlog**; здесь только removable Mag item.
- `JAZZ-WEAPONS-002-REQ-003e` — remove fail: после −1% max, `P(break|fail)=Clamp(100−resourcePct,0,95)`; break → clear slot; Scope→`JAZZ_ScopeParts`×1; else destroy; no break → attach stays. Install fail: −1% max only.
- `JAZZ-WEAPONS-002-REQ-004` — Barrel install: cost `JAZZ_BarrelParts`. Repair: `CeilDiv(restoredPct_of_factory, 10)` BarrelParts + Parts; if remountable Scope: + `CeilDiv(restoredPct, 20)` ScopeParts.
- `JAZZ-WEAPONS-002-REQ-005` — **удалить** `FineSteelPipe`, `OpticalLens`, `Microchip` (defs, craft costs, loot/shop); component costs → только `Parts` / `JAZZ_BarrelParts`; load-migrate стеки (Pipe→BarrelParts, Lens/Chip→Parts); RU/EN для BarrelParts.
- `JAZZ-WEAPONS-002-REQ-006` — scrap: `Parts` / `JAZZ_BarrelParts`.
- `JAZZ-WEAPONS-002-REQ-007` — generated sync; evidence repair + DnD.
- `JAZZ-WEAPONS-002-REQ-008` — jam % в **rollover карточки оружия**: `GetDisplayJamChancePercent` (поправить существующий виджет).
- `JAZZ-WEAPONS-002-REQ-009` — ordinary/crit jam (−0.5% / −3% max); P(crit|jam) = `Clamp(5 + wear*35/100 + mech*25/100, 5, 65)`.

## Инварианты и ограничения

- `WeaponResource` / `WeaponResourceMax` ids не удалять; сейвы с resource ок.
- Не возвращать Handling в CTH.
- Removable item ids стабильны (новые InventoryItem templates для «прицел как предмет» если сейчас component-only — явно в design doc).
- Координация с `ATTACH-001`: removable list не спорит с Phase D rename; лучше WEAPONS-002 removable **после** или в том же порядке id map.
- Deterministic integer math.

## Acceptance criteria

- `JAZZ-WEAPONS-002-AC-001` — static: UI/scrap/repair на current/max/factory; RepairItems не поднимает max.
- `JAZZ-WEAPONS-002-AC-002` — runtime: DnD; Mech≥30 / GL≥40; провал → **−1% max** + clamp current; ГП без атаки в сумке; аттачи без resource.
- `JAZZ-WEAPONS-002-AC-002b` — human: матрица −max + P(crit) + repair BarrelParts в design.
- `JAZZ-WEAPONS-002-AC-002c` — runtime: remove fail break chance + ScopeParts salvage / non-scope destroy.
- `JAZZ-WEAPONS-002-AC-003` — runtime: ствол + repair: `CeilDiv(restoredPct/10)` `JAZZ_BarrelParts` + Parts; Scope present → + `CeilDiv(restoredPct/20)` `JAZZ_ScopeParts`.
- `JAZZ-WEAPONS-002-AC-004` — runtime: нет free-repair; rollback current.
- `JAZZ-WEAPONS-002-AC-005` — static: нет live refs на `FineSteelPipe`/`OpticalLens`/`Microchip` в craft/loot; defs удалены или dormant; Mag container backlog отмечен.
- `JAZZ-WEAPONS-002-AC-006` — runtime: jam % в rollover карточки оружия = `GetDisplayJamChancePercent`.
- `JAZZ-WEAPONS-002-AC-007` — static/runtime: −max/выстрел шанс **0.5%**, loss **≤1** unit.
- `JAZZ-WEAPONS-002-AC-008` — runtime: ordinary −0.5% / crit −3%; P(crit) по формуле REQ-009.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: overrides scrap/repair + generated components/costs + new items.
- Saves: resource ok; стеки `FineSteelPipe`/`OpticalLens`/`Microchip` → migrate; экипированные optics остаются components до uninstall rules.
- Network: sync install/uninstall/repair.
- Generated data: да.
- Cross-package: нет.
- Rollback: revert write set.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Exclusive: `items.lua`
- Порядок: design table → approve → fix repair sync → part items → removable API → cost migration → scrap table; не блокировать `ATTACH-001` Phase A, но Phase D rename согласовать с removable item ids.

## Решение владельца

- Статус: **implemented** (code loaded; runtime AC remain BLOCKED; AC-005 FAIL — legacy part defs still in metadata).
- 2026-08-01 approved numbers (Mag/Bipod removable, BarrelParts/ScopeParts, P(break)/P(crit), −max/shot).
- 2026-08-18 evidence lock: AC-002 «нет removable каталога» **устарел** — `JAZZ_RemovableAttachment` catalog + DnD в `System_WeaponRemovableModify.lua` / `System_WeaponResourceMaintenance.lua`. Не откатывать каталог. REQ-005 (удалить Pipe/Lens/Chip defs) **ещё open**.
- Зафиксировано:
  - Mag / Bipod / Compensator — removable; Mag-as-container — backlog; Folding stock — toggle;
  - `JAZZ_BarrelParts` = «Ствольные запчасти» / «Barrel Parts»;
  - `JAZZ_ScopeParts` = «Детали прицелов» / «Scope Parts»; remove-fail break + repair surcharge;
  - Repair BarrelParts: **`CeilDiv(restoredPct_of_factory, 10)`**; ScopeParts: **`CeilDiv(restoredPct, 20)`** if remountable Scope;
  - P(break|remove fail): **`Clamp(100 − resourcePct, 0, 95)`**;
  - P(crit|jam): `Clamp(5 + wear×35/100 + mech×25/100, 5, 65)`;
  - −max/выстрел: **0.5%**, loss **≤1** unit; failed mount: **−1% max**;
  - jam UI — существующий rollover; ordinary/crit −0.5%/−3%; Mech 30/GL 40;
  - **удалить** craft-расходники `FineSteelPipe` / `OpticalLens` / `Microchip`; оставить `Parts` + `JAZZ_BarrelParts` + `JAZZ_ScopeParts` + attach items (load-migrate 1:1).

## Evidence

- `JAZZ-WEAPONS-002-AC-001`: `PASS / static` — `Inventory:ItemModifyCondition` maps %→current resource and debits `JAZZ_BarrelParts` / `JAZZ_ScopeParts`; RepairItems does not raise max. `BLOCKED / runtime` sector-op smoke.
- `JAZZ-WEAPONS-002-AC-002`: `PASS / static` — remountable `InventoryItem` catalog (`RemovableAttachments` / `_gen_removable_attachment_items.py`); DnD install/remove via `MoveItem` wrap (`System_WeaponRemovableModify.lua`); Mech 30 / GL 40 in remove/install helpers. `BLOCKED / runtime` in-game DnD + fail −1% max.
- `JAZZ-WEAPONS-002-AC-002b`: `PASS / static` — max-loss constants and critical-jam integer formula present; `BLOCKED / human` matrix review.
- `JAZZ-WEAPONS-002-AC-002c`: `PASS / static` — remove-fail `P=Clamp(100−resourcePct,0,95)` + `JAZZ_DepositScopeParts` / destroy in `System_WeaponResourceMaintenance.lua`. `BLOCKED / runtime` wave test.
- `JAZZ-WEAPONS-002-AC-003`: `PASS / static` — `GetRepairBarrelPartsCost` / `GetRepairScopePartsCost` + `PaySectorOperationResource`. `BLOCKED / runtime`.
- `JAZZ-WEAPONS-002-AC-004`: `PARTIAL / static` — repair current-resource mapping overridden; wave test still required.
- `JAZZ-WEAPONS-002-AC-005`: `FAIL / static` — `FineSteelPipe` / `OpticalLens` / `Microchip` still loaded (`metadata.lua` + companions); load-migrate `JazzLegacyPartMigration` exists, defs not deleted.
- `JAZZ-WEAPONS-002-AC-006`: `PASS / static`, `BLOCKED / runtime` — `RolloverInventoryWeaponBase` jam row calls `GetDisplayJamChancePercent`.
- `JAZZ-WEAPONS-002-AC-007`: `PASS / static`, `BLOCKED / runtime` — `Random(200)==0` per shot, loss ≤1 unit.
- `JAZZ-WEAPONS-002-AC-008`: `PASS / static`, `BLOCKED / runtime` — ordinary/critical max-loss and P(crit) formula.

## Documentation delta

- `docs/design/weapon-repair-parts.md` (новый) — таблица parts + removable matrix.
- `docs/technical/systems/weapons-ammo-components.md` — repair/scrap/resource truth.
- `docs/technical/systems/inventory-items-loot-crafting.md` — part items + craft policy.
- Wiki/showcase — если игрок видит новые детали/снятие (спросить).
- `docs/wiki/weapons-and-ammo.md`, `docs/showcase/ru/weapons-and-ammo.md`, `docs/showcase/en/weapons-and-ammo.md` — added current resource / Barrel Parts / jam-card copy.
- `docs/technical/systems/file-coverage.md` — added the loaded resource-maintenance module.
