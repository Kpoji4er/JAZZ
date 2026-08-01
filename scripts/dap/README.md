# JA3 DAP (agent + IDE)

Sol Engine hosts a Debug Adapter Protocol server on `127.0.0.1:8165` when `Platform.debug` is set (use `JA3Debug.exe`).

## Agent (Cursor MCP)

Project MCP: `.cursor/mcp.json` → server `ja3-dap`.

Flow:
1. Start `JA3Debug.exe` and load into game/editor.
2. Agent: `ja3_dap_probe` → `ja3_dap_connect`.
3. `ja3_dap_set_breakpoints` on absolute `Code\\….lua` paths.
4. Reproduce → `ja3_dap_wait_stopped` → `ja3_dap_stack` / `ja3_dap_evaluate`.
5. `ja3_dap_disconnect` when done.

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
