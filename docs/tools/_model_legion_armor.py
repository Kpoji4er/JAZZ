"""Build welded sheet cuirass from the official sample rig; writes staging only."""
import bpy, math, random, json
from pathlib import Path
from mathutils import Vector
import argparse, sys
parser=argparse.ArgumentParser()
parser.add_argument('--sample',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--skip-previews',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
OUT=args.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(args.sample.resolve()))
random.seed(31)
rig=bpy.data.objects['Bip001']; body=bpy.data.objects['M_BaseMesh Skin_BIP']
for o in list(bpy.data.objects):
    if o not in (rig,body): bpy.data.objects.remove(o,do_unlink=True)
for c in bpy.data.collections: c.hide_render=False; c.hide_viewport=False
body.hide_set(False); body.hide_render=False; rig.hide_set(False)
parts=[]
# Interpolate the sample skin at the closest triangle, including clavicle/twist bones.
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
body.data.calc_loop_triangles()
bind_vertices=[body.matrix_world@v.co for v in body.data.vertices]
bind_triangles=[tuple(t.vertices) for t in body.data.loop_triangles]
bind_bvh=BVHTree.FromPolygons(bind_vertices,bind_triangles,all_triangles=True)
def sample_bind(pos):
    co,normal,index,distance=bind_bvh.find_nearest(Vector(pos))
    ids=bind_triangles[index];abc=[bind_vertices[i] for i in ids]
    bary=barycentric_transform(co,*abc,Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)))
    weights={}
    for idx,factor in zip(ids,bary):
        for group in body.data.vertices[idx].groups:
            name=body.vertex_groups[group.group].name
            if name in rig.data.bones and factor>0:weights[name]=weights.get(name,0)+factor*group.weight
    weights=dict(sorted(weights.items(),key=lambda item:item[1],reverse=True)[:4])
    total=sum(weights.values());assert total>0
    return co,normal,{name:w/total for name,w in weights.items() if w>1e-7}

def torso_bind(pos):
    z=pos.z
    if z<1.18:
        t=max(0,min(1,(z-1.04)/.14));return {'Bip001 Spine':1-t,'Bip001 Spine1':t}
    t=max(0,min(1,(z-1.18)/.16));return {'Bip001 Spine1':1-t,'Bip001 Spine2':t}

def mix_bind(a,b,t):
    weights={n:a.get(n,0)*(1-t)+b.get(n,0)*t for n in a.keys()|b.keys()}
    weights=dict(sorted(weights.items(),key=lambda item:item[1],reverse=True)[:4])
    total=sum(weights.values());return {n:w/total for n,w in weights.items() if w>1e-7}

def back_bind(pos):
    # The waist rim must not switch to pelvis/leg weights at nearest triangles.
    # Use one continuous torso field for sheets, lining and their welds.
    if pos.z<=1.15:return {'Bip001 Spine1':1.0}
    if pos.z<1.24:
        weights=sample_bind(Vector((pos.x,pos.y,1.24)))[2]
        return mix_bind({'Bip001 Spine1':1.0},weights,(pos.z-1.15)/.09)
    return sample_bind(pos)[2]

