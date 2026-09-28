-- Live model QA on ModEditor only. No globals, reloads, saves or asset writes.
return function(op, id, slot, component)
  assert(GetMapName() == "ModEditor", "QA requires ModEditor test map")
  local ids = {"AK74","AKM","AK74M","AK105","AK103","SR3M","L42A1","Mosin","M16A4","M4A1","FNFAL","JAZZ_FNFAL_Tactical","M14SAW","M21","MK14EBR","JAZZ_M14_MkIII"}
  local session = "JAZZ_Legion_ArmorTest_6B3_WeaponQA"
  local function unit()
    local u=g_Units[session]
    if not IsValid(u) then
      local base=g_Units.JAZZ_Legion_ArmorTest_6B3 or SelectedObj
      assert(IsValid(base), "No placement reference")
      u=SpawnUnit("JAZZ_Legion_ArmorTest_6B3",session,base:GetPos()+point(4000,0,0),base:GetAngle(),{})
      u:SetSide("neutral")
    end
    return u
  end
  local function parts(w)
    local v=w:GetVisualObj();local p={}
    for k,a in sorted_pairs(v.parts or {}) do
      if IsValid(a) then p[#p+1]=k.."="..a:GetEntity().."@"..tostring(a:GetAttachSpot()) end
    end
    return v,table.concat(p,",")
  end
  local function record(w,label,comp)
    local v,ps=parts(w);local errors={}
    if not IsValidEntity(w.Entity) then errors[#errors+1]="INVALID_HOST:"..tostring(w.Entity) end
    if comp and WeaponComponents[comp] then
      local chosen={}
      for _,d in ipairs(WeaponComponents[comp].Visuals or {}) do
        if d:Match(w.class) then
          local old=chosen[d.Slot]
          if not old or (old:IsGeneric() and not d:IsGeneric()) then chosen[d.Slot]=d end
        end
      end
      if not next(chosen) and #(WeaponComponents[comp].Visuals or {})>0 then errors[#errors+1]="NO_MATCHING_VISUAL" end
      for k,d in sorted_pairs(chosen) do
        if d.Entity and d.Entity~="" then
          if not IsValidEntity(d.Entity) then errors[#errors+1]="INVALID_ENTITY:"..tostring(d.Entity) end
          if not IsValid(v.parts[k]) then
            local alternate=false
            for _,a in pairs(v.parts or {}) do if IsValid(a) and a:GetEntity()==d.Entity then alternate=true end end
            if not alternate then errors[#errors+1]="NO_VISUAL:"..k..":"..tostring(d.Entity) end
          end
        end
      end
    end
    return table.concat({w.class,label,tostring(w.Entity),v:GetEntity(),ps,table.concat(errors,",")},"\t")
  end
  if op=="scan" then
    local lines={"weapon\tconfiguration\tdeclared_entity\tactual_entity\tparts\tfindings"}
    for _,wid in ipairs(ids) do
      local def=InventoryItemDefs[wid];assert(def,"Missing definition "..wid)
      local base=PlaceInventoryItem(wid);lines[#lines+1]=record(base,"default");base:delete()
      for _,s in ipairs(def.ComponentSlots or {}) do
        for _,cid in ipairs(s.AvailableComponents or {}) do
          local w=PlaceInventoryItem(wid)
          local fake={context={weapon=w},GetChangesCost=function() return {},false,true end}
          local allowed,reason,blocker=ModifyWeaponDlg.CanModifySlot(fake,s,cid)
          w:SetWeaponComponent(s.SlotType,cid)
          lines[#lines+1]=record(w,s.SlotType.."="..cid..";ui="..tostring(allowed)..":"..tostring(reason)..":"..tostring(blocker),cid)
          w:delete()
        end
      end
      Sleep(1)
    end
    return table.concat(lines,"\n")
  elseif op=="pairs" then
    local lines={"weapon\tfirst\tsecond\tallowed\treason\tfirst_after\tfindings"}
    local count=0
    for _,wid in ipairs(ids) do
      local slots=InventoryItemDefs[wid].ComponentSlots or {}
      for _,a in ipairs(slots) do for _,ca in ipairs(a.AvailableComponents or {}) do
        for _,b in ipairs(slots) do if a.SlotType~=b.SlotType then
          for _,cb in ipairs(b.AvailableComponents or {}) do
            local w=PlaceInventoryItem(wid);w:SetWeaponComponent(a.SlotType,ca)
            local fake={context={weapon=w},GetChangesCost=function() return {},false,true end}
            local allowed,reason,blocker=ModifyWeaponDlg.CanModifySlot(fake,b,cb)
            local findings=""
            if allowed then
              w:SetWeaponComponent(b.SlotType,cb)
              findings=record(w,"pair",cb):match("[^\t]*$")
            end
            lines[#lines+1]=table.concat({wid,a.SlotType.."="..ca,b.SlotType.."="..cb,tostring(allowed),tostring(reason)..":"..tostring(blocker),tostring(w.components[a.SlotType]),findings},"\t")
            w:delete();count=count+1;if count%50==0 then Sleep(1) end
          end
        end end
      end end
      Sleep(1)
    end
    return table.concat(lines,"\n")
  elseif op=="equip" then
    assert(table.find(ids,id),"Not in handoff")
    local u=unit();u:SetCommand("Idle")
    local old=u:GetItemInSlot("Handheld A","Firearm")
    if old then u:RemoveItem("Handheld A",old);old:delete() end
    local w=PlaceInventoryItem(id)
    if slot and slot~="" then w:SetWeaponComponent(slot,component) end
    assert(u:AddItem("Handheld A",w),"Cannot equip")
    u:UpdateOutfit();u:UpdateItemAppearance();u:SetpieceSetStance("Standing")
    local l=u:GetVisualPos()+point(0,0,1250);cameraTac.SetCamera(l+point(2200,-3500,1700),l,0);ShowConsoleLog(false)
    return record(w,"equipped",component).."\nunit="..session.." pose="..u:GetStateText()
  elseif op=="armor" then
    local allowed={JazzArmor_6B3=true,JazzArmor_ImprovisedCuirass=true}
    for _,family in ipairs({"Twaron","Guardian","Zylon"}) do
      for _,variant in ipairs({"Light","Medium","Full"}) do allowed["JazzArmor_"..family..variant]=true end
    end
    assert(allowed[id],"Not in armor handoff")
    local u=unit();u:SetCommand("Idle")
    local old=u:GetItemInSlot("Torso","Armor")
    if old then u:RemoveItem("Torso",old);old:delete() end
    assert(u:AddItem("Torso",PlaceInventoryItem(id)),"Cannot equip armor")
    u:UpdateOutfit();u:UpdateItemAppearance();u:SetpieceSetStance("Standing")
    local l=u:GetVisualPos()+point(0,0,1250)
    cameraTac.SetCamera(l+Rotate(point(1900,-2200,450),u:GetAngle()),l,0)
    local rows={"item="..id,"unit="..session,"body="..u:GetEntity(),"pose="..u:GetStateText()}
    for k,v in sorted_pairs(u.parts or {}) do if IsValid(v) then rows[#rows+1]=tostring(k).."="..v:GetEntity() end end
    return table.concat(rows,"\n")
  elseif op=="component" then
    local u=unit();local w=u:GetItemInSlot("Handheld A","Firearm")
    w:SetWeaponComponent(slot,component);u:UpdateOutfit();u:UpdateItemAppearance()
    return record(w,slot.."="..component,component)
  elseif op=="pose" then
    local u=unit()
    u:SetCommand(function(self)
      if id~="Aim" then self:DoChangeStance(id) end
      if id=="Aim" then self:RestoreAiming(self:GetVisualPos()+Rotate(point(10000,0,1250),self:GetAngle()),{can_use_covers=false}) end
      local height=self.stance=="Prone" and 400 or (self.stance=="Crouch" and 950 or 1300)
      local l=self:GetVisualPos()+point(0,0,height)
      cameraTac.SetCamera(l+Rotate(point(0,-2300,550),self:GetAngle()),l,0)
      Sleep(120000)
    end)
    return "scheduled:"..id
  elseif op=="turn" then
    local u=unit();u:SetAngle(u:GetAngle()+(tonumber(id) or 10800));return "turned"
  elseif op=="view" then
    local u=unit();local l=u:GetVisualPos()+point(0,0,1250)
    cameraTac.SetCamera(l+Rotate(point(0,tonumber(id) or 2300,550),u:GetAngle()),l,0)
    return "camera repositioned"
  elseif op=="inspect" then
    local u=unit();local w=u:GetItemInSlot("Handheld A","Firearm")
    return record(w,"inspect").."\nstate="..u:GetStateText()..";stance="..u.stance
  elseif op=="finish" then
    local u=g_Units[session];if IsValid(u) then u:SetCommand("Idle") end
    ShowConsoleLog(true)
    return "QA unit left idle; no reload/save/pause"
  end
  error("Unknown operation")
end
