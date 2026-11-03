from pathlib import Path
import json
import math
import os
import sys
import bpy

root=Path(__file__).resolve().parents[1]
folder=root/'assets/characters/first-character/models/v01'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(folder/'character-v01.glb'))
objects=[o for o in bpy.data.objects if o.type=='MESH']
assert len(objects)>0
coordinates=[o.matrix_world@v.co for o in objects for v in o.data.vertices]
assert all(math.isfinite(c) for p in coordinates for c in p)
result={'glb_reimported':True,'mesh_objects':len(objects),'vertices':len(coordinates),
        'bounds_min':[min(p[i] for p in coordinates) for i in range(3)],
        'bounds_max':[max(p[i] for p in coordinates) for i in range(3)],
        'finite_coordinates':True,'armatures':sum(o.type=='ARMATURE' for o in bpy.data.objects)}
assert result['bounds_max'][2]-result['bounds_min'][2]>1
(folder/'reimport-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
# bpy embedded runtime may return a failure during module teardown after successful work.
# Exit only after assertions and the on-disk report are complete.
sys.stdout.flush()
os._exit(0)
