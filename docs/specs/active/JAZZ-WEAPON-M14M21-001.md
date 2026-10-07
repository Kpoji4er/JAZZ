---
id: JAZZ-WEAPON-M14M21-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/Weapon_M14Modular.lua
  - jazz/Code/System_WeaponComponent_Set.lua
  - jazz/InventoryItem/M14SAW.lua
  - jazz/InventoryItem/M21.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/Strings.csv
  - jazz-units/items.lua
  - jazz/docs/specs/active/JAZZ-WEAPON-M14M21-001.md
  - jazz/docs/specs/active/JAZZ-WEAPON-M14-FAMILY-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/design/weapons-import-20261003-progress.md
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz-units/items.lua
related_decisions:
  - JAZZ-WEAPON-M14-FAMILY-001
  - JAZZ-WEAPON-RAIL-001
approved_by: project-owner in conversation 2026-10-08
---

# JAZZ-WEAPON-M14M21-001: M14 и M21 — один предмет

## Проблема

`M14SAW` и `M21` — два магазинных ствола на одном хосте `JAZZ_M14`. M21 отличается оптикой ART (`JAZZ_M14_ART`), классом `SniperRifle` и отсутствием автоогня. План импорта уже фиксирует склейку; отдельный предмет M21 этому противоречит.

## Цели

- В магазине и у новых выдач остаётся один ствол `M14SAW`.
- Снайперский комплект на существующих моделях делает из него M21: модель ART, имя, класс, без автоогня, выше кучность, открытый слот прицела.

## Non-goals

- Новый меш, иконка или сущность. Хост остаётся `JAZZ_M14`, оптика — уже существующая `JAZZ_M14_ART`.
- Mk 14 EBR, M14 Mk III, M1A и Gold Fever.
- Смена отдачи, дальности, надёжности, магазина, калибра, тира и цены `M14SAW`.
- Рукояти и гранатомёт на деревянном M14. Нижний слот по-прежнему только сошки.

## Требования

- `JAZZ-WEAPON-M14M21-001-REQ-001` — публичный предмет один: `M14SAW`, класс по умолчанию `BattleRifle`, хост `JAZZ_M14`. `M21` остаётся в данных только как старый id. `CanAppearInShop = false`, `RestockWeight = 0`. На `LoadGame` и `NewGame` экземпляр `M21` становится `M14SAW` со снайперским комплектом; патроны и общие компоненты сохраняются. Если на нём стояла планка `JAZZ_Rail_M21`, она снимается: крепление даёт комплект. Пустой слот прицела заполняется `JAZZ_Scope_M21_ART`.
- `JAZZ-WEAPON-M14M21-001-REQ-002` — компонент `JAZZ_M14_SniperKit`, слот `Conversion`. Денежная цена 0, `AdditionalCosts` 1000 `Parts`, `ModificationDifficulty` 0. Это тариф полной переделки из `JAZZ-WEAPON-RAIL-001`: отдельной цены владелец 08.10.2026 не назвал, а комплект меняет класс ствола. Имя детали: английский исходник `Sniper Kit`, русский перевод «Снайперский комплект». Визуал комплекта на `M14SAW` — существующий кронштейн `JAZZ_M14_OpticsMount`.
- `JAZZ-WEAPON-M14M21-001-REQ-003` — пока комплект стоит, экземпляр получает имя и иконку `M21`, `object_class` `SniperRifle`, атаки `SingleShot`, `JAZZ_JokerShot`, `JAZZ_Bullseye`, `AutoShots` 0 и `BurstShots` 0. Кучность становится числом M21: `Grouping` 45 и `AimAccuracy` 12. Снятие комплекта возвращает имя, иконку, класс `BattleRifle`, атаки и числа `M14SAW`. Класс инвентаря и сущность хоста не меняются.
- `JAZZ-WEAPON-M14M21-001-REQ-004` — без комплекта любой не механический прицел на `M14SAW` запрещён. С комплектом слот открыт, включая `JAZZ_Scope_M21_ART` с мешем `JAZZ_M14_ART`. Первая установка комплекта на пустой слот прицела ставит ART, поэтому модель сразу становится M21. Снять комплект при установленном прицеле нельзя: кабинет называет этот прицел. Поставить прицел без комплекта нельзя: кабинет называет комплект.
- `JAZZ-WEAPON-M14M21-001-REQ-005` — готовые комплекты, которые спавнили `M21`, спавнят `M14SAW`. В списке улучшений комплект стоит перед прицелом. `JAZZ_Rail_M21` в этих списках заменяется комплектом. Если прицела в списке не было, добавляется `JAZZ_Scope_M21_ART`.

