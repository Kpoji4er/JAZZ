# Equipped armor → appearance map (JAZZ-APPEAR-001)

Канон mapping для CommonLib `AttachEntries` / `BodyPartData`.  
Доноры entity: коллекция **Wardrobe** (Sir Ni) и др. soft-deps — точные mod `id` после inventory скачанных паков.

**Runtime gates:** Mod Option `ShowEquippedArmorVisuals` (default off) ∧ CommonLib loaded ∧ `IsValidEntity`.

Status: `todo` | `mapped` | `skip` (причина в notes).

## Head (`Slot = Head`) — JazzArmor

23 предметов. **Правило Head:** у всех головных уборов `Hide` включает `Hair` (без исключений, пока owner не скажет иначе).

| item_id | display (RU) | class comment | asset_mod | entity_male | entity_female | hide_parts | status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `JazzArmor_UniformCap` | Военная кепка | Class 1 N | vanilla | `FactionMale_Hat_05` | `FactionMale_Hat_05` | `Hair` | mapped | entity `FactionMale_Hat_05`; Spot=`Head`; оба пола; **C1 camo** `RGBA(58, 72, 38)`; C2/C3 black unless needed |
| `JazzArmor_ConstructionHelmet` | Строительная каска | Class1 L | vanilla? | `Construction_Helmet_01` | `Construction_Helmet_01` | `Hair` | mapped | entity `Construction_Helmet_01`; Spot=`Head`; оба пола; **C1** `RGBA(200, 160, 20)`; C2/C3 black or match |
| `JazzArmor_AdrianHelmet` | Каска Адриана | Class1 L | vanilla | `JungleCamp_GraveyardHelmet_02` | `JungleCamp_GraveyardHelmet_02` | `Hair` | mapped | entity `JungleCamp_GraveyardHelmet_02`; Spot=`Head`; Offset Z=0.5; оба пола; **C1** `RGBA(88, 98, 92)`. superseded: `CODWW2_bel_m_hat_01`/`CODWW2_bel_f_hat_01` @ Origin |
| `JazzArmor_SovietHelm` | Советская каска СШ-40 | Class1 L | vanilla | `FactionMale_Hat_09` | `FactionMale_Hat_09` | `Hair` | mapped | entity `FactionMale_Hat_09` (тот же что M1); **C1=C3** `RGBA(70, 78, 58)` RU drab без сетки; C2 same |
| `JazzArmor_MetalHelm` | Самодельный шлем | Class1 M | | | | `Hair` | todo | improvised |
| `JazzArmor_WieldingHelm` | Сварочная маска | Class1 H | | | | `Hair` | todo | mask-like; Spot Head/Hat? |
| `JazzArmor_M1Helm` | Каска М1 | Class2 M | vanilla | `FactionMale_Hat_09` | `FactionMale_Hat_09` | `Hair` | mapped | entity `FactionMale_Hat_09`; Spot=`Head`; оба пола; **C1** `RGBA(61, 74, 46)`; **C2** same; **C3 net** `RGBA(48, 36, 26)`; R/M=0 |
| `JazzArmor_Stahlhelm` | Немецкий шлем M42 | Class2 M | vanilla | `EquipmentMale_WW2Helmet` | `EquipmentFemale_WW2Helmet` | `Hair` | mapped | entities `EquipmentMale_WW2Helmet` / `EquipmentFemale_WW2Helmet`; Spot=`Head`; **C1** `RGBA(72, 78, 62)`; C2/C3 `RGBA(48, 52, 42)` or black |
| `JazzArmor_PASGTHelm` | Шлем PASGT | Class2 M | vanilla | `FactionMale_Hat_08` | `FactionMale_Hat_08` | `Hair` | mapped | entity `FactionMale_Hat_08`; Spot=`Head`; оба пола; **C1=C3** `RGBA(61, 74, 46)` (иначе мед. крест); C2 black |
| `JazzArmor_ProTecHelm` | Шлем ProTec | Class2 L | | | | `Hair` | todo | sports/skater look |
| `JazzArmor_6b7Helm` | Шлем 6Б7 | Class2 M | vanilla | `FactionMale_Hat_10` | `FactionMale_Hat_10` | `Hair` | mapped | entity `FactionMale_Hat_10`; Spot=`Head`; оба пола; **C1** `RGBA(55, 68, 42)`; C2/C3 `RGBA(40, 48, 32)` or black |
| `JazzArmor_STSHHelm` | Шлем Сфера | Class2 H | | | | `Hair` | todo | |
| `JazzArmor_AltynHelm` | Шлем Алтын | Class2 SH | | | | `Hair` | todo | face-cover heavy |
| `JazzArmor_TwaronHelm` | Шлем Тварон | Class2 M | vanilla | `FactionMale_Hat_10` | `FactionMale_Hat_10` | `Hair` | mapped | entity `FactionMale_Hat_10` (как `JazzArmor_6b7Helm`); **C1 green** `RGBA(48, 78, 42)`; C2/C3 `RGBA(32, 52, 30)` |
| `JazzArmor_TwaronHelmHeavy` | Шлем Тварон, Тяжелый | Class2 H | vanilla | `FactionMale_Hat_10` | `FactionMale_Hat_10` | `Hair` | mapped | entity `FactionMale_Hat_10`; как `JazzArmor_TwaronHelm`; optional C1 `RGBA(40, 66, 36)` |
| `JazzArmor_ZylonHelm` | Шлем Зилон | Class2 M | vanilla | `FactionMale_Hat_11` | `FactionMale_Hat_11` | `Hair` | mapped | entity `FactionMale_Hat_11` (camo-вариант `FactionMale_Hat_10`); **C1** `RGBA(58, 72, 38)` |
| `JazzArmor_ZylonHelmHeavy` | Шлем Зилон, Тяжелый | Class2 H | vanilla | `FactionMale_Hat_11` | `FactionMale_Hat_11` | `Hair` | mapped | entity `FactionMale_Hat_11`; как `JazzArmor_ZylonHelm` |
| `JazzArmor_Mich2001` | Шлем MICH 2001 | Class3 L | | | | `Hair` | todo | |
| `JazzArmor_Mich2000` | Шлем MICH 2000 | Class3 M | | | | `Hair` | todo | |
| `JazzArmor_GuardianHelm` | Шлем Гвардиан | Class3 M | vanilla | `FactionMale_Hat_10` | `FactionMale_Hat_10` | `Hair` | mapped | entity `FactionMale_Hat_10` (как `JazzArmor_6b7Helm`); **C1 grey** `RGBA(78, 80, 82)`; C2/C3 `RGBA(52, 54, 56)` |
| `JazzArmor_GuardianHelmHeavy` | Шлем Гвардиан, тяжелый | Class3 H | vanilla | `FactionMale_Hat_10` | `FactionMale_Hat_10` | `Hair` | mapped | entity `FactionMale_Hat_10`; как `JazzArmor_GuardianHelm`; optional C1 `RGBA(58, 60, 62)` |
| `JazzArmor_UHMWPEHelm` | Шлем СВМПЭ | Class3 H | | | | `Hair` | todo | |
| `JazzArmor_SpectraHelm` | Шлем СПЕКТРА | Class4 H | | | | `Hair` | todo | |

