---
id: JAZZ-MED-001
status: approved
owner: project-owner
systems:
  - armor-damage-wounds-will
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/System_JazzStackableMedicine.lua
  - Code/Systems_Medicine.lua
  - Code/GritOnStart.lua
  - Code/System_ArmorRating.lua
  - Code/Systems_Wounds_HealWounds.lua
  - Code/System_Wounds_OperationHeal.lua
  - Code/System_UnitInventory.lua
  - CharacterEffect/BandageInCombat.lua
  - CharacterEffect/Bleeding.lua
  - CharacterEffect/BleedingMedium.lua
  - CharacterEffect/BleedingHeavy.lua
  - CharacterEffect/Pain.lua
  - CharacterEffect/Analgesia.lua
  - CharacterEffect/Wounded.lua
  - CharacterEffect/TraumaArmsLight.lua
  - CharacterEffect/TraumaArmsMedium.lua
  - CharacterEffect/TraumaArmsHeavy.lua
  - CharacterEffect/TraumaLegsLight.lua
  - CharacterEffect/TraumaLegsMedium.lua
  - CharacterEffect/TraumaLegsHeavy.lua
  - CharacterEffect/TraumaRibsLight.lua
  - CharacterEffect/TraumaRibsMedium.lua
  - CharacterEffect/TraumaRibsHeavy.lua
  - CharacterEffect/TraumaHeadLight.lua
  - CharacterEffect/TraumaHeadMedium.lua
  - CharacterEffect/TraumaHeadHeavy.lua
  - CharacterEffect/TraumaBurnLight.lua
  - CharacterEffect/TraumaBurnMedium.lua
  - CharacterEffect/TraumaBurnHeavy.lua
  - CharacterEffect/Armsshot.lua
  - CharacterEffect/Legsshot.lua
  - CharacterEffect/Headshot.lua
  - CharacterEffect/Torsoshot.lua
  - CharacterEffect/Groinshot.lua
  - CharacterEffect/Unconscious.lua
  - CharacterEffect/Burning.lua
  - InventoryItem/JAZZ_Bandage.lua
  - InventoryItem/JAZZ_Morphine.lua
  - InventoryItem/JAZZ_SurgicalKit.lua
  - InventoryItem/FirstAidKit.lua
  - InventoryItem/Medkit.lua
  - Icons/Items/JAZZ_*.png
  - Icons/Med/
  - Icons/StatusEffects/Trauma*.png
  - items.lua
  - metadata.lua
  - Russian.csv
  - English.csv
  - Localization/RussianManual.csv
  - Localization/EnglishManual.csv
  - Localization/Strings.csv
  - docs/design/medicine.md
  - docs/specs/active/JAZZ-MED-001.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/technical/systems/file-coverage.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
  - docs/tools/_audit_med001_analgesia.py
  - docs/tools/_audit_med001_kit_requirements.py
  - docs/tools/README.md
exclusive_resources:
  - items.lua
  - metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-MED-001: medicine redesign v1 (bleed, Pain, grit off, items, zonal traumas)

Design canon: [docs/design/medicine.md](../../design/medicine.md).

## Проблема

Жёсткий бой толкает в F5 через смерть / grit-подушку; `Wounded` стаки от HP и однородный `Bleeding` не дают читаемый долг (кровь тирами, боль, зональные травмы, предметы без skill-gate на бинт/морфий).

## Цели

- Убрать `GritOnStart` Temp HP ~25% на старте боя.
- Кровь: три тира (`Bleeding` = лёгкое / `BleedingMedium` / `BleedingHeavy`), стаки, урон 3/6/12 за стак/ход, кап суммарного урона крови ~30/ход.
- Бинт (−1 тир худшему стаку), морфий (Analgesia), IFAK=`FirstAidKit`, Medkit, Surgical kit; self+ally через CombatActions на хотбаре.
- `Pain` (−AP/−CTH, −1 стак/ход); морфий глушит штрафы боли. **Pain уже есть** в runtime v1.
- Тяжёлая кровь с хита только от экспансивных (`JHP`/`HP` AppliedEffects remap).
- Отключить выдачу `Wounded` от HP (`HpLossToAddStack` effectively off).
- **Зональные травмы** light/medium/heavy для Arms / Legs / Ribs / Head (+ Burn stub); eye folded into Head.
- Цветные inventory icons в `Icons/Items/`; `Icons/Med/` — иконки хотбар-экшенов; status icons `Icons/StatusEffects/Trauma*.png`.

## Non-goals

