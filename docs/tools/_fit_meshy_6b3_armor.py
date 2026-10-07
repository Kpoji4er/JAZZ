"""Fit a Meshy 6B3 GLB to the native Shirt08 envelope; write source only.

Blender --background --factory-startup --python this.py -- --input model.glb
  --shirt decoded-shirt.json --output build-root
The GLB is never modified. Follow with _rig_6b3_vest.py and the normal export gates.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
import bmesh
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh

p = argparse.ArgumentParser(description=__doc__)
for key in ('input', 'shirt', 'output'):
    p.add_argument('--' + key, type=Path, required=True)
p.add_argument('--item', default='6B3', help='Existing armor suffix, e.g. 6B13')
p.add_argument('--width', type=float, default=.48)
p.add_argument('--depth', type=float, default=.46)
p.add_argument('--height', type=float, default=.56)
p.add_argument('--zmin', type=float, default=.99)
p.add_argument('--clearance', type=float, default=.012)
p.add_argument('--preserve-shape', action='store_true', help='Uniform scale by height, translation only; skip radial deformation')
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
out = a.output.resolve()
(out / 'clean').mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(a.input.resolve()))
meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')
for obj in meshes:
    obj.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.join()
armor = bpy.context.object
armor.name = 'Meshy '+a.item+' fitted source'
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
lo = Vector(tuple(min(v.co[i] for v in armor.data.vertices) for i in range(3)))
hi = Vector(tuple(max(v.co[i] for v in armor.data.vertices) for i in range(3)))
center = (lo + hi) / 2
if a.preserve_shape:
    a.width = (hi.x-lo.x)*a.height/(hi.z-lo.z)
    a.depth = (hi.y-lo.y)*a.height/(hi.z-lo.z)
for v in armor.data.vertices:
    v.co = Vector(((v.co.x-center.x)*a.width/(hi.x-lo.x),
                   (v.co.y-center.y)*a.depth/(hi.y-lo.y)-.010,
                   (v.co.z-lo.z)*a.height/(hi.z-lo.z)+a.zmin))

# glTF splits vertices at UV/normal seams. Weld only coincident geometry,
# retaining per-loop UVs, then use the canonical normal preparation helper.
before_tri = sum(len(f.vertices)-2 for f in armor.data.polygons)
before_vert = len(armor.data.vertices)
bm = bmesh.new()
bm.from_mesh(armor.data)
bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-6)
bm.to_mesh(armor.data)
bm.free()
assert sum(len(f.vertices)-2 for f in armor.data.polygons) == before_tri
prepare_export_mesh(armor)

data = json.loads(a.shirt.read_text(encoding='utf-8'))
sub = data['meshes'][1]
box = sub.get('bbox') or data['bbox']
c = [(box[i]+box[i+3])/2 for i in range(3)]
shirt_verts = [Vector((-(v[1]+c[1]), -(v[0]+c[0]), v[2]+c[2])) for v in sub['vertices']]
shirt_bvh = BVHTree.FromPolygons(shirt_verts, [tuple(reversed(f)) for f in sub['faces']])
armor_bvh = BVHTree.FromPolygons([v.co.copy() for v in armor.data.vertices],
                                [tuple(f.vertices) for f in armor.data.polygons])

# A smooth radial displacement moves all layers of each panel together, so
# pouches keep their depth. Stop below the shoulders: radial fitting there
# would project straps onto the neck or sleeves.
nz, nt = 54, 96
zs = np.linspace(a.zmin, 1.44, nz)
offsets = np.full((nz, nt), np.nan)
for iz, z in enumerate(zs):
    axis = Vector((0, -.010, float(z)))
    for it in range(nt):
        th = it * 2*math.pi/nt
        direction = Vector((math.sin(th), -math.cos(th), 0))
        cloth = shirt_bvh.ray_cast(axis, direction, .38)
        shell = armor_bvh.ray_cast(axis, direction, .38)
        if cloth[0] is not None and shell[0] is not None:
            # Exclude arm hits and disconnected pouch interiors.
            if .08 < cloth[3] < .255 and shell[3] > .075:
                offsets[iz,it] = np.clip(cloth[3]+a.clearance-shell[3], -.025, .080)
known = np.argwhere(np.isfinite(offsets))
assert len(known) > nz*nt*.25, 'Not enough overlapping torso coverage'
for iz,it in np.argwhere(~np.isfinite(offsets)):
    dt = np.minimum(abs(known[:,1]-it), nt-abs(known[:,1]-it))
    j,k = known[np.argmin((known[:,0]-iz)**2+(dt*.65)**2)]
    offsets[iz,it] = offsets[j,k]
for _ in range(10):
    pad = np.pad(offsets, ((1,1),(0,0)), mode='edge')
    offsets = (offsets*4+np.roll(offsets,1,1)+np.roll(offsets,-1,1)+pad[:-2]+pad[2:])/8

def smooth(value):
    t = max(0., min(1., value))
    return t*t*(3-2*t)

def sample(theta,z):
    t = theta % (2*math.pi)/(2*math.pi)*nt
    it,ft = int(t)%nt,t-int(t)
    zz = max(0.,min(nz-1.0001,(z-zs[0])/(zs[-1]-zs[0])*(nz-1)))
    iz,fz = int(zz),zz-int(zz)
    return float((offsets[iz,it]*(1-ft)+offsets[iz,(it+1)%nt]*ft)*(1-fz)
                 +(offsets[iz+1,it]*(1-ft)+offsets[iz+1,(it+1)%nt]*ft)*fz)

moved = []
for v in armor.data.vertices:
    xy = Vector((v.co.x,v.co.y+.010,0))
    theta = math.atan2(xy.x,-xy.y)
    delta = 0. if a.preserve_shape else sample(theta,v.co.z)*(1-smooth((v.co.z-1.40)/.09))
    if xy.length > .03:
        v.co += xy.normalized()*delta
        moved.append(delta)
prepare_export_mesh(armor)
for face in armor.data.polygons:
    face.use_smooth = True

# Explicit source UVs are essential when the rigging step creates ExportUV.
armor.data.uv_layers.active.name = 'SourceUV'
for mat in armor.data.materials:
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    uv = nodes.new('ShaderNodeUVMap')
    uv.uv_map = 'SourceUV'
    for node in list(nodes):
        if node.type == 'TEX_IMAGE' and not node.inputs['Vector'].is_linked:
            links.new(uv.outputs['UV'],node.inputs['Vector'])
        if node.type == 'NORMAL_MAP':
            node.uv_map = 'SourceUV'
armor.data.calc_loop_triangles()
report = {'source': str(a.input.resolve()), 'triangles': len(armor.data.loop_triangles),
          'vertices_before_weld': before_vert, 'vertices_after_weld': len(armor.data.vertices),
          'affine_dimensions': [a.width,a.depth,a.height], 'zmin':a.zmin,
          'radial_offset_range': [min(moved),max(moved)], 'clearance_target':a.clearance,
          'has_custom_normals': armor.data.has_custom_normals,
          'shape_preserved':a.preserve_shape, 'status':'SOURCE_PREPARED', 'runtime':'NOT_RUN'}
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(out/('clean/JazzArmor_'+a.item+'.blend')))
(out/'fit-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
