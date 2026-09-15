"""Add SR3M translation memory; run canonical audit/export after integration.

python docs/tools/_localize_sr3m.py --game-csv <Game.csv> --build <build>
Only install runtime CSV after reviewing the exported old-row diff.
"""
import argparse
import csv
import subprocess
import shutil
import io
from collections import defaultdict
from pathlib import Path
from _integrate_sr3m import ROOT, TEXTS

p=argparse.ArgumentParser()
p.add_argument('--game-csv',required=True)
p.add_argument('--build',required=True)
args=p.parse_args()
build=Path(args.build).resolve()

def read_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        if not f.readline().startswith('sep='): f.seek(0)
        reader=csv.DictReader(f)
        return reader.fieldnames,list(reader)

# Existing source-keyed bark memory has contextual translations of the same
# sentence. Resolve those through the higher-priority, per-ID runtime table;
# never choose one contextual translation for every occurrence of that source.
fields_ru,memory=read_csv(ROOT/'Localization/RussianManual.csv')
_,runtime=read_csv(ROOT/'Russian.csv')
by_id={r['ID']:r for r in runtime}
groups=defaultdict(list)
for row in memory: groups[row['SourceText']].append(row)
conflicting={text for text,rs in groups.items() if len({r['Russian'] for r in rs})>1}
for text in conflicting:
    for row in groups[text]:
        assert by_id[row['AnchorID']]['Translation']==row['Russian'], 'Unresolved Russian memory conflict'
snapshot=build/'RussianManual.csv'
raw=(ROOT/'Localization/RussianManual.csv').read_bytes().decode('utf-8-sig')
lines=raw.splitlines(keepends=True)
reader=csv.DictReader(io.StringIO(raw,newline=''))
_ = reader.fieldnames
last=reader.line_num
chunks=[''.join(lines[:last])]
for row in reader:
    if row['SourceText'] not in conflicting:
        chunks.append(''.join(lines[last:reader.line_num]))
    last=reader.line_num
snapshot.write_bytes(''.join(chunks).encode('utf-8'))
print('Resolved contextual memory conflicts from authoritative per-ID runtime:',len(conflicting),flush=True)
path=ROOT/'Localization/EnglishManual.csv'
with path.open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f)
    fields=reader.fieldnames
    rows=list(reader)
seen={r['SourceText'] for r in rows}
n=max(int(r['N']) for r in rows if r['N'].isdigit())
with path.open('a',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\r\n')
    for ident,ru,en in TEXTS.values():
        if ru not in seen:
            n+=1
            writer.writerow({'N':n,'AnchorID':ident,'SourceText':ru,'English':en,'Notes':'manual-translation; SR3M'})
            seen.add(ru)
shutil.copy2(ROOT/'Localization/Strings.csv',build/'Strings.csv')
subprocess.run(['powershell','-NoProfile','-File',str(ROOT/'docs/tools/_export_sr3m_localization.ps1'),
    '-GameCsv',str(Path(args.game_csv).resolve()),'-Build',str(build)],check=True)
ids={str(v[0]) for v in TEXTS.values()}
for relative,staged in [('Russian.csv','Russian.csv'),('English.csv','English.csv'),('Localization/Strings.csv','Strings.csv')]:
    target=ROOT/relative
    fields,current=read_csv(target)
    _,exported=read_csv(build/staged)
    selected=[r for r in exported if r['ID'] in ids]
    assert {r['ID'] for r in selected}==ids
    existing={r['ID']:r for r in current}
    for row in selected:
        assert row['ID'] not in existing or row==existing[row['ID']], 'Existing SR3M translation differs'
    backup=build/'integration-backup'/ROOT.name/relative
    backup.parent.mkdir(parents=True,exist_ok=True)
    if not backup.exists(): shutil.copy2(target,backup)
    with target.open('a',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\r\n')
        writer.writerows(r for r in selected if r['ID'] not in existing)
print('Installed only the three canonical SR3M rows from the same RU/EN catalog snapshot; all prior runtime rows preserved.')
