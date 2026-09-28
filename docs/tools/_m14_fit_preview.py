"""Offline M14 component fit preview from installed HGM and proposed entity spots.
Blender --python this.py -- --assets DIR --vanilla DIR --output DIR [--revised]
Read-only for assets; saves a review blend for the culling renderer.
"""
import argparse, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _decode_vz58_hgm import decode

p = argparse.ArgumentParser()
for key in ('assets', 'vanilla', 'output'):
    p.add_argument('--' + key, type=Path, required=True)
p.add_argument('--revised', action='store_true')
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.output.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)

def mesh(name, path, offset=(0, 0, 0), roll=0, color=(.2, .2, .2, 1)):
    # Vanilla v12 has an existing decoded reference; its quantization center is
    # the entity bbox, including multi-material optics (not each submesh bbox).
    data = (json.loads((a.vanilla/'Geometry'/(path.stem+'.json')).read_text())
            if path.parent == a.vanilla/'Meshes' else decode(path))
    center = Vector(tuple((data['bbox'][i] + data['bbox'][i+3])/2 for i in range(3)))
    rotation = Matrix.Rotation(math.radians(roll), 3, 'X')
    vertices, faces = [], []
    for part in data['meshes']:
        first = len(vertices)
        for v in part['vertices']:
            v = rotation @ (Vector(v) + center) + Vector(offset)
            vertices.append((-v.y, -v.x, v.z))
        faces += [tuple(first+i for i in reversed(f)) for f in part['faces']]
    me = bpy.data.meshes.new(name); me.from_pydata(vertices, [], faces)
    obj = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(obj)
    mat = bpy.data.materials.new(name); mat.diffuse_color = color
    me.materials.append(mat)
    return obj

assets = a.assets / 'Entities/Meshes'
vanilla = a.vanilla / 'Meshes'
mesh('M14', assets/'JAZZ_M14_Mesh.m.hgm', color=(.3, .15, .06, 1))
mesh('barrel', assets/'JAZZ_M14_BarrelNormal_Mesh.m.hgm', (.5, 0, 0))
mesh('magazine', assets/'JAZZ_M14_MagazineNormal_Mesh.m.hgm', (.17, 0, .075))
mesh('scope', vanilla/'WeaponAttA_ScopeCOG_mesh.hgm', (.185 if a.revised else .13, 0, .143))
mesh('bipod', vanilla/'WeaponAttA_BipodM24_mesh.hgm', (.56, 0, .071) if a.revised else (.46, 0, .027))
mesh('light', vanilla/'WeaponAttA_SideLight_mesh.hgm', (.61, -.009, .095) if a.revised else (.32, -.026, .065), 90 if a.revised else 0)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'fit.blend'))
