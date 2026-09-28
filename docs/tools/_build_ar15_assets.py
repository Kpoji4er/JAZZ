"""Build M16A4 and M4A1 modules from the preserved tigg AR15 source (JAZZ-WEAPON-AR15-FAMILY-001).

Run with Blender:
  blender --background --factory-startup --python docs/tools/_build_ar15_assets.py -- \
      --source <tigg_ar15variants_2015.blend> --output <build-dir> --game-root <JA3_ROOT> [--export]

Nothing is written into the mod packages; the source .blend is never modified.

Module cutting uses whole connected islands only (loose parts), never a cutting plane:
JAZZ-WEAPON-AK-FAMILY-001-AC-001 was rejected by the owner because a plane crossed the
magazine feed lips and the pistol grip.

Scale is real overall length (k = 1.0). Visible barrel modules are the barrel tube
and front-sight islands; the A2 flash hider is a separate DefMuzzle so a compensator
does not stack on it. The delta ring stays on the host and is the Barrel attach
(the nut), shared by every length. Alternate lengths are harvested from sibling
tigg objects that share the same local frame.
"""
import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from _ja3_mesh_prepare import prepare_export_mesh

p = argparse.ArgumentParser()
p.add_argument('--source', required=True)
p.add_argument('--output', required=True)
p.add_argument('--game-root', required=True)
p.add_argument('--export', action='store_true')
p.add_argument('--weapon', action='append', choices=['M16A4', 'M4A1'])
args = p.parse_args(sys.argv[sys.argv.index('--') + 1:])

out = Path(args.output).resolve()
clean_dir, rigged_dir, tex_dir = out / 'clean', out / 'rigged', out / 'Textures'
for folder in (out, clean_dir, rigged_dir, tex_dir):
    folder.mkdir(parents=True, exist_ok=True)

GAME = Path(args.game_root)
spec = importlib.util.spec_from_file_location('ar15_hge', GAME / 'ModTools/BlenderExport.py')
hge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hge)
hge.SETTINGS.update(version='71', game='Zulu', appid='Jagged Alliance 3',
                    mtl_prop_0_visible=True, mtl_prop_0_name='Unit', enable_colliders=True)
hge.register()

SRC_CM = 10.0          # one source unit is ~10 cm
# Ruler = the weapons actually installed in the game, which sit at real length: G3A3 k=0.98,
# MP5A2 0.96, CAR-15 1.04. The shipped M16/M4 meshes were the outliers at 1.12-1.18, and an
# earlier pass wrongly anchored on the staged AKR_* graph (0.87), which made the carbine look
# tiny in hand. Target is therefore the real overall length, stock extended.
RULER = 1.0
TARGET_M = {'M16A4': 1.006, 'M4A1': 0.84}
HOST = {'M16A4': 'm16', 'M4A1': 'm4'}
# Texture families in the source, mapped to JA3 material maps.
TEXTURES = {
    'mat_m16': ('m16_col.png', 'm16_norm.png', 'm16_spec.png'),
    'mat_m4': ('m4_col.png', 'm4_norm.png', 'm4_spec.png'),
    'mat_m4rails': ('m4_rails_col.png', 'm4_rails_norm.png', 'm4_rails_spec.png'),
    'mat_carryhandle': ('carryhandle_col.png', 'carryhandle_norm.png', 'carryhandle_spec.png'),
    'mat_rearsight': ('rearsightCol.png', 'rearsightNor.png', 'rearsightSpec.png'),
}


