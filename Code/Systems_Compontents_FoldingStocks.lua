--function OnMsg.DataLoaded()
AppendClass.WeaponComponent = {
  properties = {
	{ id = "zzFoldingPair", category = "Misc",
			name = "Fold/Unfold-Partner", editor = "preset_id_list", default = {}, preset_class = "WeaponComponent", item_default = "", }
  }
} 

PlaceObj('WeaponComponentEffect', {
    Description = "Складной приклад",
    group = "Other",
    id = "zzStockEquipped",
})