### Out of this wave (HeadGear / face)

Не `Slot=Head`, отдельно позже: `JazzArmor_BallisticMask`, `JazzArmor_CamoBalaclava`, `JazzArmor_ESS`, `JazzArmor_Sunglasses`, `JazzArmor_NVG1`…`NVG3`.

## Torso (`Slot = Torso`) — JazzArmor

**Spot для всех торсовых жилетов: `Origin`** (не Torso/Armor attach).

Калибровка Interceptor: **Igor** = default Scale 105% / Z −10; **Steroid** (модель крупнее) = Scale 110% / Z −15 — отдельный `AttachEntries` с Appearance filter на пресет Steroid.

| item_id | display (RU) | entity_male | entity_female | hide_parts | status | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `JazzArmor_FlakM1955` | Бронежилет Flak M1955 | `EquipmentMale_FlackVest` | `EquipmentFemale_FlackVest` | | mapped | Spot=`Origin`. **C1** OD `RGBA(61, 74, 46)` (отличить от M69). Female: чуть поднять Offset Z ≈ `+3`…`+5`; **Steroid** — проверить отдельно |
| `JazzArmor_FlakM69` | Бронежилет Flak M69 | `EquipmentMale_FlackVest` | `EquipmentFemale_FlackVest` | | mapped | Spot=`Origin`; `EquipmentMale_FlackVest` / `EquipmentFemale_FlackVest`; **C1** `RGBA(78, 88, 52)` olive-nylon. Female Offset Z как у M1955 |
| `JazzArmor_IBALight` | Бронежилет "Interceptor" | `EquipmentMale_InterceptorVest_01` | `EquipmentFemale_InterceptorVest_01` | | mapped | Spot=`Origin`. **без камуфляжа** `EquipmentMale_InterceptorVest_01` / `EquipmentFemale_InterceptorVest_01`. Default: Scale **105%**, Offset Z ≈ `-10` (**эталон: Igor**). **Steroid:** Scale **110%**, Z ≈ `-15`. **C1** основа `RGBA(52, 58, 48)`; **C2** заклёпки `RGBA(120, 120, 110)`; C3 black |
| `JazzArmor_IBA` | Interceptor + пах | `EquipmentMale_InterceptorVest_02` | `EquipmentFemale_InterceptorVest_02` | | mapped | Spot=`Origin`. **камуфляж** `EquipmentMale_InterceptorVest_02` / `EquipmentFemale_InterceptorVest_02`. Default 105% / Z≈`-10` (Igor); **Steroid:** **110%** / Z ≈ `-15`. **C1** `RGBA(58, 72, 38)` + **C2** `RGBA(40, 52, 28)` camo; **C3** заклёпки `RGBA(120, 120, 110)` |
| `JazzArmor_IBAFull` | Interceptor, Тяжелый | `EquipmentMale_InterceptorVest_02` | `EquipmentFemale_InterceptorVest_02` | | mapped | Spot=`Origin`; `EquipmentMale_InterceptorVest_02` / `EquipmentFemale_InterceptorVest_02`; default 105% / Z≈`-10`; **Steroid:** **110%** / Z ≈ `-15`; C1+C2 camo темнее (`RGBA(42, 54, 30)` / `RGBA(28, 38, 22)`); **C3** заклёпки |

