"""Run real Lua selector, compose PNGs and build a self-contained interactive review.

python docs/tools/weapon_layer_icons/build_review.py --demo docs/design/weapon-layer-icons/demo
Requires Pillow and lupa. All output stays beside the given registry.
"""
import argparse
import base64
import copy
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat
from lupa import LuaRuntime

HERE = Path(__file__).resolve().parent


def lua_table(lua, value):
    if isinstance(value, dict):
        return lua.table_from({k: lua_table(lua, v) for k, v in value.items()})
    if isinstance(value, list):
        return lua.table_from([lua_table(lua, v) for v in value])
    return value


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('--demo', type=Path, required=True)
    args = p.parse_args()
    root = args.demo.resolve()
    registry = json.loads((root / 'registry.json').read_text())
    lua = LuaRuntime(unpack_returned_tuples=True)
    selector = lua.execute((HERE / 'selector.lua').read_text())
    data = lua_table(lua, registry)
    profile = registry['weapons']['M4A1']
    cases = {}
    results = []

    def resolve(changes=None, **extra):
        w = {'class': 'M4A1', 'components': changes or {}}
        w.update(extra)
        before = copy.deepcopy(w)
        weapon = lua_table(lua, w)
        result = selector.resolve(data, weapon)
        assert w == before
        # Also verify the actual Lua argument; Python copy alone would miss mutation.
        assert sorted(weapon.components.items()) == sorted(w['components'].items())
        assert weapon.Icon is None and weapon.Entity == w.get('Entity')
        return result

    def plan(changes=None):
        result = resolve(changes)
        assert not isinstance(result, tuple), result
        return {'host': result.host, 'key': result.key,
                'layers': [dict(result.layers[i].items()) for i in range(1, len(result.layers) + 1)]}

    def check(name, condition):
        assert condition, name
        results.append(name)

    default = plan()
    cases['Default'] = default
    cases['Short + RIS + collapsed'] = plan({
        'Barrel': 'JAZZ_BarrelShort', 'Handguard': 'JAZZ_Handguard_RIS',
        'Stock': 'JAZZ_StockLightFolded'})
    cases['Long (geometry study)'] = plan({'Barrel': 'JAZZ_BarrelLong'})
    cases['Muzzle removed'] = plan({'Muzzle': ''})
    cases['Iron sights'] = plan({'Scope': 'JAZZ_IronSight'})
    check('A-B-A identical key and plan', default == plan())
    check('Short selects parent-specific muzzle', 'muzzle_short' in [l['id'] for l in cases['Short + RIS + collapsed']['layers']])
    check('Real straight 20-round requires capture, no incorrect art', resolve({'Magazine': 'JAZZ_MagSmall30_20'}) == (None, 'missing-art:Magazine'))
    check('Explicit empty removes muzzle', not any(l['id'].startswith('muzzle') for l in cases['Muzzle removed']['layers']))
    check('False equals empty', plan({'Muzzle': False}) == cases['Muzzle removed'])
    check('Missing uses defaults', default == plan({s: v['default'] for s, v in profile['slots'].items()}))
    check('Dictionary order independent', plan({'Muzzle': '', 'Scope': 'JAZZ_IronSight'}) == plan({'Scope': 'JAZZ_IronSight', 'Muzzle': ''}))
    check('Unsupported component full fallback', resolve({'Scope': 'JAZZ_Scope_12x'}) == (None, 'unsupported-component:Scope'))
    check('Unsupported host full fallback', resolve(Entity='UNKNOWN') == (None, 'unsupported-host'))
    check('Unknown nonempty slot fallback', resolve({'NewSlot': 'x'}) == (None, 'unknown-slot:NewSlot'))
    check('Unknown weapon fallback', selector.resolve(data, lua_table(lua, {'class': 'AK47'})) == (None, 'unsupported-weapon'))
    broken = copy.deepcopy(registry)
    del broken['weapons']['M4A1']['hosts'][profile['host']]['layers']['body']
    check('Missing layer full fallback', selector.resolve(lua_table(lua, broken), lua_table(lua, {'class': 'M4A1'})) == (None, 'missing-fixed-art'))
    # Synthetic host change fixture verifies infrastructure without claiming Mosin art.
    host_registry = copy.deepcopy(registry)
    hp = host_registry['weapons']['M4A1']
    hp['hosts']['OTHER_HOST'] = copy.deepcopy(hp['hosts'][hp['host']])
    hp['host_rules'] = [{'when': {'Barrel': 'JAZZ_BarrelShort'}, 'host': 'OTHER_HOST'}]
    hdata = lua_table(lua, host_registry)
    switched = selector.resolve(hdata, lua_table(lua, {'class': 'M4A1', 'components': {'Barrel': 'JAZZ_BarrelShort'}}))
    restored = selector.resolve(hdata, lua_table(lua, {'class': 'M4A1'}))
    check('Host swap and return', switched.host == 'OTHER_HOST' and restored.key == default['key'])
    # Same paint plan but different host must have a different key.
    hp['host_rules'] = []
    check('Host is part of cache key', selector.resolve(lua_table(lua, host_registry), lua_table(lua, {'class': 'M4A1', 'Entity': 'OTHER_HOST'})).key != default['key'])
    # Mutate the same Lua item and bind the same pooled UI window repeatedly.
    lua.globals().test_selector = selector
    lua.globals().test_registry = data
    lua.globals().test_binder = lua.execute((HERE / 'binder.lua').read_text())
    lua.execute('''
      local alive, made, fallback_count, empty_count = 0, 0, 0, 0
      local resources, creation = true, true
      local ui = {
        available=function() return resources end,
        create_hidden=function(plan)
          if not creation then return nil end
          made=made+1; alive=alive+1; return {plan=plan}
        end,
        destroy=function(g) assert(not g.deleted);g.deleted=true;alive=alive-1 end,
        show=function(g) assert(not g.deleted and alive==1) end,
        fallback=function(item) fallback_count=fallback_count+1;assert(alive==0) end,
        empty=function() empty_count=empty_count+1;assert(alive==0) end,
      }
      local binder=test_binder.new(test_selector,test_registry,ui)
      local item={class='M4A1',components={}}
      local initial=test_selector.resolve(test_registry,item).key
      assert(binder.bind(item));assert(binder.bind(item));assert(made==1)
      item.components.Barrel='JAZZ_BarrelShort';assert(binder.bind(item));assert(alive==1)
      item.components.Barrel=nil;assert(binder.bind(item))
      assert(test_selector.resolve(test_registry,item).key==initial)
      item.components.Muzzle='';assert(binder.bind(item));item.components.Muzzle=nil
      assert(binder.bind(item));assert(test_selector.resolve(test_registry,item).key==initial)
      item.components.Scope='unrendered';assert(not binder.bind(item));assert(fallback_count==1)
      item.components.Scope=nil;assert(binder.bind(item))
      resources=false;assert(not binder.bind(item));assert(alive==0)
      resources=true;assert(binder.bind(item))
      creation=false;item.components.Muzzle='';assert(not binder.bind(item));assert(alive==0)
      creation=true;assert(binder.bind(item));assert(not binder.bind(nil));assert(empty_count==1)
      assert(binder.bind(item));binder.close();binder.close();assert(alive==0)
      assert(item.Icon==nil and item.Entity==nil and item.visual_obj==nil)
    ''')
    check('Same-instance reversal and UI subtree lifecycle', True)
    layers = profile['hosts'][profile['host']]['layers']
    for lid, layer in layers.items():
        with Image.open(root / layer['image']) as im:
            check('RGBA canvas ' + lid, im.mode == 'RGBA' and im.size == (648, 330))
            alpha = im.getchannel('A')
            check('Transparent and nonempty ' + lid, alpha.getextrema()[0] == 0 and alpha.getextrema()[1] > 0)
            check('No cropped layer ' + lid, alpha.crop((0, 0, 648, 1)).getbbox() is None and
                  alpha.crop((0, 329, 648, 330)).getbbox() is None and
                  alpha.crop((0, 0, 1, 330)).getbbox() is None and alpha.crop((647, 0, 648, 330)).getbbox() is None)

    def compose(case):
        im = Image.new('RGBA', (648, 330))
        for layer in case['layers']:
            im = Image.alpha_composite(im, Image.open(root / layer['image']).convert('RGBA'))
        return im

    def outlined(im):
        alpha = im.getchannel('A')
        ring = alpha.filter(ImageFilter.MaxFilter(9))
        back = Image.new('RGBA', im.size, (8, 7, 6, 0))
        back.putalpha(ring)
        return Image.alpha_composite(back, im)

    sheet = Image.new('RGB', (1000, 250 * len(cases)), '#252a32')
    draw = ImageDraw.Draw(sheet)
    for i, (name, case) in enumerate(cases.items()):
        im = compose(case)
        im.save(root / ('case-' + str(i) + '.png'))
        final = outlined(im).resize((324, 165), Image.Resampling.LANCZOS)
        final.save(root / ('icon-' + str(i) + '.png'))
        draw.text((22, i * 250 + 12), name, fill='#eeeeee')
        sheet.paste(im, (10, i * 250 - 15), im)
        sheet.paste(final, (660, i * 250 + 40), final)
    sheet.save(root / 'contact-sheet.png')
    reference = Image.open(root / 'reference.png').convert('RGBA')
    bg = Image.new('RGBA', reference.size, '#252a32')
    composite = compose(default)
    delta = ImageChops.difference(Image.alpha_composite(bg, composite).convert('RGB'),
                                 Image.alpha_composite(bg, reference).convert('RGB'))
    delta.point(lambda v: min(255, v * 4)).save(root / 'difference-x4.png')
    # Measure only the weapon region; whole-canvas average hides defects in small icons.
    bbox = ImageChops.lighter(reference.getchannel('A'), composite.getchannel('A')).getbbox()
    metrics = {'default_reference_rgb_mae_255': ImageStat.Stat(delta.crop(bbox)).mean,
               'bbox': bbox, 'meaning': 'Offline snapshot side-view only; shadows/occlusion not exact',
               'tests_passed': len(results), 'tests': results,
               'selector_sha256': hashlib.sha256((HERE / 'selector.lua').read_bytes()).hexdigest()}
    (root / 'verification.json').write_text(json.dumps(metrics, indent=2))
    (root / 'cases.json').write_text(json.dumps(cases, indent=2))
    images = {k: 'data:image/png;base64,' + base64.b64encode((root / v['image']).read_bytes()).decode()
              for k, v in layers.items()}
    # Embed each supported plan produced by Lua; JS only paints, never duplicates resolver logic.
    combinations = []
    import itertools
    names = list(profile['slots'])
    for ids in itertools.product(*(profile['slots'][s]['options'] for s in names)):
        changes = dict(zip(names, ids))
        result = resolve(changes)
        combinations.append({'components': changes, 'plan': None if isinstance(result, tuple) else plan(changes),
                             'reason': result[1] if isinstance(result, tuple) else None})
    fallback_path = HERE.parents[2] / 'WeaponIcons' / 'M4A1.png'
    fallback = 'data:image/png;base64,' + base64.b64encode(fallback_path.read_bytes()).decode()
    payload = json.dumps({'images': images, 'fallback': fallback, 'slots': profile['slots'], 'combinations': combinations})
    template = (HERE / 'review.html').read_text(encoding='utf-8')
    (root / 'review.html').write_text(template.replace('/*PAYLOAD*/', payload), encoding='utf-8')
    print(json.dumps({'tests_passed': len(results), 'interactive_plans': len(combinations), 'reference_mae': metrics['default_reference_rgb_mae_255']}))


if __name__ == '__main__':
    main()
