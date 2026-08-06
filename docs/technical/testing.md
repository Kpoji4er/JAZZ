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

Для deterministic контракта стрельбы выполнить:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/test-shooting-model.ps1
```

Тест читает канонический weapon CSV и проверяет 11 классов, исключённые ID, Dexterity/Marksmanship, monotonic aim, floor/cap, range/optic profile, коммутативность факторов, recoil/action windows и отношение СВД к АК-47. Он не запускает движок.

Standalone `lua`/`luac` не является repository dependency. В evidence конкретного change set можно использовать внешний parser для синтаксической проверки, но загрузку, engine globals, реакции и runtime всё равно необходимо подтверждать самой игрой и Mod Editor.

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
- процент сохраняемого урона на дистанции всегда в диапазоне `0..100`, не создаёт отрицательный урон и учитывает range modifiers атакующего/action;
- трассерный боеприпас добавляет `MarkedTraccers` один раз на произведённый выстрел при CTH больше нуля — и при попадании, и при промахе; при CTH `0`, jam или отсутствии выстрела не добавляет;
- дробовик с дробью и картечью;
- граната в эпицентре и у границы зоны;
- бросок/подствол: вблизи только лёгкий scatter (mishap% ≈ 0), цвет всё равно может теплеть от scatter; на дальней дистанции выше mishap и цвет уходит к красному (`GetMishapAimReliability` → `GetCTHColor`);
- граната при Dex+Expl ≈ 30 ощущается уверенно; пайп/TNT при среднем Expl — заметно рискованнее;
- suppression / Inaccurate увеличивают mishap% и разброс гранаты/GL;
- **контузия/травма:** frag/HE/flashbang blast-hit — всегда `Concussion` (кроме TempHitPoints); `*shot` trauma rollers сквозь непробитую броню / dedicated trauma gate шансовый; smoke/gas/fire без concussion;
- заклинивание, устранение задержки, износ и ремонт;
- Run and Gun игрока и AI;
- overwatch, interrupt и смена оружия;
- melee training visual после отмены и завершения действия.

### Модель стрельбы

- физически возможный выстрел не падает ниже `2`, невозможный получает `0`;
- опытный стрелок достигает `100%` по открытой цели в полный рост, при полном aim и внутри оптимальной зоны; любой применимый штраф должен уводить этот сценарий ниже `100%`;
- каждый дополнительный клик не уменьшает шанс;
- Dexterity сильнее влияет на ноль кликов, Marksmanship — на полный aim;
- все ситуационные факторы перемножаются без промежуточного округления;
- оптика сдвигает эффективную прицельную зону, но не `WeaponRange` и не `BulletDropRange`;
- СВД при полном aim превосходит АК-47 хотя бы на подготовленной средней/дальней части общего диапазона;
- шанс последующих пуль монотонно падает по recoil retention, а отдача учитывается один раз;
- UI, AI, predictor и фактический выстрел возвращают один результат.
- **Grazing (JAZZ-COMBAT-002):** при низком CTH (~20%) miss→graze заметен (~16%), при высоком (~80%+) почти нет (~1%); полное укрытие даёт cover-graze ≈100%; выстрел/нож через дым **без** укрытия не форсирует graze; царапина ≈40% урона без crit/trauma; ~15% шанс лёгкой крови.
- **Core overflow → crit (JAZZ-COMBAT-004):** uncapped shooter core >100 добавляет разницу к crit 1:1; финальный CTH по-прежнему ≤100 и режется укрытием; opportunity/noncrit без изменений.
- **Suppression / LR / Psycho (JAZZ-COMBAT-003):** `suppressionPinned` цель с Hotblood/Shatterhand не отвечает Retaliate; частичное подавление режет CTH в упор; stealth kill / Hidden не даёт float «Lightning Reaction»; Psycho после боя имеет полный Will, за ход теряет ~4 а не 8.

## Броня, инвентарь и лечение

- экипировка шлема, лицевого предмета и конфликт закрытого шлема;
- установка и разрушение бронеплиты;
- защита от пули, взрыва и ближнего боя;
- дробное пробитие: `PenetrationClass + 0.1×PenetrationBonus` в unit DR и корректный ammo rollover (не целое ×100);
- непробитая закрывающая броня блокирует bleeding/body-part/ammo effects, пробитая броня и отсутствие покрытия разрешают их;
- штраф тяжёлой брони бойцу с разной силой;
- перезарядка из ammo slot и отказ при патронах в неподходящем слоте;
- гранаты и ordnance в специализированных слотах;
- drag/drop на иконку мерка в party panel инвентаря (передача, не «use item»): owner PASS 2026-07-30;
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

Проверить Crosshair и CTH-модификаторы:

- без debug итоговый процент скрыт, а сила каждого эффекта выражена разным количеством `+`/`−`;
- с активными modding/debug tools показаны точные проценты и итоговый CTH;
- breakdown, AI и фактическая атака используют одно вычисление.

Также проверить inventory rollover, перенос между слотами, доступные UI actions, шкалу воли, AIM filters и отсутствие ссылок на отсутствующие иконки. Для динамических contexts проверить, что mutating-методы вызываются на настоящем объекте, а не на `SubContext()`. Закрытие окна должно удалить его именованные real-time threads.

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

Отдельно разобрать `.github/workflows/discord-player-updates.yml` YAML-парсером и выполнить `workflow_dispatch` с `dry_run=true`. Тесты должны покрывать полный `before..after`, zero-before, Structured Output JSON, invalid JSON, `should_publish=false`, `[discord]`, `[discord implemented]`, приоритет `[skip discord]`, автоматический fallback без ключа и при ошибке API, redaction, neutralization Discord mentions, embed limits и `allowed_mentions.parse=[]`.

Обязательно проверить четыре документационных сценария: docs-only без маркера пропускается до OpenAI; `[discord]` публикует только обновление документации без вывода о реализации; `[discord implemented]` включает docs diff и explicit implementation flag; смешанный code+docs диапазон использует код как implementation evidence, а обычные docs исключает из diff. Fallback и Discord embed не должны автоматически содержать «в разработке» или секцию «За кулисами».

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
