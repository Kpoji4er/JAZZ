"""Overlay a new weapon build against already accepted JAZZ weapons.

    blender --background --factory-startup --python docs/tools/_build_weapon_scale_overlay.py -- \
        --new <clean/AK103.blend> --name AK103 \
        --ref <_ak_jazz_build/AK74M_JAZZ.blend> --ref <_ak_jazz_build/AK74_JAZZ.blend> \
        --out <diag/overlay>

Mandatory gate before importing any new firearm: a long gun may never end up
shorter in game than an accepted AK of the same or smaller real length.

Both scenes are already metric and share the JAZZ convention (-Y forward, Z up),
so the reference is anchored on the magazine well - the one landmark every AK
pattern shares - and rendered translucent over the new build. Lengths are burned
into the image in metres.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

NEW_COLOUR = (0.20, 0.22, 0.26, 1.0)
REF_COLOURS = [(0.95, 0.35, 0.15, 1.0), (0.25, 0.65, 0.95, 1.0), (0.45, 0.85, 0.35, 1.0)]


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--new", required=True, type=Path)
    p.add_argument("--name", required=True)
    p.add_argument("--ref", action="append", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--res", type=int, default=1800)
    return p.parse_args(argv)


def bbox(objects):
    lo = Vector((math.inf,) * 3)
    hi = Vector((-math.inf,) * 3)
    for obj in objects:
        for corner in obj.bound_box:
            p = obj.matrix_world @ Vector(corner)
            for i in range(3):
                lo[i] = min(lo[i], p[i])
                hi[i] = max(hi[i], p[i])
    return lo, hi


def append_meshes(path, tag):
    """Append a whole rig. Origin empties carry the export transform of the
    accepted AK builds, so the hierarchy must survive or the reference shrinks."""
    before = set(bpy.data.objects)
    with bpy.data.libraries.load(str(path), link=False) as (src, dst):
        dst.objects = list(src.objects)
    linked = []
    for obj in set(bpy.data.objects) - before:
        bpy.context.scene.collection.objects.link(obj)
        obj.name = f"{tag}__{obj.name}"
        linked.append(obj)
    bpy.context.view_layer.update()
    return [o for o in linked if o.type == "MESH"], linked


def magazine_anchor(objects):
    """Centre of the magazine bbox; falls back to the whole-model centre."""
    mags = [o for o in objects if "magazine" in o.name.lower()]
    lo, hi = bbox(mags or objects)
    return (lo + hi) / 2


def add_label(text, location, size):
    """Text laid out for the side camera (-X looking towards +X)."""
    curve = bpy.data.curves.new(type="FONT", name="label")
    curve.body = text
    curve.size = size
    curve.align_x = "LEFT"
    obj = bpy.data.objects.new("label_" + text[:12], curve)
    obj.location = location
    obj.rotation_euler = (math.radians(90), 0, math.radians(-90))
    obj.color = (0.05, 0.05, 0.05, 1.0)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def main():
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    bpy.ops.wm.open_mainfile(filepath=str(args.new))
    new_objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    for obj in new_objs:
        obj.color = NEW_COLOUR
    new_lo, new_hi = bbox(new_objs)
    new_anchor = magazine_anchor(new_objs)

    measurements = {args.name: round(new_hi.y - new_lo.y, 4)}
    labels = [(args.name, new_hi.y - new_lo.y, NEW_COLOUR)]

    for index, ref_path in enumerate(args.ref):
        tag = ref_path.stem.replace("_JAZZ", "")
        objs, linked = append_meshes(ref_path, tag)
        # hide folded-stock variants so the silhouette stays readable
        for obj in list(objs):
            if "stockfolded" in obj.name.lower():
                objs.remove(obj)
                obj.hide_render = True
        lo, hi = bbox(objs)
        measurements[tag] = round(hi.y - lo.y, 4)
        shift = new_anchor - magazine_anchor(objs)
        colour = REF_COLOURS[index % len(REF_COLOURS)]
        for obj in linked:
            if obj.parent is None:
                obj.location += shift
        for obj in objs:
            obj.color = colour
        bpy.context.view_layer.update()
        labels.append((tag, hi.y - lo.y, colour))

    all_objs = [
        o
        for o in bpy.context.scene.objects
        if o.type == "MESH" and not o.hide_render
    ]
    lo, hi = bbox(all_objs)
    span = max(hi - lo)

    line = span * 0.042
    label_objs = []
    for i, (tag, length, colour) in enumerate(labels):
        obj = add_label(
            f"{tag}  {length:.3f} m",
            (lo.x, hi.y, hi.z + line * (1.3 + (len(labels) - 1 - i) * 1.25)),
            line,
        )
        obj.color = colour
        label_objs.append(obj)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = args.res
    scene.render.resolution_y = int(args.res * 0.55)
    scene.display.shading.light = "FLAT"
    scene.display.shading.color_type = "OBJECT"
    scene.display.shading.show_xray = True
    scene.display.shading.xray_alpha = 0.72
    scene.display.shading.show_object_outline = True
    scene.view_settings.view_transform = "Standard"

    # font objects report an empty bound_box before evaluation, so reserve the
    # label band explicitly instead of measuring it
    lo, hi = bbox(all_objs)
    hi.z += line * (2.6 + len(labels) * 1.25)
    centre = (lo + hi) / 2
    span = max(hi - lo)
    cam_scale = span * 1.06
    cam_data = bpy.data.cameras.new("cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = cam_scale
    cam_data.clip_start = span * 0.001
    cam_data.clip_end = span * 20
    cam = bpy.data.objects.new("cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam

    previews = []
    for view, (offset, rot) in {
        "side": (Vector((-1, 0, 0)), (math.radians(90), 0, math.radians(-90))),
        # rolled 90 deg so the barrel stays horizontal in a landscape frame
        "top": (Vector((0, 0, 1)), (0, 0, math.radians(-90))),
    }.items():
        for obj in label_objs:
            obj.hide_render = view != "side"
        cam.location = centre + offset * span * 4
        cam.rotation_euler = rot
        path = args.out / f"{args.name}_vs_ak_{view}.png"
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        previews.append(path.name)

    report = {"lengths_m": measurements, "previews": previews}
    (args.out / "scale-overlay.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
