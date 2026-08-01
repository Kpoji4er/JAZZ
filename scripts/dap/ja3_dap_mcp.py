#!/usr/bin/env python3
"""MCP server: Cursor agent attaches to JA3 SolEngine DAP on :8165.

Usage (MCP stdio — Cursor mcp.json):
  py -3 scripts/dap/ja3_dap_mcp.py

CLI smoke:
  py -3 scripts/dap/ja3_dap_mcp.py --cli probe
  py -3 scripts/dap/ja3_dap_mcp.py --cli connect
  py -3 scripts/dap/ja3_dap_mcp.py --cli status
  py -3 scripts/dap/ja3_dap_mcp.py --cli disconnect
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

# Allow `py ja3_dap_mcp.py` without installing a package
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ja3_dap_client import DEFAULT_HOST, DEFAULT_PORT, DapClient, DapError, probe_port  # noqa: E402


_SESSION: DapClient | None = None


def _session() -> DapClient:
	global _SESSION
	if _SESSION is None or not _SESSION.connected:
		raise DapError(
			"Not connected to JA3 DAP. Start JA3Debug.exe, then call ja3_dap_connect. "
			f"Expected {DEFAULT_HOST}:{DEFAULT_PORT}."
		)
	return _SESSION


def _json(data: Any) -> str:
	return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def build_mcp():
	from mcp.server.mcpserver import MCPServer

	server = MCPServer(
		name="ja3-dap",
		title="JA3 SolEngine DAP",
		instructions=(
			"Debug Jagged Alliance 3 Lua via the engine Debug Adapter Protocol. "
			"Game must run as JA3Debug (Platform.debug) with DAP listening on 127.0.0.1:8165. "
			"Typical flow: ja3_dap_probe → ja3_dap_connect → ja3_dap_set_breakpoints → "
			"reproduce in game → ja3_dap_wait_stopped → ja3_dap_stack / ja3_dap_evaluate → "
			"ja3_dap_continue / step → ja3_dap_disconnect."
		),
	)

	@server.tool(description="Check if JA3 DAP is listening (default 127.0.0.1:8165).")
	def ja3_dap_probe(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> str:
		return _json(probe_port(host, port))

	@server.tool(description="Attach to JA3 DAP server (initialize + attach + configurationDone).")
	def ja3_dap_connect(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, timeout_s: float = 10.0) -> str:
		global _SESSION
		probe = probe_port(host, port)
		if not probe.get("listening"):
			return _json(
				{
					"ok": False,
					"error": "DAP port not listening. Launch JA3Debug.exe (Platform.debug), wait for load, retry.",
					"probe": probe,
				}
			)
		if _SESSION and _SESSION.connected:
			_SESSION.disconnect()
		client = DapClient(host=host, port=port, timeout_s=timeout_s)
		try:
			result = client.connect()
		except Exception as err:
			return _json({"ok": False, "error": str(err), "probe": probe})
		_SESSION = client
		return _json(result)

	@server.tool(description="Disconnect from JA3 DAP. Set terminate_debuggee=true to quit the game.")
	def ja3_dap_disconnect(terminate_debuggee: bool = False) -> str:
		global _SESSION
		if _SESSION is None:
			return _json({"ok": True, "already": True})
		result = _SESSION.disconnect(terminate_debuggee=terminate_debuggee)
		_SESSION = None
		return _json(result)

	@server.tool(description="Session status: connected, last_stopped, pending events.")
	def ja3_dap_status() -> str:
		if _SESSION is None:
			return _json({"connected": False, "hint": "call ja3_dap_connect first"})
		st = _SESSION.status()
		st["events"] = _SESSION.drain_events(clear=False)[-10:]
		return _json(st)

	@server.tool(
		description=(
			"Set breakpoints on an absolute Lua source path (mod Code/*.lua or ModTools/Src/...). "
			"lines: list of 1-based line numbers. Optional conditions map line→Lua expression."
		)
	)
	def ja3_dap_set_breakpoints(path: str, lines: list[int], conditions_json: str = "{}") -> str:
		conds_raw = json.loads(conditions_json or "{}")
		conditions = {int(k): str(v) for k, v in conds_raw.items()}
		abs_path = str(Path(path).resolve()) if path else path
		resp = _session().set_breakpoints(abs_path, list(lines), conditions)
		return _json({"path": abs_path, "response": resp.get("body") or resp})

	@server.tool(description="Clear all breakpoints for a source path.")
	def ja3_dap_clear_breakpoints(path: str) -> str:
		abs_path = str(Path(path).resolve()) if path else path
		resp = _session().clear_breakpoints(abs_path)
		return _json({"path": abs_path, "response": resp.get("body") or resp})

	@server.tool(description="Continue execution after stop.")
	def ja3_dap_continue(thread_id: int | None = None) -> str:
		return _json(_session().continue_(thread_id))

	@server.tool(description="Pause all Lua (manual break).")
	def ja3_dap_pause(thread_id: int | None = None) -> str:
		return _json(_session().pause(thread_id))

	@server.tool(description="Step over.")
	def ja3_dap_step_over(thread_id: int | None = None) -> str:
		return _json(_session().step_over(thread_id))

	@server.tool(description="Step into.")
	def ja3_dap_step_into(thread_id: int | None = None) -> str:
		return _json(_session().step_into(thread_id))

	@server.tool(description="Step out.")
	def ja3_dap_step_out(thread_id: int | None = None) -> str:
		return _json(_session().step_out(thread_id))

	@server.tool(description="Wait until stopped (breakpoint/pause/step/exception).")
	def ja3_dap_wait_stopped(timeout_s: float = 60.0) -> str:
		stopped = _session().wait_stopped(timeout=timeout_s)
		if stopped is None:
			return _json({"stopped": False, "timeout_s": timeout_s})
		return _json({"stopped": True, "body": stopped})

	@server.tool(description="Get call stack for current/last stop.")
	def ja3_dap_stack(thread_id: int | None = None, levels: int = 40) -> str:
		resp = _session().stack_trace(thread_id=thread_id, levels=levels)
		return _json(resp.get("body") or resp)

	@server.tool(description="List scopes for a stack frame id.")
	def ja3_dap_scopes(frame_id: int) -> str:
		resp = _session().scopes(frame_id)
		return _json(resp.get("body") or resp)

	@server.tool(description="List variables for a variablesReference from scopes/variables.")
	def ja3_dap_variables(variables_reference: int) -> str:
		resp = _session().variables(variables_reference)
		return _json(resp.get("body") or resp)

	@server.tool(description="Evaluate a Lua expression in the current debug context (repl/watch).")
	def ja3_dap_evaluate(expression: str, frame_id: int | None = None, context: str = "repl") -> str:
		resp = _session().evaluate(expression, frame_id=frame_id, context=context)
		return _json(resp.get("body") or resp)

	@server.tool(description="Drain recent DAP events (stopped, output, …).")
	def ja3_dap_events(clear: bool = True) -> str:
		return _json(_session().drain_events(clear=clear))

	return server


def _cli(argv: list[str]) -> int:
	parser = argparse.ArgumentParser(description="JA3 DAP CLI")
	parser.add_argument("--cli", required=True, choices=["probe", "connect", "disconnect", "status", "pause"])
	parser.add_argument("--host", default=os.environ.get("JA3_DAP_HOST", DEFAULT_HOST))
	parser.add_argument("--port", type=int, default=int(os.environ.get("JA3_DAP_PORT", DEFAULT_PORT)))
	args = parser.parse_args(argv)

	global _SESSION
	if args.cli == "probe":
		print(_json(probe_port(args.host, args.port)))
		return 0
	if args.cli == "connect":
		probe = probe_port(args.host, args.port)
		if not probe.get("listening"):
			print(_json({"ok": False, "probe": probe}))
			return 2
		client = DapClient(host=args.host, port=args.port)
		print(_json(client.connect()))
		_SESSION = client
		# keep process? for CLI one-shot we disconnect after status print
		print(_json(client.status()))
		client.disconnect()
		_SESSION = None
		return 0
	if args.cli == "status":
		print(_json(probe_port(args.host, args.port)))
		return 0
	if args.cli == "disconnect":
		print(_json({"ok": True, "note": "CLI one-shot has no persistent session"}))
		return 0
	if args.cli == "pause":
		probe = probe_port(args.host, args.port)
		if not probe.get("listening"):
			print(_json({"ok": False, "probe": probe}))
			return 2
		client = DapClient(host=args.host, port=args.port)
		client.connect()
		print(_json(client.pause()))
		stopped = client.wait_stopped(timeout=5.0)
		print(_json({"stopped": stopped}))
		if stopped:
			print(_json(client.stack_trace().get("body")))
		client.disconnect()
		return 0
	return 1


def main() -> None:
	if len(sys.argv) > 1 and sys.argv[1] == "--cli":
		raise SystemExit(_cli(sys.argv[1:]))
	server = build_mcp()
	server.run(transport="stdio")


if __name__ == "__main__":
	main()
