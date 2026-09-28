"""Rebuild the approved EBR donor with complete Sage chassis and correct maps.
Blender --python this.py -- --source <mk14> --output <new build> --game-root <JA3>
Writes a prepared blend/FBX, native Blender preview and audit; no active-mod writes.
"""
import argparse
import json
import sys
from pathlib import Path
import bpy
import bmesh
import numpy as np
from mathutils import Vector, Matrix
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge, pixels, save_tga, assign_hge_maps, finalise, export_fbx
from _ja3_mesh_prepare import prepare_export_mesh, audit_blender_object
from _render_m14_family_icons import render_one

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--game-root', type=Path, required=True)
a = p.parse_args(sys.argv[sys.argv.index('--')+1:])
a.output.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
hge = load_hge(a.game_root)
# Native archive coordinates: muzzle -X, up +Z. Explicit proper rotation:
# Blender muzzle -Y, up +Z. Keep all donor parts in the same authored frame.
parts = [(0,'m14_rest'),(1,'m14_receiver'),(2,'m14_barrels'),
         (3,'ebr_chassis_02'),(7,'ebr_chassis_01'),(5,'stock')]
scale = 1.0 / (1.12 + 3.33)
anchor = Vector((.05, 0, -.10))
rotation = Matrix(((0,-1,0),(1,0,0),(0,0,1)))
atlas_size, tile = 4096, 1024
atlas = {k: np.ones((atlas_size,atlas_size,4),dtype=np.float32) for k in ('Base','Normal','RM','AO')}
atlas['Normal'][:,:,:3] = (.5,.5,1)
atlas['RM'][:,:,0] = .65
atlas['RM'][:,:,2] = 0
objects, removed = [], {}
for index, (part, prefix) in enumerate(parts):
    verts, texcoords, faces, uvs = [], [], [], []
    for line in (a.source/f'part_{part:02d}.obj').read_text().splitlines():
        if line.startswith('v '): verts.append(rotation @ ((Vector(tuple(map(float,line.split()[1:4])))-anchor)*scale))
        elif line.startswith('vt '): texcoords.append(tuple(map(float,line.split()[1:3])))
        elif line.startswith('f '):
            tokens=[t.split('/') for t in line.split()[1:]]
            faces.append([int(t[0])-1 for t in tokens])
            uvs.append([int(t[1])-1 for t in tokens])
    mesh=bpy.data.meshes.new(prefix)
    mesh.from_pydata(verts,[],faces)
    obj=bpy.data.objects.new(prefix,mesh)
    bpy.context.collection.objects.link(obj)
    layer=mesh.uv_layers.new(name='UVMap')
    tx,ty=index%4,index//4
    for poly,indices in zip(mesh.polygons,uvs):
        for loop,uvindex in zip(poly.loop_indices,indices):
            u,v=texcoords[uvindex]
            layer.data[loop].uv=((tx+u)/4,(ty+v)/4)
    # Only discard zero-area faces; no broad merge/weld of unrelated surfaces.
    bm=bmesh.new();bm.from_mesh(mesh)
    bad=[f for f in bm.faces if f.calc_area()<1e-12 or min(e.calc_length() for e in f.edges)<1e-10]
    removed[prefix]=len(bad)
    bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
    bm.to_mesh(mesh);bm.free()
    objects.append(obj)
    maps={k:pixels(a.source/f'{prefix}_{suffix}.png',tile) for k,suffix in
          [('Base','BaseColor'),('Normal','Normal'),('AO','ambient_occlusion'),('Rough','Roughness'),('Metal','Metallic')]}
    rm=np.ones((tile,tile,4),dtype=np.float32)
    rm[:,:,0]=maps['Rough'][:,:,0];rm[:,:,2]=maps['Metal'][:,:,0]
    maps['RM']=rm
    for k in atlas:atlas[k][ty*tile:(ty+1)*tile,tx*tile:(tx+1)*tile]=maps[k]
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
barrel=objects[2]
barrel.select_set(False)
bpy.context.view_layer.objects.active=objects[0]
bpy.ops.object.join()
body=bpy.context.object
images={k:save_tga('MK14EBR_'+k,v,a.output,k=='Base') for k,v in atlas.items()}
mat=bpy.data.materials.new('MK14EBR')
assign_hge_maps(hge,mat,images)
issues=prepare_export_mesh(body,strict=False)
bad_indices={i['triangle'] for i in issues if i['kind'] in ('degenerate','zero_normal')}
if bad_indices:
    bm=bmesh.new();bm.from_mesh(body.data);bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad_indices],context='FACES_ONLY')
    bm.to_mesh(body.data);bm.free()
