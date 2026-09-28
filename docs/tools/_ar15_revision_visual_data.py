"""One-item visual fix: --weapon M4A1|M16A4|M21 --output DIR [--apply].
AR15 uses the vanilla straight magazine; M21 restores the side mount for lights.
"""
import argparse,re,subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_ar15_family import wire_visuals
from _integrate_m14_family import matching
p=argparse.ArgumentParser();p.add_argument('--weapon',choices=('M4A1','M16A4','M21'),required=True)
p.add_argument('--fix-grip',action='store_true')
p.add_argument('--output',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parents[2];path=root/'items.lua';before=path.read_bytes()
table=({'JAZZ_MagSmall30_20':('Magazine','WeaponAttA_MagazineCAR15_02')} if a.weapon!='M21' else
 {cid:('Mountside','WeaponAttA_SideMountM14') for cid in ('JAZZ_Flashlight','JAZZ_FlashlightDot','JAZZ_FlashlightOff')})
source=before.decode('utf-8')
if a.fix_grip:
 assert a.weapon=='M4A1'
 at=source.index('id = "JAZZ_VerticalGrip"');start=source.rfind("PlaceObj('ModItemWeaponComponent'",0,at)
 end=matching(source,source.index('(',start));block=source[start:end];removed=0
 for m in reversed(list(re.finditer(re.escape("PlaceObj('WeaponComponentVisual'"),block))):
  e=matching(block,block.index('(',m.start()));v=block[m.start():e]
  if 'ApplyTo = "M4A1"' in v and 'Slot = "Mountfront"' in v:
   assert block[e]==',';block=block[:m.start()]+block[e+1:];removed+=1
 assert removed==1
 source=source[:start]+block+source[end:]
 table={'JAZZ_VerticalGrip':('Under','WeaponAttA_VerticalGripCAR15')}
text,log=wire_visuals(source,a.weapon,table)
LuaRuntime().compile(text)
a.output.mkdir(parents=True,exist_ok=True);(a.output/'items.lua').write_text(text,encoding='utf-8',newline='\n')
if a.apply:
 check=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,Ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
 assert not check.stdout.strip(),'Game/editor must be closed'
 assert path.read_bytes()==before,'Concurrent edit'
 backup=a.output/'items-before.lua';assert not backup.exists();backup.write_bytes(before)
 path.write_text(text,encoding='utf-8',newline='\n')
print('APPLIED' if a.apply else 'STAGED',log)
