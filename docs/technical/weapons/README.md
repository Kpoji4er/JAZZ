# Канонический каталог оружия

Этот раздел является current-state источником истины для балансовой классификации и справочных характеристик стрелкового оружия JAZZ. Target behavior хранится в связанных specs.

## Источники и приоритет

| Данные | Канонический источник | Назначение |
|---|---|---|
| Характеристики оружия | `data/weapons.csv` | Одна строка на технический weapon ID |
| Доступные слоты и варианты | `data/weapon-component-options.csv` | Нормализованная связь оружие → слот → компонент |
| Компоненты | `data/weapon-components.csv` | Название, цена, сложность, эффекты и параметры |
| Эффекты компонентов | `data/weapon-component-effects.csv` | Словарь стабильных effect ID |
| Первичная миграция тиров | `data/tier-migration.csv` | Только происхождение тиров из Google Sheets; не второй источник истины |


Первичное заполнение характеристик выполнено из последнего коммита JAZZ `5db078dfb2c9206f39e491a1d26b6e7f1f6f1220`, а не из незакоммиченных плейтестовых изменений. Используемые JAZZ-компоненты дополнены определениями из официального JA3 source drop с `lua_revision = 233360`. После первичной миграции каноном являются CSV этого каталога.

## Текущий охват

- 160 технических записей оружия;
- 157 активных записей, попадающих в player wiki;
- `AR15`, `M4Commando` и базовый `MP5` имеют `catalog_status = excluded_disabled` и намеренно исключены из player wiki; полный реестр cut оружия и vanilla ammo (`TEST.png`) — [вырезанный контент](cut-content.md);
- 156 существующих записей сопоставлены со строками профильных вкладок Google Sheets;
- 20 строк таблицы пока не имеют runtime weapon ID и сохранены в `tier-migration.csv` со статусом `not_in_runtime`;
- у 22 активных записей canonical tier отличается от `comment = "Tier …"` в стабильном Lua. До синхронизации runtime верным считается `tier_label`, а старое значение доступно в `code_tier_label` только для аудита.

`Auto5_quest` существует в runtime, но не имеет отдельной строки в профильной таблице и пока остаётся без balance-tier. `DragunovSVD_Custom` и `BrowningM2HMG` перечислены в таблице без тира, поэтому их canonical tier также пуст.

## Иконки оружия (миниатюры)

