---
id: JAZZ-MED-006
status: approved
owner: project-owner
systems:
  - armor-damage-wounds-will
  - ui-audio-fx
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/Systems_Medicine.lua
  - Code/System_Medicine_MED006.lua
  - Code/System_JazzTraumaEffect.lua
  - Code/System_Wounds_OperationHeal.lua
  - Code/CombatBadge_DeathRoll.lua
  - Code/GritOnStart.lua
  - Code/UnitPropertiesStats.lua
  - Code/System_UnitInventory.lua
  - InventoryItem/FirstAidKit.lua
  - InventoryItem/Medkit.lua
  - InventoryItem/Reanimationsset.lua
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
  - Icons/StatusEffects/Trauma*.png
  - Icons/StatusEffects/Trauma*Stabilized.png
  - Icons/StatusEffects/Trauma*Healing.png
  - items.lua
  - metadata.lua
  - Russian.csv
  - English.csv
  - Localization/Strings.csv
  - Localization/RussianManual.csv
  - Localization/EnglishManual.csv
  - docs/specs/active/JAZZ-MED-006.md
  - docs/specs/active/JAZZ-MED-001.md
  - docs/specs/active/JAZZ-MED-003.md
  - docs/design/medicine.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/technical/systems/file-coverage.md
  - docs/technical/systems/ui-audio-fx.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
  - docs/tools/_audit_med006_kits_stabilize.py
  - docs/tools/README.md
exclusive_resources:
  - items.lua
  - metadata.lua
  - localization-id-allocation
related_decisions:
  - none
related_specs:
  - JAZZ-MED-001
  - JAZZ-MED-002
  - JAZZ-MED-003
  - JAZZ-MED-004
  - JAZZ-MED-005
approved_by: project-owner
---

# JAZZ-MED-006: аптечка = первая помощь; стабилизация; долг макс. ОЗ; читаемые статусы ухода

Design thread (Discord / chat 2026-08-17…18): аптечки слишком похожи на RPG-хилку; лечение на глобалке и сильные медики обесцениваются; травмы должны оставаться долгом; аптечка **стабилизирует** травму (облегчает штрафы); стабилизированные и заживающие раны должны быть визуально отличимы.

Supersedes kit trauma-heal path from [JAZZ-MED-003](JAZZ-MED-003.md) `REQ-006` / `REQ-007` / targeting eligibility that marks `jazz_healing` from kits, and supersedes MED-003 `REQ-004` kit `heal_modifier` +0/+50/+100%. Field TreatWounds → `jazz_healing` from [JAZZ-MED-001](JAZZ-MED-001.md) `REQ-015` **остаётся**.

## Проблема

1. Kit Bandage восстанавливает ОЗ сильно (ещё и от Medical) и ставит `jazz_healing` по тиру кита. Игрок воспринимает аптечку как полное «выпил хилку — здоров», а операцию TreatWounds / врачей (Паучиха и др.) — как лишних.
2. Скрытый параметр `jazz_healing` на том же `Trauma*` **не читается** в UI: иконка травмы та же, что у необработанной. Новая стабилизация (`stabilized`) без отдельного знака повторит ту же ошибку.
3. Травма режет боеспособность, но не макс. ОЗ; нет читаемого долга «рана съела потолок», который чинит только глобалка.

## Цели

