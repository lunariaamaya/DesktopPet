"""Independent GLB checks for the first character's trial repair.

Checks geometry/UV/image preservation, skin validity and actual motion tracks.
Does not establish aesthetic quality, collision safety or game readiness.
"""
from pathlib import Path
import hashlib, io, json, struct
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path('C:/Users/HP/Downloads/Rigged Anime Cat Girl HD move.glb')
DELIVERY=ROOT/'exports/meshy-repair-v04'

class Document:
    def __init__(self,path):
        self.path=Path(path)
        with self.path.open('rb') as f:
            magic,version,length=struct.unpack('<4sII',f.read(12))
            assert magic==b'glTF' and version==2 and length==self.path.stat().st_size
            size,tag=struct.unpack('<I4s',f.read(8));assert tag==b'JSON';self.g=json.loads(f.read(size))
            size,tag=struct.unpack('<I4s',f.read(8));assert tag==b'BIN\x00';self.buf=f.read(size)
    def accessor(self,index):
        a=self.g['accessors'][index];v=self.g['bufferViews'][a['bufferView']]
        dtype=np.dtype({5121:'u1',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']])
        size={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']]
        assert not a.get('sparse')
        values=np.ndarray((a['count'],size),dtype,self.buf,
            offset=a.get('byteOffset',0)+v.get('byteOffset',0),
            strides=(v.get('byteStride',dtype.itemsize*size),dtype.itemsize)).copy()
        if a.get('normalized'):values=values.astype(float)/np.iinfo(dtype).max
        return values
    def image(self,index):
        image=self.g['images'][index];v=self.g['bufferViews'][image['bufferView']]
        return np.array(Image.open(io.BytesIO(self.buf[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']])).convert('RGBA'))
    def primitive(self):return self.g['meshes'][0]['primitives'][0]

def check_geometry_uv(original, positions, original_uv, uv):
    # Vertex order/count can change at tangent seams. Matching rounded sorted
    # rows is unsafe near quantization boundaries, so check actual distances.
    from itertools import product
    grid={};cell=1e-4;tolerance=2e-6
    for i,key in enumerate(np.floor(original/cell).astype(np.int32)):
        grid.setdefault(tuple(key),[]).append(i)
    max_error=0.;max_uv_error=0.
    offsets=list(product([-1,0,1],repeat=3))
    for point,tex,key in zip(positions,uv,np.floor(positions/cell).astype(np.int32)):
        candidates=grid.get(tuple(key),[])
        if not candidates or np.min(np.linalg.norm(original[candidates]-point,axis=1))>tolerance:
            candidates=[i for delta in offsets for i in grid.get(tuple(key+delta),[])]
        assert candidates,'Exported vertex has no nearby original vertex'
        distance=np.linalg.norm(original[candidates]-point,axis=1)
        near=np.asarray(candidates)[distance<tolerance]
        assert len(near),'Exported vertex position changed'
        uv_distance=np.linalg.norm(original_uv[near]-tex,axis=1)
        assert uv_distance.min()<tolerance,'Exported UV changed'
        max_error=max(max_error,float(distance.min()));max_uv_error=max(max_uv_error,float(uv_distance.min()))
    return max_error,max_uv_error

def main():
    source=Document(SOURCE);sp=source.primitive();report={}
    for name in ['character-weight-repair-v04.glb','character-weight-repair-v04-motion-check.glb']:
        doc=Document(DELIVERY/name);p=doc.primitive();g=doc.g
        original=source.accessor(sp['attributes']['POSITION']);positions=doc.accessor(p['attributes']['POSITION'])
        # glTF exporter can redistribute a uniform Armature scale into mesh coords.
        scale=float(np.ptp(original,axis=0).max()/np.ptp(positions,axis=0).max())
        assert abs(scale-1)<2e-6,'Unexpected model rescaling'
        error,uv_error=check_geometry_uv(original,positions,
            source.accessor(sp['attributes']['TEXCOORD_0']),doc.accessor(p['attributes']['TEXCOORD_0']))
        skin=g['skins'][0];j=doc.accessor(p['attributes']['JOINTS_0']);w=doc.accessor(p['attributes']['WEIGHTS_0'])
        assert (j>=0).all() and (j<len(skin['joints'])).all()
        assert np.isfinite(w).all() and (w>=0).all() and np.max(abs(w.sum(1)-1))<1e-5
        assert len(doc.accessor(p['indices']))==len(source.accessor(sp['indices'])),'Triangle count changed'
        material=g['materials'][p['material']]['pbrMetallicRoughness']
        original_material=source.g['materials'][sp['material']]['pbrMetallicRoughness']
        images={}
        for channel in ['baseColorTexture','metallicRoughnessTexture']:
            i=g['textures'][material[channel]['index']]['source'];si=source.g['textures'][original_material[channel]['index']]['source']
            images[channel]=bool(np.array_equal(doc.image(i),source.image(si)))
            assert images[channel],f'Texture pixels changed: {channel}'
        animations=[]
        for clip in g.get('animations',[]):
            tracks=[]
            for s in clip['samplers']:
                times=doc.accessor(s['input']).ravel();values=doc.accessor(s['output'])
                tracks.append({'keys':len(times),'duration':float(times.max()-times.min()),'variation':float(np.ptp(values,axis=0).max())})
            animations.append({'name':clip.get('name'),'max_duration':max(t['duration'] for t in tracks),
                               'varying_tracks':sum(t['variation']>1e-5 for t in tracks)})
        if 'motion-check' in name:assert animations and animations[0]['max_duration']>=2.99 and animations[0]['varying_tracks']>=5
        else:assert not animations
        report[name]={'sha256':hashlib.sha256(doc.path.read_bytes()).hexdigest(),'bytes':doc.path.stat().st_size,
            'triangles':len(doc.accessor(p['indices']))//3,'vertices':len(positions),'position_scale_ratio':scale,
            'geometry_preserved':True,'uv_preserved':True,'max_vertex_nearest_error_m':error,
            'max_uv_nearest_error':uv_error,'textures_identical_pixels':images,
            'joint_count':len(skin['joints']),'max_weight_sum_error':float(np.max(abs(w.sum(1)-1))),
            'animations':animations}
    original_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert original_hash=='55a81668a5eaced8b16f3c0d4188f6bf6f78ebc3014e90e4688bf4c5afe71ab0'
    report['original_unchanged']=True
    (ROOT/'tmp/meshy-repair/verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
