# `docs/tools` — скрипты агентов и аудита

Рабочие утилиты для generated data, аттачей, CSV и design-артефактов.  
Политика хранения: `.agents/docs/reference/agent-tooling.md`, `.cursor/rules/jazz-agent-tooling.mdc`.

Запуск из корня пакета `jazz/` (если не указано иное).

| `_audit_ai_mobile_shot.py` | Count `AIActionMobileShot` in `jazz-units/items.lua`: `action_id` / BiasId / RequiredKeywords + jazz action mentions. |
| `_audit_ai_rng_wiring.py` | Brace-aware RunAndGun wiring audit: real vs default MobileShot, keyword gates, `AIAttackSingleTarget` action_ids. |
| `_apply_bandage_cumulative_loc.py` | MED-001: update `890000000010013` / `010021` RU+EN for cumulative field bandage (1 bandage × bleed stack). |
| `_apply_mobile_action_damage_ui.py` | Fix AimType=mobile `GetActionDamage` (RnG/Carbine/SMGStorm/ManeuverAR/MobileShot) + RnG `GetActionResults` num_shots; uses `Jazz_GetMobileActionDamage` in `Code/CombatActions.lua`. |
| `_normalize_ernie_flare_carriers.py` | Set Ernie island `Min/MaxFlareCarriers` to 12/15 in `jazz-maps/items.lua` (ModItemSector + HotDiamonds SatelliteSector). |
| `_probe_autofire_attacks.py` | List `InventoryItem/*.lua` whose `AvailableAttacks` have jazz autofire aliases (`AbakanAutoFire` / `JAZZ_LargeAutoFire` / …) but not vanilla `AutoFire`/`MGBurstFire` (BulletHell gate audit). |
| `_check_bullethell_autofire_gate.py` | Static: `JazzWrapBulletHellAutofireGate` present; AN94 keeps `AbakanAutoFire` without vanilla `AutoFire`. |
| `_check_bullethell_projectiles.py` | Static COMBAT-006 v2: `FirearmAttack` + cone-arc projectiles (`jazz_bh_arc_sprayed`, `AlwaysHits=false`); no SingleShot dump. |
| `_fix_zastava_m92_csv.py` | WEAPONS-003 hotfix: `ZastavaM92` `burst_shots=4` `auto_shots=7` `cyclic_rpm=700` in `weapons.csv`. |
| `_scan_saves_broken_placecharacterffect.py` | Scan JA3 `.sav` under Saved Games: extract zstd `game_session`, count `PlaceCharacterEffect('Id', )` (empty props — load-breaking). |
| `_extract_ja3_game_session.py` | Extract concatenated zstd frames of `game_session` from BPUL `.sav` to `.lua` for syntax debug. |
| `_audit_ame_appearance_clothes_qa.py` | AME appearance clothes QA vs appearance-map (bank/channel checks). |
| `_audit_ame_hat_not_blue.py` | Flag AME hats that violate no-blue accent policy. |
| `_patch_ame_appearance_clothes_from_map.py` | Apply clothes fields from `ame-appearance-map.json` into generated appearance data. |
| `_export_ammo_stats.py` | Parse `InventoryItem/JAZZ_AMMO_*.lua` → `Ammopics/_gen/ammo_stats.json` + `.csv` (pen/dmg/jam/crit/BR). |
| `_gen_ammo_stats_canvas.py` | Rebuild `canvases/ammo-stats.canvas.tsx` from `ammo_stats_compact.json`. |
| `_normalize_ammo_icon_bbox.py` | Crop near-black, fit ammo-box content into fixed `fit_w`×`fit_h` on 110×110 black canvas (series size lock). |
| `_lock_ammo_icon_silhouette.py` | Silhouette lock per caliber. Cut: `--key auto\|magenta\|black\|alpha`, `--choke` after downscale, `--alpha-from draft\|sil`, `--thr`, `--hard-alpha`. Soft edge: `--soft-outline 0.45` / `--outline-only`. Prefer **magenta plate** gens. |
| `_finalize_ammo_gen_batch.py` | Batch: lock Cursor `assets/gen_*.png` → `Ammopics/_gen` + soft outline + `--key` + optional `--purge-assets` (only listed files). |
| `_paint_ammo_carton_family.py` | EXPERIMENT only — paint onto blank plate. Visual QA rejected for 9×18 (looks procedural). Prefer GenerateImage + `_lock_ammo_icon_silhouette.py`. |
| `_list_jazz_helms.py` | List `JazzArmor_*` Head-slot items (id/DisplayName/comment) for JAZZ-APPEAR-001 mapping. |
| `_list_jazz_legion_appearances.py` | List Jazz Legion appearance IDs for portrait tooling. |
| `_scan_ame_hats.py` / `_dump_ame17.py` | Hat scan / AME-17 dump helpers for appearance audits. |
| `_bump_metadata_revision.py` | `metadata.lua` Revision +1 + prepend `last_changes` bullet (`--bullet`, escape `\\n` only). |
| `_diff_list2_sheet.py` (alias `_tmp_diff_list2_sheet.py`) | Diff Google Sheet Лист2 perk cols (fresh TSV export vs prior WebFetch) for JAZZ-UNITS-006. |
| `_apply_units006_batch1_items_loc.py` | UNITS-006 §A batch1: sync `items.lua` ModItem CE from companions + `Jazz_OrderAP`/`Jazz_CombatMedicBuff`, metadata.code, RU/EN CSV for touched perk/status IDs. |
| `_apply_units006_batch1_hooks.py` | UNITS-006 batch1: register `System_NamedPerks_006` in metadata.code; Vince skip-consume wrap in `Systems_Medicine.lua`. |
| `_apply_units006_batch2_items_loc.py` | UNITS-006 §C batch2: sync vanilla personal CE companions (`GruntyPerk_JAZZ`, `GrizzlyPerk`, Ivan/Gus/Nails/Wolf/Magic/Scully/Steroid/Ice), metadata.code, RU/EN CSV (`6500+` + Grizzly/Grunty desc). Refuses VoiceResponse overwrite. |
| `_apply_steroidpunch_passive.py` | UNITS-006 SteroidPunch: sync companion → `items.lua` + RU/EN `890000000009930/9931` (passive text). Restores Gamos VR `6512/6513` if overwritten. |
| `_units006_namedperks_notes.md` | UNITS-006 batch2: shipped effects + soft cuts (Ice deferred, Wolf ops wrap scope). |
| `_gen_units006_batch3.py` | UNITS-006 §C batch3: generate signature CE companions + items/metadata/loc (`9861+`). |
| `_audit_jazz_perk_combat_actions.py` | Audit `Jazz_Perk_*` CE vs `ModItemCombatAction` SignatureAbilities companions; flags missing CA and `GetUIState→hidden` stubs. |
| `_gen_jazz_perk_passive_combat_actions.py` | Generate/fix Passive `SignatureAbilities` CombatAction companions for `Jazz_Perk_*` (skip `00` Toggle + OfficerAuraInfluence); sync metadata presets. Prefer `Perks/SignatureAbilities/<id>.png` for CA Icon when present. |
| `_build_jazz_perk_sig_icons_from_personal.py` | Build 108×54 dual-strip HUD icons for Lynx/Buzz/Spider/Colby Passive CAs from `Perks/Personal/*.png` (key black bg → transparent); wire `CombatAction.Icon` in `items.lua`. CE Personal icons unchanged. |
| `_apply_thegrim_recharge_5kills.py` | UNITS-006 Reaper `TheGrim`: ensure RU/EN loc for 5-kill recharge tooltip; runtime is `Code/System_NamedPerks.lua` (`Jazz_TheGrimKillsToRecharge`). |
| `_fix_units006_batch3_loc.py` | UNITS-006 batch3: rewrite RU CE/CSV via unicode-escapes (encoding-safe). |
| `_gen_units006_batch4.py` | UNITS-006 §B batch4: Flo/Static/Cougar + cheap §B CE text/hooks sync. |
| `_units006_namedperks_notes.md` | UNITS-006 batch4: shipped Flo/Static/Cougar + soft cuts → batch5. |
| `_units006_audit_followup.md` | UNITS-006 post-batch audit: Mike PinDown/Vince/MD heal fixes + remaining gaps. |
| `_gen_units006_batch4.py` | UNITS-006 §B batch4: Flo/Static/Cougar + Grace/Kulba/… CE text+hooks; sync items/metadata/loc (reuse CE IDs). |
| `_units006_namedperks_notes.md` | UNITS-006 batch4: before→after + soft cuts (HARD → batch5). |
| `_gen_units006_batch5.py` | UNITS-006 batch5 HARD/satellite + batch6 §D: Rothman/Miguel/Barry/… CE + Miguel aura statuses + Benny/Simon; items/metadata/loc (`9885+`/`9920+`). |
| `_merge_units006_namedperks.py` | Merge Batch3–6 into `System_NamedPerks_006.lua`; relocate Benny/Simon/Miguel aura ModItems; add ModItemCode. |
| `_build_system_namedperks.py` | Rebuild single `Code/System_NamedPerks.lua` (no BatchN Code files). |
| `_units006_perk_moditem_params.py` | Add ModItem Parameters to UNITS-006 perks; wire Code via Jazz_NamedPerkParam; sync items. |
| `_units006_namedperks_notes.md` | UNITS-006 batch5: before→after + soft cuts (Biff economy, ECON-001 Livewire op, Thor recipes). |
| `_add_doubletoss_pocket_cas.py` | Fidel: insert `DoubleTossAG–DG` (GrenadesInventory) ModItemCombatAction + metadata presets. |
| `_fix_grunty_passive_ca.py` | Grunty: Passive CA `GruntyPerk_JAZZ` + HUD icon; strip AdditionalAP double `GainAP`; metadata bump. |
| `_apply_explodingpalm_drq.py` | DrQ: ExplodingPalm unarmed HP-tier statuses + sat debt +30% + WoundInfected block + Passive CA. |
| `_apply_makethembleed_buff_icon.py` | Flay: `Jazz_MakeThemBleedBuff` HUD stacks = visible bleeding enemies (cap 5). |
| `_apply_dangerclose_larry.py` | Larry: DangerClose List2 (explosives ≥8 +40%, blast +2 bleed, stim immune) + loc IDs + items sync. |
| `_apply_gloryhog_pierre.py` | Pierre: GloryHog CE override + `Jazz_PierreRecruit` signature CA (1 recruit/combat) + loc/metadata. |
| `_fix_gloryhog_loc_collision.py` | Restore SteroidPunch 9930/9931 if overwrite; remap Pierre recruit desc/used → 9933/9934. |
| `_apply_recklessassault_smiley.py` | Smiley: RecklessAssault List2 — 4 mobile attacks, SMG/carbine/AR, +15 CTH, no Tiredness; CA+CE+loc. |
| `_patch_buildingconfidence_loc.py` / `_patch_explodingpalm_metadata.py` / `_patch_hawkseye_loc.py` / `_patch_nazdarovya_loc.py` | UNITS-006 loc/metadata helpers for MD / DrQ / Scope / Igor. |
| `_bump_metadata_thegrim.py` / `_fix_last_changes_head.py` | Bump jazz Revision + prepend TheGrim / SignatureAbilities bullets in `last_changes`. |
| `_bump_metadata_hotfix004.py` | HOTFIX-004: Revision +1 and prepend stationary-MG last_changes bullet (`\\n` only). |
| `_bump_metadata_hotfix005.py` | HOTFIX-005: Revision +1 and prepend remountable squad-bag stack last_changes bullet (`\\n` only). |
| `_bump_units_meltdown_meta.py` | Bump jazz-units Revision + Meltdown `[skip discord]` last_changes bullet. |
| `_units006_namedperks_notes.md` | UNITS-006 §D: Benny/Simon CE + StartingPerks; CombatAction soft-cut. |
| `_units006_batch6_startingperks.py` | Prepend `Jazz_Perk_Benny`/`Jazz_Perk_Simon` to jazz-units UnitData + items StartingPerks. |
| `_tmp_list2_perks_fresh.tsv` / `_tmp_list2_sheet_diff.md` | Snapshot + human diff notes for Лист2 perk sync. |
| `_restore_metadata_code_load.py` | После Mod Editor rewrite: вернуть в `metadata.code` критичные `Code/*.lua` (InventoryStacks, ReloadStyle, RemovableModify, …) и пути `InventoryItem/vanillunique/*`; убрать плоские дубликаты. |
| `_audit_metadata_code_coverage.py` | Disk/git `Code/**/*.lua` ↔ `metadata.code`: unexpected MISS / EXTRA; allowlist dormant/source-only (`AME_Browser_Template`, empty stubs, …). Exit 1 = FAIL. |
| `_check_grandchien_map_lfs.py` | `../jazz-maps/Images/GrandChien2.png`: real PNG (~70MB) vs Git LFS pointer (чёрная sat map). Игрокам — `…/releases/download/playable/jazz-maps-playable.zip`, не archive ZIP. |
| `_fix_metadata_utf8_mojibake.py` | Аудит/обратимое исправление одного ошибочного прохода UTF-8→Windows-1251 в `title`, `description`, `last_changes`; `--check` / `--apply`, BOM сохраняется. |
| `_audit_hotfix_003.py` | HOTFIX-003 static regression: Unjam on CombatActions with WeaponResource jam gate; pinned OnAdded/OnBeginTurn + BeginTurn/ApplySuppressionStatus interrupt permanent MG OW; shotgun pellet pack one FX; tooltip ID `890000000001235` catalog + RU/EN. |
| `_audit_ui002_weapon_chips.py` | UI-002 static: Fold/Flash `ShowIn = false`, Unjam stays CombatActions; `idFoldStockButton`/`idFlashlightButton` GridX=2; HUD helpers + GetUIState zzFoldingPair. |
| `_rebuild_weapon_chip_icons.py` | UI-002: rebuild thin 54×54 Fold/Flash chip glyphs from old dual-strip `Icons/stock_*.png` / `flash_*.png` (left half, pad, light thin). |
| `_match_weapon_manip_icon_pairs.py` | UI-002: derive `weapon_flash_off` / `weapon_stock_unfold` from ON/Fold masters so HUD pairs share the same silhouette (beams/arrow only differ). |
| `_rebuild_stock_chip_glyphs.py` | UI-001: replace photo stock `ChipIcon` PNGs with flat `#C8C0A8` glyphs (`--finalize-dir` drafts or `--flatten-only`). |
| `_apply_combat_005_weight_items.py` | JAZZ-COMBAT-005: sync `Weight_*Class` Description + `OnCalcMoveModifier` → `JazzArmorWeightPainOnMove` in `items.lua`. |
| `_apply_combat_007_energy_items.py` | JAZZ-COMBAT-007: insert energy ladder ModItems (`Fit`/`Winded`/`Fatigued`/Tired/Exhausted/WellRested/FreeMove) + `System_EnergyLadder` into `items.lua`/`metadata.lua`. |
| `_apply_combat_007_energy_loc.py` | JAZZ-COMBAT-007: upsert RU/EN CSV rows for energy CE + travel warn/step logs (IDs `890000000013100`–`13120`). |
| `_patch_combat_005_weight_loc.py` | JAZZ-COMBAT-005: RU/EN CSV text for five `Weight_*Class` Description IDs. |

