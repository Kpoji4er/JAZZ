"""Export every live weapon's names and structural-module decisions, no runtime edits."""
import argparse
import csv
import json
from pathlib import Path
from lupa import LuaRuntime
from build_review import lua_table

STRUCTURAL={'Stock','Barrel','Handguard','Body','Receiver','Caliber'}
NOTES={
    'AK74': ('explicit-rule', 'АК-74 → АКС-74 только для двух штатных складных прикладов; положение не меняет имя.'),
    'AKM': ('explicit-rule', 'АКМ → АКМС для штатного металлического приклада, складывающегося под оружие; оба положения. Подтверждены live-геометрия и руководство производителя.'),
    'AK103': ('preserve', 'Положение штатного складного приклада не меняет АК-103.'),
    'AK105': ('preserve', 'Не получать АК-105 из другого автомата по одному короткому стволу.'),
    'AK74M': ('preserve', 'АК-74М сохраняет собственное обозначение при складывании.'),
    'DragunovSVD': ('rejected-candidate', 'StockLight в игре — цельная ложа с отверстием под большой палец; отдельной рукоятки и складного рамочного приклада нет. СВДС не включать.'),
    'Mosin': ('coordinated-pending', '1891 / М38 / обрез: существующий Weapon_MosinModular меняет модель/размер/Icon, но в проверенном коде не имя. Именование согласовать с подготовленным изменением основной задачи; второй хук не создавать.'),
    'VZ58': ('explicit-rule', 'vz. 58 P для штатного деревянного приклада; vz. 58 V для штатного металлического складного в обоих положениях. Тактический приклад — исходное имя без исторического суффикса.'),
    'MP5': ('candidate', 'Проверить сочетание корпуса, спусковой группы и приклада для A2/A3; отсутствие приклада не превращает MP5 в MP5K.'),
    'M4A1': ('preserve', '20/30/расширенный магазин, RIS, положение приклада и доступные стволы сохраняют M4A1 без отдельного доказанного правила.'),
    'M16A4': ('preserve', 'Короткий ствол/RIS не превращает винтовку автоматически в M4.'),
    'M1A': ('candidate', 'Короткий ствол/ложа требуют отдельной проверки; не присваивать Scout/SOCOM/Mk14 по одному модулю.'),
}
UNIQUE={'Auto5_quest','DragunovSVD_Custom','Galil_FlagHill','GoldenGun','LionRoar','Sig550Custom','TexRevolver','Winchester_Quest'}


def main():
    p=argparse.ArgumentParser(__doc__)
    p.add_argument('--catalog',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    weapons=json.loads(a.catalog.read_text(encoding='utf-8'))['weapons']
    document=json.loads(a.manifest.read_text(encoding='utf-8'))
    manifest=document['rows']
    lua=LuaRuntime(unpack_returned_tuples=True)
    resolver=lua.execute((Path(__file__).parent/'names.lua').read_text(encoding='utf-8'))
    rules=json.loads((a.catalog.parent.parent/'names.json').read_text(encoding='utf-8'))
    data=lua_table(lua,rules)
    for row in manifest:
        item={'class':row['weapon'],'Entity':row.get('entity'),'components':row.get('components',{}),
              'DisplayName':row.get('name',row['weapon']),'DisplayNamePlural':row.get('plural',row['weapon'])}
        proposed,reason=resolver.resolve(data,lua_table(lua,item),'ru',False)
        row['display_name_proposal']=proposed
        row['display_name_reason']=reason
    a.manifest.write_text(json.dumps(document,ensure_ascii=False,indent=2),encoding='utf-8')
    captures={(r['weapon'],r['label']):r for r in manifest}
    rows=[]
    for weapon in weapons:
        wid=weapon['id']
        slots=[s for s in weapon['slots'] if s['slot'] in STRUCTURAL]
        alternatives=[(s,o) for s in slots for o in s['options'] if o['id']!=s['default']]
        decision,note=NOTES.get(wid,('preserve','Нет доказанного правила смены модели; сохранять исходное название.'))
        if wid in UNIQUE: decision,note='preserve-unique','Сохранять собственное имя уникального оружия; не наследовать переименование базового класса.'
        variants=[]
        for slot,option in alternatives:
            label=slot['slot']+'-'+option['id']
            capture=captures.get((wid,label))
            variants.append({'slot':slot['slot'],'component':option['id'],'component_name':option['name'],
                'modifiable':slot['modifiable'],'visuals':option['visuals'],
                'capture':capture.get('icon') if capture else None,
                'capture_status':capture['status'] if capture else 'pending',
                'name_decision':decision if slot['slot'] in {'Stock','Barrel','Body','Receiver','Caliber'} else 'preserve',
                'reason':note if slot['slot']!='Handguard' else 'Цевьё/рейка сами по себе не меняют имя модели.'})
        rows.append({'id':wid,'name':weapon['name'],'plural':weapon['plural'],'entity':weapon['entity'],
            'decision':decision,'reason':note,'structural_variants':variants,
            'default_icon':captures.get((wid,'default'),{}).get('icon'),
            'ignored_for_naming':[s['slot'] for s in weapon['slots'] if s['slot'] not in STRUCTURAL]})
    (a.output/'name-matrix.json').write_text(json.dumps({'count':len(rows),'rows':rows},ensure_ascii=False,indent=2),encoding='utf-8')
    with (a.output/'weapon-names.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f);writer.writerow(['class','name','plural','entity','decision','reason','structural_variants'])
        for r in rows:writer.writerow([r[k] for k in ['id','name','plural','entity','decision','reason']]+[len(r['structural_variants'])])
    lines=['# Имена всего живого арсенала','',f"{len(rows)} классов. Это аудит и staged-решения; игровые имена не изменены.",'',
           '| Class | Название из игры | Решение | Значимых альтернатив |','| --- | --- | --- | --- |']
    for r in rows:lines.append(f"| {r['id']} | {r['name']} | {r['decision']} | {len(r['structural_variants'])} |")
    lines+=['','## Решения по семействам','']
    for wid,(decision,note) in NOTES.items():lines.append(f'- **{wid}** ({decision}): {note}')
    (a.output/'names.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'{len(rows)} names; {sum(len(r["structural_variants"]) for r in rows)} structural alternatives')


if __name__=='__main__':main()
