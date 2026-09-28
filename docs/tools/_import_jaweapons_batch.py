"""Import audited JaWeapons sources in isolated Blender processes, never JA3.

Source paths are taken from the read-only audit. ZIP paths are checked before
extraction; RAR members are streamed with 7-Zip. Resume uses source SHA256.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path, PureWindowsPath
import re
import shutil
import subprocess
import zipfile
from PIL import Image, ImageDraw, ImageOps


def target_file(root, name):
    rel = PureWindowsPath(name)
    if rel.is_absolute() or rel.drive or '..' in rel.parts:
        raise ValueError(f'Unsafe archive member: {name}')
    dest = root.joinpath(*rel.parts).resolve()
    if not dest.is_relative_to(root.resolve()):
        raise ValueError(name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    return dest


def extract_zip(archive, root, depth=0):
    if depth > 3:
        raise ValueError('Nested archive limit')
    with zipfile.ZipFile(archive) as z:
        for entry in z.infolist():
            if entry.is_dir():
                continue
            dest = target_file(root, entry.filename)
            with z.open(entry) as source, dest.open('wb') as output:
                shutil.copyfileobj(source, output)
            if dest.suffix.lower() == '.zip':
                extract_zip(dest, dest.with_suffix(''), depth + 1)


def extract_source(source, dest, sevenzip):
    if source.suffix.lower() == '.zip':
        extract_zip(source, dest)
    elif source.suffix.lower() == '.rar':
        listing = subprocess.run([sevenzip, 'l', '-slt', '-sccUTF-8', str(source)],
                                 check=True, capture_output=True).stdout.decode('utf-8')
        for block in re.split(r'\r?\n\r?\n', listing.split('----------', 1)[1].strip()):
            match = re.search(r'^Path = (.+)$', block, re.M)
            if not match or 'Folder = +' in block:
                continue
            name = match.group(1).strip()
            destfile = target_file(dest, name)
            with destfile.open('wb') as output:
                subprocess.run([sevenzip, 'x', '-so', str(source), name],
                               stdout=output, stderr=subprocess.PIPE, check=True)
    else:
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest / source.name)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audit', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--blender', type=Path, required=True)
    p.add_argument('--sevenzip', default='C:/Program Files/7-Zip/7z.exe')
    p.add_argument('--only', nargs='*', type=int)
    p.add_argument('--reimport', action='store_true', help='Rebuild derived scenes from unchanged source copies')
    p.add_argument('--summarize-only', action='store_true')
    p.add_argument('--report', type=Path, help='Write compact repository Markdown/JSON report')
    args = p.parse_args()
    rows = json.loads(args.audit.read_text(encoding='utf-8'))
    script = Path(__file__).with_name('_import_jaweapons_scene.py').resolve()
    root = args.out.resolve(); root.mkdir(parents=True, exist_ok=True)
    if args.summarize_only:
        summarize(root, args.report)
        return
    summary = []
    for index, row in enumerate(rows, 1):
        slug = f'{index:02d}_' + re.sub(r'[^A-Za-z0-9_-]+', '_', Path(row['name']).stem).strip('_')
        build = root / slug
        result = {'index': index, 'source': row['path'], 'name': row['name'], 'build': str(build)}
        if row['status'] == 'REJECT':
            result.update(status='REJECT', reason=row['reason']); summary.append(result); continue
        source = Path(row['path'])
        digest = hashlib.file_digest(source.open('rb'), 'sha256').hexdigest()
        state_file = build / 'source-state.json'
        report = build / 'import-report.json'
        if state_file.exists():
            state = json.loads(state_file.read_text(encoding='utf-8'))
            if state['sha256'] != digest:
                raise RuntimeError(f'Source changed: {source}')
        elif not args.only or index in args.only:
            if build.exists():
                raise RuntimeError(f'Unmanaged build exists: {build}')
            build.mkdir()
            extract_source(source, build / 'source', args.sevenzip)
            state_file.write_text(json.dumps({'source': str(source), 'sha256': digest}, indent=2), encoding='utf-8')
        if (not report.exists() or args.reimport) and (not args.only or index in args.only):
            print(f'IMPORT {index}/{len(rows)} {row["name"]}', flush=True)
            with (build / 'blender.log').open('w', encoding='utf-8') as log:
                proc = subprocess.run([str(args.blender), '--background', '--factory-startup',
                                       '--disable-autoexec', '--python-exit-code', '1', '--python', str(script), '--',
                                       '--build', str(build)], stdout=log, stderr=subprocess.STDOUT)
            result['exit_code'] = proc.returncode
        if result.get('exit_code', 0) != 0:
            result.update(status='IMPORT_FAILED', reason='Blender failed; prior scene, if any, is not current evidence')
        elif report.exists():
            result.update(json.loads(report.read_text(encoding='utf-8')))
        else:
            result.update(status='NOT_IMPORTED' if args.only and index not in args.only else 'IMPORT_FAILED',
                          reason='See blender.log' if build.exists() else 'Not selected in this pass')
        result['source_unchanged'] = digest == hashlib.file_digest(source.open('rb'), 'sha256').hexdigest()
        summary.append(result)
        (root / 'batch-results.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'{index}: {result["status"]}', flush=True)
    (root / 'batch-results.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Batch complete:', len(summary), flush=True)
    summarize(root, args.report)


def summarize(root, output=None):
    rows = json.loads((root / 'batch-results.json').read_text(encoding='utf-8'))
    for row in rows:
        report = Path(row['build']) / 'import-report.json'
        if report.exists() and row.get('status') != 'IMPORT_FAILED':
            row.update(json.loads(report.read_text(encoding='utf-8')))
        if row['index'] == 51:
            row['decision'] = 'REJECT_INCOMPLETE'
            row['decision_reason'] = 'Visual check: 11 OBJ without UV include receiver, stock, handguard, barrel and magazine; only scope/bipod textured. Scene retained for diagnosis.'
        elif row['index'] == 46:
            row['decision'] = 'SKIP_DUPLICATE'
            row['decision_reason'] = 'M240 duplicates existing MG58/FN MAG; source FBX 6100 also unsupported by Blender. No new item.'
        else:
            row['decision'] = row['status']
            row['decision_reason'] = row.get('reason', '')
        if row['index'] == 11:
            row['decision_reason'] = 'Body and suppressor atlases restored; model_2 lacks UV (internal/auxiliary geometry visible in isolated review). Keep whole-source review; do not export untextured mesh.'
        elif row['index'] == 25:
            row['decision_reason'] = 'model_17 without UV is a circular accessory detail; rest of weapon has UV. Material sets still require explicit mapping.'
        elif row['index'] == 28:
            row['decision_reason'] = 'model_39 is a tiny planar strip (12 vertices/16 faces), not the receiver; main meshes have UV. Material sets still require explicit mapping.'
    (root / 'batch-results.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    candidates = [r for r in rows if r.get('previews')]
    for start in range(0, len(candidates), 12):
        canvas = Image.new('RGB', (1200, 1280), 'white'); draw = ImageDraw.Draw(canvas)
        for index, row in enumerate(candidates[start:start + 12]):
            size = row['bbox_size_source_units']; axis = 'xyz'[min(range(3), key=lambda i:size[i])]
            path = Path(row['build']) / 'review' / f'Source_axis_{axis}.png'
            tile = ImageOps.contain(Image.open(path).convert('RGB'), (390, 280))
            x, y = index % 3 * 400, index // 3 * 320
            canvas.paste(tile, (x + (400-tile.width)//2, y + 30))
            draw.text((x + 5, y + 3), f'{row["index"]}: {row["name"]}'[:55], fill='black')
            draw.text((x + 5, y + 16), row['status'], fill='black')
        canvas.save(root / f'contact-{start//12+1:02d}.png')
    if output:
        compact = []
        lines = ['# Пакетный импорт JaWeapons — 2026-09-23', '',
                 '**Это импорт исходников в Blender, не установка предметов в JA3.** Игра не запускалась, активные моды не менялись.', '',
                 'IMPORTED_SOURCE: сцена с назначенными материалами, UV и без оставшихся ошибок mesh-аудита; это ещё не rig/entity/InventoryItem. IMPORTED_REVIEW: сцена сохранена, но материалы/UV/геометрия требуют исправления.', '',
                 'Все 47 созданных сцен повторно открыты. Оригиналы не изменены. Сцена Mk 12 хранится только как диагностика отвергнутого источника.', '',
                 'Корень результатов: `Weapons/_batch_jazz_import/`; в каждой папке `source-state.json`, `source/`, `clean/Source.blend`, `review/`, `import-report.json`. Общие превью: `contact-01.png` … `contact-04.png`.', '',
                 '| # | Источник | Решение | Мешей | Без материала / UV | Ошибок геометрии | Причина |',
                 '| ---: | --- | --- | ---: | --- | ---: | --- |']
        for row in rows:
            info = {'index':row['index'], 'name':row['name'], 'decision':row['decision'],
                    'import_status':row['status'], 'build':Path(row['build']).name,
                    'mesh_count':len(row.get('objects',[])),
                    'unresolved_materials':row.get('unresolved_materials',[]),
                    'no_uv':row.get('no_uv',[]), 'geometry_issues':row.get('geometry_issues'),
                    'removed_degenerate_faces':sum(o.get('removed_zero_area_or_normal_faces',0) for o in row.get('objects',[])),
                    'source_unchanged':row.get('source_unchanged'),
                    'game_installed':False, 'reason':row['decision_reason']}
            compact.append(info)
            lines.append(f'| {info["index"]} | {info["name"]} | {info["decision"]} | {info["mesh_count"]} | {len(info["unresolved_materials"])} / {len(info["no_uv"])} | {info["geometry_issues"] if info["geometry_issues"] is not None else "—"} | {info["reason"]} |')
        lines += ['', '## Следующий этап игрового импорта', '',
                  'Нужны отдельные решения по семействам/модулям, сборка разобранных моделей и ориентирование, масштаб по АК74М, привязка к руке, spots, строгий экспорт HGE/FBX → AssetsProcessor, проверки HGM/DDS, регистрация согласованных ModItem/metadata/companion, иконки и локализация. Существующие ID не дублировать. Editor/runtime-приёмка остаётся на последующий запуск владельцем.', '',
                  'Особые зависимости: PPK/FN1910 ждут .380 ACP; G11 — безгильзовых патронов; OICW — двухствольной механики; гранатомёты — боеприпасов; SCAR/G36/XM8 — матрицы модулей. Наличие clean.blend не закрывает эти требования.']
        output.parent.mkdir(parents=True, exist_ok=True)
        output.with_suffix('.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
        output.with_suffix('.json').write_text(json.dumps(compact,ensure_ascii=False,indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
