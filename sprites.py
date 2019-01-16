# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 21:04:30 2018

@author: MCA
"""
from settings import *
import pygame as pg
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    
    def get_image(self, x, y, width, height):
        #grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height)) 
        #vezmeme kus spritesheet - dano x,y,w,h - 
        #a blitneme jej do image na pozici 0,0
        return image
        


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30,40))
        self.game = game
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH/2, HEIGHT/2
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    def jump(self):
        #jump only if standing on platform
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits:
         self.vel.y = -PLAYER_JUMP
        
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        #apply friction
        self.acc.x += self.vel.x*PLAYER_FRICTION
        #eq of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        
        #nekonecna obrazovka
        if self.pos.x > WIDTH:
            self.pos.x= 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        self.rect.midbottom = self.pos
        
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image=  pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    