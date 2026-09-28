"""Canonical multiline formatting for only VZ58 ModItemEntity records; --build DIR [--apply]."""
import argparse,re,subprocess
from pathlib import Path
from _integrate_vz58 import ASSETS
from _integrate_sr3m import matching
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
path=ASSETS/'items.lua';raw=path.read_bytes();text=raw.decode('utf-8-sig');count=0
for m in reversed(list(re.finditer(r"PlaceObj\('ModItemEntity', \{ 'name', \"(JAZZ_VZ58[^\"]*)\"",text))):
 end=matching(text,text.index('(',m.start()));name=m[1]
 replacement=f"PlaceObj('ModItemEntity', {{\n\t\t'name', \"{name}\",\n\t\t'ClassParents', {{}},\n\t\t'entity_name', \"{name}\",\n\t}})"
 text=text[:m.start()]+replacement+text[end:];count+=1
assert count in (0,13),count
if a.apply and count:
 assert not subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True).stdout.strip()
 assert path.read_bytes()==raw
 (a.build/'assets-items-before-format.lua').write_bytes(raw)
 nl='\r\n' if b'\r\n' in raw else '\n';path.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'')+text.replace('\r\n','\n').replace('\n',nl).encode('utf-8'))
print('Formatted',count,'VZ58 entity records; applied=',a.apply)
