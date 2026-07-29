---
name: create-jazz-perk-icons
description: Создавать и обновлять 68×68 PNG-иконки именных и сигнатурных перков JAZZ в стиле JA3. Использовать при запросе perk icon, Perks/Personal, SignatureAbilities или иконок JA1/JA2-мерков.
---

# Создание иконок перков JAZZ

Пакет: `jazz`. Runtime: `Perks/Personal/` и `Perks/SignatureAbilities/`.  
Референсы vanilla: `Perks/references/vanilla/`.

Asset-only PNG не требует spec. Изменение `Icon` path требует синхронизации companion и `items.lua`.

## Контракт

- Итог: **68×68 RGBA PNG**.
- Фон: **прозрачный (`A=0`)**, не чёрная заливка.
- Глиф: muted teal-grey, минималистичный силуэт, читаемый при 68×68.
- Без текста, букв, цифр, рамки, логотипа и подписи.
- Символ выбирать прежде всего из `Description` и `Mechanics`; `DisplayName` — только дополнительная подсказка.
- Один главный механический эффект на глиф; вторичный эффект обозначать простым модификатором (AP-стрелка, aura ring, crossed-out status).

## Workflow

1. Прочитать Named perk в `docs/design/mercs-ja12/<slug>.md`: `Description` и `Mechanics`.
2. Выбрать 2–3 референса из `Perks/Personal/` или `Perks/references/vanilla/`.
3. GenerateImage, `aspect_ratio: 1:1`; явно потребовать transparent-ready black draft, no text.
4. Финализировать:

   ```powershell
   .agents/scripts/finalize-perk-icon.ps1 `
     -SourceDraft "<draft.png>" `
     -Name "<MercName>"
   ```

5. Проверить итог:
   - размер 68×68;
   - углы и фон имеют `A=0`;
   - нет чёрного прямоугольника или тёмного halo;
   - символ соответствует механике, а не только названию;
   - нет случайного текста.
6. Если меняется runtime path, обновить `CharacterEffect/Jazz_Perk_<Name>.lua` и ту же запись в `items.lua`.

## Запреты

- Не сохранять непрозрачный чёрный фон.
- Не использовать портрет мерка вместо механического символа.
- Не затирать vanilla refs.
- Не считать draft готовым без запуска финализатора и alpha-аудита.
