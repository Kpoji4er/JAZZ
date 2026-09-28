"""Add only generator-derived VektorR4 entries to existing Legion loot pools.
--build DIR [--apply]; no unrelated pool regeneration or version bump.
"""
import argparse,importlib.util,json,re
from pathlib import Path
from _integrate_sr3m import ROOT,matching,add_metadata

def main():
 p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
 spec=importlib.util.spec_from_file_location('r4lootgen',ROOT/'scripts/legion-loadouts/generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 weapons=g.load_weapons(g.load_json('weapon_tag_overrides.json'));comps=g.load_components()
 assert any(w['id']=='VektorR4' for w in weapons)
 variants=g.expand_early_variants(g.load_json('early_variants.json'),weapons,comps)
 packages=g.load_json('packages.json');ammo=g.load_json('caliber_ammo.json')
 units=ROOT.parent/'jazz-units';paths=[units/'items.lua',units/'metadata.lua'];before={p:p.read_bytes() for p in paths}
 ui=before[paths[0]].decode('utf-8-sig');um=before[paths[1]].decode('utf-8-sig');prefix='JAZZ_GenW_VektorR4_';combos={};report={}
 assert prefix not in ui,'Already integrated'
 for recipe in g.load_json('recipes.json').values():
  pools=[(recipe['firearm'],recipe)]
  if recipe.get('cqb_secondary'):pools.append((recipe['cqb_secondary']['firearm'],g.recipe_for_cqb(recipe)))
  for fid,rec in pools:
   found=g.find_moditem_block(ui,fid)
   if not found:continue
   plan,all_combos=g.collect_firearm_plan(rec,weapons,packages,comps,ammo,variants)
   entries=[e for e in plan if e[0].startswith(prefix)]
   if not entries:continue
   assert all(e[1]==21 and e[3]==101000 for e in entries),entries
   combos.update({k:v for k,v in all_combos.items() if k.startswith(prefix)})
   emitted=g.emit_firearm_from_plan(fid,entries);chunks=[]
   for hit in re.finditer(r"PlaceObj\('LootEntryLootDef'",emitted):
    end=matching(emitted,emitted.index('(',hit.start()));entry=emitted[hit.start():end]
    if prefix in entry and 'game_conditions' in entry:chunks.append(entry+',\n')
   assert len(chunks)==len(entries)
   start,end=found;block=ui[start:end];pos=block.rfind('}');block=block[:pos]+''.join(chunks)+block[pos:];ui=ui[:start]+block+ui[end:];report[fid]=entries
 assert report and combos
 ui=g.upsert_shared_combos(ui,combos)
 additions=[f'PlaceObj(\'ModResourcePreset\', {{ \'Class\', "LootDef", \'Id\', "{cid}", \'ClassDisplayName\', "LootDef" }})' for cid in combos]
 um=add_metadata(um,'affected_resources',additions)
 (a.build/'loot-report.json').write_text(json.dumps({'pools':report,'combos':list(combos),'weight':101000,'unlock':21},indent=2),encoding='utf-8')
 if a.apply:
  for path in paths:assert path.read_bytes()==before[path],'Concurrent edit'
  for path,text in zip(paths,[ui,um]):
   backup=a.build/'integration-backup/jazz-units'/path.name;backup.parent.mkdir(parents=True,exist_ok=True);assert not backup.exists();backup.write_bytes(before[path])
   raw=before[path];nl='\r\n' if b'\r\n' in raw else '\n';path.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+text.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
 print('R4 loot:',len(report),'pools,',len(combos),'weapon/ammo combos; applied=',a.apply)

if __name__=='__main__':main()
