"""Bind the clean 6B3 vest to the official Male sample and join one export mesh.

Blender --background --python this.py -- --sample <BlenderScene_Appearance.blend>
  --clean <JazzArmor_6B3.blend> --output <folder or .blend>

Keeps the sample body and armature for pose QA. Writes TEST_6B3 with at most
four normalized influences. Does not bake, export or install.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
from mathutils.kdtree import KDTree

p = argparse.ArgumentParser()
p.add_argument('--sample', type=Path, required=True)
p.add_argument('--clean', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--shirt', type=Path, help='Decoded actual Legion shirt; use its native skin')
p.add_argument('--reference', type=Path, help='Preserved cuirass v7 source for lower torso skin')
p.add_argument('--native-only', action='store_true', help='Use actual shirt skin throughout; still validate the v7 skeleton')
p.add_argument('--surface-skin', action='store_true', help='Blend local barycentric shirt transfer with a bounded seam smoothing field')
p.add_argument('--item', default='6B3', help='Armor suffix for a new clean source, e.g. LeatherArmor')
p.add_argument('--torso-carrier', action='store_true', help='Sample native front/back torso weights below the shoulder straps, excluding nearby sleeves')
p.add_argument('--torso-shoulders', action='store_true', help='Continue torso-carrier weights across shoulder straps; exclude arm and clavicle motion')
p.add_argument('--preserve-uv', action='store_true', help='Copy the existing single-mesh atlas instead of packing new UV islands')
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
assert not a.torso_shoulders or a.torso_carrier, '--torso-shoulders requires --torso-carrier'
out = a.output.resolve()
blend = out if out.suffix.lower() == '.blend' else out / (a.item + '.blend')
blend.parent.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=str(a.sample.resolve()))
rig = bpy.data.objects['Bip001']
body = bpy.data.objects['M_BaseMesh Skin_BIP']
for obj in list(bpy.data.objects):
    if obj not in (rig, body) and obj.type == 'MESH':
        bpy.data.objects.remove(obj, do_unlink=True)
for collection in bpy.data.collections:
    collection.hide_render = False
    collection.hide_viewport = False
body.hide_set(False)
body.hide_render = False
rig.hide_set(False)

body.data.calc_loop_triangles()
bind_vertices = [body.matrix_world @ v.co for v in body.data.vertices]
bind_triangles = [tuple(t.vertices) for t in body.data.loop_triangles]
bind_bvh = BVHTree.FromPolygons(bind_vertices, bind_triangles, all_triangles=True)
native_weights = None
if a.shirt:
    data = json.loads(a.shirt.read_text())
    shirt = data['meshes'][1]; box = shirt.get('bbox') or data['bbox']
    centre = [(box[i] + box[i+3]) / 2 for i in range(3)]
    bind_vertices = [Vector((-(v[1]+centre[1]), -(v[0]+centre[0]), v[2]+centre[2])) for v in shirt['vertices']]
    bind_triangles = [tuple(f) for f in shirt['faces']]
    # HGM's synthetic Bip001 object entry is not a deform bone in the developer rig.
    # Omit that small root influence and normalize actual bones during interpolation.
    native_weights = [{data['bones'][i]['name']:w for i,w in zip(ids,weights) if w>0 and data['bones'][i]['name']!='Bip001'}
                      for ids,weights in zip(shirt['bone_indices'],shirt['bone_weights'])]
    assert all(n in rig.data.bones for weights in native_weights for n in weights), sorted({n for w in native_weights for n in w if n not in rig.data.bones})
    bind_bvh = BVHTree.FromPolygons(bind_vertices, bind_triangles, all_triangles=True)
    shirt_points=KDTree(len(bind_vertices))
    for index,pos in enumerate(bind_vertices):shirt_points.insert(pos,index)
    shirt_points.balance()
reference_plate = None
if a.reference:
    with bpy.data.libraries.load(str(a.reference),link=False) as (src,dst):
        dst.objects=['TEST_ImprovisedCuirass_Male_v7','Bip001']
    reference_plate, reference_rig = dst.objects
    assert reference_plate and reference_rig
    assert max(abs(x-y) for b in rig.data.bones
               for row,other in zip(b.matrix_local,reference_rig.data.bones[b.name].matrix_local)
               for x,y in zip(row,other)) < 1e-5
    reference_plate.data.calc_loop_triangles()
    plate_vertices=[reference_plate.matrix_world@v.co for v in reference_plate.data.vertices]
    plate_faces=[tuple(t.vertices) for t in reference_plate.data.loop_triangles]
    plate_bvh=BVHTree.FromPolygons(plate_vertices,plate_faces,all_triangles=True)
    bpy.data.objects.remove(reference_rig,do_unlink=True)


def sample_bind(pos):
    if native_weights is not None and a.surface_skin:
        # A 20 mm surface neighbourhood makes the nearest-triangle field
        # continuous across garment seams without the old 100 mm vertex search.
        weights = {}
        for delta in ((0, 0, 0), (.020, 0, 0), (-.020, 0, 0),
                      (0, .020, 0), (0, -.020, 0), (0, 0, .020), (0, 0, -.020)):
            co, _, index, _ = bind_bvh.find_nearest(Vector(pos) + Vector(delta))
            ids = bind_triangles[index]
            bary = barycentric_transform(co, *[bind_vertices[i] for i in ids],
                                         Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)))
            for idx, factor in zip(ids, bary):
                for name, weight in native_weights[idx].items():
                    weights[name] = weights.get(name, 0) + max(0, factor) * weight
        weights = dict(sorted(weights.items(), key=lambda item: item[1], reverse=True)[:4])
        total = sum(weights.values())
        assert total > 0
        surface = {name: weight / total for name, weight in weights.items() if weight > 1e-10}
        local_weights = {}
        surface_pos = bind_bvh.find_nearest(Vector(pos))[0]
        # Search on the garment, not around the raised pouch surface. Otherwise
        # thick parts suddenly switch to the sparse fallback neighbour set.
        nearby = shirt_points.find_range(surface_pos, .08)
        if not nearby:
            nearby = shirt_points.find_n(surface_pos, 12)
        for _, idx, distance in nearby:
            factor = math.exp(-.5 * (distance / .028) ** 2)
            for name, weight in native_weights[idx].items():
                local_weights[name] = local_weights.get(name, 0) + weight * factor
        local_total = sum(local_weights.values())
        assert local_total > 0
        return mix_bind(surface, {n: w / local_total for n, w in local_weights.items()}, .85)
    if native_weights is not None and not a.surface_skin:
        # A compact smooth field avoids abrupt nearest-triangle changes across
        # disconnected clothing seams and across layered vest/pouch surfaces.
        weights={}
        nearby=shirt_points.find_range(Vector(pos),.10)
        if not nearby:nearby=shirt_points.find_n(Vector(pos),12)
        for _,idx,distance in nearby:
            factor=math.exp(-.5*(distance/.028)**2)
            for name,weight in native_weights[idx].items():
                weights[name]=weights.get(name,0)+weight*factor
        weights=dict(sorted(weights.items(),key=lambda pair:pair[1],reverse=True)[:4])
        total=sum(weights.values());assert total>0
        return {name:weight/total for name,weight in weights.items() if weight>1e-10}
    co, normal, index, distance = bind_bvh.find_nearest(Vector(pos))
    ids = bind_triangles[index]
    abc = [bind_vertices[i] for i in ids]
    bary = barycentric_transform(co, *abc, Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)))
    weights = {}
    for idx, factor in zip(ids, bary):
        if native_weights is not None:
            for name, weight in native_weights[idx].items():
                if factor>0:weights[name]=weights.get(name,0)+factor*weight
            continue
        for group in body.data.vertices[idx].groups:
            name = body.vertex_groups[group.group].name
            if name in rig.data.bones and factor > 0:
                weights[name] = weights.get(name, 0) + factor * group.weight
    weights = dict(sorted(weights.items(), key=lambda item: item[1], reverse=True)[:4])
    total = sum(weights.values())
    assert total > 0
    return {name: w / total for name, w in weights.items() if w > 1e-7}


def torso_bind(pos):
    z = pos.z
    if z < 1.18:
        t = max(0, min(1, (z - 1.04) / .14))
        return {'Bip001 Spine': 1 - t, 'Bip001 Spine1': t}
    t = max(0, min(1, (z - 1.18) / .16))
    return {'Bip001 Spine1': 1 - t, 'Bip001 Spine2': t}


def mix_bind(left, right, t):
    weights = {n: left.get(n, 0) * (1 - t) + right.get(n, 0) * t for n in left.keys() | right.keys()}
    weights = dict(sorted(weights.items(), key=lambda item: item[1], reverse=True)[:4])
    total = sum(weights.values())
    return {n: w / total for n, w in weights.items() if w > 1e-7}


def back_bind(pos):
    if pos.z <= 1.15:
        return {'Bip001 Spine1': 1.0}
    if pos.z < 1.24:
        return mix_bind({'Bip001 Spine1': 1.0}, sample_bind(Vector((pos.x, pos.y, 1.24))),
                        (pos.z - 1.15) / .09)
    return sample_bind(pos)


surface_grid = {}


def continuous_surface_bind(pos):
    # Layered panels, seams and pouches must sample one continuous field.
    # Trilinear interpolation removes nearest-face jumps between adjacent verts.
    cell = .04
    scaled = [v / cell for v in pos]
    lower = [math.floor(v) for v in scaled]
    frac = [scaled[i] - lower[i] for i in range(3)]
    weights = {}
    for x in (0, 1):
        for y in (0, 1):
            for z in (0, 1):
                corner = (x, y, z)
                key = tuple(lower[i] + corner[i] for i in range(3))
                if key not in surface_grid:
                    surface_grid[key] = sample_bind(Vector(tuple(v * cell for v in key)))
                factor = math.prod(frac[i] if corner[i] else 1 - frac[i] for i in range(3))
                for name, weight in surface_grid[key].items():
                    weights[name] = weights.get(name, 0) + weight * factor
    weights = dict(sorted(weights.items(), key=lambda item: item[1], reverse=True)[:4])
    total = sum(weights.values())
    return {name: weight / total for name, weight in weights.items() if weight > 1e-10}


def bind_vertex(pos):
    if a.torso_carrier:
        assert native_weights is not None, '--torso-carrier requires --shirt'
        # Side belts sit closer to sleeve geometry than to the torso. Sampling
        # their nearest sleeve triangle transfers arm movement to the waist.
        # Use native centre-front/back weights and one continuous side blend.
        def core(y):
            values={}
            # Thick hide spans cloth folds: smooth the native vertical field
            # across 10 cm instead of reproducing each abrupt shirt transition.
            for dz,factor in ((-.05,1),(-.025,2),(0,3),(.025,2),(.05,1)):
                for name,weight in continuous_surface_bind(Vector((0,y,pos.z+dz))).items():
                    values[name]=values.get(name,0)+weight*factor/9
            values={n:w for n,w in values.items() if n in (
                'Bip001 Pelvis','Bip001 Spine','Bip001 Spine1','Bip001 Spine2')}
            total=sum(values.values())
            return {n:w/total for n,w in values.items()} if total else {'Bip001 Spine2':1.0}
        side=max(0,min(1,(pos.y+.14)/.28))
        torso=mix_bind(core(-.18),core(.18),side)
        if a.torso_shoulders:
            return torso
        t=max(0,min(1,(pos.z-1.37)/.09));t=t*t*(3-2*t)
        return mix_bind(torso,continuous_surface_bind(pos),t)
    if native_weights is not None and reference_plate is not None:
        # Upper body follows the actual clothing, including its clavicle/twist chains.
        # Only the skirt blends toward the accepted cuirass; no guessed back Spine field.
        native=continuous_surface_bind(pos) if a.surface_skin else sample_bind(pos)
        if a.native_only:return native
        if pos.z>=1.22:return native
        def plate_field(y):
            # Read the centre of each v7 plate, then blend continuously around the sides.
            # Nearest disconnected rivets/straps at the rim create abrupt skin changes.
            co,_,index,_=plate_bvh.find_nearest(Vector((0,y,pos.z)));ids=plate_faces[index]
            bary=barycentric_transform(co,*[plate_vertices[i] for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)))
            weights={}
            for idx,factor in zip(ids,bary):
                for g in reference_plate.data.vertices[idx].groups:
                    name=reference_plate.vertex_groups[g.group].name
                    if factor>0:weights[name]=weights.get(name,0)+g.weight*factor
            return weights
        side=max(0,min(1,(pos.y+.10)/.20));side=side*side*(3-2*side)
        plate=mix_bind(plate_field(-.3),plate_field(.3),side)
        t=max(0,min(1,(pos.z-1.10)/.12));t=t*t*(3-2*t)
        return mix_bind(plate,native,t)
    # Shoulder straps and pads follow clavicle/twist; the vest body stays on the
    # continuous torso field used by the cuirass so the hem does not pick up legs.
    def fade(value):
        t = max(0., min(1., value))
        return t * t * (3. - 2. * t)
    torso = mix_bind(torso_bind(pos), back_bind(pos), fade((pos.y + .03) / .06))
    shoulder = fade((abs(pos.x) - .10) / .07) * fade((pos.z - 1.34) / .08)
    upper = fade((pos.z - 1.36) / .09)
    # One continuous field across cover, piping and strap anchor vertices.
    # A hard z threshold previously put adjacent sewn parts on different bones.
    return mix_bind(torso, sample_bind(pos), max(shoulder, upper))


imported = []
with bpy.data.libraries.load(str(a.clean.resolve()), link=False) as (src, dst):
    dst.objects = list(src.objects)
for obj in dst.objects:
    if obj and obj.type == 'MESH':
        bpy.context.collection.objects.link(obj)
        imported.append(obj)
assert imported, 'clean blend has no mesh parts'
if a.preserve_uv:
    assert len(imported) == 1, '--preserve-uv requires a single atlas mesh'

for obj in imported:
    # Preserve the authored cloth coordinates through the joined bake atlas.
    # Reprojecting the only UV layer changed the material after studio review.
    assert obj.data.uv_layers.active, ('Missing source UV', obj.name)
    obj.data.uv_layers.active.name = 'SourceUV'
    for material in obj.data.materials:
        if not material or not material.use_nodes:
            continue
        nodes, links = material.node_tree.nodes, material.node_tree.links
        for node in list(nodes):
            if node.type == 'TEX_COORD':
                uv_links = list(node.outputs['UV'].links)
                if uv_links:
                    source_uv = nodes.new('ShaderNodeUVMap')
                    source_uv.uv_map = 'SourceUV'
                    for link in uv_links:
                        links.new(source_uv.outputs['UV'], link.to_socket)
            elif node.type == 'NORMAL_MAP':
                node.uv_map = 'SourceUV'
    obj.modifiers.clear()
    while obj.vertex_groups:
        obj.vertex_groups.remove(obj.vertex_groups[0])
    groups = {}
    for vert in obj.data.vertices:
        for name, weight in bind_vertex(obj.matrix_world @ vert.co).items():
            if name not in groups:
                groups[name] = obj.vertex_groups.new(name=name)
            groups[name].add([vert.index], weight, 'REPLACE')

if reference_plate is not None:
    bpy.data.objects.remove(reference_plate,do_unlink=True)

bpy.ops.object.select_all(action='DESELECT')
for obj in imported:
    obj.select_set(True)
bpy.context.view_layer.objects.active = imported[0]
bpy.ops.object.join()
armor = bpy.context.object
armor.name = 'TEST_' + a.item
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
atlas = armor.data.uv_layers.new(name='ExportUV')
if a.preserve_uv:
    source_uv = armor.data.uv_layers['SourceUV']
    for source_loop, export_loop in zip(source_uv.data, atlas.data):
        export_loop.uv = source_loop.uv
armor.data.uv_layers.active = atlas
atlas.active_render = True
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.normals_make_consistent(inside=False)
if not a.preserve_uv:
    bpy.ops.uv.smart_project(island_margin=.008)
bpy.ops.object.mode_set(mode='OBJECT')

for vert in armor.data.vertices:
    influences = sorted([(g.group, g.weight) for g in vert.groups if g.weight > 0],
                        key=lambda item: item[1], reverse=True)[:4]
    total = sum(weight for _, weight in influences)
    assert total > 0, ('unweighted', vert.index)
    for group in list(vert.groups):
        armor.vertex_groups[group.group].remove([vert.index])
    for index, weight in influences:
        armor.vertex_groups[index].add([vert.index], weight / total, 'REPLACE')

for modifier in list(armor.modifiers):
    armor.modifiers.remove(modifier)
arm = armor.modifiers.new('JA3 skeleton', 'ARMATURE')
arm.object = rig
armor.parent = rig
armor.data.calc_loop_triangles()

unweighted = sum(not any(g.weight > 0 for g in v.groups) for v in armor.data.vertices)
max_influences = max(sum(g.weight > 1e-6 for g in v.groups) for v in armor.data.vertices)
report = {
    'item': 'JazzArmor_' + a.item,
    'entity': 'JAZZ_' + a.item + '_Male',
    'stage': 'rigged',
    'blend': str(blend),
    'vertices': len(armor.data.vertices),
    'triangles': len(armor.data.loop_triangles),
    'unweighted_vertices': unweighted,
    'max_influences': max_influences,
    'bones': sorted({armor.vertex_groups[g.group].name for v in armor.data.vertices for g in v.groups}),
    'runtime': 'NOT_RUN',
    'native_shirt': str(a.shirt) if a.shirt else None,
    'surface_skin': a.surface_skin,
    'torso_carrier': a.torso_carrier,
    'torso_shoulders': a.torso_shoulders,
    'preserve_uv': a.preserve_uv,
    'cuirass_reference': str(a.reference) if a.reference else None,
}
assert unweighted == 0 and max_influences <= 4
(blend.parent / 'rig-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
if bpy.context.scene.camera is None:
    bpy.ops.object.camera_add(location=(-1, -2.6, 1.95))
    cam = bpy.context.object
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = 1.18
    bpy.context.scene.camera = cam
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
print('RIGGED', report['triangles'], 'triangles;', report['max_influences'], 'max influences')
