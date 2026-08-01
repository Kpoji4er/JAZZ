# `docs/tools` — скрипты агентов и аудита

Рабочие утилиты для generated data, аттачей, CSV и design-артефактов.  
Политика хранения: `.agents/docs/reference/agent-tooling.md`, `.cursor/rules/jazz-agent-tooling.mdc`.

Запуск из корня пакета `jazz/` (если не указано иное).

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
| `_insert_reload_combat_action.py` | WEAPONS-004: вставляет full `ModItemCombatAction` `Reload` в `items.lua` + `ModResourcePreset` в `metadata.lua`. |
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
| `_validate_items_quick.py` | Быстрый структурный check `items.lua`/`metadata.lua` (lone commas, braces, stacked closers, **missing comma before PlaceObj**, corrupt `id = }),`) без JA3. **Обязателен после mass apply / family split**. |
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
| `_finalize_icon_style_b.py` | Style B Icon: magenta/rembg cut → heal → Anaconda soft edge → 100×100. Canon: `WeaponComponents/references/PROMPT.md`. |
| `_qa_icon_style_b.py` | QA preview Icon: size/opaque/soft-AA/corners/bright-fringe. Fail → regen. |
| `_wire_ak74_mag_icons.py` | MagNormal/MagLarge_30_45 ApplyTo AK74+RPK74+AKSU → `AK74_Mag30` / `AK74_Mag45_long`. |
| `_wire_g36_mag_icons.py` | MagNormal ApplyTo G36 + G36c → `Magazine/G36_Mag30.png`. |
| `_wire_vss_val_mag_icons.py` | MagNormal VSS/AS_Val → VSS_Mag10; MagLarge_10_20_VAL → VSS_Mag20. |
| `_wire_sig_icons.py` | MagNormal Sig550/Custom/552/SWAT → Sig_Mag30; SigDefHandGuard + SigErgoHandGrip Icons. |
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
| `_wire_thompson_mag_icons.py` | MagNormal Thompson → Mag30; MagDrum_30_50_THOMPSON → MagDrum. |
| `_wire_pps43_mag_icons.py` | MagNormal ApplyTo PPS43 → `Magazine/PPS43_Mag35.png` (no Mag slot yet). |
| `_wire_mpl_mag_icons.py` | MagNormal ApplyTo MPL → `Magazine/MPL_Mag30.png`. |
| `_wire_m45_mag_icons.py` | MagNormal ApplyTo M45 (Carl Gustaf) → `Magazine/M45_Mag32.png`. |
| `_wire_agram_mag_icons.py` | MagNormal ApplyTo Agram2000 → `Magazine/Agram_Mag32.png`. |
| `_wire_uzi_icons.py` | MagDrum_30_50_UZI → UZI_MagDrum; StockLight Folded/UnFolded UZI → UZI_Stock. |
| `_wire_mp5_mag_icons.py` | MagNormal → MP5_Mag30; MagSmall30_15_MP5 → MP5_Mag15 на MP5/MP5K/MP5A2/MP5A4/MP5SD (+ ApplyTo MP5). |
| `_wire_berettam12_mag_icons.py` | MagNormal ApplyTo BerettaM12 → `Magazine/BerettaM12_Mag32.png`. |
| `_wire_spectrem4_mag_icons.py` | MagNormal ApplyTo SpectreM4 → `Magazine/SpectreM4_Mag50.png`. |
| `_wire_tmp_icons.py` | MagNormal/MagSmall30_15_TMP → TMP Mag30/Mag15; HolsterBelt Icon (был битый `belt.png`) + TMP Visual. |
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
| `_rebalance_recoil_physical.py` | JAZZ-WEAPONS-003: authoring mass/RPM/size/limiter и physical Recoil/Burst/Auto в companions + `items.lua`; `--apply` пишет `.bak`. |
| `_audit_recoil_dist.py` | Static AC audit полей active firearms, recoil anchors, 9×19 differentiation и M16A2/AN94 limiters. |
| `_fix_madman_salary.py` | Jazz_Madman: `StartingSalary`/`SalaryLv1`/`SalaryMaxLv` в `jazz-units/items.lua` (companion править отдельно). |
| `_fix_free_merc_salaries.py` | Jazz_Grom / Jazz_Hitman: paid hire salaries в companion + `jazz-units/items.lua`. |
| `_sync_grom_rehire_chat.py` | Гром RehireIntro: убрать «бесплатный» из `items.lua` + `Russian.csv`. |
| `_sync_madman_chat_salary_strings.py` | Синк AIM-фраз Бешеного (не «бесплатный») в `items.lua` + `Russian.csv`/`English.csv`. |

## Артефакты

- `_attach_001_audit.tsv` — dry-run/apply audit от `_apply_attach_001.py`
- `attachments-catalog.html` — generated catalog
- `_attach_*.json` — промежуточные summary (можно регенерировать)

## Добавление нового скрипта

1. Положить в `docs/tools/` с говорящим именем (`_apply_…`, `_export_…`, `_audit_…`, `_remove_…`).
2. Docstring в шапке: что делает, dry-run/apply, откуда читать, куда писать.
3. Строка в этой таблице.
4. При системной процедуре — ссылка в `.agents/docs/playbooks/…` и при необходимости в `.agents/docs/index.md`.
