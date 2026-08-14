---
id: JAZZ-COMBAT-005
status: implemented
owner: project-owner
systems:
  - armor-damage-wounds-will
  - combat-cth-actions
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - Code/System_OR_Unit.lua
  - Code/Systems_Medicine.lua
  - CharacterEffect/Weight_1Class.lua
  - CharacterEffect/Weight_2Class.lua
  - CharacterEffect/Weight_3Class.lua
  - CharacterEffect/Weight_4Class.lua
  - CharacterEffect/Weight_5Class.lua
  - CharacterEffect/Ironclad.lua
  - CharacterEffect/KillingWind.lua
  - items.lua
  - English.csv
  - Russian.csv
  - docs/specs/active/JAZZ-COMBAT-005.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/technical/testing.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
  - docs/tools/_apply_combat_005_weight_items.py
  - docs/tools/_patch_combat_005_weight_loc.py
  - docs/tools/README.md
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMBAT-005: штрафы веса брони (FreeMove + осторожный AP + Pain при перевесе)

## Проблема

`Unit:CalculateArmorWeight` задуман как налог мобильности/ОД от `Armor.Weight`, но после «среза» баланса:

1. вклад веса в обычные ОД закомментирован; остался **плоский** `TotalAPDebuff = const.Scale.AP` (−1 ОД всем независимо от комплекта);
2. FreeMove-штраф копится в **целых ОД** (0.5/1/2/3), а `ConsumeAP(..., "Move")` ожидает внутренние единицы (`× const.Scale.AP`) → иконка `Weight_*Class` есть, реального минуса FreeMove почти нет;
3. статус `Weight_NClass` берёт **N = PenetrationClass торса**, не класс веса; `OnAdded`/reactions пустые — описание врёт про снижение ОД;
4. playtest (Fauda / Grizzly / Spike): иконка без штрафа или штраф без понятной иконки; cumbersome и KillingWind/Ironclad поверх этого плохо читаются.

Экономика стрельбы: 1 клик aim ≈ 1 ОД; типичный выстрел с aim ≈ ShootAP+2…3 (часто 7–11 ОД из ~13–17). Штраф брони должен бить **мобильность**, а обычные ОД резать **аккуратно** (0–1, редко 2), не отбирая целый выстрел.

## Цели

- Починить wiring FreeMove: списание в `const.Scale.AP`.
- Убрать плоский −1 ОД; вернуть **весовой** AP-штраф с жёстким капом.
- FreeMove — основной налог; AP — вторичный.
- Сохранить таблицу веса слотов, STR-смягчение, Ironclad AP ÷2. **Ironclad** −50% FM-штрафа от брони; **KillingWind** ещё −50% (аддитивно: оба → 0). Громоздкое оружие: BeginTurn FreeMove у KillingWind без изменений.
- При **сильном перевесе** первое перемещение за ход даёт **+1 Pain** (не больше одного стека за ход); правило читаемо в статусе.
- Иконки/текст статуса отражают **фактический** штраф веса (не PenetrationClass).
- Player-facing docs (technical + wiki + showcase RU/EN) описывают контракт.

## Non-goals

- Ребаланс `Armor.Weight` на отдельных предметах / перепись каталога JazzArmor (кроме если static audit найдёт Weight=0 там, где нужен класс).
- Смена cumbersome → полный отказ FreeMove (vanilla/JAZZ BeginTurn path) и MG ShootAP.
- Новые перки; смена Ironclad/KillingWind ID.
- Удорожание шага через `move_ap_modifier` / изменение стоимости клетки.
- Больше 1 стека Pain за ход от веса; Pain от стрельбы/aim из-за брони.
- Перенос логики в CommonLib.

## Решения владельца (предложение draft — ждут approve)

| Тема | Предложение |
| --- | --- |
| Основной налог | FreeMove |
| Обычные ОД | вторичный, кап **2**, чаще **0–1** |
| Плоский −1 AP | удалить |
| Сырой FM по `Weight` | 2→+0.5, 3→+1, 4→+2, 5→+3 (сумма по надетым Armor вне Inventory) |
| AP из сырого FM | пороги: raw &lt; 4 → 0; 4…7.999 → 1; ≥ 8 → 2 (до смягчений) |
| Порядок смягчений | **Ironclad** −50% FM; **KillingWind** ещё −50% FM (оба → 0); Ironclad → AP ÷2; затем STR → floor → clamp |
| STR | при Strength &gt; 60: `StrBuff = MulDivRound(Strength−60, 1, 20)`; **сначала** вычитать из AP (до 0), остаток — из FM |
| Cumbersome | не удваивать боль: при `using_cumbersome` **не** применять AP-штраф брони; FM брони не half от cumbersome; BeginTurn: **KillingWind** получает FreeMove с cumbersome |
| Иконка | стаки = `floor(FM_penalty_AP_units)` при &gt; 0; класс иконки = **max Weight** среди учтённых предметов (1…5 → `Weight_1Class`…`Weight_5Class`); FM/AP через ConsumeAP; Pain — отдельный hook |
| Капы | FM ≤ 12 ОД; AP ≤ 2 ОД |
| Сильный перевес | после всех смягчений `floor(FM) ≥ 6` (мягкий порог: средний/лёгкий кит и сильный STR на heavy без плиты — без Pain) |
| Pain при перевесе | первое **боевое перемещение** (тратит FreeMove и/или Move AP) в ход → `JazzAddPainStacks(unit, 1)` **один раз**; дальше в том же ходу — нет; без движения Pain от веса нет |
| Читаемость | в Description `Weight_*` при пороге: явное «перевес: +1 боль при перемещении (раз за ход)»; при `floor(FM) &lt; 6` этой строки нет; floating text при срабатывании (как у trauma Pain), RU/EN |

