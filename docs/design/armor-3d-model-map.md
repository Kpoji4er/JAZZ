# JazzArmor → 3D models (Fab / Sketchfab)

Карта **всех** `JazzArmor_*` (без плит `JazzArmorPlates_*` — UI-only, меш не нужен).  
Источники: **Fab + Sketchfab** (платные ок). CGTrader — нет.  
Без retopo: только game-ready low-poly. Soft poly ok.

## Легенда моделей (база)

| Код | Ассет | Ссылка | Поли (заявл.) | Как резать |
| --- | --- | --- | --- | --- |
| **HAV** | Heavy Armor Vest (Slayver) | [Fab](https://www.fab.com/listings/cc64d82e-35d9-4f99-a3a8-17aeb0b00af4) | 4.5k v / 8.8k t | торс / плечи / пах / ноги / ворот + skins |
| **FLAK** | Flak vest (Slayver) | [Fab](https://www.fab.com/listings/36f91eb9-4aa6-4f45-8558-f03d647ca61a) | 1.5k v / 2.9k t | 8 skins |
| **MASKA** | Maska-1SCH (Slayver) | [Fab](https://www.fab.com/listings/7532f145-2fb2-4759-9d72-8bb4f9fccf33) | 1.3k v / 2.6k t | с/без забрала |
| **ZSH** | Helmet ZSH-1-2 (Slayver) | [Sketchfab](https://sketchfab.com/3d-models/helmet-zsh-1-2-34d54dba5f6b408e97371c042a7b59d1) | 2.8k v / 4.9k t | 6 skins |
| **MMC2** | Modular Military Character 2 | [Fab](https://www.fab.com/listings/fcc4a754-95b7-47e5-b4e8-2207cde09c44) | modular pack | шлемы/жилеты/штаны/pads из модулей |
| **M1** | M1 Helmet | [Sketchfab free](https://sketchfab.com/3d-models/m1-helmet-6d7929b10c994db0b6b39e35b379bfbd) | 3.4k t | as-is |
| **ADR** | Adrian WW1 | [Sketchfab free](https://sketchfab.com/3d-models/french-adrian-helmet-ww1-38d5f0a6febb434088fcbffdb40f77cb) | 10k t | soft OK |
| **HARD** | Hardhat | [Poly Pizza](https://poly.pizza/m/cyjbHPC6QAM) | ~18k | soft; origin |
| **PVS14** | AN/PVS-14 | [Sketchfab free](https://sketchfab.com/3d-models/anpvs-14-nvd-ed14bb49bdf94cd7b572daf206f1ccfb) | 6.1k t | Hat2 |
| **VAN** | Vanilla Appearance part | in-game | — | клон / ретекстур |
| **GAP** | нет готового low-poly | — | — | искать на Fab/Sketchfab или proxy |

Иконки: `jazz/ArmorIcons/*.png` (реф по силуэту).

---

## Шлемы / голова

| ID | Название (RU) | Иконка | Силуэт по иконке | Модель | Примечание |
| --- | --- | --- | --- | --- | --- |
| `JazzArmor_AltynHelm` | Шлем Алтын | Altyn | титан + забрало | **MASKA** (с визором) | иконка = Altyn/Maska-класс |
| `JazzArmor_STSHHelm` | Шлем Сфера | STSH | сфера/тяжёлый | **MASKA** без визора / **ZSH** | proxy |
| `JazzArmor_GuardianHelmHeavy` | Шлем Гвардиан тяж. | GuardianHelmH | тяжёлый с защитой | **MASKA** / **ZSH** | skin |
| `JazzArmor_GuardianHelm` | Шлем Гвардиан | GuardianHelm | средний тактический | **ZSH** / MMC2 helm | |
| `JazzArmor_6b7Helm` | Шлем 6Б7 | 6b7 | сов. баллистический | **ZSH** | proxy |
| `JazzArmor_TwaronHelm` | Шлем Тварон | TwaronHelm | PASGT-like | MMC2 helm / **ZSH** | gap PASGT exact |
| `JazzArmor_TwaronHelmHeavy` | Шлем Тварон тяж. | TwaronHelmH | +шея | **ZSH** + neck / MASKA | |
| `JazzArmor_ZylonHelm` | Шлем Зилон | ZylonHelm | как Twaron | тот же mesh + skin | |
| `JazzArmor_ZylonHelmHeavy` | Шлем Зилон тяж. | ZylonHelmH | тяжёлый | как TwaronHelmHeavy | |
| `JazzArmor_UHMWPEHelm` | Шлем УГВМПЭ | UHMWPEHelm | современный | **ZSH** / MMC2 | skin |
| `JazzArmor_SpectraHelm` | Шлем СПЕКТРА | SpectraHelm | футурист/тяж | **HAV** helmet piece / MASKA | |
| `JazzArmor_PASGTHelm` | Шлем PASGT | PASGTHelm | PASGT + woodland cover | **GAP** → MMC2 helm / искать Fab «PASGT lowpoly» | scan 79k+ reject |
| `JazzArmor_Mich2000` | Шлем MICH 2000 | TC2000 | mid/high-cut + shroud | MMC2 / Fab «MICH/ACH/FAST» lowpoly | иконка high-cut |
| `JazzArmor_Mich2001` | Шлем MICH 2001 | TC2001 / MICH2001 | high-cut rails+NVG shroud | то же | |
| `JazzArmor_M1Helm` | Каска М1 | M1 | стальная M1 | **M1** | exact free |
| `JazzArmor_AdrianHelmet` | Каска Адриана | AdrianHelm | WW1 Adrian | **ADR** | free |
| `JazzArmor_Stahlhelm` | Немецкий шлем M42 | Stahlhelm | M42 чёрный | Fab Stahlhelm / Slayver German soldier helm | [Fab M16](https://www.fab.com/listings/52834819-8a4e-4bfd-a8de-6b66cffe2c23) проверить poly |
| `JazzArmor_SovietHelm` | СШ-40 | Sh40 | сов. каска | Sketchfab SSH-40 **только lowpoly**; иначе GAP | SimplyK 320k REJECT |
| `JazzArmor_ConstructionHelmet` | Строительная каска | ConstructionHelmet | жёлтый hardhat | **HARD** | |
| `JazzArmor_ProTecHelm` | Шлем ProTec | ProTec | skate/bump | GAP / MMC2 cap-like | |
| `JazzArmor_WieldingHelm` | Сварочный шлем | WieldingHelm | welding | GAP Sketchfab welding helmet lowpoly | |
| `JazzArmor_MetalHelm` | Самодельный шлем | MetalHelm | scrap pot | M1 ретекстур / improvised | |
| `JazzArmor_BallisticMask` | Кевларовая маска | BallisticMask | face shield | **MASKA** визор-only / Face | |
| `JazzArmor_CamoBalaclava` | Балаклава | CamoMask | ткань | **VAN** / MMC2 head gear | |
| `JazzArmor_ESS` | Баллистические очки | ESS | goggles | MMC2 / Sketchfab ESS | Hat2 |
| `JazzArmor_Sunglasses` | Солнцезащитные очки | Sunglasses | glasses | **VAN** / Sketchfab | Hat2 |
| `JazzArmor_UniformCap` | Униформная кепка | UniformCap | patrol cap | MMC2 caps / **VAN** | |
| `JazzArmor_NVG1` | AN/PVS-5 | NVG1 | binocular NVG | GAP PVS-5 / proxy PVS-7 | |
| `JazzArmor_NVG2` | AN/PVS-7 | NVG2 | binocular | GAP / proxy | |
| `JazzArmor_NVG3` | AN/PVS-14 | NVG3 | monocular | **PVS14** | exact |

---

## Жилеты / торс (семьи)

### Twaron / Zylon / Guardian (один HAV + skins)

| ID | Название | Иконка | Нарезка HAV | Skin hint |
| --- | --- | --- | --- | --- |
| `JazzArmor_TwaronLight` | Тварон лёгкий | TwaronL | торс | зелёный |
| `JazzArmor_TwaronMedium` | Тварон средний | TwaronM | торс+ворот+пах | иконка = heavy collar+MOLLE+groin — совпадает с HAV |
| `JazzArmor_TwaronFull` | Тварон тяжёлый | TwaronH | +плечи/руки | |
| `JazzArmor_TwaronLegs` | Тварон ноги лёгк. | TwaronLegs | shin/pads | |
| `JazzArmor_TwaronHeavyLegs` | Тварон ноги тяж. | TwaronLegsH | больше pads | |
| `JazzArmor_ZylonLight` | Зилон лёгкий | ZylonL | как TwaronLight | другой skin |
| `JazzArmor_ZylonMedium` | Зилон средний | ZylonM | как TwaronMedium | |
| `JazzArmor_ZylonFull` | Зилон тяжёлый | ZylonH | как TwaronFull | |
| `JazzArmor_ZylonLegs` | Зилон ноги | ZylonLegs | | |
| `JazzArmor_ZylonHeavyLegs` | Зилон ноги тяж. | ZylonLegsH | | |
| `JazzArmor_GuardianLight` | Гвардиан лёгкий | GuardianL | торс | чёрный/тёмный |
| `JazzArmor_GuardianMedium` | Гвардиан средний | GuardianM | торс+ворот+пах | иконка = тот же силуэт HAV |
| `JazzArmor_GuardianFull` | Гвардиан тяжёлый | GuardianH | full | |
| `JazzArmor_GuardianLegs` | Гвардиан ноги | GuardianLegs | | |
| `JazzArmor_GuardianHeavyLegs` | Гвардиан ноги тяж. | GuardianLegsH | | |

### IBA / UHMWPE / Spectra / SWAT (HAV или Flak + нарезка)

| ID | Название | Иконка | Модель |
| --- | --- | --- | --- |
| `JazzArmor_IBALight` | IBA лёгкий | IBALight | **HAV** торс / **FLAK** |
| `JazzArmor_IBA` | IBA | IBA | **HAV** торс+ворот+пах (иконка совпадает) |
| `JazzArmor_IBAFull` | IBA full | IBAFull | **HAV** full |
| `JazzArmor_UHMWPE` | УГВМПЭ | UHMWPE | **HAV** medium |
| `JazzArmor_UHMWPEFull` | УГВМПЭ full | UHMWPEFull | **HAV** full |
| `JazzArmor_UHMWPELegs` | УГВМПЭ ноги | UHMWPELegs | HAV legs |
| `JazzArmor_Spectra` | СПЕКТРА | SpectraL / Spectra | **HAV** light + тёмный skin |
| `JazzArmor_SpectraFull` | СПЕКТРА тяж. | SpectraH | **HAV** full |
| `JazzArmor_SpectraLegs` | Штаны Спектра | SpectraLegs | HAV legs / MMC2 pants |
| `JazzArmor_SpectraCompositum` | СПЕКТРА композитум | IBAFull (reuse) | тот же mesh, другой mat |
| `JazzArmor_SpectraFullCompositum` | СПЕКТРА комп. тяж. | IBAFull | то же |
| `JazzArmor_SWAT` | SWAT | SWAT | **HAV** / MMC2 vest |

### Flak / PASGT vest / Police / RBA / EOD

| ID | Название | Иконка | Модель |
| --- | --- | --- | --- |
| `JazzArmor_FlakM1955` | Flak M1955 | FlakM1955 | **FLAK** |
| `JazzArmor_FlakM69` | Flak M69 | FlakM69 | **FLAK** (+collar) |
| `JazzArmor_EOD` | (иконка EOD; в DisplayName сейчас Flak M69 — баг данных?) | EOD | **HAV** heavy / отдельный EOD если найдётся |
| `JazzArmor_PASGT` | Бронежилет PASGT | PASGT | **FLAK** |
| `JazzArmor_PoliceVest` | Полицейский | Police | **FLAK** light skin |
| `JazzArmor_RBA` | Американский | RBA | **FLAK** / MMC2 |

### Советские / кирасы / самодел

| ID | Название | Иконка | Модель |
| --- | --- | --- | --- |
| `JazzArmor_6B3` | 6Б3 | 6b3 | **FLAK**/HAV proxy или GAP 6B exact |
| `JazzArmor_6B13` | 6Б13 | 6b13 | **HAV** (camo skin) — иконка heavy collar+plate |
| `JazzArmor_SovietAssaultArmor` | Сов. штурмовой нагрудник | USSRArmor | GAP / lamellar plate Sketchfab; не HAV |
| `JazzArmor_AssaultCuirass` | Немецкая штурмовая кираса | GermanArmor | GAP WW1/WW2 assault cuirass |
| `JazzArmor_ImprovisedCuirass` | Самодельная кираса | ImprovisedCuirass | kitbash metal plates |
| `JazzArmor_TireArmor` | Броня из шин | TireArmor | kitbash / GAP |
| `JazzArmor_TireBrigantine` | Бригантина из шин | TireBrigantine | kitbash laminar; иконка = horizontal plates |
| `JazzArmor_Chainmail` | Кольчуга | Chainmail | Sketchfab chainmail lowpoly / VAN |

### Кожа / униформа

| ID | Название | Иконка | Модель |
| --- | --- | --- | --- |
| `JazzArmor_LeatherArmor` | Кожаная броня | LeatherArmor | **VAN** / MMC2 |
| `JazzArmor_LeatherVest` | Кожаный жилет | SleevelessJacket | **VAN** |
| `JazzArmor_LeatherJacketBlk` | Кожаная куртка | LeatherJacket | **VAN** Body |
| `JazzArmor_LeatherJacketBrn` | Кожаная куртка | LeatherJacketbrn | **VAN** recolor |
| `JazzArmor_LeatherPants` | Кожаные штаны | LeatherPants | **VAN** Pants |
| `JazzArmor_Uniform` | Униформа | Uniform | **VAN** / MMC2 shirt |
| `JazzArmor_UniformPants` | Униформные штаны | UniformPants | **VAN** / MMC2 pants |

### Pads / ноги мелочь

| ID | Название | Иконка | Модель |
| --- | --- | --- | --- |
| `JazzArmor_CamoKneePads` | Военные щитки | CamoKneePads | MMC2 kneepads / HAV legs cut |
| `JazzArmor_SwatPads` | Кевларовые наколенники | SwatPads | MMC2 kneepads |
| `JazzArmor_MotoKneePads` | Мотозащита | MotoKneePads | GAP / Sketchfab moto pads |
| `JazzArmor_RaiderKneePads` | Рейдерские | RaiderPads | kitbash |
| `JazzArmor_RaiderMetalLeggins` | Металл. поножи | MetalPads | kitbash / Tire/metal |

---

## Плиты (`JazzArmorPlates_*`)

Меш на юните **не нужен** (слот пластин в жилете). Иконки в `ArmorIcons/ArmorPlates/` — только UI.

---

## Приоритет закупки

1. **HAV + FLAK + MASKA + ZSH** (Slayver) — закрывает ~45 айтемов семьями.  
2. Free: **M1, ADR, PVS14, HARD**.  
3. **MMC2** — PASGT/MICH/caps/pants/pads + UE5.  
4. Точечно: Stahlhelm, SSH-40 lowpoly, welding, ProTec, Soviet cuirass.

## JA3 slot classes (напоминание)

| Часть | class_parent |
| --- | --- |
| Каска / очки / NVG | `CharacterHat` |
| Жилет поверх | `CharacterArmorMale/Female` |
| Топ/куртка | `CharacterBodyMale/Female` |
| Штаны/ноги | `CharacterPantsMale/Female` |
| Pads | `CharacterHip*` / Pants |

Броня на Epic-риге → для JA3 всё равно пересадка на sample-скелет (кроме чистых Hat).
