"""Rebake Frostoise PBR onto the already-assembled archive AK-103.

The first archive pass hid the donor from Cycles, so the 2048 maps stayed
empty. This opens the current clean blend, appends the Frostoise donor
visible, seats each module on its counterpart, and writes new maps in place.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ATLAS = 2048
EMIT_JOBS = (("Base", "Base Color"), ("Rough", "Roughness"), ("Metal", "Metallic"))


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--clean", required=True, type=Path)
    p.add_argument("--donor", required=True, type=Path)
    p.add_argument("--build", required=True, type=Path)
    p.add_argument("--render", action="store_true")
    p.add_argument("--only", action="append", default=[])
    return p.parse_args(argv)


def world_bbox(obj):
    lo = Vector((math.inf,) * 3)
    hi = Vector((-math.inf,) * 3)
    for corner in obj.bound_box:
        p = obj.matrix_world @ Vector(corner)
        for i in range(3):
            lo[i] = min(lo[i], p[i])
            hi[i] = max(hi[i], p[i])
    return lo, hi


def centre(obj):
    lo, hi = world_bbox(obj)
    return (lo + hi) / 2


def image_nodes(obj):
    mat = obj.data.materials[0]
    found = {}
    for node in mat.node_tree.nodes:
        if node.type == "TEX_IMAGE" and node.image and node.label:
            found[node.label] = node
    return mat, found


def fresh_images(maps):
    for key, node in maps.items():
        old = node.image
        im = bpy.data.images.new(f"{node.image.name}_bake", ATLAS, ATLAS, alpha=True)
        im.colorspace_settings.name = "sRGB" if key == "Base" else "Non-Color"
        node.image = im
        if old and old.users == 0:
            bpy.data.images.remove(old)


def append_donors(path):
    before = set(bpy.data.objects)
    with bpy.data.libraries.load(str(path), link=False) as (src, dst):
        dst.objects = [n for n in src.objects if n.startswith("AK103")]
    donors = []
    for obj in bpy.data.objects:
        if obj in before or obj.type != "MESH" or not obj.name.startswith("AK103"):
            continue
        if obj.name not in bpy.context.scene.collection.objects:
            bpy.context.scene.collection.objects.link(obj)
        obj.hide_render = False
        obj.hide_viewport = False
        obj.hide_set(False)
        donors.append(obj)
    return donors


def match_donor(target, donors):
    key = target.name.replace("AK103", "").lstrip("_") or "Body"
    for obj in donors:
        name = obj.name.split(".", 1)[0]
        other = name.replace("AK103", "").lstrip("_") or "Body"
        if other == key:
            return obj
    return None


def unlink_maps(mat):
    links = mat.node_tree.links
    kill = [
        link
        for link in links
        if link.from_node.type in {"TEX_IMAGE", "NORMAL_MAP"}
    ]
    for link in kill:
        links.remove(link)


def relink_maps(mat, maps):
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = next(n for n in nodes if n.type == "BSDF_PRINCIPLED")
    links.new(maps["Base"].outputs["Color"], bsdf.inputs["Base Color"])
    links.new(maps["Rough"].outputs["Color"], bsdf.inputs["Roughness"])
    if "Metal" in maps:
        links.new(maps["Metal"].outputs["Color"], bsdf.inputs["Metallic"])
    else:
        bsdf.inputs["Metallic"].default_value = 0.15
    nmap = next((n for n in nodes if n.type == "NORMAL_MAP"), None)
    if nmap is None:
        nmap = nodes.new("ShaderNodeNormalMap")
    links.new(maps["Normal"].outputs["Color"], nmap.inputs["Color"])
    links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])


def set_donor_emit(donors, socket_name):
    for obj in donors:
        for mat in obj.data.materials:
            if not mat or not mat.use_nodes:
                continue
            nodes, links = mat.node_tree.nodes, mat.node_tree.links
            bsdf = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)
            out = next((n for n in nodes if n.type == "OUTPUT_MATERIAL"), None)
            if not bsdf or not out:
                continue
            emit = next((n for n in nodes if n.type == "EMISSION" and n.label == "JAZZ_BAKE"), None)
            if emit is None:
                emit = nodes.new("ShaderNodeEmission")
                emit.label = "JAZZ_BAKE"
            emit.inputs["Strength"].default_value = 1
            for link in list(emit.inputs["Color"].links):
                links.remove(link)
            src = bsdf.inputs[socket_name]
            if src.links:
                links.new(src.links[0].from_socket, emit.inputs["Color"])
            elif src.type == "RGBA":
                emit.inputs["Color"].default_value = src.default_value
            else:
                value = src.default_value
                emit.inputs["Color"].default_value = (value, value, value, 1)
            for link in list(out.inputs["Surface"].links):
                links.remove(link)
            links.new(emit.outputs["Emission"], out.inputs["Surface"])


def restore_donor_surface(donors):
    for obj in donors:
        for mat in obj.data.materials:
            if not mat or not mat.use_nodes:
                continue
            nodes, links = mat.node_tree.nodes, mat.node_tree.links
            bsdf = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)
            out = next((n for n in nodes if n.type == "OUTPUT_MATERIAL"), None)
            if not bsdf or not out:
                continue
            for link in list(out.inputs["Surface"].links):
                links.remove(link)
            links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])


def normals_out(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")


def seat_donors(targets, donors):
    for target in targets:
        donor = match_donor(target, donors)
        if donor is None:
            continue
        donor.location += centre(target) - centre(donor)
        donor.scale *= 1.03
    bpy.context.view_layer.update()


def activate_map(mat, maps, key):
    for node in maps.values():
        node.select = node.label == key
    mat.node_tree.nodes.active = maps[key]


def bake_module(target, donors, maps):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 4
    scene.render.bake.use_cage = False
    scene.render.bake.max_ray_distance = 0.0
    scene.render.bake.margin = 8
    mat, _ = image_nodes(target)
    unlink_maps(mat)
    fresh_images(maps)
    for key, socket in EMIT_JOBS:
        if key not in maps:
            continue
        set_donor_emit(donors, socket)
        scene.render.bake.use_selected_to_active = True
        activate_map(mat, maps, key)
        bpy.ops.object.select_all(action="DESELECT")
        for donor in donors:
            donor.select_set(True)
        target.select_set(True)
        bpy.context.view_layer.objects.active = target
        print("bake", target.name, "EMIT", key, flush=True)
        bpy.ops.object.bake(type="EMIT", use_clear=True)
    restore_donor_surface(donors)
    scene.render.bake.use_selected_to_active = True
    activate_map(mat, maps, "Normal")
    bpy.ops.object.select_all(action="DESELECT")
    for donor in donors:
        donor.select_set(True)
    target.select_set(True)
    bpy.context.view_layer.objects.active = target
    print("bake", target.name, "NORMAL", flush=True)
    bpy.ops.object.bake(type="NORMAL", use_clear=True)
    scene.render.bake.use_selected_to_active = False
    activate_map(mat, maps, "AO")
    bpy.ops.object.select_all(action="DESELECT")
    target.select_set(True)
    bpy.context.view_layer.objects.active = target
    print("bake", target.name, "AO", flush=True)
    bpy.ops.object.bake(type="AO", use_clear=True)
    maps["Base"].image.update()
    maps["AO"].image.update()
    mix_ao(maps["Base"].image, maps["AO"].image)
    relink_maps(mat, maps)


def mix_ao(base, ao):
    px = [0.0] * (ATLAS * ATLAS * 4)
    ap = [0.0] * (ATLAS * ATLAS * 4)
    base.pixels.foreach_get(px)
    ao.pixels.foreach_get(ap)
    for i in range(0, len(px), 4):
        shade = 0.72 + 0.28 * ap[i]
        px[i] *= shade
        px[i + 1] *= shade
        px[i + 2] *= shade
    base.pixels.foreach_set(px)
    base.update()


def render_beauty(out, objects, res=1800):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = res
    scene.render.resolution_y = res // 2
    scene.render.film_transparent = True
    scene.view_settings.view_transform = "Standard"
    lo, hi = Vector((math.inf,) * 3), Vector((-math.inf,) * 3)
    for obj in objects:
        a, b = world_bbox(obj)
        for i in range(3):
            lo[i] = min(lo[i], a[i])
            hi[i] = max(hi[i], b[i])
    centre_pt = (lo + hi) / 2
    span = max(hi - lo)
    cam_data = bpy.data.cameras.new("beauty_cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = span * 1.12
    cam_data.clip_end = span * 10
    cam = bpy.data.objects.new("beauty_cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    cam.location = centre_pt + Vector((-1, 0, 0)) * span * 3
    cam.rotation_euler = (math.radians(90), 0, math.radians(-90))
    light = bpy.data.objects.new("beauty_sun", bpy.data.lights.new("beauty_sun", "SUN"))
    scene.collection.objects.link(light)
    light.data.energy = 4
    light.rotation_euler = (math.radians(50), 0, math.radians(-40))
    path = out / "AK103_archive_textured_side.png"
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    return path.name


def main():
    args = parse_args()
    bpy.ops.wm.open_mainfile(filepath=str(args.clean))
    targets = [
        bpy.data.objects[name]
        for name in ("AK103_Magazine", "AK103_Stock", "AK103_Muzzle", "AK103_Handguard", "AK103")
        if not args.only or name in args.only
    ]
    donors = append_donors(args.donor)
    if not donors:
        raise SystemExit("no donor meshes appended")
    for target in targets:
        normals_out(target)
    seat_donors(targets, donors)
    dest = args.build / "Textures" / "archive_bake"
    dest.mkdir(parents=True, exist_ok=True)
    report = {"donor": str(args.donor), "modules": {}}
    for target in targets:
        _mat, maps = image_nodes(target)
        bake_module(target, donors, maps)
        donor = match_donor(target, donors)
        stats = {}
        for key, node in maps.items():
            node.image.pack()
            node.image.filepath_raw = str(dest / f"{target.name}_{key}.png")
            node.image.file_format = "PNG"
            node.image.save()
            pix = [0.0] * (ATLAS * ATLAS * 4)
            node.image.pixels.foreach_get(pix)
            nonempty = sum(1 for i in range(0, len(pix), 4) if pix[i] + pix[i + 1] + pix[i + 2] > 0.05)
            stats[key] = {
                "bytes": (dest / f"{target.name}_{key}.png").stat().st_size,
                "nonempty_px": nonempty,
            }
        report["modules"][target.name] = {"donor": donor.name, "maps": stats}
        print(target.name, stats, flush=True)
    for donor in donors:
        bpy.data.objects.remove(donor, do_unlink=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(args.clean))
    if args.render:
        report["preview"] = render_beauty(args.build / "diag" / "clean", targets)
    (args.build / "rebake-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
