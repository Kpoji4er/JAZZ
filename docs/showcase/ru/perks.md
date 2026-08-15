# Перки

[К обзору](home.md) · [Наёмники](mercenaries.md) · [Боевые действия](combat-actions.md) · [English](../en/perks.md)

Срез из `CharacterEffect/Jazz_Perk_*.lua`, `items.lua` и `Code/*` (jazz). Классовые weapon-кнопки (`JAZZ_Fanning` и т.д.) — на [боевых действиях](combat-actions.md), здесь — **именные / личные**.

## Слои

1. Именной перк мерка (`Jazz_Perk_*` в StartingPerks).
2. Личный combat action (кнопка = id перка / `GrizzlyPerk`) — только где нужен toggle/active.
3. Статус/аура (`Jazz_Perk_OfficerAura*`, `Jazz_OrderCTH`, `Jazz_OrderAP`, `Jazz_CombatMedicBuff`) — маркеры, не AIM-билд.

## Что реально работает в коде

| Id | Кто | Эффект в runtime |
| --- | --- | --- |
| `Jazz_Perk_00` | Фраг | Toggle: таймерные взрывчатки детонируют в начале хода врага |
| `Jazz_Perk_Buzz` | Тоска | +50% пуль автоогня |
| `Jazz_Perk_Lynx` | Рысь | +8 обзор днём; то же зрение смягчает штраф меткости за дальность (Range) |
| `Jazz_Perk_Spider` | Паук | ×2 Medical в sector heal |
| `Jazz_Perk_Colby` | Колби | +20% AoE гранат; 20% паника раненым в зоне |
| `Jazz_Perk_Madman` | Бешеный | Melee crit/kill → −10 Will всем ≤5 (включая союзников) |
| `Jazz_Perk_Blade` | Бритва | Зверство: каждый успешный удар в цепочке → ещё один удар |
| `Jazz_Perk_Nervous` | Нервный | Хит очереди/авто стекает +1 пулю на следующую (cap +10) |
| `Jazz_Perk_Henning` | Хеннинг | Союзники ≤10: +3 ОД (`Jazz_OrderAP`) |
| `Jazz_Perk_Vicious` | Злобный | +1 ОД за женщину в отряде (cap 3) на старте боя |
| `Jazz_Perk_Dynamo` | Динамо | Взлом замков не активирует ловушки на замках |
| `Jazz_Perk_Eskimo` | Эскимо | <50% HP без Panic; Wounded не режет firearm CTH |
| `Jazz_Perk_Lucky` | Лаки | CTH≥70% и miss → reroll выстрела |
| `Jazz_Perk_Shank` | Шенк | 50% melee defense; промах melee по нему → бросок ножа ≤8 |
| `Jazz_Perk_Vilde` | Зануда | Ночью/под землёй auto/burst +15 CTH |
| `Jazz_Perk_Laura` | Лора | После лечения союзника: +15 CTH и crit до конца следующего хода |
| `Jazz_Perk_Vince` | Винс | Пока в отряде: ~−25% расход аптечек/Meds (шанс не потратить заряд) |
| `Jazz_Perk_Steiger` | Штайгер | Ночь/подземка: союзники ≤10 получают +5 CTH |
| `Jazz_Perk_Mike` | Майк | Overwatch/PinDown +2 атаки; реакции, когда доступны |
| `GrizzlyPerk` | Grizzly | Сигнатура MG: **2×** пуль длинной очереди, **полный** урон, игнор без опоры, **2×** подавление |
| `GruntyPerk_JAZZ` | Grunty | Старт боя → +50% AP; далее шанс `10%×личный БД` (0…5; лог броска) |
| `JackOfAllTrades` | Wolf | Спутниковые операции примерно **на 33% быстрее** (vanilla `activityDurationMod`) |
| `SteroidPunch` | Steroid | Пассивка: melee CTH от Силы; успешный удар кулаками → отброс как vanilla Smash; Passive на хотбаре; стим без усталости; Burning DoT **−30%** |
| `ExplodingPalm` | DrQ | Удар голыми руками: статус по HP цели (KO / контузия / рёбра / руки / ноги / пах); сателлит **+30%** долг травм; **блок** инфекции |
| `MakeThemBleed` | Flay | +10% урона за кровоточащего врага в LOS (cap +50%); HUD-стак «Кровавый след» = число видимых |
| `DangerClose` | Larry / Larry_Clean | Взрывчатка ≥**8** клеток: **+40%** урона; взрывы **+2** стака кровотечения; без штрафов от боевых стимов |
| `GloryHog` | PierreMerc | Мачете **Charge** (не только по прямой) +**15** Grit; активка **Вербовка** — одна кнопка, список видимых врагов (один враг — сразу) → союзник ИИ / бой (не боссы) |
| `RecklessAssault` | Smiley | Улучшенный Run and Gun: **4** атаки с ПП/карабином/автоматом, **+15** СТН; **без** потери энергии; **CD после убийства** (как RnG) |
| `HawksEye` | Scope | Со снайперкой: Overwatch за **1 ОД** (остальные ОД остаются); Pin Down мин. 1 ОД; снайпер suppress **×2**; каждые **96 ч** — **7** печений; при найме тоже печёт |
| `HaveABlast` | Red | Toggle: ответ гранатой при попадании **или** промахе (руки / **слоты гранат** / рюкзак); **−50%** урона от взрывов по себе пока активен |
| `Nazdarovya` | Igor | Активка **2 ОД**, CD **на убийство**: снимает боль, лечит **15–20** HP, стак опьянения ≤**5** (−15 CTH / +20 ближний урон за стак); −1 стак / **3 ч** |
| `VengefulTemperament` | Meltdown (Лава) | Активка «Ураган Норма»: враги ≤5 клеток — Panic или Berserk (Wisdom). **Без** Run and Gun. |
| `KillingWind` | Fauda | ≥2 врагов: **+8 Grit за каждого**; штраф FM от брони **ещё −50%** (с Ironclad — **0**); громоздкое оружие **сохраняет** Free Move |
| `DoubleToss` | Fidel | Двойной бросок (≥2 в стаке): руки **или** карманы гранат |
| `BuildingConfidence` | MD | Inspired (+4 ОД) на ходах **2/5/8…**; лечение **±10%** за разницу уровней с пациентом (кап **±50%**), бой и спутник |
| `BulletHell` | Spike | Конусный ливень 15–30 пуль **без отдачи**; попадания по врагу в секторе; **Will всем в конусе**; CD **после убийства** |
| `Jazz_Perk_Flo` | Фло | В отряде: **−12%** покупка Bobby Ray / **+12%** обналичивание (аддитивно с Negotiator) |
| `Jazz_Perk_Static` | Статик | Ремонт/крафт Parts **−5%/уровень** (кап **−25%**) |
| `Jazz_Perk_Cougar` | Пума | Выстрелы **−33%** шума; SK → Inspired **1×/ход** |
| `Jazz_Perk_Grace` | Грейс | Первый бросок ножа/ход auto-hit ≤**12** |
| `Jazz_Perk_Kulba` | Кульба | US autos **−50%** отдачи |
| `Jazz_Perk_Grom` | Гром | Гранатомёт/миномёт/ПТР — Will suppress **×2** |
| `Jazz_Perk_Ricochet` | Рикошет | Melee splash на врага ≤1 от цели |
| `Jazz_Perk_Highball` | Хайболл | Лечение **±50%**, если союзник-врач Med≥80 в ≤5 |
| `Jazz_Perk_Meat` | Мясо | Мораль не роняет Will (partial) |
| `Jazz_Perk_OfficerAura` / `…Influence` | AI-офицеры | Аура командира; в тултипе — **текущий приказ**. Подробности: [Командная аура](officer-aura.md) |
| `Jazz_Perk_Mimicry` | IMP (личностные) | Диалоговые опции Negotiator/Scoundrel/Psycho без их боевых/эконом. эффектов |
| `Jazz_Perk_Veteran` | IMP (личностные) | +10 ко всем skill/stat checks |
| `Jazz_Perk_Sniper` | IMP (тактические) | +1 макс. уровень прицеливания (любое оружие) |

