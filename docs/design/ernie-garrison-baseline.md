# Ernie garrison baseline (pre-rework)

Snapshot before full Ernie / Legion squad rework. **Do not treat as target design.**

## Locked targets (owner 2026-08-10)

| Band | N |
| --- | --- |
| Typical starting garrison (one Init) | 20–30 |
| Filler coastal (e.g. M5) | 22–26 |
| Hub / story seed (I5, I7) | ~35–45 |
| Extra / spice (if any) | +3–6 |
| M1–M3 | 0 Init (map markers); ~⅓ Roughneck → Recruit on map |
| Class mix (UnitData T1–T4) | **majority T1–T2**; **a little T3**; **T4 = 1–2 on whole island**, random spots (not per sector). **Story spend:** I7 `FortressPierre` suite = **2× Headsman** (Pierre kept). |
| `FortressDefenders` (I7 maps) | **LOCKED** base ~48 for Ernie maps. |
| `FortressDefenders_NoMaps` | **~16** (half of retired `LegionFortressDefenders` 32). NoMaps `SQUAD_REMAP` / garrison lists use this — not the Ernie 48 pack. |
| `LegionFortressDefenders` | **Deleted** (was maps+NoMaps fat ~32). |
| Difficulty size delta (future setting) | Authored **base** N (Normal). **Easy = base − 10**, **Hard = base + 10**. Applies to starting garrison / authored Init packs going forward (not a one-off for I7 only). Difficulty UI/settings = follow-up work; lock the delta now. |
| Squad slot variance (replayability) | Authored packs use **weighted / alternate unit pools** in slots. Keep role+count stable; swap siblings within band. Anchors fixed: named story, officers/NCOs, medics, **≤1 HeavyT2_Grenadier**, Mortarman, RPG, key precision. |

**Class tier ≠ gear tier:** `JAZZ_Legion_*T1…T4*` = experience / archetype / role kit. Campaign `JAZZ_Legion_Tier` = loot/equipment progression only. Do not use Ernie class mix as a stand-in for gear tier, or vice versa.

**I7 Init target shape (LOCKED):** only `FortressPierre` (Pierre + Headsman suite) + **`FortressDefenders` (base 48)**. **Do not** stack `LegionFortressDefenders` or `LegionAttackers_Ordnance_Easy` — the locked Defenders pack already covers balanced fort defense (incl. mortar / RPG / single GL).

**Difficulty (owner lock):** size bands in this doc are **Normal base**. Easy/Hard shift body count by **±10** once difficulty settings exist; class-mix rules (T1–T2 majority, little T3, island T4 budget) stay unless overridden per pack. Applies to authored Init **and** quest punitive packs (e.g. `ErnieCounterAttack`).

### LOCKED `ErnieCounterAttack` (quest I7→I5; Normal base **30**; owner 2026-08-10)

Soft-nerf vs old ~37 (NoMaps complaints: too big/strong). Easy **20** / Hard **40** when difficulty settings exist.

| N | Unit |
|--:|---|
| 1 | `LeaderT1_Sergeant` (was 2) |
| 3 | Roughneck |
| 6 | ShockTrooper (was 8) |
| 2 | Ambusher |
| 2 | ShockTrooper (was 3) |
| 6 | Raider (was 8) |
| 2 | AssaultT1_Grenadier |
| 1 | Mortarman |
| 2 | GMPG (was 3) |
| 1 | Rocketeer |
| 1 | FrontT3_Veteran |
| 3 | Bonemaker |

**Total 30.** Keep: 3 medics, 1 mortar, 1 RPG, 2 thrower grenadiers. No HeavyT2_Grenadier.

### LOCKED `FortressDefenders` composition (Normal base **48**; owner 2026-08-10)