## FortifyErnie / stationary MG

| Скрипт | Назначение |
| --- | --- |
| `_audit_hotfix_004.py` | Static HOTFIX-004: EnterEmplacement wrap, LoadGame/EnterSector reseat, HUD nil-guards. |
| `_audit_hotfix_005.py` | Static HOTFIX-005: remountable CanStack by RemovableComponentId; no Amount=1 clip on bag mark/normalize. |
| `_audit_mg_emplacement.py` | Сводка `MachineGunEmplacement` в `jazz-maps/Maps/*/objects.lua` (weapon/ammo heuristics). |
| `_count_emplacement_ammo.py` | Счётчик `ammo_template` / `weapon_template` по всем `MachineGunEmplacement` в `jazz-maps/Maps`. |
| `_fix_fortify_ernie_mg_handin.py` | GreasyBasil `FortifyErnie`: `MG42` → `Jazz_Browning_MuchineGun`+`Jazz_Browning_Bench` (has/take); I5 `ubRwFgf` ammo_template → `JAZZ_AMMO_50BMG_Basic`. |
| `_patch_ernie_counterattack_heavies.py` | `jazz-units` EnemySquadDef `ErnieCounterAttack`: 1× Rocketeer + 2× AssaultT1_Grenadier + 1× Mortarman (no HeavyT2 hand GL). |

## CTH / cover

| Скрипт | Назначение |
| --- | --- |
| `_calc_cover_cth_gewehr.py` | Static Gewehr98 mid-merc cover CTH (open / full / half / stance); reads `RangeAttackTargetStanceCover` from `items.lua`. |
| `_check_cover_params_items.py` | Assert Cover/Exposed/Crouch/Prone params in `items.lua` match owner soften (−45/−12/−12/−23). |
| `_audit_cth_mod_require_action.py` | List CTHMod `RequireActionType` (missing → class default `Any Attack`). |

## JAZZ-MED-001 / медицина

| Скрипт | Назначение |
| --- | --- |
| `_apply_med002_statuses.py` | MED-002: insert `WoundInfected` + `BloodLoss50`…`1` companions/items/metadata + RU/EN loc rows. |
| `_audit_med001_analgesia.py` | Static MED-001: Pain tracks the current-turn AP penalty; Analgesia consumes it once, refunds AP directly, and companion/`items.lua` stay equivalent. |
| `_audit_med001_kit_requirements.py` | Static MED-001: IFAK/Medkit Medical 30/50 gates, full bleeding clear, Medkit +50% healing, low-skill rollover warning, and companion/`items.lua` parity. |
| `_audit_med003_kits.py` | Static MED-003: Medical 30/50/80, heal +0/+50/+100, MaxStacks 5/10/15, trauma ranks, full bleed, Analgesia+infection, Large Bobby soft-tail, Bonemaker 5% medium. |
| `_apply_med003_kits.py` | Apply MED-003 companion parity into `items.lua` + Bonemaker FirstAidKit/5% Medkit. |
| `_list_merc_medkits.py` | List Mercs loot defs with FirstAidKit/Medkit/Reanimationsset (`_merc_medkits_list.txt`). |
| `_audit_merc_med_loot_redistribute.py` | Static MED-003 hire loot: Med&lt;20 bandages-only, kit cascade, AME Small, bandage/morphine spreads vs plan. |
| `_audit_legion_med_loot_redistribute.py` | Static MED-003 Legion class loot: T2 bandage 1–2, T3 morphine 30%, medic 1–10/0–3 + kits. |
| `_audit_med001_large_kit_trauma.py` | Static MED-001 AC-017: Large Medkit (`Reanimationsset`) marks heaviest unhealed Trauma* with `jazz_healing`; targeting + GetBandaged + loc/hint wiring. |
| `_apply_localization_copy_edit.py` | Validates and applies reviewed RU/EN waves to manual memory; optional `AllIDs` propagates one source-identical review to every listed localization ID. |
| `_apply_maps_quest_repairs.py` | Идемпотентная generated-транзакция JAZZ-QUESTS-001: quest/conversation graph, companions и `jazz-maps/ModTextsMaps.csv`; map-object exports проверяются отдельным аудитом. |
| `_audit_dirty_lua_syntax.py` | Компилирует через `lupa` все modified/untracked `*.lua` в `jazz`, `jazz-maps`, `jazz-units`; read-only pre-commit gate для синтаксиса. |
| `_audit_maps_quest_contract.py` | Static JAZZ-QUESTS-001: компилирует затронутые Lua через `lupa`, проверяет quest wiring, шесть `objects.lua`, Barry Seal, wounded/ally markers, ModTexts и одинаковый RU/EN runtime ID set. |
| `_audit_maps_vanilla_quest_sectors.py` | Inventory/contract для JAZZ-QUESTS-002: stale HotDiamonds landmark refs в `jazz-maps` QuestsDef; `--strict` = exit 1 если Wave A+B ещё stale; Ernie-local I2/I3 и crocodile H14 отдельно. |
| `_apply_maps_vanilla_quest_sector_remap.py` | Идемпотентный apply JAZZ-QUESTS-002: remap sector refs в in-scope QuestsDef + `Pierre_2`/`FlagHill_Corazon_1` и `ModTextsMaps.csv` по transfer table (+ I3→J7, Elliot H14→P17); `--check` / `--apply`. |
| `_bump_package_metadata.py` | Безопасно повышает package Revision на +1 и prepend-ит `last_changes` через literal `\n`, сохраняя UTF-8 BOM; default — dry-run, запись с `--apply`. |
| `_install_localization_exports.py` | Проверяет `sep=,`, схему, numeric/unique IDs и равенство RU/EN export sets; с `--apply` атомарно устанавливает парные runtime CSV. |
| `localization-copy-edits/quests_001.csv` | Канонические RU/EN строки ремонта квестов и разговора Barry Seal; вход для `_apply_localization_copy_edit.py`. |
| `localization-copy-edits/ame_runtime_statuses.csv` | Закрывает восемь накопленных AME status/filter строк RU/EN, чтобы парный runtime export был полным. |
| `_check_ai_medic_bandage.py` | Static: Medic/Medic_Low Healer exclusive + Early + MaxHp 85; combat Score helpers; `AISelectHealTarget` / `AIActionBandage` Precalc; `JazzAI_TryMedicSwitch` all bleed tiers. |
| `_check_sniper_hold_001.py` | Static JAZZ-AI-SNIPER-001: ExtremeRange; stay-hold; useless streak soft HighGround/stay weights (no hard escape). |
| `_check_legion_support_024.py` | Static JAZZ-STRATEGY-024: support role recipe/archetypes/director/icon/loc wiring. |
| `_check_legion_rest_025.py` | Static JAZZ-STRATEGY-025: city/bunker/outpost rest helpers, top-up gate, loc/wiki smoke. |
| `_reorg_squad_icons_folders.py` | One-shot: move `SquadsIcons/Enemy/*.png` into `_shields/`, `_misc/`, `<faction>/`. |
| `_rewrite_squad_icon_doc_paths.py` | Rewrite `squad-role-icons.md` image links after folder reorg. |
| `_bump_sniper001_meta.py` | Revision +1 + prepend `last_changes` bullet for SNIPER-001 commit. |
| `_apply_medic_heal_first.py` | Patch `jazz-units/items.lua` Medic/Medic_Low: combat behaviors Score=0 when heal needed; Healer Early/Weight 1000; Priority Bandage before MobileShot; SelfHealMod 100. |
| `_key_med_item_icons.py` | Flood-fill near-black → alpha для `Icons/Items/JAZZ_{Bandage,Morphine,IFAK,Medkit,SurgicalKit}.png` (не трогает тёмные молнии/ремни). |
| `_key_merc_mark_white_bg.py` | Flood-fill near-white → alpha для `Icons/PDA/MERC_Mark.png` (белый studio plate; жёлтый `$`/teal не трогает). |
| `_check_merc_credit_hire_gate.py` | Static: `System_MERC_Account.lua` — `CanAffordMerc` wrap для MERC + waive `MedicalPaidWhenHired`. |
| `_apply_med001_loot_jazz_units.py` | В `jazz-units/items.lua` к LootDef с `FirstAidKit`/`Medkit`/`Meds`/`MedsDrop` добавляет `JAZZ_Bandage` / `JAZZ_Morphine` / редко `JAZZ_SurgicalKit`. Идемпотентен (сначала снимает старые JAZZ med entries). |
| `_apply_med001_loot_equipment_kits.py` | Phase 2: бинт/морфий (± IFAK у мерков) в Equipment-киты без медицины (`loot=all` враги + Mercs leaf tiers). Не трогает ammo/Drop_/Armor. Merc insert: Bandage 10, IFAK 5. |
| `_apply_merc_med_full_stacks.py` | Mercs `group=Mercs` в `jazz-units/items.lua`: существующий `JAZZ_Bandage` → stack 10; `FirstAidKit` → 5; `Medkit` → 10; `Reanimationsset` → 15 (MaxStacks). Идемпотентен. |
| `_apply_merc_med_loot_redistribute.py` | Hire medicine by Medical/Doctor/Tier (MED-003): Med&lt;20 bandages only; kit cascade; AME Small; bandage/morphine spreads. Idempotent. |
| `_apply_legion_med_loot_redistribute.py` | Legion class inventories (recipes.json): T2 Bandage 1–2; T3 Morphine 30%; medic Bandage 1–10 + Morphine 0–3; strip Mortarman_Launcher junk. Idempotent. |
| `_apply_enemy_med_stacks_min.py` | Не-Mercs LootDef: `JAZZ_Bandage` / Morphine / Surgical / FirstAidKit / Medkit → `stack_min/max = 1`. Mercs не трогает. |
| `_fix_med001_loot_drop_lists.py` | Снимает ошибочные JAZZ med entries с `Drop_*` / Comment=list ammo pools; патчит `PierreGuard_Ordnance`. |
| `_audit_med001_loot_jazz_units.py` / `_audit_med001_unit_kits.py` | Аудит покрытия Bandage по medical LootDef и UnitData Equipment. |
| `_audit_loot_missing_items.py` | `jazz-units` `item=` vs known InventoryItem IDs (jazz `InventoryItem/` + vanilla ModTools defs). Exit 1 если есть MissingItem-кандидаты. |
| `_patch_med_stack_kit_loc.py` | MED stack kits: RU/EN hint «refill with Meds» → «one use = one item»; append `890000000010030` (Reanimationsset). |
| `_fix_med001_loot_braces.py` | Чинит `}}),` → `}),` на строках JAZZ med loot (баг f-string). |
| `_bump_units_med_loot_meta.py` | Bump `jazz-units/metadata.lua` Revision + `last_changes` после loot apply. |
| `_wire_med001_traumas.py` / `_append_med001_trauma_loc.py` | Wiring/loc зональных Trauma* эффектов. |
| `_apply_grenade_concussion.py` / `_append_grenade_concussion_loc.py` / `_patch_he_grenade_concussion_hint_loc.py` / `_fix_concussion_loc_ids_items.py` / `_patch_grenade_concussion_guaranteed_loc.py` | Playtest: `Concussion` CharacterEffect + items/metadata; RU/EN loc `890000000010277–280`; Frag/HE hints. Runtime: `JazzTryApplyExplosionConcussionAndTrauma` (concussion guaranteed). Loc patch: chance→guaranteed on IDs `243383619902` / `663236691841`. |
| `_patch_grenade_mishap_hint_loc.py` | RU/EN Frag `243383619902` + M79 `397383171067` AdditionalHint: quarter/half mishap curve, thr ~50, elite max-range note. |
| `_patch_grenade_mishap_magnitude_90.py` | Retune `GetMishapDeviationBounds`: half≈old max magnitude, full≈+25% (90/90 ~80% pre-tune accuracy); skill floor 10%. |
| `_bump_metadata_grenade_mishap.py` / `_stage_items_grenade_hints_only.py` | Commit helpers: metadata revision+last_changes; items.lua = HEAD + Frag/M79 hints only (officer WIP aside). |
| `_apply_officer_aura_loc.py` | CMD-001 UI: RU/EN `890000000006100–6124` (OfficerAura / Influence; directives incl. OccupyHeights; buff labels; order-effect tooltip). |
| `_apply_jazz_trauma_effect_parent.py` | Trauma* → parent/`object_class` `JazzTraumaEffect` (companions + `items.lua`); paired with early `Code/System_JazzTraumaEffect.lua`. |
| `_audit_trauma_loc_ids.py` | Trauma* + medicine timing T() IDs vs `Russian.csv`/`English.csv` (Text match, non-empty Translation, no garbage). Exit 1 if broken. |
| `_patch_med001_hit_pain_ac.py` | MED-001: insert AC-012 (+ fix REQ-010 backticks) for `JazzPainOnDamagingHit` contract. |
| `_fix_med001_runtime_csv.py` | MED-001: чинит `Russian.csv` Text/Translation (EN source / RU translation) + literal `\\n` → реальные переносы в AdditionalHint. |
| `_fix_med_en_in_ru_loc.py` | Playtest: восстанавливает RU Translation для MED AdditionalHint (`010013/016/019/024/027/030`) + Concussion `010277–280`; снимает `mag-hint-aligned` vanilla stomps EN-in-RU. |
| `_scan_en_in_ru_loc.py` | Read-only: Cyrillic Text + English Translation в `Russian.csv` (perk/CA vs other vs both-EN). |
| `_alloc_mod_loc_id.py` | Следующий свободный ID в `890000000000000..890000000099999` (скан Lua/CSV, без `Maps/`). |
| `_insert_runtime_loc_row.py` | Точечная вставка одной однострочной loc-строки в RU/EN + Strings + manuals (без перезаписи всего CSV). |
| `_fix_en_in_ru_ability_loc.py` | Playtest: `Russian.csv` Translation=Text для perk/signature CA (UNITS-006 `upsert_csv` писал EN в RU). `--apply`. Не трогает VR/InventoryItem. |
| `_fix_med001_loc_append.py` | Перезаписывает RU/EN строки `890000000010200+` (JazzBandage / trauma timing / kit Bandage desc); Text=EN, Translation=язык. |
| `_patch_combat_status_ui.py` | CombatBadge: 2–3 critical icons у ника; party combat `idWounded` → `JazzGetPartyPortraitStatusEffects` (parity с satellite). |
| `_recenter_med_action_icons.py` | Recenter+upscale dual-strip 108×54: `--dir Icons/Med` (default) или `Perks/SignatureAbilities`. Мелкие/съехавшие к центру полосы → fill≈48px. `--dry-run` / `--pad`. |
| `_audit_action_icon_center.py` | Аудит bbox/dx/dy dual-strip в `Perks/SignatureAbilities` + `Icons/Med` (+ list лишних 108×54). WARN если \|dx\|/\||dy\|>2.5. |

