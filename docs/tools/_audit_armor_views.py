"""Read-only all-side review renders of an existing armor source; never save blend."""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--source', required=True, type=Path)
p.add_argument('--output', required=True, type=Path)
p.add_argument('--wide', action='store_true')
p.add_argument('--diagnostic', action='store_true', help='Neutral materials and studio lights')
p.add_argument('--poses', action='store_true', help='Include synthetic bending/twist views')
p.add_argument('--shirt', type=Path, help='Decoded native shirt JSON with original skin weights')
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.output.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
if a.shirt:
    existing = bpy.data.objects.get('QA actual LegionGoon shirt')
    if existing:
        bpy.data.objects.remove(existing, do_unlink=True)
    data = json.loads(a.shirt.read_text())
    mesh_data = data['meshes'][1]
    box = mesh_data.get('bbox') or data['bbox']
    centre = [(box[i]+box[i+3])/2 for i in range(3)]
    vertices = [(-(v[1]+centre[1]), -(v[0]+centre[0]), v[2]+centre[2]) for v in mesh_data['vertices']]
    mesh = bpy.data.meshes.new('Audit native shirt')
    mesh.from_pydata(vertices, [], mesh_data['faces'])
    mesh.update()
    shirt = bpy.data.objects.new('QA actual LegionGoon shirt', mesh)
    bpy.context.collection.objects.link(shirt)
    rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    groups = {b.name:shirt.vertex_groups.new(name=b.name) for b in rig.data.bones}
    for index, (ids, weights) in enumerate(zip(mesh_data['bone_indices'],mesh_data['bone_weights'])):
        values = {data['bones'][i]['name']:w for i,w in zip(ids,weights) if w>0 and data['bones'][i]['name'] in groups}
        total = sum(values.values())
        assert total > 0
        for name, weight in values.items():
            groups[name].add([index], weight/total, 'REPLACE')
    shirt.modifiers.new('Native shirt skin','ARMATURE').object = rig
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 12
scene.cycles.use_denoising = True
scene.render.resolution_x = 900
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
for name in ('M_BaseMesh Skin_BIP', 'QA actual LegionGoon shirt'):
    obj = bpy.data.objects.get(name)
    if obj:
        obj.hide_render = False
if a.diagnostic:
    def material(name, color):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = (*color, 1)
        bsdf.inputs['Roughness'].default_value = .7
        return mat
    armor_mat = material('Audit armor', (.35, .43, .23))
    body_mat = material('Audit body', (.18, .25, .3))
    shirt_mat = material('Audit shirt', (.55, .16, .12))
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            mat = shirt_mat if obj.name == 'QA actual LegionGoon shirt' else body_mat if obj.name == 'M_BaseMesh Skin_BIP' else armor_mat
            for i in range(len(obj.data.materials)):
                obj.data.materials[i] = mat
            if not obj.data.materials:
                obj.data.materials.append(mat)
    for location in ((-3,-4,5),(3,-1,3),(0,4,4)):
        bpy.ops.object.light_add(type='AREA', location=location)
        light = bpy.context.object
        light.data.energy = 450
        light.data.shape = 'DISK'
        light.data.size = 4
        light.rotation_euler = (Vector((0,0,1.25))-light.location).to_track_quat('-Z','Y').to_euler()
target = Vector((0, 0, 1.27))
views = {
    'front': (0, -3, 1.4),
    'right': (3, 0, 1.32),
    'back': (0, 3, 1.4),
    'left': (-3, 0, 1.32),
    'rear_left': (-2.4, 2.5, 1.5),
    'top': (0, -.25, 4),
    'bottom': (0, -1.8, -.5),
}
camera = scene.camera
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 1.55 if a.wide else 1.0
for name, location in views.items():
    camera.location = location
    camera.rotation_euler = (target - camera.location).to_track_quat('-Z', 'Y').to_euler()
    scene.render.filepath = str(a.output / (name + '.png'))
    bpy.ops.render.render(write_still=True)
if a.poses:
    rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE')
    poses = {
        'lean': [('Bip001 Spine1',(12,0,0)),('Bip001 Spine2',(23,0,12)),('Bip001 R UpperArm',(0,35,-25))],
        'deep_lean': [('Bip001 Spine1',(28,0,0)),('Bip001 Spine2',(35,0,-18))],
        'twist': [('Bip001 Spine1',(0,0,25)),('Bip001 Spine2',(0,0,25)),('Bip001 L Clavicle',(0,0,20))],
    }
    for pose, rotations in poses.items():
        for bone in rig.pose.bones:
            bone.rotation_mode = 'XYZ'
            bone.rotation_euler = (0,0,0)
        for name, angles in rotations:
            rig.pose.bones[name].rotation_euler = [math.radians(x) for x in angles]
        bpy.context.view_layer.update()
        for side, location in {'front':(-1,-2.6,1.95), 'back':(1,2.6,1.95), 'left':(-3,0,1.4)}.items():
            camera.location = location
            camera.rotation_euler = (target-camera.location).to_track_quat('-Z','Y').to_euler()
            scene.render.filepath = str(a.output / (pose+'_'+side+'.png'))
            bpy.ops.render.render(write_still=True)
(a.output / 'review.json').write_text(json.dumps({
    'source': str(a.source), 'views': list(views),
    'geometry_modified': False, 'blend_saved': False,
    'diagnostic_materials': a.diagnostic, 'synthetic_poses': a.poses,
    'shirt_json': str(a.shirt) if a.shirt else None,
    'scope': 'visual audit; supplied shirt uses native weights; synthetic poses are not runtime acceptance',
}, indent=2))
