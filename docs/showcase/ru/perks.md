# Перки

[К обзору](home.md) · [Наёмники](mercenaries.md) · [Боевые действия](combat-actions.md) · [English](../en/perks.md)

Срез из `CharacterEffect/Jazz_Perk_*.lua`, `items.lua` и `Code/*` (jazz). Классовые weapon-кнопки (`JAZZ_Fanning` и т.д.) — на [боевых действиях](combat-actions.md), здесь — **именные / личные**.

## Слои

1. Именной перк мерка (`Jazz_Perk_*` в StartingPerks).
2. Личный combat action (кнопка = id перка / `GrizzlyPerk`) — только где нужен toggle/active.
3. Статус/аура (`Jazz_Perk_OfficerAura*`, `Jazz_OrderCTH`) — маркеры, не AIM-билд.

## Что реально работает в коде

| Id | Кто | Эффект в runtime |
| --- | --- | --- |
| `Jazz_Perk_00` | Фраг | Toggle: таймерные взрывчатки детонируют в начале хода врага |
| `Jazz_Perk_Buzz` | Тоска | +50% пуль автоогня |
| `Jazz_Perk_Lynx` | Рысь | +8 обзор днём; то же зрение смягчает штраф меткости за дальность (Range) |
| `Jazz_Perk_Spider` | Паук | ×2 Medical в sector heal |
| `Jazz_Perk_Colby` | Колби | +20% AoE гранат; 20% паника раненым в зоне |
| `Jazz_Perk_Madman` | Бешеный | Kill в упор → Inspired |
| `Jazz_Perk_Blade` | Бритва | Melee +20 CTH, без критов |
| `Jazz_Perk_Nervous` | Нервный | Autofire/burst +2 пули |
| `Jazz_Perk_Henning` | Хеннинг | Союзники ≤5: +5 CTH на следующую атаку |
| `Jazz_Perk_Vicious` | Злобный | +1 ОД за женщину в отряде (cap 3) на старте боя |
| `Jazz_Perk_Dynamo` | Динамо | Head hit: 25% Blinded |
| `Jazz_Perk_Eskimo` | Эскимо | <50% HP без Panic; Wounded не режет firearm CTH |
| `Jazz_Perk_Lucky` | Лаки | 1×/бой: первый firearm miss → hit |
| `Jazz_Perk_Shank` | Шенк | Melee по нему −50 CTH |
| `Jazz_Perk_Vilde` | Зануда | Ночью/под землёй auto/burst +15 CTH |
| `Jazz_Perk_Laura` | Лора | После перевязки союзника снова Hidden |
| `Jazz_Perk_Vince` | Винс | 1×/бой: первая перевязка союзника → цели +4 ОД |
| `Jazz_Perk_Steiger` | Штайгер | Ночью: союзники ≤5 получают +5 CTH |
| `GrizzlyPerk` | Grizzly | Личная MG-атака + CTH/recoil |
| `GruntyPerk_JAZZ` | Grunty | Старт боя → +50% AP первый ход |
| `Jazz_Perk_OfficerAura` / `…Influence` | AI-офицеры | Аура командира |

Пассивные Lynx/Buzz/Spider/Colby **без** HUD-toggle (кнопки скрыты). Toggle только у Фрага (`Jazz_Perk_00`).

## Ещё stubs

Остальные именные перки волны (Ira, Miguel, Grom, Biff, …) — Wave B/C, см. `docs/design/mercs-ja12/_named-perks-plan.md` и `JAZZ-UNITS-003`.

## Итог для игрока

Рабочие именные эффекты: **Фраг, Тоска, Рысь, Паук, Колби** + Wave A (**Бешеный, Бритва, Нервный, Хеннинг, Злобный, Динамо, Эскимо, Лаки, Шенк, Зануда, Лора, Винс, Штайгер**) и Grizzly/Grunty.
