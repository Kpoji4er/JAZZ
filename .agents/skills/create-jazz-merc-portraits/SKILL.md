---
name: create-jazz-merc-portraits
description: >-
  PNG-портреты мерков/NPC JAZZ в стиле JA3 (300+2000): фон #FF00FF, color grade
  как vanilla, аккуратный soft-cut с blur маски, наёмник без лычек, класс по киту.
  При запросе мерка/портрета/BigPortrait/field medic.
---

# Создание merc / NPC portraits

Пакет: `jazz-units` → `MercPortraits/` / `NPCPortraits/` (`_wip/` для черновиков).  
Rule: `.cursor/rules/jazz-merc-portraits.mdc`.  
Style: [references/style-and-naming.md](references/style-and-naming.md).

## Style-референсы

**Только** `jazz-units/MercPortraits/References/` (+ `Portraits/`).  
Никакие другие пути как style/color/proportions refs не использовать.  
Face/pose от пользователя и `*.ja2-face.*` — отдельно (identity), не замена `References/`.

## Правила персонажа

- **Наёмник, не солдат:** без лычек / rank chevrons / sergeant stripes.
- Класс по киту; **оружие в кадре запрещено**.
- Полевой медик: IFAK/турникеты/shears/gauze + простой red cross — не «врач со стетоскопом».
- **Цвет как в vanilla:** cleaner midtones; не muddy chocolate crush. В промпте — `COLOR GRADE`.
- **Пропорции:** взрослый как JA3 — **не карлик**, **не большеголовый**, ноги анатомически верной длины; Portrait≈Big. В промпте — `PROPORTIONS`; кривое — reject.
- **Big framing:** голова/волосы и ноги/ботинки **не обрезаны**; поля `#FF00FF` сверху и снизу.
- **Appearance sheet — 3 варианта** в `wip-regen/`:
  - `v1_appearance_backstory_bio/` — APPEARANCE + BACKSTORY/LOOK + BIO
  - `v2_appearance_only/` — только APPEARANCE
  - `v3_bio_backstory/` — BIO + BACKSTORY/LOOK
  Огнестрел из sheet не рисовать. Нет строки → не генерить.

## Фон + альфа

1. GenerateImage **только** на solid `#FF00FF` (не чёрный, не transparent).
2. Удачный кадр не перегенерировать.
3. Key magenta → **blur маски** (soft AA) → лёгкий despill fringe.
4. **Не** choke / не black-key (съедает волосы/штаны).

## Workflow

```text
- [ ] Id / роль / face / References style-refs
- [ ] Строка sheet → три промпт-варианта (v1/v2/v3)
- [ ] GenerateImage Portrait+Big ×3 на #FF00FF → соответствующие папки
- [ ] Soft-cut; Read DoD на каждый вариант
```
