"""Build a local, searchable gallery of captured weapons and actual configurations."""
import argparse
import html
import json
from pathlib import Path
from content_scope import disabled_ids

p=argparse.ArgumentParser(__doc__)
p.add_argument('--staged',type=Path,required=True)
a=p.parse_args()
data=json.loads((a.staged/'manifest.json').read_text(encoding='utf-8'))
names=json.loads((a.staged/'name-matrix.json').read_text(encoding='utf-8'))
disabled=disabled_ids()
data['rows']=[r for r in data['rows'] if r['weapon'] not in disabled]
names['rows']=[r for r in names['rows'] if r['id'] not in disabled]
payload=json.dumps({'manifest':data,'names':names},ensure_ascii=False).replace('</','<\\/')
page='''<!doctype html><html lang="ru"><meta charset="utf-8">
<title>JAZZ — живой арсенал</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#181c22;color:#edf0f3;font:15px system-ui,sans-serif}
header{position:sticky;top:0;background:#222832ef;padding:18px 28px;z-index:2;border-bottom:1px solid #4b535f}
h1{font-size:23px;margin:0 0 8px}p{color:#adb8c5;margin:8px 0;line-height:1.5}
input,select,button{background:#343c48;color:inherit;border:1px solid #677487;border-radius:5px;padding:9px}
input{width:270px}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:18px;padding:24px}
article{background:#252c36;border:1px solid #444f5e;border-radius:10px;overflow:hidden}
.photo{background:#444952;display:flex;justify-content:center;align-items:center;height:185px}
body.light .photo{background:#e6e7e9}body.grid .photo{background-color:#aaa;background-image:conic-gradient(#ddd 25%,transparent 0 50%,#ddd 0 75%,transparent 0);background-size:20px 20px}
.photo img{width:324px;height:165px;object-fit:contain}.body{padding:15px}h2{font-size:18px;margin:0 0 6px}
code{font-size:12px;color:#a4b9d1}select.config{width:100%;margin:12px 0}.warn{color:#ffb390}
details{margin-top:12px}pre{white-space:pre-wrap;font-size:12px;max-height:240px;overflow:auto}a{color:#94cafa}
.meta{font-size:12px;color:#a9b3c1}footer{padding:24px;color:#9caabd}
</style>
<header><h1>JAZZ · живой арсенал</h1><p id="summary"></p>
<input id="search" placeholder="Название или class ID" aria-label="Поиск оружия">
<select id="filter" aria-label="Фильтр"><option value="all">Весь арсенал</option><option value="structural">Есть значимые варианты</option><option value="issues">Замечания</option></select>
<select id="background" aria-label="Фон"><option value="">Тёмный фон</option><option value="light">Светлый фон</option><option value="grid">Прозрачность</option></select>
<p>Снимки установленной игры. Отключённое оружие исключено. Крепления предварительные. Иконки снятых конфигураций установлены; остальные сборки используют прежние иконки. Заголовки показывают проектное имя, автоматическое переименование пока не включено.</p></header>
<main id="list"></main><footer><a href="../SDD.md">SDD</a> · <a href="names.md">Матрица имён</a> · <a href="weapon-names.csv">CSV</a> · <a href="verification.json">Проверка покрытия</a></footer>
<script type="application/json" id="data">PAYLOAD</script>
<script>
const data=JSON.parse(document.getElementById('data').textContent),rows=data.manifest.rows;
const names=data.names.rows,byWeapon=new Map(names.map(n=>[n.id,rows.filter(r=>r.weapon===n.id)]));
document.getElementById('summary').textContent=`${names.length} образцов · ${rows.length} конфигураций · единый свет и обработка`;
function el(tag,text,cls){const e=document.createElement(tag);if(text)e.textContent=text;if(cls)e.className=cls;return e}
function render(){const root=document.getElementById('list');root.replaceChildren();const q=document.getElementById('search').value.toLowerCase(),filter=document.getElementById('filter').value;
for(const n of names){const configs=byWeapon.get(n.id)||[];if(!(n.name+' '+n.id).toLowerCase().includes(q))continue;if(filter==='structural'&&!n.structural_variants.length)continue;if(filter==='issues'&&!configs.some(r=>r.issues.length))continue;
const article=el('article'),photo=el('div',null,'photo'),img=el('img'),body=el('div',null,'body'),title=el('h2',n.name);img.loading='lazy';photo.append(img);body.append(title,el('code',n.id));const select=el('select',null,'config');select.setAttribute('aria-label',n.id+' конфигурация');for(const r of configs){const option=el('option',r.label);option.value=r.label;select.append(option)}body.append(select);
const status=el('p',null,'meta'),reason=el('p',n.reason),details=el('details'),summary=el('summary','Фактические детали и источник'),pre=el('pre'),source=el('a','Исходник RGBA');details.append(summary,pre);body.append(status,reason,source,details);
function update(){const r=configs.find(r=>r.label===select.value);if(!r)return;title.textContent=r.display_name_proposal||n.name;img.hidden=!r.icon;if(r.icon)img.src=r.icon;img.style.width=(r.icon_size||[324,165])[0]+'px';img.style.height=(r.icon_size||[324,165])[1]+'px';img.alt=title.textContent+' '+r.label;source.hidden=!r.rgba;source.href=r.rgba||'#';status.textContent=r.issues.length?r.issues.join(', '):'Снято · '+r.entity;status.className=r.issues.length?'warn':'meta';pre.textContent=JSON.stringify({originalName:r.name,proposedName:r.display_name_proposal,nameRule:r.display_name_reason,components:r.components,parts:r.parts,batch:r.source_batch,sha256:r.source_sha256},null,2)}select.addEventListener('change',update);update();article.append(photo,body);root.append(article)}}
document.getElementById('search').addEventListener('input',render);document.getElementById('filter').addEventListener('change',render);document.getElementById('background').addEventListener('change',e=>document.body.className=e.target.value);render();
</script></html>'''.replace('PAYLOAD',payload)
(a.staged/'review.html').write_text(page,encoding='utf-8')
print(f'Gallery: {len(names["rows"])} weapons, {len(data["rows"])} configurations')
