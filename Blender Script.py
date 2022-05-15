import bpy
import math
from mathutils import Vector, Matrix
from random import randrange, uniform
context = bpy.context
scene = context.scene
vl = context.view_layer.depsgraph
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
bpy.context.scene.render.image_settings.file_format = 'JPEG'
bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 768


ballSize = .061
nbSphere = 100
nbImage = 100
filePath = "C:\\Users\\nicol\\Documents\\Travail\\BE\\rendus\\"
nomCamera = "Camera"
nomMur = "08_MAMMOUTHS_HQ"
nbImageMax = 100000
numeroDebut = 200

def distance(point1: Vector, point2: Vector) -> float:
    return (point2 - point1).length

def delete(obj):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.delete()
    
def hide(obj):
    obj.hide_viewport = True
    obj.hide_render = True
    
def hide_all(objList):
    for obj in objList:
        hide(obj)
    
def show(obj):
    obj.hide_viewport = False
    obj.hide_render = False
    
def show_all(objList):
    for obj in objList:
        show(obj)
    
def createMaskLight(point):
    data = bpy.data.lights.new(name="Light", type='SUN')
    data.energy = 1000000000
    light = bpy.data.objects.new(name="Mask Light",object_data=data)
    bpy.context.collection.objects.link(light)
    constraint = light.constraints.new(type='TRACK_TO')
    constraint.target = point
    hide(light)
    return light
    
def createLight(point):
    data = bpy.data.lights.new(name="Light", type='AREA')
    data.energy = 1000
    light = bpy.data.objects.new(name="Light source",object_data=data)
    bpy.context.collection.objects.link(light)
    constraint = light.constraints.new(type='TRACK_TO')
    constraint.target = point
    return light

def createPoint():
    bpy.ops.object.empty_add() 
    point = bpy.context.selected_objects[0]
    return point

def createSphereBatch(nbSphere,nameSphere,sphereSize):
    sphereList = []
    for i in range (nbSphere):
        bpy.ops.mesh.primitive_uv_sphere_add(
            scale=(sphereSize, sphereSize, sphereSize)
        )
        newSphere = bpy.context.selected_objects[0]
        if nameSphere != "":
            newSphere.name = nameSphere
        for f in newSphere.data.polygons:
            f.use_smooth = True
        sphereList.append(newSphere)
    return sphereList

def placeSphereOnPlane(sphere,plane):
    xsca = plane.scale[0]
    ysca = plane.scale[1]
    vec = Vector((uniform(xsca, -xsca), uniform(ysca, -ysca), 0))
    sphere.location = plane.matrix_world @ vec
    return sphere

def placeLightBehindCamera(camera,light):
    light.location = camera.matrix_world @ Vector((uniform(-5,5),uniform(-5,5),.1))
    return light

def castRayCamera(camera):
    origin = camera.location
    dest = (camera.matrix_world @ Vector((0,0,-1))) - origin
    (result,location,normal,index,light,matrix) = scene.ray_cast(vl,origin,dest)
    return(result,location)

def planeFromCamera(camera,dist):
    scale = (dist * 0.36, dist * .2025, 1)
    bpy.ops.mesh.primitive_plane_add(
        location = camera.matrix_world @ Vector((0,0,-dist)),
        rotation = camera.rotation_euler
    )
    bpy.context.selected_objects[0].scale = scale
    return bpy.context.selected_objects[0]

def sceneBuildUp(globalSphereList,camera,light,point):
    (result,localisation) = castRayCamera(camera)
    if result == True and len(globalSphereList) > 0:
        hide_all(globalSphereList)
        point.location = localisation
        dist = distance(localisation, camera.location)
        plane = planeFromCamera(camera, uniform(max(.25*dist,2),.75*dist))
        sphereList = []
        #randomCap = int(math.log(uniform(1,math.exp(nbSphere))))
        for i in range(min(randomCap(nbSphere),len(globalSphereList))):
            sphere = placeSphereOnPlane(globalSphereList[i],plane)
            show(sphere)
            sphereList.append(sphere)
        delete(plane)
        #check if spheres overlaps
        if (len(sphereList) > 1):
            i = 1
            while (i< len(sphereList)):
                hideCheck = False
                for j in range (i) :
                    if (i != j and (distance(sphereList[i].location,sphereList[j].location) < 2.2*ballSize) 
                        and not hideCheck):
                        hideCheck = True
                #if the object overlaps with a higher priority object, hides it
                if hideCheck:
                    sphere = sphereList[i]
                    del(sphereList[i])
                    hide(sphere)
                #if the object doesn't overlap, then we move on to the next one
                else:
                    i+=1
        placeLightBehindCamera(camera,light)
        return sphereList
    return None 

def cleanup():
    for obj in bpy.data.objects:
        if obj.name not in [nomCamera, nomMur]:
            show(obj)
            obj.select_set(True)
    bpy.ops.object.delete()
    for mesh in bpy.data.meshes:
        if mesh.name != nomMur:
            bpy.data.meshes.remove(mesh)
    
            
def randomCap(nbSpheres):
    if nbSpheres == 1:
        return 1
    rnd = randrange(1, nbSpheres)*2/nbSpheres
    return int(round(1/rnd))

def numbering(i, numeroDebut, nbImageMax):
    return str(i+numeroDebut).zfill(math.ceil(math.log10(nbImageMax)))

#-----------------------------------------------------------------------------------

def mask_render_setup(normal_light, mask_light, wall_mesh):
    bpy.context.scene.render.image_settings.color_mode = 'BW'    

    #Changing visibility of objects needed for masks
    normal_light.hide_render = True
    wall_mesh.hide_render = True
    mask_light.hide_render = False
    
#Back to normal setup
def normal_render_setup(normal_light, mask_light, wall_mesh):
    bpy.context.scene.render.image_settings.color_mode = 'RGB'

    #Changing visibility of objects needed for masks
    normal_light.hide_render = False
    wall_mesh.hide_render = False
    mask_light.hide_render = True
    
#Camera selection and rendering
def cam_and_render(camera, filepath):
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)

#Main
def mask(normal_light, mask_light, wall_mesh, camera, filepath):
    mask_render_setup(normal_light, mask_light, wall_mesh)
    cam_and_render(camera, filepath)
    normal_render_setup(normal_light, mask_light, wall_mesh)

#-----------------------------------------------------------------------------------


point = createPoint()
light = createLight(point)
maskLight = createMaskLight(point)
camera = scene.objects.get(nomCamera)
maskLight.location = camera.matrix_world @ Vector((0,0,.1))
wall = scene.objects.get(nomMur)
listSphere = createSphereBatch(nbSphere,"Ball",ballSize)
for i in range (nbImage):
    sceneBuildUp(listSphere,camera,light,point)
    pathImage = filePath + "im_"+numbering(i,numeroDebut,nbImageMax)
    cam_and_render(camera,pathImage)
    pathMask = filePath + "im_"+numbering(i,numeroDebut,nbImageMax)+"_mk"
    mask(light,maskLight,wall,camera,pathMask)
cleanup()