## Soft-deps (черновик)

Большая часть уже замапленного — **vanilla** (`FactionMale_Hat_*`, `Equipment*Flack/Interceptor*`, `Equipment*WW2Helmet`, `JungleCamp_GraveyardHelmet_02`).  
**Sir Ni / Wardrobe** (base, Vanilla Expanded, WW2, Weird): по просмотру **ничего полезного сверх vanilla** для текущих JazzArmor (WW2 bel Adrian superseded; VietHelmet без CharacterHat-class). **Не объявлять soft-dep**, пока не появится конкретный entity из коллекции.

| mod title | workshop / local id | required | role |
| --- | --- | --- | --- |
| JA3_CommonLib | `JA3_CommonLib` | false (уже) | AttachEntries API — нужен |
| Wardrobe (base) | `Wardrobe` / WS `3257716618` | **не брать** | нет нужных hat/vest под JAZZ map |
| Wardrobe Vanilla Expanded | WS `3328717726` | **не брать** | пока без хитов |
| Wardrobe WW2 Edition (Vol I–III) | WS `3334071674`… | **не брать** | Adrian ушёл на vanilla JungleCamp; ru-каски нет |
| Wardrobe Weird Edition | WS `3330466662` | **не брать** | ломает ♀ AME preview |
| PMC COMPANY (optional) | TBD | false | only if later mapped |

### Known editor conflict

- **Wardrobe Weird Edition** — держать выкл. при работе с Appearance/AME.

## Tooling

```text
python docs/tools/_list_jazz_helms.py
```
