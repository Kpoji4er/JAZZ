# Appearance preset generation rules (WIP)

Working contract for building / cloning `AppearancePreset` for JAZZ mercs (JA12, AME, handcraft).  
Visual donor inventory: [`_appearance-donor-visual-catalog.md`](_appearance-donor-visual-catalog.md).  
Existing codegen: `docs/tools/_gen_ja12_appearances.py`, map `ja12-appearance-map.json`.  
AME policy (Af heads, blue accent): [`../ame-appearance-assets.md`](../ame-appearance-assets.md).

Status: **collect correspondences first**; expand recipe rules later.

---

## Hard gates

1. **Male ↔ Female skeletons are incompatible.**  
   Never put female Head/Hair/Hat/Body/Shirt/Pants meshes on a male preset (or reverse).  
   Gender of the *target merc* locks the entire donor pool for that recipe.  
   Audit already treats ♀-on-♂ (and reverse) as hard fail (`Head_Fauda` / `Head_Lami` on male AME, etc.).

2. **Same-gender donors only** when mixing Body from A + Head/Hair/Hat from B.

3. Prefer **faction/NPC/Thug/Civ body + one head donor**.  
   **Do not ship hireables as pure AIM merc clones** (`body=head=Red`, full Sidney, full Len, etc.) — owner veto 2026-08-05.  
   AIM×AIM cross-kits are fragile (neck/collar scale) — warn / avoid.

4. **Vanilla AIM kits are usually non-paintable.**  
   Named AIM `Equipment*` / `Head_*` look is baked; BodyColor/PantsColor/HatColor typically do nothing useful.  
   For recolors / color twins prefer faction/NPC/militia donors (or accept a different *non-clone* kit).

5. Do not invent mesh IDs; only IDs observed in catalog / live `Presets.AppearancePreset` / shipped items.

6. **Read the merc sheet first** (`docs/design/mercs-ja12/<slug>.md` CHARACTER_DESCRIPTION + JA2 face).  
   BigPortrait one-liners in the generator are guesses — sheet ethnicity, kit (спецовка / medic / knife / demo), and «не клон AIM» beat a lazy donor pick.

7. **Verify in-session after every change.** Mutating `AppearancePresets` is not enough if `Unit.Appearance` is stale or `ApplyAppearance` was not run from UnitData. See § Session refresh below.

---

## How we collect

Workflow (owner browse → agent notes):

1. Screenshot: left = look, right = `Entity/Appearance` id in Anim Metadata Editor.
2. Agent dumps non-empty slots from live preset via DAP.
3. Append to [`_appearance-donor-visual-catalog.md`](_appearance-donor-visual-catalog.md) with **gender** (`Male` / `Female`).
4. Later: promote stable donors into generator pools / map recipes.

---

## Gender of known presets (this session + F-batch)

Quick index for recipe lock. Full slots live in the visual catalog.

### Male