def islands(ob):
    """Whole connected components of ob, as vertex-index sets with bounds in source units."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.verts.ensure_lookup_table()
    seen, parts = set(), []
    for v in bm.verts:
        if v.index in seen:
            continue
        stack, group = [v], []
        seen.add(v.index)
        while stack:
            cur = stack.pop()
            group.append(cur)
            for e in cur.link_edges:
                o = e.other_vert(cur)
                if o.index not in seen:
                    seen.add(o.index)
                    stack.append(o)
        faces = {f for gv in group for f in gv.link_faces}
        lo = Vector(tuple(min(gv.co[i] for gv in group) for i in range(3)))
        hi = Vector(tuple(max(gv.co[i] for gv in group) for i in range(3)))
        parts.append({'ids': {gv.index for gv in group}, 'lo': lo, 'hi': hi,
                      'tris': sum(max(0, len(f.verts) - 2) for f in faces)})
        bm.free() if False else None
    bm.free()
    return parts


def classify(parts, lo_all):
    """Assign each island to a module. Source frame: -X muzzle, +X butt, Z up, bore z~-0.6."""
    groups = {}
    for part in parts:
        lo, hi = part['lo'], part['hi']
        dx, dy, dz = (hi - lo)
        cx = (lo.x + hi.x) / 2
        if lo.z < -1.8 and cx < -0.4:
            key = 'Magazine'
        elif lo.z < -1.8:
            key = 'Grip'
        elif lo.x < lo_all.x + 0.6:
            key = 'Muzzle'
        elif hi.z > -0.1:
            key = 'FrontSight'
        elif dx > 1.2 and dy < 0.3 and dz < 0.3:
            key = 'Barrel'
        elif cx > 1.2 and dz > 0.8:
            key = 'Stock'
        elif cx > 0.4 and dy < 0.3 and dz < 0.4:
            key = 'BufferTube'
        elif hi.x < -1.5 and dz > 0.4 and part['tris'] > 200:
            key = 'Handguard'
        else:
            key = 'Body'
        groups.setdefault(key, []).append(part)
    return groups


def barrel_and_furniture(parts):
    """Split islands ahead of the receiver into barrel, handguard, ring, flash hider.

    Forward of the barrel nut the tigg hosts share the same 15-island layout:
    flash hider, barrel tube, front-sight bits, the large handguard, then the
    delta ring. The ring stays on the host so every barrel length meets the same nut.
    The birdcage leaves the barrel: empty Muzzle shows JAZZ_DefMuzzle, a compensator
    replaces it instead of stacking on the same device.
    """
    forward = [p for p in parts if p['lo'].x < -1.6]
    assert forward, 'no islands forward of the barrel nut'
    handguard = max(forward, key=lambda p: p['tris'])
    ring = None
    for part in forward:
        if part is handguard:
            continue
        if part['lo'].x > -1.85 and (part['hi'].x - part['lo'].x) < 0.5:
            ring = part
            break
    assert ring is not None, 'delta ring island not found'
    tip = min(forward, key=lambda p: p['lo'].x)
    flash = [tip] if (tip is not handguard and tip is not ring
                      and (tip['hi'].x - tip['lo'].x) < 0.6) else []
    skip = {id(handguard), id(ring)} | {id(p) for p in flash}
    barrel_ids = set().union(*(p['ids'] for p in forward if id(p) not in skip))
    flash_ids = set().union(*(p['ids'] for p in flash)) if flash else set()
    assert barrel_ids, 'barrel assembly is empty'
    assert flash_ids, 'flash hider island not found'
    return barrel_ids, handguard['ids'], ring['ids'], flash_ids


def extract_from_donor(donor, name, keep_ids, host_world):
    """Copy a donor mesh, snap it into the host local frame, keep whole islands."""
    copy = bpy.data.objects.new(name, donor.data.copy())
    bpy.context.collection.objects.link(copy)
    copy.matrix_world = host_world.copy()
    keep_only(copy, keep_ids, name)
    return copy


def keep_only(obj, keep_ids, name):
    """Delete every face of obj whose vertices are outside keep_ids (bmesh, no operators)."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    drop = []
    for f in bm.faces:
        membership = [v.index in keep_ids for v in f.verts]
        assert all(membership) or not any(membership), f'{name}: island cut crosses a polygon'
        if not any(membership):
            drop.append(f)
    assert len(drop) < len(bm.faces), f'{name}: nothing kept'
    bmesh.ops.delete(bm, geom=drop, context='FACES')
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()


def partition(ob, assignments, body_name):
    """Split ob into one object per module plus the remaining body.

    Every module is a set of whole islands. Each output starts from a pristine copy of the
    original mesh, so vertex indices stay valid for all modules.
    """
    original = ob.data
    taken = set().union(*assignments.values()) if assignments else set()
    everything = {v.index for v in original.vertices}
    outputs = {}
    for name, ids in list(assignments.items()) + [(body_name, everything - taken)]:
        copy = bpy.data.objects.new(name, original.copy())
        bpy.context.collection.objects.link(copy)
        copy.matrix_world = ob.matrix_world.copy()
        keep_only(copy, ids, name)
        outputs[name] = copy
    bpy.data.objects.remove(ob, do_unlink=True)
    return outputs


def load_tga(name, path, non_color):
    im = bpy.data.images.load(str(path), check_existing=False)
    im.colorspace_settings.name = 'Non-Color' if non_color else 'sRGB'
    if max(im.size) > 2048:
        im.scale(2048, 2048)
    w, h = im.size
    pixels = np.empty(w * h * 4, np.float32)
    im.pixels.foreach_get(pixels)
    copy = bpy.data.images.new(name, width=w, height=h, alpha=True)
    copy.colorspace_settings.name = im.colorspace_settings.name
    copy.pixels.foreach_set(pixels)
    copy.file_format = 'TARGA_RAW'
    copy.filepath_raw = str(tex_dir / (name + '.tga'))
    copy.save()
    bpy.data.images.remove(im)
    return copy, pixels.reshape(-1, 4), (w, h)


