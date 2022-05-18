import bpy
import math
from mathutils import Vector, Matrix
from random import randrange, uniform


#Paramètres

#Format de l'image
bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 768
bpy.context.scene.render.image_settings.file_format = 'JPEG'

#Paramètres des sphères
ballSize = .061 #Taille (en mm)
nbSphere = 100 #Nombre max à afficher
sphereColorMode = "" #Choix des couleurs: par défaut(toutes blanches), allSame(toutes de la même couleur), allDifferent(toutes d'une couleur différente)
sphereNbMode = "" #Choix du nombre de sphères à afficher: par défaut(au hasard), smallWeightedWithNone(plus grande proba d'avoir peu de sphères,voire pas du tout),
                  #                                       smallWeighted(plus grande proba d'avoir peu de sphères), bigWeighted(plus grande proba d'avoir bcp de sphères)

#Paramètres de la scène
nomCamera = "Camera"
nomMur = "Cube" #Nom de l'objet de référence, par défaut "Cube", à changer par le nom de l'objet voulu

#Paramètres d'enregistrement
filePath = "C:\\Users\\nicol\\Documents\\Travail\\BE\\test\\" #Filepath, à modifier
imageBatchSize = 1 #Nombre d'images à créer par lancement de script
nbImageMax = 100000 #Nombre d'images total à créer (pour la numérotation des images)
numeroDebut = 0 #Numéro de la première image

#-----------------------------------------------------------------------------------

#Utilitaires


def distance(point1: Vector, point2: Vector) -> float:
    return (point2 - point1).length

#Supprime l'objet obj
def delete(obj):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.delete()
    
#Cache l'objet obj
def hide(obj):
    obj.hide_viewport = True
    obj.hide_render = True
    
#Cache tous les objets de la liste objList
def hideAll(objList):
    for obj in objList:
        hide(obj)
    
#Montre l'objet obj
def show(obj):
    obj.hide_viewport = False
    obj.hide_render = False
    
#Montre tous les objets de la liste objList
def showAll(objList):
    for obj in objList:
        show(obj)
        
#Nettoie la scène et la data de tous les objets sauf la caméra et la paroi
def cleanup():
    for obj in bpy.data.objects:
        if obj.name not in [nomCamera, nomMur]:
            show(obj)
            obj.select_set(True)
    bpy.ops.object.delete()
    for mesh in bpy.data.meshes:
        if mesh.name != nomMur:
            bpy.data.meshes.remove(mesh)
    for mat in bpy.data.materials:
        if mat.name not in bpy.data.objects[nomMur].data.materials:
            bpy.data.materials.remove(mat)
    for light in bpy.data.lights:
        bpy.data.lights.remove(light)
        
#Retourne le nombre de sphères à afficher
def nbSphAffichees(nbSpheresMax, mode):
    if nbSpheresMax == 1:
        return 1
    elif mode == "smallWeightedWithNone":
        return int(round(1/(randrange(1, nbSpheresMax)*3/nbSpheresMax)))
    elif mode == "smallWeighted":
        return int(round(1/(randrange(1, nbSpheresMax)*2/nbSpheresMax)))
    elif mode == "bigWeighted":
        return nbSpheresMax - int(round(1/(randrange(1, nbSpheresMax)*2/nbSpheresMax)))
    else:
        return randrange(1,nbSpheresMax)
    
#Numérote les images
def numbering(i, numeroDebut, nbImageMax):
    return str(i+numeroDebut).zfill(math.ceil(math.log10(nbImageMax)))

#Sélectionne la caméra et fait le rendu
def cam_and_render(camera, filepath):
    bpy.context.scene.camera = camera
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)
        
#-----------------------------------------------------------------------------------
    
#Création de la scène


#Crée une lumière qui éclaire vers le point point    
def createLight(point):
    data = bpy.data.lights.new(name="Light", type='AREA')
    data.energy = 1000
    light = bpy.data.objects.new(name="Light source",object_data=data)
    bpy.context.collection.objects.link(light)
    constraint = light.constraints.new(type='TRACK_TO')
    constraint.target = point
    return light

#Crée un point
def createPoint():
    bpy.ops.object.empty_add() 
    point = bpy.context.selected_objects[0]
    return point

#Crée nbSphere de nom nameSphere et de taille sphereSize
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

#Place la sphère sphere sur le plan plane
def placeSphereOnPlane(sphere,plane):
    xsca = plane.scale[0]
    ysca = plane.scale[1]
    vec = Vector((uniform(xsca, -xsca), uniform(ysca, -ysca), 0))
    sphere.location = plane.matrix_world @ vec
    return sphere

