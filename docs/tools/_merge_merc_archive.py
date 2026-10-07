"""Selective mercenary items.lua merge; default is a read-only JSON plan.

Use --source extracted/items.lua --report plan.json; --apply commits the plan
to items.lua and existing UnitData companions. Localization IDs stay local.
"""
from __future__ import annotations
import argparse
import json
import csv
import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXT_FIELDS = set('Name Nick AllCapsNick Bio Title Email snype_nick Subtitle Description'.split())
VALUE_FIELDS = set('Health Agility Dexterity Strength Wisdom Will Leadership Marksmanship Mechanical Explosives Medical MaxHitPoints StartingLevel Specialization Tier StartingSalary SalaryIncrease SalaryLv1 SalaryMaxLv MedicalDeposit MedicalDepositMin MedicalDepositMax Haggling RehireHaggling DurationDiscount'.split())
DEFAULTS = {k: '60' for k in 'Health Agility Dexterity Strength Wisdom Leadership Marksmanship Mechanical Explosives Medical'.split()}
DEFAULTS.update(Will='50', StartingLevel='1', MedicalDeposit='"small"', SalaryLv1='1000', SalaryMaxLv='10000')

def mask(text):
    # Preserve positions while removing strings/comments from structural parsing.
    pattern = r'--\[(=*)\[.*?\]\1\]|--[^\n]*|\[(=*)\[.*?\]\2\]|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    return re.sub(pattern, lambda m: ' ' * len(m[0]), text, flags=re.S)

def end_delim(masked, start):
    stack = []
    for i in range(start, len(masked)):
        ch = masked[i]
        if ch in '({[': stack.append(ch)
        elif ch in ')}]':
            assert stack and stack.pop() == {')':'(', '}':'{', ']':'['}[ch], i
            if not stack: return i + 1
    raise ValueError('unclosed delimiter')

def fields(block):
    masked = mask(block)
    start = masked.index('{')
    end = end_delim(masked, start)
    chunks, pos, i = [], start + 1, start + 1
    while i < end - 1:
        if masked[i] in '({[': i = end_delim(masked, i); continue
        if masked[i] == ',': chunks.append((pos, i)); pos = i + 1
        i += 1
    if block[pos:end-1].strip(): chunks.append((pos, end-1))
    out, idx = {}, 0
    while idx < len(chunks):
        a, b = chunks[idx]
        raw = block[a:b]
        match = re.match(r'\s*(\w+)\s*=\s*', raw)
        if match:
            out[match[1]] = (a + match.end(), b, block[a+match.end():b].strip())
        elif re.fullmatch(r"\s*'\w+'\s*", raw):
            key = raw.strip()[1:-1]
            idx += 1
            c, d = chunks[idx]
            c += len(block[c:d]) - len(block[c:d].lstrip())
            out[key] = (c, d, block[c:d].strip())
        idx += 1
    return out

def units(text):
    masked = mask(text)
    result = {}
    for match in re.finditer(r"PlaceObj\('ModItemUnitDataCompositeDef',\s*\{", text):
        a = match.start(); b = end_delim(masked, text.index('(', a))
        block = text[a:b]; props = fields(block)
        uid = props.get('id', props.get('Id'))[2].strip('"\'')
        assert uid not in result, uid
        result[uid] = (a, b, block, props)
    return result

def canon(value):
    value = re.sub(r'--\[\[.*?\]\]', '', value, flags=re.S)
    return re.sub(r'\s*("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|\s+', lambda m: m[1] or '', value)

def translation(value):
    value = re.sub(r'--\[\[.*?\]\]', '', value, flags=re.S).strip()
    match = re.fullmatch(r'T\((\d+),\s*(.*)\)', value, re.S)
    if not match: return None
    try: return match[1], ast.literal_eval(match[2])
    except (SyntaxError, ValueError): return None

