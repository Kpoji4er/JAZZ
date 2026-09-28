import bpy,os
from pathlib import Path
r=Path(os.environ['USERPROFILE'])/'.codex/artifacts/armor-prototype'
for f in [r/'heavy-repair-20260922/ZylonLight/JAZZ_ZylonLight_Male.blend',r/'rebuilt-20260926-v19/chainmail/chainmail.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(f))
 print('SOURCE',f)
 for o in bpy.data.objects:
  if o.type=='MESH':
   print('MESH',o.name,len(o.data.vertices),'UV',list(o.data.uv_layers.keys()))
   for m in o.data.materials:
    print('MATERIAL',m.name,[(n.name,n.type,n.image.filepath if n.type=='TEX_IMAGE' and n.image else '') for n in m.node_tree.nodes])
