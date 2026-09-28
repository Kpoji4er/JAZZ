"""Blender read-only grip-to-fore-end measurements: --blend FILE --entity ID --output JSON."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser()
for k in ('blend','entity','output'):p.add_argument('--'+k,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=a.blend)
obj=bpy.data.objects[a.entity]
spot=next(c for c in obj.children if c.type=='EMPTY' and c.hge_obj_settings.spot_name=='Hand_l_grip')
rows=[]
for dy in (-.03,0,.03):
 origin=Vector((spot.location.x,spot.location.y+dy,-1))
 hit,loc,normal,index=obj.ray_cast(origin,Vector((0,0,1)))
 rows.append({'y':origin.y,'hit':hit,'surface_z':loc.z if hit else None,'gap_m':loc.z-spot.location.z if hit else None})
report={'entity':a.entity,'grip_m':list(spot.location),'bottom_surface':rows}
Path(a.output).write_text(json.dumps(report,indent=2));print(json.dumps(report))
