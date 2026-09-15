"""Schedule disposable weapon component/visual checks in the live JA3 engine.

Leaves a report at AppData/jazz_weapon_import_smoke.txt; no player inventory edits.
"""
from pathlib import Path
import json
from _probe_weapon_imports_runtime import evaluate
body=Path(__file__).with_name('_runtime_weapon_imports.lua').read_text(encoding='utf-8')
expr='''(function()
 CreateGameTimeThread(function()
  local ign=SafeEvalStart("weapon-import-smoke")
  local ok,result=pcall(function()
'''+body+'''
  end)
  SafeEvalEnd(ign,"weapon-import-smoke")
  AsyncStringToFile("AppData/jazz_weapon_import_smoke.txt",ok and result or ("FAIL "..tostring(result)))
 end)
 return "Scheduled disposable weapon checks; no pause or inventory edits"
end)()'''
print(json.dumps(evaluate(expr),ensure_ascii=False,indent=2))
