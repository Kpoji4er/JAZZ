"""Offline cuirass QA-pass: build, pose regression, bake, compile, stage, validate.
No game launch, DAP, resource hot reload, metadata generation or publication.
--install-existing copies ONLY this already registered cuirass after all gates.
"""
import argparse,datetime,hashlib,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];TOOLS=ROOT/'docs/tools'
p=argparse.ArgumentParser()
for name in ('blender','game-root','output','export-root'):p.add_argument('--'+name,type=Path,required=True)
p.add_argument('--install-existing',action='store_true')
a=p.parse_args();out=a.output.resolve()
# Each pass owns a fresh directory, preventing stale successful reports/backups.
out.mkdir(parents=True,exist_ok=False)
logs=out/'logs';logs.mkdir();source=out/'source';build=out/'build';pose=out/'poses'
report={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'RUNNING','runtime':'NOT_RUN','stages':[],'installed':False,'item':'JazzArmor_ImprovisedCuirass','unit':'JAZZ_Legion_ArmorTest','other_families':'source-only; not installed'}
def save(): (out/'qa-report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
def run(label,cmd):
 print(label,flush=True);start=time.time();log=logs/(label+'.log')
 with log.open('w',encoding='utf8') as stream:result=subprocess.run([str(x) for x in cmd],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
 report['stages'].append({'stage':label,'exit_code':result.returncode,'seconds':round(time.time()-start,2),'log':str(log)})
 save()
 if result.returncode:raise RuntimeError(label+' failed; see '+str(log))
def blender(script,*args):return [a.blender,'-b','--factory-startup','--threads','6','--python-exit-code','1','--python',TOOLS/script,'--',*args]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
save();lock=a.export_root/'.qa-legion-armor.lock';locked=False
try:
 a.export_root.mkdir(parents=True,exist_ok=True)
 with lock.open('x') as f:f.write(str(os.getpid()))
 locked=True
 run('00-jazz-preset-roster',[sys.executable,TOOLS/'_audit_legion_armor_presets.py','--game-root',a.game_root,'--output',out/'jazz-appearance-qa.json'])
 sample=a.game_root/'ModTools/Samples/Assets/SampleMaleModel/BlenderScene_Appearance.blend'
 run('01-model',blender('_model_legion_armor.py','--sample',sample,'--output',source,'--skip-previews'))
 blend=source/'improvised_cuirass_v7.blend'
 run('02-pose-regression',blender('_preview_legion_armor_pose.py','--source',blend,'--output',pose))
 report['pose_results']=json.loads((pose/'pose-check.json').read_text())
 run('03-bake-export',blender('_build_legion_armor.py','--source',blend,'--output',build,'--game-root',a.game_root))
 compile_start=time.time()
 run('04-compile',[a.game_root/'ModTools/AssetsProcessor/AssetsProcessor.exe',build/'JAZZ_ImprovisedCuirass_Male.fbx','-globalappdirs','-gamepath',a.game_root])
 entity=a.export_root/'JAZZ_ImprovisedCuirass_Male.ent'
 assert entity.is_file() and entity.stat().st_mtime>=compile_start-2,'Missing or stale compiled entity'
 run('05-stage',[sys.executable,TOOLS/'_prepare_rifle_assets.py','--build',build,'--prefix','JAZZ_ImprovisedCuirass','--entities','JAZZ_ImprovisedCuirass_Male','--export-root',a.export_root,'--game-root',a.game_root])
 stage=build/'mod-assets-stage/Entities';icon=build/'ImprovisedCuirass.png'
 run('06-staged-graph',[sys.executable,TOOLS/'_check_legion_armor.py','--resources',stage,'--icon',icon])
 files=[f for f in stage.rglob('*') if f.is_file() and f.suffix!='.lua']
 assert len(files)==9,(len(files),'unexpected resource count')
 report['sha256']={str(f.relative_to(stage)):digest(f) for f in files};report['icon_sha256']=digest(icon)
 if a.install_existing:
  # Preflight every destination before any copy. Existing helper keeps backups.
  assert all((ROOT.parent/'jazz_assets/Entities'/f.relative_to(stage)).is_file() for f in files)
  run('07-install-existing',[sys.executable,TOOLS/'_refresh_legion_armor.py','--build',build,'--assets',ROOT.parent/'jazz_assets','--core',ROOT,'--mount','Mod/pDGDhr/'])
  run('08-installed-graph',[sys.executable,TOOLS/'_check_legion_armor.py'])
  for f in files:assert digest(ROOT.parent/'jazz_assets/Entities'/f.relative_to(stage))==digest(f)
  assert digest(ROOT/'ArmorIcons/ImprovisedCuirass.png')==digest(icon)
  report['installed']=True
 report['status']='PASS_OFFLINE';save()
 (out/'game-acceptance.md').write_text('''# Ручная приёмка в JA3\n\nГотова к проверке только кираса, `JAZZ_Legion_ArmorTest`. Остальные семейства не установлены.\n\n- Спавн: `CheatSpawnEnemy("JAZZ_Legion_ArmorTest")`; кираса в Torso, MP40 и боезапас.\n- Стоя, присев, лёжа, прицеливание, бег, поворот и наклон: низ спины без зубцов, ремни соединены, наплечник не висит.\n- Осмотреть спереди/сзади: сварной металл, толщина, швы, нормали, тени; сверить иконку.\n- Снять/надеть, переместить в Inventory; исходная Armor восстанавливается без дубликатов.\n- Сохранение/загрузка и смена appearance; другие Legion body проверять отдельно.\n- Мерки/vanilla Legion/AME не получают этот визуал.\n\nCPU-позы не доказывают отсутствие пересечений во всех игровых анимациях.\n''',encoding='utf8')
 print('PASS_OFFLINE',out,flush=True)
except Exception as exc:
 report['status']='FAIL';report['error']=str(exc);save();raise
finally:
 if locked:lock.unlink()