| N | Role | Units |
|--:|---|---|
| 1 | Officer | `LeaderT2_Lieutenant` |
| 2 | NCOs | `LeaderT1_Sergeant` ×2 |
| 2 | Medics | `FrontT1_Bonemaker` ×2 |
| 1 | Mortar | `HeavyT3_Mortarman` |
| 1 | RPG | `HeavyT1_Rocketeer` |
| 1 | GL | `HeavyT2_Grenadier` ×1 (**hard cap**) |
| 4 | MG | 2× `GunnerT2_GMPG` + 1× `GunnerT1_Gunner` + 1× `GunnerT2_AssaultGunner` |
| 3 | Precision | 2× `FrontT3_Sniper` + 1× `FrontT2_Marksman` |
| 2 | Ambush | `FrontT2_Ambusher` |
| 6 | Flank | 2× Warden + 2× Scout + 1× Skirmisher + 1× Recon |
| 8 | Line | 3× Raider + 2× Rifleman + 2× Marauder + 1× `FrontT3_Veteran` |
| 8 | Assault | 2× Shock + 2× AssaultT1_Grenadier + 2× Crusher + 1× Pillager + 1× Pyro |
| 6 | Meat | 3× Roughneck + 3× Marauder/Rifleman pool |
| 3 | Little T3 | 1× Punisher + 1× SkullCrusher + 1× `FrontT3_Veteran` (or 2nd Punisher). **No `GunnerT3_VeteranGunner`** |

**Total 48.** Easy 38 / Hard 58. Variance: weighted pools on line / assault / flank / meat / little-T3; anchors fixed (LT, 2 SGT, 2 Bonemaker, Mortar, RPG, 1 GL, 2 Sniper). Implementation deferred until Ernie squads change-spec is approved — this table is the contract for `FortressDefenders`.

### LOCKED Villa camps K3/K5/L3/L4/L5 (owner 2026-08-10)

Shared `JAZZ_Legion_SentrySquad_AroundVilla` **base 10** (camp guard; stays) + sector `VillaAttackers_*` (**movable siege waves** for `Jazz_VillaCounterAttack`). Sector Init totals Normal **22 / 23 / 24 / 25 / 26**. Easy/Hard ±10 later.

| Sector | Sentry | Attacker | Normal | Easy | Hard |
| --- | ---: | ---: | ---: | ---: | ---: |
| K3 | 10 | K3=12 (Ranger) | 22 | 12 | 32 |
| K5 | 10 | K5=13 (Captain) | 23 | 13 | 33 |
| L3 | 10 | L3=14 (LT) | 24 | 14 | 34 |
| L4 | 10 | L4=15 (SGT + RPG) | 25 | 15 | 35 |
| L5 | 10 | L5=16 (Headsman + mortar) | 26 | 16 | 36 |

**Siege (`JAZZ-QUESTS-003`):** after `FlagHill_Emma_1` Guests → route surviving Attackers + always `JAZZ_Legion_VillaAttackers_Ernie` (30) → K4; AdvanceTo Emma; Wave2 ~25 on CombatTurn≥3; late columns dump. K4 map HouseAmbushers+Legion AdvanceTo **purged**.

Applied camp sizes via `docs/tools/_tighten_villa_squads.py`. Counts fixed (Min=Max); role variance stays in weighted pools.

Policy: with Legion Global AI, static `InitialSquads` = starting garrisons or quest packs — not the living army. Living pressure = AI (patrol / reinforce / QRF).

## Counts by sector