Пассивные Lynx/Buzz/Spider/Colby видны на signature-хотбаре (кнопки Passive только для информации; иконки из `Perks/SignatureAbilities/`). Toggle только у Фрага (`Jazz_Perk_00`).

## §A / §C / §B / §D (UNITS-006)

§A + §C batch2/3 — целевой Лист2. Soft-cut batch3: Flay groin/animal apply (dmg aura only). **GloryHog recruit** и **RecklessAssault** wired. **MD** heal%-by-level wired. **Reaper `TheGrim`:** перезарядка после **5** убийств (не одного). **Owner 2026-08-11:** личные перки Hitman/Tex/Shadow/Buns/Sidney/Raven/Mouse/Omryn/Raider/Len/Fox/Scully/Magic/Ivan/Gus/Nails/Ice/Blood — снова **vanilla JA3** (JAZZ CE overrides сняты; Reaper — CHANGE только CD×5).

§B batch4: **Flo / Static / Cougar** + Grace/Kulba/Grom/Ricochet/Highball.

**Batch5 HARD/satellite:** Rothman (шахта, loyalty-scaled доход), Miguel (аура 30 Will/CTH), Ira (+20 к случайной характеристике милиции), **Barry** (`DesignerExplosives`): каждые **168 ч** — **2× Shaped Charge**; крафт через «Изготовление взрывчатки»; **−30% Parts** в рецепте и при списании CraftAmmo/CraftExplosives, пока Barry в секторе (на операции или Idle; TNT/порох без скидки). Meat Will→Grit, Carlos detection/Hidden, Cord city repair, Conrad Leadership≥90 trainer. **Igor** (`Nazdarovya`): drink 2 ОД, CD на убийство — heal/Pain/Drunk stacks. **Thor** (`NaturalHealing`): косяки каждые 48 ч; в отряде sat +15% к восстановлению травм/ожогов/HP-долга (не инфекция); перевязка +20–25 Will. Soft: Biff troopers economy, Livewire money op (ECON-001).

**Batch6 §D:** `Jazz_Perk_Benny` («Вам посылка») и `Jazz_Perk_Simon` («Абсолютный снайпер») — CE + StartingPerks; CombatAction soft-cut. Статусы: `Jazz_MiguelAuraUp`/`Down`, `Jazz_OrderAP`, `Jazz_OrderCTH`, …

## IMP: стартовый экип

После IMP-теста кит собирается по статам и перкам (как в JA2): ствол по AutoWeapons/Heavy/Stealthy/Marksmanship, броня **JazzArmor_*** по Health (не ванильный Kevlar), инструменты по Mechanical/Medical и т.д. Подробности — в design `imp-starting-gear.md`.

## Ещё stubs

Monk/Horg/Manuel/Hitman JA12 signatures, Bull inventory, Iggy bombard call-site, full Biff/Livewire ops — см. `_units006_batch5_notes.md` / `_units006_batch6_notes.md`.

## Итог для игрока

Рабочие именные эффекты: **Фраг, Тоска, Рысь, Паук, Колби** + §A + §C batch2/3 + §B batch4 + batch5 (Ротман/Мигель/Барри/Мясо/Карлос/…) + §D Бенни/Саймон (helpers).
