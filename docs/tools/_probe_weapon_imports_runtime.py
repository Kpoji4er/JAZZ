"""Read loaded weapon versions via one DAP evaluate, without initialize/pause.

Requires a listening JA3Debug process. No game state or breakpoint changes.
"""
import json,socket
expression='''(function()
 local ign = SafeEvalStart("weapon-version-probe")
 local ok,res = pcall(function()
  return table.concat({
   "Mosin="..tostring(Mosin and Mosin.Entity),
   "test="..tostring(JAZZ_MosinModular and JAZZ_MosinModular.Entity),
   "AK74="..tostring(AK74 and AK74.Entity),
   "AK74M="..tostring(AK74M and AK74M.Entity),
   "AK105="..tostring(AK105 and AK105.Entity),
   "L42A1="..tostring(L42A1 and L42A1.Entity)
  },"; ")
 end)
 SafeEvalEnd(ign,"weapon-version-probe")
 return ok and res or tostring(res)
end)()'''
def evaluate(expression):
    message=json.dumps({'seq':1,'type':'request','command':'evaluate','arguments':{'expression':expression,'context':'repl'}}).encode()
    with socket.create_connection(('127.0.0.1',8165),timeout=8) as sock:
        sock.sendall(f'Content-Length: {len(message)}\r\n\r\n'.encode()+message)
        buffer=b''
        while True:
            while b'\r\n\r\n' not in buffer:buffer+=sock.recv(65536)
            head,buffer=buffer.split(b'\r\n\r\n',1)
            length=int(next(line.split(b':',1)[1] for line in head.split(b'\r\n') if line.lower().startswith(b'content-length:')))
            while len(buffer)<length:buffer+=sock.recv(65536)
            response=json.loads(buffer[:length]);buffer=buffer[length:]
            if response.get('type')=='response':return response

if __name__=="__main__":
    print(json.dumps(evaluate(expression),ensure_ascii=False,indent=2))
