"""Read a known Lua state in JA3Debug 67b4a208 (packed Lua 5.3 ABI).

Read-only memory inspection; no debugger attach, suspension, injection or writes.
Usage: python docs/tools/_read_ja3_lua_hang.py PID LUA_STATE_ADDRESS
The address must come from a captured native context; never guess it.
Results are racy snapshots, not a stopped debugger stack. This engine ABI has
9-byte TValue and packed closures/prototypes; do not use on another build.
"""
import ctypes as c
from ctypes import wintypes as w
import json
import struct
import sys


def main():
    pid, state = int(sys.argv[1]), int(sys.argv[2], 0)
    kernel = c.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
    kernel.OpenProcess.restype = w.HANDLE
    kernel.ReadProcessMemory.argtypes = [w.HANDLE, c.c_void_p, c.c_void_p, c.c_size_t, c.c_void_p]
    kernel.CloseHandle.argtypes = [w.HANDLE]
    kernel.QueryFullProcessImageNameW.argtypes = [w.HANDLE, w.DWORD, w.LPWSTR, c.POINTER(w.DWORD)]
    handle = kernel.OpenProcess(0x410, False, pid)
    if not handle:
        raise c.WinError(c.get_last_error())

    def read(address, size):
        if not 0 < size <= 65536:
            raise ValueError('Read bound exceeded')
        buffer = c.create_string_buffer(size)
        if not kernel.ReadProcessMemory(handle, address, buffer, size, None):
            raise c.WinError(c.get_last_error())
        return buffer.raw

    def q(address):
        return struct.unpack('<Q', read(address, 8))[0]

    def u(address):
        return struct.unpack('<I', read(address, 4))[0]

    def string(address):
        header = read(address, 24)
        tag = header[8] & 63
        if tag not in (4, 20):
            raise ValueError('Not a Lua string; unsupported ABI')
        length = header[11] if tag == 4 else struct.unpack_from('<Q', header, 16)[0]
        return read(address + 24, min(length, 1024)).decode('utf-8', errors='replace') if length else ''

    def value(address):
        raw = read(address, 9)
        tag = raw[8] & 63
        if tag == 0:
            return None
        if tag == 1:
            return bool(raw[0])
        if tag in (3, 19):
            return struct.unpack('<q', raw[:8])[0]
        if tag in (4, 20):
            return string(struct.unpack('<Q', raw[:8])[0])
        return {'tag': tag, 'address': hex(struct.unpack('<Q', raw[:8])[0])}

    try:
        name = c.create_unicode_buffer(32768)
        size = w.DWORD(len(name))
        if not kernel.QueryFullProcessImageNameW(handle, 0, name, c.byref(size)) or not name.value.lower().endswith('\\ja3debug.exe'):
            raise ValueError('Expected JA3Debug.exe')
        ci = q(state + 32)
        frames, seen = [], set()
        while ci and len(frames) < 64:
            if ci in seen:
                raise ValueError('CallInfo cycle')
            seen.add(ci)
            function, _, previous, _, base, pc = struct.unpack('<6Q', read(ci, 48))
            closure = q(function)
            frame = {'index': len(frames), 'callinfo': hex(ci)}
            if read(function + 8, 1)[0] == 0x46:
                proto = q(closure + 19)
                frame['source'] = string(q(proto + 101))
                code, lineinfo = q(proto + 53), q(proto + 69)
                instruction = (pc - code) // 4 - 1
                count = u(proto + 25)
                frame['defined'] = u(proto + 37)
                if 0 <= instruction < count < 1000000:
                    frame['line'] = u(lineinfo + instruction * 4)
                local_count, local_array = u(proto + 33), q(proto + 77)
                if local_count > 1024:
                    raise ValueError('Invalid local count')
                locals_, slot = [], 0
                for index in range(local_count):
                    var_name, start, end = struct.unpack('<QII', read(local_array + index * 16, 16))
                    if start <= instruction < end:
                        locals_.append({'name': string(var_name), 'value': value(base + slot * 9)})
                        slot += 1
                frame['locals'] = locals_
            else:
                frame['native'] = hex(closure)
            frames.append(frame)
            ci = previous
        print(json.dumps({'pid': pid, 'lua_state': hex(state), 'frames': frames}, ensure_ascii=False, indent=2))
    finally:
        kernel.CloseHandle(handle)


if __name__ == '__main__':
    main()
