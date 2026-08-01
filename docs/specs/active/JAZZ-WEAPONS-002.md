---
id: JAZZ-WEAPONS-002
status: draft
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
approved_by: pending
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
5. Стволы требуют **`GunBarrelParts`** (установка + ремонт).
6. **Не крафтить** оптику и лазеры; крафт — неснимаемые.
7. Триада ресурса: **current / max / factory**; max **только убывает**, обычный ремонт **не** поднимает max.
8. Max убывает от: **~1% шанс/выстрел**, **критический jam**, failed unjam, failed mount; обычный jam без сильного −max; аттачам resource не даём.
9. Два типа клина: обычный / критический; UI jam % эффективный.

## Non-goals

- Полный визуальный redesign ModifyWeaponDlg (кроме совместимости со снимаемыми).
- Возврат Handling в CTH (`ATTACH-001` / `WEAPONS-001`).
- Rename всех component id (`ATTACH-001` Phase D) — координировать порядок, не дублировать.
- Массовый ребаланс loot tables всего мода (только источники новых/старых part IDs).
- Броня / `JazzArmorPlates_Scrap`.

Инвентарный drag-and-drop для removable **входит** в scope (не non-goal).

## Предложение: сколько типов деталей

Рабочая таблица (**2** расходника + снимаемые items отдельно) — после замечаний владельца:

| ID (рабочее) | Роль | Куда идёт |
| --- | --- | --- |
| `Parts` | общий крепёж / мелочь / «мебель» оружия | обычный Repair; cost Stock / Handgrip / Handguard / прочий permanent без ствола |
| `GunBarrelParts` (или `JAZZ_GunBarrelParts`) | ствольные заготовки/вкладыши | **установка Barrel** + **ремонт** (доля тика или отдельный расход, когда чинят ствольный износ / тяжёлое оружие) |

**Не вводим по умолчанию:**
- `JAZZ_GunFurniture` — по сути те же `Parts`, отдельный id не нужен.
- `JAZZ_SpringSet` — нет конкретной игровой петли (что именно чинит/крафтит uniquely); не плодить item «на всякий случай». Если позже появится явный кейс (только restore `WeaponResourceMax` после jam) — отдельный micro-REQ.

**Убрать из крафта обвесов:** `OpticalLens`, `Microchip` для оптики/лазера; `FineSteelPipe` заменить на `GunBarrelParts` где это ствол, иначе на `Parts`.  
**Снимаемые обвесы** — сами InventoryItem, не расходники.

Было альтернативой 3–4 типа — **снято** в пользу двух, пока пружинам нет роли.

## Политика обвесов

| Класс | Примеры | Снятие | Получение |
| --- | --- | --- | --- |
| Removable | Scope; suppressor; Side light/laser; рукоятки; **ГП-item** | drag-and-drop; **Mech ≥30** (ГП **≥40**) — всегда успех; **ниже** — **шанс**; провал → **урон resource** (оружия; см. ниже) | loot/shop; не craft; ГП без атаки вне слота |
| Permanent | Barrel; Stock (?); Handguard structural; irons | ModifyWeapon + parts | `Parts` / `GunBarrelParts` |

### Mechanical и провал

| Операция | Guaranteed | Ниже порога |
| --- | --- | --- |
| Scope / suppressor / laser-light / grip install&remove | Mechanical **≥ 30** | **шанс** (формула калибруется; растет к 30) |
| Подствольник (GL) install&remove | Mechanical **≥ 40** | **шанс** |

При **провале** шанса монтажа/снятия: операция не проходит **и** режутся **`WeaponResource` (current) и `WeaponResourceMax` (max)** оружия. Величина loss — design table (черновик: как failed unjam, порядка 1–3% от текущего max, плюс current не выше нового max).

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
| Выстрелы / `DegradePerShot` | шанс **~1% или &lt;1%** −max | −current всегда | loss при hit маленький |
| **Обычный jam** | **−0.5% max** | jammed | |
| **Критический jam** | **−3% max** | jammed + clamp | шанс crit зависит от состояния оружия и Mechanical |
| Неудачный Unjam | −max (1–3% max) | clamp | оставить |
| **Провал** install/remove | **−max** | **−current** | |
| Обычный ремонт | **не +max** | +current до max | |
| Factory | неизменен | — | UI reference |

Итог −max: **(1)** низкий шанс на выстрел, **(2)** критический jam, **(3)** failed unjam, **(4)** failed mount.

### Два типа клина

При срабатывании jam всегда выбирается тип: обычный или критический.

| Тип | −max (от текущего max) | Прочее |
| --- | ---: | --- |
| **Обычный** | **0.5%** | `jammed`; unjam как сейчас |
| **Критический** | **3%** | `jammed` + clamp current; отдельный log/FX |

**Шанс, что jam станет критическим** (а не обычным), зависит от:
- **состояния оружия** (хуже current/max → выше шанс crit);
- **Mechanical владельца** (выше Mechanical → ниже шанс crit).

Точная формула P(crit|jam) — design table (например lerp от resource% и Mechanical); не путать с общим JamScore и с −max ~1% за выстрел.

### Триада ресурса оружия

| Слой | Поле / смысл | Можно поднять ремонтом? |
| --- | --- | --- |
| current | `WeaponResource` | **да**, до max (`Parts` ± `GunBarrelParts`) |
| max | `WeaponResourceMax` | **нет** обычным ремонтом; убывает по матрице выше |
| factory | `GetFactoryResource()` | неизменяемый reference |

### Resource аттачам

**Не делаем (зафиксировано).** Провалы и износ — только на оружии.

## Ремонт (починка resource)

