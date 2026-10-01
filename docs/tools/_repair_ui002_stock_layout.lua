-- Run with weapon_layer_icons/live.py in the isolated ModEditor debug process.
-- Official editor transaction; back up generated files before dispatch.
local mod = assert(Mods.e6L4ECj)
assert(Platform.debug and GetMapName() == "ModEditor", "isolated editor required")
assert(mod:ItemsLoaded() and not mod:IsItemsFileModified(), "reload external changes first")
local target
mod:ForEachModItem(function(item)
  if IsKindOf(item, "ModItemXTemplate") and item.id == "UIWeaponDisplay" then target = item end
end)
assert(target and not target:GetCodeFileName(), "unexpected template storage")
local edits = 0
local function visit(node)
  if node.comment == "weapon" and type(node.run_after) == "function" then
    local name, params, body = GetFuncSource(node.run_after)
    if type(body) == "table" then body = table.concat(body, "\n") end
    local anchor = "local sideButtonsSize = 0"
    local first, last = body:find(anchor, 1, true)
    if body:find("hasToggle and -27", 1, true) then
      edits = edits + 1 -- Offline fix already present: only perform the round-trip.
    elseif first then
      local indent = body:match("([ \t]*)local sideButtonsSize") or ""
      local lines = {
        "-- Keep the extra toggle column inside the vanilla HUD width.",
        "local unit = Selection and Selection[1]",
        "local foldAction, foldState = JazzResolveFoldStockAction(unit)",
        "local flashAction, flashState = JazzResolveFlashlightAction(unit)",
        "local hasToggle = (foldAction and foldState ~= \"hidden\") or (flashAction and flashState ~= \"hidden\")",
        "local sideButtonsSize = i == 1 and hasToggle and -27 or 0",
      }
      local fn, err = CompileFunc(name, params,
        body:sub(1, first - 1) .. table.concat(lines, "\n" .. indent) .. body:sub(last + 1),
        "JAZZ UI-002 stock column width")
      assert(not err, tostring(err))
      node:SetProperty("run_after", fn)
      ObjModified(node)
      edits = edits + 1
    end
  end
  for _, child in ipairs(node) do if type(child) == "table" then visit(child) end end
end
visit(target)
assert(edits == 1, "expected exactly one equipped weapon callback")
local version = mod.version
mod:SaveWholeMod()
assert(mod.version == version + 1 and not mod:IsItemsFileModified(), "save failed")
mod:UnloadItems()
mod:LoadItems()
local found = 0
local function verify(node)
  if node.comment == "weapon" and type(node.run_after) == "function"
      and GetFuncSourceString(node.run_after):find("hasToggle and -27", 1, true) then found = found + 1 end
  for _, child in ipairs(node) do if type(child) == "table" then verify(child) end end
end
verify(XTemplates.UIWeaponDisplay)
assert(found == 1, "callback lost on reload")
return "PASS: official save/reload; one equipped callback; revision " .. mod.version
