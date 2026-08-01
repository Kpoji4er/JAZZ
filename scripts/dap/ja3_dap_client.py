"""Minimal DAP client for JA3 / Sol Engine DebugAdapter (TCP :8165).

The game hosts the DAP server (CommonLua/Libs/DebugAdapter). This module is the client.
Default: host=127.0.0.1, port=8165 (config.DebugAdapterPort).
Requires Platform.debug (typically JA3Debug.exe).
"""

from __future__ import annotations

import json
import socket
import threading
import time
from dataclasses import dataclass, field
from typing import Any


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8165


class DapError(RuntimeError):
	pass


@dataclass
class DapClient:
	host: str = DEFAULT_HOST
	port: int = DEFAULT_PORT
	timeout_s: float = 10.0

	_sock: socket.socket | None = field(default=None, repr=False)
	_seq: int = 0
	_buf: bytes = field(default=b"", repr=False)
	_lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
	_reader: threading.Thread | None = field(default=None, repr=False)
	_stop: threading.Event = field(default_factory=threading.Event, repr=False)
	_pending: dict[int, dict[str, Any]] = field(default_factory=dict, repr=False)
	_events: list[dict[str, Any]] = field(default_factory=list, repr=False)
	_cv: threading.Condition = field(default_factory=threading.Condition, repr=False)
	initialized: bool = False
	last_stopped: dict[str, Any] | None = None
	capabilities: dict[str, Any] | None = None

	@property
	def connected(self) -> bool:
		return self._sock is not None

	def connect(self, wait_initialized: bool = True) -> dict[str, Any]:
		if self._sock is not None:
			return {"ok": True, "already": True, "capabilities": self.capabilities}

		sock = socket.create_connection((self.host, self.port), timeout=self.timeout_s)
		sock.settimeout(0.25)
		self._sock = sock
		self._stop.clear()
		self._reader = threading.Thread(target=self._read_loop, name="ja3-dap-reader", daemon=True)
		self._reader.start()

		init = self.request(
			"initialize",
			{
				"clientID": "jazz-agent",
				"clientName": "JAZZ Cursor Agent",
				"adapterID": "solengine",
				"pathFormat": "path",
				"linesStartAt1": True,
				"columnsStartAt1": True,
				"supportsVariableType": True,
				"supportsVariablePaging": False,
				"supportsRunInTerminalRequest": False,
			},
		)
		if not init.get("success", True) and init.get("success") is False:
			raise DapError(init.get("message") or "initialize failed")
		self.capabilities = init.get("body") or {}
		self._wait_event("initialized", timeout=self.timeout_s)

		# attach + configurationDone — same order VS Code uses with debugServer
		self.request("attach", {})
		self.request("configurationDone", {})
		self.initialized = True
		return {
			"ok": True,
			"host": self.host,
			"port": self.port,
			"capabilities": self.capabilities,
		}

	def disconnect(self, terminate_debuggee: bool = False) -> dict[str, Any]:
		try:
			if self._sock is not None:
				try:
					self.request(
						"disconnect",
						{
							"restart": False,
							"terminateDebuggee": bool(terminate_debuggee),
						},
						wait=False,
					)
					time.sleep(0.05)
				except Exception:
					pass
		finally:
			self._close()
		return {"ok": True, "disconnected": True}

	def status(self) -> dict[str, Any]:
		return {
			"connected": self.connected,
			"initialized": self.initialized,
			"host": self.host,
			"port": self.port,
			"pending_events": len(self._events),
			"last_stopped": self.last_stopped,
		}

	def set_breakpoints(
		self,
		path: str,
		lines: list[int],
		conditions: dict[int, str] | None = None,
	) -> dict[str, Any]:
		conditions = conditions or {}
		bps = []
		for line in lines:
			bp: dict[str, Any] = {"line": int(line)}
			cond = conditions.get(int(line))
			if cond:
				bp["condition"] = cond
			bps.append(bp)
		return self.request(
			"setBreakpoints",
			{
				"source": {"path": path},
				"breakpoints": bps,
			},
		)

	def clear_breakpoints(self, path: str) -> dict[str, Any]:
		return self.set_breakpoints(path, [])

	def continue_(self, thread_id: int | None = None) -> dict[str, Any]:
		args: dict[str, Any] = {}
		if thread_id is not None:
			args["threadId"] = thread_id
		self.last_stopped = None
		return self.request("continue", args)

	def pause(self, thread_id: int | None = None) -> dict[str, Any]:
		args: dict[str, Any] = {}
		if thread_id is not None:
			args["threadId"] = thread_id
		return self.request("pause", args)

	def step_over(self, thread_id: int | None = None) -> dict[str, Any]:
		return self._step("next", thread_id)

	def step_into(self, thread_id: int | None = None) -> dict[str, Any]:
		return self._step("stepIn", thread_id)

	def step_out(self, thread_id: int | None = None) -> dict[str, Any]:
		return self._step("stepOut", thread_id)

	def threads(self) -> dict[str, Any]:
		return self.request("threads", {})

	def stack_trace(self, thread_id: int | None = None, levels: int = 40) -> dict[str, Any]:
		tid = thread_id
		if tid is None and self.last_stopped:
			tid = self.last_stopped.get("threadId")
		if tid is None:
			# Global thread id used by SolEngine (see DebugAdapter Request_threads)
			tid = 200000001
		return self.request(
			"stackTrace",
			{"threadId": tid, "startFrame": 0, "levels": levels},
		)

	def scopes(self, frame_id: int) -> dict[str, Any]:
		return self.request("scopes", {"frameId": frame_id})

	def variables(self, variables_reference: int) -> dict[str, Any]:
		return self.request("variables", {"variablesReference": variables_reference})

	def evaluate(self, expression: str, frame_id: int | None = None, context: str = "repl") -> dict[str, Any]:
		args: dict[str, Any] = {"expression": expression, "context": context}
		if frame_id is not None:
			args["frameId"] = frame_id
		return self.request("evaluate", args)

	def drain_events(self, clear: bool = True) -> list[dict[str, Any]]:
		with self._cv:
			events = list(self._events)
			if clear:
				self._events.clear()
			return events

	def wait_stopped(self, timeout: float | None = None) -> dict[str, Any] | None:
		deadline = time.time() + (timeout if timeout is not None else self.timeout_s)
		with self._cv:
			while True:
				if self.last_stopped is not None:
					return self.last_stopped
				remaining = deadline - time.time()
				if remaining <= 0:
					return None
				self._cv.wait(timeout=remaining)

	def request(self, command: str, arguments: dict[str, Any] | None = None, wait: bool = True) -> dict[str, Any]:
		if self._sock is None:
			raise DapError("not connected")
		with self._lock:
			self._seq += 1
			seq = self._seq
			msg = {
				"seq": seq,
				"type": "request",
				"command": command,
			}
			if arguments is not None:
				msg["arguments"] = arguments
			self._send(msg)
			if not wait:
				return {"ok": True, "seq": seq, "command": command}

		deadline = time.time() + self.timeout_s
		with self._cv:
			while seq not in self._pending:
				remaining = deadline - time.time()
				if remaining <= 0:
					raise DapError(f"timeout waiting for response to {command} (seq={seq})")
				self._cv.wait(timeout=remaining)
			resp = self._pending.pop(seq)
		if resp.get("success") is False:
			raise DapError(resp.get("message") or f"{command} failed")
		return resp

	def _step(self, command: str, thread_id: int | None) -> dict[str, Any]:
		args: dict[str, Any] = {}
		if thread_id is not None:
			args["threadId"] = thread_id
		elif self.last_stopped and self.last_stopped.get("threadId") is not None:
			args["threadId"] = self.last_stopped["threadId"]
		self.last_stopped = None
		return self.request(command, args)

	def _send(self, message: dict[str, Any]) -> None:
		assert self._sock is not None
		body = json.dumps(message, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
		header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
		self._sock.sendall(header + body)

	def _read_loop(self) -> None:
		sock = self._sock
		if sock is None:
			return
		try:
			while not self._stop.is_set():
				try:
					chunk = sock.recv(65536)
				except socket.timeout:
					continue
				except OSError:
					break
				if not chunk:
					break
				self._buf += chunk
				while True:
					msg = self._pop_message()
					if msg is None:
						break
					self._on_message(msg)
		finally:
			self._close()

	def _pop_message(self) -> dict[str, Any] | None:
		sep = self._buf.find(b"\r\n\r\n")
		if sep < 0:
			return None
		header = self._buf[:sep].decode("ascii", errors="replace")
		length = None
		for line in header.split("\r\n"):
			if line.lower().startswith("content-length:"):
				length = int(line.split(":", 1)[1].strip())
				break
		if length is None:
			raise DapError(f"missing Content-Length: {header!r}")
		start = sep + 4
		end = start + length
		if len(self._buf) < end:
			return None
		body = self._buf[start:end]
		self._buf = self._buf[end:]
		return json.loads(body.decode("utf-8"))

	def _on_message(self, msg: dict[str, Any]) -> None:
		with self._cv:
			mtype = msg.get("type")
			if mtype == "response":
				req_seq = msg.get("request_seq")
				if isinstance(req_seq, int):
					self._pending[req_seq] = msg
					self._cv.notify_all()
			elif mtype == "event":
				self._events.append(msg)
				if msg.get("event") == "stopped":
					self.last_stopped = msg.get("body") or {}
				self._cv.notify_all()
			else:
				self._events.append(msg)
				self._cv.notify_all()

	def _wait_event(self, name: str, timeout: float) -> dict[str, Any]:
		deadline = time.time() + timeout
		with self._cv:
			while True:
				for ev in self._events:
					if ev.get("type") == "event" and ev.get("event") == name:
						return ev
				remaining = deadline - time.time()
				if remaining <= 0:
					raise DapError(f"timeout waiting for event {name}")
				self._cv.wait(timeout=remaining)

	def _close(self) -> None:
		self._stop.set()
		sock = self._sock
		self._sock = None
		self.initialized = False
		if sock is not None:
			try:
				sock.close()
			except OSError:
				pass
		with self._cv:
			self._cv.notify_all()


def probe_port(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, timeout: float = 1.0) -> dict[str, Any]:
	try:
		with socket.create_connection((host, port), timeout=timeout):
			return {"listening": True, "host": host, "port": port}
	except OSError as err:
		return {"listening": False, "host": host, "port": port, "error": str(err)}
