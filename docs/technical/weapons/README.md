# Канонический каталог оружия

Этот раздел является источником истины для балансовой классификации и справочных характеристик стрелкового оружия JAZZ. Игроковые страницы в `docs/wiki/weapons/` генерируются только из этих данных.

## Источники и приоритет

| Данные | Канонический источник | Назначение |
|---|---|---|
| Характеристики оружия | `data/weapons.csv` | Одна строка на технический weapon ID |
| Доступные слоты и варианты | `data/weapon-component-options.csv` | Нормализованная связь оружие → слот → компонент |
| Компоненты | `data/weapon-components.csv` | Название, цена, сложность, эффекты и параметры |
| Эффекты компонентов | `data/weapon-component-effects.csv` | Словарь стабильных effect ID |
| Первичная миграция тиров | `data/tier-migration.csv` | Только происхождение тиров из Google Sheets; не второй источник истины |
| Игроковая энциклопедия | `../../wiki/weapons/` | Генерируемое представление; вручную не редактируется |

Первичное заполнение характеристик выполнено из последнего коммита JAZZ `5db078dfb2c9206f39e491a1d26b6e7f1f6f1220`, а не из незакоммиченных плейтестовых изменений. Используемые JAZZ-компоненты дополнены определениями из официального JA3 source drop с `lua_revision = 233360`. После первичной миграции каноном являются CSV этого каталога.

## Текущий охват

- 160 технических записей оружия;
- 157 активных записей, попадающих в player wiki;
- `AR15`, `M4Commando` и базовый `MP5` имеют `catalog_status = excluded_disabled` и намеренно исключены из player wiki;
- 156 существующих записей сопоставлены со строками профильных вкладок Google Sheets;
- 20 строк таблицы пока не имеют runtime weapon ID и сохранены в `tier-migration.csv` со статусом `not_in_runtime`;
- у 22 активных записей canonical tier отличается от `comment = "Tier …"` в стабильном Lua. До синхронизации runtime верным считается `tier_label`, а старое значение доступно в `code_tier_label` только для аудита.

`Auto5_quest` существует в runtime, но не имеет отдельной строки в профильной таблице и пока остаётся без balance-tier. `DragunovSVD_Custom` и `BrowningM2HMG` перечислены в таблице без тира, поэтому их canonical tier также пуст.

## Контракт тиров

- `balance_tier` — силовой диапазон внутри оружейного семейства. Разница между тирами должна быть заметна по суммарной ценности оружия.
- `balance_subtier` — порядок или профиль близких вариантов внутри одного тира. Под-тир не должен создавать скрытый дополнительный тир.
- `UNIQ` — уникальный профиль внутри указанного основного тира.
- `tier_label` — каноническая запись вида `2-4` или `2-UNIQ`.
- `code_tier_label` — старый комментарий в Lua; не использовать для балансовых решений.
- `engine_tier` — независимое поле магазина/лута. Оно не является balance-tier.
- `tier_source` — происхождение текущей миграции. После утверждения CSV это поле остаётся provenance, а не разрешением снова считать Google Sheets каноном.

Сравнение тиров выполняется внутри семейства. Урон не является единственным бюджетом: магазин, ОД, прицеливание, BDR, дальность, кучность, эргономика, отдача, режимы огня, надёжность, ресурс и компоненты могут компенсировать друг друга.

## Схема `weapons.csv`

Идентификаторы и структура рассчитаны на чтение человеком, скриптом и языковой моделью:

