"""Package reviewed staging, human-readable results, and a compact comparison board."""
import argparse
from collections import Counter
import json
from pathlib import Path
import zipfile
from PIL import Image,ImageDraw,ImageFont

p=argparse.ArgumentParser(__doc__)
p.add_argument('--live',type=Path,required=True)
p.add_argument('--batches',nargs='+',required=True)
a=p.parse_args();stage=a.live/'staged'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
m=read(stage/'manifest.json');v=read(stage/'verification.json');integrity=read(stage/'integrity.json')
audit=read(stage/'visual-audit.json');names=read(stage/'name-matrix.json')
rows=m['rows'];bykey={(r['weapon'],r['label']):r for r in rows}
selected=[('AK74','default'),('AK74','Stock-JAZZ_StockLightUnFolded'),
    ('AKM','default'),('AKM','Stock-JAZZ_StockLightUnFolded'),
    ('M4A1','default'),('M4A1','Magazine-JAZZ_MagSmall30_20'),
    ('DragunovSVD','default'),('DragunovSVD','Stock-JAZZ_StockLight')]
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',13)
board=Image.new('RGB',(700,4*230+55),(29,34,41));draw=ImageDraw.Draw(board)
draw.text((18,16),'JAZZ · реальные модели, единый стиль',font=font,fill='white')
for i,key in enumerate(selected):
    row=bykey.get(key)
    if not row or not row.get('icon'):continue
    x=i%2*350;y=55+i//2*230
    draw.rectangle((x+8,y,x+342,y+168),fill=(215,218,223) if i%2 else (65,71,81))
    icon=Image.open(stage/row['icon']);board.paste(icon,(x+13,y+2),icon)
    draw.text((x+14,y+178),row.get('display_name_proposal',row['name']),font=font,fill='white')
    draw.text((x+14,y+205),row['label'].replace('JAZZ_','')[:43],font=small,fill=(175,188,205))
board.save(a.live/'preview.png')
default_rows=[r for r in rows if r['label']=='default']
rejected=[r for r in rows if r['status']!='captured']
flagged=[r for r in rows if r['issues'] and r['status']=='captured']
body=['# Результаты живой съёмки оружия','',
    '28.09.2026. Источник: запущенная владельцем JA3Debug / ModEditor. Результат находится в staging; активный комплект не изменён.','',
    '## Поставка','',
    f'- Классов в каталоге: **{m["catalog_count"]}**, изображения штатной конфигурации: **{sum(r["status"]=="captured" for r in default_rows)} / {m["catalog_count"]}**.',
    f'- В реестре **{len(rows)} конфигураций**, создано **{v["icons"]} прозрачных PNG 324×165** и столько же крупных RGBA исходников.',
    f'- Нештатные/недопустимые замены: **{len(rejected)}** записей с явным статусом. Дополнительные RIS-конфигурации записаны отдельно.',
    f'- Имён в матрице: **{len(names["rows"])}**, значимых альтернатив: **{sum(len(r["structural_variants"]) for r in names["rows"])}**.',
    '- [Галерея](staged/review.html): поиск, выбор конфигурации, три фона, проектные имена, фактические детали и source hash.',
    '- [SDD и self-review](SDD.md), [CSV имён](staged/weapon-names.csv), [таблица имён](staged/names.md), [повторение съёмки](REPLAY.md).','',
    '## Что установлено','',
    '- M4 20-round magazine — прямой ванильный WeaponAttA_MagazineCAR15_02; старый Blender-вариант не использован.',
    '- АК-74 → АКС-74, АКМ → АКМС и vz. 58 P/V заданы явными staged-правилами для проверенных семейств прикладов. Положение складного приклада само по себе не меняет имя. Основания и источники обозначений приведены в SDD.',
    '- СВД с нынешним StockLight не становится СВДС: у модели цельная thumbhole-ложа. Предложенное правило выключено.',
    '- M4A1/M16A4 требуют RIS для Side/Under; после зафиксированных отказов сняты дополнительные сборки с нужным цевьём.',
    '- У четырёх квестовых вариантов ComponentSlots класса/экземпляра и InventoryItemDefs расходятся по старым/JAZZ IDs. Сняты обе формы; 32 дополнительных записи — 14 preset-вариантов и 18 RIS-сборок.',
    '- Крепления provisional. Их сущности и parent/spot сохранены для отдельного этапа и адресной пересъёмки.','',
    '## Проверки и ограничения','',
    f'- Полнота single-slot реестра, файлы, форматы, alpha, запрошенные компоненты, имена: **{"PASS" if integrity["pass"] else "FAIL"}**, см. [integrity.json](staged/integrity.json).',
    f'- Автоматических замечаний к обработанным кадрам после пересъёмки: **{len(flagged)}**. Полный список: [verification.json](staged/verification.json).',
    f'- Сравнено **{audit["checked_single_slot_rows"]}** графов компонентов; **{len(audit["review_queue"])}** расхождений между объявленными entities и vis.parts вынесено в [visual-audit.json](staged/visual-audit.json). Это очередь проверки зависимостей/креплений, не автоматически доказанные ошибки модели.',
    '- Просмотрены контактные листы всех штатных моделей и целевые структурные варианты; не заявляется ручная проверка каждого пикселя всех одиночных прицелов.',
    '- Покрыты одиночные замены и отдельные RIS-сборки, не весь декартов продукт комбинаций. UI-доступность всех вариантов не доказана прямым setter.',
    '- Галерея проверена по данным и синтаксису; интерактивный click-through в браузере не заявляется.',
    '- 72 offline Lua-проверки структурных имён проходят. Исправлены диагностические предупреждения capture tooling; точный фактический light recipe и повторная проверка описаны в SDD.',
    '- Ранние тёмные/пилотные снимки исключены из итогового manifest. Плоские live-иконки не выдаются за независимые слои компонентов.','',
    '## Восстановление игры','']
