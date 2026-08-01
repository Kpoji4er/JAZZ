---
id: JAZZ-ASSETS-002
status: implemented
owner: project-owner
systems:
  - assets-entities
  - generated-data-validation
repositories:
  - jazz
  - jazz_assets
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-ASSETS-002.md
  - jazz/docs/technical/systems/assets-entities.md
  - jazz/.agents/skills/sync-jazz-generated-data/scripts/texture-audit-rename.ps1
  - jazz/.agents/skills/rename-jazz-weapon-textures/**
  - jazz/.agents/skills/work-on-jazz-mod/SKILL.md
  - jazz_assets/Entities/Textures/**
  - jazz_assets/Entities/Materials/**/*.mtl
  - jazz_assets/items.lua
  - jazz_assets/docs/texture-rename-*.csv
  - jazz_assets/docs/texture-unused-deleted.txt
exclusive_resources:
  - jazz_assets/Entities/Textures
  - jazz_assets/Entities/Materials
  - jazz_assets/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-ASSETS-002: читаемые DDS + unused purge + dedupe

## Проблема

Почти все weapon DDS в `jazz_assets` имеют цифровые basename (`323300…`, `10101000`). Ориентироваться в `Entities/Textures` нельзя. Часть файлов не ссылается ни из одного `.mtl`; байтовие дубликаты лежат отдельными именами. `BinAssets/*.mtlbin` запекает пути `Mod/pDGDhr/Entities/Textures/<name>.dds`.

## Цели

- удалить DDS, не упомянутые ни в одном `Entities/Materials/*.mtl` (пары Textures + Fallbacks);
- схлопнуть байт-идентичные used-текстуры в один файл с общим `Name=` в материалах;
- переименовать used numeric DDS в `Entity_MapType.dds` (`Base` / `Norm` / `RM` / `AO` / `SPEC` / `SI` / `Color`);
- синхронно обновить `.mtl` и списки `'texture'` в `items.lua`;
- дать skill + скрипт для того же контракта на **новых** стволах после editor import;
- после apply — rebuild `mtlbin` в Mod Editor и runtime smoke.

## Non-goals

- перепаковка meshes / FBX re-export;
- ручной hex-edit `mtlbin`;
- переименование уже human-readable имён без content-dedupe;
- удаление dormant Entity / починка M60/PKM долга из ASSETS-001.

## Требования

- `JAZZ-ASSETS-002-REQ-001` — unused = top-level `Textures/*.dds` basename ∉ любых `.mtl` `Name="….dds"`; удалять пару Fallbacks при наличии.
- `JAZZ-ASSETS-002-REQ-002` — slot→suffix: BaseColorMap→Base, NormalMap→Norm, RMMap→RM, AOMap→AO, SpecialMap→SPEC, SIMap→SI, ColorizationMap→Color; коллизии → `Entity_Base2`….
- `JAZZ-ASSETS-002-REQ-003` — shared basename / content-hash dupe → один канонический файл **только при том же map-suffix** (не склеивать Norm↔Base); owner: body entity предпочтительнее attachment.
- `JAZZ-ASSETS-002-REQ-004` — apply обновляет Textures, Fallbacks, `.mtl`, `items.lua`; не патчит `mtlbin`.
- `JAZZ-ASSETS-002-REQ-005` — skill `rename-jazz-weapon-textures` документирует DryRun→Apply→editor mtlbin для нового оружия (`-EntityFilter`).

## Инварианты и ограничения

- Entity / material / mesh ID не менять.
- Case-sensitive basenames.
- Битые MTL→disk refs чинить до delete (retarget/reuse), не оставлять missing.
- Runtime evidence обязателен после mtlbin rebuild.

## Acceptance criteria

- `JAZZ-ASSETS-002-AC-001` — DryRun пишет rename-map + unused list; Apply оставляет 0 unused top-level Textures по той же формуле (static).
- `JAZZ-ASSETS-002-AC-002` — `check-asset-integrity.ps1` PASS для зарегистрированных Entity; нет MTL refs на отсутствующие DDS.
- `JAZZ-ASSETS-002-AC-003` — после Mod Editor mtlbin rebuild: AA52, M2Carbine, MP7, BerettaM12 без missing texture в логе (runtime).
- `JAZZ-ASSETS-002-AC-004` — skill + `texture-audit-rename.ps1` доступны; `-EntityFilter` документирован.

## Impact и совместимость

- Vanilla/CommonLib: нет.
- Saves: entity ID те же; пути текстур — resource paths внутри assets.
- Network/determinism: нет.
- Generated data: `.mtl`, `items.lua` texture lists, DDS filenames.
- Cross-package: core ссылается на entity names, не на DDS basenames.
- Rollback: git revert `jazz_assets` (+ script/skill в `jazz`).

## План и ownership

- Пакет-владелец: `jazz_assets` (DDS/mtl/items); `jazz` (script/skill/spec/docs).
- Declared write set: см. frontmatter.

## Решение владельца

- Статус: approved (подтверждение плана в чате: 1C+2A+dedupe+skill).
- Кто подтвердил: project-owner
- Дата: 2026-07-31

## Evidence

- `JAZZ-ASSETS-002-AC-001`: `PASS` (static) — post-Apply DryRun: UnusedTex=0, RenameRows=0, Referenced=Textures=1367.
- `JAZZ-ASSETS-002-AC-002`: `PASS` (static) — `check-asset-integrity.ps1` RESULT PASSED (errors=0; pre-existing dormant warnings).
- `JAZZ-ASSETS-002-AC-003`: `PASS` (runtime/human) — 495 stale numeric-path `mtlbin` удалены (осталось 16 named-only); владелец подтвердил (2026-07-31) отсутствие missing texture в игре (smoke AA52/M2Carbine/MP7/BerettaM12); регрессия была бы заметна. Опционально: SaveWholeMod для полной регенерации оставшихся `mtlbin`.
- `JAZZ-ASSETS-002-AC-004`: `PASS` (static) — skill `rename-jazz-weapon-textures` + script `texture-audit-rename.ps1` (`-EntityFilter` documented).

## Documentation delta

- `docs/technical/systems/assets-entities.md` — counts + контракт имён DDS.
- Skill `rename-jazz-weapon-textures`; ссылка из `work-on-jazz-mod`.
