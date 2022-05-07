import bpy

#Setup of rendering
def mask_render_setup(normal_light, mask_light, wall_mesh):
    bpy.context.scene.render.image_settings.color_mode = 'BW'
    
    #Set background to black
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

    #Changing visibility of objects needed for masks
    normal_light.hide_render = True
    wall_mesh.hide_render = True
    mask_light.hide_render = False
    
#Back to normal setup
def normal_render_setup(normal_light, mask_light, wall_mesh):
    bpy.context.scene.render.image_settings.color_mode = 'RGB'
    
    #Set background to black
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.0508761, 0.0508761, 0.0508761, 1)

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

mask(bpy.data.objects["Light"], bpy.data.objects["Sun"], bpy.data.objects["Cube"], bpy.data.objects["Camera"], "C:\\Users\\nicol\\Documents\\Travail\\BE\\Masks\\test.png")