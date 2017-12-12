'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates a grid as a 2D array of True/False values (True =  traversable). Also returns the dimensions of the grid as a (columns, rows) list.
def myCreateGrid(world, cellsize):
	grid = None
	dimensions = (0, 0)
	### YOUR CODE GOES BELOW HERE ###	
	length, width = world.getPoints()[2]
	dimensions = (int(length/cellsize), int(width/cellsize))
	grid = numpy.ones(dimensions)
	#print(dimensions)
	for row in range(0,dimensions[0]):
		for col in range(0,dimensions[1]):
			a = int(row*cellsize)
			b = int(col*cellsize)
			c = int(row*cellsize+cellsize)
			d = int(col*cellsize+cellsize)
			A = (a,b)
			B = (c,b)
			C = (a,d)
			D = (c,d)
			for obstacle in world.getObstacles():
				# If point is inside of the obstacle.
				if (obstacle.pointInside(A) or obstacle.pointInside(B) or obstacle.pointInside(C) or obstacle.pointInside(D)):
					grid[row][col] = 0
				# If obstacle corner is inside of an existing grid.
				for point in obstacle.getPoints():
					if pointInsidePolygonLines((point[0],point[1]),[(A,B),(A,C),(C,D),(B,D)]):
						grid[row][col] = 0

	### YOUR CODE GOES ABOVE HERE ###
	return grid, dimensions

