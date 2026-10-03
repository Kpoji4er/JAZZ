# Аудит текстур оружия — 03.10.2026

## Установлено

По уточнению владельца восстановлены 50 карт VZ58/R4/АК103 (100 DDS с fallbacks). Сняты художественное ослабление NM, roughness floors и замена дерева. RM: R=G=roughness, B=metallic. Источники VZ58/R4 — первоначальные извлечённые PNG; АК103 — первоначальные native UV-атласы и TGA из `_ak103_native_20260926`. Последние являются производными от исходника, не новым bake. Единственный неполный авторский PBR-набор — проволочный приклад VZ58: сохранены начальные константы импорта и авторская AO. Геометрия, UV и MTL сохранены по SHA256.

BC хранится sRGB, RM/AO линейно, NM BC5. XY нормалей не ослаблены и не инвертированы. Карты проверены после декодирования: размеры, полный mip-chain, fallback, ошибка сжатия и ориентация относительно исходника. Официальные hgimgcvt/hgnvcompress, TGA без сжатия. Нет утверждения, что исходный знак Y/bake соответствует движку: это ещё проверяется по игровым скринам владельца.

Исходные архивы и staged/backup не удалены. Manifest установки: `tmp/weapon-source-restore-20261003/manifest.json`. Предыдущий проход только RM: `tmp/weapon-rm-reimport-20261002-v3`; superseded по явному требованию владельца.

## Привязки источников

Пути ниже относительно локального каталога оружейных сборок. У каждого файла в локальном manifest сохранён SHA256.

