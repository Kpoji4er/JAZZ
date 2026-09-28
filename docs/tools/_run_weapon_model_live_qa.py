"""Run scoped weapon model QA in an existing JA3Debug ModEditor session.
No initialize/pause/reload. scan writes a TSV; other operations affect only the
separate runtime QA unit. Model assets and campaign files are never written.
"""
import argparse,json,socket,time
from pathlib import Path
from _probe_inventory_hang import read_response
p=argparse.ArgumentParser()
p.add_argument('operation',choices=['scan','pairs','equip','armor','component','pose','turn','view','inspect','finish'])
p.add_argument('item',nargs='?',default='')
p.add_argument('slot',nargs='?',default='')
p.add_argument('component',nargs='?',default='')
a=p.parse_args()
script=Path(__file__).with_name('_weapon_model_live_qa.lua').read_text(encoding='utf-8')
args=','.join(json.dumps(x) for x in [a.operation,a.item,a.slot,a.component])
expr="""(function()
 if not Platform.debug or type(SafeEvalStart)~='function' then return 'BLOCKED debug/SafeEval' end
 if GetMapName()~='ModEditor' then return 'BLOCKED map' end
 CreateGameTimeThread(function()
  local ign=SafeEvalStart('weapon-model-qa')
  local ok,res=pcall(function() return assert(load(SCRIPT))()(ARGS) end)
  SafeEvalEnd(ign,'weapon-model-qa')
  AsyncStringToFile('AppData/jazz_weapon_model_qa.txt',tostring(ok)..'\\n'..tostring(res))
 end)
 return 'scheduled'
end)()""".replace('SCRIPT',json.dumps(script)).replace('ARGS',args)
result_path=Path.home()/'AppData/Roaming/Jagged Alliance 3/jazz_weapon_model_qa.txt'
before=result_path.stat().st_mtime_ns if result_path.exists() else 0
with socket.create_connection(('127.0.0.1',8165),timeout=8) as s:
 data=json.dumps({'seq':1,'type':'request','command':'evaluate','arguments':{'expression':expr,'context':'repl'}}).encode()
 s.sendall(('Content-Length: %d\r\n\r\n'%len(data)).encode()+data)
 response=read_response(s,time.monotonic()+8)
 if 'scheduled' not in str(response):raise RuntimeError(response)
 deadline=time.monotonic()+45
 while time.monotonic()<deadline:
  if result_path.exists() and result_path.stat().st_mtime_ns!=before:
   text=result_path.read_text(encoding='utf-8');print(text);raise SystemExit(0 if text.startswith('true') else 1)
  time.sleep(.15)
 raise TimeoutError('Game-time QA did not finish; do not retry blindly')
