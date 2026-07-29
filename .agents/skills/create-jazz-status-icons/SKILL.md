---
name: create-jazz-status-icons
description: >-
  Создавать и обновлять 40×40 HUD-иконки статус-эффектов JAZZ (CharacterEffect)
  в стиле JA3: цвет по Buff/Debuff/System, прозрачный canvas, GenerateImage +
  референсы. Использовать при запросе status effect icon, Icons/StatusEffects,
  suppression/officer aura PNG или правке PROMPT.md референсов.
---

# Создание status effect icons

Пакет: `jazz` → `Icons/StatusEffects/`.  
Style bank + mapping icon→CharacterEffect→цвет: [`Icons/StatusEffects/references/PROMPT.md`](../../../Icons/StatusEffects/references/PROMPT.md).  
Краткая шпаргалка: [references/style-and-naming.md](references/style-and-naming.md).

Asset-only PNG **не** требует spec. Новый CharacterEffect / смена поведения → `$specify-jazz-change`.  
Смена только `Icon` path у уже существующего эффекта: companion `.lua` + `items.lua` (generated-data sync).

## Вход от пользователя

Минимум:

1. `EffectId` (имя файла/класса, например `Jazz_BleedResist` или `suppressionLight`).
2. `type`: `Buff` · `Debuff` · `System` (или severity-серия).
3. Символ одним предложением (или 2–3 варианта).
4. Нужен ли wire в CharacterEffect/`items.lua` (по умолчанию **да**, если эффект уже есть; **нет** = только PNG).

## Workflow

```text
- [ ] 1. Id, type, семья цвета, конфликты имён
- [ ] 2. Референсы той же семьи из Icons/StatusEffects/references/
- [ ] 3. GenerateImage (промпт из PROMPT.md)
- [ ] 4. Finalize → 40×40 transparent PNG
- [ ] 5. Визуальная проверка (Read)
- [ ] 6. Wire Icon path (если просили / эффект существует)
```

### 1. Id и цвет

- Runtime файл: `Icons/StatusEffects/<EffectId>.png` (или явный ladder-name вроде `suppressionMedium.png`).
- Path в моде: `Mod/e6L4ECj/Icons/StatusEffects/<file>.png`.
- Не затирать существующий PNG без явного «заменить».
- Семья цвета — из [PROMPT.md](../../../Icons/StatusEffects/references/PROMPT.md) по `type`/polarity; severity ladder — исключение (как suppression).

| type / смысл | Семья | Hex |
| --- | --- | --- |
| Buff / позитивный System | sand | `#B8B880` … `#C0B880` |
| Debuff / негативный System | red | `#D83838` … `#E04040` |
| pain / vanilla suppressed | dark-red | `#A02020` / `#981818` |
| Hidden only | cream | `#E0D8C8` |
| Treating only | cyan | `#50A0C8` |

### 2–3. GenerateImage

1. Прочитать PROMPT.md (таблица рефов + шаблон промпта).
2. `reference_image_paths`: 2–3 PNG **той же семьи** из `Icons/StatusEffects/references/` (+ сосед серии из `Icons/StatusEffects/` для ladder).
3. `GenerateImage`, `aspect_ratio` `1:1`. В промпте: `EFFECT_ID`, `EFFECT_TYPE`, `COLOR_HEX`, `SYMBOL`.
4. Draft может быть на чёрном фоне — это нормально до finalize.

### 4. Finalize

```powershell
.agents/skills/create-jazz-status-icons/scripts/finalize-status-icon.ps1 `
  -SourceDraft "<path-to-generated.png>" `
  -EffectId Jazz_BleedResist
```

Скрипт: key near-black → alpha, resize **40×40**, пишет `Icons/StatusEffects/<EffectId>.png`.

Для **перекраски того же глифа** (severity):

```powershell
.agents/skills/create-jazz-status-icons/scripts/finalize-status-icon.ps1 `
  -SourceDraft "Icons/StatusEffects/suppressionHeavy.png" `
  -EffectId suppressionMedium `
  -Recolor "#FAFF00"
```

### 5. Визуальная проверка

Read итогового PNG:

- угол `(0,0)` с `A=0`
- нет непрозрачного чёрного фона на весь кадр
- силуэт читается; цвет семьи верный
- не путается с соседними иконками на 40×40

### 6. Wire

Если эффект уже в моде:

- `CharacterEffect/<EffectId>.lua` → `Icon = "Mod/e6L4ECj/Icons/StatusEffects/<file>.png"`
- тот же path в `items.lua`
- при необходимости `$sync-jazz-generated-data`

Новый эффект целиком — не этим skill: `$specify-jazz-change` + реализация CharacterEffect.

## Запреты

- Не править ванильные PNG в `Icons/StatusEffects/references/` (read-only style bank).
- Не класть иконки в `jazz_assets` / `jazz-maps` / `jazz-units` / корень `Icons/` (кроме уже существующих не-status ассетов).
- Не коммитить абсолютные локальные пути; не пушить без одобрения.
- Не смешивать генерацию иконок с массовым форматированием или несвязанным Lua.
