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
- Hire card **Loadout**: shows Equipment / Backpack only — **no Traits/Perks strip** (AIM keeps Perks)
- Hire pipeline: vanilla chat / `HireMerc` (no custom messenger)

### Logo (draft)

- Core mark: **black Africa continent** on tactical tan/khaki patch
- African origin accent (not Russian PMC refs): assegai + ishlangu / geometric shield — no bear, no MoD star, no “African Corps” copy
- Concept (preferred): `docs/design/_ame-logo/ame-logo-concept-v4.png` — чистый щит, Африка + ishlangu/assegai, honeycomb. `v5` отложен (артефакты по контуру/тексту). Older: v1–v3, v4b.
- **PDA chrome (shipped):** savannah/ochre tint on panels; HazOS → `Icons/PDA/AME_Mark.png` (v4); AIM banner → `Icons/PDA/AME_BannerPad.png`; backdrop `Icons/PDA/AME_PdaBackdrop.png`. Source skin: `Code/System_AME_Browser_Template.lua` → `_install_ame_xtemplate_moditem.py`.

## Categories

| id | EN | RU | Legion anchor |
| --- | --- | --- | --- |
| Irregulars | Irregulars | Новобранцы | below T1 / Recruit− |
| Fighters | Fighters | Бойцы | T1 |
| Hardened | Hardened | Закалённые | T2–T3 line |
| Specialists | Specialists | Специалисты | role peak |

Specialist roles: Medic, Instructor (`Teacher`), Sniper, Sapper, Mechanic — **одна вкладка Specialists** (без подтабов по роли).

Full design cards (all 60): [`ame-roster-60.md`](ame-roster-60.md). Fixed inventory per slot. **Kit caps:** Irregulars ≤ **1-2**; Fighters ≤ **1-3**; Hardened/Specialists ≤ **2-1** (no T2-2+). **`Type56` = AR ceiling, Hardened only.** **`SKS` + T1 bolt = Snipers only.** **SMGs:** vintage T1 (`Thompson`, `M3GreaseGun`, `PPS43`, `PPSH`, …) — no starting `UZI`. **Bandages:** Fighters ~40%; Hardened always. **Sappers:** some `PipeBomb`. **Bios:** full in-game hire-card prose (not design stubs).

### Fighters / Hardened combat mix

Inside Fighters + Hardened (not the Specialists filter), a share of slots are:

| CombatRole | Specialization icon | Typical traits (common only, no signatures) |
| --- | --- | --- |
| Rifle / general | `Marksmen` / `AllRounder` | 0–1 common |
| Autorifleman | `Autoriflemen` | often `AutoWeapons` |
| Machinegunner | `HeavyWeapons` | often `HeavyWeaponsTraining` / `AutoWeapons` |
| Grenadier | `HeavyWeapons` | often `Throwing` / `HeavyWeaponsTraining` |

Line-troop Specialization icons are **only** that quartet. Soft roles `Doctor` / `Mechanic` / `ExplosiveExpert` / `Leader` appear **only** on Specialists (Medic / Mechanic / Sapper / Instructor). Sniper specialists use `Marksmen`.

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
- Tick: every **14** campaign days / 2 weeks (deterministic; was 30)
- Terminal reasons (stay visible, no hire): JoinedLegion, Killed (+ HiredElsewhere if treated as terminal)
- Specialist soft-guarantee: Medic / Instructor / Sniper cannot stay at zero Available+Pending across a tick cycle (~14 days)
- **Mail ([`JAZZ-UI-AME-001`](../specs/active/JAZZ-UI-AME-001.md)):** welcome Email from AME on init (explains the exchange + **sales pitches** for current Available); listing-update Email after a real tick change; PDA tab `ame` **always open** (mail is not a gate). Not R.I.S.

### Specialist floor (in pool)

| Role | Count |
| --- | ---: |
| Medic | 2–3 |
| Instructor | 2–3 |
| Sniper | 2 |
| Sapper | 1–2 |

## Salary ladder (owner weekly bands, 2026-08-05)

JA3 hire week ≈ `StartingSalary × 7`. Ladder: `Irregulars < Fighters < Hardened ≪ Specialists`. Specialists stay **below** Igor/Barry weekly (`$3150` / `$3290`).

