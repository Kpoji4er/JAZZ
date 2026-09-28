"""Conservative AK103 mesh trials and paired offline renders; never installs assets.

Blender --background --python this.py -- --source <blend> --out <directory>
    [--angle 0.1] [--mode collapse --ratio .8 --unweighted] [--render]
    [--parts AKR_AK103_Handguard] [--game-root <JA3_ROOT>]
All outputs are unaccepted trials, including successful exports. Planar dissolve
respects UV/material/seam/sharp boundaries. Surface distances are
bidirectional samples, not a proof of visual equivalence; inspect paired renders.
"""
import argparse
import json
import math
from pathlib import Path
import sys

import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh


def snapshot(obj):
    mesh = obj.data
    mesh.calc_loop_triangles()
    verts = [v.co.copy() for v in mesh.vertices]
    faces = [tuple(t.vertices) for t in mesh.loop_triangles]
    return verts, faces


def distance(a, b):
    if a == b:
        return {'max_mm': 0, 'p99_mm': 0, 'samples': len(a[0])+len(a[1]), 'identical': True}
    tree = BVHTree.FromPolygons(*b, all_triangles=True)
    points = a[0] + [sum((a[0][i] for i in f), Vector()) / 3 for f in a[1]]
    ds = sorted(tree.find_nearest(p)[3] for p in points)
    return {'max_mm': max(ds)*1000, 'p99_mm': ds[int(.99*(len(ds)-1))]*1000,
            'samples': len(ds)}


