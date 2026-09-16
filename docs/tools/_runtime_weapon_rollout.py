"""Reload only JAZZ/Units item trees from disk, then native ReloadLua.

Requires live JA3Debug DAP. Does not reload assets/maps or reset the session.
Stops if either editor item tree has unsaved edits. No initialize/pause/save.
Report: AppData/jazz_weapon_rollout_reload.txt.
"""
from _probe_weapon_imports_runtime import evaluate

expression='''(function()
 CreateRealTimeThread(function()
  local ign=SafeEvalStart("weapon-rollout-reload")
  local ok,result=pcall(function()
   local targets={Mods["e6L4ECj"],Mods["Dv3mFVN"]}
   for _,mod in ipairs(targets) do
    local dirty={}
    mod:ForEachModItem(function(item)
     if item.IsDirty and item:IsDirty() then dirty[#dirty+1]=item.id or item.Id or item.class end
    end)
    if #dirty>0 then error("Unsaved editor items in "..mod.id..": "..table.concat(dirty,",")) end
   end
   for _,mod in ipairs(targets) do
    local rebound=false
    for _,ged in pairs(GedConnections or {}) do
     local root=ged:ResolveObj("root")
     if root and root[1]==mod then GedReloadModItems(ged);rebound=true;break end
    end
    if not rebound then mod:UnloadItems();mod:LoadItems() end
    assert(mod:ItemsLoaded(),"Item reload failed: "..mod.id)
   end
   ReloadLua()
   assert(AK105.Damage==27 and AK105.Cost==14500,"AK105 stats")
   assert(AK74.CyclicRPM==600 and AK74M.CyclicRPM==600,"AK rates")
   for _,id in ipairs({"AK74M","AK105","SR3M","L42A1"}) do
    local w=g_Classes[id];assert(w.CanAppearInShop and w.RestockWeight>0,id.." shop")
   end
   return "PASS disk item reload and native ReloadLua; AK105 Damage27/Cost14500; AK74/AK74M RPM600; four shop entries enabled. No asset/map reload."
  end)
  SafeEvalEnd(ign,"weapon-rollout-reload")
  AsyncStringToFile("AppData/jazz_weapon_rollout_reload.txt",ok and result or ("FAIL "..tostring(result)))
 end)
 return "Scheduled guarded item reload; report in AppData/jazz_weapon_rollout_reload.txt"
end)()'''
print(evaluate(expression))
