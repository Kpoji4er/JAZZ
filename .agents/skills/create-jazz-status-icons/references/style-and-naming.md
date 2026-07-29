# Style & naming — status effect icons

Канон (таблица icon→CharacterEffect→hex, полные промпты):  
`Icons/StatusEffects/references/PROMPT.md`.

Style-референсы GenerateImage: **только** `Icons/StatusEffects/references/*.png`  
(+ runtime `Icons/StatusEffects/*.png` для JAZZ-серий). Не брать UI из extract вне этой папки.

## Canvas

| | |
| --- | --- |
| Size | **40×40** RGBA |
| Background | transparent `A=0` |
| Style | flat HUD glyph, thick silhouette, soft AA |
| Color | monochrome family (+ optional `#242424` inset) |

## Naming

```text
Icons/StatusEffects/<EffectId>.png
Mod/e6L4ECj/Icons/StatusEffects/<EffectId>.png
```

`EffectId` = Id CharacterEffect (или явный ladder suffix: `suppressionLight` … `suppressionPinned`).

## Color → refs (быстрый выбор)

| Семья | COLOR_HEX | Пример рефов |
| --- | --- | --- |
| sand (Buff+) | `#B8B880` | `focused`, `protected`, `well_rested`, `mobility`, `stimmed` |
| red (Debuff−) | `#E03838` | `bleeding`, `wounded`, `tired`, `exposed`, `panic` |
| dark-red | `#981818` | `suppressed`, `arms_pain`, `legs_pain` |
| cream | `#E0D8C8` | `hidden` |
| cyan | `#50A0C8` | `treating` |
| JAZZ ladder | `#C3FF00`→`#FAFF00`→`#FF0000`→`#990300`→`#000000` | `../suppression*.png` |

## Промпт (кратко)

```text
Create ONE Jagged Alliance 3 HUD status-effect icon matching the reference images EXACTLY.

This icon is for CharacterEffect EFFECT_ID (type=EFFECT_TYPE).
Use the same color family as the attached references: solid fill COLOR_HEX.

Canvas: 40x40, square. Solid black draft background (keyed to alpha later).
Style: flat 2D minimalist tactical HUD glyph, thick silhouette, soft AA edges,
no gradients, no bevels, no drop shadows, no textures, no text, no numbers, no frames.

Subject centered, readable at tiny size. Monochrome COLOR_HEX only
(optional very dark inset cuts like vanilla buff icons).

SYMBOL: SYMBOL

Match line weight and simplicity of the attached JA3 status-effect references.
```

Severity:

```text
Same glyph as the attached JAZZ suppression references: three horizontal bullets
stacked vertically, tips pointing right, short motion dashes behind each base.
Change ONLY the solid fill color to COLOR_HEX. Do not redesign the silhouette.
```
