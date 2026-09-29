-- Native XImage adapter. A window owns its layers; items and saves stay untouched.
local M = {}
local states=setmetatable({}, {__mode="k"})
local transparent=RGBA(255,255,255,0)
function M.clear(img)
  local state=states[img]
  if not state then return end
  if state.group and state.group.window_state~="destroying" then state.group:delete() end
  if img.ImageColor==transparent then img:SetImageColor(state.color) end
  if img.DisabledImageColor==transparent then img:SetDisabledImageColor(state.disabled_color) end
  states[img]=nil
end
function M.crop(plan)
  local b=plan.bounds;local width,height=plan.width,plan.height
  local padding=width==162 and 5 or 8
  local crop_width=math.max((b[3]-b[1]+4)*width/(width-2*padding),(b[4]-b[2]+4)*height/(height-2*padding)*width/height)
  local crop_height=crop_width*height/width
  local cx,cy=(b[1]+b[3])/2,(b[2]+b[4])/2
  return {math.floor(cx-crop_width/2),math.floor(cy-crop_height/2),math.ceil(cx+crop_width/2),math.ceil(cy+crop_height/2)}
end
function M.bind(img,item,registry,selector)
  if not img or img.window_state=="destroying" then return false end
  local plan=selector.resolve(registry,item)
  if not plan then M.clear(img);return false end
  for _,layer in ipairs(plan.layers) do
    UIL.RequestImage(layer.image)
    local w,h=UIL.MeasureImage(layer.image)
    if not w or w<=0 or not h or h<=0 then M.clear(img);return false end
  end
  local state=states[img]
  local color=state and img.ImageColor==transparent and state.color or img.ImageColor
  local disabled_color=state and img.DisabledImageColor==transparent and state.disabled_color or img.DisabledImageColor
  local style=table.concat({tostring(img.ImageScale),tostring(img.ImageFit),tostring(color),tostring(disabled_color),tostring(img.Desaturation),tostring(img.DisabledDesaturation),tostring(img.Angle),tostring(img.FlipX),tostring(img.FlipY)},"|")
  if state and state.key==plan.key and state.style==style then return true end
  local group=XControl:new({Id="idJazzNativeWeaponLayers",Dock="box",HandleMouse=false,Visible=false,ZOrder=1},img)
  local crop=M.crop(plan)
  local rect=box(crop[1],crop[2],crop[3],crop[4])
  local sx,sy=1000,1000
  if img.ImageScale then sx,sy=img.ImageScale:xy() end
  local scale=point(math.floor(plan.width*sx/(crop[3]-crop[1])),math.floor(plan.height*sy/(crop[4]-crop[2])))
  -- First draw all dark silhouettes, then all color layers: joints get no outline.
  for pass=1,2 do
    for _,layer in ipairs(plan.layers) do
      XImage:new({Dock="box",HandleMouse=false,Image=layer.image,
        ImageRect=rect,ImageFit=img.ImageFit,ImageScale=scale,
        ImageColor=pass==1 and RGB(5,6,7) or color,
        DisabledImageColor=pass==1 and RGBA(5,6,7,160) or disabled_color,
        Desaturation=img.Desaturation,DisabledDesaturation=img.DisabledDesaturation,
        Angle=img.Angle,FlipX=img.FlipX,FlipY=img.FlipY,
        EffectType=pass==1 and "outline" or "none",EffectPixels=pass==1 and 2 or 0,
        EffectColor=RGB(5,6,7)},group)
    end
  end
  M.clear(img)
  states[img]={key=plan.key,style=style,group=group,color=color,disabled_color=disabled_color}
  img:SetImageColor(transparent);img:SetDisabledImageColor(transparent)
  group:SetEnabled(img:GetEnabled())
  if img.window_state=="open" then group:Open() end
  group:SetVisible(true)
  return true
end
return M
