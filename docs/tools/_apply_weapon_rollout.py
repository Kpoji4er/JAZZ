"""Bounded WEAPON-ROLLOUT-001 transaction. --build <backup/stage> [--apply].

Stages synchronized stats/catalog/CSV, Ivan10 and only new weapon loot entries.
Does not run the full Legion generator or change unrelated presets.
"""
import argparse, csv, hashlib, importlib.util, io, json, re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT, matching, add_metadata
from _export_attach_csv import scalar, params, costs, display_name
from _apply_attach_001 import placeobj_blocks, prop, list_ids

NEW = {'AK74M': 'AK74', 'AK105': 'AKSU', 'SR3M': 'AS_Val', 'L42A1': 'M24Sniper'}
STATS = {
    'AK74': {'CyclicRPM': 600},
    'AK74M': {'CyclicRPM': 600, 'Cost': 16000, 'Tier': 4, 'RestockWeight': 45},
    'AK105': {'Damage': 27, 'Cost': 14500, 'Tier': 4, 'RestockWeight': 40},
    'SR3M': {'Cost': 22000, 'Tier': 4, 'RestockWeight': 20},
    'L42A1': {'Cost': 10000, 'Tier': 2, 'RestockWeight': 35},
}
for wid in NEW:
    STATS[wid].update(CanAppearInShop=True, MaxStock=1)

def bounds(text, kind, key, ident):
    pat = (rf"'{key}',\s*" if key=='Id' else rf'\b{key}\s*=\s*') + '"'+re.escape(ident)+'"'
    hit = re.search(pat, text)
    assert hit, (kind, ident)
    start = text.rfind(f"PlaceObj('{kind}'", 0, hit.start())
    assert start >= 0
    return start, matching(text, text.index('(', start))

def literal(v):
    return str(v).lower() if isinstance(v, bool) else str(v)

def patch_scalar(text, key, value, moditem=False):
    pattern = (rf"('{key}',\s*)([^,\r\n]+)" if moditem else rf'(\b{key}\s*=\s*)([^,\r\n]+)')
    hits=list(re.finditer(pattern,text)); assert len(hits)<=1,(key,len(hits))
    if hits:
        m=hits[0]; return text[:m.start(2)]+literal(value)+text[m.end(2):]
    pos=text.index('{')+1
    entry=f"\n\t'{key}', {literal(value)}," if moditem else f'\n\t{key} = {literal(value)},'
    return text[:pos]+entry+text[pos:]

