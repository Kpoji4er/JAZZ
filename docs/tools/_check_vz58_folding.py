"""Read-only offline checks of actual stock actions/HUD with a minimal unit stub.

Run with Python from any directory. Does not simulate engine AP charging or rendering.
"""
import re
from lupa import LuaRuntime
from _integrate_vz58 import ROOT, component_block
from _integrate_sr3m import matching

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
function T(...) return {...} end
function PlaceObj(c,p) local r={} for k,v in pairs(p or {}) do if type(k)=='string' then r[k]=v end end for i=1,#(p or {}),2 do r[p[i]]=p[i+1] end return r end
WeaponComponents={}; CombatActions={}
function IsKindOf(o,c) return o and o.class==c end
function GetUnitNoApReason(u) return 'no_ap' end
''')
items = (ROOT/'items.lua').read_text(encoding='utf-8-sig')
for cid in ['JAZZ_StockLightUnFolded', 'JAZZ_StockLightFolded', 'JAZZ_StockNormal', 'JAZZ_StockHeavy']:
    start,end = component_block(items,cid)
    lua.globals().WeaponComponents[cid] = lua.execute('return '+items[start:end])
for cid in ['FoldStock','UnFoldStock']:
    hit = re.search(r'\bid\s*=\s*"'+cid+'"',items)
    start = items.rfind("PlaceObj('ModItemCombatAction'",0,hit.start())
    end = matching(items,items.index('(',start))
    lua.globals().CombatActions[cid] = lua.execute('return '+items[start:end])
lua.execute((ROOT/'Code/System_WeaponCompHUD.lua').read_text(encoding='utf-8-sig'))
source = (ROOT/'Code/System_WeaponRemovableModify.lua').read_text(encoding='utf-8-sig')
lua.execute(re.search(r'function JAZZ_IsHiddenModifyWeaponCraftOption\(.*?\nend',source,re.S).group())
lua.execute('''
local w={class='Firearm',components={Stock='JAZZ_StockLightUnFolded'}}
function w:SetWeaponComponent(slot,id) self.components[slot]=id end
local u={ap=4000}
function u:GetActiveWeapons() return w end
function u:UIHasAP(cost) return self.ap>=cost end
local fold,unfold=CombatActions.FoldStock,CombatActions.UnFoldStock
assert(fold:GetAPCost(u)==4000 and unfold:GetAPCost(u)==4000)
assert(fold:GetUIState({u})=='enabled' and unfold:GetUIState({u})=='hidden')
local action,state=JazzResolveFoldStockAction(u)
assert(action==fold and state=='enabled')
u.ap=3999
local disabled,reason=fold:GetUIState({u})
assert(disabled=='disabled' and reason=='no_ap')
u.ap=4000; fold:Run(u,4000)
assert(w.components.Stock=='JAZZ_StockLightFolded')
assert(fold:GetUIState({u})=='hidden' and unfold:GetUIState({u})=='enabled')
action,state=JazzResolveFoldStockAction(u)
assert(action==unfold and state=='enabled')
u.ap=3999; assert(unfold:GetUIState({u})=='disabled')
u.ap=4000; unfold:Run(u,4000)
assert(w.components.Stock=='JAZZ_StockLightUnFolded')
assert(JAZZ_IsHiddenModifyWeaponCraftOption('JAZZ_StockLightFolded'))
assert(not JAZZ_IsHiddenModifyWeaponCraftOption('JAZZ_StockLightUnFolded'))
for _,id in ipairs({'JAZZ_StockNormal','JAZZ_StockHeavy'}) do
 w.components.Stock=id
 assert(fold:GetUIState({u})=='hidden' and unfold:GetUIState({u})=='hidden')
 action,state=JazzResolveFoldStockAction(u); assert(action==nil and state=='hidden')
end
w.class='Other'; assert(fold:GetUIState({u})=='hidden')
''')
print('PASS: actual Lua fold/unfold actions, 4 AP cost, HUD routing, insufficient AP, fixed stocks, craft visibility. Engine runtime NOT_RUN.')
