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

BiDjikstras.py
"""

import Config
import Dijkstras

import time
import pygame
from pygame.locals import *

class BiDijkstras(Dijkstras.Dijkstras):
    """An implementation of the Bidirectional Dijkstra's search algorithm."""
    
    def __init__(self, bg, screen, rPos2node, gridlines, emptyNodes, barrierNodes, startNode, endNode):
	"""Initializes some attributes required for the running of the
	algorithm and then calls self.run()."""
	
	super(Dijkstras.Dijkstras, self).__init__("Bidirectional Dijkstra's", bg, screen, rPos2node, gridlines, emptyNodes, barrierNodes, startNode, endNode)

	self.unvisitedNodes = pygame.sprite.RenderPlain()
	self.unvisitedNodes2 = pygame.sprite.RenderPlain()
	
	self.closedNodes = []
	self.closedNodes2 = []
	
	self.forwardsPQpos = 0
	self.backwardsPQpos = 0
	
	self.gCost = 0
	self.gCost2 = 0
	
	self.pq = [self.startNode.sprite]
	self.pq2 = [self.endNode.sprite]
	
    def run(self):
	"""Runs the algorithm on the current groups of nodes."""
	
	super(Dijkstras.Dijkstras, self).run()
	
	a = time.time()
	print "Current time is %fs" % (a)
	
	for coll in (self.rPos2node, self.unvisitedNodes, self.unvisitedNodes2):
	    self.markNode(coll, *self.emptyNodes)
	    self.markNode(coll, *self.barrierNodes)
	    self.markNode(coll, self.endNode.sprite)

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
	
	if self.forwardsPQpos >= len(self.pq):
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
	    if not self.unvisitedNodes.has(sN):
		continue
	    
	    self.unvisitedNodes.remove(sN)
	    self.pq.append(sN)
	    if sN != self.endNode.sprite and sN != self.startNode.sprite:
		if sN in self.unvisitedNodes2:
		    sN.image.fill(Config.OPENNODECOLOR)	    
	    sN.parent = c
	    
	self.unvisitedNodes.remove(c)
	self.closedNodes.append(c)
	
	# Add the next node and repeat all over again	    
	self.forwardsPQpos += 1
	self.updateGraphics(c)
	return 0
	
    def checkBackwardsPQ(self):
	"""Checks one step in the priority queue running from the end node."""
	
	if self.backwardsPQpos >= len(self.pq2):
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
	    if not self.unvisitedNodes2.has(sN):
		continue
	    
	    self.unvisitedNodes2.remove(sN)
	    self.pq2.append(sN)
	    if sN != self.endNode.sprite and sN != self.startNode.sprite:
		if sN in self.unvisitedNodes:
		    sN.image.fill(Config.OPENNODECOLOR)
	    sN.parent2 = c
	    
	self.unvisitedNodes2.remove(c)
	self.closedNodes2.append(c)
	
	# Add the next node and repeat all over again
	self.backwardsPQpos += 1
	self.updateGraphics(c)
	return 0
	
    def updateGraphics(self, n):
	"""Updates the graphics in lieu of the Graphics Manager."""
	
	super(Dijkstras.Dijkstras, self).updateGraphics()
	
	if n != self.startNode.sprite and n != self.endNode.sprite:
	    n.image.fill(Config.VISITEDNODECOLOR)
