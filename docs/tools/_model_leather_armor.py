"""Author the improvised leather carrier, source only, from its existing icon.

Blender --background --python this.py -- --sample BLEND --shirt JSON --output DIR
Writes clean parts, studio/clothed views and a mesh audit. Never installs assets.
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

p = argparse.ArgumentParser()
for key in ('sample', 'shirt', 'output'):
    p.add_argument('--' + key, required=True, type=Path)
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
out = a.output.resolve()
(out / 'clean').mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.sample))
for obj in list(bpy.data.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for c in bpy.data.collections:
    c.hide_render = False
    c.hide_viewport = False

data = json.loads(a.shirt.read_text())
src = data['meshes'][1]
box = src.get('bbox') or data['bbox']
centre = [(box[i] + box[i + 3]) / 2 for i in range(3)]
shirt_v = [Vector((-(v[1] + centre[1]), -(v[0] + centre[0]), v[2] + centre[2]))
           for v in src['vertices']]
shirt_f = [tuple(reversed(f)) for f in src['faces']]
bvh = BVHTree.FromPolygons(shirt_v, shirt_f)

# Smooth radial fitting field: isolated shirt folds must not kink stiff hide.
NZ, NT = 64, 128
zgrid = np.linspace(1.04, 1.51, NZ)
radius_grid = np.full((NZ, NT), np.nan)
for iz, z in enumerate(zgrid):
    for it in range(NT):
        th = 2*math.pi*it/NT
        hit = bvh.ray_cast(Vector((0,-.01,float(z))),Vector((math.sin(th),-math.cos(th),0)),.5)
        if hit[0] is not None: radius_grid[iz,it] = min(.24,hit[3])
known = np.argwhere(np.isfinite(radius_grid))
for iz,it in np.argwhere(~np.isfinite(radius_grid)):
    dt=np.minimum(abs(known[:,1]-it),NT-abs(known[:,1]-it))
    j,k=known[np.argmin((known[:,0]-iz)**2+dt**2)]
    radius_grid[iz,it]=radius_grid[j,k]
for _ in range(20):
    padded=np.pad(radius_grid,((1,1),(0,0)),mode='edge')
    radius_grid=(4*radius_grid+np.roll(radius_grid,1,1)+np.roll(radius_grid,-1,1)+padded[:-2]+padded[2:])/8

def material(name, color, rough=.8, metal=0, grain=True):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    n, links = m.node_tree.nodes, m.node_tree.links
    shader = n.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Roughness'].default_value = rough
    shader.inputs['Metallic'].default_value = metal
    if grain:
        tex = n.new('ShaderNodeTexCoord')
        slow = n.new('ShaderNodeTexNoise')
        slow.inputs['Scale'].default_value = 28
        slow.inputs['Detail'].default_value = 4
        links.new(tex.outputs['Object'], slow.inputs['Vector'])
        ramp = n.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].position = .18
        ramp.color_ramp.elements[0].color = (*(c * .65 for c in color), 1)
        ramp.color_ramp.elements[1].position = .82
        ramp.color_ramp.elements[1].color = (*(min(1, c * 1.5) for c in color), 1)
        links.new(slow.outputs['Fac'], ramp.inputs[0])
        links.new(ramp.outputs[0], shader.inputs['Base Color'])
        pores = n.new('ShaderNodeTexNoise')
        pores.inputs['Scale'].default_value = 760
        pores.inputs['Detail'].default_value = 2
        links.new(tex.outputs['Object'], pores.inputs['Vector'])
        bump = n.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = .42
        bump.inputs['Distance'].default_value = .00065
        links.new(pores.outputs['Fac'], bump.inputs['Height'])
        # Broken polygonal grain and wider creases, not uniform fine cloth noise.
        grain_cells=n.new('ShaderNodeTexVoronoi')
        grain_cells.feature='DISTANCE_TO_EDGE'
        grain_cells.inputs['Scale'].default_value=215
        links.new(tex.outputs['Object'],grain_cells.inputs['Vector'])
        groove=n.new('ShaderNodeValToRGB')
        groove.color_ramp.elements[0].position=.012
        groove.color_ramp.elements[0].color=(.12,.12,.12,1)
        groove.color_ramp.elements[1].position=.065
        groove.color_ramp.elements[1].color=(.75,.75,.75,1)
        links.new(grain_cells.outputs['Distance'],groove.inputs[0])
        grain_bump=n.new('ShaderNodeBump')
        grain_bump.inputs['Strength'].default_value=.38
        grain_bump.inputs['Distance'].default_value=.0008
        links.new(groove.outputs[0],grain_bump.inputs['Height'])
        links.new(bump.outputs[0],grain_bump.inputs['Normal'])
        links.new(grain_bump.outputs[0],shader.inputs['Normal'])
        rough_map=n.new('ShaderNodeMapRange')
        rough_map.inputs['From Min'].default_value=.18
        rough_map.inputs['From Max'].default_value=.82
        rough_map.inputs['To Min'].default_value=max(.34,rough-.20)
        rough_map.inputs['To Max'].default_value=min(.90,rough+.08)
        links.new(slow.outputs['Fac'],rough_map.inputs[0])
        links.new(rough_map.outputs[0],shader.inputs['Roughness'])
        grain_color=n.new('ShaderNodeMixRGB');grain_color.blend_type='MULTIPLY'
        grain_color.inputs[0].default_value=.24
        links.new(ramp.outputs[0],grain_color.inputs[1])
        links.new(groove.outputs[0],grain_color.inputs[2])
        links.new(grain_color.outputs[0],shader.inputs['Base Color'])
    return m

leather = material('Aged chestnut hide', (.042, .016, .006), .65)
edge = material('Dark doubled leather binding', (.014, .006, .002), .66)
straps = material('Oiled leather straps', (.023, .010, .004), .60)
patch = material('Replacement russet leather', (.066, .023, .008), .72)
thread = material('Dirty waxed linen stitch', (.30, .225, .135), .94, grain=False)
steel = material('Oxidized iron rivets', (.11, .092, .066), .56, .65)
shirt_mat = material('Neutral fitting shirt', (.055, .070, .061), .95, grain=False)
parts = []
contact_surfaces = {}

def tag(obj,name,value):
    attr=obj.data.attributes.new(name=name,type='INT',domain='POINT')
    attr.data.foreach_set('value',[value]*len(obj.data.vertices))

def mesh(name, verts, faces, mat, thick=0):
    m = bpy.data.meshes.new(name)
    m.from_pydata(verts, [], faces)
    m.update()
    obj = bpy.data.objects.new(name, m)
    bpy.context.collection.objects.link(obj)
    m.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    if thick:
        mod = obj.modifiers.new('Hide thickness', 'SOLIDIFY')
        mod.thickness, mod.offset = thick, 1
        bpy.ops.object.modifier_apply(modifier=mod.name)
    prepare_export_mesh(obj)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(island_margin=.012)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj['hg_colorization'] = 0
    parts.append(obj)
    return obj

def grid(rows, cols):
    return [(r*cols+c, r*cols+c+1, (r+1)*cols+c+1, (r+1)*cols+c)
            for r in range(rows-1) for c in range(cols-1)]

def surface(theta, z, offset=.016):
    t=(theta%(2*math.pi))*NT/(2*math.pi);it=int(t);ft=t-it
    zz=max(0,min(NZ-1.00001,(z-zgrid[0])/(zgrid[-1]-zgrid[0])*(NZ-1)))
    iz=int(zz);fz=zz-iz
    radius=(radius_grid[iz,it]*(1-ft)+radius_grid[iz,(it+1)%NT]*ft)*(1-fz)
    radius+=(radius_grid[iz+1,it]*(1-ft)+radius_grid[iz+1,(it+1)%NT]*ft)*fz
    return Vector((math.sin(theta)*(radius+offset), -.01-math.cos(theta)*(radius+offset), z))

def tube(name, points, radius, mat, sides=6):
    vs, fs = [], []
    for i, pt in enumerate(points):
        tangent = (points[min(i+1,len(points)-1)]-points[max(0,i-1)]).normalized()
        axis = tangent.cross(Vector((0,1,0)))
        if axis.length < .01:
            axis = tangent.cross(Vector((0,0,1)))
        axis.normalize()
        other = tangent.cross(axis).normalized()
        for j in range(sides):
            q = pt + radius*(axis*math.cos(j*2*math.pi/sides)+other*math.sin(j*2*math.pi/sides))
            vs.append(q)
    for i in range(len(points)-1):
        for j in range(sides):
            k=i*sides+j; n=i*sides+(j+1)%sides
            fs.append((k,n,n+sides,k+sides))
    fs += [tuple(reversed(range(sides))), tuple((len(points)-1)*sides+j for j in range(sides))]
    return mesh(name, vs, fs, mat)

def rivet(name, pos, normal):
    normal = normal.normalized()
    u = normal.cross(Vector((0,0,1))).normalized()
    v = normal.cross(u).normalized()
    vs = [pos + u*.004*math.cos(t*math.pi/4) + v*.004*math.sin(t*math.pi/4) for t in range(8)]
    vs.append(pos + normal*.0025)
    return mesh(name, vs, [(i,(i+1)%8,8) for i in range(8)] + [tuple(reversed(range(8)))], steel)

def boundary(rows, cols):
    return (list(range(cols)) + [r*cols+cols-1 for r in range(1,rows)] +
            [(rows-1)*cols+c for c in range(cols-2,-1,-1)] +
            [r*cols for r in range(rows-2,0,-1)])

def panel(name, base, span, low, high, mat, offset, rows=18, cols=25):
    vertices=[]
    for r in range(rows):
        t=r/(rows-1)
        for c in range(cols):
            u=2*c/(cols-1)-1
            # Broad straight lower lip and rounded domed chest like the inventory icon.
            bottom=low+.012*abs(u)**4
            top=high-.090*abs(u)**2.6
            theta=base+u*span*(.96+.04*math.sin(math.pi*t))
            z=bottom+(top-bottom)*t
            vertices.append(surface(theta,z,offset))
    obj=mesh(name, vertices, grid(rows,cols),mat,.006)
    if name in ('Plate envelope','Back leather pad'):
        side=1 if name=='Plate envelope' else 2
        tag(obj,'leather_surface',side)
        contact_surfaces[side]=BVHTree.FromPolygons([v.co for v in obj.data.vertices],
                                                   [tuple(p.vertices) for p in obj.data.polygons])
    ids=boundary(rows,cols)
    rim=[vertices[i]+Vector((math.sin(base+(2*(i%cols)/(cols-1)-1)*span),
          -math.cos(base+(2*(i%cols)/(cols-1)-1)*span),0))*.006 for i in ids]
    if name in ('Plate envelope','Back leather pad'):
        # Binding terminates under the sewn straps instead of sticking through
        # their surface as pointed little wedges at the upper corners.
        groups=[];segment=[]
        for point in rim+[rim[0]]:
            covered=.077<abs(point.x)<.139 and point.z>1.30
            if covered:
                if len(segment)>1:groups.append(segment)
                segment=[]
            else:segment.append(point)
        if len(segment)>1:groups.append(segment)
        for segment in groups:tube(name+' rolled hide edge',segment,.004,edge)
    else:
        tube(name+' rolled hide edge',rim+[rim[0]],.004,edge)
    # Distinct little stitches, grouped into one mesh to keep the clean scene usable.
    stitch_v,stitch_f=[],[]
    for i in range(0,len(rim)-1,2):
        start=rim[i].lerp(rim[i+1],.18); end=rim[i].lerp(rim[i+1],.72)
        d=(end-start).normalized(); side=d.cross(Vector((0,1,0)))
        if side.length<.1:side=Vector((1,0,0))
        side=side.normalized()*.0008
        k=len(stitch_v)
        stitch_v.extend((start+side,start-side,end-side,end+side))
        stitch_f.append((k,k+1,k+2,k+3))
    mesh(name+' saddle stitch',stitch_v,stitch_f,thread)
    return vertices

panel('Rounded chest hide',0,.93,1.085,1.405,leather,.018)
panel('Back leather pad',math.pi,.69,1.10,1.385,edge,.018,17,21)
panel('Plate envelope',0,.70,1.108,1.378,leather,.030,17,21)
# The plate is inside the envelope; a shallow leather closing flap marks its mouth.
flap=[surface(-.35+.70*c/16,1.317+.037*r/3,.043) for r in range(4) for c in range(17)]
mesh('Plate pocket closure flap',flap,grid(4,17),patch,.0035)

for sign in (-1,1):
    # Wide shoulder straps follow the real shirt, ending in long overlaps on both pads.
    vs=[]; rows=49; cols=5
    profile=[]
    for r in range(rows):
        angle=math.pi*r/(rows-1)
        d=Vector((0,-math.cos(angle),math.sin(angle)))
        hit=bvh.ray_cast(Vector((sign*.105,-.01,1.285)),d,.6)
        profile.append(hit[3] if hit[0] is not None else .20)
    for _ in range(8):
        profile=[profile[0]]+[(profile[i-1]+2*profile[i]+profile[i+1])/4 for i in range(1,rows-1)]+[profile[-1]]
    for r in range(rows):
        t=r/(rows-1); angle=math.pi*t
        for c in range(cols):
            x=sign*(.105+.01*math.sin(angle))+(c/(cols-1)-.5)*.043
            radius=profile[r]+.013+.017*abs(math.cos(angle))**4
            vs.append(Vector((x,-.01-math.cos(angle)*radius,1.285+math.sin(angle)*radius)))
    # Project EVERY vertex of the sewn overlap onto the actual solidified pad.
    # End-only corrections leave the neighbouring rows hovering over the rim.
    for end,side in ((0,1),(rows-1,2)):
        direction=Vector((0,1 if side==1 else -1,0))
        for r in range(rows):
            distance=abs(r-end)
            if distance>10:continue
            for c in range(cols):
                i=r*cols+c;old=vs[i]
                origin=Vector((old.x,-1 if side==1 else 1,old.z))
                hit=contact_surfaces[side].ray_cast(origin,direction,2)
                if hit[0] is None:continue
                seated=hit[0]-direction*.00035
                vs[i]=seated
    strap=mesh(('Left' if sign<0 else 'Right')+' shoulder strap',vs,grid(rows,cols),straps,.0035)
    attr=strap.data.attributes.new(name='leather_anchor',type='INT',domain='POINT')
    # The inner, sewn footprint is identified geometrically after solidification.
    for v in strap.data.vertices:
        if v.co.z<1.325:
            side=1 if v.co.y<0 else 2
            co,normal,index,distance=contact_surfaces[side].find_nearest(v.co)
            if distance<.0012:attr.data[v.index].value=side
    for r in (1,3,45,47):
        pt=vs[r*cols+2]
        normal=Vector((pt.x,pt.y+.01,.2 if r<10 else 0)).normalized()
        rivet('Shoulder anchor',pt+normal*.004,normal)
    for z in (1.13,1.22):
        belt=[surface(sign*(.78+(math.pi-1.40)*r/24),z+(c/3-.5)*.032,.026)
              for r in range(25) for c in range(4)]
        mesh('Side closing strap',belt,grid(25,4),straps,.005)
        theta=sign*1.48
        corners=[surface(theta+dt,z+dz,.036) for dt,dz in ((-.10,-.023),(.10,-.023),(.10,.023),(-.10,.023),(-.10,-.023))]
        tube('Hand forged side buckle',corners,.0032,steel)
        tube('Buckle tongue',[surface(theta-.10,z,.039),surface(theta+.10,z,.039)],.0017,steel)

for theta in (-.82,.82):
    for z in (1.12,1.19,1.26):
        n=Vector((math.sin(theta),-math.cos(theta),0))
        rivet('Chest binding rivet',surface(theta,z,.031),n)

# Small asymmetric repair sewn into the lower right corner.
repair=[surface(.28+.25*c/4,1.14+.055*r/4,.041) for r in range(5) for c in range(5)]
mesh('Hand cut repair patch',repair,grid(5,5),patch,.002)
for r in (0,4):
    for c in range(5):
        pos=repair[r*5+c]
        tube('Patch stitch',[pos+Vector((-.002,-.003,0)),pos+Vector((.002,-.003,.004))],.0007,thread,4)

for obj in parts:
    obj.data.calc_loop_triangles()
triangles=sum(len(obj.data.loop_triangles) for obj in parts)
assert triangles<17000,triangles

scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.device='CPU'
scene.cycles.samples=32
scene.cycles.use_denoising=True
scene.render.resolution_x=900;scene.render.resolution_y=900
scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.055,.065,.07,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.5
def aim(obj,point):obj.rotation_euler=(Vector(point)-obj.location).to_track_quat('-Z','Y').to_euler()
for name,loc,energy,size in [('Key',(-1.2,-1.8,2.8),170,1.5),('Fill',(1.6,-.9,1.5),95,1.2),('Rim',(.7,1.8,2.5),180,1.1)]:
    bpy.ops.object.light_add(type='AREA',location=loc)
    obj=bpy.context.object;obj.name=name;obj.data.energy=energy;obj.data.shape='DISK';obj.data.size=size;aim(obj,(0,0,1.3))
bpy.ops.object.camera_add()
cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=.64;scene.camera=cam
shirt=mesh('QA reference shirt',shirt_v,shirt_f,shirt_mat)
parts.remove(shirt)
shirt.hide_render=True
for name,loc in [('front',(0,-2.5,1.36)),('back',(0,2.5,1.36)),('side',(2.5,0,1.36)),('oblique',(-1.4,-2.5,1.6))]:
    cam.location=loc;aim(cam,(0,0,1.325));scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
cam.location=(0,-2.5,1.34);cam.data.ortho_scale=.36;aim(cam,(0,-.12,1.33))
scene.render.filepath=str(out/'anchors-detail.png');bpy.ops.render.render(write_still=True)
shirt.hide_render=False
cam.location=(-1.4,-2.5,1.6);cam.data.ortho_scale=.9;aim(cam,(0,0,1.30))
scene.render.filepath=str(out/'clothed.png');bpy.ops.render.render(write_still=True)
for obj in list(bpy.data.objects):
    if obj not in parts:bpy.data.objects.remove(obj,do_unlink=True)
bpy.ops.file.pack_all()
scene['asset_item']='JazzArmor_LeatherArmor'
scene['asset_status']='clean source only; no runtime installation'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'clean/JazzArmor_LeatherArmor.blend'))
(out/'model-report.json').write_text(json.dumps({'item':'JazzArmor_LeatherArmor','stage':'clean','triangles':triangles,'parts':len(parts),'runtime':'NOT_RUN'},indent=2))
print('LEATHER_MODEL',triangles,'triangles',len(parts),'parts')
