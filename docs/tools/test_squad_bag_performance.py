"""JAZZ-INV-006 offline Lua regression tests. Requires lupa; never starts JA3.

Runs production bag/cache/scheduler code with engine stand-ins. The reference
merge is the previous all-pairs algorithm. Does not measure engine UI latency.
"""
from pathlib import Path

from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]


def main():
    bag = (ROOT / "Code/System_OR_SquadBag.lua").read_text(encoding="utf-8-sig")
    ui = (ROOT / "Code/InventoryUI.lua").read_text(encoding="utf-8-sig")
    stacks = (ROOT / "Code/System_InventoryStacks.lua").read_text(encoding="utf-8-sig")
    lua = LuaRuntime(unpack_returned_tuples=True)
    for name, source in (("bag", bag), ("ui", ui), ("stacks", stacks)):
        lua.execute('assert(load(...))', source, name)
    lua.execute(r'''
empty_table = {}
const = {JazzStorageStackMax=10000}
Min, Max = math.min, math.max
gv_Squads, Inventory, SquadBag = {}, {}, {}
gv_SquadBag = false
InventoryDragItem = false
OnMsg = {}
stats = {adds=0, contexts=0, comparisons=0}
function IsKindOf(item, class)
  return item and (item.kind == class or (class == "InventoryStack" and item.Amount ~= nil))
end
function DoneObject(item) item.deleted = true end
function GetSquadBag(id) return gv_Squads[id] and gv_Squads[id].squad_bag end
function JazzMarkSquadBagData(id)
  for _, item in ipairs(GetSquadBag(id)) do item.MaxStacks=const.JazzStorageStackMax end
end
function JazzApplyStackContext(item) item.MaxStacks=const.JazzStorageStackMax end
function JazzEnsureContainerStackContext(inv)
  stats.contexts=stats.contexts+1
  for i=2,#inv.Inventory,2 do JazzApplyStackContext(inv.Inventory[i]) end
end
InventorySlot = {}
function InventorySlot:new() return {kind="InventorySlot"} end
function Inventory:AddItem(slot_name, item)
  stats.adds=stats.adds+1
  local slot=self[slot_name]
  slot[#slot+1]=#slot/2+1
  slot[#slot+1]=item
  return #slot/2
end
function PlaceObject(class)
  assert(class=="SquadBag")
  return setmetatable({Inventory=InventorySlot:new()}, {__index=SquadBag})
end
function DeleteThread(thread) if thread then thread.cancelled=true end end
function CreateGameTimeThread(fn, id) return {fn=fn,id=id} end
function IsValidThread(thread) return thread and not thread.cancelled end
function MakeItem(id, class, amount, kind, component)
  return {id=id,class=class,Amount=amount,kind=kind,RemovableComponentId=component,
    Caliber="c" .. (id%3), width=1, height=1,
    GetUIWidth=function(self) return self.width end,
    GetUIHeight=function(self) return self.height end}
end
function Clone(items)
  local copy={}
  for i,item in ipairs(items) do
    copy[i]={}
    for k,v in pairs(item) do copy[i][k]=v end
  end
  return copy
end
function ReferenceMerge(items)
  local result={}
  for _,item in ipairs(items) do
    for _,other in ipairs(result) do
      if JazzInventoryItemsCanStack(other,item) then
        local count=Min(10000-other.Amount,item.Amount)
        if count>0 then
          other.Amount=other.Amount+count
          item.Amount=item.Amount-count
          if item.Amount==0 then DoneObject(item);item=false;break end
        end
      end
    end
    if item and item.Amount and item.Amount>0 then
      if IsKindOf(item,"InventoryStack") then item.MaxStacks=10000 end
      result[#result+1]=item
    end
  end
  return result
end
''')
    lua.execute(stacks[stacks.index("function JazzInventoryItemsCanStack"):stacks.index("function JazzGetPersonalMaxStacks")])
    lua.execute('''
local original=JazzInventoryItemsCanStack
function JazzInventoryItemsCanStack(a,b)
  stats.comparisons=stats.comparisons+1
  return original(a,b)
end
''')
    section = bag[bag.index("function SquadBag:GetMaxTilesInSlot"):bag.index("function GetSquadBag(squad_id)")]
    lua.execute(section)
    # Reuse the unchanged comparator, comparing survivor identities AND ordering.
    comparator = bag[bag.index("\ttable.sort(stacks, function(a,b)"):bag.index("\tgv_Squads[squad_id].squad_bag = stacks")]
    lua.execute("function ReferenceSort(stacks)\n" + comparator + "\nreturn stacks end")
    lua.execute(r'''
function Compare(items)
  local reference=Clone(items)
  local expected=ReferenceSort(ReferenceMerge(reference))
  gv_Squads[1]={squad_bag=items}
  _SortItemsInBag(1)
  local actual=GetSquadBag(1)
  assert(#actual==#expected,"survivor count")
  local expectedById={}
  for _,item in ipairs(expected) do expectedById[item.id]=item end
  for i,item in ipairs(actual) do
    assert(item.id==expected[i].id,"survivor order")
    assert(item.Amount==expected[i].Amount,"amount")
    assert(item.MaxStacks==expected[i].MaxStacks,"stack cap")
  end
  for i,item in ipairs(items) do
    assert(item.deleted==reference[i].deleted,"object deletion")
    assert(item.Amount==reference[i].Amount,"source mutation")
    if not item.deleted and expectedById[item.id] then
      local found=false
      for _,survivor in ipairs(actual) do if survivor==item then found=true end end
      assert(found,"object identity")
    end
  end
end
math.randomseed(20261003)
Compare({})
Compare({MakeItem(1,"Module",5,"JAZZ_RemovableAttachment"),
  MakeItem(2,"Module",10,"JAZZ_RemovableAttachment","Module"),
  MakeItem(3,"Module",10,"JAZZ_RemovableAttachment","Other")})
for trial=1,300 do
  local items={}
  for i=1,math.random(1,500) do
    local family=math.random(1,30)
    local class=family==1 and "Meds" or family==2 and "Parts" or "Item"..family
    local kind=family<8 and "Ammo" or family<15 and "JAZZ_RemovableAttachment" or nil
    local component=kind=="JAZZ_RemovableAttachment" and ("component"..math.random(1,5)) or nil
    local amounts={0,1,9999,10000,10001,25000,math.random(1,30000)}
    items[i]=MakeItem(i,class,amounts[math.random(#amounts)],kind,component)
  end
  Compare(items)
end
-- Worst-case incompatible classes: reference n*(n-1)/2; indexed merge zero.
local many={}
for i=1,1000 do many[i]=MakeItem(i,"Unique"..i,1) end
stats.comparisons=0
ReferenceMerge(Clone(many))
local oldCount=stats.comparisons
stats.comparisons=0
gv_Squads[1]={squad_bag=many}
_SortItemsInBag(1)
assert(stats.comparisons==0)
assert(oldCount==499500)
print("PASS merge: 300 randomized bags; 1000 unique stacks: 499500 -> 0 compatibility checks")
-- Many already-full stacks of one class must not become candidates either.
for i=1,1000 do many[i]=MakeItem(i,"Same",10000) end
gv_Squads[1]={squad_bag=many}
stats.comparisons=0
_SortItemsInBag(1)
assert(stats.comparisons==0 and #GetSquadBag(1)==1000)
GetSquadBagInventory(1,"small")
local largeAdds=stats.adds
for i=1,10 do GetSquadBagInventory(1,"small") end
assert(stats.adds==largeAdds,"large bag getter rebuild")

gv_Squads[1]={squad_bag={MakeItem(1,"Parts",20),MakeItem(2,"Meds",30)}}
gv_Squads[2]={squad_bag={MakeItem(3,"Ammo",40)}}
local bag=GetSquadBagInventory(1,"small")
local function Reuse()
  local adds=stats.adds
  assert(GetSquadBagInventory(1,"small")==bag)
  assert(stats.adds==adds,"unexpected rebuild")
end
local function Rebuild()
  local adds=stats.adds
  GetSquadBagInventory(1,"small")
  assert(stats.adds>adds,"missed invalidation")
  Reuse()
end
Reuse()
local first=GetSquadBag(1)[1]
first.Amount=25;first.MaxStacks=1
Reuse()
assert(first.MaxStacks==10000,"context refresh")
table.insert(GetSquadBag(1),MakeItem(4,"Misc",1));Rebuild()
table.remove(GetSquadBag(1));Rebuild()
local source=GetSquadBag(1)
source[1],source[2]=source[2],source[1];Rebuild()
source[1]=MakeItem(5,"New",1);Rebuild()
source[1].width=2;Rebuild()
source[1].height=2;Rebuild()
gv_Squads[1].squad_bag={source[1],source[2]};Rebuild()
bag.Inventory[1]=42;Rebuild()
bag.Inventory[2]=MakeItem(6,"Stale",1);Rebuild()
bag.Inventory=InventorySlot:new();Rebuild()
bag:Clear();Rebuild()
GetSquadBagInventory(1,"large");Rebuild()
GetSquadBagInventory(2,"small");Rebuild()
GetSquadBagInventory(1,nil);Rebuild()
bag.ui_mode="large"
GetSquadBagInventory(1,"large");Rebuild()
-- Empty inventories also cache, and retain the slot identity.
gv_Squads[3]={squad_bag={}}
local empty=GetSquadBagInventory(3,"small").Inventory
assert(GetSquadBagInventory(3,"small").Inventory==empty)
-- Shared handle is visible to the UI, and cancellation targets the old handle.
SortItemsInBag(1)
local old=g_squad_bag_sort_thread
assert(old.id==1)
SortItemsInBag(2)
assert(old.cancelled and g_squad_bag_sort_thread.id==2)
print("PASS cache: unchanged/amount-only reuse, source/layout/mode/squad/Clear invalidation; shared sort handle")
''')
    # A reload creates a fresh weak cache while preserving the engine handle.
    lua.execute('saved_thread=g_squad_bag_sort_thread; saved_slot=gv_SquadBag.Inventory')
    lua.execute(section)
    lua.execute('assert(g_squad_bag_sort_thread==saved_thread); assert(GetSquadBagInventory(3,"small").Inventory~=saved_slot)')
    lua.execute(r'''
queue={}; refreshes=0; resets=0
function DelayedCall(delay,fn) queue[#queue+1]=fn end
function GetMercInventoryDlg() return nil end
function JazzWeaponIcon_RefreshWeaponDisplays() refreshes=refreshes+1 end
function InventoryUIResetSquadBag() resets=resets+1 end
function Sleep(ms)
  -- Simulate callbacks arriving while the respawn waits for sorting.
  for i=1,100 do InventoryUIRespawn() end
  assert(#queue==0,"duplicate respawn while waiting for sort")
  g_squad_bag_sort_thread=false
end
function DrainOne() local fn=table.remove(queue,1);assert(fn);fn() end
g_squad_bag_sort_thread=false
''')
    lua.execute(ui[ui.index("local InventoryUIRespawn_shield"):ui.index("function InventoryEquipAPText")])
    lua.execute(r'''
for i=1,100 do InventoryUIRespawn() end
assert(#queue==1)
DrainOne();assert(refreshes==1 and #queue==0)
SortItemsInBag(1)
InventoryUIRespawn();DrainOne()
assert(refreshes==1 and resets==1 and #queue==1,"sort retry")
for i=1,100 do InventoryUIRespawn() end
assert(#queue==1)
DrainOne();assert(refreshes==2 and #queue==0)
InventoryUIRespawn();DrainOne();assert(refreshes==3)
-- Exercise the real panel-respawn branch and drag restoration with engine stubs.
local panels, contexts, scrolls, cancelled, restarted=0,0,0,0,0
local function Panel()
  return {RespawnContent=function() panels=panels+1;InventoryUIRespawn() end,
    OnContextUpdate=function() contexts=contexts+1 end}
end
local function Scroll(value)
  return {Scroll=value,ScrollTo=function(self,restored)
    assert(restored==self.Scroll);scrolls=scrolls+1
  end}
end
local dlg={idUnitInfo=Panel(),idPartyContainer={idParty=Panel()},
  idRight=Panel(),idCenter=Panel(),idScrollbar=Scroll(15),idScrollbarCenter=Scroll(42),
  GetContext=function() return {} end,OnContextUpdate=function() contexts=contexts+1 end}
function GetMercInventoryDlg() return dlg end
InventoryDragItem={}
local dragging=InventoryDragItem
function CancelDrag(window) assert(window==dlg);cancelled=cancelled+1 end
function RestartDrag(window,item)
  assert(window==dlg and item==dragging);restarted=restarted+1
end
function Msg(name) assert(name=="RespawnedInventory") end
for i=1,100 do InventoryUIRespawn() end
DrainOne()
assert(panels==4 and contexts==5 and scrolls==2 and cancelled==1 and restarted==1)
assert(#queue==0,"reentrant panel update")
print("PASS UI: 100 refresh requests -> 1 callback; active sort retry and subsequent refresh")
''')
    print("PASS syntax: complete modified Lua files; offline only, no engine rendering/drag-drop validation")


if __name__ == "__main__":
    main()
