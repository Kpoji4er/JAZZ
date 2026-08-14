# Legion weapon availability by equipment tier

Design + R.I.S. copy checklist. **Line troops only** (Assault / Front / Flanker / Gunner / Heavy).
Elites and sergeants/leaders use the same primary pools filtered by role tags, but R.I.S. supply briefs talk about the **new unlock band**, not named elites.

Source: `docs/technical/weapons/data/weapons.csv` `tier_label` (`X-Y` → Amount `XY`).
Runtime arch bands: **11–13** = arch1; **21–25** = arch2 (+ ~1% arch1 remnant); **31–33** = arch3 only.
Heavy launchers (`RPG7`/`M72LAW`, `M79`, mortar) are **not** laddered by `tier_label` — fixed LootDefs.

UNITS-008: `M2Carbine` M1 config (wood stock) is in carbine pools from day one (no Amount ≥); no-stock → SMG roles; folded/light AssaultRifles borrow into carbine at weight 6000. See `scripts/legion-loadouts/data/early_variants.json`.

Generator: `docs/tools/_gen_legion_weapon_availability_map.py`.
Briefs: `docs/design/ris-legion-tier-briefs.md` + `docs/tools/_rewrite_ris_legion_briefs.py`.

## Tier 11 (arch 1-1)

- **LightMachineGun:** `MAC2429` (Mac 2429)
- **Боевые винтовки:** `SKS` (СКС), `Mas36` (MAS36)
- **Дробовики:** `DoubleBarrelShotgun` (Double-Barrel)
- **Карабины:** `Winchester1894` (Winchester 1894)
- **ПП:** `MAT49` (MAT-49), `MP40`
- **Пистолеты / револьверы:** `MAC1950` (MAC Mle 1950), `SWModel10` (S&W Model10 .38 Special)
- **Пулемёты:** `DP27` (ДП-27)
- **Снайперские:** `Mosin` (Винтовка Мосина)

## Tier 12 (arch 1-2)

- **LightMachineGun:** `BAR`
- **Боевые винтовки:** `M1Garand` (М1 Гаранд)
- **Дробовики:** `M1897`
- **Карабины:** `M2Carbine` (Карбайн)
- **ПП:** `Sterling` (Стерлинг), `M3GreaseGun` (M3 Grease Gun)
- **Пистолеты / револьверы:** `Luger` (Люгер), `TT33` (Пистолет ТТ), `SWModel52` (S&W Model 52 .38 Special Pistol), `Colt38Special` (Colt .38 Special), `ColtM1917` (Colt M1917 .45 Service Revolver), `ColtPeacemaker` (Peacemaker)
- **Снайперские:** `Gewehr98` (Gewehr 98), `Springfield` (Springfield 1903)
- **Штурмовые:** `STG44` (StG-44)

## Tier 13 (arch 1-3)

- **Autopistol:** `Scorpion`
- **Боевые винтовки:** `SVT40` (СВТ-40), `FG42`, `G43`
- **Дробовики:** `Auto5` (Auto-5)
- **ПП:** `PPS43` (ППС-43), `PPSH` (ППШ), `Thompson`, `MPL` (Walther MP)
- **Пистолеты / револьверы:** `Makarov` (Пистолет Макарова), `Colt1911` (Colt M1911), `CZ52` (CZ Vz. 52), `P210` (P-210), `P38`, `SWModel19` (S*W Model19 .357 Combat Magnum)
- **Пулемёты:** `MG42`

## Tier 21 (arch 2-1)

- **Autopistol:** `MicroUZI` (Мини Узи), `MAC10` (MAC-10)
- **LightMachineGun:** `RPD` (РПД), `U100`
- **Боевые винтовки:** `AR10` (AR-10), `MAS49` (MAS-49/56)
- **Дробовики:** `Ithaca` (Ithaca37)
- **Карабины:** `Mini14` (Мини-14), `ZastavaM92` (Zastava M92)
- **ПП:** `Agram2000` (Аграм 2000), `UZI` (Узи Полноразмерный), `M45` (Carl Gustaf M/45)
- **Пистолеты / револьверы:** `HiPower` (Hi-Power), `SWModel5906` (S&W Model 5906), `VectorCP1` (Vektor CP1), `Webley` (Webley Mk VI)
- **Штурмовые:** `M16A1`, `Type56` (Type 56)

