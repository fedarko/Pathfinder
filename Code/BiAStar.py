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

BiAStar.py
"""

import Config
import AStar

import time
import pygame
from pygame.locals import *

class BiAStar(AStar.AStar):
    """An implementation of the Bidirectional A* search algorithm."""
    
    def __init__(self, bg, screen, rPos2node, gridlines, h, emptyNodes, barrierNodes, startNode, endNode):
	"""Initializes some attributes required for the running of the
	algorithm and then calls self.run()."""
	
	super(AStar.AStar, self).__init__("Bidirectional A*", bg, screen, rPos2node, gridlines, emptyNodes, barrierNodes, startNode, endNode)
	
	self.heuristic = h

	self.openNodes = [self.startNode.sprite]
	self.openNodes2 = [self.endNode.sprite]
	
	self.closedNodes = []
	self.closedNodes2 = []

	self.forwardsPQpos = 0
	self.backwardsPQpos = 0
	
	self.g = 0
	self.g2 = 0
	
	# This implementation uses a priority queue, but
	# steps through it manually.
	self.pq = [self.startNode.sprite]
	self.pq2 = [self.endNode.sprite]
	
    def run(self):
	"""Runs the algorithm on the current groups of nodes."""
	
	super(AStar.AStar, self).run()
	print "Using %s heuristic." % (self.heuristic)
	
	a = time.time()
	print "Current time is %fs" % (a)
	self.markNode(self.rPos2node, *self.emptyNodes)
	self.markNode(self.rPos2node, *self.barrierNodes)
	self.markNode(self.rPos2node, self.endNode.sprite)	
	
	finished = 0
	toForwards = True
	while not finished:
	    if toForwards:
		finished = self.checkForwardsPQ()
		toForwards = False
	    else:
		finished = self.checkBackwardsPQ()
		toForwards = True
	    if finished == -1:
		# The start/end nodes are isolated; thus, no path can be found
		finished = 0
		break
		
	b = time.time()
	if finished:
	    self.reconstructPath(bidirectional=True)
	self.printFinishedMessages(a, b, finished)

    def checkForwardsPQ(self):
	"""Checks one step in the priority queue running from the start node."""
	
	if len(self.openNodes) < 1:
	    # No solution
	    return -1	   
	    
	c = self.pq[self.forwardsPQpos]	
	
	if c in self.closedNodes2:
	    c.intPt = True
	    return 1
	    
	c2p = (c.rect.left, c.rect.top - Config.NODESIZE[1])
	c4p = (c.rect.left - Config.NODESIZE[0], c.rect.top)
	c5p = (c.rect.left + Config.NODESIZE[0], c.rect.top)
	c7p = (c.rect.left, c.rect.top + Config.NODESIZE[1])
	
	for s in (c2p, c4p, c5p, c7p):
	    
	    if not s in self.rPos2node.keys():
		continue
	    sN = self.rPos2node[s]
	    if sN.nodeType == 'barrier':
		continue		
	    elif sN in self.closedNodes:
		continue
	    elif sN in self.openNodes:
		if self.g + Config.NODECOST < sN.g:
		    self.assignFcost(sN)
		    sN.parent = c
	    else:
		sN.parent = c
		self.openNodes.append(sN)
	
	self.closedNodes.append(c)
	self.openNodes.remove(c)
	
	nextNode = None

	for n in self.openNodes:
	    
	    self.assignFcost(n)
	    
	    if nextNode == None or n.f < nextNode.f:
		nextNode = n

	# No path could be found
	if nextNode == None:
	    return 0
	
	# Add the next node and repeat all over again
	self.pq.append(nextNode)
	self.g = nextNode.g	    
	self.forwardsPQpos += 1
	
	self.updateGraphics(self.closedNodes, 'closed')
	
	# Don't color already-visited nodes by the other tree
	# the color of an open node
	toUpdate = []
	for x in self.openNodes:
	    if x not in self.closedNodes2:
		toUpdate.append(x)
	self.updateGraphics(toUpdate, 'open')
	return 0
	
    def checkBackwardsPQ(self):
	"""Checks one step in the priority queue running from the end node."""

	if len(self.openNodes2) < 1:
	    # No solution
	    return -1
	
	c = self.pq2[self.backwardsPQpos]
	
	if c in self.closedNodes:
	    c.intPt = True
	    return 1
	    
	c2p = (c.rect.left, c.rect.top - Config.NODESIZE[1])
	c4p = (c.rect.left - Config.NODESIZE[0], c.rect.top)
	c5p = (c.rect.left + Config.NODESIZE[0], c.rect.top)
	c7p = (c.rect.left, c.rect.top + Config.NODESIZE[1])
	
	for s in (c2p, c4p, c5p, c7p):
	    
	    if not s in self.rPos2node.keys():
		continue
	    sN = self.rPos2node[s]
	    if sN.nodeType == 'barrier':
		continue		
	    elif sN in self.closedNodes2:
		continue
	    elif sN in self.openNodes2:
		if self.g2 + Config.NODECOST < sN.g2:
		    n.g2 = self.g2 + Config.NODECOST

		    if self.heuristic == "Manhattan":
			n.h2 = self.manhattanHeuristic(n, self.startNode.sprite)
		    else:
			n.h2 = self.euclideanHeuristic(n, self.startNode.sprite)

		    n.f2 = n.h2 + n.g2
		    sN.parent2 = c
	    else:
		self.openNodes2.append(sN)
		sN.parent2 = c
	
	self.closedNodes2.append(c)
	self.openNodes2.remove(c)
	
	nextNode = None

	for n in self.openNodes2:
	    
	    # Can't call AStar.assignFcost() because the costs are for the
	    # backwards path
	    n.g2 = self.g2 + Config.NODECOST

	    if self.heuristic == "Manhattan":
		n.h2 = self.manhattanHeuristic(n, self.startNode.sprite)
	    else:
		n.h2 = self.euclideanHeuristic(n, self.startNode.sprite)

	    n.f2 = n.h2 + n.g2
	    
	    if nextNode == None or n.f2 < nextNode.f2:
		nextNode = n

	if nextNode == None:
	    return 0
	
	self.pq2.append(nextNode)
	self.g2 = nextNode.g2
	self.backwardsPQpos += 1
	
	self.updateGraphics(self.closedNodes2 , 'closed')
	
	toUpdate = []
	for x in self.openNodes2:
	    if x not in self.closedNodes:
		toUpdate.append(x)
	self.updateGraphics(toUpdate, 'open')
	return 0
