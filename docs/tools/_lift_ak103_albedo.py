"""Lift crushed archive-bake albedo so the rifle reads under inventory light."""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

clean = Path(sys.argv[sys.argv.index("--") + 1])
bpy.ops.wm.open_mainfile(filepath=str(clean))

GAIN = 2.6
LIFT = 0.04

for image in list(bpy.data.images):
    if not image.name.endswith("_Base") and "_Base_bake" not in image.name:
        continue
    w, h = image.size
    px = [0.0] * (w * h * 4)
    image.pixels.foreach_get(px)
    for i in range(0, len(px), 4):
        if px[i] + px[i + 1] + px[i + 2] <= 0.002:
            continue
        px[i] = min(1.0, px[i] * GAIN + LIFT)
        px[i + 1] = min(1.0, px[i + 1] * GAIN + LIFT)
        px[i + 2] = min(1.0, px[i + 2] * GAIN + LIFT)
    image.pixels.foreach_set(px)
    image.update()
    if image.filepath_raw:
        image.pack()
        image.save()
    print("lifted", image.name, image.size[:])

# Brighter side preview so the owner can judge the archive mesh.
objects = [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith("AK103")]
lo, hi = Vector((math.inf,) * 3), Vector((-math.inf,) * 3)
for obj in objects:
    for corner in obj.bound_box:
        p = obj.matrix_world @ Vector(corner)
        for i in range(3):
            lo[i] = min(lo[i], p[i])
            hi[i] = max(hi[i], p[i])
centre = (lo + hi) / 2
span = max(hi - lo)
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1800
scene.render.resolution_y = 900
scene.render.film_transparent = True
scene.view_settings.view_transform = "Standard"
cam_data = bpy.data.cameras.new("lift_cam")
cam_data.type = "ORTHO"
cam_data.ortho_scale = span * 1.12
cam_data.clip_end = span * 10
cam = bpy.data.objects.new("lift_cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam.location = centre + Vector((-1, 0, 0)) * span * 3
cam.rotation_euler = (math.radians(90), 0, math.radians(-90))
for i, (energy, rot) in enumerate((
    (8, (math.radians(50), 0, math.radians(-35))),
    (3, (math.radians(70), 0, math.radians(140))),
    (2, (math.radians(-20), 0, 0)),
)):
    light = bpy.data.objects.new(f"lift_sun_{i}", bpy.data.lights.new(f"lift_sun_{i}", "SUN"))
    scene.collection.objects.link(light)
    light.data.energy = energy
    light.rotation_euler = rot
out = clean.parent.parent / "diag" / "clean" / "AK103_archive_textured_side.png"
scene.render.filepath = str(out)
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(clean))
print("saved", out)