## Tier 22 (arch 2-2)

- **Боевые винтовки:** `M14SAW` (M-14)
- **Дробовики:** `R870`
- **Карабины:** `CAR15` (CAR-15)
- **ПП:** `BerettaM12` (Беретта М12)
- **Пистолеты / револьверы:** `MP446VIKING` (Викинг), `Bereta92` (Beretta 92F), `CZ75`
- **Пулемёты:** `AA52` (AA-52)
- **Снайперские:** `FRF2` (FR F2), `ZastavaM76` (Zastava M76)
- **Штурмовые:** `FAMAS`, `Zastava_M70` (Zastava M70)

## Tier 23 (arch 2-3)

- **Autopistol:** `Beretta93r` (Beretta 93r)
- **LightMachineGun:** `RPK` (РПК)
- **Боевые винтовки:** `FNFAL` (FN-FAL)
- **Дробовики:** `Striker` (Страйкер)
- **Карабины:** `AKSU` (АКС-74У)
- **ПП:** `PP19Bizon` (ПП19 Бизон), `SpectreM4` (Spectre M4)
- **Пистолеты / револьверы:** `DesertEagle` (Desert Eagle), `MR73` (Manurhin MR 73)
- **Пулемёты:** `M60` (Свинья)
- **Снайперские:** `M21` (M-21)
- **Штурмовые:** `AK47` (АК47), `AKM`, `M16A2`

## Tier 24 (arch 2-4)

- **Autopistol:** `APS` (Пистолет Стечкина)
- **LightMachineGun:** `RPK74` (РПК-74)
- **Боевые винтовки:** `Galil`
- **Дробовики:** `SPAS12` (SPAS-12)
- **Карабины:** `M4A1`
- **ПП:** `MP5A2`, `MP5K`, `TMP`
- **Пистолеты / револьверы:** `Kimber`, `USP45` (USP45 Tactical), `SWModel29`
- **Пулемёты:** `M60E3`
- **Снайперские:** `DragunovSVD` (Dragunov), `M700`
- **Штурмовые:** `AK74` (АК74), `AR10DMR` (AR-10 DMR), `HK33`

## Tier 25 (arch 2-5)

- **Autopistol:** `Glock18` (Glock 18)
- **LightMachineGun:** `FNMinimi` (Minimi)
- **Боевые винтовки:** `G3A3`, `G3A4`
- **Карабины:** `VSS` (ВСС), `G36c`
- **ПП:** `MP5A4`, `UMP45`
- **Пистолеты / револьверы:** `Glock17` (Glock 17), `GrizzlyLAR` (Grizzly LAR), `ColtAnaconda` (Anaconda)
- **Пулемёты:** `PKM` (ПКМ), `FNMAG` (FN MAG)
- **Снайперские:** `G3SniperV1` (G3 SG), `M24Sniper` (M24)
- **Штурмовые:** `AUG`, `G36`, `M16A4`

## Tier 31 (arch 3-1)

- **Дробовики:** `M41Shotgun` (M1014)
- **Карабины:** `Sig552` (Sig 552)
- **ПП:** `MP5SD`
- **Пистолеты / револьверы:** `P220` (P-220), `Korth` (Korth Revolver)
- **Пулемёты:** `M60E4`
- **Снайперские:** `M1A`
- **Штурмовые:** `Sig550` (Sig 550)

## Tier 32 (arch 3-2)

- **LightMachineGun:** `HK21`, `HK23e`
- **Дробовики:** `USAS12`
- **Карабины:** `Sig552SWAT` (Sig 552 SWAT)
- **ПП:** `MP7`, `P90`
- **Снайперские:** `SVU` (СВУ), `ArcticWarfare` (Arctic Warfare)
- **Штурмовые:** `Sig550Custom` (Sig 550 RIS)

## Tier 33 (arch 3-3)

- **Дробовики:** `AA12`
- **Карабины:** `AS_Val` (АС-ВАЛ)
- **Снайперские:** `BarretM82` (M82), `PSG1`
