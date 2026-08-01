---
id: JAZZ-WEAPONS-005
status: implemented
owner: project-owner
systems:
  - weapons-ammo-components
  - explosives-traps-heavy-weapons
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/WeaponClasses.lua
  - jazz/Code/System_OR_Grenade.lua
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/*Disposable*
  - jazz/InventoryItem/M72LAW.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Localization/Russian.csv
  - jazz/Localization/English.csv
  - jazz/docs/specs/active/JAZZ-WEAPONS-005.md
  - jazz/docs/technical/systems/explosives-traps-heavy-weapons.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/weapons/data/weapons.csv
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
related_specs:
  - JAZZ-GRENADES-001
  - JAZZ-WEAPONS-001
  - JAZZ-WEAPONS-002
approved_by: project-owner
---

# JAZZ-WEAPONS-005: disposable rocket launchers (v1 = M72 LAW)

## Проблема

1. **RPG-7** — многоразовая пусковая с отдельными выстрелами; это правильно.
2. **M72 LAW** в JAZZ уже есть как `RocketLauncher`, но ведёт себя неоднозначно: `Repairable = false`, при этом есть `ReloadAP` — не выглядит как настоящий **одноразовый** launcher (труба + ракета = один предмет, после выстрела ничего не остаётся).
3. Нужен общий контракт disposable launchers под будущую линейку (RPG-18/22, AT4…), без реализации всей линейки сейчас.

## Цели

1. Ввести явный контракт **Disposable Launcher**: один выстрел → launcher **убирается из инвентаря**, перезарядки нет; **модель пустой трубы падает на землю** в точке стрелка (world debris / dropped prop).
2. Применить контракт к **`M72LAW`** в v1 (единственный content-ствол этого spec).
3. **RPG-7** и прочие reloadable rocket launchers **не** менять на disposable.
4. Заложить property/флаг так, чтобы позже добавить линейку без смены runtime-контракта.
5. Docs + wiki + showcase RU/EN (коротко: LAW одноразовый; труба остаётся на земле).

## Non-goals

- Новые модели линейки (RPG-18, AT4, Panzerfaust disposable…) — **позже**; только хук + M72.
- Менять баллистику/урон/mishap RPG-7.
- Underslung 40 mm GL / миномёты.
- Оставлять «пустую трубу» **в инвентаре** как usable weapon — нет.
- WEAPONS-003/004 (recoil / дозарядка) — не смешивать; exclusive `items.lua` координировать.

## Контракт Disposable Launcher

### Свойство

На `RocketLauncher` (или HeavyWeapon):

| Field | v1 |
| --- | --- |
| `DisposableLauncher` | `true` на M72LAW; default `false` |

Альтернатива имени снята: канон **`DisposableLauncher`**.

### Поведение

```text
если DisposableLauncher:
  MagazineSize = 1 (или эквивалент «один выстрел встроен»)
  Reload запрещён / действие Reload недоступно
  после выстрела (атака из этого оружия завершена с расходом «патрона»):
    1. убрать item launcher из инвентаря носителя
    2. заспавнить на земле у стрелка **визуальную пустую трубу** (entity/модель spent tube)
  Repairable = false
  отдельные Ordnance для перезарядки этого ствола не требуются
    (ракета вшита / стартовый ammo Amount=1 при создании предмета)
```

### Spent tube на земле

- Цель: игрок **видит**, что труба выброшена / упала после выстрела.
- Место: сектор/воксель у ног стрелка (или точка атаки), с лёгким физическим/анимационным «падением», если движок позволяет без отдельной physics-sim спеки.
- **v1:** world prop / FX object — **только visual debris**, **не** подбираемый InventoryItem, **без** scrap Parts. Не занимает слот, не чинится, не стреляет. Уборка как обычный combat debris / по правилам сектора.

### M72LAW (v1 content — полный deliverable)

В этом spec M72 доводится **целиком**, не «только флаг»:

- `DisposableLauncher = true`
- Reload недоступен; вшитый один выстрел
- После spent shot: remove из инвентаря + **visual debris** трубы на земле
- **DisplayName / Plural** — читаемые **M72 LAW** (RU/EN), убрать битое «M72LAW2»
- Description / AdditionalHint — одноразовый, труба падает на землю, backblast/mishap как у rocket launcher
- `Repairable = false`; без осмысленного ремонта/перезарядки
- Entity/FX: spent tube использует ту же (или dedicated spent) модельку launcher’а, лежащую на земле
- Cost/Tier/loot — лёгкий sanity pass допустим, не блокер AC

### Краевые случаи

- Mishap / backblast / scatter — как у текущего RocketLauncher path (GRENADES-001).
- Если выстрел не состоялся (отмена до расхода) — LAW не убирать и трубу не спавнить.
- Remove + ground drop — после **любого** расхода выстрела, как у RPG-7 при spent round (hit / miss / **mishap**). Отмена атаки до расхода — без remove/drop.
- Не оставлять orphan OrdnanceVisual на юните после remove.

### Будущая линейка (документировать, не делать)

Тот же флаг + новые InventoryItem; примеры: RPG-18/22/26, AT4, аналог Panzerfaust disposable. Отдельный content-spec later.

## Требования

- `JAZZ-WEAPONS-005-REQ-001` — property **`DisposableLauncher`** на rocket launcher defs; default false.
- `JAZZ-WEAPONS-005-REQ-002` — M72LAW: DisposableLauncher=true; Reload недоступен; после **любого** spent shot (в т.ч. mishap) item уходит из инвентаря и spent tube (visual debris) на земле — паритет spent-round с RPG-7, без Reload.
- `JAZZ-WEAPONS-005-REQ-003` — RPG7: DisposableLauncher=false; по-прежнему перезаряжается отдельными warhead.
- `JAZZ-WEAPONS-005-REQ-004` — отмена атаки до расхода выстрела не удаляет LAW и не спавнит трубу.
- `JAZZ-WEAPONS-005-REQ-005` — spent tube v1 = **visual debris only** (не loot, не scrap, не usable launcher).
- `JAZZ-WEAPONS-005-REQ-006` — M72 **полностью**: DisplayName M72 LAW (не M72LAW2); RU/EN description/hint одноразовости + труба на земле; wiki/showcase; technical.

## Инварианты и ограничения

- Deterministic remove item после spent shot.
- Не оставлять orphan ammo/ordnance visual на юните.
- Exclusive `items.lua` — не параллелить с WEAPONS-002/003/004 без координации.
- Saves: существующий M72 в сейве после патча получает новое поведение с defs.

## Acceptance criteria

- `JAZZ-WEAPONS-005-AC-001` — static: M72LAW DisposableLauncher=true; RPG7 false/absent.
- `JAZZ-WEAPONS-005-AC-002` — runtime: выстрел из M72 → LAW нет в инвентаре; на земле видна spent tube; второго выстрела из того же item нет.
- `JAZZ-WEAPONS-005-AC-003` — runtime: Reload на M72 недоступен / no-op с блокировкой.
- `JAZZ-WEAPONS-005-AC-004` — runtime: RPG7 после выстрела остаётся, можно Reload warhead; трубы на земле нет.
- `JAZZ-WEAPONS-005-AC-005` — human: имя M72 LAW читается; падение трубы видно; пустую трубу нельзя выстрелить снова.
- `JAZZ-WEAPONS-005-AC-006` — docs sync.

## Impact и совместимость

- Vanilla/CommonLib RocketLauncher path + JAZZ WeaponClasses / grenade OR.
- AI с LAW: после выстрела оружия нет — AI должен уметь сменить оружие (минимум не падать; ideal AI follow-up).
- Loot: несколько LAW = несколько предметов.

## План и ownership

- Пакет: `jazz`
- Exclusive: `jazz/items.lua`

## Открытые решения для владельца (до approve)

*Нет открытых пунктов.* Spec **approved**; реализация — по отдельной команде.

**Закрыто направлением владельца (chat):**

- Отдельный draft; линейка later; сейчас **полный M72**.
- Property: **`DisposableLauncher`**.
- Поведение = **как RPG-7** (баллистика / mishap / backblast / spent round), но вместо перезарядки — **одноразовый**: item уходит + visual debris трубы на земле.
- Любой spent round **включая mishap** → consume + drop debris.
- Scrap/loot junk не нужен.

## Решение владельца

- Статус: **approved**
- Кто подтвердил: project-owner (chat 2026-08-01)
- Дата: 2026-08-01
- Решение: approve WEAPONS-005; implement по команде.

## Evidence

- `JAZZ-WEAPONS-005-AC-001`: `PASS (static)` — `M72LAW` has `DisposableLauncher = true`; `RPG7` has no flag and resolves the RocketLauncher default `false`.
- `JAZZ-WEAPONS-005-AC-002`: `BLOCKED (runtime)` — wave test must confirm inventory removal, one-shot behavior and visible non-loot tube after a normal shot and mishap.
- `JAZZ-WEAPONS-005-AC-003`: `PASS (static)` / `BLOCKED (runtime)` — UI availability, `UnitInventory:ReloadWeapon` and `RocketLauncher:Reload` all reject disposable launchers; wave test still needs to exercise Reload.
- `JAZZ-WEAPONS-005-AC-004`: `PASS (static)` / `BLOCKED (runtime)` — reload guards only branch on `DisposableLauncher`; wave test must confirm RPG-7 reloads and does not leave debris.
- `JAZZ-WEAPONS-005-AC-005`: `BLOCKED (human/runtime)` — verify the tube placement, orientation and non-interactivity in the wave.
- `JAZZ-WEAPONS-005-AC-006`: `PASS (static)` — technical, wiki and RU/EN showcase updated.

## Documentation delta

При реализации:

- `docs/technical/systems/explosives-traps-heavy-weapons.md` — disposable rocket launcher contract and wave checklist;
- `docs/technical/systems/weapons-ammo-components.md` — properties and M72/RPG-7 scope;
- `docs/technical/systems/file-coverage.md` — loaded disposable launcher hook;
- `docs/wiki/weapons-and-ammo.md` + `docs/showcase/{ru,en}/weapons-and-ammo.md` — M72 disposable vs RPG-7 reusable.
