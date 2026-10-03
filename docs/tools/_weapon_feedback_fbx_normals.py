"""Blender -- --input FBX --output JSON: inspect actual exported normal elements."""
import sys,argparse,json
from pathlib import Path
import numpy as np
from io_scene_fbx import parse_fbx
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);root,version=parse_fbx.parse(a.input);out=[]
def walk(node):
 if node.id==b'Geometry':
  for layer in node.elems:
   if layer.id!=b'LayerElementNormal':continue
   for entry in layer.elems:
    if entry.id==b'Normals':
     values=np.asarray(entry.props[0]).reshape(-1,3);length=np.linalg.norm(values,axis=1)
     out.append({'geometry':str(node.props[1]),'count':len(values),'zero_indices':np.where(length<.01)[0].tolist(),'min_length':float(length.min())})
 for child in node.elems:walk(child)
walk(root);a.output.write_text(json.dumps(out,indent=2));print(json.dumps(out))
