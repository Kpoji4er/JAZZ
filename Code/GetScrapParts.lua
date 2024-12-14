function ItemWithCondition:AmountOfScrapPartsFromItem()
	local parts = self:GetScrapParts()
	if self.Condition and self.Condition < 50 then
		parts = parts / 20
        --if parts < 1 then parts = 1 end
	end
    --print(parts)
    if parts < 1 then parts = 1 end
	return parts
end

function FirearmBase:GetScrapParts()
	local parts = InventoryItem.GetScrapParts(self)
	parts = parts + (#(self.components or empty_table) * const.Weapons.UpgradeScrapParts)
    if self.Condition and self.Condition < 50 then
		parts = parts / 20
       -- if parts < 1 then parts = 1 end
	end
    --print(parts)
    if parts < 1 then parts = 1 end
	return parts
end