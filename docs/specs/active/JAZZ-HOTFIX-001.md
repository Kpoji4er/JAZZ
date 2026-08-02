---
id: JAZZ-HOTFIX-001
status: implemented
owner: project-owner
systems:
  - runtime-editor-integration
  - combat-cth-actions
  - ui-audio-fx
  - strategy-squads-sectors
  - assets-entities
  - weapons-ammo-components
repositories:
  - jazz
  - jazz_assets
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/CrossHairUI.lua
  - Code/Guardpost_Patrols.lua
  - Code/SatelliteSquad.lua
  - InventoryItem/MAS36.lua
  - items.lua
  - metadata.lua
  - ParticleTextures/Explosion_emissive.dds
  - ParticleTextures/Fallbacks/Explosion_emissive.dds
  - docs/specs/active/JAZZ-HOTFIX-001.md
  - docs/tools/_fix_metadata_last_changes_and_audit_code.py
  - docs/tools/README.md
  - docs/technical/compatibility.md
  - docs/technical/override-matrix.md
  - docs/technical/systems/assets-entities.md
  - docs/technical/systems/combat-cth-actions.md
  - docs/technical/systems/runtime-editor-integration.md
  - docs/technical/systems/strategy-squads-sectors.md
  - docs/technical/systems/ui-audio-fx.md
  - docs/technical/weapons/combat-actions.md
  - docs/technical/weapons/data/weapons.csv
  - ../jazz_assets/Entities/Materials/cartridge_box_cartridge_box.mtl
  - ../jazz_assets/Entities/Materials/tyulpan_tyulpan.mtl
  - ../jazz_assets/Entities/Textures/10470000.dds
  - ../jazz_assets/Entities/Textures/10470002.dds
  - ../jazz_assets/Entities/Textures/6224005.dds
  - ../jazz_assets/Entities/Textures/6302004.dds
  - ../jazz_assets/Entities/Textures/9359000.dds
  - ../jazz_assets/Entities/Textures/9359001.dds
  - ../jazz_assets/Entities/Textures/9359002.dds
  - ../jazz_assets/Entities/Textures/9359003.dds
  - ../jazz_assets/Entities/Textures/Fallbacks/10470000.dds
  - ../jazz_assets/Entities/Textures/Fallbacks/10470002.dds
  - ../jazz_assets/Entities/Textures/Fallbacks/6224005.dds
  - ../jazz_assets/Entities/Textures/Fallbacks/6302004.dds
  - ../jazz_assets/Entities/Textures/Fallbacks/9359000.dds
  - ../jazz_assets/Entities/Textures/Fallbacks/9359001.dds
  - ../jazz_assets/Entities/Textures/Fallbacks/9359002.dds
  - ../jazz_assets/Entities/Textures/Fallbacks/9359003.dds
exclusive_resources:
  - items.lua
  - metadata.lua
  - InventoryItem/MAS36.lua
  - ModItemCombatAction/AttackShotgun
  - ModItemInventoryItemCompositeDef/MAS36
  - ModItemParticleSystemPreset/ParticlesThompson
  - ModItemXTemplate/ActionCameraCrosshair
  - ModItemXTemplate/RolloverInventoryWeaponBase
  - ModItemXTemplate/SatelliteViewMapContextMenu
  - jazz_assets/Entities/Materials/cartridge_box_cartridge_box.mtl
  - jazz_assets/Entities/Materials/tyulpan_tyulpan.mtl
  - jazz_assets/Entities/Textures/10470000.dds
  - jazz_assets/Entities/Textures/10470002.dds
  - jazz_assets/Entities/Textures/6224005.dds
  - jazz_assets/Entities/Textures/6302004.dds
  - jazz_assets/Entities/Textures/9359000.dds
  - jazz_assets/Entities/Textures/9359001.dds
  - jazz_assets/Entities/Textures/9359002.dds
  - jazz_assets/Entities/Textures/9359003.dds
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-HOTFIX-001: устранение runtime, UI и render assert-ошибок

## Проблема

При холодной загрузке JAZZ и в игровых UI-сценариях воспроизводятся независимые assert-ошибки: повторная регистрация vanilla `MapVar("gameOverState")`, чтение ещё не объявленных strict globals в Legion AI, повторный `Open` crosshair-окна, индексирование числовых aim-параметров конусом, индексирование отсутствующего региона в satellite context menu и несовместимые либо отсутствующие asset resources. В журнале рендера повреждённый материал патронной коробки непосредственно предшествует assert в `reRenderQueue.cpp`, а `ParticlesThompson` ссылается на ресурс другого мода.

Отдельно: `InventoryItem/MAS36.lua - File Not Found`. Два слоя:

