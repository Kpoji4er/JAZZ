"""Blender bounded AR15 repair: --blend --weapon M16A4|M4A1 --output --game-root.
M16A4: rifle-position sight, exposed barrel shortened 10 cm. M4: grip-origin fit.
Exports only the affected entity, preserves module-local frames, strict mesh gate.
"""
import argparse, importlib.util, json, sys
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
p=argparse.ArgumentParser()
for n in ('blend','output','game-root'):p.add_argument('--'+n,type=Path,required=True)
p.add_argument('--weapon',choices=('M16A4','M4A1'),required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.blend))
prefix='M16R_M16A4' if a.weapon=='M16A4' else 'M4R_M4A1'
if a.weapon=='M16A4':
    obj=bpy.data.objects[prefix+'_BarrelShort'];normal=bpy.data.objects[prefix+'_Barrel']
    obj.data=normal.data.copy()
    front=min(v.co.y for v in obj.data.vertices)
    for v in obj.data.vertices:
        if v.co.y<front+.0001:v.co.y+=.10
    for child in obj.children:
        if child.hge_obj_settings.spot_name=='Muzzle':child.location.y=front+.10
    # Match the unchanged normal barrel UV/material, not the former M4 donor.
    report={'shortening_m':.10,'entity':obj.name}
else:
    obj=bpy.data.objects[prefix]
    grip=bpy.data.objects[prefix+'_Handgrip']
    # Position of palm contact: upper third of the physical pistol grip.
    points=[grip.matrix_world@v.co for v in grip.data.vertices]
    z0,z1=min(v.z for v in points),max(v.z for v in points)
    contact=[v for v in points if z0+.55*(z1-z0)<v.z<z0+.85*(z1-z0)]
    centre=Vector(tuple((min(v[i] for v in contact)+max(v[i] for v in contact))/2 for i in range(3)))
    offset=-centre
    obj.data.transform(Matrix.Translation(offset))
    for child in obj.children:
        if child.type=='EMPTY':child.location+=offset
    for origin in bpy.data.objects:
        if origin.type=='EMPTY' and origin.name.startswith(prefix+'_') and origin.name.endswith('_Origin') and origin!=obj.parent:
            origin.location+=offset
    report={'entity':obj.name,'grip_contact_m':list(centre),'offset_m':list(offset)}
report['issues']=prepare_export_mesh(obj)
# A separate assembled file retains the other modules solely for review.
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(a.weapon+'-assembled.blend')))
keep={obj,*obj.children}
if obj.parent:keep.add(obj.parent)
for other in list(bpy.data.objects):
    if other not in keep:bpy.data.objects.remove(other,do_unlink=True)
if obj.parent:obj.parent.location=Vector()
spec=importlib.util.spec_from_file_location('ar15_repair_hge',a.game_root/'ModTools/BlenderExport.py')
hge=importlib.util.module_from_spec(spec);spec.loader.exec_module(hge)
hge.SETTINGS.update(version='71',game='Zulu',appid='Jagged Alliance 3',mtl_prop_0_visible=True,mtl_prop_0_name='Unit',enable_colliders=True);hge.register()
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(a.weapon+'.blend')))
with hge.ObjectNamesExportContext(bpy.context):
    bpy.ops.export_scene.fbx(filepath=str(a.output/(a.weapon+'.fbx')),axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
(a.output/'repair-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
