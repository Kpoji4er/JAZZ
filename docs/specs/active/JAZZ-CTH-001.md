---
id: JAZZ-CTH-001
status: approved
owner: project-owner
systems:
  - combat-cth-actions
  - weapons-ammo-components
  - ai-awareness
  - ui-audio-fx
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/AccuracyRangeCTH.lua
  - jazz/Code/System_OR_Unit.lua
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/CombatAI.lua
  - jazz/Code/CrossHairUI.lua
  - jazz/Code/System_Firearm_AddProperties.lua
  - jazz/InventoryItem/*.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/scripts/test-shooting-model.ps1
  - jazz/docs/specs/active/JAZZ-CTH-001.md
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/technical/testing.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/technical/systems/ui-audio-fx.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/weapons/README.md
  - jazz/docs/technical/weapons/accuracy-model.md
  - jazz/docs/technical/weapons/class-roles.md
  - jazz/docs/technical/weapons/combat-actions.md
  - jazz/docs/technical/weapons/data/*.csv
  - jazz/.agents/docs/reference/documentation-contract.md
  - jazz/.agents/skills/document-jazz-systems/SKILL.md
  - jazz/.agents/skills/document-jazz-systems/references/documentation-map.md
  - jazz/.agents/skills/document-jazz-systems/scripts/check-system-docs.ps1
  - jazz/Localization/Strings.csv
  - jazz/ModTextsJazz.csv
  - jazz/docs/README.md
  - jazz/docs/decisions/ADR-0002-technical-and-player-docs.md
  - jazz/docs/wiki/**
  - jazz/scripts/docs/weapons-docs.mjs
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - Mod Editor state for weapon, component and CTH presets
related_decisions:
  - ADR-0002-technical-and-player-docs
approved_by: project-owner
---

# JAZZ-CTH-001: множительная модель стрельбы

## Проблема

Текущий runtime строит базовый CTH из Marksmanship, Dexterity либо Strength, уровня и последовательности аддитивных модификаторов. Дистанция добавляется отдельным штрафом, а отдача линейно вычитает CTH последующих пуль. Такая композиция легко схлопывается в `0%` или `100%`, позволяет запасу положительных пунктов поглощать укрытие и плохо разделяет интуитивную стрельбу навскидку с подготовленным огнём.

Незакоммиченный плейтестовый эксперимент не был принят владельцем проекта как реализационная база. Утверждённый дизайн находится в `docs/technical/weapons/accuracy-model.md`, `class-roles.md` и `combat-actions.md`; его необходимо перенести в единый runtime-контур, которым одинаково пользуются фактическая атака, UI и AI.

## Цели

- построить единое расчётное ядро CTH с Dexterity-каналом навскидку и Marksmanship-каналом подготовленного огня;
- перевести дистанцию, укрытие, состояния, компоненты, перки и отдачу на явные множители;
- сохранить ненулевой шанс физически возможного выстрела и достижимые идеальные `100%`;
- заставить UI, AI и firearm executor использовать один результат и одну последовательность пуль;
- сдвигать оптикой эффективную прицельную зону без увеличения физического предела оружия;
- мигрировать активные оружейные и компонентные параметры согласованно с каноническими тирами;
- сохранить игроковый язык `+`/`−` без debug и точные проценты в debug.

## Non-goals

- изменение damage, armor penetration, tracer и hit-effect контрактов `JAZZ-COMBAT-001`;
- произвольный ребаланс AP, урона и пакетов пуль каждого специального CombatAction;
- изменение карт, UnitData, моделей, текстур, звуков или FX;
- external publishing of the player wiki and manual edits to generated weapon-family pages;
- объявление первого набора коэффициентов окончательным балансом после одного плейтеста;
- переименование стабильных публичных weapon, component, perk или CombatAction ID.

## Требования

- `JAZZ-CTH-001-REQ-001` — невозможная атака возвращает `0%`; физически возможная атака после единственного финального округления ограничивается диапазоном `2..100%`.
- `JAZZ-CTH-001-REQ-002` — опытный стрелок получает `100%` по открытой цели в полный рост при полном aim и оптимальной дистанции, а любой применимый штраф снижает этот результат.
- `JAZZ-CTH-001-REQ-003` — нулевой aim преимущественно использует Dexterity, полный aim раскрывает Marksmanship; второй стат и Level сохраняют меньший вклад, а дополнительный aim не уменьшает CTH.
- `JAZZ-CTH-001-REQ-004` — `Handling` не участвует в CTH; Strength влияет на пулемёт через отдачу, стойку, опору и развёртывание, а не заменяет Dexterity.
- `JAZZ-CTH-001-REQ-005` — `AimAccuracy` определяет пользу aim-клика, `MaxAimActions` — число кликов, а нелинейный aim mastery следует принятой модели `Пист`.
- `JAZZ-CTH-001-REQ-006` — `BulletDropRange`, `WeaponRange`, `Grouping` и эффективная граница `E` образуют непрерывный дистанционный профиль; непосредственно перед физическим пределом сохраняется floor, а на пределе обычная атака становится невозможной.
- `JAZZ-CTH-001-REQ-007` — оптика изменяет `E` через профиль reach/min-range/near-factor и aim progress, но не увеличивает `WeaponRange`, не переписывает `BulletDropRange` и не подменяет `Grouping`.
- `JAZZ-CTH-001-REQ-008` — укрытие, положение цели, видимость, подавление, мораль/статусы, действие, перк, компонент и состояние оружия сводятся в одно произведение fixed-point факторов без промежуточного округления.
- `JAZZ-CTH-001-REQ-009` — один эффект учитывается либо преобразованием профильного параметра, либо отдельным фактором, но не обоими способами; скрытые плоские perk-бонусы к CTH не используются.
- `JAZZ-CTH-001-REQ-010` — отдача последующих пуль использует retention-множитель из Recoil, Strength, стойки, опоры и компонентов, монотонно изменяет CTH и применяется ровно один раз.
- `JAZZ-CTH-001-REQ-011` — базовые режимы, физическая совместимость оружия, перковые техники, уникальные действия и персональные способности остаются отдельными слоями доступности.
- `JAZZ-CTH-001-REQ-012` — обычный UI скрывает итоговый процент и показывает различающееся количество `+`/`−`; debug показывает final CTH, core, факторы, `before → after` и CTH каждой пули.
- `JAZZ-CTH-001-REQ-013` — AI получает aim-level и multishot prediction из того же ядра, что crosshair и фактическая атака; отдельная линейная модель отдачи AI удаляется.
- `JAZZ-CTH-001-REQ-014` — активное оружие и компоненты мигрируются из канонического каталога по большим тирам; под-тиры меняют профиль без скачка, равного переходу большого тира.
- `JAZZ-CTH-001-REQ-015` — `AR15`, `M4Commando` и базовый `MP5` не возвращаются в активный каталог; `CompactSMG`/`CompactSubmachineGun` и legacy-действие ручного затвора не возвращаются в новую модель.
- `JAZZ-CTH-001-REQ-016` — все вычисления, влияющие на shot RNG, сохраняют deterministic ordering, существующие entry-point signatures и один общий NetUpdateHash-контракт.

## Инварианты и ограничения

- `Unit:CalcChanceToHit`, `Firearm:GetAttackResults`, `CombatActions` и существующие public IDs сохраняют вызываемые движком сигнатуры.
- Новые persistent fields, `GameVar`, `MapVar` и новый RNG не добавляются.
- Предварительный cap core выполняется до ситуационных факторов, поэтому избыток навыка не поглощает штраф.
- Математически коммутативные факторы хранятся в детерминированном fixed-point масштабе и перемножаются в стабильном порядке ID.
- Направление уже состоявшегося промаха не является вторым штрафом вероятности.
- АК-47 остаётся универсальнее и дешевле; СВД превосходит его в подготовленной средней и дальней стрельбе, но не обязана быть лучше вблизи.
- Перк может помочь достичь идеального результата, но не является скрытым обязательным условием штатных `100%`.
- Первый целостный плейтест выполняется только после согласованной миграции core, факторов, отдачи, оптики, AI, UI и активных данных.
- CommonLib snapshot: `main` commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c`, version `1.11`, build `1056`; это снимок аудита, не pin.
- `JAZZ-COMBAT-001` остаётся владельцем своего исторического damage/tracer change set; его незакрытые runtime evidence не считаются evidence этой спецификации.

## Acceptance criteria

- `JAZZ-CTH-001-AC-001` — deterministic matrix подтверждает `0%` только для невозможной атаки, `2%` перед физическим пределом и `100%` в идеальном разрешённом сценарии.
- `JAZZ-CTH-001-AC-002` — при перекрёстных Dexterity/Marksmanship нулевой aim сильнее реагирует на Dexterity, полный aim — на Marksmanship, а последовательность aim-кликов монотонна.
- `JAZZ-CTH-001-AC-003` — поиск runtime-вызовов подтверждает отсутствие `Handling` в CTH и отсутствие прямой подстановки Strength вместо Dexterity для MachineGun.
- `JAZZ-CTH-001-AC-004` — range matrix непрерывна на `E`, оптика сдвигает `E`, ближний штраф сильной оптики работает, а `WeaponRange` остаётся неизменным.
- `JAZZ-CTH-001-AC-005` — одинаковое укрытие даёт одинаковый factor при разных core CTH; штраф снижает предварительно capped `100%`.
- `JAZZ-CTH-001-AC-006` — bullet sequence монотонна, Strength/стойка/сошки улучшают retention, специальные action windows явны и ни один recoil effect не применяется дважды.
- `JAZZ-CTH-001-AC-007` — AI aim и multishot prediction совпадают с core и bullet sequence для одинакового контекста.
- `JAZZ-CTH-001-AC-008` — без debug breakdown показывает силу каждого эффекта разным числом `+`/`−`; debug показывает точные проценты и CTH каждой пули.
- `JAZZ-CTH-001-AC-009` — совместимое оружие без перка, с перком и несовместимое оружие дают ожидаемые наборы действий без двойного perk factor.
- `JAZZ-CTH-001-AC-010` — сравнительная матрица классов и тиров сохраняет роли, а СВД при полном aim превосходит АК-47 на подготовленной средней и дальней дистанции.
- `JAZZ-CTH-001-AC-011` — все активные weapon/component представления синхронны между `items.lua`, `metadata.lua`, companions и каноническими CSV; исключённые и удалённые классы отсутствуют.
- `JAZZ-CTH-001-AC-012` — scoped `git diff --check`, Lua/static contract tests, documentation check и generated audit проходят либо baseline findings перечислены отдельно.
- `JAZZ-CTH-001-AC-013` — Mod Editor load/save/reload подтверждает generated round-trip без ignored mod, load/runtime error и assert.
- `JAZZ-CTH-001-AC-014` — runtime-плейтест подтверждает одиночный огонь, очереди, дробовик, overwatch, PinDown, мобильные действия, укрытие, подавление, оптику и перки.
- `JAZZ-CTH-001-AC-015` — сетевой/replay сценарий с одинаковым save/seed подтверждает одинаковые final CTH, bullet CTH, rolls и результаты.
- `JAZZ-CTH-001-AC-016` — независимое conformance review не находит расхождения реализации с требованиями и declared write set.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ сохраняет override `Unit:CalcChanceToHit`, firearm attack results, crosshair и AI prediction. Свежий CommonLib `main` не заменяет эти функции напрямую, но его AI/UI fixes остаются upstream-слоем для трёхстороннего сравнения.
- Saves: persistent schema не меняется; старые game-time threads могут завершать ранее сохранённый bytecode до clean restart.
- Network/determinism: RNG stream не расширяется; core и factors вычисляются до существующего roll в стабильном порядке.
- Generated data: миграция weapon/component presets требует единой транзакции `items.lua` + `metadata.lua` + companions и полного Mod Editor round-trip.
- Cross-package references: новых public IDs и ссылок в `jazz_assets`, `jazz-maps` или `jazz-units` не создаётся.
- Rollback/recovery: runtime core, generated migration и technical delta откатываются единым change set; CSV сохраняет исходный snapshot/provenance.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: Codex в worktree `codex/shooting-documentation`.
- Reviewer: project-owner.
- Declared write set: поля `write_set` front matter.
- Exclusive resources: `items.lua`, `metadata.lua`, Mod Editor state для weapon/component/CTH presets.
- Последовательность: pure core и static matrix → integration с Unit/Firearm → UI/AI parity → controlled generated migration → editor/runtime evidence.
- Состояние `JAZZ-COMBAT-001`: код уже находится в `main`; его historical write set не изменяется, а незакрытые runtime проверки остаются отдельными.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner.
- Дата: 26 июля 2026 года.
- Основание: владелец утвердил модель точности, множителей, отдачи, оптики, ролей классов и перков и поручил начать реализацию в отдельной ветке.

## Evidence

- `JAZZ-CTH-001-AC-001`: `PASS` - `scripts/test-shooting-model.ps1` covers impossible, floor, and ideal 100% scenarios.
- `JAZZ-CTH-001-AC-002`: `PASS` - the static matrix covers Dexterity/Marksmanship crossover and monotonic aim.
- `JAZZ-CTH-001-AC-003`: `PASS` - source inspection and Lua parsing confirm that Handling is not a CTH input and Strength is confined to recoil control.
- `JAZZ-CTH-001-AC-004`: `PASS` - range/optic matrix covers effective-zone shift, near penalty, and unchanged physical range.
- `JAZZ-CTH-001-AC-005`: `PASS` - factor matrix confirms proportional penalties after the capped core.
- `JAZZ-CTH-001-AC-006`: `PASS` - bullet matrix and executor inspection confirm monotonic retention and a single recoil application.
- `JAZZ-CTH-001-AC-007`: `PARTIAL` - AI, UI, and executor call the shared core and bullet-sequence helpers; in-game parity remains to be measured.
- `JAZZ-CTH-001-AC-008`: `PARTIAL` - source inspection confirms variable +/- bands in normal mode and exact percentages in debug; visual runtime inspection remains.
- `JAZZ-CTH-001-AC-009`: `PARTIAL` - existing action/perk availability layers are preserved and documented; the runtime action/perk matrix remains.
- `JAZZ-CTH-001-AC-010`: `PASS` - the matrix covers 157 active weapons and all 11 families; aimed SVD exceeds AK-47 at prepared medium/long range.
- `JAZZ-CTH-001-AC-011`: `PARTIAL` - generated-data audit reports zero jazz errors/warnings and the wiki validates 160 canonical rows; Mod Editor round-trip remains.
- `JAZZ-CTH-001-AC-012`: `PASS` - Lua parse, static matrix, wiki check, documentation audit, project audit, localization audit, and scoped diff checks pass; strict suite audit exposes only 14 pre-existing jazz_assets warnings.
- `JAZZ-CTH-001-AC-013`: `BLOCKED` - Mod Editor load/save/reload requires the interactive game editor.
- `JAZZ-CTH-001-AC-014`: `BLOCKED` - the required in-game playtest has not yet been run.
- `JAZZ-CTH-001-AC-015`: `BLOCKED` - the network/replay determinism scenario has not yet been run.
- `JAZZ-CTH-001-AC-016`: `PARTIAL` - self-review, source-contract inspection, static tests, and Lua parsing are complete; independent review remains.

## Documentation delta

- `docs/technical/` describes the implemented runtime, integration, compatibility, tests, and remaining calibration parameters.
- `docs/wiki/` is restored as the player-facing source: shooting rules, eleven class roles, actions/perks, and generated weapon-family pages.
- Canonical weapon/component CSV files remain the machine-readable source for the wiki generator; generated pages are never edited by hand.
- Disabled or removed content (`AR15`, `M4Commando`, base `MP5`, `CompactSMG`, and the legacy bolt action) is excluded from player documentation.
- ADR-0002 records the technical/player documentation split and the validation contract.
