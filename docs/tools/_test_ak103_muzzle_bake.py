"""One-module bake experiments. Prints Base mean so we know the rays hit."""

import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

clean, donor_path = (Path(p) for p in sys.argv[sys.argv.index("--") + 1:][:2])
bpy.ops.wm.open_mainfile(filepath=str(clean))

target = bpy.data.objects["AK103_Muzzle"]
bpy.ops.object.select_all(action="DESELECT")
target.select_set(True)
bpy.context.view_layer.objects.active = target
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode="OBJECT")

before = set(bpy.data.objects)
with bpy.data.libraries.load(str(donor_path), link=False) as (src, dst):
    dst.objects = [n for n in src.objects if n.startswith("AK103")]
donors = []
for obj in bpy.data.objects:
    if obj in before or obj.type != "MESH" or not obj.name.startswith("AK103"):
        continue
    bpy.context.scene.collection.objects.link(obj)
    obj.hide_render = False
    donors.append(obj)
donor = next(o for o in donors if "Muzzle" in o.name)

# Seat + grow the donor so rays leaving the archive mesh must hit it.
t_lo = Vector(target.bound_box[0])
# centre align
tc = sum((target.matrix_world @ Vector(c) for c in target.bound_box), Vector()) / 8
dc = sum((donor.matrix_world @ Vector(c) for c in donor.bound_box), Vector()) / 8
donor.location += tc - dc
donor.scale *= 1.04
bpy.context.view_layer.update()

# Drive donor materials with Emission from their Base Color.
for obj in donors:
    for mat in obj.data.materials:
        if not mat or not mat.use_nodes:
            continue
        nodes, links = mat.node_tree.nodes, mat.node_tree.links
        bsdf = next((n for n in nodes if n.type == "BSDF_PRINCIPLED"), None)
        out = next((n for n in nodes if n.type == "OUTPUT_MATERIAL"), None)
        if not bsdf or not out:
            continue
        emit = nodes.new("ShaderNodeEmission")
        emit.inputs["Strength"].default_value = 1
        if bsdf.inputs["Base Color"].links:
            src = bsdf.inputs["Base Color"].links[0].from_socket
            links.new(src, emit.inputs["Color"])
        else:
            emit.inputs["Color"].default_value = bsdf.inputs["Base Color"].default_value
        for link in list(out.inputs["Surface"].links):
            links.remove(link)
        links.new(emit.outputs["Emission"], out.inputs["Surface"])

mat = target.data.materials[0]
maps = {n.label: n for n in mat.node_tree.nodes if n.type == "TEX_IMAGE" and n.label}
# break circular deps
for link in list(mat.node_tree.links):
    if link.from_node.type in {"TEX_IMAGE", "NORMAL_MAP"}:
        mat.node_tree.links.remove(link)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 4
scene.render.bake.use_selected_to_active = True
scene.render.bake.use_cage = False
scene.render.bake.max_ray_distance = 0.0
scene.render.bake.margin = 8
scene.render.bake.use_clear = True

mat.node_tree.nodes.active = maps["Base"]
for node in maps.values():
    node.select = node.label == "Base"
bpy.ops.object.select_all(action="DESELECT")
for obj in donors:
    obj.select_set(True)
target.select_set(True)
bpy.context.view_layer.objects.active = target
print("baking emit", flush=True)
bpy.ops.object.bake(type="EMIT", use_clear=True)

pix = [0.0] * (2048 * 2048 * 4)
maps["Base"].image.pixels.foreach_get(pix)
mean = sum(pix[i] + pix[i + 1] + pix[i + 2] for i in range(0, len(pix), 4)) / (2048 * 2048 * 3)
hit = sum(1 for i in range(0, len(pix), 4) if pix[i] + pix[i + 1] + pix[i + 2] > 0.05)
print(json.dumps({"mean": round(mean, 5), "hit_px": hit, "donors": [o.name for o in donors]}))