## Требования

- `JAZZ-COMBAT-005-REQ-001` — Сырой FreeMove: для каждого надетого `Armor` с `Weight` в слоте ≠ `Inventory` добавить вклад `{2:0.5, 3:1, 4:2, 5:3}` (Weight 1 = 0). Плиты/`ArmorPlate`, наследующие Armor+Weight, входят в сумму.
- `JAZZ-COMBAT-005-REQ-002` — Сырой AP: `0` если raw_FM &lt; 4; `1` если 4 ≤ raw_FM &lt; 8; `2` если raw_FM ≥ 8. **Не** инициализировать AP-штраф константой `const.Scale.AP`.
- `JAZZ-COMBAT-005-REQ-003` — Смягчения FM: **Ironclad** −50% сырого FM-штрафа; **KillingWind** ещё −50% (аддитивно: оба → `fm_mul=0`). Ironclad → AP ÷2. Затем STR: `StrBuff` вычитается из AP до 0, остаток — из FM. Cumbersome: AP-штраф брони = 0; FM брони не half от cumbersome. KillingWind **не** обнуляет штраф веса сам по себе (только вместе с Ironclad). BeginTurn cumbersome FreeMove у KillingWind без изменений.
- `JAZZ-COMBAT-005-REQ-004` — После floor: `FM = Clamp(FM, 0, 12)`, `AP = Clamp(AP, 0, 2)`. Списание: `ConsumeAP(FM * const.Scale.AP, "Move")` и `ConsumeAP(Min(ActionPoints, AP * const.Scale.AP))` на том же вызове `CalculateArmorWeight`, что и сейчас (BeginTurn + OnGearChanged). Не списывать повторно в одном BeginTurn сверх одного вызова. Сохранять на юните актуальные `FM`/`AP` после расчёта (или эквивалент), чтобы move-hook и UI читали один источник.
- `JAZZ-COMBAT-005-REQ-005` — Статусы `Weight_1Class`…`Weight_5Class`: снять все, затем при `FM ≥ 1` добавить `floor(FM)` стаков класса `max equipped Armor.Weight` (clamp 1…5). Без reactions, меняющих AP/FreeMove. Description RU/EN: FreeMove (−N), при AP&gt;0 старт ОД (−M); если `FM ≥ 6` — строка про +1 Pain при перемещении раз за ход; без PenetrationClass.
- `JAZZ-COMBAT-005-REQ-006` — BeginTurn: порядок «выдать FreeMove (cumbersome/KillingWind/Ironclad) → затем `CalculateArmorWeight`» сохранить. Cumbersome без перка по-прежнему не выдаёт FreeMove. Сброс per-turn флага Pain-от-веса в начале хода юнита.
- `JAZZ-COMBAT-005-REQ-007` — **Pain при перевесе:** если после REQ-003/004 `floor(FM) ≥ 6` и юнит в бою совершает перемещение, тратящее FreeMove и/или Move AP → один вызов `JazzAddPainStacks(unit, 1)` за ход (флаг turn-key; повторные клетки/второе Move — no-op). Не применять вне боя, если Analgesia уже блокирует Pain. Не копить больше 1 стека **от этого источника** за ход. KillingWind сам по себе не exempt (после −50% порог 6 реже). Ironclad+KillingWind → FM 0 → Pain от веса нет.
- `JAZZ-COMBAT-005-REQ-008` — Docs: `armor-damage-wounds-will.md` (вес + Pain), `testing.md`, wiki + showcase RU/EN combat. Loc: обе CSV для `Weight_*` и любого floating text.

## Инварианты и ограничения

- Публичные ID `Weight_1Class`…`Weight_5Class`, `Ironclad`, `KillingWind` не переименовывать.
- `Armor.Weight` 1…5 и `ArmorWeightIds` UI без смены семантики классов.
- Детерминизм: арифметика от экипа/статов + один флаг хода; без Random.
- `JazzAddPainStacks` / Analgesia / Pain.max_stacks без изменений контракта MED-002.
- Не менять формулу `GetMaxActionPoints`, ShootAP/aim costs, trauma FreeMove blockers, trauma Pain-on-zone (отдельный канал; могут суммироваться в общий Pain, но вес даёт ≤1/ход).
- Saves: нет нового GameVar; per-turn flag эфемерен; старые сейвы получают новый расчёт на следующем BeginTurn/gear change.

