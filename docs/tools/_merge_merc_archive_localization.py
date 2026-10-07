"""Prepare/install a scoped canonical RU+EN export for the mercenary merge.

Preserve all unrelated CSV records byte-for-byte. Run prepare, then the paired
PowerShell exporter, then install. Uses final-plan.localization.json in --build.
"""
import argparse
import csv
import io
import json
import shutil
from pathlib import Path
from _merge_merc_archive import ROOT, csv_rows

def replace_rows(path, replacements, key='ID'):
    raw = path.read_bytes().decode('utf-8-sig')
    lines = raw.splitlines(keepends=True)
    skip = int(raw.startswith('sep='))
    reader = csv.DictReader(io.StringIO(''.join(lines[skip:]), newline=''))
    fields = reader.fieldnames
    last = reader.line_num + skip
    chunks = [''.join(lines[:last])]
    pending = dict(replacements)
    def render(row):
        stream=io.StringIO(newline='')
        csv.DictWriter(stream,fieldnames=fields,lineterminator='\r\n').writerow(row)
        return stream.getvalue()
    for row in reader:
        end=reader.line_num+skip
        ident=row[key]
        if ident in replacements:
            new=dict(row);new.update(replacements[ident])
            chunks.append(render(new) if new!=row else ''.join(lines[last:end]))
            pending.pop(ident,None)
        else: chunks.append(''.join(lines[last:end]))
        last=end
    chunks.extend(render(row) for row in pending.values())
    path.write_bytes(''.join(chunks).encode('utf-8'))

def main():
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=['prepare','install'])
    p.add_argument('--build',type=Path,required=True)
    a=p.parse_args();build=a.build.resolve()
    texts=json.loads((build/'final-plan.localization.json').read_text(encoding='utf-8'))
    ids={r['ID'] for r in texts}
    if a.mode=='prepare':
        for name in ['Russian.csv','English.csv','Localization/Strings.csv','Localization/RussianManual.csv','Localization/EnglishManual.csv']:
            shutil.copy2(ROOT/name,build/Path(name).name)
        # Scope-local CSV input gives the auditor the explicitly requested RU copy.
        for lang in ['Russian','English']:
            rows={r['ID']:dict(ID=r['ID'],Text=r['SourceText'],Translation=r[lang],VoiceActor='',Context=r['Context']) for r in texts}
            replace_rows(build/f'{lang}.csv',rows)
        updates={r['ID']:{lang:r[lang] for lang in ['Russian','English']} for r in texts if r['ID'] in {x['ID'] for x in csv_rows(build/'Strings.csv')}}
        replace_rows(build/'Strings.csv',updates)
        for lang in ['Russian','English']:
            path=build/f'{lang}Manual.csv';memory=csv_rows(path)
            number=max(int(r['N']) for r in memory if r['N'].isdigit())
            updates={}
            for r in texts:
                number+=1
                updates[r['SourceText']]=dict(N=str(number),AnchorID=r['ID'],SourceText=r['SourceText'],**{lang:r[lang]},Notes='technical-copy' if r['Russian']==r['English'] else 'manual-translation; JAZZ-MERC-MERGE-001')
            replace_rows(path,updates,key='SourceText')
            # Existing contextual Russian-memory conflicts are resolved in the
            # baseline runtime table; omit only those from this staging input.
            rows=csv_rows(path); groups={}
            for r in rows: groups.setdefault(r['SourceText'],set()).add(r[lang])
            conflicts={s for s,vs in groups.items() if len(vs)>1}
            assert not conflicts.intersection(updates)
            if conflicts:
                raw=path.read_text(encoding='utf-8');lines=raw.splitlines(keepends=True)
                reader=csv.DictReader(io.StringIO(raw,newline=''));_=reader.fieldnames
                last=reader.line_num;chunks=[''.join(lines[:last])]
                for r in reader:
                    if r['SourceText'] not in conflicts:chunks.append(''.join(lines[last:reader.line_num]))
                    last=reader.line_num
                path.write_bytes(''.join(chunks).encode('utf-8'))
            print(lang,'staged; pre-existing conflicting memory sources excluded:',len(conflicts))
    else:
        exported={lang:{r['ID']:r for r in csv_rows(build/f'export-{lang}.csv')} for lang in ['Russian','English']}
        assert all(set(rows)==ids for rows in exported.values())
        for r in texts:
            for lang in exported:
                assert exported[lang][r['ID']]['Translation']==r[lang],(r['ID'],lang)
        for root in [ROOT,ROOT.parent/'jazz-units']:
            for lang in exported:replace_rows(root/f'{lang}.csv',exported[lang])
        rows={r['ID']:r for r in csv_rows(build/'Strings.csv') if r['ID'] in ids}
        assert set(rows)==ids
        assert all(not any(x in r['Status'] for x in ['collision','needs-russian','needs-english']) for r in rows.values())
        replace_rows(ROOT/'Localization/Strings.csv',rows)
        for lang in exported:
            rows={r['SourceText']:r for r in csv_rows(build/f'{lang}Manual.csv') if r['SourceText'] in {x['SourceText'] for x in texts}}
            replace_rows(ROOT/f'Localization/{lang}Manual.csv',rows,key='SourceText')
        print(f'Installed {len(ids)} paired RU/EN records; unrelated rows preserved')

if __name__=='__main__':main()
