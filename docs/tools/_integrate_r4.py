"""Bounded VektorR4 data/assets/catalog transaction; --build DIR [--apply].
Requires staged native assets and closed JA3. Preserves other working-tree edits.
"""
import argparse,csv,io,json,re,shutil,subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,ASSETS,matching,append_root_item,add_metadata

TEXTS={
 'DisplayName':('890000000019401','Vektor R4','Vektor R4'),
 'DisplayNamePlural':('890000000019402','Vektor R4','Vektor R4'),
 'Description':('890000000019403',
 'Южноафриканский армейский автомат под патрон 5,56x45 мм. Тяжёлый и надёжный, с магазином на 35 патронов. Штатная конфигурация с открытым прицелом.',
 'A South African service rifle chambered in 5.56x45 mm. Heavy and reliable, with a 35-round magazine. Standard configuration with iron sights.')}
VALUES={'comment':'Tier 2-1','Reliability':85,'RepairCost':12,'Cost':5500,'Tier':2,'RestockWeight':70,'MaxStock':2,
 'Damage':21,'AimAccuracy':11,'MagazineSize':35,'WeaponRange':46,'Noise':53,
 'Entity':'JAZZ_VektorR4','fxClass':'Galil','ShootAP':6000,'ReloadAP':6000,'Recoil':18,
 'BurstShots':3,'AutoShots':6,'WeaponMass':43,'CyclicRPM':650,'CloseRange':7,'CloseRangeFactor':80,
 'BulletDropRange':15,'Grouping':50,'BaseJamChance':-15,'WeaponResource':7000,
 'Icon':'Mod/e6L4ECj/WeaponIcons/VektorR4.png'}

def literal(v):return json.dumps(v,ensure_ascii=False)

def build_weapon():
    s=(ROOT/'InventoryItem/M16A1.lua').read_text(encoding='utf-8').replace('M16A1','VektorR4')
    for field,(ident,ru,en) in TEXTS.items():
        s=re.sub(r'^\t'+field+r' = .*$',f'\t{field} = T({ident}, --[[ModItemInventoryItemCompositeDef VektorR4 {field}]] "{ru}"),',s,flags=re.M)
    s=re.sub(r'^\tAdditionalHint = .*\n','',s,flags=re.M)
    for field,value in VALUES.items():
        line=f'\t{field} = {literal(value)},'
        s,n=re.subn(r'^\t'+field+r' = [^\n]+',lambda m:line,s,flags=re.M)
        if not n:s=s.replace('\tcomment =',line+'\n\tcomment =',1)
    start=s.index('\tComponentSlots = {');end=matching(s,s.index('{',start),'{','}')
    s=s[:start]+'\tComponentSlots = {}'+s[end:]
    props=s[s.index('\t',s.index('__generated_by_class')):s.rfind('}')]
    props=re.sub(r'^\t__generated_by_class = .*\n','',props,flags=re.M)
    props=re.sub(r'^\t([A-Za-z_][A-Za-z_0-9]*) = ',r"\t'\1', ",props,flags=re.M)
    item="\tPlaceObj('ModItemInventoryItemCompositeDef', {\n\t'Id', \"VektorR4\",\n\t'Group', \"JAZZ - Firearm - Rifles-AR\",\n"+props+'\t}),'
    return s,item