- Аптечка = **первая помощь в бою**: кровь, боль, подъём из downed, восстановление ОЗ, **стабилизация** (облегчение штрафов одной травмы). Не запуск заживления и не clear Trauma*.
- Заживление (`jazz_healing`) = **только** полевая операция TreatWounds / OperationHeal. Госпиталь instant clear — MED-002 **deferred / not loaded**, вне этого spec.
- Стабилизированная и заживающая травмы — **отдельные читаемые UI-состояния** той же Trauma* (не новые Trauma ID): своя иконка (базовый глиф зоны/тира + corner badge) и свой текст тултипа.
- Центральная функция **меняет Icon** экземпляра эффекта по состоянию (`untreated` / `stabilized` / `healing`), чтобы бейдж, party HUD и ролловер показывали одно и то же без скрытых флагов.
- Травма даёт **долг макс. ОЗ** по тиру; стабилизация его **не** снимает; TreatWounds / healing progress — да. Hospital instant clear **вне scope и не loaded**; progress downgrade пересчитывает долг.
- Морфий по-прежнему глушит только боль; стабилизация облегчает **zone-специфик** (ходить/стрелять лучше), не заменяя морфий.

## Non-goals

- Мгновенный clear Trauma* аптечкой или полевой операцией.
- Hospital instant clear (MED-002 **deferred / not loaded**).
- Отдельный InventoryItem только для стабилизации; отдельный POI «полевой госпиталь».
- Новые публичные Trauma ID (`TraumaLegsHeavyStabilized` и т.п.) — состояния через параметры на существующем эффекте.
- «Долг макс. ОЗ только после боя» (deferred max HP) — **superseded by [JAZZ-MED-007](JAZZ-MED-007.md)** (approved 2026-08-23).
- Полный пересмотр частоты лута аптечек / Legion medic density (можно follow-up; этот spec не обязан менять loot tables).
- Смена Medical gates 30/50/80 и MaxStacks 5/10/15 (MED-003 остаётся).
- Смена AP лестницы бинта/морфия (MED-005 остаётся).
- Переписывание Pain / bleed тиров / порогов травмы с хита (MED-004 остаётся), кроме чтения **эффективного** тира для штрафов под стабилизацией.

## Модель

### Слои

| Слой | Бой (аптечка / бинт / морфий) | Глобалка |
| --- | --- | --- |
| Кровь | бинт −1 тир/стак; кит — полный стоп | тики / TreatWounds |
| Боль | морфий / кит → Analgesia; −1/ход | Pain снимается с концом боя |
| ОЗ | кит: % от **макс. ОЗ** по тиру × Medical (см. ниже) | TreatWounds / отдых / операции |
| Травма (tier ID) | **стабилизация**: эффективные штрафы как у тира −1; tier не меняется | TreatWounds → `jazz_healing` → step-down |
| Макс. ОЗ долг | появляется с травмой; стабилизация **не** трогает | падает с downgrade/clear травмы |

### Хил ОЗ аптечкой

% от **текущего максимума ОЗ** пациента (`MaxHitPoints` после trauma debt), не «до полного» ванильным `CalcHealAmount` без капа.

| Кит | Medical gate | При Medical **100** | При Medical **= gate** |
| --- | --- | --- | --- |
| Small (`FirstAidKit`) | **30** | **30%** max HP | **30% × 30% = 9%** max HP |
| Medium (`Medkit`) | **50** | **60%** max HP | **30% × 60% = 18%** max HP |
| Large (`Reanimationsset`) | **80** | **100%** max HP | **30% × 100% = 30%** max HP |

Интерполяция между gate и 100 (включительно; выше 100 → как 100):

```text
t = (Medical − gate) / (100 − gate)   -- 0 at gate, 1 at 100
heal% = kit_at_100% × (0.30 + 0.70 × t)
```

Примеры Medium: Med 50 → 18%; Med 75 → 39%; Med 100 → 60%.  
Heal amount = `MulDivRound(patient.MaxHitPoints, heal%, 100)`, затем clamp к недостающим ОЗ.  
Supersedes MED-003 `REQ-004` (`heal_modifier` +0/+50/+100%). Perk-модификаторы хила (например MD `BuildingConfidence`) применяются **после** этого % (mul/add к уже посчитанному amount), если уже висят на `OnCalcHealAmount` — не ломать; не давать суммарно выше недостающих ОЗ.

### Стабилизация (`jazz_stabilized`)

