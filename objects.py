import pygame
import numpy as np
import sys


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
    

    def is_inside(self, x, y) -> bool:
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


class SoftBody:
    def __init__(self, nodes: list[list[float, float]], edge_lists: list[list[int]], m, k) -> None:
        self.nodes = np.array(nodes, dtype=float)
        self.edge_lists = edge_lists
        self.vel = np.array([[0, 0]] * len(self.nodes), dtype=float)

        self.m = m
        self.k = k
    

    def draw(self, screen: pygame.Surface) -> None:
        for i, edges in enumerate(self.edge_lists):
            for edge in edges:
                pygame.draw.line(screen, (255, 255, 255), self.nodes[i], self.nodes[edge], 1)

        for node in self.nodes:
            pygame.draw.circle(screen, (255, 0, 0), node, 3)
    

    def update(self, dt) -> None:
        for i, p in enumerate(self.nodes):
            p += self.vel[i]*dt


class RectangularSoftBody(SoftBody):
    def __init__(self, x:float, y: float, width: int, height: int, distance: float, m: float, k: float) -> None:
        directions = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]

        nodes = []
        edge_lists = []

        for i in range(height):
            for j in range(width):
                nodes.append([x + j*distance, y + i*distance])
                edge_lists.append([])

        for i in range(height):
            for j in range(width):
                for d in directions:
                    pos = [j + d[0], i + d[1]]
                    if 0 <= pos[0] and pos[0] < width and 0 <= pos[1] and pos[1] < height:
                        edge_lists[i*width + j].append(pos[1] * width + pos[0])
        
        super().__init__(nodes, edge_lists, m, k)
