"""Run the HG Blender Exporter on one object without opening Blender's UI.

`hge.export_dialog` collects its mesh list in `invoke()` and switches workspaces, so
in background mode the object flags are set here and the workspace switch is stubbed
out. Everything else (FBX naming conventions, AssetsProcessor invocation) stays with
the official exporter.

Usage:
    blender -b <source>.blend -P export_character_element.py -- --object <name>
"""
import argparse
import os
import sys

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--object", required=True)
    return parser.parse_args(argv)


def find_exporter_module():
    for module in sys.modules.values():
        if module is not None and getattr(module, "__name__", "") == "BlenderExport":
            return module
    raise SystemExit("HG Blender Exporter is not loaded; enable it in Blender preferences")


class NullWorkspace:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False


def main():
    args = parse_args()
    exporter = find_exporter_module()
    exporter.WorkspaceContext = NullWorkspace

    target = bpy.data.objects.get(args.object)
    if not target:
        raise SystemExit(f"object {args.object!r} not found")

    errors = target.hge_obj_settings.get_errors()
    if errors:
        raise SystemExit(f"HGE validation failed for {target.name}: {errors}")

    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            obj.hge_export = obj is target
    bpy.context.view_layer.objects.active = target
    target.select_set(True)

    print(f"[JAZZ] exporting {target.hge_obj_settings.get_hge_name()}")
    result = bpy.ops.hge.export_dialog("EXEC_DEFAULT")
    if "FINISHED" not in result:
        raise SystemExit(f"exporter returned {result}")

    fbx_dir = os.path.join(os.getenv("APPDATA"), "Jagged Alliance 3", "ModAssets", "FBX")
    fbx = os.path.join(fbx_dir, os.path.splitext(os.path.basename(bpy.data.filepath))[0] + ".fbx")
    print(f"[JAZZ] fbx: {fbx} exists={os.path.isfile(fbx)}")


main()
