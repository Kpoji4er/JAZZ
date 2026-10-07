-- JAZZ-WEAPON-SCAR-001. One inventory identity; native effects own numeric stats.
local function config(w)
    local c = w.components or empty_table
    local kit = c.Conversion
    local family = kit == "JAZZ_SCAR_SSR" and "SSR"
        or kit == "JAZZ_SCAR_H" and "H" or "L"
    local barrel = c.Barrel == "JAZZ_SCAR_BarrelShort" and "Short"
        or c.Barrel == "JAZZ_SCAR_BarrelLong" and "Long" or "Standard"
    return family, barrel
end

local function presentation(w)
    local family, barrel = config(w)
    local c = w.components or empty_table
    local class = family == "SSR" and "BattleRifle" or barrel == "Short" and "Carbine" or "AssaultRifle"
    local base = class == "BattleRifle" and BattleRifle or class == "Carbine" and Carbine or AssaultRifle
    w.object_class, w.WeaponType, w.ImpactForce = class, base.WeaponType, base.ImpactForce
    local ancestors = {}
    for k, v in pairs(SCAR.__ancestors) do ancestors[k] = v end
    ancestors.AssaultRifle, ancestors.Carbine, ancestors.BattleRifle = nil, nil, nil
    ancestors[class] = true
    w.__ancestors = ancestors
    w.AvailableAttacks = family == "SSR" and { "SingleShot" }
        or { "SingleShot", "BurstFire", "AutoFire", class == "Carbine" and "RunAndGun_Carbine" or "JAZZ_TargetSweep" }
    w.WeaponSizeClass = family == "SSR" and "Long" or barrel == "Short" and "Carbine" or "Long"
    local suffix = family == "SSR" and "SSR" or family .. "_" .. barrel
    w.Entity = "JAZZ_SCAR_" .. suffix
    w.Icon = "Mod/e6L4ECj/WeaponIcons/SCAR_" .. suffix
        .. (family ~= "SSR" and c.Stock == "JAZZ_SCAR_StockFolded" and "_Folded" or "") .. ".png"
    local kit = WeaponComponents[c.Conversion or "JAZZ_SCAR_L"]
    w.DisplayName = kit and kit.DisplayName or SCAR.DisplayName
    w.DisplayNamePlural = w.DisplayName
end

function SCAR:Setcomponents(components)
    self.components = components
    presentation(self)
end

function SCAR:SetWeaponComponent(slot, id, is_init)
    local def = WeaponComponents[id]
    slot = slot or (def and def.Slot)
    local family = config(self)
    if slot == "Conversion" then
        if id ~= "JAZZ_SCAR_L" and id ~= "JAZZ_SCAR_H" and id ~= "JAZZ_SCAR_SSR" then return false end
        if self.components and self.components.Conversion == id and not is_init then return end
        -- Native caliber changes unload ammunition. Reject ownerless changes
        -- before any mutation; clones use the native non-destructive path.
        if self.ammo and not is_init and not rawget(self, "is_clone") then
            local owner = gv_UnitData and gv_UnitData[self.owner]
            if not owner or not GetSquadBagInventory(owner.Squad) then return false end
        end
    elseif slot == "Barrel" then
        if id ~= "JAZZ_SCAR_BarrelShort" and id ~= "JAZZ_SCAR_BarrelNormal" and id ~= "JAZZ_SCAR_BarrelLong" then return false end
        if family == "SSR" then id = "JAZZ_SCAR_BarrelLong" end
    elseif slot == "Stock" and family == "SSR" then
        id = "JAZZ_SCAR_Stock"
    end
    FirearmBase.SetWeaponComponent(self, slot, id, is_init)
    if slot == "Conversion" and self.components.Conversion == "JAZZ_SCAR_SSR" then
        FirearmBase.SetWeaponComponent(self, "Barrel", "JAZZ_SCAR_BarrelLong", is_init)
        FirearmBase.SetWeaponComponent(self, "Stock", "JAZZ_SCAR_Stock", is_init)
    end
    presentation(self)
    if not is_init and not rawget(self, "is_clone") and JazzWeaponIcon_ScheduleWeaponDisplayRefresh then
        JazzWeaponIcon_ScheduleWeaponDisplayRefresh()
    end
end

function SCAR:UpdateVisualObj(vis)
    presentation(self)
    vis = vis or self.visual_obj
    if not IsValid(vis) or vis.weapon ~= self then return end
    if vis:GetEntity() ~= self.Entity then vis:ChangeEntity(self.Entity) end
    FirearmBase.UpdateVisualObj(self, vis)
    local family, barrel = config(self)
    local parts = vis.parts or empty_table
    if IsValid(parts.Magazine) then
        parts.Magazine:ChangeEntity("JAZZ_SCAR_" .. (family == "L" and "L" or "H") .. "_Magazine")
    end
    if IsValid(parts.Stock) then
        local suffix = family == "SSR" and "StockSSR"
            or self.components.Stock == "JAZZ_SCAR_StockFolded" and "StockFolded" or "Stock"
        parts.Stock:ChangeEntity("JAZZ_SCAR_" .. suffix)
    end
    if IsValid(parts.Muzzle) then
        local delta = (family == "SSR" or barrel == "Long") and 102 or barrel == "Short" and -102 or 0
        if self.components.Muzzle == "JAZZ_SCAR_Muzzle" then
            parts.Muzzle:ChangeEntity("JAZZ_SCAR_" .. (family == "L" and "L" or "H") .. "_Muzzle")
            parts.Muzzle:SetAttachOffset(point(delta, 0, 0))
        else
            parts.Muzzle:SetAttachOffset(point((family == "L" and 487 or 563) + delta, 4, 84))
        end
    end
    if IsValid(parts.Side) then
        parts.Side:SetAttachAxis(point(4096, 0, 0))
        parts.Side:SetAttachAngle(-5400)
    end
end
