local rows={}
for _,w in ipairs(GetChildrenOfKind(terminal.desktop,'XImage')) do
 local path=w:GetImage()
 if path and path:find('WeaponIcons/Live/',1,true) then
  rows[#rows+1]={path=path,box=tostring(w.box),size=tostring(w.measure_width)..'x'..tostring(w.measure_height)}
 end
end
local err,json=LuaToJSON(rows);return json
