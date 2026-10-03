"""Build contact sheets and an HTML review from rendered Meshy batch outputs."""
import html
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root=Path(__file__).resolve().parents[2]/'meshy_output/armor-batch-20261002'
batch=json.loads((root/'batch.json').read_text(encoding='utf-8'))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
labels={'ImprovisedCuirass':'Кираса','Chainmail':'Кольчуга','TireBrigantine':'Бригантина','TireArmor':'Шинная броня','LeatherArmor':'Кожаная броня'}
cards=[];strips=[];records=[]
for job in batch['jobs']:
    project=Path(job['project']); report=project/'views-complete.json'
    if not report.exists(): continue
    info=json.loads(report.read_text(encoding='utf-8'))
    strip=Image.new('RGB',(1600,450),'#252a32');draw=ImageDraw.Draw(strip)
    for i,(view,label) in enumerate(zip(['front','back','side','oblique'],['Спереди','Сзади','Сбоку','Три четверти'])):
        image=Image.open(project/(view+'.png')).convert('RGB');image.thumbnail((400,400));strip.paste(image,(400*i,50))
        draw.text((400*i+12,15),label,font=font,fill='white')
    strip.save(project/'views.jpg',quality=94);strips.append((labels[job['name']],strip))
    rel=project.relative_to(root).as_posix();name=job['name']
    cards.append(f'<section><h2>{labels[name]} · {info["triangles"]:,} треугольников</h2><p><a href="{rel}/{name}.glb">Скачать GLB</a> · <a href="{rel}/views.jpg">Открыть ракурсы</a></p><img src="{rel}/views.jpg" alt="Четыре ракурса"><p class="small">{job["resource"]} / {job["task_id"]} · {job["consumed_credits"]} кредитов</p></section>')
    records.append(dict(name=name,task_id=job['task_id'],triangles=info['triangles'],consumed_credits=job['consumed_credits'],rigged=info['rigged']))
if len(records)!=5: raise RuntimeError('Wait until all five models have rendered before final review')
sheet=Image.new('RGB',(1600,500*len(strips)),'#252a32');draw=ImageDraw.Draw(sheet)
for i,(label,strip) in enumerate(strips):
    draw.text((15,500*i+10),label,font=font,fill='white');sheet.paste(strip,(0,500*i+50))
sheet.save(root/'all-views.jpg',quality=93)
page='<!doctype html><html lang="ru"><meta charset="utf-8"><title>Кустарная броня — Meshy</title><style>body{font:18px system-ui;background:#181d24;color:#edf1f8;max-width:1600px;margin:32px auto;padding:20px}a{color:#8bc9ff}img{width:100%}section{margin:40px 0}.small{font-size:14px;color:#b5becb}</style><h1>Пять моделей брони · Meshy</h1><p>Рендеры исходных GLB в Blender: спереди, сзади, сбоку, три четверти. Без подгонки и установки в JA3. Twaron/Guardian/Zylon исключены. Фактически списано 150 кредитов; неудачная первая бригантина — 0.</p><p><strong>Визуальная проверка:</strong> кираса и шинная броня объёмные. Кольчуга, бригантина и кожа почти плоские, с повторением лицевой стороны на обороте; у кожи лишняя прямоугольная рамка. Эти три результата непригодны как полноценные носимые жилеты без переработки. Успешный статус Meshy означает завершение генерации, а не художественную приёмку.</p>'+''.join(cards)+'</html>'
(root/'review.html').write_text(page,encoding='utf-8')
(root/'review-summary.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,ensure_ascii=False,indent=2))
