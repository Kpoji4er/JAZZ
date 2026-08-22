# Индекс документации AGENTS

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
- Свой JA3 slab (стены/пол/крыша, имена entity, отдельный мод): `docs/design/ja3-how-to-custom-slabs.md`
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

Для задачи на стыке систем читать только общий контур, точные runtime/generated references и затронутые playbooks. Не загружать весь набор документов.
