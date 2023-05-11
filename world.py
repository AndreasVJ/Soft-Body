import pygame
import sys


class Polygon:
    def __init__(self, points: list[list[float, float]], color) -> None:
        self.points = points
        self.color = color

        self.min_x = sys.float_info.max
        self.max_x = sys.float_info.min
        self.min_y = sys.float_info.max
        self.max_y = sys.float_info.min

        for p in points:
            self.min_x = min(self.min_x, p[0])
            self.max_x = max(self.max_x, p[0])
            self.min_y = min(self.min_y, p[1])
            self.max_y = max(self.max_y, p[1])
    

    def draw(self, screen) -> None:
        pygame.draw.polygon(screen, self.color, self.points)
    

    def is_inside(self, x, y):
        count = 0
        if self.min_x < x and x < self.max_x and self.min_y < y and y < self.max_y:
            for i in range(len(self.points)):
                if min(self.points[i][1], self.points[i - 1][1]) < y and y < max(self.points[i][1], self.points[i - 1][1]):
                    if x > max(self.points[i][0], self.points[i - 1][0]):
                        count += 1
                    elif x > min(self.points[i][0], self.points[i - 1][0]):
                        a = (self.points[i][1] - self.points[i - 1][1]) / (self.points[i][0] - self.points[i - 1][0])
                        y0 = self.points[i][1] - a*self.points[i][0]
                        over = y > a*x + y0
                        if a > 0:
                            if not over:
                                count += 1
                        else:
                            if over:
                                count += 1
        return count%2 == 1
    

    # def get_closest_point(self, x, y) -> tuple[float, float]:




class World:
    def __init__(self, g) -> None:
        self.g = g
        self.objects: list[Polygon] = []
    
    def add_rectangle(self, points: list[list[float, float]], color) -> None:
        self.objects.append(Polygon(points, color))

    def draw_rectangles(self, screen: pygame.Surface) -> None:
        for obj in self.objects:
            obj.draw(screen)