"""Bounded live-eval DAP, no initialize/pause/reload. Source supplied as a Lua body.

python .../live.py --body probe.lua --output response.json [--schedule]
Scheduled body runs in game thread; outcome written to <output>.result.txt.
"""
import argparse
import json
import socket
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _probe_inventory_hang import read_response


def quote(s):
    level = '='
    while ']' + level + ']' in s:
        level += '='
    return '[' + level + '[' + s + ']' + level + ']'


def evaluate(body, output, schedule=False):
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    result_path = output.with_suffix('.result.txt').as_posix()
    run = 'local fn,err=load(' + quote(body) + ',"weapon-capture","t",_G); if not fn then return "COMPILE ERROR: "..tostring(err) end; return fn()'
    if schedule:
        run = '''CreateGameTimeThread(function()
          local ign=SafeEvalStart("weapon-capture")
          local ok,res=pcall(function() %s end)
          SafeEvalEnd(ign,"weapon-capture")
          AsyncStringToFile(%s,(ok and "OK\n" or "ERROR\n")..tostring(res))
        end); return "scheduled"''' % (run, quote(result_path))
        run = run.replace('"OK\n"', '"OK\\n"').replace('"ERROR\n"', '"ERROR\\n"')
    expression = '''(function()
      if type(SafeEvalStart)~="function" then return "BLOCKED: SafeEval missing" end
      local ign=SafeEvalStart("weapon-capture-dispatch")
      local ok,res=pcall(function() %s end)
      SafeEvalEnd(ign,"weapon-capture-dispatch")
      local text=(ok and "OK: " or "ERROR: ")..tostring(res)
      if #text>380 then local err=AsyncStringToFile(%s,text);return err or "result-file" end
      return text
    end)()''' % (run, quote(result_path))
    request = json.dumps(dict(seq=1, type='request', command='evaluate', arguments={
        'expression': expression, 'context': 'repl'})).encode()
    with socket.create_connection(('127.0.0.1', 8165), timeout=12) as sock:
        sock.sendall(f'Content-Length: {len(request)}\r\n\r\n'.encode() + request)
        response = read_response(sock, time.monotonic() + 12)
    output.write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding='utf-8')
    if not schedule:
        result=response.get('body',{}).get('result','')
        if result and not result.startswith('result-file'):
            Path(result_path).write_text(result,encoding='utf-8')
    print(json.dumps(response, ensure_ascii=False))
    return response


if __name__ == '__main__':
    p=argparse.ArgumentParser(__doc__)
    p.add_argument('--body',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--schedule',action='store_true')
    a=p.parse_args()
    evaluate(a.body.read_text(encoding='utf-8'),a.output,a.schedule)
