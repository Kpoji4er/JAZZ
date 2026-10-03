"""Check donor feed-box alignment and real AK103 UpdateVisualObj idempotence.
--reference extracted-vanilla-reference --output report.json
Offline evidence only: upper 20 mm bounding box is a fit proxy, not visual QA.
"""
import argparse
import json
from pathlib import Path
import re
import sys
import numpy as np
from lupa import LuaRuntime

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'docs/tools'))
from _decode_vz58_hgm import decode


def top_box(data):
    rows=[]
    for mesh in data['meshes']:
        b=np.array(mesh.get('bbox') or data['bbox'])
        rows.extend(np.array(mesh['vertices'])+(b[:3]+b[3:])/2)
    vertices=np.array(rows)*1000
    top=vertices[vertices[:,2]>vertices[:,2].max()-20]
    lo,hi=top.min(0),top.max(0)
    return np.array([(lo[0]+hi[0])/2,(lo[1]+hi[1])/2,hi[2]])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--reference',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();meshes=ROOT.parent/'jazz_assets/Entities/Meshes'
    target=top_box(decode(meshes/'AKR_AK103_Magazine_Mesh.m.hgm'))
    configs=[('JAZZ_MagNormal','AKMWaffleMag',(6,-9,-9)),
             ('JAZZ_MagQuick_AK','WeaponAttA_MagazineAK47_03',(3,-10,-2)),
             ('JAZZ_MagLarge_30_40','WeaponAttA_MagazineAK47_02',(3,-10,-2)),
             ('JAZZ_MagDrum_30_75','WeaponAttA_MagazineRPK74_03',(-9,-10,-8))]
    report={'level':'offline','visual_acceptance':'PENDING','target_feed_centre_top_mm':target.tolist(),'rows':[]}
    lua=LuaRuntime()
    lua.execute('AK103={};FirearmBase={UpdateVisualObj=function(self,vis) self.calls=(self.calls or 0)+1 end};IsValid=function(v) return type(v)=="table" end;point=function(x,y,z) return {x,y,z} end')
    source=(ROOT/'Code/System_WeaponComponent_Set.lua').read_text(encoding='utf-8-sig')
    start=source.index('function AK103:UpdateVisualObj(vis)')
    end=source.index('-- Type 56',start)
    lua.execute(source[start:end])
    for component,entity,offset in configs:
        d=decode(meshes/'AKMWaffleMag_AKMWaffleMag.m.hgm') if entity=='AKMWaffleMag' else json.loads((a.reference/'Geometry'/(entity+'_mesh.json')).read_text())
        donor=top_box(d);residual=donor+offset-target
        assert np.max(np.abs(residual))<.7,(entity,residual)
        lua.globals().component=component;lua.globals().entity=entity
        lua.execute('item=setmetatable({components={Magazine=component}},{__index=AK103});part={GetEntity=function() return entity end,SetAttachOffset=function(self,p) self.offset=p end};vis={weapon=item,parts={Magazine=part}};for i=1,10 do item:UpdateVisualObj(vis) end;assert(item.calls==10)')
        actual=tuple(lua.globals().part.offset[i] for i in (1,2,3))
        assert actual==offset,(component,actual)
        report['rows'].append({'component':component,'entity':entity,'offset_mm':offset,'residual_mm':residual.tolist(),'ten_updates_no_drift':True})
    text=(ROOT/'items.lua').read_text(encoding='utf-8-sig')
    assert re.search(r'ApplyTo = "AK103", Entity = "AKMWaffleMag", Slot = "Magazine"',text)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('PASS: four donor feed-box centres/tops within 0.7 mm; actual Lua setter idempotent. Visual QA pending.')


if __name__=='__main__':main()
