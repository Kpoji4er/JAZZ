---
id: JAZZ-UNITS-003
status: implemented
owner: project-owner
systems:
  - units-progression
  - legion-units-equipment
  - inventory-items-loot
repositories:
  - jazz
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-UNITS-003.md
  - jazz/docs/design/legion-loadouts.md
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz/docs/technical/systems/inventory-items-loot-crafting.md
  - jazz/scripts/legion-loadouts/**
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz-units/Code/**
exclusive_resources:
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz-units-generated-root
related_decisions:
  - none
approved_by: project-owner chat 2026-07-30 approve UNITS-003; parallel agents warned
---

# JAZZ-UNITS-003: Legion loadout generator (recipes → LootDef)

Design canon: [`docs/design/legion-loadouts.md`](../../design/legion-loadouts.md) (L1–L23). Current-state: [`legion-units-equipment-tiers.md`](../../technical/systems/legion-units-equipment-tiers.md). Weapon tiers: [`weapons.csv`](../../technical/weapons/data/weapons.csv).

## Проблема

Легион уже имеет 37 боевых `*_Inventory` / `*_Firearm` и ~739 условий на `JAZZ_Legion_Tier`, но:

- силуэт класса и качество склада смешаны в ручных весах;
- варианты одной винтовки плодятся суффиксами (`_AP_Reflex`, …);
- нет единого контракта arch/sub ↔ `weapons.csv` `X-Y`, ammo grade, mods packages, delayed utility, valuables≈unit `$`, night/flare/misc;
- сопровождение 37 классов вручную не масштабируется.

Нужен **data-driven** контур: class recipes + catalogs → build-time generator → LootDef, без смены public UnitData ID и без обязательной смены quest thresholds.

## Цели

- Зафиксировать и реализовать генератор лоадаутов Легиона по L1–L23.
- Shared ladders (weapon `balance_tier`, ammo grade, armor band, mod packages, night/misc/utility) + тонкие class recipes.
- Primary/sidearm/melee/armor/ammo/utility/night/flaregun/misc/valuables из keywords; модули только из совместимых `weapon-component-options.csv`.
- Пилот 3 класса → раскатка всех 37 боевых `JAZZ_Legion_*` (Recruit вне combat loadout recipes).
- Technical docs = current-state после внедрения.

## Non-goals

- Смена `JAZZ_LegionTier` TCE / Ernie sector thresholds (L2: оставить; материк — follow-up).
- Изменение `RegenerateLegionLoot` policy (L19: open / as-is).
- Новые UnitData ID, AI archetypes, STRATEGY squad `$` / officer density / composition.
- Condition/износ на спавне (L23: после смерти, вне этого generator).
- Полный rewrite не-Legion enemy loot.
- Push/release.
- Ручной основной workflow правки generated суффикс-вариантов после появления генератора.

## Утверждённый контракт (сводка L*)

| Тема | Контракт |
| --- | --- |
| Оси | class T1–T4 силуэт × `JAZZ_Legion_Tier` поколение склада |
| Arch/sub | `1x/2x/3x`; sub = зеркало `weapons.csv` (`1-1…1-3`, `2-1…2-5`, `3-1…3-5`) |
| Weapon gate | arch N → `balance_tier==N`; tier1 на arch2 ≈1%; tier1 на arch3 = 0% |
| Tags | family tags (напр. M2/FG42 `{carbine,assault}`) ≠ `tier_label` |
| Carbine норма | good assault / raider-line с arch2; low на arch3 может assault/АК |
| Sidearm | pistol/revolver mid+; часто delayed unlock |
| Mods | packages M0–M4; больше у элиты; совместимость из CSV |
| Ammo | grade Poor→AP; floor от arch, cap от class |
| Grenades | specialist guaranteed (+count↑ arch); non-spec chance↑ class+loot tier |
| Pipes | low-class pool с ~`21`, chance↑ arch |
| Night | night-only lights; chance/stack↑ loot tier |
| FlareGun | role-biased; mild↑ loot tier; % §5.4 design |
| Misc | low % by class band |
| Valuables | ≈ `JAZZ_LegionUnitPrices`; chance+mult; **не** на logistics карман; cargo `lEnsureMoneyCargo` лутается при грабеже |
| Regen | не менять в этом spec |

Числовые старты %: design §5.3–5.4 (тюнинг playtest допустим без смены REQ, если AC qualitative держатся).

## Требования

- `JAZZ-UNITS-003-REQ-001` — Build-time (или явно выбранный в spec-ревизии equivalent) генератор: вход = recipes + catalogs; выход = Legion LootDef / `LootEntry*` / `LootEntryUpgradedWeapon` для `jazz-units`; не плодить hand-made суффикс-зоопарк как основной процесс.
- `JAZZ-UNITS-003-REQ-002` — Каталоги минимум: weapon tags + `balance_tier` gate; mod package keywords ∩ `weapon-component-options.csv`; ammo grade ladder; armor Light/Middle/Heavy; utility (HE/smoke/molotov/pipe); night; flaregun; misc; valuables `unit_price`.
- `JAZZ-UNITS-003-REQ-003` — Recipe на каждый из **37** боевых `JAZZ_Legion_*` (не Recruit): primary tags, sidearm/melee rules, armor band, utility mode, mods_cap/packages, ammo floor/cap, night/flare/misc/valuables, arch biases — согласовано с design §5.
- `JAZZ-UNITS-003-REQ-004` — Weapon selection уважает `tier_label`/`balance_tier` ↔ `JAZZ_Legion_Tier` (L3–L5); WWII/tier1 хвост ≈1% только на arch2.
- `JAZZ-UNITS-003-REQ-005` — Upgrades только совместимые с выбранным `weapon_id`; packages по роли (CQB ≠ sniper scope-only).
- `JAZZ-UNITS-003-REQ-006` — Ammo grade следует L12; калибр от выбранного ствола.
- `JAZZ-UNITS-003-REQ-007` — Utility: specialist HE guaranteed; non-spec chance↑; pipes unlock ~`21` для low-class; delayed sidearm где задано recipe.
- `JAZZ-UNITS-003-REQ-008` — Night lights night-oriented + chance/stack↑ с loot tier; FlareGun role table; misc low-roll.
- `JAZZ-UNITS-003-REQ-009` — Valuables: `P = JAZZ_GetLegionUnitPrice(class)`; drop_chance + mult range; размен Tiny/Big; **`valuables: none` (карман)** на managed logistics roles (`tax`/`shipment`/carriers using mission cargo); не эмитить `DiamondBriefcase` из class recipe. Cargo остаётся лутаемым через Global AI.
- `JAZZ-UNITS-003-REQ-010` — Пилот: `Roughneck`, `ShockTrooper`, `Sniper` полностью на генераторе и playtest smoke до раскатки остальных.
- `JAZZ-UNITS-003-REQ-011` — Sync: generated loot + `jazz-units/items.lua` + `metadata.lua` в одной транзакции; documented regenerate command; политика сосуществования с Mod Editor (генератор владеет помеченными Legion loot ids / folder).
- `JAZZ-UNITS-003-REQ-012` — Не менять `RegenerateLegionLoot` и quest TCE `JAZZ_LegionTier` в этом change.

## Инварианты и ограничения

- Public UnitData IDs `JAZZ_Legion_*` и корневые inventory preset **имена**, на которые ссылается UnitData, сохраняются (содержимое preset может стать generated).
- Quest var `JAZZ_Legion_Tier` остаётся единственным progression signal для LootDef conditions.
- `JAZZ_LegionUnitPrices` / STRATEGY-004 — источник `P` для valuables; не дублировать вторую таблицу цен.
- Determinism: веса/conditions фиксированы в generated data; RNG остаётся engine `CreateStartingEquipment` + seed.
- Exclusive: не параллелить другой agent на `jazz-units/items.lua` / `metadata.lua` (**jazz-units-generated-root**). Параллельная работа других агентов — только вне этого exclusive set (или явная сериализация write).
- Не ломать `lEnsureMoneyCargo` payload на logistics squads.

## Параллельные агенты (owner 2026-07-30)

Пока идёт UNITS-003:

| Можно параллельно | Нельзя без координации |
| --- | --- |
| `jazz` Code вне loot-gen (STRATEGY AI, UI, …) если не трогает Legion starting loot | `jazz-units/items.lua`, `jazz-units/metadata.lua` |
| portraits / UnitData stats **без** смены Equipment/LootDef ids | ручная правка тех же Legion `*_Inventory` / `*_Firearm` |
| `jazz/scripts/**` кроме конфликта с `scripts/legion-loadouts/**` | одновременный regenerate всего `items.lua` другим пайплайном |

Пилот (Roughneck/Shock/Sniper) и полная раскатка — один владелец write на generated root за раз; merge конфликтов items.lua избегать сериализацией.

## Acceptance criteria

- `JAZZ-UNITS-003-AC-001` — static: существует runnable generator + recipe/catalog sources; README/usage в `jazz/scripts/legion-loadouts/`.
- `JAZZ-UNITS-003-AC-002` — static: пилот Roughneck / ShockTrooper / Sniper — root inventory/firearm/ammo/armor/utility/night/valuables соответствуют recipes (tags, arch gates, specialist vs chance HE, delayed rules где заданы).
- `JAZZ-UNITS-003-AC-003` — static: для пилота нет `LootEntryUpgradedWeapon` с component_id вне options выбранного оружия.
- `JAZZ-UNITS-003-AC-004` — static: weapon entries с `balance_tier==1` на legion tier≥30 отсутствуют (или weight 0); на tier∈[20,30) суммарный вес tier1 ≈1% parent pool (допуск playtest ±0.5 п.п. зафиксировать в evidence).
- `JAZZ-UNITS-003-AC-005` — static: все 37 боевых классов имеют recipes и regenerated loot; Recruit не требует combat recipe.
- `JAZZ-UNITS-003-AC-006` — static: logistics-facing recipes / spawn path не добавляют карманный `unit_price` valuables поверх mission cargo; no class-emitted `DiamondBriefcase`.
- `JAZZ-UNITS-003-AC-007` — static: sync-audit jazz-units items/metadata/companions (если companions) согласованы после генерации.
- `JAZZ-UNITS-003-AC-008` — runtime/human: Ernie smoke — arch1 loadouts читаются по силуэту; night lights ночью; specialist grenades present; Roughneck без carbine-нормы на mid.
- `JAZZ-UNITS-003-AC-009` — runtime/human: перехват tax/shipment — лутается payload сумма; не «пустой» конвой из-за generator.
- `JAZZ-UNITS-003-AC-010` — docs: `legion-units-equipment-tiers.md` (+ inventory page при необходимости) описывают generator current-state; design doc ссылает этот SPEC-ID.

## Impact и совместимость

- **Vanilla/CommonLib/JAZZ:** меняется содержимое Legion starting equipment; UnitData ID стабильны.
- **Saves:** существующие юниты до regen/respawn могут иметь старый inventory; после OpenSatellite regen — новый (текущий wipe contract).
- **Network/determinism:** loot tables static; seed path unchanged.
- **Generated data:** да, массово `jazz-units/items.lua`.
- **Cross-package:** generator/scripts в `jazz`; prices в `jazz`; loot в `jazz-units`; Global AI cargo в `jazz` Code — не ломать.
- **Rollback:** revert generated loot + recipes/scripts; восстановить pre-change items.lua snapshot.

## План и ownership

1. **Draft→approved** владельцем (этот файл).
2. Scaffold `jazz/scripts/legion-loadouts/` + catalogs + 3 pilot recipes.
3. Generate pilot loot → sync jazz-units → smoke AC-002/003/004/008.
4. Fill remaining 34 recipes → full generate → AC-005/006/007.
5. Human AC-008/009; docs AC-010.
6. `status: implemented` → review → `accepted`.

- Пакет-владелец loot: **jazz-units**; generator/docs/prices consumer: **jazz**.
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set / exclusive: frontmatter

## Решение владельца

- Дизайн L1–L23: подтверждён в чате 2026-07-30.
- Статус **этого** spec: **`approved`** — «на реализацию специ даю апрув»; следить за параллельными агентами (exclusive `jazz-units` generated root).
- Кто подтвердил: project-owner
- Дата approve: 2026-07-30

## Evidence

- `JAZZ-UNITS-003-AC-001` — `PASS` (static): `jazz/scripts/legion-loadouts/` + README/TESTING; `generate.py --dry-run` runnable.
- `JAZZ-UNITS-003-AC-002` — `PASS` (static): Roughneck / Shocktrooper / Sniper inventories regenerated from recipes (tags, HE mode, night/valuables/armor).
- `JAZZ-UNITS-003-AC-003` — `PASS` (static): generator upgrade check vs `weapon-component-options.csv` clean on dry-run/full generate.
- `JAZZ-UNITS-003-AC-004` — `PASS` (static): exclusive arch bands; Roughneck mid remnant `weight=1400` ≈ **0.999%** of active mid pool; no open-ended tier1 at ≥30.
- `JAZZ-UNITS-003-AC-005` — `PASS` (static): 37 recipes; `generate.py` patches 37/37; Recruit without combat recipe.
- `JAZZ-UNITS-003-AC-006` — `PASS` (static): no `DiamondBriefcase` in generated markers; valuables = pocket Tiny/Big bands only.
- `JAZZ-UNITS-003-AC-007` — `PASS` (static, scoped): `JAZZ_Gen*` added to `jazz-units/metadata.lua` `affected_resources` (727); pre-existing UnitData companion orphans in suite audit are unrelated to this LootDef change.
- `JAZZ-UNITS-003-AC-008` — `BLOCKED` (runtime/human deferred by owner 2026-07-30): no playtest this session; guide `scripts/legion-loadouts/TESTING.md` §2. Static silhouette checks covered under AC-002.
- `JAZZ-UNITS-003-AC-009` — `BLOCKED` (runtime/human deferred by owner 2026-07-30): no playtest this session; guide TESTING.md §3. Static: no class-emitted briefcase (AC-006).
- `JAZZ-UNITS-003-AC-010` — `PASS` (docs): `legion-units-equipment-tiers.md` + inventory note + design link updated.

Static re-run 2026-07-30: `python scripts/legion-loadouts/generate.py --dry-run` (37/37) + `python scripts/legion-loadouts/run_static_tests.py` → PASSED.

Test guide: [`scripts/legion-loadouts/TESTING.md`](../../../scripts/legion-loadouts/TESTING.md).

## Documentation delta

- После implementation: обновить `docs/technical/systems/legion-units-equipment-tiers.md` (generator, L18–L22 behavior as loaded); при необходимости `inventory-items-loot-crafting.md`.
- `docs/design/legion-loadouts.md` — ссылка на JAZZ-UNITS-003; не выдавать design за runtime.
- Showcase/wiki: только если заметно игроку после ship (отдельное решение); не блокер DoD этого spec, если technical покрыт.
