"""Read an already running JA3Debug UI over DAP, without initialize or pause.

Does not launch the game, change inventory, reload mods, or clear breakpoints.
Long reports are written by the engine to AppData/jazz_inventory_hang.txt.
Use --self-test for the offline Lua and DAP framing check.
"""
import argparse
import json
import socket
import time
from pathlib import Path

EXPRESSION = r'''(function()
 if type(SafeEvalStart) ~= "function" or type(SafeEvalEnd) ~= "function" then
  return "BLOCKED: SafeEval unavailable; no state inspected"
 end
 local ign = SafeEvalStart("inventory-hang-probe")
 local ok, result = pcall(function()
  local lines = {}
  local function line(k,v) lines[#lines+1] = k .. "=" .. tostring(v) end
  line("sector",gv_CurrentSectorId)
  line("satellite",gv_SatelliteView)
  line("combat",not not g_Combat)
  line("selected",SelectedObj and SelectedObj.session_id)
  local function inspect(name,dlg)
   line(name,dlg and dlg.class or "absent")
   if not dlg then return end
   line(name..".state",dlg.window_state)
   line(name..".mode",dlg.Mode)
   local count=0
   for reason in pairs(dlg.open_reasons or empty_table) do
    count=count+1; if count>20 then break end
    line(name..".reason",reason)
   end
   count=0
   for key,thread in pairs(dlg.threads or empty_table) do
    count=count+1; if count>20 then break end
    line(name..".thread."..tostring(key),IsValidThread(thread) and GetThreadStatus(thread) or "inactive")
   end
  end
  inspect("loading",GetLoadingScreenDialog())
  local full=GetDialog("FullscreenGameDialogs")
  inspect("fullscreen",full)
  local visited=0
  local function walk(win,depth)
   if type(win)~="table" or depth>12 or visited>=300 then return end
   visited=visited+1
   local context=rawget(win,"context")
   if type(context)=="table" and context.class and context.id then
    line("item",context.class..":"..tostring(context.id))
   end
   for _,child in ipairs(win) do walk(child,depth+1) end
  end
  walk(full,0)
  line("ui_nodes_inspected",visited)
  return table.concat(lines,"\n")
 end)
 SafeEvalEnd(ign,"inventory-hang-probe")
 if not ok then return "LUA ERROR: "..tostring(result) end
 if #result<=400 then return result end
 local err=AsyncStringToFile("AppData/jazz_inventory_hang.txt",result)
 return err and ("FILE ERROR: "..tostring(err)) or "@@FILE@@ AppData/jazz_inventory_hang.txt"
end)()'''


def read_response(sock, deadline):
    buffer = b''

    def receive():
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('DAP response deadline expired')
        sock.settimeout(remaining)
        data = sock.recv(65536)
        if not data:
            raise ConnectionError('DAP peer closed before response')
        return data

    while True:
        while b'\r\n\r\n' not in buffer:
            buffer += receive()
        header, buffer = buffer.split(b'\r\n\r\n', 1)
        length = int(next(line.split(b':', 1)[1] for line in header.split(b'\r\n')
                          if line.lower().startswith(b'content-length:')))
        if not 0 <= length <= 4 * 1024 * 1024:
            raise ValueError('Unexpected DAP response size')
        while len(buffer) < length:
            buffer += receive()
        message = json.loads(buffer[:length])
        buffer = buffer[length:]
        if message.get('type') == 'response' and message.get('request_seq') == 1:
            return message


def self_test():
    from lupa import LuaRuntime
    lua = LuaRuntime()
    lua.execute('''
    empty_table={};gv_CurrentSectorId='K4';gv_SatelliteView=false;g_Combat=false
    function SafeEvalStart() entered=true;return 42 end
    function SafeEvalEnd(v) assert(v==42);exited=true end
    function GetLoadingScreenDialog() return {class='XLoadingScreen',open_reasons={inventory=true}} end
    function GetDialog() return {class='XDialog',Mode='inventory'} end
    ''')
    result = lua.eval(EXPRESSION)
    assert 'loading.reason=inventory' in result and 'fullscreen.mode=inventory' in result
    assert lua.eval('entered and exited')
    lua.execute('function GetDialog() error("fixture failure") end;exited=false')
    assert 'LUA ERROR:' in lua.eval(EXPRESSION) and lua.eval('exited')
    left, right = socket.socketpair()
    with left, right:
        message = json.dumps(dict(type='response', request_seq=1, success=True)).encode()
        right.sendall(f'Content-Length: {len(message)}\r\n\r\n'.encode()+message)
        assert read_response(left, time.monotonic()+1)['success']
    left, right = socket.socketpair()
    with left:
        right.close()
        try:
            read_response(left, time.monotonic()+1)
        except ConnectionError:
            pass
        else:
            raise AssertionError('EOF was not detected')
    print('PASS: Lua snapshot, SafeEval restoration, DAP response and EOF handling; no game launched')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--output',type=Path,default=Path('.tmp/bug-triage/inventory-hang/dap-response.json'))
    args=parser.parse_args()
    if args.self_test:
        return self_test()
    message=json.dumps(dict(seq=1,type='request',command='evaluate',arguments={
        'expression':EXPRESSION,'context':'repl'})).encode()
    with socket.create_connection(('127.0.0.1',8165),timeout=8) as sock:
        sock.sendall(f'Content-Length: {len(message)}\r\n\r\n'.encode()+message)
        response=read_response(sock,time.monotonic()+8)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(response,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(response,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
