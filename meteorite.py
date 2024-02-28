import math
import random

import pygame


class Meteorite:
    meteorites: list["Meteorite"] = []

    def __init__(self, pos: pygame.Vector2, direction: float, speed: float) -> None:
        self.position: pygame.Vector2 = pos
        self.direction: float = direction
        self.velocity: float = speed

        self.rotation_speed: float = 0.1
        self.rotation: float = 0

        self.image: pygame.Surface = pygame.image.load("./img/meteorite/placeholder.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (492 // 2, 507 // 2))

    def update(self) -> None:
        self.rotate()
        self.move()

    def move(self) -> None:
        self.position += pygame.Vector2(
            math.sin(math.radians(self.direction)),
            math.cos(math.radians(self.direction))
        ) * self.velocity

    def rotate(self) -> None:
        self.rotation += self.rotation_speed
        self.rotation %= 360

    def draw(self, screen: pygame.Surface) -> None:
        rotated_image: pygame.Surface = pygame.transform.rotate(self.image, self.rotation)
        rotated_rect: pygame.Rect = rotated_image.get_rect(center=self.image.get_rect(center=self.position).center)

        screen.blit(rotated_image, rotated_rect.topleft)

    @staticmethod
    def create_random() -> None:
        position: pygame.Vector2 = pygame.Vector2(50, 50)
        direction: float = random.randrange(0, 360)
        speed: float = 1

        Meteorite.meteorites.append(Meteorite(position, direction, speed))

    @staticmethod
    def update_meteorites(screen: pygame.Surface) -> None:
        for meteorite in Meteorite.meteorites:
            meteorite.update()
            meteorite.draw(screen)