| Иконка | ID | Название | Семья | Тир |
|---|---|---|---|---|
| <img src='../../WeaponIcons/MAC1950.png' alt='MAC1950' width='24'/> | MAC1950 | MAC Mle 1950 | Пистолеты | 1-1 |
| <img src='../../WeaponIcons/Luger.png' alt='Luger' width='24'/> | Luger | Люгер | Пистолеты | 1-2 |
| <img src='../../WeaponIcons/TT.png' alt='TT33' width='24'/> | TT33 | Пистолет ТТ | Пистолеты | 1-2 |
| <img src='../../WeaponIcons/SW52.png' alt='SWModel52' width='24'/> | SWModel52 | S&W Model 52 .38 Special Pistol | Пистолеты | 1-2 |
| <img src='../../WeaponIcons/Makarov.png' alt='Makarov' width='24'/> | Makarov | Пистолет Макарова | Пистолеты | 1-3 |
| <img src='../../WeaponIcons/1911.png' alt='Colt1911' width='24'/> | Colt1911 | Colt M1911 | Пистолеты | 1-3 |
| <img src='../../WeaponIcons/CZ52.png' alt='CZ52' width='24'/> | CZ52 | CZ Vz. 52 | Пистолеты | 1-3 |
| <img src='../../WeaponIcons/P210.png' alt='P210' width='24'/> | P210 | P-210 | Пистолеты | 1-3 |
| <img src='../../WeaponIcons/P38.png' alt='P38' width='24'/> | P38 | P38 | Пистолеты | 1-3 |
| <img src='../../WeaponIcons/PB.png' alt='PB' width='24'/> | PB | Пистолет ПБ | Пистолеты | 1-UNIQ |
| <img src='../../WeaponIcons/Hipower.png' alt='HiPower' width='24'/> | HiPower | Hi-Power | Пистолеты | 2-1 |
| <img src='../../WeaponIcons/SW5906.png' alt='SWModel5906' width='24'/> | SWModel5906 | S&W Model 5906 | Пистолеты | 2-1 |
| <img src='../../WeaponIcons/VectorSP1.png' alt='VectorCP1' width='24'/> | VectorCP1 | Vektor CP1 | Пистолеты | 2-1 |
| <img src='../../WeaponIcons/Viking.png' alt='MP446VIKING' width='24'/> | MP446VIKING | Викинг | Пистолеты | 2-2 |
| <img src='../../WeaponIcons/Beretta92.png' alt='Bereta92' width='24'/> | Bereta92 | Beretta 92F | Пистолеты | 2-2 |
| <img src='../../WeaponIcons/CZ75.png' alt='CZ75' width='24'/> | CZ75 | CZ75 | Пистолеты | 2-2 |
| <img src='../../WeaponIcons/Deagle.png' alt='DesertEagle' width='24'/> | DesertEagle | Desert Eagle | Пистолеты | 2-3 |
| <img src='../../WeaponIcons/Kimber.png' alt='Kimber' width='24'/> | Kimber | Kimber | Пистолеты | 2-4 |
| <img src='../../WeaponIcons/USP45.png' alt='USP45' width='24'/> | USP45 | USP45 Tactical | Пистолеты | 2-4 |
| <img src='../../WeaponIcons/Glock17.png' alt='Glock17' width='24'/> | Glock17 | Glock 17 | Пистолеты | 2-5 |
| <img src='../../WeaponIcons/GrizzlyLAR.png' alt='GrizzlyLAR' width='24'/> | GrizzlyLAR | Grizzly LAR | Пистолеты | 2-5 |
| <img src='../../WeaponIcons/P220.png' alt='P220' width='24'/> | P220 | P-220 | Пистолеты | 3-1 |
| <img src='../../WeaponIcons/P226.png' alt='P226' width='24'/> | P226 | P-226 | Пистолеты | 3-4 |
| <img src='../../WeaponIcons/57.png' alt='FiveSeven' width='24'/> | FiveSeven | FiveSeven | Пистолеты | 3-5 |
| <img src='../../WeaponIcons/Scorpion.png' alt='Scorpion' width='24'/> | Scorpion | Scorpion | Автоматические пистолеты | 1-3 |
| <img src='../../WeaponIcons/MicroUZI.png' alt='MicroUZI' width='24'/> | MicroUZI | Мини Узи | Автоматические пистолеты | 2-1 |
| <img src='../../WeaponIcons/MAC10.png' alt='MAC10' width='24'/> | MAC10 | MAC-10 | Автоматические пистолеты | 2-1 |
| <img src='../../WeaponIcons/Beretta93r.png' alt='Beretta93r' width='24'/> | Beretta93r | Beretta 93r | Автоматические пистолеты | 2-3 |
| <img src='../../WeaponIcons/APS.png' alt='APS' width='24'/> | APS | Пистолет Стечкина | Автоматические пистолеты | 2-4 |
| <img src='../../WeaponIcons/Glock18.png' alt='Glock18' width='24'/> | Glock18 | Glock 18 | Автоматические пистолеты | 2-5 |
| <img src='../../WeaponIcons/SWModel10.png' alt='SWModel10' width='24'/> | SWModel10 | S&W Model10 .38 Special | Револьверы | 1-1 |
| <img src='../../WeaponIcons/38sp.png' alt='Colt38Special' width='24'/> | Colt38Special | Colt .38 Special | Револьверы | 1-2 |
| <img src='../../WeaponIcons/Colt1917.png' alt='ColtM1917' width='24'/> | ColtM1917 | Colt M1917 .45 Service Revolver | Револьверы | 1-2 |
| <img src='../../WeaponIcons/ColtPeaceMaker.png' alt='ColtPeacemaker' width='24'/> | ColtPeacemaker | Peacemaker | Револьверы | 1-2 |
| <img src='../../WeaponIcons/SWModel19.png' alt='SWModel19' width='24'/> | SWModel19 | S*W Model19 .357 Combat Magnum | Револьверы | 1-3 |
| <img src='../../WeaponIcons/Welrod.png' alt='Welrod' width='24'/> | Welrod | Welrod | Револьверы | 1-UNIQ |
| <img src='../../WeaponIcons/Webley.png' alt='Webley' width='24'/> | Webley | Webley Mk VI | Револьверы | 2-1 |
| <img src='../../WeaponIcons/MR73.png' alt='MR73' width='24'/> | MR73 | Manurhin MR 73 | Револьверы | 2-3 |
| <img src='../../WeaponIcons/SWModel29.png' alt='SWModel29' width='24'/> | SWModel29 | SWModel29 | Револьверы | 2-4 |
| <img src='../../WeaponIcons/Anaconda.png' alt='ColtAnaconda' width='24'/> | ColtAnaconda | Anaconda | Револьверы | 2-5 |
| <img src='../../WeaponIcons/HiCalRev.png' alt='RSH12' width='24'/> | RSH12 | РШ-12 | Револьверы | 2-UNIQ |
| <img src='../../WeaponIcons/Korth.png' alt='Korth' width='24'/> | Korth | Korth Revolver | Револьверы | 3-1 |
| <img src='../../WeaponIcons/Tex.png' alt='TexRevolver' width='24'/> | TexRevolver | Именной револьвер | Револьверы | 3-UNIQ |
| <img src='../../WeaponIcons/MAT49.png' alt='MAT49' width='24'/> | MAT49 | MAT-49 | Пистолеты-пулемёты | 1-1 |
| <img src='../../WeaponIcons/MP40.png' alt='MP40' width='24'/> | MP40 | MP40 | Пистолеты-пулемёты | 1-1 |
| <img src='../../WeaponIcons/Sterling.png' alt='Sterling' width='24'/> | Sterling | Стерлинг | Пистолеты-пулемёты | 1-2 |
| <img src='../../WeaponIcons/M3GreaseGun.png' alt='M3GreaseGun' width='24'/> | M3GreaseGun | M3 Grease Gun | Пистолеты-пулемёты | 1-2 |
| <img src='../../WeaponIcons/PPS43.png' alt='PPS43' width='24'/> | PPS43 | ППС-43 | Пистолеты-пулемёты | 1-3 |
| <img src='../../WeaponIcons/PPSH.png' alt='PPSH' width='24'/> | PPSH | ППШ | Пистолеты-пулемёты | 1-3 |
| <img src='../../WeaponIcons/Thompson.png' alt='Thompson' width='24'/> | Thompson | Thompson | Пистолеты-пулемёты | 1-3 |
| <img src='../../WeaponIcons/MPL.png' alt='MPL' width='24'/> | MPL | Walther MP | Пистолеты-пулемёты | 1-3 |
| <img src='../../WeaponIcons/Agram2.png' alt='Agram2000' width='24'/> | Agram2000 | Аграм 2000 | Пистолеты-пулемёты | 2-1 |
| <img src='../../WeaponIcons/UZI.png' alt='UZI' width='24'/> | UZI | Узи Полноразмерный | Пистолеты-пулемёты | 2-1 |
| <img src='../../WeaponIcons/CarlGustaf.png' alt='M45' width='24'/> | M45 | Carl Gustaf M/45 | Пистолеты-пулемёты | 2-1 |
| <img src='../../WeaponIcons/BerettaM12.png' alt='BerettaM12' width='24'/> | BerettaM12 | Беретта М12 | Пистолеты-пулемёты | 2-2 |
| <img src='../../WeaponIcons/Bizon.png' alt='PP19Bizon' width='24'/> | PP19Bizon | ПП19 Бизон | Пистолеты-пулемёты | 2-3 |
| <img src='../../WeaponIcons/SpectreM4.png' alt='SpectreM4' width='24'/> | SpectreM4 | Spectre M4 | Пистолеты-пулемёты | 2-3 |
| <img src='../../WeaponIcons/MP5A2.png' alt='MP5A2' width='24'/> | MP5A2 | MP5A2 | Пистолеты-пулемёты | 2-4 |
| <img src='../../WeaponIcons/MP5K2.png' alt='MP5K' width='24'/> | MP5K | MP5K | Пистолеты-пулемёты | 2-4 |
| <img src='../../WeaponIcons/TMP2.png' alt='TMP' width='24'/> | TMP | TMP | Пистолеты-пулемёты | 2-4 |
| <img src='../../WeaponIcons/MP5A4.png' alt='MP5A4' width='24'/> | MP5A4 | MP5A4 | Пистолеты-пулемёты | 2-5 |
| <img src='../../WeaponIcons/UMP45.png' alt='UMP45' width='24'/> | UMP45 | UMP45 | Пистолеты-пулемёты | 2-5 |
| <img src='../../WeaponIcons/MP5SD.png' alt='MP5SD' width='24'/> | MP5SD | MP5SD | Пистолеты-пулемёты | 3-1 |
| <img src='../../WeaponIcons/MP72.png' alt='MP7' width='24'/> | MP7 | MP7 | Пистолеты-пулемёты | 3-2 |
| <img src='../../WeaponIcons/P90.png' alt='P90' width='24'/> | P90 | P90 | Пистолеты-пулемёты | 3-2 |
| <img src='../../WeaponIcons/Winchester.png' alt='Winchester1894' width='24'/> | Winchester1894 | Winchester 1894 | Карабины | 1-1 |
| <img src='../../WeaponIcons/M2Carbine.png' alt='M2Carbine' width='24'/> | M2Carbine | Карбайн | Карабины | 1-2 |
| <img src='../../WeaponIcons/DeLisle.png' alt='DeLisle' width='24'/> | DeLisle | De Lisle Carbine | Карабины | 1-UNIQ |
| <img src='../../WeaponIcons/Mini14.png' alt='Mini14' width='24'/> | Mini14 | Мини-14 | Карабины | 2-1 |
| <img src='../../WeaponIcons/ZastavaM92.png' alt='ZastavaM92' width='24'/> | ZastavaM92 | Zastava M92 | Карабины | 2-1 |
| <img src='../../WeaponIcons/CAR15.png' alt='CAR15' width='24'/> | CAR15 | CAR-15 | Карабины | 2-2 |
| <img src='../../WeaponIcons/AKSU.png' alt='AKSU' width='24'/> | AKSU | АКС-74У | Карабины | 2-3 |
| <img src='../../WeaponIcons/M4A1.png' alt='M4A1' width='24'/> | M4A1 | M4A1 | Карабины | 2-4 |
| <img src='../../WeaponIcons/VSS.png' alt='VSS' width='24'/> | VSS | ВСС | Карабины | 2-5 |
| <img src='../../WeaponIcons/G36C.png' alt='G36c' width='24'/> | G36c | G36c | Карабины | 2-5 |
| <img src='../../WeaponIcons/SIG552.png' alt='Sig552' width='24'/> | Sig552 | Sig 552 | Карабины | 3-1 |
| <img src='../../WeaponIcons/SIG552SWAT.png' alt='Sig552SWAT' width='24'/> | Sig552SWAT | Sig 552 SWAT | Карабины | 3-2 |
| <img src='../../WeaponIcons/ASVAL.png' alt='AS_Val' width='24'/> | AS_Val | АС-ВАЛ | Карабины | 3-3 |
| <img src='../../WeaponIcons/STG44.png' alt='STG44' width='24'/> | STG44 | StG-44 | Штурмовые винтовки | 1-2 |
| <img src='../../WeaponIcons/M16A1.png' alt='M16A1' width='24'/> | M16A1 | M16A1 | Штурмовые винтовки | 2-1 |
| <img src='../../WeaponIcons/Type56.png' alt='Type56' width='24'/> | Type56 | Type 56 | Штурмовые винтовки | 2-1 |
| <img src='../../WeaponIcons/Famas.png' alt='FAMAS' width='24'/> | FAMAS | FAMAS | Штурмовые винтовки | 2-2 |
| <img src='../../WeaponIcons/ZastavaM70.png' alt='Zastava_M70' width='24'/> | Zastava_M70 | Zastava M70 | Штурмовые винтовки | 2-2 |
| <img src='../../WeaponIcons/AK47.png' alt='AK47' width='24'/> | AK47 | АК47 | Штурмовые винтовки | 2-3 |
| <img src='../../WeaponIcons/AKM.png' alt='AKM' width='24'/> | AKM | AKM | Штурмовые винтовки | 2-3 |
| <img src='../../WeaponIcons/M16A2.png' alt='M16A2' width='24'/> | M16A2 | M16A2 | Штурмовые винтовки | 2-3 |
| <img src='../../WeaponIcons/AK74.png' alt='AK74' width='24'/> | AK74 | АК74 | Штурмовые винтовки | 2-4 |
| <img src='../../WeaponIcons/AR10DMR.png' alt='AR10DMR' width='24'/> | AR10DMR | AR-10 DMR | Штурмовые винтовки | 2-4 |
| <img src='../../WeaponIcons/HK33.png' alt='HK33' width='24'/> | HK33 | HK33 | Штурмовые винтовки | 2-4 |
| <img src='../../WeaponIcons/Aug.png' alt='AUG' width='24'/> | AUG | AUG | Штурмовые винтовки | 2-5 |
| <img src='../../WeaponIcons/G36.png' alt='G36' width='24'/> | G36 | G36 | Штурмовые винтовки | 2-5 |
| <img src='../../WeaponIcons/M16A4.png' alt='M16A4' width='24'/> | M16A4 | M16A4 | Штурмовые винтовки | 2-5 |
| <img src='../../WeaponIcons/SIG550.png' alt='Sig550' width='24'/> | Sig550 | Sig 550 | Штурмовые винтовки | 3-1 |
| <img src='../../WeaponIcons/SIG550Custom.png' alt='Sig550Custom' width='24'/> | Sig550Custom | Sig 550 RIS | Штурмовые винтовки | 3-2 |
| <img src='../../WeaponIcons/AN94.png' alt='AN94' width='24'/> | AN94 | АН-94 | Штурмовые винтовки | 3-UNIQ |
| <img src='../../WeaponIcons/SKS.png' alt='SKS' width='24'/> | SKS | СКС | Боевые винтовки | 1-1 |
| <img src='../../WeaponIcons/MAS36.png' alt='Mas36' width='24'/> | Mas36 | MAS36 | Боевые винтовки | 1-1 |
| <img src='../../WeaponIcons/M1Garand.png' alt='M1Garand' width='24'/> | M1Garand | М1 Гаранд | Боевые винтовки | 1-2 |
| <img src='../../WeaponIcons/SVT40.png' alt='SVT40' width='24'/> | SVT40 | СВТ-40 | Боевые винтовки | 1-3 |
| <img src='../../WeaponIcons/FG42.png' alt='FG42' width='24'/> | FG42 | FG42 | Боевые винтовки | 1-3 |
| <img src='../../WeaponIcons/G43.png' alt='G43' width='24'/> | G43 | G43 | Боевые винтовки | 1-3 |
| <img src='../../WeaponIcons/AVT40.png' alt='AVT40' width='24'/> | AVT40 | АВТ-40 | Боевые винтовки | 1-UNIQ |
| <img src='../../WeaponIcons/AR10.png' alt='AR10' width='24'/> | AR10 | AR-10 | Боевые винтовки | 2-1 |
| <img src='../../WeaponIcons/MAS49.png' alt='MAS49' width='24'/> | MAS49 | MAS-49/56 | Боевые винтовки | 2-1 |
| <img src='../../WeaponIcons/M14.png' alt='M14SAW' width='24'/> | M14SAW | M-14 | Боевые винтовки | 2-2 |
| <img src='../../WeaponIcons/FNFAL.png' alt='FNFAL' width='24'/> | FNFAL | FN-FAL | Боевые винтовки | 2-3 |
| <img src='../../WeaponIcons/Galil.png' alt='Galil' width='24'/> | Galil | Galil | Боевые винтовки | 2-4 |
| <img src='../../WeaponIcons/G3A3.png' alt='G3A3' width='24'/> | G3A3 | G3A3 | Боевые винтовки | 2-5 |
| <img src='../../WeaponIcons/G3A4.png' alt='G3A4' width='24'/> | G3A4 | G3A4 | Боевые винтовки | 2-5 |
| <img src='../../WeaponIcons/Mosin.png' alt='Mosin' width='24'/> | Mosin | Винтовка Мосина | Снайперские винтовки | 1-1 |
| <img src='../../WeaponIcons/K98.png' alt='Gewehr98' width='24'/> | Gewehr98 | Gewehr 98 | Снайперские винтовки | 1-2 |
| <img src='../../WeaponIcons/Springfield.png' alt='Springfield' width='24'/> | Springfield | Springfield 1903 | Снайперские винтовки | 1-2 |
| <img src='../../WeaponIcons/FRF2.png' alt='FRF2' width='24'/> | FRF2 | FR F2 | Снайперские винтовки | 2-2 |
| <img src='../../WeaponIcons/ZastavaM76.png' alt='ZastavaM76' width='24'/> | ZastavaM76 | Zastava M76 | Снайперские винтовки | 2-2 |
| <img src='../../WeaponIcons/M21.png' alt='M21' width='24'/> | M21 | M-21 | Снайперские винтовки | 2-3 |
| <img src='../../WeaponIcons/SVD.png' alt='DragunovSVD' width='24'/> | DragunovSVD | СВД | Снайперские винтовки | 2-4 |
| <img src='../../WeaponIcons/M700.png' alt='M700' width='24'/> | M700 | M700 | Снайперские винтовки | 2-4 |
| <img src='../../WeaponIcons/G3Sniper.png' alt='G3SniperV1' width='24'/> | G3SniperV1 | G3 SG | Снайперские винтовки | 2-5 |
| <img src='../../WeaponIcons/M24.png' alt='M24Sniper' width='24'/> | M24Sniper | M24 | Снайперские винтовки | 2-5 |
| <img src='../../WeaponIcons/M1A.png' alt='M1A' width='24'/> | M1A | M1A | Снайперские винтовки | 3-1 |
| <img src='../../WeaponIcons/SVU.png' alt='SVU' width='24'/> | SVU | СВУ | Снайперские винтовки | 3-2 |
| <img src='../../WeaponIcons/AWM.png' alt='ArcticWarfare' width='24'/> | ArcticWarfare | Arctic Warfare | Снайперские винтовки | 3-2 |
| <img src='../../WeaponIcons/Barret.png' alt='BarretM82' width='24'/> | BarretM82 | M82 | Снайперские винтовки | 3-3 |
| <img src='../../WeaponIcons/PSG.png' alt='PSG1' width='24'/> | PSG1 | PSG1 | Снайперские винтовки | 3-3 |
| <img src='../../WeaponIcons/SteyrScout.png' alt='ScoutSniper' width='24'/> | ScoutSniper | Steyr Scout | Снайперские винтовки | 3-UNIQ |
| <img src='../../WeaponIcons/SVDUniq.png' alt='DragunovSVD_Custom' width='24'/> | DragunovSVD_Custom | Шах и Мат | Снайперские винтовки |  |
| <img src='../../WeaponIcons/2429.png' alt='MAC2429' width='24'/> | MAC2429 | Mac 2429 | Ручные пулемёты | 1-1 |
| <img src='../../WeaponIcons/BAR.png' alt='BAR' width='24'/> | BAR | BAR | Ручные пулемёты | 1-2 |
| <img src='../../WeaponIcons/RPD.png' alt='RPD' width='24'/> | RPD | РПД | Ручные пулемёты | 2-1 |
| <img src='../../WeaponIcons/U100.png' alt='U100' width='24'/> | U100 | U100 | Ручные пулемёты | 2-1 |
| <img src='../../WeaponIcons/RPK.png' alt='RPK' width='24'/> | RPK | РПК | Ручные пулемёты | 2-3 |
| <img src='../../WeaponIcons/RPK74.png' alt='RPK74' width='24'/> | RPK74 | РПК-74 | Ручные пулемёты | 2-4 |
| <img src='../../WeaponIcons/Minimi.png' alt='FNMinimi' width='24'/> | FNMinimi | Minimi | Ручные пулемёты | 2-5 |
| <img src='../../WeaponIcons/HK21.png' alt='HK21' width='24'/> | HK21 | HK21 | Ручные пулемёты | 3-2 |
| <img src='../../WeaponIcons/HK23.png' alt='HK23e' width='24'/> | HK23e | HK23e | Ручные пулемёты | 3-2 |
| <img src='../../WeaponIcons/DP27.png' alt='DP27' width='24'/> | DP27 | ДП-27 | Пулемёты | 1-1 |
| <img src='../../WeaponIcons/MG42.png' alt='MG42' width='24'/> | MG42 | MG42 | Пулемёты | 1-3 |
| <img src='../../WeaponIcons/AA52.png' alt='AA52' width='24'/> | AA52 | AA-52 | Пулемёты | 2-2 |
| <img src='../../WeaponIcons/M60.png' alt='M60' width='24'/> | M60 | Свинья | Пулемёты | 2-3 |
| <img src='../../WeaponIcons/M60E3.png' alt='M60E3' width='24'/> | M60E3 | M60E3 | Пулемёты | 2-4 |
| <img src='../../WeaponIcons/PKM.png' alt='PKM' width='24'/> | PKM | ПКМ | Пулемёты | 2-5 |
| <img src='../../WeaponIcons/FNMAG.png' alt='FNMAG' width='24'/> | FNMAG | FN MAG | Пулемёты | 2-5 |
| <img src='../../WeaponIcons/M60E4.png' alt='M60E4' width='24'/> | M60E4 | M60E4 | Пулемёты | 3-1 |
| <img src='../../WeaponIcons/DoubleBarrel.png' alt='DoubleBarrelShotgun' width='24'/> | DoubleBarrelShotgun | Двустволка | Дробовики | 1-1 |
| <img src='../../WeaponIcons/M1897.png' alt='M1897' width='24'/> | M1897 | M1897 | Дробовики | 1-2 |
| <img src='../../WeaponIcons/AUTO5.png' alt='Auto5' width='24'/> | Auto5 | Auto-5 | Дробовики | 1-3 |
| <img src='../../WeaponIcons/Ithaca.png' alt='Ithaca' width='24'/> | Ithaca | Ithaca37 | Дробовики | 2-1 |
| <img src='../../WeaponIcons/R870.png' alt='R870' width='24'/> | R870 | R870 | Дробовики | 2-2 |
| <img src='../../WeaponIcons/Striker.png' alt='Striker' width='24'/> | Striker | Страйкер | Дробовики | 2-3 |
| <img src='../../WeaponIcons/Spas12.png' alt='SPAS12' width='24'/> | SPAS12 | SPAS-12 | Дробовики | 2-4 |
| <img src='../../WeaponIcons/Stoeger.png' alt='Stoeger' width='24'/> | Stoeger | Вертикалка | Дробовики | 2-UNIQ |
| <img src='../../WeaponIcons/M41.png' alt='M41Shotgun' width='24'/> | M41Shotgun | M1014 | Дробовики | 3-1 |
| <img src='../../WeaponIcons/USAS12.png' alt='USAS12' width='24'/> | USAS12 | USAS12 | Дробовики | 3-2 |
| <img src='../../WeaponIcons/AA12.png' alt='AA12' width='24'/> | AA12 | AA12 | Дробовики | 3-3 |

