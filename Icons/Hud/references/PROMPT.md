# JA3 / JAZZ HUD combat-action icons — style & prompts

Skill: `.agents/skills/create-jazz-action-icons/SKILL.md` (`$create-jazz-action-icons`).  
Style-референсы: **только** PNG в этой папке (+ runtime `Perks/SignatureAbilities/*.png` / `Icons/Med/*.png` при regen).  
Vanilla extract SoT: `ui/Icons/Hud/*.dds` (BC7) → PNG сюда через `scripts/seed-hud-references.py`.

## Canvas

| Свойство | Значение |
| --- | --- |
| Размер | **108×54** RGBA |
| Layout | dual strip: **left** cool grey `#B5ADA5`, **right** sand cream `#F7F7D6` |
| Фон | прозрачный (`A=0`); draft на чёрном keyed в finalize |
| Стиль | flat tactical HUD stencil, soft AA; лёгкий scanline/distress как у vanilla |

Некоторые refs (`perk_*`, `reload_2`, …) — **54×54** single; для JAZZ hotbar всё равно **108×54** dual.

## Path contract

| Output | Path | Wire |
| --- | --- | --- |
| Signature / CombatAction hotbar | `Perks/SignatureAbilities/<Id>.png` | `Mod/e6L4ECj/Perks/SignatureAbilities/<Id>.png` |
| Medical CombatAction subset | `Icons/Med/<Id>.png` | `Mod/e6L4ECj/Icons/Med/<Id>.png` |
| Style bank only | `Icons/Hud/references/*.png` | never as CombatAction.Icon |

Не мигрировать `Perks/SignatureAbilities` → `Icons/Hud/` без явного запроса владельца.

## Рекомендуемые рефы по семье

| Семья | Примеры refs |
| --- | --- |
| Aim / single shot | `attack`, `bullseye`, `steady_does_it`, `distracting_shot` |
| Burst / auto | `burst_fire`, `full_auto`, `suppressive_barrage`, `bullet_hell` |
| Movement shoot | `run_and_gun`, `mobile_shot`, `dash` |
| Melee / special | `melee`, `coup_de_grace`, `hundred_knives` |
| Medical | `first_aid`, `stop_bleeding`, `stop_bandaging_downed` |
| Reload / utility | `reload`, `take_cover`, `overwatch` |
| Signature-like perk actions | `perk_dance_for_me`, `perk_on_my_target`, `perk_reckless_assault`, `perk_bullet_hell` |

## GenerateImage template

```text
Create ONE Jagged Alliance 3 HUD combat-action icon strip matching the reference images EXACTLY.

This icon is for CombatAction ACTION_ID (hotbar action / SignatureAbilities).

Canvas: landscape roughly 2:1 (target 108x54). Solid black draft background (keyed to alpha later).
Layout: TWO identical glyphs placed side-by-side filling the strip.
  - Left glyph: solid fill color approximately #B5ADA5 (cool grey).
  - Right glyph: solid fill color approximately #F7F7D6 (sand cream).
Style: flat 2D minimalist tactical HUD stencil glyph, thick readable silhouette, soft anti-aliased edges,
optional faint horizontal scanline distress like the attached vanilla Hud references,
no smooth gradients, no glossy bevels, no drop shadows, no photo realism, no button chrome/frames,
no text, no letters, no digits, no logos, no portraits.

Keep each half centered and legible at tiny hotbar size. Monochrome per glyph only
(optional very dark inset cuts for internal detail, like vanilla weapon silhouettes).

SYMBOL: SYMBOL

Match line weight, dual-strip layout, and simplicity of the attached JA3 Hud action references.
```

`aspect_ratio`: **`16:9`**. Затем:

```powershell
.agents/skills/create-jazz-action-icons/scripts/finalize-action-icon.ps1 `
  -SourceDraft "<draft.png>" `
  -ActionId ACTION_ID
```

## QA checklist

1. Final PNG is **108×54**.
2. Corner `(0,0)` nearly `A=0`.
3. Two glyphs visible (grey + sand).
4. Symbol matches mechanics; no accidental letters.
5. Not confused with status-effect / Personal perk / inventory art.
