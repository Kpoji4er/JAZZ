"""Build the 6B3TM-01 vest as clean, unrigged geometry fitted to the real Legion shirt.

Blender --background --python this.py -- --sample <BlenderScene_Appearance.blend>
  --shirt <NPCCostumeMale_Shirt_08_mesh.json> --output <new folder> [--quick]

Stage `clean` only: separate part objects, UVs, materials, no armature, no vertex
groups, no deform modifiers. The rig is built in a later stage from this file.

Layout follows the owner's front/back/side screenshots of the 6B3 reference at
https://sbox.game/mapperskai/ar_6b3, with the previously accepted body silhouette:

  * one large rectangular plate compartment down the middle of the chest, with a
    closure flap along its top edge, rather than a grid of small plate cells;
  * dark leather reinforcements flanking that compartment, running down from the
    shoulders and tapering to a point;
  * four magazine pouches in two pairs, with the compartment running between them;
  * wide cloth shoulder straps with leather tabs and roller buckles;
  * short side closures with frame buckles and a brown waist belt;
  * a wide upper rear compartment and two small rear-side pouches;
  * a long, rounded skirt rather than a straight hem.

Renders are CPU Cycles. Nothing is written to the game or to jazz_assets.
"""
import argparse
import json
import math
import shutil
import sys
from pathlib import Path

import bpy
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

p = argparse.ArgumentParser()
for key in ('sample', 'shirt', 'output'):
    p.add_argument('--' + key, type=Path, required=True)
p.add_argument('--skip-renders', action='store_true')
p.add_argument('--quick', action='store_true', help='icon, body and clay views only')
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
OUT = a.output.resolve()
(OUT / 'clean').mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- scene setup
bpy.ops.wm.open_mainfile(filepath=str(a.sample.resolve()))
rig = bpy.data.objects['Bip001']
body = bpy.data.objects['M_BaseMesh Skin_BIP']
for o in list(bpy.data.objects):
    if o not in (rig, body):
        bpy.data.objects.remove(o, do_unlink=True)
for c in bpy.data.collections:
    c.hide_render = False
    c.hide_viewport = False
body.hide_set(False)
body.hide_render = False
rig.hide_set(False)
rig.hide_render = True

# --------------------------------------------- actual clothed torso reference
# Same calibrated HGM convention as _morph_heavy_armor_fit.py.
data = json.loads(a.shirt.read_text(encoding='utf-8'))
mesh_data = data['meshes'][1]
box = mesh_data['bbox'] or data['bbox']
centre = [(box[i] + box[i + 3]) * .5 for i in range(3)]
shirt_verts = [(-(v[1] + centre[1]), -(v[0] + centre[0]), v[2] + centre[2])
               for v in mesh_data['vertices']]
shirt_faces = [tuple(reversed(f)) for f in mesh_data['faces']]
shirt_bvh = BVHTree.FromPolygons(shirt_verts, shirt_faces)

AXIS_Y = -.010
NZ, NT = 78, 144
ZS = np.linspace(.95, 1.53, NZ)
R_MIN, R_MAX = .125, .238


def direction(theta):
    """theta 0 is the chest; -Y is front in JA3 sample space."""
    return Vector((math.sin(theta), -math.cos(theta), 0))


radius = np.full((NZ, NT), np.nan)
for iz, z in enumerate(ZS):
    origin = Vector((0, AXIS_Y, float(z)))
    for it in range(NT):
        hit = shirt_bvh.ray_cast(origin, direction(2 * math.pi * it / NT), .8)
        if hit[0] is not None:
            radius[iz, it] = min(hit[3], R_MAX)
known = np.argwhere(np.isfinite(radius))
assert len(known) > NZ * NT * .5, 'insufficient shirt coverage'
for iz, it in np.argwhere(~np.isfinite(radius)):
    dt = np.minimum(abs(known[:, 1] - it), NT - abs(known[:, 1] - it))
    j, k = known[np.argmin((known[:, 0] - iz) ** 2 + (dt * .6) ** 2)]
    radius[iz, it] = radius[j, k]
for _ in range(7):
    padded = np.pad(radius, ((1, 1), (0, 0)), mode='edge')
    radius = (radius * 4 + np.roll(radius, 1, 1) + np.roll(radius, -1, 1)
              + padded[:-2] + padded[2:]) / 8
radius = np.clip(radius, R_MIN, R_MAX)


def smoothstep(t):
    t = max(0., min(1., t))
    return t * t * (3 - 2 * t)


def cluster(s):
    """Remap a uniform -1..1 parameter so samples bunch up near the rim."""
    return math.copysign(1 - (1 - abs(s)) ** 1.6, s)


def torso_radius(theta, z):
    t = (theta % (2 * math.pi)) / (2 * math.pi) * NT
    it, ft = int(t) % NT, t - int(t)
    zz = max(0., min(NZ - 1.0001, (z - ZS[0]) / (ZS[-1] - ZS[0]) * (NZ - 1)))
    iz, fz = int(zz), zz - int(zz)
    # Smoothstep rather than linear blending. Plain bilinear interpolation kinks
    # at every cell boundary, and those kinks beat against the panel column
    # spacing, which is what left the neckline and the plate rims sawtoothed.
    ft, fz = smoothstep(ft), smoothstep(fz)
    lo = radius[iz, it] * (1 - ft) + radius[iz, (it + 1) % NT] * ft
    hi = radius[iz + 1, it] * (1 - ft) + radius[iz + 1, (it + 1) % NT] * ft
    return float(lo * (1 - fz) + hi * fz)


def shell(theta, z, offset=0., radius_z=None):
    """Point on the clothed torso, pushed out along the radial direction.

    `radius_z` lets the skirt follow the waist instead of the flared shirt hem.
    """
    r = torso_radius(theta, z if radius_z is None else radius_z)
    return Vector((0, AXIS_Y, z)) + direction(theta) * (r + offset)


def shoulder_top(x, y, fallback=1.50):
    hit = shirt_bvh.ray_cast(Vector((x, y, 1.85)), Vector((0, 0, -1)), .6)
    return hit[0].z if hit[0] is not None else fallback


# ------------------------------------------------------------------ materials
def srgb(r, g, b):
    def channel(v):
        v /= 255.
        return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4
    return (channel(r), channel(g), channel(b))


def value_noise(n, cells, seed):
    rng = np.random.default_rng(seed)
    grid = rng.random((cells + 1, cells + 1))
    ys = np.linspace(0, cells, n, endpoint=False)
    xs = np.linspace(0, cells, n, endpoint=False)
    y0 = np.floor(ys).astype(int)
    x0 = np.floor(xs).astype(int)
    fy = ys - y0
    fx = xs - x0
    fy = fy * fy * (3 - 2 * fy)
    fx = fx * fx * (3 - 2 * fx)
    y1, x1 = y0 + 1, x0 + 1
    c00 = grid[y0[:, None], x0]
    c10 = grid[y0[:, None], x1]
    c01 = grid[y1[:, None], x0]
    c11 = grid[y1[:, None], x1]
    return (c00 * (1 - fx) + c10 * fx) * (1 - fy[:, None]) + (c01 * (1 - fx) + c11 * fx) * fy[:, None]