#Place la lumière light de façon aléatoire derrière la caméra caméra
def placeLightBehindCamera(camera,light):
    light.location = camera.matrix_world @ Vector((uniform(-5,5),uniform(-5,5),.1))
    return light


def castRayCamera(camera):
    origin = camera.location
    dest = (camera.matrix_world @ Vector((0,0,-1))) - origin
    (result,location,normal,index,light,matrix) = bpy.context.scene.ray_cast(bpy.context.view_layer.depsgraph,origin,dest)
    return(result,location)

#Place un plan à une distance de la caméra
def planeFromCamera(camera,dist):
    scale = (dist * 0.36, dist * .2025, 1)
    bpy.ops.mesh.primitive_plane_add(
        location = camera.matrix_world @ Vector((0,0,-dist)),
        rotation = camera.rotation_euler
    )
    bpy.context.selected_objects[0].scale = scale
    return bpy.context.selected_objects[0]

#Construit la scène à partir des fonctions précedentes et nettoie les sphères qui se superposent
def sceneBuildUp(globalSphereList,camera,light,point):
    (result,localisation) = castRayCamera(camera)
    if result == True and len(globalSphereList) > 0:
        hideAll(globalSphereList)
        point.location = localisation
        dist = distance(localisation, camera.location)
        plane = planeFromCamera(camera, uniform(max(.25*dist,2),.75*dist))
        sphereList = []
        for i in range(nbSphAffichees(len(globalSphereList), sphereNbMode)):
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

#-----------------------------------------------------------------------------------

#Crée la lumière qui sert à faire le masque
def createMaskLight(point):
    data = bpy.data.lights.new(name="Light", type='SUN')
    data.energy = 1000000000
    light = bpy.data.objects.new(name="Mask Light",object_data=data)
    bpy.context.collection.objects.link(light)
    constraint = light.constraints.new(type='TRACK_TO')
    constraint.target = point
    hide(light)
    return light

#Prépare la scène pour faire le rendu du masque
def mask_render_setup(normal_light, mask_light, wall_mesh):
    bpy.context.scene.render.image_settings.color_mode = 'BW'    

    #Changing visibility of objects needed for masks
    normal_light.hide_render = True
    wall_mesh.hide_render = True
    mask_light.hide_render = False
    
#Prépare la scène pour le rendu de base
def normal_render_setup(normal_light, mask_light, wall_mesh):
    bpy.context.scene.render.image_settings.color_mode = 'RGB'

    #Changing visibility of objects needed for masks
    normal_light.hide_render = False
    wall_mesh.hide_render = False
    mask_light.hide_render = True

#Main du masque
def mask(normal_light, mask_light, wall_mesh, camera, filepath):
    mask_render_setup(normal_light, mask_light, wall_mesh)
    cam_and_render(camera, filepath)
    normal_render_setup(normal_light, mask_light, wall_mesh)

#-----------------------------------------------------------------------------------

#Affecte les couleurs aux sphères
def colorSetup(objList):
    main_mat = bpy.data.materials.new("Main Material")
    for i in range(0, len(objList)):
        new_mat = bpy.data.materials.new("Material"+str(i))
    return objList

#Change les couleurs des sphères en fonction du mode choisi
def colo(objList, mode):
    if mode == "allSame":
        material = bpy.data.materials["Main Material"]
        material.use_nodes = True
        material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (randRGB(), randRGB(), randRGB(), 1)
        for obj in objList:
            obj.active_material = material
            
    elif mode == "allDifferent":
        for obj in objList:
            material = bpy.data.materials["Material"+str(objList.index(obj))] 
            material.use_nodes = True
            material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (randRGB(), randRGB(), randRGB(), 1)
            obj.active_material = material
    return mode
         
#Random pour la séléction des couleurs   
def randRGB():
    return randrange(0,101)/100

#-----------------------------------------------------------------------------------

def main():
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
    
    camera = bpy.context.scene.objects.get(nomCamera)
    wall = bpy.context.scene.objects.get(nomMur)
    point = createPoint()
    light = createLight(point)
    maskLight = createMaskLight(point)
    maskLight.location = camera.matrix_world @ Vector((0,0,.1))
    
    listSphere = createSphereBatch(nbSphere,"Ball",ballSize)
    colorSetup(listSphere)

    for i in range (imageBatchSize):
        sceneBuildUp(listSphere,camera,light,point)
        colo(listSphere, sphereColorMode)
        pathImage = filePath + "im_"+numbering(i,numeroDebut,nbImageMax)
        cam_and_render(camera,pathImage)
        pathMask = filePath + "im_"+numbering(i,numeroDebut,nbImageMax)+"_mk"
        mask(light,maskLight,wall,camera,pathMask)
    cleanup()
    
#-----------------------------------------------------------------------------------

main()