LootEntryInventoryItem.properties[#LootEntryInventoryItem.properties + 1] = {
    category = "Loot",
    id = "Deterioration",
    name = "Износ",
    help = "Износ в %",
    editor = "number",
    default = 0,
    template = true,
    slider = true,
    min = 0,
    max = 100,
    modifiable = true
}

---
--- Generates loot items based on the properties of the `LootEntryInventoryItem` object.
---
--- The function first checks if the `generate_chance` property is less than or equal to 0, in which case it returns without generating any loot. If the `generate_chance` is less than 100, it generates a random number and checks if it is less than the `generate_chance`, returning if it is not.
---
--- The function then determines the amount of loot to generate based on the `stack_min` and `stack_max` properties. If `stack_min` is equal to `stack_max`, the amount is set to `stack_max`. Otherwise, a random number between `stack_min` and `stack_max` is generated.
---
--- If the `Double` property is true, the function has a chance to halve the amount of loot generated based on the `chanceToHalveDoubleLoot` value from the current game difficulty.
---
--- The function then generates the loot items, setting their `drop_chance` and `guaranteed_drop` properties based on the `LootEntryInventoryItem` object. If the item is a stack, the amount is set accordingly. If the item is not a stack, the function sets the item's condition based on the `Condition` and `RandomizeCondition` properties, and updates the `ItemGenerated` network hash.
---
--- @param looter table The entity that is looting
--- @param looted table The entity that is being looted
--- @param seed number The random seed to use for generating loot
--- @param items table The table to add the generated loot items to
function LootEntryInventoryItem:GenerateLoot(looter, looted, seed, items)
    -- exclude this item from generation
    if self.generate_chance <= 0 then
        return
    elseif self.generate_chance < 100 then
        local rand
        rand, seed = BraidRandom(seed, 100)
        if rand >= self.generate_chance then return end
    end

    -- stacks
    local amount
    local min, max = self:GetStackSize()
    if min >= max then
        amount = max
    else
        amount, seed = BraidRandom(seed, max - min + 1)
        amount = min + amount
    end

    if self.Double then
        local roll
        roll, seed = BraidRandom(seed, 100)
        local value = GameDifficulties[Game.game_difficulty]:ResolveValue(
                          "chanceToHalveDoubleLoot") or 0
        if roll < value then amount = amount / 2 end
    end

    local chance = self:GetDropChance()
    local maxPossibleWeaponCondPenalty = Game and
                                             GameDifficulties[Game.game_difficulty]:ResolveValue(
                                                 "maxPossibleWeaponCondPenalty") or
                                             0
    local lootConditionRandomization = const.Weapons.LootConditionRandomization
    while amount > 0 do
        local item = PlaceInventoryItem(self.item)
        item.drop_chance = chance
        item.guaranteed_drop = self.guaranteed
        if IsKindOf(item, "InventoryStack") then
            item.Amount = Min(amount, item.MaxStacks)
            amount = amount - item.Amount
        else
            amount = amount - 1
            local condition = self.Condition
            if self.RandomizeCondition then
                local rnd
                rnd, seed = BraidRandom(seed, 2 * lootConditionRandomization)
                local diffRnd = 0
                diffRnd, seed =
                    -(BraidRandom(seed, maxPossibleWeaponCondPenalty))
                condition = Clamp(
                                condition - lootConditionRandomization + rnd +
                                    diffRnd, 1, 100)
            end

            if IsKindOf(item, "Firearm") then
                item.WeaponResource = item:GetCurrentResource()
                item.WeaponResourceMax = item:GetMaxResource()        

                if self.Deterioration and self.Deterioration > 0 then
                    local deterioration = self.Deterioration
                    local maxResource = MulDivRound(item:GetMaxResource(),
                                                    100-deterioration, 100)
                    item.WeaponResourceMax = maxResource
                end

                local resource = MulDivRound(item.WeaponResourceMax, condition,
                                             100)
                item.WeaponResource = resource
                
            elseif IsKindOf(item, "Armor") then
                item.ArmorResource = item:GetCurrentResource()
                item.ArmorResourceMax = item:GetMaxResource()        

                if self.Deterioration and self.Deterioration > 0 then
                    local deterioration = self.Deterioration
                    local maxResource = MulDivRound(item:GetMaxResource(),
                    100-deterioration, 100)
                    item.ArmorResourceMax = maxResource
                end

                local resource = MulDivRound(item.ArmorResourceMax, condition,
                                             100)
                item.ArmorResource = resource
            else

                item.Condition = item:GetConditionPercent()
            end
            NetUpdateHash("ItemGenerated", item.class, item.Condition)
        end
        items[#items + 1] = item
    end
end
