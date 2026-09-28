local result={}
for _,id in ipairs({"GetCamera","WaitCaptureScreenshot","LuaToJSON","TableToJSON","PlaceInventoryItem","SetLightmodel","SetCamera","GetTimeFactor"}) do
  result[#result+1]=id.."="..type(_G[id])
end
result[#result+1]="map="..GetMapName()
result[#result+1]="time="..GetTimeFactor()
result[#result+1]="camera="..ValueToLuaCode({GetCamera()})
result[#result+1]="light="..ValueToLuaCode(CurrentLightmodel and CurrentLightmodel[1])
return table.concat(result,"\n")
