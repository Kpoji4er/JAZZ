"""Offline 6B3 vest pass: clean model, rig, pose QA, bake, compile, stage.

python docs/tools/_qa_6b3_vest.py --blender <exe> --game-root <JA3_ROOT>
  --shirt <NPCCostumeMale_Shirt_08 JSON> --output <new folder>

Does not write active mods. Stops on the first failed stage.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

p = argparse.ArgumentParser()
for name in ('blender', 'game-root', 'shirt', 'output'):
    p.add_argument('--' + name, type=Path, required=True)
p.add_argument('--skip-model', action='store_true')
p.add_argument('--reference', type=Path, help='Cuirass v7 blend for exact skeleton rest validation')
p.add_argument('--native-only', action='store_true', help='Smooth real shirt skin field throughout')
p.add_argument('--surface-skin', action='store_true', help='Transfer shirt surface weights with bounded seam smoothing')
p.add_argument('--texture-size', type=int, choices=(1024, 2048), default=1024)
p.add_argument('--start-at', choices=('model', 'rig', 'pose-check', 'bake-export'),
               default='model')
a = p.parse_args()
if a.skip_model and a.start_at == 'model':
    a.start_at = 'rig'
order = ('model', 'rig', 'pose-check', 'bake-export', 'processor', 'stage')


def after(step):
    return order.index(a.start_at) <= order.index(step)
root = Path(__file__).resolve().parent
out = a.output.resolve()
out.mkdir(parents=True, exist_ok=True)
sample = a.game_root / 'ModTools/Samples/Assets/SampleMaleModel/BlenderScene_Appearance.blend'
entity = 'JAZZ_6B3_Male'
source = out / 'source'
build = out / 'build'
report = {'status': 'RUNNING', 'runtime': 'NOT_RUN', 'item': 'JazzArmor_6B3', 'entity': entity}


def run(label, args, folder=out):
    print('START', label, flush=True)
    with (folder / (label + '.log')).open('w', encoding='utf-8') as log:
        result = subprocess.run([str(x) for x in args], stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(label + ' failed; see ' + str(folder / (label + '.log')))
    print('PASS', label, flush=True)


base = [a.blender, '-b', '--factory-startup', '--threads', '4', '--python-exit-code', '1',
        '--python']
try:
    if after('model'):
        run('model', base + [root / '_model_6b3_vest.py', '--', '--sample', sample,
                             '--shirt', a.shirt, '--output', out, '--quick'])
    clean = out / 'clean' / 'JazzArmor_6B3.blend'
    assert clean.is_file(), clean
    if after('rig'):
        run('rig', base + [root / '_rig_6b3_vest.py', '--', '--sample', sample,
                           '--clean', clean, '--output', source, '--shirt', a.shirt]
            + (['--reference', a.reference] if a.reference else [])
            + (['--native-only'] if a.native_only else [])
            + (['--surface-skin'] if a.surface_skin else []))
    rigged = source / '6B3.blend'
    assert rigged.is_file(), rigged
    if after('pose-check'):
        run('pose-check', base + [root / '_check_soft_armor_poses.py', '--',
                                  '--source', rigged, '--output', out / 'poses'])
    if after('bake-export'):
        run('bake-export', base + [root / '_build_legion_armor.py', '--',
                                   '--source', rigged, '--output', build,
                                   '--game-root', a.game_root, '--entity', entity,
                                   '--mesh-prefix', 'TEST_6B3', '--icon', '6b3',
                                   '--texture-size', a.texture_size])
    run('processor', [a.game_root / 'ModTools/AssetsProcessor/AssetsProcessor.exe',
                      build / (entity + '.fbx'), '-globalappdirs', '-gamepath', a.game_root])
    candidates = [out / 'ExportedEntities', out.parent / 'ExportedEntities',
                  source / 'ExportedEntities']
    export = next((v for v in candidates if (v / (entity + '.ent')).exists()), None)
    if export is None:
        raise RuntimeError('Missing fresh compiled entity ' + entity)
    run('stage', [sys.executable, root / '_prepare_rifle_assets.py',
                  '--build', build, '--prefix', 'JAZZ_6B3', '--entities', entity,
                  '--export-root', export, '--game-root', a.game_root])
    report.update({'status': 'STAGED', 'clean': str(clean), 'rigged': str(rigged),
                   'build': str(build), 'export': str(export)})
except Exception as exc:
    report['status'] = 'FAILED'
    report['error'] = str(exc)
    raise
finally:
    (out / 'qa-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