Записей с локальной иконкой: 154

### Без локальной миниатюры в репозитории

| ID | Название | Icon path (Lua) |
|---|---|---|
| MG58 | MG58 | UI/Icons/Weapons/MG58.png |
| BrowningM2HMG | M2 Browning | UI/Icons/Weapons/M2Browning |
| Auto5_quest | «Усмиритель» Мамаши | UI/Icons/Weapons/Auto5Quest |



## Контракт тиров

- `balance_tier` — силовой диапазон внутри оружейного семейства. Разница между тирами должна быть заметна по суммарной ценности оружия.
- `balance_subtier` — порядок или профиль близких вариантов внутри одного тира. Под-тир не должен создавать скрытый дополнительный тир.
- `UNIQ` — уникальный профиль внутри указанного основного тира.
- `tier_label` — каноническая запись вида `2-4` или `2-UNIQ`.
- `code_tier_label` — старый комментарий в Lua; не использовать для балансовых решений.
- `engine_tier` — независимое поле магазина/лута. Оно не является balance-tier.
- `tier_source` — происхождение текущей миграции. После утверждения CSV это поле остаётся provenance, а не разрешением снова считать Google Sheets каноном.

Сравнение тиров выполняется внутри семейства. Урон не является единственным бюджетом: магазин, ОД, прицеливание, BDR, дальность, кучность, эргономика, отдача, режимы огня, надёжность, ресурс и компоненты могут компенсировать друг друга.

