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
| `H14` | `P17` | Камп Де Крокодиль | `ok` | suite-docs | crocodile camp; not mine H7→H14 |
| `B10` | `A5` | Highlands / вход в Lost Basin | `ok` | owner | копия ванили Maps/WfHkNqA (B-10 - Wasteland), не sVQSE5 |
| `B10_Underground` | `A5_Underground` | Lost Basin | `ok` | owner | копия ванили Maps/WfHkNqU (B-10U - Lost Basin); GroundSector A5 |
| `A6` | `A21` | Пит-Стоп база (ванильный A6) | `ok` | owner | копия ванили на Maps/fVoG4zR |
| `A6_Underground` | `A21_Underground` | Шахта под СТО (ванильный A6U) | `ok` | owner | копия ванили на Maps/UFYsMp; GroundSector A21 |
| `A7` | `A22` | Термитник (ванильный A7) | `ok` | owner | копия ванили на Maps/gmeyzDK |
| `G16` | `M18` | Marshlands (ванильный G16) | `ok` | owner | копия ванили на Maps/qdVPuVK; maps G16 minefield aApUtcM не тронут |
| `D10` | `D18` | Аванпост Гран-При (runtime) | `ok` | suite-docs | sheet F23 missing_moditem; live Camp Grand Prix = D18 |
| `D6` | `E14` | Окраины Понтагрюэля | `ok` | suite-docs | vanilla D6; maps E16 is downtown |
| `D17` | `F28` | Иль-Мора | `ok` | suite-docs | vanilla D17 |
| `C11` | `C14` | Старая бензоколонка | `ok` | suite-docs | vanilla C11 |
| `B9` | `C12` | Пит-стоп | `ok` | suite-docs | ReduceCrossroads repair shop |
| `F7` | `E10` | Кам-Саван | `ok` | suite-docs | vanilla F7 ≠ maps F7 (нет ModItem) |
| `G6` | `G13` | Колодец Саванны | `ok` | suite-docs | SavannaCamp water well map jfUUwFo |
| `G10` | `L15` | Кам-Ла-Барьер | `ok` | suite-docs | vanilla G10 ≠ maps G10 Ла-Палисад |
| `E16` | `G22` | Кам-Шьен-Саваж | `ok` | suite-docs | vanilla E16 ≠ maps E16 центр Понтагрюэля |
| `F19` | `K21` | Кам-Бьян-Шьен | `ok` | suite-docs | vanilla F19 ≠ maps F19 берег в джунглях |
| `F13` | `G25` | Шале-де-ла-Пе | `ok` | suite-docs | vanilla F13 ≠ maps F13 лагерь беженцев |
| `I18` | `H31` | Вассерграб | `ok` | suite-docs | vanilla I18 ≠ maps I18 Great Forest (crocodile patrol) |
| `I19` | `H32` | Мрачная деревня / Grimer | `ok` | suite-docs | vanilla I19 ≠ maps I19 wetlands bunker |

## Статусы

- `ok` — есть `ModItemSector` с этим `sectorId` в `jazz-maps/items.lua`.
- `missing_moditem` — target из sheet/suite не найден среди authored `ModItemSector`.

## Связанные документы

- [Атлас секторов](sector-atlas.md)
- [Сверка sheet ↔ runtime](sector-sheet-vs-runtime.md)
- Suite: [`maps-quests-content-catalog.md`](../systems/maps-quests-content-catalog.md)
