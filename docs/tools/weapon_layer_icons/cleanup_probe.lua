-- Read-only after the final batch; no scene mutation.
local rows={}
local center=point(150000,150000,150000)
MapForEach("map","CObject",function(o)
  local pos=o:GetPos()
  if pos and pos:IsValidZ() and pos:Dist(center)<12000 then
    rows[#rows+1]={class=o.class,entity=o:GetEntity(),position=tostring(pos)}
  end
end)
local state={map=GetMapName(),camera=ValueToLuaCode({GetCamera()}),
  light=CurrentLightmodel[1].id,time_factor=GetTimeFactor(),capture_area_objects=rows,
  render={terrain=hr.RenderTerrain,sky=hr.RenderSky,particles=hr.RenderParticles,
    clutter=hr.RenderClutter,rain=hr.RenderRain,auto_exposure=hr.AutoExposureMode}}
local err,text=LuaToJSON(state)
if err then return err end
return text
