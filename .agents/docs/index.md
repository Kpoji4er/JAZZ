# Индекс документации AGENTS

Правила Cursor **не always-on**. Таблица «задача → правило/skill» — в корневом `AGENTS.md`. Overlay каждого sibling-пакета (`jazz_assets`, `jazz-units`, `jazz-maps`, `jazz-nomaps`) держать согласованным с этой таблицей. Открывать только совпавшую строку.

- Spec/DoR/DoD: `.agents/skills/specify-jazz-change/SKILL.md`, `docs/specs/README.md`
- Общее: `.agents/docs/reference/project-scope.md`
- Runtime/потоки: `.agents/docs/reference/runtime-model.md`
- Generated data: `.agents/docs/reference/generated-data-sync.md`
- Чеклисты и release: `.agents/docs/reference/checklists-and-release.md`
- Current-state документация: `.agents/docs/reference/documentation-contract.md`
- Agent tooling (сохранять скрипты): `.agents/docs/reference/agent-tooling.md`, `docs/tools/README.md`

## Playbooks по типу задач

- Runtime-тест в живой JA3 (DAP): `.agents/docs/playbooks/dap-runtime-debug.md`
- AI/боевой/CTH: `.agents/docs/playbooks/ai-system.md`
- Оружие и баланс: `.agents/docs/playbooks/weapons-balance.md` (ATTACH tools: `docs/tools/README.md`)
- Карты/квесты: `.agents/docs/playbooks/maps-content.md`
- Юниты/отряды: `.agents/docs/playbooks/units-squads.md`
- Assets/UI: `.agents/docs/playbooks/assets-and-ui.md`
- Новое оружие от исходника до игры: [гайд импорта](playbooks/import-new-weapon.md); [очередь и решения владельца](../../docs/design/weapons-import-plan-jaweapons.md).
- Подготовка BC/NM/RM/AO для JA3, каналы RM, инверсии и проверка в игре: `.agents/docs/playbooks/ja3-texture-preparation.md`.
- Свой JA3 slab (стены/пол/крыша, имена entity, отдельный мод): `docs/design/ja3-how-to-custom-slabs.md` (EN: `docs/design/ja3-how-to-custom-slabs.en.md`). Sample: https://github.com/Kpoji4er/JAZZ-slabs-sample
- Squad role icons: `.agents/skills/create-jazz-squad-icons/SKILL.md`, `docs/technical/systems/squad-role-icons.md`
- Status effect icons: `.agents/skills/create-jazz-status-icons/SKILL.md`, `Icons/StatusEffects/references/PROMPT.md`
- HUD / hotbar action icons (CombatAction, SignatureAbilities, Med): `.agents/skills/create-jazz-action-icons/SKILL.md`, `Icons/Hud/references/PROMPT.md`
- WeaponComponent full Icon: `.agents/skills/create-jazz-component-icons/SKILL.md`, `Icons/Upgrades/Full/references/PROMPT.md`
- WeaponComponent ChipIcon: `.agents/skills/create-jazz-chip-icons/SKILL.md`, `Icons/Upgrades/Chips/references/PROMPT.md`
- Personal named perk icons (68×68 `Perks/Personal/`): `.agents/skills/create-jazz-perk-icons/SKILL.md`, `Perks/references/vanilla/`
- Merc/NPC portraits: `.agents/skills/create-jazz-merc-portraits/SKILL.md`, `.cursor/rules/jazz-merc-portraits.mdc`
- Full merc from design article: `.agents/skills/create-jazz-merc/SKILL.md` + `docs/design/mercs-ja12/` + plan `.agents/skills/create-jazz-merc/references/generation-plan.md`
- Penetration scales (class + tenths, ammo UI): `.agents/skills/jazz-penetration-scales/SKILL.md`
- Lua globals / wrap flags (no «Attempt to create a new global»): `.agents/skills/jazz-lua-globals/SKILL.md`
- Mod Editor / Ged diagnostics (GetError, nested_obj, сектора): `.agents/skills/diagnose-jazz-mod-editor/SKILL.md`
- Lua wrap cycles (один символ — один wrap, не re-base): `.cursor/rules/jazz-lua-wrap-no-cycle.mdc`, `docs/tools/_check_lua_wrap_cycles.py`
- Character element (Hat/Body/Pants/Armor) Blender → AP: `.agents/skills/export-jazz-character-element/SKILL.md`

Для задачи на стыке систем читать только общий контур, точные runtime/generated references и затронутые playbooks. Не загружать весь набор документов.

- Броня/одежда Легиона, developer sample, HGM-референсы и offline QA-pass: `.agents/docs/playbooks/legion-armor-modeling.md`.
- Нормали и сварка полигонов при экспорте (не кастомные, всегда recalc): `.agents/docs/playbooks/mesh-export-normals.md`.
- Приёмка свежих экспортов (что стоит на диске, что смотреть в игре, промпт Астре): `.agents/docs/playbooks/model-export-qa-handoff.md`.

- Release merge with CRLF-only conflicts: `docs/tools/_merge_lf_conflicts.py`; inspect remaining semantic conflicts before committing.

- Сочетания модулей на иконках: `docs/design/weapon-layer-icons/live/LAYERS-REPLAY.md` (native capture, графы совместимости, слои и приёмка UI).


Release ZIP parts: [prepare/test tooling](../../docs/tools/_prepare_release_assets.py), контракт в release-versioning. AK-103 editor transaction: [tool](../../docs/tools/weapon_layer_icons/edit_ak103_magazines.py).

- Installed weapon soft contour and AK-family donor/fit replay: `docs/design/weapon-layer-icons/live/LAYERS-REPLAY.md`; retained editor/capture/merge/verification tools are indexed in `docs/tools/README.md`. Runtime evidence: `docs/design/weapon-layer-icons/live/hybrid-installed/`.

- Meshy: исходные картинки брони, pnpm runner, стоимость, генерация и восстановление задач — `.agents/docs/playbooks/meshy-armor-generation.md`.

- Removable attachment binding recovery: [repair/audit](../../docs/tools/_repair_removable_bindings.py), [offline regression](../../docs/tools/_check_removable_bindings.py); JAZZ-WEAPONS-002 REQ-012/013.