def material(name,col,metal=0,rough=.65,texture=False):
    m=bpy.data.materials.new(name); m.diffuse_color=(*col,1); m.use_nodes=True
    n=m.node_tree.nodes; l=m.node_tree.links; p=n.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*col,1); p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough
    if texture:
        tex=n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value=180; tex.inputs['Detail'].default_value=3
        coords=n.new('ShaderNodeTexCoord'); l.new(coords.outputs['Object'],tex.inputs['Vector'])
        ramp=n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.27; ramp.color_ramp.elements[0].color=(*(c*.78 for c in col),1); ramp.color_ramp.elements[1].position=.74; ramp.color_ramp.elements[1].color=(*(c*1.12 for c in col),1)
        l.new(tex.outputs['Fac'],ramp.inputs[0]); l.new(ramp.outputs[0],p.inputs['Base Color'])
        b=n.new('ShaderNodeBump'); b.inputs['Strength'].default_value=.13; b.inputs['Distance'].default_value=.0009; l.new(tex.outputs['Fac'],b.inputs['Height']); l.new(b.outputs[0],p.inputs['Normal'])
    if metal>.4 and texture:
        # Layer oxidation and fine directional scratches in physical shader inputs.
        ox=n.new('ShaderNodeTexNoise');ox.inputs['Scale'].default_value=31;ox.inputs['Detail'].default_value=4
        l.new(coords.outputs['Object'],ox.inputs['Vector'])
        mask=n.new('ShaderNodeValToRGB');mask.color_ramp.elements[0].position=.55;mask.color_ramp.elements[0].color=(0,0,0,1)
        mask.color_ramp.elements[1].position=.76;mask.color_ramp.elements[1].color=(.8,.8,.8,1);l.new(ox.outputs['Fac'],mask.inputs[0])
        mix=n.new('ShaderNodeMixRGB');mix.inputs[2].default_value=(.12,.047,.017,1)
        l.new(mask.outputs[0],mix.inputs[0]);l.new(ramp.outputs[0],mix.inputs[1])
        direction=n.new('ShaderNodeVectorMath');direction.operation='MULTIPLY';direction.inputs[1].default_value=(700,700,26)
        l.new(coords.outputs['Object'],direction.inputs[0])
        scratch=n.new('ShaderNodeTexNoise');scratch.inputs['Scale'].default_value=1;scratch.inputs['Detail'].default_value=2
        l.new(direction.outputs[0],scratch.inputs['Vector'])
        scratchmask=n.new('ShaderNodeValToRGB');scratchmask.color_ramp.elements[0].position=.72;scratchmask.color_ramp.elements[0].color=(0,0,0,1)
        scratchmask.color_ramp.elements[1].position=.79;scratchmask.color_ramp.elements[1].color=(.65,.65,.65,1);l.new(scratch.outputs['Fac'],scratchmask.inputs[0])
        scratchmix=n.new('ShaderNodeMixRGB');scratchmix.inputs[2].default_value=(.27,.27,.25,1)
        l.new(scratchmask.outputs[0],scratchmix.inputs[0]);l.new(mix.outputs[0],scratchmix.inputs[1]);l.new(scratchmix.outputs[0],p.inputs['Base Color'])
        roughmix=n.new('ShaderNodeMapRange');roughmix.inputs['To Min'].default_value=.38;roughmix.inputs['To Max'].default_value=.88
        l.new(mask.outputs[0],roughmix.inputs[0]);l.new(roughmix.outputs[0],p.inputs['Roughness'])
        bevelnode=n.new('ShaderNodeBevel');bevelnode.inputs['Radius'].default_value=.001;bevelnode.samples=4
        l.new(bevelnode.outputs[0],b.inputs['Normal'])
    return m
