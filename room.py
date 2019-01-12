import bpy
import os

from room_objects import *
from other_objects import *
from materials import *

# blender scene
bpyscene = bpy.context.scene
bpyscene.render.engine = 'CYCLES'

# delete all objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# room dimensions
width = 4
length = 5
height = 2.5


# create room
room = create_room(length, width, height, bpyscene)


# Add lights in the corners
# bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(0, 0, height-1), rotation=(0.45, -0.8, 0))
# bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(0, width, height-1), rotation=(-0.45, -0.8, 0))
# add_lamp(bpyscene, 'LAMP1', 'HEMI', energy=0.5, color=(1, 0.89, 0.6), location=(0, 0, height-1), rotation=(1, -0.8, 0))
# add_lamp(bpyscene, 'LAMP2', 'HEMI', energy=0.5, color=(1, 0.89, 0.6), location=(0, width, height-1), rotation=(-1, -0.8, 0))
# add lights as a window from wall
add_lamp(bpyscene, 'LAMP1', 'AREA', color=(1, 1, 1), size=1.5, location=(0.01, width/2, height -1), rotation=(0,-1.43, 0))
add_lamp(bpyscene, 'LAMP2', 'AREA', color=(1, 1, 1), size=1.5, location=(length/2, width-0.2, height -1), rotation=(-1,-1.43, 0))



# walls color
walls_color = create_material('wild_grey', color=(0.174647, 0.212231, 0.234551), alpha=1 )
for i in range(1,5):
    set_material(bpyscene.objects['Wall ' + str(i)], walls_color)
#ceiling color
white_material = create_material('white', color=(1, 1, 1), alpha=1)
set_material(bpyscene.objects['Ceiling'], white_material)

# floor color
floor_color = create_material(('brown'), color=(0.235, 0.069, 0), alpha=1)
set_material(bpyscene.objects['Floor'], floor_color)

# set table
create_table('Table', bpyscene, location=(3.8, 0.5, 0.4), scale=(0.4, 0.4, 0.4))
table_color = create_material(('dark brwon'), color=(0.2, 0.1, 0), alpha=1)
set_material(bpyscene.objects['Table'], table_color)

# create chairs and set colors
create_chair('Chair 1', bpyscene, location=(4.5, 2.1, 0.3), scale=(0.4, 0.4, 0.4), rotation=(0, 0, -3.8))
create_chair('Chair 2', bpyscene, location=(3.1, 0.7, 0.3), scale=(0.4, 0.4, 0.4), rotation=(0, 0, -0.95))
set_material(bpyscene.objects['Chair 1'], white_material)
set_material(bpyscene.objects['Chair 2'], white_material)


# add cameras
# list of existing cameras
list_cameras = []
# bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0.2, 13, 16), rotation=(1.43, 0, -1.48), )
cam1 = add_camera(bpyscene, 'CAMERA1', 10, location=(0.2, 1.3, 1.6), rotation=(1.43, 0, -1.48))
cam2 = add_camera(bpyscene, 'CAMERA2', 10, location=(2.2, 2.2, 0.74), rotation=(1.57, 0, -2.05))
list_cameras.append(cam1.name)
list_cameras.append(cam2.name)


# Render settings
bpyscene.render.image_settings.color_mode = 'RGBA'
bpyscene.render.image_settings.file_format = 'PNG'
bpyscene.cycles.samples = 10

bpy.context.scene.cycles.film_transparent = True
# render scene
for cam in list_cameras:
    # set CAMERAX as a active camera for render
    bpyscene.camera = bpyscene.objects[cam]
    # file path for render
    bpyscene.render.filepath = os.path.join(os.path.dirname(os.path.abspath((__file__))), 'room_'+cam)
    # render to file
    bpy.ops.render.render(write_still= True)
