# Карта технической документации

| Тип изменения | Обязательный current-state документ | Условные документы |
| --- | --- | --- |
| Любой loaded Lua или generated definition | Профильная `docs/technical/systems/*.md` | `file-coverage.md` при изменении файла/load-state |
| Новый, удалённый, dormant или впервые загружаемый файл | `file-coverage.md` и системная страница | Системный индекс при смене владельца |
| Пересечение vanilla/CommonLib | `override-matrix.md` и системная страница | `compatibility.md`, если меняется риск или требование |
| Новая upstream-версия CommonLib | Канонический dependency snapshot | `override-matrix.md` и `compatibility.md` только при фактическом delta |
| Видимое игроку правило, формула, action, item или status | Профильная системная страница, связанная `docs/wiki/`-страница и spec | `docs/showcase` RU+EN при затронутом аспекте витрины; `testing.md`, если меняется общий validation profile |
| Dependency, load order, общий ID или архитектура | `architecture.md` или ADR; системная страница | `compatibility.md` |
| Savegame, NetSync или deterministic RNG | `compatibility.md`, system page и spec | `testing.md` |
| AI, awareness или tactical scoring | `ai-awareness.md` и spec | `testing.md` |
| Sector, campaign, map, quest или dialogue | Maps/strategy page и spec | `testing.md` |
| UnitData, squad, voice или progression | Units system page и spec | Cross-package contract |
| Entity, material, audio или FX | Assets/UI-FX system page | `file-coverage.md`, если меняется load-state |
| Технический долг или неактивный код | `technical-debt.md` и system page | Spec только при реализации долга |
| Публичный scope, установка или dependencies | `compatibility.md` и root README | ADR при долгоживущем решении |

`docs/wiki/` восстановлена по ADR-0002. Она является игроковым представлением current-state, а не самостоятельным источником формул или оружейных чисел; generated weapon pages строятся из канонических CSV. Публичная GitHub Wiki — копия `docs/showcase/` (ADR-0003), не канон.

## Порядок проверки

1. Spec описывает намерение и acceptance criteria до реализации.
2. Technical-страница описывает только фактически загруженное состояние.
3. `file-coverage.md` назначает документационного владельца implementation-файлу.
4. Summary/index документы не дублируют изменчивые snapshots.
5. `docs/README.md` ведёт к specs, decisions, technical, wiki и showcase.
