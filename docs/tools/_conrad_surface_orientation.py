"""Restore author-facing triangles after recalc of separated open character parts.
UV corner identity survives welding, skin transfer and coordinate changes.
No custom normals; texture coordinates, positions and weights remain unchanged.
"""
import bmesh
from _ja3_mesh_prepare import prepare_export_mesh

def uv_winding(obj):
    uv=obj.data.uv_layers.active.data
    result={}
    for face in obj.data.polygons:
        pts=[tuple(round(x,6) for x in uv[i].uv) for i in face.loop_indices]
        assert len(pts)==3
        area=sum(pts[i][0]*pts[(i+1)%3][1]-pts[(i+1)%3][0]*pts[i][1] for i in range(3))
        key=tuple(sorted(pts))
        assert key not in result,'Ambiguous UV triangle'
        result[key]=area
    return result

def prepare_author_facing(obj, reference):
    prepare_export_mesh(obj)
    bm=bmesh.new();bm.from_mesh(obj.data)
    uv=bm.loops.layers.uv.active
    flipped=0
    for face in bm.faces:
        pts=[tuple(round(x,6) for x in l[uv].uv) for l in face.loops]
        key=tuple(sorted(pts));assert key in reference
        signed=sum(pts[i][0]*pts[(i+1)%3][1]-pts[(i+1)%3][0]*pts[i][1] for i in range(3))
        assert abs(signed)>1e-12 and abs(reference[key])>1e-12,'Degenerate UV face'
        if signed*reference[key]<0:
            face.normal_flip();flipped+=1
    bm.normal_update();bm.to_mesh(obj.data);bm.free()
    obj.data.update()
    actual=uv_winding(obj)
    assert all(value*reference[key]>0 for key,value in actual.items())
    assert not obj.data.has_custom_normals
    return flipped
