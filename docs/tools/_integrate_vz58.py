"""Bounded VZ58 data/assets/catalog transaction; --build DIR [--apply].
Requires staged native assets and closed JA3. Preserves other working-tree edits.
"""
import argparse,csv,io,json,re,shutil,subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,ASSETS,matching,append_root_item,add_metadata

TEXTS={
 'DisplayName':('890000000019501','vz. 58','vz. 58'),
 'DisplayNamePlural':('890000000019502','vz. 58','vz. 58'),
 'Description':('890000000019503',
 'Чехословацкий автомат под патрон 7,62x39 мм. Лёгкий, скорострельный, с магазином на 30 патронов. Штатную мебель можно заменить современными прикладом, рукоятью и цевьём с планками.',
 'A Czechoslovak service rifle chambered in 7.62x39 mm. Light and fast-firing, with a 30-round magazine. Its original furniture can be replaced with a modern stock, pistol grip and railed handguard.')}
VALUES={'comment':'Tier 2-2','Reliability':85,'RepairCost':10,'Cost':6000,'Tier':2,'RestockWeight':55,'MaxStock':2,
 'Caliber':'JAZZ_Caliber_762x39','Damage':27,'AimAccuracy':10,'MagazineSize':30,'WeaponRange':38,'Noise':55,
 'Entity':'JAZZ_VZ58','fxClass':'AK47','ShootAP':5000,'ReloadAP':6000,'Recoil':23,
 'BurstShots':4,'AutoShots':8,'WeaponMass':29,'CyclicRPM':800,'CloseRange':7,'CloseRangeFactor':85,
 'BulletDropRange':14,'Grouping':60,'BaseJamChance':-15,'WeaponResource':7000,
 'Icon':'Mod/e6L4ECj/WeaponIcons/VZ58.png'}
# RPM/200 short burst is the suite's existing rule, hence four rounds at 800 RPM.
GENERIC_SCOPES={'JAZZ_Reflex_Open':'WeaponAttA_CompactReflexSight','JAZZ_Reflex_Eotech':'WeaponAttA_ScopeReflex','JAZZ_Reflex_M68':'Ithaca_AimPoint'}
SLOTS=[('Scope',['JAZZ_Reflex_Closed',*GENERIC_SCOPES],None),
 ('Magazine',['JAZZ_MagNormal','JAZZ_MagQuick'],'JAZZ_MagNormal'),
 ('Handguard',['JAZZ_VZ58_HandguardWood','JAZZ_Handguard_RIS'],'JAZZ_VZ58_HandguardWood'),
 ('Handgrip',['JAZZ_Handgrip_Default','JAZZ_Handgrip_Ergo'],'JAZZ_Handgrip_Default'),
 ('Under',['JAZZ_VerticalGrip'],None),
 ('Stock',['JAZZ_StockNormal','JAZZ_StockLightUnFolded','JAZZ_StockLightFolded','JAZZ_StockHeavy'],'JAZZ_StockNormal'),
 ('Muzzle',['JAZZ_Suppressor'],None)]
WIRING={'JAZZ_Reflex_Closed':('Scope','Reflex'),'JAZZ_MagNormal':('Magazine','Magazine'),
 'JAZZ_MagQuick':('Magazine','MagQuick'),'JAZZ_VZ58_HandguardWood':('Handguard','HandguardWood'),
 'JAZZ_Handguard_RIS':('Handguard','HandguardRIS'),'JAZZ_Handgrip_Default':('Handgrip','GripWood'),
 'JAZZ_Handgrip_Ergo':('Handgrip','GripModern'),'JAZZ_VerticalGrip':('Under','Foregrip'),
 'JAZZ_StockNormal':('Stock','StockWood'),'JAZZ_StockLightUnFolded':('Stock','StockWire'),'JAZZ_StockLightFolded':('Stock','StockWireFolded'),
 'JAZZ_StockHeavy':('Stock','StockModern'),'JAZZ_Suppressor':('Muzzle','Suppressor')}

def component_block(s,ident):
    hit=re.search(r'\bid\s*=\s*"'+ident+'"',s);assert hit,ident
    start=s.rfind("PlaceObj('ModItemWeaponComponent'",0,hit.start());end=matching(s,s.index('(',start));return start,end

def components(items):
    start,end=component_block(items,'JAZZ_Handguard');wood=items[start:end]
    wood=wood.replace('id = "JAZZ_Handguard"','id = "JAZZ_VZ58_HandguardWood"')
    at=wood.index('Visuals =');finish=matching(wood,wood.index('{',at),'{','}')
    wood=wood[:at]+'BlockSlots = { "Scope", "Under" },\n\tVisuals = {}'+wood[finish:]
    items=append_root_item(items,'\t'+wood+',')
    # Existing generic effects are reused; only weapon-specific visual records change.
    for ident,(slot,suffix) in WIRING.items():
        start,end=component_block(items,ident);block=items[start:end]
        visual=f'PlaceObj(\'WeaponComponentVisual\', {{ ApplyTo = "VZ58", Entity = "JAZZ_VZ58_{suffix}", Slot = "{slot}", param_bindings = false }}),'
        block,n=re.subn(r'Visuals\s*=\s*\{',lambda m:m[0]+'\n\t'+visual,block,count=1);assert n==1
        items=items[:start]+block+items[end:]
    return items

def literal(v):return json.dumps(v,ensure_ascii=False)

