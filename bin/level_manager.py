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
from re import *

# clase que carga un nivel a base de un archivo de texto sin formato
class Level:
	def __init__(self, map_file):
		lines = [line.rstrip('\n') for line in open(map_file)]
		strings = [split('\s+', line) for line in lines]
		self.heightmap = [[int(value) for value in line] for line in strings]
		self.height = 0
		for row, i in enumerate(self.heightmap):
			for column, j in enumerate(self.heightmap):
				height = self.heightmap[row][column]
				if height > self.height:
					self.height = height
		print self.height
		self.width = max([len(row) for row in self.heightmap])
		self.length = len(self.heightmap)
		self.create_cubes()

	def create_cubes(self):
		self.tilemap = [[[None for h in xrange(self.height)] for j in xrange(self.width)] for i in xrange(self.length)]
		for row, i in enumerate(self.heightmap):
			for column, j in enumerate(self.heightmap):
				for height in xrange(self.heightmap[row][column]):
					self.tilemap[row][column][height] = Particle(row * 40, column * 40, height * 40)
					self.tilemap[row][column][height].add_property("GLLIST", create_cube())
					self.tilemap[row][column][height].add_property("SIZE", [40, 40, 40])
					self.tilemap[row][column][height].set_name("Tile")
					print type(self.tilemap[row][column][height])

	def get_tilemap(self):
		return self.tilemap