# ChipIcon miniatures — GenerateImage prompts

Skill: `$create-jazz-chip-icons`  
Полная Icon кабинета: `$create-jazz-component-icons` (другой PROMPT).

## Canvas

| | |
| --- | --- |
| Size | **64×64** |
| Path | `Icons/Upgrades/Chips/<ComponentId>.png` |
| Style | ultra-simple flat glyph, thick silhouette, soft AA |
| Color | `#C8C0A8` (optional dark insets) |
| Accent | Night scopes: flat **green glass** (`#2E6B3A` family). Night irons: green tritium dots. Do **not** pass `-Recolor` on these — green must survive finalize. |

## GenerateImage template

```text
Create ONE Jagged Alliance 3 inventory CHIP miniature for a weapon attachment.
This is ChipIcon only (tiny HUD badge), NOT the full ModifyWeaponDlg upgrade icon.

ComponentId: COMPONENT_ID
Slot: SLOT
Solid fill #C8C0A8 only (except night-vision green glass / tritium accents when specified).

Canvas: square. Solid black draft background (keyed to alpha later).
Style: flat 2D minimalist tactical glyph, thick silhouette, soft AA,
no gradients, bevels, shadows, textures, text, numbers, frames, photo-realism.
No full weapon body — only the attachment silhouette.
Must stay readable when scaled to ~22x22 px.

SYMBOL: SYMBOL

Match line weight of the attached chip / Jazz glyph references.
```

## Wire

```text
ChipIcon = "Mod/e6L4ECj/Icons/Upgrades/Chips/<ComponentId>.png"
```