def main():
    p=argparse.ArgumentParser();p.add_argument('--build',required=True,type=Path);p.add_argument('--apply',action='store_true');a=p.parse_args()
    before={}; staged={}
    def read(path):
        if path not in before: before[path]=path.read_bytes()
        return staged.get(path,before[path]).decode('utf-8-sig')
    def put(path,s):
        raw=before[path]
        if s.replace('\r\n','\n')==raw.decode('utf-8-sig').replace('\r\n','\n'):
            staged[path]=raw
            return
        newline='\r\n' if b'\r\n' in raw else '\n'
        encoded=s.replace('\r\n','\n').replace('\n',newline).encode('utf-8')
        staged[path]=(b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+encoded
    items=read(ROOT/'items.lua')
    for wid,values in STATS.items():
        path=ROOT/f'InventoryItem/{wid}.lua';src=read(path)
        start,end=bounds(items,'ModItemInventoryItemCompositeDef','Id',wid);block=items[start:end]
        for key,val in values.items():
            src=patch_scalar(src,key,val);block=patch_scalar(block,key,val,True)
        put(path,src);items=items[:start]+block+items[end:]
    put(ROOT/'items.lua',items)
    lua=LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
    function T(id,text) return {id=id,text=text} end
    function PlaceObj(class,props,children)
      local r={__class=class}
      for k,v in pairs(props or {}) do if type(k)=='string' then r[k]=v end end
      for i=1,#(props or {}),2 do r[props[i]]=props[i+1] end
      return r
    end
    DefineClass={};function UndefineClass(id) DefineClass[id]=nil end
    ''')
    targets=set(STATS)|{'AKM','AKSU','Mosin'}
    weapons={}
    for wid in targets:
        lua.execute(read(ROOT/f'InventoryItem/{wid}.lua'));w=lua.globals().DefineClass[wid];weapons[wid]=w
        start,end=bounds(items,'ModItemInventoryItemCompositeDef','Id',wid)
        m=lua.execute('return '+items[start:end])
        for key,val in STATS.get(wid,{}).items(): assert w[key]==m[key]==val,(wid,key)

    data=ROOT/'docs/technical/weapons/data'
    def csv_read(path):
        reader=csv.DictReader(io.StringIO(read(path)));return reader.fieldnames,list(reader)
    def csv_put(path,fields,rows):
        f=io.StringIO(newline='');wr=csv.DictWriter(f,fieldnames=fields);wr.writeheader();wr.writerows(rows);put(path,f.getvalue())
    fields,rows=csv_read(data/'weapons.csv');byid={r['id']:r for r in rows}
    families={'AssaultRifle':('assault-rifle','Штурмовые винтовки'),'Carbine':('carbine','Карабины'),'SubmachineGun':('submachine-gun','Пистолеты-пулемёты'),'SniperRifle':('sniper-rifle','Снайперские винтовки')}
    for wid,base in NEW.items():
        if wid not in byid:
            r=dict(byid[base]);r['id']=wid;rows.append(r);byid[wid]=r
    aliases={'shoot_ap':'ShootAP','reload_ap':'ReloadAP','cyclic_rpm':'CyclicRPM','caliber':'Caliber'}
    for wid in targets:
        w=weapons[wid];r=byid[wid]
        for col in fields:
            property_name=aliases.get(col,''.join(s.title() for s in col.split('_')))
            val=w[property_name]
            if val is not None and isinstance(val,(str,int,float,bool)):r[col]=literal(val)
        if wid in NEW:
            tier=w['comment'].removeprefix('Tier ');major,sub=tier.split('-')
            cls=w['object_class'];fid,ru=families[cls]
            r.update(display_name=w['DisplayName']['text'],object_class=cls,family_id=fid,family_name_ru=ru,catalog_status='active',balance_tier=major,balance_subtier=sub,tier_label=tier,tier_status='assigned',tier_source='JAZZ-WEAPON-ROLLOUT-001',code_tier_label=tier)
        r['engine_tier']=str(w['Tier']);r['source_file']=f'InventoryItem/{wid}.lua';r['snapshot_commit']='working-tree'
        r['available_attacks']=';'.join(w['AvailableAttacks'].values())
        r['component_slot_count']=str(len(w['ComponentSlots']))
        r['component_option_count']=str(sum(len(s['AvailableComponents']) for s in w['ComponentSlots'].values()))
        r['defaulted_fields']=';'.join(k for k in r['defaulted_fields'].split(';') if w[k] is None)
    csv_put(data/'weapons.csv',fields,rows)
    ofields,options=csv_read(data/'weapon-component-options.csv')
    # Only refresh the four new weapons; retain all other authored rows/order.
    options=[r for r in options if r['weapon_id'] not in NEW]
    for wid in NEW:
        for si,s in weapons[wid]['ComponentSlots'].items():
            for oi,cid in s['AvailableComponents'].items():
                r={key:'' for key in ofields}
                r.update(weapon_id=wid,slot_index=str(si),slot_type=s['SlotType'],modifiable=literal(s['Modifiable'] is not False),can_be_empty=literal(bool(s['CanBeEmpty'])),default_component=s['DefaultComponent'] or '',default_in_options=literal(s['DefaultComponent'] in list(s['AvailableComponents'].values())),option_index=str(oi),component_id=cid,component_name=cid,component_source='jazz',is_default=literal(cid==s['DefaultComponent']),source_file=f'InventoryItem/{wid}.lua',snapshot_commit='working-tree')
                options.append(r)
    csv_put(data/'weapon-component-options.csv',ofields,options)
    cfields,crows=csv_read(data/'weapon-components.csv')
    known={r['component_id'] for r in crows}
    needed={r['component_id'] for r in options if r['weapon_id'] in targets}
    for b in placeobj_blocks(items,'ModItemWeaponComponent'):
        cid=prop(b.text,'id')
        if cid not in needed or cid in known:continue
        crows.append(dict(component_id=cid,display_name=display_name(b.text,cid),slot=prop(b.text,'Slot') or '',cost=scalar(b.text,'Cost'),modification_difficulty=scalar(b.text,'ModificationDifficulty'),effects=';'.join(sorted(list_ids(b.text,'ModificationEffects'))),parameters=params(b.text),additional_costs=costs(b.text),group=prop(b.text,'group') or '',used_by_count=str(sum(r['component_id']==cid for r in options)),source='jazz',snapshot_commit='working-tree'))
        known.add(cid)
    csv_put(data/'weapon-components.csv',cfields,crows)
    efields,erows=csv_read(data/'weapon-component-effects.csv');known={r['effect_id'] for r in erows}
    needed={e for r in crows if r['component_id'] in needed for e in r['effects'].split(';') if e}
    for b in placeobj_blocks(items,'ModItemWeaponComponentEffect'):
        eid=prop(b.text,'id')
        if eid not in needed or eid in known:continue
        desc=re.search(r'Description\s*=\s*T\([\s\S]*?"([^"]*)"\)',b.text)
        erows.append(dict(effect_id=eid,display_name=display_name(b.text,eid),description=desc[1] if desc else '',parameters=params(b.text),source='jazz',snapshot_commit='working-tree'))
    csv_put(data/'weapon-component-effects.csv',efields,erows)
    overrides_path=ROOT/'scripts/legion-loadouts/data/weapon_tag_overrides.json'
    overrides=json.loads(read(overrides_path));overrides.update(L42A1={'replace_tags':['sniper']},AK105=['smg'])
    put(overrides_path,json.dumps(overrides,ensure_ascii=False,indent=2)+'\n')

    spec=importlib.util.spec_from_file_location('rollout_generator',ROOT/'scripts/legion-loadouts/generate.py')
    gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
    stage=a.build/'rollout-stage';stage.mkdir(parents=True,exist_ok=True)
    for name in ('weapons.csv','weapon-component-options.csv'):(stage/name).write_bytes(staged[data/name])
    gen.WEAPONS_CSV=stage/'weapons.csv';gen.COMP_CSV=stage/'weapon-component-options.csv'
    catalog=gen.load_weapons(overrides);comps=gen.load_components()
    variants=gen.expand_early_variants(gen.load_json('early_variants.json'),catalog,comps)
    recipes=gen.load_json('recipes.json');packages=gen.load_json('packages.json');ammo=gen.load_json('caliber_ammo.json')
    units=ROOT.parent/'jazz-units';ui=read(units/'items.lua');um=read(units/'metadata.lua')
    combos={};report={}
    prefixes=tuple('JAZZ_GenW_'+w+'_' for w in NEW)
    for recipe in recipes.values():
        pools=[(recipe['firearm'],recipe)]
        if recipe.get('cqb_secondary'):pools.append((recipe['cqb_secondary']['firearm'],gen.recipe_for_cqb(recipe)))
        for fid,rec in pools:
            if not re.search(r'\bid\s*=\s*"'+re.escape(fid)+'"',ui):continue
            plan,all_combos=gen.collect_firearm_plan(rec,catalog,packages,comps,ammo,variants)
            entries=[e for e in plan if e[0].startswith(prefixes)]
            if not entries:continue
            combos.update({k:v for k,v in all_combos.items() if k.startswith(prefixes)})
            start,end=bounds(ui,'ModItemLootDef','id',fid);block=ui[start:end];existing=[]
            for m in reversed(list(re.finditer(r"PlaceObj\('LootEntryLootDef'",block))):
                stop=matching(block,block.index('(',m.start()));entry=block[m.start():stop]
                if any('loot_def = "'+pre in entry for pre in prefixes):
                    existing.append(re.sub(r'\s+','',entry))
                    assert block[stop]==',';block=block[:m.start()]+block[stop+1:]
            emitted=gen.emit_firearm_from_plan(fid,entries)
            chunks=[]
            for m in re.finditer(r"PlaceObj\('LootEntryLootDef'",emitted):
                stop=matching(emitted,emitted.index('(',m.start()));entry=emitted[m.start():stop]
                if 'game_conditions' in entry:chunks.append(entry+',\n')
            assert len(chunks)==len(entries)
            report[fid]=entries
            if sorted(existing)==sorted(re.sub(r'\s+','',c[:-2]) for c in chunks):continue
            pos=block.rfind('}');block=block[:pos]+''.join(chunks)+block[pos:]
            ui=ui[:start]+block+ui[end:]
    assert report and combos
    for wid in NEW:assert any(k.startswith('JAZZ_GenW_'+wid+'_') for k in combos),wid
    updates={}
    for cid,block in combos.items():
        found=gen.find_moditem_block(ui,cid)
        if not found or re.sub(r'\s+','',ui[found[0]:found[1]])!=re.sub(r'\s+','',block):updates[cid]=block
    ui=gen.upsert_shared_combos(ui,updates)
    additions=[]
    for ident in combos:
        if not re.search(r"'Id',\s*\""+re.escape(ident)+'"',um):
            additions.append(f'PlaceObj(\'ModResourcePreset\', {{ \'Class\', "LootDef", \'Id\', "{ident}", \'ClassDisplayName\', "LootDef" }})')
    if additions:um=add_metadata(um,'affected_resources',additions)
    start,end=bounds(ui,'ModItemLootDef','id','Ivan10');block=ui[start:end]
    assert 'weapon = "AK74"' in block or 'weapon = "AK74M"' in block
    block=block.replace('weapon = "AK74"','weapon = "AK74M"')
    for cid in re.findall(r'"(JAZZ_(?:Reflex|Compensator|Stock)\w*)"',block):
        assert cid in {c for s in comps['AK74M'].values() for c in s},cid
    ui=ui[:start]+block+ui[end:]
    # Owner-approved repair of the existing Crusher recipe/materialization drift.
    crusher=recipes['JAZZ_Legion_AssaultT1_Crusher']
    emitted=gen.emit_inventory('JAZZ_Legion_AssaultT1_Crusher',crusher,gen.parse_prices())
    knife=[]
    for m in re.finditer(r"PlaceObj\('LootEntryInventoryItem'",emitted):
        stop=matching(emitted,emitted.index('(',m.start()));entry=emitted[m.start():stop]
        if 'item = "Knife"' in entry:knife.append(entry)
    assert len(knife)==3
    start,end=bounds(ui,'ModItemLootDef','id','Crusher_Inventory');block=ui[start:end]
    existing=[]
    for m in re.finditer(r"PlaceObj\('LootEntryInventoryItem'",block):
        stop=matching(block,block.index('(',m.start()));entry=block[m.start():stop]
        if 'item = "Knife"' in entry:existing.append(entry)
    if not existing:
        pos=block.rfind('}');block=block[:pos]+',\n'.join(knife)+',\n'+block[pos:]
        ui=ui[:start]+block+ui[end:]
    else:assert sorted(re.sub(r'\s+','',e) for e in existing)==sorted(re.sub(r'\s+','',e) for e in knife),'Crusher changed outside the approved recipe'
    put(units/'items.lua',ui);put(units/'metadata.lua',um)
    for path,raw in staged.items():
        if path.suffix=='.lua':lua.compile(raw.decode('utf-8'))
    for fid,entries in report.items():
        for cid,lo,hi,weight in entries:
            wid=next(w for w in NEW if cid.startswith('JAZZ_GenW_'+w+'_'))
            assert lo>=({'SR3M':32,'L42A1':21}.get(wid,31)),(fid,cid,lo)
            assert weight>0
    (stage/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    changed={p:b for p,b in staged.items() if b!=before[p]}
    for path,raw in changed.items():
        rel=path.relative_to(ROOT.parent)
        target=stage/'files'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    if a.apply:
        for path,raw in before.items():assert path.read_bytes()==raw,'Concurrent modification: '+str(path)
        for path in changed:
            rel=path.relative_to(ROOT.parent);dest=a.build/'rollout-backup'/rel
            dest=dest.with_name(dest.name+'.'+hashlib.sha256(before[path]).hexdigest()[:12])
            dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists():assert dest.read_bytes()==before[path]
            else:dest.write_bytes(before[path])
        for path,raw in changed.items():path.write_bytes(raw)
    print(f'PASS: {len(changed)} files, {len(report)} existing pools, {len(combos)} combos, {len(additions)} metadata additions; Ivan10 and four shop entries. Applied={a.apply}')
    for path in changed: print('  '+str(path.relative_to(ROOT.parent)))

if __name__=='__main__':main()
