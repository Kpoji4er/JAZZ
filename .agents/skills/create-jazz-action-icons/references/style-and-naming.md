# Style & naming — HUD / action icons

Канон (промпты + рефы): `Icons/Hud/references/PROMPT.md`.

Style-референсы GenerateImage: **только** `Icons/Hud/references/*.png`  
(+ runtime `Perks/SignatureAbilities/*.png` / `Icons/Med/*.png` при regen соседней семьи).

## Canvas

| | |
| --- | --- |
| Size | **108×54** RGBA (Active) or **54×54** (Passive Signature) |
| Layout Active | dual strip: left cool blue/grey `#B5ADA5` / Hud LEFT, right sand `#F7F7D6` |
| Layout Passive | **single** cool **blue** tile (Hud LEFT ≈ `#609BB8`) — **never cream/white** |
| Background | transparent `A=0` |
| Style | flat JA3 Hud stencil, soft AA, optional light scanlines |

**Owner rule:** signature / Passive hotbar glyphs are **always blue**. Cream only as Active dual right-state. See `.cursor/rules/jazz-signature-icons-blue.mdc`.

## Naming / paths

```text
Perks/SignatureAbilities/<ActionId>.png
Mod/e6L4ECj/Perks/SignatureAbilities/<ActionId>.png

# medical CombatAction subset (same class):
Icons/Med/<ActionId>.png
Mod/e6L4ECj/Icons/Med/<ActionId>.png
```

`ActionId` = имя файла без расширения (обычно Id CombatAction или явный суффикс вроде `MobileShot_Pistol`).

## Не сюда

| Папка | Skill |
| --- | --- |
| `Perks/Personal/` 68×68 | `$create-jazz-perk-icons` |
| `Icons/StatusEffects/` 40×40 | `$create-jazz-status-icons` |
| `Icons/Items/` цветной inventory | не action skill |
| `Icons/Upgrades/Chips/` | `$create-jazz-chip-icons` |

## Промпт (кратко)

```text
Create ONE Jagged Alliance 3 HUD combat-action icon strip matching the reference images EXACTLY.

This icon is for CombatAction ACTION_ID (hotbar / SignatureAbilities).

Canvas: landscape 2:1 (approx 108x54). Solid black draft background (keyed to alpha later).
Layout: TWO identical glyphs side-by-side.
  Left glyph solid fill ~#B5ADA5 (cool grey).
  Right glyph solid fill ~#F7F7D6 (sand cream).
Style: flat 2D tactical HUD stencil, thick readable silhouette, soft AA,
optional faint horizontal scanline distress like vanilla Hud refs,
no gradients, no bevels, no drop shadows, no textures beyond light distress,
no text, no letters, no numbers, no button frames, no portraits.

Subject centered in each half. SYMBOL: SYMBOL

Match line weight and simplicity of the attached JA3 Hud action references.
```
