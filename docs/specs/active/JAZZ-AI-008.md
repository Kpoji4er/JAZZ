---
id: JAZZ-AI-008
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
  - jazz/docs/specs/active/JAZZ-AI-008.md
  - jazz/Code/CombatAI.lua
  - jazz/Code/AIContextProfiles.lua
  - jazz/Code/AiActions.lua
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/wiki/officer-aura.md
  - jazz/docs/showcase/ru/officer-aura.md
  - jazz/docs/showcase/en/officer-aura.md
  - jazz/docs/tools/_check_ai_008_egress_perch.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - none
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/specs/active/JAZZ-AI-007.md
  - docs/specs/active/JAZZ-AI-SNIPER-001.md
  - docs/specs/active/JAZZ-AI-OW-001.md
  - docs/specs/active/JAZZ-AI-CMD-001.md
approved_by: project-owner chat 2026-08-24 (надо делать; снайпер держит если LoF есть или будет на egress)
---

# JAZZ-AI-008: Hold high ground that sees player egress

## Проблема

На L4 (ход 16) линия Легиона стоит на скале/склоне. Игрок прячется за непростреливаемой сеткой — личного LOS нет, но с высоты по-прежнему виден **выход** (угол камня, куда Benny пойдёт). Сейчас ИИ бросает высоту:

1. `dest_target_score[stay] = 0` (нет тела в LoF) → **JAZZ-AI-SNIPER-001** считает ход бесполезным и за 2–3 хода обнуляет `AIPolicyHighGround`.
2. **JAZZ-AI-007** recontact без vis тянет dest в пояс 14–20 от `last_known` — спуск с крыши «ближе к звуку».
3. `AIPolicyHighGround:EvalDest` считает высоту относительно **текущей** клетки (`z - uz`), поэтому stay всегда даёт 0 за высоту.

Fallback OW уже умеет целиться в клетку выхода (007/OW-001). Dest-scoring эту «потенциальную видимость» не держит.

## Цели

- Линейный боец на **выгодной высоте**, с которой виден выход игрока, **остаётся** и ставит Fallback OW на egress, даже если модельки сейчас не видно.
- Штурмовик / фланг / медик / дезертир / farm-мишень это **не** делает: они по-прежнему сходят и ищут угол.
- Не возвращать `GetLoFData` в targeting.

## Non-goals

- Новые archetype ID / generated `items.lua` policies.
- Менять пояс recontact 14–20 для тех, кто **не** на perch.
- Менять Dump/cheap LoF (PERF-004).
- OccupуHeights aura rewrite (CMD-001 множитель HighGround остаётся).
- Полный peek_streak / AntiPeekOW.

## Требования

- `JAZZ-AI-008-REQ-001` — `JazzAI_UnitIsLinePerchHolder(unit)`: keyword `Sniper`/`Marksman`, или dynamic semi-sniper, или archetype `*_Frontliner` / `*_Machinegunner`, или aura `OccupyHeights`. **Не** Assaulter / Flanker / Medic / Deserter / `Legion_Regroup` / melee keyword / aura `pusher`.
- `JAZZ-AI-008-REQ-002` — `JazzAI_DestIsEgressPerch(context, dest)` истинно только если все:
  1. holder (REQ-001);
  2. нет личных видимых врагов (`GetVisibleEnemies` пуст);
  3. есть `last_known_enemy_pos`;
  4. dest **не** farm (007 REQ-006: игрок видит юнита, юнит не видит никого из player_team) — spotted-and-blind обязан сдвинуться;
  5. dest выше якоря: voxel Z dest ≥ last_known Z **+ 1** (const.SlabSizeZ / packed z);
  6. `egress` = тот же выбор, что Fallback OW (`JazzAI_FallbackOverwatchTargetPos` / LOS-viable клетка выхода). `CheckLOS` dest→egress в пределах `ExtremeRange` или `WeaponRange`;
  7. Burning / Reposition — false.
