---
name: create-jazz-action-icons
description: >-
  Создавать и обновлять HUD/hotbar action icons JAZZ (CombatAction / signature
  abilities): 108×54 dual-state PNG в стиле JA3 ui/Icons/Hud. Использовать при
  запросе action icon, HUD icon, hotbar icon, Perks/SignatureAbilities,
  Icons/Med CombatAction glyphs или правке Icons/Hud/references/PROMPT.md.
  Не для Personal perk tiles (68×68), status effects (40×40) или ChipIcon.
---

# Создание HUD / action-bar icons

Пакет: `jazz`.  
**Primary runtime output:** `Perks/SignatureAbilities/<ActionId>.png`  
**Style bank:** [`Icons/Hud/references/`](../../../Icons/Hud/references/) (+ [`PROMPT.md`](../../../Icons/Hud/references/PROMPT.md)).  
Шпаргалка: [references/style-and-naming.md](references/style-and-naming.md).

Vanilla SoT (extract, read-only): `<JA3_UI_EXTRACT>/ui/Icons/Hud/*.dds` → PNG bank в `Icons/Hud/references/`.

### Path decision (locked)

| Role | Path |
| --- | --- |
| CombatAction / signature hotbar icons | **`Perks/SignatureAbilities/`** (keep; do **not** move to `Icons/Hud/`) |
| Medical CombatAction glyphs | **`Icons/Med/`** (same *class* of action icon; medical subset — see below) |
| Style references only | `Icons/Hud/references/*.png` (never overwrite for runtime) |

Wire path: `Mod/e6L4ECj/Perks/SignatureAbilities/<file>.png` (or `Mod/e6L4ECj/Icons/Med/<file>.png`).

Asset-only PNG **не** требует spec. Новый CombatAction / смена поведения → `$specify-jazz-change`.  
Смена только `Icon` path: companion + `items.lua` (`$sync-jazz-generated-data`).

### Не путать с другими skill

| Skill | Что это |
| --- | --- |
| **`$create-jazz-action-icons`** (этот) | Hotbar CombatAction glyph, **108×54** dual strip |
| `$create-jazz-perk-icons` | Personal / named perk tile, **68×68** в `Perks/Personal/` |
| `$create-jazz-status-icons` | CharacterEffect HUD, **40×40** в `Icons/StatusEffects/` |
| `$create-jazz-chip-icons` | WeaponComponent ChipIcon, **64×64** |

## Контракт canvas

| | |
| --- | --- |
| Size | **108×54** RGBA (vanilla Hud action strip) |
| Layout | **Два** одинаковых глифа side-by-side: left ≈ cool grey `#B5ADA5`, right ≈ sand cream `#F7F7D6` |
| Background | transparent `A=0` (draft может быть чёрным → key в finalize) |
| Style | flat tactical HUD stencil; soft AA; optional light scanline/distress like vanilla Hud |
| Forbid | текст/буквы/цифры/рамка кнопки/портрет/инвентарный цветной арт |

Некоторые vanilla `perk_*` refs — **54×54** single tile; для JAZZ hotbar CombatAction всё равно писать **108×54** dual strip (как `attack`, `bullseye`, `run_and_gun`).

### Icons/Med (medical-action subset)

`Icons/Med/*.png` — те же HUD action icons для medical CombatActions (bandage, injector, …).  
Текущие файлы часто **108×110** (чуть выше); **не** мигрировать папку в этом skill без явного запроса.  
При новой medical hotbar-иконке: предпочитать **108×54** dual strip в `Icons/Med/` + wire туда; legacy 108×110 допустим только при «заменить пиксели, path не трогать».  
Status-эффекты Bleeding/Pain/Analgesia — **не** этот skill (`$create-jazz-status-icons`).

## Вход от пользователя

1. `ActionId` (имя PNG / CombatAction id, например `Bullseye`, `JAZZ_Bandage`).
2. Символ одним предложением (механика / DisplayName как подсказка).
3. Output: `SignatureAbilities` (default) или `Med`.
4. Нужен ли wire `Icon` в CombatAction/`items.lua` (по умолчанию **да**, если action уже есть).

## Workflow

```text
- [ ] 1. Id, output folder, конфликты имён
- [ ] 2. 2–3 рефа из Icons/Hud/references/ (attack/bullseye/run_and_gun/first_aid/…)
- [ ] 3. GenerateImage (PROMPT.md), aspect_ratio 16:9
- [ ] 4. Finalize → 108×54 transparent PNG
- [ ] 5. Визуальная QA (Read): dual strip, углы A=0, читаемый силуэт
- [ ] 6. Wire Icon path (если просили / action существует)
```

### GenerateImage

1. Прочитать `Icons/Hud/references/PROMPT.md`.
2. `reference_image_paths`: 2–3 PNG из `Icons/Hud/references/` (+ опционально сосед из `Perks/SignatureAbilities/` при QA-regen той же семьи).
3. `GenerateImage`, `aspect_ratio` **`16:9`** (ближе всего к 2:1; finalize жёстко режет в 108×54).
4. Draft на чёрном фоне — норма до finalize.

### Finalize

```powershell
.agents/skills/create-jazz-action-icons/scripts/finalize-action-icon.ps1 `
  -SourceDraft "<path-to-generated.png>" `
  -ActionId Bullseye
```

Medical:

```powershell
.agents/skills/create-jazz-action-icons/scripts/finalize-action-icon.ps1 `
  -SourceDraft "<draft.png>" `
  -ActionId bandage `
  -OutDir "Icons\Med"
```

Скрипт: key near-black → alpha, resize **108×54**, пишет target PNG.

### Визуальная проверка

Read итогового PNG:

- размер 108×54
- угол `(0,0)` с `A≈0`
- два глифа side-by-side (grey + sand)
- нет непрозрачного чёрного кадра; нет текста
- силуэт читается на hotbar scale

### Wire

- `Icon = "Mod/e6L4ECj/Perks/SignatureAbilities/<ActionId>.png"`
- тот же path в `items.lua`
- Med: `Mod/e6L4ECj/Icons/Med/<file>.png`

## Запреты

- Не править / не коммитить ванильные DDS; refs в `Icons/Hud/references/` — read-only style bank.
- Не класть action icons в `Perks/Personal/`, `Icons/StatusEffects/`, `Icons/Items/`, `jazz_assets`.
- Не выдавать Personal perk 68×68 за hotbar action icon.
- Не коммитить абсолютные локальные пути; не пушить без одобрения.
- Не смешивать генерацию иконок с массовым форматированием или несвязанным Lua.
