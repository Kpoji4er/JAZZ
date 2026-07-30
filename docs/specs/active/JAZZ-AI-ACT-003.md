---
id: JAZZ-AI-ACT-003
status: approved
owner: project-owner
systems:
  - tactical-ai
  - combat-actions
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-ACT-003.md
  - jazz/Code/AiActions.lua
  - jazz/Code/CombatAI.lua
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/weapons/combat-actions.md
  - jazz/metadata.lua
exclusive_resources:
  - none
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/specs/active/JAZZ-AI-ACT-002.md
approved_by: project-owner
---

# JAZZ-AI-ACT-003: AI MGSetup с half-cover bipod (без forced Prone)

## Проблема

Игрок может развернуть пулемётный overwatch (`MGSetup`) из **половинчатого укрытия** (`CoverLow`, `coverage > 80`): статус `BipodUnfolded`, стойка **не** форсится в `Prone` (`Unit:MGSetup`, UI-конус в `IModeCombatAreaAim`, CTH `Bipod`).

ИИ этой доктриной не пользуется:

1. `AIActionMGSetup:PrecalcAction` пытается детектить halfcover, но до выбора зоны вызывает `GetCoverPercentage(curr_target_pt or context.unit)`. На первом setup OW ещё нет → запрос cover «от себя» → halfcover почти никогда не true → Precalc всегда планирует `Prone`.
2. `action_state.stance` почти не влияет на execute: `Unit:MGSetup` пересчитывает halfcover по `args.target`; Precalc-stance для `AIPrecalcConeTargetZones` не применяется (параметр `stance` в LoF не используется; для `MGSetup` зоны early-return без CTH-фильтра).
3. Нет позиционного bias «искать low cover под bipod-deploy»: MG PositioningAI оптимизирует LOS/range/damage; setup часто в открытом поле → всегда prone-deploy.

Итог: execute-путь фичи для ИИ теоретически жив, если юнит случайно crouch за хорошим low cover с правильным углом cone; как **намеренная тактика** — нет.

## Цели

- ИИ при `MGSetup` использует **тот же** halfcover-предикат, что игрок: `CoverLow` и `coverage > 80` относительно **выбранной** точки сектора (`zone.target_pos` / `args.target`).
- При halfcover ИИ планирует и исполняет setup в **Crouch** (не Prone), с `BipodUnfolded` через существующий `Unit:MGSetup`.
- Без halfcover поведение остаётся vanilla-like: Prone + stationed MG sector.
- Dest/EndTurn scoring для MG setup **предпочитает** достижимые voxels с usable low cover в сторону угрозы/коридора, когда signature `AIActionMGSetup` актуальна.

## Non-goals

- Менять порог `coverage > 80`, семантику `Unit:MGSetup` / `BipodUnfolded` / UI для игрока.
- Новые CombatAction / CharacterEffect / archetype ID.
- Полный ребаланс `Legion_Machinegunner` / `Rebels_Machinegunner` (веса DealDamage, min_score, BiasId period).
- Отдельный revive удалённого `Rato_MGSetupPosScore.lua` как обязательный файл (scoring — в `AiActions` / `CombatAI` / существующий `AIPolicy`).
- Обычный (не-MG) `Overwatch` cone из half cover.
- Player-facing wiki/showcase (поведение для игрока уже есть; меняется только AI).

## Требования

- `JAZZ-AI-ACT-003-REQ-001` — общий helper (например `JazzAI_IsMGHalfCoverDeploy(unit, aim_pos [, stance])`) повторяет player-предикат: `unit:GetCoverPercentage(aim_pos)` → `cover == const.CoverLow` и `coverage > 80`. Не использовать `context.unit` как attack direction.
- `JAZZ-AI-ACT-003-REQ-002` — в `AIActionMGSetup:PrecalcAction` при отсутствии `StationedMachineGun`: сначала `AIActionBaseConeAttack.PrecalcAction` / EvalZones выбирает зону; **затем** halfcover считается по `zone.target_pos` (или `action_state.args.target` / `target_pos`). `action_state.stance` = `"Crouch"` при halfcover, иначе `"Prone"`.
- `JAZZ-AI-ACT-003-REQ-003` — перед execute `MGSetup`, если halfcover и unit не в `Crouch` (в т.ч. `Prone`/`Standing`), ИИ переводит в `Crouch` (AP/stance cost как у обычного AI stance change), затем вызывает setup. Без halfcover — допустим Prone как сейчас (через `Unit:MGSetup` или явный stance).
- `JAZZ-AI-ACT-003-REQ-004` — при оценке reachable dest под активный/приоритетный `AIActionMGSetup` (или MG Positioning label) voxel с low cover, дающим halfcover vs хотя бы одного релевантного enemy / last-known / corridor aim, получает **явный score bonus**. Open-ground dest без cover не штрафуются ниже работоспособности prone-setup (не запрещать vanilla prone lane).
- `JAZZ-AI-ACT-003-REQ-005` — уже stationed ветка (MGRotate / MGPack) не ломается; halfcover re-check при rotate опционален и не обязан менять stance mid-overwatch без нужды.

