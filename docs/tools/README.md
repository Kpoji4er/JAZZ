# `docs/tools` — скрипты агентов и аудита

Рабочие утилиты для generated data, аттачей, CSV и design-артефактов.  
Политика хранения: `.agents/docs/reference/agent-tooling.md`, `.cursor/rules/jazz-agent-tooling.mdc`.

Запуск из корня пакета `jazz/` (если не указано иное).

| `_fix_zastava_m92_csv.py` | WEAPONS-003 hotfix: `ZastavaM92` `burst_shots=4` `auto_shots=7` `cyclic_rpm=700` in `weapons.csv`. |
| `_bump_metadata_revision.py` | `metadata.lua` Revision +1 + prepend `last_changes` bullet (`--bullet`, escape `\\n` only). |

## FortifyErnie / stationary MG

| Скрипт | Назначение |
| --- | --- |
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
| `_check_ai_medic_bandage.py` | Static: Medic/Medic_Low Healer exclusive + Early + MaxHp 85; combat Score helpers; `AISelectHealTarget` / `AIActionBandage` Precalc; `JazzAI_TryMedicSwitch` all bleed tiers. |
| `_check_sniper_hold_001.py` | Static JAZZ-AI-SNIPER-001: ExtremeRange; stay-hold; useless streak soft HighGround/stay weights (no hard escape). |
| `_bump_sniper001_meta.py` | Revision +1 + prepend `last_changes` bullet for SNIPER-001 commit. |
| `_apply_medic_heal_first.py` | Patch `jazz-units/items.lua` Medic/Medic_Low: combat behaviors Score=0 when heal needed; Healer Early/Weight 1000; Priority Bandage before MobileShot; SelfHealMod 100. |
| `_key_med_item_icons.py` | Flood-fill near-black → alpha для `Icons/Items/JAZZ_{Bandage,Morphine,IFAK,Medkit,SurgicalKit}.png` (не трогает тёмные молнии/ремни). |
| `_apply_med001_loot_jazz_units.py` | В `jazz-units/items.lua` к LootDef с `FirstAidKit`/`Medkit`/`Meds`/`MedsDrop` добавляет `JAZZ_Bandage` / `JAZZ_Morphine` / редко `JAZZ_SurgicalKit`. Идемпотентен (сначала снимает старые JAZZ med entries). |
| `_apply_med001_loot_equipment_kits.py` | Phase 2: бинт/морфий (± IFAK у мерков) в Equipment-киты без медицины (`loot=all` враги + Mercs leaf tiers). Не трогает ammo/Drop_/Armor. Merc insert: Bandage 10, IFAK 5. |
| `_apply_merc_med_full_stacks.py` | Mercs `group=Mercs` в `jazz-units/items.lua`: существующий `JAZZ_Bandage` → stack 10; `FirstAidKit` → 5; `Medkit` → 3 (MaxStacks). Идемпотентен. |
| `_apply_enemy_med_stacks_min.py` | Не-Mercs LootDef: `JAZZ_Bandage` / Morphine / Surgical / FirstAidKit / Medkit → `stack_min/max = 1`. Mercs не трогает. |
| `_fix_med001_loot_drop_lists.py` | Снимает ошибочные JAZZ med entries с `Drop_*` / Comment=list ammo pools; патчит `PierreGuard_Ordnance`. |
| `_audit_med001_loot_jazz_units.py` / `_audit_med001_unit_kits.py` | Аудит покрытия Bandage по medical LootDef и UnitData Equipment. |
| `_audit_loot_missing_items.py` | `jazz-units` `item=` vs known InventoryItem IDs (jazz `InventoryItem/` + vanilla ModTools defs). Exit 1 если есть MissingItem-кандидаты. |
| `_patch_med_stack_kit_loc.py` | MED stack kits: RU/EN hint «refill with Meds» → «one use = one item»; append `890000000010030` (Reanimationsset). |
| `_fix_med001_loot_braces.py` | Чинит `}}),` → `}),` на строках JAZZ med loot (баг f-string). |
| `_bump_units_med_loot_meta.py` | Bump `jazz-units/metadata.lua` Revision + `last_changes` после loot apply. |
| `_wire_med001_traumas.py` / `_append_med001_trauma_loc.py` | Wiring/loc зональных Trauma* эффектов. |
| `_apply_grenade_concussion.py` / `_append_grenade_concussion_loc.py` / `_patch_he_grenade_concussion_hint_loc.py` / `_fix_concussion_loc_ids_items.py` / `_patch_grenade_concussion_guaranteed_loc.py` | Playtest: `Concussion` CharacterEffect + items/metadata; RU/EN loc `890000000010277–280`; Frag/HE hints. Runtime: `JazzTryApplyExplosionConcussionAndTrauma` (concussion guaranteed). Loc patch: chance→guaranteed on IDs `243383619902` / `663236691841`. |
| `_apply_officer_aura_loc.py` | CMD-001 UI: RU/EN `890000000006100–6117` (OfficerAura / Influence; directive labels incl. OccupyBuildings/TakeCover/GoHidden; current-order tooltip; no-order fallback). |
| `_apply_jazz_trauma_effect_parent.py` | Trauma* → parent/`object_class` `JazzTraumaEffect` (companions + `items.lua`); paired with early `Code/System_JazzTraumaEffect.lua`. |
| `_audit_trauma_loc_ids.py` | Trauma* + medicine timing T() IDs vs `Russian.csv`/`English.csv` (Text match, non-empty Translation, no garbage). Exit 1 if broken. |
| `_patch_med001_hit_pain_ac.py` | MED-001: insert AC-012 (+ fix REQ-010 backticks) for `JazzPainOnDamagingHit` contract. |
| `_fix_med001_runtime_csv.py` | MED-001: чинит `Russian.csv` Text/Translation (EN source / RU translation) + literal `\\n` → реальные переносы в AdditionalHint. |
| `_fix_med_en_in_ru_loc.py` | Playtest: восстанавливает RU Translation для MED AdditionalHint (`010013/016/019/024/027/030`) + Concussion `010277–280`; снимает `mag-hint-aligned` vanilla stomps EN-in-RU. |
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
| `_gen_setweaponcomponent_override.py` | Генерирует `Code/System_WeaponComponent_Set.lua` из vanilla `FirearmBase:SetWeaponComponent` + ветка `ModificationType=Set`. |
| `_validate_wave_weapons.py` | Статическая валидация волны ATTACH-001 MagSizeSet + WEAPONS-002..005 (якоря, metadata load, loc, CSV). |
| `_peek_mag45_kobra.py` / `_peek_mag45_kobra2.py` / `_list_reload_effects.py` | Peek Mag45 / Reflex_Cobra effects+params и Reload* effect presets в `items.lua`. |
| `_fix_stock_barrelparts_costs.py` | WEAPONS-002: `JAZZ_BarrelParts` в AdditionalCosts только у Slot=Barrel; остальное → `Parts`. `--apply` + `.bak_stock_barrelparts`. |
| `_make_barrelparts_icon.py` | Иконка `JAZZ_BarrelParts`: extract `fine_steel_pipe.dds` из `UI.hpk`, charcoal recolor → `Icons/Items/JAZZ_BarrelParts.png`, wiring companion/`items.lua`. |
| `_purge_legacy_gunsmith_parts.py` | WEAPONS-002: безопасный remap только `'Type'`/`'item'` в costs (`FineSteelPipe`→`JAZZ_BarrelParts`, lens/chip→`Parts`); **не** трогает `'Id'`. `--restore-bak` из `items.lua.bak_legacy_parts`; dormant shop на legacy defs. `--apply`. |
| `_verify_gap_fixes.py` | Smoke после wave gaps: Id uniqueness Parts/BarrelParts, Type leftovers, unique WeaponMass. |
| `_verify_nomaps_unit_remap_named_skip.py` | COMPAT-004: static mirror remap families — Bastien skip; `WeakFlagHill`→assault; `*_Tutorial` stems; Hyena skip. |
| `_verify_nomaps_fortress_pierre_squad.py` | NoMaps: `FortressPierre` must stay out of `SQUAD_REMAP` (vanilla Pierre boss; not `LegionJAZZSquadT2`). |
| `_verify_guardpost_scripted_attack.py` | Guardpost: `ForceSet` does not call `CanSpawnNewSquad`; managed early-out kept on CanSpawn/Update/Spawn (scripted Ernie attack OK, vanilla auto muted). |
| `_verify_nomaps_early_squad.py` | COMPAT-005: `LegionJAZZSquadT1_Early` all `T1_`; metadata Id; NoMaps remap/cap wiring. |
| `_verify_nomaps_globals_predeclare.py` | NoMaps wrap flags predeclared at file top + `rawset` + `lQuestVarSafeSet`. |
| `_verify_nomaps_region_radius.py` | COMPAT-007: `AUTO_REGION_RADIUS=false` (unbounded Voronoi), `AI_REGION_REV=2`, multi-outpost refresh; no legacy `<= 8`. |
| `_audit_loot_item_case.py` | `jazz-units` LootEntry `item=` vs `InventoryItem` DefineClass (ловит `Mas36`≠`MAS36`). Exit 1 при mismatch. |
| `_audit_faction_overlay_static.py` | Static AC hooks for STRATEGY-014/018: matrix API, ownership, avoid-player routing, load registration. |
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
| `_validate_items_quick.py` | Быстрый структурный check `items.lua`/`metadata.lua` (lone commas, braces, stacked closers, **missing comma before PlaceObj**, **raw newline inside quoted strings**, corrupt `id = }),`) без JA3. **Обязателен после mass apply / family split**. Опционально: `python docs/tools/_validate_items_quick.py [pkg…]` (напр. `.` и `../jazz-units`). |
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
| `_audit_chip_palette.py` | Палитра/размер `Icons/Upgrades/Chips/JAZZ_*.png` (sanity для generation). |
| `_write_attach_design_human.py` | Пересбор `docs/design/attachments-by-category.md` из CSV. |
| `_build_attachments_catalog.py` | HTML-каталог `docs/tools/attachments-catalog.html`. |
| `_attach_live_summary.py` | JSON-сводка live comps (вспомогательный). |

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
| `_rebalance_recoil_physical.py` | JAZZ-WEAPONS-003/008: authoring mass/RPM/size/limiter и physical Recoil/Burst/Auto; SMG placeholder reject + floor 12; **Carbine** class default + ignore csv `cyclic_rpm=0` when Burst/Auto exist; G36/G36c `BurstLimiter=2`; пишет CSV/companions/items. `--apply` → `.bak`. |
| `_soften_ammo_jam.py` | JAZZ-WEAPONS-008: смягчает Poor/Crafted `BaseJamChance`/`Reliability` в `items.lua` + companions. `--apply`. |
| `_tmp_audit_smg_jam_feedback.py` | Discord audit: SMG Recoil distribution + Poor/Crafted JamScore scenarios. |
| `_audit_recoil_dist.py` | Static AC audit полей active firearms, recoil anchors, 9×19 differentiation и M16A2/AN94 limiters. |
| `_fix_madman_salary.py` | Jazz_Madman: `StartingSalary`/`SalaryLv1`/`SalaryMaxLv` в `jazz-units/items.lua` (companion править отдельно). |
| `_fix_free_merc_salaries.py` | Jazz_Grom / Jazz_Hitman: paid hire salaries в companion + `jazz-units/items.lua`. |
| `_sync_grom_rehire_chat.py` | Гром RehireIntro: убрать «бесплатный» из `items.lua` + `Russian.csv`. |
| `_sync_madman_chat_salary_strings.py` | Синк AIM-фраз Бешеного (не «бесплатный») в `items.lua` + `Russian.csv`/`English.csv`. |
| `_ship_colby_voices_ja2_only.py` | Jazz_Colby: пересобрать `jazz-units/voices/<T-id>.opus` **только** из JA2 Trevor WAV (`trevor.rar` / `trevor_extract/trevor`); пробелы — дубли родственных реплик. `--dry-run` / apply. |
| `_ship_ja2_merc_voices.py` | Batch: JA2/NightOps/JA2 Gold SLF + folder packs **или** `ja2mercs:…`. Combat=`SLOT_WAV`; AIM chat via `--aim-chat` / `--aim-chat-only`: classic `081–120`, MERK/RPC/Biff=`HIRE_FALLBACK_WAV`, UB ЦС=`UB_HIRE_PROXY_WAV`, Mike hire alt OLD pack. Never ATTN as hire. Map: `jazz_to_ja2_profile.csv` + folders CSV. **Never overwrite** `done_manual`: `spouke` / `lynx` / `tosca` / `spider`. |
| `_restore_lynx_tosca_spider_voices.py` | Restore original JA3 opus for `Jazz_Lynx` / `Jazz_Buzz` / `Jazz_Spider` from pre-remesh commit `a626ebc` (after accidental overwrite in `792d1c5`). Spouke untouched. |
| `_gen_ame_roster_60.py` | Генерация design-карточек AME: `docs/design/ame-roster-60.md`. Voice pool: Jazz remesh majority + `PierreMerc` + IMP minority (~1/8; VR → `IMP_*_01`). Assert: line troops = AllRounder/Autoriflemen/HeavyWeapons/Marksmen; soft specs только у Specialists. |
| `_patch_ame_specializations.py` | Синхронизирует `Specialization` в `jazz-units/UnitData/JAZZ_AME_*.lua` + `items.lua` из roster generator **без** перезаписи зарплат/loc. |
| `_apply_ame_voice_remap.py` | Патчит только `VoiceResponseId`/`FallbackMissingVR` в `jazz-units` UnitData companions + `items.lua` из `voice_for()` roster (без regen bios/kits). |
| `_audit_ame_voices.py` | Сводка `VoiceResponseId` по `UnitData/JAZZ_AME_*.lua` (IMP / Jazz / other counts). |
| `_verify_ame_voice_items_sync.py` | Сверка AME VR в `items.lua` vs companions. |
| `_ame_names_ru.py` | RU Name/Nick для AME (кириллица); используется `_gen_ame_unitdata.py` в RU/EN loc. |
| `_gen_ame_unitdata.py` | JAZZ-UNITS-005: из roster → `jazz-units/UnitData/JAZZ_AME_01..60.lua`, fixed `Loot_*`, items/metadata markers, nationality presets, RU/EN loc (имена RU из `_ame_names_ru.py`), placeholder portraits. Idempotent (`JAZZ-UNITS-005-AME-*`). |
| `_apply_ame_weekly_salaries.py` | Playtest salary ladder: weekly bands → `StartingSalary` (week≈×7); writes all `UnitData/JAZZ_AME_*.lua`. Ceiling below Igor/Barry daily. |
| `_sync_ame_salary_items.py` | Copies companion `StartingSalary` into `jazz-units/items.lua` ModItem `'Id',"JAZZ_AME_NN"` blocks. |
| `_import_legion_raider_alt_voices.py` | Импорт Legion Raider alt takes `*-1.opus` (rar или `--dir Downloads/1`) → `jazz-units/voices/` (донор голоса для AME Male_Low). |
| `_gen_ame_voice_responses.py` | Три shared VR: `Jazz_AME_Male_Low` (Legion alt `*-1.opus`, без Legion/Major takes), `Jazz_AME_Male_Hard`, `Jazz_AME_Female`. Remesh только подходящие слоты; Selection/Order/CombatMovement **omit** → тишина. UnitData `FallbackMissingVR` = Legion/Army/Anne (Pain only, не Ice/Fox). |
| `_gen_ame_appearances.py` | 60 `JAZZ_AME_NN`; **1** синий акцент (Hat/Hat2/Shirt/BodyC2, не Pants); узкий Af bank (Chimurenga/Pierre/Jackhammer/`Head_M_IMP_01`/Rebel medic — **не** Flay/Fidel/Magic/Blood); без Legion war-paint / `GrandChien_Top_05`; red/extra-blue→slate; BodyC1 dark; HeadColor 0; map `ame-appearance-map.json`. Policy: `docs/design/ame-appearance-assets.md`. |
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
| `_install_ame_xtemplate_moditem.py` | Ставит `PDAAIMEBrowser` как `ModItemXTemplate` в `items.lua` + `ModResourcePreset`; убирает Code-load шаблона (иначе XTemplate not found). После правок `System_AME_Browser_Template.lua` (в т.ч. savannah chrome). Replace через callable `re.sub` — plain string ломает Lua `\\n` в T(...). Затем `_validate_items_quick.py`. |
| `_theme_ame_pda_savannah.py` / `_fix_ame_xtemplate_imagecolor.py` | Helpers: savannah chrome на template; снять незаконный `ImageColor` с XFrame. |
| `_gen_ame_portrait_prompts.py` | AME identity prompt bank: roster → `jazz-units/MercPortraits/_ame_face_refs/prompts.jsonl` + README (60 unique `face_traits`, `big_prompt`/`bust_prompt` for GenerateImage; no image gen). |
| `_gen_ame_flags.py` | JAZZ-UNITS-005: Pillow → `Icons/Flags/f_{nigeria,kenya,angola,mali,congo,ghana,senegal,ethiopia}.png` (128×80 simplified UI flags). |
| `_audit_ame_kit_tiers.py` | Аудит китов `ame-roster-60.md` vs потолки `tier_label`: Irr ≤1-2, Fight ≤1-3, Hard/Spec ≤2-1 (`weapons.csv`). |
| `_ja2mercs_folder_map.py` | Canonical Jazz→ja2mercs (1) pid-prefixed folder map (remesh / skip_*). Writes `jazz_to_ja2mercs_folders.csv`. |
| `_apply_ja2mercs_profile_map.py` | Apply folder map onto `jazz_to_ja2_profile.csv` (`speech_source`/`profile_id`/`status`). `--dry-run`. |
| `_wire_ja12_chat_voice_tags.py` | WIP UnitData/items compact chat `T(id,"…")` → `voice:Jazz_*` comments. `--apply` / `--dry-run` / `--only`. |
| `_clear_ja12_selection_chat_donors.py` | Delete AIM-chat opus that is Selection-copy or merc has no hire 081–120 (silent > ATTN). `--apply` / `--dry-run`. |
| `_import_ja2mercs_subtitle_bank.py` | Import ja2mercs `*.txt` → `_voice-source/subtitles/<slug>.csv` (line index = SPEECH stem; encoding utf-8/cp1251). |
| `_apply_ja12_subtitles.py` | Apply subtitle CSV → UnitData/items `T()` + `Russian.csv` via `AIM_CHAT_WAV`/`SLOT_WAV`. `--only` / `--slots chat,combat` / `--apply`. |
| `_integrate_sj_khalif_mercs.py` | Shady Job `Downloads/SJ/data`: кэш → `_sj_cache`, mercedt CSV, UnitData/VR stubs Benny+Simon, ship Grom/Benny/Simon opus. WF AIM в SJ SPEECH нет. |
| `_extract_sj_sti_faces.py` | Decode SJ `faces/bigfaces/{66,67}.sti` (+ `b66`/`b67`) → `docs/design/mercs-ja12/{simon,benny}.ja2-face.png` + `_face-source/sj/`. Indexed STCI ETRLE. |
| `_fill_sj_chat_voices.py` | Copy Selection opus onto missing Benny/Simon/Grom AIM-chat T-ids (`--apply`). |
| `_fill_ja12_chat_voices.py` | Wrapper: `_ship_ja2_merc_voices.py --aim-chat-only` (classic/fallback/ub-proxy; not Selection). `--apply` / `--dry-run` / `--only`. |
| `_pour_ja12_design_hire_chat.py` | Pour AIM-chat RU/EN from `docs/design/mercs-ja12/<slug>.md` → UnitData + `items.lua` + RU/EN CSV; sync missing PartingWords. `--apply` / `--only`. |
| `_stt_hire_chat_lines.py` | faster-whisper STT of hire stems → UnitData chat text (Quinten/Highball). `--apply` / `--only` / `--model`. |
| `_expand_ja2_merc_vr_full.py` | Expand stub (~12-slot) Jazz_* VoiceResponse to Colby-like combat coverage (~52 slots / 74 lines); allocates T-ids + RU/EN. Skips Colby/Spouke/need_pack/full VR. Then run `_ship_ja2_merc_voices.py`. |
| `_audit_ja12_merc_voices.py` | Read-only audit: Jazz_* VR T-ids vs `voices/<tid>.opus`, CSV ship status, TranslatedVoices mount, `g_VoiceVariations`. `--critical` for Selection/Aim/Movement. |
| `_inject_sj_benny_simon_vr.py` | Inject missing Benny/Simon `ModItemVoiceResponse` folders into `jazz-units/items.lua` (UnitData already via companion). |
| `_fix_benny_simon_tid_collision.py` | Remap Benny/Simon T-ids if they collided with an expand batch (safe re-run). |
| `_inject_vr_stubs_ja2_voices.py` | Для ready-мерков с пустым `ModItemVoiceResponse` — Ira-like stub (12 линий) из mercedt/NO EDT + T-ids `8900…6300+` в `jazz-units/items.lua` и RU/EN CSV. UB/ЦС без текстов — fallback-строки. |
| `_repair_ja2_voice_remaps.py` | Repair remaps: снять wrong Malice opus с `Jazz_Gaston` (FallbackMissingVR); обновить VR-тексты + re-ship `nervous`→041 / `hitman`→064 (Slay). `--dry-run` / `--skip-ship`. |
| `_audit_nightops_speech_coverage.py` | Аудит SPEECH/BATTLESNDS/NO overlays + внешние `_ub_cs_cache` (ЦС) / `_horg_stogie_cache` (Бычок). Identity по RU greeting/self-ID в mercedt, **не** по EDT filename (они часто врут). |
| `_extract_ja2_mercedt.py` | Распаковать/расшифровать `MERCEDT.SLF` (JA2 / NightOps) → UTF-8 CSV субтитров `000`..`116` в `docs/design/mercs-ja12/_voice-source/ja2no-mercedt/`. |
| `_extract_wildfire_rus_arc.py` | FreeArc extract `Jagged_Alliance_2_1_13_Wildfire_RUS.arc` (7z не открывает) через PeaZip `Arc.exe` → `_voice-source/_wildfire_cache/` (SPEECH/MercEdt + Data-UB). Это 1.13 RUS+WF maps, не commercial WF AIM VO; Gaston = Data-UB/058. |
| `_inventory_ja2mercs.py` | Read-only inventory `Downloads/ja2mercs/ja2mercs`: layout (flat/nested), audio counts/formats, profile-id guess, crosswalk к `jazz_to_ja2_profile.csv`. Не ship/convert. `--root` optional. Remesh: `_apply_ja2mercs_profile_map.py` + `_ship_ja2_merc_voices.py --ja2mercs-remesh`. |
| `_stt_ja2mercs_sample.py` | Pilot subtitles for ja2mercs: export XLSX/mercedt ref text + optional faster-whisper RU STT (ADPCM→PCM via ffmpeg). Default pilot `но-шж/гром` pids 076+047 (both Grom). `--no-stt` = refs only. Out: `_voice-source/_stt/`. |

## Артефакты

- `_attach_001_audit.tsv` — dry-run/apply audit от `_apply_attach_001.py`
- `attachments-catalog.html` — generated catalog
- `_attach_*.json` — промежуточные summary (можно регенерировать)

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
