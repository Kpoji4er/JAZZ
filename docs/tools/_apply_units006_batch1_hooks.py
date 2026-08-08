# -*- coding: utf-8 -*-
from pathlib import Path

meta_path = Path("metadata.lua")
meta = meta_path.read_text(encoding="utf-8")
needle = '"Code/System_OR_Weapons.lua",'
ins = '"Code/System_OR_Weapons.lua",\n\t\t"Code/System_NamedPerks_006.lua",'
if "System_NamedPerks_006" in meta:
    print("already registered")
elif needle in meta:
    meta_path.write_text(meta.replace(needle, ins, 1), encoding="utf-8")
    print("inserted System_NamedPerks_006")
else:
    print("FAIL: needle missing")

# Vince wrap in Systems_Medicine — patch JazzConsumeInventoryItem
med = Path("Code/Systems_Medicine.lua")
text = med.read_text(encoding="utf-8")
old = """function JazzConsumeInventoryItem(unit, class_id, amount)
	local item = JazzFindInventoryItem(unit, class_id)
	if not item then
		return false
	end
	amount = amount or 1
"""
new = """function JazzConsumeInventoryItem(unit, class_id, amount)
	-- UNITS-006 Vince: 25% chance to skip one med charge when Vince is in the squad
	if type(Jazz_VinceShouldSkipMedConsume) == "function" and Jazz_VinceShouldSkipMedConsume(unit) then
		return true
	end
	local item = JazzFindInventoryItem(unit, class_id)
	if not item then
		return false
	end
	amount = amount or 1
"""
if "Jazz_VinceShouldSkipMedConsume" in text:
    print("Vince consume already patched")
elif old in text:
    med.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("patched JazzConsumeInventoryItem for Vince")
else:
    print("FAIL: JazzConsumeInventoryItem pattern missing")