## JAZZ-ATTACH-001 / оружие–обвесы

| Скрипт | Назначение |
| --- | --- |
| `_apply_steam_ignore_files.py` | Синхронизирует `ModDef.ignore_files` + `.gitignore` по всем пакетам suite (`jazz`, `jazz_assets`, `jazz-units`, `jazz-maps`, `jazz-nomaps`): Steam pack exclusions + bump Revision + append `last_changes`. Запуск из любого cwd; пути абсолютные к `Mods/`. |
| `_apply_attach_001.py` | Основная миграция ATTACH-001: strip Handling-effects, CloseRange wiring, Mount purge, `JAZZ_` rename, unused delete. `--dry-run` (default) / `--apply` (+ `.bak`). |
| `_export_attach_csv.py` | Экспорт `weapon-components*.csv` / `weapons.csv` из **working tree** (`items.lua` + companions; weapons без companion — из ModItem). Нужен когда нет `JA3_ROOT` для `weapons-docs.mjs import`. |
| `_analyze_weapons_balance.py` | Аудит баланса по `weapons.csv`: within-family z-score, residual vs tier, rare `AvailableAttacks`, peaks → `.tmp/weapon_analysis.json`. |
| `_analyze_weapons_followup.py` | Печать срезов (AR/SMG/sniper/uniques) из `.tmp/weapon_analysis.json` для ручного разбора. |
| `_apply_weapon_role_tweaks.py` | Ролевые твики FAMAS/Agram/Sig550*/PSG1 → companions + `items.lua` + `weapons.csv`. `--apply`. |
| `_update_role_tweak_loc.py` | RU/EN AdditionalHint для тех же стволов в `Russian.csv`/`English.csv`. |
| `_verify_role_tweaks.py` | Быстрая проверка props в `items.lua` после role tweaks. |
| `_remove_cancelshot_attacks.py` | Убирает `CancelShot` из `AvailableAttacks` оружия в `items.lua` + `weapons.csv` (не трогает grenade AreaAppliedEffects / CancelShotCone). |
| `sync-reload-style-csv.py` | JAZZ-WEAPONS-004: добавляет `reload_style` в канонический `weapons.csv` и проставляет Magazine/Tube/Break/Revolver по утверждённому списку ID. |
| `_promote_vanilla_refs.py` | **Устарело / опасно:** тонкие stubs без Visuals. Не запускать. |
| `_promote_vanilla_refs_visuals.py` | AC-008: поднять 9 dangling vanilla_ref в `JAZZ_*` ModItem **с Visuals** из `Data.hpk` (`WeaponComponentSharedClass.lua`); rename AvailableComponents/DefaultComponent + metadata resources. Требует `.tmp/data-extract/` после `hpk extract Packs/Data.hpk`. |
| `_remove_handling_stat.py` | Удалить Firearm property `Handling` + данные оружия + WeaponPropertyDef/GameTerm/CTH modifier + колонку CSV. Idempotent. |
| `_fix_items_lone_commas.py` | Починить дыры `{ a, , b }` после PlaceObj-delete (одиночные `,`), откатить пустые stub-ID → vanilla, удалить stub ModItems. Запускать если `items.lua` не грузится / GPU assert после массового delete. |
| `_fix_akm_scope_mount_visuals.py` | Добавить Visual `WeaponAttA_MountAK47` `ApplyTo=AKM` на западные прицелы (`Scope_12x`/`6x`/`NightScope`), у которых не было переходника (слот Mount не нужен — меш в Visuals оптики). |
| `_rebalance_reflex_tiers.py` | `JAZZ_Reflex_*`: Precision/OW/Universal; AA% + CloseRange soft + MinAim/−1 MaxAim. Канон: `docs/design/reflex-collimator-tiers.md`. |
| `_rebalance_combat_scopes.py` | Combat: mid near/OW + AimAccuracy% 125…155. Канон: `docs/design/combat-scope-tiers.md`. |
| `_rebalance_long_scopes.py` | Длинная/entry/night: far reach, ShotAP+Crit, harsh near, cost tiers. Канон: `docs/design/long-scope-tiers.md`. |
| `_rebalance_barrel_tiers.py` | Стволы: BDR% + CloseRange* + Recoil; R ±1. Канон: `docs/design/barrel-tiers.md`. |
| `_rebalance_muzzle_tiers.py` | Дуло: Recoil vs Silent; choke pattern; без R/BDR. Канон: `docs/design/muzzle-tiers.md`. |
| `_rebalance_magazine_tiers.py` | Магазины: small / standard / expanded(no-tax) / large(tax). Канон: `docs/design/magazine-tiers.md`. |
| `_apply_mag_size_set.py` | JAZZ-ATTACH-001 MagSizeSet: добавляет effect/resource/localization, разрезает generic `JAZZ_MagLarge` на абсолютные варианты, rewires items + companions и проверяет отсутствие live mag multiplier. `--apply` пишет `.bak`. |
| `_apply_mp40_mag_normal_only.py` | MP40: только `JAZZ_MagNormal` (32). Убирает `JAZZ_MagLarge_50_MP40` из слота/компонента/remountable/metadata и из GenW `LootEntryUpgradedWeapon` в `jazz-units`. `--apply`. |
| `_verify_mp40_mag_normal_only.py` | Smoke: MP40 MagNormal-only, no MagLarge_50_MP40 in jazz/jazz-units, LoadGame reseat map present. |
| `_verify_mp40_mag_normal_only.py` | Smoke: нет `JAZZ_MagLarge_50_MP40` в jazz/units data; GenW assault_m1 = InventoryItem; reseat map в `System_WeaponComponent_Set.lua`. |
| `_gen_setweaponcomponent_override.py` | Генерирует `Code/System_WeaponComponent_Set.lua` из vanilla `FirearmBase:SetWeaponComponent` + ветка `ModificationType=Set` (`mul=1000`, `add=N−base`). |
| `_apply_grizzly_perk_full_damage.py` | GrizzlyPerk: `dmg_penalty` −50→0 + sync CE description in `items.lua`. |
| `_apply_haveablast_fix.py` | HaveABlast: sync CE reactions/description into `items.lua` (optional helper; primary edit is companion + items). |
| `_patch_haveablast_loc.py` | HaveABlast: patch RU/EN description rows in `English.csv`/`Russian.csv` without full CSV rewrite. |
| `_patch_nazdarovya_loc.py` | Nazdarovya/Drunk: upsert RU/EN rows for perk, status, CombatAction strings. |
| `_patch_buildingconfidence_loc.py` | MD BuildingConfidence: upsert RU/EN perk description (Inspired turns + heal level-diff). |
| `_patch_hawkseye_loc.py` | Scope HawksEye: upsert RU/EN (sniper OW 1 AP + biscuits + suppress ×2). |
| `_audit_mag_size_set_defaults.py` | Список оружия с default-магазином на `MagazineSizeSet` (поверхность бага MagSize=1 при `mul=0`). |
| `_validate_wave_weapons.py` | Статическая валидация волны ATTACH-001 MagSizeSet + WEAPONS-002..005 (якоря, metadata load, loc, CSV). |
| `_peek_mag45_kobra.py` / `_peek_mag45_kobra2.py` / `_list_reload_effects.py` | Peek Mag45 / Reflex_Cobra effects+params и Reload* effect presets в `items.lua`. |
| `_fix_stock_barrelparts_costs.py` | WEAPONS-002: `JAZZ_BarrelParts` в AdditionalCosts только у Slot=Barrel; остальное → `Parts`. `--apply` + `.bak_stock_barrelparts`. |
| `_make_barrelparts_icon.py` | Иконка `JAZZ_BarrelParts`: extract `fine_steel_pipe.dds` из `UI.hpk`, charcoal recolor → `Icons/Items/JAZZ_BarrelParts.png`, wiring companion/`items.lua`. |
| `_purge_legacy_gunsmith_parts.py` | WEAPONS-002: безопасный remap только `'Type'`/`'item'` в costs (`FineSteelPipe`→`JAZZ_BarrelParts`, lens/chip→`Parts`); **не** трогает `'Id'`. `--restore-bak` из `items.lua.bak_legacy_parts`; dormant shop на legacy defs. `--apply`. |
| `_verify_gap_fixes.py` | Smoke после wave gaps: Id uniqueness Parts/BarrelParts, Type leftovers, unique WeaponMass. |
| `_verify_nomaps_unit_remap_named_skip.py` | COMPAT-004: static mirror remap families — Bastien skip; `WeakFlagHill`→assault; `*_Tutorial` stems; Hyena skip. |
| `_verify_nomaps_fortress_pierre_squad.py` | NoMaps: `FortressPierre` must stay out of `SQUAD_REMAP` (vanilla Pierre boss; not `LegionJAZZSquadT2`). |
| `_retire_legion_fortress_defenders.py` | Удаляет `LegionFortressDefenders`; добавляет `FortressDefenders_NoMaps` (~16); NoMaps remap/garrison → half-size pack. |
| `_apply_ernie_counterattack_nomaps.py` | Adds `ErnieCounterAttack_NoMaps` (20, no mortar) + NoMaps `SQUAD_REMAP` from `ErnieCounterAttack`. |
| `_dump_villa_squads.py` | Dump min–max composition of AroundVilla Sentry + VillaAttackers_K3/K5/L3/L4/L5 and sector Init totals. |
| `_tighten_villa_squads.py` | Set Villa Sentry=10 + Attackers 12/13/14/15/16 (sector Normal 22–26); Easy/Hard ±10 documented in baseline. |
| `_rewrite_legion_ernie_village.py` | Rewrite `LegionErnieVillage` (I5=60 meat+10 Pillager) + `Shooters_Easy_Ernie` (J5=40); strip Extra stacking from I5/J5 Init. |
| `_ernie_init_dump.py` | Dump Ernie ModItemSector `InitialSquads` + **design-Normal** sums (gated: engine Hard; ungated always). Does not cross ModItemSector boundaries. |
| `_sync_ernie_campaign_inits.py` | Sync HotDiamonds CampaignPreset Ernie Init → ModItemSector canon (UNITS-007 + locked hubs); clear map-only I6/J6/L7/K4/K6. Dry-run / `--apply`. Edits only CampaignPreset span + ModItem clears. |
| `_audit_ernie_empty_squad_risk.py` | Ernie Init empty-spawn risk + Campaign vs ModItem drift (boundary-safe). |
| `_rollback_units006_vanilla_merc_perks.py` | Remove jazz CE overrides for listed vanilla merc personal perks (ModItem+companion+metadata+loc); also jazz-units `TheGrim`. |
| `_fix_ernie_mixed_per_unit.py` | `LegionExtra_Ernie_Mixed`: split 6–9 into per-unit slots (vanilla rolls type once per EnemySquadUnit). |
| `_fix_checkdifficulty_storeastable.py` | Mass-fix `CheckDifficulty` `'Difficulty', "X"` → `Difficulty = "X"` (FunctionObject StoreAsTable=true; prevents load assert). Also syncs CampaignPreset M4 Init + Extra. Dry-run / `--apply`. |
| `_audit_units_squad_load.py` | Audit jazz-units CheckDifficulty format + M4 InitialSquads ModItemSector vs CampaignPreset drift. |
| `_apply_ernie_i2_lighthouse.py` | Earlier I2 lighthouse draft (superseded by overflow apply). |
| `_probe_ernie_init_blocks.py` | Probe `InitialSquads` by `sectorId`. |
| `_purge_k4_house_ambushers.py` | Remove K4 `HouseAmbushers`+`Legion` AdvanceTo; insert `VillaSiege_Wave2`×25 gated by `Jazz_VillaCounterAttack.Wave2Spawn`. |
| `_add_villa_attackers_ernie.py` | Insert `JAZZ_Legion_VillaAttackers_Ernie` base 30 + metadata. |
| `_wire_villa_counterattack.py` | Quest `Jazz_VillaCounterAttack` + FlagHill Guests + ModItemCode/metadata. |
| `_verify_villa_counterattack_static.py` | Static: Ernie size, Wave2 count, old siege remaining=0. |
| `_verify_guardpost_scripted_attack.py` | Guardpost: `ForceSet` does not call `CanSpawnNewSquad`; managed early-out kept on CanSpawn/Update/Spawn (scripted Ernie attack OK, vanilla auto muted). |
| `_verify_nomaps_early_squad.py` | COMPAT-005: `LegionJAZZSquadT1_Early` all `T1_`; metadata Id; NoMaps remap/cap wiring. |
| `_verify_nomaps_globals_predeclare.py` | NoMaps wrap flags predeclared at file top + `rawset` + `lQuestVarSafeSet`. |
| `_verify_nomaps_region_radius.py` | COMPAT-007: `AUTO_REGION_RADIUS=false` (unbounded Voronoi), `AI_REGION_REV=2`, multi-outpost refresh; no legacy `<= 8`. |
| `_verify_nomaps_squad_size_cap.py` | COMPAT-009: только `InitialSquad*` NoMaps capped at 30 в `GenerateUnitsFromTemplates`, после BodyCount; dynamic squads/economy unchanged. |
| `_audit_loot_item_case.py` | `jazz-units` LootEntry `item=` vs `InventoryItem` DefineClass (ловит `Mas36`≠`MAS36`). Exit 1 при mismatch. |
| `_audit_faction_overlay_static.py` | Static AC hooks for STRATEGY-014/018: matrix API, ownership, avoid-player routing, load registration. |
| `_apply_hotfix006_difficulty_loc.py` | HOTFIX-006: rewrite Normal/Hard/VeryHard GameDifficultyDef tooltips in `items.lua` + Russian.csv/English.csv (copy limits, medics, starting funds). |
| `_test_legion_class_caps.py` | HOTFIX-006: same-id (except `JAZZ_LegionUncappedLineIds`) + escort Front specialists + Marksman deny; STRATEGY-008 bucket formulas unchanged. |
| `_test_legion_medic_density.py` | STRATEGY-015: static mirror `JAZZ_GetLegionMaxMedics` + generator wiring markers. |
| `_test_legion_spawn_pool.py` | Static STRATEGY-019: global spawn pool + tax/recruiter 72h gate + tax/recruiter → combat → supply order. |
| `_test_legion_squad_growth.py` | STRATEGY-016: early→mature sizes, economy ×0.25 markers, cadence defaults; NoMaps size override. |
| `_test_legion_money_cargo.py` | STRATEGY-017: tagged cargo sync / tax collect / regen resync markers. |
| `_dump_sergeant_firearm.py` | Read-only: dump `Sergeant_Firearm` primary unlocks (weapon / Amount band / weight / package) from `jazz-units/items.lua` after legion-loadouts regenerate. |
| `_insert_reload_combat_action.py` | WEAPONS-004: вставляет full `ModItemCombatAction` `Reload` в `items.lua` + `ModResourcePreset` в `metadata.lua`. |
| `_insert_rebels_flanker.py` | ROLE-001 repair: clone `Legion_Flanker` → `Rebels_Flanker` in `jazz-units/items.lua` (metadata Id already present). Idempotent. |
| `_set_flanker_optloc.py` | Set `OptLocSearchRadius` on `Legion_Flanker` / `Rebels_Flanker` (default 55). |
| `_count_aiarchetypes.py` | List/count `ModItemAIArchetype` ids in `jazz-units/items.lua`. |
| `_fix_weaponmod_untranslated.py` | ModifyWeaponDlg: заменить `Untranslated("<bullet_point> "..)` на `T{990002014,…}` в XTemplate (assert IsLookupTag). |
| `_fix_unique_reload_style.py` | WEAPONS-004: `ReloadStyle` на `InventoryItem/vanillunique/*` quest/unique. |
| `_rebalance_stock_tiers.py` | Приклады: Normal/Heavy/Light/Folded. Канон: `docs/design/stock-tiers.md`. |
| `_rebalance_under_grip_tiers.py` | Рукоятки: Vertical Recoil / Tac·Wrap CloseFactor / Ergo AA%. Канон: `docs/design/under-grip-tiers.md`. |
| `_rebalance_bipod_tiers.py` | Сошки: один `JAZZ_Bipod` + Under; cut Fold/MG42/KSP. Канон: `docs/design/bipod-tiers.md`. |
| `_rebalance_side_tiers.py` | Side: Flashlight/Dot/Laser/UV. Канон: `docs/design/side-tiers.md`. |
| `_fix_dup_bipod.py` | Убрать дубли `JAZZ_Bipod` после cut-remap. |
| `_fix_flashlight_off_opts.py` | Добавить `JAZZ_FlashlightOff` в AvailableComponents + stock fold pair JAZZ_ ids. |
| `_list_stock_profiles.py` | Dump текущих `JAZZ_Stock*` effects/params. |
| `_peek_stock_costs.py` | Peek `JAZZ_Stock*` `Cost` / difficulty из `items.lua` (после `_rebalance_stock_tiers`). |
| `_gen_removable_attachment_items.py` | WEAPONS-002: каталог InventoryItem на каждый remountable `JAZZ_*` component (`Id` = component id, folder RemovableAttachments). `--apply` → items/metadata/companions/loc. Hyphenated ids → `DefineClass("Id-With-Hyphen", {…})`. |
| `_split_mag_families.py` | Режет shared `JAZZ_Mag*` по mag-well семьям (`…_AK` / `…_AR15` / …); клоны WeaponComponent + InventoryItem companions. |
| `_union_mag_family_options.py` | После split: union Magazine options внутри семьи (магазин АК → РПК). |
| `_remove_mag_50_ak.py` | Убрать ошибочный `JAZZ_MagLarge_50_AK`; канон АК expanded = `JAZZ_MagLarge_30_40` (40). |
| `_fix_hyphen_defineclass.py` | One-shot: `DefineClass.Name-With-Hyphen = {` → string form (load error «syntax error near '-'»). |
| `_fix_removable_metadata_presets.py` | Починить metadata stubs каталога → `ModResourcePreset` InventoryItemCompositeDef. |
| `_add_scopeparts_loc.py` / `_fix_scopeparts_loc_schema.py` | Loc для `JAZZ_ScopeParts` + remove-fail messages (RU/EN full schema). |
| `_cut_muzzle_booster.py` | One-shot: вырезать `JAZZ_MuzzleBooster` из items/metadata/companions. |
| `_list_mag_profiles.py` | Dump текущих `JAZZ_Mag*` effects/params из `items.lua`. |
| `_cmp_optic_cth.py` | Матрица CTH по архетипам оптики; default `--weapon DragunovSVD` (`*` = слот на пушке). |
| `_audit_long_scopes.py` | Снимок long-scope профилей (данные). |
| `_calib_optic_targets.py` | Старая калибровка рычагов ×1.2 (исторически АКМ). |
| `_rebalance_long_scope_ow.py` | Длинная оптика: `ScopeOverwatchAngle`% уже по кратности (больше зум → уже OW). |
| `_validate_items_quick.py` | Быстрый структурный check `items.lua`/`metadata.lua` (lone commas, braces, stacked closers, **missing comma before PlaceObj**, **raw newline inside quoted strings**, **CheckDifficulty StoreAsTable-false**, UTF-8/Windows-1251 mojibake в metadata, corrupt `id = }),`) без JA3. **Обязателен после mass apply / family split**. Опционально: `python docs/tools/_validate_items_quick.py [pkg…]` (напр. `.` и `../jazz-units`). |
| `_fix_bobbyray_string_tier.py` | Bobby Ray: `Tier = "4"`/`'Tier', "5"` → numeric в `items.lua` + `InventoryItem/*.lua` (иначе `PrepareShopItemsForRestock` Assert string≤number). Dry-run / `--apply`. |
| `_fix_ame_callsign_in_name.py` | AME callsign в `Name`: `Didier Mbemba`+Nick `Smoke` → `Didier "Smoke" Mbemba` / `Дидье "Дым" Мбемба` (vanilla single-quoted `T`). Companions + `jazz-units/items.lua` + RU/EN. Dry-run / `--apply`. |
| `_apply_strategy_021_great_desert.py` | STRATEGY-021: `GreatDesert` Region + PortCacao `LateAwakenMinTier`/Starting* =0 в `jazz/items.lua` + metadata resource. |
| `_apply_mountain_steppe_region.py` | Trim GreatDesert (drop A9–A12/B9–B12/C8–C12) + add `MountainSteppe` / D18; metadata resource. |
| `_fix_savanna_west_from_steppe.py` | Owner fix: restore A9–A12/B9–B12/C8–C12 to `GreatDesert`; MountainSteppe from A13…; drop D11–D12 overlap. |
| `_add_great_desert_sectors.py` | Append sectors to `GreatDesert` (overlap check vs other Regions). |
| `_apply_fleatown_environs_region.py` | Add `FleatownEnvirons` / H19; drop F18 from MountainSteppe (overlap). |
| `_apply_labarrier_region.py` | Add `LaBarrier` / L15 + Ernie `MajorSupplyPriority`; wire L15 Global AI lists. |
| `_apply_great_forest_region.py` | Add `GreatForest` / G22+K21 shared dual-outpost; wire Global AI lists. |
| `_verify_late_awaken_regions.py` | Print `LateAwakenMinTier` / `LegionAIEnabled` per authored Region in `jazz/items.lua`. |
| `_restore_ernie_sectors.py` | Restore `ErnieIsland.Sectors` from `HEAD` (keeps `MajorSupplyPriority`). |
| `_fix_metadata_last_changes_and_audit_code.py` | HOTFIX-001: чинит raw newline в `metadata.lua` `last_changes` (иначе local mod не грузится → Steam packed); аудитит все `metadata.code` пути vs disk/git (missing/case). |
| `_append_imp001_loc.py` | JAZZ-IMP-001: RU/EN строки `890000000001931–936` (Russian.csv: Translation=RU; English.csv: Translation=EN). |
| `_append_close_range_rollover_loc.py` | CloseRange card-row values RU/EN `890000000001937–938` (`+N (tiles)` / `−N% (tiles)`); label = `982641736210`. |
| `_upsert_grizzly_perk_loc.py` | JAZZ-WEAPONS-012: upsert `272740235755` GrizzlyPerk Description RU/EN (signature ignores unsupported penalties). |
| `_bump_close_range_stg_anchor.py` | Scale Firearm `CloseRange` by StG-44 anchor (6→8, ×4/3 tiers: 2→3, 4→5, 6→8, 8→11, 12→16); companions + `items.lua` + `BASE_CLOSE_RANGE`. Dry-run / `--apply`; idempotent if STG already 8. |
| `_check_imp_certificate_fix.py` | Static: IMP loc Translation columns + Sniper `Perk-Specialization` + Veteran `OldDog` + personal wrap. |
| `_insert_imp_personality_perks.py` | JAZZ-IMP-001: вставляет `Jazz_Perk_{Mimicry,Veteran,Sniper}` в Personality-папку `items.lua`. |
| `_check_imp_perk_items.py` | Проверяет наличие трёх IMP Personality ModItems и Icon. |
| `_ensure_imp001_metadata.py` | Гарантирует code/CharacterEffect/ModResourcePreset записи IMP-001 в `metadata.lua` + revision bump. |
| `_bump_units_imp001_meta.py` | Bump `jazz-units/metadata.lua` Revision после placeholder `IMP_equipment_basic`. |
| `_list_perk_icons.py` | Список vanilla CharacterEffect Icon paths (для подбора IMP perk icons). |
| `_audit_imp001_ids.py` | JAZZ-IMP-001: static audit class IDs (оружие/перки/расходники) в jazz+jazz-units. |
| `_bump_imp001_fix_meta.py` | Revision bump + last_changes bullet после hotfix Sniper/LMG. |
| `_bump_metadata_for_commit.py` | Универсальный Revision +1 и prepend `last_changes` bullet (literal `\\n` only). `--path` для sibling packages. |
| `_audit_region_descriptions.py` | Печатает DisplayName/Description_len для mainland Region presets в `items.lua` (Ernie/PortCacao/…). |
| `_bump_suite_018.py` | One-shot: suite display → `0.18` (`version_minor` 18, rev 6015), title `v0.18`, prepend `last_changes` (literal `\\n` only). |
| `_wire_med001_traumas.py` | MED-001: генерирует `Trauma*` CharacterEffect companions + inserts ModItems/metadata; патчит `*shot` / `Unconscious` / `Burning` → trauma API. |
| `_append_med001_trauma_loc.py` | MED-001: дописывает RU/EN строки `890000000009226`–`009255` для Trauma* DisplayName/Description. |
| `_lupa_load_items.py` | Реальный Lua parse `items.lua`/`metadata.lua` через lupa (stubs PlaceObj/T). Ловит syntax как игра. |
| `_audit_items_structure.py` | Аудит: `})` без `,` перед `PlaceObj`, PlaceObj@col0, brace depth. |
| `_fix_maglarge_50_ak_remnant.py` | Удалить битый remnant `MagLarge_50_AK` (`id = }),`). `--apply`. |
| `_strip_lone_commas.py` | Только вырезать lone-comma строки из `items.lua`/`metadata.lua` (артефакт insert). Атомарная запись через `.tmp`. |
| `_rename_mag_hyphen_ids.py` | Public id MagBelt/MagDrum: `-` → `_` (DefineClass-safe). items/metadata/companions/CSV. `--apply`. |
| `_clean_broken_comp_ids.py` | Убрать битые `DefaultComponent`/`AvailableComponents` (`su`, пустые/multiline id). |
| `_attach_classify.py` | Классификатор comps/effects (`live` / `legacy_handling` / …) для catalog/audits. |
| `_audit_attach_ids.py` | Audit: prefix `JAZZ_`, Mount, unused comps (читает CSV). |
| `_audit_attach_effects.py` | Audit: Handling/orphan effect presets (читает CSV + `items.lua`). |
| `_audit_attachment_icons.py` | Audit `Icon`/`ChipIcon` vs disk: wired / need-wire / need-generate; пишет `_audit_attachment_icons_report.txt`. |
| `_audit_component_icon.py` | Audit только `WeaponComponent.Icon` (кабинет ModifyWeaponDlg): missing / vanilla / `WeaponComponents/` / Full; `_audit_component_icon_report.txt`. |
| `_audit_unique_entity_icons.py` | Unique Entity-set vs shared Icon backlog (style B). Scope/Magazine priority; barrels optional. |
| `_finalize_icon_style_b.py` | Style B Icon: magenta/rembg cut (incl. enclosed cutouts) → heal → Anaconda soft edge → 100×100. Canon: `WeaponComponents/references/PROMPT.md`. |
| `_punch_enclosed_dark_holes.py` | Punch closed near-black fills inside skeleton stocks (triangle/trapezoid cutouts). |
| `_apply_fix_batch_icons.py` | Fix-batch: FAMAS/SIG/G36/SVT/AUG42/AR10 finalize + M72 WeaponIcon. |
| `_audit_icon_crosswire.py` | Проверка: content-dup PNG, cross-family ApplyTo, orphan Sig UnFolded, SVT/AVT map. |
| `_qa_icon_style_b.py` | QA preview Icon: size/opaque/soft-AA/corners/bright-fringe. Fail → regen. |
| `_wire_ak74_mag_icons.py` | MagNormal/MagLarge_30_45 ApplyTo AK74+RPK74+AKSU+AN94 → `AK74_Mag30` / `AK74_Mag45_long`; MagQuick_AK AN94 → Mag30. |
| `_wire_g36_mag_icons.py` | MagNormal ApplyTo G36 + G36c → `Magazine/G36_Mag30.png`. |
| `_wire_g36_stock_icons.py` | StockNormal ApplyTo G36 → `Stock/G36_Stock_Normal.png` (базовый скелетный). |
| `_wire_vss_val_mag_icons.py` | MagNormal VSS/AS_Val → VSS_Mag10; MagLarge_10_20_VAL → VSS_Mag20. |
| `_wire_sig_icons.py` | MagNormal Sig550/Custom/552/SWAT → Sig_Mag30; SigDefHandGuard + SigErgoHandGrip Icons. |
| `_wire_sig_stock_icons.py` | SIG Stock Folded/UnFolded/Heavy Style B; fix Sig550Custom/Sig552 DefaultComponent → StockLightUnFolded. |
| `_fix_ak_mag_caliber_options.py` | AK 7.62 vs 5.45: `MagLarge_30_40`/drum только на АКМ/АК47/…; `MagLarge_30_45` только на АК74/…. Companions+items. `--apply`. |
| `_hide_fold_only_stock_slots.py` | `Modifiable=false` на Stock, если options только `StockLightFolded`+`StockLightUnFolded`. Companions + `items.lua`. `--apply`. |
| `_strip_freeswap_wiki.py` | После strip: убрать Freeswap из `docs/wiki/weapons/*` по CSV options; оставить MP5K/MicroUZI/Scorpion; обновить count в `components.md`. |
| `_wire_ak74_stock_icon.py` | Wire `JAZZ_StockNormal` ApplyTo=AK74 → `WeaponComponents/Stock/AK74_StockNormal.png`. |
| `_wire_ak74_stock_fold_icon.py` | Wire AK74 fold stock on UnFolded/Folded/StockLight/UnfoldStocks → `AK74_StockFold_v2.png` (folded shares art until distinct). |
| `_wire_akm_stock_icons.py` | Wire AKM wood `StockNormal` + underfolder Folded/UnFolded/UnfoldStocks → `AKM_StockNormal/Fold.png`. |
| `_wire_mag_762_vanilla.py` | MagNormal 7.62 (AK47/AKM/RPK/Type56/Zastava_M70/ZastavaM92) → vanilla `UI/Icons/Upgrades/AK47_magazine`. |
| `_wire_stanag_mag_icons.py` | CAR15/M4/M16/AR15: MagNormal+MagSmall30_20 → `m16_magazine`; MagQuick gaps → `quick_STANAG_magazine`. |
| `_wire_p210_ironsight.py` | `JAZZ_IronSight` ApplyTo=P210 → vanilla `UI/Icons/Upgrades/ironsights`. |
| `_wire_p210_ironsight_aim.py` | `JAZZ_IronSight_AIM` P210 → `Optics/P210_IronSight_AIM.png`; comp Icon `ironsights_hands`. |
| `_wire_p210_handgrip_default.py` | `JAZZ_Handgrip_Default` ApplyTo=P210 → `Handgrip/P210_Handgrip_Default.png`. |
| `_wire_p210_handgrip_ergo.py` | `JAZZ_Handgrip_Ergo` ApplyTo=P210 → `Handgrip/P210_Handgrip_Ergo.png`. |
| `_wire_1911_mag_icons.py` | MagNormal Colt1911 (+Kimber) → `Magazine/Colt1911_MagNormal.png` (style B). |
| `_wire_p220_mag_icons.py` | MagNormal P220 → `P220_Mag8.png`; MagLarge_8_10 → `P220_Mag10.png`. |
| `_wire_kimber_mag_icons.py` | MagLarge_7_10 ApplyTo Kimber → `Magazine/Kimber_Mag10.png`. |
| `_wire_p226_mag_icons.py` | MagNormal P226 → `P226_Mag15.png`; MagLarge_18_20 → `P226_Mag20.png`. |
| `_wire_p226_handgrip_icons.py` | Handgrip Default/Ergo ApplyTo P226 → `Handgrip/P226_Handgrip_*.png`. |
| `_wire_p226_ironsight.py` | `JAZZ_IronSight` ApplyTo P226 (rear) → `Optics/P226_IronSight.png`. |
| `_wire_p226_ironsight_aim.py` | `JAZZ_IronSight_AIM` ApplyTo P226 → `Optics/P226_IronSight_AIM.png`. |
| `_wire_p226_ironsight_fast.py` | `JAZZ_IronSight_FAST` ApplyTo P226 → `Optics/P226_IronSight_FAST.png`. |
| `_wire_p226_ironsight_night.py` | `JAZZ_IronSight_NIGHT` ApplyTo P226 → `Optics/P226_IronSight_NIGHT.png`. |
| `_wire_fiveseven_mag_icons.py` | MagNormal ApplyTo FiveSeven → `Magazine/FiveSeven_Mag20.png` (slot later). |
| `_wire_barrel_normal_icons.py` | `JAZZ_BarrelNormal` Icon Style B + ChipIcon (was empty Chip / vanilla default_barrel). |
| `_wire_scorpion_icons.py` | MagNormal + StockLight Folded/UnFolded ApplyTo Scorpion → Mag20/Stock PNG. |
| `_wire_mac10_icons.py` | MagNormal + StockLight Folded/UnFolded ApplyTo MAC10 → Mag30/Stock PNG. |
| `_wire_aps_icons.py` | MagNormal APS → Mag18; BarrelNormal_Sil → APS_BarrelSil (comp Icon too). |
| `_wire_mat49_mag_icons.py` | MagNormal ApplyTo MAT49 → `Magazine/MAT49_Mag32.png`. |
| `_wire_mp40_mag_icons.py` | MagNormal ApplyTo MP40 → `Magazine/MP40_Mag32.png` (was magpictures). |
| `_wire_m3_mag_icons.py` | MagNormal ApplyTo M3GreaseGun → `Magazine/M3_Mag30.png` (no Mag slot yet). |
| `_wire_sterling_mag_icons.py` | MagNormal ApplyTo Sterling → `Magazine/Sterling_Mag34.png` (no Mag slot yet). |
| `_wire_stg44_mag_icons.py` | MagNormal ApplyTo STG44 → `Magazine/STG44_Mag30.png` (no Mag slot; mag in mesh). |
| `_wire_thompson_mag_icons.py` | MagNormal Thompson → Mag30; MagDrum_30_50_THOMPSON → MagDrum. |
| `_wire_pps43_mag_icons.py` | MagNormal ApplyTo PPS43 → `Magazine/PPS43_Mag35.png` (no Mag slot yet). |
| `_wire_mpl_mag_icons.py` | MagNormal ApplyTo MPL → `Magazine/MPL_Mag30.png`. |
| `_wire_m45_mag_icons.py` | MagNormal ApplyTo M45 (Carl Gustaf) → `Magazine/M45_Mag32.png`. |
| `_wire_agram_mag_icons.py` | MagNormal ApplyTo Agram2000 → `Magazine/Agram_Mag32.png`. |
| `_wire_famas_mag_icons.py` | MagNormal ApplyTo FAMAS → `Magazine/FAMAS_Mag25.png` (прямой F1). |
| `_wire_fg42_mag_icons.py` | MagNormal ApplyTo FG42 → `Magazine/FG42_Mag20.png` (no Mag slot; mag in mesh). |
| `_wire_svt_mag_icons.py` | MagNormal: SVT40→`SVT_Mag10`; AVT40→`SVT_MagLarge`. |
| `_wire_ar10_mag_icons.py` | MagNormal Visual AR10+AR10DMR → `Magazine/AR10_Mag20.png` (no Mag slot). |
| `_wire_m72law_icon.py` | M72LAW InventoryItem Icon → `WeaponIcons/M72LAW.png`. |
| `_wire_aug_mag_icons.py` | AUG MagNormal→Mag30; MagLarge_30_42→Mag42; MagQuick_AUG→MagQuick (+ remountable Inv Icons). |
| `_wire_hk33_icons.py` | HK33 Mag30/MagDrum + Handguards Style B; fix default HG Entity `HK33_HandGuardStock` (был `HK_33_Lower`). |
| `_wire_m16a2_handguard_icons.py` | JAZZ_Handguard ApplyTo M16A2 → `Handguard/M16A2_Handguard.png` (A2 ribbed). |
| `_wire_m1garand_enbloc_icons.py` | MagNormal ApplyTo M1Garand → `Magazine/M1Garand_Enbloc.png` (обойма; no Mag slot). |
| `_wire_uzi_icons.py` | MagDrum_30_50_UZI → UZI_MagDrum; StockLight Folded/UnFolded UZI → UZI_Stock. |
| `_wire_mp5_mag_icons.py` | MagNormal → MP5_Mag30; MagSmall30_15_MP5 → MP5_Mag15 на MP5/MP5K/MP5A2/MP5A4/MP5SD (+ ApplyTo MP5). |
| `_wire_berettam12_mag_icons.py` | MagNormal ApplyTo BerettaM12 → `Magazine/BerettaM12_Mag32.png`. |
| `_wire_spectrem4_mag_icons.py` | MagNormal ApplyTo SpectreM4 → `Magazine/SpectreM4_Mag50.png`. |
| `_wire_tmp_icons.py` | MagNormal/MagSmall30_15_TMP → TMP Mag30/Mag15; HolsterBelt Icon (был битый `belt.png`) + TMP Visual. |
| `_wire_holsterbelt_m16_icon.py` | HolsterBelt ApplyTo M16A1 Visual Icon (пустое General без ghost, если Icon только на компоненте). |
| `_wire_ump45_mag_icons.py` | MagNormal ApplyTo UMP45 → `Magazine/UMP45_Mag25.png` (insert Visual). |
| `_wire_p90_mag_icons.py` | MagNormal ApplyTo P90 → `Magazine/P90_Mag50.png`. |
| `_wire_mp7_mag_icons.py` | MagNormal ApplyTo MP7 → `Magazine/MP7_Mag30.png`. |
| `_wire_mini14_mag_icons.py` | MagNormal → Mini14_Mag20; MagLarge_20_30_MINI14 → Mini14_Mag30. |
| `_enable_remountable_bobby_ray.py` | Временный shop-pass: `CanAppearInShop` + Restock/MaxStock/Tier на remountable InventoryItems (dry-run / `--apply`). |
| `_apply_bobby_catalog.py` | ECON-004: apply Cost/Tier/RW/CAS/CategoryPair из `.tmp/bobby_*_prices.json` в companions + `items.lua`. `--dry-run` / `--apply`. |
| `_patch_bobby_econ004_items.py` | ECON-004: ModItemCode + Other SubCategories (Optics/…) + `TCE_Tier4/5Unlock` в `items.lua`. Idempotent. |
| `_audit_bobby_weapon_prices.py` | Аудит `Cost` active оружия (`weapons.csv` + GL/RL). `proposed` = канон `InventoryItem.Cost` для **Bobby и world** buy/sell; `shop=out_*` только вне витрины. `--json` / `--tsv`. |
| `_annotate_bobby_cas.py` | К `.tmp/bobby_weapon_prices.json` добавляет `cas_action`/`cas_label` (нужен ли `CanAppearInShop=false`). |
| `_gen_bobby_price_canvas.py` | Сборка canvas `bobby-ray-weapon-prices.canvas.tsx` из `.tmp/bobby_weapon_prices.json`. |
| `_audit_bobby_armor_prices.py` | Аудит брони: JazzArmor + plates + NVG/GasMask; `out_legion` (импровиз/рейдер), `out_special`, stubs. BR 1–5 + proposed Cost. `--json` / `--tsv`. |
| `_audit_bobby_ammo_prices.py` | Аудит `JAZZ_AMMO_*` + Flare: BR 1–5 по grade×caliber; out_craft/mortar/antique/dupe. `proposed` = stack Cost. `--json` / `--tsv`. |
| `_gen_bobby_ammo_canvas.py` | Сборка canvas `bobby-ray-ammo-prices.canvas.tsx` из `.tmp/bobby_ammo_prices.json`. |
| `_audit_bobby_consumables_prices.py` | Аудит медицины / инструментов / Meds·Parts: flat staples; specialty Surgical/Stim/Metaviron soft-tail. `--json` / `--tsv`. |
| `_audit_bobby_attach_prices.py` | Аудит remountable аттачей: Optics BR из design tiers; Mag/Muzzle/Side/Under heuristic; Cost=Parts×100; out integral/GL/irons. `--json` / `--tsv`. |
| `_gen_bobby_attach_canvas.py` | Сборка canvas `bobby-ray-attach-prices.canvas.tsx` из `.tmp/bobby_attach_prices.json`. |
| `_audit_bobby_explosive_prices.py` | Аудит TNT/C4/PETN + fused + grenades/demo/Warhead: soft-tail BR; cross BlackPowder/40mm/mortar. `--json` / `--tsv`. |
| `_gen_bobby_explosive_canvas.py` | Сборка canvas `bobby-ray-explosive-prices.canvas.tsx` из `.tmp/bobby_explosive_prices.json`. |
| `_audit_chip_palette.py` | Палитра/размер `Icons/Upgrades/Chips/JAZZ_*.png` (sanity для generation). |
| `_write_attach_design_human.py` | Пересбор `docs/design/attachments-by-category.md` из CSV. |
| `_build_attachments_catalog.py` | HTML-каталог `docs/tools/attachments-catalog.html`. |
| `_attach_live_summary.py` | JSON-сводка live comps (вспомогательный). |
| `_export_merc_salary_json.py` | Roster зарплат: vanilla AIM (`IsMercenary`) + Jazz/AME из `jazz-units` → `merc-salary-data.json` (Affiliation из `items.lua`). Нужен `JA3_ROOT`/ModTools для vanilla. |
| `_gen_merc_salary_calculator.py` | HTML-калькулятор `merc-salary-calculator.html`: `GetMercPrice` / daily / medical / duration discount (JAZZ maxDay=30) / squad sum. |

