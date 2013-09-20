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

Config.py
"""

## Nodes ##
# EMPTYNODECOLOR (tuple): The color of an empty node, in (R, G, B) format.
#
# BARRIERNODECOLOR (tuple): The color of a barrier node, in (R, G, B) format.
#
# STARTNODECOLOR (tuple): The color of the start node, in (R, G, B) format.
#
# ENDNODECOLOR (tuple): The color of the end node, in (R, G, B) format.
#
# VISITEDNODECOLOR (tuple): The color of a visited node, in (R, G, B) format.
#
# OPENNODECOLOR (tuple): The color of an open node, in (R, G, B) format.
#
# PATHNODECOLOR (tuple): The color of a node in the final path of an algorithm,
# in (R, G, B) format.
#
# PATHNODECOLOR_P (tuple): The color of a node in the final path of a bidirectional
# algorithm in between the start node and intersection point between the two trees,
# in (R, G, B) format.
#
# PATHNODECOLOR_Q (tuple): The color of a node in the final path of a bidirectional
# algorithm in between the end node and intersection point between the two trees, in
# (R, G, B) format.
#
# NODESIZE (tuple): The size of each node, in (width, height) format.
#
# NODECOST (int): The cost to get from one node to an adjacent UDLR node. Doesn't
# affect the outcome of the program, except for the final distance traveled.

EMPTYNODECOLOR = (255, 255, 255) # Default = (255, 255, 255)

BARRIERNODECOLOR = (100, 100, 100) # Default = (100, 100, 100) 

STARTNODECOLOR = (0, 255, 0) # Default = (0, 255, 0)

ENDNODECOLOR = (255, 0, 0) # Default = (255, 0, 0)

VISITEDNODECOLOR = (0, 0, 255) # Default = (0, 0, 255)

OPENNODECOLOR = (0, 200, 50) # Default = (0, 255, 50)

PATHNODECOLOR = (255, 255, 0) # Default = (255, 255, 0)

PATHNODECOLOR_P = (255, 255, 0) # Default = (255, 255, 0)

PATHNODECOLOR_Q = (255, 255, 0) # Default = (255, 255, 0)

NODESIZE = (10, 10) # Default = (10, 10)

NODECOST = 1 # Default = 1

## Display ##
# SCREENSIZE (tuple): The dimensions of the program's window, in (x, y) format.
#
# FULLSCREEN (bool): Whether or not to run the program in fullscreen.
#
# WINDOWTITLE (str): The title displayed in the bar atop the program's window.

SCREENSIZE = (400, 300) # Default = (400, 300)

FULLSCREEN = False # Default = False

WINDOWTITLE = "Pathfinder, Marcus Fedarko" # Default = "Pathfinder, Marcus Fedarko"

## Misc. ##
# FPS (int): The frames per second at which the program runs.
#
# BGCOLOR (tuple): The color of the background behind the nodes, in (R, G, B)
# format. You shouldn't see this unless something goes wrong with the program -
# I recommend keeping this color unique so that you can know if something goes wrong.
#
# GRIDLINECOLOR (tuple): The color of the grid lines, in (R, G, B) format.
#
# SHOWGRIDLINES (bool): Whether or not to show grid lines.

FPS = 60 # Default = 60

BGCOLOR = (0, 0, 0) # Default: (0, 0, 0)

GRIDLINECOLOR = (150, 150, 150) # Default: (150, 150, 150)

SHOWGRIDLINES = True # Default: True
