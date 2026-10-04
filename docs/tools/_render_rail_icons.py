"""Photograph rail and dovetail meshes as 100x100 component icons.

Blender:
  blender --background --factory-startup --python docs/tools/_render_rail_icons.py -- ^
    --manifest <json> --out <WeaponComponents/Rails>

The manifest is a list of {id, hgm}. Each icon is the part alone, side view,
muzzle-right, with the same outline used for other component photos.
Inventory and the modify cabinet both read WeaponComponent.Icon.
"""
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _decode_vz58_hgm import decode as decode_v14
import _render_ak103_icon as iconmod

iconmod.RING_DISTANCE = 2
iconmod.HALO_DISTANCE = 4
iconmod.HALO_BLUR = 3
build_compositor = iconmod.build_compositor

import struct


def decode_mesh(path):
    path = Path(path)
    data = path.read_bytes()
    version = struct.unpack_from("<H", data, 4)[0]
    if version == 14:
        return decode_v14(path)
    assert version in (9, 12), (path.name, version)
    offset = 32
    keys = []

    def take(fmt):
        nonlocal offset
        values = struct.unpack_from("<" + fmt, data, offset)
        offset += struct.calcsize("<" + fmt)
        return values[0] if len(values) == 1 else values

    def string():
        nonlocal offset
        size = take("I")
        value = data[offset:offset + size].decode("ascii").rstrip("\0")
        offset += size
        return value

    meshes = []
    for _ in range(take("I")):
        take("I")
        take("2I")
        nv = take("I")
        ni = take("I")
        if take("B") == 2:
            string()
        fields = []
        for _field in range(take("I")):
            marker = take("B")
            key = string() if marker == 2 else keys[take("I")]
            if marker == 2:
                keys.append(key)
            take("I")
            fmt = string()
            take("I")
            pos = take("I")
            take("B")
            fields.append((key, fmt, pos))
        take("I")
        stride = take("I")
        assert take("B") == 1
        field = next(v for v in fields if v[0] == "pos")
        points = [
            [v / 32767 for v in struct.unpack_from("<3h", data, offset + i * stride + field[2])]
            for i in range(nv)
        ]
        offset += nv * stride
        assert take("B") == 1
        faces = [struct.unpack_from("<3H", data, offset + i * 6)[0:3] for i in range(ni // 3)]
        offset += ni * 2 + 40
        meshes.append({"vertices": points, "faces": list(faces), "bbox": [0, 0, 0, 0, 0, 0]})
    return {"bbox": [0, 0, 0, 0, 0, 0], "meshes": meshes}

p = __import__("argparse").ArgumentParser()
p.add_argument("--manifest", type=Path, required=True)
p.add_argument("--out", type=Path, required=True)
p.add_argument("--samples", type=int, default=32)
a = p.parse_args(sys.argv[sys.argv.index("--") + 1:])
a.out.mkdir(parents=True, exist_ok=True)
report = {}

for item in json.loads(a.manifest.read_text(encoding="utf-8")):
    label = item["id"]
    data = decode_mesh(Path(item["hgm"]))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    verts = []
    faces = []
    for mesh in data["meshes"]:
        if not mesh["vertices"]:
            continue
        box = mesh["bbox"] or data["bbox"]
        center = Vector(tuple((box[i] + box[i + 3]) / 2 for i in range(3)))
        offset = len(verts)
        for v in mesh["vertices"]:
            x, y, z = Vector(v) + center
            verts.append((-y, -x, z))
        faces.extend(tuple(offset + i for i in reversed(f)) for f in mesh["faces"])
    if not faces:
        report[label] = "empty"
        continue
    mesh = bpy.data.meshes.new(label)
    mesh.from_pydata(verts, [], faces)
    obj = bpy.data.objects.new(label, mesh)
    scene.collection.objects.link(obj)
    mat = bpy.data.materials.new(label + "_Metal")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.025, 0.028, 0.030, 1)
    bsdf.inputs["Metallic"].default_value = 0.6
    bsdf.inputs["Roughness"].default_value = 0.55
    obj.data.materials.append(mat)
    bpy.context.view_layer.update()
    points = [obj.matrix_world @ Vector(v) for v in obj.bound_box]
    lo = Vector(tuple(min(v[i] for v in points) for i in range(3)))
    hi = Vector(tuple(max(v[i] for v in points) for i in range(3)))
    center = (lo + hi) / 2
    scene.render.engine = "CYCLES"
    scene.cycles.samples = a.samples
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 1.0
    scene.world = bpy.data.worlds.new("World")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.3
    camera = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
    scene.collection.objects.link(camera)
    scene.camera = camera
    camera.data.type = "ORTHO"
    span = hi - lo
    camera.data.ortho_scale = max(span.y, span.z, 0.01) * 1.35
    camera.location = center + Vector((-2, 0, 0))
    camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
    for pos, power in [((-1, -0.5, 1.5), 70), ((-0.5, 0.5, 1), 50), ((1, 1, 0), 50)]:
        light = bpy.data.lights.new("Light", "AREA")
        light.energy = power
        light.size = 1.5
        ob = bpy.data.objects.new("Light", light)
        scene.collection.objects.link(ob)
        ob.location = center + Vector(pos)
        ob.rotation_euler = (center - ob.location).to_track_quat("-Z", "Y").to_euler()
    build_compositor(scene)
    scene.render.resolution_x = 100
    scene.render.resolution_y = 100
    scene.render.resolution_percentage = 100
    scene.render.filepath = str(a.out / (label + ".png"))
    bpy.ops.render.render(write_still=True)
    report[label] = scene.render.filepath
    print("rendered", label)

(a.out / "render-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("done", len(report))
