import bpy,math
from pathlib import Path
from mathutils import Matrix,Vector
import argparse,sys
parser=argparse.ArgumentParser()
parser.add_argument('--build',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=args.build
base=out
configs=[
 ('AK74','AK74Pack',1, 'Y',[(10,'body'),(17,'furniture_1'),(20,'AK-74_polymer_furniture'),(14,'AK-74_polymer_furniture'),(12,'AK-74_mag_bak30rds')]),
 ('AKM','AKM',.01,'-Z',[(0,'AKM_furniture'),(1,'AKM_body'),(2,'AK-74_mag_bak30rds')]),
 ('AK105','AK105',.0037,'-Z',[(0,'barrel_mag_stock_tex_stock_1'),(1,'AK105_Main'),(2,'barrel_mag_stock_tex_barrel_mat1'),(3,'barrel_mag_stock_tex_magazine_mat1')]),
 ('AK74M','AK74M',1,'-Z',[(0,'ak_74m_texture_Yellow'),(1,'ak_74m_texture_Red')]),
]
for name,folder,scale,axis,parts in configs:
    bpy.ops.wm.read_factory_settings(use_empty=True);src=base/folder/'source';mats={};meshes=[]
    for idx,prefix in parts:
        bpy.ops.wm.obj_import(filepath=str(src/f'model_{idx}.obj'));o=bpy.context.object;o.name=name+'_'+str(idx)
        if name=='AK74M':
            # Keep the assembled specimen; source also contains an exploded copy.
            import bmesh
            bm=bmesh.new();bm.from_mesh(o.data)
            bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.co.x>.2],context='VERTS');bm.to_mesh(o.data);bm.free()
        r=Matrix.Rotation(math.pi,4,'Z')
        if axis=='-Z':r=r@Matrix.Rotation(math.pi/2,4,'X')
        o.data.transform(r@Matrix.Scale(scale,4));o.matrix_world=Matrix.Identity(4)
        if prefix not in mats:
            mat=bpy.data.materials.new(prefix);mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;p=n.get('Principled BSDF')
            for key,tokens in [('Base Color',['Albedo','BaseColor','BaseCol','base_color']),('Roughness',['Roughness','Roughne','roughness']),('Metallic',['Metalness','Metallic','Metalli','metallic']),('Normal',['Normal','normal'])]:
                paths=[f for f in src.glob(prefix+'*') if any(('_'+t) in f.name for t in tokens)]
                if not paths:continue
                t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(paths[0]))
                if key!='Base Color':t.image.colorspace_settings.name='Non-Color'
                if key=='Normal':
                    normal=n.new('ShaderNodeNormalMap');l.new(t.outputs[0],normal.inputs[1]);l.new(normal.outputs[0],p.inputs[key])
                else:l.new(t.outputs[0],p.inputs[key])
            mats[prefix]=mat
        o.data.materials.clear();o.data.materials.append(mats[prefix]);meshes.append(o)
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.render.resolution_x=1200;s.render.resolution_y=500;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA'
    points=[v.co for o in meshes for v in o.data.vertices];lo=Vector(tuple(min(p[i] for p in points) for i in range(3)));hi=Vector(tuple(max(p[i] for p in points) for i in range(3)));target=(lo+hi)/2
    d=bpy.data.cameras.new('Review');c=bpy.data.objects.new('Review',d);s.collection.objects.link(c);c.location=target+Vector((-2,.04,.25));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=max(hi.y-lo.y,(hi.z-lo.z)*2.4)*1.1;s.camera=c
    for i,offset in enumerate([(-1,-.5,1.5),(-.5,.5,1),(1,1,0)]):
        d=bpy.data.lights.new('Light'+str(i),'AREA');d.energy=85;d.size=1.5;o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);o.location=target+Vector(offset);o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
    s.render.filepath=str(base/(name+'_review.png'));bpy.ops.wm.save_as_mainfile(filepath=str(base/(name+'_review.blend')));bpy.ops.render.render(write_still=True)
