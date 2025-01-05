import pygame as pg
import time
import os
import random
import neat

WIN_WIDTH = 600
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
            Displacement = Displacement/abs(Displacement) * 16
            