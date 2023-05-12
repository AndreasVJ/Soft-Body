import pygame
from math import pi, cos, sin
from world import World
from objects import SoftBody, Polygon


WIDTH = 400
HEIGHT = 600

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
world = World(100)

x = 150
y = 400
width = 100
height = 25
angle = pi/4

rectangle = Polygon([[x, y], 
                     [x + width*cos(angle), y + width*sin(angle)], 
                     [x + width*cos(angle) - height*sin(angle), y + width*sin(angle) + height*cos(angle)], 
                     [x - height*sin(angle), y + height*cos(angle)]],
                     (0, 255, 0))

body = SoftBody("body.json", 1, 1)

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
    dt = clock.tick(60) / 1000

    world.apply_gravity(dt)
    world.update_bodies(dt)

    world.draw_static_objects(screen)
    world.draw_bodies(screen)

    x, y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (0, 0, 255), (x, y), 5)
    # print(world.static_objects[0].is_inside(x, y))

    pygame.display.flip()