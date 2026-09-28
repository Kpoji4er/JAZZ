from pathlib import Path
import subprocess,tempfile,json
root=Path.cwd();entries=subprocess.check_output(['git','ls-files','-u','-z']).split(b'\0');files={}
for e in entries:
 if not e:continue
 meta,path=e.split(b'\t',1);mode,oid,stage=meta.split();files.setdefault(path.decode(),{})[int(stage)]=oid.decode()
oids=list({oid for v in files.values() for oid in v.values()});proc=subprocess.run(['git','cat-file','--batch'],input=('\n'.join(oids)+'\n').encode(),stdout=subprocess.PIPE,check=True);buf=proc.stdout;pos=0;objects={}
for oid in oids:
 end=buf.index(b'\n',pos);size=int(buf[pos:end].split()[-1]);objects[oid]=buf[end+1:end+1+size];pos=end+size+2
resolved=[];pending=[]
with tempfile.TemporaryDirectory(prefix='jazz-merge-') as d:
 for name,stages in files.items():
  vals={k:objects[v] for k,v in stages.items()};ours=vals.get(2,b'');theirs=vals.get(3,b'');base=vals.get(1,b'')
  norm=lambda b:b.replace(b'\r\n',b'\n')
  if norm(ours)==norm(theirs):result=ours
  elif norm(base)==norm(theirs):result=ours
  elif norm(base)==norm(ours):result=theirs
  elif b'\0' in ours+theirs:pending.append(name);continue
  else:
   paths=[Path(d)/str(i) for i in range(3)]
   for p,b in zip(paths,[ours,base,theirs]):p.write_bytes(norm(b))
   res=subprocess.run(['git','merge-file','-p',*map(str,paths)],stdout=subprocess.PIPE)
   if res.returncode:pending.append(name);continue
   result=res.stdout
  (root/name).write_bytes(result);resolved.append(name)
 if resolved:subprocess.run(['git','add','--',*resolved],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print(json.dumps({'resolved':len(resolved),'pending':pending},ensure_ascii=False,indent=2))
