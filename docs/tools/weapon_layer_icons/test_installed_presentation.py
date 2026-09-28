"""Exercise the installed Lua selector against photographs and unsupported builds."""
import argparse, hashlib, json
from pathlib import Path
from lupa import LuaRuntime
from PIL import Image
from install_presentation import ROOT, STAGED, BEGIN, END, build
from content_scope import disabled_ids
from icon_layout import target_size

def run(active):
    lua=LuaRuntime(unpack_returned_tuples=True)
    text=(active/'Code/InventoryUI.lua').read_text(encoding='utf-8-sig')
    block=text[text.index(BEGIN):text.index(END)]
    lua.execute(block)
    resolve=lua.globals().JazzWeaponIcon_GetCaptured
    rows=json.loads((STAGED/'manifest.json').read_text(encoding='utf-8'))['rows']
    passed=0
    for row in rows:
        if row['status'] != 'captured' or not isinstance(row['entity'],str): continue
        item=lua.table_from({'class':row['weapon'],'Entity':row['entity'],
                             'components':lua.table_from(row['components'] or {})})
        path=resolve(item)
        if row['weapon'] in disabled_ids():
            assert path is None
            passed+=1
            continue
        assert path and (active/path.removeprefix('Mod/e6L4ECj/')).is_file(), row
        item.Entity='unphotographed-host'
        assert resolve(item) is None
        item.Entity=row['entity']
        item.components['UnknownSlot']='unphotographed-component'
        assert resolve(item) is None
        passed+=3
    for item in [None,lua.table_from({}),lua.table_from({'class':'AK74','Entity':'AK74'})]:
        assert resolve(item) is None
        passed+=1
    maintenance=(active/'Code/System_WeaponResourceMaintenance.lua').read_text(encoding='utf-8-sig')
    hook=maintenance[maintenance.index('local VanillaInventoryItemGetItemUIIcon ='):maintenance.index('end -- FirstLoad: InventoryItem rollover/icon hooks')]
    lua.execute('''InventoryItem = {GetItemUIIcon=function(self) return self.Icon end}
      function IsKindOf(item,kind) return item.class == kind end
      function JAZZ_RemovableAttachment_GetItemUIIcon(item) return "attachment-icon" end''')
    lua.execute(hook)
    for cls,expected in [('UnknownWeapon','original-icon'),('JAZZ_RemovableAttachment','attachment-icon')]:
        item=lua.table_from({'class':cls,'Icon':'original-icon'})
        assert lua.globals().InventoryItem.GetItemUIIcon(item)==expected
        passed+=1
    _,files,_=build()
    catalog={r['id']:r for r in json.loads((STAGED.parent/'catalog.json').read_text(encoding='utf-8'))['weapons']}
    for name,src in files.items():
        target=active/'WeaponIcons/Live'/name
        assert hashlib.sha256(src.read_bytes()).digest()==hashlib.sha256(target.read_bytes()).digest()
        with Image.open(target) as img:
            assert img.mode=='RGBA' and img.size==target_size(catalog[name.split('__',1)[0]])
            bounds=img.getchannel('A').point(lambda a:255 if a>16 else 0).getbbox()
            assert bounds and min(bounds[0],bounds[1],img.width-bounds[2],img.height-bounds[3])>=2
            assert max((bounds[2]-bounds[0])/img.width,(bounds[3]-bounds[1])/img.height)>=.85
    # Both changed files compile, and the existing hook still delegates attachment chips.
    compile_lua=lua.eval('function(s) local f,e=load(s); return f ~= nil,e end')
    for root in [ROOT,active]:
        for file in ['Code/InventoryUI.lua','Code/System_WeaponResourceMaintenance.lua']:
            source=(root/file).read_text(encoding='utf-8-sig')
            ok,error=compile_lua(source)
            assert ok,error
        assert 'JazzAttachChips_Apply(self.idItemImg, item)' in (root/'Code/InventoryUI.lua').read_text(encoding='utf-8')
    return {'status':'PASS','lua_cases':passed,'installed_icons':len(files),
            'compiled_files':4,'runtime':'not tested: game is closed, DAP unavailable',
            'excluded':'UnderslungGrenadeLauncher: no standalone entity',
            'deduplicated_configurations':2}

if __name__=='__main__':
    p=argparse.ArgumentParser(__doc__)
    p.add_argument('--active',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    result=run(args.active)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
