# Тестирование

## Статические проверки

Выполнять отдельно для каждого изменённого репозитория:

```powershell
git status --short
git diff --check
```

Дополнительно проверить:

- каждый путь из `metadata.lua` существует;
- нет неожиданных загружаемых пустых Lua-файлов;
- новые Lua-файлы действительно включены в metadata;
- lifecycle handlers не читают ModItem раньше `ClassesBuilt`/`DataLoaded`/`ModsReloaded`, если данные ещё не готовы;
- порядок `metadata.code` соответствует требуемому registration order `OnMsg`;
- `MsgClear` не применяется к общему engine-message без доказанного владения;
- class/preset/entity/message ID уникальны в области проекта;
- межпакетные `Mod/<id>/...` ссылки имеют владельца и зависимость;
- CSV локализации существует и имеет ожидаемую кодировку;
- нет новых абсолютных путей к локальным исходникам;
- официальный CommonLib `main`/metadata проверен, установленная версия совпадает с последней, матрица CommonLib/JAZZ обновлена.

В окружении аудита не были доступны standalone `lua`, `luac`, `stylua` или `selene`, поэтому синтаксис и runtime необходимо подтверждать самой игрой и Mod Editor.

## Базовый запуск

1. Сверить установленную CommonLib с последней опубликованной версией из официального `main`, затем включить её и все четыре пакета JAZZ. Тест со старой CommonLib не считается поддерживаемым.
2. Проверить отсутствие ошибок загрузки и asserts в runtime log и панели сообщений Mod Editor.
3. Открыть главное меню и список модов.
4. Начать новую игру.
5. Загрузить сохранение предыдущей поддерживаемой версии.
6. Проверить переход со стратегической карты в тактический сектор и обратно.

## Runtime lifecycle и сохранения

- сравнить clean process и `ReloadLua`/mod reload: результат не должен зависеть от старых globals, tables, handlers или threads;
- проверить, что file-scope code только регистрирует определения либо явно обосновывает ранний доступ к данным;
- подтвердить ordering двух и более handlers одного message;
- проверить `GameVar`, `MapVar` и `GlobalVar` на new game, map change, save/load и default старого save;
- загрузить сохранение, созданное до изменения, со спящим game-time thread или активным repeat;
- проверить game-time pause/speed/save semantics и real-time UI thread;
- убедиться, что repeat с нулевым/отрицательным interval не выполняет busy loop;
- проверить отсутствие потери mutable state из временной Lua-таблицы обычного `CObject`.

## Бой

- одиночный выстрел без прицеливания и с максимальным прицеливанием;
- короткая и длинная очередь с разной силой стрелка;
- стрельба на ближней, эффективной и предельной дистанции;
- дробовик с дробью и картечью;
- граната в эпицентре и у границы зоны;
- заклинивание, устранение задержки, износ и ремонт;
- Run and Gun игрока и AI;
- overwatch, interrupt и смена оружия;
- melee training visual после отмены и завершения действия.

## Броня, инвентарь и лечение

- экипировка шлема, лицевого предмета и конфликт закрытого шлема;
- установка и разрушение бронеплиты;
- защита от пули, взрыва и ближнего боя;
- штраф тяжёлой брони бойцу с разной силой;
- перезарядка из ammo slot и отказ при патронах в неподходящем слоте;
- гранаты и ordnance в специализированных слотах;
- противогаз с полным и нулевым состоянием;
- лечение bleeding, wounded, inaccurate и slowed;
- стратегическая операция лечения.

## AI и awareness

Это обязательная зона после обновления CommonLib:

- выбор signature action;
- выбор атакующей цели и targeting options;
- движение indoor/outdoor;
- proximity policy;
- использование гранат и осветительных средств;
- работа пулемётчика с сошками;
- поиск укрытия и обход фланга;
- накопление suspicion;
- обнаружение через дым, ночью и при плохой погоде;
- отсутствие зависания AI-хода.

## UI

Проверить Crosshair и CTH-модификаторы, inventory rollover, перенос между слотами, доступные UI actions, шкалу воли, AIM filters и отсутствие ссылок на отсутствующие иконки. Для динамических contexts проверить, что mutating-методы вызываются на настоящем объекте, а не на `SubContext()`. Закрытие окна должно удалить его именованные real-time threads.

## Карты и стратегия

Проверить основные сектора Эрни, входы и deployment, квестовые маркеры, setpieces, guardpost, патрули, стратегические отряды, squad logo, POI, доход, World Flip, разговоры, banters и лояльность.

## Assets

Проверить оружие в руках и на земле, состояния компонентов, магазины, сошки, прицелы, материалы и отсутствие `missing entity/state/spot` в логе. После re-export/re-import повторить проверку в новом процессе игры, чтобы исключить устаревшую cached Entity.

## GitHub automation

Для workflow сводок изменений выполнить:

```powershell
node --check .github/scripts/discord-player-update.mjs
node --check .github/scripts/discord-player-update.test.mjs
node --test .github/scripts/discord-player-update.test.mjs
```

Отдельно разобрать `.github/workflows/discord-player-updates.yml` YAML-парсером и выполнить `workflow_dispatch` с `dry_run=true`. Тесты должны покрывать полный `before..after`, zero-before, Structured Output JSON, invalid JSON, `should_publish=false`, `[discord]`, `[skip discord]`, автоматический fallback без ключа и при ошибке API, redaction, neutralization Discord mentions, embed limits и `allowed_mentions.parse=[]`.

Реальный Discord webhook не вызывать без тестового канала. Отсутствие ключа или ошибка OpenAI должны автоматически публиковать fallback после prefilter; ошибка Discord после решения публиковать должна завершать workflow ошибкой.

## Критерий завершения

В отчёте всегда разделять: проверено статически, проверено в Mod Editor, проверено в игре, не проверено и почему. Runtime-изменение не считается полностью проверенным по одному статическому анализу.
## Проверка документационного контракта

Перед завершением любой задачи выполнить:

```powershell
.agents/skills/work-on-jazz-mod/scripts/audit-project.ps1
.agents/skills/document-jazz-systems/scripts/check-system-docs.ps1
```

Профильные сценарии перечислены на каждой странице [каталога систем](systems/README.md). Изменение системы должно добавить или уточнить её validation checklist. Статическая проверка не заменяет Mod Editor/game runtime; в отчёте явно разделять оба уровня.
