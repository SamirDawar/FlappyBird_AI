import pygame as pg
import time
import os
import random
import neat

WIN_WIDTH = 500
WIN_HEIGHT = 800


BIRD_IMAGES = [pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird1.png"))), pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird2.png"))), pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird3.png")))]
BACKGROUND_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bg.png")))
PIPE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "pipe.png")))
GROUND_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "base.png")))

class Bird:
    IMGS = BIRD_IMAGES
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]


    def Jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y + self.y


    def move(self):
        self.tick_count += 1

        Displacement = self.velocity * self.tick_count + 1.5*self.tick_count**2

        if Displacement >= 16:
            Displacement = 16
            
        #JUMP
        if Displacement < 0:
            Displacement -= 2

        self.y = self.y + Displacement

        #BIRD TILT
        if Displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.ROTATION_VELOCITY
        else: 
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    
    def draw(self, window):
        self.img_count += 1

         # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        rotated_image = pg.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        return pg.mask.from_surface(self.img)
    

    #WINDOW
def draw_window(window, bird):
    window.blit(BACKGROUND_IMG, (0, 0))
    bird.draw(window)
    pg.display.update()

    

def main():
    bird = Bird(200, 200)
    window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pg.time.Clock()


    run = True
    while run:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False


        bird.move()
        draw_window(window, bird)

    pg.quit()
    quit()

main()
