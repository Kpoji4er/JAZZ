-- Read-only editor/runtime template provenance before a scoped UI transaction.
local mod=Mods.e6L4ECj
local out={version=mod.version,items_loaded=mod:ItemsLoaded(),external_items_changed=mod:IsItemsFileModified(),templates={}}
mod:ForEachModItem(function(item)
  if IsKindOf(item,"ModItemXTemplate") and item.id=="UIWeaponDisplay" then
    local row={id=item.id,code=item:GetCodeFileName(),save=item:GetSavePath(),callbacks={}}
    local function visit(node)
      if type(node.run_after)=="function" then
        local info=debug.getinfo(node.run_after,"S")
        row.callbacks[#row.callbacks+1]={comment=node.comment,line=info.linedefined,source=info.source}
      end
      for _,child in ipairs(node) do if type(child)=="table" then visit(child) end end
    end
    visit(item);out.templates[#out.templates+1]=row
  end
end)
return ValueToLuaCode(out)
