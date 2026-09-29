"""Run a finite native-capture dependency plan sequentially after a current batch.

Never overlaps camera jobs. Stops on failed cleanup, capture error, DAP failure,
or a stale receipt; a resumed run reuses completed matching batch plans.
"""
import argparse,json,subprocess,sys,time
from pathlib import Path

def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))

def wait(directory,starting=False):
    receipt=directory/'capture-report.json';started=time.monotonic()
    while True:
        try:r=read(receipt)
        except (FileNotFoundError,json.JSONDecodeError):r=None
        if r and r['phase']!='running':
            assert r['phase']=='done',str(directory)+': '+str(r.get('error'))
            assert not any(row['status']=='error' for row in r['rows']),str(directory)+': failed capture rows'
            assert r['original_camera']==r['restored_camera'] and r['restored_light'] and r['disposed'],str(directory)+': cleanup failed'
            assert r['original_render']==r['restored_render'] and r.get('inventory_pause_restored'),str(directory)+': render or pause not restored'
            return
        age=time.time()-receipt.stat().st_mtime if receipt.exists() else time.monotonic()-started
        assert age<300,str(directory)+': receipt stale; inspect game before resuming'
        time.sleep(2)

def main():
    p=argparse.ArgumentParser(__doc__);p.add_argument('--plan',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--after',type=Path);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    if a.after:
        print('Waiting for '+str(a.after),flush=True);wait(a.after)
    tasks=read(a.plan)['tasks']
    for index,task in enumerate(tasks):
        directory=a.output/(str(index+1).zfill(3)+'-'+task['weapon'])
        existing=directory/'capture-plan.json'
        if existing.exists():
            previous=read(existing)
            assert previous['ids']==[task['weapon']] and previous['prerequisites']==task['prerequisites'] and previous['variants']==task['variants'],'Changed capture plan: '+str(directory)
            if (directory/'capture-report.json').exists():wait(directory);continue
        print(str(index+1)+'/'+str(len(tasks))+' '+json.dumps(task),flush=True)
        command=[sys.executable,str(Path(__file__).with_name('dispatch_capture.py')),'--output',str(directory),'--ids',task['weapon'],'--layers','--matte','--resume-inventory-pause','--variants',*task['variants']]
        for slot,component in task['prerequisites'].items():command+=['--prerequisite',slot+'='+component]
        subprocess.run(command,check=True)
        wait(directory,True)
    (a.output/'complete.json').write_text(json.dumps({'status':'PASS','batches':len(tasks)}),encoding='utf-8')
    print('Dependency captures complete: '+str(len(tasks)),flush=True)

if __name__=='__main__':main()
