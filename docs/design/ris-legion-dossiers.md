# R.I.S. Legion unit dossiers (canon)

Unlock: contact sighting mail (catalog) and/or ≥3 player-side kills (full body).
Copy source: `docs/tools/_ris_dossier_copy.py` → apply via `_apply_ris_dossier_copy.py`.
Gameplay sources: current `../jazz-units/UnitData/JAZZ_Legion_*.lua`, `scripts/legion-loadouts/data/recipes.json`, and `docs/technical/systems/legion-units-equipment-tiers.md`.

## Review checklist

- [ ] The opening explains whom the Major recruits, promotes, or hires and how that tier is prepared.
- [ ] Combat behavior matches the current UnitData role, archetype, AIKeywords, and relevant perks.
- [ ] Weapon, armor, and utility claims are supported by the current loadout recipe.
- [ ] The closing gives useful threat or counterplay without raw stats, IDs, or unlock mechanics.
- [ ] English reads as an analyst's field note; Russian is idiomatic prose, not a literal calque.
- [ ] RU and EN preserve the same gameplay meaning, titles, and degree of certainty.
- [ ] Design-only AI proposals are not presented as loaded runtime behavior.

## Runtime coverage

| UnitData id | Title | Notes |
| --- | --- | --- |
| `JAZZ_Legion_AssaultT1_Crusher` | **Crusher** / Громила | The Legion picks its strongest bruisers for Crusher duty and teaches them one job: close the distance. A shotgun, solid armor, and sheer… |
| `JAZZ_Legion_AssaultT1_Grenadier` | **Grenadier** / Гренадёр | New Grenadiers receive a short course in assault explosives before the Legion sends them forward. They carry several grenades beside a… |
| `JAZZ_Legion_AssaultT1_Roughneck` | **Roughneck** / Головорез | Roughnecks receive little formal training; the Legion expects speed and aggression to make up the difference. They fire pistols or… |
| `JAZZ_Legion_AssaultT2_Pillager` | **Pillager** / Грабитель | The Legion forms Pillager teams from raiders who survived their first street fights and learned to keep moving. Light armor keeps them… |
| `JAZZ_Legion_AssaultT2_Pyro` | **Pyro** / Пироман | Pyros are assault troops singled out for incendiary work rather than careful demolition. They wear heavy armor, carry several firebombs,… |
| `JAZZ_Legion_AssaultT2_ShockTrooper` | **Shock Trooper** / Штурмовик | Shock Troopers are survivors of the early assault ranks, retrained to keep an attack moving through resistance. They open the assault with… |
| `JAZZ_Legion_AssaultT3_Punisher` | **Punisher** / Каратель | Punishers are drawn from assault veterans and trained to keep an attack moving after the first breach. Heavy armor, automatic rifles, and… |
| `JAZZ_Legion_AssaultT3_SkullCrusher` | **Skull Crusher** / Череполом | Skull Crushers are veteran brawlers trained to force a close fight through smoke and confusion. Heavy armor carries them into shotgun or… |
| `JAZZ_Legion_AssaultT4_Headsman` | **Headsman** / Палач | Only the Legion's best assault veterans are promoted to Headsman duty and equipped as elite professionals. Heavy armor, upgraded automatic… |
| `JAZZ_Legion_FlankerT1_Warden` | **Warden** / Дозорный | Wardens are ordinary riflemen given basic scouting instruction and posted away from the main line. Their light gear helps them reach a… |
| `JAZZ_Legion_FlankerT2_Scout` | **Scout** / Скаут | Scouts are survivors of Warden patrols who have learned to move quietly and choose their approach. They slip around the line with… |
| `JAZZ_Legion_FlankerT2_Skirmisher` | **Skirmisher** / Застрельщик | Skirmishers are picked for marksmanship and trained to fight away from the main line. They carry light armor and battle rifles, shifting… |
| `JAZZ_Legion_FlankerT3_Pathfinder` | **Pathfinder** / Следопыт | Pathfinders are seasoned scouts trained to choose a concealed firing lane and hold it. Their light gear lets them reach a flank with a… |
| `JAZZ_Legion_FlankerT3_Recon` | **Recon** / Разведчик | Recon troops are veteran scouts trained for quiet approaches and night fighting. They use light gear and compact automatic weapons to… |
| `JAZZ_Legion_FlankerT4_Ranger` | **Ranger** / Рейнджер | Rangers are elite scouts selected from the Legion's best flankers and given its finest field training. They move quickly and quietly with… |
| `JAZZ_Legion_FrontT1_Bonemaker` | **Bonemaker** / Костоправ | A recruit who breaks from the line to reach a wounded Legionnaire is probably a Bonemaker. The Major chooses people who stay calm around… |
| `JAZZ_Legion_FrontT1_Marauder` | **Marauder** / Мародёр | Looters and local toughs fill the Marauder ranks. They start with pistols and submachine guns; assault rifles appear once better supplies… |
| `JAZZ_Legion_FrontT1_Rifleman` | **Rifleman** / Стрелок | Most Riflemen are conscripts with a few marksmanship lessons, posted to guard roads, doorways, and village approaches. From cover, they… |
| `JAZZ_Legion_FrontT2_Ambusher` | **Ambusher** / Засадник | Ambushers are patient shooters taught to prepare concealed firing positions along likely approaches. From a prepared position, they wait… |
| `JAZZ_Legion_FrontT2_Marksman` | **Marksman** / Охотник | The best shots in regular squads are given accurate rifles and taught to wait for a clean shot. They work behind the front, hold useful… |
| `JAZZ_Legion_FrontT2_Raider` | **Raider** / Налётчик | Raiders are adaptable front-line fighters drilled with automatic weapons; every one also receives hand grenades. They move with the line,… |
| `JAZZ_Legion_FrontT3_Sniper` | **Sniper** / Снайпер | Only the Legion's finest riflemen receive sniper training: patience, target selection, and careful use of scoped rifles. They watch open… |
| `JAZZ_Legion_FrontT3_Veteran` | **Veteran** / Ветеран | Veterans have survived several campaigns and stayed steady under fire. They advance stubbornly with automatic fire and grenades; a few… |
| `JAZZ_Legion_FrontT4_Mercenary` | **Mercenary** / Наёмник | The Legion hires experienced Mercenaries to hold important positions and sends them out with good weapons. They move with the front and… |
| `JAZZ_Legion_FrontT4_MercenarySniper` | **Mercenary Sniper** / Наёмник-снайпер | Mercenary Snipers are proven specialists hired for operations where accurate long-range fire can decide the opening exchange. They begin… |
| `JAZZ_Legion_GunnerT1_Gunner` | **Gunner** / Пуляло | The Legion hands its strongest new recruits old machine guns and gives them a hurried lesson in using them. They set up across roads and… |
| `JAZZ_Legion_GunnerT2_AssaultGunner` | **Assault Gunner** / Коммандо | Surviving Gunners are promoted to Assault Gunner duty and taught to carry their light machine guns forward instead of guarding one… |
| `JAZZ_Legion_GunnerT2_GMPG` | **GPMG** / Пулемётчик | Reliable machine gunners are assigned to GPMG duty and taught to keep their fire steady without wasting ammunition. They settle into… |
| `JAZZ_Legion_GunnerT3_VeteranGunner` | **Veteran Gunner** / Подавитель | Veteran Gunners have survived repeated engagements and are trusted with stronger machine guns. They use disciplined bursts and expert… |
| `JAZZ_Legion_GunnerT4_MercGunner` | **Merc Gunner** / Наёмник-пулемётчик | Merc Gunners are experienced heavy-weapon specialists hired to use the strongest machine guns available to the Legion. They combine… |
| `JAZZ_Legion_HeavyT1_Rocketeer` | **Rocketeer** / Ракетчик | Rocketeers are recruits with enough nerve to shoulder a launcher and just enough instruction to avoid hitting their own squad. They fire… |
| `JAZZ_Legion_HeavyT2_Grenadier` | **Heavy Grenadier** / Гранатомётчик | Heavy Grenadiers already understand explosives before they are trained on RPGs and grenade launchers. They send explosive rounds into… |
| `JAZZ_Legion_HeavyT3_Mortarman` | **Mortarman** / Миномётчик | Mortarmen are proven heavy-weapon crews trained to lob shells over walls and other obstacles. They use a portable mortar to strike… |
| `JAZZ_Legion_LeaderT1_Sergeant` | **Sergeant** / Бригадир | When frightened recruits suddenly start moving as one, look for the loudest man among them. The Major turns dependable Legionnaires like… |
| `JAZZ_Legion_LeaderT2_Lieutenant` | **Lieutenant** / Командир | Successful Sergeants become Lieutenants and trade shouting at one group for directing several squads. Their orders reach a wider area,… |
| `JAZZ_Legion_LeaderT3_Captain` | **Captain** / Советник | Captains are officers trusted to control several units at once. They issue orders across the entire Legion force, redirect the attack as… |
| `JAZZ_Legion_LeaderT4_MercenaryCaptain` | **Mercenary Captain** / Мастер | Mercenary Captains are experienced officers hired to command mixed troops; they need little more than local intelligence. They issue… |
| `JAZZ_Legion_Recruit` | **Recruit** / Новобранец | Legion recruiters sweep up villagers and send them out after only a few days of drill. They rush forward with whatever weapon they are… |

## Quest cards

- **Pierre**: Pierre Laurent — Luc Laurent's son serves as the Legion's face on Ernie, always in a pressed uniform and with something to prove. He likes being seen as much as being obeyed,…
- **Bastien**: Bastien — A local fixer with a trader's smile. He knows who controls each road, what passage costs, and whom to pay. A useful contact, but never mistake business for…
- **TheMajor**: The Major — The man behind the Legion built his army with fear, money, and stolen supplies, then spread it across Grand Chien. Every Legion supply report ultimately leads…
- **Legion**: Legion (faction) — The Major's army survives on stolen supplies, forced recruitment, and officers who treat villages as property. Its troops range from frightened locals to…
