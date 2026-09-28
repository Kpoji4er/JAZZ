# -*- coding: utf-8 -*-
"""Audit the already-open Blender file for custom normals and weld spikes.

  blender --background --factory-startup <file.blend> --python docs/tools/_audit_blender_normals.py
"""
from __future__ import annotations

import json
import argparse
import sys
from pathlib import Path

import bpy

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from _ja3_mesh_prepare import audit_blender_object, mesh_has_custom_normals

FATAL = {"degenerate", "zero_normal", "spike", "nan", "custom_normals", "empty"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mesh-prefix', help='Audit only authored export meshes, excluding unchanged reference bodies')
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    report = {"blend": bpy.data.filepath, "objects": []}
    fatal = 0
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        if args.mesh_prefix and not obj.name.startswith(args.mesh_prefix):
            continue
        issues = audit_blender_object(obj)
        bad = [issue for issue in issues if issue["kind"] in FATAL]
        entry = {
            "name": obj.name,
            "custom_normals": mesh_has_custom_normals(obj.data),
            "issues": len(bad),
            "kinds": {},
            "samples": [str(issue["detail"]) for issue in bad[:5]],
        }
        for issue in bad:
            kind = str(issue["kind"])
            entry["kinds"][kind] = entry["kinds"].get(kind, 0) + 1
        report["objects"].append(entry)
        fatal += len(bad)
    if not report['objects']:
        raise RuntimeError('No matching mesh to audit')
    print("BLEND_NORMALS=" + json.dumps(report, ensure_ascii=True))
    print(f"{'FAIL' if fatal else 'OK'} {Path(bpy.data.filepath).name}: {fatal} fatal issue(s) on {len(report['objects'])} mesh(es)")
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
