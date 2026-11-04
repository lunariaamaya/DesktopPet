"""Character-specific, non-destructive first-pass weight repair in isolated bpy.

This is a conservative artist-review prototype, not a general auto-rigger.
Run --inspect to review colored spatial masks without exporting a model.
Original Downloads GLBs are never written. Re-running refuses existing exports.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, sys
import bpy
import numpy as np
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('C:/Users/HP/Downloads/Rigged Anime Cat Girl HD move.glb')
SOURCE_HASH = '55a81668a5eaced8b16f3c0d4188f6bf6f78ebc3014e90e4688bf4c5afe71ab0'
OUT = ROOT / 'tmp/meshy-repair'
DELIVERY = ROOT / 'exports/meshy-repair-v04'

def smooth(a, b, x):
    t = np.clip((x-a)/(b-a), 0, 1)
    return t*t*(3-2*t)

def masks(points):
    """Blender world coordinates, meters. Tuned only for the pinned source.

    White hair and dress have no separate material/topological boundary; these
    spatial masks need visual review and must not be reused on another mesh.
    """
    x, back, h = points.T
    # Back hair occupies the rear shell above the waist. Keep the lower front
    # arm/sleeve surfaces out; smoothly fade into the existing correct head rig.
    rear_boundary = np.interp(h, [.82,.88,1.02,1.18,1.30], [.19,.14,.07,.015,-.06])
    hair = smooth(.815,.86,h) * smooth(-.015,.015,back-rear_boundary)
    # Upper head and its ear ornaments already belong to Head; include them
    # to avoid a discontinuity between crown and the repaired hair shell.
    hair = np.maximum(hair, smooth(1.29,1.36,h))
    lateral=smooth(.13,.165,np.abs(x-.05))*smooth(-.015,.015,back)*smooth(.815,.86,h)
    hair=np.maximum(hair,lateral)
    # Forward side-locks are later refined by inspection, not inferred from color.
    # Tail is a tube outside the skirt; a narrow rear strip catches its root.
    tail = smooth(.81,.88,1.66-h) * smooth(.30,.36,h)
    tail *= smooth(.205,.245,-x) * smooth(.07,.12,back)
    # The upper tail curves inward toward the pelvis. Define a local tapered
    # tube around the shaft, with width shrinking near the skirt attachment.
    shaft_x = np.interp(h,[.45,.55,.65,.75,.85],[-.29,-.30,-.265,-.14,-.035])
    shaft_y = np.interp(h,[.45,.55,.65,.75,.85],[.23,.25,.245,.18,.105])
    radius = np.interp(h,[.45,.65,.75,.85],[.075,.045,.045,.038])
    distance = np.sqrt((x-shaft_x)**2+(back-shaft_y)**2)
    shaft = (1-smooth(radius*.7,radius,distance))*smooth(.42,.47,h)*(1-smooth(.84,.89,h))
    tail = np.maximum(tail, shaft)
    tail *= 1-hair
    # Only non-skin skirt/bodice candidates below the sleeve line. Existing
    # leg controls remain; this pass removes accidental hand/arm contributions.
    skirt = smooth(.31,.35,h)*(1-smooth(.97,1.015,h))
    return {'hair':hair, 'tail':tail, 'skirt':skirt}

def sampled_skin(mesh):
    """Texture color aid, NOT a semantic classifier; keep skin out below neck.

    A per-vertex maximum protects both sides of a UV seam. Pink lace also
    matches this color aid; the lower-skirt cleanup must override that result.
    """
    image=next(n.image for n in mesh.data.materials[0].node_tree.nodes
               if n.type=='TEX_IMAGE' and n.image and 'BASE COLOR' in n.label.upper())
    pixels=np.empty(len(image.pixels),dtype=np.float32);image.pixels.foreach_get(pixels)
    pixels=pixels.reshape(image.size[1],image.size[0],4)
    uv=np.empty(len(mesh.data.loops)*2,dtype=np.float32);mesh.data.uv_layers.active.data.foreach_get('uv',uv)
    uv=uv.reshape(-1,2);i=np.clip((uv[:,0]*image.size[0]).astype(int),0,image.size[0]-1)
    j=np.clip((uv[:,1]*image.size[1]).astype(int),0,image.size[1]-1)
    c=pixels[j,i,:3]
    skin=(c[:,0]>c[:,1]*1.075)&(c[:,1]>c[:,2]*1.035)&(c[:,0]>.25)
    vi=np.empty(len(mesh.data.loops),dtype=np.int32);mesh.data.loops.foreach_get('vertex_index',vi)
    result=np.zeros(len(mesh.data.vertices),dtype=np.float32);np.maximum.at(result,vi,skin.astype(np.float32))
    return result

def configure_scene():
    scene=bpy.context.scene
    scene.render.engine='CYCLES'; scene.cycles.samples=8;scene.cycles.use_denoising=True
    scene.render.resolution_x=640;scene.render.resolution_y=800;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
    scene.world.use_nodes=True
    scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1)
    scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
    scene.view_settings.view_transform='Standard'
    cd=bpy.data.cameras.new('RepairReviewCamera');cam=bpy.data.objects.new('RepairReviewCamera',cd)
    scene.collection.objects.link(cam);scene.camera=cam;cd.type='ORTHO';cd.ortho_scale=1.95
    for name,loc,power in [('key',(-3,-4,6),400),('fill',(4,-3,4),200)]:
        ld=bpy.data.lights.new(name,'AREA');ld.energy=power;ld.size=3
        light=bpy.data.objects.new(name,ld);scene.collection.objects.link(light);light.location=loc
        light.rotation_euler=(Vector((0,0,.83))-light.location).to_track_quat('-Z','Y').to_euler()
    return scene,cam

def render(scene,cam,path,view='front'):
    cam.location={'front':(0,-5,.88),'side':(-5,0,.88),'back':(0,5,.88)}[view]
    cam.rotation_euler=(Vector((0,0,.83))-cam.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)

def show_masks(mesh, regions):
    attr=mesh.data.color_attributes.new(name='RepairRegionReview',type='FLOAT_COLOR',domain='POINT')
    colors=np.ones((len(mesh.data.vertices),4),dtype=np.float32);colors[:,:3]=.45
    for name,color in [('skirt',(.12,.7,.15)),('hair',(.08,.4,1)),('tail',(1,.35,.04))]:
        a=regions[name][:,None];colors[:,:3]=colors[:,:3]*(1-a)+np.array(color)*a
    attr.data.foreach_set('color',colors.ravel())
    mat=bpy.data.materials.new('Repair region visualization');mat.use_nodes=True
    nodes=mat.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial')
    emission=nodes.new('ShaderNodeEmission');color=nodes.new('ShaderNodeAttribute');color.attribute_name=attr.name
    mat.node_tree.links.new(color.outputs['Color'],emission.inputs['Color']);mat.node_tree.links.new(emission.outputs[0],out.inputs[0])
    originals=list(mesh.data.materials);mesh.data.materials.clear();mesh.data.materials.append(mat)
    return originals,attr

def get_weights(mesh):
    result=np.zeros((len(mesh.data.vertices),len(mesh.vertex_groups)),dtype=np.float32)
    for v in mesh.data.vertices:
        for item in v.groups:result[v.index,item.group]=item.weight
    return result

def set_weights(mesh, weights):
    # Batch equal rounded weights. Quantization only affects weights, never geometry.
    indices=list(range(len(mesh.data.vertices)))
    for group in mesh.vertex_groups:group.remove(indices)
    for column,group in enumerate(mesh.vertex_groups):
        values=weights[:,column]
        selected=np.flatnonzero(values>0)
        ordered=selected[np.argsort(values[selected])]
        unique,starts=np.unique(values[ordered],return_index=True)
        ends=np.r_[starts[1:],len(ordered)]
        for weight,start,end in zip(unique,starts,ends):
            group.add(ordered[start:end].tolist(),float(weight),'REPLACE')

def add_controls(arm,mesh):
    definitions=[
        ('HairRoot','Head',(.05,.07,1.32),(.05,.16,1.08)),
        ('HairTip','HairRoot',(.05,.16,1.08),(.05,.20,.84)),
        ('TailRoot','Hips',(-.035,.105,.85),(-.14,.18,.75)),
        ('TailMid','TailRoot',(-.14,.18,.75),(-.28,.245,.61)),
        ('TailTip','TailMid',(-.28,.245,.61),(-.29,.23,.42)),
    ]
    bpy.context.view_layer.objects.active=arm;arm.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT');inv=arm.matrix_world.inverted()
    # Imported display tails are ~100x too long. Shorten along the same axis,
    # retaining heads/roll/parenting; tail length is not a skinning influence.
    for b in arm.data.edit_bones:
        lengths=[(child.head-b.head).length for child in b.children if (child.head-b.head).length>1e-3]
        length=min(lengths) if lengths else ((b.head-b.parent.head).length*.5 if b.parent else 10.)
        b.length=max(2.,min(25.,length))
    for name,parent,head,tail in definitions:
        b=arm.data.edit_bones.new(name);b.head=inv@Vector(head);b.tail=inv@Vector(tail)
        b.parent=arm.data.edit_bones[parent];b.use_connect=False;b.use_deform=True
    bpy.ops.object.mode_set(mode='OBJECT')
    for name,_,_,_ in definitions:mesh.vertex_groups.new(name=name)
    return [d[0] for d in definitions]

def interpolated_weights(height, centers):
    result=np.zeros((len(height),len(centers)))
    for i in range(len(centers)):
        y=np.zeros(len(centers));y[i]=1
        result[:,i]=np.interp(height,centers,y)
    return result

def repair(mesh, arm, points, regions):
    original=get_weights(mesh);old_count=original.shape[1];controls=add_controls(arm,mesh)
    names=[g.name for g in mesh.vertex_groups];index={n:i for i,n in enumerate(names)}
    weights=np.pad(original,((0,0),(0,len(controls))))
    upper=[i for n,i in index.items() if any(word in n for word in ['Arm','Hand','Shoulder'])]
    # Below the sleeve line, reassign accidental upper-limb contributions to
    # the pelvis. Preserve existing leg weights pending a separate skirt rig.
    removed=weights[:,upper]*regions['skirt'][:,None]
    weights[:,upper]-=removed;weights[:,index['Hips']]+=removed.sum(axis=1)
    target=np.zeros_like(weights)
    # Piecewise weights from low tip through hair root to existing Head.
    hw=interpolated_weights(points[:,2],[.91,1.15,1.34])
    for j,name in enumerate(['HairTip','HairRoot','Head']):target[:,index[name]]=hw[:,j]
    alpha=regions['hair'][:,None];weights=weights*(1-alpha)+target*alpha
    target[:]=0;tw=interpolated_weights(points[:,2],[.48,.66,.84])
    for j,name in enumerate(['TailTip','TailMid','TailRoot']):target[:,index[name]]=tw[:,j]
    alpha=regions['tail'][:,None];weights=weights*(1-alpha)+target*alpha
    # The original skin also has inconsistent near-wrist weights. Use local
    # arm capsules (plus the texture skin aid) to keep fingers/forearms together.
    skin=sampled_skin(mesh)
    for side in ['Right','Left']:
        shoulder=arm.matrix_world@arm.data.bones[side+'Arm'].head_local
        elbow=arm.matrix_world@arm.data.bones[side+'ForeArm'].head_local
        wrist=arm.matrix_world@arm.data.bones[side+'Hand'].head_local
        tip=np.array(wrist)+np.array((-.057 if side=='Right' else .053,-.015,-.095))
        distance=np.full(len(points),np.inf)
        for p,q in [(np.array(shoulder),np.array(elbow)),(np.array(elbow),np.array(wrist)),(np.array(wrist),tip)]:
            t=np.clip((points-p)@(q-p)/np.dot(q-p,q-p),0,1)
            distance=np.minimum(distance,np.linalg.norm(points-(p+t[:,None]*(q-p)),axis=1))
        alpha=np.maximum(1-smooth(.03,.042,distance),skin*(1-smooth(.045,.065,distance)))
        alpha*=1-smooth(.02,.05,points[:,1])
        alpha*=smooth(.70,.73,points[:,2])*(1-smooth(1.20,1.24,points[:,2]))
        hand=1-smooth(wrist.z-.015,wrist.z+.035,points[:,2])
        upper_blend=smooth(elbow.z-.025,elbow.z+.045,points[:,2])
        target[:]=0
        target[:,index[side+'Hand']]=hand
        target[:,index[side+'Arm']]=(1-hand)*upper_blend
        target[:,index[side+'ForeArm']]=(1-hand)*(1-upper_blend)
        weights=weights*(1-alpha[:,None])+target*alpha[:,None]
    # No real hand/arm vertices are below .70m in this pinned character.
    # This catches UV-seam/hem flower vertices that evade color-based masks.
    low=points[:,2]<.70
    lower_arm_weight=weights[np.ix_(low,upper)].sum(axis=1)
    weights[np.ix_(low,upper)]=0
    weights[low,index['Hips']]+=lower_arm_weight
    # Keep strongest four for predictable GLB skinning; normalize AFTER rounding.
    keep=np.argpartition(weights,-4,axis=1)[:,-4:]
    limited=np.zeros_like(weights);np.put_along_axis(limited,keep,np.take_along_axis(weights,keep,axis=1),axis=1)
    limited=np.round(limited,4);limited/=limited.sum(axis=1,keepdims=True)
    assert np.isfinite(limited).all() and limited.min()>=0
    assert np.max(np.abs(limited.sum(axis=1)-1))<1e-6
    set_weights(mesh,limited)
    return {'original_group_count':old_count,'new_controls':controls,
            'changed_vertices':int((np.max(np.abs(limited-np.pad(original,((0,0),(0,len(controls))))),axis=1)>1e-4).sum()),
            'max_weight_sum_error':float(np.max(np.abs(limited.sum(axis=1)-1))),
            'hair_mask_strong_vertices':int((regions['hair']>.99).sum()),
            'tail_mask_strong_vertices':int((regions['tail']>.99).sum()),
            'skirt_upper_limb_weight_removed_total':float(removed.sum())}

def pose(arm, settings):
    for bone in arm.pose.bones:
        bone.matrix_basis.identity();bone.rotation_mode='XYZ'
    for name,(axis,degrees) in settings.items():arm.pose.bones[name].rotation_euler[axis]=math.radians(degrees)
    bpy.context.view_layer.update()

def evaluated_points(mesh):
    obj=mesh.evaluated_get(bpy.context.evaluated_depsgraph_get());data=obj.to_mesh()
    points=np.empty(len(data.vertices)*3,dtype=np.float32);data.vertices.foreach_get('co',points)
    points=points.reshape(-1,3);m=np.array(obj.matrix_world);points=points@m[:3,:3].T+m[:3,3]
    obj.to_mesh_clear();return points

def measure(scene,cam,arm,mesh,regions,prefix,render_images=True):
    pose(arm,{});rest=evaluated_points(mesh);report={}
    for label,settings in [('rest',{}),('raise-arm',{'RightArm':(0,60)}),('head-turn',{'Head':(1,20)}),('step',{'LeftUpLeg':(0,25)})]:
        pose(arm,settings);current=evaluated_points(mesh)
        distance=np.linalg.norm(current-rest,axis=1)
        report[label]={}
        for name in ['hair','tail']:
            # Hair displacement is measured below the head, in strong mask only.
            region=(regions[name]>.99)&((rest[:,2]<1.27) if name=='hair' else True)
            d=distance[region];report[label][name]={'n':len(d),'median_m':float(np.median(d)), 'p95_m':float(np.percentile(d,95)), 'max_m':float(d.max())}
        if render_images:
            render(scene,cam,OUT/f'{prefix}-{label}-front.png')
            if label in ['raise-arm','head-turn']:render(scene,cam,OUT/f'{prefix}-{label}-back.png','back')
    pose(arm,{})
    return report,rest

def motion_check(arm,scene):
    pose(arm,{})
    arm.animation_data_create();action=bpy.data.actions.new('RepairDiagnostic_NotOriginal')
    arm.animation_data.action=action;scene.render.fps=30;scene.frame_start=1;scene.frame_end=91
    controls=['RightArm','Head','TailRoot','TailMid','TailTip','HairRoot','HairTip']
    for frame in [1,16,31,46,61,76,91]:
        scene.frame_set(frame);settings={}
        if frame==16:settings={'RightArm':(0,60)}
        if frame==46:settings={'Head':(1,20)}
        if frame==76:settings={'TailRoot':(0,4),'TailMid':(0,6),'TailTip':(0,8),'HairTip':(0,3)}
        pose(arm,settings)
        for name in controls:arm.pose.bones[name].keyframe_insert(data_path='rotation_euler',frame=frame,group=name)
    for curve in action.fcurves:
        for key in curve.keyframe_points:key.interpolation='LINEAR'
    scene.frame_set(1)

def export_model(arm,mesh,path,animate):
    bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);mesh.select_set(True)
    bpy.context.view_layer.objects.active=arm
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,
                             export_animations=animate,export_animation_mode='ACTIVE_ACTIONS',
                             export_skins=True,export_yup=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inspect',action='store_true')
    parser.add_argument('--reuse-before-renders',action='store_true',help='Only reuse images from this exact script/source/mask setup')
    args=parser.parse_args()
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_HASH,'Source changed; review masks again'
    OUT.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    bpy.ops.import_scene.gltf(filepath=str(SOURCE))
    scene,cam=configure_scene()
    arm=next(o for o in scene.objects if o.type=='ARMATURE')
    mesh=next(o for o in scene.objects if o.type=='MESH')
    arm.animation_data_clear();arm.data.pose_position='POSE'
    for bone in arm.pose.bones:bone.matrix_basis.identity()
    bpy.context.view_layer.update()
    points=np.array([mesh.matrix_world@v.co for v in mesh.data.vertices])
    regions=masks(points)
    skin=sampled_skin(mesh)
    regions['hair']*=1-skin*(1-smooth(1.27,1.33,points[:,2]))
    # Pink hem embroidery resembles skin in the texture. Protect skin only
    # near actual arms; do not leave its accidental wrist weights on the hem.
    regions['skirt']*=1-skin*smooth(.66,.72,points[:,2])
    if args.inspect:
        show_masks(mesh,regions)
        for view in ['front','side','back']:render(scene,cam,OUT/f'mask-{view}.png',view)
        print({k:int((v>.5).sum()) for k,v in regions.items()},flush=True)
    else:
        DELIVERY.mkdir(parents=True,exist_ok=True)
        assert not any(DELIVERY.iterdir()),'Refusing to replace existing trial; use a new version directory'
        before,rest_before=measure(scene,cam,arm,mesh,regions,'before',not args.reuse_before_renders)
        (OUT/'before-metrics.json').write_text(json.dumps(before,indent=2))
        print('Writing corrected weights',flush=True)
        result=repair(mesh,arm,points,regions)
        print('Corrected weights written',flush=True)
        after,rest_after=measure(scene,cam,arm,mesh,regions,'after')
        result.update({'source_sha256':SOURCE_HASH,'source':str(SOURCE),'before':before,'after':after,
                       'rest_max_vertex_difference_m':float(np.max(np.linalg.norm(rest_after-rest_before,axis=1))),
                       'limitations':['Spatial masks require artist review; blended boundaries remain.',
                                      'No cloth/physics/collision; original thigh-skirt weights remain.',
                                      'No face, finger or topology repair; diagnostic motion is newly scripted.']})
        assert result['rest_max_vertex_difference_m']<1e-5,'Rest shape changed unexpectedly'
        pose(arm,{})
        export_model(arm,mesh,DELIVERY/'character-weight-repair-v04.glb',False)
        motion_check(arm,scene)
        # Remove unused original single-pose action from this working copy only.
        for action in list(bpy.data.actions):
            if action!=arm.animation_data.action and not action.users:bpy.data.actions.remove(action)
        export_model(arm,mesh,DELIVERY/'character-weight-repair-v04-motion-check.glb',True)
        scene.frame_set(1);pose(arm,{})
        bpy.ops.wm.save_as_mainfile(filepath=str(DELIVERY/'character-weight-repair-v04.blend'))
        result['outputs']=[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in DELIVERY.iterdir()]
        (OUT/'repair-result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':
    main();sys.stdout.flush();os._exit(0)
