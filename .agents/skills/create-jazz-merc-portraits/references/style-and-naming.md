# Style bible: JA3 / JAZZ merc & NPC portraits

## Style-референсы (обязательно)

Для стиля / color grade / пропорций / framing в `GenerateImage` использовать **только**:

`jazz-units/MercPortraits/References/`  
(включая `References/Portraits/` для bust)

- Big → файлы из `References/*.png`
- Portrait → файлы из `References/Portraits/*.png`

**Больше нигде:** не брать style-refs из UI extract вне этой папки, DDS/HPK на диске, других модов, `NPCPortraits/`, финальных JAZZ merc PNG, `_wip/` чужих мерков, случайных assets.

Допустимо рядом со style-refs (это не style-канон):

- face identity: `docs/design/mercs-ja12/<slug>.ja2-face.*` и/или face от пользователя;
- **appearance sheet** строка мерка: [`_appearance-sheet.md`](../../../../docs/design/mercs-ja12/_appearance-sheet.md) (Google Sheet);
- pose-ref от пользователя;
- утверждённый bust этого же мерка для Big identity lock.

## Appearance sheet в промпте (обязательно)

Источник: Google Sheet «JAZZ Mercs» → зеркало `_appearance-sheet.md` / `_sheet_export.tsv`.

Генерировать **3 варианта** каждого мерка в разные папки `MercPortraits/wip-regen/`:

| Вариант | Папка | Поля из таблицы в промпте |
| --- | --- | --- |
| **v1** | `v1_appearance_backstory_bio/` | `APPEARANCE` + `BACKSTORY/LOOK` + `BIO` |
| **v2** | `v2_appearance_only/` | только `APPEARANCE` (внешность) |
| **v3** | `v3_bio_backstory/` | `BIO` + `BACKSTORY/LOOK` (без колонки внешность) |

В GenerateImage явно помечать вариант, например `VARIANT: v1` / `v2` / `v3`.

Шаблоны полей:

```text
# v1
APPEARANCE: <внешность>
BACKSTORY/LOOK: <Бекстори/внешка>
BIO: <биография JA2>

# v2
APPEARANCE: <внешность>
(не вставлять BACKSTORY/LOOK и BIO)

# v3
BIO: <биография JA2>
BACKSTORY/LOOK: <Бекстори/внешка>
(не вставлять APPEARANCE)
```

- Face ref (`*.ja2-face.*`) — во всех трёх вариантах.
- Style-refs — только `MercPortraits/References/`.
- Глобальные правила (no firearms / no chevrons / proportions / `#FF00FF`) побеждают sheet во всех вариантах.
- Нет строки в sheet → STOP.
- Portrait и Big одного варианта должны быть согласованы (Big от bust того же варианта).

Канон визуала внутри `References/`: semi-realistic JA3 character art.

## Размеры

| Слот | Размер | Framing |
| --- | --- | --- |
| `Portrait` | **300×300** RGBA | bust |
| `BigPortrait` | **2000×2000** RGBA | full body |

Готовый файл: прозрачный фон + по возможности **мягкая полупрозрачная** кромка (волосы).

## Фон генерации (обязательно)

GenerateImage всегда на **сплошном фиолетовом хромакее**, не на чёрном:

- Цвет: **pure magenta/violet `#FF00FF`** (rgb 255,0,255), плоский, без градиента.
- Запрещено в промпте просить: black bg, transparent, checkerboard, gray/white matte.
- На персонаже **нельзя** magenta/violet (кожа, волосы, одежда, kit).
- После генерации: key только `#FF00FF` → alpha; затем **blur маски** (soft AA). Не choke.
- Чёрный фон ломает тёмные волосы/штаны при key — **не использовать**.

## Наёмник ≠ военный

- **Запрещены** лычки / rank chevrons / sergeant stripes / army rank insignia.
- Класс — PMC/civilian kit: простой medic red cross, IFAK, инструменты, сумки.
- Полевой медик: турникеты, shears, gauze, IFAK — **не** кабинетный стетоскоп.
- **Оружие в кадре запрещено** (кобура — редко).

## Альфа pipeline (с фиолетового)

Если кадр уже хороший по стилю/лицу:

1. **Не перегенерировать.**
2. Hard-mask: пиксели близкие к `#FF00FF` (chroma distance) → фон.
3. **Смазать обводку через blur маски** (Gaussian/box ~1–1.5px): soft AA на кромке. RGB силуэта сохранить; лёгкий magenta-despill только на fringe.
4. **Не** choke/erode и не binary cut без blur (даёт «лесенку»).
5. Не key по чёрному — тёмные волосы/штаны съедает.

Запрещено «улучшать» удачный кадр повторными генерациями и chromakey-choke.

## Цветовая гамма (как в vanilla)

Канон цвета — **только** `MercPortraits/References/` (+ `Portraits/`). Raven / Buns / MD и др. из этой папки.

