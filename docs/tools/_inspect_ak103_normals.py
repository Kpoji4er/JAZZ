"""Count split verts and custom normals on the archive AK-103."""

import json
import sys
from pathlib import Path

import bpy

bpy.ops.wm.open_mainfile(filepath=sys.argv[sys.argv.index("--") + 1])
report = {}
for obj in bpy.data.objects:
    if obj.type != "MESH" or not obj.name.startswith("AK103"):
        continue
    mesh = obj.data
    uniq = { (round(v.co.x, 6), round(v.co.y, 6), round(v.co.z, 6)) for v in mesh.vertices }
    report[obj.name] = {
        "verts": len(mesh.vertices),
        "unique_pos": len(uniq),
        "faces": len(mesh.polygons),
        "has_custom_normals": bool(getattr(mesh, "has_custom_normals", False)),
        "use_auto_smooth": getattr(mesh, "use_auto_smooth", None),
    }
print(json.dumps(report, indent=2))
