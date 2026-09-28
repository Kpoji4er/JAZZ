"""Rigged AK-103 pass: spots, Origin empties, HGE settings, TGA + FBX.

    blender --background --factory-startup --python docs/tools/_export_ak103_assets.py -- \
        --build <_ak103_jazz_build> --game-root <JA3_ROOT> [--assets <jazz_assets>]

Follows _export_ak_assets.py. Entity split mirrors the accepted AKR_AK105:
body, _Handguard, _Magazine, _Muzzle, _Stock, _StockFolded.

Frame: the clean scene has the buttplate at y=0, so it is first shifted to put
the magazine feed lip on the AKM Magazine spot. AK-103 is 7.62x39 and shares
the AKM magazine presets, so its receiver interface has to match AKM's, and the
optics triangle (General/Scope/Mount) is inherited from AKM.ent rather than
re-invented. Everything the geometry actually dictates - muzzle, handguard,
left hand, stock pivot, underbarrel, bipod - is measured on this mesh.
"""

import argparse
import importlib.util
import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Vector

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from _ja3_mesh_prepare import audit_blender_object, prepare_export_mesh

WEAPON = "AK103"
ENTITY = "AKR_" + WEAPON
ATLAS = 2048
# bogdanzloy roughness sits at 0.70-0.77; accepted AK family is 0.34-0.60.
# Inventory lighting then reads as chalky plastic. Scale the packed R channel
# to this mean while keeping the map's own variation. Metallic is unchanged.
ROUGHNESS_TARGET = 0.45

# Optics ride the AKM triangle, re-seated on this receiver's own dovetail.
OPTICS = ("General", "Scope", "Mount")
# Underbarrel hardware keeps its AKM distance from the muzzle spot instead of
# being guessed off the front sight block.
MUZZLE_RELATIVE = ("Under", "Bipod")


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--build", required=True, type=Path)
    p.add_argument("--game-root", required=True, type=Path)
    p.add_argument(
        "--assets",
        type=Path,
        default=Path(__file__).resolve().parents[2].parent / "jazz_assets",
    )
    return p.parse_args(argv)


def load_hge(game_root):
    spec = importlib.util.spec_from_file_location(
        "ak103_hge", game_root / "ModTools/BlenderExport.py"
    )
    hge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hge)
    hge.SETTINGS.update(
        version="71",
        game="Zulu",
        appid="Jagged Alliance 3",
        mtl_prop_0_visible=True,
        mtl_prop_0_name="Unit",
        enable_colliders=True,
    )
    hge.register()
    return hge


def ent_spots(path):
    """HGM centimetres -> Blender metres, per the (-Y,-X,Z) reader convention."""
    spots = {}
    for node in ET.parse(path).findall(".//attach"):
        x, y, z = (float(v) for v in node.attrib["spot_pos"].split(","))
        spots[node.attrib["name"]] = Vector((-y / 100, -x / 100, z / 100))
    return spots


def bounds(obj):
    co = [v.co for v in obj.data.vertices]
    lo = Vector(tuple(min(c[i] for c in co) for i in range(3)))
    hi = Vector(tuple(max(c[i] for c in co) for i in range(3)))
    return lo, hi


def image_from_socket(socket, prefer=None):
    if not socket.links:
        return None
    stack = [socket.links[0].from_node]
    seen = set()
    found = []
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        if node.type == "TEX_IMAGE" and node.image:
            found.append(node.image)
        for inp in node.inputs:
            if inp.links:
                stack.append(inp.links[0].from_node)
    if prefer:
        for im in found:
            if prefer.lower() in im.name.lower():
                return im
    return found[0] if found else None


def weld(obj):
    """Archive OBJ verts are split per face. Smooth shading needs a weld first."""
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.remove_doubles(threshold=1e-4)
    bpy.ops.object.mode_set(mode="OBJECT")


def drop_needles(obj):
    """The Izhmash rip has hairline scribe faces that become weld-spikes."""
    import bmesh

    issues = audit_blender_object(obj)
    kill = {
        issue["triangle"]
        for issue in issues
        if issue["kind"] in {"spike", "degenerate", "zero_normal"}
        and issue["triangle"] is not None
    }
    if not kill:
        return 0
    mesh = obj.data
    mesh.calc_loop_triangles()
    face_ids = {
        mesh.loop_triangles[i].polygon_index
        for i in kill
        if i < len(mesh.loop_triangles)
    }
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.faces.ensure_lookup_table()
    geom = [bm.faces[i] for i in face_ids if i < len(bm.faces)]
    bmesh.ops.delete(bm, geom=geom, context="FACES")
    bm.to_mesh(obj.data)
    obj.data.update()
    bm.free()
    return len(geom)


