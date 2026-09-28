UndefineClass('JAZZ_Legion_ArmorTest_LeatherArmor')
DefineClass.JAZZ_Legion_ArmorTest_LeatherArmor = {
    __parents = { "UnitData" },
    __generated_by_class = "ModItemUnitDataCompositeDef",

    comment = "JAZZ-APPEAR-001 TEST ONLY: leather carrier + MP40; not in campaign pools",
    object_class = "UnitData",
    Health = 85,
    Agility = 70,
    Dexterity = 70,
    Strength = 90,
    Wisdom = 50,
    Will = 60,
    Marksmanship = 70,
    MaxHitPoints = 85,
    Portrait = "Mod/Dv3mFVN/EnemyPortraits/Legion/Recruit.png",
    BigPortrait = "UI/Enemies/LegionRaider",
    Name = T(890000000001643, "Новобранец"),
    Affiliation = "Legion",
    gender = "Male",
    Randomization = false,
    archetype = "Assault",
    role = "Stormer",
    Equipment = {},
    AppearancesList = { PlaceObj('AppearanceWeight', { 'Preset', "LegionGoon" }) },
    CustomEquipGear = function(self, items)
        items[#items + 1] = PlaceInventoryItem("JazzArmor_LeatherArmor")
        items[#items + 1] = PlaceInventoryItem("MP40")
        local ammo = PlaceInventoryItem("JAZZ_AMMO_9x19_FMJ")
        ammo.Amount = 120
        items[#items + 1] = ammo
        self:TryEquip(items, "Torso", "Armor")
        self:TryEquip(items, "Handheld A", "Firearm")
        self:TryLoadAmmo("Handheld A", "Firearm", "JAZZ_AMMO_9x19_FMJ")
    end,
}
