"""Compare current/soft/soft+sharp on existing native graphs; never install assets."""
import argparse
import hashlib
import html
import json
import subprocess
from pathlib import Path
from types import ModuleType

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from lupa import LuaRuntime
from icon_layout import fit, fit_body
from hybrid_style import hybrid


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--library', type=Path, required=True)
    parser.add_argument('--graphs', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    registry = json.loads((args.library / 'registry.json').read_text(encoding='utf-8'))
    lua = LuaRuntime(unpack_returned_tuples=True)

    def table(value):
        if isinstance(value, dict):
            return lua.table_from({k: table(v) for k, v in value.items()})
        if isinstance(value, list):
            return lua.table_from([table(v) for v in value])
        return value

    selector = lua.execute(Path(__file__).with_name('layer_selector.lua').read_text(encoding='utf-8'))
    data = table(registry)
    # Verify the shared layout refactor against the pre-change implementation.
    repo = Path(__file__).resolve().parents[3]
    old = ModuleType('prior_layout')
    old.__file__ = str(Path(__file__).with_name('icon_layout.py'))
    old_source = subprocess.check_output(['git', '-C', str(repo), 'show',
        'HEAD:docs/tools/weapon_layer_icons/icon_layout.py']).decode('utf-8')
    exec(compile(old_source, old.__file__, 'exec'), old.__dict__)
    requests = [('AK103', '30', None), ('AK103', '40', 'JAZZ_MagLarge_30_40'),
                ('AK103', 'drum', 'JAZZ_MagDrum_30_75'), ('AK103', 'combined', 'combined'),
                ('AK74', 'combined', 'combined'), ('DesertEagle', 'default', None),
                ('HiPower', 'default', None)]
    sheet = Image.new('RGB', (1020, 225 * len(requests)), '#292d32')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
    source_hashes, records, sections = {}, [], []
    for index, (weapon, label, variant) in enumerate(requests):
        profile = registry['weapons'][weapon]
        base = {s['slot']: s['default'] for s in profile['slots']}
        rows = json.loads((args.graphs / (weapon + '.json')).read_text(encoding='utf-8'))['rows']
        changes = lambda r: sum(v != base.get(k) for k, v in (r['components'] or {}).items())
        if variant == 'combined':
            candidates = sorted(rows, key=changes, reverse=True)
        elif variant:
            candidates = sorted((r for r in rows if r['components'].get('Magazine') == variant), key=changes)
        else:
            candidates = [{'entity': profile['base']['__host'], 'components': base}]
        plan = None
        for row in candidates:
            result = selector.resolve(data, table({'class': weapon, 'Entity': row['entity'],
                                                   'components': row['components']}))
            plan = result[0] if isinstance(result, tuple) else result
            if plan:
                break
        assert plan, (weapon, label)
        canvas = Image.new('RGBA', (1296, 660))
        for _, layer in plan.layers.items():
            path = args.library / 'layers' / (layer.id + '.png')
            source_hashes[path] = hashlib.sha256(path.read_bytes()).hexdigest()
            with Image.open(path) as image:
                canvas.alpha_composite(image.convert('RGBA'))
        size = (profile['width'], profile['height'])
        body = np.asarray(fit_body(canvas, size))
        current = fit(canvas, size)
        assert current.tobytes() == old.fit(canvas, size).tobytes(), 'Existing style changed'
        soft = hybrid(canvas, size)
        sharp = hybrid(canvas, size, sharpen=True)
        mask = body[..., 3] == 255
        assert np.array_equal(np.asarray(soft)[mask], body[mask]), 'Soft style altered opaque body'
        cards = []
        for column, (style, title, icon) in enumerate([
            ('current', 'Текущая обработка', current), ('soft', 'Мягкий контур', soft),
            ('sharp', 'Контур + резкость', sharp)]):
            assert icon.size == size
            alpha = np.asarray(icon)[..., 3]
            assert not any((alpha[0].any(), alpha[-1].any(), alpha[:, 0].any(), alpha[:, -1].any()))
            filename = f'{weapon}-{label}-{style}.png'
            icon.save(args.output / filename)
            x, y = column * 340, index * 225
            sheet.paste(icon, (x + (340 - icon.width) // 2, y + 42), icon)
            draw.text((x + 8, y + 8), f'{weapon} {label}', fill='white', font=font)
            draw.text((x + 8, y + 25), title, fill='#bdc5cf', font=font)
            cards.append(f'<figure><figcaption>{title}</figcaption><img src="{filename}"></figure>')
        records.append({'weapon': weapon, 'variant': label, 'components': row['components'],
                        'size': size, 'native_layers': len(plan.layers), 'checks': 'PASS'})
        sections.append(f'<section><h2>{html.escape(weapon + " · " + label)}</h2><div class="row">'
                        + ''.join(cards) + '</div></section>')
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == sha for p, sha in source_hashes.items())
    sheet.save(args.output / 'comparison.png')
    report = {'status': 'PASS', 'installed': False, 'runtime_glow_verified': False,
              'source_files_unchanged': len(source_hashes), 'current_style_byte_identical': True,
              'soft_opaque_color_unchanged': True, 'sizes_and_empty_edges': True,
              'recipe': {'sigma_at_height_110': 3.2, 'spread': 1, 'opacity': .9,
                         'rgb': [3, 3, 3], 'unsharp_percent': 45}, 'builds': records}
    (args.output / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (args.output / 'review.html').write_text('''<!doctype html><html lang="ru"><meta charset="utf-8">
<meta name="viewport" content="width=device-width"><title>JAZZ · Мягкий контур</title>
<style>body{background:#191c20;color:#e8ebef;font:16px system-ui;max-width:1080px;margin:32px auto;padding:0 16px}
.row{display:flex;flex-wrap:wrap;gap:12px}figure{margin:0;width:340px;background:#292d32;height:205px;display:flex;flex-direction:column;align-items:center;justify-content:center}figcaption{color:#bdc5cf;margin:8px}img{max-width:100%}h2{font-size:19px}p{line-height:1.5}</style>
<h1>Наши снимки + мягкий контур</h1><p>Слева — текущая обработка offline preview; в центре — мягкий контур;
справа — тот же контур и лёгкая резкость. Цветовые профили, тело оружия и масштаб сохранены.
Контур построен после сборки всех модулей. В игру этот прототип не установлен: текущий runtime outline
может отличаться от левого offline-примера.</p>''' + ''.join(sections) + '</html>', encoding='utf-8')
    print(json.dumps({'status': 'PASS', 'builds': len(records), 'unchanged_sources': len(source_hashes),
                      'output': str(args.output)}))


if __name__ == '__main__':
    main()
