"""Identify archive OBJ parts and whether they overlap or explode."""

import bpy
from mathutils import Vector
from pathlib import Path

SRC = Path(r"E:\JaWeapons\Weapons\_ak103_jazz_build\source")
OUT = Path(r"E:\JaWeapons\Weapons\_ak103_jazz_build\diag\archive")


def bbox(obj):
    lo = Vector((1e9,) * 3)
    hi = Vector((-1e9,) * 3)
    for corner in obj.bound_box:
        p = obj.matrix_world @ Vector(corner)
        for i in range(3):
            lo[i] = min(lo[i], p[i])
            hi[i] = max(hi[i], p[i])
    return lo, hi


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for path in sorted(SRC.glob("model_*.obj")):
        bpy.ops.wm.obj_import(filepath=str(path))
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    for obj in meshes:
        lo, hi = bbox(obj)
        uv = obj.data.uv_layers.active
        uvs = [0, 0]
        if uv:
            coords = [d.uv for d in uv.data]
            uvs = [
                sum(1 for c in coords if 0 <= c.x <= 1 and 0 <= c.y <= 1) / max(len(coords), 1),
                len(coords),
            ]
        print(
            f"{obj.name:12} tris={sum(len(p.vertices)-2 for p in obj.data.polygons):6} "
            f"size=({(hi-lo).x:7.2f},{(hi-lo).y:7.2f},{(hi-lo).z:7.2f}) "
            f"lo=({lo.x:7.2f},{lo.y:7.2f},{lo.z:7.2f}) "
            f"hi=({hi.x:7.2f},{hi.y:7.2f},{hi.z:7.2f}) "
            f"uv_in_01={uvs[0]:.2f}"
        )

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 800
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "OBJECT"
    scene.display.shading.show_cavity = True
    scene.view_settings.view_transform = "Standard"
    ulo = Vector((1e9,) * 3)
    uhi = Vector((-1e9,) * 3)
    for obj in meshes:
        lo, hi = bbox(obj)
        for i in range(3):
            ulo[i] = min(ulo[i], lo[i])
            uhi[i] = max(uhi[i], hi[i])
    centre = (ulo + uhi) / 2
    span = max(uhi - ulo)
    cam_data = bpy.data.cameras.new("cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = span * 1.1
    cam_data.clip_end = span * 10
    cam = bpy.data.objects.new("cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    cam.location = centre + Vector((0, -1, 0)) * span * 3
    cam.rotation_euler = (1.5708, 0, 0)
    for obj in meshes:
        obj.color = (0.55, 0.55, 0.55, 1)
    for obj in meshes:
        obj.color = (0.9, 0.15, 0.1, 1)
        scene.render.filepath = str(OUT / f"hl_{obj.name}.png")
        bpy.ops.render.render(write_still=True)
        obj.color = (0.55, 0.55, 0.55, 1)
        print("wrote", obj.name)


if __name__ == "__main__":
    main()
