"""Apply only Mosin loadout deltas from canonical Legion recipes.

--build <Mosin build> [--apply]. Does not regenerate inventories or other weapons.
"""
import argparse,importlib.util,json,re,hashlib
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import ROOT,matching,write,add_metadata

p=argparse.ArgumentParser();p.add_argument('--build',required=True,type=Path);p.add_argument('--apply',action='store_true');a=p.parse_args()
spec=importlib.util.spec_from_file_location('mosin_legion_generator',ROOT/'scripts/legion-loadouts/generate.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
recipes=gen.load_json('recipes.json');packages=gen.load_json('packages.json');ammo=gen.load_json('caliber_ammo.json')
weapons=gen.load_weapons(gen.load_json('weapon_tag_overrides.json'));comps=gen.load_components()
variants=gen.expand_early_variants(gen.load_json('early_variants.json'),weapons,comps)
paths=[gen.ITEMS,gen.UNITS/'metadata.lua'];before={path:path.read_bytes() for path in paths}
items=before[paths[0]].decode('utf-8-sig');meta=before[paths[1]].decode('utf-8-sig')
combos={};report={}
def bounds(text,ident):
    m=re.search(r'\bid\s*=\s*"'+re.escape(ident)+'"',text);assert m,ident
    start=text.rfind("PlaceObj('ModItemLootDef'",0,m.start());assert start>=0
    return start,matching(text,text.index('(',start))
for unit,recipe in recipes.items():
    targets=[(recipe['firearm'],recipe)]
    if recipe.get('cqb_secondary'):targets.append((recipe['cqb_secondary']['firearm'],gen.recipe_for_cqb(recipe)))
    for fid,r in targets:
        # Some authored recipes have a CQB pool that has not been installed yet.
        # This transaction only extends existing pools; it does not activate them.
        if not re.search(r'\bid\s*=\s*"'+re.escape(fid)+'"',items):continue
        plan,all_combos=gen.collect_firearm_plan(r,weapons,packages,comps,ammo,variants)
        for cid,lo,hi,weight in plan:
            if '_Mosin_obrez_' not in cid:continue
            peers=[e[3] for e in plan if '_Mosin_' not in e[0] and e[2]==hi and e[3]>0]
            assert peers and weight<min(peers),(fid,cid,weight,peers)
        combos.update({k:v for k,v in all_combos.items() if k.startswith('JAZZ_GenW_Mosin_')})
        # Replace only gated Mosin entries. Other guns and the pre-existing
        # unconditional sniper fallback remain byte-for-byte unchanged.
        start,end=bounds(items,fid);old=items[start:end];patched=old
        for m in reversed(list(re.finditer(r"PlaceObj\('LootEntryLootDef'",patched))):
            stop=matching(patched,patched.index('(',m.start()));entry=patched[m.start():stop]
            if 'loot_def = "JAZZ_GenW_Mosin_' in entry and 'game_conditions' in entry:
                assert patched[stop]==','
                line=patched.rfind('\n',0,m.start())+1
                begin=line if not patched[line:m.start()].strip() else m.start()
                patched=patched[:begin]+patched[stop+1:]
        new=[e for e in plan if e[0].startswith('JAZZ_GenW_Mosin_')]
        if new:
            emitted=gen.emit_firearm_from_plan(fid,new)
            children=emitted[emitted.index("PlaceObj('LootEntryLootDef'"):emitted.rfind('}')]
            pos=patched.rfind('}');patched=patched[:pos]+children+patched[pos:]
        if not new and patched==old:continue
        items=items[:start]+patched+items[end:]
        report[fid]=new
items=gen.upsert_shared_combos(items,combos)
missing=[]
for ident in sorted(combos):
    if not re.search(r"'Id',\s*\""+re.escape(ident)+'"',meta):
        missing.append("PlaceObj('ModResourcePreset', { 'Class', \"LootDef\", 'Id', \""+ident+"\", 'ClassDisplayName', \"LootDef\" })")
if missing:meta=add_metadata(meta,'affected_resources',missing)
for source in (items,meta):LuaRuntime().compile(source)
assert any('obrez_t1' in e[0] for e in report['Marauder_Firearm'])
for fid,entries in report.items():
    for cid,lo,hi,weight in entries:
        short=bool(re.match(r'JAZZ_GenW_Mosin_(?:m38|obrez)_',cid))
        assert (lo,hi) in ([(12,19),(20,29)] if short else [(11,19),(20,29)]),(cid,lo,hi)
        if '_Mosin_obrez_' in cid:
            assert weight==((1 if lo==20 else 10) if fid=='Roughneck_Firearm' else (10 if lo==20 else 100))
        else:assert weight==1400 if lo==20 else weight in (50500,101000)
        if not short:assert '"JAZZ_Scope_PU"' in combos[cid],(fid,cid)
for block in combos.values():
    assert '"Mosin"' in block and '762x54_sniper_ammo' in block
    for upgrade in re.findall(r'"(JAZZ_(?:Mosin\w+|Scope_PU))"',block):
        assert upgrade in {c for values in comps['Mosin'].values() for c in values}
out=a.build/'legion-stage';out.mkdir(exist_ok=True)
write(out/'items.lua',items);write(out/'metadata.lua',meta)
(out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
if a.apply:
    for path,raw in before.items():
        assert path.read_bytes()==raw,'Concurrent modification: '+str(path)
        dest=a.build/'legion-integration-backup'/path.name
        dest.parent.mkdir(exist_ok=True)
        if dest.exists() and dest.read_bytes()!=raw:
            dest=dest.with_name(dest.stem+'-'+hashlib.sha256(raw).hexdigest()[:12]+dest.suffix)
            if dest.exists():assert dest.read_bytes()==raw,dest
            else:dest.write_bytes(raw)
        else:dest.write_bytes(raw)
    write(paths[0],items);write(paths[1],meta)
print(f'PASS: {len(report)} weapon pools; {len(combos)} Mosin combos, {len(missing)} new metadata records; approved 12-19 / 20-29 gates, earlier sniper PU preserved. Applied={a.apply}')
