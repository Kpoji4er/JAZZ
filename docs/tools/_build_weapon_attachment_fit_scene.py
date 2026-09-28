"""Offline attachment fit check for a weapon that is not installed yet.

    blender --background --factory-startup --python docs/tools/_build_weapon_attachment_fit_scene.py -- \
        --blend <rigged/AK103_JA3.blend> --spots <export-report.json> \
        --reference <_vanilla_reference> --out <diag/attachments> --name AK103

Same idea as _build_ak_attachment_fit_scene.py, but it reads spots from the
export report instead of an installed `.ent`, so a weapon can be judged before
anything is written into jazz_assets.

Real decoded HGM attachments are placed at the spots and colour coded. This is
geometry fit only: it does not prove the in-game component bindings.
"""

import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

CONFIGS = ("GP30", "GP45", "Bipod30", "PSO", "Kobra", "tyulpan", "NSPU")
OPTICS = ("PKAA", "Kobra", "tyulpan", "NSPU", "PSO")
TOP_VIEW = {"PSO", "Kobra", "tyulpan", "NSPU"}


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--blend", required=True, type=Path)
    p.add_argument("--spots", required=True, type=Path)
    p.add_argument("--reference", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--name", required=True)
    p.add_argument("--config", action="append", choices=CONFIGS)
    p.add_argument("--samples", type=int, default=32)
    return p.parse_args(argv)


def material(name, colour):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*colour, 1)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*colour, 1)
    bsdf.inputs["Roughness"].default_value = 0.7
    return mat


def add_mesh(path, name, position, mat):
    data = json.loads(path.read_text())
    vertices, faces = [], []
    for mesh in data["meshes"]:
        if not mesh["vertices"]:
            print("PARTIAL REFERENCE: empty submesh in", path)
            continue
        box = mesh["bbox"] or data["bbox"]
        centre = [(box[i] + box[i + 3]) * 0.5 for i in range(3)]
        offset = len(vertices)
        for v in mesh["vertices"]:
            x, y, z = (v[i] + centre[i] for i in range(3))
            vertices.append((-y, -x, z))
        faces.extend(tuple(i + offset for i in reversed(f)) for f in mesh["faces"])
    data_mesh = bpy.data.meshes.new(name)
    data_mesh.from_pydata(vertices, [], faces)
    data_mesh.update()
    obj = bpy.data.objects.new(name, data_mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = position
    obj.data.materials.append(mat)
    return obj


def main():
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    spots = {
        name: Vector(value)
        for name, value in json.loads(args.spots.read_text())["spots_m"].items()
    }

    bpy.ops.wm.open_mainfile(filepath=str(args.blend))
    scene = bpy.context.scene

    grey = material("Gun geometry", (0.24, 0.28, 0.31))
    orange = material("Vanilla GP", (0.75, 0.25, 0.045))
    blue = material("Vanilla bipod", (0.07, 0.35, 0.7))
    green = material("Existing optic", (0.2, 0.55, 0.16))

    for obj in list(scene.objects):
        if obj.type == "MESH":
            obj.hide_render = obj.name.endswith("_StockFolded")
            obj.data.materials.clear()
            obj.data.materials.append(grey)
        elif obj.type in {"LIGHT", "CAMERA"}:
            bpy.data.objects.remove(obj, do_unlink=True)

    ref = args.reference
    gp = add_mesh(
        ref / "Geometry/WeaponAttA_GrenadeLauncherAK47_mesh.json",
        "Vanilla GP at Under", spots["Under"], orange,
    )
    bipod = add_mesh(
        ref / "Geometry/WeaponAttA_BipodAK47_mesh.json",
        "Vanilla bipod at Bipod", spots["Bipod"], blue,
    )
    mag45 = add_mesh(
        ref / "CustomGeometry/AK74_Backelite_45.json",
        "Shared magazine 45", spots["Magazine"], orange,
    )
    mag30 = next(o for o in scene.objects if o.name.endswith("_Magazine"))

    optics = {}
    for optic in OPTICS:
        path = ref / (
            "Geometry/WeaponAttA_ScopeDragunov_01_mesh.json"
            if optic == "PSO"
            else f"CustomGeometry/{optic}.json"
        )
        optics[optic] = add_mesh(path, optic + " at Scope", spots["Scope"], green)
    plate = add_mesh(
        ref / "CustomGeometry/AKSeriaMount.json",
        "AK plate at General", spots["General"], green,
    )

    for name, position in spots.items():
        empty = bpy.data.objects.new("Installed " + name, None)
        scene.collection.objects.link(empty)
        empty.location = position
        empty.empty_display_size = 0.008
        empty.show_name = True

    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = args.samples
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 650
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "Standard"
    scene.world = bpy.data.worlds.new("Fit neutral world")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.18,) * 3 + (1,)

    cam_data = bpy.data.cameras.new("FitCamera")
    cam_data.type = "ORTHO"
    camera = bpy.data.objects.new("FitCamera", cam_data)
    scene.collection.objects.link(camera)
    scene.camera = camera

    aim = Vector((0, -0.18, -0.015))
    for index, position in enumerate([(1, -0.4, 1), (-1, 0.1, 0.7)]):
        light = bpy.data.lights.new("Fit light " + str(index), "AREA")
        light.energy = 70
        light.size = 1.2
        obj = bpy.data.objects.new(light.name, light)
        scene.collection.objects.link(obj)
        obj.location = position
        obj.rotation_euler = (aim - obj.location).to_track_quat("-Z", "Y").to_euler()

    made = []
    for config in args.config or CONFIGS:
        gp.hide_render = config not in ("GP30", "GP45")
        bipod.hide_render = config != "Bipod30"
        mag45.hide_render = config != "GP45"
        mag30.hide_render = config == "GP45"
        selected = config if config in optics else "PKAA"
        for name, obj in optics.items():
            obj.hide_render = name != selected
        plate.hide_render = selected in ("PSO", "Kobra")
        bpy.context.view_layer.update()

        points = [
            obj.matrix_world @ Vector(v)
            for obj in scene.objects
            if obj.type == "MESH" and not obj.hide_render
            for v in obj.bound_box
        ]
        lo = Vector(tuple(min(p[i] for p in points) for i in range(3)))
        hi = Vector(tuple(max(p[i] for p in points) for i in range(3)))
        target = (lo + hi) / 2
        cam_data.ortho_scale = max(hi.y - lo.y, (hi.z - lo.z) * 1400 / 650) * 1.10

        views = [("left", Vector((2, 0.04, 0.18))), ("right", Vector((-2, 0.04, 0.18)))]
        if config in TOP_VIEW:
            views.append(("top", Vector((0.0001, 0, 2))))
        for view, offset in views:
            camera.location = target + offset
            camera.rotation_euler = (
                (target - camera.location).to_track_quat("-Z", "Y").to_euler()
            )
            path = args.out / f"{args.name}_{config}_{view}_fit.png"
            scene.render.filepath = str(path)
            bpy.ops.render.render(write_still=True)
            made.append(path.name)

    bpy.ops.wm.save_as_mainfile(
        filepath=str(args.out / f"{args.name}_attachment_fit.blend")
    )
    print(json.dumps({"renders": made}, indent=2))


if __name__ == "__main__":
    main()
