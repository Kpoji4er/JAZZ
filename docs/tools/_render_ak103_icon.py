"""Inventory icon for AK-103, matching the accepted WeaponIcons/AK74.png style.

    blender --background --factory-startup --python docs/tools/_render_ak103_icon.py -- \
        --build <_ak103_jazz_build> [--samples 64]

324x165 with the muzzle to the right, like AK74.png and AKM.png. The outline is
deliberately heavier than _render_ak_icons.py: that script used a single
DilateErode at distance 2 and produced the thin-contour 512x256 icons
(AK74M/AK105/SR3M) the owner rejected. Here a solid ring is layered over a
blurred halo so the weapon still reads against a light inventory slot.

Cycles on CPU, one Blender instance.
"""

import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ICON = (324, 165)
COMPONENT_ICON = (100, 100)
OUTLINE = (0.006, 0.005, 0.004, 1.0)
RING_DISTANCE = 4
HALO_DISTANCE = 9
HALO_BLUR = 7
HALO_STRENGTH = 0.6


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument("--build", required=True, type=Path)
    p.add_argument("--samples", type=int, default=64)
    return p.parse_args(argv)


def build_compositor(scene):
    scene.use_nodes = True
    nodes = scene.node_tree.nodes
    nodes.clear()
    link = scene.node_tree.links.new

    layers = nodes.new("CompositorNodeRLayers")

    halo = nodes.new("CompositorNodeDilateErode")
    halo.mode = "DISTANCE"
    halo.distance = HALO_DISTANCE
    link(layers.outputs["Alpha"], halo.inputs[0])
    blur = nodes.new("CompositorNodeBlur")
    blur.filter_type = "GAUSS"
    blur.size_x = HALO_BLUR
    blur.size_y = HALO_BLUR
    blur.use_relative = False
    link(halo.outputs[0], blur.inputs[0])
    fade = nodes.new("CompositorNodeMixRGB")
    fade.blend_type = "MULTIPLY"
    fade.inputs[0].default_value = 1.0
    fade.inputs[2].default_value = (HALO_STRENGTH,) * 3 + (1.0,)
    link(blur.outputs[0], fade.inputs[1])
    halo_rgba = nodes.new("CompositorNodeSetAlpha")
    halo_rgba.inputs["Image"].default_value = OUTLINE
    link(fade.outputs[0], halo_rgba.inputs["Alpha"])

    ring = nodes.new("CompositorNodeDilateErode")
    ring.mode = "DISTANCE"
    ring.distance = RING_DISTANCE
    link(layers.outputs["Alpha"], ring.inputs[0])
    ring_rgba = nodes.new("CompositorNodeSetAlpha")
    ring_rgba.inputs["Image"].default_value = OUTLINE
    link(ring.outputs[0], ring_rgba.inputs["Alpha"])

    over_ring = nodes.new("CompositorNodeAlphaOver")
    over_ring.inputs[0].default_value = 1
    link(halo_rgba.outputs[0], over_ring.inputs[1])
    link(ring_rgba.outputs[0], over_ring.inputs[2])

    over_weapon = nodes.new("CompositorNodeAlphaOver")
    over_weapon.inputs[0].default_value = 1
    link(over_ring.outputs[0], over_weapon.inputs[1])
    link(layers.outputs["Image"], over_weapon.inputs[2])

    composite = nodes.new("CompositorNodeComposite")
    link(over_weapon.outputs[0], composite.inputs[0])
    return {"ring": ring, "halo": halo, "blur": blur}


def main():
    args = parse_args()
    build = args.build
    bpy.ops.wm.open_mainfile(filepath=str(build / "rigged/AK103_JA3.blend"))

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = args.samples
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.resolution_percentage = 100
    # AgX lifts the near-black outline to grey and washes the textures out;
    # the accepted icons are rendered straight.
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"

    cam_data = bpy.data.cameras.new("InventoryCamera")
    cam_data.type = "ORTHO"
    camera = bpy.data.objects.new(cam_data.name, cam_data)
    scene.collection.objects.link(camera)
    scene.camera = camera

    lights = []
    for index, offset in enumerate([(-1, -0.5, 1.5), (-0.5, 0.5, 1), (1, 1, 0)]):
        data = bpy.data.lights.new("InventoryLight" + str(index), "AREA")
        data.energy = 25
        data.size = 1.5
        obj = bpy.data.objects.new(data.name, data)
        scene.collection.objects.link(obj)
        lights.append((obj, Vector(offset)))

    nodes = build_compositor(scene)

    renders = {}
    targets = [
        ("AK103", ICON, RING_DISTANCE, HALO_DISTANCE, HALO_BLUR),
        ("AK103_Magazine", COMPONENT_ICON, 2, 5, 4),
    ]
    for name, (width, height), ring, halo, blur in targets:
        component = name.endswith("_Magazine")
        entity = "AKR_" + name
        for obj in (o for o in scene.objects if o.type == "MESH"):
            obj.hide_render = obj.name.endswith("_StockFolded") or (
                component and obj.name != entity
            )
        scene.render.resolution_x = width
        scene.render.resolution_y = height
        nodes["ring"].distance = ring
        nodes["halo"].distance = halo
        nodes["blur"].size_x = blur
        nodes["blur"].size_y = blur
        bpy.context.view_layer.update()

        visible = [o for o in scene.objects if o.type == "MESH" and not o.hide_render]
        points = [o.matrix_world @ Vector(v) for o in visible for v in o.bound_box]
        lo = Vector(tuple(min(p[i] for p in points) for i in range(3)))
        hi = Vector(tuple(max(p[i] for p in points) for i in range(3)))
        target = (lo + hi) / 2
        aspect = width / height
        # The halo grows the alpha by about halo+blur pixels per side. Solve for
        # the framing that leaves the finished icon at ~92% of the width, which
        # is what AK74.png and AKM.png measure.
        bleed = 2 * (halo + blur)
        margin = width / (0.92 * width - bleed)
        cam_data.ortho_scale = max(hi.y - lo.y, (hi.z - lo.z) * aspect) * margin

        # -X puts the muzzle on the right, as on AK74.png
        camera.location = target + Vector((-2, 0.04, 0.25))
        camera.rotation_euler = (
            (target - camera.location).to_track_quat("-Z", "Y").to_euler()
        )
        for light, offset in lights:
            light.location = target + offset
            light.rotation_euler = (
                (target - light.location).to_track_quat("-Z", "Y").to_euler()
            )

        path = build / f"{name}_icon.png"
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        renders[name] = {"path": str(path), "size": [width, height]}

    bpy.ops.wm.save_as_mainfile(filepath=str(build / "rigged/AK103_JA3_icons.blend"))
    (build / "icon-report.json").write_text(
        json.dumps(renders, indent=2), encoding="utf-8"
    )
    print(json.dumps(renders, indent=2))


if __name__ == "__main__":
    main()
