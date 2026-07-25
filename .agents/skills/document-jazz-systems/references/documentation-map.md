# Карта документации

| Тип изменения | Technical | Wiki |
|---|---|---|
| Любой loaded Lua или generated definition | Профильная `docs/technical/systems/*.md`; `file-coverage.md` | Только если меняется наблюдаемое поведение |
| Новый, удалённый, dormant или впервые загружаемый файл | `file-coverage.md`; системный индекс при смене владельца | Обычно не требуется |
| Пересечение vanilla/CommonLib | `override-matrix.md`; системная страница; `compatibility.md` | Обновить, если пересечение меняет механику или требования |
| Новая upstream-версия CommonLib | Повторный аудит; `override-matrix.md`; `compatibility.md`; snapshot | `getting-started.md` или ограничения, если изменились требования |
| Видимое игроку правило, формула, action, item или status | Профильная системная страница; tests | Профильный гайд механики |
| Dependency, load order, общий ID или архитектура | `architecture.md`; system page; `compatibility.md` | `getting-started.md` при изменении установки |
| Savegame, NetSync или deterministic RNG | `compatibility.md`; `testing.md`; system page | `content-and-limitations.md`, если затронут игрок |
| AI, awareness или tactical scoring | AI system page; `testing.md` | `ai-stealth-weather.md` |
| Sector, campaign, map, quest или dialogue | Maps/strategy pages; `testing.md` | `strategy-and-world.md` и/или `content-and-limitations.md` |
| UnitData, squad, voice или progression | Units system page; cross-package references | `mercenaries-and-progression.md` |
| Entity, material, audio или FX | Assets/UI-FX system page | Профильный гайд, только если результат заметен |
| Технический долг или неактивный код | `technical-debt.md`; system page | Только если это пользовательское ограничение |
| Публичный scope, установка или dependencies | `compatibility.md`; root README | `getting-started.md`; `content-and-limitations.md` |

## Порядок проверки

1. Technical-страница содержит точное поведение и происхождение.
2. `file-coverage.md` назначает владельца каждому implementation-файлу.
3. Wiki объясняет подтверждённое поведение без implementation dump.
4. `docs/README.md` ведёт к обеим аудиториям.
5. Корневой README остаётся публичным описанием мода.