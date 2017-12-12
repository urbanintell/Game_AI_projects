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

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates the pathnetwork as a list of lines between all pathnodes that are traversable by the agent.
def myBuildPathNetwork(pathnodes, world, agent = None):
	lines = []
	### YOUR CODE GOES BELOW HERE ###
	for i in range(len(pathnodes)):
		for j in range(i + 1, len(pathnodes)):
			lines.append((pathnodes[i], pathnodes[j]))
		
	obstacleLines = world.getLinesWithoutBorders()

	for i in range(len(lines)):
		if rayTraceWorld(lines[i][0], lines[i][1], obstacleLines) != None :
			 lines[i] = ((0,0),(0,0))

	obstaclePoints = world.getPoints()
	agentWidth = agent.getMaxRadius()
	print(agentWidth)
	for i in range(len(obstaclePoints)):
		for j in range(len(lines)):
			if minimumDistance(lines[j], obstaclePoints[i]) < agentWidth:
				lines[j] = ((0,0),(0,0))
	### YOUR CODE GOES ABOVE HERE ###
	return lines
