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

Main.py
"""

import Config
import GraphicsManager
import Node

import pygame
from pygame.locals import *

class Main(object):
    """The class that starts up and maintains the most basic
    level of the program's processes."""
    
    def __init__(self):
	"""Initializes pygame and the display, and enters the
	mainloop."""
	
	print "============"
	print "Initializing pygame..."
	
	pygame.init()
	pygame.display.set_caption(Config.WINDOWTITLE)
	
        print "Creating graphics..."
        self.g_manager = GraphicsManager.GraphicsManager()  
        self.mainloop()
        
    def mainloop(self):
	"""Manages the program by checking for input and updating the graphics."""
	
	print "Program successfully started!"
	
	clock = pygame.time.Clock()
	toDraw = 'empty'
	mouseDown = False
        running = True
        while running:
            clock.tick(Config.FPS)
            for e in pygame.event.get():

                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
		    print "Quitting the program..."
		    print "============"		    
                    running = False
                
                if e.type == MOUSEBUTTONDOWN:
		    left, mid, right = pygame.mouse.get_pressed()
		    if left:
			toDraw = 'barrier'
		    if right:
			toDraw = 'empty'
		    mouseDown = True
		    
		if e.type == MOUSEBUTTONUP:
		    mouseDown = False
		    
		if e.type == KEYDOWN:
		    
		    if e.key == K_z:			
			self.g_manager.n_manager.addNode(pygame.mouse.get_pos(), 'start')
		    elif e.key == K_x:
			self.g_manager.n_manager.addNode(pygame.mouse.get_pos(), 'end')
			
		    elif e.key == K_q:
			# If the left ctrl key modifier is pressed, clear all of the
			# nodes. Otherwise, just clear blue visited ones
			mods = pygame.key.get_mods()
			# This uses the bitwise AND operator to see if the left ctrl
			# key is being pressed.
			if KMOD_LCTRL & mods:
			    self.g_manager.clearAll()
			else:
			    self.g_manager.clearVisited()
		
		    elif e.key == K_SPACE:
			self.g_manager.n_manager.writeLevel()
			
		    elif e.key in (K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9):
			self.g_manager.n_manager.loadLevel(int(e.key) - 48)
		
		    elif e.key in (K_F1, K_F2, K_F3, K_F4, K_F5, K_F6):
			self.g_manager.clearVisited()
			self.g_manager.n_manager.a_manager.runAlgorithm(e.key, self.g_manager.bg, \
			self.g_manager.screen, self.g_manager.n_manager.rPos2node)
		
	    self.g_manager.update()
	    # Add nodes if the mouse is down. Using a flag variable allows for dragging the mouse to
	    # draw multiple nodes at once
	    if mouseDown:
		self.g_manager.n_manager.addNode(pygame.mouse.get_pos(), toDraw)	