- Параметр на экземпляре `Trauma*`: `jazz_stabilized = 1` (или bool-эквивалент через `SetParameter`).
- Один юз кита стабилизирует **одну** eligible unhealed / unstabilized травму (приоритет heaviest в пределах капа кита; zone order on ties — как сейчас у kit trauma mark).
- Кап по киту (тот же rank, что MED-003 для healing, но цель — stabilize, не heal):
  - Small (`FirstAidKit`): только **Light**
  - Medium (`Medkit`): **Medium** или **Light**
  - Large (`Reanimationsset`): **any** (включая Heavy)
- Пока `jazz_stabilized`: **эффективный combat tier** для zone-специфика и zone-use Pain / Heavy unused Pain ramp = на **один** ранг ниже (Heavy→Medium, Medium→Light, Light→нет специфика; Light zone-use Pain остаётся +1, если зона всё ещё Light и нет Analgesia).
- Реальный `JazzGetTraumaTier` / progress / infection / MaxHP debt **читают stored tier**, не effective.
- Стабилизация **не** ставит `jazz_healing` и **не** меняет interval/improve/worsen.
- Снятие стабилизации: квалифицирующий хит в ту же зону (травма step-up или повторный qualifying hit), или clear/downgrade зоны. Конец боя **не** снимает стабилизацию (можно доползти до эвакуации / TreatWounds).
- Если уже `jazz_healing`, кит **не** обязан стабилизировать ту же травму (уже в уходе); targeting может предпочесть другую unstabilized, иначе no-op по травме.

### Заживление (`jazz_healing`)

- Без изменений правил progress (half interval, improve 100%, worsen 0) после TreatWounds.
- Kits **больше не** вызывают `JazzMarkKitTraumaHealing` / `JazzMarkHeaviestTraumaHealing`.
- Helpers kit-eligible переименовать/заменить на stabilize-path (`JazzFindKitEligibleUnstabilizedTrauma`, `JazzMarkKitTraumaStabilized`) либо оставить имена с новой семантикой — в коде предпочтительно **новые** имена + deprecate старых mark-heal-from-kit.

### Долг макс. ОЗ

- Base max HP = текущий `GetInitialMaxHitPoints` / Health path (без grit).
- Активные зональные травмы (не Burn stub unless owner includes Burn) дают штраф к max HP, суммируется по зонам, floor **1** HP:

| Stored tier | Штраф |
| --- | --- |
| Light | **10%** base max |
| Medium | **30%** base max |
| Heavy | **60%** base max |

- Применить через единый recalc (`RecalcMaxHitPoints` / wrap рядом с `GritOnStart.lua` / `UnitProperties`), синхрон Unit + UnitData.
- `jazz_stabilized` **не** уменьшает этот штраф.
- При downgrade/clear травмы штраф пересчитывается; текущие HP clamp к новому max.
- BloodLoss ladder (MED-002) остаётся от **текущих** HP%; не путать с trauma max-HP debt.

### UI / иконки

Три визуальных состояния одной Trauma*:

| Состояние | Параметры | Иконка |
| --- | --- | --- |
| Untreated | нет healing, нет stabilized | текущий `Icons/StatusEffects/Trauma{Zone}{Tier}.png` |
| Stabilized | `jazz_stabilized`, не healing | `…/Trauma{Zone}{Tier}Stabilized.png` (базовый глиф + corner badge стабилизации/креста) |
| Healing | `jazz_healing` | `…/Trauma{Zone}{Tier}Healing.png` (базовый глиф + corner badge часов/лечения; cyan medical family) |

Приоритет, если когда-либо оба флага: **Healing** побеждает Stabilized (показать healing icon; stabilized можно снять при mark healing).

**Обязательная функция смены иконки** (канон реализации):

```text
JazzResolveTraumaStatusIcon(effect) → icon_path
JazzApplyTraumaStatusIcon(effect)   -- SetProperty("Icon", …); stamp UI
```

