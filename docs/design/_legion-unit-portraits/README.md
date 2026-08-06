# Legion unit portraits (schematic)

Transparent `300×300` PNG in `jazz-units/EnemyPortraits/Legion/`.
Red-only (`RGB≈216,72,72`). No opaque background.

## Slots (locked)

| Slot | Position | Content |
| --- | --- | --- |
| Family mark | **inside** shield, top-center | `chevron` / `bar` / `bars` / `arrow` / `star` / `diamond` / none |
| Role glyph | **inside** shield, below family mark | one silhouette |
| Tier | **outside** under tip | 0..4 solid dots (not stars) |

Faction color stays red; family is mark **shape**, not hue.
Do not copy filled ivory satellite squad shields — unit frame is outline heater shield.
The family mark stays clear of the upper-left `xN` stack counter.
Leader role glyphs are rank insignia: sergeant chevrons, one lieutenant bar,
two captain bars, and an elite diamond with three bars for T4.
Assault role glyphs use the same single-silhouette treatment as the other
families; `masters/sheets/assault.png` is current and the old composite
Assaulter layers in `Legion.psd` are reference-only.

## Rebuild

```text
python docs/tools/_compose_legion_unit_portraits.py
python docs/tools/_wire_legion_unit_portraits.py
python docs/tools/_audit_legion_unit_portraits.py
```

Catalog: `catalog.json` (38 units). `masters/sheets/` is the current glyph
source; `Legion.psd` remains the frame and legacy reference. Shipped PNGs are
compose output.
QA writes `preview-sheet.png` (100 px) and `preview-stack.png` (`xN` overlay).
