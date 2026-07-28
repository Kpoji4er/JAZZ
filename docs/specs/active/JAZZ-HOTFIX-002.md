---
id: JAZZ-HOTFIX-002
status: implemented
owner: project-owner
systems:
  - strategy-squads-sectors
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - Code/SatelliteSquad.lua
  - Code/POI Extension.lua
  - docs/specs/active/JAZZ-HOTFIX-002.md
  - docs/technical/systems/strategy-squads-sectors.md
  - docs/technical/override-matrix.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-HOTFIX-002: убрать двойной SatelliteTick и починить GetMineIncome

## Проблема

На глобальной карте наблюдаются подфризы, появившиеся **до** Legion AI. Причины:

1. `OnMsg` в движке **накапливает** handlers. Полный копипаст `Code/SatelliteSquad.lua` повторно регистрирует `OnMsg.SatelliteTick`, идентичный vanilla → каждый campaign tick выполняет `SatelliteUnitsTick` + `ObjModified` **дважды**.
2. Stub `GetMineIncome` в `POI Extension.lua` всегда возвращает число `(a or 0)+…`. В Lua `if 0 then` истинно, поэтому vanilla `SectorsTick` проходит income-ветку по **всем** секторам и зовёт 5 lookup’ов вместо early-out `nil`.

## Цели

- На один `Msg("SatelliteTick")` JAZZ не добавляет второй идентичный handler: tick path выполняется один раз.
- `GetMineIncome` возвращает `nil`, когда суммарный доход 0; пробрасывает `showEvenIfUnowned` во все источники.

## Non-goals

- Не рефакторить весь `SatelliteSquad.lua` до diff-only.
- Не снимать остальные duplicate `OnMsg` из того же файла (отдельный follow-up).
- Не менять Legion AI / Guardpost_Patrols.
- Не батчить `ObjModified` внутри vanilla tick.

## Требования

- `JAZZ-HOTFIX-002-REQ-001` — JAZZ не регистрирует `OnMsg.SatelliteTick`, если тело совпадает с vanilla; остаётся один handler (vanilla), вызывающий актуальный `SatelliteUnitsTick` (global override из JAZZ, сейчас идентичен vanilla).
- `JAZZ-HOTFIX-002-REQ-002` — `GetMineIncome(id, showEvenIfUnowned)` суммирует mine/farm/donations/wood/slon, возвращает `nil` при сумме 0, иначе сумму; второй аргумент передаётся во все источники.

## Инварианты и ограничения

- Поведение одного tick path не менять относительно vanilla (только кратность).
- Income для секторов с реальным POI-доходом сохраняется.
- Save/network contract не меняется.
- Deterministic RNG не затрагивается.

## Acceptance criteria

- `JAZZ-HOTFIX-002-AC-001` — static: в loaded `Code/SatelliteSquad.lua` нет активной регистрации `OnMsg.SatelliteTick` (закомментирована или удалена с пояснением).
- `JAZZ-HOTFIX-002-AC-002` — static: `GetMineIncome` возвращает `nil` при нулевой сумме и принимает `showEvenIfUnowned`.
- `JAZZ-HOTFIX-002-AC-003` — human/runtime: на satellite при ускорении времени подфризы заметно слабее vs до фикса (или не хуже baseline без двойного tick). `BLOCKED` до прогона в игре.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: снимает дубль JAZZ поверх vanilla SatelliteTick; другие моды с собственным SatelliteTick не затрагиваются `MsgClear`.
- Saves: без миграции.
- Network/determinism: один tick вместо двух — ближе к vanilla.
- Generated data: нет.
- Cross-package: нет.
- Rollback: вернуть handler / старый stub.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (запрос «поправить и закоммитить» после ревью двойного SatelliteTick)
- Дата: 2026-07-28

## Evidence

- `JAZZ-HOTFIX-002-AC-001`: `PASS` — static: `OnMsg.SatelliteTick` в `Code/SatelliteSquad.lua` обёрнут в `--[[ ... ]]` с комментарием JAZZ-HOTFIX-002.
- `JAZZ-HOTFIX-002-AC-002`: `PASS` — static: `GetMineIncome(id, showEvenIfUnowned)` суммирует источники и `return` при `income == 0`.
- `JAZZ-HOTFIX-002-AC-003`: `BLOCKED` — runtime/human: прогон satellite с ускорением времени в игре.

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — OnMsg append + снятие дубля SatelliteTick; GetMineIncome nil contract.
- `docs/technical/override-matrix.md` — пометка про нерегистрируемый SatelliteTick handler.
