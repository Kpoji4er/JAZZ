"""Capture a local JA3Debug minidump without attaching a debugger or terminating it.

Usage: python docs/tools/_capture_ja3_hang_dump.py PID OUTPUT.dmp
Windows x64 Python required. Output must not exist. No uploads or restart.
"""
import argparse
import ctypes as c
from ctypes import wintypes as w
import msvcrt
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pid', type=int)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    kernel = c.WinDLL('kernel32', use_last_error=True)
    dbg = c.WinDLL('dbghelp', use_last_error=True)
    kernel.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
    kernel.OpenProcess.restype = w.HANDLE
    kernel.CloseHandle.argtypes = [w.HANDLE]
    kernel.QueryFullProcessImageNameW.argtypes = [w.HANDLE, w.DWORD, w.LPWSTR, c.POINTER(w.DWORD)]
    dbg.MiniDumpWriteDump.argtypes = [w.HANDLE, w.DWORD, w.HANDLE, w.DWORD, c.c_void_p, c.c_void_p, c.c_void_p]
    dbg.MiniDumpWriteDump.restype = w.BOOL
    process = kernel.OpenProcess(0x0400 | 0x0010, False, args.pid)
    if not process:
        raise c.WinError(c.get_last_error())
    try:
        name = c.create_unicode_buffer(32768)
        size = w.DWORD(len(name))
        if not kernel.QueryFullProcessImageNameW(process, 0, name, c.byref(size)):
            raise c.WinError(c.get_last_error())
        if Path(name.value).name.lower() != 'ja3debug.exe':
            raise ValueError('Refusing non-JA3Debug process: ' + name.value)
        # Normal stacks + memory map + thread info. No full heap or handle scan.
        with args.output.open('xb') as stream:
            if not dbg.MiniDumpWriteDump(process, args.pid, msvcrt.get_osfhandle(stream.fileno()), 0x1800, None, None, None):
                raise c.WinError(c.get_last_error())
        print(f'{args.output}: {args.output.stat().st_size} bytes')
    finally:
        kernel.CloseHandle(process)


if __name__ == '__main__':
    main()
