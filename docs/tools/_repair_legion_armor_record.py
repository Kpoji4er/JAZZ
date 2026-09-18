"""Repair the initial APPEAR test ModItem serialization; narrow and idempotent.

An already open Mod Editor must reload from disk before any subsequent save.
"""
import re
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import matching,write
path=Path(__file__).resolve().parents[3]/'jazz-units/items.lua'
before=path.read_bytes();text=before.decode('utf-8-sig')
needle='Id = "JAZZ_Legion_ArmorTest"'
if needle not in text:
    assert "'Id', \"JAZZ_Legion_ArmorTest\"" in text
    print('Already repaired')
else:
    pos=text.index(needle);start=text.rfind("PlaceObj('ModItemUnitDataCompositeDef'",0,pos);end=matching(text,text.index('(',start))
    old=text[start:end];new=re.sub(r'^    (\w+) = ',r"    '\1', ",old,flags=re.M).replace("'group', \"JAZZ Tests\"","'Group', \"JAZZ Tests\"")
    result=text[:start]+new+text[end:];LuaRuntime().compile(result)
    assert path.read_bytes()==before,'Concurrent modification'
    write(path,result);print('Repaired test unit ModItem property array and Group')