def main():
    p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
    # No stale editor may overwrite this transaction.
    proc=subprocess.run(['powershell','-NoProfile','-Command',"Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id"],capture_output=True,text=True)
    assert not proc.stdout.strip(),'JA3/editor must be closed'
    before={};updates={}
    def read(path):before[path]=path.read_bytes();return before[path].decode('utf-8-sig')
    def put(path,text):
        raw=before.get(path,b'');nl='\r\n' if b'\r\n' in raw else '\n'
        updates[path]=(b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+text.replace('\r\n','\n').replace('\n',nl).encode('utf-8')
    items=read(ROOT/'items.lua');meta=read(ROOT/'metadata.lua')
    assert '"VektorR4"' not in items,'Already installed'
    for ident,_,_ in TEXTS.values():assert ident not in items,'ID collision'
    companion,item=build_weapon()
    lua=LuaRuntime(unpack_returned_tuples=True);lua.execute('''
    function T(id,text) return {id=id,text=text} end
    function PlaceObj(c,p,ch) local r={} for k,v in pairs(p or {}) do if type(k)=='string' then r[k]=v end end for i=1,#(p or {}),2 do r[p[i]]=p[i+1] end return r end
    DefineClass={};function UndefineClass(id) end
    ''');lua.execute(companion)
    w=lua.globals().DefineClass.VektorR4;m=lua.execute('return '+item.strip().rstrip(','))
    for field in VALUES:assert w[field]==m[field],field
    put(ROOT/'InventoryItem/VektorR4.lua',companion)
    put(ROOT/'items.lua',append_root_item(items,item))
    meta=add_metadata(meta,'code',['"InventoryItem/VektorR4.lua"'])
    meta=add_metadata(meta,'affected_resources',["PlaceObj('ModResourcePreset', { 'Class', \"InventoryItemCompositeDef\", 'Id', \"VektorR4\", 'ClassDisplayName', \"Inventory item\" })"])
    put(ROOT/'metadata.lua',meta)
    ai=read(ASSETS/'items.lua');am=read(ASSETS/'metadata.lua')
    ent='JAZZ_VektorR4'
    assert ent not in ai,'Entity already registered'
    put(ASSETS/'items.lua',append_root_item(ai,f'\tPlaceObj(\'ModItemEntity\', {{\n\t\t\'name\', "{ent}",\n\t\t\'ClassParents\', {{}},\n\t\t\'entity_name\', "{ent}",\n\t}}),'))
    am=add_metadata(am,'entities',[f'"{ent}"']);am=add_metadata(am,'code',[f'"Entities/{ent}.lua"']);put(ASSETS/'metadata.lua',am)
    path=ROOT/'docs/technical/weapons/data/weapons.csv';reader=csv.DictReader(io.StringIO(read(path)));fields=reader.fieldnames;rows=list(reader)
    row=dict(next(r for r in rows if r['id']=='M16A1'))
    aliases={'shoot_ap':'ShootAP','reload_ap':'ReloadAP','cyclic_rpm':'CyclicRPM','caliber':'Caliber'}
    for col in fields:
        value=w[aliases.get(col,''.join(s.title() for s in col.split('_')))]
        if isinstance(value,(str,int,float,bool)):row[col]=str(value).lower() if isinstance(value,bool) else str(value)
    row.update(id='VektorR4',display_name='Vektor R4',balance_tier='2',balance_subtier='1',tier_label='2-1',code_tier_label='2-1',tier_source='JAZZ-WEAPON-R4-001',engine_tier='2',source_file='InventoryItem/VektorR4.lua',snapshot_commit='working-tree',component_slot_count='0',component_option_count='0',available_attacks=';'.join(w.AvailableAttacks.values()))
    row['defaulted_fields']=';'.join(k for k in row['defaulted_fields'].split(';') if w[k] is None)
    rows.append(row);out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=fields);writer.writeheader();writer.writerows(rows);put(path,out.getvalue())
    stage=a.build/'mod-assets-stage/Entities';assert (stage/(ent+'.ent')).exists()
    for src in stage.rglob('*'):
        if src.is_file():
            target=ASSETS/'Entities'/src.relative_to(stage);assert not target.exists(),target;updates[target]=src.read_bytes()
    updates[ROOT/'WeaponIcons/VektorR4.png']=(a.build/'VektorR4_icon.png').read_bytes()
    report={'files':[str(p.relative_to(ROOT.parent)) for p in updates],'stats':VALUES,'runtime':'NOT_RUN'}
    (a.build/'integration-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    if a.apply:
        for path,raw in before.items():assert path.read_bytes()==raw,'Concurrent edit: '+str(path)
        for path,data in updates.items():
            if path.exists():
                backup=a.build/'integration-backup'/path.relative_to(ROOT.parent);backup.parent.mkdir(parents=True,exist_ok=True);assert not backup.exists();backup.write_bytes(path.read_bytes())
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print(('Installed' if a.apply else 'Staged'),len(updates),'files')

if __name__=='__main__':main()
