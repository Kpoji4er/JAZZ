"""Blender: rebuild the rejected PASGT rear panel; preserve original front. Preview source only."""
import argparse, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output=a.output.resolve();a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
old=next(o for o in bpy.context.scene.objects if o.type=='MESH')
bm=bmesh.new();bm.from_mesh(old.data)
cut=[f for f in bm.faces if f.calc_center_median().y>.015 and f.calc_center_median().z<1.53]
bmesh.ops.delete(bm,geom=cut,context='FACES');bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(old.data);bm.free()
mat=bpy.data.materials.new('PASGT rebuilt woodland cloth');mat.use_nodes=True
n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');bs.inputs['Roughness'].default_value=.86
coord=n.new('ShaderNodeTexCoord');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=11.;noise.inputs['Detail'].default_value=2.;noise.inputs['Roughness'].default_value=.6
l.new(coord.outputs['Position'] if 'Position' in coord.outputs else coord.outputs['Generated'],noise.inputs['Vector'])
# World-sized, continuous cloth coordinates shared by panel and shoulder strips.
geom=n.new('ShaderNodeNewGeometry');l.new(geom.outputs['Position'],noise.inputs['Vector'])
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='CONSTANT'
palette=[(.0,(.045,.054,.031,1)),(.37,(.14,.125,.079,1)),(.46,(.225,.26,.15,1)),(.59,(.34,.33,.23,1)),(.69,(.14,.17,.09,1))]
for el in list(ramp.color_ramp.elements)[2:]:ramp.color_ramp.elements.remove(el)
for i,(pos,color) in enumerate(palette):
 el=ramp.color_ramp.elements[i] if i<2 else ramp.color_ramp.elements.new(pos);el.position=pos;el.color=color
l.new(noise.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs['Color'],bs.inputs['Base Color'])
fine=n.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=1200.;fine.inputs['Detail'].default_value=1.
l.new(geom.outputs['Position'],fine.inputs['Vector']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.00035;l.new(fine.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal'])
trim=bpy.data.materials.new('PASGT rear edge binding');trim.use_nodes=True;trim.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.16,.175,.10,1);trim.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.88
parts=[old]
def width(t):return .232-.062*max(0,(t-.65)/.35)
def surface(u,t):
 x=u*width(t);z=.995+.522*t
 y=.176-.025*t-.073*abs(u)**2+.0018*math.sin(t*math.pi*5)*(1-u*u)
 return Vector((x,y,z))
def patch(name,coords,faces,material):
 me=bpy.data.meshes.new(name);me.from_pydata(coords,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material)
 uv=me.uv_layers.new(name='SourceUV')
 for f in me.polygons:
  for li in f.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=((v.x+.25)/.5,(v.z-.98)/.56)
 prepare_export_mesh(o);parts.append(o);return o
nx,nz=32,40;coords=[surface(-1+2*i/nx,j/nz) for j in range(nz+1) for i in range(nx+1)]
faces=[(j*(nx+1)+i,(j+1)*(nx+1)+i,(j+1)*(nx+1)+i+1,j*(nx+1)+i+1) for j in range(nz) for i in range(nx)]
panel=patch('Clean rear cloth panel',coords,faces,mat)
def seam(name,pts,radius=.0015):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=radius;c.bevel_resolution=1;s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for p,v in zip(s.points,pts):p.co=(*v,1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(trim);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH');o=bpy.context.object;o.data.uv_layers.new(name='SourceUV');parts.append(o)
for u in (-.98,.98):seam('Rear side binding',[surface(u,j/40)+Vector((0,.001,0)) for j in range(41)])
for t in (.018,.48,.985):seam('Rear horizontal stitch',[surface(-.98+1.96*i/32,t)+Vector((0,.001,0)) for i in range(33)],.0009)
for sign in (-1,1):
 v=[]
 for j in range(14):
  t=.70+.28*j/13
  for u in (sign*.72-.07,sign*.72+.07):v.append(surface(u,t)+Vector((0,.004,0)))
 patch('Rear shoulder reinforcement',v,[(2*j,2*j+2,2*j+3,2*j+1) for j in range(13)],mat)
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=old;bpy.ops.object.join();old=bpy.context.object;old.name='PASGT rebuilt back source';prepare_export_mesh(old)
# Rigging will pack a fresh ExportUV atlas; source materials remain editable.
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'PASGT_rebuilt.blend'))
old.data.calc_loop_triangles();(a.output/'rebuild.json').write_text(json.dumps({'removed_rear_faces':len(cut),'triangles':len(old.data.loop_triangles),'front_preserved':True,'stage':'PREVIEW_NOT_INSTALLED'},indent=2))