for batch in a.batches:
    r=read(a.live/batch/'capture-report.json')
    body.append(f'- `{batch}`: {r["phase"]}; камера совпала: {r.get("original_camera")==r.get("restored_camera")}; строк: {len(r["rows"])}.')
    if 'restored_render' in r:
        body.append(f'  Render flags совпали: {r["original_render"]==r["restored_render"]}; исходный lightmodel восстановлен: {r["restored_light"]}; временные объекты освобождены: {r["disposed"]}.')
body+=['','[Отдельный read-only осмотр зоны съёмки после cleanup](cleanup.result.txt): временных объектов нет. Наёмники/сохранения не редактировались, установка и публикация не выполнялись. Диагностический overlay скрыт, лог сохранён; игровая сцена проверена визуально.','',
       '## Решение по SDD','',
       '**APPROVE — self-review по поручению владельца.** Утверждены staging и архитектурное решение. Runtime-интеграция и независимая/human приёмка не объявляются завершёнными.','']
(a.live/'REPORT.md').write_text('\n'.join(body),encoding='utf-8')
archive=a.live/'JAZZ-weapon-capture.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for path in [a.live/'SDD.md',a.live/'REPORT.md',a.live/'REPLAY.md',a.live/'preview.png',a.live/'catalog.json',
                 a.live/'catalog-before-capture.json',a.live/'lighting-consistency.json',a.live/'cleanup.json']:
        z.write(path,path.relative_to(a.live).as_posix())
    for path in stage.rglob('*'):
        if path.is_file():z.write(path,path.relative_to(a.live).as_posix())
    for batch in a.batches:
        for filename in ['capture-report.json','capture-plan.json','capture-source.lua']:
            path=a.live/batch/filename
            if path.exists():z.write(path,path.relative_to(a.live).as_posix())
    if (a.live/'cleanup.result.txt').exists():z.write(a.live/'cleanup.result.txt','cleanup.result.txt')
print(f'{v["icons"]} icons; {archive.stat().st_size/1048576:.1f} MiB archive')
