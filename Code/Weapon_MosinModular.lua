-- JAZZ-WEAPON-MOSIN-001: Barrel selects a complete historical configuration.
-- Only the existing Mosin weapon class changes; generic firearm methods remain untouched.
local configurations = {
    JAZZ_Mosin1891 = { entity = "MOSIN_1891", size = "Long" },
    JAZZ_MosinM38 = { entity = "MOSIN_M38", size = "Carbine" },
    JAZZ_MosinObrez = { entity = "MOSIN_Obrez", size = "Compact" },
}

local function update_configuration_name(weapon)
    local id = weapon.components and weapon.components.Barrel
    local component = id and WeaponComponents[id]
    local standard = not id or id == "JAZZ_Mosin1891"
    weapon.DisplayName = standard and Mosin.DisplayName or (component and component.DisplayName or Mosin.DisplayName)
    weapon.DisplayNamePlural = standard and Mosin.DisplayNamePlural or weapon.DisplayName
end

local function configuration(weapon)
    return configurations[weapon.components and weapon.components.Barrel] or configurations.JAZZ_Mosin1891
end

function Mosin:SetWeaponComponent(slot, id, is_init)
    local component = WeaponComponents[id]
    slot = slot or (component and component.Slot)
    -- The cabinet blocks this choice; direct callers and initialization must
    -- obey the same rule regardless of component assignment order.
    if slot == "Scope" and configuration(self) ~= configurations.JAZZ_Mosin1891 then
        id = false
    end
    FirearmBase.SetWeaponComponent(self, slot, id, is_init)
    update_configuration_name(self)
    local current = configuration(self)
    self.Entity = current.entity
    self.WeaponSizeClass = current.size
    self.Icon = "Mod/e6L4ECj/WeaponIcons/" .. current.entity .. ".png"
end

function Mosin:UpdateVisualObj(vis)
    vis = vis or self.visual_obj
    if not IsValid(vis) or vis.weapon ~= self then return end
    update_configuration_name(self)
    local current = configuration(self)
    if vis:GetEntity() ~= current.entity then
        vis:ChangeEntity(current.entity)
    end
    FirearmBase.UpdateVisualObj(self, vis)
end
