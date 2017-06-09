# coding:UTF-8

from pygltoolbox.camera import *
import json as json
from pprint import pprint


class EdgeyCamera():
    def __init__(self):
        # load configuration from json file
        with open("config.json") as config_file:
            config = json.load(config_file)

        self.camera_config = config["camera"]

        self.frames = self.camera_config["rot_frames"]
        self.angle = self.camera_config["rot_angle"]

        self.camera = CameraR(1700.0, 45, 56)
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
