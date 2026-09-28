"""Build the AK-103 clean scene from the CC-BY Frostoise source.

    blender --background --factory-startup --python docs/tools/_build_ak103_assets.py -- \
        --blend <_ak103_jazz_build/candidates/frostoise/source/ak103 clean.blend> \
        --build  <_ak103_jazz_build> [--render]

Geometry: "AK 103" by Frostoise, CC Attribution. Spec: JAZZ-WEAPON-AK103-001.
The source is one mesh with seven materials. Modules are split by material and
already-separate loose islands — never by a plane through connected faces.

    Magazine  <- Clip
    Handguard <- Grip (three islands, all on the forend)
    Stock     <- Stock + Cube.080 + BezierCurve.002 (sling loop on the butt)
    Muzzle    <- frontmost Barrel island (the brake)
    Body      <- Metal, ShinyMetal, Handgrip, remaining Barrel islands

Muzzle towards -Y, Z up, metres, butt-to-muzzle = 943 mm.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

REAL_LENGTH_M = 0.943

MODULE_COLOURS = {
    "Body": (0.55, 0.55, 0.55, 1.0),
    "Handguard": (0.90, 0.45, 0.10, 1.0),
    "Magazine": (0.15, 0.55, 0.90, 1.0),
    "Stock": (0.25, 0.75, 0.30, 1.0),
    "Muzzle": (0.90, 0.15, 0.30, 1.0),
}


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--blend", required=True, type=Path)
    p.add_argument("--build", required=True, type=Path)
    p.add_argument("--render", action="store_true")
    p.add_argument("--res", type=int, default=1600)
    return p.parse_args(argv)


def select_only(objects):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]


def apply_transforms(objects):
    select_only(objects)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def world_bbox(objects):
    lo = Vector((math.inf,) * 3)
    hi = Vector((-math.inf,) * 3)
    for obj in objects:
        for corner in obj.bound_box:
            p = obj.matrix_world @ Vector(corner)
            for i in range(3):
                lo[i] = min(lo[i], p[i])
                hi[i] = max(hi[i], p[i])
    return lo, hi


def used_material(obj):
    used = {
        obj.data.materials[poly.material_index].name
        for poly in obj.data.polygons
        if obj.data.materials[poly.material_index]
    }
    if len(used) != 1:
        raise SystemExit(f"{obj.name} uses {used}")
    return used.pop()


def centroid_y(obj):
    verts = obj.data.vertices
    return sum((obj.matrix_world @ v.co).y for v in verts) / len(verts)


def join_named(members, name, colour):
    if isinstance(members, bpy.types.Object):
        members = [members]
    members = [o for o in members if o and o.name in bpy.data.objects]
    select_only(members)
    if len(members) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    obj.name = name
    obj.data.name = name + "_Mesh"
    obj.color = colour
    return obj


def orient_and_scale(objects):
    apply_transforms(objects)
    lo, hi = world_bbox(objects)
    raw_length = hi.y - lo.y
    factor = REAL_LENGTH_M / raw_length
    empty = bpy.data.objects.new("pivot", None)
    bpy.context.scene.collection.objects.link(empty)
    for obj in objects:
        obj.parent = empty
    empty.scale = (factor, factor, factor)
    bpy.context.view_layer.update()
    for obj in objects:
        matrix = obj.matrix_world.copy()
        obj.parent = None
        obj.matrix_world = matrix
    bpy.data.objects.remove(empty)
    apply_transforms(objects)
    return raw_length, factor


def zero_at_butt(objects):
    lo, hi = world_bbox(objects)
    offset = Vector((-(lo.x + hi.x) / 2, -hi.y, -(lo.z + hi.z) / 2))
    for obj in objects:
        obj.location += offset
    apply_transforms(objects)
    return offset


def place_landmarks(landmarks):
    for label, data in landmarks.items():
        lo = Vector(data["min"])
        hi = Vector(data["max"])
        empty = bpy.data.objects.new(label, None)
        empty.empty_display_size = 0.01
        empty.location = (lo + hi) / 2
        empty["bbox_min"] = list(lo)
        empty["bbox_max"] = list(hi)
        bpy.context.scene.collection.objects.link(empty)
        data["min"] = [round(v, 6) for v in lo]
        data["max"] = [round(v, 6) for v in hi]


def split_modules(primary, extras):
    select_only([primary])
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.separate(type="MATERIAL")
    bpy.ops.object.mode_set(mode="OBJECT")
    parts = {}
    for obj in bpy.context.selected_objects:
        parts[used_material(obj)] = obj

    required = {"Barrel", "Clip", "Grip", "Handgrip", "Metal", "ShinyMetal", "Stock"}
    missing = required - set(parts)
    if missing:
        raise SystemExit(f"materials not found after split: {missing}")

    select_only([parts["Barrel"]])
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.separate(type="LOOSE")
    bpy.ops.object.mode_set(mode="OBJECT")
    barrel_parts = list(bpy.context.selected_objects)
    barrel_parts.sort(key=centroid_y)
    muzzle = barrel_parts[0]
    barrel_rest = barrel_parts[1:]

    stock_extras = []
    for extra in extras:
        if extra.name.startswith("Cube.079"):
            bpy.data.objects.remove(extra, do_unlink=True)
            continue
        stock_extras.append(extra)

    before_join = {
        "Handgrip": parts["Handgrip"],
        "ShinyMetal": parts["ShinyMetal"],
        "BarrelBody": barrel_rest[0] if barrel_rest else None,
    }
    landmarks = {
        "LM_Grip": bbox_entry(parts["Handgrip"], "Handgrip"),
        "LM_Trigger": bbox_entry(parts["Handgrip"], "Handgrip"),
        "LM_Rail": bbox_entry(parts["ShinyMetal"], "ShinyMetal"),
        "LM_Bore": bbox_entry(barrel_rest[0], "Barrel") if barrel_rest else bbox_entry(muzzle, "Barrel"),
        "LM_FrontSight": front_sight_entry(barrel_rest[0] if barrel_rest else muzzle),
    }
    # Trigger sits at the front of the pistol grip, not the whole grip volume.
    grip = landmarks["LM_Trigger"]
    lo, hi = Vector(grip["min"]), Vector(grip["max"])
    landmarks["LM_Trigger"] = {
        "source": "Handgrip_front",
        "min": [lo.x, hi.y - 0.015, (lo.z + hi.z) / 2],
        "max": [hi.x, hi.y, hi.z],
    }

    joined = {
        "Magazine": join_named(parts["Clip"], "AK103_Magazine", MODULE_COLOURS["Magazine"]),
        "Handguard": join_named(parts["Grip"], "AK103_Handguard", MODULE_COLOURS["Handguard"]),
        "Muzzle": join_named(muzzle, "AK103_Muzzle", MODULE_COLOURS["Muzzle"]),
        "Stock": join_named([parts["Stock"], *stock_extras], "AK103_Stock", MODULE_COLOURS["Stock"]),
        "Body": join_named(
            [parts["Metal"], parts["ShinyMetal"], parts["Handgrip"], *barrel_rest],
            "AK103",
            MODULE_COLOURS["Body"],
        ),
    }
    return joined, landmarks, before_join


def bbox_entry(obj, source):
    lo, hi = world_bbox([obj])
    return {"source": source, "min": list(lo), "max": list(hi)}


def front_sight_entry(obj):
    lo, hi = world_bbox([obj])
    span = hi - lo
    return {
        "source": "Barrel_front_top",
        "min": [lo.x, lo.y, hi.z - span.z * 0.25],
        "max": [hi.x, lo.y + span.y * 0.12, hi.z],
    }


def render_module_map(out, objects, res):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = res
    scene.render.resolution_y = res // 2
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "OBJECT"
    scene.display.shading.show_cavity = True
    scene.view_settings.view_transform = "Standard"

    lo, hi = world_bbox(objects)
    centre = (lo + hi) / 2
    span = max(hi - lo)
    cam_data = bpy.data.cameras.new("cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = span * 1.1
    cam_data.clip_start = span * 0.001
    cam_data.clip_end = span * 10
    cam = bpy.data.objects.new("cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

    made = []
    for view, (offset, rot) in {
        "side": (Vector((-1, 0, 0)), (math.radians(90), 0, math.radians(-90))),
        "top": (Vector((0, 0, 1)), (0, 0, 0)),
    }.items():
        cam.location = centre + offset * span * 3
        cam.rotation_euler = rot
        path = out / f"AK103_modules_{view}.png"
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        made.append(path.name)
    bpy.data.objects.remove(cam)
    return made


def main():
    args = parse_args()
    clean_dir = args.build / "clean"
    diag_dir = args.build / "diag" / "clean"
    clean_dir.mkdir(parents=True, exist_ok=True)
    diag_dir.mkdir(parents=True, exist_ok=True)

    previous = clean_dir / "AK103.blend"
    if previous.is_file() and not (clean_dir / "AK103_bogdanzloy.blend").is_file():
        previous.replace(clean_dir / "AK103_bogdanzloy.blend")

    bpy.ops.wm.open_mainfile(filepath=str(args.blend))
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    primary = max(meshes, key=lambda o: len(o.data.polygons))
    extras = [o for o in meshes if o is not primary]
    raw_length, factor = orient_and_scale([primary, *extras])
    modules, landmarks, _ = split_modules(primary, extras)
    objects = list(modules.values())
    offset = zero_at_butt(objects)
    for data in landmarks.values():
        data["min"] = [round(v + o, 6) for v, o in zip(data["min"], offset)]
        data["max"] = [round(v + o, 6) for v, o in zip(data["max"], offset)]
    place_landmarks(landmarks)

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1

    lo, hi = world_bbox(objects)
    report = {
        "source": str(args.blend),
        "author": "Frostoise",
        "license": "CC Attribution",
        "source_raw_length_units": round(raw_length, 4),
        "scale_factor": round(factor, 8),
        "origin_offset": [round(v, 5) for v in offset],
        "length_m": round(hi.y - lo.y, 4),
        "height_m": round(hi.z - lo.z, 4),
        "width_m": round(hi.x - lo.x, 4),
        "landmarks": landmarks,
        "modules": {
            name: {
                "object": obj.name,
                "tris": sum(len(p.vertices) - 2 for p in obj.data.polygons),
                "dimensions_m": [round(v, 4) for v in obj.dimensions],
            }
            for name, obj in modules.items()
        },
    }
    if args.render:
        report["previews"] = render_module_map(diag_dir, objects, args.res)

    bpy.ops.wm.save_as_mainfile(filepath=str(clean_dir / "AK103.blend"))
    (args.build / "build-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
