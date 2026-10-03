"""Run the explicitly approved 2026-10-02 torso batch through Meshy CLI 0.4.0.

No automatic paid retries. Each submission is journalled before project setup.
Usage: python docs/tools/meshy_armor_batch.py prepare|submit|wait|download [--name NAME]
"""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'meshy_output/armor-batch-20261002'
RUNNER = ['pnpm.cmd', 'dlx', 'npm@11.6.2', 'exec', '--yes', '--package=meshy-cli@0.4.0', '--', 'meshy']
FLAGS = ['--output-schema', 'v1', '--format', 'json', '--no-update-check']
NAMES = ['ImprovisedCuirass', 'Chainmail', 'TireBrigantine', 'TireArmor', 'LeatherArmor']

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def cli(args, log):
    proc = subprocess.run(RUNNER + list(map(str,args)) + FLAGS, capture_output=True, text=True, encoding='utf-8')
    log.write_text(proc.stdout, encoding='utf-8')
    log.with_suffix('.stderr.txt').write_text(proc.stderr, encoding='utf-8')
    if proc.stdout:
        obj = json.loads(proc.stdout)
        task = (obj.get('result') or {}).get('task') or {}
        if task.get('status') in ['FAILED', 'CANCELED'] and args[1] == 'wait':
            return obj['result']
    if proc.returncode:
        raise RuntimeError(f'CLI exit {proc.returncode}; inspect {log}; do not repeat paid create blindly')
    obj = json.loads(proc.stdout)
    if not obj.get('ok'):
        raise RuntimeError(f'CLI did not confirm success: {log}')
    return obj['result']

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare','submit','wait','download'])
    parser.add_argument('--name', choices=NAMES)
    a=parser.parse_args()
    WORK.mkdir(parents=True,exist_ok=True)
    manifest=WORK/'batch.json'
    if a.action=='prepare':
        if manifest.exists():
            raise RuntimeError('Manifest already exists; preserve task history')
        refs=WORK/'references';refs.mkdir(exist_ok=True)
        jobs=[]
        for name in NAMES:
            source={'ImprovisedCuirass':'ArmorIcons/Raw/Cuirass Orig.png','TireArmor':'ArmorIcons/Raw/gachivest.png'}.get(name)
            out=refs/(name+'.png')
            if source:
                shutil.copyfile(ROOT/source,out)
                origin=source
            else:
                origin='ae4e775a:ArmorIcons/'+name+'.png'
                out.write_bytes(subprocess.check_output(['git','show',origin],cwd=ROOT))
            jobs.append(dict(name=name,reference=str(out),origin=origin,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),resource='image-to-3d'))
        save(WORK/'settings.json',dict(should_remesh=True,topology='triangle',target_polycount=15000,image_enhancement=False))
        save(manifest,dict(estimated_credits=150,balance_before=2970,jobs=jobs,reused_6b3=dict(resource='multi-image-to-3d',task_id='01a0f974-6ad9-7565-80ab-cd96f804dfe3',project=str(Path.home()/'.codex/artifacts/meshy-6b3-20261002/20261002_005244_6b3-multiview-lowpoly_01a0f974'))))
        print('Prepared 5 references and existing 6B3 lineage',flush=True)
        return
    data=json.loads(manifest.read_text(encoding='utf-8'))
    for job in data['jobs']:
        name=job['name']
        if name not in NAMES: continue
        if a.name and a.name!=name: continue
        logs=WORK/'logs'/name;logs.mkdir(parents=True,exist_ok=True)
        if a.action=='submit':
            if not job.get('task_id'):
                marker=logs/'submission-started.json'
                if marker.exists():
                    raise RuntimeError(f'{name}: ambiguous earlier submission; recover its ID before continuing')
                save(marker,dict(name=name,operation_id='jazz-armor-20261002-'+name.lower()))
                result=cli(['image-to-3d','create','--image-url',job['reference'],'--model-type','standard','--data','@'+str(WORK/'settings.json'),'--should-texture','true','--enable-pbr','true','--texture-resolution','2k','--target-formats','glb','--async','--operation-id','jazz-armor-20261002-'+name.lower(),'--workspace',WORK],logs/'create.json')
                job['task_id']=result['submission']['task_id'];save(manifest,data)
                print(name+' accepted '+job['task_id'],flush=True)
            if not job.get('project'):
                result=cli(['project','init','--root',WORK,'--name',name,'--task-id',job['task_id'],'--task-type',job['resource'],'--workspace',WORK],logs/'init.json')
                job['project']=result['project_dir'];save(manifest,data)
        elif a.action=='wait':
            if job.get('status') in ['SUCCEEDED','FAILED','CANCELED']: continue
            print('Waiting '+name+' '+job['task_id'],flush=True)
            result=cli([job['resource'],'wait',job['task_id'],'--timeout','600','--project',job['project'],'--stage','generation','--workspace',WORK],logs/'wait.json')
            task=result['task'];job['status']=task['status'];job['consumed_credits']=task.get('consumed_credits');save(manifest,data)
            print(name+' '+job['status']+' credits='+str(job['consumed_credits']),flush=True)
        elif a.action=='download':
            if job.get('status') != 'SUCCEEDED': continue
            project=Path(job['project']);snapshot=project/('task_'+job['task_id']+'.json')
            listing=cli(['download','--task-json',snapshot,'--list'],logs/'assets.json')
            print(name+' assets saved to '+str(logs/'assets.json'),flush=True)
            for option,value,filename in [('--model-format','glb',name+'.glb'),('--asset','thumbnail.primary','preview.png')]:
                if option == '--asset' and not any(x['key']==value for x in listing['assets']):
                    print(name+' has no thumbnail.primary',flush=True)
                    continue
                out=project/filename
                if out.exists(): continue
                cli(['download','--task-json',snapshot,option,value,'--output',out,'--project',project,'--stage','delivered' if filename.endswith('.glb') else 'preview','--workspace',WORK],logs/('download-'+filename+'.json'))
            job['model']=str(project/(name+'.glb'));job['preview']=str(project/'preview.png');save(manifest,data)
            print(name+' downloaded',flush=True)

if __name__=='__main__': main()
