#!/usr/bin/env python3
"""Summarize JA3 log error/warning clusters (load lag / popup storms)."""
from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

ASSIGN_ID = re.compile(r"Assigning window id '([^']+)'")
LUA_ERR = re.compile(r"\[LUA ERROR\]\s*(.*)")
MISSING_IMG = re.compile(r"Once only:\s*Missing (?:image|entity|sound)[^\n]*", re.I)


def classify(line: str) -> str | None:
	if "[LUA ERROR]" in line:
		m = LUA_ERR.search(line)
		msg = (m.group(1) if m else line)[:160]
		msg = re.sub(r"\s+", " ", msg)
		return "LUA ERROR: " + msg
	if "[UI WARNING]" in line:
		m = ASSIGN_ID.search(line)
		if m:
			return "UI WARNING id=" + m.group(1)
		return "UI WARNING: " + line[line.find("[UI WARNING]") :][:120]
	if "Attempt to create a new global" in line:
		return "NEW GLOBAL: " + line.strip()[-80:]
	if "Call stack too big" in line:
		return "STACK OVERFLOW"
	if "Failed to load mod items" in line:
		return "FAILED ITEMS: " + line.strip()[-120:]
	if "Once only:" in line and "Missing" in line:
		return "MISSING: " + line.split("Once only:", 1)[-1].strip()[:140]
	if "[ERROR]" in line:
		return "ERROR: " + line.strip()[:140]
	return None


def main() -> int:
	ap = argparse.ArgumentParser()
	ap.add_argument("log", nargs="?", default="")
	args = ap.parse_args()
	log_dir = Path.home() / "AppData/Roaming/Jagged Alliance 3/logs"
	if args.log:
		path = Path(args.log)
	else:
		cands = sorted(log_dir.glob("JA3.exe-*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
		if not cands:
			print("no logs")
			return 1
		path = cands[0]
	text = path.read_text(encoding="utf-8", errors="replace")
	lines = text.splitlines()
	print(f"log: {path}")
	print(f"lines: {len(lines)}  bytes: {path.stat().st_size}")
	keys = Counter()
	samples: dict[str, list[tuple[int, str]]] = defaultdict(list)
	for i, line in enumerate(lines, 1):
		tag = classify(line)
		if not tag:
			continue
		keys[tag] += 1
		if len(samples[tag]) < 2:
			samples[tag].append((i, line[:240]))
	print("\n=== COUNTS ===")
	for k, v in keys.most_common(50):
		print(f"{v:6d}  {k}")
	print("\n=== SAMPLES ===")
	for k, _ in keys.most_common(20):
		print("---", k)
		for ln, s in samples[k]:
			print(f"  L{ln}: {s}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
