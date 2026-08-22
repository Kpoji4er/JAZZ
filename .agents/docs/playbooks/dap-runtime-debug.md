# Playbook: runtime-тест JA3 через DAP

Агент тестирует загруженный Lua JAZZ/vanilla **в живом процессе** через Debug Adapter Protocol Sol Engine, не только статическим чтением файлов.

Канон для агента — эта страница. Клиент: `scripts/dap/`. MCP: `ja3-dap` (`user-ja3-dap`). Движок: `<JA3_ROOT>/ModTools/Src/CommonLua/Libs/DebugAdapter/DebugAdapter.lua`.

## Зачем

- Подтвердить, что код реально вызывается и с какими значениями.
- Поймать ветку бага breakpoint’ом, а не гадать по логам.
- Снять `evaluate` / locals как **runtime evidence** для spec / DoD.

Читы/консоль (`docs/technical/debug.md`) — дополнение. Для step/locals/breakpoints нужен режим **debugger**. Для чтения живого состояния **без паузы** — режим **live eval**.

## Два режима

| | Debugger | Live eval |
|---|---|---|
| Цель | hit line, step, locals | прочитать/проверить state, пока игра идёт |
| Pause | да, на BP / `ja3_dap_pause` | **нет** — не звать `pause` «чтобы evaluate заработал» |
| Handshake | `initialize` + `attach` + `configurationDone` | движку достаточно одного `evaluate`; **наш MCP пока всегда делает полный handshake** |
| Риск | заморозка UI, если забыть `continue` | assert-диалог из async-потока; truncate 512; порча sync-state при записи |

Выбор:

1. Нужна строка кода / call stack / step → debugger.
2. Нужны `gv_*`, `SelectedObj`, dump таблицы, «мод загружен?» → live eval, игра не на паузе.
3. Не смешивать: не ставить BP и не `pause`, если задача — один probe.

Исторический провал: `ja3_dap_pause` ради evaluate оставлял всю Lua стоять (AITurn «завис», Thor.team exception freeze). Pause только если нужен stopped-context.

## Предусловия