- Вызывать при: apply trauma, set/clear stabilized, set/clear healing, twin sync, `JazzStampStatusEffectUIProps` для Trauma*, UI refresh paths (`GetUIVisibleStatusEffects` / party portrait stamp).
- `JazzStampStatusEffectUIProps` для Trauma* **не** должен безусловно затирать Icon дефолтом Def, если состояние stabilized/healing — stamp идёт через `JazzApplyTraumaStatusIcon`.
- Тултип (`JazzFormatTraumaStatusDescription` / `ResolveValue("Description")`): явная строка «Стабилизирована» / «Заживает» + hours-to-check как сейчас.
- Не полагаться на невидимый параметр без смены Icon.

Asset pipeline: `$create-jazz-status-icons` / finalize 40×40; можно собрать base Trauma PNG + corner overlay скриптом (оставить в `docs/tools/` при появлении).

## Требования

### Аптечка: первая помощь

- `JAZZ-MED-006-REQ-001` — Любой kit Bandage: полный clear крови, Analgesia, clear `WoundInfected`, rally downed; **хил ОЗ** по таблице % макс. ОЗ (Small/Medium/Large при Medical 100 → **30 / 60 / 100%**; при Medical = gate → **30% от этих** значений; линейная интерполяция gate→100). Не использовать MED-003 `heal_modifier` +0/+50/+100 как основной источник силы хила.
- `JAZZ-MED-006-REQ-001a` — База хила: `amount = MulDivRound(MaxHitPoints, heal%, 100)` от пациента; clamp к `MaxHitPoints − HitPoints`. Medical ниже gate — кит недоступен (существующие gates 30/50/80).
- `JAZZ-MED-006-REQ-002` — Kits **не** ставят `jazz_healing` ни на одну Trauma*.
- `JAZZ-MED-006-REQ-003` — Успешный kit Bandage ставит `jazz_stabilized` на **одну** eligible травму по капу кита (Light / ≤Medium / any), если такая есть и ещё не stabilized / не healing.
- `JAZZ-MED-006-REQ-004` — Targeting / consume: kit eligible при bleed, HP debt, downed, Pain, WoundInfected, **или** kit-eligible unstabilized trauma. Consume один стак при любом успешном эффекте (включая только stabilize).
- `JAZZ-MED-006-REQ-005` — Item hints / loc RU+EN: убрать «starts healing trauma» и старые «+50% / +100% bandage healing»; писать стабилизацию, % хила от Medical и отсутствие лечения травмы на глобалке.

### Стабилизация: эффективные штрафы

- `JAZZ-MED-006-REQ-006` — Пока `jazz_stabilized` и не healing: zone combat modifiers (CTH, move AP, start AP, Free Move, sight) и Pain-on-zone-use / Heavy unused ramp используют **effective tier = stored − 1** (Light effective = no zone-специфик; Pain-on-use Light +1 сохраняется).
- `JAZZ-MED-006-REQ-007` — `JazzGetTraumaTier` и satellite progress / infection / MaxHP debt используют **stored** tier.
- `JAZZ-MED-006-REQ-008` — Стабилизация снимается при qualifying hit в ту же зону или при clear/downgrade зоны; конец боя не снимает.
- `JAZZ-MED-006-REQ-009` — TreatWounds / `JazzMarkUnitTraumasHealing` снимает `jazz_stabilized` на помечаемых травмах (или healing icon priority) и ставит `jazz_healing` как сейчас.

### Долг макс. ОЗ

- `JAZZ-MED-006-REQ-010` — Активная Trauma* (Arms/Legs/Ribs/Head; Burn — **включить** с теми же %) снижает max HP: Light **10%**, Medium **30%**, Heavy **60%** base; сумма по зонам; floor **1**.
- `JAZZ-MED-006-REQ-011` — `jazz_stabilized` не меняет MaxHP debt. Recalc при apply/remove/downgrade trauma и LoadGame/NewGame merc refresh path.
- `JAZZ-MED-006-REQ-012` — UI: в тултипе травмы или status Information видно вклад в max HP (число/%); не требовать отдельный CE только ради долга.

