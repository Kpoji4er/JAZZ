"""Offline regression: catalog persistence, old saves and AUG cabinet costs (lupa)."""
from pathlib import Path
from lupa import LuaRuntime
from _repair_removable_bindings import ROOT, repair


def main():
    count, changes = repair()
    assert count and not changes, 'catalog bindings missing or inconsistent'
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
        DefineClass={}; WeaponComponents={}; Catalog={}; empty_table={}
        function UndefineClass() end
        function box(...) return {...} end
        point=box; RGBA=box; range=box
        function set(t) return t or {} end
        function Untranslated(t) return t end
        function T(a,b) return b or a end
        function PlaceObj(c,p,children)
          p=p or {}; for i=1,#p,2 do p[p[i]]=p[i+1] end
          if c=='ModItemWeaponComponent' then WeaponComponents[p.id]=p end
          if c=='ModItemInventoryItemCompositeDef' then Catalog[p.Id]=p end
          return p
        end
        function table.find(t,v) for i,x in ipairs(t) do if x==v then return i end end end
        function string.starts_with(s,p) return s:sub(1,#p)==p end
        function CheatEnabled() return false end
        ModifyWeaponDlg={}; gv_Squads={}; g_Units={}; gv_UnitData={}
        function GetSquadBagInventory() return nil end
    ''')
    # Compile full changed runtime, metadata and catalog without executing engine hooks.
    syntax = lua.eval('function(s) local f,e=load(s); assert(f,e) end')
    resource = (ROOT/'Code/System_WeaponResourceMaintenance.lua').read_text(encoding='utf-8')
    syntax(resource)
    syntax((ROOT/'metadata.lua').read_text(encoding='utf-8'))
    lua.execute((ROOT/'items.lua').read_text(encoding='utf-8-sig'))
    for path in (ROOT/'InventoryItem').glob('*.lua'):
        body = path.read_text(encoding='utf-8-sig')
        if '__parents = { "JAZZ_RemovableAttachment" }' in body or path.stem in ('AUG','AKM','M16A4'):
            lua.execute(body)
    assert 'template = true' in resource[resource.index('id = "RemovableComponentId"'):][:240]
    lua.execute(resource[resource.index('local JazzRemovableSlots ='):resource.index('function JAZZ_ResolveRemovableAttachmentIcon')])
    lua.execute(resource[resource.index('function JAZZ_HasRemovableComponentOption'):resource.index('if FirstLoad then',resource.index('function JAZZ_HasRemovableComponentOption'))])
    modify=(ROOT/'Code/System_WeaponRemovableModify.lua').read_text(encoding='utf-8')
    # Keep production local inventory helper and cost calculation in the same chunk.
    helper=modify[modify.index('local function JazzFindRemovableAttachmentItem'):modify.index('-- Folded half')]
    costs=modify[modify.index('local function JazzFoldingPairIdsMatch'):modify.index('local VanillaPayCosts')]
    lua.execute(helper+costs+'''
        local n=0
        for id,def in pairs(DefineClass) do
          if def.__parents[1]=='JAZZ_RemovableAttachment' then
            n=n+1
            assert(def.RemovableComponentId==id and Catalog[id].RemovableComponentId==id,id)
            local old=setmetatable({}, {__index=def})
            local owner={ForEachItem=function(self,kind,fn) fn(old) end}
            assert(JazzFindRemovableAttachmentItem(owner,id)==old,id)
            old.RemovableComponentId='explicit-save-id'
            assert(old.RemovableComponentId=='explicit-save-id')
            assert(not JazzFindRemovableAttachmentItem(owner,id))
          end
        end
        assert(n>0)
        local cid='JAZZ_GrenadeLauncher_AUG'
        assert(JAZZ_IsRemovableWeaponComponent(cid,'Grenadelauncher'))
        assert(JAZZ_IsRemovableWeaponComponent(cid,'GrenadeLauncher'))
        assert(JAZZ_GetRemovableAttachmentThreshold(cid,'Grenadelauncher')==40)
        assert(JAZZ_HasRemovableComponentOption(DefineClass.AUG,cid))
        assert(not JAZZ_HasRemovableComponentOption(DefineClass.AUG,'JAZZ_GP25'))
        assert(not JAZZ_HasRemovableComponentOption(DefineClass.AUG,'JAZZ_GrenadeLauncher'))
        assert(not JAZZ_HasRemovableComponentOption(DefineClass.M16A4,cid))
        assert(JAZZ_HasRemovableComponentOption(DefineClass.M16A4,'JAZZ_GrenadeLauncher'))
        assert(JAZZ_HasRemovableComponentOption(DefineClass.AKM,'JAZZ_GP25'))
        local stock={}
        gv_UnitData.test={ForEachItem=function(self,kind,fn) for _,v in ipairs(stock) do fn(v) end end}
        local dlg={context={owner='test',weapon={components={Grenadelauncher=''}}},
                   weaponClone={components={Grenadelauncher=cid}}}
        local c,changed,afford=ModifyWeaponDlg.GetChangesCost(dlg,'Grenadelauncher')
        assert(changed and not afford and next(c)==nil,'AUG must require an inventory item')
        stock[1]=setmetatable({}, {__index=DefineClass[cid]})
        c,changed,afford=ModifyWeaponDlg.GetChangesCost(dlg,'Grenadelauncher')
        assert(changed and afford and next(c)==nil,'AUG must consume item, not Parts')
    ''')
    print(f'PASS: {count} catalog bindings; inherited save IDs; AUG/M16/AK compatibility; cabinet costs')


if __name__ == '__main__':
    main()
