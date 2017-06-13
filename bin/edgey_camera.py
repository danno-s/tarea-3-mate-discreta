# coding:UTF-8

import json as json
from pygltoolbox.camera import *
from pygltoolbox.utils_math import *


class EdgeyCamera():
    def __init__(self, player):
        # load configuration from json file
        with open("config.json") as config_file:
            config = json.load(config_file)

        camera_config = config["camera"]
        constants = config["constants"]

        self.frames = constants["rot_frames"]
        self.angle = constants["rot_angle"]
        self.radius = camera_config["radius"]
        self.phi = camera_config["phi"]
        self.theta = camera_config["theta"]

        self.center = [player.get_x(), player.get_y(), player.get_z()]

        # valor entero entre 0 y 3, cada número indica un distinto set de acciones para ejecutar
        self.orientation = 0

        self.place()

        self.counter = 0
        # boolean value: True means left, False means right
        self.direction = None

    def gradual_rotateLeft(self):
        if not self.direction:
            self.counter = self.frames - self.counter
        else:
            self.counter += self.frames
        self.rot_spd_z = self.angle / self.frames
        self.direction = True
        self.orientation -= 1

    def gradual_rotateRight(self):
        if self.direction:
            self.counter = self.frames - self.counter
        else:
            self.counter += self.frames
        self.rot_spd_z = -self.angle / self.frames
        self.direction = False
        self.orientation += 1

    def update(self):
        if self.counter > 0:
            self.phi += self.rot_spd_z
            self.counter -= 1
        if self.orientation == -1:
            self.orientation = 3
        elif self.orientation == 4:
            self.orientation = 0

    def place(self):
        glLoadIdentity()
        gluLookAt(self.radius * sin(self.theta) * cos(self.phi) + self.center[0],
                  self.radius * sin(self.theta) * sin(self.phi) + self.center[1],
                  self.radius * cos(self.theta) + self.center[2],
                  self.center[0],
                  self.center[1],
                  self.center[2],
                  0, 0, 1)

    def get_orientation(self):
        return self.orientation    