1. **Parse-blocker `metadata.lua`:** в `last_changes` после первого буллета (`WEAPONS-006…recoil`) стоял raw newline вместо `\n`. Lua: `unfinished string` → `Failed to load mod metadata from AppData/Mods/jazz` → игра грузит **Steam packed** `e6L4ECj`, а не working tree. Локальный companion при этом не участвует.
2. **Id-case companion:** ModItem Id / `GetCodeFileName()` требуют `InventoryItem/MAS36.lua`. Metadata-only retarget на `Mas36.lua` — ошибочный подход (расходится с editor path); companion нужно переименовать в точный Id-case, а `metadata.code` держать как `InventoryItem/MAS36.lua`.

## Цели

- Устранить показанные пользователем Lua/XWindow asserts при загрузке, выборе атаки и открытии satellite context menu.
- Восстановить самодостаточный resource contract JAZZ/JAZZ Assets для подтверждённых отсутствующих textures и Thompson particle.
- Сделать `metadata.lua` снова парсируемым (валидный `last_changes`), чтобы local AppData `jazz` не падал на Steam packed.
- Companion + `metadata.code` для Id `MAS36` — буквально `InventoryItem/MAS36.lua` (не metadata-only retarget на `Mas36.lua`).
- Устранить подтверждённую несовместимую комбинацию opaque/blending properties материала патронной коробки.
- Сохранить публичные IDs, текущие формулы боя, save/network contract и владельцев данных.

## Non-goals

- Добавление новых регионов, секторов, карт, юнитов или игровых правил.
- Перебалансировка дробовиков или изменение их локализованного описания.
- Массовая регенерация `items.lua`, `metadata.lua`, entities или материалов.
- Восстановление не найденных исходных RM-карт `5281002` и `5281006`; ссылки на отсутствующие optional resources удаляются.
- Исправление неподтверждённого asset debt вне точного списка resources.

## Требования

- `JAZZ-HOTFIX-001-REQ-001` — `Code/SatelliteSquad.lua` не должен повторно регистрировать vanilla `gameOverState`, а `Guardpost_Patrols.lua` не должен читать отсутствующий global через strict-global lookup.
- `JAZZ-HOTFIX-001-REQ-002` — crosshair XTemplate не должен вручную открывать уже открываемый framework-окном `idContainer`; динамический zoom label должен передаваться в перевод как `Untranslated`.
- `JAZZ-HOTFIX-001-REQ-003` — мета-действие `AttackShotgun` должно использовать line targeting, соответствующий фактическим firing members, и не передавать число в cone-targeting код как таблицу.
- `JAZZ-HOTFIX-001-REQ-004` — satellite context menu должен корректно отображаться для секторов без Region preset и не обращаться к `nil`.
- `JAZZ-HOTFIX-001-REQ-005` — weapon rollover не должен предполагать наличие необъявленного `idIcon`.
- `JAZZ-HOTFIX-001-REQ-006` — `ParticlesThompson` должен ссылаться на ресурс собственного пакета JAZZ, существующий в основном и fallback слоях.
- `JAZZ-HOTFIX-001-REQ-007` — подтверждённые texture IDs должны существовать в `jazz_assets`, отсутствующие Tyulpan RM-ссылки не должны оставаться активными, а opaque cartridge-box material не должен включать translucency/distortion/depth-softness.
- `JAZZ-HOTFIX-001-REQ-008` — `metadata.lua` парсится без unfinished string; `metadata.code` и disk/git companion для Id `MAS36` — `InventoryItem/MAS36.lua` (как `GetCodeFileName()`); публичный ID / содержимое `items.lua` не меняются. Metadata-only путь `Mas36.lua` не использовать.

## Инварианты и ограничения

- Сохраняются class names, ModItem IDs, localization IDs, dependency metadata и порядок `metadata.code`.
- `metadata.lua` входит в exclusive transaction для проверки, но не изменяется без обнаруженного contract delta.
- Правка generated data выполняется точечно на свежем состоянии с последующим строгим аудитом; открытый устаревший Mod Editor не должен сохранять мод поверх неё.
- Бинарные ресурсы копируются без перекодирования из установленного официального sample либо из локального source-пакета того же asset-набора.
- Никакие файлы `jazz-maps/Maps/` не обходятся и не изменяются.
- Посторонние незакоммиченные изменения во всех четырёх репозиториях сохраняются.

## Acceptance criteria