Типичный post-migrate конвейер:

```text
python docs/tools/_apply_attach_001.py --apply   # если ещё не применено
# python docs/tools/_promote_vanilla_refs.py   # только осознанно; иначе vanilla_ref OK
python docs/tools/_remove_handling_stat.py       # если нужно снять stat Handling
python docs/tools/_fix_items_lone_commas.py    # если после delete остались lone commas / stubs
python docs/tools/_export_attach_csv.py
python docs/tools/_audit_attach_ids.py
python docs/tools/_audit_attach_effects.py
python docs/tools/_write_attach_design_human.py
python docs/tools/_build_attachments_catalog.py
```

Официальный CSV import через Node (нужен установленный JA3):

```text
$env:JA3_ROOT = '<JA3 install>'
node scripts/docs/weapons-docs.mjs import --force
```

Без `JA3_ROOT` использовать `_export_attach_csv.py`.

## Карта / сектора jazz-maps

| Скрипт | Назначение |
| --- | --- |
| `export-jazz-maps-sectors.py` | Парсит `ModItemSector` из `../jazz-maps/items.lua` (+ index `metadata.lua`); пишет `sectors-runtime.json/.csv` в `docs/technical/maps/data/`. **Не** обходит `Maps/`. |
| `build-sector-atlas-docs.py` | Собирает атлас / трансфер / сверку sheet↔runtime (MD+CSV) из runtime JSON + снимка Google Sheet «Карта». |

