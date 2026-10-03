"""Install only staged Conrad entities and patch the existing Conrad appearance.
Run with the game/editor closed. --assets DIR --units DIR --stage DIR --backup DIR.
Refuses existing new IDs; snapshots edited text and records installed hashes.
"""
import argparse, hashlib, json, re, shutil
from pathlib import Path
p=argparse.ArgumentParser()
for k in ('assets','units','stage','backup'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args()
names={ 'JAZZ_ConradBody':'CharacterBodyMale','JAZZ_ConradPants':'CharacterPantsMale','JAZZ_ConradHead':'CharacterHeadMale'}
a.backup.mkdir(parents=True,exist_ok=True)
def read(path):return path.read_bytes().decode('utf-8')
def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(text.encode('utf-8'))
items=a.assets/'items.lua';meta=a.assets/'metadata.lua';units=a.units/'items.lua'
old={items:read(items),meta:read(meta),units:read(units)}
assert all(n not in old[items] and n not in old[meta] for n in names),'Already registered'
u=old[units];match=re.search(r'\bid\s*=\s*"Conrad"',u);assert match
start=u.rfind("PlaceObj('ModItemAppearancePreset', {",0,match.start())
end=u.index("}),",match.end())+3
block=u[start:end]
for field,value in {'Body':'JAZZ_ConradBody','Pants':'JAZZ_ConradPants','Head':'JAZZ_ConradHead','Hair':''}.items():
    block,n=re.subn(r'\b'+field+r'\s*=\s*"[^"]*"',field+' = "'+value+'"',block);assert n==1,(field,n)
for field in ('BodyColor','PantsColor','HeadColor'):
    block,n=re.subn(field+r" = PlaceObj\('ColorizationPropSet', \{.*?\}\),",field+" = PlaceObj('ColorizationPropSet', {}),",block,flags=re.S);assert n==1
for field in ('Armor','Shirt','Hat','Hat2','Chest','Hip'):
    if re.search(r'\b'+field+r'\s*=',block):block=re.sub(r'\b'+field+r'\s*=\s*"[^"]*"',field+' = ""',block)
    else:block=block.replace("PlaceObj('ModItemAppearancePreset', {","PlaceObj('ModItemAppearancePreset', {\n\t\t\t"+field+' = "",',1)
updated_units=u[:start]+block+u[end:]
tail=old[items].rstrip();idx=tail.rfind('}')
assert idx>=0 and tail[idx:]=='}' and tail.startswith('return {')
records=''.join("\nPlaceObj('ModItemEntity', { 'name', \""+n+"\", 'entity_name', \""+n+"\", 'class_parent', \""+c+"\", 'ClassParents', {} }),\n" for n,c in names.items())
updated_items=tail[:idx]+records+tail[idx:]+'\n'
updated_meta=old[meta]
for field,entries in [('entities',list(names)),('code',['Entities/'+n+'.lua' for n in names])]:
    pattern=r"('"+field+r"'\s*,\s*\{)"
    updated_meta,count=re.subn(pattern,lambda m:m.group(0)+''.join('\n\t\t"'+n+'",' for n in entries),updated_meta,count=1)
    assert count==1,field
for source,text in old.items():
    prefix='assets' if source.parent==a.assets else 'units'
    dest=a.backup/(prefix+'-'+source.name)
    assert not dest.exists(),dest
    dest.write_bytes(text.encode('utf8'))
write(a.backup/'Conrad-before.lua',u[start:end])
# Validate complete staged dependency graph before mutating active paths.
files=list(a.stage.rglob('*'));files=[f for f in files if f.is_file()]
assert len(files)>=15
for f in files:
    rel=f.relative_to(a.stage);assert 'JAZZ_Conrad' in f.name
    assert not (a.assets/'Entities'/rel).exists(),rel
for n,c in names.items():
    write(a.stage/(n+'.lua'),'EntityData["'+n+'"] = { editor_artset = "Mods", entity = { class_parent = "'+c+'" } }\n')
manifest=[]
for f in files:
    dest=a.assets/'Entities'/f.relative_to(a.stage)
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
    manifest.append({'path':dest.relative_to(a.assets).as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
write(items,updated_items);write(meta,updated_meta);write(units,updated_units)
(a.backup/'install-manifest.json').write_text(json.dumps(manifest,indent=2))
print('Installed',len(files),'files; registered',list(names),'; existing Conrad appearance updated.')
