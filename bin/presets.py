# coding: UTF-8
from pygltoolbox.particles import *
from pygltoolbox.figures import *
from pygltoolbox.materials import *
import json as json
from random import random


class Player():
    def __init__(self):
        with open("config.json") as config:
            self.constants = json.load(config)["constants"]

        self.side_length = self.constants["side_length"]

        self.move_frames = self.constants["move_frames"]

        self.gravity = self.constants["gravity"]

        self.fall_speed = 0
        self.falling = False
        self.fall_counter = 0
        self.move_speed = 90 / self.move_frames
        self.rot_counter = 0
        self.rot_spd = 0
        self.rot_progress = 0
        # booleano
        self.move_axis = None
        self.direction = None
        self.rising = False

        self.figure = Particle()
        self.figure.add_property("GLLIST", create_cube())
        self.figure.add_property("SIZE", [self.side_length / 2,
                                          self.side_length / 2,
                                          self.side_length / 2])
        self.figure.add_property("MATERIAL", material_player_cube)
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
        # animación de la rotación
        if self.rot_counter > 0:
            self.rot_counter -= 1
            self.rot_progress += self.rot_spd

        # actualización de la posición al finalizar la rotación
        if self.rot_counter == 0:
            self.rot_progress = 0
            if self.move_axis is not None and self.direction is not None and not self.rising:
                if self.move_axis and self.direction:
                    self.add_y(-self.side_length)
                elif self.move_axis and not self.direction:
                    self.add_y(self.side_length)
                elif not self.move_axis and self.direction:
                    self.add_x(self.side_length)
                elif not self.move_axis and not self.direction:
                    self.add_x(-self.side_length)
            if self.move_axis is not None and self.direction is not None and self.rising:
                if self.move_axis and self.direction:
                    self.add_y(-self.side_length)
                    self.add_z(self.side_length)
                elif self.move_axis and not self.direction:
                    self.add_y(self.side_length)
                    self.add_z(self.side_length)
                elif not self.move_axis and self.direction:
                    self.add_x(self.side_length)
                    self.add_z(self.side_length)
                elif not self.move_axis and not self.direction:
                    self.add_x(-self.side_length)
                    self.add_z(self.side_length)
                self.rising = False
            self.move_axis = None
            self.direction = None

        # caída si no hay bloques abajo
        if self.falling and self.get_z() - self.fall_speed - self.gravity > self.ground:
            self.fall_speed += self.gravity
            self.add_z(-self.fall_speed)
        elif self.falling:
            self.add_z(-self.get_z() + self.ground)
            self.falling = False
            self.fall_speed = 0

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

    def get_grid_coordinates(self):
        height = self.get_z() / self.side_length
        column = self.get_y() / self.side_length
        row = self.get_x() / self.side_length
        return [int(row), int(column), int(height)]

    def draw(self):
        if self.rot_counter > 0 and not self.rising:
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
        elif self.rot_counter > 0 and self.rising:
            if self.move_axis and self.direction:
                glTranslatef(self.get_x(),
                             self.get_y() - self.side_length / 2,
                             self.get_z() + self.side_length / 2)

                glRotatef(self.rot_progress, 1, 0, 0)

                glTranslatef(-self.get_x(),
                             -self.get_y() + self.side_length / 2,
                             -self.get_z() - self.side_length / 2)
            elif self.move_axis and not self.direction:
                glTranslatef(self.get_x(),
                             self.get_y() + self.side_length / 2,
                             self.get_z() + self.side_length / 2)

                glRotatef(self.rot_progress, 1, 0, 0)

                glTranslatef(-self.get_x(),
                             -self.get_y() - self.side_length / 2,
                             -self.get_z() - self.side_length / 2)
            elif not self.move_axis and self.direction:
                glTranslatef(self.get_x() + self.side_length / 2,
                             self.get_y(),
                             self.get_z() + self.side_length / 2)

                glRotatef(self.rot_progress, 0, 1, 0)

                glTranslatef(-self.get_x() - self.side_length / 2,
                             -self.get_y(),
                             -self.get_z() - self.side_length / 2)
            elif not self.move_axis and not self.direction:
                glTranslatef(self.get_x() - self.side_length / 2,
                             self.get_y(),
                             self.get_z() + self.side_length / 2)

                glRotatef(self.rot_progress, 0, 1, 0)

                glTranslatef(-self.get_x() + self.side_length / 2,
                             -self.get_y(),
                             -self.get_z() - self.side_length / 2)
        self.figure.exec_property_func("MATERIAL")
        draw_list(self.figure.get_property("GLLIST"),
                  self.figure.get_position_list(),
                  0, None, self.figure.get_property("SIZE"), None)

    def move_neg_y(self):
        if (self.move_axis is None or self.move_axis) and self.rot_counter == 0:
            self.move_axis = True
            self.rot_counter += self.move_frames
            self.rot_spd = self.move_speed
            self.direction = True

    def move_y(self):
        if (self.move_axis is None or self.move_axis) and self.rot_counter == 0:
            self.move_axis = True
            self.rot_counter += self.move_frames
            self.rot_spd = -self.move_speed
            self.direction = False

    def move_x(self):
        if (self.move_axis is None or not self.move_axis) and self.rot_counter == 0:
            self.move_axis = False
            self.rot_counter += self.move_frames
            self.rot_spd = self.move_speed
            self.direction = True

    def move_neg_x(self):
        if (self.move_axis is None or not self.move_axis) and self.rot_counter == 0:
            self.move_axis = False
            self.rot_counter += self.move_frames
            self.rot_spd = -self.move_speed
            self.direction = False

    def rise_neg_y(self):
        if (self.move_axis is None or self.move_axis) and self.rot_counter == 0:
            self.move_axis = True
            self.rot_counter += 2 * self.move_frames
            self.rot_spd = self.move_speed
            self.direction = True
            self.rising = True

    def rise_y(self):
        if (self.move_axis is None or self.move_axis) and self.rot_counter == 0:
            self.move_axis = True
            self.rot_counter += 2 * self.move_frames
            self.rot_spd = -self.move_speed
            self.direction = False
            self.rising = True

    def rise_x(self):
        if (self.move_axis is None or not self.move_axis) and self.rot_counter == 0:
            self.move_axis = False
            self.rot_counter += 2 * self.move_frames
            self.rot_spd = self.move_speed
            self.direction = True
            self.rising = True

    def rise_neg_x(self):
        if (self.move_axis is None or not self.move_axis) and self.rot_counter == 0:
            self.move_axis = False
            self.rot_counter += 2 * self.move_frames
            self.rot_spd = -self.move_speed
            self.direction = False
            self.rising = True

    def fall(self, coords, level):
        self.falling = True
        row = coords[0]
        column = coords[1]
        for height in xrange(coords[2], -1, -1):
            tile = level.get_object_at([row, column, height])
            if tile is not None:
                self.ground = tile.get_z() + self.side_length
                return
        self.ground = -sys.maxint - 1

    def is_falling(self):
        return self.falling

    def can_rise_x(self, level):
        coord = self.get_grid_coordinates()
        coord[0] += 1
        try:
            if isinstance(level.get_object_at(coord), BasicTile):
                return True
        except IndexError:
            return False
        return False

    def can_rise_neg_x(self, level):
        coord = self.get_grid_coordinates()
        coord[0] -= 1
        try:
            if isinstance(level.get_object_at(coord), BasicTile):
                return True
        except IndexError:
            return False
        return False

    def can_rise_y(self, level):
        coord = self.get_grid_coordinates()
        coord[1] += 1
        try:
            if isinstance(level.get_object_at(coord), BasicTile):
                return True
        except IndexError:
            return False
        return False

    def can_rise_neg_y(self, level):
        coord = self.get_grid_coordinates()
        coord[1] -= 1
        try:
            if isinstance(level.get_object_at(coord), BasicTile):
                return True
        except IndexError:
            return False
        return False


