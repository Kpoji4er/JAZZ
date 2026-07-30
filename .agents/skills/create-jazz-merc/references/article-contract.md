# Article contract — mercs-ja12

Статья в `docs/design/mercs-ja12/<slug>.md` — единственный вход `$create-jazz-merc`.

## Frontmatter (обязательные ключи)

`status`, `priority`, `origin`, `unit_id`, `portrait_id`, `affiliation`, `role`, `tier`, `specialization`, `gender`, `nationality`, `voice_source`, `starting_level`, `will`, `salary` (starting/increase/lv1/max), `medical_deposit`, `haggling`, `executable`.

`medical_deposit` — только vanilla enum: `none` | `small` | `large` | `extreme` (default движка = `small`; **не** писать `standard` — `CalculateMedical` вернёт nil и AIM hire упадёт).
`haggling` — `normal` | `low` | `high`.

`executable: true` только если нет Open blockers и заполнены все обязательные секции.

## Обязательные секции

1. Identity (RU+EN)
2. Bio (RU+EN)
3. Stats (все 10 + MaxHitPoints + StartingLevel)
4. Perks (StartingPerks + named perk mechanics)
5. Personality
6. Hire
7. Inventory (loot id + tier contents)
8. Portrait prompt (`CHARACTER_DESCRIPTION`, no-weapons, class kit, refs, **JA2 face match** if ``*.ja2-face.*`` present)
9. Phrases — AIM chat (см. `_phrase-checklist.md`)
10. Phrases — VoiceResponse (минимум)
11. Wiring
12. Open blockers

## Portrait rules

- Нет оружия в руках/на плече; holstered pistol — крайний случай.
- Классовые принадлежности обязательны (медкит/шеврон, инструменты, demo bag, …).
