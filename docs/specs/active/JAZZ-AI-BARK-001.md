---
id: JAZZ-AI-BARK-001
status: implemented
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-BARK-001.md
  - jazz/docs/design/combat-ai-barks.md
  - jazz/docs/tools/_aibark_bank_data.py
  - jazz/docs/tools/_check_aibark_bank.py
  - jazz/docs/tools/README.md
  - jazz/Code/System_AI_CombatBarks.lua
  - jazz/Code/AIContextProfiles.lua
  - jazz/Code/CombatAI.lua
  - jazz/Code/AiActions.lua
  - jazz/Code/AiAction_ThrowFlare.lua
  - jazz/metadata.lua
  - jazz/items.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/wiki/officer-aura.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/officer-aura.md
  - jazz/docs/showcase/en/officer-aura.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - localization ID range 890000000020157-890000000020596
  - jazz/Russian.csv
  - jazz/English.csv
related_decisions:
  - docs/design/combat-ai-barks.md
  - docs/specs/active/JAZZ-AI-CMD-001.md
  - docs/specs/active/JAZZ-AI-CMD-002.md
  - docs/specs/active/JAZZ-AI-007.md
  - docs/specs/active/JAZZ-AI-DES-001.md
approved_by: pending
---

# JAZZ-AI-BARK-001: floating combat barks over enemy AI

## Проблема

Офицер уже выбирает директиву (`JazzAI_PickOfficerDirective`), юнит уже
падает в `Panicked` / `Deserter` или кидает фаер / дым / гранату /
разворачивает пулемёт. Игрок это видит только если читает тултип ауры
или угадывает по анимации. Хода врага не слышно: нет окрика, нет
координации, побег выглядит немым.

Голос и `BanterDef` здесь лишние. Нужен короткий текст над головой —
только когда решение уже принято и оно редкое.

## Цели

- Враг, которого игрок **видит**, иногда орёт над головой: смена приказа
  офицера (все директивы CMD-001), смена динамического архетипа,
  тип гранаты, смена класса оружия, посадка пулемёта,
  **Press/обход CMD-002** и **дальняя перебежка**.
- Текст — канон из [`combat-ai-barks.md`](../../design/combat-ai-barks.md),
  по тиру / рангу, RU+EN, без вейва.
- Антиспам важнее полноты: лучше тишина, чем очередь подписей.
- Скоринг, директивы, dest, Dump **не** меняются. Барк только читает
  уже принятое решение.

## Non-goals

- VoiceResponse, TTS, `BanterDef`, портрет, пауза диалога.
- LLM / runtime generation / sidecar.
- Окрики игрока, милиции, повстанцев (`side=ally` / `player_ally`).
- Ack «есть / понял» от соседних бойцов.
- Dump, обычный выстрел **тем же классом** оружия, reload, Overwatch,
  MobileShot, stim, end-turn TakeCover, пустые руки→ствол
  (`JAZZ_AIEnsureActiveFirearm`).
- Новая директива, новый archetype, смена шансов panic/deserter.
- Mod option в этом срезе (можно follow-up).
- Combat log spam (только floating text).

## Locked defaults

| Param | Value |
| --- | --- |
| Vehicle | `CreateFloatingText` on the speaker unit |
| Color | one speech color, not damage / heal / `Reload` |
| Voice | none |
| Who | enemy AI only (`team.player_enemy` or enemy side) |
| Visibility | `HasVisibilityTo(GetPoVTeam(), unit)` |
| Fast-forward | skip if `g_FastForwardGameSpeed == "Fast"` |
| Team cap | **2** barks per enemy team per AI-turn |
| Unit cap | **1** bark per activation |
| Event cap | same `event` id once per team per AI-turn |
| Once / combat | `panic`, `desert` per unit |
| Directive | shout only if id **changed** this write; **including** `HoldLine` / `GoHidden` |
| FocusFire | `order_focus` if display name exists, else `order_focus_anon` — one shout |
| Weapon | bark `wpn_*` only when bark-class **changes** (not every shot) |
| Variant | `unit:Random` among lines whose tags ⊆ facts; 5 lines/slot, ≥2 untagged |
| Copy | 440 strings, IDs `890000000020157`–`890000000020596` |
| Long dash | dest ≥ **12** tiles; skip if `FallBack` |
| Press bark | CMD-002 `kind=press` or directive `Push`, dest ≥ **6** tiles |
| Flank bark | directive `Envelop` or recontact probe, dest ≥ **6**; not if press already picked |
| State | `MapVar("JazzAI_CombatBarks", false)` — combat only; clear CombatStart / CombatEnd |

## Требования

