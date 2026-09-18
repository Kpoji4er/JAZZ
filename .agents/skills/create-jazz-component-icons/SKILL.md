---
name: create-jazz-component-icons
description: >-
  Использовать при WeaponComponent.Icon кабинета (100×100). Не для ChipIcon на тайле.
---

# Создание WeaponComponent.Icon (кабинет)

**Канон сейчас — style B** (тёмный 3D): `WeaponComponents/<Folder>/`.  
Промпты: [`WeaponComponents/references/PROMPT.md`](../../../WeaponComponents/references/PROMPT.md).  
Шпаргалка: [references/style-and-naming.md](references/style-and-naming.md).

Миниатюра тайла (`ChipIcon`) — **другой** skill: `$create-jazz-chip-icons`.

Уникальные Entity / уникальный Id у **Scope** и **Magazine** → уникальный `Icon`.  
**Barrel**: уникальные Icon не требуются (vanilla OK).

Asset-only PNG не требует spec. Wire `Icon` → `items.lua` sync.

Для генерации/редактирования применять доступный `$imagegen` и актуальную схему его инструмента. Размеры и пропорции ниже — требования к результату, не имена API-параметров. Передавать референсы способом, поддерживаемым инструментом; финализацию выполнять с учётом его инструкций.

## Контракт (style B)

| | |
| --- | --- |
| Поле | `Icon` |
| Path | `Mod/e6L4ECj/WeaponComponents/<Folder>/<ComponentId>.png` |
| Size | **100×100** RGBA, transparent |
| UI | `ModifyWeaponDlg`, списки апгрейдов |
| Стиль | dark 3D + **soft Anaconda silhouette AA** (реф `style_B_edge_ref_Anaconda.png`) |
| Gen BG | magenta `#FF00FF` (не portrait `#504633`) |
| Cut | rembg → fit ~78% → black outline (`docs/tools/_finalize_icon_style_b.py`) |

## Magazine orientation

Как магазин висит на винтовке **вид сбоку**, дуло вправо:

1. Губки (**feed lips**) — сверху  
2. Пятка — снизу  
3. Изгиб AK — вперёд/вправо (к дулу)  
4. Почти вертикально, лёгкий forward lean  
5. Только магазин — без receiver / magwell  

## Вход

1. `ComponentId`
2. Slot + DisplayName / отличие
3. Уточнить scope из запроса: только draft или готовая вставка. Для явно разрешённой вставки повторное согласование не нужно; при запросе draft wiring не выполнять.

## Workflow

```text
- [ ] 1. Id, конфликты; Scope/Magazine → unique Icon if unique look
- [ ] 2. Рефы: **shape** = WC 3D / Visual.Icon / vanilla (chip — last resort); **style** = Anaconda + Optics
- [ ] 3. генерация изображения на #FF00FF **с точным shape-рефом** (не chip-глиф, если есть CarbineMag/Optics)
- [ ] 4. Finalize → WeaponComponents/<Folder>/<ComponentId>.png
- [ ] 5. Ревью (силуэт = chip, край = Anaconda)
- [ ] 6. Wire Icon = "Mod/e6L4ECj/WeaponComponents/<Folder>/<ComponentId>.png"
```

```text
python docs/tools/_finalize_icon_style_b.py
```

## Запреты

- Не писать Icon PNG в `ChipIcon` / `Icons/Upgrades/Chips/`.
- Не key с `#504633` для тёмного металла (съедает объект) — только magenta / rembg.
- Не генерить chip-миниатюры этим skill.
- Не шарить один Icon на разные уникальные Scope/Magazine.
