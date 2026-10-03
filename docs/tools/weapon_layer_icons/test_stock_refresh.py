"""Execute installed fold/unfold Run, setter and UI traversal without action-end.
Proves already-open inventory/HUD images refresh; clone/init changes stay quiet.
"""
from pathlib import Path
import re
from lupa import LuaRuntime
root=Path(__file__).resolve().parents[3]
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
FirearmBase={};WeaponComponentEffects={};empty_table={}
WeaponComponents={open={zzFoldingPair={'folded'},ModificationEffects={},Visuals={}},folded={zzFoldingPair={'open'},ModificationEffects={},Visuals={}}}
function ObjModified() end
function FirearmBase:UnregisterReactions() end
function FirearmBase:RegisterReactions() end
function FirearmBase:RemoveModifiers() end
function FirearmBase:UpdateVisualObj() end
item=setmetatable({class='VZ58',components={Stock='open'},subweapons={}},{__index=FirearmBase})
unit={GetActiveWeapons=function() return item end}
hud={context=item,idIcon={}};inventory={context=item,idItemImg={}}
function GetInGameInterface() return {hud} end
function GetMercInventoryDlg() return {inventory} end
function JazzAttachChips_IsFirearm(o) return o==item end
updates=0
function JazzWeaponIcon_BindItemImage(img,o) img.stock=o.components.Stock;updates=updates+1 end
queue={}
function DelayedCall(_,fn) queue[#queue+1]=fn end
function flush() for _,fn in ipairs(queue) do fn() end;queue={} end
''')
setter=(root/'Code/System_WeaponComponent_Set.lua').read_text(encoding='utf-8-sig').split('-- MP40 is MagNormal-only')[0]
lua.execute(setter)
ui=(root/'Code/InventoryUI.lua').read_text(encoding='utf-8-sig')
lua.execute(ui[ui.index('function JazzWeaponIcon_RefreshWeaponDisplays()'):ui.index('function OnMsg.SelectionChange()')])
items=(root/'items.lua').read_text(encoding='utf-8-sig')
for ident,state in [('FoldStock','folded'),('UnFoldStock','open')]:
 end=items.index('id = "'+ident+'"')
 start=items.rfind("PlaceObj('ModItemCombatAction'",0,end)
 fn=re.search(r'Run = (function .*?\n\s*end),',items[start:end],re.S).group(1)
 lua.globals().action=lua.eval(fn)
 lua.execute('assert(action(nil,unit,0)==false);flush()')
 assert lua.globals().hud.idIcon.stock==state and lua.globals().inventory.idItemImg.stock==state
lua.execute('''
assert(updates==8)
item.is_clone=true;item:SetWeaponComponent('Stock','folded');assert(#queue==0)
item.is_clone=nil;item:SetWeaponComponent('Stock','open',true);assert(#queue==0)
''')
print('PASS: actual Fold/UnFold Run updates both open HUD/inventory via setter; no CombatActionEnd; clones/init quiet')
