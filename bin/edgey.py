# coding: UTF-8

# imports
import json as json
from level_manager import Level
from presets import Player
from edgey_camera import EdgeyCamera
from pygltoolbox.glpython import *
from pygltoolbox.opengl_lib import *

# constants
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

config = config_dict["settings"]

clock = pygame.time.Clock()

# nivel
level = Level("maps/flat.json")

# crea y ubica al jugador en el nivel
player = Player()
player.place(level)

camera = EdgeyCamera(player)

axes = create_axes(10000)


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
            elif event.key == K_q:
                camera.gradual_rotateLeft()
            elif event.key == K_e:
                camera.gradual_rotateRight()
            elif event.key == K_w:
                player.move_up()
            elif event.key == K_s:
                player.move_down()
            elif event.key == K_a:
                player.move_left()
            elif event.key == K_d:
                player.move_right()

    keys = pygame.key.get_pressed()

    glDisable(GL_LIGHTING)
    glCallList(axes)
    glEnable(GL_LIGHTING)

    # actualiza camara
    camera.update()

    # actualiza modelos
    player.update()

    # dibuja luces
    glLightfv(GL_LIGHT0, GL_POSITION, [1000, 250, 1000])

    # dibuja mapa
    level.draw()

    # dibuja modelos
    player.draw()

    pygame.display.flip()