```text
python docs/tools/export-jazz-maps-sectors.py
python docs/tools/build-sector-atlas-docs.py
```

Выход: `docs/technical/maps/sector-atlas.md`, `sector-transfer.md`, `sector-sheet-vs-runtime.md` и CSV в `docs/technical/maps/data/`.

## Прочие утилиты баланса / accuracy

| Скрипт | Назначение |
| --- | --- |
| `_soft_nerf_smg_aa.py` | Точечный nerf SMG AimAccuracy |
| `_apply_tier_acc_buffs.py` | Tier accuracy buffs |
| `_build_accuracy_html.py` | HTML по accuracy-модели |
| `_apply_buckshot_projectiles.py` | JAZZ-WEAPONS-006: `BuckshotProjectiles=1` на SG, ammo `target_prop` → `BuckshotProjectiles`, CombatAction/CSV; Auto/Burst снова 0. `--apply`. |
| `_verify_buckshot_projectiles.py` | Static AC-001..003 для WEAPONS-006. Exit 1 при FAIL. |
| `_fix_shotgun_pellet_autoshots.py` | **Superseded by 006** — старый hotfix AutoShots=1; не использовать. |
| `_rebalance_recoil_physical.py` | JAZZ-WEAPONS-003/008: mass/RPM/size/limiter → Recoil/Burst/Auto; SMG floor 12; Carbine + select-fire sniper rpm holefix; G36 lim=2; M16A2/A4/FAMAS/AUG/HK33/Sig550*/G3 lim=3; M2Carbine component-gated JAZZ_Autofire shot counts; token-safe attack match. `--apply` → `.bak`. |
| `_audit_weapons_rpm_holes.py` | WEAPONS-003 hole scan: select-fire/`MGBurst` with `cyclic_rpm=0`, Auto/Burst=0 with mode, known BurstLimiter drift, CSV↔companion, SMG mass/Long placeholders, spec anchors. |
| `_soften_ammo_jam.py` | JAZZ-WEAPONS-008: смягчает Poor/Crafted `BaseJamChance`/`Reliability` в `items.lua` + companions. `--apply`. |
| `_audit_weapon_jam_balance.py` | JAZZ-WEAPONS-010 static audit: soft-stack wear, quadratic −5pp service softener at 100%, softer mid steps, Rel 5..95, MP40 0/2/7/100, Mosin mid 8%/17% capped; Poor/Crafted ≤5% at perfect resource. |
| `_patch_jam_reliability_score.py` | Rewrite `JazzGetBaseJamScore` in `System_OR_Weapons.lua` (Rel clamp + Rel95 zero + scaled BaseJamChance); writes `.jamrel.new` then replaces when the game unlocks the file. |
| `_tmp_audit_smg_jam_feedback.py` | Discord audit: SMG Recoil distribution + Poor/Crafted JamScore scenarios. |
| `_audit_recoil_dist.py` | Static AC audit полей active firearms, recoil anchors, 9×19 differentiation и M16A2/AN94 limiters. |
| `_fix_madman_salary.py` | Jazz_Madman: `StartingSalary`/`SalaryLv1`/`SalaryMaxLv` в `jazz-units/items.lua` (companion править отдельно). |
| `_fix_free_merc_salaries.py` | Jazz_Grom / Jazz_Hitman: paid hire salaries в companion + `jazz-units/items.lua`. |
| `_sync_grom_rehire_chat.py` | Гром RehireIntro: убрать «бесплатный» из `items.lua` + `Russian.csv`. |
| `_sync_madman_chat_salary_strings.py` | Синк AIM-фраз Бешеного (не «бесплатный») в `items.lua` + `Russian.csv`/`English.csv`. |
| `_ship_colby_voices_ja2_only.py` | Jazz_Colby: пересобрать `jazz-units/voices/<T-id>.opus` **только** из JA2 Trevor WAV (`trevor.rar` / `trevor_extract/trevor`); пробелы — дубли родственных реплик. `--dry-run` / apply. |
| `_ship_ja2_merc_voices.py` | Batch: JA2/NightOps/JA2 Gold SLF + folder packs **или** `ja2mercs:…`. Combat=`SLOT_WAV`; AIM chat via `--aim-chat` / `--aim-chat-only`: classic `081–120`, MERK/RPC/Biff=`HIRE_FALLBACK_WAV`, UB ЦС=`UB_HIRE_PROXY_WAV`, Mike hire alt OLD pack. Never ATTN as hire. Map: `jazz_to_ja2_profile.csv` + folders CSV. **Never overwrite** `done_manual`: `spouke` / `lynx` / `tosca` / `spider`. |
| `_restore_lynx_tosca_spider_voices.py` | Restore original JA3 opus for `Jazz_Lynx` / `Jazz_Buzz` / `Jazz_Spider` from pre-remesh commit `a626ebc` (after accidental overwrite in `792d1c5`). Spouke untouched. |
| `_gen_ame_roster_60.py` | Генерация design-карточек AME: `docs/design/ame-roster-60.md`. Voice pool: Jazz remesh majority + `PierreMerc` + IMP minority (~1/8; VR → `IMP_*_01`). Assert: line troops = AllRounder/Autoriflemen/HeavyWeapons/Marksmen; soft specs только у Specialists. Sparse personality map **12/60**. |
| `_apply_ame_personality_traits.py` | Пишет Personality-tier perk (~12/60) в `jazz-units` UnitData companions + `items.lua`, сохраняя common traits. Dry-run / `--apply`. |
| `_verify_ame_personality.py` | Static assert: ровно 12 AME companions + items.lua содержат mapped Personality. |
| `_bump_metadata_last_changes.py` | Commit helper: `version` +1 and prepend `last_changes` bullet with escaped `\\n` (no raw LF). Args: metadata path, bullet, optional `--version-minor`. |
| `_ame_copy_bank.py` | Importable канон 60 самостоятельных RU+EN биографий и двуязычных profile blurbs; сам ничего не пишет. |
| `_export_ame_bio_copy_edits.py` | Проецирует 60 AME biography ID из copy-bank в `localization-copy-edits/ame_bios_bilingual.csv` для безопасного обновления обеих manual memories. |
| `_patch_ame_specializations.py` | Синхронизирует `Specialization` в `jazz-units/UnitData/JAZZ_AME_*.lua` + `items.lua` из roster generator **без** перезаписи зарплат/loc. |
| `_apply_ame_voice_remap.py` | Патчит только `VoiceResponseId`/`FallbackMissingVR` в `jazz-units` UnitData companions + `items.lua` из `voice_for()` roster (без regen bios/kits). |
| `_audit_ame_voices.py` | Аудит `VoiceResponseId` по 60 UnitData + 114 generated T/audio: opus exists, managed Context-ID set точно совпадает с items, без faction slogans, EN совпадает с audible donor phrase, RU — с `_ame_voice_subtitles_ru.py`. |
| `_audit_ame_copy.py` | Проверяет 60 самостоятельных RU/EN биографий и profile blurbs: 3–4 предложения, 38–105 слов, без stat/tier/meta copy и повторов; сверяет точную проекцию в roster, а с `--generated` ещё runtime CSV и `jazz-units/UnitData`. |
| `_verify_ame_voice_items_sync.py` | Сверка AME VR в `items.lua` vs companions. |
| `_ame_names_ru.py` | RU Name/Nick для AME (кириллица); используется `_gen_ame_unitdata.py` в RU/EN loc. |
| `_gen_ame_unitdata.py` | JAZZ-UNITS-005: из roster → `jazz-units/UnitData/JAZZ_AME_01..60.lua`, fixed `Loot_*`, items/metadata markers, nationality presets, RU/EN loc (имена RU из `_ame_names_ru.py`), placeholder portraits. Idempotent (`JAZZ-UNITS-005-AME-*`). |
| `_test_ame_contract.py` | Targeted lupa-harness для реальных AME Lua: синтаксис, детерминированное окно ровно 15 кандидатов, отдельная soft-guarantee Medic/Instructor/Sniper, защита нанятых, AME-only `My Team`, idempotent mail wrapper и обязательные поля сайта. Read-only; live PDA acceptance не заменяет. |
| `_apply_ame_weekly_salaries.py` | Playtest salary ladder: weekly bands → `StartingSalary` (week≈×7); writes all `UnitData/JAZZ_AME_*.lua`. Ceiling below Igor/Barry daily. |
| `_sync_ame_salary_items.py` | Copies companion `StartingSalary` into `jazz-units/items.lua` ModItem `'Id',"JAZZ_AME_NN"` blocks. |
| `_import_legion_raider_alt_voices.py` | Импорт Legion Raider alt takes `*-1.opus` (rar или `--dir Downloads/1`) → `jazz-units/voices/` (донор голоса для AME Male_Low). |
| `_ame_voice_subtitles_ru.py` | Канонический RU-перевод фактически слышимой donor-фразы для shared AME voice banks; не подменяет реплику текстом gameplay event. Неизвестная новая фраза — hard fail генератора. |
| `_gen_ame_voice_responses.py` | Три shared VR: `Jazz_AME_Male_Low` (Legion alt `*-1.opus`, без Legion/Major/Grand Chien takes), `Jazz_AME_Male_Hard`, `Jazz_AME_Female`. Remesh только подходящие слоты; Selection/Order/CombatMovement **omit** → тишина. EN совпадает с audio, RU берётся из `_ame_voice_subtitles_ru.py`; generated loc принадлежит стабильному Context и переиспользует те же IDs даже после CSV round-trip без comment markers. |
| `_gen_ame_appearances.py` | 60 `JAZZ_AME_NN` full regen from **vanilla** AP only; **1** синий акцент; Af head bank; без Legion war-paint / `GrandChien_Top_05`; red/extra-blue→slate; map `ame-appearance-map.json`. Policy: `docs/design/ame-appearance-assets.md`. |
| `_patch_ame_appearance_clothes_from_map.py` | Clothing shuffle from map: jazz-units **canon `Legion*`** + Rebels/GC/keep; preserve Head/BodyC1/HeadColor; strip helmets/turbans/balaclavas/`Equipment*_Hat`; ~12 male **berets** (earth, never blue); blue accent on non-camo Shirt/Chest/Armor/BodyC2/scarf — **not** Hat, **not** Hip pouches; camo earth + Recon chest carrier; ♀ `NPCFemale_Hair_*` or empty if Hat/Hat2. `--dry-run` / `--write-map-only`. Do **not** replace with bare `_gen_ame_appearances.py` (wipes jazz clothing). |
| `_audit_ame_appearance_clothes_qa.py` | Static QA: Irregular jazz `Legion*` lean; no war-paint/AIM hair/hat+hair/helmets/balaclavas/blue hips; beret count. |
| `_list_jazz_legion_appearances.py` | List handcrafted jazz-units `Legion*` AppearancePreset ids (canon pool). |
| `_audit_patch_ame_heads.py` | Repair pass по `jazz-units/items.lua` AME: pale/AIM heads, ♀-on-♂, war-paint bodies, pale-hand `GrandChien_Top_05`, gloves Shirt, BodyColor C1, HeadColor 0. `--dry-run` / `--sync-map` / `--verbose`. Exit 0 ⇒ `bad_after=0`. |
| `_audit_loot_upgrade_ids.py` | Audit `LootEntryUpgradedWeapon` upgrade IDs in `jazz-units/items.lua` vs known `JAZZ_*` WeaponComponent map. |
| `_apply_loot_upgrade_id_remap.py` | Remap legacy vanilla upgrade IDs on loot entries to `JAZZ_*` companions (dry-run default). |
| `_emit_ame_live_patch.py` | Emit pasteable live-Lua AppearancePreset patches for in-session AME head/body repair. |
| `_gen_ja12_appearances.py` | JAZZ-UNITS-002: same-gender mixes from BigPortrait cues. Prefer **faction/NPC body + head**, or AIM clone; **warn on AIM×AIM**. Skips `KEEP_HANDCRAFTED` (Lynx/Buzz/Spider/JAZZ_Spouke/Ivanov + vanilla Biff/Hitman/Simon→Shadow) unless `--force`. Map `ja12-appearance-map.json`. |
| `_purge_ja12_app_dupes.py` | Removes listed `ModItemAppearancePreset` ids that appear **before** `JAZZ-UNITS-002-JA12-APP` (avoid duplicate Mike/Horg when moving into generated folder). |
| `_list_appearance_donors.py` | Каталог donor AppearancePreset по категории/полу (для подбора JA12 recipes). |
| (manual) `_appearance-preset-rules.md` | WIP rules: gender lock (♂/♀ skeletons incompatible), recipe shape, index; visual slots in `_appearance-donor-visual-catalog.md`. |
| (manual) `_appearance-donor-visual-catalog.md` | Working visual catalog: preset id → gender + slots + look (AME browse). Includes **jazz-units** Legion* (through Sniper) + named + merc skins batch7–8 (`*_Savana`/`*_Jungle`/`*_DustStorm`/`*_Hot`/`*_Forest`/`*_Snake`, `Buzz`, `Spider`). Scratch: `.tmp/ame-crops/batch{3…8}_*`. |
| `_audit_ja12_appearance_links.py` | UnitData `AppearancesList` → shipped/vanilla preset ids + gender lock on JA12 section. |
| `_gen_ame_flags.py` | PNG флаги 128×80 для новых AME Nationality (`Icons/Flags/f_*.png`). |
| `_gen_ame_portrait_prompts.py` | JSONL prompt-bank 60 слотов → `jazz-units/MercPortraits/_ame_face_refs/prompts.jsonl`. |
| `_process_ame_portraits.py` | rembg BiRefNet + resize 2000 + bust_crop 300 из `*_Big_raw.png` (assets/_raw). |
| `_append_ame_mail_loc.py` | JAZZ-UI-AME-001: RU/EN Email strings `890000000006900–6910` (welcome + listing update). Idempotent upsert; proper multiline CSV. |
| `_append_merc_mail_loc.py` | JAZZ-UI-MERC-001: RU/EN Speck mail + MERC PDA strings `890000000009900+`. Idempotent upsert; multiline CSV. |
| `_remap_merc_loc_ids.py` | One-shot: move MERC loc off VoiceResponse `007xxx` → `009900+`; restore stolen VR rows from `HEAD`. |
| `_restore_vanilla_aim_vr_ids.py` | Restore vanilla T-IDs for AIM `ModItemVoiceResponse` Raven/Thor/Vicki/Wolf from `bb6d97a^` (LOC remap broke VO). Then run `_purge_restored_aim_vr_loc.py`. |
| `_purge_restored_aim_vr_loc.py` | After VR id restore: delete orphaned `8900*` rows from jazz + jazz-units CSV by record (multiline-safe), no full CSV rewrite. |
| `_apply_merc_affiliations.py` | UI-MERC-001: set `Affiliation = "MERC"` on Jazz shelf/world UnitData companions (+ Larry/Smiley overrides). |
| `_apply_ship_iggy.py` | UNITS-002: ship `Jazz_Iggy` (perk stub, loot clone Grom, UnitData+VR, Appearance, loc RU/EN, metadata bumps). Idempotent. Uses `_grom_snippets/`. |
| `_sync_merc_affiliation_items.py` | Sync same Affiliation into `jazz-units/items.lua` ModItem blocks. |
| `_fork_ame_template_to_merc.py` / `_polish_merc_template.py` | Fork/polish `System_MERC_Browser_Template.lua` from AME skin. |
| `_install_merc_xtemplate_moditem.py` | Install `PDAMERCBrowser` ModItemXTemplate + Emails + metadata code/resource (не Code-load шаблона). |
| `_update_ame_mail_sales_copy.py` | Канонические RU/EN письма AME + естественные listing pitches `6960–6984`; безопасно синхронизирует `AME_Welcome` / `AME_ListingUpdate`, сохраняя English source в `Text` обеих runtime CSV. |
| `_apply_ris_mail_emails.py` | Compatibility wrapper → полный `_apply_ris_editorial.py`; отдельный Phase A mail/copy bank удалён. |
| `_rewrite_ris_legion_briefs.py` | Отдельный канон 11 RU/EN supply briefs по loadout unlock map; loc IDs `11300…11321`. CLI делегирует полному `_apply_ris_editorial.py`, чтобы старый partial-run не рассинхронизировал CSV/catalog/items. |
| `_gen_legion_weapon_availability_map.py` | Build `docs/design/legion-weapon-availability-by-tier.md` from `weapons.csv` `tier_label` (11…33). |
| `_compose_legion_unit_portraits.py` | Compose 38 Legion unit Portrait PNGs (transparent 300×300, red-only): family mark inside shield at top-center, unified single-silhouette role glyph below it, tier dots under tip. Catalog + sheet/PSD masters → `jazz-units/EnemyPortraits/Legion/`. |
| `_audit_legion_unit_portraits.py` | Static + visual QA of all 38 portraits: alpha/color/slots/pip count/100px readability/duplicate types; writes design preview, `xN` overlay preview and QA report. |
| `_wire_legion_unit_portraits.py` | Set `Portrait` on all `JAZZ_Legion_*` UnitData companions + matching `items.lua` blocks to `Mod/Dv3mFVN/EnemyPortraits/Legion/<File>.png`. |
| `_dispatch_discord_player_update.ps1` | После agent `git push` в `main`: поллит до 90с; Discord run на SHA уже есть → exit. **Один пост на логическую фичу** (primary пакет); sibling с `[skip discord]`. `-SuitePackages jazz,jazz-units,jazz-nomaps` — список затронутых пакетов в поле Discord «Пакеты». `-Force`/`-AlwaysDispatch` только для явной перепубликации одного диапазона — не на все репы suite. |
| `_ris_copy_bank.py` | Единственный importable RU+EN канон R.I.S.: identity/sender 3, welcome 3, UI 13, AAR 60, field mail 7, 38+4 досье, 9 Strategy mails (`11322…11339`) и 8 support strings (`11340…11347`); сам ничего не пишет. |
| `_ris_dossier_copy.py` | Compatibility facade: только переэкспортирует public bank из `_ris_copy_bank.py`, собственной прозы не содержит. |
| `_apply_ris_editorial.py` | Канонический generated apply JAZZ-UI-RIS-002: Content Lua, 24 Email, ровно 9 Strategy metadata resources (старые `LegionTier1…5` удаляются), RU/EN runtime CSV, Strings и обе manual memory. Default = dry-run; `--check` возвращает 1 при drift; запись только с `--apply`; повторный apply идемпотентен. |
| `_apply_ris_dossier_copy.py` | Compatibility wrapper → полный `_apply_ris_editorial.py`; отдельной прозы и partial-write больше нет. |
| `_audit_ris_copy.py` | Read-only editorial audit: все категории и 218 RU/EN IDs, включая identity/sender, contiguous AAR 60 / field mail 7, 11 briefs, exact placeholders/signatures/reserved range, factual retired-phrase guards, CSV writer orientation, per-row review coverage и exact 9 Strategy texts vs design. `python -B docs/tools/_audit_ris_copy.py`; stdout + exit 0/1, файлов не пишет. |
| `_test_ris_contract.py` | Targeted lupa-harness для реальных R.I.S. Lua: синтаксис пяти loaded-файлов, Strategy observability/Awakening и inbox gate, engine-like old-save mail migration, delivery-gated dossiers, concurrent auto-resolve, двухфазный tactical snapshot с quest params/named fate и legacy AAR reconstruction. Read-only; live JA3/DAP не заменяет. |
| `../design/ris-editorial-style.md` | Канон голоса R.I.S.: бренд/подпись, RU/EN термины, placeholders, числа, уверенность, примеры mail/AAR и human-review checklist. |
| `_dump_ris_ru_strings.py` | Dump RIS-tagged Russian.csv strings for artistic review. |
| `_fix_ris_brief11_ru_calque.py` | Compatibility wrapper → полный `_apply_ris_editorial.py`; one-shot с устаревшим loc ID и текстом удалён. |
| `_audit_ris_brief_loc_ids.py` | Print brief Email T-ids vs Russian/English.csv columns (catch AME ID collisions). |
| `_apply_ris_phase_b.py` | Compatibility wrapper → полный `_apply_ris_editorial.py`; отдельный Phase B dossier/AAR bank удалён. |
| `_apply_ris_queue_field_mails.py` / `_fix_ris_sighting_loc.py` / `_fix_ris_english_csv_text_keys.py` | Compatibility wrappers → полный `_apply_ris_editorial.py`; старые partial copy/fix значения удалены. |