- `JAZZ-AI-BARK-001-REQ-001` — новый loaded `jazz/Code/System_AI_CombatBarks.lua` в `metadata.lua.code` (рядом с прочими AI Code). `JazzAI_TryCombatBark(unit, event, ctx)` — единственная точка показа. Не создаёт глобалы в `OnMsg` обычным присвоением (`$jazz-lua-globals`).
- `JAZZ-AI-BARK-001-REQ-002` — барк не ставится, если юнит мёртв / invalid / unconscious; не враг; нет PoV visibility; идёт Fast-forward; сработал team/unit/event cap; `panic`/`desert` уже были в этом бою у юнита.
- `JAZZ-AI-BARK-001-REQ-003` — хуки только **после** решения:
  1. `JazzAI_WriteOfficerAura` — если `directive` ≠ last (все 10 директив CMD-001, включая `HoldLine` и `GoHidden`);
  2. смена динамического архетипа: `Panicked` / `Deserter` / `Berserk` / medic / melee (`JazzAI_SelectArchetype`, once/combat на юнита);
  3. Execute гранаты по `aoeType` → `nade_flare` / `nade_smoke` / `nade_frag` / `nade_fire` / `nade_gas`;
  4. смена bark-класса оружия после `SwapActiveWeapon` / `ChangeWeapon` → `wpn_rifle` | `wpn_shotgun` | `wpn_mg` | `wpn_sidearm` | `wpn_gl` | `wpn_rocket` | `wpn_sniper` | `wpn_melee`. Не орать на `JAZZ_AIEnsureActiveFirearm` (пустые руки→ствол);
  5. `AIActionMGSetup` deploy → `mg_setup` (не то же событие, что `wpn_mg`);
  6. после lock dest, **не** меняя dest. Приоритет (одно на активацию):
     - `seq_press` — `JazzAI_GetUnitActSlot(unit).kind == "press"` **или** директива `Push`, и длина пути ≥6; не `FallBack`;
     - иначе `seq_flank` — директива `Envelop` **или** `JazzAI_UnitIsRecontactProbe`, путь ≥6;
     - иначе `move_long` — путь ≥12 и не `FallBack` (AI-007 recontact / длинный рывок).
  Хуки не меняют score / destination / AP.
  CMD-002 support (flare / smoke / mg_setup / heal) уже закрыт событиями `nade_*` / `mg_setup` / `arch_medic`. Офицерский `order_push` — смена директивы; `seq_press` — боец Late-волны **бежит**. Event cap: один `seq_press` на команду за ход.
  Классы: `MeleeWeapon`→`melee`; `GrenadeLauncher`→`gl`; `RocketLauncher`/`HeavyWeapon`→`rocket`; `SniperRifle`→`sniper`; `Shotgun`→`shotgun`; `MachineGun`/`LightMachineGun`→`mg`; `Pistol`/`Revolver`→`sidearm`; прочий `Firearm` (AR/SMG/BR)→`rifle`. Барк только если класс **A≠B**.
- `JAZZ-AI-BARK-001-REQ-004` — голос: офицерский приказ — `boss` при aura radius **15**, `officer` при **25** или карта; индивидуальные — class tier из `unitdatadef_id` `_T1_` / `_T2_`|`_T3_` / `_T4_`, иначе `t2`. Канон и запрещённые формулировки — design-файл.
- `JAZZ-AI-BARK-001-REQ-005` — обе runtime-таблицы `Russian.csv` + `English.csv` для всех **440** ID; множества совпадают; аудитор `needs Russian=0` / `needs English=0`. Канон строк — `docs/tools/_aibark_bank_data.py` (5 фраз на слот).
- `JAZZ-AI-BARK-001-REQ-006` — player-facing docs: technical `ai-awareness.md` + `file-coverage.md`; wiki + showcase RU/EN `officer-aura` и короткий абзац в `combat-and-accuracy`.
- `JAZZ-AI-BARK-001-REQ-007` — выбор фразы **контекстный**. Теги в `_aibark_bank_data.py`; фраза играет, только если все её теги истинны. Пустой тег — всегда можно. Факты на момент окрика (не меняют AI):
  - `in` — цель / точка удара в интерьере (`AICheckIndoors` / `unit.indoors`);
  - `out` — эта точка снаружи;
  - `into` — говорящий снаружи и цель внутри (окно / дверь / «в хату»);
  - `high` — slab Z говорящего > цели (холм / крыша);
  - `houses` — на карте есть дома (`JazzAI_ShouldOccupyBuildings`).
  «Хата» / «окно» / «дверь» / «дом» (не «домой») без тега запрещены, кроме приказов `order_buildings` / `order_heights` (их уже отсекает picker). Не орать «хата», если цель на улице; взять untagged из того же слота. Не пустой пул: ≥2 untagged на слот.

## Инварианты и ограничения

- Не трогать `JazzAI_PickOfficerDirective` веса, fatigue, aura buffs, grenade budget, medic exclusive, Dump, FF logic besides the skip-read.
- Не писать в `gv_JAZZ_LegionAI`. Save schema без bump: только combat `MapVar`.
- Determinism: нет `AsyncRand` / wall-clock; только `unit:Random`.
- NetSync: текст косметика; выбор строки sync-safe. Не звать сеть.
- Не подменять существующий `CreateFloatingText` Reload / Jammed / status.
- Не показывать сырой UnitData / handle / «T3» / имя директивы в прозе.

## Acceptance criteria

