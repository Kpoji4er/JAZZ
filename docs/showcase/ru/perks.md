# Перки

[К обзору](home.md) · [Наёмники](mercenaries.md) · [Боевые действия](combat-actions.md) · [English](../en/perks.md)

Срез из `CharacterEffect/Jazz_Perk_*.lua`, `items.lua` и `Code/*` (jazz). Классовые weapon-кнопки (`JAZZ_Fanning` и т.д.) — на [боевых действиях](combat-actions.md), здесь — **именные / личные**.

## Слои

1. Именной перк мерка (`Jazz_Perk_*` в StartingPerks).
2. Личный combat action (кнопка = id перка / `GrizzlyPerk`).
3. Статус/аура (`Jazz_Perk_OfficerAura*`) — не AIM-билд.

## Что реально работает в коде

| Id | Кто | Эффект в runtime |
| --- | --- | --- |
| `Jazz_Perk_00` | Фраг (`JAZZ_Merc_Spouke`) | Toggle: таймерные взрывчатки детонируют в начале хода врага |
| `Jazz_Perk_Buzz` | Тоска (`Jazz_Buzz`) | +50% число пуль автоогня (хуки в WeaponAttacks / items) |
| `Jazz_Perk_Lynx` | Рысь | +8 к обзору (`System_OR_Unit`); текст про CTH на дистанции **не** подтверждён кодом |
| `Jazz_Perk_Spider` | Паук | ×2 Medical в sector heal operations |
| `Jazz_Perk_Colby` | Колби | +20% AoE гранат; 20% паника по раненым в зоне взрыва |
| `GrizzlyPerk` | Grizzly (vanilla+JAZZ) | Личная MG-атака + CTH/recoil hooks |
| `GruntyPerk_JAZZ` | Grunty (+ Doctor_Leevsy) | В старте боя → +50% AP на первый ход |
| `Jazz_Perk_OfficerAura` / `…Influence` | AI-офицеры | Маркеры ауры командира (`AIContextProfiles`) |

**Важно:** HUD-кнопки у Lynx/Buzz/Spider/Colby сейчас ошибочно копируют toggle `Jazz_Perk_00`. Пассив перка при этом может работать; кнопка — нет.

`JAZZ_VovaVist` — полный код атаки есть, **grant-path в UnitData не найден** (кнопка сама себя не выдаёт).

## Заглушки

Остальные `Jazz_Perk_*` у AIM/MERC волны (Allik, Blade, Ira, Miguel, … — **~40** файлов): `unit_reactions = {}`, WIP-текст, нет gameplay-refs в `Code/`. Слот на мерке есть, эффекта в бою нет.

Орфан: `Jazz_Perk_44840` — файл есть, в `items.lua`/`metadata` не зарегистрирован.

## Итог для игрока

Ждите рабочих именных эффектов у **Фрага, Тоски, Рыси, Паука, Колби** (+ Grizzly/Grunty). Остальные ники волны — наёмны и играбельны, но «фирменный» перк пока пустой.
