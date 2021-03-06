# coding: UTF-8

# imports
import json as json
from presets import Shard, BasicTile, FallingTile, PushingBlock, FinishTile, OptionTile
from pygltoolbox.utils_geometry import *


# clase que carga un nivel a base de un archivo de texto sin formato
class Level:
    def __init__(self, map_file):
        with open(map_file) as json_map:
            map_dict = json.load(json_map)
        map_array = map_dict["levels"]
        self.tag = map_dict["tag"]

        with open("config.json") as config:
            self.constants = json.load(config)["constants"]

        side_length = self.constants["side_length"]
        shard_side_length = self.constants["shard_side_length"]
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
                    elif cell == 2:
                        self.tilemap[row][column][level] = Shard(row, column, level,
                                                                 side_length,
                                                                 shard_side_length)
                    elif cell == 3:
                        self.tilemap[row][column][level] = FallingTile(row,
                                                                       column,
                                                                       level,
                                                                       side_length)
                    elif cell == 4:
                        self.tilemap[row][column][level] = PushingBlock(row,
                                                                        column,
                                                                        level,
                                                                        side_length,
                                                                        0)
                    elif cell == 5:
                        self.tilemap[row][column][level] = PushingBlock(row,
                                                                        column,
                                                                        level,
                                                                        side_length,
                                                                        1)
                    elif cell == 6:
                        self.tilemap[row][column][level] = PushingBlock(row,
                                                                        column,
                                                                        level,
                                                                        side_length,
                                                                        2)
                    elif cell == 7:
                        self.tilemap[row][column][level] = PushingBlock(row,
                                                                        column,
                                                                        level,
                                                                        side_length,
                                                                        3)
                    elif cell == 8:
                        self.tilemap[row][column][level] = FinishTile(row,
                                                                      column,
                                                                      level,
                                                                      side_length)
                    elif cell // 10 == 9:
                        # get text from the map´s json file
                        text = map_dict["options"][cell % 10]
                        action = map_dict["actions"][cell % 10]
                        parameter = map_dict["parameters"][cell % 10]
                        self.tilemap[row][column][level] = OptionTile(row,
                                                                      column,
                                                                      level,
                                                                      side_length,
                                                                      text, action,
                                                                      parameter)

    def draw(self):
        for row, i in enumerate(self.tilemap):
            for column, j in enumerate(self.tilemap[row]):
                for height, z in enumerate(self.tilemap[row][column]):
                    if (
                        self.tilemap[row][column][height] is not None and
                        not isinstance(self.tilemap[row][column][height], Shard)
                    ):
                        self.tilemap[row][column][height].draw()

    def get_object_below(self, coords):
        row = coords[0]
        column = coords[1]
        height = coords[2] - 1
        if row < 0 or column < 0 or height < 0:
            return None
        try:
            obj = self.tilemap[row][column][height]
        except IndexError:
            return None
        return obj

    def get_object_at(self, coords):
        try:
            return self.tilemap[coords[0]][coords[1]][coords[2]]
        except IndexError:
            return None

    def get_shards(self):
        shards = []
        for row, i in enumerate(self.tilemap):
            for column, j in enumerate(self.tilemap[row]):
                for height, z in enumerate(self.tilemap[row][column]):
                    if isinstance(self.tilemap[row][column][height], Shard):
                        shards.append(self.tilemap[row][column][height])
        return shards

    def get_fallers(self):
        fallers = []
        for row, i in enumerate(self.tilemap):
            for column, j in enumerate(self.tilemap[row]):
                for height, z in enumerate(self.tilemap[row][column]):
                    if isinstance(self.tilemap[row][column][height], FallingTile):
                        fallers.append(self.tilemap[row][column][height])
        return fallers

    def get_pushers(self):
        pushers = []
        for row, i in enumerate(self.tilemap):
            for column, j in enumerate(self.tilemap[row]):
                for height, z in enumerate(self.tilemap[row][column]):
                    if isinstance(self.tilemap[row][column][height], PushingBlock):
                        pushers.append(self.tilemap[row][column][height])
        return pushers

    def get_options(self):
        options = []
        for row, i in enumerate(self.tilemap):
            for column, j in enumerate(self.tilemap[row]):
                for height, z in enumerate(self.tilemap[row][column]):
                    if isinstance(self.tilemap[row][column][height], OptionTile):
                        options.append(self.tilemap[row][column][height])
        return options

    def get_finish(self):
        finishes = []
        for row, i in enumerate(self.tilemap):
            for column, j in enumerate(self.tilemap[row]):
                for height, z in enumerate(self.tilemap[row][column]):
                    if isinstance(self.tilemap[row][column][height], FinishTile):
                        finishes.append(self.tilemap[row][column][height])
        return finishes

    def remove_object_at(self, position):
        try:
            self.tilemap[position[0]][position[1]][position[2]] = None
        except:
            print "Failed to remove object"

    def get_tag(self):
        return self.tag
