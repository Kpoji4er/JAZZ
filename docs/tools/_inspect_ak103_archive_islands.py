"""Cluster archive islands: assembled rifle vs exploded duplicates."""

import bmesh
import bpy
from mathutils import Vector
from pathlib import Path

SRC = Path(r"E:\JaWeapons\Weapons\_ak103_jazz_build\source")


def islands(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    remaining = set(bm.faces)
    groups = []
    while remaining:
        seed = remaining.pop()
        stack = [seed]
        group = {seed}
        while stack:
            face = stack.pop()
            for edge in face.edges:
                for other in edge.link_faces:
                    if other in remaining:
                        remaining.remove(other)
                        group.add(other)
                        stack.append(other)
        verts = [obj.matrix_world @ v.co for f in group for v in f.verts]
        xs, ys, zs = zip(*[(v.x, v.y, v.z) for v in verts])
        cx, cy, cz = sum(xs) / len(xs), sum(ys) / len(ys), sum(zs) / len(zs)
        groups.append(
            {
                "faces": len(group),
                "c": (round(cx, 2), round(cy, 2), round(cz, 2)),
                "size": (
                    round(max(xs) - min(xs), 2),
                    round(max(ys) - min(ys), 2),
                    round(max(zs) - min(zs), 2),
                ),
            }
        )
    bm.free()
    return groups


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for path in sorted(SRC.glob("model_*.obj")):
        bpy.ops.wm.obj_import(filepath=str(path))
    for obj in sorted(bpy.data.objects, key=lambda o: o.name):
        if obj.type != "MESH":
            continue
        groups = islands(obj)
        print(f"\n{obj.name} islands={len(groups)}")
        for i, g in enumerate(sorted(groups, key=lambda r: r["faces"], reverse=True)[:8]):
            print(f"  {i:02} faces={g['faces']:5} c={g['c']} size={g['size']}")


if __name__ == "__main__":
    main()
