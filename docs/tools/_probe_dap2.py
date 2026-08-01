# -*- coding: utf-8 -*-
"""Try alternate DAP framing against JA3 DebugAdapter."""
import socket
import time
import json

HOST, PORT = "127.0.0.1", 8165

def try_once(payload: bytes, label: str):
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect((HOST, PORT))
        s.sendall(payload)
        time.sleep(0.3)
        chunks = []
        try:
            while True:
                d = s.recv(4096)
                if not d:
                    break
                chunks.append(d)
                if len(b"".join(chunks)) > 20000:
                    break
        except socket.timeout:
            pass
        data = b"".join(chunks)
        print(label, "sent", len(payload), "recv", len(data), repr(data[:200]))
    except Exception as e:
        print(label, "ERR", e)
    finally:
        s.close()

init = {"seq": 1, "type": "request", "command": "initialize", "arguments": {"adapterID": "lua", "clientID": "probe"}}
body = json.dumps(init).encode()

# variants
try_once(b"Content-Length: %d\r\n\r\n" % len(body) + body, "dap-header")
try_once(body + b"\n", "json-newline")
try_once(b"evaluate\nprint(1)\n", "plain-eval")
try_once(b"{\"cmd\":\"evaluate\",\"expression\":\"1+1\"}\n", "cmd-json")
# just connect and wait for banner
s = socket.socket(); s.settimeout(2)
s.connect((HOST, PORT))
try:
    d = s.recv(4096)
    print("banner", repr(d[:300]))
except Exception as e:
    print("no banner", e)
s.close()
