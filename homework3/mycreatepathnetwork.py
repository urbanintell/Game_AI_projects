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
from random import shuffle

# Creates a pathnode network that connects the midpoints of each navmesh together
def myCreatePathNetwork(world, agent = None):
	nodes = []
	edges = []
	polys = []
	### YOUR CODE GOES BELOW HERE ###
	polys = initializePolygon(world, polys)
	mergePolygons(polys)

	allObstacles = world.obstacles

	for polygon in polys:
		polynodes = []
		for i in range(len(polygon)):
			isObstacle = False
			if i < len(polygon) - 1:
				k = i+1
			else:
				k = 0
			middlepoint = ((polygon[i][0]+polygon[k][0])/2,(polygon[i][1]+polygon[k][1])/2)
			for obstacle in allObstacles:
				if (polygon[i],polygon[k]) in obstacle.getLines() or (polygon[k],polygon[i]) in obstacle.getLines():
					isObstacle = True
					break
			if not isObstacle:
				polynodes.append(middlepoint)
				nodes.append(middlepoint)		

		center = getPolygonMiddlepoint(polygon)
		polynodes.append(center)
		nodes.append(center)

		for i in range(len(polynodes)):
			if i < len(polynodes) - 1:
				k = i + 1
			else:
				k = 0
			if not collision(allObstacles, (polynodes[i],polynodes[k]), agent.getMaxRadius()):
				edges.append((polynodes[i],polynodes[k]))
	### YOUR CODE GOES ABOVE HERE ###
	return nodes, edges, polys

	
def initializePolygon(world, polygons):
	worldNodes = world.getPoints()
	shuffle(worldNodes)
	for node1 in worldNodes:
		for node2 in worldNodes:
			for node3 in worldNodes:
				if node1 == node2 or node1 == node3 or node2 == node3:
					continue
				if not isOverlapping(world, node1, node2, node3, polygons) and notExist(node1, node2, node3, polygons):
					polygons.append((node1, node2, node3))
	return polygons


def isOverlapping(world, node1, node2, node3, polygons):
	worldLines = world.getLines()
	#extend all existing triangles to worldLines
	for (corner1, corner2, corner3) in polygons:
		line1 = (corner1, corner2)
		line2 = (corner1, corner3)
		line3 = (corner2, corner3)
		worldLines.extend((line1, line2, line3))

	#case 1: pre-req  -> new line is not existing.
	case1_line1 = (node1, node2) not in worldLines and (node2, node1) not in worldLines
	case1_line2 = (node1, node3) not in worldLines and (node3, node1) not in worldLines
	case1_line3 = (node2, node3) not in worldLines and (node3, node2) not in worldLines
	#case 2: new line intersects with existing lines.
	case2_line1 = rayTraceWorldNoEndPoints(node1, node2, worldLines) != None and case1_line1
	case2_line2 = rayTraceWorldNoEndPoints(node1, node3, worldLines) != None and case1_line2
	case2_line3 = rayTraceWorldNoEndPoints(node2, node3, worldLines) != None and case1_line3

	if case2_line1 or case2_line2 or case2_line3: 
		return True
	#case 3: new line is inside of an obstacle
	for obstacle in world.obstacles:
		outline = obstacle.getLines()
		outcorners = obstacle.getPoints()

		case3_line1 = pointInsidePolygonLines(((node1[0]+node2[0])/2,(node1[1]+node2[1])/2), outline) and case1_line1
		case3_line2 = pointInsidePolygonLines(((node1[0]+node3[0])/2,(node1[1]+node3[1])/2), outline) and case1_line2
		case3_line3 = pointInsidePolygonLines(((node2[0]+node3[0])/2,(node2[1]+node3[1])/2), outline) and case1_line3

		if case3_line1 or case3_line2 or case3_line3:
			return True

		#case 4: the whole obstacle is within the polygon
		middlepoint = [0,0]		
		for corner in outcorners:
			middlepoint[0] += corner[0]
			middlepoint[1] += corner[1]
		middlepoint[0] /= len(outcorners)
		middlepoint[1] /= len(outcorners)
		if pointInsidePolygonPoints(middlepoint, (node1, node2, node3)):
			return True

	return False

def notExist(node1, node2, node3, polygons):
	s1 = (node1, node2, node3) not in polygons
	s2 = (node1, node3, node2) not in polygons
	s3 = (node2, node1, node3) not in polygons
	s4 = (node2, node3, node1) not in polygons
	s5 = (node3, node1, node2) not in polygons
	s6 = (node3, node2, node1) not in polygons
	return s1 and s2 and s3 and s4 and s5 and s6

def mergePolygons(polygons):
	notExhaustive = True
	#loop until no more merging can be done
	while notExhaustive:
		notExhaustive = False
		for polygon1 in polygons:
			for polygon2 in polygons:
				#we don't actually need to check this.
				if polygon1 == polygon2:
					continue
				if polygonsAdjacent(polygon1, polygon2):
					#get points' list
					newCorners = []
					for point in polygon1:
						newCorners.append(point)
					for point in polygon2:
						if point not in newCorners:
							newCorners.append(point)
					if isConvex(formPolygon(newCorners)):
						polygons.remove(polygon1)
						polygons.remove(polygon2)
						polygons.append(formPolygon(newCorners))
						notExhaustive = True
						break
			if notExhaustive: break

def formPolygon(points):
	polygon = []
	middlepoint = [0,0]
	for point in points:
		middlepoint[0] += point[0]
		middlepoint[1] += point[1]
	middlepoint[0] /= len(points)
	middlepoint[1] /= len(points)
	#counter-clockwisely sorting all points to get rid of crossing.
	def cc(point):
		return math.atan2(middlepoint[1]-point[1], middlepoint[0]-point[0])

	polygon = sorted(points, key = cc)
	return polygon

def getPolygonMiddlepoint(polygon):
	result = []
	middlepoint = [0,0]
	for i in range(len(polygon)):
		middlepoint[0] += polygon[i][0]
		middlepoint[1] += polygon[i][1]
	middlepoint[0] /= len(polygon)
	middlepoint[1] /= len(polygon)
	return middlepoint

def collision(obstacles, line, radius):
	for obstacle in obstacles:
		for point in obstacle.getPoints():
			if minimumDistance(line, point) < radius: return True
	return False