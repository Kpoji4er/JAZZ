# Mercenaries

[Overview](home.md) · [Perks](perks.md) · [Русский](../ru/mercenaries.md)

Source: `jazz-units/UnitData` + `items.lua`. No merc UnitData in the `jazz` package.

## Code summary

| | |
| --- | ---: |
| Hireable Jazz mercs | **48** |
| Aff AIM (explicit in items) | 24 |
| Aff MERC | 12 |
| Aff omitted (still hireable, AIM-like) | 12 |
| Nearby NPCs | 2 (`JAZZ_Ivanov`, `Jazz_RecruterG10`) |

Hire tiers: Regular **21** · Veteran **16** · Elite **10** · blank (Spider) **1**.

Roles: Leader 7 · ExplosiveExpert 7 · Melee 6 · Autoriflemen 5 · Stealth 5 · Doctor 5 · Mechanic 4 · Marksmen 4 · HeavyWeapons 2 · AllRounder 2 · Negotiator 1.

Core AIM filters: **Autoriflemen**, **HeavyWeapons**, **Stealth**. XP to **level 21**.

All 48 have a named perk in StartingPerks; **working hooks** are only a subset — see [perks](perks.md).

## Full roster (UnitData)

Salary = `StartingSalary`. `0` means zero in data.

| Id | Nick (RU) | Role | Lvl | Tier | Aff | Perk | $ |
| --- | --- | ---: | ---: | --- | --- | --- | ---: |
| Jazz_Allik | Знаток | AllRounder | 5 | Elite | AIM | Jazz_Perk_Allik | 2600 |
| Jazz_Biff | Бифф | Leader | 2 | Regular | MERC | Jazz_Perk_Biff | 600 |
| Jazz_Biggens | Биггенс | ExplosiveExpert | 3 | Regular | AIM | Jazz_Perk_Biggens | 900 |
| Jazz_Blade | Бритва | Melee | 4 | Veteran | — | Jazz_Perk_Blade | 900 |
| Jazz_Bull | Бык | Melee | 2 | Regular | AIM | Jazz_Perk_Bull | 400 |
| Jazz_Buzz | Тоска | Autoriflemen | 4 | Elite | — | Jazz_Perk_Buzz ✓ | 1950 |
| Jazz_Carlos | Карлос | Stealth | 3 | Regular | AIM | Jazz_Perk_Carlos | 450 |
| Jazz_Colby | Колби | ExplosiveExpert | 5 | Elite | — | Jazz_Perk_Colby ✓ | 2800 |
| Jazz_Conrad | Конрад | Leader | 5 | Elite | — | Jazz_Perk_Conrad | 3300 |
| Jazz_Cord | Кардан | Mechanic | 3 | Regular | MERC | Jazz_Perk_Cord | 550 |
| Jazz_Cougar | Пума | Stealth | 4 | Veteran | MERC | Jazz_Perk_Cougar | 1600 |
| Jazz_Devin | Девин | ExplosiveExpert | 4 | Veteran | AIM | Jazz_Perk_Devin | 2000 |
| Jazz_Dimitri | Димитрий | ExplosiveExpert | 3 | Regular | — | Jazz_Perk_Dimitri | 500 |
| Jazz_Dynamo | Динамо | Mechanic | 3 | Regular | MERC | Jazz_Perk_Dynamo | 50 |
| Jazz_Eskimo | Эскимо | Marksmen | 3 | Regular | AIM | Jazz_Perk_Eskimo | 400 |
| Jazz_Flo | Фло | Negotiator | 2 | Regular | MERC | Jazz_Perk_Flo | 500 |
| Jazz_Gamos | Гамос | Stealth | 3 | Regular | AIM | Jazz_Perk_Gamos | 250 |
| Jazz_Gaston | Гастон | Marksmen | 5 | Elite | MERC | Jazz_Perk_Gaston | 2500 |
| Jazz_Grace | Грейс | Melee | 3 | Regular | AIM | Jazz_Perk_Grace | 1600 |
| Jazz_Grom | Гром | HeavyWeapons | 5 | Veteran | — | Jazz_Perk_Grom | 2500 |
| Jazz_Henning | Хеннинг | Leader | 5 | Elite | AIM | Jazz_Perk_Henning | 5000 |
| Jazz_Highball | Скала | Doctor | 3 | Regular | AIM | Jazz_Perk_Highball | 900 |
| Jazz_Hitman | Убийца | Marksmen | 4 | Veteran | AIM | Jazz_Perk_Hitman | 1500 |
| Jazz_Hobbit | Хоббит | ExplosiveExpert | 3 | Regular | MERC | Jazz_Perk_Hobbit | 700 |
| Jazz_Horg | Сигара | HeavyWeapons | 4 | Veteran | MERC | Jazz_Perk_Horg | 2700 |
| Jazz_Ira | Айра | Leader | 2 | Regular | — | Jazz_Perk_Ira | 400 |
| Jazz_Kulba | Кульба | Autoriflemen | 3 | Regular | AIM | Jazz_Perk_Kulba | 800 |
| Jazz_Laura | Лора | Doctor | 3 | Regular | AIM | Jazz_Perk_Laura | 1700 |
| Jazz_Lucky | Лаки | Autoriflemen | 4 | Veteran | AIM | Jazz_Perk_Lucky | 1900 |
| Jazz_Lynx | Рысь | Marksmen | 4 | Elite | — | Jazz_Perk_Lynx ✓ | 2650 |
| Jazz_Madman | Бешеный | Mechanic | 4 | Veteran | — | Jazz_Perk_Madman | 900 |
| Jazz_Manuel | Мануэль | Stealth | 3 | Regular | AIM | Jazz_Perk_Manuel | 600 |
| Jazz_Meat | Мясо | ExplosiveExpert | 3 | Regular | MERC | Jazz_Perk_Meat | 750 |
| JAZZ_Merc_Spouke | Фраг | ExplosiveExpert | 4 | Veteran | — | Jazz_Perk_00 ✓ | 2000 |
| Jazz_Miguel | Мигель | Leader | 4 | Veteran | AIM | Jazz_Perk_Miguel | 800 |
| Jazz_Mike | Майк | AllRounder | 6 | Elite | — | Jazz_Perk_Mike | 4000 |
| Jazz_Monk | Монк | Stealth | 4 | Veteran | AIM | Jazz_Perk_Monk | 2400 |
| Jazz_Nervous | Нервный | Autoriflemen | 3 | Regular | MERC | Jazz_Perk_Nervous | 700 |
| Jazz_Quinten | Дэнни | Doctor | 5 | Elite | AIM | Jazz_Perk_Quinten | 3000 |
| Jazz_Ricochet | Рикошет | Melee | 3 | Regular | MERC | Jazz_Perk_Ricochet | 800 |
| Jazz_Rothman | Ротман | Leader | 4 | Veteran | AIM | Jazz_Perk_Rothman | 2200 |
| Jazz_Shank | Шенк | Melee | 1 | Regular | MERC | Jazz_Perk_Shank | 50 |
| Jazz_Spider | Паук | Doctor | — | — | — | Jazz_Perk_Spider ✓ | — |
| Jazz_Static | Статик | Mechanic | 4 | Veteran | AIM | Jazz_Perk_Static | 1400 |
| Jazz_Steiger | Штайгер | Leader | 5 | Elite | AIM | Jazz_Perk_Steiger | 5500 |
| Jazz_Vicious | Злобный | Melee | 4 | Veteran | AIM | Jazz_Perk_Vicious | 1800 |
| Jazz_Vilde | Зануда | Autoriflemen | 4 | Veteran | AIM | Jazz_Perk_Vilde | 1800 |
| Jazz_Vince | Винс | Doctor | 4 | Veteran | AIM | Jazz_Perk_Vince | 1200 |

✓ = perk with confirmed gameplay hooks. Spider: Doctor + perk + AIM chat, but UnitData has no StartingSalary / StartingLevel / Tier (only SalaryLv1/Max).
