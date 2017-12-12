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
from moba import *

class MyMinion(Minion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		self.states = [Idle, MoveToTower, Attack, RushBase]
		### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###

		### YOUR CODE GOES ABOVE HERE ###

	def start(self):
		Minion.start(self)
		self.changeState(Idle)





############################
### Idle
###
### This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):
	
	def enter(self, oldstate):
		State.enter(self, oldstate)
		# stop moving
		self.agent.stopMoving()
	
	def execute(self, delta = 0):
		

		State.execute(self, delta)
		### YOUR CODE GOES BELOW HERE ###
		enemyTowers = self.agent.world.getEnemyTowers(self.agent.getTeam())
		enemyBases = self.agent.world.getEnemyBases(self.agent.getTeam())
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())


		if enemyTowers:
			if enemyTowers[0].alive:
				self.agent.changeState(MoveToTower, enemyTowers[0])
			else:
				self.agent.changeState(MoveToTower, enemyTowers[1])
		elif enemyBases:
			base = enemyBases[0]
			self.agent.changeState(RushBase, base)

		### YOUR CODE GOES ABOVE HERE ###
		return None


###############Helpers##################
def targetInRange(agent, targets):
	for target in targets:
		if distance(agent.getLocation(), target.getLocation()) < BIGBULLETRANGE:
			return target
	return None

##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		if self.victim is not None:
			print "Hey " + str(self.victim) + ", I don't like you!"
		self.agent.changeState(Idle)

##############################
### YOUR STATES GO HERE:

class MoveToTower(State):
	def parseArgs(self, args):
		self.target = args[0]

	def enter(self, oldstate):
		State.enter(self, oldstate)
		self.agent.navigateTo(self.target.getLocation())

	def execute(self, delta = 0):
		if not self.target.alive:
			self.agent.changeState(Idle)

		if distance(self.agent.getLocation(), self.target.getLocation()) < BIGBULLETRANGE:
			self.agent.stopMoving()
			self.agent.turnToFace(self.target.getLocation())
			self.agent.shoot()
		else:
			# hit enemy if could
			for npc in self.agent.getVisible():
				if (
					npc in self.agent.world.getEnemyNPCs(self.agent.getTeam()) and 
					npc.isAlive() and 
					distance(self.agent.getLocation(), npc.getLocation()) < BIGBULLETRANGE
					):
						self.agent.changeState(Attack, npc)

	def exit(self):
		self.agent.stopMoving()

##############################
### YOUR STATES GO HERE:

class RushBase(State):
	def parseArgs(self, args):
		self.target = args[0]

	def enter(self, oldstate):
		State.enter(self, oldstate)
		self.agent.navigateTo(self.target.getLocation())

	def execute(self, delta = 0):
		if not self.target.alive:
			self.agent.changeState(Idle)

		if distance(self.agent.getLocation(), self.target.getLocation()) < BIGBULLETRANGE:
			self.agent.stopMoving()
			self.agent.turnToFace(self.target.getLocation())
			self.agent.shoot()

	def exit(self):
		self.agent.stopMoving()

##############################
### YOUR STATES GO HERE:

class Attack(State):
	def parseArgs(self, args):
		self.enemy = args[0]

	def execute(self, delta = 0):
		if (distance(self.enemy.getLocation(), self.agent.getLocation()) < BIGBULLETRANGE):
			#self.agent.stopMoving()
			self.agent.turnToFace(self.enemy.getLocation())
			self.agent.shoot()
		self.agent.changeState(Idle)
