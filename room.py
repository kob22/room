import bpy
import os



def create_plane_object(name, vertices, faces):
    """Creates a plane object from vertices and faces and return a BlendData object"""
    new_mesh = bpy.data.meshes.new(name)
    new_mesh.from_pydata(vertices, [], [faces])
    new_mesh.update()
    return bpy.data.objects.new(name, new_mesh)


def create_room(length, width, height):
    """Creates a room with given dimensions and returns 6 BlendData objects"""
    vertices = [(0, 0, 0), (0, width, 0), (length, width, 0), (length, 0, 0), (0, 0, height), (0, width, height), (length, width, height) , (length, 0, height)]
    floor = create_plane_object("Floor", vertices, [0, 1, 2, 3])
    ceiling = create_plane_object("Ceiling", vertices, [4, 5, 6, 7])

    wall_1 = create_plane_object("Wall 1", vertices, [0, 1, 5, 4])
    wall_2 = create_plane_object("Wall 2", vertices, [1, 2, 6, 5])
    wall_3 = create_plane_object("Wall 3", vertices, [2, 3, 7, 6])
    wall_4 = create_plane_object("Wall 4", vertices, [3, 0, 4, 7])
    return floor, ceiling, wall_1, wall_2, wall_3, wall_4


# blender scene
bpyscene = bpy.context.scene

# delete all objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# room dimensions
width = 40
length = 50
height = 24.5

# add camera in the corner
bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0.2, 13, 16), rotation=(1.43, 0, -1.48), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpyscene.camera = bpy.context.object

bpyscene.objects['Camera'].select

#camera zoom out
bpy.context.object.data.lens = 10

# create room
room = create_room(length, width, height)

# add room to the scene
for part in room:
    bpyscene.objects.link(part)

# Add lights in the corners
bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(0, 0, height), rotation=(0.45, -0.8, 0))
bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(0, width, height), rotation=(-0.45, -0.8, 0))

# Render settings
bpyscene.render.image_settings.color_mode = 'RGBA'
bpyscene.render.image_settings.file_format = 'PNG'
bpyscene.render.filepath = os.path.join(os.path.dirname(os.path.abspath((__file__))), 'room')
bpy.ops.render.render(write_still= True)
