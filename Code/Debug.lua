function Firearm:__toluacode(indent, pstr, GetPropFunc)
	return self:SaveToLuaCode(indent, pstr, GetPropFunc)
end

---
--- Saves the Firearm object to Lua code representation.
---
--- @param indent string The indentation string to use for nested structures.
--- @param pStr string|nil The string buffer to append the Lua code to.
--- @param GetPropFunc function|nil A function to get the property value for serialization.
--- @param pos number|nil The position of the Firearm object in the inventory.
--- @return string The Lua code representation of the Firearm object.
---
function Firearm:SaveToLuaCode(indent, pStr, GetPropFunc, pos)
	if not pStr then
		local additional
		if self.ammo then
			local ammo_props = self.ammo:SavePropsToLuaCode(indent, GetPropFunc)
			ammo_props = ammo_props or "nil"
			additional = string.format("\n\t 'ammo',PlaceInventoryItem('%s', %s)", self.ammo.class, ammo_props)
		end
		if next(self.subweapons) ~= nil then
			if additional then additional = string.format("%s,", additional) end
			additional = string.format("%s\n\t 'subweapons',{", additional or "")
			local additionalWeps = {}
			for slot, item in sorted_pairs(self.subweapons) do
				additionalWeps[#additionalWeps + 1] = string.format("\n\t\t['%s'] = %s", slot, item:__toluacode("\t\t\t", nil, GetPropFunc))
			end
			additional = string.format("%s%s%s", additional, table.concat(additionalWeps, ", "), "\n\t},")
		end

		local props = self:SavePropsToLuaCode(indent, GetPropFunc, pStr, additional)
		props = props or "nil"
		if pos then
			return string.format("%d, PlaceInventoryItem('%s', %s)", pos, self.class, props);
		else
			return string.format("PlaceInventoryItem('%s', %s)", self.class, props);
		end
	else
		local additional = pstr("", 1024)
		if self.ammo then
			additional:appendf("\n\t 'ammo',PlaceInventoryItem('%s', ", self.ammo.class)
			if not self.ammo:SavePropsToLuaCode(indent, GetPropFunc, additional) then
				additional:append("nil")
			end
			additional:append("),")
		end
		if next(self.subweapons) ~= nil then
			additional:append("\n\t 'subweapons',{")
			for slot, item in sorted_pairs(self.subweapons) do
				additional:appendf("\n\t\t['%s'] = %s", slot, item:__toluacode("\t\t\t", nil, GetPropFunc))
			end
			additional:append("\n\t},")
		end
		
		if pos then
			pStr:append(tostring(pos)..", " )
			pStr:appendf("PlaceInventoryItem('%s', ", self.class)
			if not self:SavePropsToLuaCode(indent, GetPropFunc, pStr, additional) then
				pStr:append("nil")
			end
			return pStr:append(") ")
		else
			pStr:appendf("PlaceInventoryItem('%s', ", self.class)
			if not self:SavePropsToLuaCode(indent, GetPropFunc, pStr, additional) then
				pStr:append("nil")
			end
			return pStr:append(") ")
		end
	end
end