"""Read-only scope and companion checks for JAZZ-MERC-MERGE-001.

Compare the current units tree with HEAD (which must be the clean baseline),
and with the immutable final-plan.json produced before apply.
"""
import argparse
import json
import subprocess
from pathlib import Path
from _merge_merc_archive import ROOT, units, fields, canon, translation, csv_rows

def equivalent(a,b):
    ta,tb=translation(a),translation(b)
    return ta==tb if ta and tb else canon(a)==canon(b)

def main():
    p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True)
    p.add_argument('--data-only',action='store_true')
    a=p.parse_args();package=ROOT.parent/'jazz-units'
    before=subprocess.check_output(['git','-C',str(package),'show','HEAD:items.lua']).decode('utf-8-sig')
    after=(package/'items.lua').read_text(encoding='utf-8-sig')
    old,new=units(before),units(after)
    plan=json.loads((a.build/'final-plan.json').read_text(encoding='utf-8'))
    allowed={(r['unit'],r['field']):r for r in plan}
    assert old.keys()==new.keys(),'Unit set changed'
    changes=set()
    for uid in old:
        op,np=old[uid][3],new[uid][3]
        for k in set(op)|set(np):
            ov=op.get(k,('','',''))[2];nv=np.get(k,('','',''))[2]
            if equivalent(ov,nv):continue
            changes.add((uid,k))
            assert (uid,k) in allowed,(uid,k,'outside scope')
            assert equivalent(nv,allowed[uid,k]['after']),(uid,k,'not planned value')
            cp=fields((package/'UnitData'/f'{uid}.lua').read_text(encoding='utf-8-sig'))
            assert equivalent(nv,cp[k][2]),(uid,k,'companion mismatch')
    assert changes==set(allowed),(changes.symmetric_difference(allowed))
    # Everything outside UnitData is byte-equivalent (normalizing CRLF only).
    def strip_units(text,parsed):
        for uid,(start,end,_,_) in sorted(parsed.items(),key=lambda r:r[1][0],reverse=True):
            text=text[:start]+f'<UNIT:{uid}>'+text[end:]
        return text
    assert strip_units(before,old)==strip_units(after,new),'Non-UnitData content changed'
    changed_paths=subprocess.check_output(['git','-C',str(package),'diff','--name-only']).decode().splitlines()
    expected={'items.lua','metadata.lua','Russian.csv','English.csv'}|{f'UnitData/{u}.lua' for u,k in allowed}
    assert set(changed_paths)<=expected,set(changed_paths)-expected
    if 'metadata.lua' in changed_paths:
        original=subprocess.check_output(['git','-C',str(package),'show','HEAD:metadata.lua']).decode('utf-8-sig')
        previous=fields(original);current=fields((package/'metadata.lua').read_text(encoding='utf-8-sig'))
        assert previous.keys()==current.keys()
        for key in previous:
            if key not in ('version','last_changes'):assert canon(previous[key][2])==canon(current[key][2]),key
        assert int(current['version'][2])==int(previous['version'][2])+1
        assert current['last_changes'][2].endswith(previous['last_changes'][2][1:])
    if a.data_only:
        print(f'PASS: {len(allowed)} planned fields match companions; all other data preserved')
        return
    texts=json.loads((a.build/'final-plan.localization.json').read_text(encoding='utf-8'))
    selected={r['ID']:r for r in texts}
    for tid,r in selected.items():
        _,uid,field=r['Context'].split()
        assert translation(new[uid][3][field][2])==(tid,r['SourceText']),(uid,field,'stale localization source')
        cp=fields((package/'UnitData'/f'{uid}.lua').read_text(encoding='utf-8-sig'))
        assert translation(cp[field][2])==(tid,r['SourceText']),(uid,field,'companion localization source')
    for root in [ROOT,package]:
        for lang in ['Russian','English']:
            rows=csv_rows(root/f'{lang}.csv');index={r['ID']:r for r in rows}
            assert len(index)==len(rows),(root,lang,'duplicate IDs')
            for tid,r in selected.items():
                assert index[tid]['Text']==r['SourceText'],(root,tid,'source')
                assert index[tid]['Translation']==r[lang],(root,tid,lang)
            baseline=a.build/'backup'/root.name/f'{lang}.csv'
            originals={r['ID']:r for r in csv_rows(baseline)}
            assert {k:v for k,v in originals.items() if k not in selected}=={k:v for k,v in index.items() if k not in selected},(root,lang,'unrelated CSV edit')
    catalog={r['ID']:r for r in csv_rows(ROOT/'Localization/Strings.csv')}
    for tid in selected:
        r=catalog[tid]
        assert not any(s in r['Status'] for s in ['collision','needs-russian','needs-english']),r
    print(f'PASS: {len(allowed)} scoped fields, {len({u for u,k in allowed})} mercenaries; {len(selected)} paired localization IDs; all unrelated records preserved')

if __name__=='__main__':main()
