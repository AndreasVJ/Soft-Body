import pygame
from math import pi, cos, sin
from world import World
from objects import Polygon, RectangularSoftBody

FPS = 60
WIDTH = 800
HEIGHT = 800

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
world = World(100)

x = 50
y = 300
width = 350
height = 25
angle = pi/4

rectangle = Polygon([[x, y], 
                     [x + width*cos(angle), y + width*sin(angle)], 
                     [x + width*cos(angle) - height*sin(angle), y + width*sin(angle) + height*cos(angle)],
                     [x - height*sin(angle), y + height*cos(angle)]],
                     (0, 255, 0))


body = RectangularSoftBody(100, 100, 6, 4, 20, 1, 1000)

world.add_static_object(rectangle)
world.add_body(body)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_ESCAPE:
                    exit()
    
    screen.fill((0, 0, 0))
    dt = clock.tick(FPS) / 1000


    world.apply_gravity(dt)
    world.update_bodies(dt)
    world.handle_collisions()

    world.draw_static_objects(screen)
    world.draw_bodies(screen)

    pygame.display.flip()