class BasicTile:
    def __init__(self, row, column, level, side_length):
        self.tile = Particle(row * side_length,
                             column * side_length,
                             level * side_length)
        self.tile.add_property("GLLIST", create_cube())
        self.tile.add_property("SIZE", [side_length / 2,
                                        side_length / 2,
                                        side_length / 2])
        self.tile.add_property("MATERIAL", material_tile_cube)

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


class Shard():
    def __init__(self, row, column, level, cube_side_length, shard_side_length):
        self.side_length = shard_side_length
        self.cube_side_length = cube_side_length
        self.figure = Particle(row * cube_side_length,
                               column * cube_side_length,
                               level * cube_side_length)
        roll = random()
        self.figure.add_property("GLLIST", create_octahedron())
        self.figure.add_property("SIZE", [self.side_length,
                                          self.side_length,
                                          self.side_length])
        self.figure.add_property("MATERIAL", material_shard)
        self.figure.set_name("Shard")

    def get_x(self):
        return self.figure.get_x()

    def get_y(self):
        return self.figure.get_y()

    def get_z(self):
        return self.figure.get_z()

    def draw(self):
        self.figure.exec_property_func("MATERIAL")
        draw_list(self.figure.get_property("GLLIST"),
                  self.figure.get_position_list(),
                  0,
                  None,
                  self.figure.get_property("SIZE"),
                  None)

    def get_name(self):
        return self.figure.get_name()

    def get_grid_coordinates(self):
        height = self.get_z() / self.cube_side_length
        column = self.get_y() / self.cube_side_length
        row = self.get_x() / self.cube_side_length
        return [int(row), int(column), int(height)]


