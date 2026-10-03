# АЕК-971 / АЕК-973С — установленный кандидат

По запросу «вставь пока в игру аек» установлен один предмет `AEK971`.
Комплект `JAZZ_AEK_545` / `JAZZ_AEK_762` в слоте Barrel переключает модель,
имя, калибр и штатные числовые модификаторы. Стандартный магазин на 30,
складной приклад; непроверенный внешний обвес не включён.

Баланс: Т3-2; исходные Damage 26/30, Range 50/42, Recoil 13/17,
AimAccuracy 12/11, RPM 900. Bobby: in, engine Tier 4, RW 25,
MaxStock 1, Cost 22000. Фракционные loadouts не менялись.

## Доказательства

- Восемь entity HGM: compiled/source triangle counts совпали, winding PASS,
  максимальное отклонение вершин менее 0,03 мм.
- Авторские BC/NM, RM=(rough,rough,metal), без художественной коррекции.
- Отдельные CPU Cycles PBR-превью и четыре иконки; overlay с АК-74М:
  971 — 0,9626 м, 973С — 0,9600 м, референс — 0,9418 м.
- Offline Lua использует настоящий JAZZ setter и native ChangeCaliber:
  повторные переходы без накопления дельт, сохранение Condition/id,
  возврат патронов, запрет ownerless-конверсии заряженного оружия,
  изоляция clone, выбор деталей и иконки PASS.
- Items/metadata/companion, ModItemCode и восемь entity зарегистрированы.
- Девять новых ID RU/EN проверены через канонический каталог и exporter.
  Общий localization audit не прошёл из-за существующих конфликтов чужих строк;
  выполнен ограниченный экспорт АЕК с проверкой неизменности всех прежних
  runtime-строк. Чужой RussianManual не исправлялся и не перезаписывался.

## Что ещё не подтверждено

Editor save/reload, настоящий save/load, отображение в руках и кабинете,
анимации, посадка хвата и стрельба не проверялись в игре. Установка кандидата
не означает визуальную приёмку или готовность всего нового списка.

## Воспроизведение и откат

Build: `<WEAPON_SOURCE_ROOT>/_aek_jazz_build`.
`integration-receipt.json`, `integration-backup`, `localization-backup`,
`compiled-audit.json`, `lua-audit.json` сохраняют результат и исходные файлы.
Не возвращать старые items/metadata целиком после чужих последующих правок:
откатывать только записи АЕК и новые ресурсы по receipt.

Инструменты: `_integrate_aek.py`, `_check_aek_configurations.py`,
`_localize_aek.ps1`, `_document_aek.py`; контракт —
[JAZZ-WEAPON-AEK-001](../specs/active/JAZZ-WEAPON-AEK-001.md).