removed['post_triangulation']=len(bad_indices)
finalise(body,'MK14EBR',mat)
# Spots are measured in the donor's authored frame, not fractions of its bbox.
raw_spots={'Muzzle':(-3.33,0,.30),'MuzzleTip':(-3.37,0,.30),
 'Barrel':(-.89,0,.30),'Scope':(-.85,0,.54),'Mount':(-.85,0,.52),
 'General':(-.85,0,.52),'Magazine':(-.62,0,.0),
 'Hand_l_grip':(-1.55,0,.0),'Under':(-1.55,0,-.015),
 'Bipod':(-2.15,0,.0),'Side':(-1.65,-.12,.28),'Mountside':(-1.65,-.12,.28),
 'Stock':(.25,0,.18),'Trigger':(-.08,0,-.035)}
for name,pt in raw_spots.items():
    spot=bpy.data.objects.new('MK14EBR_'+name,None)
    bpy.context.collection.objects.link(spot);spot.parent=body
    spot.location=rotation@((Vector(pt)-anchor)*scale)
    spot.hge_obj_settings.spot_name=name
issues=prepare_export_mesh(body)
assert not issues,issues
barrel_anchor=rotation@((Vector(raw_spots['Barrel'])-anchor)*scale)
barrel.data.transform(Matrix.Translation(-barrel_anchor))
barrels=[]
for suffix,factor in [('Normal',1.0),('Short',.82),('Long',1.18)]:
    obj=barrel if suffix=='Normal' else bpy.data.objects.new('barrel_'+suffix,barrel.data.copy())
    if obj!=barrel:bpy.context.collection.objects.link(obj)
    if factor!=1:
        for v in obj.data.vertices:v.co.y*=factor
    finalise(obj,'MK14EBR_Barrel'+suffix,mat)
    # Muzzle and support attachments follow the selected barrel length.
    for name in ('Muzzle','MuzzleTip'):
        pt=rotation@((Vector(raw_spots[name])-anchor)*scale)-barrel_anchor
        pt.y*=factor
        spot=bpy.data.objects.new(obj.name+'_'+name,None)
        bpy.context.collection.objects.link(spot);spot.parent=obj;spot.location=pt
        spot.hge_obj_settings.spot_name=name
    barrels.append(obj)
blend=a.output/'MK14EBR.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
export_fbx(hge,a.output/'MK14EBR.fbx')
(a.output/'repair-report.json').write_text(json.dumps({'parts':parts,'removed_zero_faces':removed,
 'triangles':len(body.data.polygons),'issues':audit_blender_object(body),
 'scale':scale,'anchor_native':list(anchor),'spots_native':raw_spots},indent=2))
# A separate assembled preview retains entity-local coordinates in export blend.
for obj in barrels:
    if obj==barrel:obj.parent.location=barrel_anchor
    else:obj.hide_render=True
preview=a.output/'MK14EBR-assembled.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(preview))
render_one(preview,a.output/'MK14EBR-preview.png')
mat=bpy.data.materials['MK14EBR'];mat.use_nodes=True
node=mat.node_tree.nodes.new('ShaderNodeTexImage')
node.image=bpy.data.images.load(str(a.output/'MK14EBR_Base.tga'))
mat.node_tree.nodes.active=node
bpy.context.scene.display.shading.color_type='TEXTURE'
bpy.context.scene.render.filepath=str(a.output/'MK14EBR-textured.png')
bpy.ops.render.render(write_still=True)
