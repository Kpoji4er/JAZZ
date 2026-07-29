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

**Актуально — `MercPortraits/newrules2/<Id>/`:** папка на мерка, вариант — суффикс:

| Суффикс | Поля |
| --- | --- |
| `_appearance` | APPEARANCE |
| `_appearance_backstory` | APPEARANCE + BACKSTORY/LOOK |
| `_appearance_backstory_bio` | APPEARANCE + BACKSTORY/LOOK + BIO |
| `_bio` | BIO |
| `_bio_backstory` | BIO + BACKSTORY/LOOK |

Файлы: `<Id>_<variant>.png` (300) + `<Id>_<variant>_Big.png` (2000).

Legacy `wip-regen/v1|v2|v3_*` не использовать для новых батчей.

Шаблоны полей:

```text
# appearance
APPEARANCE: <внешность>

# appearance_backstory
APPEARANCE: <внешность>
BACKSTORY/LOOK: <Бекстори/внешка>

# appearance_backstory_bio
APPEARANCE: <внешность>
BACKSTORY/LOOK: <Бекстори/внешка>
BIO: <биография JA2>

# bio
BIO: <биография JA2>

# bio_backstory
BIO: <биография JA2>
BACKSTORY/LOOK: <Бекстори/внешка>
```

- Face ref (`*.ja2-face.*`) — во всех вариантах.
- Style-refs — только `MercPortraits/References/`.
- Глобальные правила (holstered pistol OK / no guns in hands or on props / PMC chevrons OK, army rank нет / proportions / exposure / folds denoise / `#504633`) побеждают sheet во всех вариантах.
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

GenerateImage всегда на **сплошном olive-brown хромакее `#504633`**, не на чёрном:

- Цвет: **pure olive-brown chroma `#504633`** (rgb 255,0,255), плоский, без градиента.
- Запрещено в промпте просить: black bg, transparent, checkerboard, gray/white matte.
- На персонаже **нельзя** olive-brown chroma (кожа, волосы, одежда, kit).
- Генератор выдаёт **opaque** кадр на #504633; альфу **не** просить у GenerateImage.
- Сырой результат **до обрезания** сохранять в соседнюю папку **`_raw/`**:
  - `_wip/_raw/<Id>.png`, `_wip/_raw/<Id>_Big.png`
  - `wip-regen/<variant>/_raw/<Id>_bust.png`, `…/_raw/<Id>_big.png`
- В `_raw/` только uncut opaque; cut/RGBA и финальные 300/2000 — **вне** `_raw/`.
- Чёрный фон ломает тёмные волосы/штаны при любом key — **не использовать**.

## Альфа — отдельный проход (предпочтительно нейронка)

Если кадр уже хороший по стилю/лицу/позе (файл лежит в `_raw/`):

1. **Не перегенерировать** ради фона.
2. Снять фон **отдельным** инструментом (не смешивать с GenerateImage); вход — файл из `_raw/`.
3. Выход cut писать **рядом / выше `_raw/`**, не поверх raw (raw сохранить).

### Preferred: neural matting (BiRefNet)

