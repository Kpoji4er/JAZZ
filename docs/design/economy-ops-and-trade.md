# Economy: satellite ops + trade (backlog)

Статус: **design backlog** для ECON-001…003; **ECON-004 Bobby Ray** — runtime loaded 2026-08-07 (spec ещё `draft`, Evidence частично static). Current-state магазина: [bobby-ray-shop.md](../technical/systems/bobby-ray-shop.md).

Связанный долг того же класса (не в этой четвёрке): **Rothman** mine oversee op — текст перка есть, runtime нет (`docs/design/mercs-ja12/rothman.md`).

## Карта фич → specs

| # | Фича | Spec | Статус |
| --- | --- | --- | --- |
| 1 | Livewire: городской заработок (операция) | [JAZZ-ECON-001](../specs/active/JAZZ-ECON-001.md) | draft |
| 2 | Порт: операция продажи лута (в т.ч. алмазов) | [JAZZ-ECON-002](../specs/active/JAZZ-ECON-002.md) | draft |
| 3 | JA2-style купля-продажа с квестовыми NPC | [JAZZ-ECON-003](../specs/active/JAZZ-ECON-003.md) | draft |
| 4 | Bobby Ray: 5 тиров, restock/цена по Δтира | [JAZZ-ECON-004](../specs/active/JAZZ-ECON-004.md) | draft / runtime loaded (формулы locked) |

## 4. Bobby Ray — тиры / restock / цена (ECON-004)

**Design principles (owner):** полезный, не ультимативный; кампания жива без магазина; витрина **не опережает** прогрессию мира (рядом с Легионом, не на major вперёд). Подробности → [JAZZ-ECON-004](../specs/active/JAZZ-ECON-004.md).

**Current (loaded):** unlock **1–5** (TCE: open / ≥2 mines / WorldFlip / ≥4 mines / ≥5 mines); restock soft-tail + ammo boost + staples flat; цена `Cost × (3^Δ|0.3^|Δ|) × jitter` (`Code/System_BobbyRay_ECON004.lua`); catalog Cost/Tier/CAS applied from audits.

**Locked (owner 2026-08-07):** см. spec; runtime соответствует locked формулам.

Черновик каталога + **универсальный `Cost`**: оружие / броня / патроны / consumables / аттачи / **explosives** — `_audit_bobby_*_prices.py` + canvas `bobby-ray-*-prices`.

**Process (owner 2026-08-07):** новый предмет → сразу решение **Bobby in|out** (+ Tier/RW/Cost или причина out). Правило агента: `.cursor/rules/jazz-bobby-ray-new-items.mdc`.

## 1. Livewire — city income op

**Обещание уже в UI:** `InnerInfo_JAZZ` Description — «Открывает операцию по заработку денег в городском секторе (Пока недоступно)». Wired только bonus intel при хаке.

**Locked (owner 2026-08-06):**

- Сектор с городом (`sector.City ~= "none"`), игрок контролирует.
- Livewire в секторе / гарнизоне (точный assign — в ECON-001).
- Длительность **2** дня campaign time.
- Ставка **~1000 $/день**.
- Выплата **lump sum** (не daily tick): полный прогон → **~2000 $**; **при отмене** — за фактически отработанные дни (~1000 $/день, floor по целым дням).
- После ship: убрать «Пока недоступно» из Description; выровнять EN/RU (сейчас EN CSV обрезан / расходится).

Паттерн соседа: Rothman mine op (2 дня, garrison gate) — отдельный spec later.

## 2. Port — sell loot op

**Current:** `sector.Port` = лодки + Bobby Ray delivery multiplier. Отдельной операции сдачи лута нет. Алмазы уже в экономике (`DiamondBriefcase` / `TinyDiamonds`, Legion cargo).

**Intent:**

- Controlled port-сектор → satellite operation «продать / отгрузить лут».
- Очередь предметов со склада/отряда + алмазы → `$` с haircut vs мгновенный Bobby Ray / будущий NPC-shop.
- Не заменяет ECON-003 (локальные торговцы); порт = bulk/export канал.

Числа haircut, whitelist категорий, cooldown — открыты в draft ECON-002.

## 3. Quest NPC buy/sell (JA2-style)

**Current:** Bobby Ray (почта) + точечные give/dialog. Нет полноценного меню продажи как в JA2.

**Intent:**

- Отдельный sell/buy UI с инвентарём торговца.
- Квестовые NPC (кто / что / когда / цены) через конфиг, не хардкод одной реплики.
- Buyback / квестовые locked items — в scope спеки; полный магазин всех граждан мира — non-goal v1.

Крупный UI+economy; не смешивать с ECON-002.

## Порядок реализации (рекомендация)

1. **ECON-001** — маленький, закрывает уже видимый текст перка.
2. **ECON-004** — Bobby Ray тиры/цены (уже locked formulas; нужен approve ladder + catalog).
3. **ECON-002** — порт как второй satellite money sink/source.
4. **ECON-003** — после стабилизации UI shell / inventory patterns.

## Открытые вопросы (вне Livewire payout)

- Livewire: нужен ли cooldown / loyalty gate / heat risk? (cancel = пропорционально — locked)
- Port: % от `Cost` / фиксированные tiers; алмазы по номиналу или haircut?
- Merchant: первый wave NPC (кто именно на Ernie / mainland)?
- Rothman mine op — отдельный ECON-00x или UNITS perk-wave?