Abraham, Adonis_*, Artillery_Rebels*, Barry, Bastien, BellaLover, Biff, BillyBoy, Blood, Bonecrusher, Bounce, Broker, Bulldozer, Butcher, Butler, Butler_Ghost, Captain_Pierrot, Chimurenga, Commander_Rebels, Commando_*, Demolitions_Rebels*, DirtyHenri, DocRobert, Doctor_01, Doctor_02, Doctor_Leevsy (jazz-units), Doorknob, DrFracture, DrQ, Dr_Gruselheim, EraserHead, Faction_Infected_Male_*, Faucheux, Fidel, Flay, FleatownBoss, ForeignMerc_01/02/03, Fournier, FraBaggz, Frederic, Gangster_01 (incomplete), Genessier, GeorgeSenior, Gouvernour, GrandChien_Artillery(+GasMask), GrandChien_Demolition(+GasMask), GrandChien_Heavy, GrandChien_Marksman, GrandChien_Medic, GrandChien_Officer, GrandChien_Recon, GrandChien_Soldier, GrandChien_Stormer, GreasyBasil, Grizzly, Grunty, Gunther, Gus, HeadshotHue, Heavy_Rebels(+_02/_03), Heinrich, Herman, Hitman, HunterHunted_DeadBody_01/02/03_Legion/04_Legion, Hyena, Ice, Igor, IMP_Male_01/02/03, Itsadi, Ivan, Jackhammer, JAZZ_Spouke (jazz-units), KingChicken, Landsbach_SuperSoldier_Assault/Skirmisher/Stormer, Larry, Larry_Addicted, Legion_Artillery(+02/03), Legion_Demolishion(+02/03), Legion_Heavy(+02/03), Legion_Jose, Legion_Marksman(+02/03), Legion_Recon(+02/03), Legion_Shaman(+02/03), Legion_Soldier(+02…06), Legion_Stormer(+02/03), Legion_WitchDoctor(+02/03), Legionraider (=Soldier meshes), LegionButcher*(jazz-units), LegionGoon*(jazz-units), LegionGrenadir*(jazz-units), LegionGunner*(jazz-units), LegionHyenaHandler*(jazz-units), LegionManiac*(jazz-units), LegionMedic*(jazz-units), LegionMortalman_Stronger*(jazz-units; no base in dump), LegionRaidLeader*(jazz-units), LegionRaider*(jazz-units), LegionRanger_Stronger*(jazz-units; no base in dump), LegionRoceteer_Stronger*(jazz-units; spelling Roceteer), LegionScout*(jazz-units), LegionSergant_Stronger*(jazz-units; spelling Sergant), LegionSharpShooter*(jazz-units), LegionSniper*(jazz-units), Len, Luc, LuckiVernard, Luigi, Lurch, MD, Magic, MajorOat, Manny, Mario, Marksman_Rebels(+_02/_03), Medic_Rebels(+_02/_03), MikeDitch, MilitiaRookie_Male_01/02, Militia_Artillery/Demolition/Heavy/Marksman/Medic/Officer/Recon/Soldier/Stormer, MineForeman, Miner_01/02/03, Mole, Molotov, Monday, MrGattz, Nails, Omryn, Pangloom, Pastor, Pierre, Pierre_Steroid, Poacher_01/02, President, Prisoner_01/02/04/06/08 (+DAP siblings 03/05/07), Raider, Raider_01, Reaper, Recon_Rebels(+_02/_03), Red, Referee, Sample_Horatio, VillagerMale_01…20, VillagerMale_Drowned, Weirdo, Wlad, Wolf, WorkingGuy01…04, Xavier, civ_Antoine, civ_Pepe, test_Militia, Ivanov (jazz-units), Barry_Savana / Blood_Savana / DrQ_Jungle / DrQ_Savana / Grizzly_Savana_DustStorm / Grunty_Jungle / Grunty_Savana / Gus_Savana / Hitman_Jungle / Hitman_Savana_DustStorm / Ice_DustStorm / Igor_DustStorm / Ivan_Hot / Larry_Savana_DustStorm / Len_Hot / MD_Jungle / MD_Savana / Magic_DustStorm / Nails_DustStorm / Omryn_DustStorm / Raider_DustStorm / Reaper_DustStorm / Reaper_Jungle / Reaper_Snake / Red_DustStorm / Scully_Forest / Scully_Savana / Sidney_DustStorm / Steroid_DustStorm / Wolf_DustStorm (jazz-units merc skins)

### Female

Baronne, Bella, Buns, Caroline, CorazonSantiago, Deedee, DoctorMangel, Emma, Faction_Infected_Female_*, Fauda, Fox, GangHannah, GangKayla, GangTrudy, GangVinnie, GangWilma, GrandChien_CommanderFemale(+GasMask), Granny, IMP_Female_01/02/03, Justine, Kalyna, Lami, Livewire, MaBaggz, MaBaxter, Maman, Martha, Meltdown, MilitiaRookie_Female_01/02, Mollie, Mouse, MrsGouvernour, Nurse_01/02, Nurse_Hazard_test, Peta, Raven, RebelFemaleSniper(+_1), Reporter, Scope, VillagerFemale_19/20 (+DAP siblings 01–18), Wanda, WorkingGirl01…04, civ_Claudette, civ_Karen, Buns_Savana / Buzz / Fox_Jungle / Fox_Savana_Hot / Kalyna_Hot / Raven_DustStorm / Scope_DustStorm (jazz-units merc skins), Spider (jazz-units named)

---

## Recipe shape (future — not enforced yet)

```text
target_gender: Male|Female   # HARD
body_donor:   <AppearancePreset id>   # same gender
head_donor:   <AppearancePreset id>   # same gender (may equal body)
hair_donor:   optional, usually with head
hat_donor:    optional
notes:        role / colors / avoid war-paint …
```

Generator already uses this shape in `_gen_ja12_appearances.py` RECIPES.

---

## Open / later

