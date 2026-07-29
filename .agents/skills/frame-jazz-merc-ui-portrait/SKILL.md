---
name: frame-jazz-merc-ui-portrait
description: >-
  Кадрирование UI-портрета мерка JAZZ 300×300: лицо почти на всю плоскость
  как у vanilla JA3 (Blood/Ice), не поясной/chest-up. При генерации Portrait,
  bust crop из Big, жалобе что портрет мелкий / лицо маленькое.
---

# UI Portrait framing (300×300)

Пакет: `jazz-units` → `MercPortraits/`.  
Связанный skill: `create-jazz-merc-portraits` (Big + общий стиль).  
Rule: `.cursor/rules/jazz-merc-portraits.mdc`.

## Проблема

Новые мерки в UI выглядят «мелкими»: в квадрате торс по пояс, голова ~20% кадра.  
У ванили (Len/Grizzly/Blood/Ice) **лицо занимает почти всю плоскость** (голова + шея + чуть плеч).

## Эталон кадра

`MercPortraits/_quality_bar/OK_ui_portrait_framing_Blood.png`  
(+ `References/Portraits/*.png`)

Accept: headshot like Ice/Blood/Omryn — **вся голова в кадре** (макушка + подбородок), чуть плеч/груди; лицо крупное, но не обрезанное.

Reject: waist-up / distant passport.  
Reject: extreme zoom — обрезаны макушка/подбородок/рот (перебор).


## Выход

| Слот | Файл | Размер | Кадр |
| --- | --- | --- | --- |
| Portrait | `<Id>.png` / `newrules2/<Id>/<Id>_<variant>.png` | **300×300** RGBA | **close-up face** |
| BigPortrait | `*_Big.png` | 2000×2000 | full-body (без изменения) |

## Два пути

### A) GenerateImage bust (предпочтительно для нового слота)

`aspect_ratio` `1:1`. Refs: face_png + `References/Portraits/` (Blood/Ice) + quality bar framing.

```text
JA3 mercenary UI PORTRAIT, square 300-style close-up.
FRAMING (CRITICAL): UI headshot like vanilla JA3 (Ice/Blood/Omryn) — full head in frame (crown to chin), upper shoulders/chest; face large but NOT cropped; NOT waist-up; NOT extreme face-only zoom.
BACKGROUND: solid olive-brown chroma #504633 only.
FACE: recognizable from JA2 face ref; slightly realistic JA3 anatomy; NOT sticker; NOT beauty-filter.
POSE: slight ¾ head/shoulders, lively; not stiff passport.
SETTING: hot African climate (Arulco) — heat-appropriate collar/kit visible at shoulders.
SURFACE: sharp; few large folds only on visible cloth.
```

### B) Crop из утверждённого Big (если bust-ген тащит оружие)

Скрипт: `create-jazz-merc-portraits/scripts/bust_crop_tight.py`  
или `_postprocess.py` → `bust_crop` с **head fraction ~0.28** высоты силуэта (Ice/Blood; не 0.42 waist-up и не 0.15 face-clip).

```text
python bust_crop_tight.py <Big.png> <out_300.png>
python bust_crop_tight.py --batch newrules2 --frac 0.28
```

## QA

До принятия Portrait: `Read` кандидата рядом с Blood/Ice / `OK_ui_portrait_framing_Blood.png`.  
Если голова заметно меньше, чем у ванили → reject / tighter crop / regen.
