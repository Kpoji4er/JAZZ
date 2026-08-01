# Playbook: runtime-тест JA3 через DAP

Агент тестирует загруженный Lua JAZZ/vanilla **в живом процессе** через Debug Adapter Protocol движка Sol Engine, не только статическим чтением файлов.

## Зачем

- Подтвердить, что код реально вызывается и с какими значениями.
- Поймать ветку бага breakpoint’ом, а не гадать по логам.
- Снять `evaluate` / locals как **runtime evidence** для spec / DoD.

Читы/консоль (`docs/technical/debug.md`) — дополнение; для step/locals/breakpoints — DAP.

## Предусловия

| Требование | Детали |
|---|---|
| Бинарь | **`JA3Debug.exe`** (`Platform.debug`). Retail `JA3.exe` DAP не поднимает. |
| Порт | `127.0.0.1:8165` (`config.DebugAdapterPort`) |
| MCP | сервер `ja3-dap` / `user-ja3-dap` — `.cursor/mcp.json`, код `scripts/dap/` |
| Исходники | breakpoints на файлах, которые игра может смонтировать: мод `Code\`, `ModTools\Src\…` |

Установка IDE (опционально для человека): `ModTools\Src\SolEngineLua.vsix`, launch `.vscode/launch.json`. Агент ходит **напрямую** TCP→DAP через MCP, UI Attach не обязателен.

## Инструменты MCP

| Tool | Назначение |
|---|---|
| `ja3_dap_probe` | Порт слушает? |
| `ja3_dap_connect` | initialize + attach + configurationDone |
| `ja3_dap_set_breakpoints` | absolute path + lines (+ optional conditions_json) |
| `ja3_dap_clear_breakpoints` | снять BP с файла |
| `ja3_dap_wait_stopped` | ждать hit / pause / step |
| `ja3_dap_stack` / `ja3_dap_scopes` / `ja3_dap_variables` | кадр и locals |
| `ja3_dap_evaluate` | Lua expression в debug context |
| `ja3_dap_continue` / `ja3_dap_step_*` / `ja3_dap_pause` | управление |
| `ja3_dap_events` / `ja3_dap_status` | события и состояние сессии |
| `ja3_dap_disconnect` | отсоединиться; `terminate_debuggee` только по просьбе убить игру |

CLI без MCP: `py -3 scripts/dap/ja3_dap_mcp.py --cli probe|connect`.

## Стандартный сценарий агента

```
probe → (если нет порта: Start-Process JA3Debug.exe, ждать listen)
→ connect
→ set_breakpoints(abs_path, lines)
→ [пользователь/агент воспроизводит действие в игре]
→ wait_stopped
→ stack + evaluate (нужные выражения)
→ continue / step по необходимости
→ disconnect (сессия больше не нужна)
```

### Пример breakpoint на код мода

Абсолютный путь, например:

`C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\Code\SatelliteSquad.lua`

Строки — 1-based, на исполняемый код (не пустая/только-комментарий).

### Пример evaluate

После stop: `ja3_dap_evaluate` с выражениями вроде `gv_CurrentSectorId`, `SelectedObj and SelectedObj.session_id`, локальных имён из scopes. Не ожидать полный dump `_G` без нужды.

## Запуск игры агентом

Если порт молчит и пользователь хочет runtime-тест:

1. Проверить, нет ли уже `JA3` / `JA3Debug`.
2. `Start-Process` на `…\Jagged Alliance 3\JA3Debug.exe` (рабочая директория = корень игры).
3. Поллить `ja3_dap_probe` / TCP `:8165` до listen (десятки секунд на cold start).
4. Затем `connect`. Не считать тест проваленным из‑за «ещё грузится» — подождать.

Steam/DRM: если exe сразу падает — сообщить пользователю; не крутить бесконечный relaunch.

## Гигиена сессии

- После pause/breakpoint **обязательно** `continue` или явное «игра оставлена на паузе, сделай X», иначе UI заморожен.
- Не вызывать disconnect с `terminate_debuggee=true`, пока пользователь не просил закрыть игру.
- Одна логическая debug-сессия на MCP-процесс; перед повторным connect при сомнении — disconnect.

## Что писать в evidence / ответ

Кратко и проверяемо:

- бинарь / attach ok;
- `file:line` и reason stop;
- 1–3 ключевых `evaluate` или locals;
- вывод: PASS / FAIL / BLOCKED (например мод не загружен, BP unverified).

Уровень проверки: **runtime**. Static-only не подменяет этот playbook.

## Связанные документы

- `docs/technical/debug.md` — читы, консоль, секция DAP
- `scripts/dap/README.md` — файлы клиента
- `ModTools/Docs/ModItemCode.md.html` — официальный Debugging
- `.cursor/rules/jazz-dap-runtime-debug.mdc` — короткий триггер для агента
