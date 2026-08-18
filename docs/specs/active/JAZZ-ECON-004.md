---
id: JAZZ-ECON-004
status: implemented
owner: project-owner
systems:
  - bobby-ray
  - economy
  - inventory-items
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-ECON-004.md
  - jazz/Code/System_Firearm_AddProperties.lua
  - jazz/Code/*Bobby* (new runtime if needed)
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/InventoryItem/*.lua
  - jazz/docs/technical/systems/*bobby* (or economy/shop page)
  - jazz/docs/design/economy-ops-and-trade.md
  - jazz/docs/tools/_audit_bobby_weapon_prices.py
exclusive_resources:
  - BobbyRayQuest UnlockedTier / TCE unlock ladder
  - InventoryItem.Cost / Tier / RestockWeight / CanAppearInShop
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-ECON-004: Bobby Ray — 5 тиров, restock по совпадению тира, цены по Δтира

## Проблема

1. Vanilla/JAZZ Bobby Ray unlock сейчас только **1–3** (`BobbyRayQuest` / `BobbyRaySetState`), при этом у части предметов (ammo) уже стоят `Tier` 4–5 → они **никогда** не restockятся.
2. Restock берёт weighted random из пула `Tier <= UnlockedTier` без предпочтения «текущего» тира и без мягкого хвоста соседних тиров.
3. Цена покупки = плоский `item.Cost` (used: condition/mods); нет наценки за оружие выше текущего unlock и скидки за «устаревшее» относительно текущего тира магазина.
4. Каталог/цены/shop-flags оружия несогласованы (unique, ~2005 market, Cost outliers) — отдельный apply-pass после утверждения этой спеки и price-таблицы.

Design notes (session 2026-08-07): canvas `bobby-ray-weapon-prices`; audit `docs/tools/_audit_bobby_weapon_prices.py`.

## Design principles (owner 2026-08-07)

Магазин Bobby Ray в кампании:

1. **Полезный, не ультимативный** — даёт опции (замена сломанного, альтернатива луту, дыры в ките), но не закрывает билд / не становится единственным «правильным» источником силы.
2. **Игра без магазина остаётся возможной** — ключевой прогресс и достаточный арсенал доступны через мир (лут Легиона, квесты, сектор-дропы). Bobby не gate-ит обязательные столпы кампании.
3. **Не опережать прогрессию мира** — unlock ladder и витрина идут **рядом** с Легионом/картой, не на тир–два вперёд. «Чуть лучше / другое» в моменте — ок; mid-game покупка endgame-ствола — нет.

Вывод для authoring:

| Рычаг | Следствие |
| --- | --- |
| Unlock TCE | BR `U` открывается когда мир уже на сопоставимом Legion band (см. rough map ниже); не раньше ключевых story beats без причины |
| `item.Tier` / catalog | оружие BR N ≈ сила мира на этом же участке; BR5 только поздний endgame (AN94 и т.п.) |
| Soft-tail `T > U` | оружие: джекпот `0.1^Δ`/`3^Δ`. **Патроны:** below-U **масса** `2^(U−T)`; Poor fade→0 |
| `RestockWeight` / MaxStock | рары низкий RW; FMJ высокий base; ammo MaxStock boost when `T<U` |
| Цена / Cost | mid-tier не обязан быть дёшевым sink; дорогой хвост не должен быть «дешёвым читом» при раннем `$` spike |

## Цели

- **5** unlock-тиров Bobby Ray (`UnlockedTier` 1…5), примерно параллельно major/sub прогрессии Легиона (**чуть лучше / альтернативное** снаряжение в моменте — не скачок вперёд).
- Restock: **оружие/броня** — макс. вес при `item.Tier == UnlockedTier`, соседи слабее (`0.1^|Δ|`). **Патроны** — отдельно: ниже unlock **чаще** и больше; Poor со временем вытесняется (см. Locked).
- Цена витрины: база `Cost`, затем множитель от **Δтира** (предмет vs текущий unlock); плюс **±20%** jitter на конкретный экземпляр уже в стоке.
- Каталог оружия: без квест-уников / нетипичного ~2005 антиквариата (список в audit); отдельные rare/late исключения (Welrod, De Lisle, AN94…) с низким `RestockWeight` и высоким BR tier.
- Соблюдать design principles выше при ladder, catalog apply и acceptance.

## Non-goals

- Продажа игроком в Bobby Ray (ECON-002/003).
- Полный rewrite PDA UI / delivery defs (Express/Premium/Economy остаются, если не потребует AC).
- Перенос **полного** remountable economy был долгом; **оптика + аттачи** теперь в scope ECON-004 (audit/canvas; apply + CategoryPair/SubCategory — после owner OK).
- Изменение Legion loot tiers (`JAZZ_Legion_Tier` 11–33) — только **ориентир** для unlock ladder Bobby.
- Мгновенный mass-apply всех `Cost` из canvas без отдельного owner OK на таблицу.
- Формулы haircut/buy world ops (ECON-002/003) — только контракт: они читают тот же `InventoryItem.Cost`.

## Locked defaults (owner 2026-08-07)

### Unlock

| Параметр | Значение |
| --- | --- |
| Число unlock-тиров | **5** |
| Параллель Легиону | rough: BR1≈L11–13 · BR2≈21–22 · BR3≈23–25 · BR4≈31–32 · BR5≈33 (точные TCE-триггеры — при approve ladder) |
| Vanilla TCE 1–3 | заменить/расширить до 5; emails для 4–5 |

### Restock weight (шанс встретить)

Базовый вес предмета: `RestockWeight` (authored; default vanilla 100).

#### Оружие / броня / прочее (не Ammo)

```
Δ = |T − U|
tier_mult = 0.1 ^ Δ
# Δ=0 → 1.0 (максимум у текущего unlock)
# Δ=1 → 0.1
# …

effective_weight = RestockWeight × tier_mult
```

- `Tier > U` **может** в пул (джекпот-хвост). **Без потолка по Δ** (owner 2026-08-07).

**Пример — AN94 (BR5, RW=5, Cost≈55000) при `U=1` (Δ=4):** вес `5×0.1^4`; цена `×81 ≈ 4.5M`.

#### Патроны (`Ammo` / shop Ordnance packs) — owner 2026-08-07

Ниже unlock **больше** доступности (ресапплай); выше unlock — тот же мягкий хвост; **Poor** вытесняется.

```
# T, U = item.Tier, UnlockedTier
if T > U:
  tier_mult = 0.1 ^ (T − U)          # soft-tail как у стволов
elif T == U:
  tier_mult = 1.0
else:  # T < U — массовее с ростом магазина
  tier_mult = 2.0 ^ (U − T)          # Δ1→×2, Δ2→×4, Δ3→×8 (cap ×8)
  tier_mult = min(tier_mult, 8.0)

# Poor grade (*_Poor / AmmoPoorColor): fade then drop
if is_poor:
  poor_mult = {1: 1.0, 2: 0.35, 3: 0.08}.get(U, 0.0)  # U≥4 → 0 (вне пула)
else:
  poor_mult = 1.0

effective_weight = RestockWeight × tier_mult × poor_mult
```

Дополнительно на implement: для `T < U` (не Poor) можно поднимать **MaxStock** на restock (`MaxStock × (1 + (U−T))`, cap ×3) — больше пачек в витрине, не только вес ролла.

Пример (`FMJ` T=2, RW=85): при `U=2` вес 85; при `U=4` вес `85×4=340`. `Poor` T=1 при `U=3`: `RW×4×0.08`; при `U=4+`: 0.

#### Медицина / инструменты / ресурсы (Meds·Parts) — owner 2026-08-07

**Staples — вне тира:** доступны с `U≥1`, вес = `RestockWeight` (без Δ).

```
# staples (Meds/Parts/Bandage/Morphine/IFAK/Medkit/tools/gunpowder/barrel·scope parts)
effective_weight = RestockWeight
unit_price = Cost × stock_jitter[0.80, 1.20]
```

**Specialty medicine — soft-tail** (как оружие/броня): owner 2026-08-07.

| Id | BR Tier | Note |
| --- | ---: | --- |
| `Medkit` | **1** | staple flat (не specialty) |
| `JAZZ_SurgicalKit` | **2** | soft-tail |
| `CombatStim` | **3** | soft-tail |
| `MetaviraShot` (Metaviron) | **3** | soft-tail, MaxStock=1 |

Каталог-черновик: audit `_audit_bobby_consumables_prices.py` / canvas `bobby-ray-consumables-prices`.
Staples flat: Meds, Parts, Bandage, Morphine, IFAK, **Medkit**, Lockpick, Wirecutter, Crowbar, BlackPowder, Barrel/Scope Parts.
Rare flat: SkillMag_Medical.
Вне Bobby здесь: craft Microchip/Lens/Pipe, uniques. **Explosives** → отдельный audit `_audit_bobby_explosive_prices.py`.

- `CanAppearInShop == false` / `RestockWeight == 0` / `effective_weight == 0` — вне пула.
- Used vs standard: без смены долей const.BobbyRay, если AC не расширит.

### Цена (витрина / корзина)

База: `item.Cost` (для used — текущая used-формула vanilla **после** tier mult, или base×used_factor×tier_mult — уточнить в implement; v1: tier mult на **catalog Cost**, затем used/condition).

```
Δ_signed = T − U
# оружие / броня / ammo выше текущего unlock-тира магазина:
if Δ_signed > 0:  price_mult = 3 ^ Δ_signed
# ниже:
if Δ_signed < 0:  price_mult = 0.3 ^ (|Δ_signed|)
# совпало:
if Δ_signed == 0: price_mult = 1

stock_jitter ∈ [0.80, 1.20]   # на конкретный экземпляр уже в стоке
unit_price = round(Cost × price_mult × stock_jitter)

# staples medicine/tools/resources (flat):
unit_price = round(Cost × stock_jitter)   # price_mult := 1 всегда
# specialty medicine (SurgicalKit / CombatStim / Metaviron): как оружие — price_mult(Δ)
```

Примеры (`Cost=1000`, `U=3`):

| T | price_mult | до jitter |
| ---: | ---: | ---: |
| 3 | ×1 | 1000 |
| 4 | ×3 | 3000 |
| 5 | ×9 | 9000 |
| 2 | ×0.3 | 300 |
| 1 | ×0.09 | 90 |

Дополнительно (endgame в early shop), `Cost=55000`, `U=1`, `T=5`: **×81 → ~4.5M**.

Jitter **±20%** только для строки стока (не переписывает `InventoryItem.Cost` в def); детерминизм: seed от shop restock RNG / entry id (не гонять заново каждый PDA open).

### Каталог (черновик, из audit; apply отдельным шагом)

- Вне Bobby: квест-уники; ~2005-нетипичное (StG, Luger, MP40, **MAT-49**, Auto5, Garand, Peacemaker…); PB/RSH12/Scout/… по списку audit.
- В Bobby с оговорками: P38, Thompson, M1897, BAR, Winchester1894, Stoeger; Welrod/De Lisle редко+дорого (BR4); **AN94 только BR5**.
- Пистолеты: family band / overrides **ниже** (owner 2026-08-07).
- Heavy: M79 (BR1), RPG-7 (BR2), China Lake / M72 LAW (BR3), MGL (BR4) — не раньше сопоставимого мира; подствол вне витрины.
- **Catalog DoD vs principles:** каждый BR-tier bucket не должен содержать стволы, которые заметно сильнее типичного Legion loot того же band; «премиум альтернатива» ок, «следующий major Legion» — нет (править `Tier`/исключать, не надеяться только на цену).
- **`Cost` для всех active стволов:** proposed в audit — канон `InventoryItem.Cost` и для `shop=out_*` (antique/квест). Вне Bobby = только `CanAppearInShop=false`; цена нужна для лута и будущих world buy/sell (ECON-002/003).
- **Броня (тот же контракт):** audit `docs/tools/_audit_bobby_armor_prices.py` / canvas `bobby-ray-armor-prices`. Legion-style → `out_legion`; JazzArmor + плиты + NVG по BR 1–5.
- **Патроны:** audit `_audit_bobby_ammo_prices.py` / canvas `bobby-ray-ammo-prices`. Grade ladder; handgun T1–T3 vs gun map; restock: below-U **boost** `2^(U−T)`, Poor fade→0 at U≥4. Cost = pack SSS.
- **Медицина / инструменты / Meds·Parts:** audit `_audit_bobby_consumables_prices.py` / canvas `bobby-ray-consumables-prices`. Flat staples; specialty SurgicalKit BR2 / CombatStim+Metaviron BR3 soft-tail.
- **Оружейные аттачи (вкл. прицелы):** audit `_audit_bobby_attach_prices.py` / canvas `bobby-ray-attach-prices`. Soft-tail; `BR = max(design, earliest Bobby host)`; Cold War optics out; 12× BR4; Eotech BR4; Cost=Parts×100; CategoryPair Optics|….
- **Explosives / grenades / demo:** audit `_audit_bobby_explosive_prices.py` / canvas `bobby-ray-explosive-prices`. Soft-tail; TNT BR1 / C4 BR2 / PETN BR3; fused MaxStock1; grenades BR1–2 (**Smoke BR1**). Out: PipeBomb, ShapedCharge, ToxicGas, mortar. BlackPowder → consumables flat; 40mm → ammo. **Owner OK catalog 2026-08-07** (остальное без правок).

## Требования

- `JAZZ-ECON-004-REQ-001` — `UnlockedTier` поддерживает **1…5**; quest/TCE открывают все пять ступеней; meta `Tier` max ≥ 5 (уже 10).
- `JAZZ-ECON-004-REQ-002` — restock **оружие/броня**: `effective_weight = RestockWeight × (0.1 ^ |T−U|)` (вкл. `T>U`).
- `JAZZ-ECON-004-REQ-002b` — restock **патроны**: `T<U` → `× 2^(U−T)` (cap 8); `T==U` → ×1; `T>U` → `× 0.1^(T−U)`; Poor → `poor_mult` 1.0/0.35/0.08/0 по U=1..4+; optional MaxStock boost for `T<U`.
- `JAZZ-ECON-004-REQ-002c` — restock **staples** (Meds/Parts/IFAK/Medkit/tools…): `effective_weight = RestockWeight` (игнор Δ); доступ с `U≥1`.
- `JAZZ-ECON-004-REQ-002d` — restock **specialty medicine**: SurgicalKit BR2, CombatStim+Metaviron BR3 — soft-tail как оружие (`RW × 0.1^|T−U|`).
- `JAZZ-ECON-004-REQ-003` — цена покупки **оружие/броня/ammo/specialty medicine** = `Cost × price_mult(Δ) × stock_jitter`, где `price_mult = 3^Δ` при `T>U`, `0.3^|Δ|` при `T<U`, `1` при равенстве; jitter ∈ [0.8, 1.2] per stock entry.
- `JAZZ-ECON-004-REQ-003b` — цена **staples** medicine/tools/resources: `Cost × stock_jitter` (без `price_mult(Δ)`).
- `JAZZ-ECON-004-REQ-004` — GameRule `BobbyPays` (если активен) применяется **после** tier/jitter (или явно зафиксировать порядок в implement notes).
- `JAZZ-ECON-004-REQ-005` — delivery tariffs / sector multipliers без регрессии.
- `JAZZ-ECON-004-REQ-006` — catalog pass: `CanAppearInShop` / `Tier` / `RestockWeight` / `Cost` по утверждённой таблице (audit/canvas); **`Cost` apply на все active** (в т.ч. out of Bobby); validate items.
- `JAZZ-ECON-004-REQ-007` — technical current-state + design pointer; wiki/showcase только если player-facing numbers shipped.

## Инварианты и ограничения

- Не ломать PDA cart / shipment / used generation beyond intentional price/weight.
- Save: уже открытый shop с `UnlockedTier≤3` должен продолжать жить; T4/T5 unlock на существующих сейвах — только через новые TCE.
- Determinism: restock picks и stock_jitter от existing Bobby RNG / reproducible seed.
- Не смешивать strategic Legion `$` prices с `InventoryItem.Cost`.

## Acceptance criteria

- `JAZZ-ECON-004-AC-001` — static: quest/effects позволяют `UnlockedTier` 1…5; нет предметов с `CanAppearInShop` и `Tier>5` без причины.
- `JAZZ-ECON-004-AC-002` — static/runtime: оружие при `U=3` вес `T=3`:`T=4`:`T=5` ≈ `W:0.1W:0.01W`.
- `JAZZ-ECON-004-AC-002b` — runtime: патрон `T=2` при `U=4` имеет вес ≈ `4×` base RW; `Poor` при `U≥4` не появляется; при `U=2` Poor ещё реже base (~0.35×).
- `JAZZ-ECON-004-AC-002c` — runtime/static: Meds/Parts/IFAK/Medkit/tools при `U=1` и `U=5` имеют одинаковый `effective_weight` (= RW); цена без Δ-множителя.
- `JAZZ-ECON-004-AC-002d` — static: SurgicalKit Tier=2; CombatStim Tier=3; MetaviraShot Tier=3; soft-tail restock/price.
- `JAZZ-ECON-004-AC-003` — runtime: цена `T=U+1` ≈ 3× базы; `T=U-1` ≈ 0.3×; jitter в [0.8, 1.2] на entry (оружие/броня/ammo).
- `JAZZ-ECON-004-AC-004` — runtime: предмет `Tier=5` может появиться при `U=3` с очень малым весом (не zero pool filter).
- `JAZZ-ECON-004-AC-005` — human: catalog exclusions/exceptions совпадают с owner list (AN94 BR5, Welrod rare, …).
- `JAZZ-ECON-004-AC-006` — docs: technical + design economy pointer; Evidence на каждый AC.
- `JAZZ-ECON-004-AC-007` — human: при типичном `$` mid-game витрина на `U` не читается как «купил кампанию»; без Bobby кампания проходима на Legion/quest loot того же этапа.
- `JAZZ-ECON-004-AC-008` — human/static: BR unlock triggers не открывают `U` раньше rough Legion parallel (AC ladder table); в bucket `T==U` нет стволов на major Legion впереди.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: override `PrepareShopItemsForRestock` / entry cost helpers в `BobbyRayGuns` path (JAZZ Code wrap); quest `BobbyRayQuest` в `items.lua`.
- Saves: старые сейвы с Tier≤3 ok; новый ассортимент после restock.
- Network/determinism: jitter/restock must be synced if coop uses shared shop (проверить vanilla model).
- Generated data: `InventoryItem` Cost/Tier/RestockWeight/CanAppearInShop + items.lua.
- Cross-package: jazz-maps delivery multipliers untouched unless AC.
- Rollback: revert Code wrap + quest TCEs; catalog flags revert via git.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent / owner
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: BobbyRayQuest; InventoryItem shop fields

## Решение владельца

- Статус: **implemented** 2026-08-18 (code + catalog loaded; runtime/human AC remain BLOCKED, not accepted)
- Кто подтвердил: project-owner (чат 2026-08-07 формулы; 2026-08-18 status lock)
- Дата: 2026-08-07 / lock 2026-08-18
- Open before approve (2026-08-07) — закрыто по loaded code, кроме human shelf/ladder:
  1. TCE BR2–BR5: AC-001 static PASS.
  2. BobbyPays × tier × jitter: `System_BobbyRay_ECON004.lua` — BobbyPays after tier/jitter.
  3. Rare MaxStock: AN94 MaxStock=1 в catalog apply.
- Locked дополнительно (owner 2026-08-07): soft-tail **без** `T≤U+1` cap — джекпот вроде early Абакана ок при `0.1^Δ` / `3^Δ` (см. пример AN94).
- Locked (owner 2026-08-07): **staples** medicine/tools/Meds·Parts — flat restock с U≥1; **Medkit BR1** flat; **SurgicalKit BR2**, **CombatStim BR3**, **Metaviron BR3** — soft-tail.
- Process (owner 2026-08-07): при добавлении нового shoppable item — сразу **Bobby in|out** (`.cursor/rules/jazz-bobby-ray-new-items.mdc`).
## Evidence

- `JAZZ-ECON-004-AC-001`: `PASS` (static) — TCE 1–5 + `BobbyRaySetState` 1…5; SubCategories; meta Tier max 10
- `JAZZ-ECON-004-AC-002`: `BLOCKED` — runtime weight ratios (code loaded; playtest)
- `JAZZ-ECON-004-AC-002b`: `BLOCKED` — runtime ammo/Poor (code loaded)
- `JAZZ-ECON-004-AC-002c`: `PASS` (static) — staples set in `System_BobbyRay_ECON004.lua` flat path
- `JAZZ-ECON-004-AC-002d`: `PASS` (static) — SurgicalKit/CombatStim/Metaviron tiers from consumables apply
- `JAZZ-ECON-004-AC-003`: `BLOCKED` — runtime price/jitter
- `JAZZ-ECON-004-AC-004`: `BLOCKED` — runtime Tier5 at U=3 soft-tail
- `JAZZ-ECON-004-AC-005`: `PASS` (static) — catalog apply from audits (`_apply_bobby_catalog.py`)
- `JAZZ-ECON-004-AC-006`: `PASS` (static) — technical + wiki + showcase RU/EN + design pointer
- `JAZZ-ECON-004-AC-007`: `BLOCKED` — human mid-game shelf feel

## Documentation delta

- `docs/technical/systems/bobby-ray-shop.md`, `file-coverage.md`, systems README
- `docs/wiki/bobby-ray.md`; `docs/showcase/{ru,en}/bobby-ray.md` + `pages.json`
- `docs/design/economy-ops-and-trade.md` current pointer
- Tools: `_apply_bobby_catalog.py`, `_patch_bobby_econ004_items.py`, `_audit_bobby_*`, `_gen_bobby_*`