def csv_rows(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        if not f.readline().startswith('sep='): f.seek(0)
        return list(csv.DictReader(f))

def keep_id(incoming, current):
    old = re.match(r'T\((\d+),', current)
    new = re.match(r'T\((\d+),', incoming)
    if old and new:
        incoming = incoming[:new.start(1)] + old[1] + incoming[new.end(1):]
    return incoming

def write_preserved(path, text):
    data = path.read_bytes()
    newline = '\r\n' if b'\r\n' in data else '\n'
    path.write_bytes(text.replace('\r\n','\n').replace('\n', newline).encode('utf-8'))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--target', type=Path, default=ROOT.parent/'jazz-units')
    ap.add_argument('--report', type=Path, required=True)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--game-csv', type=Path, required=True)
    ap.add_argument('--translations', type=Path, required=True)
    args = ap.parse_args()
    source = units(args.source.read_text(encoding='utf-8-sig'))
    path = args.target/'items.lua'; text = path.read_text(encoding='utf-8-sig')
    target = units(text)
    base = {r['ID']: r for r in csv_rows(args.game_csv)}
    catalog = {r['ID']: r for r in csv_rows(ROOT/'Localization/Strings.csv')}
    overrides = json.loads(args.translations.read_text(encoding='utf-8'))
    localized = {}
    changes, edits, outputs = [], [], {}
    for uid, (_, _, sb, sp) in source.items():
        if sp.get('IsMercenary', ('','',''))[2] != 'true': continue
        if uid not in target: raise ValueError(f'missing target mercenary: {uid}')
        a, b, tb, tp = target[uid]
        assert tp.get('IsMercenary', ('','',''))[2] == 'true', uid
        companion = args.target/'UnitData'/f'{uid}.lua'
        ct = companion.read_text(encoding='utf-8-sig'); cp = fields(ct)
        be, ce = [], []
        for key in sorted(TEXT_FIELDS | VALUE_FIELDS):
            if key not in sp and (key not in DEFAULTS or key not in tp): continue
            sv = sp[key][2] if key in sp else DEFAULTS[key]
            tv = tp.get(key, ('','',''))[2]
            new = keep_id(sv, tv) if key in TEXT_FIELDS else sv
            if key in TEXT_FIELDS:
                st, tt = translation(sv), translation(tv)
                if not st: raise ValueError(f'Unsupported text: {uid}.{key}')
                tid, incoming = st
                override = overrides.get(uid+'.'+key)
                if override:
                    tid = override.get('id', tt[0] if tt else tid)
                    ru, en = override['ru'], override['en']
                elif tid in base:
                    assert incoming in (base[tid]['Text'], base[tid]['Translation']), (uid,key)
                    # Same vanilla text in a different editor language is not a change.
                    continue
                elif tt and incoming == tt[1]:
                    continue
                else:
                    tid = tt[0] if tt else tid
                    row = catalog.get(tid,{})
                    if re.search('[А-Яа-яЁё]', incoming):
                        ru, en = incoming, row.get('English','')
                        assert en, (uid,key,'missing English')
                    else:
                        en = incoming
                        ru = incoming if key in ('Email','snype_nick') else row.get('Russian','')
                        assert ru, (uid,key,'missing Russian')
                source_text = incoming if override and override.get('source') == 'archive' else en
                new = tv if tt == (tid, source_text) else f'T({tid}, {json.dumps(source_text,ensure_ascii=False)})'
                localized[tid] = dict(ID=tid, Russian=ru, English=en, SourceText=source_text,
                                     Context=f'ModItemUnitDataCompositeDef {uid} {key}')
            if canon(new) == canon(tv): continue
            # Missing fields are inserted without serializing other properties.
            changes.append(dict(unit=uid, field=key, before=tv, after=new))
            for body, props, dest in ((tb,tp,be),(ct,cp,ce)):
                if key in props:
                    x,y,_ = props[key]; dest.append((x,y,new))
                else:
                    x = body.index('{')+1
                    indent = re.search(r'\n([\t ]+)\S', body[x:])[1]
                    value = f"'{key}', {new}" if body.startswith('PlaceObj') else f'{key} = {new}'
                    dest.append((x,x,f'\n{indent}{value},'))
        for x,y,v in sorted(be, reverse=True): tb=tb[:x]+v+tb[y:]
        for x,y,v in sorted(ce, reverse=True): ct=ct[:x]+v+ct[y:]
        if be: edits.append((a,b,tb)); outputs[companion]=ct
    for a,b,v in sorted(edits, reverse=True): text=text[:a]+v+text[b:]
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
    args.report.with_suffix('.localization.json').write_text(json.dumps(list(localized.values()),ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(changes)} fields, {len(outputs)} mercenaries')
    for uid in sorted({r['unit'] for r in changes}):
        print(uid + ': ' + ', '.join(r['field'] for r in changes if r['unit']==uid))
    if args.apply:
        if edits: write_preserved(path,text)
        for p,t in outputs.items(): write_preserved(p,t)

if __name__=='__main__': main()