Порядок проверки и применения JAZZ-UI-RIS-002 (из корня `jazz/`):

```text
python -B docs/tools/_audit_ris_copy.py
python -B docs/tools/_apply_ris_editorial.py
# review полного dry-run; только после одобрения:
python -B docs/tools/_apply_ris_editorial.py --apply
python docs/tools/_validate_items_quick.py
python -B docs/tools/_apply_ris_editorial.py --check
python -B docs/tools/_test_ris_contract.py
```

`--check` до применения ожидаемо возвращает `1`, если есть drift; после успешного
apply обязан вернуть `0`. Legacy wrapper-команды не запускать для частичных волн:
они намеренно выполняют тот же полный pipeline.

| `_install_ame_xtemplate_moditem.py` | Ставит `PDAAIMEBrowser` как `ModItemXTemplate` в `items.lua` + `ModResourcePreset`; убирает Code-load шаблона (иначе XTemplate not found). После правок `System_AME_Browser_Template.lua` (в т.ч. savannah chrome). Replace через markers или, если editor их снял, по `id = "PDAAIMEBrowser"` (без дубля). Callable `re.sub` — plain string ломает Lua `\\n` в T(...). Затем `_validate_items_quick.py`. |
| `_theme_ame_pda_savannah.py` / `_fix_ame_xtemplate_imagecolor.py` | Helpers: savannah chrome на template; снять незаконный `ImageColor` с XFrame. |
| `_gen_ame_portrait_prompts.py` | AME identity prompt bank: roster → `jazz-units/MercPortraits/_ame_face_refs/prompts.jsonl` + README (60 unique `face_traits`, `big_prompt`/`bust_prompt` for GenerateImage; no image gen). |
| `_gen_ame_flags.py` | JAZZ-UNITS-005: Pillow → `Icons/Flags/f_{nigeria,kenya,angola,mali,congo,ghana,senegal,ethiopia}.png` (128×80 simplified UI flags). |
| `_audit_ame_kit_tiers.py` | Аудит китов `ame-roster-60.md` vs потолки `tier_label`: Irr ≤1-2, Fight ≤1-3, Hard/Spec ≤2-1 (`weapons.csv`). |
| `_ja2mercs_folder_map.py` | Canonical Jazz→ja2mercs (1) pid-prefixed folder map (remesh / skip_*). Writes `jazz_to_ja2mercs_folders.csv`. |
| `_apply_ja2mercs_profile_map.py` | Apply folder map onto `jazz_to_ja2_profile.csv` (`speech_source`/`profile_id`/`status`). `--dry-run`. |
| `_wire_ja12_chat_voice_tags.py` | WIP UnitData/items compact chat `T(id,"…")` → `voice:Jazz_*` comments. `--apply` / `--dry-run` / `--only`. |
| `_clear_ja12_selection_chat_donors.py` | Delete AIM-chat opus that byte-duplicates Selection; preserve owner-approved same-voice fallback remesh. `--strict-hire-only` restores no-081–120 purge; `--apply` / `--dry-run`. |
| `_import_ja2mercs_subtitle_bank.py` | Import ja2mercs `*.txt` → `_voice-source/subtitles/<slug>.csv` (line index = SPEECH stem; encoding utf-8/cp1251). |
| `_apply_ja12_subtitles.py` | Apply subtitle CSV → UnitData/items `T()` + `Russian.csv` via `AIM_CHAT_WAV`/`SLOT_WAV`. `--only` / `--slots chat,combat` / `--apply`. |
| `_integrate_sj_khalif_mercs.py` | Shady Job `Downloads/SJ/data`: кэш → `_sj_cache`, mercedt CSV, UnitData/VR stubs Benny+Simon, ship Grom/Benny/Simon opus. WF AIM в SJ SPEECH нет. |
| `_extract_sj_sti_faces.py` | Decode SJ `faces/bigfaces/{66,67}.sti` (+ `b66`/`b67`) → `docs/design/mercs-ja12/{simon,benny}.ja2-face.png` + `_face-source/sj/`. Indexed STCI ETRLE. |
| `_process_ja12_facefix_portraits.py` | Preserve eight generated JA12 face-fix raws, cut with local BiRefNet, emit 2000/300 RGBA candidates + contact sheet under `jazz-units/MercPortraits/_wip/ja12-facefix/`; `--crop-only`, explicit `--apply` for runtime art. |
| `_fill_sj_chat_voices.py` | Copy Selection opus onto missing Benny/Simon/Grom AIM-chat T-ids (`--apply`). |
| `_fill_ja12_chat_voices.py` | Wrapper: `_ship_ja2_merc_voices.py --aim-chat-only` (classic/fallback/ub-proxy; not Selection). `--apply` / `--dry-run` / `--only`. |
| `_pour_ja12_design_hire_chat.py` | Pour AIM-chat RU/EN from `docs/design/mercs-ja12/<slug>.md` → UnitData + `items.lua` + RU/EN CSV; sync missing PartingWords. `--apply` / `--only`. |
| `_pour_ja12_design_identity_bio.py` | JAZZ-LOC-002: source-aware pour of RU/EN `Identity.Name` + `Bio` for the 42 approved `ready`/`executable` JA12 mercs. Preserves T-ids and unrelated bytes in UnitData/`items.lua`, emits `localization-copy-edits/ja12_identity_bio.csv`, and never edits runtime RU/EN CSV. `--dry-run` / `--apply` / `--check`. |
| `_stt_hire_chat_lines.py` | faster-whisper STT of hire stems → UnitData chat text (Quinten/Highball). `--apply` / `--only` / `--model`. |
| `_expand_ja2_merc_vr_full.py` | Expand stub (~12-slot) Jazz_* VoiceResponse to Colby-like combat coverage (~52 slots / 74 lines); allocates T-ids + RU/EN. Skips Colby/Spouke/need_pack/full VR. Then run `_ship_ja2_merc_voices.py`. |
| `_audit_ja12_merc_voices.py` | Read-only audit: Jazz_* VR T-ids vs `voices/<tid>.opus`, CSV ship status, TranslatedVoices mount, `g_VoiceVariations`. `--critical` for Selection/Aim/Movement. |
| `_audit_ja12_hire_chat_voices.py` | Read-only AIM-chat audit: UnitData T-ids vs shipped opus, per-merc `OK`/`PARTIAL`/`SILENT`, source mode and missing-slot summary. `--only` / `--fail-on-silent`. |
| `_inject_sj_benny_simon_vr.py` | Inject missing Benny/Simon `ModItemVoiceResponse` folders into `jazz-units/items.lua` (UnitData already via companion). |
| `_fix_benny_simon_tid_collision.py` | Remap Benny/Simon T-ids if they collided with an expand batch (safe re-run). |
| `_inject_vr_stubs_ja2_voices.py` | Для ready-мерков с пустым `ModItemVoiceResponse` — Ira-like stub (12 линий) из mercedt/NO EDT + T-ids `8900…6300+` в `jazz-units/items.lua` и RU/EN CSV. UB/ЦС без текстов — fallback-строки. |
| `_repair_ja2_voice_remaps.py` | Repair remaps: снять wrong Malice opus с `Jazz_Gaston` (FallbackMissingVR); обновить VR-тексты + re-ship `nervous`→041 / `hitman`→064 (Slay). `--dry-run` / `--skip-ship`. |
| `_audit_nightops_speech_coverage.py` | Аудит SPEECH/BATTLESNDS/NO overlays + внешние `_ub_cs_cache` (ЦС) / `_horg_stogie_cache` (Бычок). Identity по RU greeting/self-ID в mercedt, **не** по EDT filename (они часто врут). |
| `_extract_ja2_mercedt.py` | Распаковать/расшифровать `MERCEDT.SLF` (JA2 / NightOps) → UTF-8 CSV субтитров `000`..`116` в `docs/design/mercs-ja12/_voice-source/ja2no-mercedt/`. |
| `_extract_wildfire_rus_arc.py` | FreeArc extract `Jagged_Alliance_2_1_13_Wildfire_RUS.arc` (7z не открывает) через PeaZip `Arc.exe` → `_voice-source/_wildfire_cache/` (SPEECH/MercEdt + Data-UB). Это 1.13 RUS+WF maps, не commercial WF AIM VO; Gaston = Data-UB/058. |
| `_inventory_ja2mercs.py` | Read-only inventory `Downloads/ja2mercs (1)/ja2mercs`: layout (flat/nested), audio counts/formats, profile-id guess, crosswalk к `jazz_to_ja2_profile.csv`. Не ship/convert. `--root` optional. Remesh: `_apply_ja2mercs_profile_map.py` + `_ship_ja2_merc_voices.py --ja2mercs-remesh`. |
| `_stt_ja2mercs_sample.py` | Pilot subtitles for ja2mercs: export XLSX/mercedt ref text + optional faster-whisper RU STT (ADPCM→PCM via ffmpeg). Default pilot `но-шж/гром` pids 076+047 (both Grom). `--no-stt` = refs only. Out: `_voice-source/_stt/`. |
| `_audit_truncated_voice_responses.py` | Find JA2-style ~80-char mid-cut VoiceResponse strings in `English.csv`; match full RU from `ja2mercs (1)` XLSX (+ known STT repairs for Carlos/Devin). Report only → `_tmp_truncated_vr_strict.txt`. |
| `_apply_trunc_vr_and_lore_names.py` | Apply Grandier/Грандье + Khalif lore canon and truncated VR repairs into `jazz-units` `T()` + `Russian.csv`/`English.csv` (+ Manual). Canon: Grandier / Кавалье / Khalif. |

