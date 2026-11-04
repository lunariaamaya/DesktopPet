"""Reimport the delivered motion GLB and verify it genuinely animates in bpy."""
from pathlib import Path
import json,os,sys
import bpy
import numpy as np
from mathutils import Vector
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('repair',ROOT/'scripts/repair-meshy-rig.py')
repair=importlib.util.module_from_spec(spec);spec.loader.exec_module(repair)
OUT=ROOT/'tmp/meshy-repair'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.context.scene.render.fps=30
bpy.ops.import_scene.gltf(filepath=str(repair.DELIVERY/'character-weight-repair-v04-motion-check.glb'))
scene,cam=repair.configure_scene();scene.render.fps=30
arm=next(o for o in scene.objects if o.type=='ARMATURE');mesh=next(o for o in scene.objects if o.type=='MESH')
assert len(arm.data.bones)>=29
assert arm.animation_data and arm.animation_data.action
start,end=arm.animation_data.action.frame_range
frames=np.linspace(start,end,7);points=[];report={'frames':[]}
for phase,frame in enumerate(frames):
    frame=float(frame)
    scene.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update()
    points.append(repair.evaluated_points(mesh))
    report['frames'].append({'frame':frame,'time_seconds':(frame-start)/scene.render.fps})
    if phase in [1,3,5]:
        label={1:'raise-arm',3:'head-turn',5:'accessory-control'}[phase]
        repair.render(scene,cam,OUT/f'roundtrip-{label}.png','back' if phase==5 else 'front')
report['max_displacement_m']=[float(np.max(np.linalg.norm(p-points[0],axis=1))) for p in points]
assert max(report['max_displacement_m'])>.05
assert report['max_displacement_m'][-1]<1e-4
report['animation_frame_range']=list(arm.animation_data.action.frame_range)
report['bone_count']=len(arm.data.bones)
report['passed']=True
arm.animation_data_clear();repair.pose(arm,{})
rest=repair.evaluated_points(mesh)
repair.pose(arm,{'LeftForeArm':(0,65)})
posed=repair.evaluated_points(mesh)
hem=(rest[:,2]>.34)&(rest[:,2]<.60)
report['elbow_test_hem_max_m']=float(np.max(np.linalg.norm(posed[hem]-rest[hem],axis=1)))
assert report['elbow_test_hem_max_m']<1e-4,'Forearm still pulls lower skirt'
repair.render(scene,cam,OUT/'supplementary-left-elbow.png')
(OUT/'roundtrip-verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2),flush=True)
sys.stdout.flush();os._exit(0)
