"""Exercise structural names against current repository component slots, offline.

python docs/tools/weapon_layer_icons/test_names.py
Writes names-verification.json beside the prototype catalog. Requires lupa.
"""
import copy
import json
from pathlib import Path
from lupa import LuaRuntime
from audit import setup, array
from build_review import lua_table

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'docs/design/weapon-layer-icons'
lua = setup()
resolver = lua.execute((Path(__file__).parent / 'names.lua').read_text())
catalog = json.loads((OUT / 'names.json').read_text(encoding='utf-8'))
data = lua_table(lua, catalog)
checks = []


def check(name, ok):
    assert ok, name
    checks.append(name)


def resolve(stock=None, language='ru', cls='AK74', **extra):
    item = {'class': cls, 'DisplayName': 'Original', 'DisplayNamePlural': 'Original plural',
            'components': {} if stock is None else {'Stock': stock}}
    item.update(extra)
    arg = lua_table(lua, item)
    result = resolver.resolve(data, arg, language, False)
    check('Item unchanged: ' + str((cls, stock, language, extra)),
          arg.DisplayName == 'Original' and arg.DisplayNamePlural == 'Original plural' and
          sorted(arg.components.items()) == sorted(item['components'].items()))
    return result


check('Default AK74', resolve() == ('АК-74', 'ak74-fixed-stock'))
check('Unfolded is AKS74', resolve('JAZZ_StockLightUnFolded')[0] == 'АКС-74')
check('Folded keeps AKS74', resolve('JAZZ_StockLightFolded')[0] == 'АКС-74')
check('Restored fixed stock', resolve('JAZZ_StockNormal')[0] == 'АК-74')
check('English', resolve('JAZZ_StockLightFolded', 'en')[0] == 'AKS-74')
check('Unsupported language preserves original', resolve('JAZZ_StockLightFolded', 'fr') == ('Original', 'untranslated'))
check('Explicit empty not default', resolve('')[0] == 'Original')
check('False not default', resolve(False)[0] == 'Original')
check('Unknown stock', resolve('OTHER')[0] == 'Original')
check('Unknown host', resolve('JAZZ_StockLightFolded', Entity='OTHER')[0] == 'Original')
check('AK74M does not become AKS74', resolve('JAZZ_StockLightFolded', cls='AK74M')[0] == 'Original')
check('AKM fixed', resolve('JAZZ_StockNormal', cls='AKM')[0] == 'АКМ')
check('AKMS extended', resolve('JAZZ_StockLightUnFolded', cls='AKM')[0] == 'АКМС')
check('AKMS folded', resolve('JAZZ_StockLightFolded', cls='AKM')[0] == 'АКМС')
check('AKM unrelated stock', resolve('JAZZ_StockHeavy', cls='AKM')[0] == 'Original')
check('vz58 fixed P', resolve('JAZZ_StockNormal', cls='VZ58')[0] == 'vz. 58 P')
check('vz58 extended V', resolve('JAZZ_StockLightUnFolded', cls='VZ58')[0] == 'vz. 58 V')
check('vz58 folded V', resolve('JAZZ_StockLightFolded', cls='VZ58')[0] == 'vz. 58 V')
check('vz58 modern is not historical V', resolve('JAZZ_StockHeavy', cls='VZ58')[0] == 'Original')
check('Named unique SVD preserved', resolve('JAZZ_StockLight', cls='DragunovSVD_Custom')[0] == 'Original')
check('SVD candidate rejected by live stock evidence', resolve('JAZZ_StockLight', cls='DragunovSVD')[0] == 'Original')
item = lua_table(lua, {'class': 'AK74', 'DisplayName': 'Original', 'components': {}})
for stock in ('JAZZ_StockNormal', 'JAZZ_StockLightUnFolded', 'JAZZ_StockLightFolded', 'JAZZ_StockNormal'):
    item.components.Stock = stock
    check('Same-instance transition ' + stock, resolver.resolve(data, item, 'ru', False)[0] ==
          ('АК-74' if stock == 'JAZZ_StockNormal' else 'АКС-74'))
check('No stored name mutation', item.DisplayName == 'Original')
check('Plural', resolver.resolve(data, item, 'en', True)[0] == 'AK-74s')
ambiguous = copy.deepcopy(catalog)
ambiguous['weapons']['AK74']['rules'].append(copy.deepcopy(ambiguous['weapons']['AK74']['rules'][0]))
check('Ambiguous matches preserve original', resolver.resolve(lua_table(lua, ambiguous), item, 'ru', False) == ('Original', 'ambiguous-rules'))

# Current files, not the earlier snapshot catalog, establish actual slot IDs.
for cls in ('AK74', 'AKM', 'VZ58', 'DragunovSVD'):
    lua.execute((ROOT / 'InventoryItem' / (cls + '.lua')).read_text(encoding='utf-8-sig'))
    definition = lua.globals().DefineClass[cls]
    stock = next(s for s in array(definition.ComponentSlots) if s.SlotType == 'Stock')
    known = set(array(stock.AvailableComponents))
    check('Current host ' + cls, definition.Entity == catalog['weapons'][cls]['host'])
    for rule in catalog['weapons'][cls]['rules']:
        check('Current component IDs ' + rule['id'], set(rule['when']['Stock']) <= known)
    if cls == 'AK74':
        for slot in array(definition.ComponentSlots):
            if slot.SlotType == 'Stock': continue
            for cid in array(slot.AvailableComponents):
                item.components[slot.SlotType] = cid
                check('Nonstructural slot ignored ' + slot.SlotType + '/' + cid,
                      resolver.resolve(data, item, 'ru', False)[0] == 'АК-74')
                item.components[slot.SlotType] = None

(OUT / 'names-verification.json').write_text(json.dumps({'passed': len(checks), 'checks': checks,
    'level': 'offline Lua and current companion data; no game UI or localization registration'},
    ensure_ascii=False, indent=2), encoding='utf-8')
print('PASS:', len(checks), 'structural-name checks')
