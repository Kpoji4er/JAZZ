-- Run inside a temporary GameTimeThread, with SafeEvalStart/End.
-- No inventory/world placement, RNG, firing, save writes or persistent item IDs.
local objects, visuals, output = {}, {}, {}
local before_id = nextItemId
local function check(value, message) if not value then error(message) end end
local function make(id)
  local w = g_Classes[id]:new({is_clone=true})
  objects[#objects+1] = w
  check(not w.id, id..": preview allocated persistent id")
  local vis = w:CreateVisualObj()
  visuals[#visuals+1] = vis
  w:UpdateVisualObj(vis)
  check(vis:GetEntity()==w.Entity, id..": fallback visual")
  return w,vis
end
InventoryItem.DetachIdInitialization("weapon-import-smoke")
local ok,err = pcall(function()
  local w,vis=make("Mosin")
  check(w.components.Barrel=="JAZZ_Mosin1891", "Mosin: missing default Barrel")
  w:SetWeaponComponent("Scope","JAZZ_Scope_PU")
  for _,row in ipairs({
    {"JAZZ_Mosin1891","MOSIN_1891",9000,40,50,66},
    {"JAZZ_MosinM38","MOSIN_M38",7000,38,50,52},
    {"JAZZ_MosinObrez","MOSIN_Obrez",5000,32,35,24},
    {"JAZZ_Mosin1891","MOSIN_1891",9000,40,50,66},
  }) do
    w:SetWeaponComponent("Barrel",row[1]);w:UpdateVisualObj(vis)
    local long=row[1]=="JAZZ_Mosin1891"
    if long then w:SetWeaponComponent("Scope","JAZZ_Scope_PU");w:UpdateVisualObj(vis) end
    check(w.Entity==row[2] and vis:GetEntity()==row[2],"Mosin: entity "..row[1])
    check(w.ShootAP==row[3] and w.Damage==row[4] and w.CritChanceScaled==row[5] and w.WeaponRange==row[6], "Mosin: stats "..row[1].." "..tostring(w.ShootAP).."/"..tostring(w.Damage).."/"..tostring(w.CritChanceScaled).."/"..tostring(w.WeaponRange))
    if long then
      check(IsValid(vis.parts.Scope) and vis.parts.Scope:GetEntity()=="PUOptic","Mosin: long rifle PU missing")
    else
      check(not IsValid(vis.parts.Scope) and (w.components.Scope or "")=="","Mosin: PU remained on short configuration")
      check(w:GetNumModifySlotOptions(table.find_value(w.ComponentSlots,"SlotType","Scope"))==0,"Mosin: scope slot must be blocked")
    end
    check(vis:GetSpotBeginIndex("Hand_l_grip")~=-1,"Mosin: left-hand spot")
  end
  w:SetWeaponComponent("Scope","");check(w.ShootAP==8000,"Mosin: PU removal left AP modifier")
  output[#output+1]="PASS Mosin: long/M38/Obrez/reversal, PU only on long rifle, AP/damage/crit/range, left-hand spots"
  for _,id in ipairs({"AK74","AK74M","AK105","AKSU","AKM","AK47"}) do
    local gun,v=make(id)
    local large=(id=="AKM" or id=="AK47") and "JAZZ_MagLarge_30_40" or "JAZZ_MagLarge_30_45"
    local count=(id=="AKM" or id=="AK47") and 40 or 45
    for _,pair in ipairs({{"JAZZ_MagNormal",30},{large,count},{"JAZZ_MagQuick_AK",30},{"JAZZ_MagNormal",30}}) do
      gun:SetWeaponComponent("Magazine",pair[1]);gun:UpdateVisualObj(v)
      check(gun.MagazineSize==pair[2],id..": magazine capacity "..pair[1].." = "..tostring(gun.MagazineSize))
      check(IsValid(v.parts.Magazine),id..": missing magazine visual "..pair[1])
    end
    if id=="AKM" or id=="AK47" then
      gun:SetWeaponComponent("Magazine","JAZZ_MagDrum_30_75");check(gun.MagazineSize==75,id..": drum capacity")
    end
    if id=="AK74M" or id=="AK105" then
      for _,pair in ipairs({{"JAZZ_StockLightFolded","StockFolded"},{"JAZZ_StockLightUnFolded","Stock"}}) do
        gun:SetWeaponComponent("Stock",pair[1]);gun:UpdateVisualObj(v)
        check(IsValid(v.parts.Stock) and v.parts.Stock:GetEntity()=="AKR_"..id.."_"..pair[2],id..": folding stock")
      end
      gun:SetWeaponComponent("Scope","JAZZ_Reflex_PKAS");gun:UpdateVisualObj(v)
      check(IsValid(v.parts.Scope),id..": missing optic")
      gun:SetWeaponComponent("Muzzle","JAZZ_Suppressor");gun:UpdateVisualObj(v)
      check(IsValid(v.parts.Muzzle),id..": missing suppressor")
    end
    output[#output+1]="PASS "..id..": magazine capacities and visuals, reversal"..((id=="AK74M" or id=="AK105") and ", folding stock/optic/suppressor" or "")
  end
  local rifle,scope=make("L42A1")
  check(IsValid(scope.parts.Scope) and scope.parts.Scope:GetEntity()=="L42A1_Scope","L42A1: dedicated scope")
  local sr,sv=make("SR3M")
  for _,pair in ipairs({{"JAZZ_StockLightFolded","SR3M_StockFolded"},{"JAZZ_StockLightUnFolded","SR3M_Stock"}}) do
    sr:SetWeaponComponent("Stock",pair[1]);sr:UpdateVisualObj(sv)
    check(IsValid(sv.parts.Stock) and sv.parts.Stock:GetEntity()==pair[2],"SR3M: stock")
  end
  output[#output+1]="PASS L42A1 dedicated scope; SR3M stock folding/reversal"
end)
InventoryItem.AttachIdInitialization("weapon-import-smoke")
for _,vis in ipairs(visuals) do if IsValid(vis) then DoneObject(vis) end end
for _,w in ipairs(objects) do w.visual_obj=false;DoneObject(w) end
output[#output+1]=(before_id==nextItemId and "PASS" or "FAIL").." persistent item-id counter unchanged"
if not ok then output[#output+1]="FAIL "..tostring(err) end
return table.concat(output,"\n")
