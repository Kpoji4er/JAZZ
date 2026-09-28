"""Repair one existing M14 entity per invocation, retaining UV/material contract.
Blender --python this.py -- --source <blend> --entity JAZZ_M14|JAZZ_M14_ART
--output <new build> --game-root <JA3>. No active-mod writes.
"""
import argparse,json,sys,math
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,finalise,export_fbx
from _ja3_mesh_prepare import prepare_export_mesh
from _render_m14_family_icons import render_one
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--entity',choices=['JAZZ_M14','JAZZ_M14_ART','JAZZ_M14_MkIII'],required=True)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--game-root',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
hge=load_hge(a.game_root);bpy.ops.wm.open_mainfile(filepath=str(a.source))
body=bpy.data.objects[a.entity];mat=body.data.materials[0]
for obj in list(bpy.data.objects):
    if obj!=body:bpy.data.objects.remove(obj,do_unlink=True)
body.parent=None;body.matrix_world=Matrix.Identity(4)
if a.entity in ('JAZZ_M14','JAZZ_M14_MkIII'):
    unique=a.entity=='JAZZ_M14_MkIII'
    if unique:
        bm=bmesh.new();bm.from_mesh(body.data);uv=bm.loops.layers.uv.active
        remove=[]
        for f in bm.faces:
            avg=sum((l[uv].uv for l in f.loops),Vector((0,0)))/len(f.loops)
            if avg.x>=.5 or avg.y>=.5:remove.append(f)
        bmesh.ops.delete(bm,geom=remove,context='FACES')
        bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
        bm.to_mesh(body.data);bm.free()
        # The old exporter incorrectly packed part_03 (magazine/bolt) into
        # the Laser tile. Restore it from the same donor using body texture.
        donor=a.source.parent.parent/'src/uniq'
        raw4=[Vector(tuple(map(float,l.split()[1:4]))) for l in (donor/'part_04.obj').read_text().splitlines() if l.startswith('v ')]
        raw_center=Vector(tuple((min(v[i] for v in raw4)+max(v[i] for v in raw4))/2 for i in range(3)))
        dest_center=Vector(tuple((min(v.co[i] for v in body.data.vertices)+max(v.co[i] for v in body.data.vertices))/2 for i in range(3)))
        s=(max(v.co.y for v in body.data.vertices)-min(v.co.y for v in body.data.vertices))/(max(v.x for v in raw4)-min(v.x for v in raw4))
        rot=Matrix(((0,1,0),(1,0,0),(0,0,-1)))
        delta=dest_center-rot@raw_center*s
        verts,uvs,faces,faceuv=[],[],[],[]
        for line in (donor/'part_03.obj').read_text().splitlines():
            if line.startswith('v '):verts.append(rot@Vector(tuple(map(float,line.split()[1:4])))*s+delta)
            elif line.startswith('vt '):uvs.append(tuple(map(float,line.split()[1:3])))
            elif line.startswith('f '):
                ts=[t.split('/') for t in line.split()[1:]]
                faces.append([int(t[0])-1 for t in ts]);faceuv.append([int(t[1])-1 for t in ts])
        mesh=bpy.data.meshes.new('unique_mag_bolt');mesh.from_pydata(verts,[],faces)
        layer=mesh.uv_layers.new()
        for f,indices in zip(mesh.polygons,faceuv):
            for li,ui in zip(f.loop_indices,indices):layer.data[li].uv=((uvs[ui][0]%1)*.5,uvs[ui][1]*.5)
        obj=bpy.data.objects.new('unique_mag_bolt',mesh);bpy.context.collection.objects.link(obj)
        mesh.materials.append(mat)
        bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);body.select_set(True)
        bpy.context.view_layer.objects.active=body;bpy.ops.object.join()
    midx=(min(v.co.x for v in body.data.vertices)+max(v.co.x for v in body.data.vertices))/2
    if unique:midx=dest_center.x
    factor=1.12/(max(v.co.y for v in body.data.vertices)-min(v.co.y for v in body.data.vertices))
    for v in body.data.vertices:
        v.co=(Vector((v.co.x-midx,v.co.y+.070,v.co.z+.010)) if unique else
              Vector((-v.co.x+midx,v.co.y+.075,-v.co.z+.045)))*factor
    preliminary=prepare_export_mesh(body,strict=False)
    zero={i['triangle'] for i in preliminary if i['kind'] in ('degenerate','zero_normal')}
    if zero:
        bm=bmesh.new();bm.from_mesh(body.data);bm.faces.ensure_lookup_table()
        bmesh.ops.delete(bm,geom=[bm.faces[i] for i in zero],context='FACES_ONLY')
        bm.to_mesh(body.data);bm.free()
    # Split at the hidden transition inside the wooden fore-end.
    cut=-.50
    bm=bmesh.new();bm.from_mesh(body.data)
    bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,
      plane_co=(0,cut,0),plane_no=(0,1,0),clear_inner=False,clear_outer=False)
    bm.to_mesh(body.data);bm.free()
    barrelmesh=body.data.copy()
    for mesh,front in [(body.data,False),(barrelmesh,True)]:
        bm=bmesh.new();bm.from_mesh(mesh)
        discard=[f for f in bm.faces if (f.calc_center_median().y<cut-1e-7)!=front]
        bmesh.ops.delete(bm,geom=discard,context='FACES')
        loose=[v for v in bm.verts if not v.link_faces]
        bmesh.ops.delete(bm,geom=loose,context='VERTS')
        bm.to_mesh(mesh);bm.free()
    magazine=body.data.copy()
    # Identify the complete disconnected magazine island, including its hidden
    # top. A plane/face-centre crop also cuts the wooden receiver above it.
    parent=list(range(len(body.data.vertices)));positions={}
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for v in body.data.vertices:
        key=tuple(round(x,5) for x in v.co)
        if key in positions:parent[root(v.index)]=root(positions[key])
        else:positions[key]=v.index
    for f in body.data.polygons:
        for i in f.vertices[1:]:parent[root(i)]=root(f.vertices[0])
    groups={}
    for v in body.data.vertices:groups.setdefault(root(v.index),[]).append(v)
    selected=set()
    for vs in groups.values():
        if (len(vs)>20 and min(v.co.y for v in vs)>(-.40 if unique else -.24) and max(v.co.y for v in vs)<(-.10 if unique else -.115)
            and min(v.co.z for v in vs)<(-.04 if unique else .02) and max(v.co.z for v in vs)<.10):
            selected.update(v.index for v in vs)
    assert (len(selected)>100 if unique else len(selected)==271),('Unexpected magazine island',len(selected))
    print('MAGAZINE_SELECTED',a.entity,len(selected))
    mag_faces={f.index for f in body.data.polygons if all(i in selected for i in f.vertices)}
    for mesh,keep_mag in [(body.data,False),(magazine,True)]:
        bm=bmesh.new();bm.from_mesh(mesh)
        bmesh.ops.delete(bm,geom=[f for f in bm.faces if (f.index in mag_faces)!=keep_mag],context='FACES')
        bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
        bm.to_mesh(mesh);bm.free()
    assert len(magazine.polygons)>50,'Magazine selection failed'
    finalise(body,a.entity,mat)
    coords={'Barrel':(0,cut,0),'Scope':(0,-.13,.143),'Mount':(0,-.13,.14),
     'General':(0,-.13,.14),'Side':(.026,-.32,.065),'Mountside':(.026,-.32,.065),
     'Hand_l_grip':(0,-.32,.025),'Under':(0,-.38,.025),'Bipod':(0,-.46,.027),
     'Muzzle':(0,-.835,.095),'MuzzleTip':(0,-.84,.095),'Magazine':(0,-.17,.075),
     'Stock':(0,.18,.025),'Trigger':(0,-.04,-.01)}
    if unique:
        coords.update(Scope=(0,-.18,.115),Mount=(0,-.18,.11),General=(0,-.18,.11),
                      Muzzle=(0,-.798,.073),MuzzleTip=(0,-.803,.073),Magazine=(0,-.19,.035))
    barrels=[]
    for suffix,ratio in [('Normal',1),('Short',.75),('Long',1.12)]:
        obj=bpy.data.objects.new(a.entity+'_Barrel'+suffix,barrelmesh.copy())
        bpy.context.collection.objects.link(obj)
        for v in obj.data.vertices:v.co.y=(v.co.y-cut)*ratio
        finalise(obj,obj.name,mat)
        for name in ('Muzzle','MuzzleTip'):
            q=Vector(coords[name]);q.y=(q.y-cut)*ratio
            spot=bpy.data.objects.new(obj.name+'_'+name,None);bpy.context.collection.objects.link(spot)
            spot.parent=obj;spot.location=q;spot.hge_obj_settings.spot_name=name
        barrels.append(obj)
    for suffix,ratio in [('Short',.55 if unique else 1),('Normal',1 if unique else 2)]:
        obj=bpy.data.objects.new(a.entity+'_Magazine'+suffix,magazine.copy())
        bpy.context.collection.objects.link(obj)
        for v in obj.data.vertices:
            v.co-=Vector(coords['Magazine']);v.co.z*=ratio
        finalise(obj,obj.name,mat);barrels.append(obj)
