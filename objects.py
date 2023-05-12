import pygame
import numpy as np
import json
import sys
from pathlib import Path


class SoftBody:
    def __init__(self, path, m, k) -> None:
        with open(Path(__file__).parent / path, "r") as file:
            data = json.load(file)

            self.point = np.array(data["nodes"], dtype=float)
            self.point_edges = data["edges"]

            self.vel = np.array([[0, 0]] * len(self.point), dtype=float)

        self.m = m
        self.k = k
    

    def draw(self, screen: pygame.Surface) -> None:
        for i, edges in enumerate(self.point_edges):
            for edge in edges:
                pygame.draw.line(screen, (255, 255, 255), self.point[i], self.point[edge], 2)

        for point in self.point:
            pygame.draw.circle(screen, (255, 0, 0), point, 5)
    

    def update(self, dt):
        for i, p in enumerate(self.point):
            p += self.vel[i]*dt


class Polygon:
    def __init__(self, points: list[list[float, float]], color: tuple[int, int, int]) -> None:
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
        
        self.a = []
        self.y0 = []
        for i, p in enumerate(self.points):
            self.a.append((p[1] - self.points[i - 1][1]) / (p[0] - self.points[i - 1][0]))
            self.y0.append(p[1] - self.a[i]*p[0])
    

    def draw(self, screen) -> None:
        pygame.draw.polygon(screen, self.color, self.points)
    

    def is_inside(self, x, y):
        count = 0
        if self.min_x < x and x < self.max_x and self.min_y < y and y < self.max_y:
            for i, p in enumerate(self.points):
                if min(p[1], self.points[i - 1][1]) < y and y < max(p[1], self.points[i - 1][1]):
                    if x > max(p[0], self.points[i - 1][0]):
                        count += 1
                    elif x > min(p[0], self.points[i - 1][0]):
                        over = y > self.a[i]*x + self.y0[i]
                        if self.a[i] > 0:
                            if not over:
                                count += 1
                        else:
                            if over:
                                count += 1
        return count%2 == 1
    

    # def get_closest_point(self, x, y) -> tuple[tuple[float, float], tuple[float, float]]:
    #     min_distance = sys.float_info.max

    #     for i, p in enumerate(self.points):