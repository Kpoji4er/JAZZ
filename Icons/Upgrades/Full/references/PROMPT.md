# WeaponComponent.Icon (Full) — GenerateImage prompts

Skill: `$create-jazz-component-icons`  
Chip-миниатюры тайла: `$create-jazz-chip-icons` (другой PROMPT).

## Canvas

| | |
| --- | --- |
| Size | **128×128** |
| Path | `Icons/Upgrades/Full/<ComponentId>.png` |
| Style | flat JA3 upgrade icon, more detail than chip, still not photo |
| Color | sand/metal greys; soft AA |

## GenerateImage template

```text
Create ONE Jagged Alliance 3 weapon-component FULL upgrade icon for ModifyWeaponDlg.
This is WeaponComponent.Icon — richer than a tiny inventory chip, still flat UI art.

ComponentId: COMPONENT_ID
Slot: SLOT
Primary colors: muted tactical sand/metal (#C8C0A8 / soft greys). Optional dark inset cuts.

Canvas: square. Solid black draft background (keyed to alpha later).
Style: flat 2D item/upgrade icon, clear silhouette, soft AA,
no photo-realism, no text, no numbers, no frames, no drop-shadow blobs.
Show the attachment itself (scope, muzzle, mag, …) recognizable at 128x128;
more detail than a 24px chip is OK (knobs, lens glass cue, mounts).

SYMBOL: SYMBOL

Match the attached JA3 / JAZZ upgrade icon references.
```

## Wire

```text
Icon = "Mod/e6L4ECj/Icons/Upgrades/Full/<ComponentId>.png"
```

Vanilla `UI/Icons/Upgrades/…` можно оставить без генерации, если устраивает.
