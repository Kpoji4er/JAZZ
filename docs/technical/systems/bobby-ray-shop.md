# Bobby Ray (магазин)

Срез: **2026-08-07** — JAZZ-ECON-004 catalog + restock/price wraps loaded.

## Коротко

PDA-магазин Bobby Ray: **5** unlock-тиров (`UnlockedTier` 1…5). Restock больше не режет пул по `Tier <= U`; вместо этого веса и цены зависят от **Δтира** (и особых правил для патронов / staples). Каталог `Cost` / `Tier` / `CanAppearInShop` / `RestockWeight` прогнан audit→apply.

## Origin

| Слой | Вклад |
| --- | --- |
| Vanilla | `BobbyRayGuns.lua` restock/order/delivery; `BobbyRayQuest` TCE 1–3; Email Tier2/3; shop categories/subcategories |
| CommonLib | без отдельного Bobby overlay в этом срезе |
| JAZZ | `Code/System_BobbyRay_ECON004.lua`; catalog apply; TCE 4–5; Other SubCategories Optics/Magazines/Muzzle/Side/Under/Bipod |

## Unlock ladder

| U | Триггер (quest `BobbyRayQuest`) |
| ---: | --- |
| 1 | open shop (JAZZ: без Ernie gate — см. quest TCE open) |
| 2 | ≥2 mines (`TCE_Tier2Unlock`) |
| 3 | WorldFlip (`TCE_Tier3Unlock`) |
| 4 | WorldFlip + ≥4 mines (`TCE_Tier4Unlock`) |
| 5 | WorldFlip + ≥5 mines (`TCE_Tier5Unlock`) |

Emails 4–5 переиспользуют vanilla `BobbyRayShopTier3Unlocked`. Save с `U≤3` продолжает жить; 4/5 открываются новыми Once-TCE.

## Restock weights

База: `RestockWeight`. Эффективный вес считает `JazzBobbyEffectiveRestockWeight` (wrap `PrepareShopItemsForRestock` / `PickRandomWeightItems`).

| Класс | Правило |
| --- | --- |
| Оружие / броня / аттачи / specialty med / explosives | `RW × 0.1^|T−U|` (хвост `T>U` разрешён) |
| Патроны / Ordnance packs | `T<U` → `×2^(U−T)` cap 8; `T>U` soft-tail; Poor: U1→1 / U2→0.35 / U3→0.08 / U≥4→0 |
| Staples (Meds/Parts/IFAK/Medkit/tools/BlackPowder/Barrel·Scope parts/…) | `RW` flat при `U≥1` |

Ammo ниже unlock дополнительно поднимает `Stock` до `MaxStock × (1+(U−T))` cap ×3 на restock.

## Цены

На restock instance: `Cost_catalog × price_mult(Δ) × jitter[0.8–1.2]`.

- `price_mult`: `3^Δ` если `T>U`, `0.3^|Δ|` если `T<U`, иначе 1.
- Staples: только jitter (без Δ).
- GameRule **BobbyPays** остаётся на vanilla path **после** записи instance `Cost` (порядок: tier/jitter → затем pays).

## UI categories

`CategoryPair` аттачей: `Optics|Magazines|Muzzle|Side|Under|Bipod` → `BobbyRayShopSubCategory` под **Other**.

## Implementation files

- `Code/System_BobbyRay_ECON004.lua` — wraps (loaded)
- `items.lua` — `BobbyRayQuest` TCE 4–5, SubCategories, ModItemCode
- `InventoryItem/*.lua` + `items.lua` — catalog Cost/Tier/CAS/RW/CategoryPair
- Audits/apply: `docs/tools/_audit_bobby_*_prices.py`, `_apply_bobby_catalog.py`, `_patch_bobby_econ004_items.py`

## Spec / design

- Intent: [JAZZ-ECON-004](../../specs/active/JAZZ-ECON-004.md)
- Design pointer: [economy-ops-and-trade.md](../../design/economy-ops-and-trade.md)
- Player: [wiki/bobby-ray.md](../../wiki/bobby-ray.md), showcase `bobby-ray`

## Validation

- Static: `_validate_items_quick.py`; quest ParamId TCE_Tier4/5; SubCategory ids present.
- Runtime AC (вес/цена/Poor fade) — human/console playtest still required for full Evidence PASS.
