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

Dijkstras.py
"""

import Config
import Algorithm

import time
import pygame
from pygame.locals import *

class Dijkstras(Algorithm.Algorithm):
    """An implementation of Dijkstra's Algorithm."""
    
    def __init__(self, bg, screen, rPos2node, gridlines, emptyNodes, barrierNodes, startNode, endNode):
	"""Initializes some attributes required for the running of the
	algorithm and then calls self.run()."""
	
	super(Dijkstras, self).__init__("Dijkstra's", bg, screen, rPos2node, gridlines, emptyNodes, barrierNodes, startNode, endNode)
	
	self.unvisitedNodes = pygame.sprite.RenderPlain()
	
    def run(self):
	"""Runs the algorithm on the current groups of nodes."""
	
	super(Dijkstras, self).run()
	
	# Time, in seconds, since the epoch
	a = time.time()
	print "Current time is %fs" % (a)
	
	for coll in (self.rPos2node, self.unvisitedNodes):
	    self.markNode(coll, *self.emptyNodes)
	    self.markNode(coll, *self.barrierNodes)
	    self.markNode(coll, self.endNode.sprite)
	
	# pq stands for priority queue; not using collections.deque b/c we want to be
	# able to iterate over pq
	pq = [self.startNode.sprite]
	finished = False

	for c in pq:

	    if c == self.endNode.sprite:
		finished = True
		break
	
	    # The cells surrounding the current node are as follows:
	    # 1 2 3
	    # 4 c 5
	    # 6 7 8
	    # This is called c's Moore neighborhood in cellular automata.
	    # For the sake of simplicity, and since it is the most common way
	    # of implementing these algorithms on a nonweighted graph, diagonal
	    # movement is disallowed - so the algorithm can only move to cells 2, 4, 5, and 7.
	    c2p = (c.rect.left, c.rect.top - Config.NODESIZE[1])
	    c4p = (c.rect.left - Config.NODESIZE[0], c.rect.top)
	    c5p = (c.rect.left + Config.NODESIZE[0], c.rect.top)
	    c7p = (c.rect.left, c.rect.top + Config.NODESIZE[1])	
	    
	    for s in (c2p, c4p, c5p, c7p):
		
		if not s in self.rPos2node.keys():
		    continue
		sN = self.rPos2node[s]
		if not self.unvisitedNodes.has(sN):
		    continue
		if sN.nodeType == 'barrier':
		    continue
		
		# The node has been visited, so remove it from self.unvisitedNodes.
		# I actually didn't include this line until 11/26/11, and it sped
		# the program up dramatically when it was introduced.
		self.unvisitedNodes.remove(sN)    
		
		# This is a grid, so all adjacent nodes have the same cost.
		# Thus, let's set up a priority queue so we can update multiple
		# nodes with the same costs

		pq.append(sN)
		if sN != self.endNode.sprite:
		    sN.image.fill(Config.OPENNODECOLOR)			    
		sN.parent = c
		
	    if finished: break
	    self.unvisitedNodes.remove(c)
	    
	    if c != self.startNode.sprite:
		c.image.fill(Config.VISITEDNODECOLOR)
	    
	    self.updateGraphics()

	b = time.time()
	if finished:
	    self.reconstructPath()
	self.printFinishedMessages(a, b, finished)
