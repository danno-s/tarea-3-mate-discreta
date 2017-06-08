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

clock = pygame.time.Clock()

# objetos
axes = create_axes(AXES_LENGTH)
camera = CameraR(CAMERA_RAD, CAMERA_PHI, CAMERA_THETA)

while(True):
    clock.tick(FPS)
    camera.place()

    # eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    pygame.display.flip()