else:
    for v in body.data.vertices:v.co=Vector((-v.co.x,v.co.y,-v.co.z))
    minz=min(v.co.z for v in body.data.vertices)
    cx=(min(v.co.x for v in body.data.vertices)+max(v.co.x for v in body.data.vertices))/2
    cy=(min(v.co.y for v in body.data.vertices)+max(v.co.y for v in body.data.vertices))/2
    for v in body.data.vertices:v.co-=Vector((cx,cy,minz))
    finalise(body,a.entity,mat);coords={};barrels=[]
for name,pt in coords.items():
    spot=bpy.data.objects.new(a.entity+'_'+name,None);bpy.context.collection.objects.link(spot)
    spot.parent=body;spot.location=pt;spot.hge_obj_settings.spot_name=name
report={}
for obj in [body]+barrels:
    issues=prepare_export_mesh(obj,strict=False)
    bad={x['triangle'] for x in issues if x['kind'] in ('degenerate','zero_normal')}
    if bad:
        bm=bmesh.new();bm.from_mesh(obj.data);bm.faces.ensure_lookup_table()
        bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES_ONLY')
        bm.to_mesh(obj.data);bm.free()
    report[obj.name]={'removed_degenerate':len(bad),'issues':prepare_export_mesh(obj),'triangles':len(obj.data.polygons)}
blend=a.output/(a.entity+'.blend')
bpy.ops.wm.save_as_mainfile(filepath=str(blend));export_fbx(hge,a.output/(a.entity+'.fbx'))
(a.output/(a.entity+'-report.json')).write_text(json.dumps(report,indent=2))
for i,obj in enumerate(barrels):
    if i==0:obj.parent.location.y=cut
    elif ('MagazineNormal' if a.entity=='JAZZ_M14_MkIII' else 'MagazineShort') in obj.name:obj.parent.location=coords['Magazine']
    else:obj.hide_render=True
assembled=a.output/(a.entity+'-assembled.blend');bpy.ops.wm.save_as_mainfile(filepath=str(assembled))
render_one(assembled,a.output/(a.entity+'-preview.png'))
