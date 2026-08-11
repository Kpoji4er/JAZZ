---
id: JAZZ-APPEAR-001
status: draft
owner: project-owner
systems:
  - visibility-weather-appearance
  - assets-entities
  - armor-damage-wounds-will
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/System_UnitAppearance.lua
  - jazz/Code/** (equipped-armor visuals module if split)
  - jazz/InventoryItem/JazzArmor_*.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/specs/active/JAZZ-APPEAR-001.md
  - jazz/docs/design/equipped-armor-appearance-map.md
  - jazz/docs/technical/systems/visibility-weather-appearance.md
  - jazz/docs/wiki/**
  - jazz/docs/showcase/ru/**
  - jazz/docs/showcase/en/**
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
related_decisions:
  - none
approved_by: pending
---

# JAZZ-APPEAR-001: визуал надетой брони (CommonLib AttachEntries + soft Wardrobe)

## Проблема

`JazzArmor_*` меняет статы, но не внешний вид юнита. Свои меши не планируются: донор ассетов — коллекция **Wardrobe** (Sir Ni) и при необходимости смежные asset-моды. Нужен опциональный слой «надел шлем/жилет → сменилась модель» без обязательной зависимости от чужих пакетов.

## Цели

- Показать надетую броню/шлем на юните через паттерн CommonLib (`AttachEntries` / `BodyPartData` / `OnUpdateItemsVisuals`).
- Soft-deps на Wardrobe-паки (`required = false`); без них и при выключенной опции поведение = текущие AppearancePreset.
- Mod Option вкл/выкл (default **off**).
- Каноническая таблица item → entity (male/female) + mod-id донора; заполняется волнами (сначала Head).

## Non-goals

- Собственные CharacterArmor/CharacterHat meshes в `jazz_assets` (wave 1).
- Обязательная установка Wardrobe для игры в JAZZ.
- Переписывание AppearancePreset мерков/AME под постоянный armor outfit.
- Visual для `JazzArmorPlates_*` (слот плиты).
- Wave 1 не включает полный Torso/Legs map (только контракт + шлемы draft table).

## Требования

- `JAZZ-APPEAR-001-REQ-001` — runtime apply visuals только если **все** верно: Mod Option on; CommonLib loaded (`GetModLoaded` / `IsModLoaded`); выбранный entry имеет `IsValidEntity(Entity)`. Иначе silent no-op (без assert/crash).
- `JAZZ-APPEAR-001-REQ-002` — Mod Option toggle (рабочее имя `ShowEquippedArmorVisuals`), default `false` в `metadata.default_options` + `ModItemOptionToggle` в `items.lua`; RU/EN подписи опции.
- `JAZZ-APPEAR-001-REQ-003` — внешние asset-моды (Wardrobe и т.п.) **не обязательны**: soft-dep только если map реально ссылается на их entity. На 2026-08-11 Head/Torso map = vanilla (+ CommonLib API); Wardrobe soft-dep **не** объявлять.
- `JAZZ-APPEAR-001-REQ-004` — mapping живёт в design-таблице `docs/design/equipped-armor-appearance-map.md` (и/или JSON companion); generated `AttachEntries` на `JazzArmor_*` синхронизируются с таблицей. Первая волна: **Head** (`Slot = "Head"`). Все Head: `Hide` включает `Hair`.
- `JAZZ-APPEAR-001-REQ-005` — при Option on и отсутствии донор-модов: один раз за сессию допустим `ModLog` (не спам); геймплей и статы брони не меняются.
- `JAZZ-APPEAR-001-REQ-006` — использовать CommonLib item appearance API (`AttachEntries`, filters Gender/Slot/Type, `Hide` parts), не reinvent sample `CosmeticArmor`, если CL покрывает кейс.
- `JAZZ-APPEAR-001-REQ-007` — опция / missing mod не ломают save; снятие брони / выкл опции возвращает baseline appearance parts.

## Инварианты и ограничения

- Без Wardrobe / с Option off юнит неотличим от pre-APPEAR-001 по внешности.
- Не требовать Wardrobe в supported install profile (compat docs: optional extras).
- Не менять combat/armor formulas этим спеком.
- Entity ID чужих модов не форкать в `jazz_assets` без отдельного решения.
- Load order: CommonLib до JAZZ (уже soft-dep); Wardrobe до или с JAZZ — visuals просто no-op, если entity ещё нет.
- **Wardrobe Weird Edition** — не в soft-deps: ломает female preview в Anim Metadata Editor (owner 2026-08-11).
- **Wardrobe / Vanilla Expanded / WW2 (Sir Ni):** после inventory — **не нужны** для текущего Head/Torso map (почти всё vanilla). Soft-dep не объявлять, пока не появится конкретный entity. Цель «чужие меши» сужена: CommonLib + vanilla entities + Option.

## Acceptance criteria

- `JAZZ-APPEAR-001-AC-001` — Option off: надетый `JazzArmor_*Head*` не меняет head/hat parts (runtime/human).
- `JAZZ-APPEAR-001-AC-002` — Option on + Wardrobe loaded + mapped helm: appearance обновляется по таблице; unequip восстанавливает baseline (runtime/human).
- `JAZZ-APPEAR-001-AC-003` — Option on + Wardrobe **не** loaded: нет crash; статы брони работают; optional single ModLog (runtime).
- `JAZZ-APPEAR-001-AC-004` — `metadata` soft-deps `required=false` для зафиксированных Wardrobe ids; JAZZ грузится без них (editor/static + human).
- `JAZZ-APPEAR-001-AC-005` — design map покрывает все `JazzArmor_*` с `Slot=Head` (23 ids); unmapped помечены `todo`/`skip` с причиной (static).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: опирается на CL `FixAppearanceItems` (`AttachEntries`, `UpdateItemAppearance`). Конфликт возможен с модами, которые тоже вешают `OnUpdateItemsVisuals` / CosmeticArmor на те же слоты (напр. Misc – Show Equipped Armor) — non-goal полного resolve в wave 1; документировать known conflict.
- Saves: только visuals; save-friendly.
- Network/determinism: visuals client-side appearance; не менять combat RNG.
- Generated data: `AttachEntries` на InventoryItem + options в items/metadata.
- Cross-package: entity из внешних модов; soft-dep только в `jazz`.
- Rollback: Option off или удаление AttachEntries / soft-deps.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent + owner (таблица entity jointly)
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: `items.lua`, `metadata.lua`
- Волны: (1) draft spec + Head table skeleton → (2) inventory Wardrobe entity catalog → (3) fill Head map + wire Option/guards → (4) Torso/Legs

## Решение владельца

- Статус: `draft`
- Кто подтвердил: pending
- Дата: 2026-08-11
- Зафиксировано в обсуждении: Option default off; soft Wardrobe; не обязательно; таблица item↔asset; старт со шлемов.

## Evidence

- `JAZZ-APPEAR-001-AC-001`…`005`: `BLOCKED` — draft; runtime после Wardrobe inventory.

## Documentation delta

- Design map: `docs/design/equipped-armor-appearance-map.md` (создаётся с Head skeleton).
- После implementation: `docs/technical/systems/visibility-weather-appearance.md`; player-facing wiki/showcase — при shipping visuals.
- Tooling: `docs/tools/_list_jazz_helms.py`.
