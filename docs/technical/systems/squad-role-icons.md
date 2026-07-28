# Squad role icons (enemy satellite)

Каталог PNG для сателлитных иконок отрядов Global AI / фракций. Файлы — `64×64`, **прозрачный** canvas вне щита (как у `legion.png` / `army.png`), щит фракции + ivory-силуэт роли.

Пути runtime: `Mod/e6L4ECj/SquadsIcons/Enemy/<file>.png`  
Ассеты: [`SquadsIcons/Enemy/`](../../../SquadsIcons/Enemy/)  
Стратегический контекст: [strategy-squads-sectors.md](strategy-squads-sectors.md) · wiki: [legion-global-ai.md](../../wiki/legion-global-ai.md)

---

## Базовые щиты фракций

Пустой щит без ролевого символа (подложка для композита).

| Фракция | Файл | Щит |
| --- | --- | --- |
| Legion | `legion.png` | ![legion](../../../SquadsIcons/Enemy/legion.png) |
| Army | `army.png` | ![army](../../../SquadsIcons/Enemy/army.png) |
| Adonis | `adonis.png` | ![adonis](../../../SquadsIcons/Enemy/adonis.png) |
| Rebels | `rebels.png` | ![rebels](../../../SquadsIcons/Enemy/rebels.png) |
| Smugglers | `smugglers.png` | ![smugglers](../../../SquadsIcons/Enemy/smugglers.png) |

Доп. варианты щитов (не ролевые): `army2.png`, `army3.png`, `rebels2.png`, `rebels3.png`, `enemy_squad.png`, `nazi.png`.

---

## Роли — смысл и символ

| Role ID | Смысл | Символ | Статус runtime (Legion) |
| --- | --- | --- | --- |
| `major` / BASE | Штаб / Major response | череп | wired → `legion_BASE_squad.png` |
| `garrison` | Держит сектор | башня / rook | wired |
| `patrol` | Патруль ключевых точек | скрещённые стрелы | wired |
| `recon` | Наблюдение / разведка | бинокль | wired |
| `qrf` | Быстрая реакция | тесак / cutlass | wired |
| `supply` | Конвой снабжения | грузовик | wired |
| `shipment` | Алмазный груз в HQ | грузовик + ромб | wired |
| `reinforce` | Пограничное усиление гарнизона | плюс | asset only |
| `retribution` | Карательный удар Major с HQ | кулак | asset only |
| `recruiter` | Вербовщик / агитатор | мегафон | asset only |
| `manpower` | Конвой живой силы | колонна солдат с флагом | asset only |
| `tax` | Сбор налогов / дани | мешок с монетами | asset only |

`wired` = путь в `Guardpost_Patrols.lua` → `JAZZ_GetLegionAISquadIcon`.  
`asset only` = PNG есть у всех фракций, роль в director ещё не привязана.

Имена файлов: `<faction>_<ROLE>_squad.png`  
`faction` ∈ `legion` · `army` · `adonis` · `rebels` · `smugglers`

---

## Галерея по ролям

### BASE / major — череп

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_BASE_squad.png) | ![A](../../../SquadsIcons/Enemy/army_BASE_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_BASE_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_BASE_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_BASE_squad.png) |

### GARRISON — башня

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_GARRISON_squad.png) | ![A](../../../SquadsIcons/Enemy/army_GARRISON_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_GARRISON_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_GARRISON_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_GARRISON_squad.png) |

### PATROL — скрещённые стрелы

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_PATROL_squad.png) | ![A](../../../SquadsIcons/Enemy/army_PATROL_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_PATROL_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_PATROL_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_PATROL_squad.png) |

### RECON — бинокль

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_RECON_squad.png) | ![A](../../../SquadsIcons/Enemy/army_RECON_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_RECON_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_RECON_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_RECON_squad.png) |

### QRF — тесак

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_QRF_squad.png) | ![A](../../../SquadsIcons/Enemy/army_QRF_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_QRF_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_QRF_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_QRF_squad.png) |

### SUPPLY — грузовик

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_SUPPLY_squad.png) | ![A](../../../SquadsIcons/Enemy/army_SUPPLY_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_SUPPLY_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_SUPPLY_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_SUPPLY_squad.png) |

### SHIPMENT — грузовик + ромб

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_SHIPMENT_squad.png) | ![A](../../../SquadsIcons/Enemy/army_SHIPMENT_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_SHIPMENT_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_SHIPMENT_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_SHIPMENT_squad.png) |

### REINFORCE — плюс *(asset only)*

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_REINFORCE_squad.png) | ![A](../../../SquadsIcons/Enemy/army_REINFORCE_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_REINFORCE_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_REINFORCE_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_REINFORCE_squad.png) |

### RETRIBUTION — кулак *(asset only)*

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_RETRIBUTION_squad.png) | ![A](../../../SquadsIcons/Enemy/army_RETRIBUTION_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_RETRIBUTION_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_RETRIBUTION_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_RETRIBUTION_squad.png) |

### RECRUITER — мегафон *(asset only)*

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_RECRUITER_squad.png) | ![A](../../../SquadsIcons/Enemy/army_RECRUITER_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_RECRUITER_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_RECRUITER_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_RECRUITER_squad.png) |

### MANPOWER — колонна солдат *(asset only)*

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_MANPOWER_squad.png) | ![A](../../../SquadsIcons/Enemy/army_MANPOWER_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_MANPOWER_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_MANPOWER_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_MANPOWER_squad.png) |

### TAX — мешок с монетами *(asset only)*

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion_TAX_squad.png) | ![A](../../../SquadsIcons/Enemy/army_TAX_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis_TAX_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels_TAX_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers_TAX_squad.png) |

---

## Style bible (кратко)

- Canvas `64×64`, **прозрачный** фон вне щита (не заливать непрозрачным чёрным)
- Щит: плоский верх, вертикальные бока, остриё снизу
- Символ: ivory/cream, толстый силуэт, читается в мелком масштабе
- Без текста, цифр, градиентов, фотореализма
- Legion: сплошной madder-red; Army — красно-коричневый camo; Adonis — purple; Rebels — green camo; Smugglers — money/orange

Порты фракций: ivory-маска с `legion_*_squad.png` → поверх щита фракции + тёмный 1px outline символа. Маска обязана игнорировать прозрачные пиксели (`A < 200`).

---

## Связанные места кода

- Резолв Legion icons: `Code/Guardpost_Patrols.lua` (`JAZZ_GetLegionAISquadIcon`, role → path map)
- UI bind: `SquadWindow:SpawnSquadIcon` / `GetSatelliteIconImagesSquad`
- Technical overview: [strategy-squads-sectors.md](strategy-squads-sectors.md)
