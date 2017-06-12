# coding: UTF-8
from pygltoolbox.particles import *
from pygltoolbox.figures import *
from pygltoolbox.materials import *
import json as json


class Player():
    def __init__(self):
        with open("config.json") as config:
            self.constants = json.load(config)["constants"]

        self.side_length = self.constants["side_length"]

        self.move_frames = self.constants["move_frames"]

        self.move_speed = 90 / self.move_frames
        self.counter = 0
        self.rot_spd = 0
        self.rot_progress = 0
        # booleano
        self.move_axis = None
        self.direction = None

        self.figure = Particle()
        self.figure.add_property("GLLIST", create_cube())
        self.figure.add_property("SIZE", [self.side_length / 2, self.side_length / 2, self.side_length / 2])
        self.figure.add_property("MATERIAL", material_red_plastic)
        self.figure.set_name("Jugador")

    def place(self, level):
        tilemap = level.tilemap
        # busca casilla donde comienza el jugador
        for row, i in enumerate(tilemap):
            for column, j in enumerate(tilemap[row]):
                for height, z in enumerate(tilemap[row][column]):
                    if tilemap[row][column][height] is not None:
                        # si es el spawn, ubica en las mismas coordenadas una altura más arriba
                        if tilemap[row][column][height].get_name() == "Spawn":
                            self.figure.set_x(tilemap[row][column][height].get_x())
                            self.figure.set_y(tilemap[row][column][height].get_y())
                            self.figure.set_z(tilemap[row][column][height].get_z() + self.side_length)

    def update(self):
        self.figure.update()
        if self.counter > 0:
            self.counter -= 1
            self.rot_progress += self.rot_spd
        if self.counter == 0:
            self.rot_progress = 0
            if self.move_axis is not None and self.direction is not None:
                if self.move_axis and self.direction:
                    self.add_y(-self.side_length)
                elif self.move_axis and not self.direction:
                    self.add_y(self.side_length)
                elif not self.move_axis and self.direction:
                    self.add_x(self.side_length)
                elif not self.move_axis and not self.direction:
                    self.add_x(-self.side_length)
            self.move_axis = None
            self.direction = None

    def add_x(self, x):
        self.figure.set_x(self.get_x() + x)

    def add_y(self, y):
        self.figure.set_y(self.get_y() + y)

    def add_z(self, z):
        self.figure.set_z(self.get_z() + z)

    def get_x(self):
        return self.figure.get_x()

    def get_y(self):
        return self.figure.get_y()

    def get_z(self):
        return self.figure.get_z()

    def draw(self):
        if self.counter > 0:
            if self.move_axis and self.direction:
                glTranslatef(self.get_x(),
                             self.get_y() - self.side_length / 2,
                             self.get_z() - self.side_length / 2)

                glRotatef(self.rot_progress, 1, 0, 0)

                glTranslatef(-self.get_x(),
                             -self.get_y() + self.side_length / 2,
                             -self.get_z() + self.side_length / 2)
            elif self.move_axis and not self.direction:
                glTranslatef(self.get_x(),
                             self.get_y() + self.side_length / 2,
                             self.get_z() - self.side_length / 2)

                glRotatef(self.rot_progress, 1, 0, 0)

                glTranslatef(-self.get_x(),
                             -self.get_y() - self.side_length / 2,
                             -self.get_z() + self.side_length / 2)
            elif not self.move_axis and self.direction:
                glTranslatef(self.get_x() + self.side_length / 2,
                             self.get_y(),
                             self.get_z() - self.side_length / 2)

                glRotatef(self.rot_progress, 0, 1, 0)

                glTranslatef(-self.get_x() - self.side_length / 2,
                             -self.get_y(),
                             -self.get_z() + self.side_length / 2)
            elif not self.move_axis and not self.direction:
                glTranslatef(self.get_x() - self.side_length / 2,
                             self.get_y(),
                             self.get_z() - self.side_length / 2)

                glRotatef(self.rot_progress, 0, 1, 0)

                glTranslatef(-self.get_x() + self.side_length / 2,
                             -self.get_y(),
                             -self.get_z() + self.side_length / 2)
        self.figure.exec_property_func("MATERIAL")
        draw_list(self.figure.get_property("GLLIST"),
                  self.figure.get_position_list(),
                  0, None, self.figure.get_property("SIZE"), None)

    def move_up(self):
        if self.move_axis is None or self.move_axis:
            self.move_axis = True
            if not self.direction:
                self.counter = self.move_frames - self.counter
            else:
                self.counter += self.move_frames
            self.rot_spd = self.move_speed
            self.direction = True

    def move_down(self):
        if self.move_axis is None or self.move_axis:
            self.move_axis = True
            if self.direction:
                self.counter = self.move_frames - self.counter
            else:
                self.counter += self.move_frames
            self.rot_spd = -self.move_speed
            self.direction = False

    def move_left(self):
        if self.move_axis is None or not self.move_axis:
            self.move_axis = False
            if not self.direction:
                self.counter = self.move_frames - self.counter
            else:
                self.counter += self.move_frames
            self.rot_spd = self.move_speed
            self.direction = True

    def move_right(self):
        if self.move_axis is None or not self.move_axis:
            self.move_axis = False
            if self.direction:
                self.counter = self.move_frames - self.counter
            else:
                self.counter += self.move_frames
            self.rot_spd = -self.move_speed
            self.direction = False


class BasicTile:
    def __init__(self, row, column, level, side_length):
        self.tile = Particle(row * side_length, column * side_length, level * side_length)
        self.tile.add_property("GLLIST", create_cube())
        self.tile.add_property("SIZE", [side_length / 2, side_length / 2, side_length / 2])
        self.tile.add_property("MATERIAL", material_silver)

    def set_name(self, name):
        self.tile.set_name(name)

    def get_name(self):
        return self.tile.get_name()

    def get_x(self):
        return self.tile.get_x()

    def get_y(self):
        return self.tile.get_y()

    def get_z(self):
        return self.tile.get_z()

    def draw(self):
        self.tile.exec_property_func("MATERIAL")
        draw_list(self.tile.get_property("GLLIST"),
                  self.tile.get_position_list(),
                  0,
                  None,
                  self.tile.get_property("SIZE"),
                  None)