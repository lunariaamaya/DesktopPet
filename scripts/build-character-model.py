"""Reference-guided editable 3D blockout. Run with isolated bpy runtime.

This is procedural modeling from the approved design specification, not learned
multi-view reconstruction and not an animation-ready production character.
"""
from pathlib import Path
import math
import json
import hashlib
import random
import os
import sys
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/characters/first-character/models/v01'
OUT.mkdir(parents=True, exist_ok=True)
REF = ROOT / 'assets/characters/first-character/concepts/turnaround-v02-accessories-v12.png'
random.seed(19)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
collections = {}
for name in ['body', 'face', 'hair', 'headwear', 'chest_accessory', 'upper', 'lower', 'waist', 'feet', 'presentation']:
    col = bpy.data.collections.new(name)
    scene.collection.children.link(col)
    collections[name] = col

def link(obj, group):
    for col in list(obj.users_collection):
        col.objects.unlink(obj)
    collections[group].objects.link(obj)
    obj['module'] = group
    return obj

def linear(v):
    return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4

def material(name, hexcolor, rough=.6, metal=0):
    rgb = tuple(linear(int(hexcolor[i:i+2], 16)/255) for i in (0, 2, 4))
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*rgb, 1)
    mat.use_nodes = True
    bs = mat.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*rgb, 1)
    bs.inputs['Roughness'].default_value = rough
    bs.inputs['Metallic'].default_value = metal
    return mat

skin = material('skin_pink_ivory', 'FEEEEA', .62)
hair = material('hair_white', 'FAFAFE', .46)
cloth = material('dress_white', 'FCFCFF', .78)
lace = material('lace_white', 'FFFFFF', .73)
purple = material('ribbon_blue_violet', '9282BD', .5)
pink = material('ear_inner_soft_pink', 'F2CCCA', .7)
gold = material('pendant_frame', 'C2A66C', .35, .48)
emerald = material('emerald', '2EAA79', .2, .12)
white = material('eye_white', 'FFFDFC', .4)
red = material('iris_anatomical_left_red', 'C64247', .3)
blue = material('iris_anatomical_right_blue', '3D91CE', .3)
dark = material('eyelashes', '65526F', .7)
pupil = material('pupil', '273040', .4)
lip = material('tiny_mouth', 'B9989B', .7)

def mesh(name, verts, faces, mat, group):
    data = bpy.data.meshes.new(name)
    data.from_pydata(verts, [], faces)
    data.update()
    obj = bpy.data.objects.new(name, data)
    collections[group].objects.link(obj)
    obj.data.materials.append(mat)
    for poly in data.polygons:
        poly.use_smooth = True
    return obj

def sphere(name, at, scale, mat, group, segments=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=at)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(mat)
    for p in obj.data.polygons:
        p.use_smooth = True
    return link(obj, group)

def tube(name, points, radii, mat, group, sides=9, flatten=1.0):
    verts, faces = [], []
    for i, point in enumerate(points):
        p = Vector(point)
        tangent = Vector(points[min(i+1, len(points)-1)]) - Vector(points[max(0, i-1)])
        if tangent.length < 1e-7:
            tangent = Vector((0, 0, 1))
        tangent.normalize()
        anchor = Vector((0, 1, 0)) if abs(tangent.y) < .9 else Vector((1, 0, 0))
        u = tangent.cross(anchor).normalized()
        v = tangent.cross(u).normalized()
        for j in range(sides):
            theta = 2*math.pi*j/sides
            q = p + radii[i] * (u*math.cos(theta) + v*math.sin(theta)*flatten)
            verts.append(tuple(q))
    for i in range(len(points)-1):
        for j in range(sides):
            a=i*sides+j; b=i*sides+(j+1)%sides
            faces.append((a,b,b+sides,a+sides))
    faces.append(tuple(reversed(tuple(range(sides)))))
    faces.append(tuple((len(points)-1)*sides+j for j in range(sides)))
    return mesh(name, verts, faces, mat, group)

def curve(name, points, radius, mat, group, cyclic=False):
    c = bpy.data.curves.new(name, 'CURVE')
    c.dimensions='3D'; c.resolution_u=8
    c.bevel_depth=radius; c.bevel_resolution=2
    spline=c.splines.new('POLY')
    spline.points.add(len(points)-1)
    for dst, p in zip(spline.points, points):
        dst.co=(*p,1)
    spline.use_cyclic_u=cyclic
    obj=bpy.data.objects.new(name,c)
    collections[group].objects.link(obj)
    c.materials.append(mat)
    return obj

