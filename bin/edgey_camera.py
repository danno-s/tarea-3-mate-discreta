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
        radius = camera_config["radius"]
        phi = camera_config["phi"]
        theta = camera_config["theta"]

        self.center = player

        self.camera = CameraR(radius, phi, theta)
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

    def gradual_rotateRight(self):
        if self.direction:
            self.counter = self.frames - self.counter
        else:
            self.counter += self.frames
        self.rot_spd_z = -self.angle / self.frames
        self.direction = False

    def update(self):
        if self.counter > 0:
            self.camera.rotateZ(self.rot_spd_z)
            self.counter -= 1

    def place(self):
        self.camera.place()

    def __str__(self):
        return str(self.camera)
