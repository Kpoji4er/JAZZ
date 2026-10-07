"""Inventory retained armor/helmet sources for future body fitting; never modify models."""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[2]
suite = root.parent
assets = suite / 'jazz_assets/Sources/Character'
out = root / 'docs/technical/armor-sources'
out.mkdir(parents=True, exist_ok=True)
rows = []
for folder in sorted(assets.iterdir()):
    if not folder.is_dir() or folder.name == 'JAZZ_Conrad':
        continue
    for file in sorted(folder.rglob('*')):
        if file.suffix.lower() not in ('.blend', '.glb', '.fbx', '.obj', '.tga'):
            continue
        if any(x in file.parts for x in ('ModAssets', 'installation-backup', 'install-backup', 'refresh-backup')):
            continue
        rel = file.relative_to(suite).as_posix()
        rows.append({'family': folder.name, 'path': rel, 'bytes': file.stat().st_size})
for file in sorted((root / 'meshy_output').rglob('*')):
    if file.suffix.lower() not in ('.blend', '.glb') or 'conrad' in str(file).lower():
        continue
    if not any(t in str(file).lower() for t in ('armor', 'chainmail', 'pasgt', 'rba', 'cuirass', 'helmet', '6b7', 'ssh60')):
        continue
    rows.append({'family': 'Originals and earlier candidates', 'path': file.relative_to(suite).as_posix(), 'bytes': file.stat().st_size})
(out / 'inventory.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
lines = ['# Исходники брони, касок и одежды', '',
         'Каталог существующих локальных исходников. Обновление: `python docs/tools/_catalog_armor_sources.py`.', '',
         'Сохранять оригинальный GLB с текстурами и metadata задания, очищенную геометрию, исходные карты, сцену с ригом и сцену экспорта. Новую посадку делать в отдельном каталоге под целевое тело; не перезаписывать оригинал или ранее принятый риг. Бинарные исходники лежат в `jazz_assets/Sources/Character`, ссылки и инвентарь — здесь. Наличие в каталоге не означает, что файл закоммичен или имеет внешнюю резервную копию.', '',
         'Текущий импорт PASGT/RBA: `import-20261007/original` — неизменный оригинал и SHA256; `clean` — подгонка; `source` — Male rig; `clothed` — LegionGoon Shirt08 reference; `build` — финальная сцена и TGA. Для других тел требуется новая подгонка/риг. Helmet meshes — rigid Head attachments; их origin, offset и scale также нужно сохранять при переносе.', '',
         'Старые варианты не считаются автоматически актуальными. Для выбора установленной версии сверяться с installation receipt, mapping и журналом игровой приёмки. Здесь не заявляется полнота архива для ванильных моделей или прежних HAV: отсутствующие исходники нужно восстановить отдельно.', '']
for family in sorted({r['family'] for r in rows}):
    group = [r for r in rows if r['family'] == family]
    lines += ['## ' + family, '', '<details>', '<summary>Исходные файлы: ' + str(len(group)) + '</summary>', '']
    for r in group:
        link = '../../../../' + r['path']
        lines.append('- [' + r['path'] + '](<' + link + '>)')
    lines += ['', '</details>', '']
(out / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
print('Cataloged', len(rows), 'source files')