def fbm(n, seed, octaves=5, start=4):
    acc, amp, cells, norm = np.zeros((n, n)), 1., start, 0.
    for i in range(octaves):
        acc += amp * value_noise(n, cells, seed + i * 17)
        norm += amp
        amp *= .5
        cells = min(cells * 2, n // 2)
    return acc / norm


def height_to_normal(height, strength=6.):
    dy, dx = np.gradient(height)
    nrm = np.dstack((-dx * strength, -dy * strength, np.ones_like(height)))
    nrm /= np.linalg.norm(nrm, axis=2, keepdims=True)
    return nrm * .5 + .5


def save_map(path, rgb, color=True):
    """Write HxWx3 float 0-1 as a packed Blender image."""
    h, w = rgb.shape[:2]
    img = bpy.data.images.new(path.stem, w, h, alpha=False, float_buffer=False)
    img.colorspace_settings.name = 'sRGB' if color else 'Non-Color'
    pixels = np.ones((h, w, 4), dtype=np.float32)
    # Generated image buffers save these map values directly. Do not apply a
    # second sRGB conversion here (it darkens an olive 106 to about 36).
    pixels[..., :3] = rgb
    img.pixels.foreach_set(pixels[::-1].reshape(-1))
    img.filepath_raw = str(path)
    img.file_format = 'PNG'
    img.save()
    img.colorspace_settings.name = 'sRGB' if color else 'Non-Color'
    img.pack()
    return img


def build_preview_maps(folder, n=1024):
    """Tileable preview maps for the beauty render. Not a JA3 bake."""
    folder.mkdir(parents=True, exist_ok=True)
    u = np.linspace(0, 1, n, endpoint=False)
    uu, vv = np.meshgrid(u, u)
    maps = {}

    def store(stem, albedo, height, rough, nrm_str, color=True):
        base = save_map(folder / (stem + '_base.png'), np.clip(albedo, 0, 1), True)
        nrm = save_map(folder / (stem + '_nrm.png'), height_to_normal(height, nrm_str), False)
        rgh = save_map(folder / (stem + '_rgh.png'), np.clip(np.dstack([rough] * 3), 0, 1), False)
        maps[stem] = (base, nrm, rgh)

    # Cotton cover: soft yarn and wear only. A regular twill on a curved
    # torso beat against the lighting and zebra-striped the chest.
    wear = fbm(n, 11)
    dirt = fbm(n, 23, start=3)
    yarn = fbm(n, 37, octaves=6, start=24)
    weave = np.sin(uu * math.tau * 240) * np.sin(vv * math.tau * 240)
    height = .50 + .06 * (yarn - .5) + .04 * (wear - .5) + .012 * weave
    olive = np.array((91, 108, 71)) / 255.
    olive_d = np.array((62, 77, 48)) / 255.
    olive_dirt = np.array((102, 96, 68)) / 255.
    mix = np.clip(.5 + 1.4 * (wear - .5) + .4 * (dirt - .5), 0, 1)[..., None]
    albedo = olive_d * (1 - mix) + olive * mix
    albedo = albedo * (1 - .12 * dirt[..., None]) + olive_dirt * (.12 * dirt[..., None])
    rough = .78 + .10 * (1 - height) + .06 * dirt
    store('cover', albedo, height, rough, 24.)

    # Pouches: same family, slightly darker, no regular grid.
    height = .50 + .07 * (fbm(n, 41, start=20) - .5)
    pouch = np.array((91, 105, 70)) / 255.
    pouch_d = np.array((64, 77, 48)) / 255.
    mix = height[..., None]
    albedo = pouch_d * (1 - mix) + pouch * mix
    rough = .72 + .14 * (1 - height)
    store('pouch', albedo, height, rough, 9.)

    # Webbing: clear ribs along the strap.
    ribs = .5 + .5 * np.sin(vv * math.tau * 180)
    fibre = .15 * np.sin(uu * math.tau * 90)
    height = .48 + .06 * ribs + .025 * fibre + .04 * (fbm(n, 59) - .5)
    web = np.array((98, 102, 74)) / 255.
    web_d = np.array((70, 74, 50)) / 255.
    albedo = web_d * (1 - height[..., None]) + web * height[..., None]
    rough = .78 + .12 * (1 - ribs)
    store('webbing', albedo, height, rough, 10.)

    # Dark vinyl/leather: glossy grain, as on the owner's photograph.
    grain = fbm(n, 71, octaves=6, start=16)
    wrinkle = fbm(n, 83, start=3)
    height = .45 + .22 * (grain - .5) + .18 * (wrinkle - .5)
    hide = np.array((49, 58, 41)) / 255.
    hide_h = np.array((76, 86, 59)) / 255.
    albedo = hide * (1 - height[..., None]) + hide_h * height[..., None]
    rough = .52 + .13 * grain + .06 * wrinkle
    store('leather', albedo, height, rough, 7.)

    # Brushed steel hardware.
    brush = .5 + .5 * np.sin((uu * 140 + fbm(n, 97) * .8) * math.tau)
    pit = fbm(n, 101, start=8)
    height = .45 + .20 * (brush - .5) + .08 * (pit - .5)
    steel = np.array((138, 136, 128)) / 255.
    steel_d = np.array((88, 86, 80)) / 255.
    albedo = steel_d * (1 - brush[..., None]) + steel * brush[..., None]
    rough = .28 + .22 * (1 - brush) + .15 * pit
    store('hardware', albedo, height, rough, 5.)

    # Rust-red jersey for the fitting shirt.
    knit = .5 + .35 * np.sin(uu * math.tau * 48) + .15 * np.sin(vv * math.tau * 64)
    height = .45 + .20 * (knit - .5) + .10 * (fbm(n, 113) - .5)
    rust = np.array((118, 48, 40)) / 255.
    rust_d = np.array((78, 32, 28)) / 255.
    albedo = rust_d * (1 - height[..., None]) + rust * height[..., None]
    rough = .82 + .10 * (1 - height)
    store('shirt', albedo, height, rough, 6.)
    return maps


TEX = build_preview_maps(OUT / 'textures')


def material(name, colour, rough, metal=0., sheen=0., maps=None, uv_scale=6.,
             nrm_str=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*colour, 1)
    nodes, links = m.node_tree.nodes, m.node_tree.links
    bsdf = nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*colour, 1)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metal
    if sheen and 'Sheen Weight' in bsdf.inputs:
        bsdf.inputs['Sheen Weight'].default_value = sheen
        bsdf.inputs['Sheen Roughness'].default_value = .32
    if maps:
        uv = nodes.new('ShaderNodeTexCoord')
        mapping = nodes.new('ShaderNodeMapping')
        mapping.inputs['Scale'].default_value = (uv_scale, uv_scale, uv_scale)
        # UV, not Object: Object XYZ on a cylindrical torso cuts concentric
        # zebra rings through the cover, which is what the owner cropped.
        links.new(uv.outputs['UV'], mapping.inputs['Vector'])
        img_col = nodes.new('ShaderNodeTexImage')
        img_col.image = maps[0]
        links.new(mapping.outputs['Vector'], img_col.inputs['Vector'])
        links.new(img_col.outputs['Color'], bsdf.inputs['Base Color'])
        # Broad cloth variation survives the game atlas and ordinary camera distance.
        if 'hardware' not in name and 'shirt' not in name:
            noise = nodes.new('ShaderNodeTexNoise')
            noise.inputs['Scale'].default_value = 7.5
            noise.inputs['Detail'].default_value = 3.
            position = nodes.new('ShaderNodeNewGeometry')
            links.new(position.outputs['Position'], noise.inputs['Vector'])
            ramp_node = nodes.new('ShaderNodeValToRGB')
            ramp_node.color_ramp.elements[0].color = (.55, .58, .50, 1)
            ramp_node.color_ramp.elements[1].color = (1.10, 1.08, .98, 1)
            links.new(noise.outputs['Fac'], ramp_node.inputs['Fac'])
            mix_node = nodes.new('ShaderNodeMixRGB'); mix_node.blend_type = 'MULTIPLY'
            mix_node.inputs[0].default_value = .55
            links.new(img_col.outputs['Color'], mix_node.inputs[1])
            links.new(ramp_node.outputs['Color'], mix_node.inputs[2])
            links.new(mix_node.outputs[0], bsdf.inputs['Base Color'])
        img_rgh = nodes.new('ShaderNodeTexImage')
        img_rgh.image = maps[2]
        links.new(mapping.outputs['Vector'], img_rgh.inputs['Vector'])
        links.new(img_rgh.outputs['Color'], bsdf.inputs['Roughness'])
        img_n = nodes.new('ShaderNodeTexImage')
        img_n.image = maps[1]
        links.new(mapping.outputs['Vector'], img_n.inputs['Vector'])
        nrm = nodes.new('ShaderNodeNormalMap')
        nrm.inputs['Strength'].default_value = nrm_str
        links.new(img_n.outputs['Color'], nrm.inputs['Color'])
        links.new(nrm.outputs['Normal'], bsdf.inputs['Normal'])
    return m