## Схема `weapons.csv`

Идентификаторы и структура рассчитаны на чтение человеком, скриптом и языковой моделью:

- `id`, `object_class`, `family_id` — стабильные ключи; `display_name` и `family_name_ru` — представление;
- `catalog_status` — `active` или `excluded_disabled`;
- `balance_tier`, `balance_subtier`, `tier_label`, `tier_status` — каноническая классификация;
- `tier_source`, `code_tier_label`, `engine_tier` — provenance и независимые legacy/runtime поля;
- `caliber`, `damage`, `obj_damage_mod`, `penetration_class`, `penetration_bonus`, `crit_chance_scaled`, `magazine_size` — поражающее действие;
- `shoot_ap`, `reload_ap`, `max_aim_actions`, `aim_accuracy` — стоимость и прицеливание; AP хранится во внутренних тысячных движка;
- `burst_shots`, `auto_shots`, `recoil`, `available_attacks` — режимы огня;
- `weapon_range`, `bullet_drop_range`, `grouping` — дистанционный профиль; `handling` временно хранит legacy/runtime snapshot;
- `overwatch_angle`, `noise`, `reliability`, `base_jam_chance`, `weapon_resource`, `weapon_resource_max`, `degrade_per_shot` — применение и состояние;
- `hand_slot`, `holster_slot`, `large_item`, `cumbersome`, `cost`, `scrap_parts`, `repair_cost` — инвентарь и экономика;
- `component_slot_count`, `component_option_count` — быстрые счётчики;
- `defaulted_fields` — поля, отсутствовавшие в сериализованном weapon-файле и разрешённые через подтверждённый default класса;
- `source_file`, `snapshot_commit` — происхождение первичного импорта.

