-- JAZZ-WEAPON-AEK-001. Native component effects own caliber and numeric stats.
local function configuration(weapon)
    return weapon.components and weapon.components.Barrel == "JAZZ_AEK_762" and "973S" or "971"
end

local function presentation(weapon)
    local variant = configuration(weapon)
    local component = WeaponComponents[variant == "973S" and "JAZZ_AEK_762" or "JAZZ_AEK_545"]
    weapon.DisplayName = component and component.DisplayName or AEK971.DisplayName
    weapon.DisplayNamePlural = weapon.DisplayName
    weapon.Entity = "JAZZ_AEK" .. variant
    local folded = weapon.components and weapon.components.Stock == "JAZZ_StockLightFolded"
    weapon.Icon = "Mod/e6L4ECj/WeaponIcons/AEK" .. variant .. (folded and "_Folded" or "") .. ".png"
end

function AEK971:Setcomponents(components)
    self.components = components
    presentation(self)
end

function AEK971:SetWeaponComponent(slot, id, is_init)
    local def = WeaponComponents[id]
    slot = slot or (def and def.Slot)
    if slot == "Barrel" then
        if id ~= "JAZZ_AEK_545" and id ~= "JAZZ_AEK_762" then return false end
        if not is_init and self.components and self.components.Barrel == id then return end
        -- Native ChangeCaliber cannot unload an ownerless weapon. Reject before
        -- touching components, caliber, modifiers or ammunition in that case.
        if self.ammo and not is_init and not rawget(self, "is_clone") then
            local owner = gv_UnitData and gv_UnitData[self.owner]
            if not owner or not GetSquadBagInventory(owner.Squad) then return false end
        end
    end
    FirearmBase.SetWeaponComponent(self, slot, id, is_init)
    presentation(self)
    if not is_init and not rawget(self, "is_clone") and JazzWeaponIcon_ScheduleWeaponDisplayRefresh then
        JazzWeaponIcon_ScheduleWeaponDisplayRefresh()
    end
end

function AEK971:UpdateVisualObj(vis)
    presentation(self)
    vis = vis or self.visual_obj
    if not IsValid(vis) or vis.weapon ~= self then return end
    if vis:GetEntity() ~= self.Entity then vis:ChangeEntity(self.Entity) end
    FirearmBase.UpdateVisualObj(self, vis)

    -- Post-release attachment fit: AKM adapter, with taller 973S receiver.
    local mount = vis.parts and vis.parts.Mount
    local scope = vis.parts and vis.parts.Scope
    if IsValid(mount) and mount:GetEntity() == "WeaponAttA_MountAK47" then
        local lift = configuration(self) == "973S" and 28 or 0
        mount:SetAttachOffset(point(13, 0, -40 + lift))
        if IsValid(scope) then scope:SetAttachOffset(point(0, 0, 26 + lift)) end
    end
    -- Both source variants use their own magazine and stock meshes. Their
    -- compiled attachment spots share the body origin, preserving exact fit.
    local variant = configuration(self)
    local magazine = vis.parts and vis.parts.Magazine
    if IsValid(magazine) then magazine:ChangeEntity("JAZZ_AEK" .. variant .. "_Magazine") end
    local stock = vis.parts and vis.parts.Stock
    if IsValid(stock) then
        local folded = self.components.Stock == "JAZZ_StockLightFolded"
        stock:ChangeEntity("JAZZ_AEK" .. variant .. (folded and "_StockFolded" or "_Stock"))
    end
end
