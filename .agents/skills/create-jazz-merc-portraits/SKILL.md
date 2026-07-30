---
name: create-jazz-merc-portraits
description: >-
  PNG-портреты мерков/NPC JAZZ в стиле JA3 (300+2000): рендер на #504633,
  фон снимать отдельным проходом (BiRefNet / useknockout; fallback soft-key),
  color grade как vanilla, наёмник без лычек, класс по киту.
  При запросе мерка/портрета/BigPortrait/field medic.
---

# Создание merc / NPC portraits

Пакет: `jazz-units` → `MercPortraits/` / `NPCPortraits/` (`_wip/` для черновиков).  
Rule: `.cursor/rules/jazz-merc-portraits.mdc`.  
Style: [references/style-and-naming.md](references/style-and-naming.md).

## Style-референсы

**Только** `jazz-units/MercPortraits/References/` (+ `Portraits/`).  
Никакие другие пути как style/color/proportions refs не использовать.  
Face/pose от пользователя и `*.ja2-face.*` — **identity** (узнаваемость), не замена `References/`.  
Лицо: вдохновляться JA2-face, оставаться узнаваемым, но анатомия/объём **чуть реалистичнее** как у лиц в `References/` (не плоский стикер, не beauty-filter).

## Правила персонажа

- **Наёмник, не солдат:** армейские лычки / sergeant stripes / army rank — нет; **шевроны/патчи наёмников и PMC — ок**.
- **Климат:** жарко, Африка — **Grand Chien** — лёгкая/полевая одежда под жару; без зимнего kit, если sheet не требует.
- **NPC (`NPCPortraits/newgen/`):** только один full-body `_Big.png`; не мерки — роль по префиксу (`Rebels_` повстанцы, `Adonis_`, `Local_` гражданские). Style-lock на существующий NPC Big + appearance preset; не перекрашивать в AIM-merc. Пайплайн `#504633` + rembg + QA/regen как у мерков.
- Класс по киту; **пистолет в кобуре — ок**; огнестрел в руках / на столе / винтовки — нет.
- Полевой медик: IFAK/турникеты/shears/gauze + простой red cross — не «врач со стетоскопом».
- **Quality bar:** `MercPortraits/_quality_bar/Highball_ideal_Big.png` — эталон уровня (пропорции, поза, чистота, kit). Сверять каждый Big; ниже бара = reject. Не копировать Highball-образ на чужих мерков.
- **Много мелких складок на штанах = HARD reject** → чинить **GPT GenerateImage denoise** (noisy Big + `OK_clean_folds_Laura_pants.png`; keep sharp; 2–3 прохода ок). **Не** OpenCV/bilateral (мыло). Regen если GPT-денойз не спас.
- **Позы интересные:** как у refs — ¾, вес на одной ноге, асимметрия рук / жест с kit; **не** симметричный mannequin. Роль/характер влияют на стойку. Pose-ref пользователя — копировать. Без огнестрела в руках и без ломки пропорций/кадра (кобура с пистолетом ок).
- **Big framing:** голова/волосы и ноги/ботинки **не обрезаны**; поля `#504633` сверху и снизу.
- **Оба слота:** Portrait 300 (tight headshot — лицо почти на весь кадр) + Big 2000; skill `frame-jazz-merc-ui-portrait`. Не поясной crop.
- Если bust-ген тащит огнестрел — crop из Big через `bust_crop_tight.py` (**frac≈0.28**, Ice/Blood), не 0.42 waist-up и не 0.15 face-clip.
- **Appearance sheet — 5 вариантов** в `MercPortraits/newrules2/<Id>/`:
  - файлы: `<Id>_<variant>.png` + `<Id>_<variant>_Big.png`
  - суффиксы: `appearance` | `appearance_backstory` | `appearance_backstory_bio` | `bio` | `bio_backstory`
  Источник: `docs/design/mercs-ja12/_appearance-sheet.md` (+ Google sheet). Нет строки / нет face → не генерить.  
  Огнестрел в руках / длинноствол из sheet не рисовать; пистолет в кобуре — ок.

## Фон + альфа (два прохода)

1. GenerateImage **только** opaque на solid `#504633` (не чёрный, не transparent в промпте).
2. Сохранить сырой кадр **до cut** в отдельную **`_raw/`** (не в папку с финальными RGBA).
3. Удачный кадр не перегенерировать ради альфы.
4. **Снятие фона — отдельный проход**, предпочтительно локальной нейронкой:
   - **Локально (предпочтительно на этой машине):** `rembg` + BiRefNet  
     `...\Python312\Scripts\rembg.exe i -m birefnet-general <raw.png> <out.png>`  
     (после `winget` Python 3.12 + `pip install "rembg[cpu,cli]"`).
   - Hosted: [useknockout](https://useknockout.com/) при наличии `KNOCKOUT_TOKEN`.
   - Запасной UI: Photoroom / remove.bg.
5. **Fallback** без нейронки: chroma soft-key (#504633) (`scripts/key-magenta-portrait.ps1` / `_softcut.ps1`) — blur маски, лёгкий despill. **Не** choke / не black-key.
6. Resize к 300 / 2000 после cut; проверить уголки и fringe. Cut-выход — вне `_raw/`.

## Workflow

```text
- [ ] Id / роль / face / References style-refs
- [ ] Строка sheet → 5 суффиксов варианта в `newrules2/<Id>/`
- [ ] GenerateImage Portrait+Big на #504633 → …/_raw/ (opaque, до обрезания)
- [ ] QA стиля: **длина ног / рост** (не карлик), цвет, экспозиция, поза, чистота vs References + `_quality_bar/Highball_ideal_Big.png`
- [ ] Отдельный cut: rembg BiRefNet (preferred) → RGBA вне _raw/; иначе soft-key fallback
- [ ] Resize 300/2000; DoD cornerA=0; Read cut рядом с refs (в т.ч. экспозиция)
- [ ] **Второй проход:** последовательно QA всех Big батча → reject → переген rejected ещё раз → повторный QA
```
