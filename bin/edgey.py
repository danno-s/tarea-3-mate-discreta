# coding: UTF-8

# imports
import json as json
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
FPS = 60
NUM_LIGHTS = 2
WINDOW_SIZE = [1280, 720]

# init
initPygame(WINDOW_SIZE[0], WINDOW_SIZE[1], "Edgey", centered=True)
initGl(transparency=False, materialcolor=False, normalized=True, lighting=True,
       numlights=1,
       perspectivecorr=True, antialiasing=True, depth=True, smooth=True,
       texture=True, verbose=False)
glutInit()
reshape(*WINDOW_SIZE)
initLight(GL_LIGHT0)

with open("config.json") as json_config:
    config_dict = json.load(json_config)

config = config_dict["config"]

clock = pygame.time.Clock()

# objetos
axes = create_axes(AXES_LENGTH)
camera = EdgeyCamera()

cubo = Particle(posz=100.0)
cubo.add_property("GLLIST", create_cube([255, 0, 0, 1]))
cubo.add_property("SIZE", [40, 40, 40])
cubo.add_property("MATERIAL", material_red_plastic)
cubo.set_name("Cubo")

# nivel
level = Level("maps/basic.json")
tilemap = level.get_tilemap()

print "Main loop started"

while(True):
    clock.tick(FPS)
    clearBuffer()
    camera.place()

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
                camera.gradual_rotateLeft()
            if event.key == K_e:
                camera.gradual_rotateRight()

    # actualiza camara
    camera.update()
    if islightEnabled():
        glDisable(GL_LIGHTING)
        glCallList(axes)
        glEnable(GL_LIGHTING)
    else:
        glCallList(axes)

    # actualiza modelos
    cubo.update

    # dibuja luces
    glLightfv(GL_LIGHT0, GL_POSITION, [1000, 250, 1000])

    # dibuja mapa
    for row, i in enumerate(tilemap):
        for column, j in enumerate(tilemap[row]):
            for height, z in enumerate(tilemap[row][column]):
                if tilemap[row][column][height] is not None:
                    tilemap[row][column][height].exec_property_func("MATERIAL")
                    draw_list(tilemap[row][column][height].get_property("GLLIST"),
                              tilemap[row][column][height].get_position_list(),
                              0,
                              None,
                              tilemap[row][column][height].get_property("SIZE"),
                              None)

    # dibuja modelos
    cubo.exec_property_func("MATERIAL")
    draw_list(cubo.get_property("GLLIST"), cubo.get_position_list(), 0, None, cubo.get_property("SIZE"), None)

    pygame.display.flip()
