# Документация JAZZ

Документация разделена по типу истины:

- [`specs/`](specs/README.md) — требования, DoR, DoD и evidence до приёмки изменения;
- [`decisions/`](decisions/README.md) — долгоживущие архитектурные решения;
- [`technical/`](technical/README.md) — фактически загруженное текущее состояние;
- [ownership/](ownership/README.md) — write sets и exclusive resources параллельных агентов;
- [`glossary.md`](glossary.md) — единый словарь терминов.

`docs/wiki/` сейчас отсутствует и не входит в Definition of Done. Не создавать ссылки или обязательные проверки wiki до отдельного ADR о её восстановлении.

## Контракт изменения

1. Утверждённая spec разрешает реализацию и фиксирует acceptance criteria.
2. Реализация не выходит за declared write set без новой ревизии spec.
3. Technical docs обновляются по фактически реализованному состоянию.
4. Evidence сопоставляет каждый `AC-*` с static/editor/runtime/human результатом.
5. Архитектурное решение, которое должно пережить задачу, фиксируется ADR.

`AGENTS.md` и project skills задают маршрутизацию и автоматические проверки этого контракта.
