"""Replace only installed cuirass resources, retain backups and emit live reload Lua.
python docs/tools/_refresh_legion_armor.py --build <build> --assets <jazz_assets>
  --core <jazz> --mount <runtime Mod/id/ path from Mods>
Does not execute Lua or touch editor-generated metadata.
"""
import argparse,json,shutil
from pathlib import Path
p=argparse.ArgumentParser()
for name in ('build','assets','core'):p.add_argument('--'+name,type=Path,required=True)
p.add_argument('--mount',required=True)
a=p.parse_args();stage=a.build/'mod-assets-stage/Entities';dst=a.assets.resolve()/'Entities'
backup=a.build/'live-backup';backup.mkdir(exist_ok=True);resources=[]
for src in stage.rglob('*'):
    if not src.is_file() or src.suffix=='.lua':continue
    rel=src.relative_to(stage);target=dst/rel
    assert 'JAZZ_ImprovisedCuirass' in src.name and target.is_file(),target
    old=backup/'Entities'/rel;old.parent.mkdir(parents=True,exist_ok=True)
    if not old.exists():shutil.copy2(target,old)
    shutil.copy2(src,target);resources.append(a.mount.rstrip('/')+'/Entities/'+rel.as_posix())
icon=a.core/'ArmorIcons/ImprovisedCuirass.png';old=backup/'ImprovisedCuirass.png'
if not old.exists():shutil.copy2(icon,old)
shutil.copy2(a.build/'ImprovisedCuirass.png',icon)
lua='CreateGameTimeThread(function()\n'
for r in resources:lua+='ReloadEntityResource('+json.dumps(r)+', "modified")\n'
lua+='end)\nreturn "Armor resource reload queued"\n'
(a.build/'reload.lua').write_text(lua,encoding='utf-8')
print('Replaced',len(resources),'resources plus icon; backup:',backup)