## Acceptance criteria

- `JAZZ-COMBAT-005-AC-001` — Static: в `CalculateArmorWeight` нет плоского `TotalAPDebuff = const.Scale.AP`; FM/AP consume умножены на `const.Scale.AP`; cumbersome не half FM и обнуляет AP-штраф брони.
- `JAZZ-COMBAT-005-AC-002` — Runtime: мерк STR 60, medium kit raw≈2.5–3.5 → AP-штраф 0, FM-штраф заметен (≥1 ОД FreeMove после floor); иконка стаков = floor(FM), класс = max Weight.
- `JAZZ-COMBAT-005-AC-003` — Runtime: STR 60, heavy full raw≈6 → AP 1, FM ≈6 (до perk); STR 100 → AP 0 (StrBuff съедает AP), FM снижен на 2.
- `JAZZ-COMBAT-005-AC-004` — Runtime: heavy+plate/EOD raw≥8, STR 60 → AP 2 (кап); только KillingWind → FM ≈ half raw, AP 2; только Ironclad → FM ≈ half, AP 1; Ironclad+KillingWind → FM 0, AP 1. Weight_* при floor(FM)≥1 (нет статуса, если FM 0).
- `JAZZ-COMBAT-005-AC-005` — Runtime: Grizzly с cumbersome MG — FreeMove 0 от BeginTurn; AP-штраф брони не применяется; без MG в том же бронекомплекте FreeMove выдаётся и режется весом.
- `JAZZ-COMBAT-005-AC-006` — Runtime: STR 60, kit с `floor(FM) ≥ 6` (heavy full / EOD) — первое Move даёт +1 Pain; второе Move / продолжение пути в том же ходу — без второго стека от веса; без Move — Pain от веса нет. Статус явно предупреждает о перевесе.
- `JAZZ-COMBAT-005-AC-007` — Runtime: medium или heavy после STR с `floor(FM) &lt; 6` — Move не даёт Pain от веса. KillingWind в EOD — Pain только если после −50% всё ещё `floor(FM) ≥ 6`. Ironclad+KillingWind — Pain от веса нет.
- `JAZZ-COMBAT-005-AC-008` — Human/docs: technical + wiki + showcase RU/EN согласованы; статус не обещает FM/AP/Pain, которых код не делает.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: только override `CalculateArmorWeight` / BeginTurn уже в `System_OR_Unit.lua`; Weight CharacterEffect companions.
- Saves: soft — следующий ход применяет новый налог (танки внезапно почувствуют FM).
- Network/determinism: те же входы → тот же consume.
- Generated data: `items.lua`/`metadata.lua` при правке Weight_* descriptions/loc wiring.
- Cross-package: нет.
- Rollback: revert `System_OR_Unit.lua` + Weight effect strings/docs.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: `jazz/items.lua`, `jazz/metadata.lua`

## Решение владельца

- Статус: **approved** — пороги AP 4/8; Pain при `FM ≥ 6`; Ironclad −50% FM + AP ÷2; KillingWind ещё −50% FM (оба → 0); Pain ≤1 стек/ход.
- Кто подтвердил: project-owner («делаем», 2026-08-08); **amend 2026-08-15** — owner + playtest Баюн: Ironclad сначала −50% FM от тяжёлой брони; KillingWind ещё −50%; cumbersome FreeMove KillingWind не трогать.
- Дата: 2026-08-08; amend 2026-08-15

## Evidence

- `JAZZ-COMBAT-005-AC-001`: `PASS (static)` — `CalculateArmorWeight` без плоского 1 AP; FM/AP × `const.Scale.AP`; cumbersome не half FM, AP брони = 0; Ironclad и KillingWind каждый −50% FM (`fm_mul`), оба → 0; Ironclad AP ÷2.
- `JAZZ-COMBAT-005-AC-002`…`005`, `007`: `BLOCKED (runtime)` — нужен JA3Debug smoke (medium/heavy/EOD, STR, MG, Ironclad, KillingWind stack, Pain once).
- `JAZZ-COMBAT-005-AC-006`: `BLOCKED (runtime)` — Pain на первом Move при FM≥6.
- `JAZZ-COMBAT-005-AC-008`: `PASS (static)` — technical + wiki + showcase RU/EN + Weight loc CSV.

## Documentation delta

`armor-damage-wounds-will.md`, `testing.md`, `units-progression-specializations.md`, `docs/wiki/combat-and-accuracy.md`, `docs/showcase/ru|en/combat-and-accuracy.md`, `docs/showcase/ru|en/perks.md`, Ironclad/KillingWind Description loc, `docs/tools/_apply_ironclad_killingwind_fm_stack.py`.
