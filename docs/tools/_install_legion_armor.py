"""Install staged armor and an isolated Legion test UnitData, with game/editor closed.

python docs/tools/_install_legion_armor.py --build <game-build>
One-shot transaction; existing files backed up, no revisions/hashes guessed.
"""
import argparse, re, shutil, subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import matching, append_root_item, add_metadata, write

ROOT=Path(__file__).resolve().parents[2]; ASSETS=ROOT.parent/'jazz_assets'; UNITS=ROOT.parent/'jazz-units'
ENTITY='JAZZ_ImprovisedCuirass_Male'; ID='JAZZ_Legion_ArmorTest'

def main():
    p=argparse.ArgumentParser();p.add_argument('--build',required=True,type=Path);a=p.parse_args();build=a.build.resolve()
    check=subprocess.run(['powershell','-NoProfile','-Command',"Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id"],capture_output=True,text=True)
    assert not check.stdout.strip(),'Close game/editor before manual transaction'
    paths=[ROOT/'items.lua',ROOT/'metadata.lua',ASSETS/'items.lua',ASSETS/'metadata.lua',UNITS/'items.lua',UNITS/'metadata.lua']
    before={p:p.read_bytes() for p in paths};texts={p:b.decode('utf-8-sig') for p,b in before.items()}
    assert ID not in texts[UNITS/'items.lua'] and ENTITY not in texts[ASSETS/'items.lua'],'Already installed'
    # A self-contained test character. Existing localized Recruit name, no new T ID.
    props='''
    comment = "JAZZ-APPEAR-001 TEST ONLY: cuirass + MP40; not in campaign pools",
    object_class = "UnitData",
    Health = 85,
    Agility = 70,
    Dexterity = 70,
    Strength = 90,
    Wisdom = 50,
    Will = 60,
    Marksmanship = 70,
    MaxHitPoints = 85,
    Portrait = "Mod/Dv3mFVN/EnemyPortraits/Legion/Recruit.png",
    BigPortrait = "UI/Enemies/LegionRaider",
    Name = T(890000000001643, "Новобранец"),
    Affiliation = "Legion",
    gender = "Male",
    Randomization = false,
    archetype = "Assault",
    role = "Stormer",
    Equipment = {},
    AppearancesList = { PlaceObj('AppearanceWeight', { 'Preset', "LegionGoon" }) },
    CustomEquipGear = function(self, items)
        items[#items + 1] = PlaceInventoryItem("JazzArmor_ImprovisedCuirass")
        items[#items + 1] = PlaceInventoryItem("MP40")
        local ammo = PlaceInventoryItem("JAZZ_AMMO_9x19_FMJ")
        ammo.Amount = 120
        items[#items + 1] = ammo
        self:TryEquip(items, "Torso", "Armor")
        self:TryEquip(items, "Handheld A", "Firearm")
        self:TryLoadAmmo("Handheld A", "Firearm", "JAZZ_AMMO_9x19_FMJ")
    end,
'''
    companion="UndefineClass('"+ID+"')\nDefineClass."+ID+" = {\n    __parents = { \"UnitData\" },\n    __generated_by_class = \"ModItemUnitDataCompositeDef\",\n"+props+"}\n"
    # Composite ModItems use StoreAsTable=false: alternating property/value array.
    serialized=re.sub(r'^    (\w+) = ',r"    '\1', ",props,flags=re.M)
    unititem="PlaceObj('ModItemUnitDataCompositeDef', {\n    'Group', \"JAZZ Tests\",\n    'Id', \""+ID+"\",\n"+serialized+"}),"
    text=texts[UNITS/'items.lua'];pos=text.rfind('}')
    # The generated voice-response block ends with a line comment after its comma.
    texts[UNITS/'items.lua']=text[:pos]+unititem+'\n'+text[pos:]
    texts[UNITS/'metadata.lua']=add_metadata(texts[UNITS/'metadata.lua'],'code',['"UnitData/'+ID+'.lua"'])
    texts[UNITS/'metadata.lua']=add_metadata(texts[UNITS/'metadata.lua'],'affected_resources',["PlaceObj('ModResourcePreset', { 'Class', \"UnitDataCompositeDef\", 'Id', \""+ID+"\", 'ClassDisplayName', \"Unit\" })"])
    entityitem="PlaceObj('ModItemEntity', {\n    'name', \""+ENTITY+"\",\n    'ClassParents', { \"CharacterArmorMale\" },\n    'entity_name', \""+ENTITY+"\",\n}),"
    texts[ASSETS/'items.lua']=append_root_item(texts[ASSETS/'items.lua'],entityitem)
    texts[ASSETS/'metadata.lua']=add_metadata(texts[ASSETS/'metadata.lua'],'entities',['"'+ENTITY+'"'])
    texts[ASSETS/'metadata.lua']=add_metadata(texts[ASSETS/'metadata.lua'],'code',['"Entities/'+ENTITY+'.lua"'])
    # Keep existing load order, insert immediately after the established appearance module.
    meta=texts[ROOT/'metadata.lua'];anchor='"Code/System_UnitAppearance.lua",'
    assert meta.count(anchor)==1
    texts[ROOT/'metadata.lua']=meta.replace(anchor,anchor+'\n\t\t"Code/System_LegionArmorVisuals.lua",',1)
    text=texts[ROOT/'items.lua'];start=text.index("'CodeFileName', \"Code/System_UnitAppearance.lua\"");end=text.index('}),',start)+3
    texts[ROOT/'items.lua']=text[:end]+'\n\t\tPlaceObj(\'ModItemCode\', { \'name\', "System_LegionArmorVisuals", \'CodeFileName\', "Code/System_LegionArmorVisuals.lua" }),'+text[end:]
    lua=LuaRuntime()
    for text in list(texts.values())+[companion]:lua.compile(text)
    stage=build/'mod-assets-stage/Entities'
    entlua='EntityData["'+ENTITY+'"] = {\n    editor_artset = "Mods",\n    entity = { class_parent = "CharacterArmorMale" },\n}\n'
    write(stage/(ENTITY+'.lua'),entlua)
    copies={ASSETS/'Entities'/p.relative_to(stage):p for p in stage.rglob('*') if p.is_file()}
    copies[ROOT/'ArmorIcons/ImprovisedCuirass.png']=build/'ImprovisedCuirass.png'
    for dest,src in copies.items():
        assert src.is_file()
        if dest.exists():assert dest==ROOT/'ArmorIcons/ImprovisedCuirass.png',dest
    for path,old in before.items():assert path.read_bytes()==old,'Concurrent edit: '+str(path)
    for path in paths+[ROOT/'ArmorIcons/ImprovisedCuirass.png']:
        target=build/'integration-backup'/path.relative_to(ROOT.parent);target.parent.mkdir(parents=True,exist_ok=True)
        assert not target.exists();target.write_bytes(path.read_bytes())
    for dest,src in copies.items():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
    write(UNITS/'UnitData'/f'{ID}.lua',companion)
    for path,text in texts.items():write(path,text)
    print('Installed Legion armor module, entity, render icon and isolated test UnitData.')

if __name__=='__main__':main()
