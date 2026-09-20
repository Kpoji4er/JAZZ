"""JAZZ-WEAPON-FAL-FAMILY-001: add the tactical FAL weapon item.

The tactical rifle keeps the vanilla Weapon_FNFAL entity and differs through
components, so this script has three jobs:

  1. clone the FNFAL weapon block into JAZZ_FNFAL_Tactical with tier 3 stats,
     the RIS handguard and the long barrel options (REQ-004)
  2. add the RIS handguard WeaponComponent
  3. mirror every WeaponComponentVisual that carries ApplyTo = "FNFAL" onto the
     new weapon id, swapping the stock for the tactical polymer entity

WeaponComponentVisual.ApplyTo matches the inventory item id, not the entity, so
without step 3 the new rifle would lose every attachment visual.

  python docs/tools/_add_fal_tactical_item.py [--apply]
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NEW_ID = 'JAZZ_FNFAL_Tactical'
LOC = {'name': 990002700, 'plural': 990002701, 'desc': 990002702,
       'hint': 990002703, 'handguard': 990002704}

STAT_OVERRIDES = {
    'Reliability': 70, 'Cost': 8500, 'Tier': 3, 'RestockWeight': 60,
    'Recoil': 36, 'AimAccuracy': 14, 'WeaponRange': 57, 'BaseJamChance': -15,
    'RepairCost': 12, 'WeaponResource': 8200,
}
BARREL_OLD = '"JAZZ_BarrelNormal",'
BARREL_NEW = ('"JAZZ_BarrelNormal",\n%(i)s"JAZZ_BarrelLong",\n%(i)s"JAZZ_BarrelLongImproved",')

HANDGUARD_COMPONENT = """\t\t\t\t\tPlaceObj('ModItemWeaponComponent', {{
\t\t\t\t\t\tDisplayName = T({hg}, --[[ModItemWeaponComponent JAZZ_FNFAL_TacHandguard DisplayName]] "RIS Handguard"),
\t\t\t\t\t\tModificationDifficulty = -25,
\t\t\t\t\t\tSlot = "Handguard",
\t\t\t\t\t\tVisuals = {{
\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {{
\t\t\t\t\t\t\t\tApplyTo = "{wid}",
\t\t\t\t\t\t\t\tEntity = "JAZZ_FNFAL_TacHandguard",
\t\t\t\t\t\t\t\tSlot = "Handguard",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}}),
\t\t\t\t\t\t}},
\t\t\t\t\t\tcomment = "FAL family - tactical RIS forend",
\t\t\t\t\t\tgroup = "FNFAL Specific",
\t\t\t\t\t\tid = "JAZZ_FNFAL_TacHandguard",
\t\t\t\t\t}}),
"""


def find_block(text, marker_id):
    """Return (start, end) of the ModItem PlaceObj carrying 'Id', "<marker_id>"."""
    needle = '\'Id\', "%s",' % marker_id
    at = text.find(needle)
    if at < 0:
        raise SystemExit('item not found: %s' % marker_id)
    start = text.rfind("PlaceObj('ModItemInventoryItemCompositeDef', {", 0, at)
    if start < 0:
        raise SystemExit('cannot find block head for %s' % marker_id)
    indent = ''
    line_start = text.rfind('\n', 0, start) + 1
    indent = text[line_start:start]
    close = '\n%s}),\n' % indent
    end = text.find(close, at)
    if end < 0:
        raise SystemExit('cannot find block end for %s' % marker_id)
    return start, end + len(close), indent


def build_tactical(block, indent):
    out = block
    out = out.replace('\'Id\', "FNFAL",', '\'Id\', "%s",' % NEW_ID, 1)
    out = out.replace('\'comment\', "Tier 2-3",', '\'comment\', "Tier 3 - JAZZ-WEAPON-FAL-FAMILY-001",', 1)
    out = re.sub(r"'Icon', \"[^\"]+\",", '\'Icon\', "Mod/e6L4ECj/WeaponIcons/%s.png",' % NEW_ID, out, count=1)

    for field, value in STAT_OVERRIDES.items():
        pattern = r"'%s', -?\d+," % field
        replacement = "'%s', %d," % (field, value)
        out, n = re.subn(pattern, replacement, out, count=1)
        if n == 0:
            raise SystemExit('field %s not present in FNFAL block' % field)

    # Localisation for the new public id. re.sub treats backslashes in the
    # replacement as template escapes, so every replacement goes through a
    # lambda; otherwise the \n inside AdditionalHint becomes a real newline and
    # JA3 refuses to load items.lua (see .cursor/rules/jazz-lua-short-strings).
    ICON = '<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120>'
    hint = ICON + ' Планки везде \\n' + ICON + ' Ровнее в очереди \\n' + ICON + ' Длинный ствол'
    desc = ('Та же фалочка, но собранная под современное железо: цевьё на планках, '
            'полимерный приклад, место под длинный ствол. Бельгийская классика, '
            'доведённая до ума теми, кому из неё стрелять.')
    fields = [
        (r"'DisplayName', T\(\d+, --\[\[[^\]]*\]\] \"[^\"]*\"\),",
         "'DisplayName', T(%d, --[[ModItemInventoryItemCompositeDef %s DisplayName]] \"FN FAL Tactical\")," % (LOC['name'], NEW_ID)),
        (r"'DisplayNamePlural', T\(\d+, --\[\[[^\]]*\]\] \"[^\"]*\"\),",
         "'DisplayNamePlural', T(%d, --[[ModItemInventoryItemCompositeDef %s DisplayNamePlural]] \"FN FAL Tacticals\")," % (LOC['plural'], NEW_ID)),
        (r"'Description', T\(\d+, --\[\[[^\]]*\]\] '[^']*'\),",
         "'Description', T(%d, --[[ModItemInventoryItemCompositeDef %s Description]] \"%s\")," % (LOC['desc'], NEW_ID, desc)),
        (r"'AdditionalHint', T\(\d+, --\[\[[^\]]*\]\] \"[^\"]*\"\),",
         "'AdditionalHint', T(%d, --[[ModItemInventoryItemCompositeDef %s AdditionalHint]] \"%s\")," % (LOC['hint'], NEW_ID, hint)),
    ]
    for pattern, replacement in fields:
        out, n = re.subn(pattern, lambda m, r=replacement: r, out, count=1)
        if n != 1:
            raise SystemExit('localisation field not replaced: %s' % pattern[:40])

    out = out.replace('"FNFAL_Handguard",', '"JAZZ_FNFAL_TacHandguard",')

    slot_indent = re.search(r"\n(\t+)\"JAZZ_BarrelNormal\",", out)
    if not slot_indent:
        raise SystemExit('barrel list not found')
    out = out.replace(BARREL_OLD, BARREL_NEW % {'i': slot_indent.group(1)}, 1)

    # tactical keeps a single fixed stock; the folding pair belongs to the classic
    out, n = re.subn(r'(\n\t+)"JAZZ_StockLightUnFolded",\n\t+"JAZZ_StockLightFolded",',
                     lambda m: m.group(1) + '"JAZZ_StockHeavy",', out, count=1)
    if n != 1:
        raise SystemExit('tactical stock slot not rewritten')
    return out


def mirror_visuals(text):
    """Duplicate every ApplyTo = "FNFAL" visual for the tactical id."""
    pattern = re.compile(
        r"([ \t]*)PlaceObj\('WeaponComponentVisual', \{\n"
        r"((?:[ \t]*\w+ = [^\n]*\n)*?)"
        r"[ \t]*ApplyTo = \"FNFAL\",\n"
        r"((?:[ \t]*\w+ = [^\n]*\n)*?)"
        r"([ \t]*)\}\),\n")
    count = 0

    def clone_of(whole):
        clone = whole.replace('ApplyTo = "FNFAL",', 'ApplyTo = "%s",' % NEW_ID)
        clone = clone.replace('Entity = "WeaponAttA_StockFNFal_02",',
                              'Entity = "JAZZ_FNFAL_TacStock",')
        clone = clone.replace('Entity = "WeaponAttA_HandguardFNFal_01",',
                              'Entity = "JAZZ_FNFAL_TacHandguard",')
        return clone

    # Idempotent: emit the clone only when it is not already the next sibling,
    # and collapse any run of identical clones left by an earlier partial run.
    out = []
    pos = 0
    for m in pattern.finditer(text):
        whole = m.group(0)
        if NEW_ID in whole:
            continue
        clone = clone_of(whole)
        out.append(text[pos:m.end()])
        tail = text[m.end():]
        repeats = 0
        while tail.startswith(clone):
            tail = tail[len(clone):]
            repeats += 1
        out.append(clone)
        if repeats != 1:
            count += 1
        pos = m.end() + len(clone) * repeats
    out.append(text[pos:])
    return ''.join(out), count


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--apply', action='store_true')
    a = p.parse_args()

    items = ROOT / 'items.lua'
    text = items.read_text(encoding='utf-8')
    if '\'Id\', "%s",' % NEW_ID in text:
        print('tactical item already present; only mirroring visuals')
        new_block = None
    else:
        start, end, indent = find_block(text, 'FNFAL')
        new_block = build_tactical(text[start:end], indent)
        text = text[:end] + new_block + text[end:]
        print('inserted %s (%d chars) after the FNFAL block' % (NEW_ID, len(new_block)))

    if 'id = "JAZZ_FNFAL_TacHandguard",' not in text:
        # FNFAL_Handguard is vanilla-only, so hang the new component off the last
        # ModItemWeaponComponent the mod already defines and copy its indentation.
        marker = "PlaceObj('ModItemWeaponComponent', {"
        anchor = text.rfind(marker)
        if anchor < 0:
            raise SystemExit('no ModItemWeaponComponent in items.lua')
        line_start = text.rfind('\n', 0, anchor) + 1
        indent = text[line_start:anchor]
        close_marker = '\n%s}),\n' % indent
        close = text.find(close_marker, anchor)
        if close < 0:
            raise SystemExit('cannot find end of the last ModItemWeaponComponent')
        close += len(close_marker)
        block = HANDGUARD_COMPONENT.format(hg=LOC['handguard'], wid=NEW_ID)
        block = re.sub(r'^\t{5}', indent, block, flags=re.M)
        block = re.sub(r'^\t{6}', indent + '\t', block, flags=re.M)
        text = text[:close] + block + text[close:]
        print('inserted JAZZ_FNFAL_TacHandguard component at indent %d' % len(indent))
    else:
        print('handguard component already present')

    text, mirrored = mirror_visuals(text)
    print('mirrored/normalised %d WeaponComponentVisual entries onto %s' % (mirrored, NEW_ID))

    # repair: a raw string replacement in an earlier revision of this script
    # leaked escaped quotes into the tactical stock slot
    broken = '\\"JAZZ_StockHeavy\\",'
    if broken in text:
        text = text.replace(broken, '"JAZZ_StockHeavy",')
        print('repaired escaped-quote artifact in the tactical stock slot')

    if a.apply:
        items.write_text(text, encoding='utf-8')
        print('APPLIED')
    else:
        print('DRY RUN - nothing written')


if __name__ == '__main__':
    sys.exit(main())
