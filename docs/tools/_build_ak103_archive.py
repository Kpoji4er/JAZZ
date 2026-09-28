"""Build AK-103 from the owner's archive mesh, textures baked from Frostoise.

    blender --background --factory-startup --python docs/tools/_build_ak103_archive.py -- \
        --source <_ak103_jazz_build/source> \
        --donor  <_ak103_jazz_build/clean/AK103_frostoise.blend> \
        --build  <_ak103_jazz_build> [--render]

The archive is the Andruxa-snajper rip: high-detail OBJ parts, each duplicated
as an exploded diagram. Keep the assembled cluster (island centroid Z < 20),
drop the exploded copy, group into the AKR_AK105 modules, then project
Frostoise PBR onto new per-module UVs. Geometry stays archive; maps are CC-BY.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

REAL_LENGTH_M = 0.943
EXPLODED_Z = 20.0
ATLAS = 2048

MODULES = {
    "Magazine": ["model_5"],
    "Stock": ["model_12"],
    "Muzzle": ["model_6"],
    "Handguard": ["model_2", "model_7", "model_8"],
}

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
    p.add_argument("--source", required=True, type=Path)
    p.add_argument("--donor", required=True, type=Path)
    p.add_argument("--build", required=True, type=Path)
    p.add_argument("--render", action="store_true")
    p.add_argument("--res", type=int, default=1600)
    return p.parse_args(argv)


def select_only(objects):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        if obj.name in bpy.data.objects:
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


def drop_exploded(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    remaining = set(bm.faces)
    kill = []
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
        zs = [(obj.matrix_world @ v.co).z for f in group for v in f.verts]
        if sum(zs) / len(zs) > EXPLODED_Z:
            kill.extend(group)
    if kill:
        bmesh.ops.delete(bm, geom=kill, context="FACES")
        bm.to_mesh(obj.data)
        obj.data.update()
    bm.free()


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


def import_assembled(source):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    meshes = []
    for path in sorted(source.glob("model_*.obj")):
        bpy.ops.wm.obj_import(filepath=str(path))
        obj = bpy.context.view_layer.objects.active
        drop_exploded(obj)
        if len(obj.data.polygons) == 0:
            bpy.data.objects.remove(obj, do_unlink=True)
            continue
        meshes.append(obj)
    return meshes


def orient_and_scale(objects):
    apply_transforms(objects)
    # +X is muzzle in the archive. JAZZ wants -Y forward.
    empty = bpy.data.objects.new("pivot", None)
    bpy.context.scene.collection.objects.link(empty)
    for obj in objects:
        obj.parent = empty
    empty.rotation_euler = (0, 0, math.radians(-90))
    bpy.context.view_layer.update()
    for obj in objects:
        matrix = obj.matrix_world.copy()
        obj.parent = None
        obj.matrix_world = matrix
    bpy.data.objects.remove(empty)
    apply_transforms(objects)
    lo, hi = world_bbox(objects)
    raw = hi.y - lo.y
    factor = REAL_LENGTH_M / raw
    for obj in objects:
        obj.scale *= factor
    apply_transforms(objects)
    return raw, factor


def zero_at_butt(objects):
    lo, hi = world_bbox(objects)
    offset = Vector((-(lo.x + hi.x) / 2, -hi.y, -(lo.z + hi.z) / 2))
    for obj in objects:
        obj.location += offset
    apply_transforms(objects)
    return offset


def group_modules(meshes):
    by_name = {o.name: o for o in meshes}
    assigned = {}
    taken = set()
    for module, names in MODULES.items():
        members = [by_name[n] for n in names if n in by_name]
        missing = [n for n in names if n not in by_name]
        if missing:
            raise SystemExit(f"{module}: missing {missing}")
        assigned[module] = members
        taken.update(members)
    assigned["Body"] = [o for o in meshes if o not in taken]
    joined = {}
    for module, members in assigned.items():
        name = "AK103" if module == "Body" else f"AK103_{module}"
        joined[module] = join_named(members, name, MODULE_COLOURS[module])
    return joined


def unwrap(obj):
    select_only([obj])
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=1.15192, island_margin=0.002)
    bpy.ops.object.mode_set(mode="OBJECT")


def make_image(name, color=(0.5, 0.5, 0.5, 1)):
    im = bpy.data.images.new(name, width=ATLAS, height=ATLAS, alpha=True)
    im.generated_color = color
    return im


def setup_target_material(obj):
    mat = bpy.data.materials.new(obj.name + "_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    maps = {}
    for key, color in (
        ("Base", (0.12, 0.12, 0.12, 1)),
        ("Normal", (0.5, 0.5, 1, 1)),
        ("Rough", (0.45, 0.45, 0.45, 1)),
        ("Metal", (0, 0, 0, 1)),
        ("AO", (1, 1, 1, 1)),
    ):
        im = make_image(f"{obj.name}_{key}", color)
        tex = nodes.new("ShaderNodeTexImage")
        tex.image = im
        tex.label = key
        maps[key] = tex
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return mat, maps


def feed_lip(obj):
    lo, hi = world_bbox([obj])
    pts = []
    for v in obj.data.vertices:
        p = obj.matrix_world @ v.co
        if p.z > hi.z - 0.012:
            pts.append(p)
    if not pts:
        return Vector((0, (lo.y + hi.y) / 2, hi.z))
    return Vector((0, sum(p.y for p in pts) / len(pts), hi.z))


def append_donor(path):
    before = set(bpy.data.objects)
    with bpy.data.libraries.load(str(path), link=False) as (src, dst):
        dst.objects = [n for n in src.objects if n.startswith("AK103")]
    donors = []
    for obj in bpy.data.objects:
        if obj in before:
            continue
        if obj.name.startswith("AK103"):
            bpy.context.scene.collection.objects.link(obj)
            obj.hide_render = False
            obj.hide_viewport = False
            donors.append(obj)
    return donors


def bake_maps(target, donors, maps):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 8
    scene.render.bake.use_selected_to_active = True
    scene.render.bake.margin = 8
    scene.render.bake.cage_extrusion = 0.025
    scene.render.bake.max_ray_distance = 0.08
    jobs = [
        ("Base", "DIFFUSE", {"use_pass_direct": False, "use_pass_indirect": False, "use_pass_color": True}),
        ("Normal", "NORMAL", {}),
        ("Rough", "ROUGHNESS", {}),
        ("AO", "AO", {}),
    ]
    for key, btype, flags in jobs:
        for node in maps.values():
            node.select = node.label == key
        bpy.context.view_layer.objects.active = target
        bpy.ops.object.select_all(action="DESELECT")
        for donor in donors:
            donor.select_set(True)
        target.select_set(True)
        bake = scene.render.bake
        bake.use_pass_direct = flags.get("use_pass_direct", False)
        bake.use_pass_indirect = flags.get("use_pass_indirect", False)
        bake.use_pass_color = flags.get("use_pass_color", True)
        target.data.materials[0].node_tree.nodes.active = maps[key]
        print("bake", target.name, key, flush=True)
        bpy.ops.object.bake(type=btype, use_clear=True)
    # Metallic is not a bake type on all builds; sample from donor DIFFUSE is enough
    # for polymer/metal split. Copy roughness as a stand-in then darken later if needed.
    # Mix AO into albedo so the high-poly cavities read in inventory lighting.
    base = maps["Base"].image
    ao = maps["AO"].image
    px = [0.0] * (ATLAS * ATLAS * 4)
    ap = [0.0] * (ATLAS * ATLAS * 4)
    base.pixels.foreach_get(px)
    ao.pixels.foreach_get(ap)
    for i in range(0, len(px), 4):
        shade = 0.45 + 0.55 * ap[i]
        px[i] *= shade
        px[i + 1] *= shade
        px[i + 2] *= shade
    base.pixels.foreach_set(px)
    bsdf = next(n for n in target.data.materials[0].node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    links = target.data.materials[0].node_tree.links
    links.new(maps["Base"].outputs["Color"], bsdf.inputs["Base Color"])
    links.new(maps["Rough"].outputs["Color"], bsdf.inputs["Roughness"])
    nmap = target.data.materials[0].node_tree.nodes.new("ShaderNodeNormalMap")
    links.new(maps["Normal"].outputs["Color"], nmap.inputs["Color"])
    links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    # Archive geo is mostly polymer furniture + painted steel. A low metallic
    # keeps inventory lighting from chalking the way the first import did.
    bsdf.inputs["Metallic"].default_value = 0.15


def place_landmarks(modules):
    body = modules["Body"]
    mag = modules["Magazine"]
    hand = modules["Handguard"]
    muzzle = modules["Muzzle"]
    blo, bhi = world_bbox([body])
    mlo, mhi = world_bbox([mag])
    hlo, hhi = world_bbox([hand])
    zlo, zhi = world_bbox([muzzle])
    marks = {
        "LM_Grip": {"source": "Body_rear", "min": [blo.x, (blo.y + bhi.y) * 0.35, blo.z], "max": [bhi.x, (blo.y + bhi.y) * 0.45, (blo.z + bhi.z) * 0.4]},
        "LM_Trigger": {"source": "Mag_well", "min": [mlo.x, mhi.y - 0.02, mhi.z - 0.02], "max": [mhi.x, mhi.y, mhi.z]},
        "LM_Rail": {"source": "Receiver_left", "min": [blo.x, (blo.y + bhi.y) * 0.45, bhi.z - 0.03], "max": [blo.x + 0.01, (blo.y + bhi.y) * 0.7, bhi.z]},
        "LM_Bore": {"source": "Barrel", "min": [ -0.01, hhi.y, (zlo.z + zhi.z) / 2 - 0.01], "max": [0.01, zlo.y, (zlo.z + zhi.z) / 2 + 0.01]},
        "LM_FrontSight": {"source": "Muzzle_top", "min": [-0.01, zlo.y + 0.02, zhi.z - 0.01], "max": [0.01, zlo.y + 0.06, zhi.z]},
    }
    for label, data in marks.items():
        lo, hi = Vector(data["min"]), Vector(data["max"])
        empty = bpy.data.objects.new(label, None)
        empty.empty_display_size = 0.01
        empty.location = (lo + hi) / 2
        empty["bbox_min"] = list(lo)
        empty["bbox_max"] = list(hi)
        bpy.context.scene.collection.objects.link(empty)
        data["min"] = [round(v, 6) for v in lo]
        data["max"] = [round(v, 6) for v in hi]
    return marks


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
    return made


def main():
    args = parse_args()
    clean_dir = args.build / "clean"
    diag_dir = args.build / "diag" / "clean"
    clean_dir.mkdir(parents=True, exist_ok=True)
    diag_dir.mkdir(parents=True, exist_ok=True)

    current = clean_dir / "AK103.blend"
    frostoise_backup = clean_dir / "AK103_frostoise.blend"
    if current.is_file() and not frostoise_backup.is_file():
        current.replace(frostoise_backup)
    donor_path = args.donor
    if not donor_path.is_file() and frostoise_backup.is_file():
        donor_path = frostoise_backup

    meshes = import_assembled(args.source)
    raw, factor = orient_and_scale(meshes)
    modules = group_modules(meshes)
    objects = list(modules.values())
    offset = zero_at_butt(objects)
    for obj in objects:
        unwrap(obj)

    donors = append_donor(donor_path)
    if modules.get("Magazine") and any("Magazine" in o.name for o in donors):
        donor_mag = next(o for o in donors if "Magazine" in o.name)
        shift = feed_lip(donor_mag) - feed_lip(modules["Magazine"])
        shift.x = 0
        for obj in objects:
            obj.location += shift
        apply_transforms(objects)
        offset = offset + shift

    for obj in objects:
        mat, maps = setup_target_material(obj)
        bake_maps(obj, donors, maps)
        dest = args.build / "Textures" / "archive_bake"
        dest.mkdir(parents=True, exist_ok=True)
        for key, node in maps.items():
            node.image.filepath_raw = str(dest / f"{obj.name}_{key}.png")
            node.image.file_format = "PNG"
            node.image.save()

    for donor in donors:
        bpy.data.objects.remove(donor, do_unlink=True)

    landmarks = place_landmarks(modules)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1
    lo, hi = world_bbox(objects)
    report = {
        "source": str(args.source),
        "donor": str(donor_path),
        "source_raw_length_units": round(raw, 4),
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
