# Оружие и баланс

## Перед правкой

1. `.agents/docs/reference/project-scope.md`
2. `.agents/docs/reference/generated-data-sync.md` (если touch items/metadata)
3. `.agents/docs/reference/runtime-model.md` для hook order и потоков
4. Профильная техническая страница оружия: `docs/technical/weapons/accuracy-model.md`, `docs/technical/systems/weapons-ammo-components.md`

## Практические правила

- Балансные правки фиксировать в `items.lua` и companion-файлах через корректную синхронизацию.
- Для статовых/численных формул проверять deterministic-контуры в репликации.
- Пробитие (класс + десятые, ammo tooltip): `.agents/skills/jazz-penetration-scales/SKILL.md` — не класть float в `T{}`.
- Не выносить «внешнюю» переоценку баланса в чистый refactor без технической заметки.
- Проверить взаимодействие с AI и visibility/CTH, если формулы затрагивают chance/accuracy.
- **ATTACH / components / CSV без JA3_ROOT:** канон скриптов в `docs/tools/README.md` (`_apply_attach_001.py`, `_export_attach_csv.py`, `_audit_attach_*.py`, `_remove_handling_stat.py`, …). Не удалять эти скрипты после прогона; см. `.agents/docs/reference/agent-tooling.md`.
- **Тиры коллиматоров** (Precision / Overwatch / Universal, будущие loot-предметы): `docs/design/reflex-collimator-tiers.md`.
- **Боевые прицелы** (mid universal + mild near): `docs/design/combat-scope-tiers.md`.

## Финальная упаковка

- Обновить technical-описание изменений механики.
- Зафиксировать действующий контракт на профильной technical-странице; для player-facing — wiki + showcase.
- Новые docs/tools-скрипты — строка в `docs/tools/README.md` в том же change set.
