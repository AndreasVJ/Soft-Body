import pygame
from objects import SoftBody, Polygon


class World:
    def __init__(self, g: float) -> None:
        self.g = g
        self.static_objects: list[Polygon] = []
        self.bodies: list[SoftBody] = []
    

    def add_static_object(self, object: Polygon) -> None:
        self.static_objects.append(object)
    

    def add_body(self, body: SoftBody) -> None:
        self.bodies.append(body)


    def draw_static_objects(self, screen: pygame.Surface) -> None:
        for obj in self.static_objects:
            obj.draw(screen)
    

    def draw_bodies(self, screen: pygame.Surface) -> None:
        for body in self.bodies:
            body.draw(screen)
    

    def apply_gravity(self, dt) -> None:
        for body in self.bodies:
            for v in body.vel:
                v[1] += self.g * dt
    

    def update_bodies(self, dt) -> None:
        for body in self.bodies:
            for i, n in enumerate(body.nodes):
                n += body.vel[i] * dt