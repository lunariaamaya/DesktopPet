"""Inspect the two user-supplied GLBs without modifying either original."""
from pathlib import Path
import hashlib,json,struct
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tmp/meshy-diagnostics'
OUT.mkdir(parents=True,exist_ok=True)

class GLB:
    def __init__(self,path):
        self.path=Path(path)
        with self.path.open('rb') as f:
            magic,version,length=struct.unpack('<4sII',f.read(12))
            assert magic==b'glTF' and version==2 and length==self.path.stat().st_size
            n,tag=struct.unpack('<I4s',f.read(8));assert tag==b'JSON'
            self.g=json.loads(f.read(n))
            n,tag=struct.unpack('<I4s',f.read(8));assert tag==b'BIN\x00'
            self.bin=f.read(n)
    def accessor(self,index):
        a=self.g['accessors'][index];v=self.g['bufferViews'][a['bufferView']]
        assert not a.get('sparse'),'Sparse accessor not implemented'
        dt=np.dtype({5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']])
        size={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
        values=np.ndarray((a['count'],size),dt,self.bin,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',dt.itemsize*size),dt.itemsize)).copy()
        if a.get('normalized') and dt.kind in 'iu':values=values.astype(float)/np.iinfo(dt).max
        return values

reports=[]
for filename in ['Anime_Cat_Girl_Model_191.glb','Rigged Anime Cat Girl HD move.glb']:
    doc=GLB(Path('C:/Users/HP/Downloads')/filename);g=doc.g
    prim=g['meshes'][0]['primitives'][0];attrs=prim['attributes']
    pos=doc.accessor(attrs['POSITION'])
    report={'file':filename,'sha256':hashlib.sha256(doc.path.read_bytes()).hexdigest(),
            'bytes':doc.path.stat().st_size,'vertices':len(pos),
            'triangles':len(doc.accessor(prim['indices']))//3,
            'mesh_count':len(g['meshes']),'primitive_count':sum(len(m['primitives']) for m in g['meshes']),
            'materials':len(g.get('materials',[])),'morph_targets':len(prim.get('targets',[])),
            'geometry_bounds':[pos.min(axis=0).tolist(),pos.max(axis=0).tolist()],
            'animations':[]}
    for animation in g.get('animations',[]):
        channels=[]
        for channel in animation['channels']:
            sampler=animation['samplers'][channel['sampler']]
            times=doc.accessor(sampler['input']).ravel();values=doc.accessor(sampler['output'])
            channels.append({'node':g['nodes'][channel['target']['node']].get('name'),'path':channel['target']['path'],
                             'keys':len(times),'time_min':float(times.min()),'time_max':float(times.max()),
                             'max_component_range':float(np.ptp(values,axis=0).max())})
        report['animations'].append({'name':animation.get('name'),'channels':channels,
                                     'effective_duration':max(c['time_max'] for c in channels)-min(c['time_min'] for c in channels)})
    if g.get('skins'):
        skin=g['skins'][0];names=[g['nodes'][i].get('name',str(i)) for i in skin['joints']]
        joints=doc.accessor(attrs['JOINTS_0']).astype(int);weights=doc.accessor(attrs['WEIGHTS_0'])
        ibm=doc.accessor(skin['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1)
        bind=np.linalg.inv(ibm)
        report['skin']={'joint_count':len(names),'joints':names,
                        'max_weight_sum_error':float(np.abs(weights.sum(axis=1)-1).max()),
                        'zero_weight_vertices':int((weights.sum(axis=1)<1e-6).sum()),
                        'invalid_joint_indices':int(((joints<0)|(joints>=len(names))).sum()),
                        'bind_joint_positions':dict(zip(names,bind[:,:3,3].tolist())),
                        'weight_per_joint':{name:float(weights[joints==i].sum()) for i,name in enumerate(names)}}
        # Explicit spatial regions are inspection aids, not semantic segmentation.
        regions={
            'rear_upper_hair_candidate':(pos[:,1]>.95)&(pos[:,1]<1.35)&(pos[:,2]<-.13),
            'rear_low_hair_candidate':(pos[:,1]>.82)&(pos[:,1]<1.1)&(pos[:,2]<-.15),
            'lower_skirt_front_candidate':(pos[:,1]>.38)&(pos[:,1]<.78)&(pos[:,2]>.12),
            'lower_skirt_rear_candidate':(pos[:,1]>.38)&(pos[:,1]<.78)&(pos[:,2]<-.12),
            'tail_left_candidate':(pos[:,0]<-.23)&(pos[:,1]>.32)&(pos[:,1]<.8)}
        report['spatial_weight_probes']={}
        for label,mask in regions.items():
            if not mask.any():continue
            totals={name:float(weights[mask][joints[mask]==i].sum()/mask.sum()) for i,name in enumerate(names)}
            report['spatial_weight_probes'][label]={'vertices':int(mask.sum()),'definition':'Manual XYZ box; may include nearby materials',
                'average_weight':dict(sorted(totals.items(),key=lambda p:p[1],reverse=True)[:8])}
        np.savez_compressed(OUT/'rig-inspection-arrays.npz',positions=pos,joints=joints,weights=weights,joint_names=np.array(names))
    reports.append(report)
(OUT/'glb-analysis.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2),encoding='utf-8')
for r in reports:
    print(json.dumps({k:v for k,v in r.items() if k not in {'skin','animations'}},ensure_ascii=False))
    if 'skin' in r:
        print(json.dumps({'weight_error':r['skin']['max_weight_sum_error'],'zero_weights':r['skin']['zero_weight_vertices'],
            'joint_positions':r['skin']['bind_joint_positions'],
            'animations':[{'name':a['name'],'channels':len(a['channels']),'effective_duration':a['effective_duration'],
                           'key_counts':sorted(set(c['keys'] for c in a['channels']))} for a in r['animations']]},ensure_ascii=False))