- Satellite hospital clear / полная стационарная хирургия (мгновенное снятие Trauma* по концу Hospital).
- Инфекция / choking rework / pneumothorax / concussion package (D-layer).
- Отдельные `TraumaEye*` ID (folded into Head for v1).
- Burn medium/heavy apply pipeline beyond `Burning` → `TraumaBurnLight` stub.
- Medic profile tags (санитар/врач) как жёсткий gate (v1: Medical thresholds soft).
- Medical-quality tiers для скорости `jazz_healing` (v1: фиксированный буст после TreatWounds).
- Переписать весь loot distribution.
- Удаление ID `Wounded` / `FirstAidKit` (rebrand/disable behavior only).

## Требования

- `JAZZ-MED-001-REQ-001` — `CombatStart` не выдаёт Temp HP grit 25%.
- `JAZZ-MED-001-REQ-002` — три bleed ID; урон 3/6/12 × stacks; суммарный tick capped ~30.
- `JAZZ-MED-001-REQ-003` — бинт: −1 тир одному худшему стаку; без Medical; мало AP.
- `JAZZ-MED-001-REQ-004` — морфий: `Analgesia` глушит штрафы `Pain`; не снимает кровь/травму.
- `JAZZ-MED-001-REQ-005` — экспансив: hit effect `Bleeding` → `BleedingHeavy`; обычные попадания могут вешать лёгкое/среднее по шансу.
- `JAZZ-MED-001-REQ-006` — `HpLossToAddStack` не добавляет `Wounded` в нормальном бою (sentinel / bypass).
- `JAZZ-MED-001-REQ-007` — переходы bleed по рекомендованной таблице design (70/15/15 · 35/45/20 · 15/85).
- `JAZZ-MED-001-REQ-008` — docs: technical + wiki + showcase RU/EN + design status sync.
- `JAZZ-MED-001-REQ-009` — цветные `Icons/Items` для новых/rebrand предметов; hotbar icons из `Icons/Med`.
- `JAZZ-MED-001-REQ-010` — публичные trauma IDs: `Trauma{Arms|Legs|Ribs|Head|Burn}{Light|Medium|Heavy}` (15). Light = боль при юзе зоны, без zone CTH/move; Medium+ = специфик + боль; Heavy = near-ineffective + Pain. **Pain on solid damaging hit:** **+1** via `JazzPainOnDamagingHit` from `ApplyDamageAndEffects` (damage > 0; **graze excluded**; separate from zone-use). **Pain stacks on zone use:** Light **1** / Medium **2** / Heavy **3** (`JazzTraumaPainOnZoneUse`); **unused Heavy** zones still add **+1 Pain each** EndTurn (`JazzTraumaHeavyPainRamp`, skip if that zone already used this turn). Ribs: **no Tired**. Head: повышенный шанс Medium/Heavy с хита. Eye → Head.
- `JAZZ-MED-001-REQ-011` — hit→trauma через `*shot` rollers (`Armsshot`/`Legsshot`/`Headshot`/`Torsoshot`/`Groinshot` → `JazzTryRollTraumaFromBodyPart`). `UnitDowned` немедленно создаёт одну физическую Heavy trauma (+3 Pain), апгрейдит уже выпавшую Light/Medium и подавляет более лёгкий эффект того же хита; последующий `Unconscious` через совместимый `JazzApplyKnockoutTraumaPackage` идемпотентен. Wounded stacks не остаются.
- `JAZZ-MED-001-REQ-012` — status icons `Icons/StatusEffects/Trauma*.png` wired on effects.
- `JAZZ-MED-001-REQ-013` — worn armor covering the hit zone (`ProtectedBodyParts`: Arms / Legs / Torso|Groin→Ribs / Head|Neck→Head) reduces trauma roll chance via `JazzGetTraumaArmorChanceFactor` (Coverage×Condition, max ~60% cut, floor factor 40). Does not apply to Burn or knockout package. Unpierced armor still blocks `*shot` separately.
- `JAZZ-MED-001-REQ-014` — behind-armor trauma (BAT): when hit has `armor_decay` and no `armor_pen`, `JazzTryBehindArmorTrauma` may apply Light (rarely Medium) zone trauma; no bleed. Pain: residual damage > 0 uses hit +1 (`JazzPainOnDamagingHit`); full absorb (0 residual) adds `JazzAddPainStacks(1)` in BAT. Chance scales with `armor_prevented + residual` damage.
- `JAZZ-MED-001-REQ-015` — field TreatWounds / `PatientAddHealWoundProgress` marks each patient `Trauma*` with `jazz_healing`: progress checks use halved interval (floor 2h), improve **100%** (guaranteed tier step-down via improve branch), worsen **0**; flag survives tier downgrade. Does **not** instant-clear Trauma*. `HealWounds` Effect does **not** set healing.
- `JAZZ-MED-001-REQ-016` - `Analgesia` suppresses every `Pain` penalty immediately: CTH is gated while the effect is active, and AP already withheld by `Pain.OnCalcStartTurnAP` in the current turn is refunded exactly once from a tracked applied-penalty value. Applying Analgesia again or gaining Pain after start of turn grants no AP.
- `JAZZ-MED-001-REQ-017` — `FirstAidKit` requires Medical **30**, restores HP, and removes every `Bleeding` / `BleedingMedium` / `BleedingHeavy` stack. `Medkit` requires Medical **50**, has the same bleed clear, and applies **+50%** heal modifier. One requirement helper controls action availability, execution, and the inventory rollover. The rollover always shows the threshold; when the current/owner unit is below it, the requirement row is a red warning.
- `JAZZ-MED-001-REQ-018` — **superseded by [JAZZ-MED-003](JAZZ-MED-003.md)** (kit trauma healing by tier + Large Medical 80 / +100% / full bleed / BR / Legion loot).

