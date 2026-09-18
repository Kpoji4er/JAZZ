"""Sequential CPU build/stage for the three improvised Legion armor models."""
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser()
for name in ('blender','game-root','output','reference-shirt'):p.add_argument('--'+name,type=Path,required=True)
p.add_argument('--only',nargs='+',choices=['chainmail','brigantine','tire'])
a=p.parse_args();root=Path(__file__).resolve().parent;out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
sample=a.game_root/'ModTools/Samples/Assets/SampleMaleModel/BlenderScene_Appearance.blend'
rows=[('chainmail','Chainmail'),('brigantine','TireBrigantine'),('tire','TireArmor')]
if a.only:rows=[r for r in rows if r[0] in a.only]
report={'status':'RUNNING','runtime':'NOT_RUN','models':[]}
if a.only and (out/'qa-report.json').exists():
 report['models']=[r for r in json.loads((out/'qa-report.json').read_text())['models'] if r['kind'] not in a.only]
def run(label,args,folder):
    print('START',label,flush=True)
    with (folder/(label+'.log')).open('w',encoding='utf-8') as log:
        result=subprocess.run([str(x) for x in args],stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:raise RuntimeError(label+' failed; see '+str(folder/(label+'.log')))
    print('PASS',label,flush=True)
try:
 for kind,item in rows:
    folder=out/kind;folder.mkdir(exist_ok=True);source=folder/'source';build=folder/'build';entity='JAZZ_'+item+'_Male'
    base=[a.blender,'-b','--factory-startup','--threads','4','--python-exit-code','1','--python']
    run('model',base+[root/'_model_legion_soft_armor.py','--','--sample',sample,'--output',source,'--kind',kind,'--reference-shirt',a.reference_shirt],folder)
    run('pose-check',base+[root/'_check_soft_armor_poses.py','--','--source',source/(kind+'.blend'),'--output',folder/'poses'],folder)
    run('bake-export',base+[root/'_build_legion_armor.py','--','--source',source/(kind+'.blend'),'--output',build,'--game-root',a.game_root,'--entity',entity,'--mesh-prefix','TEST_'+kind,'--icon',item],folder)
    run('processor',[a.game_root/'ModTools/AssetsProcessor/AssetsProcessor.exe',build/(entity+'.fbx'),'-globalappdirs','-gamepath',a.game_root],folder)
    # AssetsProcessor exports beside the build's parent directory.
    candidates=[folder/'ExportedEntities',out/'ExportedEntities',out.parent/'ExportedEntities']
    export=next((v for v in candidates if (v/(entity+'.ent')).exists()),None)
    if export is None:raise RuntimeError('Missing fresh compiled entity '+entity)
    run('stage',[sys.executable,root/'_prepare_rifle_assets.py','--build',build,'--prefix','JAZZ_'+item,'--entities',entity,'--export-root',export,'--game-root',a.game_root],folder)
    report['models'].append({'kind':kind,'item':'JazzArmor_'+item,'entity':entity,'build':str(build),'status':'STAGED'})
    (out/'qa-report.json').write_text(json.dumps(report,indent=2))
 report['status']='STAGED; resource and pose checks pending'
except Exception as e:
 report['status']='FAILED';report['error']=str(e);raise
finally:(out/'qa-report.json').write_text(json.dumps(report,indent=2))
