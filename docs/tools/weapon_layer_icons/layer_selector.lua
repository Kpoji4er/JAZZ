-- Pure resolver for native photographed layers. No globals or engine mutation.
local M = {}
local function matches(when, values)
  local count=0
  for slot,id in pairs(when or {}) do
    if values[slot]~=id then return false,0 end
    count=count+1
  end
  return true,count
end
function M.resolve(registry,item)
  local profile=item and registry.weapons[item.class]
  if not profile then return nil,"unsupported-weapon" end
  local values,parts={},{}
  for _,slot in ipairs(profile.slots) do
    local value=item.components and item.components[slot.slot]
    if value==nil then value=slot.default end
    if value==false then value="" end
    if not slot.options[value] then return nil,"unknown-component:"..tostring(slot.slot) end
    values[slot.slot]=value
  end
  local rail_slots={Dovetail=true,Rail=true,RailSide=true,Conversion=true}
  for slot,value in pairs(item.components or {}) do
    if values[slot]==nil and value and value~="" and not rail_slots[slot] then return nil,"unknown-slot:"..slot end
  end
  for spot,entity in pairs(profile.base) do parts[spot]=entity end
  for _,slot in ipairs(profile.slots) do
    local rule=profile.rules[slot.slot] and profile.rules[slot.slot][values[slot.slot]]
    if not rule then return nil,"missing-component-rule:"..tostring(slot.slot) end
    for spot,entity in pairs(rule) do parts[spot]=entity or nil end
  end
  for _,override in ipairs(profile.overrides or {}) do
    if matches(override.when,values) then
      for spot,entity in pairs(override.parts) do parts[spot]=entity or nil end
    end
  end
  local host=item.Entity or parts.__host
  parts.__host=host
  local art=profile.art[host]
  if not art then return nil,"unknown-host" end
  local chosen,visiting={},{}
  local function choose(spot)
    if chosen[spot] then return chosen[spot] end
    if visiting[spot] then return nil end
    visiting[spot]=true
    local candidates=art[spot] and art[spot][parts[spot]]
    local best,best_score=nil,-1
    for _,candidate in ipairs(candidates or {}) do
      local ok,score=matches(candidate.when,values)
      if ok and candidate.parent then
        ok=parts[candidate.parent]~=nil and choose(candidate.parent)==candidate.parent_id
      end
      if ok and score>best_score then best,best_score=candidate.id,score end
    end
    visiting[spot]=nil
    chosen[spot]=best
    return best
  end
  local layers,nodes,seen={},{},{}
  local bounds={math.huge,math.huge,-math.huge,-math.huge}
  for spot in pairs(parts) do
    local id=choose(spot)
    local layer=id and registry.layers[id]
    if not layer then return nil,"missing-art:"..spot end
    if not seen[id] then
      seen[id]=true;nodes[#nodes+1]=id
      if layer.image and layer.bounds then
        layers[#layers+1]={id=id,image=layer.image,z=layer.z,bounds=layer.bounds}
        for i=1,2 do bounds[i]=math.min(bounds[i],layer.bounds[i]) end
        for i=3,4 do bounds[i]=math.max(bounds[i],layer.bounds[i]) end
      end
    end
  end
  table.sort(layers,function(a,b) return a.z==b.z and a.id<b.id or a.z<b.z end)
  if #layers==0 then return nil,"empty-assembly" end
  table.sort(nodes)
  local key={registry.revision,item.class,host}
  for _,layer in ipairs(layers) do key[#key+1]=layer.id end
  return {layers=layers,nodes=nodes,key=table.concat(key,"|"),bounds=bounds,width=profile.width,height=profile.height}
end
return M
