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
    local conversion = weapon.components and weapon.components.Conversion
    if standard and conversion == "JAZZ_Conversion_Mosin" then
        local piece = WeaponComponents[conversion]
        weapon.DisplayName = piece and piece.DisplayName or Mosin.DisplayName
        weapon.DisplayNamePlural = piece and (piece.DisplayNamePlural or piece.DisplayName) or Mosin.DisplayNamePlural
        return
    end
    weapon.DisplayName = standard and Mosin.DisplayName or (component and component.DisplayName or Mosin.DisplayName)
    weapon.DisplayNamePlural = standard and Mosin.DisplayNamePlural or weapon.DisplayName
end

local function configuration(weapon)
    return configurations[weapon.components and weapon.components.Barrel] or configurations.JAZZ_Mosin1891
end

local function update_configuration_class(weapon)
    local short = configuration(weapon) ~= configurations.JAZZ_Mosin1891
    local base = short and BattleRifle or SniperRifle
    weapon.WeaponType = base.WeaponType
    weapon.object_class = short and "BattleRifle" or "SniperRifle"
    weapon.ImpactForce = base.ImpactForce
    weapon.AvailableAttacks = short and { "SingleShot", "JAZZ_Salvo" }
        or { "SingleShot", "JAZZ_JokerShot", "JAZZ_Bullseye" }
    -- Keep the inventory ID/metatable Mosin for serialization, FX and component
    -- matching. Never mutate its shared ancestry (other Mosins may be long).
    local ancestors = {}
    for name, value in pairs(Mosin.__ancestors) do
        ancestors[name] = value
    end
    ancestors.SniperRifle = not short or nil
    ancestors.BattleRifle = short or nil
    weapon.__ancestors = ancestors
end

-- PlaceInventoryItem/UIClone restore the components property through its setter.
function Mosin:Setcomponents(components)
    self.components = components
    update_configuration_name(self)
    update_configuration_class(self)
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
    update_configuration_class(self)
    local current = configuration(self)
    self.Entity = current.entity
    self.WeaponSizeClass = current.size
    self.Icon = "Mod/e6L4ECj/WeaponIcons/" .. current.entity .. ".png"
end

function Mosin:UpdateVisualObj(vis)
    update_configuration_class(self)
    vis = vis or self.visual_obj
    if not IsValid(vis) or vis.weapon ~= self then return end
    update_configuration_name(self)
    local current = configuration(self)
    if vis:GetEntity() ~= current.entity then
        vis:ChangeEntity(current.entity)
    end
    FirearmBase.UpdateVisualObj(self, vis)
end