leather=material('Dark oxblood leather backing',(.031,.018,.014),0,.91,True)
edge=material('Worn leather edging',(.073,.039,.023),0,.84,True)
metals=[material('Scrap steel %02d'%i,c,.6,.68,True) for i,c in enumerate([(.105,.099,.087),(.085,.091,.088),(.11,.084,.062),(.080,.074,.064),(.12,.105,.084),(.071,.077,.076)])]
cutedge=material('Exposed cut steel',(.26,.27,.25),.85,.32,True)
stud=material('Dark iron rivets',(.16,.13,.093),.75,.47,True)
body.data.materials.clear(); body.data.materials.append(material('Slate fitting mannequin',(.048,.062,.065),0,.86))
def meshpart(name,verts,faces,mat,bone,thickness=0,bevel=0):
    part_name=name
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update()
    o=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(o)
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); bpy.context.view_layer.objects.active=o
    o.data.materials.append(mat)
    steel=mat.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value>.4
    if steel:o.data.materials.append(cutedge)
    if thickness:
        mod=o.modifiers.new('Thickness','SOLIDIFY'); mod.thickness=thickness; mod.offset=0; mod.material_offset_rim=1 if steel else 0; bpy.ops.object.modifier_apply(modifier=mod.name)
    if bevel:
        mod=o.modifiers.new('Rounded worn edges','BEVEL'); mod.width=bevel; mod.segments=2; mod.affect='EDGES'; mod.material=1 if steel else -1; bpy.ops.object.modifier_apply(modifier=mod.name)
    if name.startswith(('Bent welded','Flexible leather','Shallow bent')):
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(35))
    binder=bone if callable(bone) else None
    if bone=='TORSO':
        binder=back_bind if sum(v.co.y for v in o.data.vertices)/max(1,len(o.data.vertices))>0 else torso_bind
    elif bone in ('SHOULDER','SURFACE'):binder=lambda p:sample_bind(p)[2]
    if binder:
        groups={}
        for v in o.data.vertices:
            for name,w in binder(v.co).items():
                if w<=1e-7:continue
                if name not in groups:groups[name]=o.vertex_groups.new(name=name)
                groups[name].add([v.index],w,'REPLACE')
    else:o.vertex_groups.new(name=bone).add(list(range(len(o.data.vertices))),1,'REPLACE')
    role=1 if part_name=='Bent welded chest sheet' else 2 if part_name=='Bent welded back sheet' else 3 if part_name=='Leather lined lower edge' and sum(v.co.y for v in o.data.vertices)>0 else 4 if part_name=='Flexible leather shoulder strap' else 0
    attr=o.data.attributes.new('qa_role','INT','POINT')
    for value in attr.data:value.value=role
    a=o.modifiers.new('JA3 skeleton','ARMATURE'); a.object=rig; parts.append(o); o.select_set(False); return o
def rivet(pos,normal,bone,r=.003):
    normal=Vector(normal).normalized(); u=normal.cross(Vector((0,0,1)))
    if u.length<.1: u=normal.cross(Vector((0,1,0)))
    u.normalize(); v=normal.cross(u); c=Vector(pos)
    verts=[tuple(c+u*math.cos(i*math.tau/6)*r+v*math.sin(i*math.tau/6)*r) for i in range(6)]+[tuple(c+normal*r*.52)]
    return meshpart('Peened rivet',verts,[(i,(i+1)%6,6) for i in range(6)],stud,bone)
def radius(z):
    return .203+.027*max(0,min(1,(z-1.04)/.30))
def surface(a,z,offset=0):
    # Negative Y is front; the shell follows the actual sample torso.
    ry=.184 if math.cos(a)>0 else (.205-.047*max(0,min(1,(z-1.16)/.25)))
    rx=(.198+.034*max(0,min(1,(z-1.05)/.30))) if math.cos(a)>0 else radius(z)
    return Vector(((rx+offset)*math.sin(a),-.018-(ry+offset)*math.cos(a),z))
def normal(a): return Vector((math.sin(a),-math.cos(a),0))
def band(name,a0,a1,z0,z1,mat,bone,offset=.0,steps=8,thick=.004):
    vs=[surface(a0+(a1-a0)*i/steps,z,offset) for z in (z0,z1) for i in range(steps+1)]
    fs=[(i,i+1,steps+2+i,steps+1+i) for i in range(steps)]
    return meshpart(name,vs,fs,mat,bone,thick,.0007)

# Broad faceted sheets, with visible welds instead of a tiled vest.
salvage=material('Salvaged faded ochre painted iron',(.17,.135,.064),.48,.61,True)
weld=material('Uneven bright weld metal',(.19,.17,.135),.8,.5,True)
def seam(points,bone='TORSO',r=.0022):
    vs=[]
    for i,pt in enumerate(points):
        tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])
        tangent.normalize(); u=tangent.cross(Vector((0,0,1)))
        if u.length<.1:u=tangent.cross(Vector((0,1,0)))
        u.normalize(); v=tangent.cross(u)
        for j in range(6):
            rr=r*random.uniform(.80,1.20); q=j*math.tau/6
            vs.append(Vector(pt)+rr*(u*math.cos(q)+v*math.sin(q)))
    meshpart('Raised irregular weld',vs,[(i*6+j,i*6+(j+1)%6,(i+1)*6+(j+1)%6,(i+1)*6+j) for i in range(len(points)-1) for j in range(6)],weld,bone)
