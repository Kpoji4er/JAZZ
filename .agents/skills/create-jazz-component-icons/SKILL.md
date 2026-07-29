---
name: create-jazz-component-icons
description: >-
  Создавать и обновлять полные WeaponComponent.Icon JAZZ для кабинета
  ModifyWeaponDlg (Icons/Upgrades/Full, детальнее чем chip). Не для ChipIcon
  миниатюр на тайле. Использовать при component Icon, upgrade icon, иконке
  обвеса в моддинге оружия.
---

# Создание WeaponComponent.Icon (кабинет)

Пакет: `jazz` → `Icons/Upgrades/Full/`.  
Промпты: [`Icons/Upgrades/Full/references/PROMPT.md`](../../../Icons/Upgrades/Full/references/PROMPT.md).  
Шпаргалка: [references/style-and-naming.md](references/style-and-naming.md).

Миниатюра тайла (`ChipIcon`) — **другой** skill: `$create-jazz-chip-icons`.  
Новый компонент: пара через оба skill; этим skill пишется только `Icon`.

Можно оставить vanilla `UI/Icons/Upgrades/…` если устраивает — генерить Jazz Full только когда нужна своя картинка или Icon пустой.

Asset-only PNG не требует spec. Wire `Icon` → `items.lua` sync.

## Контракт

| | |
| --- | --- |
| Поле | `Icon` |
| Path | `Mod/e6L4ECj/Icons/Upgrades/Full/<ComponentId>.png` |
| Size | **128×128** RGBA, transparent |
| UI | `ModifyWeaponDlg`, списки апгрейдов |
| Стиль | детальнее chip: узнаваемый обвес, всё ещё flat JA3, без фото |

## Вход

1. `ComponentId`
2. Slot + DisplayName / отличие
3. Показать draft до wire (если не «сразу вставь»)

## Workflow

```text
- [ ] 1. Id, конфликты
- [ ] 2. Рефы: Icons/Upgrades/Full/references/ (+ vanilla style bank если есть)
- [ ] 3. GenerateImage (PROMPT full)
- [ ] 4. Finalize → Icons/Upgrades/Full/<ComponentId>.png
- [ ] 5. Ревью
- [ ] 6. Wire Icon = "Mod/e6L4ECj/Icons/Upgrades/Full/<ComponentId>.png"
```

```powershell
.agents/skills/create-jazz-component-icons/scripts/finalize-component-icon.ps1 `
  -SourceDraft "<draft.png>" `
  -ComponentId AdvancedHOLO
```

## Запреты

- Не писать Full PNG в `ChipIcon` / `Icons/Upgrades/Chips/`.
- Не затирать vanilla `UI/Icons/Upgrades` на диске игры.
- Не генерить chip-миниатюры этим skill.
