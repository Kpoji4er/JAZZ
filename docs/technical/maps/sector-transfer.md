# Трансфер локаций: vanilla HotDiamonds → jazz-maps

Канон дизайна: Google Sheet «Карта» → блок **Трансфер локаций** (spreadsheet `19Je4n5Ju4cYmTLimzw45aFq_Ll8Wxz21RLIETFRsH2g`, gid `863693534`, снимок 2026-08-01).

Machine-readable: [`data/sector-transfer.csv`](data/sector-transfer.csv).

Профиль **без maps** (`jazz-nomaps`) сохраняет vanilla ID — эта таблица для authored `jazz-maps` / `HotDiamonds` с `sector_bottomright = P32`.

| vanilla | maps | Название | runtime | source | notes |
| --- | --- | --- | --- | --- | --- |
| `A2` | `A4` | Даймонд Рэд | `ok` | sheet |  |
| `A11` | `B15` | Ферма Нигде (Nowhere) | `ok` | sheet |  |
| `A20` | `B28` | Орлиное гнездо | `ok` | sheet | Major HQ |
| `B2` | `C6` | Порт (рядом с Даймонд Рэд) | `ok` | sheet | sheet писал С6 (кириллица С) |
| `B12` | `A25` | Шахта Драхенберг | `ok` | sheet | sheet: Драхтенберг |
| `B13` | `A26` | Ландсбах / Лансбах | `ok` | sheet |  |
| `B16` | `D22` | Разлом (Аванпост) | `missing_moditem` | sheet |  |
| `C5` | `D9` | Лагерь Браконьеров | `ok` | sheet |  |
| `C7` | `E15` | Окраина Понтагрюэля (Мастерская) | `ok` | sheet | sheet target E15; D7 тоже → E15 |
| `D7` | `E15` | Понтагрюэль | `ok` | sheet | sheet: D7→E15 (трущобы/хаб — уточнять с runtime names) |
| `D8` | `E16` | Понтагрюэль Больница | `ok` | sheet |  |
| `D10` | `F23` | Аванпост Гран-При | `missing_moditem` | sheet |  |
| `E9` | `F13` | Лагерь Беженцев | `ok` | sheet |  |
| `F5` | `G9` | Код-Дазур (берег со сломанным кораблём) | `ok` | sheet |  |
| `H2` | `I5` | Деревня Эрни | `ok` | sheet |  |
| `H3` | `I6` | Жестянка | `ok` | sheet | sheet: H3 - I6 |
| `H4` | `I7` | Форт Ло-Блё (Аванпост) | `ok` | sheet | Ernie outpost / Global AI |
| `H7` | `H14` | Шахта (около Флитауна) | `ok` | sheet |  |
| `I1` | `K4` | Флаговый холм | `ok` | sheet |  |
| `I2` | `M4` | Смотровая площадка | `ok` | sheet | vanilla I2 ≠ maps I2 (доктор) |
| `I3` | `M7` | Изумрудный берег (пляж с минами) | `missing_moditem` | sheet | sheet → M7 (заглушка); runtime Emerald Coast = J7 |
| `I1` | `M1` | Старт кампании (зона высадки) | `ok` | suite-docs | suite: InitialSector M1; sheet I1→K4 is Flag Hill. This row is start remap, not Flag Hill. |

## Статусы

- `ok` — есть `ModItemSector` с этим `sectorId` в `jazz-maps/items.lua`.
- `missing_moditem` — target из sheet/suite не найден среди 245 authored sectors.

## Связанные документы

- [Атлас секторов](sector-atlas.md)
- [Сверка sheet ↔ runtime](sector-sheet-vs-runtime.md)
- Suite: [`maps-quests-content-catalog.md`](../systems/maps-quests-content-catalog.md)
