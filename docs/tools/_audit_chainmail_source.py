"""Blender inspect Chainmail atlas ranges and retained skin before export."""
import bpy,json
obj=next(o for o in bpy.data.objects if o.name.startswith('TEST_Chainmail'))
out={'layers':[(x.name,x.active_render) for x in obj.data.uv_layers],'active':obj.data.uv_layers.active.name,'materials':[]}
for i,mat in enumerate(obj.data.materials):
    faces=[f for f in obj.data.polygons if f.material_index==i];loops=[j for f in faces for j in f.loop_indices]
    row={'name':mat.name,'faces':len(faces),'skin':mat.get('jazz_skin_colorization'),'uv':{}}
    for uv in obj.data.uv_layers:
        row['uv'][uv.name]=[[min(uv.data[j].uv[k] for j in loops),max(uv.data[j].uv[k] for j in loops)] for k in (0,1)]
    out['materials'].append(row)
print('ATLAS_AUDIT='+json.dumps(out))