### UI / Icon swap

- `JAZZ-MED-006-REQ-013` — Для каждого `Trauma{Zone}{Tier}` существуют (или генерируются) PNG untreated / Stabilized / Healing; wired path `Mod/e6L4ECj/Icons/StatusEffects/…`.
- `JAZZ-MED-006-REQ-014` — `JazzResolveTraumaStatusIcon(effect)` возвращает path по состоянию; `JazzApplyTraumaStatusIcon(effect)` пишет `Icon` на экземпляр.
- `JAZZ-MED-006-REQ-015` — Combat badge, party portrait (`JazzGetPartyPortraitStatusEffects`), и StatusEffectIcon показывают Icon после apply; twin sync копирует параметры + Icon.
- `JAZZ-MED-006-REQ-016` — Description append различает Stabilized vs Healing (RU/EN).

### Docs / audit

- `JAZZ-MED-006-REQ-017` — Обновить `docs/design/medicine.md`, technical `armor-damage-wounds-will.md` (+ UI note), wiki + showcase RU/EN combat-and-accuracy; note supersede в MED-001/MED-003.
- `JAZZ-MED-006-REQ-018` — Static audit `docs/tools/_audit_med006_kits_stabilize.py`: kits не mark healing; stabilize caps; icon helpers present; MaxHP % table wired; kit heal% at gate/100 matches 9/18/30 and 30/60/100.

## Инварианты и ограничения

- Публичные Trauma* / kit class IDs не меняются.
- Bleed 3/6/12, Pain/Analgesia, MED-004 hit thresholds, MED-005 field AP — без регрессии.
- Deterministic InteractionRand / Random для trauma progress без изменений seed policy.
- Saves: старые `jazz_healing` на Trauma* валидны; отсутствие `jazz_stabilized` = untreated stabilize state; после load вызвать `JazzApplyTraumaStatusIcon` на всех Trauma*.
- Не вводить второй параллельный CE рядом с каждой Trauma* только ради иконки (кроме опционального helper CE — **запрещён** этим spec; только Icon swap на существующем эффекте).

## Acceptance criteria

- `JAZZ-MED-006-AC-001` — static: kit Bandage path не вызывает mark-healing; вызывает stabilize с caps Light / ≤Medium / any; heal% helpers: Small/Med/Large at Med 100 → 30/60/100, at gate → 9/18/30; MED-003 heal_modifier +0/+50/+100 не источник силы.
- `JAZZ-MED-006-AC-002` — static: `JazzResolveTraumaStatusIcon` / `JazzApplyTraumaStatusIcon` существуют; stamp/twin paths call apply; Healing приоритетнее Stabilized.
- `JAZZ-MED-006-AC-003` — static: MaxHP debt 10/30/60% wired; stabilize не в формуле долга.
- `JAZZ-MED-006-AC-004` — static: companion hints + RU/EN без «kit starts trauma healing» и без старых +50/+100 healing bonus строк; есть stabilize + % heal от Medical.
- `JAZZ-MED-006-AC-005` — static: PNG set Stabilized/Healing для всех 15 Trauma* (или documented generator + committed outputs).
- `JAZZ-MED-006-AC-006` — docs: design + technical + wiki + showcase RU/EN + MED-003 supersede note (heal + trauma mark).
- `JAZZ-MED-006-AC-007` — runtime: Medium trauma Legs + Medium kit → move penalty как у Light, max HP всё ещё −30%, иконка Stabilized; TreatWounds → иконка Healing, штрафы снова full Medium до step-down.
- `JAZZ-MED-006-AC-008` — runtime: Heavy trauma + Small kit → крови/боли/ОЗ ок, **без** stabilize; Large kit → stabilize Heavy→effective Medium.
- `JAZZ-MED-006-AC-009` — human: на портрете/бейдже отличимы untreated / stabilized / healing без открытия тултипа.
- `JAZZ-MED-006-AC-010` — runtime: пациент MaxHP 100, пустой; Large + Medical 80 → ~30 HP; Large + Medical 100 → full; Medium + Medical 50 → ~18; Small + Medical 30 → ~9.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: Bandage/GetBandaged, Trauma reactions, RecalcMaxHitPoints, status Icon stamp.
- Saves: новые параметры на CharacterEffect; Icon path на инстансе; старые сейвы без stabilize OK.
- Network/determinism: stabilize/heal flags sync Unit↔UnitData как trauma twin sync.
- Generated data: kit companions, Trauma companions если Description/Icon defaults, items/metadata, icons, loc.
- Cross-package: нет обязательного jazz-units diff (loot out of scope).
- Rollback: revert write_set; вернуть MED-003 kit→`jazz_healing`.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent (после `approved`)
- Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive resources: `items.lua`, `metadata.lua`, localization ID allocation

