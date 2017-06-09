# coding: UTF-8

# imports
from pygltoolbox.glpython import *
from pygltoolbox.opengl_lib import *
from pygltoolbox.camera import *
from pygltoolbox.particles import *
from pygltoolbox.figures import *
from pygltoolbox.materials import *
from pygltoolbox.textures import *
from pygltoolbox.shader import *
from level_manager import Level
from edgey_camera import EdgeyCamera

# constants
AXES_LENGTH = 700
CAMERA_PHI = 45
CAMERA_RAD = 1700.0
CAMERA_ROT_VEL = 2.5
CAMERA_THETA = 56
FPS = 60
NUM_LIGHTS = 2
WINDOW_SIZE = [1280, 720]

# init
initPygame(WINDOW_SIZE[0], WINDOW_SIZE[1], "Edgey", centered=True)
initGl()
glutInit()
reshape(*WINDOW_SIZE)

clock = pygame.time.Clock()

# objetos
axes = create_axes(AXES_LENGTH)
camera = EdgeyCamera()

cubo = Particle(posz=100.0)
cubo.add_property("GLLIST", create_cube())
cubo.add_property("SIZE", [40, 40, 40])
cubo.set_name("Cubo")

cubo1 = Particle(posx=100.0, posz=100.0)
cubo1.add_property("GLLIST", create_cube())
cubo1.add_property("SIZE", [40, 40, 40])
cubo1.set_name("Cubo1")


# nivel
level = Level("maps/basic")
tilemap = level.get_tilemap()

print "Main loop start"
while(True):
    clock.tick(FPS)
    clearBuffer()
    camera.place()

    glCallList(axes)

    draw_list(cubo.get_property("GLLIST"), cubo.get_position_list(), 0, None, cubo.get_property("SIZE"), None)
    draw_list(cubo1.get_property("GLLIST"), cubo1.get_position_list(), 0, None, cubo1.get_property("SIZE"), None)

    for row, i in enumerate(tilemap):
        for column, j in enumerate(tilemap[row]):
            for height, z in enumerate(tilemap[row][column]):
                if tilemap[row][column][height] is not None:
                    draw_list(tilemap[row][column][height].get_property("GLLIST"), tilemap[row][column][height].get_position_list(), 0, None, tilemap[row][column][height].get_property("SIZE"), None)

    # eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            if event.key == K_s:
                print str(camera)
            if event.key == K_q:
                print "rotating camera"
                camera.gradual_rotateLeft()
            if event.key == K_e:
                print "rotating camera"
                camera.gradual_rotateRight()

    camera.update()

    pygame.display.flip()