| DDS | Слот | Исходник |
| --- | --- | --- |
| `JAZZ_VZ58_1_Norm.dds` | NormalMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Steel_Body_Normal.png` |
| `JAZZ_VZ58_2_Base.dds` | BaseColorMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Steel_Body_BaseCol.png` |
| `JAZZ_VZ58_3_RM.dds` | RMMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Steel_Body_Roughne.png` + `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Steel_Body_Metalli.png` |
| `JAZZ_VZ58_4_Norm.dds` | NormalMap | `_vz58_jazz_20260926/source/modern/Attatchemnts_Normal_DirectX.png` |
| `JAZZ_VZ58_5_Base.dds` | BaseColorMap | `_vz58_jazz_20260926/source/modern/Attatchemnts_Base_Color.png` |
| `JAZZ_VZ58_6_RM.dds` | RMMap | `_vz58_jazz_20260926/source/modern/Attatchemnts_Roughness.png` + `_vz58_jazz_20260926/source/modern/Attatchemnts_Metallic.png` |
| `JAZZ_VZ58_7_Norm.dds` | NormalMap | `_vz58_jazz_20260926/source/modern/Stock,Grip_CZX_Normal_DirectX.png` |
| `JAZZ_VZ58_8_Base.dds` | BaseColorMap | `_vz58_jazz_20260926/source/modern/Stock,Grip_CZX_Base_Color.png` |
| `JAZZ_VZ58_9_RM.dds` | RMMap | `_vz58_jazz_20260926/source/modern/Stock,Grip_CZX_Roughness.png` + `_vz58_jazz_20260926/source/modern/Stock,Grip_CZX_Metallic.png` |
| `JAZZ_VZ58_10_Norm.dds` | NormalMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Wood_Front_Normal.png` |
| `JAZZ_VZ58_11_Base.dds` | BaseColorMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Wood_Front_BaseCol.png` |
| `JAZZ_VZ58_12_RM.dds` | RMMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Wood_Front_Roughne.png` + `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Wood_Front_Metalli.png` |
| `JAZZ_VZ58_13_Norm.dds` | NormalMap | `_vz58_jazz_20260926/source/modern/Gun_Expert_Foregrip_Normal_DirectX.png` |
| `JAZZ_VZ58_14_Base.dds` | BaseColorMap | `_vz58_jazz_20260926/source/modern/Gun_Expert_Foregrip_Base_Color.png` |
| `JAZZ_VZ58_15_RM.dds` | RMMap | `_vz58_jazz_20260926/source/modern/Gun_Expert_Foregrip_Roughness.png` + `_vz58_jazz_20260926/source/modern/Gun_Expert_Foregrip_Metallic.png` |
| `JAZZ_VZ58_16_Norm.dds` | NormalMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Mag_and_Bullet_Nor.png` |
| `JAZZ_VZ58_17_Base.dds` | BaseColorMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Mag_and_Bullet_Bas.png` |
| `JAZZ_VZ58_18_RM.dds` | RMMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Mag_and_Bullet_Rou.png` + `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Mag_and_Bullet_Met.png` |
| `JAZZ_VZ58_19_Norm.dds` | NormalMap | `_vz58_jazz_20260926/source/modern/Mag_Grip_Normal_DirectX.png` |
| `JAZZ_VZ58_20_Base.dds` | BaseColorMap | `_vz58_jazz_20260926/source/modern/Mag_Grip_Base_Color.png` |
| `JAZZ_VZ58_21_RM.dds` | RMMap | `_vz58_jazz_20260926/source/modern/Mag_Grip_Roughness.png` + `_vz58_jazz_20260926/source/modern/Mag_Grip_Metallic.png` |
| `JAZZ_VZ58_25_Norm.dds` | NormalMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Wood_Back_Stock_No.png` |
| `JAZZ_VZ58_26_Base.dds` | BaseColorMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Wood_Back_Stock_Ba.png` |
| `JAZZ_VZ58_27_RM.dds` | RMMap | `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Wood_Back_Stock_Ro.png` + `_vz58_jazz_20260926/source/classic/SA_vz.58_(TextureReady)_Wood_Back_Stock_Me.png` |
| `JAZZ_VZ58_28_Norm.dds` | NormalMap | `_vz58_jazz_20260926/source/modern/SA_vz.58_Suppressor_Suppressor_Normal.png` |
| `JAZZ_VZ58_29_Base.dds` | BaseColorMap | `_vz58_jazz_20260926/source/modern/SA_vz.58_Suppressor_Suppressor_BaseColor.png` |
| `JAZZ_VZ58_30_RM.dds` | RMMap | `_vz58_jazz_20260926/source/modern/SA_vz.58_Suppressor_Suppressor_Roughness.png` + `_vz58_jazz_20260926/source/modern/SA_vz.58_Suppressor_Suppressor_Metallic.png` |
| `JAZZ_VektorR4_1_Norm.dds` | NormalMap | `_r4_jazz_20260926/source/R4_low_R4_Normal.png` |
| `JAZZ_VektorR4_3_Base.dds` | BaseColorMap | `_r4_jazz_20260926/source/R4_low_R4_BaseColor.png` |
| `JAZZ_VektorR4_4_RM.dds` | RMMap | `_r4_jazz_20260926/source/R4_low_R4_Roughness.png` + `_r4_jazz_20260926/source/R4_low_R4_Metallic.png` |
| `JAZZ_VektorR4_2_AO.dds` | AOMap | `_r4_jazz_20260926/source/R4_low_R4_AmbientOcclusion.png` |
| `AKR_AK103_0_Norm.dds` | NormalMap | `_ak103_native_20260926/Textures/AKR_AK103_NativeAtlas_Normal.tga` |
| `AKR_AK103_1_Base.dds` | BaseColorMap | `_ak103_native_20260926/Textures/AKR_AK103_NativeAtlas_Base.tga` |
| `AKR_AK103_2_RM.dds` | RMMap | `_ak103_native_20260926/Textures/AKR_AK103_NativeAtlas_RM.tga` |
| `AKR_AK103_3_Norm.dds` | NormalMap | `_ak103_native_20260926/Textures/AKR_AK103_Handguard_NativeAtlas_Normal.tga` |
| `AKR_AK103_4_Base.dds` | BaseColorMap | `_ak103_native_20260926/Textures/AKR_AK103_Handguard_NativeAtlas_Base.tga` |
| `AKR_AK103_5_RM.dds` | RMMap | `_ak103_native_20260926/Textures/AKR_AK103_Handguard_NativeAtlas_RM.tga` |
| `AKR_AK103_6_Norm.dds` | NormalMap | `_ak103_native_20260926/Textures/AKR_AK103_mag_ak_762x39_izhmash_103_Normal.tga` |
| `AKR_AK103_8_Base.dds` | BaseColorMap | `_ak103_native_20260926/Textures/AKR_AK103_mag_ak_762x39_izhmash_103_Base.tga` |
| `AKR_AK103_9_RM.dds` | RMMap | `_ak103_native_20260926/Textures/AKR_AK103_mag_ak_762x39_izhmash_103_RM.tga` |
| `AKR_AK103_7_AO.dds` | AOMap | `_ak103_native_20260926/Textures/AKR_AK103_mag_ak_762x39_izhmash_103_AO.tga` |
| `AKR_AK103_10_Norm.dds` | NormalMap | `_ak103_native_20260926/Textures/AKR_AK103_Muzzlebrake_Normal.tga` |
| `AKR_AK103_11_Base.dds` | BaseColorMap | `_ak103_native_20260926/Textures/AKR_AK103_Muzzlebrake_Base.tga` |
| `AKR_AK103_12_RM.dds` | RMMap | `_ak103_native_20260926/Textures/AKR_AK103_Muzzlebrake_RM.tga` |
| `AKR_AK103_13_Norm.dds` | NormalMap | `_ak103_native_20260926/Textures/AKR_AK103_Stock_Normal.tga` |
| `AKR_AK103_14_Base.dds` | BaseColorMap | `_ak103_native_20260926/Textures/AKR_AK103_Stock_Base.tga` |
| `AKR_AK103_15_RM.dds` | RMMap | `_ak103_native_20260926/Textures/AKR_AK103_Stock_RM.tga` |
| `JAZZ_VZ58_22_AO.dds` | AOMap | `_vz58_jazz_20260926/Textures/JAZZ_VZ58_Wire_AO.tga` |
| `JAZZ_VZ58_23_Base.dds` | BaseColorMap | `_vz58_jazz_20260926/Textures/JAZZ_VZ58_Wire_Base.tga` |
| `JAZZ_VZ58_24_RM.dds` | RMMap | `_vz58_jazz_20260926/Textures/JAZZ_VZ58_Wire_RM.tga` |

## Последние экспорты: read-only

Срез истории Git с 15.09.2026 плюс рабочее дерево: 112 entity, 111 уникальных материалов, 201 уникальных привязок карт. Семейства: АК, VZ58, R4, M4/M16/CAR15, M14/M21/Mk14/MkIII, SR-3M, L42A1, Мосина; обвес FAL. Мосинки только аудированы: цвет не менялся.

Все найденные DDS читаются, mip-цепочки полные; numeric карты не помечены sRGB. Первый аудит обнаружил 35 RM с несовпадением R/G вне восстановленных трёх семейств. После отдельного разрешения владельца все 35 пересобраны и установлены (70 DDS с fallbacks). Повторный аудит: 0 отклонений упаковки RM; остался только отдельный флаг NM M14 MkIII. BC/NM/AO/меши/материалы этих дополнительных семейств сохранены по SHA256. Manifest: `tmp/weapon-rm-remaining-20261003-v4`. Несовпадение — отклонение от упаковки, не доказательство причины видимого дефекта.

Таблица ниже — исходные находки; все строки RM устранены, NM остаётся для диагностики.

| Карта | Первоначальный результат |
| --- | --- |
| `RMMap:AKR_AK105_3_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AK105_12_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AK105_6_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AK105_9_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AK74M_6_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AK74M_3_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AK74_6_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AK74_12_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AK74_3_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AK74_9_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AKM_6_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AKM_9_RM.dds` | roughness not duplicated in G |
| `RMMap:AKR_AKM_3_RM.dds` | roughness not duplicated in G |
| `RMMap:FNFAL_ParaStk_4_RM.dds` | roughness not duplicated in G |
| `RMMap:JAZZ_FNFAL_Tac_4_RM.dds` | roughness not duplicated in G |
| `RMMap:JAZZ_FNFAL_Tac_8_RM.dds` | roughness not duplicated in G |
| `RMMap:JAZZ_M14_ART_RM.dds` | roughness not duplicated in G |
| `RMMap:JAZZ_M14_RM.dds` | roughness not duplicated in G |
| `NormalMap:JAZZ_M14_MkIII_Norm.dds` | more than 5% XY vectors exceed unit disk; investigate encoding |
| `RMMap:JAZZ_M14_MkIII_RM.dds` | roughness not duplicated in G |
| `RMMap:L42A1_4_RM.dds` | roughness not duplicated in G |
| `RMMap:L42A1_7_RM.dds` | roughness not duplicated in G |
| `RMMap:M16R_3_RM.dds` | roughness not duplicated in G |
| `RMMap:M16R_6_RM.dds` | roughness not duplicated in G |
| `RMMap:M16R_12_RM.dds` | roughness not duplicated in G |
| `RMMap:M16R_9_RM.dds` | roughness not duplicated in G |
| `RMMap:M16R_15_RM.dds` | roughness not duplicated in G |
| `RMMap:M4R_9_RM.dds` | roughness not duplicated in G |
| `RMMap:M4R_3_RM.dds` | roughness not duplicated in G |
| `RMMap:M4R_12_RM.dds` | roughness not duplicated in G |
| `RMMap:M4R_6_RM.dds` | roughness not duplicated in G |
| `RMMap:M4R_15_RM.dds` | roughness not duplicated in G |
| `RMMap:MK14EBR_RM.dds` | roughness not duplicated in G |
| `RMMap:MOSIN_4_RM.dds` | roughness not duplicated in G |
| `RMMap:MOSIN_8_RM.dds` | roughness not duplicated in G |
| `RMMap:MOSIN_12_RM.dds` | roughness not duplicated in G |

NM M14 MkIII: около 6,01% XY-векторов выходят за единичный диск с допуском 0,05. Это сигнал для проверки исходника/неиспользуемых UV-областей, не основание автоматически переворачивать G. Проверка знака Y и совпадения bake с mesh normals статистикой не выполнена.

## Магазины АК103

Штатный visual JAZZ_MagNormal для AK103 заменён на AKMWaffleMag, как у установленного AKM; Icon также от штатного AKM. Компонент хранится в items.lua без отдельного companion; metadata/load order не менялись. Существующий AK103:UpdateVisualObj выставляет абсолютные смещения: штатный (6,-9,-9), быстрый/40 (3,-10,-2), барабан (-9,-10,-8), мм. Прежние -30/-35 мм опускали верх заметно ниже native reference.

Offline proxy: центр bbox верхних 20 мм и верхняя точка относительно native AK103; максимальный остаток <0,7 мм. Реальная Lua-функция прогнана по 10 обновлений на вариант без накопления offset. Это не визуальная приёмка и не проверка столкновений. Владелец проверяет картинку сам; editor save/reload и визуальный verdict остаются открытыми. Составные иконки ранее снятых вариантов могут потребовать повторной съёмки после приёмки посадки.

## Проверки

- quick items/metadata: PASS; wrap-cycle: PASS.
- Generated-sync jazz: 0 blocking до и после; остаются посторонние warnings.
- Установка при закрытых JA3/Mod Editor; все изменённые DDS имеют backup, хеши и полные mip-chain.
- Runtime/human: прежний вид отвергнут владельцем как плоский. Восстановленный исходный вариант и новая посадка ещё не приняты.
