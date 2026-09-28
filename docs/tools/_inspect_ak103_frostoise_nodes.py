import bpy
from pathlib import Path

bpy.ops.wm.open_mainfile(filepath=str(Path(r"E:\JaWeapons\Weapons\_ak103_jazz_build\clean\AK103.blend")))
for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if not bsdf:
        print(mat.name, "no bsdf")
        continue
    print(f"=== {mat.name} ===")
    for sock in ("Base Color", "Roughness", "Metallic", "Normal"):
        links = bsdf.inputs[sock].links
        if not links:
            print(f"  {sock}: unbound")
            continue
        node = links[0].from_node
        print(f"  {sock}: {node.type} {node.name} image={getattr(node, 'image', None) and node.image.name} inputs={[i.name for i in node.inputs if i.links]}")
        for inp in node.inputs:
            if inp.links:
                src = inp.links[0].from_node
                print(f"    .{inp.name} <- {src.type} {src.name} image={getattr(src, 'image', None) and src.image.name}")