- [ ] Formal mesh-prefix gender heuristics (`Female_*`, `Head_F_*`, `EquipmentBuns_*`, …)
- [ ] Color-only variants (same meshes, different HatColor) — mark in catalog
- [ ] Promote high-value donors into JA12/AME pools with evidence
- [ ] Keep catalog ↔ rules in sync when browsing continues

---

## Session append log

| When | Batch |
| --- | --- |
| 2026-08-04 | Abraham → Doorknob; Dr* → Infected; Faucheux → Fox |
| 2026-08-04 | Frederic → Gouvernour (Gang* gender from meshes; Gangster_01 incomplete) |
| 2026-08-04 | GrandChien Army/Faucheux: Artillery…Stormer (+ GasMask / CommanderFemale) |
| 2026-08-04 | Granny → Hitman (Heavy_Rebels color twins; AIM Grizzly/Grunty/Gus/Hitman) |
| 2026-08-04 | HunterHunted DeadBody 01–04_Legion; Hyena; IMP Female/Male 01–03 |
| 2026-08-04 | Ice → Landsbach SuperSoldiers (Assault/Skirmisher/Stormer; AIM Ice/Igor/Ivan/Kalyna) |
| 2026-08-04 | Larry / Larry_Addicted (Clean vs Addicted twins, shared Head_Larry) |
| 2026-08-04 | Vanilla Legion roles: Artillery…WitchDoctor (+ numbered color twins; Demolishion spelling; Legionraider≈Soldier; Jose = civ kit) |
| 2026-08-04 | Len (♂ AIM) + Livewire (♀ AIM); rule: vanilla AIM kits generally non-paintable |
| 2026-08-04 | Luc → Medic_Rebels_03 (AIM MD/Magic; Marksman/Medic_Rebels color twins; Marta/Mollie civ; MajorOat=GrandChien+Elliot) |
| 2026-08-04 | Meltdown + MikeDitch + Militia Rookies + Militia roles Artillery…Stormer (Adonis bottoms; Officer=GrandChien; Soldier Hip=Acc_Heavy) |
| 2026-08-04 | MineForeman → MrsGouvernour (Miners no Head; Mollie≠Maman kits; Molotov Legion hybrid; Mouse AIM) |
| 2026-08-04 | Nails → Peta (AIM Nails/Omryn non-paintable; Nurse_01/02 twins + Hazard_test GasMask/WW2; Pangloom Shaman bracelets Body; Pastor Hat2 earrings; Peta Deedee glasses) |
| 2026-08-04 | Pierre → Scope (Pierre_Steroid no Head; Prisoners mixed kits; RebelFemaleSniper color twins+Vicki+♂ hat; Recon_Rebels Head twins; AIM Raider/Raven/Reaper/Red/Scope; Reporter PRESS Hat2) |
| 2026-08-04 | VillagerFemale_19/20 → test_Militia (VillagerMale_01–20 unique kits not twins; WorkingGirl/Guy families; AIM Wolf; Wlad hybrid; Weirdo Legion; civ_* + Claudette←Vicki; test_Militia skull hat) |
| 2026-08-04 | **jazz-units mod** AppearancePresets (not vanilla donors): Doctor_Leevsy, JAZZ_Spouke, LegionButcher/Goon/Grenadir/Gunner/HyenaHandler + Maniac through Stronger_alt (47 unique; Medic/Mortalman/RaidLeader + remaining Maniac alts unbrowsed) |
| 2026-08-05 | **jazz-units mod batch4:** remaining Maniac alts + Medic* + Mortalman_Stronger* + RaidLeader* + Raider base (24 unique; Raider_Stronger / Ranger / Roceteer still unbrowsed) |
| 2026-08-05 | **jazz-units mod batch5:** Raider_Stronger* + alt* + Ranger_Stronger* + Roceteer_Stronger* + Scout through Stronger_alt (24 unique; Scout remaining alts + Sergant/SharpShooter unbrowsed; spellings Roceteer/Sergant) |
| 2026-08-05 | **jazz-units mod batch6:** Scout remainder + Sergant_Stronger* + SharpShooter* + Sniper* + Ivanov + Barry_Savana (24 unique; Legion* ModItem wave complete; further Mercs *_Savana/*_Jungle unbrowsed) |
| 2026-08-05 | **jazz-units merc skins batch7:** Blood_Savana → Omryn_DustStorm (24 unique; ♀ Buns_Savana/Buzz/Fox_Jungle/Fox_Savana_Hot/Kalyna_Hot; Buzz = Fauda+Livewire hybrid) |
| 2026-08-05 | **jazz-units merc skins batch8:** Raider_DustStorm → Wolf_DustStorm + Spider (13 unique; ♀ Raven_DustStorm/Scope_DustStorm/Spider; skipped vanilla Red/Scully headers + Discord shots) |
| 2026-08-05 | **JA12 appearances BigPortrait pass:** regenerated non-handcrafted JA12 presets via `_gen_ja12_appearances.py`; KEEP Lynx/Buzz/Spider/JAZZ_Spouke (+ vanilla Biff/Hitman/Simon→Shadow/Ivanov); Mike/Horg generated |
| 2026-08-05 | **JA12 live playtest fixes:** Vince PantsColor brown; Manuel Hair≠Chimurenga (under-helm); Quinten=Steroid body+Adonis medic Chest/Hip (Adonis_Top+Steroid clipped); Meat=Grizzly+Raider hair (Bulldozer skin mismatch; Grizzly hair under-beret). Gotchas § below. |

---

## Gotchas / known pitfalls (live playtest)

Append here when a recipe looks wrong in-game. Do not re-learn the hard way.

### Under-helmet / under-beret hair (bald crown if Hat empty)

These Hair meshes are cut for headgear. **Without** matching Hat they show a bald top + side ring.

| Hair / donor | Looks like | Fix |
| --- | --- | --- |
| `EquipmentChimurenga_Hair` (Chimurenga) | Bald crown + side hair / headband | Give Chimurenga Hat (beret), or swap Hair (e.g. Raider). **Manuel** → Hair=Raider. Miguel keeps Chimurenga+Hat. |
| `EquipmentGrizzly_Hair` (Grizzly) | Bald cap + sideburns/beard under beret | Give `EquipmentGrizzly_Hat`, or swap Hair. **Meat** → Hair=Raider, no hat. |
| `EquipmentNails_Hair` (Nails) | Long hair clipped for paisley headband | Keep `EquipmentNails_Headband`, or clear Hair. **Madman** → Hair="" (was clip through face). |
| `EquipmentBuns_Hair_Hat` | Catalog: short under helmet | Only with hat / female hat kits |

When browsing donors, mark Hair as **under-hat** in the visual catalog if the top is open.

### Skin / BodyColor mismatch (head ≠ torso)

Faction/NPC `Body` often carries dark `BodyColor.EditableColor1` (skin channel on the top). AIM named heads are their own tone. Mixing without checking → sharp neck line.

| Bad combo | Symptom | Fix |
| --- | --- | --- |
| Bulldozer (`Faction_Legion_Top_09`, dark BC1) + `Head_Grizzly` | Pale head / dark torso | Prefer **same-tone body**/faction kit — **not** a full AIM hireable clone. **Meat** → Grizzly body+head. |
| **Bonecrusher** (dark `NPCBonecrusher_Top_01`) | Dark shirtless torso — wrong if sheet/owner wants **white** bruiser | **Bull** → Steroid pale body+head, Hair="", pants from Bonecrusher. Do not leave Bull on Bonecrusher. |
| `ThugMelee` / other `Male_Body_01` civ thugs (dark BC1) + pale AIM head | Pale head / dark arms | Same. **Blade** was Reaper on ThugMelee — → GrandChien_Recon + Reaper. **Vicious** → Ivan leather (not Hitman on Thug). |
| **Female_Body_01** (RebelFemaleSniper etc., BC1 ≈ black) + pale AIM ♀ head | Pale face / dark arms-neck | Prefer pale AIM body (Livewire/Fox). **Forced pale BC1 `(205,165,135)` → solid white arms** — Flo/Ira/Laura. **Ira**→Livewire+Fox; **Laura**→Livewire+medic; **Flo**→Livewire+Buns. |
| **Faction_Adonis_Top_05** (Officer) **C1=skin**, C2=plate | Olive/black on C1 paints **hands/arms** | Recolor plate via **C2/C3/pants** only unless head matches that skin. **Conrad** olive-on-C1 → green hands. |
| **Mario / MilitiaCostume shirts** C1=skin | Painting overalls color on C1 | **Cord**: pale C1 + khaki C2. **Allik**: pale C1 + Sidney. **Dynamo**: dark C1 + Blood. |
| **Bonecrusher** + pale Hitman/Steroid head | Pale head / dark shirtless torso | Do not mix. **Horg** → Adonis_Heavy + Hitman + cigar. **Bull** (white) → Steroid body+head, not Bonecrusher. |
| Any dark Legion/NPC top + pale AIM head | Same | Match ethnicity/tone; **never** “fix” by cloning a full AIM hireable kit |

Sheet ethnicity beats BigPortrait jacket guess when they conflict.

### Collar / shoulder clip (body peeking through clothes)

Thick AIM necks on slim faction tops leave flesh at the yoke.

| Bad combo | Symptom | Fix |
| --- | --- | --- |
| `Faction_Adonis_Top_*` + `Head_Steroid` | Skin through collar/shoulder | Use **Steroid body** + graft medic gear (`chest`/`hip` from Adonis_Medic). **Quinten/Danny**. |
| AIM×AIM cross body/head | Neck/collar scale weird | Prefer faction body + one head (generator WARNs); never “fix” with full AIM clone |

### Banned / trap body donors (JA12 hireables)

| Donor | Why bad | Instead |
| --- | --- | --- |
| `WorkingGuy01`–`04` | Magenta/pink shirt + red pants; leg artifacts | Faction/NPC workwear; **Cord** → Mario overalls; never WG |
| `WorkingGirl01`/`04` (Mollie purple+pink) | Looks like carnival dress, not merc | **Grace**→Meltdown; **Ira/Flo**→RebelFemale (+pale BC1). Ban Mollie top for hireables |
| Pure AIM clone of hireable twin | Owner: «не делай клонов мерков» | Faction body + head/hair only from AIM. **Static** was pure Thor → GreasyBasil + Thor head/hair + welder hat |
| `Tex` head for Latino/Arulco | JA3 Tex is Asian; Hair often empty | **Carlos/Gamos** → Blood |
| `LuckiVernard` bomber for khaki security | Jacket paints blue-grey on preview | **Rothman** → Sidney top (holster) + NPC pants brown |
| `Adonis_Officer` without recolor | Donor C2 pale cyan plate | **Mike** black C2/C3/pants (+ dark C1 OK with Raider). **Conrad**: never put olive on **C1** — Top_05 **C1=skin**, C2=plate → olive C1 = green hands; use pale C1 + olive C2 |
| `Militia_*` `Faction_Militia_Top_02` + dark AIM head | **Pale baked arm skin** — `body_color*` recolors tee/accents, not arms | Do **not** pair with `Head_Blood` etc. **Dimitri** → `Soldier_Rebels_03` + Blood |
| Sidney / other AIM bottoms + `pants_color` | Non-paintable — color ignored | Graft `pants` from NPC/faction (**Allik** DirtyHenri; **Rothman** LuckiVernard pants) |

### Session refresh (DAP / live playtest) — do this every batch

Disk `items.lua` does **not** update spawned units by itself.

1. After recipe regen + validate: mutate live `AppearancePresets.<Id>` **or** rely on already-written disk only after **mod reload + sector re-enter**.
2. Hot-apply all hireables on map (reliable pattern):

```lua
for _, u in ipairs(g_Units or empty_table) do
  local sid = tostring(u.session_id or "")
  if sid:find("Jazz_") then
    local preset
    local def = UnitDataDefs and UnitDataDefs[u.unitdatadef_id]
    if def and def.AppearancesList then
      for _, e in ipairs(def.AppearancesList) do
        if e.Preset and AppearancePresets[e.Preset] then preset = e.Preset break end
      end
    end
    preset = preset or sid:match("Jazz_(.+)")
    if preset and AppearancePresets[preset] then
      u.Appearance = preset
      u:ApplyAppearance(preset)
    end
  end
end
```

3. Do **not** claim “applied” from mutating the preset alone. Confirm `u.Appearance` + visible mesh, or ask owner to screenshot.
4. If DAP Apply still looks stale: mod reload → leave sector → re-enter (or restart JA3Debug).
5. Never leave `Unit.Appearance = false` after experiments.

### Playtest process (do better next time)

Failures this pass (2026-08-05): guessed BigPortrait kits without sheet; shipped AIM clones; WorkingGirl/WorkingGuy garbage; skin mismatches; colors left at donor defaults; said “уже в сессии” when unit refresh was incomplete.

**Next playtest batch:**

1. Open sheet (`CHARACTER_DESCRIPTION` + face ref) **before** picking body.
2. Check donor catalog for skin tone, under-hat hair, paintability, ethnicity (Tex≠Latino).
3. Prefer one faction/NPC body + one head; graft `chest`/`hip`/`pants`/`hat_mesh` as needed.
4. If note promises a color (olive / black / brown / burnt-orange) — set `body_color*` / `pants_color` / `shirt_color` in the **same** recipe, not “later”.
5. Regen `--only Id` → `_validate_items_quick.py` on `jazz-units` → DAP preset patch **and** UnitData-based Apply refresh (§ above).
6. One merc per owner screenshot when possible; don’t batch-claim success.
7. Append new gotchas here the same turn.

### Recolor overrides

Vanilla AIM kits are mostly non-paintable. Faction/NPC colors work:

| Recipe key | Sets | Example |
| --- | --- | --- |
| `pants_color` | `PantsColor.EditableColor1` | **Vince** / **Highball** brown `(102,68,38)` on Pants_04; **Conrad** olive |
| `shirt_color` | `ShirtColor.EditableColor1` | **Gamos** burnt-orange on Poacher shirt |
| `hat_color` | `HatColor.EditableColor1` | **Biggens** khaki beret; **Henning** black beret |
| `body_color1/2/3` | `BodyColor.EditableColor{n}` | Know channel meaning first. Adonis_Top_05: C1 skin / C2 plate. Mario shirt: C1 skin / C2 fabric. **Never** put garment color on skin channel. |
| `hat_mesh` | `Hat` string override | **Horg** `EquipmentFidel_Cigar` after `hat: ""` |
| `pants` / `chest` / `hip` | mesh + ColorizationPropSet graft | **Rothman** NPC pants; **Quinten/Highball/Ira/Laura** Adonis medic |

Full regen wipes hand-tuned colors unless these keys (or KEEP_HANDCRAFTED) preserve them.

### Face camo heads

| Head / donor | Notes |
| --- | --- |
| `Head_M_Ca_NPC_Camo_01` (GrandChien_Recon, Adonis_Recon) | Explicit face paint — only when wanted (Monk). |
| `Head_Shadow` | JA3 Shadow has **baked face camo**. **Vilde** → Raider. **Simon** must not use `AppearancesList → Shadow` (face/arm camo bleed) — own preset: Shadow body + Raider head. |
| Vanilla **Hitman** pink AIM kit | Flashy pink shirt + aviators — not sheet «inconspicuous hoodie». **Jazz_Hitman / Убийца** → Ice jacket + Hitman face (own ModItem `Hitman`). Do not leave UnitData aliased to flashy AIM clone only. |
| **Tex** | Asian face in JA3; Hair often `""`. Not for Arulco Latino (**Carlos**, **Gamos** → Blood). |

### Mustache donors (Caucasian)

| Donor | Where is the mustache | Notes |
| --- | --- | --- |
| **Hitman** | `EquipmentHitman_Hair` (+ face) | Best swap for Russian/officer kits. Clear Hat (aviators) unless wanted. |
| **IMP_Male_03** | `IMP_male03_Hair` | Slicked + mustache; NPC head `Head_M_As_NPC_04` |
| **Pierre** | Baked into `Head_Pierre` | Hair empty; usually with bandana |
| **Igor** | — | **Clean-shaven in JA3** despite JA2 mustache lore. **Grom** → Hitman head/hair on Igor body. |

### WorkingGuy / WorkingGirl kits

`WorkingGuy01`–`04` — magenta/pink + red pants; leg artifacts with AIM heads. **Banned** as JA12 body donors.  
`WorkingGirl01`/`04` — purple Mollie tunic + pink skirt. **Banned** for hireables (same carnival look).  

Purged WG/WGirl wave: Colby→Barry, Static→Thor, Kulba→Gus, Cord→Mario+Sidney, Allik→DirtyHenri+Sidney, Hobbit→Barry, Nervous→Tex, Grace→Meltdown+Buns, Ira/Flo→RebelFemale+Fox/Buns, Rothman→Sidney+NPC pants, Horg→Adonis_Heavy (not Bonecrusher), Bull→Steroid pale + Bonecrusher pants (owner: white, not Bonecrusher dark).

---

| 2026-08-05 | **JA12 live playtest wave2:** no AIM hireable clones; ban WorkingGirl Mollie; skin-match Bonecrusher/Female_Body/ThugMelee; force Adonis_Officer/Militia colors; UnitData Apply refresh required; gotchas + process § updated after owner feedback «плохо сделал». |