def build_material(mat_name, source_textures, prefix):
    """One JA3 material per source texture family: Base, Normal, RM (roughness = 1 - spec)."""
    col, norm, spec_map = source_textures
    base, _, _ = load_tga(f'{prefix}_Base', src_tex / col, False)
    normal, _, _ = load_tga(f'{prefix}_Norm', src_tex / norm, True)
    _, spec_px, (w, h) = load_tga(f'{prefix}_SpecSrc', src_tex / spec_map, True)
    luma = spec_px[:, 0] * 0.299 + spec_px[:, 1] * 0.587 + spec_px[:, 2] * 0.114
    rm = np.ones((w * h, 4), np.float32)
    rm[:, 0] = np.clip(1.0 - luma, 0.05, 1.0)   # roughness from inverted specular
    rm[:, 1] = 0.0
    # Careful metalness: ID-mask cool colors (barrel, receiver, rails) get a low
    # metallic; furniture/plastic stays near zero. Spec luma is the fallback.
    metal = np.clip(luma * 0.28, 0.0, 0.40)
    mask_rel = {
        'mat_m16': 'bakes/m16_mask.png',
        'mat_m4': 'bakes/m4_mask.png',
    }.get(mat_name)
    mask_path = src_tex / mask_rel if mask_rel else None
    if mask_path and mask_path.is_file():
        mask_img, mask_px, (mw, mh) = load_tga(f'{prefix}_MaskSrc', mask_path, True)
        if (mw, mh) != (w, h):
            mask_img.scale(w, h)
            mask_px = np.empty(w * h * 4, np.float32)
            mask_img.pixels.foreach_get(mask_px)
            mask_px = mask_px.reshape(w * h, 4)
        red, grn, blu = mask_px[:, 0], mask_px[:, 1], mask_px[:, 2]
        cool = np.clip((grn + blu) * 0.5 - red, 0.0, 1.0)
        purple = np.clip(blu - (red + grn) * 0.5, 0.0, 1.0)
        metal = np.clip(np.maximum(cool, purple * 0.45) * 0.50, 0.0, 0.45)
    rm[:, 2] = metal
    rm_img = bpy.data.images.new(f'{prefix}_RM', width=w, height=h, alpha=True)
    rm_img.colorspace_settings.name = 'Non-Color'
    rm_img.pixels.foreach_set(rm.ravel())
    rm_img.file_format = 'TARGA_RAW'
    rm_img.filepath_raw = str(tex_dir / f'{prefix}_RM.tga')
    rm_img.save()

    mat = bpy.data.materials.new(prefix)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes['Principled BSDF']
    tex_base = nt.nodes.new('ShaderNodeTexImage')
    tex_base.image = base
    nt.links.new(bsdf.inputs['Base Color'], tex_base.outputs['Color'])
    tex_rm = nt.nodes.new('ShaderNodeTexImage')
    tex_rm.image = rm_img
    sep = nt.nodes.new('ShaderNodeSeparateColor')
    nt.links.new(sep.inputs['Color'], tex_rm.outputs['Color'])
    nt.links.new(bsdf.inputs['Roughness'], sep.outputs['Red'])
    nt.links.new(bsdf.inputs['Metallic'], sep.outputs['Blue'])
    tex_n = nt.nodes.new('ShaderNodeTexImage')
    tex_n.image = normal
    nmap = nt.nodes.new('ShaderNodeNormalMap')
    nt.links.new(nmap.inputs['Color'], tex_n.outputs['Color'])
    nt.links.new(bsdf.inputs['Normal'], nmap.outputs['Normal'])

    hge.add_material_props(mat)
    paths = {'base_color': base.filepath_raw, 'normal_map': normal.filepath_raw,
             'roughness_metallic_map': rm_img.filepath_raw}
    for prop in hge.MATERIAL_PROPERTIES:
        if not prop.settings_name:
            continue
        if prop.settings_name in paths:
            mat[prop.id] = paths[prop.settings_name]
        elif prop.map:
            mat[prop.id] = ''
        else:
            mat[prop.id] = getattr(mat.hgm_settings, prop.settings_name)
    return mat


bpy.ops.wm.open_mainfile(filepath=str(Path(args.source).resolve()))
src_tex = Path(args.source).resolve().parent / 'textures'
report = {'ruler': RULER, 'weapons': {}}

# Rotate the source into the JA3 weapon frame: -Y forward, Z up, and metres.
ROT = Matrix.Rotation(math.pi / 2, 4, 'Z')

