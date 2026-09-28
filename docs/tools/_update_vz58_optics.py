"""Stage/apply VZ58's existing rail-compatible collimators; --output DIR [--apply].

Only the VZ58 Scope list in items.lua/companion and its catalog count change. Metadata and
global component presets already register all three optional generic visuals.
Apply requires closed JA3/JA3Debug and backs up the current files.
"""
import argparse, csv, io, json, re, subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_vz58 import ROOT,component_block
from _integrate_sr3m import matching

OPTIONS=['JAZZ_Reflex_Closed','JAZZ_Reflex_Open','JAZZ_Reflex_Eotech','JAZZ_Reflex_M68']
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=True)
items=(ROOT/'items.lua').read_text(encoding='utf-8-sig')
hit=re.search(r"'Id',\s*\"VZ58\"",items);assert hit
start=items.rfind("PlaceObj('ModItemInventoryItemCompositeDef'",0,hit.start());end=matching(items,items.index('(',start))
def change(block):
 hit=re.search(r"'SlotType',\s*\"Scope\"",block);assert hit
 begin=block.index("'AvailableComponents'",hit.end());op=block.index('{',begin);close=matching(block,op,'{','}')
 return block[:op]+'{\n'+''.join('\t\t\t\t"'+v+'",\n' for v in OPTIONS)+'\t\t\t}'+block[close:]
updated=items[:start]+change(items[start:end])+items[end:]
companion=change((ROOT/'InventoryItem/VZ58.lua').read_text(encoding='utf-8-sig'))
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('function PlaceObj(c,p) local r={} for k,v in pairs(p or {}) do if type(k)=="string" then r[k]=v end end for i=1,#(p or {}),2 do r[p[i]]=p[i+1] end return r end; function T(id,text) return text end; function point(...) return {...} end; DefineClass={}; function UndefineClass(id) end')
lua.compile(updated);lua.execute(companion)
def native(value):return {k:native(v) for k,v in value.items()} if hasattr(value,'items') else value
staged_item=native(lua.execute('return '+change(items[start:end])))
staged_companion=native(lua.globals().DefineClass.VZ58)
for key,value in staged_companion.items():
 if not key.startswith('__'):assert staged_item[key]==value,('Companion mismatch',key)
visuals={}
for cid in OPTIONS[1:]:
 lo,hi=component_block(items,cid);c=lua.execute('return '+items[lo:hi])
 candidates=[v for v in c.Visuals.values() if v.Slot=='Scope' and not v.ApplyTo]
 assert len(candidates)==1,(cid,len(candidates));visuals[cid]=candidates[0].Entity
assert len(set(visuals.values()))==3
catalog_path='docs/technical/weapons/data/weapons.csv'
catalog=(ROOT/catalog_path).read_text(encoding='utf-8-sig');lines=catalog.splitlines(keepends=True)
header=next(csv.reader([lines[0]]));id_column=header.index('id');count_column=header.index('component_option_count')
for i,line in enumerate(lines[1:],1):
 row=next(csv.reader([line]))
 if row[id_column]!='VZ58':continue
 row[count_column]=str(sum(len(slot['AvailableComponents']) for slot in staged_companion['ComponentSlots'].values()))
 buffer=io.StringIO();csv.writer(buffer,lineterminator='\n').writerow(row);lines[i]=buffer.getvalue();break
else:raise AssertionError('VZ58 catalog row missing')
updates={'items.lua':updated,'InventoryItem/VZ58.lua':companion,catalog_path:''.join(lines)}
before={rel:(ROOT/rel).read_bytes() for rel in updates}
for rel,value in updates.items():
 # Snapshot suffix prevents repository-wide generated-Lua discovery from
 # mistaking review copies for active companions.
 staged=a.output/'staged'/(rel+'.txt');staged.parent.mkdir(parents=True,exist_ok=True);staged.write_text(value,encoding='utf-8')
report={'options':OPTIONS,'generic_scope_visuals':visuals,'metadata_changed':False,'applied':False}
if a.apply:
 running=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True).stdout.strip()
 assert not running,'Close game/editor before generated-data transaction'
 assert all((ROOT/rel).read_bytes()==raw for rel,raw in before.items()),'Concurrent file change; restage'
 for rel,value in updates.items():
  target=ROOT/rel;backup=a.output/'backup'/(rel+'.txt');backup.parent.mkdir(parents=True,exist_ok=True)
  assert not backup.exists(),'Refuse to overwrite backup'
  backup.write_bytes(target.read_bytes());target.write_text(value,encoding='utf-8')
 report['applied']=True
(a.output/'optics-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