# Leather only lines the edge; the outer surface is large joined metal sheets.
for side in (0,math.pi):
    for col,(a0,a1) in enumerate([(-1.10,-.36),(-.36,.36),(.36,1.10)]):
        aa=[side+a0+(a1-a0)*i/3 for i in range(4)]
        zz=[1.045,1.13,1.22,1.30,1.385] if side==0 else [1.065,1.15,1.24,1.33,1.410]
        vs=[surface(a,z-((.042 if side==0 else .070)*abs(math.sin(a))**4 if row==4 else 0),.006) for row,z in enumerate(zz) for a in aa]
        fs=[(row*4+i,row*4+i+1,(row+1)*4+i+1,(row+1)*4+i) for row in range(4) for i in range(3)]
        meshpart('Bent welded chest sheet' if side==0 else 'Bent welded back sheet',vs,fs,metals[(col+(0 if side==0 else 1))%6],'TORSO',.005,.001)
        if col<2:
            seam([surface(side+a1,(1.049+i*.008 if side==0 else 1.068+i*.0083),.010) for i in range(41)])
    # Exposed worn binding around the lower iron edge.
    band('Leather lined lower edge',side-1.10,side+1.10,(1.029 if side==0 else 1.052),(1.046 if side==0 else 1.068),edge,'TORSO',.009,12,.006)
    # A short horizontal repair weld, with an irregular sheet patch.
    pa=side+(.18 if side==0 else -.58)
    coords=[(pa-.19,1.16),(pa+.12,1.153),(pa+.185,1.18),(pa+.175,1.25),(pa+.11,1.266),(pa-.16,1.278)]
    meshpart('Welded scrap repair patch',[surface(a,z,.013) for a,z in coords],[tuple(range(len(coords)))],salvage,'TORSO',.003,.0006)
    for k in range(len(coords)):
        a0,z0=coords[k];a1,z1=coords[(k+1)%len(coords)]
        seam([surface(a0+(a1-a0)*i/12,z0+(z1-z0)*i/12,.016) for i in range(13)],r=.0017)
# Two rough iron repair braces break the regular back silhouette.
for a0,z0,a1,z1 in [(math.pi-.81,1.14,math.pi-.30,1.20),(math.pi+.22,1.28,math.pi+.86,1.32)]:
    vs=[surface(a0+(a1-a0)*i/5,z0+(z1-z0)*i/5+dz,.017) for i in range(6) for dz in (-.009,.009)]
    meshpart('Welded salvaged iron brace',vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(5)],metals[4],'TORSO',.005,.001)
    for aa,zz in ((a0+.045,z0),(a1-.045,z1)):rivet(surface(aa,zz,.023),normal(aa),'TORSO',.004)

# Open flanks and straps leave clearance for arm motion.
for side in (-math.pi/2,math.pi/2):
    for z in (1.09,1.25):
        band('Side fastening leather',side-.51,side+.51,z-.018,z+.018,leather,'TORSO',.006,6,.007)
        band('Forged side buckle',side-.055,side+.055,z-.023,z+.023,stud,'TORSO',.013,2,.004)
# Find anchors on the actual faceted iron, not on the body hidden underneath.
plate_surfaces={}
for side,label in ((-1,'chest'),(1,'back')):
    vv=[];ff=[]
    for obj in parts:
        if obj.name.startswith('Bent welded '+label):
            offset=len(vv);vv.extend(v.co.copy() for v in obj.data.vertices)
            ff.extend(tuple(offset+i for i in poly.vertices) for poly in obj.data.polygons)
    plate_surfaces[side]=BVHTree.FromPolygons(vv,ff)