def build_weapon():
    s=(ROOT/'InventoryItem/AK47.lua').read_text(encoding='utf-8').replace('AK47','VZ58')
    for field,(ident,ru,en) in TEXTS.items():
        s=re.sub(r'^\t'+field+r' = .*$',f'\t{field} = T({ident}, --[[ModItemInventoryItemCompositeDef VZ58 {field}]] "{ru}"),',s,flags=re.M)
    s=re.sub(r'^\tAdditionalHint = .*\n','',s,flags=re.M)
    for field,value in VALUES.items():
        line=f'\t{field} = {literal(value)},'
        s,n=re.subn(r'^\t'+field+r' = [^\n]+',lambda m:line,s,flags=re.M)
        if not n:s=s.replace('\tcomment =',line+'\n\tcomment =',1)
    start=s.index('\tComponentSlots = {');end=matching(s,s.index('{',start),'{','}')
    from _apply_sr3m_slots import slot
    body=''.join(slot('\t\t',name,options,default,can_be_empty=default is None) for name,options,default in SLOTS)
    s=s[:start]+'\tComponentSlots = {\n'+body+'\t}'+s[end:]
    props=s[s.index('\t',s.index('__generated_by_class')):s.rfind('}')]
    props=re.sub(r'^\t__generated_by_class = .*\n','',props,flags=re.M)
    props=re.sub(r'^\t([A-Za-z_][A-Za-z_0-9]*) = ',r"\t'\1', ",props,flags=re.M)
    item="\tPlaceObj('ModItemInventoryItemCompositeDef', {\n\t'Id', \"VZ58\",\n\t'Group', \"JAZZ - Firearm - Rifles-AR\",\n"+props+'\t}),'
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
    assert '"VZ58"' not in items,'Already installed'
    for ident,_,_ in TEXTS.values():assert ident not in items,'ID collision'
    companion,item=build_weapon()
    lua=LuaRuntime(unpack_returned_tuples=True);lua.execute('''
    function T(id,text) return {id=id,text=text} end
    function PlaceObj(c,p,ch) local r={} for k,v in pairs(p or {}) do if type(k)=='string' then r[k]=v end end for i=1,#(p or {}),2 do r[p[i]]=p[i+1] end return r end
    DefineClass={};function UndefineClass(id) end
    ''');lua.execute(companion)
    w=lua.globals().DefineClass.VZ58;m=lua.execute('return '+item.strip().rstrip(','))
    for field in VALUES:assert w[field]==m[field],field
    put(ROOT/'InventoryItem/VZ58.lua',companion)
    put(ROOT/'items.lua',components(append_root_item(items,item)))
    meta=add_metadata(meta,'code',['"InventoryItem/VZ58.lua"'])
    meta=add_metadata(meta,'affected_resources',["PlaceObj('ModResourcePreset', { 'Class', \"InventoryItemCompositeDef\", 'Id', \"VZ58\", 'ClassDisplayName', \"Inventory item\" })"])
    meta=add_metadata(meta,'affected_resources',["PlaceObj('ModResourcePreset', { 'Class', \"WeaponComponent\", 'Id', \"JAZZ_VZ58_HandguardWood\", 'ClassDisplayName', \"Weapon component\" })"])
    put(ROOT/'metadata.lua',meta)
    ai=read(ASSETS/'items.lua');am=read(ASSETS/'metadata.lua')
    entities=sorted(p.stem for p in (a.build/'mod-assets-stage/Entities').glob('JAZZ_VZ58*.ent'))
    assert len(entities)==14,entities
    for ent in entities:
        assert ent not in ai,'Entity already registered'
        ai=append_root_item(ai,f'\tPlaceObj(\'ModItemEntity\', {{\n\t\t\'name\', "{ent}",\n\t\t\'ClassParents\', {{}},\n\t\t\'entity_name\', "{ent}",\n\t}}),')
    put(ASSETS/'items.lua',ai)
    am=add_metadata(am,'entities',[f'"{ent}"' for ent in entities]);am=add_metadata(am,'code',[f'"Entities/{ent}.lua"' for ent in entities]);put(ASSETS/'metadata.lua',am)
    path=ROOT/'docs/technical/weapons/data/weapons.csv';reader=csv.DictReader(io.StringIO(read(path)));fields=reader.fieldnames;rows=list(reader)
    row=dict(next(r for r in rows if r['id']=='AK47'))
    aliases={'shoot_ap':'ShootAP','reload_ap':'ReloadAP','cyclic_rpm':'CyclicRPM','caliber':'Caliber'}
    for col in fields:
        value=w[aliases.get(col,''.join(s.title() for s in col.split('_')))]
        if isinstance(value,(str,int,float,bool)):row[col]=str(value).lower() if isinstance(value,bool) else str(value)
    row.update(id='VZ58',display_name='vz. 58',balance_tier='2',balance_subtier='2',tier_label='2-2',code_tier_label='2-2',tier_source='JAZZ-WEAPON-VZ58-001',engine_tier='2',source_file='InventoryItem/VZ58.lua',snapshot_commit='working-tree',component_slot_count=str(len(SLOTS)),component_option_count=str(sum(len(v[1]) for v in SLOTS)),available_attacks=';'.join(w.AvailableAttacks.values()))
    row['defaulted_fields']=';'.join(k for k in row['defaulted_fields'].split(';') if w[k] is None)
    rows.append(row);out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=fields);writer.writeheader();writer.writerows(rows);put(path,out.getvalue())
    stage=a.build/'mod-assets-stage/Entities';assert (stage/'JAZZ_VZ58.ent').exists()
    for src in stage.rglob('*'):
        if src.is_file():
            target=ASSETS/'Entities'/src.relative_to(stage);assert not target.exists(),target;updates[target]=src.read_bytes()
    updates[ROOT/'WeaponIcons/VZ58.png']=(a.build/'VZ58_icon.png').read_bytes()
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
