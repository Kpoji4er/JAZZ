# Generated data и редакторные файлы

## 1) Что считается сгенерированным

`items.lua`, `metadata.lua`, `InventoryItem`, `CharacterEffect`, `UnitData`, Entity-файлы и карты/patch-слайды часто являются результатом редакторного pipeline.

## 2) Запреты

- Не редактировать вручную только один файл из связанных сгенерированных групп.
- Не массово форматировать карты/`mapdata.lua`/`objects.lua`/grids вручную.
- Не удалять «непонятный» companion-файл только из-за отсутствия ссылки.

## 3) Обязательная транзакция

Перед и после изменения ModItem/preset/Entity/`items.lua`/`metadata.lua` запускать read-only аудит:

1) `.agents/skills/sync-jazz-generated-data/SKILL.md`
2) Проверка `items.lua` + `metadata.lua` + companion-файл на целостность
3) Проверка round-trip через Mod Editor (ignored mod, load error, runtime error, assert)

## 4) Для импорта/экспорта Entity

- Экспорт инкрементальный: старые части могут не удалиться автоматически.
- После re-export обязательно сверять cleaned export-state и делать runtime-проверку.

## 5) Ключевая проверка данных

- Любое изменение generated data всегда валидировать вместе с владельцем системы и документировать в technical-странице.
