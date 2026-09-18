"""Read-only balance probes using actual Lua functions through lupa.

Run: python docs/tools/_audit_weapon_balance_runtime.py
No game process required. Engine APIs are stubs; this is NOT a JA3 playtest.
Companion stats override CSV fallbacks; no installed component modifiers are
applied to the isolated recoil examples. Prints evidence, does not edit data.
"""
from pathlib import Path
import csv
from lupa import LuaRuntime

ROOT = Path(__file__).resolve().parents[2]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def section(path, start, stop):
    text = source(path)
    return text[text.index(start):text.index(stop, text.index(start))]


def main():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
        Max=math.max; Min=math.min; empty_table={}; const={SlabSizeX=1000}
        function Clamp(x,a,b) return Max(a,Min(x,b)) end
        function DivRound(a,b)
            local x=a/b
            return x>=0 and math.floor(x+0.5) or math.ceil(x-0.5)
        end
        function MulDivRound(a,b,c) return DivRound(a*b,c) end
        function HasPerk() return false end
        function IsKindOf(x,k) return x and x.object_class==k end
        function T(...) return '' end
        function UndefineClass() end
        function PlaceObj(k,t) return t end
        function set(...) local t={} for _,v in ipairs({...}) do t[v]=true end return t end
        DefineClass={}; Unit={}; Armor={}; FirearmBase={}; CombatActions={Buckshot={}}
        function WaitMsg() end
        function GetComponentEffectValue(w,e,k)
            return w.effects and w.effects[e] and w.effects[e][k]
        end
    ''')
    lua.execute(source("Code/AccuracyRangeCTH.lua"))
    lua.execute(section("Code/System_OR_Weapons.lua",
                        "function FirearmBase:GetAutofireShots(",
                        "-- Jazz_Perk_Nervous / Jazz_Perk_Buzz"))
    lua.execute(section("Code/ExecFirearmAttacks.lua",
                        "function Unit:ShotgunBurst(",
                        "-- makes the actual bullets"))
    lua.execute(section("Code/System_ArmorRating.lua",
                        "function GetAttackPenetrationClass(",
                        "function Unit:ApplyDamageAndEffects("))
    lua.execute(section("Code/System_ArmorRating.lua",
                        "function Armor:CalculateArmorRating(",
                        "function Armor:CalculateArmorRatingMelee("))
    print("Actual Lua methods; stubbed engine, standard Lua arithmetic, no live game.")
    print("SHOTGUN BURST calls:", lua.execute('''
        local n=0
        local u={GetActiveWeapons=function() return {} end,
                 CanUseWeapon=function() return true end,
                 FirearmAttack=function() n=n+1 end}
        Unit.ShotgunBurst(u,'BuckshotBurst',0,{target={}})
        return n
    '''))
    print("ARMOR damage=100, DR=10 then 20 / reversed:", lua.execute('''
        Unit.Random=function() return 0 end
        local function run(a,b)
            local function armor(dr)
                return {Condition=100, ProtectedBodyParts={Torso=true},
                    PenetrationClass=2,Coverage=100,Degradation=0,ArmorResource=100,
                    CalculateArmorRating=function() return dr end,
                    CalculateArmorRatingMelee=function() return dr end,
                    CalculateArmorRatingExplosive=function() return dr end}
            end
            local u={ForEachItem=function(self,kind,fn,...)
                fn(armor(a),'Torso',0,0,...)
                fn(armor(b),'ArmorPlate',0,0,...)
            end}
            local hit={damage=100}
            Unit.ApplyHitDamageReduction(u,hit,
                {object_class='Firearm',PenetrationClass=2,PenetrationBonus=0,
                 HasMember=function(self,k) return self[k]~=nil end},'Torso')
            return hit.damage
        end
        return run(10,20),run(20,10)
    '''))
    rows = list(csv.DictReader((ROOT / "docs/technical/weapons/data/weapons.csv").open(encoding="utf-8-sig")))
    mapping = {"damage":"Damage", "weapon_range":"WeaponRange", "bullet_drop_range":"BulletDropRange",
               "grouping":"Grouping", "recoil":"Recoil", "burst_shots":"BurstShots", "auto_shots":"AutoShots",
               "shoot_ap":"ShootAP", "max_aim_actions":"MaxAimActions", "aim_accuracy":"AimAccuracy",
               "close_range":"CloseRange", "close_range_factor":"CloseRangeFactor"}
    weapons = {}
    drift = []
    metadata = source("metadata.lua")
    for row in rows:
        if row["catalog_status"] != "active":
            continue
        path = row["source_file"]
        lua.execute(source(path))
        w = lua.globals().DefineClass[row["id"]]
        if w is None:
            drift.append(f'{row["id"]}: companion does not define catalog ID ({path})')
            continue
        for col, prop in mapping.items():
            if row[col] == "":
                continue
            old = float(row[col])
            if w[prop] is None:
                w[prop] = old  # explicit CSV fallback, NOT claimed to be resolved runtime default
            elif float(w[prop]) != old:
                drift.append(f'{row["id"]}.{prop}: CSV={old:g}, companion={w[prop]}')
        w["components"] = lua.table()
        weapons[row["id"]] = w
        if f'"{path}"' not in metadata:
            drift.append(f'{path}: not found in metadata')
    print("ACTIVE companions read:", len(weapons))
    print("BuckshotBurst authored on:", [wid for wid,w in weapons.items()
          if w.AvailableAttacks and 'BuckshotBurst' in list(w.AvailableAttacks.values())])
    print("CSV drift:", *drift, sep="\n  ")
    lua.globals().weapons = lua.table_from(weapons)
    print("RECOIL isolation: first CTH=70, Str=70 Mrk=70; no ammo/components/perks")
    for wid, aid in [("AK47","BurstFire"),("AKM","BurstFire"),("G36","BurstFire"),
                     ("M16A4","BurstFire"),("MG42","MGBurstFire"),("HK21","MGBurstFire"),
                     ("PKM","MGBurstFire"),("FNMinimi","MGBurstFire")]:
        is_mg = weapons[wid].object_class in ('MachineGun','LightMachineGun')
        for stance, deployed in [("Standing", False),("Prone", is_mg)]:
            vals = lua.eval('''function(w,aid,stance,deployed)
                local action={id=aid,ResolveValue=function() return nil end}
                local n=FirearmBase.GetAutofireShots(w,action)
                local r=JAZZ_CTHGetRecoilProfile(w,{Strength=70,Marksmanship=70},stance,action,{deployed=deployed})
                local seq={} local total=0
                for i=1,n do
                    local p=JAZZ_CTHGetBulletChance(70,i,r,true)
                    seq[#seq+1]=p; total=total+p
                end
                return n,table.concat(seq,','),total/100
            end''')(weapons[wid], aid, stance, deployed)
            print(wid, aid, stance, "supported="+str(deployed), vals)
    print("RANGE isolation: aim=0, no optics/ammo/components; factor also damage percent")
    for wid in ["AKM","M16A4","G36","DragunovSVD","MG42","PKM","FNMinimi"]:
        w = weapons[wid]
        vals = []
        for dist in [10,20,30,40]:
            factor, profile = lua.globals().JAZZ_CTHGetRangeProfile(w,dist*1000,None,None,0)
            vals.append((dist,factor/10,lua.globals().GetRangeDamageReduction(w,dist*1000,None,None)))
        print(wid, vals)
    # This probe executes the exact numeric-for loop and armor method above.
    # Do not turn observed bugs into assertions that bless the broken behavior.


if __name__ == "__main__":
    main()
