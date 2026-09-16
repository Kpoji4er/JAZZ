"""MED-009: real eligibility installer and treatment progress in isolated Lua."""
from pathlib import Path
from lupa import LuaRuntime

root = Path(__file__).resolve().parents[2]
source = (root / 'Code/System_Wounds_OperationHeal.lua').read_text(encoding='utf-8')
eligibility = source[:source.index('-- Vanilla OperationMerc Patient UI')]
progress = source[source.index('function PatientAddHealWoundProgress('):]
lua = LuaRuntime()
lua.execute('''
empty_table={}; JazzTraumaZones={'Arm'}
function JazzGetTraumaTier(u) return u.trauma and 1 end
function JazzTraumaIsHealing(e) return e.healing end
function JazzMarkUnitTraumasHealing(u) if u.trauma then u.trauma.healing=true end end
function IsPatient(u) return u.Operation=='HospitalTreatment' end
function IsGameRuleActive() return false end
function PlayVoiceResponse() end
Min=math.min; const={utNormal=0}
function CombatLog() end
function T(t) return t end
sentinel=function() return 'preserved' end
function hospital()
 return {FilterAvailable=function() return false end,IsEnabled=sentinel,
 GetOperationCost=sentinel,Tick=sentinel,GetSectorSlots=sentinel}
end
SectorOperations={HospitalTreatment=hospital()}
function patient(hp,trauma,dead)
 return {HitPoints=hp,MaxHitPoints=100,trauma=trauma,dead=dead,
 Operation='HospitalTreatment',heal_wound_progress=0,wounds_being_treated=0,Tiredness=0,
 IsDead=function(self) return self.dead end,
 GetStatusEffect=function(self,id) if id=='TraumaArm1' then return self.trauma end end,
 RemoveStatusEffect=function(self,id) assert(id~='TraumaArm1') end,
 SetTired=function() end}
end
''')
lua.execute(eligibility + '\ninstall=JazzInstallTreatWoundsEligibility\n' + progress)
lua.execute('''
install();install()
local h=SectorOperations.HospitalTreatment
assert(h.IsEnabled==sentinel and h.GetOperationCost==sentinel and h.Tick==sentinel and h.GetSectorSlots==sentinel)
assert(h:FilterAvailable(patient(100,{})))
assert(h:FilterAvailable(patient(90,nil)))
assert(not h:FilterAvailable(patient(100,nil)))
assert(not h:FilterAvailable(patient(90,{},true)))
assert(not h:FilterAvailable(patient(100,{healing=true})))
local u=patient(100,{})
assert(PatientGetWoundedStacks(u)==1)
u.wounds_being_treated=PatientGetWoundedStacks(u)
for i=1,12 do PatientAddHealWoundProgress(u,40,500,true) end
assert(not IsPatientReady(u) and not u.trauma.healing)
PatientAddHealWoundProgress(u,40,500,true)
assert(u.trauma.healing and IsPatientReady(u) and u.wounds_being_treated==0)
SectorOperations.TreatWounds={}
install()
assert(SectorOperations.TreatWounds:FilterAvailable(patient(100,{}),'Patient'))
assert(h:FilterAvailable(patient(100,{})))
SectorOperations={};install()
''')
print('PASS: hospital eligibility, preserved callbacks, repeat install, trauma healing progress')
