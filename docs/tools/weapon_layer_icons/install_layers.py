"""Install a checked native layer library into a selected core checkout.

Only the marked local block and existing binder call sites are changed. Other
InventoryUI changes survive; no additional global or method wrapper is added.
"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

HERE=Path(__file__).parent
BEGIN='-- BEGIN JAZZ NATIVE WEAPON LAYERS\n'
END='-- END JAZZ NATIVE WEAPON LAYERS\n'

def lua(value):
    if value is None:return 'nil'
    if isinstance(value,bool):return str(value).lower()
    if isinstance(value,(int,float)):return str(value)
    if isinstance(value,str):return json.dumps(value,ensure_ascii=False)
    if isinstance(value,list):return '{'+','.join(map(lua,value))+'}'
    return '{'+','.join('['+lua(k)+']='+lua(v) for k,v in sorted(value.items()))+'}'

def build_block(registry):
    # Capture signatures are audit evidence, unnecessary in the loaded UI table.
    registry=json.loads(json.dumps(registry))
    for layer in registry['layers'].values():layer.pop('signature',None)
    return (BEGIN+'local JazzNativeWeaponRegistry='+lua(registry)+'\n'
        +'local JazzNativeWeaponSelector=(function()\n'+(HERE/'layer_selector.lua').read_text(encoding='utf-8-sig')+'\nend)()\n'
        +'local JazzNativeWeaponBinder=(function()\n'+(HERE/'layer_binder.lua').read_text(encoding='utf-8-sig')+'\nend)()\n'+END)

def patch_ui(source,block):
    if BEGIN in source:
        start=source.index(BEGIN);end=source.index(END,start)+len(END)
        source=source[:start]+block+source[end:]
    else:
        anchor='function JazzWeaponIcon_BindItemImage(img, item)'
        assert source.count(anchor)==1,'Expected existing single binder'
        source=source.replace(anchor,block+'\n'+anchor,1)
    start=source.index('function JazzWeaponIcon_BindItemImage(img, item)')
    end=source.index('\nfunction JazzWeaponIcon_RefreshWeaponDisplays()',start)
    source=source[:start]+'''function JazzWeaponIcon_BindItemImage(img, item)
    if not img or img.window_state=="destroying" then return false end
    if not item then JazzNativeWeaponBinder.clear(img);return false end
    local icon = JazzWeaponIcon_GetCaptured(item) or (item.GetItemUIIcon and item:GetItemUIIcon()) or item.Icon
    if icon then img:SetImage(icon) end
    return JazzNativeWeaponBinder.bind(img, item, JazzNativeWeaponRegistry, JazzNativeWeaponSelector)
end
'''+source[end:]
    anchor='function JazzWeaponIcon_SuppressModBadge(img, item, _baked)\n'
    call='\tJazzWeaponIcon_BindItemImage(img, item)\n'
    assert source.count(anchor)==1
    if anchor+call not in source:source=source.replace(anchor,anchor+call,1)
    old='JazzWeaponIcon_OldOnContextUpdate(self, item, ...)\n\tif not item then\n\t\treturn'
    new='JazzWeaponIcon_OldOnContextUpdate(self, item, ...)\n\tif not item then\n\t\tJazzWeaponIcon_BindItemImage(self.idItemImg, nil)\n\t\treturn'
    source=source.replace(old,new,1)
    return source

def main():
    p=argparse.ArgumentParser(__doc__)
    p.add_argument('--library',type=Path,required=True)
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--backup',type=Path,required=True)
    a=p.parse_args()
    registry=json.loads((a.library/'registry.json').read_text(encoding='utf-8'))
    report=json.loads((a.library/'tests.json').read_text(encoding='utf-8'))
    assert report['status']=='PASS','Selector tests must pass before installation'
    assert report['registry_sha256']==hashlib.sha256((a.library/'registry.json').read_bytes()).hexdigest(),'Registry changed after tests'
    assert report['selector_sha256']==hashlib.sha256((HERE/'layer_selector.lua').read_bytes()).hexdigest(),'Selector changed after tests'
    ui=a.repo/'Code/InventoryUI.lua'
    original=ui.read_text(encoding='utf-8-sig')
    updated=patch_ui(original,build_block(registry))
    a.backup.parent.mkdir(parents=True,exist_ok=True)
    if not a.backup.exists():shutil.copy2(ui,a.backup)
    destination=a.repo/'WeaponIcons/Live/Layers';destination.mkdir(parents=True,exist_ok=True)
    for ident,layer in registry['layers'].items():
        if layer['image']:shutil.copy2(a.library/'layers'/(ident+'.png'),destination/(ident+'.png'))
    ui.write_text(updated,encoding='utf-8',newline='\n')
    print(json.dumps({'weapons':len(registry['weapons']),'layers':len(registry['layers']),'ui':str(ui)}))

if __name__=='__main__':main()
