---
id: JAZZ-COMBAT-001
status: implemented
owner: project-owner
systems:
  - combat-cth-actions
  - armor-damage-wounds-will
  - weapons-ammo-components
  - runtime-editor-integration
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/AccuracyRangeCTH.lua
  - jazz/Code/System_ArmorRating.lua
  - jazz/Code/System_OR_Weapons.lua
  - jazz/CharacterEffect/DamageReduction.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/AGENTS.md
  - jazz/.agents/docs/reference/project-scope.md
  - jazz/.agents/docs/reference/generated-data-sync.md
  - jazz/docs/specs/active/JAZZ-COMBAT-001.md
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/technical/systems/armor-damage-wounds-will.md
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/technical/systems/runtime-editor-integration.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/testing.md
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - Mod Editor state for DamageReduction
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMBAT-001: эффекты попадания, трассеры и урон на дистанции

## Проблема

В незакоммиченной реализации дальностного урона объект preset передавался в `hit.effects` вместо строкового ID, обычные эффекты попадания отбрасывались некорректной проверкой структуры, непробитая броня не имела явного контракта блокировки физических статусов, а формула дальностного урона могла вернуть отрицательный процент. Generated companion `DamageReduction` потерял обязательный заголовок полной замены vanilla-класса. Трассерный эффект должен работать при промахе, но только для фактически произведённого выстрела с ненулевой вероятностью попадания.

## Цели

- восстановить строковый контракт `hit.effects`;
- отделить shot-level эффект трассеров от hit-level эффектов попадания;
- запретить обычные физические статусы при непробитой закрывающей броне;
- ограничить дальностный damage multiplier диапазоном `0..100`;
- восстановить полную замену vanilla-класса `DamageReduction`;
- закрепить общее правило полной замены vanilla-классов в проектных контрактах.

## Non-goals

- изменение общего баланса оружия, CTH или бронепробития;
- переименование публичного ID `MarkedTraccers`;
- изменение версии CommonLib или dependency metadata;
- исправление посторонних orphan generated companions;
- изменение карт, юнитов или assets.

## Требования

- `JAZZ-COMBAT-001-REQ-001` — `hit.effects` содержит только непустые строковые CharacterEffect ID; preset/class objects не добавляются.
- `JAZZ-COMBAT-001-REQ-002` — обычные hit-level эффекты применяются без закрывающей брони либо при наличии хотя бы одного пробитого предмета в `hit.armor_pen`.
- `JAZZ-COMBAT-001-REQ-003` — `MarkedTraccers` применяется один раз за каждый фактически произведённый трассерный выстрел по unit-цели с итоговым `shot_cth > 0`, независимо от попадания; при CTH `0`, jam или отсутствии выстрела не применяется.
- `JAZZ-COMBAT-001-REQ-004` — `GetRangeDamageReduction` возвращает значение только в диапазоне `0..100`, а вызывающая сторона передаёт `attacker` и `action`.
- `JAZZ-COMBAT-001-REQ-005` — `DamageReduction` полностью заменяет vanilla-класс с сохранением ID через `UndefineClass('DamageReduction')` непосредственно перед `DefineClass.DamageReduction = { ... }`.
- `JAZZ-COMBAT-001-REQ-006` — общее правило полной замены vanilla-классов отражено в project/generated/technical current-state документации.

## Инварианты и ограничения

- Публичные ID `DamageReduction` и `MarkedTraccers` не меняются.
- Прогноз атаки не мутирует status effects цели.
- Трассерное попадание не добавляет второй stack через damage pipeline.
- Psycho остаётся защищён от потери Will, но не получает отдельного иммунитета к трассерной метке.
- Существующие сигнатуры vanilla entry points, порядок `metadata.lua.code` и deterministic shot RNG сохраняются.
- Generated companion, `items.lua` и `metadata.lua` рассматриваются как одна editor-owned транзакция.

## Acceptance criteria

- `JAZZ-COMBAT-001-AC-001` — `DamageReduction.lua` начинается обязательной парой override, а `items.lua` и `metadata.lua` содержат ровно одну соответствующую регистрацию.
- `JAZZ-COMBAT-001-AC-002` — дальностный multiplier на ближней, рабочей, предельной и запредельной дистанции остаётся в `0..100` и учитывает `attacker`/`action`.
- `JAZZ-COMBAT-001-AC-003` — без брони и при пробитии обычный effect применяется, при непробитой закрывающей броне не применяется.
- `JAZZ-COMBAT-001-AC-004` — трассерный hit и miss при CTH больше нуля дают по одному stack на произведённый выстрел; CTH `0`, jam и отсутствие выстрела stack не дают.
- `JAZZ-COMBAT-001-AC-005` — scoped `git diff --check`, статические contract assertions и профильный documentation check проходят либо известные baseline-блокеры перечислены.
- `JAZZ-COMBAT-001-AC-006` — Mod Editor load/save/reload подтверждает generated round-trip без ignored mod, load/runtime error и assert.
- `JAZZ-COMBAT-001-AC-007` — чистый запуск игры, новая игра и существующее сохранение подтверждают hit/miss, armor penetration, range damage и tracer stacking.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ сохраняет намеренные overrides vanilla damage/effect pipeline; подтверждённый CommonLib 1.11 build 1056 не определяет затронутые символы.
- Saves: новые persistent fields не добавляются; существующие game-time threads могут продолжить старый bytecode до завершения.
- Network/determinism: новый RNG не добавляется; решение о tracer stack основано на уже рассчитанном deterministic `shot_cth`.
- Generated data: восстановлен companion `DamageReduction`; требуется Mod Editor round-trip.
- Cross-package references: новых ссылок нет.
- Rollback/recovery: откатить runtime, companion и technical/spec delta одним change set.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: Codex.
- Reviewer: project-owner.
- Declared write set: поля `write_set` front matter.
- Exclusive resources: `items.lua`, `metadata.lua`, Mod Editor state `DamageReduction`.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner.
- Дата: 26 июля 2026 года.
- Основание: владелец явно подтвердил ошибки, уточнил правила `DamageReduction` и `MarkedTraccers`, поручил исправить их и отправить весь change set в `main`.

## Evidence

- `JAZZ-COMBAT-001-AC-001`: `PASS` — static; header, brace balance, одна metadata code registration и один ModItem ID подтверждены contract assertions.
- `JAZZ-COMBAT-001-AC-002`: `PASS` — static smoke; значения для range `30`/effective range `15` на дистанциях `0, 15, 30, 45, 60` равны `100, 100, 1, 0, 0`.
- `JAZZ-COMBAT-001-AC-003`: `PASS` — static truth table; no armor=`true`, armor/no penetration=`false`, armor/penetration=`true`.
- `JAZZ-COMBAT-001-AC-004`: `PASS` — static truth table и code inspection; fired/CTH `1`=`true`, fired/CTH `0`=`false`, not fired/CTH `75`=`false`.
- `JAZZ-COMBAT-001-AC-005`: `PASS` — scoped `git diff --check` и contract assertions прошли; strict generated audit больше не сообщает malformed `DamageReduction`, но сохраняет 12 посторонних orphan-ошибок и предупреждение о необходимом editor round-trip.
- `JAZZ-COMBAT-001-AC-006`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-COMBAT-001-AC-007`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`

## Documentation delta

- Обновлены current-state страницы armor/damage, combat/CTH, weapons/ammo, runtime/editor, compatibility, override matrix и общий testing contract.
- Общее правило полной замены vanilla-классов добавлено в `AGENTS.md` и project/generated references.
- `docs/wiki/` отсутствует и не входит в Definition of Done.
