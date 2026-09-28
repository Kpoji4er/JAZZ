"""Fix duplicate AR15 furniture choices; --output DIR [--apply].
Stages items and both companions together; never changes shared components.
"""
import argparse, hashlib, shutil, subprocess
from pathlib import Path
from _integrate_m14_family import find_item_block, matching

p=argparse.ArgumentParser()
p.add_argument('--output',type=Path,required=True)
p.add_argument('--apply',action='store_true')
a=p.parse_args()
root=Path(__file__).resolve().parents[2]
a.output.mkdir(parents=True,exist_ok=True)
def lock(text,slot,component):
    at=text.index("'SlotType', \""+slot+'"')
    start=text.rfind("PlaceObj('WeaponComponentSlot'",0,at)
    end=matching(text,text.index('(',start))
    assert component in text[start:end]
    return text[:start]+f'''PlaceObj('WeaponComponentSlot', {{
            'SlotType', "{slot}",
            'Modifiable', false,
            'AvailableComponents', {{ "{component}" }},
            'DefaultComponent', "{component}",
        }})'''+text[end:]
def fix(text,wid):
    text=lock(text,'Handgrip','JAZZ_Handgrip_Default')
    if wid=='M16A4':text=lock(text,'Stock','JAZZ_StockNormal')
    return text
original={'items.lua':(root/'items.lua').read_bytes()}
items=original['items.lua'].decode('utf-8')
outputs={}
for wid in ('M16A4','M4A1'):
    start,end=find_item_block(items,wid)
    items=items[:start]+fix(items[start:end],wid)+items[end:]
    rel='InventoryItem/'+wid+'.lua'
    original[rel]=(root/rel).read_bytes()
    outputs[rel]=fix(original[rel].decode('utf-8'),wid)
outputs['items.lua']=items
for rel,text in outputs.items():
    path=a.output/rel;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text.replace('\r\n','\n'),encoding='utf-8',newline='\n')
if a.apply:
    check=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,Ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
    assert not check.stdout.strip(),'Game/editor must be closed'
    for rel,old in original.items():assert (root/rel).read_bytes()==old,rel
    for rel,old in original.items():
        backup=a.output/'backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True)
        assert not backup.exists(),str(backup)
        backup.write_bytes(old);shutil.copy2(a.output/rel,root/rel)
print('APPLIED' if a.apply else 'STAGED', 'M16A4 fixed stock; M4A1/M16A4 fixed pistol grip')
