"""Copy only missing AKM-compatible AK103 visuals (GP25, bipod, 40-round mag).
--backup <dir> [--apply]; closed game, items.lua only (inline component presets).
"""
import argparse,re,shutil,subprocess
from pathlib import Path
from _integrate_m14_family import matching
p=argparse.ArgumentParser();p.add_argument('--backup',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
path=Path(__file__).resolve().parents[2]/'items.lua';text=path.read_text(encoding='utf-8')
for component in ('JAZZ_GP25','JAZZ_Bipod','JAZZ_MagLarge_30_40'):
    at=text.index('id = "'+component+'"');start=text.rfind("PlaceObj('ModItemWeaponComponent'",0,at);end=matching(text,text.index('(',start))
    block=text[start:end]
    if 'ApplyTo = "AK103"' in block:print(component,'already present');continue
    rx=re.compile(r"PlaceObj\('WeaponComponentVisual',\s*\{[^{}]*?ApplyTo = \"AKM\",[^{}]*?\}\)",re.S)
    block,n=rx.subn(lambda m:m.group()+',\n'+m.group().replace('ApplyTo = "AKM"','ApplyTo = "AK103"'),block)
    assert n>0,component;print(component,'added visuals',n);text=text[:start]+block+text[end:]
if a.apply:
    r=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue).Count"],capture_output=True,text=True)
    assert r.stdout.strip()=='0','Game must be closed'
    a.backup.mkdir(parents=True,exist_ok=True);bak=a.backup/'items-before-ak103-visuals.lua'
    if not bak.exists():shutil.copy2(path,bak)
    path.write_text(text,encoding='utf-8',newline='\n')