## Инварианты и ограничения

- Determinism: без нового `InteractionRand` в halfcover/dest path; порядок оценки зон стабилен.
- Player `Unit:MGSetup` / `IModeCombatAreaAim` / CTH `Bipod` контракт не менять без отдельного spec.
- `StationedMachineGun`, permanent OW, `MGBurstFire` interrupt path без регрессий.
- Не требовать `jazz-units` `items.lua` в этом change set; archetype PrefStance `Crouch` у Legion/Rebels MG уже совместим.
- Saves: только ephemeral AI state / status effects как сейчас.
- CommonLib: не расширять коллизии сверх существующих override `AiActions` / `CombatAI`.

## Acceptance criteria

- `JAZZ-AI-ACT-003-AC-001` — **static**: Precalc больше не вызывает halfcover через `GetCoverPercentage(context.unit)` на первом setup; helper + post-zone stance selection присутствуют; dest bonus path присутствует.
- `JAZZ-AI-ACT-003-AC-002` — **runtime/human S1**: MG-юнит за полноценным half cover (парапет/мешки) с врагом по ту сторону — выбирает `MGSetup`, остаётся **Crouch**, получает `BipodUnfolded` / permanent sector, не уходит в Prone.
- `JAZZ-AI-ACT-003-AC-003` — **runtime/human S2**: тот же archetype в открытом поле без usable low cover — `MGSetup` в **Prone** как раньше; сектор валиден.
- `JAZZ-AI-ACT-003-AC-004` — **runtime/human S3**: при наличии reachable half-cover lane и open lane с похожим LOS, dest/setup **чаще** берёт half-cover ( qualitatively; не строгий %, playtest note).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: override `AIActionMGSetup:PrecalcAction` / Execute stance prep; возможно `AIPrecalcConeTargetZones` stance wiring или dest score hook. Player MGSetup body не трогать без нужды.
- Saves: нет нового persistent contract.
- Network/determinism: только детерминированные cover/LOS/score.
- Generated data: нет (если не трогаем units items).
- Cross-package: читает cover/OW runtime; units archetypes без обязательного diff.
- Rollback: revert Code + docs + metadata `last_changes` / minor при bump.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: see frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (chat 2026-07-31: «делай, только аккуратно»)
- Дата: 2026-07-31

## Evidence

- `JAZZ-AI-ACT-003-AC-001`: `PASS` (static) — `JazzAI_IsMGHalfCoverDeploy` / `JazzAI_MGHalfCoverDestBonus` in `Code/AiActions.lua`; Precalc picks zone then halfcover vs aim (no `GetCoverPercentage(context.unit)`); Execute crouch-then-setup; `AIScoreDest` +45 hook in `Code/CombatAI.lua`.
- `JAZZ-AI-ACT-003-AC-002`: `BLOCKED` — runtime/human S1 (crouch+bipod behind half cover).
- `JAZZ-AI-ACT-003-AC-003`: `BLOCKED` — runtime/human S2 (open field Prone).
- `JAZZ-AI-ACT-003-AC-004`: `BLOCKED` — runtime/human S3 (prefers half-cover lane).

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — ACT-003 current-state + load note
- `docs/technical/weapons/combat-actions.md` — MGSetup halfcover + AI note
- `docs/design/tactical-ai-archetypes.md` — MGSetup audit row ACT-003
- Wiki/showcase not required (player contract unchanged)