def ring(name, center, rx, ry, radius, mat, group, waves=0, amplitude=0):
    pts=[]
    for i in range(96):
        a=2*math.pi*i/96
        pts.append((center[0]+rx*math.cos(a), center[1]+ry*math.sin(a), center[2]+amplitude*math.sin(waves*a)))
    return curve(name,pts,radius,mat,group,True)

def lathe(name, rows, mat, group, count=96, pleats=0, amp=0):
    verts=[]; faces=[]
    for z,rx,ry in rows:
        for j in range(count):
            a=2*math.pi*j/count
            f=1+amp*math.cos(pleats*a)
            verts.append((rx*f*math.cos(a),ry*f*math.sin(a),z))
    for i in range(len(rows)-1):
        for j in range(count):
            a=i*count+j;b=i*count+(j+1)%count
            faces.append((a,b,b+count,a+count))
    obj=mesh(name,verts,faces,mat,group)
    thick=obj.modifiers.new('fabric_thickness','SOLIDIFY');thick.thickness=.0015
    return obj

def flower(name, at, size, normal, group):
    n=Vector(normal).normalized()
    u=n.cross(Vector((0,0,1)))
    if u.length<.01:u=n.cross(Vector((0,1,0)))
    u.normalize();v=n.cross(u).normalized();p=Vector(at)
    for j in range(5):
        a=2*math.pi*j/5
        center=p+(u*math.cos(a)+v*math.sin(a))*size*.58
        petal=sphere(f'{name}_petal{j}',center,(size*.50,size*.50,size*.20),lace,group,12,8)
        petal.rotation_mode='QUATERNION';petal.rotation_quaternion=Vector((0,0,1)).rotation_difference(n)
    sphere(name+'_center',p+n*size*.1,(size*.22,)*3,gold,group,12,8)

def bow(name, at, size, group):
    # Bow plane is XZ; it has real thickness in Y, so a side camera sees its edge.
    x,y,z=at
    for s in [-1,1]:
        verts=[(x,y,z),(x+s*size*.95,y+.006,z+size*.50),
               (x+s*size,y+.010,z-size*.27),(x+s*size*.28,y-.005,z-size*.10)]
        obj=mesh(name+('_L' if s<0 else '_R'),verts,[(0,1,2,3)],purple,group)
        mod=obj.modifiers.new('ribbon_thickness','SOLIDIFY');mod.thickness=.006
        bevel=obj.modifiers.new('soft_ribbon_edges','BEVEL');bevel.width=.004;bevel.segments=3
        mesh(name+f'_ribbon{s}',[(x+s*.004,y,z),(x+s*size*.45,y,z-size*1.30),
            (x+s*size*.67,y+.006,z-size*1.05),(x+s*size*.18,y+.006,z-size*.05)],[(0,1,2,3)],purple,group)
    sphere(name+'_knot',(x,y-.004,z),(size*.21,.011,size*.16),purple,group,16,10)

# Anatomical frame: Z up, face points -Y, anatomical left is +X.
sphere('body_torso',(0,0,.865),(.092,.048,.135),skin,'body')
sphere('neck',(0,-.002,1.005),(.037,.033,.055),skin,'body')
head=sphere('head',(0,-.006,1.118),(.115,.094,.137),skin,'face',48,32)
for vert in head.data.vertices:
    if vert.co.z<0:
        vert.co.x*=1+.22*vert.co.z
sphere('nose',(0,-.101,1.090),(.009,.009,.012),skin,'face',16,10)

# Eyes are layered shallow meshes on the front, with anatomy-specific colors.
for s, iris in [(-1,blue),(1,red)]:
    x=s*.045
    sphere(f'eye_white_{s}',(x,-.091,1.128),(.032,.006,.025),white,'face',32,20)
    sphere(f'iris_{s}',(x,-.097,1.127),(.019,.002,.022),iris,'face',24,16)
    sphere(f'pupil_{s}',(x,-.100,1.127),(.008,.001,.014),pupil,'face',16,12)
    sphere(f'catchlight_{s}',(x-.005,-.102,1.136),(.004,.001,.005),lace,'face',12,8)
    pts=[(x+.032*math.cos(t),-.104,1.128+.025*math.sin(t)) for t in [math.pi*j/16 for j in range(17)]]
    curve(f'upper_lash_{s}',pts,.0023,dark,'face')
