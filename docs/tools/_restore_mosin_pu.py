"""Restore the existing Mosin appearance and PU on the modular prototype.

Run with --build <Mosin build directory>. Existing Mosin resources are reused,
not overwritten. Attachment positions on the new short models require in-game QA.
"""
import argparse
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT, ASSETS, write

p=argparse.ArgumentParser();p.add_argument('--build',required=True,type=Path);a=p.parse_args()
slot='''        PlaceObj('WeaponComponentSlot', {
            'SlotType', "Scope",
            'CanBeEmpty', true,
            'AvailableComponents', { "JAZZ_Scope_PU" },
        }),
'''
marker='''        PlaceObj('WeaponComponentSlot', {
            'SlotType', "Barrel",
            'AvailableComponents', { "JAZZ_Mosin1891", "JAZZ_MosinM38", "JAZZ_MosinObrez" },'''
paths=[ROOT/'items.lua',ROOT/'InventoryItem/Mosin.lua',
       a.build/'mod-data-stage/weapon-item.lua',a.build/'mod-data-stage/JAZZ_MosinModular.lua']
for path in paths:
    s=path.read_text(encoding='utf-8-sig')
    assert s.count(marker)==1,path
    if slot+marker not in s:
        s=s.replace(marker,slot+marker,1)
        LuaRuntime().compile(s if path.name!='weapon-item.lua' else 'return '+s)
        write(path,s)

ent=ASSETS/'Entities'
legacy=ET.parse(ent/'Mosin.ent');legacy.getroot().set('name','MOSIN_1891')
for lod in legacy.findall('.//lod'):
    for src in list(lod.findall('src')):lod.remove(src)
mesh=legacy.find('.//mesh_description')
# Preserve the old rifle's placement and scope mount. Correct its historical
# letter-i typo so the engine can actually find the left-hand IK target.
for attach in mesh.findall('attach'):
    if attach.get('name')=='Hand_i_grip':attach.set('name','Hand_l_grip')
ET.SubElement(mesh,'attach',name='Barrel',spot_pos='0.000,0.000,0.000',spot_rot='0,0,1,0')
trees={'MOSIN_1891':legacy}
for name,grip,scope in [
    ('MOSIN_M38','30.000,0.000,4.000','9.721,-1.328,9.329'),
    ('MOSIN_Obrez','16.000,0.000,1.500','9.721,-1.328,7.329'),
]:
    tree=ET.parse(ent/(name+'.ent'));mesh=tree.find('.//mesh_description')
    for attach in mesh.findall('attach'):
        if attach.get('name')=='Hand_l_grip':attach.set('spot_pos',grip)
    scope_node=next((x for x in mesh.findall('attach') if x.get('name')=='Scope'),None)
    if scope_node is None:scope_node=ET.SubElement(mesh,'attach',name='Scope')
    scope_node.set('spot_pos',scope);scope_node.set('spot_rot','0,0,1,0')
    trees[name]=tree
backup=a.build/'pu-restoration-backup';backup.mkdir(exist_ok=True)
for name,tree in trees.items():
    path=ent/(name+'.ent')
    if not (backup/path.name).exists():shutil.copy2(path,backup/path.name)
    for dest in [path,a.build/'mod-assets-stage/Entities'/path.name]:
        tree.write(dest,encoding='utf-8',xml_declaration=True)
    for ref in tree.findall('.//mesh')+tree.findall('.//material'):
        assert (ent/ref.attrib['file']).is_file(),ref.attrib
    assert tree.find('.//attach[@name="Scope"]') is not None
shutil.copy2(ROOT/'WeaponIcons/Mosin.png',ROOT/'WeaponIcons/MOSIN_1891.png')
print('PASS: PU slot restored; long configuration reuses old Mosin mesh/material/icon; three Scope and hand spots present. Runtime fit pending.')
