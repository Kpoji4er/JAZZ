# Наёмники JA1/2 — generation-каталог

Контракты для `$create-jazz-merc`: одна статья → полностью готовый мерк (UnitData, perk, loot, портреты, loc, VR).

- Шаблон: [`_template.md`](_template.md)
- Фразы: [`_phrase-checklist.md`](_phrase-checklist.md)
- Skill: [`.agents/skills/create-jazz-merc/SKILL.md`](../../.agents/skills/create-jazz-merc/SKILL.md)
- Источник дизайна: [AIM sheet → «Наемники из JA1/2»](https://docs.google.com/spreadsheets/d/19Je4n5Ju4cYmTLimzw45aFq_Ll8Wxz21RLIETFRsH2g/edit?gid=1773591798#gid=1773591798)

**Портреты:** без оружия в руках (кобура — крайний случай); роль по классовому киту (эталон — [Паук](spider.md)). Лицо — по JA2-референсу ``<slug>.ja2-face.*`` рядом со статьёй.

`executable: true` только у Ready и у planned без Open blockers. Генерацию planned не стартовать без approved change-spec волны.

## JA2 face files

Файлы ``*.ja2-face.gif|jpg`` лежат в этой же папке. Карта: [`_ja2-faces-map.txt`](_ja2-faces-map.txt). Нет лица у: `biff`, `spouke` (оригинал JAZZ / нет в архиве).

## Ready (as-shipped)

| Slug | Nick | UnitData Id |
| --- | --- | --- |
| [lynx](lynx.md) | Рысь | `Jazz_Lynx` |
| [tosca](tosca.md) | Тоска | `Jazz_Buzz` |
| [spider](spider.md) | Паук | `Jazz_Spider` |
| [spouke](spouke.md) | Фраг | `JAZZ_Merc_Spouke` |

## High

| Slug | Nick | Origin |
| --- | --- | --- |
| [colby](colby.md) | Колби | ja2 |
| [blade](blade.md) | Бритва | ja2 |
| [ira](ira.md) | Айра | ja2 |
| [dimitri](dimitri.md) | Димитрий | ja2 |
| [madman](madman.md) | Бешеный | ja2 |
| [conrad](conrad.md) | Конрад | ja2 |
| [mike](mike.md) | Майк | nightops |
| [grom](grom.md) | Гром | nightops |

## Medium

| Slug | Nick | Origin |
| --- | --- | --- |
| [rothman](rothman.md) | Ротман | ja2 |
| [quinten](quinten.md) | Дэнни | ja2 |
| [vicious](vicious.md) | Злобный | ja2 |
| [biff](biff.md) | Бифф | ja2 |
| [nervous](nervous.md) | Нервный | ja2 |
| [flo](flo.md) | Фло | ja2 |
| [cougar](cougar.md) | Пума | ja2 |
| [miguel](miguel.md) | Мигель | ja2 |
| [gamos](gamos.md) | Гамос | ja2 |
| [dynamo](dynamo.md) | Динамо | ja2 |
| [gaston](gaston.md) | Гастон | ub |
| [horg](horg.md) | Сигара | ub |
| [manuel](manuel.md) | Мануэль | ub/nightops |
| [monk](monk.md) | Монк | wildfire |
| [allik](allik.md) | Знаток | wildfire |
| [henning](henning.md) | Хеннинг | wildfire |

## Low

| Slug | Nick | Origin |
| --- | --- | --- |
| [static](static.md) | Статик | ja2 |
| [highball](highball.md) | Скала | ja2 |
| [bull](bull.md) | Бык | ja2 |
| [cord](cord.md) | Кардан | ja2 |
| [hobbit](hobbit.md) | Хоббит | ja2 |
| [ricochet](ricochet.md) | Рикошет | ja2 |
| [meat](meat.md) | Мясо | ja2 |
| [carlos](carlos.md) | Карлос | ja2 |
| [devin](devin.md) | Девин | ja2 |
| [shank](shank.md) | Шенк | ja2 |
| [vince](vince.md) | Винс | ja2 |
| [hitman](hitman.md) | Убийца | ja2 |
| [biggens](biggens.md) | Биггенс | ub |
| [kulba](kulba.md) | Кульба | ub |
| [vilde](vilde.md) | Зануда | wildfire |
| [grace](grace.md) | Грейс | wildfire |
| [steiger](steiger.md) | Штайгер | wildfire |
| [lucky](lucky.md) | Лаки | wildfire |
| [laura](laura.md) | Лора | wildfire |
| [eskimo](eskimo.md) | Эскимо | nightops |

## Команда генерации

```text
Сгенерируй мерка из docs/design/mercs-ja12/<slug>.md по skill create-jazz-merc
```