curve('small_mouth',[(-.009,-.098,1.066),(0,-.101,1.064),(.009,-.098,1.066)],.001,lip,'face')

for s in [-1,1]:
    # Pointed elf ears, separate from top wearable cat ears.
    verts=[(s*.101,.002,1.136),(s*.191,.007,1.158),(s*.119,.006,1.094),
           (s*.122,-.016,1.126),(s*.122,.019,1.126)]
    ear=mesh(f'elf_ear_{s}',verts,[(0,1,3),(1,2,3),(2,0,3),(1,0,4),(2,1,4),(0,2,4)],skin,'face')
    bevel=ear.modifiers.new('soft_ear','BEVEL');bevel.width=.006;bevel.segments=3
    mesh(f'elf_inner_{s}',[(s*.117,-.015,1.134),(s*.173,-.002,1.151),(s*.128,-.015,1.111)],[(0,1,2)],pink,'face')

for s in [-1,1]:
    shoulder=(s*.142,0,.938); elbow=(s*.205,-.008,.782); wrist=(s*.254,-.015,.624)
    tube(f'arm_{s}',[shoulder,elbow,wrist],[.028,.022,.015],skin,'body',14)
    sphere(f'palm_{s}',(s*.264,-.014,.602),(.019,.012,.026),skin,'body')
    for j in range(4):
        spread=(j-1.5)*.010
        start=(s*(.264+spread),-.014,.591)
        end=(s*(.267+spread*1.18),-.017,.561+abs(j-1.3)*.006)
        tube(f'finger_{s}_{j}',[start,end],[.0058,.0045],skin,'body',8)
        sphere(f'finger_tip_{s}_{j}',end,(.0045,)*3,skin,'body',10,6)
    tube(f'thumb_{s}',[(s*.248,-.023,.611),(s*.239,-.030,.589)],[.007,.005],skin,'body',8)
    sphere(f'thumb_tip_{s}',(s*.239,-.030,.589),(.005,)*3,skin,'body',10,6)
    sphere(f'puff_sleeve_{s}',(s*.155,.001,.904),(.054,.055,.069),cloth,'upper')
    ring(f'sleeve_ruffle_{s}',(s*.169,0,.851),.049,.047,.007,lace,'upper',12,.004)

lathe('bodice',[(.79,.099,.063),(.84,.108,.066),(.90,.125,.073),(.948,.133,.072)],cloth,'upper',80,12,.012)
ring('off_shoulder_ruffle',(0,0,.946),.133,.074,.010,lace,'upper',20,.005)
ring('waist_band',(0,0,.791),.103,.067,.006,lace,'upper')
bow('bodice_bow',(0,-.074,.801),.031,'upper')

# Calf-length dress: actual open gap bridged by white lace loops.
lathe('skirt',[(.791,.103,.068),(.73,.128,.089),(.63,.165,.125),(.51,.205,.159),(.39,.246,.190),(.334,.262,.205)],cloth,'lower',128,20,.025)
lathe('hem_ruffle',[(.291,.265,.208),(.275,.275,.216),(.255,.273,.217)],cloth,'lower',128,30,.035)
ring('lace_upper_edge',(0,0,.334),.262,.205,.0028,lace,'lower')
ring('lace_lower_edge',(0,0,.291),.265,.208,.0028,lace,'lower')
for j in range(28):
    a=2*math.pi*j/28
    center=Vector((.264*math.cos(a),.207*math.sin(a),.313))
    tangent=Vector((-math.sin(a),math.cos(a),0))
    for petal in range(5):
        pa=petal*2*math.pi/5
        pc=center+tangent*(.010*math.cos(pa))+Vector((0,0,.010*math.sin(pa)))
        points=[]
        for k in range(14):
            t=2*math.pi*k/14
            points.append(tuple(pc+tangent*(.008*math.cos(t))+Vector((0,0,.008*math.sin(t)))))
        curve(f'open_lace_{j}_{petal}',points,.0013,lace,'lower',True)

