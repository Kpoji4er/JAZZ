# Squad role icons (enemy satellite)

Каталог PNG для сателлитных иконок отрядов Global AI / фракций. Файлы — `64×64`, **прозрачный** canvas вне щита (как у `legion.png` / `army.png`), щит фракции + ivory-силуэт роли.

Новые иконки создавать по skill [`.agents/skills/create-jazz-squad-icons/SKILL.md`](../../../.agents/skills/create-jazz-squad-icons/SKILL.md).

Пути runtime: `Mod/e6L4ECj/SquadsIcons/Enemy/<faction>/<faction>_<ROLE>_squad.png`  
Ассеты: [`SquadsIcons/Enemy/`](../../../SquadsIcons/Enemy/)

Раскладка: `_shields/` (пустые щиты), `<faction>/` (ролевые PNG), `_misc/` (прочее).  
Стратегический контекст: [strategy-squads-sectors.md](strategy-squads-sectors.md) · wiki: [legion-global-ai.md](../../wiki/legion-global-ai.md)

---

## Базовые щиты фракций

Пустой щит без ролевого символа (подложка для композита).

| Фракция | Файл | Щит |
| --- | --- | --- |
| Legion | `_shields/legion.png` | ![legion](../../../SquadsIcons/Enemy/_shields/legion.png) |
| Army | `_shields/army.png` | ![army](../../../SquadsIcons/Enemy/_shields/army.png) |
| Adonis | `_shields/adonis.png` | ![adonis](../../../SquadsIcons/Enemy/_shields/adonis.png) |
| Rebels | `_shields/rebels.png` | ![rebels](../../../SquadsIcons/Enemy/_shields/rebels.png) |
| Smugglers | `_shields/smugglers.png` | ![smugglers](../../../SquadsIcons/Enemy/_shields/smugglers.png) |

Доп. варианты щитов (не ролевые): `_shields/army2.png`, `_shields/army3.png`, `_shields/rebels2.png`, `_shields/rebels3.png`; прочее: `_misc/enemy_squad.png`, `_misc/nazi.png`.

---

## Роли — смысл и символ

| Role ID | Смысл | Символ | Статус runtime (Legion) |
| --- | --- | --- | --- |
| `major` / BASE | Штаб / Major response | череп | wired → `legion/legion_BASE_squad.png` |
| `garrison` | Держит сектор | башня / rook | wired |
| `patrol` | Патруль ключевых точек | скрещённые стрелы | wired |
| `recon` | Наблюдение / разведка | бинокль | wired |
| `qrf` | Быстрая реакция | тесак / cutlass | wired |
| `supply` | Конвой снабжения | грузовик | wired |
| `shipment` | Алмазный груз в HQ | грузовик + ромб | wired |
| `reinforce` | Пограничное усиление гарнизона | плюс | wired |
| `support` | Малая огневая поддержка (снайпер/MG/миномёт) | прицел / reticle | wired → `legion/legion_SUPPORT_squad.png` |
| `retribution` | Карательный удар Major с HQ | кулак | wired |
| `recruiter` | Вербовщик / агитатор | мегафон | asset only |
| `manpower` | Конвой живой силы | колонна солдат с флагом | asset only |
| `tax` | Сбор налогов / дани | мешок с монетами | asset only |

`wired` = путь в `Guardpost_Patrols.lua` → `JAZZ_GetLegionAISquadIcon`.  
`asset only` = PNG есть у всех фракций, роль в director ещё не привязана.

Имена файлов: `<faction>/<faction>_<ROLE>_squad.png`  
`faction` ∈ `legion` · `army` · `adonis` · `rebels` · `smugglers`

---

## Галерея по ролям

### BASE / major — череп

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_BASE_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_BASE_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_BASE_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_BASE_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_BASE_squad.png) |

### GARRISON — башня

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_GARRISON_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_GARRISON_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_GARRISON_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_GARRISON_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_GARRISON_squad.png) |

### PATROL — скрещённые стрелы

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_PATROL_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_PATROL_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_PATROL_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_PATROL_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_PATROL_squad.png) |

### RECON — бинокль

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_RECON_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_RECON_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_RECON_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_RECON_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_RECON_squad.png) |

### QRF — тесак

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_QRF_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_QRF_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_QRF_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_QRF_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_QRF_squad.png) |

### SUPPLY — грузовик

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_SUPPLY_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_SUPPLY_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_SUPPLY_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_SUPPLY_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_SUPPLY_squad.png) |

### SHIPMENT — грузовик + ромб

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_SHIPMENT_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_SHIPMENT_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_SHIPMENT_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_SHIPMENT_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_SHIPMENT_squad.png) |

### REINFORCE — плюс

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_REINFORCE_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_REINFORCE_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_REINFORCE_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_REINFORCE_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_REINFORCE_squad.png) |

### SUPPORT — прицел *(STRATEGY-024)*

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_SUPPORT_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_SUPPORT_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_SUPPORT_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_SUPPORT_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_SUPPORT_squad.png) |

### RETRIBUTION — кулак

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_RETRIBUTION_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_RETRIBUTION_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_RETRIBUTION_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_RETRIBUTION_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_RETRIBUTION_squad.png) |

### RECRUITER — мегафон *(asset only)*

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_RECRUITER_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_RECRUITER_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_RECRUITER_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_RECRUITER_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_RECRUITER_squad.png) |

### MANPOWER — колонна солдат *(asset only)*

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_MANPOWER_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_MANPOWER_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_MANPOWER_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_MANPOWER_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_MANPOWER_squad.png) |

### TAX — мешок с монетами *(asset only)*

| Legion | Army | Adonis | Rebels | Smugglers |
| --- | --- | --- | --- | --- |
| ![L](../../../SquadsIcons/Enemy/legion/legion_TAX_squad.png) | ![A](../../../SquadsIcons/Enemy/army/army_TAX_squad.png) | ![D](../../../SquadsIcons/Enemy/adonis/adonis_TAX_squad.png) | ![R](../../../SquadsIcons/Enemy/rebels/rebels_TAX_squad.png) | ![S](../../../SquadsIcons/Enemy/smugglers/smugglers_TAX_squad.png) |

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