## Инварианты и ограничения

- Публичный ID `FirstAidKit` сохраняется (IFAK rebrand).
- `TrueGrit` perk не трогаем.
- Deterministic RNG: `unit:Random` / InteractionRand как соседние medicine hooks.
- HealWounds / operation heal обновляются под новые bleed ID (не оставлять только `Bleeding`); trauma **clear** на госпитале — MED-002; trauma **healing flag** после полевой операции — MED-001 (см. REQ-015); trauma **healing** с большой аптечки — одна heaviest unhealed (REQ-018).
- Small/Medium Bandage kits не ставят `jazz_healing`; Large (`Reanimationsset`) ставит на одну heaviest unhealed Trauma*.

## Acceptance criteria

- `JAZZ-MED-001-AC-001` — static: нет grit TempHP на CombatStart.
- `JAZZ-MED-001-AC-002` — static: bleed damage params 3/6/12 + shared tick/cap + bandage −1 tier API.
- `JAZZ-MED-001-AC-003` — static: JHP/HP remap to BleedingHeavy; Pain/Analgesia effects exist.
- `JAZZ-MED-001-AC-004` — static: items Bandage/Morphine/Surgical + FirstAidKit/Medkit icons+hints.
- `JAZZ-MED-001-AC-005` — docs synced; design marked implemented-scope v1.
- `JAZZ-MED-001-AC-006` — runtime/human: бинт снижает тир; морфий глушит боль; без grit на старте.
- `JAZZ-MED-001-AC-007` — static: 15 trauma CharacterEffects + *shot/Unconscious/Burning wiring + icons + loc RU/EN; `UnitDowned` immediately guarantees one Heavy trauma and repeated Unconscious is idempotent.
- `JAZZ-MED-001-AC-008` — runtime/human: body hit rolls trauma; knockout applies heavy package; zone debuffs match design formula.
- `JAZZ-MED-001-AC-009` — static: `JazzGetTraumaArmorChanceFactor` scales thresholds when covering armor Condition>0; Burn/knockout untouched.
- `JAZZ-MED-001-AC-010` — static: unpierced armor path calls `JazzTryBehindArmorTrauma`; no bleed on BAT.
- `JAZZ-MED-001-AC-011` — static: `PatientAddHealWoundProgress` calls `JazzMarkUnitTraumasHealing`; healing chances/interval match REQ-015; `HealWounds` does not mark healing.
- `JAZZ-MED-001-AC-012` — static: solid damaging hit -> `JazzPainOnDamagingHit` +1 (cap 8); graze excluded; no double with BAT when residual damage > 0.

- `JAZZ-MED-001-AC-013` - static: `Pain` records the AP penalty actually applied at start of turn; `Analgesia.OnAdded` consumes that value through the medicine helper and refunds it once; companion and `items.lua` stay equivalent.
- `JAZZ-MED-001-AC-014` - runtime/human: morphine during the unit turn restores exactly the AP withheld by Pain and suppresses Pain CTH; repeated morphine and Pain gained later in the turn do not grant extra AP.
- `JAZZ-MED-001-AC-015` — static: companion/`items.lua` parity for IFAK and Medkit; Medical thresholds are 30/50; both clear all bleed stacks; Medkit heal modifier is +50; selectors and `GetBandaged` enforce the shared helper.
- `JAZZ-MED-001-AC-016` — runtime/human: the rollover shows current/required Medical and turns red below the threshold; a blocked kit cannot heal, clear bleed, or be consumed; eligible kits heal and remove every bleed stack.
- `JAZZ-MED-001-AC-017` — static: `GetBandaged` on `Reanimationsset` calls `JazzMarkHeaviestTraumaHealing`; helper picks heaviest unhealed Trauma*; kit Bandage targeting accepts trauma-only patients when Large is equipped.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: overrides bleed/bandage/heal paths; new CharacterEffect + InventoryItem IDs.
- Saves: юниты со старым `Bleeding`/`Wounded` остаются валидны; новые ID появляются после load.
- Network/determinism: сохраняется при unit RNG.
- Generated data: items.lua + companions + metadata.code.
- Cross-package: нет обязательных units/maps правок в v1.
- Rollback: откатить write_set.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: items.lua, metadata.lua