def render_pairs(out, objects, before):
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.eevee.taa_render_samples = 32
    scene.render.resolution_x = 1500
    scene.render.resolution_y = 850
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = True
    scene.view_settings.view_transform = 'AgX'
    if scene.world is None:scene.world=bpy.data.worlds.new('QualityWorld')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes.get('Background').inputs[0].default_value = (.18,.18,.18,1)
    scene.world.node_tree.nodes.get('Background').inputs[1].default_value = .6
    for obj in list(scene.objects):
        if obj.type in {'LIGHT','CAMERA'}:
            bpy.data.objects.remove(obj, do_unlink=True)
    for name, pos, power, size in [('key',(1,-.3,1.2),100,1.2),('fill',(-1,0,.5),65,1),('rim',(0,.8,.8),80,.8)]:
        light=bpy.data.lights.new(name,'AREA');light.energy=power;light.shape='DISK';light.size=size
        ob=bpy.data.objects.new(name,light);scene.collection.objects.link(ob);ob.location=pos
        ob.rotation_euler=(-ob.location).to_track_quat('-Z','Y').to_euler()
    cam=bpy.data.objects.new('quality_camera',bpy.data.cameras.new('quality_camera'))
    scene.collection.objects.link(cam);scene.camera=cam;cam.data.type='ORTHO';cam.data.clip_start=.001
    stockfold=bpy.data.objects['AKR_AK103_StockFolded']; stock=bpy.data.objects['AKR_AK103_Stock']
    allpoints=[o.matrix_world@v.co for o in objects if o!=stockfold for v in o.data.vertices]
    centre=(Vector(tuple(min(p[i] for p in allpoints) for i in range(3)))+Vector(tuple(max(p[i] for p in allpoints) for i in range(3))))/2
    hg=bpy.data.objects['AKR_AK103_Handguard']
    hgpoints=[hg.matrix_world@v.co for v in hg.data.vertices]
    hgcentre=sum(hgpoints,Vector())/len(hgpoints)
    views=[('right',(1,0,.08),centre,1.05,False),('left',(-1,0,.08),centre,1.05,False),
           ('quarter',(1,-.7,.55),centre,1.05,False),('top',(.1,0,1),centre,1.05,False),
           ('handguard',(1,-.25,.3),hgcentre,.34,False),('receiver',(-1,.25,.4),centre,.5,False),
           ('folded',(1,-.5,.4),centre,1.05,True)]
    after={o.name:o.data for o in objects}
    out.mkdir(parents=True,exist_ok=True)
    for label, offset, target, span, fold in views:
        stockfold.hide_render=not fold;stock.hide_render=fold
        cam.location=target+Vector(offset).normalized()*2
        cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=span
        for phase, meshes in [('before',before),('after',after)]:
            for obj in objects:obj.data=meshes[obj.name]
            for shading in ('pbr','clay'):
                scene.render.engine='BLENDER_EEVEE_NEXT' if shading=='pbr' else 'BLENDER_WORKBENCH'
                if shading=='clay':
                    scene.display.shading.light='STUDIO';scene.display.shading.color_type='SINGLE'
                    scene.display.shading.single_color=(.5,.5,.5);scene.display.shading.show_cavity=True
                scene.render.filepath=str(out/f'{label}_{shading}_{phase}.png')
                bpy.ops.render.render(write_still=True)
    for obj in objects:obj.data=after[obj.name]
    stock.hide_render=False;stockfold.hide_render=True


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--angle',type=float,default=.1);p.add_argument('--render',action='store_true')
    p.add_argument('--mode',choices=['planar','collapse'],default='planar')
    p.add_argument('--ratio',type=float,default=.8)
    p.add_argument('--unweighted',action='store_true',help='Diagnostic trial only; visual acceptance still required')
    p.add_argument('--parts',nargs='+',default=['AKR_AK103','AKR_AK103_Handguard'])
    p.add_argument('--game-root',type=Path)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(a.source),use_scripts=False)
    # Resolve texture paths before saving into another directory.
    for image in bpy.data.images:
        if image.filepath:image.filepath=bpy.path.abspath(image.filepath)
    objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('AKR_AK103')]
    assert len(objects)==6
    before={o.name:o.data.copy() for o in objects}; report={}
    for obj in objects:
        bpy.ops.object.select_all(action='DESELECT');obj.hide_set(False);obj.select_set(True);bpy.context.view_layer.objects.active=obj
        orig=snapshot(obj)
        if a.mode=='planar':
            mod=obj.modifiers.new('Conservative planar dissolve','DECIMATE');mod.decimate_type='DISSOLVE'
            mod.angle_limit=math.radians(a.angle);mod.delimit={'NORMAL','MATERIAL','SEAM','SHARP','UV'};mod.use_dissolve_boundaries=False
            bpy.ops.object.modifier_apply(modifier=mod.name)
            prepare_export_mesh(obj)
        elif obj.name in a.parts:
            # Prioritize low-curvature interiors; protect hard edges and UV seams.
            bm=bmesh.new();bm.from_mesh(obj.data);bm.verts.ensure_lookup_table()
            uv=bm.loops.layers.uv.active;locked=set()
            for edge in bm.edges:
                hard=not edge.is_manifold or edge.calc_face_angle(0)>math.radians(20)
                if not hard and uv:
                    for v in edge.verts:
                        values=[l[uv].uv for f in edge.link_faces for l in f.loops if l.vert==v]
                        if len(values)==2 and (values[0]-values[1]).length>1e-6:hard=True
                if hard:locked.update(v.index for v in edge.verts)
            group=obj.vertex_groups.new(name='OptimizeInterior')
            free=[v.index for v in bm.verts if v.index not in locked];bm.free()
            if free:group.add(free,1,'REPLACE')
            mod=obj.modifiers.new('Protected collapse trial','DECIMATE');mod.ratio=a.ratio
            if not a.unweighted:
                mod.vertex_group=group.name;mod.vertex_group_factor=1000
            bpy.ops.object.modifier_apply(modifier=mod.name);obj.vertex_groups.remove(obj.vertex_groups['OptimizeInterior'])
            prepare_export_mesh(obj)
        new=snapshot(obj)
        report[obj.name]={'before':len(orig[1]),'after':len(new[1]),'old_to_new':distance(orig,new),'new_to_old':distance(new,orig)}
        print(obj.name,json.dumps(report[obj.name]),flush=True)
    (a.out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    bpy.ops.wm.save_as_mainfile(filepath=str(a.out/'AK103_JA3.blend'))
    if a.game_root:
        from _export_ak103_assets import load_hge
        from _export_m14_family_assets import export_fbx
        hge=load_hge(a.game_root);export_fbx(hge,a.out/'AK103_JA3.fbx')
    if a.render:render_pairs(a.out/'review',objects,before)


if __name__=='__main__':main()

