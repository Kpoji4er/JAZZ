# African Mercenary Exchange (AME)

Design companion for [`JAZZ-UNITS-005`](../specs/active/JAZZ-UNITS-005.md). Normative ranges live in the spec; this page is the human-readable mirror for design/implement.

## Fantasy

| Market | Sells |
| --- | --- |
| **AIM** | Ready professionals (brand, perks, kit, voice) |
| **AME** | Local fighters — cheap because they lack name/reputation, not because of ethnicity. Growth is the product. |

Background flavor (bio tags): ex-army, militia, police, hunter, rebel. Legion is a competitor for the same labor pool (market Away reason `JoinedLegion`), not the player’s branded clone.

Short bio per slot + varied origins: **mostly Africa**, with a solid share from **Grand Chien** (vanilla setting), plus other African backgrounds.

## PDA site

- Browser mode id: `ame`
- Org / Affiliation: `AME`
- UnitData slots: `JAZZ_AME_01` … `JAZZ_AME_60`
- UI class: subclass of `PDAAIMBrowser` + separate XTemplate skin
- Hire pipeline: vanilla chat / `HireMerc` (no custom messenger)

### Logo (draft)

- Core mark: **black Africa continent** on tactical tan/khaki patch
- African origin accent (not Russian PMC refs): assegai + ishlangu / geometric shield — no bear, no MoD star, no “African Corps” copy
- Concept (preferred): `docs/design/_ame-logo/ame-logo-concept-v4.png` — чистый щит, Африка + ishlangu/assegai, honeycomb. `v5` отложен (артефакты по контуру/тексту). Older: v1–v3, v4b.
- Final PDA chrome / tab icon still open (RU motto vs EN “AME” / bilingual)

## Categories

| id | EN | RU | Legion anchor |
| --- | --- | --- | --- |
| Irregulars | Irregulars | Новобранцы | below T1 / Recruit− |
| Fighters | Fighters | Бойцы | T1 |
| Hardened | Hardened | Закалённые | T2–T3 line |
| Specialists | Specialists | Специалисты | role peak |

Specialist roles: Medic, Instructor (`Teacher`), Sniper, Sapper, Mechanic — **одна вкладка Specialists** (без подтабов по роли).

Full design cards (all 60): [`ame-roster-60.md`](ame-roster-60.md). Fixed inventory per slot. **Kit caps:** Irregulars ≤ **1-2**; Fighters ≤ **1-3**; Hardened/Specialists ≤ **2-1** (no T2-2+). **`Type56` = AR ceiling, Hardened only.** **`SKS` + T1 bolt = Snipers only.** **Bandages:** Fighters ~40%; Hardened always. **Sappers:** some `PipeBomb`. **Bios:** full in-game hire-card prose (not design stubs).

### Fighters / Hardened combat mix

Inside Fighters + Hardened (not the Specialists filter), a share of slots are:

| CombatRole | Typical traits (common only, no signatures) |
| --- | --- |
| Rifle / general | 0–1 common |
| Autorifleman | often `AutoWeapons` |
| Machinegunner | often `HeavyWeaponsTraining` / `AutoWeapons` |
| Grenadier | often `Throwing` / `HeavyWeaponsTraining` |

Target: at least ~30% of Fighters+Hardened slots are Autorifleman / Machinegunner / Grenadier.

### Soft-skill sparsity (line troops)

| Skill | Rule |
| --- | --- |
| Leadership | usually low; **1–2** Fighters/Hardened in the whole pool at **≈50** |
| Mechanical | usually **~0**; **1–2** in Fighters+Hardened at **≈30**; Irregulars ~0 with rare exceptions |
| Explosives | Irregulars ~0 (rare exceptions); Fighters usually ~0, **2** at **≈30**; Hardened usually **10–20**, **2** at **30–40** |

## Pool and living market

- Pool size: **60**
- Hireable Available on shelf: **14–16** (target ~15)
- **Shop visibility:**
  - show: current **Available**
  - show (disabled): already unhireable — at least **JoinedLegion** and **Killed** (grayed card + reason)
  - show: player’s **Hired** (My Team)
  - hide: **NotListed** (not yet appeared) — never preview future mercs
