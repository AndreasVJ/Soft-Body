import pygame
from soft_body import SoftBody
from world import World
from math import pi


WIDTH = 600
HEIGHT = 900

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

world = World(9.81)

world.add_rectangle([[150, 500], [250, 500], [250, 525], [150, 525]], (0, 255, 0))

body = SoftBody("body.json", world, 1, 1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_ESCAPE:
                    exit()
    
    dt = clock.tick(60) / 1000

    screen.fill((0, 0, 0))

    body.update(dt)
    world.draw_rectangles(screen)
    body.draw(screen)

    pygame.display.flip()