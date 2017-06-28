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

        self.player = player

        self.frames = constants["rot_frames"]
        self.angle = constants["rot_angle"]
        self.radius = camera_config["radius"]
        self.phi = camera_config["phi"]
        self.theta = camera_config["theta"]
        self.moving = False
        self.rising = False
        self.move_speed = constants["side_length"] / self.frames

        self.center = [self.player.get_x(), self.player.get_y(), self.player.get_z()]

        # valor entero entre 0 y 3, cada número indica un distinto set de acciones para ejecutar
        self.orientation = 2

        self.place()

        self.counter = 0
        # boolean value: True means left, False means right
        self.direction = None
        self.move_direction = None

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
        if not self.moving:
            if self.counter > 0:
                self.phi += self.rot_spd_z
                self.counter -= 1
            if self.orientation == -1:
                self.orientation = 3
            elif self.orientation == 4:
                self.orientation = 0
        elif self.moving and not self.rising:
            if self.counter > 0:
                if self.move_direction == 0:
                    self.center[0] += self.move_speed
                elif self.move_direction == 1:
                    self.center[1] += self.move_speed
                elif self.move_direction == 2:
                    self.center[0] -= self.move_speed
                elif self.move_direction == 3:
                    self.center[1] -= self.move_speed
                self.counter -= 1
            if self.counter == 0:
                self.moving = False
        elif self.moving and self.rising:
            if self.counter > 0:
                if self.move_direction == 0:
                    self.center[0] += self.move_speed / 2
                    self.center[2] += self.move_speed / 2
                elif self.move_direction == 1:
                    self.center[1] += self.move_speed / 2
                    self.center[2] += self.move_speed / 2
                elif self.move_direction == 2:
                    self.center[0] -= self.move_speed / 2
                    self.center[2] += self.move_speed / 2
                elif self.move_direction == 3:
                    self.center[1] -= self.move_speed / 2
                    self.center[2] += self.move_speed / 2
                self.counter -= 1
            if self.counter == 0:
                self.moving = False
                self.rising = False

        if not self.player.is_moving():
            self.center = [self.player.get_x(), self.player.get_y(), self.player.get_z()]


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

    def move_x(self):
        self.counter += self.frames
        self.move_direction = 0
        self.moving = True

    def move_y(self):
        self.counter += self.frames
        self.move_direction = 1
        self.moving = True

    def move_neg_x(self):
        self.counter += self.frames
        self.move_direction = 2
        self.moving = True

    def move_neg_y(self):
        self.counter += self.frames
        self.move_direction = 3
        self.moving = True

    def rise_x(self):
        self.counter += self.frames * 2
        self.move_direction = 0
        self.moving = True
        self.rising = True

    def rise_y(self):
        self.counter += self.frames * 2
        self.move_direction = 1
        self.moving = True
        self.rising = True

    def rise_neg_x(self):
        self.counter += self.frames * 2
        self.move_direction = 2
        self.moving = True
        self.rising = True

    def rise_neg_y(self):
        self.counter += self.frames * 2
        self.move_direction = 3
        self.moving = True
        self.rising = True
