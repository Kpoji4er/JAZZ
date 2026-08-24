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

### Контузия и травмы от blast (playtest)

Для `aoeType == "none"` (осколочные/фугасные/flashbang/demo; **не** дым/газ/огонь):

- `ApplyDamageAndEffects` применяет `hit.effects` даже если броня не «пробита» по pen-class — blast-статусы не баллистические. Bleed по-прежнему только при pierce. BAT на explosion **не** вызывается (травма — `JazzTryApplyExplosionConcussionAndTrauma` по урону хита).
- `JazzTryApplyExplosionConcussionAndTrauma` (`Systems_Medicine.lua`): **`Concussion` гарантированно** на любом blast-hit юните (`aoeType none`, center и area); без ролла и без снижения от `StunGrenadeProtection` (тот по-прежнему влияет на flashbang Will/`SuppressStunGrenade`). Пропуск только при `TempHitPoints > 0`, не-blast aoe, grazing, мёртвых/invulnerable на входе `ApplyDamageAndEffects`. Длительность ~1–2 хода (−2 ОД, −15 CTH, +30% move, без Free Move).
- Травма (MED-004): Frag/HE `CenterAppliedEffects` **без** `*shot`. Одна зона (`spot_group`, иначе Ribs) по той же полосе урона, что и пуля (пол **20**, шаг +1, Heavy при ≥ **50%** MaxHP). Leftover `*shot` на хите — второй ролл не делается.
- Hits штампуют `aoe_type`/`weapon` в `Grenade`/`HeavyWeapon` `GetAttackResults`, чтобы smoke/fire не получали concussion. `JazzIsEnvironmentalAoeHit` (`smoke`/`teargas`/`toxicgas`/`fire`) также **блокирует** `JazzTryRollBleedFromHit` / graze-bleed / AppliedEffects `Bleeding*` / DangerClose bleed — дымовая граната не вешает кровь.

### Blast knockback — JAZZ-GRENADES-002

После concussion/trauma package живой Human (мерки и враги) **во внутреннем кольце** (`Dist2D(unit, epicenter) ≤ CenterAreaOfEffect × SlabSizeX` — то же, что inner mesh прицела / `min_range` в `GetAreaAttackParams`) проходит skill roll устоять на ногах:

```text
force = pre-armor blast damage          -- jazz_pre_armor_damage (= damage + armor_prevented)
body  = Strength + Health [+10 Veteran]
value = Clamp(body − force, 0, 100)
roll  = 1 + unit:Random(100)
устоял если force ≤ 0 или roll < value
```

Outer `AreaOfEffect` (за пределами `CenterAreaOfEffect`) — без ролла и без отлёта (контузия/травмы по-прежнему по своим правилам). Не использовать голый `hit.explosion_center` (слишком узкий: same-slab при CAOE=1).

Провал → отлёт как у `SteroidPunch`: свободные slab’ы от эпицентра (`pushSlabs = 1`), команда `JazzBlastKnocked` (knockdown-анимация → prone), **без** mock-`SteroidPunchGrenade`. Нет прохода → prone на месте. Skip: Dead, Prone, Unconscious, grit (`TempHitPoints > 0`), grazing, non-Human, non-blast aoe, вне inner Dist2D. Эпицентр штампуется в wrap `GetAreaAttackResults` → `hit.jazz_blast_epicenter`.

Публичный ID: `Concussion`. Icon: `Icons/StatusEffects/Concussion.png`.

AI использует собственную оценку допустимой дальности, targeting options и специальное действие flare. Поскольку `AIGetAttackTargetingOptions` в JAZZ заменяет и vanilla, и CommonLib версию, тест grenade/flare обязателен после обновления dependency.

### Отклонение (scatter / mishap) — JAZZ-GRENADES-001

Канон в `MishapProperties` (`System_OR_Weapons.lua`); `Grenade` и `HeavyWeapon` вызывают `ApplyImpactDeviation`.

- **Всегда** есть лёгкий scatter (Min-band), даже при «удачном» ролле.
- **Mishap** (Max-band + notification) только при провале ролла / `AlwaysMiss`; `results.mishap` только тогда.
- Шанс: smoothstep от 0 до **личной** дальности (без обрыва на ¼/½). Thrown blend `(Strength + Dexterity×2 + Explosives×2)/5`; потолок `Clamp(100−blend×60/100, 25, 100)` — 100/100/100 на mid ~20%, на краю ~40%. Дальность круга — `GetMaxAimRange` по **Силе**. GL: `(MS×2+Expl)/3`. Suppression/Inaccurate входят в effective dist.
- Величина **лёгкого scatter**: remap `scatter_tiles` — на половине ≈ старая полная интенсивность; на полном броске ≈ **+25%** к ней. `skill_mod = Clamp(100−blend, 10, 100)` только на **Min-band**.
- **Mishap (Max-band):** навык **не** ужимает отклонение (иначе элита сажает провал в 1–2 клетки). Нижняя граница ≥ **4** тайла (`Max(4, MinMishapRange, MaxMishapRange/2)`), верх — `MaxMishapRange`, дальше `dist_mod` 100..400% и CapTiles. Шанс mishap по-прежнему падает от навыка.
- Профили: ThrowGrenade `(Str + Dex×2 + Expl×2)/5` (без threshold); AimedHeavy `(MS×2+Expl)/3`; Demo/пайпы `(Expl×3+Dex)/4`.
- Cap отклонения: `Max(2×MaxMishapRange, 8)` тайлов; Min-band `dist_mod` clamp 40..200, Max-band 100..400.
- Area-aim: **радиус** колец = зона поражения; **цвет** blast/sphere tiles и дуги траектории = `GetCTHColor(GetMishapAimReliability)` — mix `(100 − mishap%) × (100 − scatter_risk%)`, где `scatter_risk` = mid(Min-band) / CapTiles (material `FillColor`/`fill_color`).

