import pygame
import random
import math

from meteorite import Meteorite


class Debris(pygame.sprite.Sprite):
    debris_group: pygame.sprite.Group = pygame.sprite.Group()

    def __init__(self, pos: pygame.Vector2, direction: float, speed: float) -> None:
        super().__init__()

        self.position: pygame.Vector2 = pos
        self.direction: float = direction
        self.velocity: float = speed

        self.rotation_speed: float = 0.1
        self.rotation: float = 0

    def update(self, *args, **kwargs) -> None:
        screen: pygame.Surface = kwargs["screen"]

        self.rotate()
        self.move()
        self.check_outside(screen.get_size())

        self.draw(screen)

    def draw(self, screen: pygame.Surface) -> None:
        # not permanent, just for testing
        pygame.draw.circle(screen, "yellow", self.position, 10)

    def rotate(self) -> None:
        self.rotation += self.rotation_speed

    def move(self) -> None:
        self.position += pygame.Vector2(0, 1).rotate(-self.direction) * self.velocity

    def check_outside(self, screen_resolution: tuple[int, int]) -> None:
        if self.position.x < -20 or self.position.x > screen_resolution[0] + 20 or \
                self.position.y < -20 or self.position.y > screen_resolution[1] + 20:
            self.kill()

    @staticmethod
    def create_random(screen_resolution: tuple[int, int]) -> None:
        position: pygame.Vector2 = Meteorite.generate_point_outside_screen(screen_resolution, 10)
        direction: float = Meteorite.create_random_direction(screen_resolution, position)
        speed: float = random.random() * 2 + 1

        Debris.debris_group.add(Debris(position, direction, speed))