## Артефакты

- `_attach_001_audit.tsv` — dry-run/apply audit от `_apply_attach_001.py`
- `attachments-catalog.html` — generated catalog
- `_attach_*.json` — промежуточные summary (можно регенерировать)
- `merc-salary-data.json` / `merc-salary-calculator.html` — калькулятор зарплат AIM/AME/MERC (`python docs/tools/_export_merc_salary_json.py` → `_gen_merc_salary_calculator.py`)

## Добавление нового скрипта

1. Положить в `docs/tools/` с говорящим именем (`_apply_…`, `_export_…`, `_audit_…`, `_remove_…`).
2. Docstring в шапке: что делает, dry-run/apply, откуда читать, куда писать.
3. Строка в этой таблице.
4. При системной процедуре — ссылка в `.agents/docs/playbooks/…` и при необходимости в `.agents/docs/index.md`.

| `_loc_csv_io.py` | Safe read/write for `Russian.csv`/`English.csv`: **never** `splitlines()` before `csv.DictReader` (that flattens multiline AdditionalHint / perk text). |
| `_fix_dup_loc_ids_ame_perk_mag.py` | CommonLib «duplicated loc IDs»: JA2 perks off AME `5009–5028` → `5029–5048`; AME copyright → `5049`; Bleeding Text=EN; nationalities T()=EN; mag/parts Text↔T() align. |
| `_fix_dup_loc_ids_ame_perk_wave2.py` | Wave2: Meat/Carlos/Devin/Shank off AME filter `5001–5008` → `5050–5057`; English.csv AME Text = T() source. |
| `_fix_mag_hint_loc_align.py` | Mag/parts `AdditionalHint` only (`JAZZ_Mag*`, Scope/Barrel parts): unify family-prefix vs short T() + RU/EN CSV. **Не** сканирует весь `InventoryItem/` (иначе EN→RU Translation у Bandage/Medkit и vanilla stomps). |
| `_audit_additionalhint_newlines.py` | Audit/restore weapon `AdditionalHint` bullets: compare `InventoryItem/**/*.lua` `\n` vs CSV; `--apply` inserts newlines before bullet markers. |
| `_restore_csv_newlines_from_head.py` | Restore any CSV cell newlines lost vs `HEAD` when wording still matches (whitespace-insensitive). `--apply`. |
| `_purge_workshop_aim_mercs.py` | One-shot purge of six Steam Workshop AIM mercs from jazz + jazz-units (ModItems, companions, voices, loc, design). |
| _dump_legion_unit_dossiers.py | Dump Legion UnitData dossiers for design catalog. |
| _check_carlos_iggy.py / _check_iggy_insert.py | Verify Iggy/Carlos UnitData insert integrity. |
| _find_grom_id.py / _probe_grom_loot.py | Locate Grom UnitData/loot wiring. |
| _purge_restored_aim_vr_loc.py / _restore_vanilla_aim_vr_ids.py | AIM VR localization ID restore/purge helpers. |
