from pathlib import Path
import base64
import json
import struct
import hashlib
from PIL import Image, ImageDraw

root=Path(__file__).resolve().parents[1]
folder=root/'assets/characters/first-character/models/v01'
raw=(folder/'character-v01.glb').read_bytes()
magic,version,length=struct.unpack_from('<III',raw)
assert magic==0x46546c67 and version==2 and length==len(raw)
n,kind=struct.unpack_from('<II',raw,12)
assert kind==0x4e4f534a
gltf=json.loads(raw[20:20+n])
assert gltf['asset']['version']=='2.0' and gltf.get('meshes')
assert not gltf.get('skins') and not gltf.get('animations')
template=(root/'scripts/model-viewer-template.html').read_text(encoding='utf-8')
(folder/'viewer.html').write_text(template.replace('__GLB_BASE64__',base64.b64encode(raw).decode()),encoding='utf-8')
sheet=Image.new('RGB',(1536,560),'white')
draw=ImageDraw.Draw(sheet)
for i,name in enumerate(['front','side','back','three-quarter']):
    im=Image.open(folder/f'preview-{name}.png').convert('RGBA')
    bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im)
    image=bg.convert('RGB').resize((384,512),Image.Resampling.LANCZOS)
    # Preserve aspect ratio: each tile is 384x512, never squeeze the render.
    sheet.paste(image,(384*i,40))
    draw.text((384*i+15,15),name,fill='#6a5d79')
sheet.save(folder/'preview-sheet.png')
report={'glb_header_valid':True,'mesh_count':len(gltf['meshes']),
        'node_count':len(gltf['nodes']),'material_count':len(gltf.get('materials',[])),
        'animations':len(gltf.get('animations',[])),'skins':len(gltf.get('skins',[])),
        'glb_bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
        'standalone_viewer':'viewer.html','external_viewer_dependencies':False,
        'validation_limit':'structural header/schema checks, not full Khronos validator'}
(folder/'file-validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
