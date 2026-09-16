"""Run the real region tooltip with strict translation-argument mocks."""
from pathlib import Path
from lupa import LuaRuntime

root = Path(__file__).resolve().parents[2]
source = (root / 'Code/Regions_Sectors.lua').read_text(encoding='utf-8')
body = source[source.index('function Region:GetRolloverHint('):source.index('function Region:GetRuntimeState(')]
lua = LuaRuntime()
lua.execute('''
Region={}; gv_Sectors={}; g_RevealedSectors={}
function Untranslated(s) return {text=s} end
function T(t)
 if t[1]==227814808041 then
  assert(type(t.Description)=='table', 'plain text reached translation')
  seen=t.Description; count=count+1
 end
 return 'translated'
end
''')
lua.execute(body)
lua.execute('''
for _,value in ipairs({'saved plain description', {text='localized'}, '', false}) do
 local original=value or nil
 local region={Description=original,GetHeat=function() return 0 end}
 count=0;seen=nil
 Region.GetRolloverHint(region,'D7')
 assert(region.Description==original)
 if original and original~='' then
  assert(count==1)
  if type(original)=='string' then assert(seen.text==original)
  else assert(seen==original) end
 else assert(count==0) end
end
''')
print('PASS: plain/localized/empty/nil description, no source mutation')
