"""Inspect Frostoise AK-103 for material-based module split. Read-only on source."""

import bmesh
import bpy
from collections import defaultdict
from mathutils import Vector
from pathlib import Path

BLEND = Path(r"E:\JaWeapons\Weapons\_ak103_jazz_build\candidates\frostoise\source\ak103 clean.blend")
OUT = Path(r"E:\JaWeapons\Weapons\_ak103_jazz_build\diag\frostoise_split")


def bbox(verts):
    xs, ys, zs = zip(*verts)
    lo, hi = Vector((min(xs), min(ys), min(zs))), Vector((max(xs), max(ys), max(zs)))
    return lo, hi, hi - lo


def islands(bm, faces):
    remaining = set(faces)
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
        groups.append(group)
    return groups


def main():
    bpy.ops.wm.open_mainfile(filepath=str(BLEND))
    OUT.mkdir(parents=True, exist_ok=True)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    print("objects", [(o.name, len(o.data.polygons), [m.name if m else None for m in o.data.materials]) for o in meshes])

    obj = next(o for o in meshes if o.data.polygons)
    # pick the big one
    obj = max(meshes, key=lambda o: len(o.data.polygons))
    print("primary", obj.name, "verts", len(obj.data.vertices), "faces", len(obj.data.polygons))

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()

    by_mat = defaultdict(list)
    for face in bm.faces:
        name = obj.data.materials[face.material_index].name if obj.data.materials[face.material_index] else f"slot{face.material_index}"
        by_mat[name].append(face)

    for name, faces in sorted(by_mat.items()):
        verts = [obj.matrix_world @ f.calc_center_median() for f in faces]
        # better: all unique verts
        vset = {(obj.matrix_world @ v.co).freeze() for f in faces for v in f.verts}
        lo, hi, size = bbox([(v.x, v.y, v.z) for v in vset])
        groups = islands(bm, faces)
        print(
            f"MAT {name:16} faces={len(faces):5} islands={len(groups):3} "
            f"size=({size.x:.3f},{size.y:.3f},{size.z:.3f}) "
            f"lo=({lo.x:.3f},{lo.y:.3f},{lo.z:.3f}) hi=({hi.x:.3f},{hi.y:.3f},{hi.z:.3f})"
        )
        if name in {"Barrel", "Metal", "ShinyMetal", "Grip", "Stock"} and len(groups) > 1:
            for i, g in enumerate(sorted(groups, key=len, reverse=True)[:12]):
                gv = {(obj.matrix_world @ v.co).freeze() for f in g for v in f.verts}
                glo, ghi, gsz = bbox([(v.x, v.y, v.z) for v in gv])
                print(
                    f"  island {i:02} faces={len(g):4} "
                    f"size=({gsz.x:.3f},{gsz.y:.3f},{gsz.z:.3f}) "
                    f"y={glo.y:.3f}..{ghi.y:.3f} z={glo.z:.3f}..{ghi.z:.3f}"
                )

    bm.free()
    print("images")
    for im in bpy.data.images:
        print(f"  {im.name:50} packed={im.packed_file is not None} size={list(im.size)} path={im.filepath}")
    for extra in meshes:
        if extra is obj:
            continue
        lo, hi, size = bbox([( (extra.matrix_world @ v.co).x, (extra.matrix_world @ v.co).y, (extra.matrix_world @ v.co).z) for v in extra.data.vertices])
        print(f"EXTRA {extra.name} faces={len(extra.data.polygons)} size=({size.x:.3f},{size.y:.3f},{size.z:.3f}) y={lo.y:.3f}..{hi.y:.3f} z={lo.z:.3f}..{hi.z:.3f}")


if __name__ == "__main__":
    main()
