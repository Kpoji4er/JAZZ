# GitHub Wiki showcase

Публичная двуязычная витрина мода. Канон страниц лежит здесь; GitHub Wiki — только опубликованная копия.

## Контракт

- Источник истины витрины: `docs/showcase/ru/` и `docs/showcase/en/`.
- Детальный игроковый справочник в репозитории: [`docs/wiki/`](../wiki/README.md) (ADR-0002).
- Реализация и формулы: [`docs/technical/`](../technical/README.md).
- Витрина не спорит с `docs/wiki/` и technical; числа оружия не копируются вручную из generated pages.
- Каждая страница существует **на обоих языках** с одинаковым `slug` из [`pages.json`](pages.json).

## Публикация

```powershell
# Собрать staging без push
.\scripts\docs\publish-github-wiki.ps1

# Собрать и запушить в Kpoji4er/JAZZ.wiki
.\scripts\docs\publish-github-wiki.ps1 -Publish
```

CI: `.github/workflows/publish-github-wiki.yml` публикует при изменении `docs/showcase/**` на `main`.

### Первый запуск (один раз)

GitHub создаёт `JAZZ.wiki.git` только после первой страницы:

1. Открыть https://github.com/Kpoji4er/JAZZ/wiki
2. Create the first page (имя `Home`, любое содержимое) и сохранить
3. Запустить `.\scripts\docs\publish-github-wiki.ps1 -Publish` или дождаться workflow после merge в `main`

Дальше править только `docs/showcase/`; wiki перезаписывается публикацией.

## Имена страниц на GitHub Wiki

| Источник | Wiki page |
| --- | --- |
| `ru/<slug>.md` | `RU-<wikiBase>` |
| `en/<slug>.md` | `EN-<wikiBase>` |
| (генерируется) | `Home`, `_Sidebar`, `_Footer` |

`Home` — языковой вход. Боковое меню строится из `pages.json`.

## Когда обновлять

Любое заметное игроку изменение поведения, которое уже требует правки `docs/wiki/`, в том же change set обновляет соответствующие страницы showcase на **русском и английском**. После merge в `main` wiki обновляется workflow'ом.
