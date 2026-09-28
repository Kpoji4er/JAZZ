"""Stage follow-up attachment fixes; never writes installed resources.
--build DIR. Outputs stage plus a before/after hash manifest for review.
"""
import argparse,json,re,hashlib
from pathlib import Path
import xml.etree.ElementTree as ET
from _integrate_m14_family import matching
from _integrate_sr3m import add_metadata,append_root_item
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);a=p.parse_args()
root=Path(__file__).resolve().parents[2];suite=root.parent;stage=a.build/'stage';outputs={}
def read(rel):return (suite/rel).read_text(encoding='utf-8-sig')
def put(rel,s):
 old=(suite/rel).read_bytes() if (suite/rel).exists() else b''
 if isinstance(s,str):s=(b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\r\n','\n').replace('\n','\r\n' if b'\r\n' in old else '\n').encode('utf-8')
 outputs[rel]=s
s=read('jazz/items.lua');count=s.count('Slot = "OpticsMount"');assert count==21,count
s=s.replace('Slot = "OpticsMount"','Slot = "Opticsmount"')
# A fixed handguard owns the FAL rail; changing Scope no longer removes it.
removed=0
for m in reversed(list(re.finditer(r"PlaceObj\('ModItemWeaponComponent'",s))):
 end=matching(s,s.index('(',m.start()));block=s[m.start():end]
 if 'ApplyTo = "JAZZ_FNFAL_Tactical"' not in block:continue
 if 'id = "JAZZ_FNFAL_TacHandguard"' in block:
  extra='\nPlaceObj(\'WeaponComponentVisual\', { ApplyTo = "JAZZ_FNFAL_Tactical", Entity = "WeaponAttA_MountFNFal_01", Slot = "Mount1", param_bindings = false }),'
  block,n=re.subn(r'Visuals\s*=\s*\{',lambda m:m[0]+extra,block,count=1);assert n==1
 else:
  for v in reversed(list(re.finditer(r"PlaceObj\('WeaponComponentVisual'",block))):
   ve=matching(block,block.index('(',v.start()));visual=block[v.start():ve]
   if 'ApplyTo = "JAZZ_FNFAL_Tactical"' in visual and 'Slot = "Mount1"' in visual:
    assert 'Entity = "WeaponAttA_MountFNFal_01"' in visual
    if block[ve:ve+1]==',':ve+=1
    block=block[:v.start()]+block[ve:];removed+=1
 s=s[:m.start()]+block+s[end:]
assert removed==13,removed
# Vanilla removes matching entities even from other weapons' scope visuals.
# Rebuild the fixed rail after Scope, so that removal cannot leave it absent.
def rail_owner_last(block):
 slots=list(re.finditer(r"PlaceObj\('WeaponComponentSlot'",block))
 matches=[]
 for m in slots:
  end=matching(block,block.index('(',m.start()))
  if 'JAZZ_FNFAL_TacHandguard' in block[m.start():end]:matches.append((m.start(),end))
 assert len(matches)==1
 start,end=matches[0];part=block[start:end]
 if block[end:end+1]==',':end+=1
 block=block[:start]+block[end:]
 last=list(re.finditer(r"PlaceObj\('WeaponComponentSlot'",block))[-1]
 at=matching(block,block.index('(',last.start()))
 assert block[at:at+1]==','
 return block[:at+1]+'\n'+part+','+block[at+1:]
# Find the definition by its id, not one of its component ApplyTo references.
for m in re.finditer(r"PlaceObj\('ModItemInventoryItemCompositeDef'",s):
 end=matching(s,s.index('(',m.start()));block=s[m.start():end]
 if re.search(r"(?:'Id',\s*|id\s*=\s*)\"JAZZ_FNFAL_Tactical\"",block):
  s=s[:m.start()]+rail_owner_last(block)+s[end:];break
else:raise AssertionError('FAL item missing')
put('jazz/InventoryItem/JAZZ_FNFAL_Tactical.lua',rail_owner_last(read('jazz/InventoryItem/JAZZ_FNFAL_Tactical.lua')))
put('jazz/items.lua',s)
carry=a.build/'components/JAZZ_CarryHandle_AR15.png'
if carry.exists():
 s=outputs['jazz/items.lua'].decode('utf-8-sig').replace('\r\n','\n')
 at=s.index('id = "JAZZ_CarryHandle_AR15"');start=s.rfind("PlaceObj('ModItemWeaponComponent'",0,at);end=matching(s,s.index('(',start));block=s[start:end]
 icon='Mod/e6L4ECj/WeaponComponents/Optics/JAZZ_CarryHandle_AR15.png'
 block,n=re.subn(r'\bIcon = "[^"]*"',lambda m:'Icon = "'+icon+'"',block,count=1)
 if n==0:block=block.replace("PlaceObj('ModItemWeaponComponent', {","PlaceObj('ModItemWeaponComponent', {\nIcon = \""+icon+'\",',1)
 put('jazz/items.lua',s[:start]+block+s[end:]);put('jazz/WeaponComponents/Optics/JAZZ_CarryHandle_AR15.png',carry.read_bytes())
# Same item and existing translated component titles; no item replacement.
rel='jazz/Code/Weapon_MosinModular.lua';code=read(rel)
anchor='local function configuration(weapon)'
helper='''local function update_configuration_name(weapon)
    local id = weapon.components and weapon.components.Barrel
    local component = id and WeaponComponents[id]
    local standard = not id or id == "JAZZ_Mosin1891"
    weapon.DisplayName = standard and Mosin.DisplayName or (component and component.DisplayName or Mosin.DisplayName)
    weapon.DisplayNamePlural = standard and Mosin.DisplayNamePlural or weapon.DisplayName
end

'''
assert code.count(anchor)==1;code=code.replace(anchor,helper+anchor)
code=code.replace('    local current = configuration(self)','    update_configuration_name(self)\n    local current = configuration(self)')
put(rel,code)
# Side attachments use the upper rail and its normal (no quarter turn).
for entity,position in [('M4R_M4A1','27.000,0.000,12.000'),('M16R_M16A4','43.316,0.000,10.310')]:
 rel='jazz_assets/Entities/'+entity+'.ent';s=read(rel)
 s,n=re.subn(r'<attach name="Side"[^>]*/>',f'<attach name="Side" spot_pos="{position}" spot_rot="0.000000,0.000000,1.000000,0.0000" />',s);assert n==1
 if entity=='M4R_M4A1':
  s,n=re.subn(r'(<attach name="Under" spot_pos=")[^"]+',r'\g<1>34.450,0.000,5.267',s);assert n==1
 put(rel,s)
rel='jazz_assets/Entities/JAZZ_M14.ent';s=read(rel);assert s.count('name="OpticsMount"')==1
put(rel,s.replace('name="OpticsMount"','name="Opticsmount"'))
# A dedicated MkIII scope visual retains the current component's gameplay.
name='JAZZ_M14_MkIII_Scope';compiled=a.build/'ExportedEntities'/(name+'.ent')
if compiled.exists():
 s=outputs['jazz/items.lua'].decode('utf-8-sig').replace('\r\n','\n')
 at=s.index('id = "JAZZ_Scope_12x"');start=s.rfind("PlaceObj('ModItemWeaponComponent'",0,at);end=matching(s,s.index('(',start));block=s[start:end]
 pattern=r'(ApplyTo = "JAZZ_M14_MkIII",\s*Entity = ")[^"]+("[,]\s*Slot = "Scope")'
 block,n=re.subn(pattern,lambda m:m[1]+name+m[2],block);assert n<=1,n
 if n==0:
  extra=f'\nPlaceObj(\'WeaponComponentVisual\', {{ ApplyTo = "JAZZ_M14_MkIII", Entity = "{name}", Slot = "Scope", param_bindings = false }}),'
  block,n=re.subn(r'Visuals\s*=\s*\{',lambda m:m[0]+extra,block,count=1);assert n==1
 put('jazz/items.lua',s[:start]+block+s[end:])
 tree=ET.parse(compiled);entity=tree.getroot();entity.set('path','');entity.set('name',name)
 for parent in entity.iter():
  for child in list(parent):
   if child.tag in ('src','attach'):parent.remove(child)
 for node in entity.findall('.//material'):node.set('file','Materials/JAZZ_M14_MkIII_Mesh.mtl')
 put('jazz_assets/Entities/'+name+'.ent',ET.tostring(entity,encoding='utf-8',xml_declaration=True))
 put('jazz_assets/Entities/'+name+'.lua','EntityData["'+name+'"] = { editor_artset = "Mods" }\n')
 s=read('jazz_assets/items.lua');assert name not in s
 s=append_root_item(s,f'PlaceObj(\'ModItemEntity\', {{\n\t\'name\', "{name}",\n\t\'ClassParents\', {{}},\n\t\'entity_name\', "{name}",\n}}),');put('jazz_assets/items.lua',s)
 s=read('jazz_assets/metadata.lua');s=add_metadata(s,'entities',['"'+name+'"']);s=add_metadata(s,'code',['"Entities/'+name+'.lua"']);put('jazz_assets/metadata.lua',s)
 reports=json.loads((a.build/'compiled-report.json').read_text())
 for r in reports:
  assert r['pass'];n=r['entity'];assert n in ('AKR_AK103_Magazine','M16R_M16A4_HandguardRIS',name),n
  put('jazz_assets/Entities/Meshes/'+n+'_Mesh.m.hgm',(a.build/'ExportedEntities/Meshes'/(n+'_Mesh.m.hgm')).read_bytes())
  if n=='M16R_M16A4_HandguardRIS':
   rel='jazz_assets/Entities/'+n+'.ent';old=read(rel);fresh=(a.build/'ExportedEntities'/(n+'.ent')).read_text()
   for tag in ('box','bsphere'):
    replacement=re.search(r'<'+tag+r'\b[^>]*/>',fresh)[0];old=re.sub(r'<'+tag+r'\b[^>]*/>',lambda m:replacement,old)
   put(rel,old)
 for sub in ('','Fallbacks/'):
  texture=a.build/'mag-normal'/sub/'AKR_AK103_6_Norm.dds'
  if texture.exists():put('jazz_assets/Entities/Textures/'+sub+texture.name,texture.read_bytes())
for icon in (a.build/'icons').glob('*.png'):
 if icon.stem.endswith('-review'):continue
 assert icon.stem in ('M4A1','M16A4','AK103','M14','M21','MK14EBR','VZ58','VektorR4','JAZZ_M14_MkIII'),icon
 put('jazz/WeaponIcons/'+icon.name,icon.read_bytes())
# Only the visually checked chainmail candidate is accepted here. HAV/6B3
# experiments remain outside the transaction until their actual defect is fixed.
chain=a.build/'armor/JAZZ_Chainmail_Male/compiled-audit.json'
if chain.exists():
 assert json.loads(chain.read_text())['pass']
 assert json.loads((chain.parent/'repair.json').read_text())['bottom_after']==1.055
 put('jazz_assets/Entities/Meshes/JAZZ_Chainmail_Male_mesh.m.hgm',(a.build/'ExportedEntities/Meshes/JAZZ_Chainmail_Male_mesh.m.hgm').read_bytes())
manifest={}
for rel,data in outputs.items():
 dest=stage/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 manifest[rel]={'before':hashlib.sha256((suite/rel).read_bytes()).hexdigest() if (suite/rel).exists() else None,'after':hashlib.sha256(data).hexdigest()}
(a.build/'data-manifest.json').write_text(json.dumps(manifest,indent=2))
print('STAGED',len(outputs),'files; FAL scope mounts removed:',removed)
