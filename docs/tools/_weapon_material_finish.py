"""Approved VZ58/R4 tangent normal amplitude and metal finish, no base-color edit."""
import numpy as np

def separate_hard_edges(obj):
    """Separate >60-degree joins, including opposing sheets with cancelling normals.

    Drops only near-collinear submicron slivers that the native FBX optimizer
    turns into zero normals; all remaining corner positions/UVs are untouched.
    """
    import bpy,bmesh,math
    bm=bmesh.new();bm.from_mesh(obj.data)
    slivers=[]
    for f in bm.faces:
        area=f.calc_area();longest=max((e.calc_length() for e in f.edges),default=0)
        if longest and area<1e-8 and area/(longest*longest)<1e-4:slivers.append(f)
    assert len(slivers)<10,('Unexpected sliver count',len(slivers))
    report={'removed_submicron_faces':len(slivers),'removed_area_m2':sum(f.calc_area() for f in slivers)}
    bmesh.ops.delete(bm,geom=slivers,context='FACES_ONLY')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(obj.data);bm.free()
    bpy.ops.object.select_all(action='DESELECT');obj.select_set(True)
    bpy.context.view_layer.objects.active=obj
    mod=obj.modifiers.new('Mechanical hard edges','EDGE_SPLIT')
    mod.split_angle=math.radians(60);mod.use_edge_angle=True;mod.use_edge_sharp=False
    bpy.ops.object.modifier_apply(modifier=mod.name)
    assert not obj.data.has_custom_normals
    return report

def finish_material(normal,rm,family,key):
    normal=normal.copy();rm=rm.copy();metal=rm[:,:,2]>.5
    strength=np.full(metal.shape,.22 if family=='r4' or key=='Steel' else .30,np.float32)
    if key in ('Wood','StockWood'):strength[~metal]=.08
    elif family=='r4':strength[~metal]=.45
    xyz=normal[:,:,:3]*2-1
    xyz[:,:,:2]*=strength[:,:,None]
    xyz[:,:,2]=1+(xyz[:,:,2]-1)*strength
    xyz/=np.maximum(np.linalg.norm(xyz,axis=2,keepdims=True),1e-8)
    normal[:,:,:3]=(xyz+1)/2
    before=float(rm[:,:,0][metal].mean()) if metal.any() else 0
    rm[:,:,0][metal]=np.maximum(rm[:,:,0][metal],.62 if family=='r4' else .66)
    rm[:,:,1]=rm[:,:,0]  # JA3: roughness in both R and G, metallic in B.
    report={'normal_strength_metal':float(strength[metal].mean()) if metal.any() else 0,
            'roughness_before':before,'roughness_after':float(rm[:,:,0][metal].mean()) if metal.any() else 0}
    return normal,rm,report
