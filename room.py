import bpy
import os


def create_plane_object(name, vertices, faces):
    """Creates a plane object from vertices and faces and return a BlendData object"""
    # new object type BlendData Mesh
    new_mesh = bpy.data.meshes.new(name)
    # make mesh from list vertices and faces
    new_mesh.from_pydata(vertices, [], [faces])
    # update
    new_mesh.update()
    return bpy.data.objects.new(name, new_mesh)


def create_room(length, width, height):
    """Creates a room with given dimensions and returns 6 BlendData objects"""
    # Room vertices
    vertices = [(0, 0, 0), (0, width, 0), (length, width, 0), (length, 0, 0), (0, 0, height), (0, width, height), (length, width, height) , (length, 0, height)]

    # creates room planes
    floor = create_plane_object("Floor", vertices, [0, 1, 2, 3])
    ceiling = create_plane_object("Ceiling", vertices, [4, 5, 6, 7])

    wall_1 = create_plane_object("Wall 1", vertices, [0, 1, 5, 4])
    wall_2 = create_plane_object("Wall 2", vertices, [1, 2, 6, 5])
    wall_3 = create_plane_object("Wall 3", vertices, [2, 3, 7, 6])
    wall_4 = create_plane_object("Wall 4", vertices, [3, 0, 4, 7])

    return floor, ceiling, wall_1, wall_2, wall_3, wall_4


def add_lamp(scene, name, type, size, color, location, rotation):
    """Creates a lamp (lamp name, type, location, rotation) at given location on the scene"""
    # create lamp
    new_lamp = bpy.data.lamps.new(name, type)
    # size lamp
    new_lamp.size = size
    # color
    new_lamp.color = color
    # create blender object
    lamp_obj = bpy.data.objects.new(name, new_lamp)
    # set location and rotation
    lamp_obj.location = location
    lamp_obj.rotation_euler = rotation
    # link to the scene
    scene.objects.link(lamp_obj)
    return lamp_obj


def add_camera(scene, name, lens,  location, rotation):
    """Creates new came at given location on the scene"""
    new_camera = bpy.data.cameras.new(name)
    # camera lens(zoom)
    new_camera.lens = lens
    # create blender camera obj
    camera_obj = bpy.data.objects.new(name, new_camera)
    # add to the scene
    scene.objects.link(camera_obj)
    # set location and rotation camera
    camera_obj.location = location
    camera_obj.rotation_euler = rotation

    return camera_obj


def create_material(name, color, alpha):
    """Create material with color"""
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    material.alpha = alpha
    return material


def set_material(object, material):
    """Set material at object"""
    obj_data = object.data
    obj_data.materials.append(material)


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
room = create_room(length, width, height)

# add room to the scene
for part in room:
    bpyscene.objects.link(part)


# Add lights in the corners
# bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(0, 0, height-1), rotation=(0.45, -0.8, 0))
# bpy.ops.object.lamp_add(type='HEMI', view_align=False, location=(0, width, height-1), rotation=(-0.45, -0.8, 0))
# add_lamp(bpyscene, 'LAMP1', 'HEMI', energy=0.5, color=(1, 0.89, 0.6), location=(0, 0, height-1), rotation=(1, -0.8, 0))
# add_lamp(bpyscene, 'LAMP2', 'HEMI', energy=0.5, color=(1, 0.89, 0.6), location=(0, width, height-1), rotation=(-1, -0.8, 0))
# add lights as a window from wall
add_lamp(bpyscene, 'LAMP1', 'AREA', color=(1, 1, 1), size=1.5, location=(0.01, width/2, height -1), rotation=(0,-1.43, 0))

# add cameras
# list of existing cameras
list_cameras = []
# bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0.2, 13, 16), rotation=(1.43, 0, -1.48), )
cam1 = add_camera(bpyscene, 'CAMERA1', 10, location=(0.2, 1.3, 1.6), rotation=(1.43, 0, -1.48))
cam2 = add_camera(bpyscene, 'CAMERA2', 10, location=(2.2, 2.2, 1.6), rotation=(1.40, 0, -1.96))
list_cameras.append(cam1.name)
list_cameras.append(cam2.name)


# walls color
walls_color = create_material('wild_grey', color=(0.174647, 0.212231, 0.234551), alpha=1 )
for i in range(1,5):
    set_material(bpyscene.objects['Wall ' + str(i)], walls_color)
#ceiling color
ceiling_color = create_material('white', color=(1, 1, 1), alpha=1)
set_material(bpyscene.objects['Ceiling'], ceiling_color)

# floor color
floor_color = create_material(('brown'), color=(0.235, 0.069, 0), alpha=1)
set_material(bpyscene.objects['Floor'], floor_color)


g = list(bpyscene.objects)
# Render settings
bpyscene.render.image_settings.color_mode = 'RGBA'
bpyscene.render.image_settings.file_format = 'PNG'
#bpyscene.cycles.samples = 10
# render scene
for cam in list_cameras:
    # set CAMERAX as a active camera for render
    bpyscene.camera = bpyscene.objects[cam]
    # file path for render
    bpyscene.render.filepath = os.path.join(os.path.dirname(os.path.abspath((__file__))), 'room_'+cam)
    # render to file
    bpy.ops.render.render(write_still= True)