- Tick/UI/scrap: только helpers от resource; не сырой `Condition`.
- Rollback: откат **`WeaponResource`** (current).
- Убрать/`перекалибровать` хак `*3`.
- Обычный ремонт: **`Parts`** + по формуле **`GunBarrelParts`**; только current ≤ max.
- Max **не** покупается обратно RepairItems.

## Scrap

- Не масштабировать выплату только от `#components` так, что «весь арсенал Parts».
- Removable перед scrap: auto-eject в инвентарь, потом scrap корпуса → `Parts` + шанс `GunBarrelParts`.
- Permanent: доля `Parts` / `GunBarrelParts`, без Lens/Chip.

## Требования

- `JAZZ-WEAPONS-002-REQ-001` — repair/scrap/UI согласованы с триадой **current / max / factory**; обычный ремонт чинит только current ≤ max; max не поднимается RepairItems.
- `JAZZ-WEAPONS-002-REQ-002` — gunsmith: **`Parts` + `GunBarrelParts`**; furniture → `Parts`; без SpringSet/GunFurniture. Optics/laser не требуют OpticalLens/Microchip.
- `JAZZ-WEAPONS-002-REQ-003` — removable: Scope, suppressor, light/laser, grip, GL; DnD; Mech **≥30** (GL **≥40**) guaranteed; **ниже — шанс**; провал уменьшает **current и max** resource оружия.
- `JAZZ-WEAPONS-002-REQ-003a` — GL InventoryItem без атаки вне слота.
- `JAZZ-WEAPONS-002-REQ-003b` — снимаемые обвесы **без** resource-триады (**зафиксировано: не делаем**).
- `JAZZ-WEAPONS-002-REQ-003c` — матрица −max: (a) шанс/выстрел ~1% или меньше; (b) обычный jam **−0.5% max**; (c) критический jam **−3% max**; (d) failed unjam; (e) failed mount. RepairItems не +max.
- `JAZZ-WEAPONS-002-REQ-008` — UI jam % = эффективный score roll.
- `JAZZ-WEAPONS-002-REQ-009` — два типа клина: обычный (−0.5% max) / критический (−3% max); P(crit\|jam) от **состояния оружия** и **Mechanical**; различимы в feedback.
- `JAZZ-WEAPONS-002-REQ-004` — Barrel install + repair тратят `GunBarrelParts` (+ `Parts` по формуле).
- `JAZZ-WEAPONS-002-REQ-005` — OpticalLens/Microchip не для крафта оптики/лазеров; RU/EN.
- `JAZZ-WEAPONS-002-REQ-006` — scrap без взрыва номенклатуры; documented drop (`Parts` / `GunBarrelParts`).
- `JAZZ-WEAPONS-002-REQ-007` — generated sync; evidence repair + DnD uninstall.

## Инварианты и ограничения

- `WeaponResource` / `WeaponResourceMax` ids не удалять; сейвы с resource ок.
- Не возвращать Handling в CTH.
- Removable item ids стабильны (новые InventoryItem templates для «прицел как предмет» если сейчас component-only — явно в design doc).
- Координация с `ATTACH-001`: removable list не спорит с Phase D rename; лучше WEAPONS-002 removable **после** или в том же порядке id map.
- Deterministic integer math.

## Acceptance criteria

- `JAZZ-WEAPONS-002-AC-001` — static: UI/scrap/repair на current/max/factory; RepairItems не поднимает max.
- `JAZZ-WEAPONS-002-AC-002` — runtime: DnD; Mech≥30 / GL≥40 guaranteed; ниже шанс; провал режет **current и max**; ГП без атаки в сумке; аттачи без своего resource.
- `JAZZ-WEAPONS-002-AC-002b` — human: матрица убывания max + пороги в design.
- `JAZZ-WEAPONS-002-AC-003` — runtime: ствол + repair жрут `GunBarrelParts`/`Parts`.
- `JAZZ-WEAPONS-002-AC-004` — runtime: нет free-repair; rollback current.
- `JAZZ-WEAPONS-002-AC-006` — human/runtime: UI jam % = эффективный score roll.
- `JAZZ-WEAPONS-002-AC-007` — static: шанс −max за выстрел ≤ 1%.
- `JAZZ-WEAPONS-002-AC-008` — runtime: обычный jam ≈ −0.5% max; критический ≈ −3% max; низкий Mechanical / плохой resource повышают частоту crit; log различает типы.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: overrides scrap/repair + generated components/costs + new items.
- Saves: resource ok; старые OpticalLens/Microchip в сумках остаются; экипированные optics остаются components до uninstall rules.
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

- Статус: draft
- Открыто до approve:
  1. Формула repair: когда жрёт `GunBarrelParts`?
  2. Mag / Bipod / Compensator — removable?
  3. Folding stock — toggle или item?
  4. Display RU/EN для `GunBarrelParts`.
  5. Формула P(crit|jam) от resource% + Mechanical; шанс −max/выстрел 1.0 vs 0.5; loss на провале монтажа.
  6. Аудит jam UI.
- Зафиксировано:
  - обычный jam **−0.5% max**, критический **−3% max**;
  - P(crit) ↑ при плохом состоянии, ↓ при высоком Mechanical;
  - max ещё: ~1%/выстрел + failed unjam + failed mount;
  - UI jam % эффективный; DnD; Mech 30/GL 40; `Parts`+`GunBarrelParts`.

## Evidence

- Все AC: `BLOCKED` — до реализации.

## Documentation delta

- `docs/design/weapon-repair-parts.md` (новый) — таблица parts + removable matrix.
- `docs/technical/systems/weapons-ammo-components.md` — repair/scrap/resource truth.
- `docs/technical/systems/inventory-items-loot-crafting.md` — part items + craft policy.
- Wiki/showcase — если игрок видит новые детали/снятие (спросить).
