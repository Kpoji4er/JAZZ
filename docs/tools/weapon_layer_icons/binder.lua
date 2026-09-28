-- Engine-independent adapter prototype. All resources belong to a UI window,
-- never to the item. Dependencies are injected and exercised by offline tests.
local M = {}
function M.new(selector, registry, ui)
  local current_key, group
  local function clear()
    if group then ui.destroy(group) end
    group, current_key = nil, nil
  end
  local function fallback(item, reason)
    clear()
    ui.fallback(item) -- production: existing GetItemUIIcon() or Icon binding
    return false, reason
  end
  return {
    bind = function(item)
      if not item then clear(); ui.empty(); return false, "no-item" end
      local plan, reason = selector.resolve(registry, item)
      if not plan then return fallback(item, reason) end
      -- Check even when key is unchanged: texture resources may be unloaded.
      for _, layer in ipairs(plan.layers) do
        if not ui.available(layer.image) then return fallback(item, "unavailable-image") end
      end
      if current_key == plan.key then return true end
      -- Build a hidden complete subtree before replacing the displayed subtree.
      local next_group = ui.create_hidden(plan)
      if not next_group then return fallback(item, "creation-failed") end
      clear()
      group, current_key = next_group, plan.key
      ui.show(group)
      return true
    end,
    close = clear,
  }
end
return M
