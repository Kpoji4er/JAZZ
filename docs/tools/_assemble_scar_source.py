"""Recover a SCAR assembly from the supplied OBJ library, preserving loop UV.

Blender --background --factory-startup --python ... -- --source DIR
--previous-build DIR --output DIR. Development assembly, not an installer.
"""
import argparse
import json
import math
import sys
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector, Matrix

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--previous-build', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--upper-map', default='upper_scarl')
p.add_argument('--caliber', choices=('L','H'), default='L')
p.add_argument('--barrel', choices=('Short','Standard','Long'), default='Standard')
a = p.parse_args(sys.argv[sys.argv.index('--')+1:])
a.output.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
materials = {}

def material(prefix):
    if prefix in materials:
        return materials[prefix]
    mat = bpy.data.materials.new(prefix)
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes.get('Principled BSDF')
    def tex(suffix, space):
        node = nodes.new('ShaderNodeTexImage')
        node.image = bpy.data.images.load(str(a.previous_build / 'tga' / f'{prefix}_{suffix}.tga'))
        node.image.colorspace_settings.name = space
        return node.outputs['Color']
    links.new(tex('BaseColor', 'sRGB'), bsdf.inputs['Base Color'])
    nm = nodes.new('ShaderNodeNormalMap')
    links.new(tex('Normal', 'Non-Color'), nm.inputs['Color'])
    links.new(nm.outputs['Normal'], bsdf.inputs['Normal'])
    sep = nodes.new('ShaderNodeSeparateColor')
    links.new(tex('RM', 'Non-Color'), sep.inputs['Color'])
    links.new(sep.outputs['Red'], bsdf.inputs['Roughness'])
    links.new(sep.outputs['Blue'], bsdf.inputs['Metallic'])
    materials[prefix] = mat
    return mat

def load(path, name, basis, prefix, clip=None):
    vertices, raw, uv, faces, loop_uv = [], [], [], [], []
    matrix = Matrix(basis)
    for line in path.read_text().splitlines():
        bits = line.split()
        if not bits: continue
        if bits[0] == 'v':
            raw.append(Vector(tuple(map(float, bits[1:4]))))
            vertices.append(matrix @ raw[-1])
        elif bits[0] == 'vt': uv.append(tuple(map(float, bits[1:3])))
        elif bits[0] == 'f':
            corners = [s.split('/') for s in bits[1:]]
            if matrix.determinant() < 0: corners.reverse()
            ids = [int(c[0])-1 for c in corners]
            if clip and not all(clip(raw[i]) for i in ids): continue
            # Render-capture triangle-strip connectors are degenerate. Keeping
            # them falsely connects unrelated parts and contaminates smoothing.
            if (vertices[ids[1]]-vertices[ids[0]]).cross(vertices[ids[2]]-vertices[ids[0]]).length < 1e-7:
                continue
            faces.append(ids)
            loop_uv.extend([uv[int(c[1])-1] for c in corners])
    used=sorted({i for face in faces for i in face})
    index={old:new for new,old in enumerate(used)}
    vertices=[vertices[i] for i in used]
    faces=[[index[i] for i in face] for face in faces]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    layer = mesh.uv_layers.new(name='UVMap')
    for loop, coord in zip(layer.data, loop_uv): loop.uv = coord
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    mesh.materials.append(material(prefix))
    return obj

def bounds(obj):
    points = [obj.matrix_world @ v.co for v in obj.data.vertices]
    return Vector(tuple(min(v[i] for v in points) for i in range(3))), Vector(tuple(max(v[i] for v in points) for i in range(3)))

def place(obj, minimum_x=None, maximum_x=None, top=None, centre_y=0):
    lo, hi = bounds(obj)
    shift = Vector((0, centre_y-(lo.y+hi.y)/2, 0))
    if minimum_x is not None: shift.x = minimum_x-lo.x
    if maximum_x is not None: shift.x = maximum_x-hi.x
    if top is not None: shift.z = top-hi.z
    for v in obj.data.vertices: v.co += shift