def feed_lip(mag):
    """Top-centre of the magazine: the receiver interface, not the bbox centre."""
    lo, hi = bounds(mag)
    top = [v.co for v in mag.data.vertices if v.co.z > hi.z - 0.012]
    return Vector((0, sum(v.y for v in top) / len(top), hi.z))


def main():
    args = parse_args()
    hge = load_hge(args.game_root)
    build = args.build
    rigged = build / "rigged"
    rigged.mkdir(parents=True, exist_ok=True)

    bpy.ops.wm.open_mainfile(filepath=str(build / "clean/AK103.blend"))
    akm = ent_spots(args.assets / "Entities/AKM.ent")

    body = bpy.data.objects["AK103"]
    stock = bpy.data.objects["AK103_Stock"]
    hand = bpy.data.objects["AK103_Handguard"]
    mag = bpy.data.objects["AK103_Magazine"]
    muzzle = bpy.data.objects["AK103_Muzzle"]
    meshes = [body, stock, hand, mag, muzzle]

    landmarks = {
        o.name: (Vector(o["bbox_min"]), Vector(o["bbox_max"]))
        for o in bpy.data.objects
        if o.type == "EMPTY" and o.name.startswith("LM_")
    }

    shift = akm["Magazine"] - feed_lip(mag)
    shift.x = 0
    transform = Matrix.Translation(shift)
    for obj in meshes:
        obj.data.transform(transform @ obj.matrix_world)
        obj.matrix_world = Matrix.Identity(4)
    landmarks = {k: (lo + shift, hi + shift) for k, (lo, hi) in landmarks.items()}

    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            bpy.data.objects.remove(obj, do_unlink=True)

    blo, bhi = bounds(body)
    slo, shi = bounds(stock)
    hlo, hhi = bounds(hand)
    mzlo, mzhi = bounds(muzzle)
    bore_lo, bore_hi = landmarks["LM_Bore"]
    bore_z = (bore_lo.z + bore_hi.z) / 2
    trigger_lo, trigger_hi = landmarks["LM_Trigger"]
    rail_lo, rail_hi = landmarks["LM_Rail"]
    rail = (rail_lo + rail_hi) / 2

    muzzle_spot = Vector((0, mzhi.y, (mzlo.z + mzhi.z) / 2))
    hand_mid = (hlo.y + hhi.y) / 2
    side = Vector((-0.025, hand_mid, (hlo.z + hhi.z) / 2))

    spots = {
        "Magazine": feed_lip(mag),
        # rear face of the muzzle device, on the bore axis
        "Muzzle": muzzle_spot,
        "MuzzleTip": Vector((0, mzlo.y, (mzlo.z + mzhi.z) / 2)),
        "Handguard": Vector((0, hand_mid, (hlo.z + hhi.z) / 2)),
        "Hand_l_grip": Vector((0, hand_mid, hlo.z + 0.015)),
        # forward end of the stock: the hinge the folded variant turns on
        "Stock": Vector((-0.02, slo.y + 0.005, (slo.z + shi.z) / 2)),
        "Trigger": Vector(
            (0, (trigger_lo.y + trigger_hi.y) / 2, (trigger_lo.z + trigger_hi.z) / 2)
        ),
        "Barrel": Vector((0, (hlo.y + mzhi.y) / 2, bore_z)),
        "Side": side,
        # Side3 keeps AKM's absolute lateral offset; only the fore-aft and
        # height follow this handguard.
        "Side3": Vector(
            (akm["Side3"].x, side.y + (akm["Side3"].y - akm["Side"].y),
             side.z + (akm["Side3"].z - akm["Side"].z))
        ),
    }
    # This receiver sits a few millimetres lower over the magazine than AKM's,
    # so the optics triangle is translated onto the real dovetail centre.
    seat = Vector((0, rail.y - akm["Mount"].y, rail.z - akm["Mount"].z))
    for name in OPTICS:
        spots[name] = akm[name] + seat
    for name in MUZZLE_RELATIVE:
        spots[name] = muzzle_spot + (akm[name] - akm["Muzzle"])
        spots[name].x = akm[name].x

    entities = {
        ENTITY: body,
        ENTITY + "_Stock": stock,
        ENTITY + "_Handguard": hand,
        ENTITY + "_Magazine": mag,
        ENTITY + "_Muzzle": muzzle,
    }

    textures = build / "Textures"
    textures.mkdir(parents=True, exist_ok=True)
    materials = sorted(
        {m for o in entities.values() for m in o.data.materials if m}, key=lambda m: m.name
    )
    for index, mat in enumerate(materials):
        bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        images = {}
        for key, socket in [
            ("Base", "Base Color"),
            ("Rough", "Roughness"),
            ("Metal", "Metallic"),
            ("Normal", "Normal"),
        ]:
            im = image_from_socket(bsdf.inputs[socket], prefer="Normal" if key == "Normal" else None)
            if im is None:
                continue
            work = im.copy()
            work.colorspace_settings.name = "sRGB" if key == "Base" else "Non-Color"
            work.scale(ATLAS, ATLAS)
            arr = np.empty(ATLAS * ATLAS * 4, np.float32)
            work.pixels.foreach_get(arr)
            images[key] = arr.reshape(-1, 4)
            bpy.data.images.remove(work)
            if key == "Normal":
                # Smart-UV bake of Frostoise normals reads as a pencil hatch
                # under JA3 inspect lighting. Archive geo already has the rivets.
                images[key][:, 0] = 0.5
                images[key][:, 1] = 0.5
                images[key][:, 2] = 1.0
                images[key][:, 3] = 1.0

        rm = np.ones((ATLAS * ATLAS, 4), np.float32)
        rough = images.get("Rough", rm)[:, 0]
        mean = float(rough.mean()) or 1.0
        # Only compress chalky maps. Frostoise already sits in the AK family range.
        if mean > 0.60:
            rough = np.clip(rough * (ROUGHNESS_TARGET / mean), 0.0, 1.0)
        rm[:, 0] = rough
        rm[:, 1] = 0
        rm[:, 2] = images["Metal"][:, 0] if "Metal" in images else 0
        images["RM"] = rm

        mat.name = f"{ENTITY}_{index}"
        paths = {}
        for key in ("Base", "Normal", "RM"):
            if key not in images:
                continue
            im = bpy.data.images.new(
                f"{mat.name}_{key}", width=ATLAS, height=ATLAS, alpha=True
            )
            im.colorspace_settings.name = "sRGB" if key == "Base" else "Non-Color"
            im.pixels.foreach_set(images[key].ravel())
            im.filepath_raw = str(textures / (im.name + ".tga"))
            im.file_format = "TARGA_RAW"
            im.save()
            paths[key] = im.filepath_raw

        hge.add_material_props(mat)
        for prop in hge.MATERIAL_PROPERTIES:
            if not prop.settings_name:
                continue
            key = {
                "base_color": "Base",
                "normal_map": "Normal",
                "roughness_metallic_map": "RM",
            }.get(prop.settings_name)
            if key in paths:
                mat[prop.id] = paths[key]
            elif prop.map:
                mat[prop.id] = ""
            else:
                mat[prop.id] = getattr(mat.hgm_settings, prop.settings_name)

    for name, obj in entities.items():
        obj.name = name
        obj.data.name = name + "_Mesh"
        weld(obj)
        for _ in range(4):
            if drop_needles(obj) == 0:
                break
        prepare_export_mesh(obj)

        pivot = Vector() if obj is body else spots[name.rsplit("_", 1)[1]]
        origin = bpy.data.objects.new(name + "_Origin", None)
        bpy.context.collection.objects.link(origin)
        origin.location = pivot
        obj.data.transform(Matrix.Translation(-pivot))
        obj.parent = origin
        obj.location = Vector()

        settings = obj.hge_obj_settings
        settings.entity = name
        settings.mesh = "Mesh"
        settings.state = "idle"
        settings.lod = 1
        settings.ignore = False
        obj.hge_export = True

    folded = stock.copy()
    folded.data = stock.data.copy()
    folded.name = ENTITY + "_StockFolded"
    bpy.context.collection.objects.link(folded)
    folded.data.transform(Matrix.Rotation(math.pi, 4, "Z"))
    folded.hge_obj_settings.entity = folded.name
    folded.hide_render = True
    entities[folded.name] = folded

    for name, point in spots.items():
        empty = bpy.data.objects.new(name, None)
        bpy.context.collection.objects.link(empty)
        empty.parent = body
        empty.location = point
        empty.hge_obj_settings.spot_name = name

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1

    blend_path = rigged / f"{WEAPON}_JA3.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    with hge.ObjectNamesExportContext(bpy.context):
        bpy.ops.export_scene.fbx(
            filepath=str(rigged / f"{WEAPON}_JA3.fbx"),
            axis_forward="Y",
            axis_up="Z",
            apply_scale_options="FBX_SCALE_ALL",
            object_types={"MESH", "EMPTY"},
            use_custom_props=True,
            add_leaf_bones=False,
            bake_anim=False,
        )

    report = {
        "blend": str(blend_path),
        "fbx": str(rigged / f"{WEAPON}_JA3.fbx"),
        "frame_shift_m": [round(v, 5) for v in shift],
        "entities": sorted(entities),
        "materials": [m.name for m in materials],
        "spots_m": {n: [round(v, 5) for v in p] for n, p in sorted(spots.items())},
        "akm_reference_m": {n: [round(v, 5) for v in p] for n, p in sorted(akm.items())},
    }
    (build / "export-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