Текущая [модель стрельбы](accuracy-model.md) исключает `handling` из CTH. CSV продолжает хранить значение как legacy/runtime snapshot для машинного сравнения, но оно не является действующим статом точности.

## Нормализация компонентов

Плоские CTH-effects удалены из активной оптики в `weapon-components.csv`; оптический профиль теперь сдвигает эффективную зону. Улучшенные механические прицелы и не-оптические component effects сохраняют свои профильные эффекты.

`weapon-component-options.csv` содержит по одной строке на вариант компонента. Ключ связи — `(weapon_id, slot_index, component_id)`. Поля `default_component`, `default_in_options` и `is_default` позволяют находить сериализационные аномалии без разбора вложенного Lua.

`weapon-components.csv` хранит стабильный `component_id`, имя, слот, цену, сложность, effect ID, параметры и дополнительные материалы. `source = jazz` означает определение JAZZ; `source = vanilla_233360` — используемый fallback из официального source drop. `weapon-component-effects.csv` позволяет соединить effect ID с названием и описанием.

Из первичного снимка сохранены десять случаев, где `DefaultComponent` отсутствует среди `AvailableComponents`. Это не исправлено документацией автоматически: список показывается в индексе player wiki как data anomaly.

## Запланированные, но отсутствующие в runtime записи