for s in [-1,1]:
    tube(f'leg_{s}',[(s*.068,.005,.66),(s*.073,.004,.41),(s*.076,0,.052)],[.035,.027,.018],skin,'body',16)
    sphere(f'foot_{s}',(s*.076,-.029,.037),(.026,.057,.022),skin,'feet',24,16)
    for j in range(5):
        toe=(s*.076+(j-2)*.008,-.078+abs(j-1)*.002,.029)
        sphere(f'toe_{s}_{j}',toe,(.0053,.010,.006),skin,'feet',10,8)
    for level in [.091,.104]:
        ring(f'anklet_{s}_{level}',(s*.076,0,level),.021,.021,.0025,lace,'feet')
    flower(f'ankle_flower_{s}',(s*.076,-.023,.100),.010,(0,-1,0),'feet')

ring('necklace_chain',(0,0,.992),.039,.036,.0016,gold,'chest_accessory')
curve('pendant_chain',[(0,-.036,.993),(0,-.078,.965)],.0016,gold,'chest_accessory')
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(0,-.080,.958))
gem=bpy.context.object;gem.name='emerald_pendant';gem.scale=(.015,.006,.022);gem.data.materials.append(emerald);link(gem,'chest_accessory')
flower('neck_ruffle',(0,-.039,.995),.011,(0,-1,0),'chest_accessory')

# Partial scalp cap, open across face; independent strand meshes retain editability.
verts=[];faces=[];rows=14;cols=64
for i in range(rows):
    t=i/(rows-1)
    for j in range(cols):
        phi=2*math.pi*j/cols
        front=(1-math.sin(phi))/2
        theta=t*math.radians(133-68*front)
        verts.append((.125*math.sin(theta)*math.cos(phi),.006+.103*math.sin(theta)*math.sin(phi),1.124+.149*math.cos(theta)))
for i in range(rows-1):
    for j in range(cols):
        a=i*cols+j;b=i*cols+(j+1)%cols;faces.append((a,b,b+cols,a+cols))
mesh('hair_cap',verts,faces,hair,'hair')
for strand in range(22):
    u=(strand-10.5)/10.5
    points=[];radii=[]
    length=.55+random.random()*.06
    for k in range(43):
        t=k/42
        x=u*(.095+.160*t)+.025*math.sin(t*math.pi*7+strand*.7)*(t**.6)
        y=.045+.085*math.sin(math.pi*t/2)+.020*math.cos(t*math.pi*7+strand*.6)
        z=1.20-length*t
        points.append((x,y,z))
        radii.append((.014+.009*math.sin(math.pi*t))*(1-t**5)+.0015)
    tube(f'back_curl_{strand:02}',points,radii,hair,'hair',10,.70)
for s in [-1,1]:
    for j in range(4):
        pts=[];r=[]
        for k in range(22):
            t=k/21
            pts.append((s*(.018+j*.022+(.028-j*.004)*math.sin(math.pi*t/2)),
                        -.015-.102*math.sin(math.pi*t/2),1.267-(.135+j*.011)*t))
            r.append((.016+.003*math.sin(math.pi*t))*(1-t**3)+.001)
        tube(f'fringe_{s}_{j}',pts,r,hair,'hair',10,.5)
    pts=[(s*(.113+.028*math.sin(t*math.pi*3)),.004+.014*t,1.135-.40*t) for t in [j/35 for j in range(36)]]
    tube(f'side_curl_{s}',pts,[.018*(1-(j/35)**5)+.002 for j in range(36)],hair,'hair',10,.65)
    # Cat-ear ornaments above head, not elf ears.
    outer=[(s*.060,.016,1.244),(s*.112,.020,1.371),(s*.158,.018,1.252),
           (s*.101,-.024,1.275),(s*.104,.057,1.273)]
    mesh(f'cat_ear_{s}',outer,[(0,1,3),(1,2,3),(2,0,3),(1,0,4),(2,1,4),(0,2,4)],hair,'headwear')
    mesh(f'cat_inner_{s}',[(s*.079,-.005,1.255),(s*.111,.006,1.345),(s*.139,-.005,1.261)],[(0,1,2)],pink,'headwear')
    bow(f'head_bow_{s}',(s*.133,.018,1.246),.038,'headwear')
    flower(f'head_flower_{s}',(s*.112,-.031,1.257),.015,(0,-1,0),'headwear')
    flower(f'cat_back_flower_{s}',(s*.111,.049,1.280),.010,(0,1,0),'headwear')

