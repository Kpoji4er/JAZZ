"""Write a reviewable status ledger from the 32-position active source audit.
--sources sources.json --output report.md. Import success is never installation.
"""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
r=json.loads(a.sources.read_text());assert {e['number'] for e in r['entries']}==set(range(1,34))-{10}
lines=['# Новая очередь оружия: состояние подготовки 03.10.2026','','Текущая очередь: 32 позиции, 38 файлов-источников. Mk12 временно исключён владельцем; номера остальных позиций сохранены. Исходные архивы не изменены.',
'Это реестр подготовки, **не отчёт об установленном оружии**. Общая игровая проверка отложена владельцем до сборки всего комплекта.',
'','| № | Позиция | Существующие ID | Подготовка исходников |','| --- | --- | --- | --- |']
for entry in sorted(r['entries'],key=lambda e:e['number']):
 notes=[]
 for src in entry['sources']:
  row=r['sources'][src];audit=row.get('audit',{});unmapped=len(audit.get('unresolved_materials',[]));no_uv=len(audit.get('no_uv',[]))
  text=Path(src).name+': '+row['status']
  if unmapped:text+=f'; без привязки материала {unmapped}'
  if no_uv:text+=f'; без UV {no_uv}'
  notes.append(text)
 if not notes:notes=['Переиспользуются текущие модели; объединение M14/M21 ещё не реализовано.']
 if entry['number']==1:
  notes.append('АЕК установлен как кандидат: 8 entity, один модульный предмет 971/973С, RU/EN и иконки; compiled/winding, Lua и регистрация PASS, игровая проверка впереди.' if entry.get('integration')=='INSTALLED_CANDIDATE_RUNTIME_PENDING' else 'Отдельная сборка АЕК: 8 деталей скомпилированы, source/compiled geometry и winding PASS; установка и Lua ещё не выполнены.')
 lines.append('| '+str(entry['number'])+' | '+entry['name']+' | '+', '.join('`'+s+'`' for s in entry['existing_ids'])+' | '+'<br>'.join(notes)+' |')
pbr_path=a.sources.parent/'pbr-stage/pbr-stage.json'
if pbr_path.exists():
 groups=[g for key,s in json.loads(pbr_path.read_text())['sources'].items() if key in r['sources'] for g in s['groups'].values()]
 count=sum(g['status']=='STAGED_EXPLICIT_PBR' for g in groups)
 lines+=['','## Подготовка карт','',f'В staging подготовлено {count} однозначных полных PBR-наборов. Декодированные BC/NM сохранены без изменений, RM=(rough,rough,metal) проверен после записи. Привязка к мешам и установка не выполнены. Неполные/неоднозначные наборы и specular-glossiness требуют отдельного разбора; отсутствие набора в этом отчёте не означает отсутствие карт в GLB/Blender.']
lines+=['','## Ограничения доказательств','','- `IMPORTED_SOURCE`: Blender-сцена сохранена и повторно открыта; это не проверка всех вариантов обвеса, материалов в JA3 или анимаций.',
'- `IMPORTED_REVIEW`: материалы/UV/геометрия требуют разбора. Кандидаты атласов не назначаются автоматически по оценке совпадения фона.',
'- Mk12 временно исключён владельцем. Историческое заключение `REJECT_INCOMPLETE` и исходные файлы сохранены; его UV не блокируют текущую очередь.',
'- У нового прохода префиксы `qNN`: старый импортёр резервирует `01_`, `09_`, `11_` для PPK/Кипариса/Кедра. Неудачные первые сборки Kar98 сохранены отдельно, исправленные проходят импорт.',
'- Восстановление bindings, физический масштаб и хват, модульные конфигурации, иконки, регистрация, боеприпасы, RU/EN, миграции и offline Lua остаются обязательными этапами.',
'','## Воспроизведение','','Скрипты: `_weapon_import_20261003_sources.py`, `_weapon_import_20261003_atlases.py`, `_weapon_import_20261003_report.py`.',
'Машинные артефакты: `<WEAPON_SOURCE_ROOT>/_weapon_import_20261003/sources.json` и `atlas-review/atlas-review.json`. SHA256 каждого источника сохранён в sources.json; старые сборки переиспользованы только при совпадении SHA256.','']
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text('\n'.join(lines),encoding='utf-8');print(a.output)