class FallingTile:
    def __init__(self, row, column, level, side_length):
        self.side_length = side_length
        self.start_pos = [row * self.side_length, column * self.side_length, (level + 0.4) * self.side_length]
        self.tile = Particle(row * self.side_length,
                             column * self.side_length,
                             (level + 0.4) * self.side_length)
        self.tile.add_property("GLLIST", create_cube())
        self.tile.add_property("SIZE", [self.side_length / 2,
                                        self.side_length / 2,
                                        self.side_length / 10])
        self.tile.add_property("MATERIAL", material_tile_cube)

        self.stable = None
        self.fall_speed = 0

        with open("config.json") as config:
            constants = json.load(config)["constants"]
            self.gravity = constants["gravity"]
            self.height_treshold = constants["height_treshold"]

    def set_name(self, name):
        self.tile.set_name(name)

    def get_name(self):
        return self.tile.get_name()

    def add_x(self, x):
        self.tile.set_x(self.get_x() + x)

    def add_y(self, y):
        self.tile.set_y(self.get_y() + y)

    def add_z(self, z):
        self.tile.set_z(self.get_z() + z)

    def get_x(self):
        return self.tile.get_x()

    def get_y(self):
        return self.tile.get_y()

    def get_z(self):
        return self.tile.get_z()

    def get_grid_coordinates(self):
        height = self.get_z() / self.side_length
        column = self.get_y() / self.side_length
        row = self.get_x() / self.side_length
        return [int(row), int(column), int(height)]

    def get_original_coordinates(self):
        row = self.start_pos[0] / self.side_length
        column = self.start_pos[1] / self.side_length
        height = self.start_pos[2] / self.side_length
        return [int(row), int(column), int(height)]

    def fall(self):
        self.stable = True

    def draw(self):
        self.tile.exec_property_func("MATERIAL")
        draw_list(self.tile.get_property("GLLIST"),
                  self.tile.get_position_list(),
                  0,
                  None,
                  self.tile.get_property("SIZE"),
                  None)

    def update(self, player):
        if not self.stable and self.stable is not None:
            self.fall_speed += self.gravity
            self.add_z(-self.fall_speed)
        elif self.stable and self.stable is not None:
            self.check_above(player)

    def check_above(self, player):
        player_coord = player.get_grid_coordinates()
        tile_coord = self.get_grid_coordinates()
        above_tile = [tile_coord[0], tile_coord[1], tile_coord[2] + 1]

        if player_coord != above_tile:
            self.stable = False

    def is_deletable(self):
        return self.get_z() < -10