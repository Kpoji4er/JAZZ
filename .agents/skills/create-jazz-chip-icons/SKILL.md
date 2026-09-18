---
name: create-jazz-chip-icons
description: >-
  Использовать при ChipIcon 64×64 (Icons/Upgrades/Chips). Не для полной Icon кабинета.
---

# Создание ChipIcon (миниатюры чипов)

Пакет: `jazz` → `Icons/Upgrades/Chips/`.  
Промпты: [`Icons/Upgrades/Chips/references/PROMPT.md`](../../../Icons/Upgrades/Chips/references/PROMPT.md).  
Шпаргалка: [references/style-and-naming.md](references/style-and-naming.md).

Полная иконка кабинета (`WeaponComponent.Icon`) — **другой** skill: `$create-jazz-component-icons`.  
Новый компонент, доступный на оружии: сделать **оба** skill (пара Icon + ChipIcon), но генерация раздельная.

Asset-only PNG не требует spec. Wire `ChipIcon` → `items.lua` sync.

Для генерации/редактирования применять доступный `$imagegen` и актуальную схему его инструмента. Размеры и пропорции ниже — требования к результату, не имена API-параметров. Передавать референсы способом, поддерживаемым инструментом; финализацию выполнять с учётом его инструкций.

## Контракт

| | |
| --- | --- |
| Поле | `ChipIcon` |
| Path | `Mod/e6L4ECj/Icons/Upgrades/Chips/<ComponentId>.png` |
| Size | **64×64** RGBA, transparent |
| UI | inventory / HUD attachment chips |
| Стиль | ultra-simple glyph, читается на ~22–24px |

Runtime: `ChipIcon` → иначе `Icon` → иначе `slot_*` fallback (`$create-jazz-chip-icons` не пишет в `Icon`).

**Не генерить ChipIcon** для слотов `Mount` / `Mount1` / `Mount2` / `Mountside` / `Mountfront` (крепы/планки не показываем чипами).

## Вход

1. `ComponentId`
2. Slot + DisplayName / отличие от соседей
3. Уточнить scope из запроса: только draft или готовая вставка. Для явно разрешённой вставки повторное согласование не нужно; при запросе draft wiring не выполнять.

## Workflow

```text
- [ ] 1. Id, конфликты PNG
- [ ] 2. Рефы: Icons/Upgrades/Chips/references/ + соседние Chips/
- [ ] 3. генерация изображения (PROMPT chip)
- [ ] 4. Finalize → Icons/Upgrades/Chips/<ComponentId>.png
- [ ] 5. Самостоятельная визуальная QA; согласование draft только если пользователь его запросил
- [ ] 6. Wire ChipIcon path в items.lua
```

```powershell
.agents/skills/create-jazz-chip-icons/scripts/finalize-chip-icon.ps1 `
  -SourceDraft "<draft.png>" `
  -ComponentId AdvancedHOLO
```

## Запреты

- Не писать Chip PNG в поле `Icon` / не класть в `Icons/Upgrades/` корень вместо `Chips/`.
- Не затирать vanilla `UI/Icons/Upgrades`.
- Не генерить full component Icon этим skill.
