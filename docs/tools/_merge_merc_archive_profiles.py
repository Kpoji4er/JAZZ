"""Extend the reviewed profile manifest to fix stale runtime CSV overrides.

Inputs are the extracted items.lua and checked-in English biography translations.
Keeps equivalent, already edited narrative biographies. Does not write runtime.
"""
import argparse
import json
import re
from pathlib import Path
from _merge_merc_archive import ROOT, units, translation, csv_rows, TEXT_FIELDS

NAMES = {
 'Jazz_Spider':'Dr. Donna "Spider" Houston',
 'Jazz_Blade':'Bill "Razor" Lamont',
 'Jazz_Madman':'Kevin "Mad Dog" Cameron',
 'Jazz_Grom':'Major Sergey Gromov',
 'Jazz_Iggy':'Igmus "Iggy" Palkov',
 'Jazz_Benny':'Alexandra Benedict',
 'Jazz_Quinten':'Dr. Daniel Quinten',
 'Jazz_Vicious':'Jean-Pierre "Malice" Viau',
 'Jazz_Nervous':'Frankie "Haywire" Gordon',
 'Jazz_Flo':'Florence Gabriel',
 'Jazz_Cougar':'Jim "Cougar" Wallace',
 'Jazz_Dynamo':'Greg "Dynamo" Duncan',
 'Jazz_Monk':'Viktor "Monk" Kolesnikov',
 'Jazz_Allik':'Janno "Allik" Allik',
 'Jazz_Static':'Kirk "Static" Stevenson',
 'Jazz_Highball':'Dr. Clifford Highball',
 'Jazz_Bull':'John "Bull" Peters',
 'Jazz_Cord':'Doug "Gasket" Milton',
 'Jazz_Hobbit':'Tim "Gumpy" Hillman',
 'Jazz_Ricochet':'Tim "Numb" Sutton',
 'Jazz_Meat':'Thorton "Bubba" Jones',
 'Jazz_Shank':'Briem "Shank" Druz',
 'Jazz_Vince':'Dr. Vincent Beaumont',
 'Jazz_Hitman':'Richard Ruthven',
 'Jazz_Vilde':'Lennart "Scream" Vilde',
 'Jazz_Grace':'Graziella Girelli',
 'Jazz_Lucky':'Luc "Lucky" Fabre',
 'Jazz_Eskimo':'Emil "Eskimo" Kimos',
}
NICKS={'Jazz_Colby':'Trevor','Jazz_Rothman':'Stephan','Jazz_Steiger':'Rudolf','Jazz_Hitman':'Slay'}
REPAIRS={
 'безвоздмездно':'безвозмездно', 'задейстован':'задействован', 'Органзиации':'Организации',
 'как то':'как-то', 'не разумно':'неразумно', 'отрял':'отряд', 'в гораж':'в горах',
 'совего':'своего', 'постречался':'повстречался', 'по сравнею':'по сравнению',
 'решительно не возможно':'решительно невозможно', 'какую то':'какую-то',
 'стралась':'старалась', 'как бы она не':'как бы она ни', 'Как бы она не':'Как бы она ни',
 'не ясно':'неясно', 'уже нет тот':'уже не тот', 'со Луизой':'с Луизой',
 'конфликта,а':'конфликта, а', 'сколько нибудь':'сколько-нибудь',
 'в Арулько ту же тюрьму':'в ту же тюрьму в Арулько',
 'Мигеля Кордона':'Мигеля Кордоны', 'Динамо самый':'Динамо — самый',
 'Лейтенант Конрад Джиллет можно сказать,':'Лейтенант Конрад Джиллет, можно сказать,',
 'Джим настоящий':'Джим — настоящий', 'Грациелла Джирелли потомок':'Грациелла Джирелли — потомок',
 'наем':'наём', 'Наем':'Наём', 'сапер':'сапёр', 'Сапер':'Сапёр',
 'вертолет':'вертолёт', 'заключенн':'заключённ', 'рассеян':'рассеян',
 'уверен,':'уверен,', 'остается':'остаётся', 'подведет':'подведёт',
 'не везет':'не везёт', 'умрет':'умрёт', 'принесет':'принесёт',
 'тяжел':'тяжёл', 'разношерст':'разношёрст', 'все так же':'всё так же',
 'все, что угодно':'всё что угодно', 'еще':'ещё',
}

def polish(text):
    for old,new in REPAIRS.items():text=text.replace(old,new)
    text=text.replace(' - ',' — ').replace('  ',' ').strip()
    if text[-1:] not in '.!?':text+='.'
    return text

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args()
    source=units(a.source.read_text(encoding='utf-8-sig'))
    path=Path(__file__).with_name('_merge_merc_archive_translations.json')
    data=json.loads(path.read_text(encoding='utf-8'))
    bios=json.loads(path.with_name('_merge_merc_archive_bios.json').read_text(encoding='utf-8'))
    for uid,en in bios.items():
        if uid.startswith('__'):continue
        raw=translation(source[uid][3]['Bio'][2])[1]
        data[uid+'.Bio']={'ru':polish(raw),'en':en,'source':'archive'}
    for uid,en in NAMES.items():
        raw=translation(source[uid][3]['Name'][2])[1]
        data[uid+'.Name']={'ru':raw,'en':en,'source':'archive'}
    for uid,en in NICKS.items():
        for field in ['Nick','AllCapsNick']:
            raw=translation(source[uid][3][field][2])[1]
            data[uid+'.'+field]={'ru':raw.strip(),'en':en if field=='Nick' else en.upper(),'source':'archive'}
    runtime={r['ID']:r for r in csv_rows(ROOT/'English.csv')}
    for uid,(_,_,_,props) in source.items():
        if props.get('IsMercenary',('','',''))[2]!='true':continue
        for field in ['Email','snype_nick']:
            if field not in props:continue
            tid,text=translation(props[field][2])
            if re.search('[А-Яа-яЁё]',text):continue
            if uid+'.'+field in data:continue
            if tid in runtime and runtime[tid]['Translation']!=text:
                data[uid+'.'+field]={'ru':text,'en':text,'source':'archive'}
    data['Jazz_Monk.Title']['ru']='Буддийский монах'
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Reviewed profile overrides:',len(data))

if __name__=='__main__':main()
