---
id: JAZZ-WEAPON-SCAR-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
  - jazz_assets
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/InventoryItem/SCAR.lua
  - jazz/Code/Weapon_SCARModular.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/WeaponIcons/SCAR*.png
  - jazz/docs/tools/*scar*
  - jazz/docs/tools/README.md
  - jazz/docs/design/weapons-import-20261003-progress.md
  - jazz/docs/design/scar-import.md
  - jazz/docs/specs/active/JAZZ-WEAPON-SCAR-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/technical/weapons/data/*.csv
  - jazz/docs/wiki/weapons/**
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/*/weapons-and-ammo.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/JAZZ_SCAR*
  - jazz_assets/Entities/Meshes/JAZZ_SCAR*
  - jazz_assets/Entities/Materials/JAZZ_SCAR*
  - jazz_assets/Entities/Textures/JAZZ_SCAR*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_SCAR*
exclusive_resources:
  - items.lua
  - metadata.lua
  - localization-runtime-export
  - mod-editor-state
approved_by: project-owner
---

# JAZZ-WEAPON-SCAR-001: один FN SCAR, калибр и класс конфигурациями

## Проблема

Очередь №3. Предмета SCAR нет. Архив — 73 OBJ без MTL и без p3d; имя карты задаёт семейство, каналы — Arma. Ручная сборка отклонена владельцем. 08.10 владелец предоставил `untitled.blend`: взаимная посадка частей сохранена в координатах OBJ. Выделенная сборка H из model_0/1/3/4/7/8/11 принята по боковому clay-render. model_67 — EGLM, не верх оружия. 08.10 установлен локальный комплект L/H/SSR; игровая приёмка отложена владельцем.

## Цели

- Один предмет. Короткий L/H — карабин, обычный L/H — штурмовая винтовка, включая H под 7,62×51. SSR — боевая винтовка (`BattleRifle`) под 7,62×51, только одиночный огонь; решение владельца 08.10.2026.
- Материалы: цвет и нормаль без второй раскодировки и без переворота G; RM = (1 − gloss, 1 − gloss, metal). Specular не становится металлом.
- Масштаб новых стволов сверять с АК-74М (0,942 м). Короткий SCAR может быть короче; длинный не должен оказаться короче АК-74М.

## Non-goals

- Второй public ID, отдельные предметы на камуфляж и на каждый OBJ.
- Mk12, запуск игры, публикация.
- Параллельная реализация платных планок: слот Mount не добавлять своим кодом.
- Регистрация меша, пока цевьё не закрывает пролёт ствола и приклад не сидит на штифте.

## Требования

- `JAZZ-WEAPON-SCAR-001-REQ-001`: исходный архив read-only. В игре один предмет с L/H/SSR; исходная сборка H принята владельцем. L/SSR совмещаются по опорным точкам ресивера. Магазины STANAG/H и приклады — отдельные сущности; все материалы проверяются на финальных сборках.
- `JAZZ-WEAPON-SCAR-001-REQ-002`: рабочие статы плана для базы L/H: Damage 24/33, WeaponRange 48/56, Recoil 16/27, Grouping 63/60, AimAccuracy 13, RPM 650/600, магазин 30/20, ОД выстрела/перезарядки 5/6 и 6/6, Reliability 90, WeaponResource 10000. Короткий ствол: Damage −1, Range −8, Recoil +2, Grouping −3. Длинный: Range +8, Grouping +3, AimAccuracy +1. ОД от длины ствола не снижать. После просьбы завершить винтовку целиком SSR установлен с рабочими числами H + длинный ствол (33/64/27/63/14); окончательная балансная приёмка впереди.
- `JAZZ-WEAPON-SCAR-001-REQ-003`: дизайнерский тир Т3, подступень плана Т3-2 как рабочая, не как принятый баланс. Bobby Ray in: CanAppearInShop, Tier 4, RestockWeight 25, MaxStock 1, Cost 22000, CategoryPair AssaultRifles. Игровой Т3-2 не записывать в поле Tier.
- `JAZZ-WEAPON-SCAR-001-REQ-004`: items, metadata, companion и сущности одной транзакцией; RU/EN через экспорт локализации; иконка 324×165 с тёмным контуром из финальной сборки. Holster Shoulder.

