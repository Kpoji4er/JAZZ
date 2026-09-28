"""Diagnostic pass over a raw weapon source folder before any JAZZ build work.

Launched through Blender:

    blender --background --factory-startup --python docs/tools/_inspect_weapon_source.py -- \
        --source <dir with .obj/.fbx/.glb> --out <report dir> [--name AK103]

Writes <out>/inspect-report.json plus three orthographic Workbench previews
(axis_x / axis_y / axis_z) so the source orientation, part split, scale and
texture coverage can be judged without opening the UI.

Read-only for the source folder.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

import bpy
from mathutils import Vector

MESH_SUFFIXES = {".obj", ".fbx", ".glb", ".gltf", ".dae", ".ply", ".stl"}


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--source", type=Path, help="folder with .obj/.fbx/.glb/.dae")
    g.add_argument("--blend", type=Path, help="open an existing .blend instead")
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--name", default="source")
    p.add_argument("--res", type=int, default=1600)
    p.add_argument(
        "--shading",
        choices=("MATERIAL", "TEXTURE", "SINGLE"),
        default="MATERIAL",
        help="Workbench colour source for the previews",
    )
    p.add_argument(
        "--show-hidden",
        action="store_true",
        help="also render objects flagged hide_render, e.g. folded-stock variants",
    )
    p.add_argument(
        "--highlight",
        help="regex over object names; renders one side view per match with that "
        "object in red, to identify anonymous parts such as Cube6_low",
    )
    return p.parse_args(argv)


def wipe_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_file(path):
    suffix = path.suffix.lower()
    if suffix == ".obj":
        bpy.ops.wm.obj_import(filepath=str(path))
    elif suffix == ".fbx":
        bpy.ops.import_scene.fbx(filepath=str(path))
    elif suffix in {".glb", ".gltf"}:
        bpy.ops.import_scene.gltf(filepath=str(path))
    elif suffix == ".dae":
        bpy.ops.wm.collada_import(filepath=str(path))
    elif suffix == ".ply":
        bpy.ops.wm.ply_import(filepath=str(path))
    elif suffix == ".stl":
        bpy.ops.wm.stl_import(filepath=str(path))
    else:
        raise ValueError(f"unsupported source {path}")


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


def describe(objects):
    rows = []
    for obj in sorted(objects, key=lambda o: o.name):
        mats = []
        for slot in obj.material_slots:
            mat = slot.material
            if mat is None:
                continue
            images = []
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == "TEX_IMAGE" and node.image is not None:
                        images.append(
                            {
                                "image": node.image.name,
                                "filepath": node.image.filepath,
                                "size": list(node.image.size),
                                "has_data": bool(node.image.has_data),
                            }
                        )
            mats.append({"material": mat.name, "textures": images})
        mesh = obj.data
        lo, hi = world_bbox([obj])
        rows.append(
            {
                "object": obj.name,
                "verts": len(mesh.vertices),
                "tris": sum(len(p.vertices) - 2 for p in mesh.polygons),
                "uv_layers": [uv.name for uv in mesh.uv_layers],
                "dimensions": [round(v, 5) for v in obj.dimensions],
                "location": [round(v, 5) for v in obj.location],
                "bbox_min": [round(v, 5) for v in lo],
                "bbox_max": [round(v, 5) for v in hi],
                "materials": mats,
            }
        )
    return rows


def setup_render(res, shading="MATERIAL"):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = res
    scene.render.resolution_y = res
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = shading
    scene.display.shading.show_cavity = True
    scene.view_settings.view_transform = "Standard"


AXIS_VIEWS = {
    # name: (camera direction offset, rotation euler)
    "axis_y": (Vector((0, -1, 0)), (math.radians(90), 0, 0)),
    "axis_x": (Vector((1, 0, 0)), (math.radians(90), 0, math.radians(90))),
    "axis_z": (Vector((0, 0, 1)), (0, 0, 0)),
}


def render_views(out, name, lo, hi):
    centre = (lo + hi) / 2
    size = hi - lo
    span = max(size) or 1.0
    made = []
    cam_data = bpy.data.cameras.new("diag_cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = span * 1.15
    # the camera is parked at 3x the model span, well past the default 100 m clip
    cam_data.clip_start = span * 0.001
    cam_data.clip_end = span * 10
    cam = bpy.data.objects.new("diag_cam", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    for view, (offset, rot) in AXIS_VIEWS.items():
        cam.location = centre + offset * span * 3
        cam.rotation_euler = rot
        path = out / f"{name}_{view}.png"
        bpy.context.scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        made.append(path.name)
    return made


def render_highlights(out, name, lo, hi, meshes, pattern):
    """One side view per matching object, painted red against the grey rest."""
    scene = bpy.context.scene
    scene.display.shading.color_type = "OBJECT"
    for obj in meshes:
        obj.color = (0.55, 0.55, 0.55, 1.0)

    centre = (lo + hi) / 2
    span = max(hi - lo) or 1.0
    cam = scene.camera
    cam.location = centre + Vector((1, 0, 0)) * span * 3
    cam.rotation_euler = (math.radians(90), 0, math.radians(90))

    made = []
    for obj in meshes:
        if not pattern.search(obj.name):
            continue
        obj.color = (0.9, 0.1, 0.1, 1.0)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in obj.name)
        path = out / f"{name}_hl_{safe}.png"
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        obj.color = (0.55, 0.55, 0.55, 1.0)
        made.append(path.name)
    return made


def render_highlights(out, name, lo, hi, meshes, pattern):
    """One side view per matching object, painted red against the grey rest."""
    scene = bpy.context.scene
    scene.display.shading.color_type = "OBJECT"
    for obj in meshes:
        obj.color = (0.55, 0.55, 0.55, 1.0)

    centre = (lo + hi) / 2
    span = max(hi - lo) or 1.0
    cam = scene.camera
    cam.location = centre + Vector((1, 0, 0)) * span * 3
    cam.rotation_euler = (math.radians(90), 0, math.radians(90))

    made = []
    for obj in meshes:
        if not pattern.search(obj.name):
            continue
        obj.color = (0.9, 0.1, 0.1, 1.0)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in obj.name)
        path = out / f"{name}_hl_{safe}.png"
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        obj.color = (0.55, 0.55, 0.55, 1.0)
        made.append(path.name)
    return made


def main():
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    if args.blend:
        bpy.ops.wm.open_mainfile(filepath=str(args.blend))
        files = [args.blend]
        scan_dir = args.blend.parent
    else:
        wipe_scene()
        files = sorted(
            p for p in args.source.iterdir() if p.suffix.lower() in MESH_SUFFIXES
        )
        if not files:
            raise SystemExit(f"no mesh files in {args.source}")
        for path in files:
            import_file(path)
        scan_dir = args.source

    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if args.show_hidden:
        for obj in meshes:
            obj.hide_render = False
    else:
        meshes = [o for o in meshes if not o.hide_render]
    lo, hi = world_bbox(meshes)
    size = hi - lo

    loose_textures = sorted(
        p.name
        for p in scan_dir.iterdir()
        if p.is_file()
        and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".tga", ".tif", ".tiff", ".dds"}
    )
    mtl_files = sorted(
        p.name for p in scan_dir.iterdir() if p.is_file() and p.suffix.lower() == ".mtl"
    )

    setup_render(args.res, args.shading)
    previews = render_views(args.out, args.name, lo, hi)

    if args.highlight:
        previews += render_highlights(
            args.out, args.name, lo, hi, meshes, re.compile(args.highlight, re.I)
        )

    if args.highlight:
        previews += render_highlights(
            args.out, args.name, lo, hi, meshes, re.compile(args.highlight, re.I)
        )

    if args.highlight:
        previews += render_highlights(
            args.out, args.name, lo, hi, meshes, re.compile(args.highlight, re.I)
        )

    report = {
        "source": str(args.blend or args.source),
        "files": [p.name for p in files],
        "mtl_files": mtl_files,
        "loose_texture_files": loose_textures,
        "mesh_count": len(meshes),
        "union_bbox_min": [round(v, 5) for v in lo],
        "union_bbox_max": [round(v, 5) for v in hi],
        "union_size": [round(v, 5) for v in size],
        "longest_axis": "XYZ"[max(range(3), key=lambda i: size[i])],
        "objects": describe(meshes),
        "previews": previews,
    }
    (args.out / "inspect-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps({k: report[k] for k in
                      ("mesh_count", "mtl_files", "loose_texture_files",
                       "union_size", "longest_axis", "previews")}, indent=2))


if __name__ == "__main__":
    main()