- `id`, `object_class`, `family_id` — стабильные ключи; `display_name` и `family_name_ru` — представление;
- `catalog_status` — `active` или `excluded_disabled`;
- `balance_tier`, `balance_subtier`, `tier_label`, `tier_status` — каноническая классификация;
- `tier_source`, `code_tier_label`, `engine_tier` — provenance и независимые legacy/runtime поля;
- `caliber`, `damage`, `obj_damage_mod`, `penetration_class`, `penetration_bonus`, `crit_chance_scaled`, `magazine_size` — поражающее действие;
- `shoot_ap`, `reload_ap`, `max_aim_actions`, `aim_accuracy` — стоимость и прицеливание; AP хранится во внутренних тысячных движка;
- `burst_shots`, `auto_shots`, `recoil`, `available_attacks` — режимы огня;
- `weapon_range`, `bullet_drop_range`, `grouping`, `handling` — дистанционный профиль;
- `overwatch_angle`, `noise`, `reliability`, `base_jam_chance`, `weapon_resource`, `weapon_resource_max`, `degrade_per_shot` — применение и состояние;
- `hand_slot`, `holster_slot`, `large_item`, `cumbersome`, `cost`, `scrap_parts`, `repair_cost` — инвентарь и экономика;
- `component_slot_count`, `component_option_count` — быстрые счётчики;
- `defaulted_fields` — поля, отсутствовавшие в сериализованном weapon-файле и разрешённые через подтверждённый default класса;
- `source_file`, `snapshot_commit` — происхождение первичного импорта.

## Нормализация компонентов

`weapon-component-options.csv` содержит по одной строке на вариант компонента. Ключ связи — `(weapon_id, slot_index, component_id)`. Поля `default_component`, `default_in_options` и `is_default` позволяют находить сериализационные аномалии без разбора вложенного Lua.

`weapon-components.csv` хранит стабильный `component_id`, имя, слот, цену, сложность, effect ID, параметры и дополнительные материалы. `source = jazz` означает определение JAZZ; `source = vanilla_233360` — используемый fallback из официального source drop. `weapon-component-effects.csv` позволяет соединить effect ID с названием и описанием.

Из первичного снимка сохранены десять случаев, где `DefaultComponent` отсутствует среди `AvailableComponents`. Это не исправлено документацией автоматически: список показывается в индексе player wiki как data anomaly.

## Запланированные, но отсутствующие в runtime записи

| Вкладка | Название | Тир |
|---|---|---|
| ПП | Beretta MX4 Storm | 2-2 |
| ПП | PP-19 Vityaz | 3-2 |
| КАР | AK-105 | 3-1 |
| КАР | FN F2000 | 3-2 |
| ШВ | Stoner 63A | 2-3 |
| ШВ | FB Beryl | 2-5 |
| ШВ | AK-103 | 2-5 |
| ШВ | HK G11 | 2-UNIQ |
| ШВ | XM29 OICW | 2-UNIQ |
| ШВ | АК-74М | 3-1 |
| ШВ | HK416 | 3-1 |
| ШВ | АЕК-973 | 3-2 |
| ШВ | H&K XM8 | 3-3 |
| БВ | FN SCAR | 3-1 |
| ПУЛ | Negev | 3-1 |
| ПУЛ | MG4 | 3-3 |
| ПУЛ | PKP Pecheneg | 3-3 |
| ДРБ | Mossberg500 | 2-3 |
| ДРБ | KS-23 | 3-1 |
| ДРБ | Saiga-12 | 2-5 |

Они не появляются в player wiki, пока не получат runtime ID и полный набор характеристик/слотов.

## Процесс изменения

1. Сначала изменить канонические CSV и зафиксировать балансовое намерение.
2. Выполнить `node scripts/docs/weapons-docs.mjs build`.
3. Внести те же данные через Mod Editor в принадлежащие JAZZ generated files; не править только одну сериализованную копию.
4. Проверить diff `items.lua`, `metadata.lua` и профильных `InventoryItem`.
5. Выполнить `node scripts/docs/weapons-docs.mjs check`, статические проверки и игровые smoke-тесты.

Команда `import` предназначена только для первичной загрузки или осознанного полного re-bootstrap и без `--force` не перезаписывает существующий каталог. Обычное обновление никогда не должно начинаться с импорта из Lua.

Перед `import` задать `JA3_ROOT` корнем установленной игры либо `JA3_WEAPON_COMPONENTS_PATH` полным путём к `WeaponComponentSharedClass.lua`. В tracked-файлах используется только `<JA3_ROOT>`; абсолютный путь конкретной машины не сохраняется.

## Связанные документы

- [Каноническая модель точности](accuracy-model.md)
- [Техническая система оружия, боеприпасов и компонентов](../systems/weapons-ammo-components.md)
- [Текущий runtime CTH pipeline](../systems/combat-cth-actions.md)
- [Игроковая энциклопедия](../../wiki/weapons/README.md)
