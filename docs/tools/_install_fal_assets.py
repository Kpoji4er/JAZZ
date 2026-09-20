"""JAZZ-WEAPON-FAL-FAMILY-001: install staged FAL entities into jazz_assets.

Copies the tree produced by _prepare_rifle_assets.py and registers every entity
in items.lua (ModItemEntity) and metadata.lua ('entities' and 'code' lists) as
one transaction. Dry-run by default; pass --apply to write.

  python docs/tools/_install_fal_assets.py \
      --stage <build>/mod-assets-stage/Entities \
      --assets-root ../jazz_assets [--apply]

Run only with the game and Mod Editor closed, otherwise the next editor save
overwrites the generated files.
"""
import argparse
import shutil
import sys
from pathlib import Path

ENTITY_TEMPLATE = (
    "\t\t\t\tPlaceObj('ModItemEntity', {{\n"
    "\t\t\t\t\t'name', \"{name}\",\n"
    "\t\t\t\t\t'ClassParents', {{}},\n"
    "\t\t\t\t\t'entity_name', \"{name}\",\n"
    "\t\t\t\t}}),\n"
)


def read(path):
    return path.read_text(encoding='utf-8')


def write(path, text, apply):
    if not apply:
        return
    backup = path.with_suffix(path.suffix + '.falbak')
    if not backup.exists():
        backup.write_text(read(path), encoding='utf-8')
    path.write_text(text, encoding='utf-8')


def entities_from_stage(stage):
    return sorted(p.stem for p in stage.glob('*.ent'))


def copy_tree(stage, assets_root, apply):
    target = assets_root / 'Entities'
    copied = []
    for src in sorted(stage.rglob('*')):
        if src.is_dir():
            continue
        rel = src.relative_to(stage)
        dst = target / rel
        same = dst.exists() and dst.stat().st_size == src.stat().st_size
        copied.append((rel.as_posix(), 'same' if same else ('replace' if dst.exists() else 'new')))
        if apply:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    return copied


def patch_items(path, names, apply):
    text = read(path)
    added = []
    marker = "PlaceObj('ModItemEntity', {"
    last = text.rfind(marker)
    if last < 0:
        raise SystemExit('no ModItemEntity block found in %s' % path)
    end = text.find('}),\n', last)
    if end < 0:
        raise SystemExit('malformed ModItemEntity block in %s' % path)
    insert_at = end + len('}),\n')
    block = ''
    for name in names:
        if '"%s"' % name in text:
            continue
        block += ENTITY_TEMPLATE.format(name=name)
        added.append(name)
    if block:
        text = text[:insert_at] + block + text[insert_at:]
        write(path, text, apply)
    return added


def patch_metadata(path, names, apply):
    text = read(path)
    added = {'entities': [], 'code': []}
    for key, fmt in (('entities', '\t\t"{name}",\n'), ('code', '\t\t"Entities/{name}.lua",\n')):
        head = text.find("'%s', {" % key)
        if head < 0:
            raise SystemExit("no '%s' list in %s" % (key, path))
        close = text.find('\n\t},', head)
        if close < 0:
            raise SystemExit("unterminated '%s' list in %s" % (key, path))
        block = ''
        existing = text[head:close]
        for name in names:
            needle = '"%s"' % name if key == 'entities' else '"Entities/%s.lua"' % name
            if needle in existing:
                continue
            block += fmt.format(name=name)
            added[key].append(name)
        if block:
            text = text[:close + 1] + block + text[close + 1:]
    if added['entities'] or added['code']:
        write(path, text, apply)
    return added


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--stage', type=Path, required=True)
    p.add_argument('--assets-root', type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    a = p.parse_args()

    names = entities_from_stage(a.stage)
    if not names:
        raise SystemExit('no .ent files in %s' % a.stage)
    print('entities: ' + ', '.join(names))

    for rel, state in copy_tree(a.stage, a.assets_root, a.apply):
        print('  %-8s %s' % (state, rel))

    items_added = patch_items(a.assets_root / 'items.lua', names, a.apply)
    meta_added = patch_metadata(a.assets_root / 'metadata.lua', names, a.apply)
    print('items.lua ModItemEntity added: ' + (', '.join(items_added) or 'none'))
    print('metadata entities added: ' + (', '.join(meta_added['entities']) or 'none'))
    print('metadata code added: ' + (', '.join(meta_added['code']) or 'none'))
    print('APPLIED' if a.apply else 'DRY RUN - nothing written')


if __name__ == '__main__':
    sys.exit(main())