- Tick: every **30** campaign days (deterministic)
- Terminal reasons (stay visible, no hire): JoinedLegion, Killed (+ HiredElsewhere if treated as terminal)
- Specialist soft-guarantee: Medic / Instructor / Sniper cannot stay at zero Available+Pending for more than 30 days

### Specialist floor (in pool)

| Role | Count |
| --- | ---: |
| Medic | 2–3 |
| Instructor | 2–3 |
| Sniper | 2 |
| Sapper | 1–2 |

## Salary ladder (StartingSalary orient)

`Irregulars < Fighters < Hardened ≪ Specialists` (Specialists = max on AME, still below comparable AIM).

| Band | $ |
| --- | --- |
| Irregulars | 80–150 |
| Fighters | 150–300 |
| Hardened | 350–600 |
| Sapper / Sniper | 600–900 |
| Medic | 700–1100 |
| Instructor | 900–1400 |

## Stats

See `JAZZ-UNITS-005-REQ-016` for full tables.

**Will:** low (20–40) for Irregulars, Fighters, and all Specialists; medium (45–65) only for Hardened (veterans).

**Agi / Dex / Marks ladder:** category medians **≈60 / 65 / 70** (Irregulars / Fighters / Hardened). Pool Agi/Dex ceiling **70**. **Health and Strength** may deviate more widely than the combat triad. Perk tax on strong combat combos lowers Marks below category median.

Summary peaks:

| Category | Peak | Marks | Wisdom |
| --- | --- | ---: | ---: |
| Irregulars | growth / high HP | **медиана ≈60** | high |
| Fighters | T1 kit | **медиана ≈65** | mid |
| Hardened | kit/Will | **медиана ≈70 / потолок 70** | mid-low |
| Medic | Medical **потолок 70** | ~32–36 | mid-high |
| Instructor | Lead + Teacher | ~42–48 | high |
| Sniper | only above Hardened ceiling | **71–80** | mid |
| Sapper | Explosives **потолок <70** | ~34–36 | mid |
| Mechanic | Mechanical peak | ~32–34 | mid |

Potential UI label from Wisdom: Low (below 45), Medium (45–64), High (65+).

## Names / bio / nationality

- **Names:** African first/last (or single given name) from AME pools (Legion/Rebels-style, not AIM US/EU roster)
- **Nick:** rare. Mostly on **Hardened** (~15–30% of Hardened); almost never on Irregulars / Fighters / Specialists
- Full hire-card `Bio` RU/EN (prose, 3rd person; origin / past / character / weakness; no stats, tiers, marketplace/UI meta)
- Origins mostly African; **~20–35%** Grand Chien locals
- **New Nationalities + flags are in scope** (JAZZ-owned, no workshop nationality-lib dependency):
  - Reuse vanilla: `GrandChien`, `SouthAfrica`
  - New v1 ids (each with RU/EN name + flag asset for `MercFlagImage`): `Nigeria`, `Kenya`, `Angola`, `Mali`, `Congo`, `Ghana`, `Senegal`, `Ethiopia`

## Voice / look

- Male Irregulars / Fighters: `LegionRaider` (+ optional `-1.opus` alt takes)
- Male Hardened / Specialists: `ArmySoldier`
- **Female slots:** `VoiceResponseId = "AnneLeMitrailleur"` (Anne la Mitrailleuse — existing rebel/army female donor; also used by `RebelSniper_female`, `ArmyCommanderFemale`)
- Appearance sources: **Rebels** / **Militia** / **Legion** — clone to AME ids; **per-slot donor** listed on [`ame-roster-60.md`](ame-roster-60.md) as `Appearance (donor)`
- Female looks (thin bank): `RebelFemaleSniper` (`AnneLeMitrailleur`), `GrandChien_CommanderFemale` (`ArmyCommanderFemale`)
- Recolor: **blue-dominant** uniform (`ColorizationPropSet` on clothes); do not edit source faction presets; keep skin/metal/leather natural
- Machinegunners: only T1 LMGs (`MAC2429`, `BAR`) — `RPK`/`RPK74` are T2, forbidden on AME
- Portraits: shared bank ≥16 faces

## Out of v1

- EE / LatAm markets (API-shaped only)
- Unique personal perks per slot
- Quest lock on first open
- New recorded voice banks
