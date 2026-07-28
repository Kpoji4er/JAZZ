# Style bible: JA3 / JAZZ merc & NPC portraits

Канон — `MercPortraits/References/` (vanilla JA3 PNG): semi-realistic character art.

## Размеры

| Слот | Размер | Framing |
| --- | --- | --- |
| `Portrait` | **300×300** RGBA | bust |
| `BigPortrait` | **2000×2000** RGBA | full body |

Готовый файл: прозрачный фон + по возможности **мягкая полупрозрачная** кромка (волосы).

## Наёмник ≠ военный

- **Запрещены** лычки / rank chevrons / sergeant stripes / army rank insignia.
- Класс — PMC/civilian kit: простой medic red cross, IFAK, инструменты, сумки.
- Полевой медик: турникеты, shears, gauze, IFAK — **не** кабинетный стетоскоп.
- **Оружие в кадре запрещено** (кобура — редко).

## Альфа pipeline

Если кадр уже хороший по стилю/лицу:

1. **Не перегенерировать.**
2. Hard-mask: pure-black фон (`maxRGB ≤ ~6`) → кандидат на прозрачность.
3. **Смазать обводку через blur маски** (Gaussian/box blur alpha ~1–1.5px): появляются полупрозрачные AA-пиксели на кромке. RGB силуэта сохраняется; лёгкий smudge RGB только на semi-transparent fringe.
4. **Не** choke/erode и не binary cut без blur маски (даёт «лесенку»).

Запрещено «улучшать» удачный кадр повторными генерациями и chromakey-choke.

## Стиль / палитра

- Как `References/` (olive/khaki/taupe midtones; не muddy crush).
- JA3 semi-realistic; не anime/фото/waifu.

## Naming

```text
MercPortraits/<Id>.png | <Id>_Big.png
NPCPortraits/<Id>.png  | <Id>_Big.png
*/_wip/ — черновики
docs/design/mercs-ja12/<slug>.ja2-face.gif|.jpg — JA2 face identity (обязательный face ref для legacy мерков)
```

Для мерков из `docs/design/mercs-ja12/`: всегда включать ``<slug>.ja2-face.*`` в `reference_image_paths`. Лицо Portrait/BigPortrait должно быть узнаваемо как JA2-референс (возраст, этничность, причёска, ключевые черты).

## BigPortrait identity & pose

- Сначала утвердить Portrait; Big всегда с `reference_image_paths` = готовый bust **первым**.
- Лицо Big = лицо Portrait (не старить, не перерисовывать).
- Поза компактная, руки у корпуса; избегать «рука в бок» с большим треугольником пустоты (на чёрном выглядит как чернота между руками).
- После ключа: pure-black чистить **глобально** (`max≤5`), чтобы закрытые карманы между рукой и торсом тоже стали прозрачными.

## Промпт Portrait

```text
JA3 mercenary PORTRAIT, square bust.
BACKGROUND: solid pure BLACK #000000 (no checkerboard/magenta/transparency request).
Mercenary contractor (NOT military): no rank chevrons / лычки.
Class kit visible; no firearms.
FACE: match JA2 face reference image (same identity).
CHARACTER: ...
Match JA3 reference color grade.
```

## Промпт BigPortrait

```text
Extend the EXACT woman from the bust reference to JA3 FULL-BODY.
FACE must be 100% identical to bust (same age — do not age up).
BACKGROUND: solid pure BLACK #000000.
Arms relaxed at sides, close to torso — no large empty triangles between arms and body.
Same kit downward; merc not soldier; no firearms.
```