## Ловушки и мины

`System_OR_Traps.lua` создаёт динамические mine objects и хранит team ownership. При срабатывании система:

1. определяет владельца/отношение команд;
2. создаёт alert и noise;
3. запускает trap/explosion эффект;
4. синхронизирует последствия с состоянием тактической карты.

Для соответствующего JAZZ perk предусмотрено ускоренное/мгновенное время действия. Изменение времени, владельца или RNG является сетевой и savegame-чувствительной правкой.

**Proximity C4** (и остальные proximity-заряды): бросок ставит `DynamicSpawnLandmine` с `TriggerType = "Proximity"` и `triggerRadius = 1` воксель. Взрыв, когда юнит входит в радиус (`GetTriggerDistance` ≈ полклетки от центра мины). Союзники игрока видят свой заряд; враги **не** видят и не «находят» мины команды `player1` (`SeenBy` / `SeenByTeam`). Срабатывает от шага **любой** стороны в радиусе, не только врагов — подсказка предмета говорит «когда враг подходит», но движок не фильтрует союзников на trigger. Выстрел по заряду тоже подрывает.

**INV-004 salvage:** успешный `Landmine:AttemptDisarm` по-прежнему даёт 1–2 Parts. `OnMsg.TrapDisarm` затем с **40%** кладёт в сумку отряда один закладываемый кирпич: если мина брошенная (`item_thrown` Prox/Timed/Remote C4/TNT/PETN) — тот же тип; иначе вес TNT 60 / C4 30 / PETN 10. Бочки и booby не Landmine — без заряда.

## Газ и защитное снаряжение

`System_GasMask.lua` интегрирует gas mask с toxic gas и tear gas. Результат зависит от наличия/состояния защитного предмета; полностью изношенная маска не должна считаться полной защитой. Armor/appearance код дополнительно управляет конфликтами face/head slots и визуальным состоянием.

## Тяжёлое оружие и подавление

`GrenadeLauncher`, `RocketLauncher` и `Mortar` имеют собственный `GetBaseDegradePerShot`. Финальная версия методов определяется порядком `System_OR_Grenade.lua -> WeaponClasses.lua`. Machine gun actions и `JAZZ_MGSuppressionFire` передают попадания/промахи в suppression pipeline. Уровни представлены эффектами `suppressionLight`, `suppressionMedium`, `suppressionHeavy`, `suppressionHeavy2`, `Pinned`; очередь может накапливать Will damage.

### Одноразовые ракетные пусковые — JAZZ-WEAPONS-005

`RocketLauncher.DisposableLauncher` по умолчанию `false`. У `M72LAW` он включён: при добавлении предмета `EmbeddedOrdnance = "Warhead_Frag"` создаёт один встроенный выстрел, а `MagazineSize = 1`. Перезарядка блокируется в UI-проверке, `UnitInventory:ReloadWeapon` и `RocketLauncher:Reload`; RPG-7 остаётся обычной перезаряжаемой пусковой. `RocketLauncher:Reload` **возвращает** `prev, played_fx, change` из `Firearm.Reload` (иначе `ReloadWeapon` не чистит опустошённый стек). Пустой `Warhead_Frag` (`0/1`) снимается из фактического слота рюкзака, не из `OrdnanceInventory`.

После любого расходующего выстрела (включая mishap) `OnMsg.OnAttack` удаляет M72 из слота стрелка, создаёт отдельный `WeaponVisual` с entity `M72LAW2` у его ног и обновляет outfit. Это только world debris: визуальная труба не InventoryItem, не loot, не scrap и не пригодна для нового выстрела. Отмена до расхода и jam не вызывают этот путь. Runtime wave test остаётся обязательным.

## Данные

- ordnance и grenade items входят в 558 InventoryItem core;
- есть специализированные inventory slots `GrenadesInventory` и `OrdnanceInventory`;
- 50 crafting-operation recipes включают ammo (кустарные в picker) и mortar/ordnance;
- AI keywords `Explosives`, `Ordnance`, `Smoke`, `MG`, `Control` связывают роли юнитов с доступными действиями.

## Межпакетные зависимости

`jazz-units` задаёт grenade/heavy loadouts, AI keywords и archetypes; `jazz-maps` размещает мины, зоны, контейнеры и боевые сцены; `jazz_assets` предоставляет entities оружия, снарядов и визуальных состояний; core связывает всё действиями, FX и sound presets.

## Проверка

- ручной и AI-бросок на минимальной/максимальной дальности;
- obstruction, indoor/outdoor, smoke и friendly-fire оценка;
- граната в эпицентре и на границе зоны, разные explosive armor ratings;
- scatter/mishap: smoothstep 0→full personal range; throw blend Str+Dex+Expl; mishap = miss (≥4 tiles, no skill shrink); CapTiles, AoE tint (`JAZZ-GRENADES-001`);
- установка, обнаружение и подрыв мины союзником/врагом, save/load;
- perk-вариант времени установки;
- toxic/tear gas с новой, повреждённой и отсутствующей маской;
- grenade launcher/rocket/mortar degradation и reload; M72: один выстрел, Reload blocked, после normal и mishap shot нет в inventory и у стрелка есть непригодная spent tube; RPG-7 не спавнит tube и перезаряжается;
- MG setup, suppression tiers, Will loss и снятие эффектов;
- сетевой повтор area attack и trap.

## Ограничения и сопровождение

Дубли `GetBaseDegradePerShot` нельзя механически удалять без фиксации финального поведения. Изменения grenade action, trap state, gas protection или heavy weapon classes требуют обновить эту страницу, inventory/armor/AI страницы и тесты.