## Решение владельца

- Статус: **approved**
- Кто подтвердил: project-owner («пока апрувд, реализуй»; зональные травмы — сразу в MED-001, не откладывать в MED-002)
- Дата: 2026-08-02

## Evidence

- `JAZZ-MED-001-AC-001`: `PASS` — static: `GritOnStart.lua` без CombatStart Temp HP.
- `JAZZ-MED-001-AC-002`: `PASS` — static: `Systems_Medicine.lua` + bleed effects 3/6/12 + bandage −1 tier.
- `JAZZ-MED-001-AC-003`: `PASS` — static: JHP remap + Pain/Analgesia companions.
- `JAZZ-MED-001-AC-004`: `PASS` — static: Bandage/Morphine/Surgical + IFAK/Medkit icons/items wired.
- `JAZZ-MED-001-AC-005`: `PASS` — static: technical + wiki + showcase RU/EN + design status (trauma included).
- `JAZZ-MED-001-AC-006`: `BLOCKED` — runtime/human playtest pending.
- `JAZZ-MED-001-AC-007`: `PASS` — static: Trauma* companions/items/metadata/icons/loc; *shot → `JazzTryRollTraumaFromBodyPart`; Unconscious → knockout package; Burning → `TraumaBurnLight`; `_audit_med001_downed_heavy.py` verifies immediate Heavy upgrade and idempotence.
- `JAZZ-MED-001-AC-008`: `BLOCKED` — runtime/human trauma playtest pending.
- `JAZZ-MED-001-AC-009`: `PASS` — static: armor zone→factor wired in `Systems_Medicine.lua`.
- `JAZZ-MED-001-AC-010`: `PASS` — static: BAT wired from `ApplyDamageAndEffects` unpierced branch.
- `JAZZ-MED-001-AC-011`: `PASS` — static: OperationHeal marks `jazz_healing`; progress **100%** improve / **0** worsen / half interval; HealWounds unchanged for trauma.
- `JAZZ-MED-001-AC-012`: `PASS` — static: `JazzPainOnDamagingHit` (+1 Pain, damage>0, graze excluded) from `ApplyDamageAndEffects`; BAT full-absorb Pain only when residual<=0.

- `JAZZ-MED-001-AC-013`: `PASS` - static: `python docs/tools/_audit_med001_analgesia.py` verifies tracked current-turn AP penalty, one-shot direct refund, stale/post-start no-grant cases, and companion/`items.lua` parity.
- `JAZZ-MED-001-AC-014`: `BLOCKED` - runtime/human morphine playtest pending.
- `JAZZ-MED-001-AC-015`: `PASS` — `python docs/tools/_audit_med001_kit_requirements.py` verifies Medical 30/50 gates, hard treatment recheck, full bleed removal, Medkit +50%, red rollover warning, and companion/`items.lua` parity.
- `JAZZ-MED-001-AC-016`: `BLOCKED` — runtime/human rollover and treatment playtest pending.
- `JAZZ-MED-001-AC-017`: `PASS` — static: `python docs/tools/_audit_med001_large_kit_trauma.py` verifies `JazzMarkHeaviestTraumaHealing` / `JazzFindHeaviestUnhealedTrauma` wiring and `GetBandaged` + kit targeting hooks.

status note: code wired including zonal traumas + armor trauma mitigation + BAT + split hotbar medicine (`JazzBandage` / kit `Bandage` / `JazzMorphine`) + trauma progress timers/UI + OperationHeal→healing flag; mark `implemented` after smoke in editor/game.

**Contract note (owner):** Hospital clear remains MED-002. Soft satellite progress + **field TreatWounds → `jazz_healing`** (guaranteed improve each check, block worsen) are MED-001 per design agreement («полевое лечение запускает медленное заживление»). Medical-quality speed tiers still deferred.

## Documentation delta

- `docs/design/medicine.md` — status → approved / v1 implementing (traumas in scope); Pain growth includes solid damaging hit +1; Morphine also rallies downed
- `docs/technical/systems/armor-damage-wounds-will.md` — grit off, bleed tiers, Pain (hit + zone-use + heavy ramp), zonal traumas, items, OperationHeal healing flag; Morphine→DownedRally
- `docs/technical/systems/file-coverage.md` — Systems_Medicine.lua + Trauma* effects
- `docs/wiki/combat-and-accuracy.md` + showcase RU/EN — player-facing wounds/medicine/trauma notes (+ field healing; hit Pain; graze no hit Pain; Morphine downed rally; kit thresholds/full bleed clear/+50% Medkit heal)
