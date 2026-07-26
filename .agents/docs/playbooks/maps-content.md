# Карты, квесты и диалоги

## Перед правкой

1. `.agents/docs/reference/project-scope.md`
2. Важно: не трогать `Maps/` полностью без конкретного адреса.
3. Для data-ссылок — `.agents/docs/reference/generated-data-sync.md`.

## Жёсткие ограничения

- Не делать recursive scan `jazz-maps/Maps/` без явного указания карты/сектора/patch.
- Контентовые правки в `jazz-maps` не трогаем в связке с `jazz-units` без проверки зависимостей `Mod/<id>/...`.
- Любой map patch проверять через Map Editor, не массовым grep-реформатом.

## Что обязателено после изменений

- Проверить links на `UnitData`, assets, quest objectives.
- Обновить технический контракт: `docs/technical/systems/maps-quests-*` или соответствующий профильный документ.
- Отметить в доке, что изменился контентовый scope и его влияние на совместимость.
