---
name: jazz-penetration-scales
description: Считать и показывать дробное пробитие JAZZ (PenetrationClass + PenetrationBonus в десятых). Использовать при AmmoRolloverHint, GetAttackPenetrationClass, CaliberModification на pen, UI «Бронебойность»/Penetration, правках формул брони.
---

# Шкалы пробития JAZZ

Пакет: `jazz`. Runtime: `Code/System_ArmorRating.lua` (`GetAttackPenetrationClass`), `Code/AmmoRolloverHint.lua` (`FormatAmmoPenetrationDisplay`), ammo `CaliberModification`.

Technical: `docs/technical/systems/armor-damage-wounds-will.md`, `docs/technical/systems/weapons-ammo-components.md`.

## Две единицы — не смешивать

| Поле | Единицы | Смысл |
|---|---|---|
| `PenetrationClass` | целые классы **1–5** | грубая ступень |
| `PenetrationBonus` | **целые десятые** класса (`+2` = `+0.2`) | тонкая подстройка |

Боевой pen атаки:

```text
weapon_pen = PenetrationClass + 0.1 × PenetrationBonus
```

Источник истины: `GetAttackPenetrationClass(weapon)`.

## Патрон (`CaliberModification`)

- `PenetrationClass` + `mod_mul`: шкала **×1000** (`1000` = ×1 к базовому классу оружия, обычно `1` → итог класс `1`; `2000` → класс `2`).
- `PenetrationBonus` + `mod_add`: те же **десятые**, что у оружия (`-1` → −0.1).
- **Не** ставить `mod_mul = 0` на `PenetrationBonus`: движок делает `MulDivRound(base + add, mul, 1000)` — `mul=0` **зануляет add**. Карточка патрона (`FormatAmmoPenetrationDisplay`) add всё равно показывает, заряженное оружие — нет. Канон: только `mod_add`, mul не задавать (1000).
- Явный `mod_mul = 0` на **классе** — валидный «почти ноль» (соль); не подменять на `1000`.
- `mod_mul == nil` (поле не задано) в UI трактовать как `1000`.

Пример `.45ACP FMJ`: нет `mod_mul` (=×1 → класс 1) + `mod_add = -1` → **0.9**.

## UI: никогда float в `T{}` number-slot

JA3 подставляет число в `T{ "... <pen>", pen = x }` с **усечением к нулю**.  
`0.9` → **`0`**, `2.2` → **`2`**. Это не «ошибка формулы», а формат шаблона.

Правильно — считать **целые десятые**, форматировать строку, отдать `Untranslated`:

```text
tenths = DivRound(mod_mul_or_1000, 100) + mod_add_bonus
display = "W.F"   -- 9 → "0.9", 22 → "2.2"
pen = Untranslated(display)
```

Канон: `FormatAmmoPenetrationDisplay(mod_mul, mod_add)` в `AmmoRolloverHint.lua`. Карточка заряженного оружия: `FormatWeaponPenetrationDisplay(weapon)` через `RolloverInventoryWeaponBase` `CreatePropValText` на `PenetrationClass` (`Untranslated`, не float в `T{}`).

### Запрещённые антипаттерны

```lua
-- ПЛОХО: float в T{} → 0.9 становится 0
pen = (mod_mul / 1000) + mod_add * 0.1
T{ "... <pen>", pen = pen }

-- ПЛОХО: лишний ×10 после DivRound(..., 100) → 202 вместо 2.2
pen = DivRound(mod_mul, 100)
pen = pen * 10 + bonus

-- ПЛОХО: путать /10 (JamScore→%) с десятыми pen
-- BaseJamChance: DivRound(mod_add, 10) .. "%"
-- PenetrationBonus: уже десятые, в UI не делить ещё раз для «процентов»
```

### Допустимо

```lua
-- Бой (математика): float ок
return class + 0.1 * bonus

-- UI:
pen = Untranslated(FormatAmmoPenetrationDisplay(val_mul, val_add))
```

## Чеклист перед сдачей

1. Tooltip `.45ACP FMJ` / любой `bonus=-1` при классе 1 → **0.9**, не 0.
2. FMJ 5.56 `mul=2000`, `bonus=+2` → **2.2**, не 22 и не 202.
3. Jam `%` по-прежнему `DivRound(BaseJamChance, 10)`.
4. Unit DR / object armor / crit pierce вызывают `GetAttackPenetrationClass`, не сырой `PenetrationClass`.
5. Аудит `python docs/tools/_audit_ammo_pen_mul_zero.py` — нет `PenetrationBonus` `mod_mul=0`.
6. Обновить technical, если меняется контракт шкалы или UI.

## Связанные файлы

- `Code/AmmoRolloverHint.lua`
- `Code/System_ArmorRating.lua` — `GetAttackPenetrationClass`, `CalculateArmorRating*`
- `Code/System_OR_Weapons.lua` — object armor
- ammo companions: `InventoryItem/JAZZ_AMMO_*.lua`
