"""Read local companions + ModItemWeaponComponents; output portable coverage JSON.

python docs/tools/weapon_layer_icons/audit.py --output <worktree>/.../arsenal.json
Requires lupa. Executes data constructors only, never loaded mod/game code.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[3]


def expression_end(text, start):
    """Balance a Lua call, respecting strings and long comments/strings."""
    depth, i = 0, start
    while i < len(text):
        if text.startswith('--', i):
            long = re.match(r'--\[(=*)\[', text[i:])
            i = (text.index(']' + long[1] + ']', i + len(long[0])) + len(long[1]) + 2
                 if long else text.find('\n', i))
            if i < 0:
                raise ValueError('Unclosed Lua call')
            continue
        long = re.match(r'\[(=*)\[', text[i:i + 32]) if text[i] == '[' else None
        if long:
            i = text.index(']' + long[1] + ']', i + len(long[0])) + len(long[1]) + 2
            continue
        if text[i] in '\"\'':
            quote = text[i]
            i += 1
            while i < len(text) and text[i] != quote:
                i += 2 if text[i] == '\\' else 1
        elif text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError('Unclosed Lua call')


def setup():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
      DefineClass={}
      function UndefineClass() end
      function T(id,text) return text end
      function PlaceObj(c,p)
        p=p or {}
        for i=1,#p,2 do if type(p[i])=='string' then p[p[i]]=p[i+1] end end
        return p
      end
      function point(...) return {...} end
      function RGB(...) return {...} end
      RGBA=RGB
      function set(...) local r={} for _,v in ipairs({...}) do r[v]=true end return r end
    ''')
    return lua


def array(value):
    return [value[i] for i in range(1, len(value) + 1)] if value is not None else []


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    lua = setup()
    text = (ROOT / 'items.lua').read_text(encoding='utf-8-sig')
    components = {}
    for match in re.finditer(r"PlaceObj\('ModItemWeaponComponent'", text):
        end = expression_end(text, text.index('(', match.start()))
        obj = lua.execute('return ' + text[match.start():end])
        components[obj.id] = obj
    rows, errors = [], []
    firearm_classes = {'Firearm', 'FirearmBase', 'Pistol', 'Revolver', 'SubmachineGun',
                       'AssaultRifle', 'Carbine', 'SniperRifle', 'Shotgun', 'MachineGun',
                       'HeavyWeapon', 'RocketLauncher', 'GrenadeLauncher', 'Autopistol',
                       'BattleRifle', 'LightMachineGun', 'FlareGun', 'Mortar'}
    for path in sorted((ROOT / 'InventoryItem').glob('*.lua')):
        source = path.read_text(encoding='utf-8-sig')
        if not re.search(r'__parents\s*=\s*\{\s*"(' + '|'.join(firearm_classes) + ')"', source):
            continue
        try:
            lua.execute(source)
            definition = lua.globals().DefineClass[path.stem]
            slots = []
            for slot in array(definition.ComponentSlots):
                options = []
                for cid in array(slot.AvailableComponents):
                    component = components.get(cid)
                    best = {}
                    if component:
                        for visual in array(component.Visuals):
                            target = visual.ApplyTo or ''
                            if target not in ('', path.stem):
                                continue
                            old = best.get(visual.Slot)
                            if old is None or (not old['specific'] and target):
                                best[visual.Slot] = {'entity': visual.Entity or '', 'specific': bool(target)}
                    options.append({'id': cid, 'component_found': component is not None,
                                    'visuals': best, 'art': 'not-rendered'})
                slots.append({'slot': slot.SlotType, 'default': slot.DefaultComponent or '',
                              'can_be_empty': slot.CanBeEmpty if slot.CanBeEmpty is not None else 'inherited',
                              'options': options})
            rows.append({'weapon': path.stem, 'host': definition.Entity or None,
                         'icon': definition.Icon, 'parent': array(definition.__parents),
                         'slots': slots, 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                         'art': 'not-rendered'})
        except Exception as exc:
            errors.append({'file': path.name, 'error': str(exc)})
    report = {'kind': 'offline-local-catalog-not-runtime', 'items_sha256': hashlib.sha256(
        (ROOT / 'items.lua').read_bytes()).hexdigest(), 'component_count': len(components),
        'weapon_count': len(rows), 'slot_option_count': sum(len(s['options']) for r in rows for s in r['slots']),
        'weapons': rows, 'errors': errors,
        'limitations': ['No inherited vanilla slots resolved', 'No legal-combination enumeration',
                        'No entity/spot geometry verification', 'Visual absence is not art completeness',
                        'Host overrides such as Mosin are separate profile rules',
                        'All art remains unreviewed; M4 demo is a separate historical source snapshot']}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: report[k] for k in ('weapon_count', 'component_count', 'slot_option_count', 'errors')}))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
