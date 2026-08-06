# Economy: satellite ops + trade (backlog)

Статус: **design backlog** (2026-08-06). Не current-state. Реализация только через approved specs `JAZZ-ECON-001`…`003`.

Связанный долг того же класса (не в этой тройке): **Rothman** mine oversee op — текст перка есть, runtime нет (`docs/design/mercs-ja12/rothman.md`).

## Карта фич → specs

| # | Фича | Spec | Статус |
| --- | --- | --- | --- |
| 1 | Livewire: городской заработок (операция) | [JAZZ-ECON-001](../specs/active/JAZZ-ECON-001.md) | draft |
| 2 | Порт: операция продажи лута (в т.ч. алмазов) | [JAZZ-ECON-002](../specs/active/JAZZ-ECON-002.md) | draft |
| 3 | JA2-style купля-продажа с квестовыми NPC | [JAZZ-ECON-003](../specs/active/JAZZ-ECON-003.md) | draft |

## 1. Livewire — city income op

**Обещание уже в UI:** `InnerInfo_JAZZ` Description — «Открывает операцию по заработку денег в городском секторе (Пока недоступно)». Wired только bonus intel при хаке.

**Locked (owner 2026-08-06):**

- Сектор с городом (`sector.City ~= "none"`), игрок контролирует.
- Livewire в секторе / гарнизоне (точный assign — в ECON-001).
- Длительность **2** дня campaign time.
- Ставка **~1000 $/день**.
- Выплата **lump sum в конце** операции (не daily tick) → **~2000 $** за полный прогон.
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
2. **ECON-002** — порт как второй satellite money sink/source.
3. **ECON-003** — после стабилизации UI shell / inventory patterns.

## Открытые вопросы (вне Livewire payout)

- Livewire: нужен ли cooldown / loyalty gate / heat risk?
- Port: % от `Cost` / фиксированные tiers; алмазы по номиналу или haircut?
- Merchant: первый wave NPC (кто именно на Ernie / mainland)?
- Rothman mine op — отдельный ECON-00x или UNITS perk-wave?