| Sector | Name | Init sum | Init packs | Patrol/Strong/Extra | Map enemies≈ | Notes |
| --- | --- | ---: | --- | --- | ---: | --- |
| M1 | Зона высадки | 0 | — | — | 1 | Стартовый берег; map-only enemies |
| M2 | Скалистый берег | 0 | — | — | 24 | Филер_2я локация; map-only enemies |
| M3 | Водопад | 0 | — | — | 33 | Водопад; map-only enemies |
| M4 | The Outlook | 30 | LegionOutlook_Easy(30) | — | 0 | Смотровая площадка |
| M5 | Береговая линия | 53 | LegionAttackers_JazzBalanced_Easy_Assault(35), LegionExtraSquadFireArms_T2(18) | — | 0 | Филер по пути к пляжу |
| M6 | Старый порт | 36 | LegionExtraSquadFireArms_T2(18), LegionAttackers_Marksmen_Easy(12), LegionHeavyTroops_Gunners(6) | — | 0 | Филер_2 по пути к пляжу |
| I2 | Лечебница в маяке | 32 | LegionAttackers_Marksmen_Easy(12), LegionAttackers_Balanced_Easy(8), LegionDefenders_Mobile_Easy(12) | — | 0 | Маяк доктора |
| I3 | Дорога к маяку | 8 | LegionAttackers_Balanced_Easy(8) | — | 0 | Мост в Эрни |
| I4 | Дорога на маяк | 8 | LegionDefenders_Entrenched_Easy(8) | — | 0 | Дорога на острове эрни |
| I5 | Village of Ernie | 61 | LegionErnieVillage(46), LegionExtraSquadFireArms(15) | — | 10 | Деревня Эрни |
| I6 | The Rust | 0 | — | — | 0 | Жестянка |
| I6_Underground | Bunker FB45-68 | 0 | — | — | 0 | Бункер_Жестянки |
| I7 | Fort L'Eau Bleu | (pre-rework snapshot) | … | … | 0 | **Target Init:** only FortressPierre + FortressDefenders(48). Drop LegionFortressDefenders + Ordnance |
| J4 | Дорога в Эрни | 0 | — | — | 4 | Дорога; map-only enemies |
| J5 | Фермы Эрни | 56 | LegionExtraSquadFireArms(15), LegionDefenders_Shooters_Easy(33), LegionDefenders_Balanced_Easy(8) | — | 0 | Фермы Эрни |
| J6 | Аванпост контрабандистов | 0 | — | — | 55 | Аванпост туда ходи; map-only enemies |
| J7 | Emerald Coast | 0 | — | — | 0 | Изумрудный берег |
| K3 | Походный лагерь Легиона | **22** | Sentry(10) + VillaAttackers_K3(12) | — | 0 | LOCKED Normal; Easy 12 / Hard 32 |
| K4 | Flag Hill | (map Raiders) | — | — | ~24 Raiders | HouseAmbushers AdvanceTo **purged**; siege = sat `Jazz_VillaCounterAttack` |
| K5 | Походный лагерь Легиона | **23** | Sentry(10) + VillaAttackers_K5(13) | — | 2 | LOCKED Normal; Easy 13 / Hard 33 |
| K6 | Запасной лагерь Контрабандистов | 0 | — | — | 91 | Запасной лагерь Контрабандистов; map-only enemies |
| L1 | База партизан на острове Эрни | 65 | LegionRaidSquad_01(6), LegionHeavyTroops(10), LegionJAZZSquadT2(34), LegionExtraSquadFireArms(15) | — | 0 | База партизан на острове |
| L2 | Непроходимая местность | 27 | LegionExtraSquadMeleeV2(7), LegionExtraSquadMelee_T2(14), LegionRaidSquad_01(6) | — | 0 | Река, дебри |
| L3 | Походный лагерь Легиона | **24** | Sentry(10) + VillaAttackers_L3(14) | — | 0 | LOCKED Normal; Easy 14 / Hard 34 |
| L4 | Походный лагерь Легиона | **25** | Sentry(10) + VillaAttackers_L4(15) | — | 1 | LOCKED Normal; Easy 15 / Hard 35 |
| L5 | Походный Лагерь Легиона | **26** | Sentry(10) + VillaAttackers_L5(16) | — | 1 | LOCKED Normal; Easy 16 / Hard 36 |
| L6 | Заброшенный вход в бункер | 30 | Legion_Patrol_1(16), LegionExtraSquadMelee_T2(14) | — | 0 | Вход в бункер, соединенный с L1 |
| L6_Underground | Бункер партизан | 31 | LegionExtraSquadFireArms_T2(18), LegionRaidSquad_01(6), LegionExtraSquadMeleeV2(7) | — | 0 | Бункер партизан |
| L7 | Рыбацкая деревня | 0 | — | — | 0 | Небольшая рыбацкая деревня |

## Notes on measurement

- **Init sum** = sum of `UnitCountMin` over referenced `ModItemEnemySquads` in `jazz-units` (fallback: vanilla `EnemySquads.lua` if ID not in jazz-units).
- **Map enemies≈** = `UnitMarker` with enemy-ish Side / Legion-like UnitData on the sector map dump (approximate; triggers/spawns may add more).
- I7 Patrol/Strong/Extra are **pools**, not all spawned at once — do not add them to Init sum.
- Regenerated by `docs/tools/_ernie_garrison_baseline.py`.

