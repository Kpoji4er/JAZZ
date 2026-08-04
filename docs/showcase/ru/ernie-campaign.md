# Кампания на Эрни

[К обзору](home.md) · [Карта Grand Chien](grand-chien-map.md) · [Юниты Легиона](legion-units.md) · [Легион на стратегии](legion-strategy.md) · [English](../en/ernie-campaign.md)

Источник: `jazz-maps/items.lua` (сектора, квесты, setpieces). Демо-скоуп — остров Эрни; mainland в данных есть, полный playthrough не обещан. Расширенная сетка и переносы знакомых локаций — [карта Grand Chien](grand-chien-map.md).

## Старт

| | |
| --- | --- |
| Кампания | `HotDiamonds` |
| InitialSector | **M1** — «Зона высадки» |
| Setpiece входа | `M1Landing` (карта `EPA7FVN`) |
| Старт | reveal `M1`/`M2`/`M3` |

Города: **Ernie** (`ErnieVillage`), база повстанцев (`Rebels_Ernie`), контрабандисты (`SmugglersErnie`).

## Сектора Эрни (код)

Фильтр: `WeatherZone=Erny` **или** город `ErnieVillage`/`Rebels_Ernie` **или** `Label1=Ernie` → **20** секторов (не «23 из старого каталога»).

| Id | Имя в данных | Заметка |
| --- | --- | --- |
| M1 | Зона высадки | Старт |
| M2 | Скалистый берег | |
| M4 | The Outlook / смотровая | Label Ernie |
| M5 | Береговая линия | |
| M6 | Старый порт | |
| I2 | Лечебница в маяке | City ErnieVillage |
| I5 | Village of Ernie | Хаб |
| I6 | The Rust / Жестянка | Label Ernie |
| I6_Underground | Bunker FB45-68 | Label Ernie |
| I7 | Fort L'Eau Bleu | Outpost / Global AI |
| J5 | Фермы Эрни | |
| J7 | Emerald Coast | Herman |
| K4 | Flag Hill | |
| K5 | Походный лагерь Легиона | |
| K6 | Запасной лагерь контрабандистов | |
| L1 | База партизан | City Rebels_Ernie |
| L2 | Непроходимая местность | Rebels_Ernie |
| L5 | Походный лагерь Легиона | |
| L6 | Заброшенный вход в бункер | Rebels_Ernie |
| L7 | Рыбацкая деревня | |

Рядом на острове, но **без** Ernie-тега в ModItemSector: `I3`/`I4` (дорога к маяку), `M3` (водопад), `K3`/`L3`/`L4` (квест виллы), `I7_Underground`, `L6_Underground`.

## Квесты (из items.lua)

### QuestGroup «Ernie Island»

| Id | DisplayName | Hidden |
| --- | --- | --- |
| `TakeTheFortress` | Fort L'Eau Bleu | нет |
| `RescueHerMan` | Herman is missing | нет |
| `FortifyErnie` | Helping Ernie Village | нет |
| `ReduceFortressStrength` | How to reduce the Fort's defenses | да |
| `LegionFlag` | Fooling Pierre | да |
| `Ernie_CounterAttack` | *(без имени)* | да |

После освобождения деревни при вражеском форте — **квестовая** sat-атака с форта на деревню (~16 ч). Под Global AI / Vanilla Maps это снова работает; обычные ванильные периодические вылазки с managed-форта не включаются.
| `ErnieSideQuests` | *(без имени)* | да |
| `ErnieSideQuests_WorldFlip` | *(без имени)* | да |
| `RescueTeam` | Мы в спасатели нанимались | нет |
| `RebelsSavior` | Маленькая спасательная операция | нет |

### Intro / освобождение

| Id | DisplayName |
| --- | --- |
| `01_Landing` | Встреча с нанимателем |
| `02_LiberateErnie` | Retake Ernie Village |
| `02A_LiberateErnie_2` | Освобождение острова Эрни |
| `PierreDefeated` | Pierre |
| `JoseFamily` | Bastien |

### Ernie_Rebels / локальные JAZZ

| Id | DisplayName |
| --- | --- |
| `JAZZ_REBELS_0_MeetTheRebels` | Повстанцы |
| `JAZZ_REBELS_1_SeizeTheOutlook` | Атака на Смотровую Площадку |
| `Jazz_Doctor_need_Help` | Неугодный доктор |
| `JAZZ_Ernie_Locals_M2_SaveMyFamily` | Спасти Кики |
| `Jazz_ClearTheWay` | Зачистить лагеря вокруг Виллы |

## Setpieces

Зарегистрированы в maps: **`M1Landing`**, **`EncounterHerman`**. По ходу Эрни также вызываются (часто vanilla ID): `PierreLucTalk`, `ErnieReturn_FirstEnter`, `FortressBasement_FirstEnter`, `PierreDies` / `PierreRetreat`, `HangingLuc`, `BastienDies`.