MAT_COVER = material('6B3 cotton cover', srgb(118, 124, 86), .80, sheen=.12,
                     maps=TEX['cover'], uv_scale=2.2, nrm_str=.70)
MAT_POUCH = material('6B3 pouch cloth', srgb(104, 110, 76), .82, sheen=.18,
                     maps=TEX['pouch'], uv_scale=2.4, nrm_str=.32)
MAT_WEBBING = material('6B3 webbing', srgb(110, 114, 82), .86,
                       maps=TEX['webbing'], uv_scale=3.0, nrm_str=.45)
MAT_LEATHER = material('6B3 leather reinforcement', srgb(22, 22, 20), .52,
                       maps=TEX['leather'], uv_scale=3., nrm_str=.18)
# No coat: a clearcoat on a dark map reads as brushed steel under studio lights.
MAT_BELT = material('6B3 brown waist belt', srgb(57, 43, 32), .66)
MAT_HARDWARE = material('6B3 hardware', srgb(120, 118, 108), .34, metal=.92,
                        maps=TEX['hardware'], uv_scale=10., nrm_str=.9)
body.data.materials.clear()
body.data.materials.append(material('Fitting mannequin', srgb(52, 58, 62), .9))

# Colorization channel per part. Hardware is channel 0, meaning unmasked: the
# buckles keep their own metal in game rather than taking a cover tint.
CHANNEL = {MAT_COVER.name: 1, MAT_POUCH.name: 2, MAT_WEBBING.name: 2,
           MAT_LEATHER.name: 3, MAT_HARDWARE.name: 0, MAT_BELT.name: 0}
parts = []


