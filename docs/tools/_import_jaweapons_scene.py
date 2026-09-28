"""Blender worker for _import_jaweapons_batch.py; source units are preserved."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

import bpy
import bmesh

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh, mesh_has_custom_normals
from _inspect_weapon_source import world_bbox, setup_render, render_views

IMAGE_SUFFIXES = {'.png', '.jpg', '.jpeg', '.dds', '.tga', '.tif', '.tiff'}
BASE = re.compile(r'(?i)(?:base_?colou?r|albedo(?:transparency)?|diffuse(?:texture)?|diff|_co|_d)(?:[_. -]|$)')


def socket_image(mat):
    if not mat or not mat.use_nodes:
        return None
    for node in mat.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            links = node.inputs['Base Color'].links
            if links and links[0].from_node.type == 'TEX_IMAGE':
                return links[0].from_node.image
    return None


def native_material_valid(mat):
    if not mat or not mat.use_nodes:
        return False
    nodes = mat.node_tree.nodes
    shaders = [n for n in nodes if n.type == 'BSDF_PRINCIPLED']
    pictures = [n.image for n in nodes if n.type == 'TEX_IMAGE' and n.image]
    return bool(shaders and pictures) and all(
        im.packed_file or im.has_data or Path(bpy.path.abspath(im.filepath)).is_file()
        for im in pictures)


def material_for(base, images):
    mat = bpy.data.materials.new(base.stem)
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    shader = nodes.get('Principled BSDF')
    match = BASE.search(base.stem)
    prefix = base.stem[:match.start()] if match else base.stem
    candidates = [p for p in images if p != base and p.stem.lower().startswith(prefix.lower())]
    def image_node(path, color=False):
        node = nodes.new('ShaderNodeTexImage')
        node.image = bpy.data.images.load(str(path), check_existing=True)
        node.image.colorspace_settings.name = 'sRGB' if color else 'Non-Color'
        return node
    tex = image_node(base, True)
    links.new(tex.outputs['Color'], shader.inputs['Base Color'])
    mat['base_source'] = base.name
    for pattern, socket in [('rough', 'Roughness'), ('metal', 'Metallic')]:
        found = [p for p in candidates if pattern in p.stem.lower()]
        if len(found) == 1:
            links.new(image_node(found[0]).outputs['Color'], shader.inputs[socket])
    normals = [p for p in candidates if re.search(r'(?i)(normal|normals|_nrm|_nohq|_nm)', p.stem)]
    # DirectX maps need a green-channel conversion during export; preserve as unbound here.
    normals = [p for p in normals if 'directx' not in p.stem.lower()]
    if len(normals) == 1:
        normal = nodes.new('ShaderNodeNormalMap')
        links.new(image_node(normals[0]).outputs['Color'], normal.inputs['Color'])
        links.new(normal.outputs['Normal'], shader.inputs['Normal'])
    nodes.active = tex
    return mat


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--uv-review', action='store_true')
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    build = args.build; source = build / 'source'
    if args.uv_review:
        bpy.ops.wm.open_mainfile(filepath=str(build / 'clean/Source.blend'), use_scripts=False)
        meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
        for obj in meshes:
            obj.color = (0.9, 0.02, 0.02, 1) if not obj.data.uv_layers else (0.5, 0.5, 0.5, 1)
        setup_render(900, 'SINGLE')
        bpy.context.scene.display.shading.color_type = 'OBJECT'
        lo, hi = world_bbox(meshes)
        review = build / 'review_uv'; review.mkdir(exist_ok=True)
        render_views(review, 'MissingUV_red', lo, hi)
        no_uv = [o for o in meshes if not o.data.uv_layers]
        for obj in meshes:
            obj.hide_render = obj not in no_uv
        if no_uv:
            lo, hi = world_bbox(no_uv)
            render_views(review, 'OnlyMissingUV', lo, hi)
        return
    files = sorted(p for p in source.rglob('*') if p.is_file())
    blends = [p for p in files if p.suffix.lower() == '.blend']
    objs = [p for p in files if p.suffix.lower() == '.obj']
    glbs = [p for p in files if p.suffix.lower() == '.glb']
    fbxs = [p for p in files if p.suffix.lower() == '.fbx']
    bpy.ops.wm.read_factory_settings(use_empty=True)
    selected = []
    if blends:
        selected = [blends[0]]
        bpy.ops.wm.open_mainfile(filepath=str(blends[0]), use_scripts=False)
    elif glbs:
        selected = glbs
        for p in selected:
            bpy.ops.import_scene.gltf(filepath=str(p))
    elif objs:
        selected = objs
        for p in selected:
            previous = set(bpy.data.objects)
            bpy.ops.wm.obj_import(filepath=str(p))
            for obj in set(bpy.data.objects) - previous:
                obj['source_file'] = p.relative_to(source).as_posix()
    elif fbxs:
        selected = [fbxs[0]]
        bpy.ops.import_scene.fbx(filepath=str(fbxs[0]))
    else:
        raise RuntimeError('No supported source representation')
    images = [p for p in files if p.suffix.lower() in IMAGE_SUFFIXES and 'internal_ground' not in p.name.lower()]
    # Repair paths only by an exact unique basename, never guess similarly named maps.
    for im in list(bpy.data.images):
        if im.packed_file or im.source != 'FILE':
            continue
        basename = Path(im.filepath.replace('\\', '/')).name.lower()
        matches = [p for p in images if p.name.lower() == basename]
        if len(matches) == 1:
            im.filepath = str(matches[0]); im.reload()
    bases = [p for p in images if BASE.search(p.stem)]
    if build.name.startswith('09_'):
        # Native source provides standard and camouflage atlases in duplicate DDS/TGA.
        # Select the standard diffuse atlas, retaining all alternatives in source/.
        bases = [p for p in images if p.name.lower() == 'kiparis.dds']
    # Exported PBR filenames sometimes contain a sole atlas without a channel suffix.
    if not bases and len(images) == 1:
        bases = images
    # Prefer PNG to redundant JPEG copies, preserving distinct atlases.
    unique = {}
    for p in bases:
        key = p.stem.lower()
        if key not in unique or p.suffix.lower() == '.png':
            unique[key] = p
    library = [material_for(p, images) for p in unique.values()]
    explicit = {}
    if build.name.startswith('01_'):
        explicit = {'model_0': 'walther_ppk_metal_BaseColor',
                    'model_1': 'walther_ppk_grip_and_mag_BaseColor'}
    elif build.name.startswith('11_'):
        explicit = {'model_0': 'KEDR-B_defaultMat.004_BaseColor',
                    'model_1': 'suppressor_texture_Material.003_BaseColor'}
    for mat in library:
        mat.use_fake_user = True
    missing = bpy.data.materials.new('UNRESOLVED_MATERIAL_NOT_FOR_EXPORT')
    missing.diffuse_color = (1, 0, 1, 1)
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    if not meshes:
        raise RuntimeError('No mesh objects')
    rows = []
    for obj in meshes:
        obj.hide_set(False); obj.hide_viewport = False; obj.hide_render = False
        has_uv = bool(obj.data.uv_layers)
        native = bool(obj.data.materials) and all(native_material_valid(mat) for mat in obj.data.materials)
        assignment = 'native' if native else 'unresolved'
        if obj.name in explicit and has_uv:
            mat = next(m for m in library if m.name == explicit[obj.name])
            obj.data.materials.clear(); obj.data.materials.append(mat); assignment = 'explicit-source-atlas'
        elif not native and has_uv and len(library) == 1:
            obj.data.materials.clear(); obj.data.materials.append(library[0]); assignment = 'single-atlas'
        elif not native:
            obj.data.materials.clear(); obj.data.materials.append(missing)
        issues = prepare_export_mesh(obj, strict=False)
        # Delete only triangles that fail the existing zero-area/zero-normal gate.
        # Never weld vertices, drop spikes, or repair missing UV automatically.
        removed = 0
        bad = {x['triangle'] for x in issues if x['kind'] in {'degenerate', 'zero_normal'}
               and x['triangle'] is not None}
        if bad:
            obj.data.calc_loop_triangles()
            polygons = {obj.data.loop_triangles[i].polygon_index for i in bad}
            bm = bmesh.new(); bm.from_mesh(obj.data); bm.faces.ensure_lookup_table()
            faces = [bm.faces[i] for i in polygons]; removed = len(faces)
            bmesh.ops.delete(bm, geom=faces, context='FACES')
            bm.to_mesh(obj.data); bm.free(); obj.data.update()
            issues = prepare_export_mesh(obj, strict=False)
        rows.append({'object': obj.name, 'source_file': obj.get('source_file'),
                     'vertices': len(obj.data.vertices), 'triangles': len(obj.data.polygons),
                     'uv': has_uv, 'assignment': assignment,
                     'materials': [m.name if m else None for m in obj.data.materials],
                     'custom_normals': mesh_has_custom_normals(obj.data),
                     'removed_zero_area_or_normal_faces': removed,
                     'issues': dict(Counter(x['kind'] for x in issues)), 'issue_samples': issues[:8]})
    clean = build / 'clean'; clean.mkdir(exist_ok=True)
    scene_path = clean / 'Source.blend'
    library_names = [m.name for m in library]
    bpy.ops.wm.save_as_mainfile(filepath=str(scene_path))
    # Re-open proves the saved file is loadable and clears transient import state.
    bpy.ops.wm.open_mainfile(filepath=str(scene_path), use_scripts=False)
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    lo, hi = world_bbox(meshes)
    review = build / 'review'; review.mkdir(exist_ok=True)
    setup_render(700, 'TEXTURE')
    previews = render_views(review, 'Source', lo, hi)
    unresolved = [r['object'] for r in rows if r['assignment'] == 'unresolved']
    no_uv = [r['object'] for r in rows if not r['uv']]
    defects = sum(sum(r['issues'].values()) for r in rows)
    status = 'IMPORTED_REVIEW' if unresolved or no_uv or defects else 'IMPORTED_SOURCE'
    report = {'status': status, 'scene': str(scene_path), 'reopened': True,
              'selected_sources': [p.relative_to(source).as_posix() for p in selected],
              'source_units_preserved': True, 'bbox_size_source_units': list(hi - lo),
              'material_library': library_names, 'objects': rows,
              'unresolved_materials': unresolved, 'no_uv': no_uv, 'geometry_issues': defects,
              'previews': [str(review / p) for p in previews], 'game_installed': False}
    (build / 'import-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('SOURCE_IMPORT', status, 'objects', len(rows), 'issues', defects)


if __name__ == '__main__':
    main()
