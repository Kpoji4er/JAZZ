"""One-shot JA3 DAP live expression without initialize, breakpoints or pause.
Use --file <Lua statements> or --expr <expression>. Long results spill to AppData.
Mutation snippets must schedule their own GameTimeThread.
"""
import argparse,json,socket,os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--file',type=Path);p.add_argument('--expr');a=p.parse_args()
body=a.file.read_text(encoding='utf-8-sig') if a.file else 'return '+a.expr
expr='''(function()
local ign=IgnoreDebugErrors(true); SuspendDesyncErrors("armor-fit")
local ok,res=pcall(function() BODY end)
ResumeDesyncErrors("armor-fit"); IgnoreDebugErrors(ign)
if not ok then return "ERROR: "..tostring(res) end
res=tostring(res); if #res>380 then AsyncStringToFile("AppData/jazz_armor_eval.txt",res); return "@@ARMOR_FILE@@" end
return res end)()'''.replace('BODY',body)
with socket.create_connection(('127.0.0.1',8165),timeout=12) as s:
    req=json.dumps({'seq':1,'type':'request','command':'evaluate','arguments':{'expression':expr,'context':'repl'}}).encode()
    s.sendall(f'Content-Length: {len(req)}\r\n\r\n'.encode()+req);buf=b''
    while True:
        while b'\r\n\r\n' not in buf:buf+=s.recv(65536)
        h,data=buf.split(b'\r\n\r\n',1);n=int(next(x.split(b':')[1] for x in h.split(b'\r\n') if x.lower().startswith(b'content-length:')))
        while len(data)<n:data+=s.recv(65536)
        msg=json.loads(data[:n]);buf=data[n:]
        if msg.get('type')=='response' and msg.get('request_seq')==1:
            result=msg.get('body',{}).get('result',str(msg));print(result)
            if '@@ARMOR_FILE@@' in result:print((Path(os.environ['APPDATA'])/'Jagged Alliance 3/jazz_armor_eval.txt').read_text(encoding='utf-8-sig'))
            break