# Upper-hip rear attachment, physically separate costume accessory.
points=[];radii=[]
for j in range(46):
    t=j/45
    points.append((-.34*math.sin(math.pi*t/2),.09+.14*t,.715-.30*t+.025*math.sin(math.pi*t)))
    radii.append(.013+.008*t*t)
tube('wearable_tail',points,radii,hair,'waist',14)
sphere('tail_tip',(-.34,.23,.402),(.025,.022,.045),hair,'waist')
bow('tail_bow',(-.339,.23,.446),.046,'waist')

# Save source reference packed in the blend as an image datablock (not a projected fake model).
reference=bpy.data.images.load(str(REF));reference.pack()
scene['reference_sha256']=hashlib.sha256(REF.read_bytes()).hexdigest()
scene['model_status']='procedural_blockout_v01_not_production_rigged'
scene['axis_convention']='Z up; front -Y; anatomical left +X'

def camera(name,location,target,ortho=1.60):
    data=bpy.data.cameras.new(name);obj=bpy.data.objects.new(name,data);collections['presentation'].objects.link(obj)
    obj.location=location;obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
    data.type='ORTHO';data.ortho_scale=ortho;data.lens=55;return obj

front=camera('camera_front',(0,-3.5,.72),(0,0,.70))
side=camera('camera_right',(3.5,0,.72),(0,0,.70))
back=camera('camera_back',(0,3.5,.72),(0,0,.70))
beauty=camera('camera_three_quarter',(2.1,-3.5,1.55),(0,0,.72))
for name,at,energy,size in [('key',(0,-3,1.5),90,3),('fill',(3,1,2),30,4),('back',(-2,2,2),25,3)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=energy;data.shape='DISK';data.size=size
    obj=bpy.data.objects.new(name,data);collections['presentation'].objects.link(obj);obj.location=at
    obj.rotation_euler=(Vector((0,0,.7))-obj.location).to_track_quat('-Z','Y').to_euler()
scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(1,1,1,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.22
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.render.resolution_x=768;scene.render.resolution_y=1024;scene.render.resolution_percentage=100
scene.render.film_transparent=True
scene.view_settings.view_transform='Standard'
scene.view_settings.look='None'
scene.view_settings.exposure=-.15
scene.camera=beauty

# Export only character geometry, converting curves/modifiers to independent editable meshes.
for obj in list(bpy.data.objects):
    if obj.type=='CURVE':
        bpy.context.view_layer.objects.active=obj;obj.select_set(True)
        bpy.ops.object.convert(target='MESH');obj.select_set(False)
bpy.ops.object.select_all(action='DESELECT')
for colname,col in collections.items():
    if colname!='presentation':
        for obj in col.objects:obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'character-v01.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False,export_extras=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'character-v01.blend'))
for cam,name in [(front,'front'),(side,'side'),(back,'back'),(beauty,'three-quarter')]:
    key=bpy.data.objects['key'];key.location=cam.location+Vector((0,0,.25))
    key.rotation_euler=(Vector((0,0,.7))-key.location).to_track_quat('-Z','Y').to_euler()
    scene.camera=cam;scene.render.filepath=str(OUT/f'preview-{name}.png')
    bpy.ops.render.render(write_still=True)
stats={'status':'procedural_blockout_v01','reference':REF.name,'reference_sha256':scene['reference_sha256'],
       'vertices':sum(len(o.data.vertices) for o in bpy.data.objects if o.type=='MESH'),
       'polygons':sum(len(o.data.polygons) for o in bpy.data.objects if o.type=='MESH'),
       'mesh_objects':sum(o.type=='MESH' for o in bpy.data.objects),'rigged':False,'animations':False,
       'method':'reference-guided procedural modeling, not AI multi-view reconstruction',
       'limitations':['not final facial likeness','no production retopology','no UV texture atlas',
                      'no facial blendshapes','no deformation rig','no cloth/hair simulation']}
(OUT/'model-report.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
print(json.dumps(stats),flush=True)
# The standalone bpy wheel can fail during CPython module teardown on Windows.
# All exports and renders above must finish before this explicit headless exit.
sys.stdout.flush()
os._exit(0)
