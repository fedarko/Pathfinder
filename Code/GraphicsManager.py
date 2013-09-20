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

GraphicsManager.py
"""

import Config
import NodeManager

import pygame
from pygame.locals import *

class GraphicsManager(object):
    """Manages the graphics of the program."""
    
    def __init__(self):
        """Creates the screen, background, and a group of nodes."""
        
	if Config.FULLSCREEN:
            self.screen = pygame.display.set_mode(Config.SCREENSIZE, FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(Config.SCREENSIZE)
            
        self.bg = pygame.Surface(Config.SCREENSIZE)
        
        if Config.SHOWGRIDLINES:
	    self.addGridLines()        
	else:
	    # Since self.lines is passed as an argument, it needs to exist, regardless
	    # of whether we want grid lines or not. If not, then it just will be an empty
	    # group.
	    self.lines = pygame.sprite.RenderPlain()
	    
        self.n_manager = NodeManager.NodeManager(self.screen, self.lines)         
	
    def update(self):
	"""Draws nodes to the background, blits the background
	to the screen, and updates the display."""

        self.bg.fill(Config.BGCOLOR)   
        
        self.n_manager.emptyNodes.draw(self.bg)
        self.n_manager.barrierNodes.draw(self.bg)
        self.n_manager.startNode.draw(self.bg)
        self.n_manager.endNode.draw(self.bg)
        self.lines.draw(self.bg)
        
        self.screen.blit(self.bg, (0, 0))
        pygame.display.flip()

    def addGridLines(self):
	"""Adds horizontal and vertical grid lines."""
	
	self.lines = pygame.sprite.RenderPlain()
	
	# Vertical lines
	for x in range(1, Config.SCREENSIZE[0] / Config.NODESIZE[0]):
	    line = pygame.sprite.Sprite()
	    line.rect = pygame.Rect(x * Config.NODESIZE[0], 0, 1, Config.SCREENSIZE[1])
	    line.image = pygame.Surface((1, Config.SCREENSIZE[1]))
	    line.image.fill(Config.GRIDLINECOLOR)
	    self.lines.add(line)
	    
	# Horizontal lines
	for y in range(1, Config.SCREENSIZE[1] / Config.NODESIZE[1]):
	    line = pygame.sprite.Sprite()
	    line.rect = pygame.Rect(0, y * Config.NODESIZE[1], Config.SCREENSIZE[0], 1)
	    line.image = pygame.Surface((Config.SCREENSIZE[0], 1))
	    line.image.fill(Config.GRIDLINECOLOR)
	    self.lines.add(line)
        
    def clearAll(self):
	"""Clears all of the nodes to the empty state, including calling
	self.clearVisited()."""
	
	print "----"
	print "Clearing all nodes to empty state and color..."
	
	for g in (self.n_manager.emptyNodes, self.n_manager.barrierNodes, self.n_manager.startNode, self.n_manager.endNode):
	    for n in g:
		self.n_manager.addNode(n.rect.topleft, 'empty')
		n.kill()
		
	print "Finished clearing all nodes."
	
    def clearVisited(self):
	"""Clears all of the empty nodes to the default unvisited node color and state."""
	
	print "----"	
	print "Clearing visited nodes to empty state and color..."
	
	for n in self.n_manager.emptyNodes:
	    self.n_manager.addNode(n.rect.topleft, 'empty')
	    n.kill()
	    
	print "Finished clearing visited nodes."
	    
