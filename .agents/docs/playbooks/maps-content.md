# Карты, квесты и диалоги

## Перед правкой

1. `.agents/docs/reference/project-scope.md`
2. Важно: не трогать `Maps/` полностью без конкретного адреса.
3. Для data-ссылок — `.agents/docs/reference/generated-data-sync.md`.

## Жёсткие ограничения

- Не делать recursive scan `jazz-maps/Maps/` без явного указания карты/сектора/patch.
- Контентовые правки в `jazz-maps` не трогаем в связке с `jazz-units` без проверки зависимостей `Mod/<id>/...`.
- Любой map patch проверять через Map Editor, не массовым grep-реформатом.

## География / атлас секторов

- Канон атласа и трансфера: `jazz-maps/docs/content/sector-atlas.md`, `sector-transfer.md`, сверка `sector-sheet-vs-runtime.md`.
- Regen из `items.lua` (не из `Maps/`): `docs/tools/export-jazz-maps-sectors.py` + `docs/tools/build-sector-atlas-docs.py`.
- Player: `docs/wiki/grand-chien-map.md` + showcase `grand-chien-map` (RU/EN).
- Сателлит: `jazz-maps/Images/GrandChien2.png` (`sector_bottomright = P32`, старт `M1`).

## Что обязателено после изменений

- Проверить links на `UnitData`, assets, quest objectives.
- Обновить технический контракт: `docs/technical/systems/maps-quests-*` или соответствующий профильный документ.
- При смене сетки/трансфера секторов — пересобрать atlas docs и при player-facing эффекте wiki/showcase.
- Отметить в доке, что изменился контентовый scope и его влияние на совместимость.