| Требование | Детали |
|---|---|
| Бинарь | **`JA3Debug.exe`** (`Platform.debug`). Retail `JA3.exe` DAP не поднимает. |
| Порт | `127.0.0.1:8165` (`config.DebugAdapterPort`) |
| MCP | `.cursor/mcp.json` → `ja3-dap`; код `scripts/dap/` |
| Исходники BP | абсолютный путь к файлу, который игра монтирует: мод `Code\`, `ModTools\Src\…` |
| CommonLib | JAZZ зависит от `JA3_CommonLib`. `SafeEval*` — в `_Utils.lua` с 1.11-1060 (`6758d82`, 2026-08-22). Steam Workshop может отставать от git `main`. |

IDE для человека (не обязателен агенту): `ModTools\Src\SolEngineLua.vsix`, `.vscode/launch.json` → **Attach to SolEngine (JA3 DAP :8165)**.

Несколько клиентов могут висеть на одном сервере (`DAServer.debuggers` — список). Это не делает `initialize` безопасным (см. ниже).

## Инструменты MCP

| Tool | Назначение |
|---|---|
| `ja3_dap_probe` | Порт слушает? |
| `ja3_dap_connect` | **полный** initialize + attach + configurationDone |
| `ja3_dap_set_breakpoints` | absolute path + lines (+ optional `conditions_json`) |
| `ja3_dap_clear_breakpoints` | снять BP с файла |
| `ja3_dap_wait_stopped` | ждать hit / pause / step |
| `ja3_dap_stack` / `ja3_dap_scopes` / `ja3_dap_variables` | кадр и locals |
| `ja3_dap_evaluate` | Lua **expression** в debug context (сейчас **без** авто-обёртки SafeEval) |
| `ja3_dap_continue` / `ja3_dap_step_*` / `ja3_dap_pause` | управление |
| `ja3_dap_events` / `ja3_dap_status` | события и состояние сессии |
| `ja3_dap_disconnect` | закрыть сессию; `terminate_debuggee` только по просьбе убить игру |

CLI без MCP: `py -3 scripts/dap/ja3_dap_mcp.py --cli probe|connect`.

Клиент держит **одно** TCP-соединение на MCP-процесс. Не connect/disconnect на каждый probe — адаптер логирует каждую пару в консоль игры.

## Что делает наш клиент vs что умеет движок

`scripts/dap/ja3_dap_client.py` при `connect` всегда шлёт `initialize`. Handler в JA3:

- `DebuggerInit()` + **`DebuggerClearBreakpoints()`** — сносит **все** BP, в том числе IDE;
- `configurationDone` вызывает `Continue()` — снимает чужой stop.

`EvaluateExpression` без `frameId` не читает состояние сокета: `load("return " .. expr)` в `GetRawG()` (`_G` через rawget/rawset). Handshake для eval **не нужен**. Live-eval-only сокет (один `evaluate`, без `initialize`) в нашем MCP **ещё не выделен**.

Следствие: **не** `ja3_dap_connect`, пока пользователь отлаживается в Cursor/VS Code, если он не согласен потерять BP и получить `Continue`. Если сессия MCP уже есть — повторный connect не делать.

`disconnect` без `terminateDebuggee` игру не гасит (`quit` только при флаге). Предпочитать закрыть сокет / `terminate_debuggee=false`. Не слать `disconnect` в чужую IDE-сессию.

## Сценарий debugger

```
probe → (нет порта: Start-Process JA3Debug.exe, ждать listen)
→ connect          -- только если IDE не держит debug-сессию
→ set_breakpoints(abs_path, lines)
→ воспроизвести действие
→ wait_stopped
→ stack + evaluate (locals / узкие выражения)
→ continue / step
→ disconnect, когда сессия больше не нужна
```

Breakpoint: абсолютный путь на машине, строки 1-based, на исполняемый код. Пример: `<JA3_USERDATA>/Mods/jazz/Code/SatelliteSquad.lua` (`JA3_USERDATA` = `%APPDATA%/Jagged Alliance 3`).

После stop evaluate без SafeEval-обёртки допустим: поток уже в debug break, нужен кадр (`frame_id`). Не ждать полный dump `_G`.

## Сценарий live eval

```
probe → connect     -- если MCP ещё не подключён и IDE не в debug
→ ja3_dap_evaluate(обёрнутое expression)
→ при необходимости ещё evaluate на том же соединении
→ disconnect не обязателен до конца работы с игрой
```

Не `pause`. Не BP. Не step.

### Обязательная обёртка evaluate

`ja3_dap_evaluate` сейчас шлёт expression как есть. Для live eval агент **сам** оборачивает.

Контракт CommonLib (не версия из сторонних agent-instructions):

- `SafeEvalStart(reason)` → прежний `IgnoreDebugErrors`, внутри `SuspendDesyncErrors`
- `SafeEvalEnd(ignore_errors, reason)` → restore
- `SafeEval(func, ...)` → `true, ...` / `false, tostring(err)` — **не** старая пара `err, result`

Для DAP не звать `SafeEval(func)`: нужна строка наружу и spill длинного результата. Использовать Start/End вокруг `pcall`.

Канон (clib загружен):

```lua
(function()
	local ign = SafeEvalStart("jazz-dap")
	local ok, res = pcall(function()
		return <EXPR>
	end)
	SafeEvalEnd(ign, "jazz-dap")
	if not ok then return "LUA ERROR: " .. tostring(res) end
	if res == nil then return "(nil)" end
	if type(res) ~= "string" then res = tostring(res) end
	if #res <= 400 then return res end
	local err = AsyncStringToFile([[AppData/jazz_dap_eval.txt]], res)
	return err and ("FILE ERROR: " .. tostring(err)) or "@@FILE@@"
end)()
```

Если `SafeEvalStart` нет (старый Workshop clib): те же `IgnoreDebugErrors(true)` + `SuspendDesyncErrors("jazz-dap")` / `ResumeDesyncErrors` + restore ignore.

Statements: тело `pcall` — `function() <stmts>; return ... end`, не сырой `if ... end` (движок делает `load("return " .. expression)`).

Прочитать spill: `%APPDATA%\Jagged Alliance 3\jazz_dap_eval.txt`. В ответе DAP строка `@@FILE@@` значит «читай файл», не «пустой результат».

Хвост `{ metatable = table:` — это dump watch-entries адаптера, не часть значения; обрезать до него.

## Контракт expression

| Ограничение | Следствие |
|---|---|
| Только expression | statements → syntax error; wrap IIFE |
| Наружу только return | `print` / `Inspect` идут в лог игры, MCP их не видит |
| Env = `GetRawG()` (`_G`) | классы `DefineClass` видны; имена только в mod env — `Mods.e6L4ECj.env.<name>` (id пакета `jazz`). `__newindex` идёт через `rawset` — assert «new global» **не** ловит запись из eval |
| Чёрный список mod env не действует | `AsyncStringToFile` из `_G` **можно** |
| `Debugger_ToString` режет **512** (`config.MaxWatchLenValue`) | поднять лимит внутри expression бесполезно: stringify **после** return. Длинное — файл |
| Поток адаптера = real-time / `IsAsyncCode()` | sync-only код → **модальный assert**, не Lua error; `pcall` не ловит. Без SafeEval/IgnoreDebugErrors агент клинит на диалоге |
| Ошибка **внутри handler’а** адаптера | ответа нет, MCP timeout; смотреть лог игры |
| C-функция `return 0` (ноль значений) | не `nil`; `tostring()` → *value expected*. Диагностика: ранний выход на C. Писать `select("#", ...) == 0` |

Типичные probe:

```lua
gv_CurrentSectorId
SelectedObj and SelectedObj.session_id
type(SafeEvalStart)
Mods.e6L4ECj and true
```

Сборки: таблица строк → `table.concat` → один return. Не сериализовать огромные `_G`.

## Запись состояния

Читать из eval-потока можно. **Писать sync game state нельзя** (`SetCommand`, инвентарь пачкой, `CheatAddMercIG` на всех мерков сразу — уже валило процесс).

Мутации: `CreateGameTimeThread(function() ... end)` и `return "scheduled"`. Поток **не** бежит при паузе: если `GetTimeFactor() == 0`, «ничего не произошло» — не баг мутации.

`ReloadLua`: только `CreateRealTimeThread(ReloadLua)` (не из самого eval-потока). После reload одноразовые `Msg("DataLoaded")` / часть `OnMsg` не повторятся; ждать `const.LuaReloads`. См. `.agents/docs/reference/runtime-model.md`.

## Запуск игры агентом

Если порт молчит и нужен runtime-тест:

1. Нет ли уже `JA3` / `JA3Debug`.
2. `Start-Process` на `…\Jagged Alliance 3\JA3Debug.exe` (cwd = корень игры).
3. Поллить `ja3_dap_probe` до listen (десятки секунд на cold start).
4. Затем connect. «Ещё грузится» — не FAIL.

Steam/DRM: exe сразу умер — сказать пользователю, не крутить relaunch.

## Гигиена сессии

- После BP/pause — `continue` или явно «игра на паузе, сделай X».
- `terminate_debuggee=true` только если просили закрыть игру.
- Одна логическая сессия на MCP-процесс.
- Не оставлять BP на горячем боевом коде после теста (`clear_breakpoints`).
- Ошибка в handler → timeout; не спамить evaluate, сначала лог `%APPDATA%\Jagged Alliance 3\logs\`.

## Evidence

- бинарь / probe+attach ok;
- режим: debugger (`file:line`, reason) или live eval (expression + result);
- 1–3 ключевых значения; для spill — путь файла;
- PASS / FAIL / BLOCKED (мод не загружен, BP unverified, timeout, assert dialog).

Уровень: **runtime**. Static-only этот playbook не подменяет.

## Не делать

- DAP на goldmaster/retail без `JA3Debug`.
- `initialize` поверх чужой IDE-сессии.
- `pause` для «просто посмотреть переменную».
- Сырой live eval без SafeEval/IgnoreDebugErrors, если код может быть sync-only.
- Путать `SafeEval` из zip/SAD-инструкций (`err, result`) с clib (`ok, ...`).
- Путать Lua DAP с OllyDbg `odbg64`.
- Массовые читы одним evaluate в async-потоке.

## Связанные документы

- `docs/technical/debug.md` — читы, консоль, краткий указатель DAP
- `scripts/dap/README.md` — файлы клиента
- `.cursor/rules/jazz-dap-runtime-debug.mdc` — короткий триггер
- `.agents/skills/jazz-lua-globals/SKILL.md` — обычные runtime-глобалы (eval идёт через `rawset`)
- `ModTools/Docs/ModItemCode.md.html` — официальный Debugging
- CommonLib: `Code/_Utils.lua` → `SafeEvalStart` / `SafeEvalEnd` / `SafeEval`
