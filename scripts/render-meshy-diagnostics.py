"""Read-only GLB pose inspection using the project's isolated bpy runtime."""
from pathlib import Path
import bpy, json, os, sys, math
import numpy as np
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tmp/meshy-diagnostics'
OUT.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.samples=8
scene.cycles.use_denoising=True
scene.render.resolution_x=640
scene.render.resolution_y=800
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
scene.view_settings.view_transform='Standard'
reports=[]

def present():
    meshes=[o for o in scene.objects if o.type=='MESH']
    deps=bpy.context.evaluated_depsgraph_get()
    coords=[]
    for o in meshes:
        obj=o.evaluated_get(deps)
        mesh=obj.to_mesh()
        points=np.empty(len(mesh.vertices)*3,dtype=np.float32)
        mesh.vertices.foreach_get('co',points)
        points=points.reshape(-1,3)
        matrix=np.array(obj.matrix_world)
        points=points@matrix[:3,:3].T+matrix[:3,3]
        coords.extend([Vector(points.min(axis=0)),Vector(points.max(axis=0))])
        obj.to_mesh_clear()
    low=Vector(tuple(min(p[i] for p in coords) for i in range(3)))
    high=Vector(tuple(max(p[i] for p in coords) for i in range(3)))
    center=(low+high)/2; height=high.z-low.z
    data=bpy.data.cameras.new('diagnostic_camera');cam=bpy.data.objects.new('diagnostic_camera',data)
    scene.collection.objects.link(cam)
    cam.location=center+Vector((0,-height*3,.05*height))
    cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
    data.type='ORTHO';data.ortho_scale=max(height*1.18,(high.x-low.x)*1.45)
    scene.camera=cam
    for name,offset,power in [('key',(-2,-3,4),150),('fill',(3,-2,2),80)]:
        ld=bpy.data.lights.new(name,'AREA');ld.energy=power*height**2;ld.size=height*2
        light=bpy.data.objects.new(name,ld);scene.collection.objects.link(light)
        light.location=center+Vector(offset)*height
        light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
    return cam,center,height

for label,filename in [('static','Anime_Cat_Girl_Model_191.glb'),('rigged','Rigged Anime Cat Girl HD move.glb')]:
    if '--rig-only' in sys.argv and label=='static':continue
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(Path('C:/Users/HP/Downloads')/filename))
    meshes=[o for o in scene.objects if o.type=='MESH']
    armatures=[o for o in scene.objects if o.type=='ARMATURE']
    report={'file':filename,'meshes':[{'name':o.name,'vertices':len(o.data.vertices),'polygons':len(o.data.polygons)} for o in meshes],
            'armatures':[{'name':a.name,'bones':[{'name':b.name,'head':list(a.matrix_world@b.head_local),'tail':list(a.matrix_world@b.tail_local)} for b in a.data.bones]} for a in armatures]}
    if not armatures:
        cam,center,height=present()
        scene.render.filepath=str(OUT/'static-front.png');bpy.ops.render.render(write_still=True)
        cam.location=center+Vector((height*2,-height*3,height*.3));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(OUT/'static-three-quarter.png');bpy.ops.render.render(write_still=True)
    else:
        a=armatures[0]
        action=a.animation_data.action if a.animation_data else None
        report['action']={'name':action.name,'frame_range':list(action.frame_range)} if action else None
        a.data.pose_position='REST'
        cam,center,height=present()
        cam.location=(0,-6,.88)
        cam.rotation_euler=(Vector((0,0,.83))-cam.location).to_track_quat('-Z','Y').to_euler()
        cam.data.ortho_scale=2.0
        scene.render.filepath=str(OUT/'rigged-rest-front.png');bpy.ops.render.render(write_still=True)
        a.data.pose_position='POSE'
        start,end=action.frame_range
        scene.frame_set(int(start),subframe=start-int(start))
        scene.render.filepath=str(OUT/'supplied-animation-pose.png');bpy.ops.render.render(write_still=True)
        # Controlled probes are NOT frames from the user's original animation.
        a.animation_data_clear()
        for bone_name,axis,angle,label_test in [('Head',1,35,'head-turn'),('LeftForeArm',0,65,'left-elbow'),('LeftLeg',0,55,'left-knee'),('RightArm',0,60,'right-upper-arm'),('LeftUpLeg',0,50,'left-thigh')]:
            for b in a.pose.bones:b.matrix_basis.identity()
            b=a.pose.bones[bone_name];b.rotation_mode='XYZ';b.rotation_euler[axis]=math.radians(angle)
            scene.frame_set(1);bpy.context.view_layer.update()
            scene.render.filepath=str(OUT/f'probe-{label_test}.png');bpy.ops.render.render(write_still=True)
        for b in a.pose.bones:b.matrix_basis.identity()
        a.data.pose_position='REST'
        colors={'head':(.15,.4,1,1),'arm':(1,.08,.08,1),'hand':(1,.5,.04,1),'leg':(.08,.8,.25,1),'other':(.65,.65,.65,1)}
        for mesh in meshes:
            attr=mesh.data.color_attributes.new(name='DiagnosticWeight',type='FLOAT_COLOR',domain='POINT')
            data=[]
            for vertex in mesh.data.vertices:
                group=max(vertex.groups,key=lambda g:g.weight) if vertex.groups else None
                name=mesh.vertex_groups[group.group].name if group else ''
                category='head' if name in ['Head','neck','head_end','headfront'] else 'hand' if 'Hand' in name else 'arm' if any(x in name for x in ['Arm','Shoulder']) else 'leg' if any(x in name for x in ['Leg','Foot','Toe']) else 'other'
                data.extend(colors[category])
            attr.data.foreach_set('color',data)
            mat=bpy.data.materials.new('Dominant bone group diagnosis');mat.use_nodes=True
            nodes=mat.node_tree.nodes;nodes.clear()
            output=nodes.new('ShaderNodeOutputMaterial');emission=nodes.new('ShaderNodeEmission');attribute=nodes.new('ShaderNodeAttribute');attribute.attribute_name='DiagnosticWeight'
            mat.node_tree.links.new(attribute.outputs['Color'],emission.inputs['Color']);mat.node_tree.links.new(emission.outputs[0],output.inputs[0])
            mesh.data.materials.clear();mesh.data.materials.append(mat)
        scene.render.filepath=str(OUT/'weights-front.png');bpy.ops.render.render(write_still=True)
        cam.location=(2,5,.9);cam.rotation_euler=(Vector((0,0,.83))-cam.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(OUT/'weights-back.png');bpy.ops.render.render(write_still=True)
    reports.append(report)
    print('Completed '+label,flush=True)
(OUT/'blender-inspection.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
sys.stdout.flush();os._exit(0)
