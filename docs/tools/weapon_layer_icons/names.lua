-- Offline presentation-only prototype; labels are draft text, not game T IDs.
local M = {}
function M.resolve(catalog, item, language, plural)
  local fallback = plural and item.DisplayNamePlural or item.DisplayName
  fallback = fallback or item.DisplayName
  local profile = catalog.weapons[item.class]
  if not profile then return fallback, "base-name" end
  if item.Entity and item.Entity ~= profile.host then return fallback, "unknown-host" end
  local winner
  for _, rule in ipairs(profile.rules) do
    if rule.enabled ~= false then
      local match = true
      for slot, accepted in pairs(rule.when) do
        local component = item.components and item.components[slot]
        if component == nil then component = profile.defaults[slot] end
        if component == false then component = "" end
        if not accepted[component or ""] then match = false; break end
      end
      if match then
        if winner then return fallback, "ambiguous-rules" end
        winner = rule
      end
    end
  end
  if not winner then return fallback, "no-structural-match" end
  local label = winner.labels[language]
  if not label then return fallback, "untranslated" end
  return (plural and label.plural or label.singular), winner.id
end
return M
