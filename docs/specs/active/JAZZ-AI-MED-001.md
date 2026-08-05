---
id: JAZZ-AI-MED-001
status: approved
owner: project-owner
systems: [tactical-ai]
repositories: [jazz, jazz-units]
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-MED-001.md
  - jazz/Code/AiActions.lua
  - jazz-units/items.lua
  - jazz-units/Code/AICombatStance.lua
exclusive_resources: [jazz-units/items.lua]
related_decisions: [docs/design/tactical-ai-archetypes.md]
approved_by: project-owner
---

# JAZZ-AI-MED-001: Medic early heal + Bandage fail-safe

## Проблема

Medic freeze на Bandage unreachable; Late-only heal; bleed не приоритетнее HP%.

## Цели

- Bleed-first + early 85% Healer; turn_phase Early; exclusive Healer vs Standard/SeekEnemy; один Bandage entry; OptLocSearchRadius 45; Execute fail-safe без freeze.

## Non-goals

- Новый Medic archetype ID; POL/CTX/CMD/ACT.

## Требования

- `JAZZ-AI-MED-001-REQ-001` — Healer Score: Bleeding → высокий weight; иначе HP&lt;85%.
- `JAZZ-AI-MED-001-REQ-002` — turn_phase Early; один Priority Bandage (перед MobileShot); при bleed/HP need Healer exclusive (combat behavior Score = 0).
- `JAZZ-AI-MED-001-REQ-003` — OptLocSearchRadius ≤45.
  - items.lua: Medic / Medic_Low = 45.
  - **Runtime:** `JazzAI_ApplyMedicOptLocCap` in `Code/AICombatStance.lua` (`ModsReloaded` / `DataLoaded`) clamps preset to 45 so editor autosave cannot restore 80.
- `JAZZ-AI-MED-001-REQ-004` — Bandage unreachable → no "stop" freeze; optional revert Frontliner.

## Инварианты и ограничения

- Determinism; не ломать Stim path.

## Acceptance criteria

- `JAZZ-AI-MED-001-AC-001` — static: Medic Healer Normal + 85% + single Bandage + radius 45.
- `JAZZ-AI-MED-001-AC-002` — static: AIActionBandage:Execute fail-safe in AiActions.lua.
- `JAZZ-AI-MED-001-AC-003` — runtime/human: medic не вешает ход; bleed первым.

## Impact и совместимость

- jazz AiActions + jazz-units Medic preset; saves ок.

## План и ownership

- Пакеты: jazz + jazz-units. Исполнитель: agent. Reviewer: project-owner.

## Решение владельца

- Статус: approved (доделаем все 29.07.2026). Кто: project-owner. Дата: 2026-07-29.

## Evidence

- `JAZZ-AI-MED-001-AC-001`: `PASS` (static, re-verified) — Medic/Medic_Low Healer Score = bleed (all Jazz tiers) OR HP&lt;85%; combat behaviors Score=0 while heal needed; `turn_phase` Early; OptLoc/Bandage MaxHp 85 + BleedingWeight 300 + SelfHealMod 100; Priority Bandage before MobileShot; radius 45 via ApplyMedicOptLocCap.
- `JAZZ-AI-MED-001-AC-002`: `PASS` — static Execute fail-safe + Precalc score&gt;0 / JazzBandage fallback in AiActions.lua; `AISelectHealTarget` override in CombatAI.lua (self-bleed skips SelfHealMod penalty).
- `JAZZ-AI-MED-001-AC-003`: `BLOCKED` — smoke/human: medic treats bleed (incl. self) before advancing/engaging.

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — medic heal / bleed targeting
- `docs/design/tactical-ai-archetypes.md` — Medic Healer Normal / 85% / bleed-first
- `docs/showcase/en/legion-units.md`, `docs/showcase/ru/legion-units.md` — Bonemaker treats bleeding
