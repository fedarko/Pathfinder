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

Node.py
"""

import Config

import pygame
from pygame.locals import *

class Node(pygame.sprite.Sprite):
    """A tile in a course."""
    
    def __init__(self, pos, nodeType):
        """Initializes the node."""
        
        super(Node, self).__init__()

	self.nodeType = nodeType
        
	self.image = pygame.Surface(Config.NODESIZE)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.assignColor()

    def assignColor(self):
	"""Assigns the node's color based on its type, and
	raises an error if the type is invalid."""
	
	if self.nodeType == 'barrier':
	    self.image.fill(Config.BARRIERNODECOLOR)
	elif self.nodeType == 'start':
	    self.image.fill(Config.STARTNODECOLOR)
	elif self.nodeType == 'end':
	    self.image.fill(Config.ENDNODECOLOR)
	elif self.nodeType == 'empty':
	    self.image.fill(Config.EMPTYNODECOLOR)
	else:
	    raise ValueError, "Inappropriate node type"
