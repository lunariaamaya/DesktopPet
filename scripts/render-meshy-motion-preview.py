"""Render the actual repaired GLB, front/back synchronously, without editing it.

Stage 1 (isolated bpy): PNG frames; stage 2 (Pillow): labeled GIF;
stage 3 (isolated bpy): encode the labeled frames to H.264 MP4 using VSE.
"""
from pathlib import Path
import argparse,hashlib,json,os,sys

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/'exports/meshy-repair-v04/character-weight-repair-v04-motion-check.glb'
FRAMES=ROOT/'tmp/meshy-motion-preview-2026-11-07'
OUT=ROOT/'assets/characters/first-character/diagnostics/meshy-motion-preview-2026-11-07'

def render():
    import bpy
    from mathutils import Vector
    import importlib.util,math
    spec=importlib.util.spec_from_file_location('repair',ROOT/'scripts/repair-meshy-rig.py')
    repair=importlib.util.module_from_spec(spec);spec.loader.exec_module(repair)
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    bpy.context.scene.render.fps=30
    bpy.ops.import_scene.gltf(filepath=str(MODEL))
    arm=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
    mesh=next(o for o in bpy.context.scene.objects if o.type=='MESH')
    assert arm.animation_data and arm.animation_data.action
    # Put a front and a back copy beside one another, sharing the actual clip.
    back_arm=arm.copy();back_arm.data=arm.data.copy();bpy.context.scene.collection.objects.link(back_arm)
    back_mesh=mesh.copy();bpy.context.scene.collection.objects.link(back_mesh)
    back_mesh.parent=back_arm
    for modifier in back_mesh.modifiers:
        if modifier.type=='ARMATURE':modifier.object=back_arm
    arm.location.x-=.55
    # Keep the imported quaternion animation untouched; rotate an outer parent.
    back_parent=bpy.data.objects.new('Back view placement',None);bpy.context.scene.collection.objects.link(back_parent)
    back_arm.parent=back_parent;back_parent.location.x=.55;back_parent.rotation_euler.z=math.pi
    scene,cam=repair.configure_scene()
    cam.location=(0,-5,.88);cam.rotation_euler=(Vector((0,0,.83))-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.ortho_scale=2.75
    # Orthographic scale is horizontal for this landscape render.
    scene.render.resolution_x=720;scene.render.resolution_y=480
    scene.cycles.samples=3;scene.render.fps=30
    start,end=arm.animation_data.action.frame_range
    assert abs((end-start)/30-3)<.01
    FRAMES.mkdir(parents=True,exist_ok=True)
    for frame in range(round(start),round(end)+1,2):
        scene.frame_set(frame)
        scene.render.filepath=str(FRAMES/f'raw-{frame:03}.png')
        bpy.ops.render.render(write_still=True)
        print('PREVIEW_FRAME',frame,flush=True)
    (FRAMES/'source.json').write_text(json.dumps({'model':str(MODEL),'sha256':hashlib.sha256(MODEL.read_bytes()).hexdigest(),
        'animation_source_seconds':3,'preview_fps':8,'sampled_frames':list(range(round(start),round(end)+1,2)),
        'note':'Actual exported GLB clip, front and back simultaneously; slowed playback. No new rig edits.'},indent=2))

def label():
    from PIL import Image,ImageDraw,ImageFont
    OUT.mkdir(parents=True,exist_ok=True)
    files=sorted(FRAMES.glob('raw-*.png'));assert len(files)==46
    title=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
    font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',18)
    frames=[]
    for index,path in enumerate(files):
        im=Image.open(path).convert('RGB');c=Image.new('RGB',(720,580),'#f4f5f7');c.paste(im,(0,58))
        d=ImageDraw.Draw(c);d.text((205,16),'正面',font=title,fill='#17212e');d.text((485,16),'背面',font=title,fill='#17212e')
        actual_frame=int(path.stem.split('-')[-1]);phase='抬手 → 复位' if actual_frame<=31 else '转头 → 复位' if actual_frame<=61 else '尾饰、发梢控制 → 复位'
        d.text((18,540),phase+'  ·  慢速检查',font=font,fill='#17212e')
        d.text((18,562),'试修版：袖口、裙摆自然运动与碰撞仍待完善',font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',13),fill='#46546a')
        c.save(FRAMES/f'labeled-{index:03}.png');frames.append(c)
    frames[8].save(OUT/'poster.png')
    palette=frames[0].quantize(colors=256)
    frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    # GIF time units are 10ms: alternate 120/130ms to average exactly 8 fps.
    durations=[120 if i%2==0 else 130 for i in range(len(frames))]
    frames[0].save(OUT/'motion-preview.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=False,disposal=2)
    (OUT/'preview-source.json').write_text((FRAMES/'source.json').read_text())

def encode():
    import bpy
    scene=bpy.data.scenes.new('Encoded preview')
    scene.render.resolution_x=720;scene.render.resolution_y=580;scene.render.resolution_percentage=100
    scene.render.fps=8;scene.frame_start=1;scene.frame_end=46
    editor=scene.sequence_editor_create();files=sorted(FRAMES.glob('labeled-*.png'));assert len(files)==46
    strip=editor.sequences.new_image('Rendered actual motion',str(files[0]),channel=1,frame_start=1)
    for path in files[1:]:strip.elements.append(path.name)
    strip.colorspace_settings.name='sRGB'
    scene.view_settings.view_transform='Standard';scene.render.image_settings.file_format='FFMPEG'
    scene.render.ffmpeg.format='MPEG4';scene.render.ffmpeg.codec='H264';scene.render.ffmpeg.constant_rate_factor='HIGH'
    scene.render.ffmpeg.audio_codec='NONE';scene.render.filepath=str(OUT/'motion-preview.mp4')
    bpy.ops.render.render(animation=True,scene=scene.name)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['render','label','encode']);args=parser.parse_args()
    {'render':render,'label':label,'encode':encode}[args.stage]()
    sys.stdout.flush();os._exit(0)
