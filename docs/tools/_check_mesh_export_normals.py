# -*- coding: utf-8 -*-
"""FAIL export scripts that keep custom normals, and scan OBJ/HGM JSON for weld spikes.

Successful exporter output is not a PASS. Run from jazz/:

  python docs/tools/_check_mesh_export_normals.py
  python docs/tools/_check_mesh_export_normals.py --scan-dir <build-or-OBJ>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _ja3_mesh_prepare import audit_hgm_json, audit_triangles, parse_obj

KEEP_CUSTOM = re.compile(r"keep_custom_normals\s*=\s*True")
SKIP_PY = {
    "_check_mesh_export_normals.py",
}
FATAL_KINDS = {"degenerate", "zero_normal", "spike", "nan", "custom_normals", "empty"}


def scan_scripts(tools_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(tools_dir.glob("*.py")):
        if path.name in SKIP_PY:
            continue
        text = path.read_text(encoding="utf-8")
        if KEEP_CUSTOM.search(text):
            errors.append(f"{path.name}: keep_custom_normals assigned True (never keep custom normals)")
    return errors


def scan_file(path: Path) -> list[str]:
    errors: list[str] = []
    suffix = path.suffix.lower()
    try:
        if suffix == ".obj":
            verts, faces = parse_obj(path.read_text(encoding="utf-8", errors="replace"))
            issues = audit_triangles(verts, faces, name=path.name)
        elif suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return []
            if "meshes" in data:
                issues = audit_hgm_json(data, name=path.name)
            elif "vertices" in data and "faces" in data:
                issues = audit_triangles(data["vertices"], data["faces"], name=path.name)
            else:
                return []
        else:
            return []
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"{path}: read failed: {exc}"]
    for issue in issues:
        if issue["kind"] in FATAL_KINDS:
            errors.append(f"{path}: {issue['detail']}")
    return errors


def scan_dir(root: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".obj", ".json"}:
            errors.extend(scan_file(path))
    return errors


def _issue_path(err: str) -> str:
    if len(err) >= 3 and err[1] == ":" and err[0].isalpha():
        rest = err[2:]
        cut = rest.find(":")
        return err if cut < 0 else err[: 2 + cut]
    cut = err.find(":")
    return err if cut < 0 else err[:cut]


def _issue_kind(err: str) -> str:
    if "keep_custom_normals" in err:
        return "keep_custom"
    if "weld-spike" in err:
        return "spike"
    if "zero-length normal" in err:
        return "zero_normal"
    if "area=" in err or "degenerate" in err:
        return "degenerate"
    if "non-finite" in err:
        return "nan"
    if "custom/split" in err:
        return "custom_normals"
    if "no geometry" in err or "no meshes" in err:
        return "empty"
    return "other"


def summarize(errors: list[str]) -> list[str]:
    files: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for err in errors:
        if err.startswith("--scan-dir") or err.startswith("self-check"):
            continue
        files[_issue_path(err)] = files.get(_issue_path(err), 0) + 1
        kind = _issue_kind(err)
        kinds[kind] = kinds.get(kind, 0) + 1
    lines = [f"summary: {len(errors)} issue(s) in {len(files)} path(s)"]
    for kind, count in sorted(kinds.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"  {kind}: {count}")
    for path, count in sorted(files.items(), key=lambda item: (-item[1], item[0]))[:20]:
        lines.append(f"  {count}  {path}")
    return lines


def self_check() -> list[str]:
    """Synthetic needle: a weld to a far stray vertex must FAIL."""
    verts = [(0.0, 0.0, 0.0), (0.01, 0.0, 0.0), (0.0, 0.01, 0.0), (50.0, 0.0, 0.0)]
    good = audit_triangles(verts[:3], [(0, 1, 2)], name="ok")
    spike = audit_triangles(verts, [(0, 1, 3)], name="spike")
    errors: list[str] = []
    if any(issue["kind"] in FATAL_KINDS for issue in good):
        errors.append("self-check: clean triangle was rejected")
    if not any(issue["kind"] == "spike" for issue in spike):
        errors.append("self-check: weld-spike triangle was not rejected")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tools", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--scan-dir", type=Path, action="append", default=[])
    parser.add_argument("--summary", action="store_true", help="print counts, not every face")
    parser.add_argument("--max-print", type=int, default=80)
    args = parser.parse_args()
    errors = self_check()
    errors.extend(scan_scripts(args.tools))
    for folder in args.scan_dir:
        if not folder.is_dir():
            errors.append(f"--scan-dir missing: {folder}")
            continue
        errors.extend(scan_dir(folder))
    if errors:
        if args.summary:
            for line in summarize(errors):
                print(f"FAIL {line}")
        else:
            for err in errors[: max(args.max_print, 0)]:
                print(f"FAIL {err}")
            if len(errors) > args.max_print:
                print(f"FAIL ... {len(errors) - args.max_print} more")
        print(f"FAIL {len(errors)} mesh-normal issue(s)")
        return 1
    extra = f"; scanned {len(args.scan_dir)} dir(s)" if args.scan_dir else ""
    print(f"OK recalc-only normals; no keep-custom-normals in {args.tools.name}{extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