strap_checks=[]
for x in (-.128,.128):
    path=[(-.191,1.35),(-.167,1.411),(-.133,1.457),(-.081,1.484),(-.025,1.498),(.034,1.495),(.091,1.476),(.133,1.439),(.158,1.382)]
    path=[(path[i][0]+(path[i+1][0]-path[i][0])*t/3,path[i][1]+(path[i+1][1]-path[i][1])*t/3) for i in range(len(path)-1) for t in range(3)]+[path[-1]]
    centers=[];normals=[];bindings=[]
    for y,z in path:
        co,n,w=sample_bind(Vector((x,y,z)));centers.append(co+n*.014);normals.append(n);bindings.append(w)
    for side,indices,zs in ((-1,(0,1,2),(1.325,1.345,1.365)),(1,(24,23,22),(1.34,1.36,1.38))):
        for i,z in zip(indices,zs):
            co,n,_,_=plate_surfaces[side].find_nearest(Vector((x,side*.19,z)))
            if n.y*side<0:n=-n
            gap=.009 if side>0 else .004
            centers[i]=co+n*gap;normals[i]=n
            bindings[i]=(torso_bind if side<0 else back_bind)(co)
            strap_checks.append({'side':side,'x':x,'row':i,'plate_gap_m':gap,'position':list(centers[i]),'weights':bindings[i]})
    # Blend from the overlapping leather ends to the shoulder contour.
    for start,end in ((2,7),(17,22)):
        for i in range(start+1,end):
            t=(i-start)/(end-start);centers[i]=centers[start].lerp(centers[end],t)
            normals[i]=normals[start].lerp(normals[end],t).normalized()
            bindings[i]=mix_bind(bindings[start],bindings[end],t)
    def strap_bind(pos,cc=centers,ww=bindings):
        best=None
        for i in range(len(cc)-1):
            segment=cc[i+1]-cc[i];t=max(0,min(1,(pos-cc[i]).dot(segment)/segment.length_squared))
            distance=(pos-(cc[i]+segment*t)).length_squared
            if best is None or distance<best[0]:best=(distance,i,t)
        _,i,t=best;return mix_bind(ww[i],ww[i+1],t)
    verts=[]
    for i,co in enumerate(centers):
        for dx in (-.018,.018):
            v=co+Vector((dx,0,0))
            if i>=22:
                # Both rails follow the plate, rather than a flat ribbon crossing it.
                q,n,_,_=plate_surfaces[1].find_nearest(v)
                if n.y<0:n=-n
                v=q+n*.009
            verts.append(v)
    meshpart('Flexible leather shoulder strap',verts,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(path)-1)],edge,strap_bind,.007,.001)
    co=centers[4];n=normals[4];c=co+n*.006
    for dx0,dx1,dz0,dz1 in [(-.023,-.017,-.013,.013),(.017,.023,-.013,.013),(-.023,.023,-.013,-.008),(-.023,.023,.008,.013)]:
        vs=[c+Vector((dx,0,dz)) for dx,dz in [(dx0,dz0),(dx1,dz0),(dx1,dz1),(dx0,dz1)]]
        meshpart('Forged shoulder strap buckle',vs,[(0,1,2,3)],stud,strap_bind,.003,.0007)
    for i in (0,1,23,24):
        for dx in (-.009,.009):rivet(centers[i]+Vector((dx,0,0))+normals[i]*.005,normals[i],strap_bind,.003)
# Small angular shoulder guard: folded sheet, with two overlapping lower strips.
# No circular rim, radial wedges or bowl. Its long axis follows the upper arm.
bone='SURFACE'
for row in range(2):
    # Shallow, chamfered cap with a smooth curve across the shoulder.
    x=-.195-row*.058; z=1.509-row*.028
    profile=[(-.088,-.043),(-.071,-.018),(-.04,-.004),(0,0),(.038,-.005),(.067,-.020),(.082,-.043)]
    verts=[(xx,y*(.94 if edge else 1),z+dz-(.036 if edge else 0)) for edge,xx in enumerate((x,x-.082)) for y,dz in profile]
    meshpart('Shallow bent shoulder iron',verts,[(i,i+1,i+8,i+7) for i in range(6)],salvage if row==0 else metals[2],bone,.005,.0018)
    if row==0: seam([Vector(verts[1]).lerp(Vector(verts[5]),i/16) for i in range(17)],bone,.0018)
    for idx in (1,5):rivet(Vector(verts[idx])+Vector((0,0,.004)),(0,0,1),bone,.0045)