body = load(a.source/'model_5.obj', 'Common', ((1,0,0),(0,0,-1),(0,1,0)), 'scar_common')
front_delta=2.176 if a.caliber=='H' else 0
barrel_delta={'Short':-10.16,'Standard':0,'Long':10.16}[a.barrel]
for v in body.data.vertices:
    if v.co.x < -13 and v.co.z < -8: v.co += Vector((-2,0,6.5))
    elif v.co.x < -9: v.co += Vector((0,0,5.3))
    else:
        if v.co.x>25.7: v.co.x+=barrel_delta*(v.co.x-25.7)/(42.83883285522461-25.7)
        v.co += Vector((-4+front_delta,0,3.7))
if a.caliber=='L':
    upper = load(a.source/'model_13.obj', 'Upper', ((-1,0,0),(0,0,1),(0,1,0)), a.upper_map)
else:
    upper = load(a.source/'model_71.obj', 'Upper', ((1,0,0),(0,0,-1),(0,1,0)), 'upper_scarh')
place(upper, minimum_x=-22, top=5.5)
c,s=math.cos(math.radians(20)),math.sin(math.radians(20))
if a.caliber=='L':
    lower = load(a.source/'model_19.obj', 'Lower', ((1,0,0),(0,c,-s),(0,s,c)), 'scar_lower', lambda v: -15<v.x<7.1 and 1<v.y<8 and -38.3<v.z<-30)
else:
    lower = load(a.source/'model_68.obj', 'Lower', ((1,0,0),(0,0,-1),(0,1,0)), 'scar_lower')
place(lower, minimum_x=-22, top=0)
stock = load(a.source/'model_2.obj', 'Stock', ((1,0,0),(0,0,-1),(0,1,0)), 'stock')
place(stock, maximum_x=-19.3, top=5)
if a.caliber=='L':
    mag = load(a.source/'model_15.obj', 'Magazine', ((-1,0,0),(0,0,1),(0,1,0)), 'magazine_stanag_fn')
else:
    mag = load(a.source/'model_9.obj', 'Magazine', ((1,0,0),(0,0,-1),(0,1,0)), 'magazine_scarh_oem')
place(mag, maximum_x=-0.5+front_delta, top=-2)
rear = load(a.source/'model_3.obj', 'RearSight', ((1,0,0),(0,0,-1),(0,1,0)), 'acc_fn_rearsight',lambda v: -31<v.x<-25 and v.y>76)
place(rear, minimum_x=-21, top=9.2)
muzzle=load(a.source/'model_12.obj','Muzzle',((-1,0,0),(0,0,1),(0,1,0)),'acc_muzzledevices1',lambda v:14<v.y<18)
place(muzzle, minimum_x=38+front_delta+barrel_delta, top=1.15)
meshes = [body, upper, lower, stock, mag, rear, muzzle]
report = {}
for obj in meshes:
    lo, hi = bounds(obj)
    report[obj.name] = {'min_cm':list(lo),'max_cm':list(hi),'faces':len(obj.data.polygons)}
    bm=bmesh.new();bm.from_mesh(obj.data)
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=0.00001)
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    edges=[e for e in bm.edges if len(e.link_faces)==2 and e.calc_face_angle(0)>math.radians(45)]
    bmesh.ops.split_edges(bm,edges=edges)
    bm.to_mesh(obj.data);bm.free()
    for poly in obj.data.polygons: poly.use_smooth = True
    obj.scale = (.01,)*3
(a.output/'assembly.json').write_text(json.dumps(report, indent=2))
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1600
scene.render.resolution_y = 650
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'Standard'
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs[0].default_value = (.25,.25,.25,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value = .7
for name, loc, energy, size in [('Key',(0,-2,3),500,3),('Fill',(0,2,1),350,3)]:
    ld = bpy.data.lights.new(name,'AREA'); ld.energy=energy; ld.shape='DISK'; ld.size=size
    ob=bpy.data.objects.new(name,ld); scene.collection.objects.link(ob); ob.location=loc
    ob.rotation_euler=(-ob.location).to_track_quat('-Z','Y').to_euler()
camdata=bpy.data.cameras.new('Camera'); camdata.type='ORTHO'; camdata.ortho_scale=1.12
cam=bpy.data.objects.new('Camera',camdata); scene.collection.objects.link(cam); scene.camera=cam
for name, eye in [('side',(0,-2,0)),('back',(0,2,0)),('angle',(1,-2,.8))]:
    target=Vector((-.05,0,-.08)); cam.location=target+Vector(eye)
    cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(a.output/f'{name}.png')
    bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'SCAR-recovery.blend'))
