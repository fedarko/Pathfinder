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

NodeManager.py
"""

import Config
import Node
import AlgorithmManager

import pygame
from pygame.locals import *

class NodeManager(object):
    """Manages nodes and node groups."""

    def __init__(self, screen, gridlines):
	"""Creates the node groups and calls buildEmptyNodes()."""
	
	self.screen = screen

	self.emptyNodes = pygame.sprite.RenderPlain()
        self.barrierNodes = pygame.sprite.RenderPlain()
        self.startNode = pygame.sprite.GroupSingle()
        self.endNode = pygame.sprite.GroupSingle()

	self.a_manager = AlgorithmManager.AlgorithmManager(gridlines, self.emptyNodes, \
	self.barrierNodes, self.startNode, self.endNode)

	self.rPos2node = {}

	self.buildEmptyNodes()

    def addNode(self, pos, nodeType):
	"""Adds a node to self.nodes."""

	# If a node occupies the same space as the new node, kill the old node
	rPos = self.roundPos(pos)	
	
	if rPos in self.rPos2node.keys():
	    self.rPos2node[rPos].kill() 
	
	# If nodeType is invalid, then Node.assignColor() will catch the error
	node = Node.Node(rPos, nodeType)
	node.rect.clamp_ip(self.screen.get_rect())
	
	if nodeType == 'start':
	    if self.startNode.sprite:
		self.addNode(self.startNode.sprite.rect.topleft, 'empty')
	    self.startNode.add(node)
	    
	elif nodeType == 'end':
	    if self.endNode.sprite:
		self.addNode(self.endNode.sprite.rect.topleft, 'empty')
	    self.endNode.add(node)
	    
	elif nodeType == 'barrier':
	    self.barrierNodes.add(node)
	elif nodeType == 'empty':
	    self.emptyNodes.add(node)
	    
	self.rPos2node[rPos] = node
	
    def roundPos(self, pos):
	"""Rounds a given (x, y) position up or down to the nearest tens digit."""
	
	rPos = [0, 0]
	posRDigits = (pos[0] % 10, pos[1] % 10)

	for i in range(2):		
	    if posRDigits[i] >= Config.NODESIZE[i] / 2:
		rPos[i] = pos[i] + (Config.NODESIZE[i] - posRDigits[i])
	    else:
		rPos[i] = pos[i] - posRDigits[i]

	# Lists aren't hashable, which is why a tuple is returned here
	rPosT = (rPos[0], rPos[1])

	return rPosT

    def buildEmptyNodes(self):
	"""Adds empty nodes to exactly cover the screen."""
	
	x = 0
	y = 0	
	while x < Config.SCREENSIZE[0]:
	    while y < Config.SCREENSIZE[1]:
		# The node is created here instead of calling addNode() because it's
		# faster this way.
		node = Node.Node((x, y), 'empty')
		self.emptyNodes.add(node)
		self.rPos2node[(x, y)] = node
		y += Config.NODESIZE[1]
	    x += Config.NODESIZE[0]
	    y = 0
	    
    def writeLevel(self):
	"""Writes a level list to a text file that can
	be loaded into the program."""
	
	print "----"
	print "Writing on-screen level to Levels.txt..."
	level = self.convertLevel()
	doTruncate = False
	with open("Levels.txt", 'r') as f:
	    
	    #If the upper limit of levels (10) in Levels.txt has
	    #been reached, truncate the last level
	    levelCount = 0
	    charCount = 0
	    lines = f.readlines()
	    for s in lines:
		charCount += len(s)
		if "{" in s:
		    levelCount += 1
		    if levelCount >= 10:
			doTruncate = True
			break
	
	with open("Levels.txt", 'a') as f:
	    if doTruncate:
		# charCount gets subtracted by 3 to account for
		# lheaders (level-headers)
		f.truncate(charCount - 3)
		print "Truncating levels #9 and up, maximum level amount exceeded."
		levelCount = 9
	    lheader = "%d{\n" % (levelCount)
	    f.write(lheader)
	    for l in level:
		f.write("[")
		f.write(l)
		f.write("]\n")
	    f.write("}\n")
	print "Writing of level #%d to Levels.txt complete!" % (levelCount)
	
    def loadLevel(self, levelNum):
	"""Loads a given level list from Levels.txt onto the screen."""
	
	print "----"
	print "Loading level #%d..." % (levelNum)
	
	with open("Levels.txt", 'r') as f:
	    
	    lines = f.readlines()
	    lineCount = 0
	    foundStart = False
	    startLineNum = 0
	    
	    for l in lines:
		if str(levelNum) in l:
		    startLineNum = lineCount
		    foundStart = True
		if foundStart and "}" in l:
		    break
		lineCount += 1
		
	if not foundStart:
	    print "Cannot load level #%d - level does not exist." % (levelNum)
	else:
	    # First, clear out all the current nodes
	    self.barrierNodes.empty()
	    self.emptyNodes.empty()
	    self.startNode.empty()
	    self.endNode.empty()
	    self.buildEmptyNodes()
	    
	    x = 0
	    y = 0
	    # isNode prevents the brackets [] and other non-node characters from
	    # being counted as nodes.
	    isNode = False
	    for row in lines[(startLineNum + 1):lineCount]:
		for col in row:
		    if col == "#":
			self.addNode((x, y), 'barrier')
			isNode = True
		    elif col == "S":
			self.addNode((x, y), 'start')
			isNode = True
		    elif col == "E":
			self.addNode((x, y), 'end')
			isNode = True
		    elif col == " ":
			isNode = True
			
		    if isNode:
			x += Config.NODESIZE[0]
		    isNode = False
		    
		y += Config.NODESIZE[1]
		x = 0	
		
	    print "Loading of level #%d complete!" % (levelNum)
	    
    def convertLevel(self):
	"""Converts the nodes on the screen into a level list."""
	
	x = 0
	y = 0
	level = [""]
	
	# Fill the level with blank spaces
	while y < (Config.SCREENSIZE[1] / 10):
	    while x < (Config.SCREENSIZE[0] / 10):
		level[y] += ' '
		x += 1
	    level.append("")
	    y += 1
	    x = 0
	level.pop(len(level) - 1)
	
	# Add all of the nodes to the level
	for n in self.rPos2node:
	    node = self.rPos2node[n]
	    level[node.rect.top / 10] = self.swapNode(node, level[node.rect.top / 10])
	    
	# For testing: prints out the contents of the level
	#for l in level:
	    #print "[%s]" % (l)
	    
	return level

    def swapNode(self, node, s):
	"""Swaps in a node into a string in a level list."""
	
	if node.nodeType == 'barrier':
	    nodeSymbol = "#"
	elif node.nodeType == 'start':
	    nodeSymbol = "S"
	elif node.nodeType == 'end':
	    nodeSymbol = "E"
	else:
	    nodeSymbol = " "
	
	pos = node.rect.left / 10
	return s[:pos] + nodeSymbol + s[(pos + 1):]
