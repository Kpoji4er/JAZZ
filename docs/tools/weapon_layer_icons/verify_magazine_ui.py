"""Photograph installed soft outline and revised magazines in real XImage/inventory widgets."""
import argparse
import json
from pathlib import Path
from install_layers import lua
from live import evaluate, quote

p = argparse.ArgumentParser(__doc__)
p.add_argument('--library', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--group', choices=['ak103', 'family', 'remaining'], required=True)
a = p.parse_args()
groups = {
    'ak103': [('AK103', 'JAZZ_MagQuick_AK'), ('AK103', 'JAZZ_MagLarge_30_40'), ('AK103', 'JAZZ_MagDrum_30_75')],
    'family': [('AK47', 'JAZZ_MagQuick_AK'), ('Type56', 'JAZZ_MagQuick_AK'), ('ZastavaM92', 'JAZZ_MagQuick_AK')],
    'remaining': [('Zastava_M70', 'JAZZ_MagDrum_30_75'), ('DesertEagle', 'JAZZ_MagNormal'), ('HiPower', 'JAZZ_MagNormal')],
}
registry = json.loads((a.library / 'registry.json').read_text(encoding='utf-8'))
builds = []
for weapon, magazine in groups[a.group]:
    rows = json.loads((a.library / 'graphs' / (weapon + '.json')).read_text(encoding='utf-8'))['rows']
    profile = registry['weapons'][weapon]
    defaults = {s['slot']: s['default'] for s in profile['slots']}
    row = max((r for r in rows if r['components'].get('Magazine') == magazine),
              key=lambda r: sum(v != defaults.get(k) for k, v in r['components'].items()))
    builds.append(dict(weapon=weapon, label=weapon + ' / ' + magazine.removeprefix('JAZZ_Mag'),
                       order=[s['slot'] for s in profile['slots']], requested=row['requested'], expected=row['components']))
a.output.mkdir(parents=True, exist_ok=True)
settings = dict(output=a.output.resolve().as_posix(), builds=builds, effect='glow')
source = Path(__file__).with_name('probe_installed_ui.lua').read_text(encoding='utf-8')
body = 'local fn=assert(load(' + quote(source) + ',"installed magazine UI","t",_G))();return fn(' + lua(settings) + ')'
evaluate(body, a.output / 'dispatch.json', True)
