"""Apply the scoped K4 conversation transaction, then canonical RU/EN export.

Run with the game/editor closed. Requires --game-csv and --build (staging path).
Preserves existing unrelated CSV records and backs up touched inputs.
"""
import argparse
import csv
import io
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXTS = [
    ('Контратака на виллу', 'Villa counterattack'),
    ('Легион идёт на виллу Коразон. Приготовьтесь к обороне — уйти из сектора нельзя.',
     "The Legion is advancing on Corazon's villa. Prepare to defend it; you cannot leave the sector."),
    ('Контратака на виллу отбита.', 'The villa counterattack has been repelled.'),
    ('Гости', 'Guests'),
    ('Тихо. У нас гости.', 'Quiet. We have company.'),
    ('Легион снова идёт на виллу — с лагерей и со стороны Эрни. Займите позиции до подхода противника. Уйти отсюда сейчас нельзя.',
     'The Legion is advancing on the villa again, from the camps and Ernie. Take your positions before they arrive. You cannot leave now.'),
    ('Принять $40 000', 'Accept $40,000'),
    ('Отказаться от $40 000', 'Refuse $40,000'),
    ('Принять $40 000 и попросить больше', 'Accept $40,000 and request more'),
]
IDS = [str(761915400101 + i) for i in range(len(TEXTS))]


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        if not f.readline().startswith('sep='):
            f.seek(0)
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-csv', required=True)
    parser.add_argument('--build', required=True)
    args = parser.parse_args()
    build = Path(args.build).resolve()
    build.mkdir(parents=True, exist_ok=True)
    items = ROOT.parent / 'jazz-maps/items.lua'
    for path in [items, ROOT/'Localization/EnglishManual.csv', ROOT/'Localization/Strings.csv', ROOT/'Russian.csv', ROOT/'English.csv']:
        backup = build/'backup'/path.relative_to(ROOT.parent)
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            shutil.copy2(path, backup)
    source = items.read_bytes().decode('utf-8')
    for i in range(6):
        # Only the six quest-specific IDs in the maps package move.
        pattern = rf'T\({890000000013100+i}, (--\[\[.*?\]\] )"[^"\r\n]*"\)'
        source, count = re.subn(pattern, lambda m: f'T({IDS[i]}, {m[1]}"{TEXTS[i][0]}")', source)
        assert count == 1 or (count == 0 and f'T({IDS[i]},' in source), (i, count)
    begin = source.rfind("PlaceObj('ModItemConversation'", 0, source.index('id = "FlagHill_Emma_1"'))
    end = source.index("PlaceObj('ModItemConversation'", source.index('id = "FlagHill_Emma_1"'))
    block = source[begin:end]
    block = block.replace("'Value', 2000,", "'Value', 40000,").replace('Amount = 2000,', 'Amount = 40000,')
    for old, i in [('153443670599', 6), ('476973554424', 7), ('148723557614', 8), ('246952293895', 8), ('265154709855', 7)]:
        block = re.sub(rf'T\({old}, (--\[\[.*?\]\] )"[^"\r\n]*"\)', lambda m: f'T({IDS[i]}, {m[1]}"{TEXTS[i][0]}")', block)
    block = re.sub(r"[\t ]*PlaceObj\('QuestSetVariableTimer', \{\s*Prop = \"PrepTimer\",\s*QuestId = \"Jazz_VillaCounterAttack\",\s*TimeAmount = 2,\s*Timescale = \"h\",\s*\}\),\r?\n", '', block)
    source = source[:begin]+block+source[end:]
    items.write_bytes(source.encode('utf-8'))

    memory = ROOT/'Localization/EnglishManual.csv'
    fields, rows = read_csv(memory)
    seen = {r['SourceText'] for r in rows}
    n = max(int(r['N']) for r in rows if r['N'].isdigit())
    with memory.open('a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\r\n')
        for ident, (ru, en) in zip(IDS, TEXTS):
            if ru not in seen:
                n += 1
                writer.writerow(dict(N=n, AnchorID=ident, SourceText=ru, English=en, Notes='manual-translation; K4 feedback'))
    # Match the existing canonical export workflow: ambiguous contextual Russian
    # memory is excluded from the staged input only when runtime resolves it.
    fields, rows = read_csv(ROOT/'Localization/RussianManual.csv')
    _, runtime = read_csv(ROOT/'Russian.csv')
    runtime = {r['ID']:r for r in runtime}
    groups = {}
    for row in rows:
        groups.setdefault(row['SourceText'], set()).add(row['Russian'])
    conflicts = {s for s, translations in groups.items() if len(translations)>1}
    for row in rows:
        if row['SourceText'] in conflicts:
            assert runtime[row['AnchorID']]['Translation'] == row['Russian']
    raw = (ROOT/'Localization/RussianManual.csv').read_bytes().decode('utf-8-sig')
    lines = raw.splitlines(keepends=True)
    reader = csv.DictReader(io.StringIO(raw, newline=''))
    _ = reader.fieldnames
    last = reader.line_num
    chunks = [''.join(lines[:last])]
    for row in reader:
        if row['SourceText'] not in conflicts:
            chunks.append(''.join(lines[last:reader.line_num]))
        last = reader.line_num
    (build/'RussianManual.csv').write_bytes(''.join(chunks).encode('utf-8'))
    shutil.copy2(ROOT/'Localization/Strings.csv', build/'Strings.csv')
    subprocess.run(['powershell','-NoProfile','-File',str(ROOT/'docs/tools/_export_k4_localization.ps1'),
                    '-GameCsv',args.game_csv,'-Build',str(build)],check=True)
    for relative, staged in [('Russian.csv','Russian.csv'),('English.csv','English.csv'),('Localization/Strings.csv','Strings.csv')]:
        path=ROOT/relative
        fields, current=read_csv(path)
        _, exported=read_csv(build/staged)
        selected={r['ID']:r for r in exported if r['ID'] in IDS}
        assert set(selected)==set(IDS)
        existing={r['ID']:r for r in current}
        for ident,row in selected.items():
            assert ident not in existing or existing[ident]==row, f'Unexpected existing row {ident}'
        with path.open('a',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\r\n')
            writer.writerows(row for ident,row in selected.items() if ident not in existing)
    print('PASS: K4 items transaction and nine canonical RU/EN rows installed; unrelated CSV records preserved')


if __name__ == '__main__':
    main()
