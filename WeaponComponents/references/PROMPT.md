# WeaponComponent.Icon — style B (WeaponComponents 3D)

Skill: `$create-jazz-component-icons`  
Chip-миниатюры: `$create-jazz-chip-icons` (отдельно).

Канон для **уникальных** Icon Scope / Magazine (и прочих, когда нужна своя картинка вместо шареного vanilla): тёмный 3D-рендер как `WeaponComponents/Optics/*`.

Стволы (**Barrel**): уникальные Icon **не** требуются — можно оставлять vanilla.

## Canvas / wire

| | |
| --- | --- |
| Size | **100×100** RGBA |
| Path | `Mod/e6L4ECj/WeaponComponents/<Folder>/<ComponentId>.png` |
| Folders | `Optics/`, `Magazine/`, `Side/`, `Muzzle/`, … |
| Style | realistic dark 3D product render, matte charcoal metal |
| Edge | **как Anaconda**: мягкий AA-силуэт (чёрный fringe + плавная альфа 25→255), лёгкий soft body; **не** жёсткая pixel-обводка / лесенка. Реф: `WeaponComponents/references/style_B_edge_ref_Anaconda.png` |
| Cut | rembg → fit ~78% → harden/fringe clean → Anaconda soft edge → 100×100 |
| Tool | `docs/tools/_finalize_icon_style_b.py` |

Preview drafts: `Icons/Upgrades/_review/icon_style_B/`.

## GenerateImage — обязательно с референсов

Не выдумывать форму «из головы». Приоритет **shape-рефа** (сверху вниз):

1. **Уже существующий 3D Icon** этого обвеса / близкого Visual: `WeaponComponents/**` (напр. `Carbine/CarbineMag30.png`, `Optics/ACOG.png`) или `Icon` на `WeaponComponentVisual` ApplyTo  
2. **Vanilla** `UI/Icons/Upgrades/…` с компонента (если есть распакованный PNG)  
3. **Chip** `Icons/Upgrades/Chips/<Id>.png` — только грубый силуэт, **не** точная форма (часто неверный семейством: AK-glyph у `MagNormal`)  
4. Скрин/рендер entity меша — лучший вариант, когда 1–2 нет  

**Style / edge** всегда дополнительно:  
`WeaponComponents/references/style_B_edge_ref_Anaconda.png` + любой чистый `WeaponComponents/Optics/*`.

`JAZZ_MagNormal` — архетип на десятки мешей (STANAG / AK / MP5 / pistol…). Один Icon ≠ все меши; для превью/дефолта брать **STANAG-like** (`CarbineMag30`), не chip-AK.

```text
Create ONE Jagged Alliance 3 weapon-component Icon for ModifyWeaponDlg.
Realistic dark 3D product render matching the STYLE references (Anaconda / Optics).
Preserve the SHAPE of the attached ACCURATE 3D/vanilla magazine reference —
same proportions, ribs, feed lips, floor plate. Do NOT follow the beige Chip glyph
if a CarbineMag / Optics / vanilla upgrade icon is attached.

ComponentId: COMPONENT_ID
Slot: SLOT

BACKGROUND: solid flat MAGENTA chroma #FF00FF filling the entire canvas.
No black/brown bg, no gradient, no checkerboard, no transparency request.
Leave generous magenta margins — object must NOT touch frame edges.

Subject: ATTACHMENT alone (no full weapon body).
Matte dark charcoal / gunmetal, soft upper-left studio light, subtle rim highlights.
Soft filmic edges like Anaconda (no hard pixel outline, no staircase).
No text, no numbers, no UI frame, no drop shadow onto magenta.
Never paint magenta on the attachment itself.

SHAPE LOCK: attached accurate WC/vanilla ref (not Chip unless that is all we have).
STYLE LOCK: lighting/materials/edge AA like Anaconda + Optics.
```

Мягкий AA-край доводит finalize.

## Magazine rules (обязательно)

Ориентация как магазин **на винтовке в боковом виде** (левый бок, дуло **вправо**):

| | |
| --- | --- |
| Feed lips | **сверху** (вставляется вверх в шахту) |
| Floor plate | **снизу** |
| Изгиб (AK banana) | вперёд, **вправо** (к дулу) |
| Угол | почти вертикально, лёгкий forward lean как у АК |
| Не делать | диагональный «hero spin», вверх ногами, изгиб назад/влево |
| Состав | **только магазин** — без receiver / magwell |
| Силуэт @icon | гладкие внешние края; **без** зубцов/notches на спинке (на 100px читаются как «пожёванность») |

Дополнение к SYMBOL для магазинов:

```text
ORIENTATION: installed on a rifle in LEFT-SIDE view, muzzle RIGHT —
feed lips TOP, floor plate BOTTOM, banana curve bows FORWARD to the RIGHT,
nearly upright with slight forward lean. Magazine alone, no rifle body.
SILHOUETTE: clean smooth outer edges for tiny UI — NO rear-spine sawtooth notches
(they read as chewed/jagged at 100x100).
```

Примеры превью: `Icons/Upgrades/_review/icon_style_B/preview_JAZZ_MagNormal.png`.

## Scope notes

- Уникальный меш / уникальный Id оптики → уникальный Icon (не шарить `compact_reflex_sight` / один NSPU на разные прицелы).
- Night optics: допустим слабый green/red lens cue; обводка всё равно чёрная.

## Finalize + QA

```text
python docs/tools/_finalize_icon_style_b.py
python docs/tools/_qa_icon_style_b.py
```

FAIL → regen from shot/refs, finalize again, re-QA. Не wire пока QA не PASS.

Скриншоты для shape: `Icons/Upgrades/_review/icon_style_B/_shots/<ComponentId>/`
Чеклист: `Icons/Upgrades/_review/icon_style_B/SCREENSHOT_CHECKLIST.md`

Wire:

```text
Icon = "Mod/e6L4ECj/WeaponComponents/Magazine/<ComponentId>.png"
Icon = "Mod/e6L4ECj/WeaponComponents/Optics/<ComponentId>.png"
```
