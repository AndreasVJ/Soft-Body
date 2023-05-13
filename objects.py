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
    

    def is_inside(self, pos) -> bool:
        x, y = pos
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
    

    def get_reflection(self, pos, vel) -> tuple[np.ndarray[float, float], np.ndarray[float, float]]:

        # Not working properly :(

        min_distance = sys.float_info.max
        result = None

        x, y = pos
        if vel[0] == 0:
            vel[0] = 0.0001
        a = vel[1] / vel[0]
        y0 = y - a*x

        for i, p in enumerate(self.points):
            if a == self.a[i]:
                continue
            intersection_x = (self.y0[i] - y0) / (a - self.a[i])
            if min(p[0], self.points[i - 1][0]) <= intersection_x and intersection_x <= max(p[0], self.points[i - 1][0]):
                intersection_y = a*intersection_x + y0
                distance = np.sqrt((intersection_x - x)**2 + (intersection_y - y)**2)
                if distance < min_distance:
                    min_distance = distance
                    direction = np.array([1, np.tan(2*np.arctan(self.a[i]) - np.arctan(a))/vel[0]])
                    result = np.array([intersection_x, intersection_y]), direction / np.sqrt(direction[0]**2 + direction[1]**2) * np.sqrt(vel[0]**2 + vel[1]**2)
        
        return result


class SoftBody:
    def __init__(self, nodes: list[list[float, float]], edges: list[list[int, int]], equilibrium: list[list[float]], m, k) -> None:
        self.nodes = np.array(nodes, dtype=float)
        self.vel = np.array([[0, 0]] * len(self.nodes), dtype=float)
        self.edges = edges
        self.equilibrium = equilibrium

        self.m = m
        self.k = k
    

    def draw(self, screen: pygame.Surface) -> None:
        for edge in self.edges:
            pygame.draw.line(screen, (255, 255, 255), self.nodes[edge[0]], self.nodes[edge[1]], 1)

        for node in self.nodes:
            pygame.draw.circle(screen, (255, 0, 0), node, 3)
    

    def update(self, dt) -> None:
        for i, edge in enumerate(self.edges):
            distance = self.nodes[edge[1]] - self.nodes[edge[0]]
            abs_distance = np.sqrt(distance[0]**2 + distance[1]**2)

            direction = distance / abs_distance
            a = self.k * (abs_distance - self.equilibrium[i]) / self.m

            self.vel[edge[0]] += a*direction*dt
            self.vel[edge[1]] -= a*direction*dt

        for i, p in enumerate(self.nodes):
            p += self.vel[i]*dt


class RectangularSoftBody(SoftBody):
    def __init__(self, x:float, y: float, width: int, height: int, distance: float, m: float, k: float) -> None:
        nodes = []
        edges = []
        equilibrium = []

        for i in range(height):
            for j in range(width):
                nodes.append([x + j*distance, y + i*distance])


        for i in range(height - 1):
            for j in range(width - 1):
                edges.append([i*width + j, i*width + j + 1])
                equilibrium.append(distance)
                
                edges.append([i*width + j, (i + 1)*width + j + 1])
                equilibrium.append(distance*1.41)
                
                edges.append([i*width + j, (i + 1)*width + j])
                equilibrium.append(distance)

                edges.append([(i + 1)*width + j, i*width + j + 1])
                equilibrium.append(distance*1.41)


        for i in range (1, height):
            edges.append([width*i - 1, width*(i + 1) - 1])
            equilibrium.append(distance)
        

        for i in range (width - 1):
            edges.append([width*(height - 1) + i, width*(height - 1) + i + 1])
            equilibrium.append(distance)
        

        super().__init__(nodes, edges, equilibrium, m, k)