- `JAZZ-AI-BARK-001-AC-001` — static: файл в metadata; `JazzAI_TryCombatBark`; MapVar declared at file load; loc 20157–20596 в RU+EN.
- `JAZZ-AI-BARK-001-AC-002` — static: хуки не меняют return/score обёрнутых Precalc/Execute кроме вызова bark после успешного решения.
- `JAZZ-AI-BARK-001-AC-003` — runtime/human: смена директивы на `Push` / `FallBack` / `FocusFire` / `HoldLine` / `GoHidden` у видимого офицера → один окрик; повтор того же приказа на следующем ходе без смены → тишина.
- `JAZZ-AI-BARK-001-AC-004` — runtime/human: `Panicked` и `Deserter` у видимого врага → по одной фразе на юнита за бой; массовый fear AOE не даёт пачку одинаковых окриков (event cap).
- `JAZZ-AI-BARK-001-AC-005` — runtime/human: видимый фаер / дым / осколок / огонь / газ / MG setup / **смена класса оружия** → фраза у исполнителя; тот же класс, пустые руки→ствол, невидимый или Fast-forward → нет текста.
- `JAZZ-AI-BARK-001-AC-006` — runtime/human: T1 и T4 на одном событии звучат по-разному (банк); сержант и капитан на приказе — разные ленты.
- `JAZZ-AI-BARK-001-AC-007` — human copy: ни одна показанная строка не совпадает с тултипом ауры и не звучит как radio/tutorial; owner читает банк вслух.
- `JAZZ-AI-BARK-001-AC-008` — docs: technical + file-coverage + wiki + showcase RU/EN.
- `JAZZ-AI-BARK-001-AC-009` — runtime/human: цель **снаружи** → ни «хата», ни «в окно/дверь»; цель **в интерьере**, говорящий снаружи → можно `into`; пулемёт «улицу крою» только если точка снаружи; снайпер «с холма» только если говорящий выше. Иначе нейтральная фраза того же слота.
- `JAZZ-AI-BARK-001-AC-010` — runtime/human: под `Push` Late-press с путём ≥6 → `seq_press` (не повтор офицерского `order_push`); `Envelop`/probe ≥6 → `seq_flank`; путь ≥12 без FallBack → `move_long`; короткий шаг и FallBack → тишина на этих трёх.

## Impact и совместимость

- Vanilla/CommonLib: только `CreateFloatingText` + тонкие after-hooks на уже переопределённых JAZZ AI функциях.
- Saves: mid-combat MapVar; старые сейвы без поля — пустой init.
- Network/determinism: cosmetic; `unit:Random` sync.
- Generated data: нет ModItem. `metadata.lua.code` — одна запись нового файла (не косметический reorder прочих).
- Cross-package: только `jazz`. UnitData id pattern `*T#*` читается, не пишется.
- Rollback: выгрузить файл из metadata + убрать хуки.

## План и ownership

- Пакет-владелец: jazz.
- Исполнитель: agent после `approved`.
- Reviewer: project-owner (обязательна вычитка банка).
- Exclusive: loc range выше; не пересекать с CMD-001 `6100–6125`.

## Решение владельца

- Статус: implemented (static). Runtime/human AC ещё открыты.
- Кто подтвердил: owner asked to ship after bank QA.
- Дата: 2026-08-24

## Evidence

- `JAZZ-AI-BARK-001-AC-001`: `PASS` (static) — `Code/System_AI_CombatBarks.lua` in `metadata.lua.code`; `JazzAI_TryCombatBark`; `MapVar JazzAI_CombatBarks`; loc `890000000020157–20596` in Russian.csv + English.csv (440 rows).
- `JAZZ-AI-BARK-001-AC-002`: `PASS` (static) — hooks are after-writes (`JazzAI_WriteOfficerAura`, `JazzAI_SelectArchetype`, `AIExecuteUnitBehavior`, grenade/MG Execute, `SwapActiveWeapon`); no score/dest/return mutation besides the bark call.
- `JAZZ-AI-BARK-001-AC-003`: `BLOCKED` — runtime/human.
- `JAZZ-AI-BARK-001-AC-004`: `BLOCKED` — runtime/human.
- `JAZZ-AI-BARK-001-AC-005`: `BLOCKED` — runtime/human.
- `JAZZ-AI-BARK-001-AC-006`: `BLOCKED` — runtime/human.
- `JAZZ-AI-BARK-001-AC-007`: `BLOCKED` — human copy review in combat.
- `JAZZ-AI-BARK-001-AC-008`: `PASS` (static) — `ai-awareness.md`, `file-coverage.md`, wiki + showcase RU/EN officer-aura and combat-and-accuracy.
- `JAZZ-AI-BARK-001-AC-009`: `BLOCKED` — runtime/human.
- `JAZZ-AI-BARK-001-AC-010`: `BLOCKED` — runtime/human.

## Documentation delta

Планируется при реализации (не раньше `approved`):

- `docs/technical/systems/ai-awareness.md` — bark layer, caps, silent events.
- `docs/technical/systems/file-coverage.md` — `System_AI_CombatBarks.lua` loaded.
- `docs/wiki/officer-aura.md` + showcase RU/EN — офицер орёт смену приказа.
- `docs/wiki/combat-and-accuracy.md` + showcase RU/EN — страх / граната / смена ствола, без спама.
