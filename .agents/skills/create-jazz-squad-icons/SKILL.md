---
name: create-jazz-squad-icons
description: >-
  Создавать и обновлять 64×64 сателлитные иконки ролей отрядов JAZZ
  (Legion/Army/Adonis/Rebels/Smugglers) по единому шаблону щит+символ.
  Использовать при запросе новой squad icon, role PNG в SquadsIcons/Enemy,
  переносе силуэта на щиты фракций или правке галереи squad-role-icons.md.
---

# Создание squad role icons

Пакет-владелец ассетов: `jazz` → `SquadsIcons/Enemy/`.  
Current-state каталог: `docs/technical/systems/squad-role-icons.md`.  
Детали стиля и промпта: [references/style-and-naming.md](references/style-and-naming.md).

Asset-only PNG **не** требует spec. Привязка role → path в `Guardpost_Patrols.lua` / director — отдельное behaviour-изменение → `$specify-jazz-change`.

## Вход от пользователя

Минимум:

1. `ROLE` в `SCREAMING_SNAKE` (пример: `TAX`, `REINFORCE`).
2. Смысл роли одним предложением.
3. Символ (или 2–3 варианта на выбор).
4. Фракции: по умолчанию все пять; иначе явный список.

Если символ неочевиден — предложить 2–3 варианта, не пересекающихся с уже занятыми (череп, башня, стрелы, бинокль, тесак, грузовик, ромб, плюс, кулак, мегафон, колонна, мешок).

## Workflow

Скопировать и вести чеклист:

```text
- [ ] 1. Имя файла и конфликты
- [ ] 2. Draft символа (GenerateImage + референсы)
- [ ] 3. Композит Legion
- [ ] 4. Порты фракций
- [ ] 5. Визуальная проверка
- [ ] 6. Обновить squad-role-icons.md
- [ ] 7. Runtime wiring (только если просили)
```

### 1. Имя и конфликты

- Файл: `<faction>_<ROLE>_squad.png`
- `faction` ∈ `legion` · `army` · `adonis` · `rebels` · `smugglers`
- Runtime path: `Mod/e6L4ECj/SquadsIcons/Enemy/<file>.png`
- Не затирать существующий ROLE без явного «заменить».

### 2. Draft символа

1. Прочитать style bible в [style-and-naming.md](references/style-and-naming.md).
2. Взять референсы: `legion.png` + 2–3 близких `legion_*_squad.png`.
3. Сгенерировать draft через `GenerateImage` (`aspect_ratio` `1:1`), промпт из reference.
4. Итерировать, пока силуэт читается на 64×64 и не путается с соседними ролями.

### 3. Композит Legion

Запустить скрипт (предпочтительно) или повторить его логику:

```powershell
.agents/skills/create-jazz-squad-icons/scripts/compose-role-icon.ps1 `
  -Role TAX `
  -SourceDraft "<path-to-generated-draft.png>" `
  -Factions legion,army,adonis,rebels,smugglers
```

Обязательные свойства выхода:

- `64×64`, `Format32bppArgb`
- **прозрачный** canvas вне щита (`A=0`), не заливать непрозрачным чёрным
- ivory только при `A >= 200` у исходника (прозрачный «белый» canvas — не ivory)
- символ только на непрозрачных пикселях щита
- тёмный 1px outline вокруг символа
- без бежевой кромки по верху щита (rim-артефакты снимать)

### 4. Порты фракций

Тот же силуэт на `army.png` / `adonis.png` / `rebels.png` / `smugglers.png`.  
Скрипт с `-Factions` без `legion` — только порты с уже готового `legion_<ROLE>_squad.png`:

```powershell
.agents/skills/create-jazz-squad-icons/scripts/compose-role-icon.ps1 `
  -Role TAX `
  -SourceLegion `
  -Factions army,adonis,rebels,smugglers
```

### 5. Визуальная проверка

Прочитать итоговые PNG инструментом Read (картинки):

- угол `(0,0)` прозрачный (`A=0`)
- нет ivory-заливки фона
- символ отличим от соседних ролей на мелком размере

### 6. Документация

В том же change set обновить `docs/technical/systems/squad-role-icons.md`:

- строка в таблице ролей (`asset only` или `wired`)
- ряд превью во всех нужных фракциях

Коммит asset/docs-only помечать как технический:

```text
docs(squad-icons): ...

Technical/docs-only. Do not include in player changelog. [skip discord]
```

### 7. Runtime wiring

Только по явной просьбе: path map в `Guardpost_Patrols.lua`, diagnostics/tests, `$specify-jazz-change` при новом поведении.

## Запреты

- Не класть иконки в `jazz_assets` / `jazz-maps` / `jazz-units`.
- Не коммитить абсолютные локальные пути.
- Не пушить без отдельного одобрения.
- Не смешивать генерацию иконок с массовым форматированием или несвязанным Lua.
