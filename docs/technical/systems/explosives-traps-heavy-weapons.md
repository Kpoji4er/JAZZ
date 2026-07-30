# Взрывчатка, ловушки и тяжёлое оружие

## Назначение и эффект для игрока

Система охватывает бросок гранат, зональный урон, гранатомёты, ракеты, миномёты, устанавливаемые ловушки, газ и тяжёлое подавление. JAZZ добавляет специализированные действия, расход/износ оружия, AI-оценку дальности и собственную обработку динамических мин.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | `Grenade`, `Ordnance`, area attacks, traps/mines, gas zones, heavy weapon classes и AI grenade actions |
| CommonLib | Исправляет общие AI targeting/action функции; отдельной одноимённой коллизии trap/grenade methods в проверенном срезе не подтверждено |
| JAZZ | Заменяет grenade/ordnance runtime, trap creation/triggering, gas-mask protection, heavy weapon degradation и AI range/scoring |

## Реализация и load-state

Загружаются:

- `Code/System_OR_Grenade.lua` — grenade, grenade launcher, rocket launcher и mortar extensions;
- `Code/System_OR_Traps.lua` — динамические мины, принадлежность, шум и alert;
- `Code/System_GasMask.lua` — защита от toxic/tear gas;
- `Code/AiAction_ThrowFlare.lua` — AI action для flare/броска;
- `Code/IModeCombatAreaAim.lua` — выбор зоны;
- `Code/WeaponClasses.lua` — финальные class methods тяжёлого оружия;
- `Code/System_ArmorRating.lua` и `Code/System_OR_Unit.lua` — урон, воля, статусы и unit reactions;
- generated grenade/ordnance items, actions, calibers, ammo и recipes.

## Гранаты и зональная атака

Семейство `ThrowGrenade` представлено несколькими action presets для разных вариантов применения. Area-aim строит зону и набор целей, после чего grenade runtime применяет урон/effects. Для взрывов отдельно учитываются explosive armor rating, дистанция до эпицентра, suppression/Will damage и состояния цели.

AI использует собственную оценку допустимой дальности, targeting options и специальное действие flare. Поскольку `AIGetAttackTargetingOptions` в JAZZ заменяет и vanilla, и CommonLib версию, тест grenade/flare обязателен после обновления dependency.

### Отклонение (scatter / mishap) — JAZZ-GRENADES-001

Канон в `MishapProperties` (`System_OR_Weapons.lua`); `Grenade` и `HeavyWeapon` вызывают `ApplyImpactDeviation`.

- **Всегда** есть лёгкий scatter (Min-band), даже при «удачном» ролле.
- **Mishap** (Max-band + notification) только при провале ролла / `AlwaysMiss`; `results.mishap` только тогда.
- На дистанции ≤ половины `ThrowMaxRange` / `WeaponRange` (с учётом suppression/Inaccurate в effective dist) **mishap chance = 0** — только scatter.
- Дальше шанс растёт к 100% у полной дальности; base от skill blend + competence remap.
- Профили: ThrowGrenade `(Dex×2+Expl)/3` thr **30**; AimedHeavy `(MS×2+Expl)/3` thr **30**; Demo/пайпы `(Expl×3+Dex)/4` thr **60**.
- Cap отклонения: `Max(2×MaxMishapRange, 8)` тайлов; Min-band плавнее (`/10`, clamp 40..200).
- Area-aim: **радиус** колец = зона поражения; **цвет** = `GetCTHColor(100 − mishap%)` как у кольца прицела.

## Ловушки и мины

`System_OR_Traps.lua` создаёт динамические mine objects и хранит team ownership. При срабатывании система:

1. определяет владельца/отношение команд;
2. создаёт alert и noise;
3. запускает trap/explosion эффект;
4. синхронизирует последствия с состоянием тактической карты.

Для соответствующего JAZZ perk предусмотрено ускоренное/мгновенное время действия. Изменение времени, владельца или RNG является сетевой и savegame-чувствительной правкой.

## Газ и защитное снаряжение

`System_GasMask.lua` интегрирует gas mask с toxic gas и tear gas. Результат зависит от наличия/состояния защитного предмета; полностью изношенная маска не должна считаться полной защитой. Armor/appearance код дополнительно управляет конфликтами face/head slots и визуальным состоянием.

## Тяжёлое оружие и подавление

`GrenadeLauncher`, `RocketLauncher` и `Mortar` имеют собственный `GetBaseDegradePerShot`. Финальная версия методов определяется порядком `System_OR_Grenade.lua -> WeaponClasses.lua`. Machine gun actions и `JAZZ_MGSuppressionFire` передают попадания/промахи в suppression pipeline. Уровни представлены эффектами `suppressionLight`, `suppressionMedium`, `suppressionHeavy`, `suppressionHeavy2`, `Pinned`; очередь может накапливать Will damage.

## Данные

- ordnance и grenade items входят в 558 InventoryItem core;
- есть специализированные inventory slots `GrenadesInventory` и `OrdnanceInventory`;
- 49 crafting-operation recipes включают ammo и mortar/ordnance;
- AI keywords `Explosives`, `Ordnance`, `Smoke`, `MG`, `Control` связывают роли юнитов с доступными действиями.

## Межпакетные зависимости

`jazz-units` задаёт grenade/heavy loadouts, AI keywords и archetypes; `jazz-maps` размещает мины, зоны, контейнеры и боевые сцены; `jazz_assets` предоставляет entities оружия, снарядов и визуальных состояний; core связывает всё действиями, FX и sound presets.

## Проверка

- ручной и AI-бросок на минимальной/максимальной дальности;
- obstruction, indoor/outdoor, smoke и friendly-fire оценка;
- граната в эпицентре и на границе зоны, разные explosive armor ratings;
- scatter/mishap: half-range zero chance, skill blends, CapTiles, AoE tint (`JAZZ-GRENADES-001`, playtest);
- установка, обнаружение и подрыв мины союзником/врагом, save/load;
- perk-вариант времени установки;
- toxic/tear gas с новой, повреждённой и отсутствующей маской;
- grenade launcher/rocket/mortar degradation и reload;
- MG setup, suppression tiers, Will loss и снятие эффектов;
- сетевой повтор area attack и trap.

## Ограничения и сопровождение

Дубли `GetBaseDegradePerShot` нельзя механически удалять без фиксации финального поведения. Изменения grenade action, trap state, gas protection или heavy weapon classes требуют обновить эту страницу, inventory/armor/AI страницы и тесты.