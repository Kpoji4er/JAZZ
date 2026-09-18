"""Rebind existing fitted HAV sources, validate, render, bake/export and stage."""
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser()
for key in ('source-root','output','blender','game-root'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--only',nargs='+');a=p.parse_args();root=Path(__file__).resolve().parent;a.output.mkdir(parents=True,exist_ok=True)
rows=a.only or [f+v for f in ['Twaron','Guardian','Zylon'] for v in ['Light','Medium','Full']]
report={'status':'RUNNING','runtime':'NOT_RUN','models':[]}
pose_templates={}
def run(label,cmd,folder):
 print(folder.name,label,flush=True)
 with (folder/(label+'.log')).open('w',encoding='utf-8') as log:r=subprocess.run(list(map(str,cmd)),stdout=log,stderr=subprocess.STDOUT)
 if r.returncode:raise RuntimeError(str(folder/(label+'.log')))
try:
 for item in rows:
  folder=a.output/item;folder.mkdir(exist_ok=True);source=folder/'source';build=folder/'build';entity='JAZZ_'+item+'_Male'
  base=[a.blender,'-b','--factory-startup','--threads','4','--python-exit-code','1','--python']
  run('rebind',base+[root/'_rebind_heavy_armor.py','--','--source',a.source_root/item/'source/model.blend','--output',source],folder)
  variant=next(v for v in ('Light','Medium','Full') if item.endswith(v))
  manifest=json.loads((source/'model.json').read_text())
  signature=(manifest['geometry_sha256'],manifest['skin_sha256'])
  if variant not in pose_templates:
   run('poses',base+[root/'_check_soft_armor_poses.py','--','--source',source/'model.blend','--output',folder/'poses','--clothed'],folder)
   pose_templates[variant]=(signature,folder/'poses/pose-check.json')
  else:
   reference_signature,reference=pose_templates[variant]
   assert signature==reference_signature,'Geometry/skin differs between material families: '+item
   pose=json.loads(reference.read_text());assert pose['status']=='PASS_SKIN_STRUCTURE'
   pose['reused_from']=reference.relative_to(a.output).as_posix()
   pose['reuse_signature']={'geometry_sha256':signature[0],'skin_sha256':signature[1]}
   (folder/'poses').mkdir(exist_ok=True)
   (folder/'poses/pose-check.json').write_text(json.dumps(pose,indent=2))
   print(item,'poses reused from',pose['reused_from'],flush=True)
  run('bake',base+[root/'_build_legion_armor.py','--','--source',source/'model.blend','--output',build,'--game-root',a.game_root,'--entity',entity,'--mesh-prefix','TEST_'+item,'--icon',item],folder)
  run('processor',[a.game_root/'ModTools/AssetsProcessor/AssetsProcessor.exe',build/(entity+'.fbx'),'-globalappdirs','-gamepath',a.game_root],folder)
  export=next(v for v in [folder/'ExportedEntities',a.output/'ExportedEntities',a.output.parent/'ExportedEntities'] if (v/(entity+'.ent')).exists())
  run('stage',[sys.executable,root/'_prepare_rifle_assets.py','--build',build,'--prefix','JAZZ_'+item,'--entities',entity,'--export-root',export,'--game-root',a.game_root],folder)
  report['models'].append(item);(a.output/'qa-report.json').write_text(json.dumps(report,indent=2))
 report['status']='STAGED'
except Exception as exc:report['status']='FAILED';report['error']=str(exc);raise
finally:(a.output/'qa-report.json').write_text(json.dumps(report,indent=2))