## Инварианты и ограничения

- `MK14EBR`, `JAZZ_M14_MkIII`, `M1A`, `GoldenGun` и их слоты не меняются.
- Нижний слот `M14SAW` принимает только `JAZZ_Bipod_Under` или пусто.
- Один wrap `FirearmBase:SetWeaponComponent` и `ModifyWeaponDlg:CanModifySlot`. Поведение M14 живёт в методе `M14SAW` и в уже существующем `JAZZ_RailReject`.
- Новые глобалы объявляются при загрузке `Code/Weapon_M14Modular.lua`.

## Acceptance criteria

- `JAZZ-WEAPON-M14M21-001-AC-001` — static: у `JAZZ_M14_SniperKit` слот `Conversion`, `Cost` 0, 1000 `Parts`. `M21.CanAppearInShop` ложно. В `M14SAW` есть слот `Conversion` и прицел `JAZZ_Scope_M21_ART`.
- `JAZZ-WEAPON-M14M21-001-AC-002` — static: правило прицела `M14SAW` требует комплект; снятие комплекта при занятом прицеле возвращает id прицела. Runtime: в кабинете M14 без комплекта прицел не ставится, с комплектом имя M-21, автоогня нет, стоит ART, `Grouping` 45.
- `JAZZ-WEAPON-M14M21-001-AC-003` — static: лут-дефы бывшего M21 ссылаются на `M14SAW`, и комплект в списке раньше прицела.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: класс `M21` остаётся для старых сохранений и мигрирует на загрузке.
- Saves: существующий M21 становится M14 с комплектом и сохраняет патроны. Уже установленный прицел на M14 получает комплект бесплатно тем же проходом, что и остальные крепления.
- Network/determinism: без нового RNG.
- Generated data: `items.lua`, companion и `metadata.code`.
- Cross-package references: лут `jazz-units`.
- Rollback/recovery: снять комплект можно после снятия прицела; ствол возвращается к M14.

## План и ownership

- Пакет-владелец: `jazz`. Лут — `jazz-units`.
- Исполнитель: текущий агент.
- Reviewer: владелец, кабинет в игре.
- Declared write set: фронт spec.
- Exclusive resources: `jazz/items.lua`, `jazz/metadata.lua`, `jazz-units/items.lua`.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец в чате 08.10.2026. Склейка M14/M21 на существующих моделях. Снайперский комплект меняет модель, название и класс, отключает автоогонь, повышает кучность и открывает прицел.
- Дата: 2026-10-08.

## Evidence

- `JAZZ-WEAPON-M14M21-001-AC-001`: `PASS` — static, 08.10.2026. В `items.lua` у `JAZZ_M14_SniperKit` слот `Conversion`, `Cost` 0, 1000 `Parts`. `M21.CanAppearInShop` ложно. У `M14SAW` есть слот `Conversion` и `JAZZ_Scope_M21_ART`.
- `JAZZ-WEAPON-M14M21-001-AC-002`: `BLOCKED` — static-правило записано (`M14SAW` требует комплект, снятие комплекта при прицеле возвращает id прицела), но кабинет в игре не открывался.
- `JAZZ-WEAPON-M14M21-001-AC-003`: `PASS` — static, 08.10.2026. В `jazz-units/items.lua` нет `weapon = "M21"`; у бывших M21 комплект стоит раньше прицела, оружие `M14SAW`.

## Documentation delta

- `docs/technical/systems/weapons-ammo-components.md` и `file-coverage.md`.
- Игровые `docs/wiki/weapons-and-ammo.md`, `docs/showcase/ru/weapons-and-ammo.md`, `docs/showcase/en/weapons-and-ammo.md`.
- Строка прогресса в `docs/design/weapons-import-20261003-progress.md`.