| Band | ≈ $/week | `StartingSalary` (daily) |
| --- | ---: | ---: |
| Floor (cheap Irregulars) | ~50 | ~7 |
| Irregulars | 50–350 | 7–50 |
| Fighters | 400–750 | 57–107 |
| Hardened (non-spec max) | 750–1000 | 107–143 |
| Specialists | 1100–2000 | 157–286 |

`JAZZ-UNITS-005-REQ-014` matches this ladder (older 80–1400 daily bands superseded).

## Stats

See `JAZZ-UNITS-005-REQ-016` for full tables.

**Will:** low (20–40) for Irregulars, Fighters, and all Specialists; medium (45–65) only for Hardened (veterans).

**Agi / Dex / Marks ladder:** category Marks medians **≈45 / 55 / 60** (Irregulars / Fighters / Hardened); Agi/Dex still **≈60 / 65 / 70**. Pool Agi/Dex ceiling **70**. **Health and Strength** may deviate more widely than the combat triad. Perk tax on strong combat combos lowers Marks below category median.

Summary peaks:

| Category | Peak | Marks | Wisdom |
| --- | --- | ---: | ---: |
| Irregulars | growth / high HP | **медиана ≈45** | high |
| Fighters | T1 kit | **медиана ≈55** | mid |
| Hardened | kit/Will | **медиана ≈60 / потолок ≈60** | mid-low |
| Medic | Medical **потолок 70** | ~22–26 | mid-high |
| Instructor | Lead **потолок 70** + Teacher | ~32–38 | high |
| Sniper | only above Hardened ceiling | **≈68–70** | mid |
| Sapper | Explosives **потолок <70** | ~24–26 | mid |
| Mechanic | Mechanical **потолок 70** | ~22–24 | mid |

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

Voice pool (Jazz remesh majority + local hireable + small IMP minority):

- ~7/8 slots → Jazz remesh (`Jazz_AME_Male_Low` / `Male_Hard` / `Female`) or `PierreMerc` (African hireable bank with full Selection/Order)
- ~1/8 → IMP pool (`IMP_male_01..03` / `IMP_female_01..03`; VR resolves to `IMP_male_01` / `IMP_female_01`)
- Bucket `(slot-1)%8`: `7` → IMP; `3` → `PierreMerc` (males); else Jazz remesh. Hardened/Specialists and odd buckets prefer `Male_Hard`.
- `FallbackMissingVR`: IMP/`PierreMerc` → same VR; remesh → `LegionRaider` / `ArmySoldier` / `AnneLeMitrailleur` (**not** Ice/Fox). Empty Selection/Move on remesh → silence.
- Heads: safe Af bank only (see [`ame-appearance-assets.md`](ame-appearance-assets.md)); **no** Flay/Fidel/Magic/Blood/Fauda/Omryn; **no** `Faction_Legion_Head_*` war-paint
- Tooling: `_import_legion_raider_alt_voices.py` + `_gen_ame_voice_responses.py` + `_gen_ame_appearances.py` + `_audit_patch_ame_heads.py` + `_apply_ame_voice_remap.py`; assignment in `_gen_ame_roster_60.py`
- Appearance sources: **unique clone per slot** `JAZZ_AME_NN` from **Rebels** / **Militia** / **Legion** (Hardened/Specialists may use **GrandChien**); map [`ame-appearance-map.json`](ame-appearance-map.json); asset policy [`ame-appearance-assets.md`](ame-appearance-assets.md)
- Recolor: **red cloth → blue** (`ColorizationPropSet`); **BodyColor C1** dark African bank; **HeadColor** black (never skin-tint heads); do not edit source faction presets
- Female looks: thin faction female bank (`RebelFemaleSniper`×2, `GrandChien_CommanderFemale`, MilitiaRookie female×2) — unique ModItems even when donor mesh repeats
- Machinegunners: only T1 LMGs (`MAC2429`, `BAR`) — `RPK`/`RPK74` are T2, forbidden on AME
- Portraits: unique per slot `MercPortraits/JAZZ_AME_NN`

## Out of v1

- EE / LatAm markets (API-shaped only)
- Unique personal perks per slot
- Quest lock on first open
- Neural re-record of voice banks (v1 = remesh + Legion alt pack)
