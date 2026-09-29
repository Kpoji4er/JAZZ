"""Back up Lua sources, dispatch the official two-callback UI editor transaction.

The backup is a review baseline, not an automatic rollback. No camera batch may
be running. The active mod must already have current items loaded from disk.
"""
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path
from install_layers import lua
from live import evaluate,quote

p=argparse.ArgumentParser(__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--backup',type=Path,required=True);p.add_argument('--version',type=int,required=True);p.add_argument('--bullet',required=True);p.add_argument('--captures',type=Path,nargs='+',required=True);a=p.parse_args()
for directory in a.captures:
    receipt=json.loads((directory/'capture-report.json').read_text(encoding='utf-8'))
    assert receipt['phase']=='done' and receipt['disposed'],'Camera capture must finish first'
assert not a.backup.exists(),'Use a new immutable baseline directory'
a.backup.mkdir(parents=True)
paths=subprocess.check_output(['git','-C',str(a.repo),'ls-files','-z']).decode().split('\0')
hashes={}
for name in paths:
    if not name.endswith('.lua'):continue
    source=a.repo/name
    if not source.is_file():continue
    target=a.backup/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    hashes[name]=hashlib.sha256(source.read_bytes()).hexdigest()
(a.backup/'manifest.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
source=Path(__file__).with_suffix('.py').with_name('edit_template_bindings.lua').read_text(encoding='utf-8')
settings=lua({'version':a.version,'bullet':a.bullet})
receipt=(a.backup/'editor-result.json').resolve().as_posix()
body='''CreateRealTimeThread(function()
  local ign=SafeEvalStart("JAZZ native layer editor transaction")
  local ok,result=pcall(function() local fn=assert(load(%s,"JAZZ template editor","t",_G))();return fn(%s) end)
  SafeEvalEnd(ign,"JAZZ native layer editor transaction")
  local err,text=LuaToJSON({ok=ok,result=result})
  AsyncStringToFile(%s,text or tostring(err))
end);return "editor transaction scheduled"
'''%(quote(source),settings,quote(receipt))
evaluate(body,a.backup/'dispatch.json')
