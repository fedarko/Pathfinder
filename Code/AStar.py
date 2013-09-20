"""
Copyright 2012 Marcus Fedarko

This file is part of Pathfinder.

    Pathfinder is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Pathfinder is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Pathfinder.  If not, see <http://www.gnu.org/licenses/>.

====
marcus.fedarko@gmail.com
Chemistry G/T
Long Reach High School
Science Fair 2011-2012

AStar.py
"""

import Config
import Algorithm

import time
import math
import pygame
from pygame.locals import *

class AStar(Algorithm.Algorithm):
    """An implementation of the A* search algorithm."""
    
    def __init__(self, bg, screen, rPos2node, gridlines, h, emptyNodes, barrierNodes, startNode, endNode):
	"""Initializes some attributes required for the running of the
	algorithm and then calls self.run()."""
	
	super(AStar, self).__init__("A*", bg, screen, rPos2node, gridlines, emptyNodes, barrierNodes, startNode, endNode)
    
	self.heuristic = h
    
    def run(self):
	"""Runs the algorithm on the current groups of nodes."""
	
	super(AStar, self).run()
	print "Using %s heuristic." % (self.heuristic)
	
	a = time.time()
	print "Current time is %fs" % (a)
	self.markNode(self.rPos2node, *self.emptyNodes)
	self.markNode(self.rPos2node, *self.barrierNodes)
	self.markNode(self.rPos2node, self.endNode.sprite)
	
	# unvisited nodes
	openNodes = [self.startNode.sprite]
	# visited nodes
	closedNodes = []
	
	finished = False
	self.g = 0
	# We don't need a priority queue, since only one path will be created
	# at a time - this differs from Dijkstra's Algorithm.
	# This saves some time, but mostly helps simplify things
	nextNode = self.startNode.sprite
	while True:
	    
	    c = nextNode
	    c2p = (c.rect.left, c.rect.top - Config.NODESIZE[1])
	    c4p = (c.rect.left - Config.NODESIZE[0], c.rect.top)
	    c5p = (c.rect.left + Config.NODESIZE[0], c.rect.top)
	    c7p = (c.rect.left, c.rect.top + Config.NODESIZE[1])	    
	    for s in (c2p, c4p, c5p, c7p):
		
		if not s in self.rPos2node.keys():
		    # Is the node outside the screen?
		    continue
		sN = self.rPos2node[s]
		if sN.nodeType == 'barrier':
		    # Is the node a barrier?
		    continue		
		elif sN in closedNodes:
		    # Is the node already in closedNodes?
		    continue
		elif sN in openNodes:
		    # This was what was slowing the program down. If the node
		    # is already on the open list, don't add it again!
		    # Recalculate to see if there's a better path.
		    if self.g + Config.NODECOST < sN.g:
			self.assignFcost(sN)
			sN.parent = c
		else:
		    # This is the first time visiting the node
		    sN.parent = c
		    openNodes.append(sN)
		
	    if c == self.endNode.sprite:
		finished = True
		break
	    
	    closedNodes.append(c)
	    # As soon as it hits a dead end, go back to most optimal open node.
	    # This is why the program would mess up when it hit most obstacles.
	    # -12/5/11
	    openNodes.remove(c)

	    nextNode = None

	    for n in openNodes:
		self.assignFcost(n)
		if nextNode == None or n.f < nextNode.f:
		    nextNode = n
		
	    # No path could be found
	    if nextNode == None: break
	    
	    # Add the next node and repeat all over again
	    self.g = nextNode.g 
	    
	    self.updateGraphics(closedNodes, 'closed')
	    self.updateGraphics(openNodes, 'open')
	    
	b = time.time()	
	if finished:
	    self.reconstructPath()
	self.printFinishedMessages(a, b, finished)
	
    def assignFcost(self, n):
	"""Assigns an F, G, and H cost to a given node."""
	
	n.g = self.g + Config.NODECOST

	# heuristic = trying to estimate remaining distance
	# among the path - the closer, the better
	if self.heuristic == "Manhattan":
	    n.h = self.manhattanHeuristic(n, self.endNode.sprite)
	else:
	    n.h = self.euclideanHeuristic(n, self.endNode.sprite)
	    
	n.f = n.h + n.g
	
    def manhattanHeuristic(self, n, goal):
	"""Uses the Manhattan method to find the heuristic h-cost from a node
	to a goal. The heuristic is abs(n.x - goal.x) + abs(n.y - goal.y)"""
	
	hCx = abs(n.rect.left - goal.rect.left) / Config.NODESIZE[0]
	hCy = abs(n.rect.top - goal.rect.top) / Config.NODESIZE[1]
	hCost = Config.NODECOST * (hCx + hCy)
	return hCost
	
    def euclideanHeuristic(self, n, goal):
	"""Uses Euclidean distance to find the h-cost from a node to a goal.
	The heuristic is sqrt((n.x - goal.x) ** 2 + (n.y - goal.y) ** 2)."""
	
	hCx = (n.rect.left - goal.rect.left) / Config.NODESIZE[0]
	hCy = (n.rect.top - goal.rect.top) / Config.NODESIZE[1]
	hCost = Config.NODECOST * math.sqrt(hCx ** 2 + hCy ** 2)
	return hCost

    def updateGraphics(self, nodes, nodeType):
	"""Updates the graphics in lieu of the Graphics Manager."""
	
	super(AStar, self).updateGraphics()
	
	for n in nodes:
	    if n != self.startNode.sprite and n != self.endNode.sprite:
		if nodeType == 'closed':
		    n.image.fill(Config.VISITEDNODECOLOR)
		elif nodeType == 'open':
		    n.image.fill(Config.OPENNODECOLOR)
