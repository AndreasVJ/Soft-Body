import pygame
from math import cos, sin


class Polygon:
    def __init__(self, points: list[list[float, float]], color) -> None:
        self.points = points
        self.color = color
    

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)


class World:
    def __init__(self, g) -> None:
        self.g = g
        self.objects: list[Polygon] = []
    
    def add_rectangle(self, points: list[list[float, float]], color):
        self.objects.append(Polygon(points, color))

    def draw_rectangles(self, screen: pygame.Surface):
        for obj in self.objects:
            obj.draw(screen)