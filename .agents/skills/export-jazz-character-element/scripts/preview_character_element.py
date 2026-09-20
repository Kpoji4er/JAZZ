"""Render orthographic head previews of a character element (headless Blender).

The agent cannot look through the viewport, so fit is reviewed from rendered images.

Usage:
    blender -b <source>.blend -P preview_character_element.py -- --object <name> --out <dir>
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

VIEWS = {
    "front": (0.0, -1.0, 0.0),
    "side": (1.0, 0.0, 0.0),
    "back34": (-0.75, 0.66, 0.15),
}


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--object", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args(argv)


def setup_colors(target):
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        obj.color = (0.13, 0.15, 0.10, 1.0) if obj is target else (0.78, 0.72, 0.66, 1.0)


def render_view(name, direction, focus, radius, out_dir):
    scene = bpy.context.scene
    camera_data = bpy.data.cameras.new(f"cam_{name}")
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = radius * 2.6
    camera = bpy.data.objects.new(f"cam_{name}", camera_data)
    scene.collection.objects.link(camera)

    offset = Vector(direction).normalized() * (radius * 6.0)
    camera.location = focus + offset
    direction_to_focus = focus - camera.location
    camera.rotation_euler = direction_to_focus.to_track_quat("-Z", "Y").to_euler()
    scene.camera = camera

    path = os.path.join(out_dir, f"preview_{name}.png")
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(camera, do_unlink=True)
    return path


def main():
    args = parse_args()
    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)

    target = bpy.data.objects.get(args.object)
    if not target:
        raise SystemExit(f"object {args.object!r} not found")

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = 700
    scene.render.resolution_y = 800
    scene.render.film_transparent = False
    shading = scene.display.shading
    shading.light = "STUDIO"
    shading.color_type = "OBJECT"
    # Workbench shadows and cavity smear a bright band across geometry that sits
    # behind another object; they make the fit unreadable on head renders.
    shading.show_shadows = False
    shading.show_cavity = False
    setup_colors(target)

    corners = [target.matrix_world @ Vector(c) for c in target.bound_box]
    focus = sum(corners, Vector()) / len(corners)
    radius = max((c - focus).length for c in corners)
    focus.z -= radius * 0.35

    for name, direction in VIEWS.items():
        print("[JAZZ] rendered", render_view(name, direction, focus, radius, out_dir))


main()
