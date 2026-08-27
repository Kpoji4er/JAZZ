---
name: jazz-lua-globals
description: Правильно объявлять и писать Lua-глобалы JAZZ/JA3 без Assert «Attempt to create a new global». Использовать при rawset/_G, g_JAZZ_*, wrapper flags, OnMsg install, GameVar/MapVar, или любом runtime-присвоении нового имени в _G (jazz, jazz-nomaps, jazz-units, jazz-maps).
---

# JA3 / JAZZ: глобалы без Assert

Движок в runtime запрещает **создавать** новые ключи в `_G` обычным присвоением. Типичный assert:

```text
Attempt to create a new global 'g_JAZZ_NoMapsGenerateEnemySquadWrapped'
```

Часто срабатывает из `OnMsg.ModsReloaded` / `NewGame` / `LoadGame` / закрытия Mod Manager — не только «в бою».

## Правила

### 1. File-load vs runtime

| Когда | Можно ли `Name = value` в `_G`? |
| --- | --- |
| Загрузка mod `Code/*.lua` (top-level файла) | Да — имена регистрируются |
| Позже (`OnMsg.*`, handlers, delayed) | **Нет** для *нового* имени |

### 2. Как заводить флаги / base-функции обёрток

**Обязательно** объявить на top-level файла (как в `jazz/Code/Guardpost_Patrols.lua`):

```lua
g_JAZZ_FooWrapped = rawget(_G, "g_JAZZ_FooWrapped") or false
g_JAZZ_FooBase = rawget(_G, "g_JAZZ_FooBase") or false
```

`rawget` нужен, чтобы Lua reload не затирал уже установленный base.

В install-функции писать через `rawset` (безопасно при любом lifecycle):

```lua
local function lInstallFooWrapper()
	if rawget(_G, "g_JAZZ_FooWrapped") then
		return
	end
	local base = rawget(_G, "SomeEngineFunc")
	if type(base) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_FooBase", base)
	rawset(_G, "g_JAZZ_FooWrapped", true)
	function SomeEngineFunc(...)
		-- ...
		return g_JAZZ_FooBase(...)
	end
end
```

**Нельзя** в runtime:

```lua
g_JAZZ_FooWrapped = true  -- если имени ещё не было в _G → Assert
```

даже если рядом стоит `rawget` check — check не создаёт ключ.

DAP `evaluate` ходит в `GetRawG()`: `__newindex` делает `rawset(_G, …)` и **не** ловит этот assert. Это не повод плодить глобалы из probe; для кода мода по-прежнему top-level + `rawset`. Контракт eval: `.agents/docs/playbooks/dap-runtime-debug.md`.

### 3. Предпочитать local upvalue

Если флаг/base нужны только внутри одного файла и **не** должны переживать reload как отдельный контракт — `local wrapped = false` / `local base = false`. Не плодить `_G`.

Globals нужны когда: detect wrap после ReloadLua, доступ из другого файла, или engine callback смотрит `_G`.

### 4. GameVar / MapVar

- Состояние кампании/карты — `GameVar("gv_…", factory)` / `MapVar("g_…", default)`.
- Не присваивать `nil` в GameVar/MapVar.
- Не путать с одноразовыми wrap-флагами (те — top-level `false` + `rawset`).

### 5. SetQuestVar рано в NewGame

`SetQuestVar` гоняет `QuestTCEEvaluation`. Пока `Groups` ещё boolean (early `ZuluNewGame`), будет:

```text
attempt to index a boolean value (global 'Groups')
```

Если значение нужно только для `rawget` loot conditions — `rawset(quest, var_id, value)` пока `type(Groups) ~= "table"`. Пример: `jazz-nomaps` `lQuestVarSafeSet`, `LegionTierProgression` `lSetTier`.

### 6. Переопределение существующих engine globals

`function GenerateEnemySquad(...)` / `CreateUnitData = function...` — OK, если символ **уже** существует. Сначала `rawget` + type check. Новый public API (`function JAZZ_Foo()`) объявлять на top-level файла.

## 7. Чтение возможно отсутствующих engine globals

Assert также бывает:

```text
Attempt to use an undefined global 'Team'
```

**Любое** bare-имя (`Team`, `g_Units`, `Groups`, …) при отсутствии ключа в `_G` → Assert, не только запись. На `ModsReloaded` класс `Team` ещё может не существовать.

```lua
-- BAD
if type(Team) ~= "table" then return end
function Team:IsEnemySide(other) ... end

-- GOOD
local team_class = rawget(_G, "Team")
if type(team_class) ~= "table" then return end
local base = team_class.IsEnemySide
if type(base) ~= "function" then return end
team_class.IsEnemySide = function(self, other)
	return base(self, other)
end
```

То же для `g_Units` / `gv_UnitData` в ранних handlers: `local u = rawget(_G, "g_Units")`.

## Чеклист перед commit

- [ ] Все `g_JAZZ_*` / wrap flags, которые пишутся из `OnMsg`, есть на top-level как `= false` (или `rawget or false`).
- [ ] Runtime-записи в `_G` новых/перезаписываемых служебных ключей — через `rawset(_G, "Name", value)`.
- [ ] Нет первого присвоения `NewName = …` внутри `OnMsg` / local function без предварительного top-level.
- [ ] Нет bare-read engine globals, которые могут отсутствовать на reload (`Team`, …) — только `rawget(_G, …)`.
- [ ] Early NewGame не зовёт `SetQuestVar`, если нужен только raw value для loot.
- [ ] После фикса NoMaps: закрытие Mod Manager + NewGame без Assert; `JAZZ_LegionAIPrintEconomy()` → HQ=`A20` (не `B28`).

## Не путать с wrap-циклом

Второй wrap на тот же метод + re-base → `Call stack too big`, не assert «new global». Канон: `.cursor/rules/jazz-lua-wrap-no-cycle.mdc`. Проверка: `python docs/tools/_check_lua_wrap_cycles.py`.

## Канон в репо

- Wrap flags: `jazz/Code/Guardpost_Patrols.lua` (top-level init).
- `rawset(_G, …)`: `jazz/Code/System_WeaponRemovableModify.lua`.
- NoMaps wrappers + safe quest set: `jazz-nomaps/Code/NoMaps_Autonomy.lua`.

## Антипаттерн (уже ломало NoMaps)

```lua
-- BAD: first touch in OnMsg.ModsReloaded / bootstrap
g_JAZZ_NoMapsGenerateEnemySquadWrapped = true
JAZZ_NoMaps_CreateUnitDataWrapped = true
```

Следствие: bootstrap обрывается → Major HQ остаётся `B28`, auto-regions/mainland AI не поднимаются, «глобалка не живёт».
