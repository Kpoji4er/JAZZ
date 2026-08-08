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
| `GrizzlyPerk` | Grizzly | Сигнатура MG: игнор штрафов без опоры; −урон / контроль отдачи |
| `GruntyPerk_JAZZ` | Grunty | Старт боя → +50% AP первый ход |
| `Jazz_Perk_OfficerAura` / `…Influence` | AI-офицеры | Аура командира; в тултипе — **текущий приказ**. Подробности: [Командная аура](officer-aura.md) |
| `Jazz_Perk_Mimicry` | IMP (личностные) | Диалоговые опции Negotiator/Scoundrel/Psycho без их боевых/эконом. эффектов |
| `Jazz_Perk_Veteran` | IMP (личностные) | +10 ко всем skill/stat checks |
| `Jazz_Perk_Sniper` | IMP (тактические) | +1 макс. уровень прицеливания (любое оружие) |

Пассивные Lynx/Buzz/Spider/Colby **без** HUD-toggle (кнопки скрыты). Toggle только у Фрага (`Jazz_Perk_00`).

## §A (UNITS-006) — переписанная Wave A

Перечень выше для Madman / Blade / Nervous / Henning / Dynamo / Lucky / Shank / Laura / Vince / Steiger / Mike — целевой Лист2 (не старый Wave A текст). Статусы: `Jazz_OrderAP` (Хеннинг), `Jazz_CombatMedicBuff` (Лора), `Jazz_OrderCTH` (Штайгер).

## IMP: стартовый экип

После IMP-теста кит собирается по статам и перкам (как в JA2): ствол по AutoWeapons/Heavy/Stealthy/Marksmanship, броня **JazzArmor_*** по Health (не ванильный Kevlar), инструменты по Mechanical/Medical и т.д. Подробности — в design `imp-starting-gear.md`.

## Ещё stubs

Остальные именные перки волны (Ira, Miguel, Grom, Biff, …) — Wave B/C, см. `docs/design/mercs-ja12/_named-perks-plan.md` и `JAZZ-UNITS-003` / `JAZZ-UNITS-006`.

## Итог для игрока

Рабочие именные эффекты: **Фраг, Тоска, Рысь, Паук, Колби** + §A (**Бешеный, Бритва, Нервный, Хеннинг, Злобный, Динамо, Эскимо, Лаки, Шенк, Зануда, Лора, Винс, Штайгер, Майк**) и Grizzly/Grunty.