def add_part(name, verts, faces, mat, solidify=0., bevel=0., smooth=0.):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([tuple(v) for v in verts], [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    obj.data.materials.append(mat)
    obj['hg_colorization'] = CHANNEL[mat.name]
    if solidify:
        mod = obj.modifiers.new('Cover thickness', 'SOLIDIFY')
        mod.thickness = solidify
        mod.offset = 1
        bpy.ops.object.modifier_apply(modifier=mod.name)
    if bevel:
        mod = obj.modifiers.new('Softened seam', 'BEVEL')
        mod.width = bevel
        mod.segments = 2
        mod.affect = 'EDGES'
        bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.uv.smart_project(island_margin=.01)
    bpy.ops.object.mode_set(mode='OBJECT')
    if smooth:
        bpy.ops.object.shade_smooth()
    obj.select_set(False)
    parts.append(obj)
    return obj


def grid_faces(rows, cols):
    return [(r * cols + c, r * cols + c + 1, (r + 1) * cols + c + 1, (r + 1) * cols + c)
            for r in range(rows - 1) for c in range(cols - 1)]


def sheet_faces(cols, rows):
    """Faces closing a front sheet over a back sheet built on the same grid."""
    n = cols * rows
    faces = []
    for r in range(rows - 1):
        for c in range(cols - 1):
            i = r * cols + c
            faces.append((i, i + 1, i + cols + 1, i + cols))
            j = n + i
            faces.append((j + cols, j + cols + 1, j + 1, j))
    rim = list(range(cols))
    rim += [r * cols + cols - 1 for r in range(1, rows)]
    rim += [(rows - 1) * cols + c for c in range(cols - 2, -1, -1)]
    rim += [r * cols for r in range(rows - 2, 0, -1)]
    for i, idx in enumerate(rim):
        nxt = rim[(i + 1) % len(rim)]
        faces.append((idx, nxt, n + nxt, n + idx))
    return faces


def ramp(a_, stops):
    for i in range(len(stops) - 1):
        a0, z0 = stops[i]
        a1, z1 = stops[i + 1]
        if a_ <= a1:
            return z0 + (z1 - z0) * smoothstep((a_ - a0) / (a1 - a0))
    return stops[-1][1]


def fold(theta, z, damp=1.):
    """Slack in the cloth, so the cover is not a perfectly ruled surface.

    `damp` fades the noise out at the panel outline. Left running to the rim it
    aliased against the column spacing and left the neck edge visibly sawtoothed.
    """
    return damp * (.0010 * math.sin(theta * 6.7 + z * 37) * math.cos(z * 29 - theta * 3.3)
                   + .0007 * math.sin(theta * 12.1 - z * 61))


# ------------------------------------------------------------- panel geometry
COVER_GAP, COVER_THICK = .014, .008
OUTER = COVER_GAP + COVER_THICK
FRONT_SPAN, BACK_SPAN = 1.18, 1.26
# A long skirt with a rounded bottom, as in the reference. The earlier straight
# hem finishing just under the pouches made the vest look like a plate carrier.
# Measured off the reference rather than guessed: the collar bottoms out only
# 9% of the vest's height below the crown of the shoulder pads, and the cloth
# rises away from it in a wide shallow arc. The steeper cut used before read as
# a narrow V and bared the upper chest.
# High, shallow neck and bulky shoulders: the photograph is a hanging 6B3
# cover, not a plate carrier. The earlier scoop left a deep V and long straps.
FRONT_TOP = [(0, 1.429), (.18, 1.432), (.38, 1.445), (.62, 1.470),
             (.84, 1.478), (1.02, 1.462), (1.14, 1.410), (1.18, 1.368)]
FRONT_BOTTOM = [(0, 0.982), (.40, 0.988), (.78, 1.010), (1.04, 1.042), (1.18, 1.072)]
BACK_TOP = [(0, 1.448), (.22, 1.454), (.48, 1.470), (.88, 1.476),
            (1.08, 1.450), (1.26, 1.372)]
BACK_BOTTOM = [(0, 0.994), (.40, 1.000), (.78, 1.022), (1.08, 1.054), (1.26, 1.082)]
HEM_CLING = 1.075  # below the waist, keep following the waist radius


def panel_grid(span, top, bottom, cols, rows):
    """(theta, z, radial offset) per grid node, shared by the panel and its binding.

    The binding used to walk its own coarser outline. Where the two disagreed the
    tape alternately poked through and sank into the cover, which is what tore up
    the neckline. One grid, one outline.
    """
    grid = []
    for r in range(rows):
        edge_z = smoothstep(min(r, rows - 1 - r) / 2.)
        row = []
        for c in range(cols):
            theta = -span + 2 * span * c / (cols - 1)
            a_ = abs(theta)
            z = ramp(a_, bottom) + (ramp(a_, top) - ramp(a_, bottom)) * r / (rows - 1)
            damp = edge_z * smoothstep((span - a_) / .18)
            row.append((theta, z, COVER_GAP + fold(theta, z, damp)))
        grid.append(row)
    return grid


def panel(name, base, grid):
    rows, cols = len(grid), len(grid[0])
    verts = [shell(base + theta, z, off, radius_z=max(z, HEM_CLING))
             for row in grid for theta, z, off in row]
    # The binding tape covers the rim, so the panel needs no bevel of its own.
    obj = add_part(name, verts, grid_faces(rows, cols), MAT_COVER, COVER_THICK, 0., 52)
    # Continuous cloth coordinates across the cover. Smart-project islands cut
    # both the colour and weave into visible triangular patches on the back.
    for loop in obj.data.loops:
        point = obj.data.vertices[loop.vertex_index].co
        theta = math.atan2(point.x, -(point.y - AXIS_Y)) - base
        theta = (theta + math.pi) % math.tau - math.pi
        span = max(abs(row[0][0]) for row in grid)
        obj.data.uv_layers.active.data[loop.index].uv = (
            .225 + .20 * theta / span, .015 + (point.z - .97) * .75)
    return obj


def binding(name, base, grid, radius=.0055):
    """Bound edge tape, threaded through the exact nodes of the panel outline.

    The radius has to exceed the panel's half thickness, or the tape hides
    inside the 19 mm slab and all that shows is a thin crescent past the rim,
    which reads as a torn edge rather than a bound one.
    """
    rows, cols = len(grid), len(grid[0])
    loop = [grid[0][c] for c in range(cols)]
    loop += [grid[r][cols - 1] for r in range(1, rows)]
    loop += [grid[rows - 1][c] for c in range(cols - 2, -1, -1)]
    loop += [grid[r][0] for r in range(rows - 2, 0, -1)]
    pts = [shell(base + theta, z, off + COVER_THICK * .5, radius_z=max(z, HEM_CLING))
           for theta, z, off in loop]
    verts, faces = [], []
    n = len(pts)
    for i in range(n):
        # Carry the cross-section perpendicular to the path. Pinned to the radial
        # and vertical axes instead, it pinched into a spike where the outline
        # climbs steeply from the neck cut to the shoulder.
        tangent = pts[(i + 1) % n] - pts[(i - 1) % n]
        tangent = tangent.normalized() if tangent.length > 1e-6 else Vector((1, 0, 0))
        radial = direction(base + loop[i][0])
        u = radial - tangent * radial.dot(tangent)
        u = u.normalized() if u.length > 1e-6 else Vector((0, 0, 1))
        v = tangent.cross(u)
        for j in range(4):
            ang = j * math.tau / 4 + math.pi / 4
            verts.append(pts[i] + u * (radius * math.cos(ang))
                         + v * (radius * math.sin(ang)))
    for i in range(n):
        i2 = (i + 1) % n
        for j in range(4):
            faces.append((i * 4 + j, i * 4 + (j + 1) % 4,
                          i2 * 4 + (j + 1) % 4, i2 * 4 + j))
    return add_part(name, verts, faces, MAT_WEBBING, 0., 0., 60)


FRONT_GRID = panel_grid(FRONT_SPAN, FRONT_TOP, FRONT_BOTTOM, cols=41, rows=15)
BACK_GRID = panel_grid(BACK_SPAN, BACK_TOP, BACK_BOTTOM, cols=35, rows=15)
panel('Vest front panel', 0., FRONT_GRID)
panel('Vest back panel', math.pi, BACK_GRID)
binding('Front edge binding', 0., FRONT_GRID)
binding('Rear edge binding', math.pi, BACK_GRID)

# Everything sewn onto the vest is placed on the cover the mesh actually has,
# not on the ideal torso. Over the collarbone, where the torso radius changes
# fastest, the chords of a 15 row panel bow outward by nearly 3 mm, and patches
# placed on the ideal surface sank under the cover along their top edge. No
# amount of extra tessellation on the patch could fix that, because the error
# was in the surface underneath it.
cover_trees = {}
for _name, _key in (('Vest front panel', 0), ('Vest back panel', 1)):
    _obj = bpy.data.objects[_name]
    _obj.data.calc_loop_triangles()
    cover_trees[_key] = BVHTree.FromPolygons(
        [v.co.copy() for v in _obj.data.vertices],
        [tuple(t.vertices) for t in _obj.data.loop_triangles], all_triangles=True)


def cover_out(base, theta, z):
    """Height of the cover's outer face above the torso at (theta, z)."""
    d = direction(base + theta)
    start = Vector((0, AXIS_Y, z)) + d * .60
    hit = cover_trees[0 if abs(base) < 1. else 1].ray_cast(start, -d, .55)
    if hit[0] is None:
        return OUTER
    return (.60 - hit[3]) - torso_radius(base + theta, z)


def bulge(half_th, half_z, depth, power, fillet):
    """Raised profile over a rounded-rectangle footprint, in local -1..1 space.

    `power` rounds the corners, `fillet` sets how much of the span is spent
    climbing to full height: small for a plate compartment that should read flat
    on top, large for a soft pouch.
    """
    def f(u, v):
        if abs(u) >= 1 or abs(v) >= 1:
            return 0.
        t = (abs(u) ** power + abs(v) ** power) ** (1. / power)
        return depth * smoothstep((1 - t) / fillet)
    return f


def pillow(name, base, th0, th1, z0, z1, depth, mat, cols=9, rows=7,
           power=4., fillet=.85, lie=.0030, carrier=None, taper=0., skew=0.,
           tilt=0., smooth=48):
    """A closed puffy volume sewn to the cover: compartment, pouch, flap or pad.

    An open grid plus Solidify reads as a box with a dark hole at the bottom,
    which is what made the first pouches look like paper bags. A watertight
    pillow is both cheaper in triangles and correct for anything soft.

    `lie` is how far the rim stands off its carrier. It has to clear the slack in
    the cloth underneath, about 1.2 mm, because the whole rim ring is visible and
    the carrier must pass behind it rather than through it.

    `carrier` is the profile of whatever this part lies on, so a flap follows the
    bulge of its pouch instead of floating in front of it as a flat slab.
    `taper` narrows the footprint towards the bottom and `skew` slides it
    sideways there. `tilt` rakes the whole footprint, dropping one end below the
    other: that is what gives the leather reinforcements their diagonal lower
    edge, which no amount of taper can produce on its own.
    Returns a seat function for the next part up.
    """
    lie = max(lie, .0035)
    th0, th1 = min(th0, th1), max(th0, th1)
    th_c, half_th = (th0 + th1) * .5, (th1 - th0) * .5
    z_c, half_z = (z0 + z1) * .5, (z1 - z0) * .5
    profile = bulge(half_th, half_z, depth, power, fillet)

    def place(u, v):
        """Local -1..1 to (theta, z), honouring taper, skew and tilt."""
        drop = (1 - v) * .5
        return (th_c + half_th * (skew * drop + u * (1 - taper * drop)),
                z_c + half_z * v + tilt * u)

    def seat(theta, z):
        """Height of this part's surface above the cover, in panel coordinates.

        Carriers have to speak a common language: every pillow has its own local
        -1..1 space, so handing one part's local profile to a part with a
        different footprint put the pouch closures nowhere near their flaps.

        With tilt on, u and v depend on each other, so the inverse is reached by
        a few fixed point passes rather than in closed form.
        """
        u, v = (theta - th_c) / half_th, (z - z_c) / half_z
        for _ in range(3):
            v = (z - z_c - tilt * u) / half_z
            drop = (1 - v) * .5
            width = 1 - taper * drop
            u = 2. if width < 1e-6 else ((theta - th_c) / half_th - skew * drop) / width
        return lie + profile(u, v) + (carrier(theta, z) if carrier else 0.)

    # The backing sheet is a dish: a thin lip at the rim, dropping away to well
    # under the carrier in the middle. Sinking it by a constant amount instead
    # left a tall vertical wall all round, and the cover cut across that wall
    # half way up, so the visible outline of every patch followed the slack in
    # the cloth and came out wavy no matter how finely the patch was tessellated.
    dip = max(.0060, depth * .45)
    front, back = [], []
    for r in range(rows):
        v = cluster(r / (rows - 1) * 2 - 1)
        for c in range(cols):
            u = cluster(c / (cols - 1) * 2 - 1)
            theta, z = place(u, v)
            t = (abs(u) ** power + abs(v) ** power) ** (1. / power)
            inside = smoothstep((1 - t) / .30)
            base_r = cover_out(base, theta, z) + lie + (carrier(theta, z) if carrier else 0.)
            cloth_fold = (.0016 * math.sin(u * 11 + v * 4) * math.sin(v * 8 - u * 3)
                          * max(0., 1 - abs(u)) * max(0., 1 - abs(v))) if depth > .01 else 0.
            front.append(shell(base + theta, z, base_r + profile(u, v) + cloth_fold))
            back.append(shell(base + theta, z, base_r - .0060 - max(0., dip - .0060) * inside))
    part=add_part(name, front + back, sheet_faces(cols, rows), mat, 0., 0., smooth)
    if name.startswith(('Magazine pouch flap', 'Upper vinyl reinforcement', 'Front plate compartment')):
        # A narrow sewn border, following the same surface as the flap, not a floating card.
        seam_verts, seam_faces = [], []
        part.data.calc_loop_triangles()
        seam_bvh=BVHTree.FromPolygons([v.co for v in part.data.vertices],
            [tuple(t.vertices) for t in part.data.loop_triangles],all_triangles=True)
        for i in range(64):
            angle = math.tau * i / 64
            u = math.copysign(abs(math.cos(angle)) ** (2 / power), math.cos(angle))
            v = math.copysign(abs(math.sin(angle)) ** (2 / power), math.sin(angle))
            for radius in (.88, .90):
                theta, z = place(u * radius, v * radius)
                ray=direction(base+theta)
                point=shell(base+theta,z,.20)
                hit,normal,_,_=seam_bvh.ray_cast(point,-ray,.5)
                assert hit is not None,name
                seam_verts.append(hit+normal*.0005)
        for i in range(64):
            j = (i + 1) % 64
            seam_faces.append((2*i, 2*i+1, 2*j+1, 2*j))
        add_part(name + ' sewn edge', seam_verts, seam_faces, MAT_WEBBING, 0., 0., 0.)
    return seat


def ribbon(name, frames, half_w, thick, mat, smooth=50):
    """Sweep a rectangular cross-section along a framed path, capped at the ends."""
    verts = []
    for point, side_v, normal_v in frames:
        s = side_v.normalized() * half_w
        nrm = normal_v.normalized() * (thick * .5)
        verts += [point - s - nrm, point + s - nrm, point + s + nrm, point - s + nrm]
    faces = []
    for i in range(len(frames) - 1):
        for j in range(4):
            faces.append((i * 4 + j, i * 4 + (j + 1) % 4,
                          (i + 1) * 4 + (j + 1) % 4, (i + 1) * 4 + j))
    last = (len(frames) - 1) * 4
    faces.append((3, 2, 1, 0))
    faces.append((last, last + 1, last + 2, last + 3))
    return add_part(name, verts, faces, mat, 0., 0., smooth)


def frames_along(points, side_v):
    """Frames whose normal always points away from the torso axis."""
    out = []
    for i, pt in enumerate(points):
        tangent = points[min(i + 1, len(points) - 1)] - points[max(i - 1, 0)]
        if tangent.length < 1e-6:
            tangent = Vector((0, 1, 0))
        nrm = side_v.cross(tangent).normalized()
        if nrm.dot((pt - Vector((0, AXIS_Y, 1.24))).normalized()) < 0:
            nrm = -nrm
        out.append((pt, side_v.copy(), nrm))
    return out


def strap_surface(name, path, half_w, thick, mat, cols=5, window=.30, smooth=50,
                  conform=True):
    """Strap that wraps the torso at its ends and flattens over the crown.

    A flat 90 mm chord stands 32 mm off a 200 mm torso, so a planar ribbon punched
    straight out through the cover wherever it entered the panel. Returns the
    centre line with its outward normal, for mounting tabs and buckles.
    """
    steps = len(path)
    front, back, spine = [], [], []
    for i, pt in enumerate(path):
        t = i / (steps - 1)
        # A part that never touches the torso must stay planar end to end. Left
        # to conform at its ends, the shoulder pad wrapped a torso radius sampled
        # above the shoulder, where there is no torso, and threw out spikes.
        flat = smoothstep(min(t, 1 - t) / window) if conform else 1.
        r = math.hypot(pt.x, pt.y - AXIS_Y)
        theta = math.atan2(pt.x, -(pt.y - AXIS_Y))
        # Hold a constant offset from the torso across the width. Sweeping a
        # circular arc of fixed radius instead assumes a round body, and on the
        # narrower chest the outer corner of the strap came out of the cover.
        off = r - torso_radius(theta, pt.z)
        out = (Vector((pt.x, pt.y - AXIS_Y, 0)).normalized() * (1 - flat)
               + Vector((0, 0, 1)) * flat)
        out = out.normalized() if out.length > 1e-6 else Vector((0, 0, 1))
        spine.append((pt, out))
        for c in range(cols):
            s = cluster(c / (cols - 1) * 2 - 1)
            curved = shell(theta + s * half_w / r, pt.z, off)
            rounded_width = half_w * (.70 + .30 * math.sin(math.pi * t) ** .5)
            mid = curved.lerp(pt + Vector((s * rounded_width, 0, 0)), flat)
            # A flat transverse section left shoulder wings hovering above the
            # sloping shirt. Preserve centre-line clearance while following the
            # real garment across the width, including the outer pad corners.
            centre_surface = shoulder_top(pt.x, pt.y, fallback=pt.z)
            edge_surface = shoulder_top(mid.x, mid.y, fallback=centre_surface)
            # The inner ray can hit the neck/collar instead of the shoulder;
            # do not turn that height discontinuity into an upward spike.
            slope = max(-.025, min(.005, edge_surface - centre_surface))
            mid.z += slope * flat * smoothstep((pt.z - 1.42) / .05)
            front.append(mid + out * (thick * .5))
            back.append(mid - out * (thick * .5))
    add_part(name, front + back, sheet_faces(cols, steps), mat, 0., 0., smooth)
    return spine


def buckle(name, centre, along, normal, half_along, half_across, bar=.0032, steps=12):
    """Rectangular frame buckle. A flat dark quad read as a sticker on the strap."""
    along = along.normalized()
    normal = normal.normalized()
    across = along.cross(normal).normalized()
    verts, faces = [], []
    for i in range(steps):
        ang = math.tau * i / steps
        ca, sa = math.cos(ang), math.sin(ang)
        offset = (along * (math.copysign(abs(ca) ** .5, ca) * (half_along - bar))
                  + across * (math.copysign(abs(sa) ** .5, sa) * (half_across - bar)))
        radial = offset.normalized() if offset.length > 1e-6 else along
        for j in range(4):
            b = math.tau * j / 4 + math.pi / 4
            verts.append(centre + offset + radial * (bar * 1.414 * math.cos(b))
                         + normal * (bar * 1.414 * math.sin(b)))
    for i in range(steps):
        i2 = (i + 1) % steps
        for j in range(4):
            faces.append((i * 4 + j, i * 4 + (j + 1) % 4,
                          i2 * 4 + (j + 1) % 4, i2 * 4 + j))
    return add_part(name, verts, faces, MAT_HARDWARE, 0., 0., 45)


# -------------------------------------------------------- plate compartment
# One big rectangle down the centre of the chest, with its closure flap along the
# top edge. The reference has no grid of small plate cells on the outside.
# Sized off the reference: the compartment is a third of the chest's width, its
# top sits just under the collar and it runs down to the line the pouches hang
# from. The earlier one was two fifths wide, which crowded the leather out to
# the armholes.
COMP_TH, COMP_TOP, COMP_BOTTOM = .46, 1.402, 1.205
comp = pillow('Front plate compartment', 0., -COMP_TH, COMP_TH, COMP_BOTTOM, COMP_TOP,
              .0055, MAT_COVER, cols=15, rows=13, power=10., fillet=.18)
# Keep the flap inside the flat top of the compartment, clear of the rim where
# the compartment is already falling away.
flap = pillow('Front compartment flap', 0., -COMP_TH + .036, COMP_TH - .036, 1.356,
              COMP_TOP - .003, .006, MAT_COVER, cols=13, rows=4, power=8.,
              fillet=.30, lie=.0012, carrier=comp)
# The upper rear compartment has its own broad closure flap.
rear_comp = pillow('Rear plate compartment', math.pi, -.68, .68, 1.215, 1.445,
                   .007, MAT_COVER, cols=15, rows=13, power=8., fillet=.18)
pillow('Rear plate compartment flap', math.pi, -.665, .665, 1.402, 1.447,
       .005, MAT_COVER, cols=15, rows=4, power=8., fillet=.25,
       lie=.001, carrier=rear_comp)

# The current owner reference has olive vinyl reinforcements from the shoulder
# buckles to the sides of the chest compartment, with a diagonal lower edge.
for side in (-1, 1):
    pillow('Upper vinyl reinforcement '+str(side), 0., side*.46, side*1.08,
           1.285, 1.418, .0025, MAT_LEATHER, cols=11, rows=11,
           power=6., fillet=.30, taper=.12, tilt=0., lie=.0012)

# ----------------------------------------------------------- magazine pouches
# Two pairs, with the compartment running down between them.
# Inboard of the vest sides, with a clear skirt below. The earlier pair sat
# on the outline and read as a plate-carrier belt of crates.
POUCH_TOP, POUCH_BOTTOM, POUCH_HALF = 1.220, 1.017, .155
for index, th in enumerate((-.86, -.54, .54, .86)):
    tag = index + 1
    # Magazine pouches hold two AK magazines. They are shallow cloth boxes, not
    # cargo balloons: a flatter face, short rounded sides, about 28 mm of
    # stand-off. The 50 mm pillow with a long fillet read as stuffed duffels.
    body_profile = pillow('Magazine pouch %d' % tag, 0.,
                          th - POUCH_HALF, th + POUCH_HALF, POUCH_BOTTOM, POUCH_TOP,
                          .024, MAT_POUCH, cols=11, rows=9, power=8., fillet=.18)
    # The lid covers two thirds of the pouch face, as on the reference, and the
    # inner pouch of each pair carries a longer one. A 50 mm lid on a 120 mm
    # pouch left a band of bare pouch that reads as a seam rather than a flap.
    drop = .128 if abs(th) > .8 else .150
    lid = pillow('Magazine pouch flap %d' % tag, 0.,
                 th - POUCH_HALF + .004, th + POUCH_HALF - .004,
                 POUCH_TOP - drop, POUCH_TOP - .004, .006, MAT_POUCH,
                 cols=11, rows=6, power=10., fillet=.14, lie=.0015,
                 carrier=body_profile)
# Small rear-side pockets leave the middle of the back free for the belt.
for side in (-1, 1):
    th = side * .92
    pocket = pillow('Rear side pocket ' + str(side), math.pi, th - .20, th + .20,
                    1.035, 1.170, .028, MAT_POUCH, cols=9, rows=7, power=5., fillet=.30)
    pillow('Rear side pocket flap ' + str(side), math.pi, th - .196, th + .196,
           1.120, 1.174, .004, MAT_POUCH, cols=9, rows=4, power=5., fillet=.30,
           lie=.001, carrier=pocket)

# ------------------------------------------------------------ shoulder straps
STRAP_THETA = .74
STRAP_HALF = .052
STRAP_STEPS = 17


def shoulder_layer(name, surface, half_width, thickness, mat, offset=0., start=0, end=None):
    # Every sewn layer samples the same shoulder surface and tangent normals.
    # Slicing/reframing the centreline separately made the pads float at their ends.
    end = len(surface) if end is None else end
    verts, frames = [], []
    for i in range(start, end):
        row = surface[i]
        across = (row[-1] - row[0]).normalized()
        tangent = surface[min(i + 1, len(surface)-1)][2] - surface[max(i - 1, 0)][2]
        normal = across.cross(tangent).normalized()
        if normal.z < 0:
            normal = -normal
        frames.append((row[2], across, normal))
        for face_sign in (1, -1):
            for c in range(5):
                q = 2 + (c / 4 * 2 - 1) * 2 * half_width / STRAP_HALF
                j = min(3, max(0, int(q)))
                point = row[j].lerp(row[j + 1], q - j)
                verts.append(point + normal * (offset + face_sign * thickness / 2))
    front = [verts[i * 10 + c] for i in range(len(frames)) for c in range(5)]
    back = [verts[i * 10 + 5 + c] for i in range(len(frames)) for c in range(5)]
    add_part(name, front + back, sheet_faces(5, len(frames)), mat, smooth=50)
    return frames


for side in (-1, 1):
    tag = 'L' if side < 0 else 'R'
    front_z = ramp(STRAP_THETA, FRONT_TOP) - .003
    back_z = ramp(STRAP_THETA, BACK_TOP) - .003
    front_anchor = shell(side * STRAP_THETA, front_z,
                         cover_out(0., side * STRAP_THETA, front_z) - COVER_THICK * .5)
    back_anchor = shell(math.pi - side * STRAP_THETA, back_z,
                        cover_out(math.pi, -side * STRAP_THETA, back_z) - COVER_THICK * .5)
    # Fit one smooth centre-line to the shoulder. A worst-case outer-edge
    # envelope inflated the whole arch and left the pad floating over the shirt.
    ts = np.linspace(0., 1., STRAP_STEPS)
    heights = []
    for t in ts:
        base = front_anchor.lerp(back_anchor, float(t))
        top = shoulder_top(base.x, base.y, fallback=base.z)
        clearance = max(base.z, min(top, 1.555) + .011)
        blend = smoothstep(min(t, 1 - t) / .16)
        heights.append(base.z + (clearance - base.z) * blend)
    curve = np.polyval(np.polyfit(ts, heights, 4), ts)
    curve += (front_z - curve[0]) * (1 - ts) + (back_z - curve[-1]) * ts
    path = []
    for t, height in zip(ts, curve):
        pt = front_anchor.lerp(back_anchor, float(t))
        pt.z = float(height)
        path.append(pt)
    surface = []
    for i, point in enumerate(path):
        t = i / (len(path) - 1)
        row = []
        for c in range(5):
            u = c / 4 * 2 - 1
            theta = side * STRAP_THETA + u * .28
            fz = ramp(abs(theta), FRONT_TOP) - .003
            bz = ramp(abs(theta), BACK_TOP) - .003
            fa = shell(theta, fz, cover_out(0., theta, fz) - .003)
            ba = shell(math.pi - theta, bz, cover_out(math.pi, -theta, bz) - .003)
            endpoint = fa.lerp(ba, t)
            endpoint.z += point.z - (front_z * (1-t) + back_z * t)
            # Transverse arch fades continuously into both panel rims.
            endpoint.z -= .002 * u*u * math.sin(math.pi*t)
            row.append(endpoint)
        surface.append(row)
    shoulder_layer('Shoulder strap ' + tag, surface, STRAP_HALF, .006, MAT_COVER)
    shoulder_layer('Shoulder pad ' + tag, surface, STRAP_HALF - .004,
                   .003, MAT_COVER, offset=.0048, start=2, end=9)
    belt = shoulder_layer('Shoulder adjustment strap ' + tag, surface,
                          .015, .0025, MAT_WEBBING, offset=.0085, start=1, end=14)
    point, across, normal = belt[3]
    along = path[5] - path[3]
    buckle('Shoulder buckle ' + tag, point + normal * .016,
           along, normal, .014, .022, bar=.0025)
    # Visible circular eyelets on one continuous punched adjustment strap.
    for number in (3, 5, 7, 9):
        point, across, normal = belt[number]
        along = normal.cross(across).normalized()
        centre = point + normal * .012
        verts = []
        for eyelet_radius in (.0028, .0046):
            for j in range(8):
                angle = math.tau * j / 8
                verts.append(centre + (across * math.cos(angle) + along * math.sin(angle)) * eyelet_radius)
        faces = [(j, (j + 1) % 8, (j + 1) % 8 + 8, j + 8) for j in range(8)]
        add_part('Shoulder eyelet %s %s' % (tag, number), verts, faces, MAT_HARDWARE)

# -------------------------------------------------------- side leather closure
# Both ends sit well under the panels; running them to the very edge left the
# straps apparently hanging in mid air from some angles.
# The buckles ride just outboard of the panel edge, where the reference has
# them and where they clear the magazine pouches. Set 160 mrad inboard as
# before, the lower buckle sat inside the outer pouch and vanished.
SIDE_FROM = FRONT_SPAN - .05
SIDE_TO = math.pi - (BACK_SPAN - .05)
for side in (-1, 1):
    tag = 'L' if side < 0 else 'R'
    for level, z in enumerate((1.150, 1.245)):
        steps = 9
        path = []
        for i in range(steps):
            th = side * (SIDE_FROM + (SIDE_TO - SIDE_FROM) * i / (steps - 1))
            local = th if abs(th) < math.pi * .5 else math.pi - th
            path.append(shell(th, z, cover_out(0. if abs(th) < math.pi * .5 else math.pi,
                                               local, z) - .005))
        ribbon('Side strap %s%d' % (tag, level + 1),
               frames_along(path, Vector((0, 0, 1))), .011, .004, MAT_LEATHER)
        anchor = side * (SIDE_FROM + .06)
        buckle('Side buckle %s%d' % (tag, level + 1),
               shell(anchor, z, cover_out(0., anchor, z) + .002),
               Vector((0, 0, 1)), direction(anchor), .015, .019)
# Brown waist belt lies behind the magazine pouches and crosses the back.
belt_path = []
for i in range(65):
    th = math.tau * i / 64
    local = (th + math.pi) % math.tau - math.pi
    base = 0. if math.cos(th) >= 0 else math.pi
    if base:
        local = (th - math.pi + math.pi) % math.tau - math.pi
    belt_path.append(shell(th, 1.128, cover_out(base, local, 1.128) + .004))
ribbon('Waist belt', frames_along(belt_path, Vector((0, 0, 1))), .023, .004, MAT_BELT)
buckle('Waist belt buckle', shell(0, 1.128, cover_out(0, 0, 1.128) + .012),
       Vector((0, 0, 1)), direction(0), .025, .033, bar=.003)

# ------------------------------------------------------------------- measures
for obj in parts:
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    # The final export joins these parts and prepares again; keep the clean
    # source free of split/custom normals as well.
    from _ja3_mesh_prepare import clear_custom_normals
    clear_custom_normals(obj)
    obj.data.calc_loop_triangles()

triangles = sum(len(o.data.loop_triangles) for o in parts)
vertices = sum(len(o.data.vertices) for o in parts)
assert triangles <= 17000, 'over the Torso budget: %d' % triangles

# Clearance to the real clothing, measured rather than eyeballed from renders.
panel_bvh = {}
for obj in parts:
    if obj.name.startswith('Vest '):
        panel_bvh[obj.name] = BVHTree.FromPolygons(
            [v.co.copy() for v in obj.data.vertices],
            [tuple(t.vertices) for t in obj.data.loop_triangles], all_triangles=True)


def clearance(name, centre_theta, span):
    """Gap from the cover to the shirt, along the whole span of the panel.

    Rays that land on a sleeve are dropped. The vest passes under the arm by
    design, and the radius map is capped at R_MAX exactly there, so those
    samples would report a penetration that does not exist on the torso.
    """
    gaps, sleeve = [], 0
    for z in np.linspace(1.06, 1.39, 28):
        for theta in np.linspace(centre_theta - span, centre_theta + span, 27):
            origin = Vector((0, AXIS_Y, float(z)))
            d = direction(float(theta))
            armour = panel_bvh[name].ray_cast(origin, d, .8)
            cloth = shirt_bvh.ray_cast(origin, d, .8)
            if armour[0] is None or cloth[0] is None:
                continue
            if cloth[3] > R_MAX - .002:
                sleeve += 1
                continue
            gaps.append(armour[3] - cloth[3])
    return {'samples': len(gaps), 'sleeve_samples_dropped': sleeve,
            'min_mm': round(min(gaps) * 1000, 2),
            'median_mm': round(float(np.median(gaps)) * 1000, 2),
            'p95_mm': round(float(np.percentile(gaps, 95)) * 1000, 2)}


# Sample the whole span, including the side wings: the narrower window used
# before could not have caught a wing standing off the ribs.
fit = {'front': clearance('Vest front panel', 0., FRONT_SPAN - .04),
       'rear': clearance('Vest back panel', math.pi, BACK_SPAN - .04)}
assert fit['front']['min_mm'] > -1 and fit['rear']['min_mm'] > -1, fit
assert fit['front']['p95_mm'] < 35 and fit['rear']['p95_mm'] < 35, fit

# ------------------------------------------------------------------- renders
shirt_mesh = bpy.data.meshes.new('LegionGoon shirt reference')
shirt_mesh.from_pydata(shirt_verts, [], shirt_faces)
shirt_mesh.update()
shirt_obj = bpy.data.objects.new('Fitting reference LegionGoon shirt', shirt_mesh)
bpy.context.collection.objects.link(shirt_obj)
shirt_mesh.materials.append(material('Fitting shirt', srgb(118, 48, 40), .86,
                                     maps=TEX['shirt'], uv_scale=16., nrm_str=1.0))
for poly in shirt_mesh.polygons:
    poly.use_smooth = True
bpy.ops.object.select_all(action='DESELECT')
shirt_obj.select_set(True)
bpy.context.view_layer.objects.active = shirt_obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(island_margin=.01)
bpy.ops.object.mode_set(mode='OBJECT')
shirt_obj.select_set(False)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 40
scene.cycles.use_denoising = True
scene.view_settings.view_transform = 'AgX'
scene.view_settings.look = 'None'
scene.view_settings.exposure = -0.10
scene.world.use_nodes = True
background = scene.world.node_tree.nodes['Background']
background.inputs[0].default_value = (.05, .05, .055, 1)
background.inputs[1].default_value = .5


def aim(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()


for name, location, power, size in (('Key', (-1.5, -2.2, 3.0), 130, 1.7),
                                    ('Fill', (2.1, -1.2, 1.8), 70, 1.6),
                                    ('Rim', (-.8, 2.4, 2.7), 165, 1.3)):
    bpy.ops.object.light_add(type='AREA', location=location)
    light = bpy.context.object
    light.name = name
    light.data.energy = power
    light.data.shape = 'DISK'
    light.data.size = size
    aim(light, (0, 0, 1.24))

bpy.ops.object.camera_add(location=(0, -2.6, 1.28))
camera = bpy.context.object
camera.data.type = 'ORTHO'
scene.camera = camera

lo = Vector((min(v.co.x for o in parts for v in o.data.vertices),
             min(v.co.y for o in parts for v in o.data.vertices),
             min(v.co.z for o in parts for v in o.data.vertices)))
hi = Vector((max(v.co.x for o in parts for v in o.data.vertices),
             max(v.co.y for o in parts for v in o.data.vertices),
             max(v.co.z for o in parts for v in o.data.vertices)))
focus = (lo + hi) * .5
frame = max(hi.x - lo.x, hi.z - lo.z) * 1.08


def render(path, resolution=None, transparent=False):
    if resolution:
        scene.render.resolution_x, scene.render.resolution_y = resolution
    scene.render.film_transparent = transparent
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def place(cx, cy, cz, target, scale):
    camera.location = (cx, cy, cz)
    camera.data.ortho_scale = scale
    aim(camera, target)


VIEWS = {'front': (0, -2.6), 'back': (0, 2.6), 'side': (2.6, 0), 'oblique': (-1.85, -1.85)}
if not a.skip_renders:
    if not a.quick:
        for dressed in (True, False):
            shirt_obj.hide_render = not dressed
            body.hide_render = not dressed
            for view, (cx, cy) in VIEWS.items():
                place(cx, cy, 1.24, (0, AXIS_Y, 1.20), .80 if dressed else frame * 1.25)
                render(OUT / ('%s_%s.png' % ('clothed' if dressed else 'clean', view)),
                       (1100, 1250), not dressed)

    # 1. Inventory-style icon straight from the model, same size as ArmorIcons.
    shirt_obj.hide_render = True
    body.hide_render = True
    place(0, -2.6, focus.z, focus, frame)
    render(OUT / 'icon_large.png', (880, 864), True)
    render(OUT / 'icon.png', (110, 108), True)

    # 2. Studio beauty with the preview maps, light backdrop like the photograph.
    background.inputs[0].default_value = (.90, .90, .88, 1)
    background.inputs[1].default_value = 1.05
    for lamp in (o for o in bpy.data.objects if o.type == 'LIGHT'):
        if lamp.name == 'Key':
            lamp.data.energy = 170
        elif lamp.name == 'Fill':
            lamp.data.energy = 80
        elif lamp.name == 'Rim':
            lamp.data.energy = 55
    scene.cycles.samples = 48 if a.quick else 160
    shirt_obj.hide_render = True
    body.hide_render = True
    place(0, -2.6, focus.z, focus, frame * 1.02)
    render(OUT / 'studio_front.png', (1000, 1100) if a.quick else (1600, 1760), False)
    place(-1.55, -2.05, focus.z + .04, focus, frame * .94)
    render(OUT / 'studio_oblique.png', (1000, 1100) if a.quick else (1500, 1600), False)
    place(0, 2.6, focus.z, focus, frame * 1.02)
    render(OUT / 'studio_back.png', (1000, 1100) if a.quick else (1600, 1760), False)
    place(2.6, .05, focus.z, focus, frame * 1.02)
    render(OUT / 'studio_side.png', (1000, 1100) if a.quick else (1600, 1760), False)
    shirt_obj.hide_render = False
    body.hide_render = False
    place(-1.35, -2.15, 1.26, (0, AXIS_Y, 1.22), .76)
    render(OUT / 'studio_on_body.png', (1000, 1100) if a.quick else (1500, 1600), False)
    # Keep the older names so existing QA crops still work.
    shutil.copyfile(OUT / 'studio_oblique.png', OUT / 'beauty_oblique.png')
    shutil.copyfile(OUT / 'studio_on_body.png', OUT / 'beauty_on_body.png')
    scene.cycles.samples = 40
    background.inputs[0].default_value = (.05, .05, .055, 1)
    background.inputs[1].default_value = .5

    # 3. Geometry and topology, without material noise.
    shirt_obj.hide_render = True
    body.hide_render = True
    clay = material('QA clay', srgb(178, 178, 172), .55)
    original = [list(o.data.materials) for o in parts]
    for obj in parts:
        obj.data.materials.clear()
        obj.data.materials.append(clay)
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.light = 'STUDIO'
    scene.display.shading.color_type = 'SINGLE'
    scene.display.shading.single_color = (.72, .72, .70)
    scene.display.shading.show_object_outline = True
    scene.display.shading.show_cavity = True
    scene.display.shading.type = 'SOLID'
    geometry_views = (('oblique', (-1.85, -1.85)),) if a.quick else \
        (('front', (0, -2.6)), ('oblique', (-1.85, -1.85)))
    for view, (cx, cy) in geometry_views:
        place(cx, cy, focus.z, focus, frame)
        render(OUT / ('geometry_%s.png' % view), (900, 900), True)
    # Workbench wireframe only draws silhouettes in a background render, so the
    # topology view is real geometry from a Wireframe modifier on throwaway copies.
    wire = []
    for obj in parts:
        copy = obj.copy()
        copy.data = obj.data.copy()
        bpy.context.collection.objects.link(copy)
        bpy.ops.object.select_all(action='DESELECT')
        copy.select_set(True)
        bpy.context.view_layer.objects.active = copy
        mod = copy.modifiers.new('Topology', 'WIREFRAME')
        mod.thickness = .0013
        bpy.ops.object.modifier_apply(modifier=mod.name)
        obj.hide_render = True
        wire.append(copy)
    scene.display.shading.single_color = (.10, .10, .10)
    for view, (cx, cy) in geometry_views:
        place(cx, cy, focus.z, focus, frame)
        render(OUT / ('wireframe_%s.png' % view), (900, 900), True)
    for copy in wire:
        bpy.data.objects.remove(copy, do_unlink=True)
    for obj in parts:
        obj.hide_render = False
    scene.render.engine = 'CYCLES'
    for obj, materials in zip(parts, original):
        obj.data.materials.clear()
        for slot in materials:
            obj.data.materials.append(slot)

# ------------------------------------------------------- save the clean file
for obj in (shirt_obj, body, rig):
    bpy.data.objects.remove(obj, do_unlink=True)
for obj in list(bpy.data.objects):
    if obj.type in {'LIGHT', 'CAMERA'}:
        bpy.data.objects.remove(obj, do_unlink=True)
for obj in parts:
    assert not obj.modifiers, obj.name
    assert not obj.vertex_groups, obj.name
    assert obj.parent is None, obj.name
assert not [o for o in bpy.data.objects if o.type == 'ARMATURE']
bpy.ops.file.pack_all()
scene['asset_status'] = 'clean geometry; no rig'
scene['asset_item'] = 'JazzArmor_6B3'
scene['asset_reference'] = 'https://sbox.game/mapperskai/ar_6b3; owner front/back/side screenshots'
clean_path = OUT / 'clean' / 'JazzArmor_6B3.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(clean_path))

report = {
    'item': 'JazzArmor_6B3',
    'prototype': '6B3TM-01 (1985)',
    'stage': 'clean',
    'clean_blend': str(clean_path),
    'parts': [{'name': o.name, 'triangles': len(o.data.loop_triangles),
               'colorization': o['hg_colorization']} for o in parts],
    'triangles': triangles,
    'vertices': vertices,
    'budget': 17000,
    'reference': 'owner front/back/side screenshots; https://sbox.game/mapperskai/ar_6b3',
    'fitted_to': a.shirt.name,
    'clearance_to_shirt': fit,
    'armatures': 0,
    'vertex_groups': 0,
    'deform_modifiers': 0,
    'materials': 'preview maps in textures/; JA3 bake and colorization mask not produced yet',
    'runtime': 'NOT_RUN',
}
(OUT / 'clean-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print('TRIANGLES', triangles, 'VERTICES', vertices, 'PARTS', len(parts))
print('CLEARANCE', json.dumps(fit))
