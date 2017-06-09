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


# clase que carga un nivel a base de un archivo de texto sin formato
class Level:
    def __init__(self, map_file):
        with open(map_file) as json_map:
            map_dict = json.load(json_map)
        map_array = map_dict["levels"]

        # inicializa arreglo para cada celda
        height = len(map_array)
        width = len(map_array[0])
        length = len(map_array[0][0])

        self.tilemap = [
            [
                [
                    None for h in xrange(height)
                ]
                for j in xrange(width)
            ]
            for i in xrange(length)
        ]

        for level, h in enumerate(map_array):
            for row, j in enumerate(map_array[level]):
                for column, i in enumerate(map_array[level][row]):
                    cell = map_array[level][row][column]
                    if cell == 0:
                        continue
                    elif cell == 1:
                        self.tilemap[row][column][level] = Particle(row * 40, column * 40, level * 40)
                        self.tilemap[row][column][level].add_property("GLLIST", create_cube())
                        self.tilemap[row][column][level].add_property("SIZE", [40, 40, 40])
                        self.tilemap[row][column][level].set_name("Tile")

    def get_tilemap(self):
        return self.tilemap