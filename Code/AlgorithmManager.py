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

AlgorithmManager.py
"""

import Config
import Node
import AStar
import BiAStar
import Dijkstras
import BiDijkstras

import pygame
from pygame.locals import *

class AlgorithmManager(object):
    """Manages the game's pathfinding algorithms. The 6 types of algorithms
    implemented for the science fair project are:
    
    -A* Search Algorithm (Manhattan and Euclidean)
    -Bidirectional A* Search (Manhattan and Euclidean)
    -Dijkstra's Algorithm
    -Bidirectional Dijkstra's Algorithm
    
    The hypothesis predicts that the average order of them, from fastest to
    slowest, will be:
    
    1. A* Search Algorithm (Manhattan)
    2. Bidirectional A* Search (Manhattan)
    3. A* Search Algorithm (Euclidean)
    4. Bidirectional A* Search Algorithm (Euclidean)
    5. Bidirectional Dijkstra's Algorithm
    6. Dijkstra's Algorithm
    
    The reasons for this are explained in the paper attached to the project.
    """
    
    def __init__(self, gridlines, emptyNodes, barrierNodes, startNode, endNode):
	"""Creates aliased copies of the node groups."""
	
	self.emptyNodes = emptyNodes
	self.barrierNodes = barrierNodes
	self.startNode = startNode
	self.endNode = endNode
	
	self.lines = gridlines
	
    def runAlgorithm(self, key, bg, screen, rPos2node):
	"""Runs an algorithm based on a key pressed."""
	
	self.nodes = self.emptyNodes, self.barrierNodes, self.startNode, self.endNode
	
	valid = True
	
	if len(self.startNode) == 0:
	    print "Cannot run an algorithm - no current start node"
	    valid = False
	    
	if len(self.endNode) == 0:
	    print "Cannot run an algorithm - no current end node"
	    valid = False
	
	if valid:
	    if key == K_F1:
		a = AStar.AStar(bg, screen, rPos2node, self.lines, "Manhattan", *self.nodes)
	    elif key == K_F2:
		a = AStar.AStar(bg, screen, rPos2node, self.lines, "Euclidean", *self.nodes)
	    elif key == K_F3:
		a = BiAStar.BiAStar(bg, screen, rPos2node, self.lines, "Manhattan", *self.nodes)
	    elif key == K_F4:
		a = BiAStar.BiAStar(bg, screen, rPos2node, self.lines, "Euclidean", *self.nodes)
	    elif key == K_F5:
		a = Dijkstras.Dijkstras(bg, screen, rPos2node, self.lines, *self.nodes)
	    elif key == K_F6:
		a = BiDijkstras.BiDijkstras(bg, screen, rPos2node, self.lines, *self.nodes)
	    
	    a.run()