### Порядок реализации (после approve)

1. Параметры `jazz_stabilized` + helpers find/mark/clear + effective-tier readers для reactions/Pain.
2. Убрать kit→`jazz_healing`; переключить targeting/hints; заменить kit heal на % max HP × Medical.
3. MaxHP debt recalc.
4. `JazzResolveTraumaStatusIcon` / `JazzApplyTraumaStatusIcon` + stamp/UI/twin.
5. Asset PNG Stabilized/Healing (+ tool если batch).
6. Loc RU/EN; audit; docs/wiki/showcase.

## Решение владельца

- Статус: **approved**
- Кто подтвердил: project-owner (chat 2026-08-18: approve + heal% 30/60/100 at Med 100, 30% of that at gate; «шина»→стабилизация; implement + push)
- Дата: 2026-08-18

### Зафиксировать при approve (закрыть до Ready)

1. MaxHP debt: **% от base** 10/30/60 (REQ-010) — **locked**.
2. Heal ОЗ китов: при Medical 100: Small/Medium/Large **30 / 60 / 100%** max HP; при Medical = gate — **30% от этих** (9 / 18 / 30%); линейная интерполяция gate→100 — **locked**.
3. Burn травмы: участвуют в MaxHP debt и stabilize ladder — **да** (REQ-010).
4. Повторный kit на уже stabilized: consume только если есть другой эффект (кровь/HP/pain…) — **да**.

## Evidence

- `JAZZ-MED-006-AC-001`…`006`: `PASS` — static `python docs/tools/_audit_med006_kits_stabilize.py` (+ MED-003 audit updated for heal supersede).
- `JAZZ-MED-006-AC-007`: `PASS` (static) — `JazzTraumaResolveNum` keeps Light-effective **0** (no `x or preset`); companions + `items.lua` synced. `BLOCKED` (runtime/human) — Medium kit → move as Light still needs playtest.
- `JAZZ-MED-006-AC-008`…`010`: `BLOCKED` — runtime/human playtest after ship.

status note: code + icons + loc + docs wired; mark `implemented` after smoke.

## Documentation delta

После реализации:

- `docs/design/medicine.md` — аптечка/стабилизация vs TreatWounds; anti-RPG-heal
- `docs/technical/systems/armor-damage-wounds-will.md` — stabilize, MaxHP debt, Icon swap API
- `docs/technical/systems/ui-audio-fx.md` — trauma status icon states
- `docs/technical/systems/file-coverage.md` — если новые Code/*.lua
- `docs/wiki/combat-and-accuracy.md` + `docs/showcase/ru|en/combat-and-accuracy.md`
- Notes в `JAZZ-MED-001` / `JAZZ-MED-003` — kit healing superseded by MED-006 stabilize
