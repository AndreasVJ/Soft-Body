import pygame
import numpy as np
import json
from pathlib import Path
from world import World


class SoftBody:
    def __init__(self, path, world: World, m, k) -> None:
        with open(Path(__file__).parent / path, "r") as file:
            data = json.load(file)

            self.point = np.array(data["nodes"], dtype=float)
            self.point_edges = data["edges"]

            self.vel = np.array([[0, 0]] * len(self.point), dtype=float)

        self.world = world
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
            a = np.array([0, self.world.g])
            self.vel[i] += a
            p += self.vel[i]*dt