- **Match JA3 color grade** в каждом промпте Portrait и BigPortrait.
- Чище midtones, чуть cooler-neutral тени; кожа реалистичная, не «грязная».
- Ткани читаемые: taupe / grey / muted olive / khaki — **не** chocolate-brown crush и не зажатые чёрные.
- Средние тона субъекта ближе к vanilla (~светлее, меньше brown cast), не тёмный muddy AI-рендер.
- При сомнении сверить визуально с 1–2 refs из `References/` до принятия кадра.

Запрещено: anime / фото / waifu / plastic beauty filter.

## Naming

```text
MercPortraits/<Id>.png | <Id>_Big.png
NPCPortraits/<Id>.png  | <Id>_Big.png
*/_wip/ — черновики
docs/design/mercs-ja12/<slug>.ja2-face.gif|.jpg — JA2 face identity (обязательный face ref для legacy мерков)
```

Для мерков из `docs/design/mercs-ja12/`: всегда включать ``<slug>.ja2-face.*`` в `reference_image_paths`. Лицо Portrait/BigPortrait должно быть узнаваемо как JA2-референс (возраст, этничность, причёска, ключевые черты).

## Пропорции (обязательно)

Сверять с vanilla `References/` (Raven/Buns/MD и др.) **до принятия** кадра. Анатомическая проверка обязательна:

- **Не карлики:** нормальный взрослый рост относительно кадра; короткие ноги / сжатый торс / «детский» силуэт — reject.
- **Не большеголовые:** голова не доминирует над телом (нет bobblehead / oversized head).
- **Ноги:** анатомически верная длина и пропорция бедро/голень/стопа; не коротышки, не палки, не обрезанные в пропорциях.
- **Голова / тело:** как у JA3 Mercs full-body; шея и плечи естественные.
- **Руки / кисти / стопы:** нормальная длина и размер; не «детские» и не гипертрофированные.
- **Торс / бёдра / плечи:** реалистичные взрослые пропорции.
- **Portrait vs Big:** одно телосложение; Big не «другой человек» по масштабу частей.
- **Поза:** суставы правдоподобны; pose-ref не оправдывает карлика/большеголовость/кривые ноги.

В промпте явно:  
`PROPORTIONS: adult human like JA3 Mercs refs — correct head-to-body ratio, full-length natural legs, no dwarf proportions, no oversized head, realistic hands/feet.`  
В Read/DoD: отклонить кадр с кривыми пропорциями / карликовостью / большеголовостью, даже если лицо/kit ок.

## BigPortrait identity, pose & framing

- Сначала утвердить Portrait; Big всегда с `reference_image_paths` = готовый bust **первым**.
- Лицо Big = лицо Portrait (не старить, не перерисовывать).
- Поза по умолчанию компактная; **если пользователь дал pose-ref** — копировать эту позу (в т.ч. рука в бок / ¾), а не упрощать; пустоты под рукой заливать `#FF00FF`.
- **Framing Big (обязательно):** весь персонаж в кадре — **голова и волосы не обрезаны сверху**, **ноги и стопы/ботинки не обрезаны снизу**; небольшие поля `#FF00FF` сверху и снизу. Crop головы или ног = reject / переген.
- Дырки между рукой и торсом: key только если там реально `#FF00FF`, не выжигать тёмные пиксели персонажа.

## Промпт Portrait

```text
JA3 mercenary PORTRAIT, square bust.
BACKGROUND: solid pure MAGENTA/VIOLET #FF00FF only (flat chroma). No black, no checkerboard, no transparency request. No magenta on character.
Mercenary contractor (NOT military): no rank chevrons / лычки.
Class kit visible; no firearms.
FACE: match JA2 face reference image (same identity).
APPEARANCE: <sheet внешность>
BACKSTORY/LOOK: <sheet Бекстори/внешка>
CHARACTER / class kit: ...
COLOR GRADE: match JA3 MercsPortraits refs (Raven/Buns/MD) — cleaner midtones, muted earth, readable fabrics; NOT muddy chocolate crush / dark brown cast.
PROPORTIONS: adult human like JA3 Mercs refs — correct head-to-body/shoulder ratio, natural neck and collarbones; no oversized head.
```

## Промпт BigPortrait

```text
Extend the EXACT person from the bust reference to JA3 FULL-BODY.
FACE must be 100% identical to bust (same age — do not age up).
BACKGROUND: solid pure MAGENTA/VIOLET #FF00FF only (flat chroma). No black, no checkerboard. No magenta on character.
FRAMING: full body head-to-toe fully inside frame — head/hair NOT cropped at top, feet/boots NOT cropped at bottom; small magenta margins.
If pose-ref given: match that pose; else arms relaxed close to torso.
APPEARANCE: <same sheet внешность>
BACKSTORY/LOOK: <same sheet Бекстори/внешка — full-body continuation>
Same kit downward; merc not soldier; no firearms (even if sheet mentions a gun).
COLOR GRADE: same as JA3 Mercs full-body refs — cleaner midtones, readable khaki/olive, NOT muddy chocolate crush.
PROPORTIONS: adult human like JA3 Mercs refs — correct head-to-body ratio, full-length natural legs (no dwarf/short-leg proportions), no oversized head, natural limb thickness, realistic hands/feet.
```