| Вкладка | Название | Тир |
|---|---|---|
| ПП | Beretta MX4 Storm | 2-2 |
| ПП | PP-19 Vityaz | 3-2 |
| КАР | AK-105 | 3-1 |
| КАР | FN F2000 | 3-2 |
| ШВ | Stoner 63A | 2-3 |
| ШВ | FB Beryl | 2-5 |
| ШВ | AK-103 | 2-5 |
| ШВ | HK G11 | 2-UNIQ |
| ШВ | XM29 OICW | 2-UNIQ |
| ШВ | АК-74М | 3-1 |
| ШВ | HK416 | 3-1 |
| ШВ | АЕК-973 | 3-2 |
| ШВ | H&K XM8 | 3-3 |
| БВ | FN SCAR | 3-1 |
| ПУЛ | Negev | 3-1 |
| ПУЛ | MG4 | 3-3 |
| ПУЛ | PKP Pecheneg | 3-3 |
| ДРБ | Mossberg500 | 2-3 |
| ДРБ | KS-23 | 3-1 |
| ДРБ | Saiga-12 | 2-5 |

Они не появляются в player wiki, пока не получат runtime ID и полный набор характеристик/слотов.

## Процесс изменения

1. Сначала изменить канонические CSV и зафиксировать балансовое намерение.
2. Выполнить `node scripts/docs/weapons-docs.mjs build`.
3. Внести те же данные через Mod Editor в принадлежащие JAZZ generated files; не править только одну сериализованную копию.
4. Проверить diff `items.lua`, `metadata.lua` и профильных `InventoryItem`.
5. Выполнить `node scripts/docs/weapons-docs.mjs check`, статические проверки и игровые smoke-тесты.

Команда `import` предназначена только для первичной загрузки или осознанного полного re-bootstrap и без `--force` не перезаписывает существующий каталог. Обычное обновление никогда не должно начинаться с импорта из Lua.

Перед `import` задать `JA3_ROOT` корнем установленной игры либо `JA3_WEAPON_COMPONENTS_PATH` полным путём к `WeaponComponentSharedClass.lua`. В tracked-файлах используется только `<JA3_ROOT>`; абсолютный путь конкретной машины не сохраняется.

## Связанные документы

- [Каноническая модель точности](accuracy-model.md)
- [Роли классов оружия и будущие перковые действия](class-roles.md)
- [Стрелковые Combat Actions и их связь с оружием](combat-actions.md)
- [Техническая система оружия, боеприпасов и компонентов](../systems/weapons-ammo-components.md)
- [Текущий runtime CTH pipeline](../systems/combat-cth-actions.md)
- Игроковая энциклопедия
