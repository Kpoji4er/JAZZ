# Ремонт и запчасти оружия (design)

Канон: `docs/specs/active/JAZZ-WEAPONS-002.md` (**draft**).

## Триада

| Слой | Поле | Ремонт |
| --- | --- | --- |
| current | `WeaponResource` | да, до max |
| max | `WeaponResourceMax` | **нельзя** поднять обычным ремонтом |
| factory | `GetFactoryResource()` | reference |

## Как падает max

| Событие | −max |
| --- | --- |
| Выстрел (низкий шанс ~1% или меньше) | маленький loss при hit |
| **Обычный jam** | **0.5%** текущего max |
| **Критический jam** | **3%** текущего max |
| Failed Unjam | 1–3% max (как сейчас) |
| Failed install/remove | current + max |
| RepairItems | нет (+ только current) |

## Два типа клина

При любом jam → roll типа:

| Тип | −max |
| --- | ---: |
| Обычный | 0.5% |
| Критический | 3% |

**P(критический | jam)** растёт, когда оружие в плохом состоянии (низкий current/max %), и падает с ростом **Mechanical** владельца. Точная кривая — при реализации.

## UI jam %

Эффективный % (`GetDisplayJamChancePercent`).

## Снимаемые

| Что | Guaranteed Mech | Ниже |
| --- | ---: | --- |
| Scope, глушитель, лазер/фонарь, рукоятка | ≥30 | шанс; провал → −current/−max |
| ГП item | ≥40 | шанс; то же |

Аттачам resource **нет**.

## Расходники

`Parts` + `GunBarrelParts`.

## Открыто

- Когда repair жрёт BarrelParts?
- Mag/Bipod/compensator?
- Формула P(crit|jam)?
- 1.0% vs 0.5% на −max/выстрел; loss при hit?
- Loss на провале монтажа?