| Вариант | Ссылка | Когда |
| --- | --- | --- |
| Hosted API | [useknockout.com](https://useknockout.com/) · [github.com/useknockout/api](https://github.com/useknockout/api) | Быстрый batch, transparent PNG |
| Local model | [ZhengPeng7/BiRefNet](https://github.com/ZhengPeng7/BiRefNet) · ComfyUI BiRefNet · `rembg` + BiRefNet weights | Offline / self-host |
| Manual SaaS | Photoroom, remove.bg | Разовый ручной cut |

BiRefNet сейчас сильный SOTA по волосам/меху/тонкой кромке — лучше классического chroma для сложных силуэтов. Однородный `#504633` в исходнике помогает: фон не конкурирует с одеждой.

Сохранить cut как RGBA → resize HQ к **300** / **2000**.

### Fallback: chroma soft-key (#504633) (локальный скрипт)

Только если нейронка недоступна:

1. Hard-mask по chroma distance к `#504633`.
2. Blur маски (~1–1.5px) → soft AA; лёгкий despill кромки от `#504633`.
3. **Не** choke/erode и не binary cut без blur.
4. Не key по чёрному.

Скрипты: `scripts/key-magenta-portrait.ps1` (legacy name; ключ под текущий chroma), `MercPortraits/wip-regen/_softcut.ps1` — при fallback обновить key color на `#504633`.

Запрещено «улучшать» удачный кадр повторными генерациями и chromakey-choke.

## Наёмник ≠ военный

- **Запрещены** армейские лычки / sergeant stripes / national army rank insignia.
- **Ок:** шевроны, патчи, нашивки наёмников / PMC / агентства / moral patches.
- Класс — PMC/civilian kit: простой medic red cross, IFAK, инструменты, сумки.
- Полевой медик: турникеты, shears, gauze, IFAK — **не** кабинетный стетоскоп.
- **Оружие:** **пистолет в кобуре — ок**. Запрещены огнестрел в руках, на столе/земле, винтовки/длинноствол в кадре. Ножи/инструменты/kit — ок.

## QA после генерации: пропорции + цвет по References (обязательно)

Канон — **только** готовые мерки в `MercPortraits/References/` (+ `Portraits/` для bust).  
До принятия любого кадра агент обязан:

1. `Read` кандидат (Portrait или Big).
2. `Read` **1–2** файла refs того же типа (Big → `References/*.png`, bust → `References/Portraits/*.png`), напр. Raven / Buns / MD.
3. Сравнить **пропорции тела**, **цветовую гамму**, **экспозицию**, **позу** и **чистоту поверхности** с refs (поза живая; яркость midtones как у refs; ткани/кожа без лишнего AI-шума и сетки складок).
4. Расхождение = reject / переген. Без шагов 1–3 кадр не принимать.

### Цветовая гамма

- **Match JA3 color grade** в каждом промпте Portrait и BigPortrait.
- Чище midtones, чуть cooler-neutral тени; кожа реалистичная, не «грязная».
- Ткани читаемые: taupe / grey / muted olive / khaki — **не** chocolate-brown crush и не зажатые чёрные.
- Средние тона субъекта ближе к refs (~светлее, меньше brown cast), не тёмный muddy AI-рендер.

### Экспозиция (обязательно vs References)

Сверять яркость с refs (`References/*.png` для Big, `References/Portraits/` для bust):

- Не пересвет (выбитые блики на лбу/тканях) и не underexposure / crushed blacks.
- Лицо и одежда в том же «окне» midtones, что у Raven/Buns/MD и др.
- После cut на прозрачном фоне сравнивать сам субъект с refs, не яркость фона.
- В промпте:  
  `EXPOSURE: match JA3 Mercs refs brightness — readable midtones, not overexposed, not dark muddy underexposure.`

### Чистый силуэт (меньше шума / лишних складок)

**HARD REJECT:** плотная сетка мелких складок/морщин по штанам, куртке, crotch/бёдрам/коленям —  
`MercPortraits/_quality_bar/REJECT_excess_folds_Laura_pants.png`.

**Как чинить:** **GPT GenerateImage denoise** (2–3 прохода ок), эталон `OK_clean_folds_Laura_pants.png`.  
Refs: noisy Big + OK Laura pants. Промпт: keep sharp identity/pose/kit; remove dense micro-wrinkle noise on fabric only; few large structural folds.  
**Не** OpenCV bilateral — мылит и не убирает сетку. Полный переген — если GPT-денойз не хватил.

В промпте gen:  
`SURFACE: clean readable forms like JA3 Mercs / Highball / OK_clean_folds_Laura_pants — only a few large fabric folds; NO dense wrinkle grid on pants or jacket, NO excess wrinkle noise, NO micro-dirt spam, NO over-detailed noisy cloth texture.`
В Read/DoD: excess folds = reject; cleanup target = OK Laura pants.
Сверять с refs: у JA3 Mercs крупные читаемые формы, не «пережаренный» AI-detail.

- **Запрещён визуальный шум:** микрокрап, грязь ради грязи, noise grain, over-sharpen, хаотичная micro-bump на всей одежде.
- **Складки умеренные:** несколько крупных правдоподобных заломов (локоть, колено, пояс) — **не** сетка мелких морщин по всей куртке/штанам/сумке.
- Кожа: чистые midtones как у refs; без pore-spam и plastic roughness.
- Worn/dirty из sheet — точечно (пятно, потёртость), не весь силуэт в грязи.

Запрещено: anime / фото / waifu / plastic beauty filter.

### Quality bar (идеал нашей генерации)

Файл: `MercPortraits/_quality_bar/Highball_ideal_Big.png` (Highball с тростью — approved идеал).

Что брать с эталона как **уровень**, не как копипаст kit:

- полные ноги / взрослый рост;
- характерная поза (вес, асимметрия, prop роли — трость у Highball);
- чистый cut-силуэт, спокойная экспозиция, мало шума складок;
- читаемый персонаж с первого взгляда.

QA: кандидат не хуже этого бара по пропорциям/позе/чистоте.

### Пропорции тела (жёстко, анатомия взрослого)

Сверять с vanilla `References/` + quality bar **до принятия**. Короткие ноги — частый брак модели.

- **Эталон роста:** ~7.5–8 голов; промежность около середины высоты фигуры; **ноги ≈ половина роста** (бедро + голень + стопа).
- **Не карлики / не короткие ноги:** сжатый торс, «пенек»-ноги, детский силуэт — **reject / переген**, даже если лицо и kit идеальны.
- Крупный эндоморф (массивный торс) **не** оправдывает укороченные ноги — шире да, ниже за счёт ног нет.
- **Не большеголовые:** голова не доминирует над телом (нет bobblehead / oversized head).
- **Ноги:** анатомически верная длина бедро/голень/стопа; не коротышки, не палки.
- **Голова / тело / шея / плечи:** как у JA3 Mercs full-body в `References/`.
- **Руки / кисти / стопы:** взрослые размеры.
- **Portrait vs Big:** одно телосложение.
- **Поза:** суставы правдоподобны; pose-ref не оправдывает карлика/короткие ноги.

В промпте Big явно:  
`PROPORTIONS: anatomically correct adult like JA3 Mercs refs (~7.5-8 heads tall) — crotch near mid-height, legs about half of body height, FULL-LENGTH natural legs; NO dwarf, NO short stubby legs, NO oversized head, realistic hands/feet.`  
В Read/DoD: отклонить короткий-ногий / карликовый кадр сразу.

## Naming

```text
MercPortraits/<Id>.png | <Id>_Big.png          — финал после cut
MercPortraits/_wip/_raw/<Id>.png | <Id>_Big.png — сырьё до обрезания
NPCPortraits/<Id>.png  | <Id>_Big.png
*/_wip/ — черновики; */_raw/ — opaque #504633 до cut
docs/design/mercs-ja12/<slug>.ja2-face.gif|.jpg — JA2 face identity (обязательный face ref для legacy мерков)
```

Для мерков из `docs/design/mercs-ja12/`: всегда включать ``<slug>.ja2-face.*`` в `reference_image_paths`.

### Лицо: узнаваемое + чуть реалистичнее

- **Identity lock:** тот же человек, что на JA2-face — возраст, этничность, причёска, ключевые черты.
- **Вдохновляться** источником, не paste/стикер: лицо встроено в JA3 semi-real стиль refs.
- Анатомия **чуть лучше/реалистичнее** JA2-sprite: объём лба/скул/челюсти, симметрия глаз, уши, шея, естественная кожа — как у Raven/Buns/MD, не кукла и не фото-beauty.
- Узнаваемость важнее «идеальной» красоты: характерные дефекты/асимметрия JA2 сохранять, если они часть образа.
- В промпте:  
  `FACE: recognizable identity from JA2 face ref (same person) — inspire from source, improve anatomy/volume slightly toward JA3 Mercs realism; NOT flat pixel-sticker paste; NOT beauty-filter / plastic skin.`

Reject: другое лицо; flat sticker; over-beautify; потеря узнаваемости.

## BigPortrait identity, pose & framing

- Сначала утвердить Portrait; Big всегда с `reference_image_paths` = готовый bust **первым**.
- Лицо Big = лицо Portrait (не старить, не перерисовывать).
- **Поза (обязательно интересная, как в `References/`):** не симметричный front-facing mannequin.
  - ¾ корпус + голова к камере или чуть мимо;
  - вес на одной ноге / лёгкий contrapposto;
  - асимметрия рук: на бедре / на ремне / держит class kit (IFAK, инструмент, радио…) / одна согнута;
  - поза под роль и характер мерка — варьировать между персонажами;
  - bust тоже с живыми плечами/наклоном головы, не «паспорт».
  - **если пользователь дал pose-ref** — копировать (в т.ч. рука в бок / ¾), не упрощать; пустоты под рукой заливать `#504633`.
- **Framing Big (обязательно):** весь персонаж в кадре — **голова и волосы не обрезаны сверху**, **ноги и стопы/ботинки не обрезаны снизу**; небольшие поля `#504633` сверху и снизу. Crop головы или ног = reject / переген.
- Дырки между рукой и торсом: key только если там реально `#504633`, не выжигать тёмные пиксели персонажа.

## Промпт Portrait

```text
JA3 mercenary UI PORTRAIT, square close-up.
FRAMING (CRITICAL): tight headshot like vanilla JA3 MercsPortraits (Blood/Ice) — face fills MOST of the frame (head ~70-80% of height); top of shoulders only; NOT waist-up, NOT chest-up, NOT distant.
BACKGROUND: solid olive-brown chroma #504633 only (flat chroma). No black, no checkerboard, no transparency request. Avoid flat #504633 fill on character (normal khaki/olive fabric OK).
SETTING: hot African climate (Arulco) — heat-appropriate clothing (rolled sleeves, lighter fabrics, light sweat/dust OK); NO winter/arctic gear unless sheet says so.
Mercenary contractor (NOT army): PMC/merc patches & chevrons OK; no army rank insignia / sergeant stripes / армейские лычки.
Class kit visible at collar/shoulders only; holstered pistol OK; no guns in hands / on furniture / rifles.
FACE: recognizable identity from JA2 face ref (same person) — inspire from source, improve anatomy/volume slightly toward JA3 Mercs realism; NOT flat pixel-sticker paste; NOT beauty-filter / plastic skin.
POSE: lively close-up — slight ¾ head tilt like JA3 Mercs refs; not stiff passport-front.
APPEARANCE: <sheet внешность>
BACKSTORY/LOOK: <sheet Бекстори/внешка>
CHARACTER / class kit: ...
COLOR GRADE: match JA3 MercsPortraits refs (Raven/Buns/MD) — cleaner midtones, muted earth, readable fabrics; NOT muddy chocolate crush / dark brown cast.
EXPOSURE: match JA3 Mercs refs brightness — readable midtones, not overexposed, not dark muddy underexposure.
SURFACE: clean readable forms like JA3 Mercs / Highball / OK_clean_folds_Laura_pants — only a few large fabric folds; NO dense wrinkle grid on pants/jacket, NO excess wrinkle noise, NO micro-dirt spam, NO over-detailed noisy texture.
PROPORTIONS: adult human like JA3 Mercs refs — correct head-to-body/shoulder ratio, natural neck and collarbones; no oversized head.
```

## Промпт BigPortrait

```text
Extend the EXACT person from the bust reference to JA3 FULL-BODY.
FACE must stay the same recognizable person as bust — slightly realistic JA3 anatomy, not aged up, not redrawn into a stranger.
BACKGROUND: solid olive-brown chroma #504633 only (flat chroma). No black, no checkerboard. Avoid flat #504633 fill on character (normal khaki/olive fabric OK).
SETTING: hot African climate (Arulco) — heat-appropriate clothing (rolled sleeves, lighter fabrics, light sweat/dust OK); NO winter/arctic gear unless sheet says so.
FRAMING: full body head-to-toe fully inside frame — head/hair NOT cropped at top, feet/boots NOT cropped at bottom; small #504633 margins.
POSE: interesting idle like JA3 Mercs refs — body ¾ turn, weight on one leg (contrapposto), asymmetric arms (hand on hip / belt / holding class kit tool); holstered pistol OK; NO gun in hands, NO rifle, NO weapon props on ground; silhouette with attitude matching character; NOT symmetric mannequin with both arms glued to sides. If pose-ref given: match that pose exactly.
APPEARANCE: <same sheet внешность>
BACKSTORY/LOOK: <same sheet Бекстори/внешка — full-body continuation>
Same kit downward; merc not army (PMC patches/chevrons OK, no army rank); holstered pistol OK if sheet implies sidearm; no long guns / no gun-in-hand.
COLOR GRADE: same as JA3 Mercs full-body refs — cleaner midtones, readable khaki/olive, NOT muddy chocolate crush.
EXPOSURE: match JA3 Mercs refs brightness — readable midtones, not overexposed, not dark muddy underexposure.
SURFACE: clean readable forms like JA3 Mercs / Highball / OK_clean_folds_Laura_pants — only a few large fabric folds; NO dense wrinkle grid on pants/jacket, NO excess wrinkle noise, NO micro-dirt spam, NO over-detailed noisy texture.
PROPORTIONS: anatomically correct adult like JA3 Mercs refs (~7.5-8 heads tall) — crotch near mid-height, legs about half of body height, FULL-LENGTH natural legs; NO dwarf, NO short stubby legs, NO oversized head, natural limb thickness, realistic hands/feet.
```
