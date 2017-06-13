# coding: UTF-8

# imports
import json as json
from presets import BasicTile
from pygltoolbox.utils_geometry import *


# clase que carga un nivel a base de un archivo de texto sin formato
class Level:
    def __init__(self, map_file):
        with open(map_file) as json_map:
            map_dict = json.load(json_map)
        map_array = map_dict["levels"]

        with open("config.json") as config:
            side_length = json.load(config)["constants"]["side_length"]

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
            for column, j in enumerate(map_array[level]):
                for row, i in enumerate(map_array[level][column]):
                    cell = map_array[level][column][row]
                    if cell == 0:
                        continue
                    elif abs(cell) == 1:
                        self.tilemap[row][column][level] = BasicTile(row,
                                                                column,
                                                                level,
                                                                side_length)
                        if cell == -1:
                            self.tilemap[row][column][level].set_name("Spawn")
                        else:
                            self.tilemap[row][column][level].set_name("Tile")

    def draw(self):
        for row, i in enumerate(self.tilemap):
            for column, j in enumerate(self.tilemap[row]):
                for height, z in enumerate(self.tilemap[row][column]):
                    if self.tilemap[row][column][height] is not None:
                    	self.tilemap[row][column][height].draw()

    def get_object_below(self, coords):
    	row = coords[0]
    	column = coords[1]
    	height = coords[2] - 1
    	try:
    		obj = self.tilemap[row][column][height]
    	except IndexError:
    		return None
    	return obj