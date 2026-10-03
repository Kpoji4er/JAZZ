-- JAZZ-WEAPON-HK416-001: one item, authored receiver/barrel configurations.
local function presentation(weapon)
    local c = weapon.components or empty_table
    local variant = c.Barrel == "JAZZ_HK416_BarrelShort" and "Short"
        or c.Barrel == "JAZZ_HK416_BarrelLong" and "Long" or "Standard"
    weapon.Entity = "JAZZ_HK416_" .. variant
    weapon.Icon = "Mod/e6L4ECj/WeaponIcons/HK416_" .. variant
        .. (c.Stock == "JAZZ_HK416_StockCTR" and "_CTR" or "") .. ".png"
end

function HK416:Setcomponents(components)
    self.components = components
    presentation(self)
end

function HK416:SetWeaponComponent(slot, id, is_init)
    local def = WeaponComponents[id]
    slot = slot or (def and def.Slot)
    if slot == "Barrel" and id ~= "JAZZ_HK416_BarrelNormal"
        and id ~= "JAZZ_HK416_BarrelShort" and id ~= "JAZZ_HK416_BarrelLong" then
        return false
    end
    if slot == "Stock" and id ~= "JAZZ_HK416_Stock" and id ~= "JAZZ_HK416_StockCTR" then
        return false
    end
    FirearmBase.SetWeaponComponent(self, slot, id, is_init)
    presentation(self)
    if not is_init and not rawget(self, "is_clone") and JazzWeaponIcon_ScheduleWeaponDisplayRefresh then
        JazzWeaponIcon_ScheduleWeaponDisplayRefresh()
    end
end

function HK416:UpdateVisualObj(vis)
    presentation(self)
    vis = vis or self.visual_obj
    if not IsValid(vis) or vis.weapon ~= self then return end
    if vis:GetEntity() ~= self.Entity then vis:ChangeEntity(self.Entity) end
    FirearmBase.UpdateVisualObj(self, vis)
end
