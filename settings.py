# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 21:04:18 2018

@author: MCA
"""
# game options/settings
TITLE = "2D platformer"
WIDTH = 600
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'

HS_FILE = "high_score.txt"

#player property section
PLAYER_FRICTION = -0.12
PLAYER_ACC = 0.5
PLAYER_GRAV = 0.8
PLAYER_JUMP = 25


#starting platforms (X, Y, WIDTH, THICKNESS)
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH /2 - 50, HEIGHT * 3/4, 100, 20),
                 (120, HEIGHT*0.5, 100, 20),
                 (300, 300, 30, 30),
                 (400, 200, 100, 40)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 140, 140)
BGCOLOR = LIGHTBLUE
