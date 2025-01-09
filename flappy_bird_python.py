import neat.nn.feed_forward
import neat.population
import neat.statistics
import pygame as pg
import time
import os
import random
import neat
import keyboard
pg.font.init()


WIN_WIDTH = 500
WIN_HEIGHT = 800


BIRD_IMAGES = [pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird1.png"))), pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird2.png"))), pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird3.png")))]
BACKGROUND_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bg.png")))
PIPE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "pipe.png")))
GROUND_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "base.png")))

STAT_FONT = pg.font.SysFont("comicsans", 50)

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
    

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pg.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    #function to set height of the PIPES
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    #KEEPS THE PIPES MOVING BY SUBTRACTING THE X POSITION BY THE VELOCITY
    def move(self):
        self.x -= self.VEL

    #DRAWS THE PIPES
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    #Function that uses pygames mask to check for collisions
    def collide(self, bird):
        bird_mask = bird.get_mask()
        bottom_mask = pg.mask.from_surface(self.PIPE_BOTTOM)
        top_mask = pg.mask.from_surface(self.PIPE_TOP)

        #Find the bird to pipe offset
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        #Check for bird and pipe collision using masks
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True
        
        return False


class Base:
    VEL = 5
    WIDTH = GROUND_IMG.get_width()
    IMG = GROUND_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    #Move the ground
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH


    #Draw the ground
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))



    #WINDOW
def draw_window(window, bird, pipes, base, score):
    window.blit(BACKGROUND_IMG, (0, 0))
    #Draw the pipes
    for pipe in pipes:
        pipe.draw(window)
    
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(window)

        

    bird.draw(window)
    pg.display.update()

    

def main(genomes, config):
    nets = []
    ge = []
    birds = []

    for g in genomes:
        net = neat.nn.FeedForwardNetwork(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)



    base = Base(730)
    pipes = [Pipe(600)]
    window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pg.time.Clock()

    score = 0


    run = True
    while run:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False


        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        
        for x, birds in enumerate(bird):
            bird.move()
            ge[x].fitness += 0.1

            #TODO: FINISH THIS
            output = nets[x].activate((bird.y, abs))

        
        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)


                    

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            #check if the pipe is completely off the screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        
        for p in rem:
            pipes.remove(p)


        #Check if Bird has hit the ground
        for bird in birds:
            if bird.y + bird.img.get_height() >= 730:
                for x, bird in enumerate(bird):
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

        base.move()
        draw_window(window, bird, pipes, base, score)

    pg.quit()
    quit()

main()


def run():
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    
    population = neat.population(config)

    #Get stats on each generation
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main(), 50)



if __name__ == "__main__":

    #Path for the file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

