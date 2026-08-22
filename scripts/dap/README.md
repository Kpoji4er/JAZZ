# JA3 DAP (agent + IDE)

Sol Engine hosts a Debug Adapter Protocol server on `127.0.0.1:8165` when `Platform.debug` is set (use `JA3Debug.exe`).

Agent playbook (modes, SafeEval wrap, truncation, do-nots): `.agents/docs/playbooks/dap-runtime-debug.md`.

## Agent (Cursor MCP)

Project MCP: `.cursor/mcp.json` → server `ja3-dap`.

- `ja3_dap_client.py` — TCP client (initialize / attach / eval / breakpoints).
- `ja3_dap_mcp.py` — MCP + CLI.

`connect` always sends `initialize`. In JA3 that calls `DebuggerClearBreakpoints()` and `configurationDone` resumes. Do not attach over a live IDE debug session.

`evaluate` is a raw DAP `evaluate` (expression only, env `_G`). The MCP does **not** wrap `SafeEvalStart`/`SafeEvalEnd`; the agent must, for live probes. Results longer than `config.MaxWatchLenValue` (512) are truncated by `Debugger_ToString` after return.

CLI smoke (no MCP):

```powershell
py -3 scripts/dap/ja3_dap_mcp.py --cli probe
py -3 scripts/dap/ja3_dap_mcp.py --cli connect
```

## Human (Cursor Run and Debug)

1. Extension `SolEngineLua.vsix` from `ModTools\\Src` (already installable via Cursor).
2. Launch config: `.vscode/launch.json` → **Attach to SolEngine (JA3 DAP :8165)**.
3. Same requirement: `JA3Debug.exe` running.

Official docs: `ModTools/Docs/ModItemCode.md.html` (Debugging).
