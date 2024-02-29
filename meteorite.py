import math
import random

import pygame


class Meteorite:
    meteorites: list["Meteorite"] = []

    def __init__(self, pos: pygame.Vector2, direction: float, speed: float, radius: int) -> None:
        self.position: pygame.Vector2 = pos
        self.direction: float = direction
        self.velocity: float = speed

        self.rotation_speed: float = 0.1
        self.rotation: float = 0

        self.image: pygame.Surface = pygame.image.load("./img/meteorite/placeholder.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (radius, radius))

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
    def create_random(screen_resolution: tuple[int, int]) -> None:
        radius: int = random.randrange(100, 300)
        position: pygame.Vector2 = Meteorite.generate_point_outside_screen(screen_resolution, radius)
        direction: float = Meteorite.create_random_direction(screen_resolution, position)
        speed: float = 1

        Meteorite.meteorites.append(Meteorite(position, direction, speed, radius))

    @staticmethod
    def create_random_direction(screen_resolution: tuple[int, int], position: pygame.Vector2) -> float:
        point: pygame.Vector2 = pygame.Vector2(random.randint(50, screen_resolution[0] - 50),
                                               random.randint(50, screen_resolution[1] - 50))
        c: float = point.distance_to(position)

        print(point.x, c)

        return math.degrees(math.asin((point.x - position.x) / c))

    @staticmethod
    def generate_point_outside_screen(screen_resolution: tuple[int, int], meteorite_width: int):
        bounding_width: int = screen_resolution[0] + meteorite_width * 2
        bounding_height: int = screen_resolution[1] + meteorite_width * 2

        position: pygame.Vector2 = pygame.Vector2(0, 0)

        p = random.randint(0, (bounding_width + bounding_height) * 2)
        if p < (bounding_width + bounding_height):
            if p < bounding_width:
                position.x = p
                position.y = 0
            else:
                position.x = bounding_width
                position.y = p - bounding_width
        else:
            p = p - (bounding_width + bounding_height)
            if p < bounding_width:
                position.x = bounding_width - p
                position.y = bounding_height
            else:
                position.x = 0
                position.y = bounding_height - (p - bounding_width)

        position.x += 50 - meteorite_width
        position.y += 50 - meteorite_width

        return position

    @staticmethod
    def update_meteorites(screen: pygame.Surface) -> None:
        for meteorite in Meteorite.meteorites:
            meteorite.update()
            meteorite.draw(screen)
