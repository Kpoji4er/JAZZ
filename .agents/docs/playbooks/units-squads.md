# Юниты, отряды и прогрессия

## Перед правкой

1. `.agents/docs/reference/project-scope.md`
2. `.agents/docs/reference/generated-data-sync.md` (если меняются UnitData/профили/составы)
3. `.agents/docs/reference/runtime-model.md`

## Обязательные проверки

- Проверить корректность ссылок между `jazz-units` и `jazz-maps` (squad/quest/sector IDs).
- Проверить порядок инициализации после `DataLoaded`/`ModsReloaded`.
- Учитывать determinism для hiring/randomization/персетов.
- Не переименовывать unit/ID/class без проверки usage по всем 4 репозиториям.

## После правки

- Обновить соответствующую technical-страницу (`docs/technical/systems/units-progression-specializations.md` и др.).
- Указать влияние на игрока в технической заметке для временной замены wiki.
