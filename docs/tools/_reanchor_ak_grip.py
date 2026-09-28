"""Shift an AK body so the pistol grip sits on the entity origin (right hand).

blender --background --factory-startup --python this.py --
  --blend <AK74M_JAZZ.blend> --entity AKR_AK74M
  --offset-game-cm 4.63,0,-1.11
  --out <AK74M_JAZZ.blend> --fbx <AK74M_JAZZ.fbx> --game-root <JA3_ROOT>

Only the body mesh and attach spots move. Magazine/stock/handguard/muzzle
meshes stay in their own entity frames so they snap back when attached to
the updated spots. Dry-run prints the planned shift; --write applies it.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from _ja3_mesh_prepare import prepare_export_mesh

p = argparse.ArgumentParser()
p.add_argument('--blend', type=Path, required=True)
p.add_argument('--entity', required=True)
p.add_argument('--offset-game-cm', required=True, help='dx,dy,dz in game centimetres, +X forward')
p.add_argument('--out', type=Path, required=True)
p.add_argument('--fbx', type=Path)
p.add_argument('--game-root', type=Path)
p.add_argument('--write', action='store_true')
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
dx, dy, dz = (float(v) for v in a.offset_game_cm.split(','))
# Game (+X forward, cm) -> Blender (-Y, -X, Z) metres.
offset = Vector((-dy / 100, -dx / 100, dz / 100))

bpy.ops.wm.open_mainfile(filepath=str(a.blend))
body = bpy.data.objects[a.entity]
spots = [o for o in bpy.data.objects if o.type == 'EMPTY' and o.parent == body]
# Module origins move so the assembled preview stays together. The body's own
# Origin empty stays at the entity origin — moving it would double the shift
# in world space and confuse overlay measurement.
origins = [o for o in bpy.data.objects
           if o.type == 'EMPTY' and o.name.startswith(a.entity + '_')
           and o.name.endswith('_Origin') and o.name != a.entity + '_Origin']

report = {
    'entity': a.entity,
    'offset_game_cm': [dx, dy, dz],
    'offset_blender_m': [round(v, 5) for v in offset],
    'spots': sorted(o.name for o in spots),
    'origins_moved': sorted(o.name for o in origins),
    'body_verts': len(body.data.vertices),
}

if not a.write:
    print('DRY=' + json.dumps(report))
    print('Re-run with --write to apply.')
    raise SystemExit(0)

body.data.transform(Matrix.Translation(offset))
for empty in spots:
    empty.location += offset
for empty in origins:
    empty.location += offset

a.out.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(a.out))
report['blend'] = str(a.out)

if a.fbx and a.game_root:
    spec = importlib.util.spec_from_file_location(
        'ak_grip_hge', a.game_root / 'ModTools/BlenderExport.py')
    hge = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hge)
    hge.SETTINGS.update(version='71', game='Zulu', appid='Jagged Alliance 3',
                        mtl_prop_0_visible=True, mtl_prop_0_name='Unit',
                        enable_colliders=True)
    hge.register()
    s = bpy.context.scene
    s.unit_settings.system = 'METRIC'
    s.unit_settings.scale_length = 1
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            prepare_export_mesh(obj)
    with hge.ObjectNamesExportContext(bpy.context):
        bpy.ops.export_scene.fbx(
            filepath=str(a.fbx), axis_forward='Y', axis_up='Z',
            apply_scale_options='FBX_SCALE_ALL', object_types={'MESH', 'EMPTY'},
            use_custom_props=True, add_leaf_bones=False, bake_anim=False)
    report['fbx'] = str(a.fbx)

print('REANCHOR=' + json.dumps(report))
