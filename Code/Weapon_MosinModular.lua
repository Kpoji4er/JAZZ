-- JAZZ-WEAPON-MOSIN-001: Barrel selects a complete historical configuration.
-- Only the existing Mosin weapon class changes; generic firearm methods remain untouched.
local configurations = {
    JAZZ_Mosin1891 = { entity = "MOSIN_1891", size = "Long" },
    JAZZ_MosinM38 = { entity = "MOSIN_M38", size = "Carbine" },
    JAZZ_MosinObrez = { entity = "MOSIN_Obrez", size = "Compact" },
}

local function configuration(weapon)
    return configurations[weapon.components and weapon.components.Barrel] or configurations.JAZZ_Mosin1891
end

function Mosin:SetWeaponComponent(slot, id, is_init)
    FirearmBase.SetWeaponComponent(self, slot, id, is_init)
    local current = configuration(self)
    self.Entity = current.entity
    self.WeaponSizeClass = current.size
    self.Icon = "Mod/e6L4ECj/WeaponIcons/" .. current.entity .. ".png"
end

function Mosin:UpdateVisualObj(vis)
    vis = vis or self.visual_obj
    if not IsValid(vis) or vis.weapon ~= self then return end
    local current = configuration(self)
    if vis:GetEntity() ~= current.entity then
        vis:ChangeEntity(current.entity)
    end
    FirearmBase.UpdateVisualObj(self, vis)
end