# Two visible leather supports bridge the chest harness to the shoulder guard.
for y in (-.043,.042):
    points=[(-.127,y,1.497),(-.153,y,1.501),(-.178,y,1.505),(-.203,y,1.511),(-.232,y,1.505)]
    verts=[(x,yy+dy,z) for x,yy,z in points for dy in (-.011,.011)]
    meshpart('Shoulder guard retaining strap',verts,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(4)],leather,'SHOULDER',.004,.0007)

# Single export mesh with original sample skeleton and real UVs.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]; bpy.ops.object.join(); armor=bpy.context.object; armor.name='TEST_ImprovisedCuirass_Male_v7'
armor['qa_anchors']=json.dumps(strap_checks)
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.normals_make_consistent(inside=False); bpy.ops.uv.smart_project(island_margin=.008); bpy.ops.object.mode_set(mode='OBJECT')
armor.parent=rig; armor.data.calc_loop_triangles()
report={'vertices':len(armor.data.vertices),'triangles':len(armor.data.loop_triangles),'unweighted_vertices':sum(not any(g.weight>0 for g in v.groups) for v in armor.data.vertices),'reference':'ArmorIcons/ImprovisedCuirass.png','status':'Welded sheet iron prototype; full Legion animation coverage unverified','materials':'Procedural; not baked for JA3','strap_anchors':strap_checks,'lower_back_binding':'continuous Spine1 lower edge shared by plate and lining'}
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
bpy.ops.object.select_all(action='DESELECT'); armor.select_set(True); rig.select_set(True); bpy.context.view_layer.objects.active=armor
bpy.ops.export_scene.fbx(filepath=str(OUT/'improvised_cuirass_v7.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},add_leaf_bones=False,bake_anim=False)
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.samples=48; scene.cycles.use_denoising=True
scene.render.resolution_x=1200; scene.render.resolution_y=1200; scene.render.resolution_percentage=100
scene.world.use_nodes=True; scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.055,.055,.055,1); scene.world.node_tree.nodes['Background'].inputs[1].default_value=.45
scene.view_settings.view_transform='AgX'
def aim(o,pt):o.rotation_euler=(Vector(pt)-o.location).to_track_quat('-Z','Y').to_euler()
for name,loc,power,size in [('Key',(-1.3,-2,3),110,1.6),('Fill',(2,-1,1.7),65,1.5),('Rim',(-1,2,2.6),150,1.2)]:
    bpy.ops.object.light_add(type='AREA',location=loc); o=bpy.context.object; o.name=name; o.data.energy=power; o.data.shape='DISK'; o.data.size=size; aim(o,(0,0,1.25))
bpy.ops.object.camera_add(location=(-.95,-2.6,1.85)); camera=bpy.context.object; camera.data.type='ORTHO'; camera.data.ortho_scale=.90; aim(camera,(-.035,0,1.29)); scene.camera=camera
for area in bpy.context.screen.areas:
    if area.type=='VIEW_3D':
        area.spaces.active.region_3d.view_distance=1.1; area.spaces.active.region_3d.view_location=Vector((0,0,1.25))
bpy.ops.object.select_all(action='DESELECT'); armor.select_set(True); bpy.context.view_layer.objects.active=armor
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'improvised_cuirass_v7.blend'))
if args.skip_previews:
    print('REPORT',report); raise SystemExit(0)
scene.render.filepath=str(OUT/'on_body.png'); bpy.ops.render.render(write_still=True)
body.hide_render=True; camera.data.ortho_scale=.76; aim(camera,(-.035,0,1.28)); scene.render.film_transparent=True
scene.render.filepath=str(OUT/'armor_front.png'); bpy.ops.render.render(write_still=True)
camera.location=(1.1,2.6,1.85); aim(camera,(-.035,0,1.28)); scene.render.filepath=str(OUT/'armor_back.png'); bpy.ops.render.render(write_still=True)
print('REPORT',report)


