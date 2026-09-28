-- Offline module: no globals, hooks, engine calls or writes to weapon instances.
-- The adapter must clear previous layers on BOTH success and fallback.
local M = {}
local function matches(when, components)
  for slot, id in pairs(when or {}) do
    if components[slot] ~= id then return false end
  end
  return true
end
local function token(s)
  s = tostring(s)
  return #s .. ":" .. s
end
function M.resolve(registry, weapon)
  local profile = registry.weapons[weapon.class]
  if not profile then return nil, "unsupported-weapon" end
  local components = {}
  for slot, definition in pairs(profile.slots) do
    local id = weapon.components and weapon.components[slot]
    if id == nil then id = definition.default or "" end
    if id == false then id = "" end
    if not definition.options[id] then return nil, "unsupported-component:" .. slot end
    components[slot] = id
  end
  for slot, id in pairs(weapon.components or {}) do
    if not profile.slots[slot] and id and id ~= "" then
      return nil, "unknown-slot:" .. slot
    end
  end
  local host = weapon.Entity or profile.host
  for _, rule in ipairs(profile.host_rules or {}) do
    if matches(rule.when, components) then host = rule.host; break end
  end
  local art = profile.hosts[host]
  if not art then return nil, "unsupported-host" end
  local plan, seen = {}, {}
  local function add(ids)
    for _, id in ipairs(ids) do
      local layer = art.layers[id]
      if not layer then return false end
      if not seen[id] then
        seen[id] = true
        plan[#plan + 1] = {id=id, image=layer.image, z=layer.z}
      end
    end
    return true
  end
  if not add(art.fixed or {}) then return nil, "missing-fixed-art" end
  local slots = {}
  for slot in pairs(profile.slots) do slots[#slots + 1] = slot end
  table.sort(slots)
  for _, slot in ipairs(slots) do
    local options = art.slots[slot]
    local bundle = options and options[components[slot]]
    if not bundle then return nil, "missing-art:" .. slot end
    local ids = bundle.layers
    for _, variant in ipairs(bundle.variants or {}) do
      if matches(variant.when, components) then ids = variant.layers; break end
    end
    if not ids or not add(ids) then return nil, "missing-variant:" .. slot end
  end
  table.sort(plan, function(a,b) return a.z == b.z and a.id < b.id or a.z < b.z end)
  local key = token(registry.revision) .. token(weapon.class) .. token(host)
  for _, layer in ipairs(plan) do
    key = key .. token(layer.id) .. token(layer.image) .. token(layer.z)
  end
  return {host=host, width=art.width, height=art.height, layers=plan, key=key}
end
return M
