# Наёмники JA1/2 — generation-каталог

Контракты для `$create-jazz-merc`: одна статья → полностью готовый мерк (UnitData, perk, loot, портреты, loc, VR).

- Шаблон: [`_template.md`](_template.md)
- Фразы: [`_phrase-checklist.md`](_phrase-checklist.md)
- Skill: [`.agents/skills/create-jazz-merc/SKILL.md`](../../.agents/skills/create-jazz-merc/SKILL.md)
- План генерации (один за другим): [`.agents/skills/create-jazz-merc/references/generation-plan.md`](../../.agents/skills/create-jazz-merc/references/generation-plan.md)
- Источник дизайна: [AIM sheet → «Наемники из JA1/2»](https://docs.google.com/spreadsheets/d/19Je4n5Ju4cYmTLimzw45aFq_Ll8Wxz21RLIETFRsH2g/edit?gid=1773591798#gid=1773591798)

**Портреты:** без оружия в руках (кобура — крайний случай); роль по классовому киту (эталон — [Паук](spider.md)). Лицо — по JA2-референсу ``<slug>.ja2-face.*`` рядом со статьёй.

`executable: true` только у Ready и у planned без Open blockers. Генерацию planned не стартовать без approved change-spec волны. Очередь: **один мерк за раз** по явной команде; текущий кандидат — см. generation-plan.

## JA2 face files

Файлы ``*.ja2-face.gif|jpg`` лежат в этой же папке. Карта: [`_ja2-faces-map.txt`](_ja2-faces-map.txt). Нет лица у: `biff`, `spouke` (оригинал JAZZ / нет в архиве).

## Ready (as-shipped / wave codegen)

Внешние эталоны: lynx, tosca, spider, spouke.  
Волна JAZZ-UNITS-002: **44/44** — UnitData + perk companion + портреты 300/2000.  
Очередь: [`_generation-queue.md`](_generation-queue.md). Gaps (perk hooks, rich AIM, Appearance, sync/loc audit) — там же.

| Slug | Nick | UnitData Id |
| --- | --- | --- |
| [lynx](lynx.md) | Рысь | `Jazz_Lynx` |
| [tosca](tosca.md) | Тоска | `Jazz_Buzz` |
| [spider](spider.md) | Паук | `Jazz_Spider` |
| [spouke](spouke.md) | Фраг | `JAZZ_Merc_Spouke` |
| [colby](colby.md) | Колби | `Jazz_Colby` |
| [blade](blade.md) | Бритва | `Jazz_Blade` |
| [ira](ira.md) | Айра | `Jazz_Ira` |
| [dimitri](dimitri.md) | Димитрий | `Jazz_Dimitri` |
| [madman](madman.md) | Бешеный | `Jazz_Madman` |
| [conrad](conrad.md) | Конрад | `Jazz_Conrad` |
| [mike](mike.md) | Майк | `Jazz_Mike` |
| [grom](grom.md) | Гром | `Jazz_Grom` |
| [rothman](rothman.md) | Ротман | `Jazz_Rothman` |
| [quinten](quinten.md) | Дэнни | `Jazz_Quinten` |
| [vicious](vicious.md) | Злобный | `Jazz_Vicious` |
| [biff](biff.md) | Бифф | `Jazz_Biff` |
| [nervous](nervous.md) | Нервный | `Jazz_Nervous` |
| [flo](flo.md) | Фло | `Jazz_Flo` |
| [cougar](cougar.md) | Пума | `Jazz_Cougar` |
| [miguel](miguel.md) | Мигель | `Jazz_Miguel` |
| [gamos](gamos.md) | Гамос | `Jazz_Gamos` |
| [dynamo](dynamo.md) | Динамо | `Jazz_Dynamo` |
| [gaston](gaston.md) | Гастон | `Jazz_Gaston` |
| [horg](horg.md) | Сигара | `Jazz_Horg` |
| [manuel](manuel.md) | Мануэль | `Jazz_Manuel` |
| [monk](monk.md) | Монк | `Jazz_Monk` |
| [allik](allik.md) | Знаток | `Jazz_Allik` |
| [henning](henning.md) | Хеннинг | `Jazz_Henning` |
| [static](static.md) | Статик | `Jazz_Static` |
| [highball](highball.md) | Скала | `Jazz_Highball` |
| [bull](bull.md) | Бык | `Jazz_Bull` |
| [cord](cord.md) | Кардан | `Jazz_Cord` |
| [hobbit](hobbit.md) | Хоббит | `Jazz_Hobbit` |
| [ricochet](ricochet.md) | Рикошет | `Jazz_Ricochet` |
| [meat](meat.md) | Мясо | `Jazz_Meat` |
| [carlos](carlos.md) | Карлос | `Jazz_Carlos` |
| [devin](devin.md) | Девин | `Jazz_Devin` |
| [shank](shank.md) | Шенк | `Jazz_Shank` |
| [vince](vince.md) | Винс | `Jazz_Vince` |
| [hitman](hitman.md) | Убийца | `Jazz_Hitman` |
| [biggens](biggens.md) | Биггенс | `Jazz_Biggens` |
| [kulba](kulba.md) | Кульба | `Jazz_Kulba` |
| [vilde](vilde.md) | Зануда | `Jazz_Vilde` |
| [grace](grace.md) | Грейс | `Jazz_Grace` |
| [steiger](steiger.md) | Штайгер | `Jazz_Steiger` |
| [lucky](lucky.md) | Лаки | `Jazz_Lucky` |
| [laura](laura.md) | Лора | `Jazz_Laura` |
| [eskimo](eskimo.md) | Эскимо | `Jazz_Eskimo` |

## High / Medium / Low

*(пусто — волна в Ready; приоритеты в frontmatter статей и в `_generation-queue.md`)*

## Команда генерации

```text
Сгенерируй мерка из docs/design/mercs-ja12/<slug>.md по skill create-jazz-merc
```