## Инварианты и ограничения

Архив и чужие предметы не менять. Не создавать custom/split normals. Не инвертировать RM целиком. Камуфляж, tan и Mk17-tan — перекраски, не предметы. Существующие компоненты оптики и дульных устройств переиспользовать, не копировать ради SCAR.

## Acceptance criteria

- `JAZZ-WEAPON-SCAR-001-AC-001`: боковой и верхний вид собранного короткого L, длина в метрах рядом с 0,942 м, цевьё закрывает ствол, приклад на штифте, магазин подающей частью в шахту. Compiled mesh без нулевых нормалей, winding проверен.
- `JAZZ-WEAPON-SCAR-001-AC-002`: смена калибра L/H сохраняет экземпляр и не оставляет чужие патроны. SSR меняет класс экземпляра на BattleRifle, калибр на 7,62×51 и оставляет одиночный огонь; простой длинный ствол класс SSR не включает. Числа SSR и runtime-проверка остаются открытыми.
- `JAZZ-WEAPON-SCAR-001-AC-003`: три слоя регистрации, RU/EN и иконка согласованы. Editor и игра — отдельно, игру не запускать.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: один новый предмет и его сущности; общий setter компонентов не оборачивать второй раз.
- Saves: новый ID, старые сохранения не мигрируют.
- Network/determinism: штатная смена компонентов, без своего RNG.
- Generated data: jazz и jazz_assets одной транзакцией.
- Cross-package references: предмет в jazz, меши в jazz_assets.
- Rollback/recovery: hash-guarded backup до записи items.lua.

## План и ownership

jazz — предмет, код, иконки, локализация. jazz_assets — сущности. Исполнитель — текущий чат. Reviewer — владелец, игровая проверка отложена до всего комплекта. Declared write set и exclusive resources — в шапке. Изменения не коммитить без отдельной просьбы.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец, очередь «делай все сразу по списку» и повторное «делай» на SCAR после проверки, что карты назначаются по имени, а конвертировать нужно каналы Arma.
- Дата: 2026-10-04.
- 2026-10-08: владелец принял исходную сборку («идеально»), разрешил подготовку модулей и уточнил «SSR пусть в боевую винтовку превращает». Первый комплект: L/H, три длины ствола, складной штатный приклад, магазины по калибру, оптика, дульники, рукоятка/сошки, фонарь/ЛЦУ. EGLM и PDW — следующие этапы.
- Mk12 по-прежнему исключён. Игру не запускать.

## Evidence

- `JAZZ-WEAPON-SCAR-001-AC-001`: static PASS — 14 compiled mesh audits, поверхности в пределах 0,1 мм; H/L/SSR проверены на финальном material preview. Human — H принят владельцем; игровые материалы/обвес ещё NOT_RUN.
- `JAZZ-WEAPON-SCAR-001-AC-002`: static PASS — 12 executable Lua checks на установленном коде: L/H × три ствола, SSR BattleRifle/SingleShot, обратимость, патроны, clone isolation, складная иконка. Runtime/save-load NOT_RUN.
- `JAZZ-WEAPON-SCAR-001-AC-003`: static PASS — companion/ModItem/metadata, 14 entities, 13 иконок согласованы; 21 строка RU/EN установлена парным каноническим экспортом; scoped needs/collisions = 0. Общие ранее существовавшие проблемы локализации сохранены отдельно, не исправлялись в этой задаче. Editor NOT_RUN по просьбе владельца.

## Documentation delta

Текущее установленное поведение описано в weapons-ammo-components, file-coverage, wiki и showcase RU/EN. Детали сборки и артефакты: [scar-import](../../design/scar-import.md). Статус approved сохраняется до общей игровой приёмки.
