# -*- coding: utf-8 -*-
import socket
import json

s = socket.socket()
s.settimeout(3)
try:
    s.connect(("127.0.0.1", 8165))
    print("TCP 8165 OPEN")
    req = {
        "seq": 1,
        "type": "request",
        "command": "initialize",
        "arguments": {
            "clientID": "cursor",
            "adapterID": "lua",
            "linesStartAt1": True,
            "columnsStartAt1": True,
            "pathFormat": "path",
        },
    }
    body = json.dumps(req).encode("utf-8")
    msg = b"Content-Length: %d\r\n\r\n" % len(body) + body
    s.sendall(msg)
    data = s.recv(8192)
    print("recv bytes", len(data))
    print(data[:800])
except Exception as e:
    print("FAIL", type(e).__name__, e)
finally:
    s.close()
