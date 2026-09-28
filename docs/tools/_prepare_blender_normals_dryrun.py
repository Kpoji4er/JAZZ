# -*- coding: utf-8 -*-
"""Apply prepare_export_mesh in memory and re-audit. Does not save the blend."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import bpy

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from _ja3_mesh_prepare import audit_blender_object, mesh_has_custom_normals, prepare_export_mesh

FATAL = {"degenerate", "zero_normal", "spike", "nan", "custom_normals", "empty"}


def main() -> int:
    report = {"blend": bpy.data.filepath, "objects": []}
    fatal = 0
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        prepare_export_mesh(obj, strict=False)
        issues = [issue for issue in audit_blender_object(obj) if issue["kind"] in FATAL]
        entry = {
            "name": obj.name,
            "custom_normals": mesh_has_custom_normals(obj.data),
            "issues": len(issues),
            "kinds": {},
            "samples": [str(issue["detail"]) for issue in issues[:5]],
        }
        for issue in issues:
            kind = str(issue["kind"])
            entry["kinds"][kind] = entry["kinds"].get(kind, 0) + 1
        report["objects"].append(entry)
        fatal += len(issues)
    print("PREPARE_DRYRUN=" + json.dumps(report, ensure_ascii=True))
    print(f"{'FAIL' if fatal else 'OK'} {Path(bpy.data.filepath).name} after prepare: {fatal} fatal")
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
