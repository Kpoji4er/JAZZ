"""Render default/combined review sheets using the exact runtime Lua selector."""
import argparse,html,json
from pathlib import Path
from PIL import Image,ImageDraw
from lupa import LuaRuntime
from icon_layout import fit

p=argparse.ArgumentParser(__doc__);p.add_argument('--library',type=Path,required=True);p.add_argument('--graphs',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--ids',nargs='+');a=p.parse_args()
registry=json.loads((a.library/'registry.json').read_text(encoding='utf-8'))
if not a.ids:a.ids=sorted(registry['weapons'])
lua=LuaRuntime(unpack_returned_tuples=True)
def table(v):
 if isinstance(v,dict):return lua.table_from({k:table(x) for k,x in v.items()})
 if isinstance(v,list):return lua.table_from([table(x) for x in v])
 return v
selector=lua.execute(Path(__file__).with_name('layer_selector.lua').read_text(encoding='utf-8'));data=table(registry)
sheet=Image.new('RGB',(1020,220*min(len(a.ids),8)),(38,42,46));draw=ImageDraw.Draw(sheet);evidence=[];sections=[]
a.output.mkdir(parents=True,exist_ok=True)
for y,weapon in enumerate(a.ids):
 profile=registry['weapons'][weapon];base={s['slot']:s['default'] for s in profile['slots']}
 rows=json.loads((a.graphs/(weapon+'.json')).read_text(encoding='utf-8'))['rows']
 candidates=sorted(rows,key=lambda r:sum(bool(v) and v!=base.get(k) for k,v in (r['components'] or {}).items()),reverse=True)
 builds=[{'weapon':weapon,'entity':profile['base']['__host'],'components':base}]
 for row in candidates:
  result=selector.resolve(data,table({'class':weapon,'Entity':row['entity'],'components':row['components']}))
  plan=result[0] if isinstance(result,tuple) else result
  if plan:builds.append(row)
  if len(builds)==3:break
 cards=[]
 for x,row in enumerate(builds):
  result=selector.resolve(data,table({'class':weapon,'Entity':row['entity'],'components':row['components']}))
  plan=result[0] if isinstance(result,tuple) else result
  if not plan:raise ValueError('Default failed: '+weapon)
  canvas=Image.new('RGBA',(1296,660))
  for _,layer in plan.layers.items():canvas.alpha_composite(Image.open(a.library/'layers'/(layer.id+'.png')).convert('RGBA'))
  icon=fit(canvas,(profile['width'],profile['height']));icon.save(a.output/(weapon+'-'+str(x)+'.png'))
  if y<8:
   sheet.paste(icon,(x*340+(340-icon.width)//2,y*220+35),icon)
   draw.text((x*340+8,y*220+8),weapon+(' default' if x==0 else ' combined '+str(x)),fill='white')
  evidence.append({'weapon':weapon,'column':x,'components':row['components'],'key':plan.key})
  changes=[k+' = '+(v or '(empty)') for k,v in (row['components'] or {}).items() if v!=base.get(k)]
  cards.append('<figure><figcaption>'+('Базовая сборка' if x==0 else 'Несколько модулей · '+str(x))+'</figcaption><div class="image"><img src="'+html.escape(weapon+'-'+str(x)+'.png')+'"></div><details><summary>Состав</summary><pre>'+html.escape('\n'.join(changes) or 'По умолчанию')+'</pre></details></figure>')
 sections.append('<section data-name="'+html.escape(weapon.lower())+'"><h2>'+html.escape(weapon)+'</h2><div class="builds">'+''.join(cards)+'</div></section>')
sheet.save(a.output/'preview.png');(a.output/'builds.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
(a.output/'review.html').write_text('''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>JAZZ · Сборки оружия</title><style>
body{margin:32px auto;padding:0 24px;max-width:1120px;background:#181b20;color:#e6e9ec;font:16px system-ui}h1{margin-bottom:8px}p{color:#adb6c0}input{position:sticky;top:12px;z-index:2;box-sizing:border-box;width:100%;padding:14px;border:1px solid #56616e;border-radius:8px;background:#242a32;color:white;font:inherit}section{margin-top:32px;border-top:1px solid #3b434d}h2{font-size:20px}.builds{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px}figure{margin:0;background:#262a2e;padding:12px;border-radius:8px}figcaption{color:#adb6c0;font-size:14px}.image{height:185px;display:flex;align-items:center;justify-content:center}img{max-width:100%;height:auto}details{font-size:12px;color:#a5b0bc}pre{white-space:pre-wrap;overflow-wrap:anywhere}footer{margin:40px 0;color:#8f9aa7}
</style><h1>Сборки оружия</h1><p>Базовое оружие и примеры одновременной установки нескольких модулей. Изображения собраны тем же Lua-селектором, который используется интерфейсом игры.</p><input id="search" placeholder="Найти оружие" aria-label="Найти оружие">'''+''.join(sections)+'''<footer>Показанные примеры — часть сочетаний. Полное покрытие проверяется отдельно по каталогу и фактическим графам игры.</footer><script>document.querySelector('#search').addEventListener('input',e=>document.querySelectorAll('section').forEach(s=>s.hidden=!s.dataset.name.includes(e.target.value.toLowerCase().trim())))</script></html>''',encoding='utf-8')
print(json.dumps({'weapons':len(a.ids),'builds':len(evidence),'image':str(a.output/'preview.png')}))