- `JAZZ-AI-008-REQ-003` — `JazzAI_ScoreRecontactDest`: если dest — stay и perch, **+180** и **не** применять бонус «идти ближе к last_known» / штраф stay за пояс. Остальные dest юнита скорятся как в 007.
- `JAZZ-AI-008-REQ-004` — `JazzAI_ApplySniperHoldDestination` (и тот же wrap `AIScoreReachableVoxels` для Frontliner/MG без sniper keyword): если stay — perch, выбранный dest **заменяется на stay**. `JazzAI_NoteSniperUselessTurn` для perch **не** инкрементирует streak (коридор = полезная позиция).
- `JAZZ-AI-008-REQ-005` — после Disengage на perch без vis: Fallback OW на egress, как OW-001/007 (не random, не в стену).
- `JAZZ-AI-008-REQ-006` — без нового RNG. `JazzAI_HasLosToPos` / Fallback OW target pos — generic (не local-only в `AiActions.lua`), чтобы dest-score и OW делили якорь.
- `JAZZ-AI-008-REQ-007` — docs: technical `ai-awareness.md` + wiki/showcase officer-aura (линия держит высоту, если виден выход).

## Инварианты и ограничения

- 007 farm relocate не отменяется perch.
- Assaulter у подножия скалы без LOS на egress **не** hold (L4 ShockTrooper в камень — не perch).
- SNIPER-001 hold-if-shot (`dest_target_score[stay] > 0`) важнее: живой выстрел → stay как сейчас.
- DestLos/Precalc caps не расширять ради perch.
- Deterministic; ephemeral combat only.

## Acceptance criteria

- `JAZZ-AI-008-AC-001` — static: helpers + ScoreRecontact stay+180; hold wrap for line holders; useless streak skip on perch; Fallback OW pos shared; no GetLoFData.
- `JAZZ-AI-008-AC-002` — runtime/human L4: Frontliner/sniper на скале без LOS на Benny, но с LOS на угол/выход — **остаётся** и ставит сектор туда, не спускается «к звуку».
- `JAZZ-AI-008-AC-003` — runtime/human: Assaulter без LOS на egress не кемпит; farm-мишень на хребте сдвигается (007).
- `JAZZ-AI-008-AC-004` — docs: technical + wiki + showcase RU/EN officer-aura.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: wrap `AIScoreReachableVoxels` + `JazzAI_ScoreRecontactDest`; вынести OW pos helper.
- Saves: ephemeral (тот же MapVar streak).
- Network/determinism: без нового RNG.
- Generated data: нет.
- Cross-package: keywords/archetype id из `jazz-units`; runtime в `jazz`.
- Rollback/recovery: revert Lua + spec.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: implemented
- Кто подтвердил: project-owner (чат 2026-08-24: «снайпер должен на lof держать позицию если потенциально она будет — это к JAZZ-AI-008 надо делать»)
- Дата: 2026-08-24

## Evidence

- `JAZZ-AI-008-AC-001`: `PASS` (static) — `python docs/tools/_check_ai_008_egress_perch.py`; holder/perch helpers; ScoreRecontact stay +180; hold wrap; HasLosToPos/FallbackOverwatchTargetPos/DestSeesPos global; no GetLoFData in perch.
- `JAZZ-AI-008-AC-002`: `BLOCKED` — runtime/human L4: Frontliner/sniper on ridge without LOS on Benny, LOS on egress — stays and OW, does not drop toward sound.
- `JAZZ-AI-008-AC-003`: `BLOCKED` — runtime/human: Assaulter without egress LOS does not camp; farm target still relocates.
- `JAZZ-AI-008-AC-004`: `PASS` (static) — technical `ai-awareness.md` + override-matrix + wiki/showcase RU/EN officer-aura.

## Documentation delta

- `docs/technical/systems/ai-awareness.md`
- `docs/technical/override-matrix.md`
- `docs/design/tactical-ai-archetypes.md`
- `docs/wiki/officer-aura.md`
- `docs/showcase/ru/officer-aura.md`
- `docs/showcase/en/officer-aura.md`