for weapon in args.weapon or ['M16A4', 'M4A1']:
    bpy.ops.wm.open_mainfile(filepath=str(Path(args.source).resolve()))
    host = bpy.data.objects[HOST[weapon]]
    prefix = 'M16R_M16A4' if weapon == 'M16A4' else 'M4R_M4A1'

    host_world = host.matrix_world.copy()
    parts = islands(host)
    lo_all = Vector(tuple(min(p['lo'][i] for p in parts) for i in range(3)))
    hi_all = Vector(tuple(max(p['hi'][i] for p in parts) for i in range(3)))
    groups = classify(parts, lo_all)
    source_len_cm = (hi_all.x - lo_all.x) * SRC_CM
    scale = TARGET_M[weapon] / (hi_all.x - lo_all.x)

    barrel_ids, hg_ids, ring_ids, flash_ids = barrel_and_furniture(parts)
    ring_hi_x = next(p['hi'].x for p in parts if p['ids'] == ring_ids)
    assert 'Magazine' in groups, f'{weapon}: no Magazine island found'
    assert 'Grip' in groups, f'{weapon}: no Grip island found'
    assignments = {
        f'{prefix}_Magazine': set().union(*[p['ids'] for p in groups['Magazine']]),
        f'{prefix}_Handguard': hg_ids,
        f'{prefix}_Barrel': barrel_ids,
        f'{prefix}_Handgrip': set().union(*[p['ids'] for p in groups['Grip']]),
        f'{prefix}_DefMuzzle': flash_ids,
    }
    if 'Stock' in groups:
        assignments[f'{prefix}_Stock'] = set().union(*[p['ids'] for p in groups['Stock']])
    else:
        assert weapon != 'M16A4', 'M16A4: no Stock island found'
    produced = partition(host, assignments, prefix)
    detached = {name.split('_')[-1]: produced[name] for name in assignments}
    host = produced[prefix]
    keep = set(produced)

    # Shared attachments, duplicated per weapon so each matches its host scale.
    extras = {}
    host_centre = host_world.translation
    for src_stem, suffix in (('carryhandle', 'CarryHandle'), ('RearSight', 'RearSight')):
        # Pick the copy that sits on this variant in the source layout, so its position
        # relative to the receiver is already correct.
        candidates = [o for o in bpy.data.objects
                      if o.type == 'MESH' and o.name.split('.')[0] == src_stem
                      and 'lod' not in o.name.lower()]
        src = min(candidates, key=lambda o: (o.matrix_world.translation - host_centre).length)
        copy = src.copy()
        copy.data = src.data.copy()
        copy.name = f'{prefix}_{suffix}'
        bpy.context.collection.objects.link(copy)
        extras[suffix] = copy
        keep.add(copy.name)

    # Carbine-length RAS. No rifle-length rail exists in the source; on M16A4 it only
    # looks right with the short (14.5") barrel harvested from m4.
    rail = bpy.data.objects['m4_rails']
    ris_parts = [p for p in islands(rail) if p['lo'].x >= -3.35 and p['hi'].x <= -1.60]
    assert len(ris_parts) >= 4, f'RIS: expected the rail strips, found {len(ris_parts)} islands'
    extras['HandguardRIS'] = extract_from_donor(
        rail, f'{prefix}_HandguardRIS',
        set().union(*[p['ids'] for p in ris_parts]), host_world)
    keep.add(extras['HandguardRIS'].name)

    # Alternate barrels live on sibling hosts that share the same local modeling frame.
    donors = {'BarrelShort': 'm4'} if weapon == 'M16A4' else {'BarrelShort': 'mk18',
                                                              'BarrelLong': 'm16'}
    for suffix, donor_name in donors.items():
        donor = bpy.data.objects[donor_name]
        donor_barrel, _, _, _ = barrel_and_furniture(islands(donor))
        extras[suffix] = extract_from_donor(donor, f'{prefix}_{suffix}', donor_barrel, host_world)
        keep.add(extras[suffix].name)
    if weapon == 'M16A4':
        # Rifle-length furniture requires the rifle-position front sight. A
        # carbine gas block lands inside either A4 handguard. Keep the entire
        # sight assembly and shorten only the exposed tube by 10 cm (~16").
        short = extras['BarrelShort']
        short.data = detached['Barrel'].data.copy()
        front = min(v.co.x for v in short.data.vertices)
        for v in short.data.vertices:
            if v.co.x < front + 0.001:
                v.co.x += 0.10 / scale
    if weapon == 'M4A1':
        # The 20" tube is not modelled under the carbine handguard, so the long barrel
        # carries the rifle handguard as a second visual.
        donor = bpy.data.objects['m16']
        _, rifle_hg, _, _ = barrel_and_furniture(islands(donor))
        extras['HandguardRifle'] = extract_from_donor(
            donor, f'{prefix}_HandguardRifle', rifle_hg, host_world)
        keep.add(extras['HandguardRifle'].name)
    if weapon == 'M16A4':
        donor = bpy.data.objects['m4']
        donor_parts = islands(donor)
        donor_groups = classify(donor_parts, Vector(tuple(
            min(p['lo'][i] for p in donor_parts) for i in range(3))))
        assert 'Stock' in donor_groups, 'M16A4: m4 donor has no Stock island'
        extras['StockLight'] = extract_from_donor(
            donor, f'{prefix}_StockLight',
            set().union(*[p['ids'] for p in donor_groups['Stock']]), host_world)
        keep.add(extras['StockLight'].name)

    for o in list(bpy.data.objects):
        if o.name not in keep:
            bpy.data.objects.remove(o, do_unlink=True)

    objects = [o for o in bpy.data.objects if o.type == 'MESH']
    transform = Matrix.Scale(scale, 4) @ ROT
    host_inv = host_world.inverted()
    dropped_groups = set()
    for o in objects:
        bpy.ops.object.select_all(action='DESELECT')
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        # Strip the source layout offset: keep every part where it sits relative to the host
        # receiver, not where its variant stands in the showcase row.
        world = host_inv @ o.matrix_world
        o.parent = None
        o.data.transform(transform @ world)
        o.matrix_world = Matrix.Identity(4)
        o.hide_set(False)
        o.hide_render = False
        # These are static props. Leftover source vertex groups make the official exporter
        # treat the mesh as skinned and demand an animated state.
        if o.vertex_groups:
            dropped_groups.update(g.name for g in o.vertex_groups)
            o.vertex_groups.clear()
        prepare_export_mesh(o)

    # The source .blend lays the variants out side by side, so each carries a layout offset.
    # Re-anchor to the frame of the entity being replaced: keep the old ratio of origin to
    # overall length and the old bore height, both scaled to the new length. This keeps hand
    # grips, holster and muzzle FX in the same relative place as the shipped entity.
    import xml.etree.ElementTree as ET
    old_ent = ET.parse(Path(__file__).resolve().parents[2].parent / 'jazz_assets/Entities' / f'{weapon}.ent')
    box = old_ent.find('.//box')
    old_lo = [float(v) for v in box.get('min').split(',')]
    old_hi = [float(v) for v in box.get('max').split(',')]
    old_len_cm = old_hi[0] - old_lo[0]
    old_front_cm = old_hi[0]
    old_attach = {n.get('name'): n for n in old_ent.findall('.//attach')}
    old_spots_cm = {name: [float(v) for v in node.get('spot_pos').split(',')]
                    for name, node in old_attach.items()}
    old_rot = {name: node.get('spot_rot', '') for name, node in old_attach.items()}
    old_bore_cm = old_spots_cm['Muzzle'][2]

    reference = [o for o in objects if o.name in (
        prefix, f'{prefix}_Magazine', f'{prefix}_Handguard', f'{prefix}_Barrel',
        f'{prefix}_Stock', f'{prefix}_DefMuzzle', f'{prefix}_Handgrip')]
    r_lo = Vector(tuple(min(min(v.co[i] for v in o.data.vertices) for o in reference) for i in range(3)))
    r_hi = Vector(tuple(max(max(v.co[i] for v in o.data.vertices) for o in reference) for i in range(3)))
    new_len_m = r_hi.y - r_lo.y
    ratio = new_len_m / (old_len_cm / 100.0)
    # Bore height taken from the real muzzle face: the front-most centimetre of geometry.
    front = [v.co.z for o in reference for v in o.data.vertices if v.co.y < r_lo.y + 0.01]
    bore_now = sum(front) / len(front)
    delta = Vector((
        -(r_lo.x + r_hi.x) / 2,
        -(old_front_cm / 100.0) * ratio - r_lo.y,
        (old_bore_cm / 100.0) * ratio - bore_now,
    ))
    for o in objects:
        o.data.transform(Matrix.Translation(delta))
    bore_z = bore_now + delta.z

    def bounds(o):
        return [Vector(tuple(fn(v.co[i] for v in o.data.vertices) for i in range(3)))
                for fn in (min, max)]

    # Rifle-length RAS: the source only has a carbine rail. Stretch it along the bore
    # so M16A4's RIS covers the A2 handguard window instead of sitting as a stub.
    if weapon == 'M16A4':
        ris = extras['HandguardRIS']
        hlo, hhi = bounds(detached['Handguard'])
        glo, ghi = bounds(ris)
        factor = (hhi.y - hlo.y) / (ghi.y - glo.y)
        rear = max(v.co.y for v in ris.data.vertices)
        for v in ris.data.vertices:
            v.co.y = rear - (rear - v.co.y) * factor

    if weapon == 'M16A4':
        a2 = detached['Stock']
        light = extras['StockLight']
        alo, ahi = bounds(a2)
        llo, lhi = bounds(light)
        light.data.transform(Matrix.Translation(Vector((
            (alo.x + ahi.x - llo.x - lhi.x) / 2,
            alo.y - llo.y,
            (alo.z + ahi.z - llo.z - lhi.z) / 2,
        ))))

    # 20-round STANAG is not in the source; shorten the 30-round mag downward from the lip.
    mag20 = detached['Magazine'].copy()
    mag20.data = detached['Magazine'].data.copy()
    mag20.name = f'{prefix}_Magazine20'
    bpy.context.collection.objects.link(mag20)
    mlo, mhi = bounds(mag20)
    for v in mag20.data.vertices:
        v.co.z = mhi.z - (mhi.z - v.co.z) * 0.72
    extras['Magazine20'] = mag20
    objects.append(mag20)

    # Measure while every module still shares one frame; the per-entity origin pass below
    # re-centres each mesh on its own pivot and makes cross-object bounds meaningless.
    default_set = [o for o in objects if o.name in (
        prefix, f'{prefix}_Magazine', f'{prefix}_Handguard', f'{prefix}_Barrel',
        f'{prefix}_Stock', f'{prefix}_Handgrip', f'{prefix}_DefMuzzle')]
    assembled_lo = min(min(v.co.y for v in o.data.vertices) for o in default_set)
    assembled_hi = max(max(v.co.y for v in o.data.vertices) for o in default_set)
    assembled_len_cm = round((assembled_hi - assembled_lo) * 100, 1)

    # Visual verification of the island cuts and of the module fit (AK lesson: the owner
    # rejected a plane cut; renders are how we show the cut is clean before integration).
    previews = {}
    scene = bpy.context.scene
    # Workbench in TEXTURE mode: fast, deterministic, and shows the actual albedo we export.
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.light = 'STUDIO'
    scene.display.shading.color_type = 'TEXTURE'
    scene.display.shading.show_cavity = True
    scene.display.render_aa = '8'
    scene.render.resolution_x, scene.render.resolution_y = 1500, 620
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = 'PNG'
    if scene.world is None:
        scene.world = bpy.data.worlds.new('World')
    scene.world.use_nodes = True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.18, .18, .2, 1)
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    cam_data = bpy.data.cameras.new('PreviewCam')
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = (assembled_hi - assembled_lo) * 1.12
    cam = bpy.data.objects.new('PreviewCam', cam_data)
    bpy.context.collection.objects.link(cam)
    centre = Vector((0, (assembled_lo + assembled_hi) / 2, bore_z - 0.02))
    cam.location = centre + Vector((-1.6, 0, 0))
    cam.rotation_euler = (centre - cam.location).to_track_quat('-Z', 'Y').to_euler()
    scene.camera = cam
    for idx, (loc, energy) in enumerate([((-1.2, -0.6, 1.2), 55), ((-0.8, 0.8, 0.6), 30),
                                         ((0.9, 0.2, 0.9), 18)]):
        data = bpy.data.lights.new(f'PreviewLight{idx}', 'AREA')
        data.energy, data.size = energy, 1.0
        light = bpy.data.objects.new(data.name, data)
        bpy.context.collection.objects.link(light)
        light.location = Vector(loc) + centre
        light.rotation_euler = (centre - light.location).to_track_quat('-Z', 'Y').to_euler()

    optional = {o.name: o for o in objects if o.name not in {o2.name for o2 in default_set}}
    for o in optional.values():
        o.hide_render = True

    def shoot(tag, extra_visible=(), hidden=()):
        for o in optional.values():
            o.hide_render = o.name not in extra_visible
        for name in hidden:
            bpy.data.objects[name].hide_render = True
        for name in extra_visible:
            bpy.data.objects[name].hide_render = False
        scene.render.filepath = str(out / f'{weapon}_{tag}.png')
        bpy.ops.render.render(write_still=True)
        for name in hidden:
            bpy.data.objects[name].hide_render = False
        previews[tag] = scene.render.filepath

    shoot('default')
    shoot('carryhandle', extra_visible=[f'{prefix}_CarryHandle'])
    shoot('buis', extra_visible=[f'{prefix}_RearSight'])
    shoot('ris', extra_visible=[f'{prefix}_HandguardRIS'], hidden=[f'{prefix}_Handguard'])
    shoot('short', extra_visible=[f'{prefix}_BarrelShort'], hidden=[f'{prefix}_Barrel'])
    shoot('short_ris', extra_visible=[f'{prefix}_BarrelShort', f'{prefix}_HandguardRIS'],
          hidden=[f'{prefix}_Barrel', f'{prefix}_Handguard'])
    if weapon == 'M4A1':
        shoot('long', extra_visible=[f'{prefix}_BarrelLong', f'{prefix}_HandguardRifle'],
              hidden=[f'{prefix}_Barrel', f'{prefix}_Handguard'])
    if weapon == 'M16A4':
        shoot('stock_light', extra_visible=[f'{prefix}_StockLight'], hidden=[f'{prefix}_Stock'])
        shoot('mag20', extra_visible=[f'{prefix}_Magazine20'] if f'{prefix}_Magazine20' in bpy.data.objects
              else [], hidden=[f'{prefix}_Magazine'])
    for o in optional.values():
        o.hide_render = False
    for o in list(bpy.data.objects):
        if o.type in {'CAMERA', 'LIGHT'}:
            bpy.data.objects.remove(o, do_unlink=True)

    # Materials, one per source texture family actually used.
    used = {}
    for o in objects:
        for slot in o.material_slots:
            if slot.material and slot.material.name in TEXTURES:
                used.setdefault(slot.material.name, []).append(o)
    made = {}
    for mat_name, owners in used.items():
        made[mat_name] = build_material(mat_name, TEXTURES[mat_name],
                                        f'{prefix}_{mat_name.replace("mat_", "")}')
        for o in owners:
            for slot in o.material_slots:
                if slot.material and slot.material.name == mat_name:
                    slot.material = made[mat_name]

    root = bpy.data.objects[prefix]
    rlo, rhi = bounds(root)
    mag = detached['Magazine']
    mlo, mhi = bounds(mag)
    MUZZLE_DROP = 0.004

    # Hand, trigger and attachment spots come from the entity being replaced, scaled by the
    # same ratio as the frame. Those positions are proven in game; deriving them from the new
    # geometry put the left hand near the magazine well on the rifle.
    # .ent (x, y, z) in cm maps to Blender (-y, -x, z) in metres.
    def from_old(name):
        x, y, z = old_spots_cm[name]
        return Vector((-y / 100.0 * ratio, -x / 100.0 * ratio, z / 100.0 * ratio))

    spots = {name: from_old(name) for name in old_spots_cm}
    spot_rotations = {}
    for name, rot in old_rot.items():
        if not rot:
            continue
        axis = [float(v) for v in rot.split(',')[:3]]
        angle = float(rot.split(',')[3])
        if abs(axis[0]) > 0.9 and abs(angle - 90.0) < 0.1:
            # A quarter turn about the bore, as the shipped Side spots use. The .ent +X axis is
            # Blender -Y, and the sign is chosen so the exported spot_rot matches the shipped
            # entity (1,0,0,90) rather than its mirror.
            spot_rotations[name] = (0.0, math.pi / 2 * (1 if axis[0] > 0 else -1), 0.0)

    # Geometry wins where a spot must coincide with real geometry or with a module pivot.
    # Barrel attach is the delta ring (nut), not the rear of the exposed 20" FSB.
    barrel = detached['Barrel']
    blo, bhi = bounds(barrel)
    # Ring rear in source X becomes Blender Y after ROT+scale+delta. Do not use
    # post-triangulate vertex indices: triangulate can rewrite the host mesh.
    nut = Vector((0.0, ring_hi_x * scale + delta.y, bore_z))
    spots['Barrel'] = nut
    # Threads of the default barrel. Devices sit 4 mm lower than the previous bore guess.
    spots['Muzzle'] = Vector((0.0, blo.y, bore_z - MUZZLE_DROP))
    spots['Magazine'] = Vector((0.0, (mlo.y + mhi.y) / 2, mhi.z - 0.004))
    hg = detached['Handguard']
    hlo, hhi = bounds(hg)
    spots['Handguard'] = (hlo + hhi) / 2
    grip = detached['Handgrip']
    glo, ghi = bounds(grip)
    spots['Handgrip'] = (glo + ghi) / 2
    if 'Stock' in detached:
        stock = detached['Stock']
        slo, shi = bounds(stock)
        spots['Stock'] = Vector((0.0, slo.y + 0.004, (slo.z + shi.z) / 2))
    # Sights a bit forward onto the rail; carry handle still sits on the receiver.
    spots['Scope'] = spots['Scope'] + Vector((0.0, -0.03, 0.0))

    entities = {prefix: root}
    entities.update({o.name: o for o in detached.values()})
    entities.update({o.name: o for o in extras.values()})

    for name, o in entities.items():
        suffix = name[len(prefix) + 1:] if name != prefix else ''
        pivot = spots.get(suffix, Vector()) if suffix in spots else Vector()
        if suffix in ('CarryHandle', 'RearSight'):
            pivot = spots['Scope']
        if suffix in ('HandguardRIS', 'HandguardRifle'):
            pivot = spots.get('Handguard', Vector())
        if suffix.startswith('Barrel'):
            pivot = nut
        if suffix == 'DefMuzzle':
            dlo, dhi = bounds(o)
            pivot = Vector((0.0, dhi.y, bore_z - MUZZLE_DROP))
        if suffix == 'Magazine20':
            pivot = spots['Magazine']
        if suffix == 'StockLight':
            pivot = spots['Stock']
        origin = bpy.data.objects.new(name + '_Origin', None)
        bpy.context.collection.objects.link(origin)
        origin.location = pivot
        o.data.transform(Matrix.Translation(-pivot))
        o.parent = origin
        o.location = Vector()
        st = o.hge_obj_settings
        st.entity = name
        st.mesh = 'Mesh'
        st.state = 'idle'
        st.lod = 1
        st.ignore = False
        o.hge_export = True

    if weapon == 'M4A1':
        stock = entities[f'{prefix}_Stock']
        folded = stock.copy()
        folded.data = stock.data.copy()
        folded.name = f'{prefix}_StockFolded'
        bpy.context.collection.objects.link(folded)
        folded.parent = stock.parent
        folded.data.transform(Matrix.Translation(Vector((0, -0.055, 0))))
        folded.hge_obj_settings.entity = folded.name
        folded.hide_render = True
        entities[folded.name] = folded

    for name, point in spots.items():
        e = bpy.data.objects.new(name, None)
        bpy.context.collection.objects.link(e)
        e.parent = root
        e.location = point
        e.rotation_euler = spot_rotations.get(name, (0.0, 0.0, 0.0))
        e.hge_obj_settings.spot_name = name
    # Barrel Muzzle is the thread face. DefMuzzle / compensator attach here and
    # follow the installed length; they no longer sit on a baked birdcage.
    for name, o in entities.items():
        suffix = name[len(prefix) + 1:] if name != prefix else ''
        if not suffix.startswith('Barrel'):
            continue
        front_y = min(v.co.y for v in o.data.vertices)
        tip = Vector((0.0, front_y, -MUZZLE_DROP))
        e = bpy.data.objects.new(f'{name}_Muzzle', None)
        bpy.context.collection.objects.link(e)
        e.parent = o
        e.location = tip
        e.hge_obj_settings.spot_name = 'Muzzle'

    scene = bpy.context.scene
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1
    bpy.ops.wm.save_as_mainfile(filepath=str(clean_dir / f'{weapon}.blend'))
    bpy.ops.wm.save_as_mainfile(filepath=str(rigged_dir / f'{weapon}_JA3.blend'))

    info = {'source_object': HOST[weapon], 'source_len_cm': round(source_len_cm, 1),
            'scale': round(scale, 6), 'target_m': TARGET_M[weapon],
            'assembled_len_cm': assembled_len_cm, 'previews': previews,
            'body_len_cm': round((rhi.y - rlo.y) * 100, 1),
            'default_barrel_len_cm': round((bhi.y - blo.y) * 100, 1),
            'bore_height_cm': round(bore_z * 100, 2),
            'dropped_vertex_groups': sorted(dropped_groups),
            'islands': {k: len(v) for k, v in sorted(groups.items())},
            'entities': {}, 'spots_m': {k: [round(c, 4) for c in v] for k, v in spots.items()}}
    for name, o in entities.items():
        o.data.calc_loop_triangles()
        lo, hi = bounds(o)
        info['entities'][name] = {
            'triangles': len(o.data.loop_triangles), 'vertices': len(o.data.vertices),
            'size_cm': [round((hi[i] - lo[i]) * 100, 1) for i in range(3)],
            'material': o.data.materials[0].name if o.data.materials else None,
            'valid': o.hge_obj_settings.is_valid(),
            'errors': o.hge_obj_settings.get_errors(),
        }
    report['weapons'][weapon] = info

    if args.export:
        for o in list(bpy.data.objects):
            if o.type in {'CAMERA', 'LIGHT'}:
                bpy.data.objects.remove(o, do_unlink=True)
        with hge.ObjectNamesExportContext(bpy.context):
            bpy.ops.export_scene.fbx(filepath=str(rigged_dir / f'{weapon}_JA3.fbx'),
                                     axis_forward='Y', axis_up='Z',
                                     apply_scale_options='FBX_SCALE_ALL',
                                     object_types={'MESH', 'EMPTY'}, use_custom_props=True,
                                     add_leaf_bones=False, bake_anim=False)

(out / 'build-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print('AR15_BUILD=' + json.dumps(report))