- `JAZZ-HOTFIX-001-AC-001` — при холодной загрузке отсутствуют asserts о повторном `gameOverState` и undefined `g_JAZZ_BaseGetSatelliteIconImages*`.
- `JAZZ-HOTFIX-001-AC-002` — открытие crosshair и выбор shotgun attack не вызывают `self.window_state == "new"` и `attempt to index a number value (aoe_params)`.
- `JAZZ-HOTFIX-001-AC-003` — context menu сектора без Region preset открывается без ошибки и скрывает region-блок.
- `JAZZ-HOTFIX-001-AC-004` — статический asset-аудит не находит заявленных missing DDS/particle paths и несовместимых cartridge-box material flags.
- `JAZZ-HOTFIX-001-AC-005` — generated-data sync проходит по комплекту из четырёх пакетов без нового `FAIL`.
- `JAZZ-HOTFIX-001-AC-006` — системная документация и override matrix описывают фактический post-fix contract.
- `JAZZ-HOTFIX-001-AC-007` — metadata/items/companion для `MAS36` согласованы, active path существует с точным регистром, а холодная загрузка не выдаёт `InventoryItem/MAS36.lua - File Not Found`.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: удаляется только дублирующая JAZZ-регистрация vanilla `MapVar`; CommonLib snapshot `main` подтверждён на commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c`, версия 1.11. Публичные функции и IDs сохраняются.
- Saves: новое persistent state не добавляется, существующее значение `gameOverState` остаётся vanilla MapVar.
- Network/determinism: NetSync events, RNG, формулы и порядок действий не изменяются.
- Generated data: точечно меняются properties/handlers пяти существующих ModItems. Для `MAS36`: rename companion `Mas36.lua`→`MAS36.lua` + `metadata.code` → `InventoryItem/MAS36.lua`; плюс fix raw newline в `last_changes` (иначе local metadata не грузится). Порядок списка, содержимое companion/`items.lua` и IDs прежние.
- Cross-package references: texture/material resources принадлежат `jazz_assets`; particle preset и его texture принадлежат `jazz`.
- Rollback/recovery: текстовые изменения откатываются по точному diff, добавленные binaries удаляются только вместе с возвратом ссылок; Mod Editor перед последующим save обязан reload мод с диска.

## План и ownership

- Пакет-владелец: runtime/generated UI — `jazz`; materials/textures — `jazz_assets`.
- Исполнитель: Codex.
- Reviewer: project-owner/runtime tester.
- Declared write set: перечислен во front matter; другие файлы не меняются.
- Exclusive resources: `items.lua`, проверяемый `metadata.lua`, точные ModItems и asset paths из front matter.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner, команда «чини» после предъявления конкретных стеков и предложенного hotfix scope.
- Дата: 2026-07-26.

- Дополнение 2026-07-27: project-owner предъявил load error MAS36 и поручил закоммитить все незакоммиченные изменения перед merge в `main`; ранний scope «metadata → Mas36.lua» **superseded**.
- Дополнение 2026-08-03: owner — MAS36 File Not Found всё ещё в логе; root cause = broken `last_changes` (local metadata не грузится → Steam packed) + companion/code path must be Id-case `InventoryItem/MAS36.lua`.

## Evidence

- `JAZZ-HOTFIX-001-AC-001`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-HOTFIX-001-AC-002`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-HOTFIX-001-AC-003`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`
- `JAZZ-HOTFIX-001-AC-004`: `PASS (static)  - post-implementation audit; owner accepted 2026-07-28`
- `JAZZ-HOTFIX-001-AC-005`: `PASS (static)  - post-implementation audit; owner accepted 2026-07-28`
- `JAZZ-HOTFIX-001-AC-006`: `PASS (static)  - post-implementation audit; owner accepted 2026-07-28`

- `JAZZ-HOTFIX-001-AC-007`: `PASS (static)` — 2026-08-03: `last_changes` raw newline → `\n` (metadata снова один валидный string); `metadata.code` = `"InventoryItem/MAS36.lua"`; git index + disk `InventoryItem/MAS36.lua`; audit `code` 1045/1045 OK, missing=0, case_mismatch=0; `_validate_items_quick.py` OK. Prior evidence «path = Mas36.lua» / metadata-only retarget — **superseded**. `BLOCKED (runtime/human)` — cold-load re-check: лог не должен показывать `Failed to load mod metadata from AppData/Mods/jazz` и не должен грузить jazz только как `packed from steam` с `InventoryItem/MAS36.lua - File Not Found`.

## Documentation delta

- После реализации обновляются профильные страницы runtime/editor, combat, UI/FX, strategy, assets, точное описание `AttackShotgun` и override matrix.
- Игроковая wiki не меняется: hotfix восстанавливает заявленное текущее поведение, не вводя нового правила, числа или публичного ID.
- Для MAS36: `docs/technical/weapons/data/weapons.csv` companion = `InventoryItem/MAS36.lua`; контракт пути — эта spec + audit tool `docs/tools/_fix_metadata_last_changes_and_audit_code.py`.
