# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 21:08:43 2018

@author: MCA
"""
#main file, 2D platform game

import pygame as pg
import sys
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
    #init game window
        pg.init()
        pg.mixer.init() #mixer modul se stara o zvuk
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        
    def load_data(self):
        #load high score
        self.dir = path.dirname(__file__)
        try:
            with open(path.join(self.dir, HS_FILE), 'r') as f:
                #w = povoleni zapisu, cteni + pripadne vytvori soubor
                try:
                    self.highscore = int(f.read())
                except:
                    self.highscore = 0
        except:
            self.highscore = 0

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group() # prida entity sprite do skupiny
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for i in PLATFORM_LIST:
            p = Platform(*i)
            self.platforms.add(p)
            self.all_sprites.add(p)
        self.run()

    def run(self):
     self.playing = True
     while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #game loop update
       self.all_sprites.update()
        #check if player is falling
       if self.player.vel.y > 0:
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
           self.player.pos.y = hits[0].rect.top + 1
           self.player.vel.y = 0
       #if player reaches top 1/4 of screen
       if self.player.rect.top <= HEIGHT / 4:
           self.player.pos.y += abs(self.player.vel.y)
           for i in self.platforms:
               i.rect.y += abs(self.player.vel.y)
               if i.rect.top >= HEIGHT:
                   i.kill()
                   self.score += 5
       #DIE
       if self.player.rect.bottom > HEIGHT:
           for sprite in self.all_sprites:
               sprite.rect.y -= max(self.player.vel.y, 10) #fce vybere maximum z techto dvou cisel
               if sprite.rect.bottom < 0:
                   sprite.kill()

       if len(self.platforms) == 0:
           self.playing = False


       #spawn new platforms to keep some average number
       while len(self.platforms)<8:
            width = random.randrange(50,100)
            p = Platform(random.randrange(0, WIDTH-width),
                         random.randrange(-75, -30),
                         width, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        #game loop events
     for event in pg.event.get():
            # check for closing window
        if event.type == pg.QUIT:
         if self.playing:
            self.playing = False
            self.running = False
         pg.quit()
         sys.exit()
        if event.type == pg.KEYDOWN:
         if event.key == pg.K_UP:
          self.player.jump()
         if event.key == ord('q'):
            if self.playing:
             self.playing = False
             self.running = False


    def draw(self):
        #game loop draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WHITE, WIDTH/2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text("arrows to move", 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT*2/3)
        self.draw_text("Highscore: " + str(self.highscore), 22, WHITE, WIDTH/2, HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()

    def show_game_over_screen(self):
        if not self.running:
            return #pokud je running false pak ukonci tuto fci
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text("Score: "+ str(self.score), 22, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH/2, HEIGHT*2/3)
        if self.score>self.highscore:
            self.highscore = self.score
            self.draw_text("New highscore!", 22, WHITE, WIDTH/2, HEIGHT/2 + 40)
            with open(path.join(self.dir, HS_FILE), "w") as f:
                f.write(str(self.highscore))
        else:
            self.draw_text("Highscore: " + str(self.highscore), 22, WHITE, WIDTH/2, HEIGHT/2 + 40)
            
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size) #True = anti aliasing
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()

while g.running:
    g.new()
    g.show_game_over_screen()

pg.quit()
g.running = False
sys.exit()
