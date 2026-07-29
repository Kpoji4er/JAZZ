# Документация JAZZ

Документация разделена по типу истины:

- [`specs/`](specs/README.md) — требования, DoR, DoD и evidence до приёмки изменения;
- [`decisions/`](decisions/README.md) — долгоживущие архитектурные решения;
- [`technical/`](technical/README.md) — фактически загруженное текущее состояние для разработчика и агента;
- [`wiki/`](wiki/README.md) — игроковый справочник без внутренних реализационных деталей;
- [`showcase/`](showcase/README.md) — двуязычная витрина для GitHub Wiki (ADR-0003);
- [ownership/](ownership/README.md) — write sets и exclusive resources параллельных агентов;
- [`glossary.md`](glossary.md) — единый словарь терминов.

`docs/wiki/` восстановлена решением [ADR-0002](decisions/ADR-0002-technical-and-player-docs.md). Публичная GitHub Wiki собирается из [`showcase/`](showcase/README.md) ([ADR-0003](decisions/ADR-0003-github-wiki-showcase.md)). Для заметного игроку изменения technical current-state, профильная wiki-страница и при затронутом аспекте — RU/EN showcase обновляются вместе; generated weapon pages изменяются только через канонические CSV и генератор.

## Контракт изменения

1. Утверждённая spec разрешает реализацию и фиксирует acceptance criteria.
2. Реализация не выходит за declared write set без новой ревизии spec.
3. Technical docs обновляются по фактически реализованному состоянию.
4. Evidence сопоставляет каждый `AC-*` с static/editor/runtime/human результатом.
5. Архитектурное решение, которое должно пережить задачу, фиксируется ADR.

`AGENTS.md` и project skills задают маршрутизацию и автоматические проверки этого контракта.
