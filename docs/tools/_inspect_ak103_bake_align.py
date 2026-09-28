"""Print archive vs Frostoise donor bounds so the rebake can be aimed."""

import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
clean = Path(argv[0])
donor = Path(argv[1])

bpy.ops.wm.open_mainfile(filepath=str(clean))


def bbox(obj):
    lo = Vector((math.inf,) * 3)
    hi = Vector((-math.inf,) * 3)
    for corner in obj.bound_box:
        p = obj.matrix_world @ Vector(corner)
        for i in range(3):
            lo[i] = min(lo[i], p[i])
            hi[i] = max(hi[i], p[i])
    return [round(v, 4) for v in lo], [round(v, 4) for v in hi]


report = {
    "archive": {
        o.name: {
            "parent": o.parent.name if o.parent else None,
            "hide_render": o.hide_render,
            "bbox": bbox(o),
            "verts": len(o.data.vertices) if o.type == "MESH" else 0,
        }
        for o in bpy.data.objects
        if o.name.startswith("AK103")
    }
}

before = set(bpy.data.objects)
with bpy.data.libraries.load(str(donor), link=False) as (src, dst):
    dst.objects = [n for n in src.objects if n.startswith("AK103")]
donors = []
for obj in bpy.data.objects:
    if obj in before or not obj.name.startswith("AK103"):
        continue
    if obj.name not in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.link(obj)
    donors.append(obj)

report["donor_objects"] = {
    o.name: {
        "parent": o.parent.name if o.parent else None,
        "hide_render": o.hide_render,
        "bbox": bbox(o),
        "verts": len(o.data.vertices) if o.type == "MESH" else 0,
        "mats": [m.name if m else None for m in (o.data.materials if o.type == "MESH" else [])],
    }
    for o in donors
}

print(json.dumps(report, indent=2, ensure_ascii=False))
