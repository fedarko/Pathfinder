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

Algorithm.py
"""

import Config

import pygame
from pygame.locals import *

class Algorithm(object):
    """A superclass for all of the pathfinding algorithm
    classes in the program."""
	
    def __init__(self, algName, bg, screen, rPos2node, gridlines, emptyNodes, barrierNodes, startNode, endNode):
	"""Creates copies of the node groups and initializes a few attributes."""
	
	self.algName = algName
	
	self.bg = bg
	self.screen = screen
	
	self.rPos2node = {}
	
	self.lines = gridlines
	
	# These groups are aliased; however, this doesn't matter, because if the algorithm
	# is being run, then the nodes won't be changeable until the algorithm is finished
	# running
	self.emptyNodes = emptyNodes
	self.barrierNodes = barrierNodes
	self.startNode = startNode
	self.endNode = endNode
	
    def run(self):
	"""Runs the algorithm on the current groups of nodes. This superclass' implementation
	of this method is very basic, to allow for extensability in Algorithm's subclasses."""
	
	print "----"
	print "Running %s algorithm..." % (self.algName)
	# The lines that determine the time since the epoch and mark nodes, while
	# universal among all the algorithms, are not included here because I'd
	# rather have a tad more verbose code and accuracy in results than
	# including the lines here and having the scope possibly impact the results.
	
    def markNode(self, collection, *nodes):
	"""Puts any number of nodes in a collection."""
	
	for n in nodes:
	    if type(collection) == dict:
		collection[n.rect.topleft] = n
	    elif type(collection) == pygame.sprite.RenderPlain:
		collection.add(n)

    def reconstructPath(self, bidirectional=False):
	"""Reconstructs the shortest path (or at least almost shortest path) from the end
	node to the start node."""
	
	if not bidirectional:	  
	    print "Reconstructing path..."
	    
	    pathLength = 0  
	    
	    p = self.endNode.sprite.parent
	    while p != self.startNode.sprite:
		p.image.fill(Config.PATHNODECOLOR)
		p = p.parent	
		pathLength += 1
		
	    print "Finished reconstructing path. Path length: %d" % (pathLength)
	else:
	    # Reconstruct the path for bidirectional algorithms
	    print "Reconstructing path..."
	    
	    pathLength = 0
	    foundPath = False
	    # start and end nodes are tested because in some cases, they are
	    # the intersection point. This doesn't happen that often, but if it does
	    # and it isn't accounted for, then a path isn't generated.
	    nodeGroups = (self.emptyNodes, self.startNode, self.endNode)
	    
	    for g in nodeGroups:
		for n in g:
		    if hasattr(n, 'intPt'):
			p = n # CollPt to Start Node
			q = n # CollPt to End Node
			
			# Final path will look something like this:
			# S pppppp I qqqqqq E
			# Where S is the start node, p and q are the path, I is the
			# intersection point, and E is end node
			
			while p != self.startNode.sprite:
			    if p != self.endNode.sprite:
				p.image.fill(Config.PATHNODECOLOR_P)
			    p = p.parent
			    pathLength += 1
			    
			while q != self.endNode.sprite:
			    if q != self.startNode.sprite:
				q.image.fill(Config.PATHNODECOLOR_Q)
			    q = q.parent2
			    pathLength += 1
			    
			#Subtract 1 from path length to account for overlap between
			#the two trees at the collision point
			pathLength -= 1
			foundPath = True
			break
		if foundPath:
		    break
	    print "Finished reconstructing path. Path length: %d" % (pathLength)
	    
    def updateGraphics(self):
	"""Quickly updates the graphics while an algorithm is running, in lieu of
	the Graphics Manager."""
	
	self.bg.fill(Config.BGCOLOR)
	    
	self.emptyNodes.draw(self.bg)
	self.barrierNodes.draw(self.bg)
	self.startNode.draw(self.bg)
	self.endNode.draw(self.bg)
	
	self.lines.draw(self.bg)
    
	self.screen.blit(self.bg, (0, 0))
	pygame.display.flip()
	
    def printFinishedMessages(self, startTime, endTime, hugeSuccess=True):
	"""Prints the messages at the end of running an algorithm."""
	
	print "Finished at %fs" % (endTime)
	
	if not hugeSuccess:
	    print "No path can be created."
	else:
	    print "A path was found."

	print "Algorithm took %f seconds to run." % (endTime - startTime)	
