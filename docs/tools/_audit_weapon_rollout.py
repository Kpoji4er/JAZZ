"""Verify the rollout against the pre-install Units snapshot: --build <build>."""
import argparse, json, re
from pathlib import Path
from _apply_weapon_rollout import ROOT, NEW, bounds
from _integrate_sr3m import matching

p=argparse.ArgumentParser();p.add_argument('--build',required=True,type=Path);a=p.parse_args()
unit=ROOT.parent/'jazz-units'
baseline=min((a.build/'rollout-backup/jazz-units').glob('items.lua.*'),key=lambda p:p.stat().st_mtime)
old=baseline.read_text(encoding='utf-8-sig');current=(unit/'items.lua').read_text(encoding='utf-8-sig')
report=json.loads((a.build/'rollout-stage/report.json').read_text(encoding='utf-8'))
allowed=set(report)|{'Ivan10','Crusher_Inventory'}
def lootdefs(text):
    out={}
    for m in re.finditer(r"PlaceObj\('ModItemLootDef'",text):
        end=matching(text,text.index('(',m.start()));block=text[m.start():end]
        ident=re.search(r'\bid\s*=\s*"([^"]+)"',block)
        assert ident and ident[1] not in out
        out[ident[1]]=block
    return out
before=lootdefs(old);after=lootdefs(current)
def clean(text):return re.sub(r'\s+','',text)
changed={k for k,v in before.items() if k not in after or clean(v)!=clean(after[k])}
assert changed<=allowed,('Unexpected changed LootDefs',changed-allowed)
assert all(k.startswith(tuple('JAZZ_GenW_'+w+'_' for w in NEW)) for k in after.keys()-before.keys())
# Preserve every existing entry within amended firearm pools, including all Mosins.
for fid in report:
    for m in re.finditer(r"PlaceObj\('LootEntryLootDef'",before[fid]):
        end=matching(before[fid],before[fid].index('(',m.start()))
        assert clean(before[fid][m.start():end]) in clean(after[fid]),fid
assert 'weapon = "AK74M"' in after['Ivan10'] and 'JAZZ_AMMO_545_EPR' in after['Ivan10']
assert clean(before['Ivan10'].replace('weapon = "AK74"','weapon = "AK74M"'))==clean(after['Ivan10'])
assert len(re.findall(r'item = "Knife"',after['Crusher_Inventory']))==3
for n in (40,55,70):assert 'generate_chance = '+str(n) in after['Crusher_Inventory']
print(f'PASS: {len(before)} pre-existing LootDefs retained; only {len(changed)} approved presets changed; {len(after)-len(before)} new weapon/ammo combos; existing pool entries/Mosin preserved; Ivan and Crusher verified.')
