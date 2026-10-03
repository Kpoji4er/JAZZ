---
id: JAZZ-CONRAD-001
status: approved
owner: project-owner
systems:
  - merc-appearance
repositories:
  - jazz
  - jazz_assets
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-CONRAD-001.md
  - jazz/docs/tools/*conrad*
  - jazz/docs/tools/README.md
  - jazz/docs/technical/systems/units-progression-specializations.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/wiki/merc-recruiting-center.md
  - jazz/docs/showcase/ru/mercenaries.md
  - jazz/docs/showcase/en/mercenaries.md
  - jazz_assets/Sources/Character/JAZZ_Conrad/
  - jazz_assets/Entities/*JAZZ_Conrad*
  - jazz_assets/Entities/Materials/*JAZZ_Conrad*
  - jazz_assets/Entities/Meshes/*JAZZ_Conrad*
  - jazz_assets/Entities/Textures/*JAZZ_Conrad*
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz-units/items.lua
exclusive_resources:
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz-units/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-CONRAD-001: Meshy Conrad in JA3

## Проблема
Одобренный визуально low-poly Conrad (20 809 triangles) не имеет skin и игровых entities.

## Цели
Подключить эту модель к существующему AppearancePreset Conrad и Jazz_Conrad.

## Non-goals
Другие мерки, баланс, новая генерация Meshy, публикация и релиз.

## Требования
- JAZZ-CONRAD-001-REQ-001: подготовить модель на официальном Male/Bip001, экспортировать Body, Pants и Head с волосами через официальный экспортёр/AP.
- JAZZ-CONRAD-001-REQ-002: зарегистрировать JAZZ_ConradBody, JAZZ_ConradPants, JAZZ_ConradHead в assets и подключить существующий Conrad в units; сохранить портреты, ID и характеристики.
- JAZZ-CONRAD-001-REQ-003: сохранить source и отчёты, выполнить structural/pose и доступные игровые проверки.

## Инварианты и ограничения
Не изменять официальный skeleton и игровые сэмплы; максимум четыре нормированных влияния, без custom normals. Исходный GLB неизменен. Разделение головы сохраняет штатную замену головы противогазом.

## Acceptance criteria
- JAZZ-CONRAD-001-AC-001: static — экспортированные entities имеют Male inheritance, skin, валидные ссылки и нормали.
- JAZZ-CONRAD-001-AC-002: static — Conrad ссылается на новые части; metadata/items/EntityData согласованы.
- JAZZ-CONRAD-001-AC-003: offline — rest и согнутые конечности без взрывов геометрии; texture/UV сохранены.
- JAZZ-CONRAD-001-AC-004: runtime/editor — модель видна на Conrad, материалы и штатные анимации проверены; при недоступности явно BLOCKED.

## Impact и совместимость
- Vanilla/CommonLib/JAZZ: штатный AppearancePreset и Male animation inheritance; без нового хука.
- Saves: ID не меняется; для обновления уже созданного внешнего вида может потребоваться reload.
- Network/determinism: без изменений.
- Generated data: assets Entity registration и units appearance item одной транзакцией; appearance не имеет отдельного companion в этом пакете.
- Cross-package references: units -> assets.
- Rollback/recovery: исходный Conrad item сохраняется в source backup; новые entities имеют отдельные имена.

## План и ownership
- Пакет-владелец: assets — бинарные модели, units — appearance, jazz — spec/tools/docs.
- Исполнитель: текущий Codex.
- Reviewer: project-owner.
- Declared write set: frontmatter.
- Exclusive resources: frontmatter; проверить отсутствие открытой игры перед ручной транзакцией.

## Решение владельца
- Статус: approved.
- Кто подтвердил: владелец в текущем чате — «давай его в игру вставим».
- Дата: 2026-10-02.

## Evidence
- JAZZ-CONRAD-001-AC-001: PASS — static/offline. Official AP: three entities, Male inheritance, 86 exported skeleton entries (85 bones + root), no OptimizeElementNormals errors. Compiled geometry/winding matches source: maximum displacement 0.0268 mm. Evidence: jazz_assets/Sources/Character/JAZZ_Conrad/{Body,Pants,Head}-audit.json.
- JAZZ-CONRAD-001-AC-002: PASS — static. 18 resources installed with hashes; ModItemEntity class_parent, metadata.entities/code and EntityData agree. Existing Conrad appearance updated, UnitData unchanged. Quick structural validator PASS; generated-sync units 0 errors/0 warnings, assets 0 errors/13 pre-existing warnings (baseline 14).
- JAZZ-CONRAD-001-AC-003: PASS — offline rest/front/back/three-quarter and bent forearms reviewed. 20 809 triangles, zero unweighted vertices, maximum four influences, no custom normals or geometry issues. Native twist helper bones included in donor-pose inverse skinning. Evidence: jazz_assets/Sources/Character/JAZZ_Conrad/rig-report.json and pose.png. Walking/crouch/prone and weapon grips still require runtime acceptance.
- JAZZ-CONRAD-001-AC-004: BLOCKED — runtime/editor not verified. User explicitly requested to launch the game personally. Steam launch request had already been sent before that instruction arrived; no further game control. Mod Editor save/reload, material cache, gas mask, weapon grip and game animation checks remain with owner.

## Documentation delta
Technical/wiki/showcase/coverage updated with installed-on-disk status, not a runtime PASS. Changes remain uncommitted. Independent owner acceptance remains pending. Done validator correctly fails AC-004 because runtime evidence is missing; lifecycle stays approved until owner game/editor acceptance. Asset-integrity audit: zero errors, 19 unrelated dormant-resource warnings, no Conrad issue.
