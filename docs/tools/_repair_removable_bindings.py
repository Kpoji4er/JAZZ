"""Restore catalog component IDs in ModItems and companions; --apply writes.

Run with the game/editor closed. Preserve all unrelated bytes and metadata.
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def repair(apply=False):
    source = ROOT / "items.lua"
    items = source.read_bytes()
    changes = {}
    count = 0
    for path in sorted((ROOT / "InventoryItem").glob("*.lua")):
        body = path.read_bytes()
        if b'__parents = { "JAZZ_RemovableAttachment" }' not in body:
            continue
        cid = path.stem.encode()
        count += 1
        binding = b'RemovableComponentId = "' + cid + b'",'
        if b'RemovableComponentId' not in body:
            anchor = b'object_class = "JAZZ_RemovableAttachment",'
            assert body.count(anchor) == 1, path
            newline = b'\r\n' if b'\r\n' in body else b'\n'
            changes[path] = body.replace(anchor, anchor + newline + b'\t' + binding)
        else:
            assert binding in body, path
        # Bound the edit to the next ModItem; never cross into another record.
        pattern = (rb"(PlaceObj\('ModItemInventoryItemCompositeDef', \{(?:(?!PlaceObj\().)*?"
                   rb"'Id', \"" + re.escape(cid) + rb"\",(?:(?!PlaceObj\().)*?"
                   rb"'object_class', \"JAZZ_RemovableAttachment\",)([^}]*?)(\}\),)")
        matches = list(re.finditer(pattern, items, re.S))
        assert len(matches) == 1, (path, len(matches))
        match = matches[0]
        entry = b"'RemovableComponentId', \"" + cid + b'",'
        if b'RemovableComponentId' not in match.group():
            newline = b'\r\n' if b'\r\n' in items else b'\n'
            pos = match.end(1)
            items = items[:pos] + newline + b'\t\t\t\t\t' + entry + items[pos:]
        else:
            assert entry in match.group(), path
    if items != source.read_bytes():
        changes[source] = items
    if apply:
        for path, body in changes.items():
            path.write_bytes(body)
    print(f'catalog={count}, changed_files={len(changes)}, apply={apply}')
    return count, changes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    repair(parser.parse_args().apply)
