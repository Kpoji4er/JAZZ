// Geometry-only QA bridge using the MIT-licensed mxtsdev/hgm-viewer parser.
// Raw HGM coordinates are preserved; no claim of animation/material round-trip.
using HgmViewer.Formats;
using System.Text.Json;
using static HgmViewer.Formats.Hgm.Mesh;
if(args.Length!=2)throw new ArgumentException("input.hgm output.json");
var hgm=Hgm.FromFile(args[0]);hgm._read();
var meshes=new List<object>();
foreach(var mesh in hgm.Meshes){
 var b=(mesh.Bbox??hgm.Header.Bbox).Values;
 var scale=Math.Max(1f,Enumerable.Range(0,3).Select(i=>Math.Abs(b[i+3]-b[i])).Max()/2f);
 var pf=mesh.GetFieldByName("pos");var bi=mesh.GetFieldByName("bi");var bw=mesh.GetFieldByName("bw");
 var verts=mesh.Vertices.Select(v=>((VertexFieldSint16)v.Fields[pf.Index]).Values.Select(x=>x/32767f*scale).ToArray()).ToArray();
 var indices=bi==null?null:mesh.Vertices.Select(v=>((VertexFieldUint8)v.Fields[bi.Index]).Values.Select(x=>(int)x).ToArray()).ToArray();
 var weights=bw==null?null:mesh.Vertices.Select(v=>((VertexFieldUnorm8)v.Fields[bw.Index]).Values.Select(w=>w/255f).ToArray()).ToArray();
 meshes.Add(new {vertices=verts,faces=mesh.Faces.Face.Select(f=>new[]{f.F1,f.F2,f.F3}),bone_indices=indices,bone_weights=weights,bbox=b,material_index=mesh.MaterialIndex});
}
var bones=hgm.Armature?.Bones.Select(b=>new {name=b.Name.Str,index=b.GroupIndex}).ToArray();
var result=new {source=Path.GetFileName(args[0]),version=hgm.Header.Version,bbox=hgm.Header.Bbox.Values,bones,meshes};
Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(args[1]))!);
File.WriteAllText(args[1],JsonSerializer.Serialize(result));
Console.WriteLine($"{Path.GetFileName(args[0])}: {hgm.Meshes.Count} meshes, {hgm.Meshes.Sum(m=>m.Vertices.Count)} vertices");
