"""Build exact photographed configurations; prepare scoped runtime patches and backups.

Uses --active for the installed checkout; never copies whole worktree files over it.
"""
import argparse, hashlib, json, shutil
from pathlib import Path
from content_scope import disabled_ids

ROOT = Path(__file__).resolve().parents[3]
STAGED = ROOT / 'docs/design/weapon-layer-icons/live/staged'
BEGIN = '-- BEGIN JAZZ-WEAPON-PRESENTATION-001'
END = '-- END JAZZ-WEAPON-PRESENTATION-001'

def q(s):
    return json.dumps(s, ensure_ascii=False)

def build():
    rows = json.loads((STAGED/'manifest.json').read_text(encoding='utf-8'))['rows']
    registry = {}
    files = {}
    disabled = disabled_ids()
    for row in sorted(rows, key=lambda r: (r['label'] != 'default', r['weapon'], r['label'])):
        if row['weapon'] in disabled or row['status'] != 'captured' or not isinstance(row['entity'], str):
            continue
        components = row['components'] or {}
        key = row['weapon']+'|'+row['entity']+'|'+';'.join(k+'='+str(v or '') for k,v in sorted(components.items()) if v)
        if key in registry:
            continue
        name = Path(row['icon']).name
        registry[key] = 'Mod/e6L4ECj/WeaponIcons/Live/'+name
        files[name] = STAGED/row['icon']
    lua = BEGIN+'\nlocal JazzLiveWeaponIcons = {\n'
    lua += '\n'.join('  ['+q(k)+'] = '+q(v)+',' for k,v in sorted(registry.items()))
    lua += '''
}

-- Missing or extra nonempty components deliberately fail exact matching.
function JazzWeaponIcon_GetCaptured(item)
  if not item or not item.components or not item.class or not item.Entity then return nil end
  local parts = {}
  for slot, component in pairs(item.components) do
    if component and component ~= "" then
      parts[#parts + 1] = slot .. "=" .. component
    end
  end
  table.sort(parts)
  return JazzLiveWeaponIcons[item.class .. "|" .. item.Entity .. "|" .. table.concat(parts, ";")]
end
'''+END+'\n'
    return lua,files,registry

def patch(text, old, new):
    if new in text: return text
    if text.count(old) != 1: raise RuntimeError('Patch anchor missing or ambiguous: '+old[:90])
    return text.replace(old,new,1)

def run(active, backup):
    lua, files, registry = build()
    results=[]
    for target in [ROOT, active]:
        for relative in ['Code/InventoryUI.lua','Code/System_WeaponResourceMaintenance.lua']:
            p=target/relative
            text=p.read_text(encoding='utf-8-sig')
            original=text
            if relative.endswith('InventoryUI.lua'):
                if BEGIN in text:
                    text=text[text.index(END)+len(END):].lstrip('\n')
                text=lua+text
                text=patch(text, 'local icon = (item.GetItemUIIcon and item:GetItemUIIcon()) or item.Icon',
                    'local icon = JazzWeaponIcon_GetCaptured(item) or (item.GetItemUIIcon and item:GetItemUIIcon()) or item.Icon')
            else:
                text=patch(text, '\treturn VanillaInventoryItemGetItemUIIcon(self)',
                    '\tlocal captured = JazzWeaponIcon_GetCaptured and JazzWeaponIcon_GetCaptured(self)\n\treturn captured or VanillaInventoryItemGetItemUIIcon(self)')
            if text != original:
                saved=backup/('active' if target==active else 'worktree')/relative
                saved.parent.mkdir(parents=True,exist_ok=True)
                if not saved.exists(): shutil.copy2(p,saved)
                p.write_text(text,encoding='utf-8',newline='\n')
                results.append(str(p))
        dest=target/'WeaponIcons/Live'
        dest.mkdir(parents=True,exist_ok=True)
        # Preserve excluded photos in the staged archive, remove only our known installed copies.
        for out in dest.glob('*.png'):
            if out.name.split('__',1)[0] in disabled_ids():
                source=STAGED/'icons'/out.name
                if source.is_file() and source.read_bytes()==out.read_bytes():
                    out.unlink()
        for name, source in files.items():
            out=dest/name
            if out.exists() and out.read_bytes()!=source.read_bytes():
                saved=backup/('active' if target==active else 'worktree')/'WeaponIcons/Live'/name
                saved.parent.mkdir(parents=True,exist_ok=True)
                if not saved.exists(): shutil.copy2(out,saved)
            shutil.copy2(source,out)
    report={'icons':len(files),'configurations':len(registry),'patched':results,'backup':str(backup)}
    backup.mkdir(parents=True,exist_ok=True)
    (backup/'install.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__)
    p.add_argument('--active',type=Path,required=True)
    p.add_argument('--backup',type=Path,required=True)
    args=p.parse_args()
    run(args.active.resolve(),args.backup.resolve())

